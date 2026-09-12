#!/usr/bin/env python3
"""Cycle IQ: consecutive G=1 kind is determined by the parent half-run.

On odd n=2m+1, every G=1 pair sits in a half-run image. Parent run-1
gives left/right of a triple; parent run-2 or run-3 gives isolated
pairs. Isolated pairs do not come from run-1; triples do not come from
run-2; n%4==3 triples still come from run-1. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_iq.py --certify
Dump: research/cycle_iq.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_in import g_run_kind
from cycle_ip import g_runs
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IP_JSON = Path(__file__).resolve().parent / "cycle_ip.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def g11_parent(n: int, j: int):
    """(start, r) on m=n//2 for consecutive G=1 at j, else None."""
    if n % 2 == 0 or G(n, j) == 0 or G(n, j + 1) == 0:
        return None
    m = n // 2
    for start, r in g_runs(m):
        lo = 2 * start
        if r == 1 and j in (lo, lo + 1):
            return (start, r)
        if r == 2 and j in (lo, lo + 3):
            return (start, r)
        if r == 3 and j in (lo, lo + 5):
            return (start, r)
    return None


def parent_kind_table() -> dict:
    """Odd n<64: iso iff parent r in {2,3}; left/right iff parent r=1."""
    n_left_r1 = n_right_r1 = n_iso_r2 = n_iso_r3 = 0
    for n in range(1, 64, 2):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            if kind is None:
                continue
            par = g11_parent(n, j)
            if par is None:
                return {"ok": False, "miss": True, "n": n, "j": j}
            _start, r = par
            if kind == "iso":
                if r == 1:
                    return {"ok": False, "iso_r1": True, "n": n, "j": j}
                if r == 2:
                    n_iso_r2 += 1
                elif r == 3:
                    n_iso_r3 += 1
                else:
                    return {"ok": False, "iso_r": True, "n": n, "j": j, "r": r}
            else:
                if r != 1:
                    return {"ok": False, "lr": True, "n": n, "j": j, "r": r}
                if kind == "left":
                    n_left_r1 += 1
                else:
                    n_right_r1 += 1
    ok = (
        n_left_r1 == 141
        and n_right_r1 == 141
        and n_iso_r2 == 140
        and n_iso_r3 == 90
    )
    return {
        "ok": ok,
        "n_left_r1": n_left_r1,
        "n_right_r1": n_right_r1,
        "n_iso_r2": n_iso_r2,
        "n_iso_r3": n_iso_r3,
    }


def _walk_parent(k: int, q: int) -> dict:
    """Parent-run kind on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = 0
    n_left_r1 = n_right_r1 = n_iso_r2 = n_iso_r3 = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                bits[j] = packed
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                if kind is None:
                    continue
                par = g11_parent(n, j)
                if par is None:
                    return {"ok": False, "miss": True, "k": k, "n": n, "j": j}
                _start, r = par
                n_g11 += 1
                if kind == "iso":
                    if r == 1:
                        return {"ok": False, "iso_r1": True, "k": k, "n": n, "j": j}
                    if r == 2:
                        n_iso_r2 += 1
                    elif r == 3:
                        n_iso_r3 += 1
                    else:
                        return {"ok": False, "iso_r": True, "k": k, "n": n, "r": r}
                else:
                    if r != 1:
                        return {"ok": False, "lr": True, "k": k, "n": n, "r": r}
                    if kind == "left":
                        n_left_r1 += 1
                    else:
                        n_right_r1 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left_r1": n_left_r1,
        "n_right_r1": n_right_r1,
        "n_iso_r2": n_iso_r2,
        "n_iso_r3": n_iso_r3,
        "xor_j": xor_j,
    }


def parent_cover() -> dict:
    """Parent-run kind on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = 0
    n_left_r1 = n_right_r1 = n_iso_r2 = n_iso_r3 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_parent(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_g11 += w["n_g11"]
            n_left_r1 += w["n_left_r1"]
            n_right_r1 += w["n_right_r1"]
            n_iso_r2 += w["n_iso_r2"]
            n_iso_r3 += w["n_iso_r3"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_left_r1": w["n_left_r1"],
                "n_right_r1": w["n_right_r1"],
                "n_iso_r2": w["n_iso_r2"],
                "n_iso_r3": w["n_iso_r3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_left_r1 == 2380
        and n_right_r1 == 2380
        and n_iso_r2 == 2339
        and n_iso_r3 == 1478
        and n_left_r1 + n_right_r1 + n_iso_r2 + n_iso_r3 == n_g11
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left_r1": n_left_r1,
        "n_right_r1": n_right_r1,
        "n_iso_r2": n_iso_r2,
        "n_iso_r3": n_iso_r3,
        "rows": rows,
    }


def killed_iso_from_r1() -> dict:
    """Isolated pair comes from parent run-1: G(3) pair at 0 from G(1) run-3."""
    k, s, n, j, p = 0, 3, 3, 0, 10
    par = g11_parent(n, j)
    ok = (
        g_run_kind(n, j) == "iso"
        and par == (0, 3)
        and par[1] != 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "parent": list(par) if par else None,
        "kind": g_run_kind(n, j),
    }


def killed_lr_from_r2() -> dict:
    """Triple left/right comes from parent run-2: G(1) from G(0) run-1."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    par = g11_parent(n, j)
    ok = (
        g_run_kind(n, j) == "left"
        and par == (0, 1)
        and par[1] != 2
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "parent": list(par) if par else None,
        "kind": g_run_kind(n, j),
    }


def killed_n3_triple_from_r2() -> dict:
    """n%4==3 triple comes from parent run-2: G(7) 111 at 6 from G(3) run-1."""
    k, s, n, j, p = 1, 5, 7, 6, 8
    par = g11_parent(n, j)
    ok = (
        n % 4 == 3
        and g_run_kind(n, j) == "left"
        and par == (3, 1)
        and par[1] == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "parent": list(par) if par else None,
        "kind": g_run_kind(n, j),
    }


def prefixes() -> dict:
    ip = json.loads(IP_JSON.read_text())
    ok = (
        ip["checks"]["all_ok"]
        and ip["verdict"]["half_run_dictionary"] == "LEMMA"
        and ip["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g11_parent(1, 0) == (0, 1)
    assert g11_parent(3, 0) == (0, 3)
    assert g11_parent(7, 0) == (0, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = parent_kind_table()
    sc = parent_cover()
    k0 = killed_iso_from_r1()
    k1 = killed_lr_from_r2()
    k2 = killed_n3_triple_from_r2()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "parent_kind_table": {k: rt[k] for k in rt if k != "ok"},
        "parent_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_iso_from_r1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_lr_from_r2": {k: k1[k] for k in k1 if k != "ok"},
        "killed_n3_triple_from_r2": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g11_kind_from_parent_r": True,
            "iso_from_r2_r3": True,
            "covering_parent_kind": True,
            "iso_from_r1": False,
            "lr_from_r2": False,
            "n3_triple_from_r2": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g11_kind_from_parent_r": "LEMMA",
            "iso_from_r2_r3": "LEMMA",
            "covering_parent_kind": "LEMMA",
            "iso_from_r1": "KILLED",
            "lr_from_r2": "KILLED",
            "n3_triple_from_r2": "KILLED",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("parent_kind_table", dump["parent_kind_table"])
    cov = dump["parent_cover"]
    print(
        "parent_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_left_r1",
        cov["n_left_r1"],
        "n_iso_r2",
        cov["n_iso_r2"],
        "n_iso_r3",
        cov["n_iso_r3"],
    )
    print("killed_iso_from_r1", dump["killed_iso_from_r1"])
    print("killed_lr_from_r2", dump["killed_lr_from_r2"])
    print("killed_n3_triple_from_r2", dump["killed_n3_triple_from_r2"])


if __name__ == "__main__":
    main()
