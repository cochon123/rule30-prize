#!/usr/bin/env python3
"""Cycle IR: isolated ones on odd n are the middle 1 of a parent run-3.

A length-3 half-run image is 011010110; the center 1 is isolated.
Every isolated G=1 on odd n<64 (all n%4==3) is that middle bit.
Even n isolated ones are not parent run-3; n%4==1 has no isolated
ones. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_ir.py --certify
Dump: research/cycle_ir.json
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
from cycle_ip import g_runs
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IQ_JSON = Path(__file__).resolve().parent / "cycle_iq.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def isolated_one(n: int, j: int) -> bool:
    """G(n,j)=1 with both neighbors 0."""
    return G(n, j) == 1 and G(n, j - 1) == 0 and G(n, j + 1) == 0


def r3_middle(n: int, j: int) -> bool:
    """Whether j is the isolated 1 in a parent run-3 image."""
    if n % 2 == 0:
        return False
    m = n // 2
    return any(r == 3 and j == 2 * start + 3 for start, r in g_runs(m))


def iso1_table() -> dict:
    """n<64: odd isolated ones are r3 middle; even isolated ones are not."""
    n_odd = n_from = n_even = n_odd_n3 = n_odd_n1 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            if n % 2 == 0:
                n_even += 1
                if r3_middle(n, j):
                    return {"ok": False, "even": True, "n": n, "j": j}
                continue
            n_odd += 1
            if n % 4 == 3:
                n_odd_n3 += 1
            else:
                n_odd_n1 += 1
            if r3_middle(n, j):
                n_from += 1
            else:
                return {"ok": False, "miss": True, "n": n, "j": j}
    ok = (
        n_odd == 45
        and n_from == 45
        and n_even == 416
        and n_odd_n3 == 45
        and n_odd_n1 == 0
    )
    return {
        "ok": ok,
        "n_odd": n_odd,
        "n_from": n_from,
        "n_even": n_even,
        "n_odd_n3": n_odd_n3,
        "n_odd_n1": n_odd_n1,
    }


def _walk_iso1(k: int, q: int) -> dict:
    """Odd-n isolated ones are r3 middle on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso1 = n_from = n_iso1_and = 0
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
            if n % 2 == 1:
                for j, packed in bits.items():
                    if not isolated_one(n, j):
                        continue
                    n_iso1 += 1
                    if not r3_middle(n, j):
                        return {"ok": False, "miss": True, "k": k, "n": n, "j": j}
                    n_from += 1
                    if packed:
                        n_iso1_and += 1
            else:
                for j in bits:
                    if isolated_one(n, j) and r3_middle(n, j):
                        return {"ok": False, "even": True, "k": k, "n": n, "j": j}
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso1": n_iso1,
        "n_from": n_from,
        "n_iso1_and": n_iso1_and,
        "xor_j": xor_j,
    }


def iso1_cover() -> dict:
    """Odd-n isolated ones on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso1 = n_from = n_iso1_and = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_iso1(k, q)
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
            n_iso1 += w["n_iso1"]
            n_from += w["n_from"]
            n_iso1_and += w["n_iso1_and"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso1": w["n_iso1"],
                "n_from": w["n_from"],
                "n_iso1_and": w["n_iso1_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso1 == 741
        and n_from == 741
        and n_iso1_and == 159
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso1": n_iso1,
        "n_from": n_from,
        "n_iso1_and": n_iso1_and,
        "rows": rows,
    }


def killed_odd_not_r3() -> dict:
    """Odd-n isolated 1 is not r3 middle: G(3,3)=1 is the middle of G(1)=111."""
    k, s, n, j, p = 0, 3, 3, 3, 4
    ok = (
        n % 2 == 1
        and isolated_one(n, j)
        and r3_middle(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def killed_even_is_r3() -> dict:
    """Even-n isolated 1 is r3 middle: G(2,0)=1 with no parent."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    ok = (
        n % 2 == 0
        and isolated_one(n, j)
        and not r3_middle(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def killed_n1_iso1() -> dict:
    """n%4==1 has an isolated one: G(1)=111 is a triple."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    ok = (
        n % 4 == 1
        and not isolated_one(n, j)
        and G(n, j) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": [G(n, i) for i in range(0, 3)],
    }


def prefixes() -> dict:
    iq = json.loads(IQ_JSON.read_text())
    ok = (
        iq["checks"]["all_ok"]
        and iq["verdict"]["g11_kind_from_parent_r"] == "LEMMA"
        and iq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert isolated_one(3, 3) and r3_middle(3, 3)
    assert isolated_one(2, 0) and not r3_middle(2, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = iso1_table()
    sc = iso1_cover()
    k0 = killed_odd_not_r3()
    k1 = killed_even_is_r3()
    k2 = killed_n1_iso1()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "iso1_table": {k: rt[k] for k in rt if k != "ok"},
        "iso1_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_odd_not_r3": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_is_r3": {k: k1[k] for k in k1 if k != "ok"},
        "killed_n1_iso1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "odd_iso1_from_r3_mid": True,
            "odd_iso1_only_n3": True,
            "covering_iso1_r3_mid": True,
            "odd_iso1_not_r3": False,
            "even_iso1_is_r3": False,
            "n1_has_iso1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_iso1_from_r3_mid": "LEMMA",
            "odd_iso1_only_n3": "LEMMA",
            "covering_iso1_r3_mid": "LEMMA",
            "odd_iso1_not_r3": "KILLED",
            "even_iso1_is_r3": "KILLED",
            "n1_has_iso1": "KILLED",
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
    print("iso1_table", dump["iso1_table"])
    cov = dump["iso1_cover"]
    print(
        "iso1_cover n_ok",
        cov["n_ok"],
        "n_iso1",
        cov["n_iso1"],
        "n_from",
        cov["n_from"],
        "n_iso1_and",
        cov["n_iso1_and"],
    )
    print("killed_odd_not_r3", dump["killed_odd_not_r3"])
    print("killed_even_is_r3", dump["killed_even_is_r3"])
    print("killed_n1_iso1", dump["killed_n1_iso1"])


if __name__ == "__main__":
    main()
