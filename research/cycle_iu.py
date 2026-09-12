#!/usr/bin/env python3
"""Cycle IU: dual j to 2n-j palindromes core IMAGE_ONES slots.

A core slot (start, r, d) maps to (2m-start-r+1, r, 2r-d) on the
odd core's parent m. Dual preserves r; the center is self-dual of
type (r,d) in {(1,1),(3,3)}; n=0 stays seed. Dual does not change r;
dual start is not 2m-start; dual of even G=1 is not a parent slot.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_iu.py --certify
Dump: research/cycle_iu.json
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
from cycle_is import IMAGE_ONES, g1_slot
from cycle_it import g1_core_slot, odd_core
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IT_JSON = Path(__file__).resolve().parent / "cycle_it.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

WANT_CENTER = {(1, 1): 42, (3, 3): 21}
WANT_COV_PAIR = 9692
WANT_COV_CENTER = 748
WANT_COV_XOR = 3246


def dual_slot(slot: tuple, m: int) -> tuple:
    """IMAGE_ONES dual of (start, r, d) on parent m."""
    start, r, d = slot
    return (2 * m - start - r + 1, r, 2 * r - d)


def dual_core_slot(n: int, j: int):
    """Predicted dual of g1_core_slot(n, j) under j to 2n-j."""
    got = g1_core_slot(n, j)
    if got == "seed" or got is None or got == "bad":
        return got
    core, _v = odd_core(n)
    return dual_slot(got, core // 2)


def _center_key(ctr: dict) -> dict:
    return {f"{r},{d}": ctr[(r, d)] for r, d in sorted(WANT_CENTER)}


def dual_table() -> dict:
    """n<64: dual core slot is dual_slot; center is self-dual."""
    n_g1 = n_hit = n_seed = n_center = 0
    ctr = {k: 0 for k in WANT_CENTER}
    for r, offs in IMAGE_ONES.items():
        for d in offs:
            if 2 * r - d not in offs:
                return {"ok": False, "ones": True, "r": r, "d": d}
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_g1 += 1
            got = g1_core_slot(n, j)
            pred = dual_core_slot(n, j)
            got2 = g1_core_slot(n, 2 * n - j)
            if pred != got2:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "pred": pred,
                    "got2": got2,
                }
            if got == "seed":
                n_seed += 1
                continue
            n_hit += 1
            if pred[1] != got[1]:
                return {"ok": False, "rchg": True, "n": n, "j": j}
            if j == n:
                n_center += 1
                if pred != got:
                    return {"ok": False, "center": True, "n": n, "got": got}
                rd = (got[1], got[2])
                if rd not in ctr:
                    return {"ok": False, "rd": True, "n": n, "got": got}
                ctr[rd] += 1
    ok = (
        n_g1 == 1344
        and n_hit == 1343
        and n_seed == 1
        and n_center == 63
        and ctr == WANT_CENTER
    )
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "n_center": n_center,
        "center": _center_key(ctr),
    }


def _walk_dual(k: int, q: int) -> dict:
    """Dual core slots on covering G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_pair = n_seed = n_center = n_xor = 0
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
                n_ok += 1
                if not G(n, j):
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                bits[j] = (g1_core_slot(n, j), packed)
            for j in range(0, n + 1):
                j2 = 2 * n - j
                if j not in bits or j2 not in bits:
                    continue
                got, a = bits[j]
                got2, b = bits[j2]
                pred = dual_core_slot(n, j)
                if pred != got2:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "pred": pred,
                        "got2": got2,
                    }
                if got == "seed":
                    n_seed += 1
                    continue
                n_pair += 1
                if a != b:
                    n_xor += 1
                if j == n:
                    n_center += 1
                    if pred != got:
                        return {"ok": False, "center": True, "k": k, "n": n}
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_pair": n_pair,
        "n_seed": n_seed,
        "n_center": n_center,
        "n_xor": n_xor,
        "xor_j": xor_j,
    }


def dual_cover() -> dict:
    """Dual slots on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_pair = n_seed = n_center = n_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dual(k, q)
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
            n_pair += w["n_pair"]
            n_seed += w["n_seed"]
            n_center += w["n_center"]
            n_xor += w["n_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_pair": w["n_pair"],
                "n_seed": w["n_seed"],
                "n_center": w["n_center"],
                "n_xor": w["n_xor"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_pair == WANT_COV_PAIR
        and n_seed == 14
        and n_center == WANT_COV_CENTER
        and n_xor == WANT_COV_XOR
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_pair": n_pair,
        "n_seed": n_seed,
        "n_center": n_center,
        "n_xor": n_xor,
        "rows": rows,
    }


def killed_dual_changes_r() -> dict:
    """Dual changes parent run length: G(1,0) vs G(1,2) both r=1."""
    k, s, n, j, p = 1, 9, 1, 0, 12
    j2 = 2 * n - j
    p2 = 8
    got = g1_core_slot(n, j)
    got2 = g1_core_slot(n, j2)
    ok = (
        got == (0, 1, 0)
        and got2 == (0, 1, 2)
        and got2 == dual_core_slot(n, j)
        and got[1] == got2[1]
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "slot": list(got),
        "dual": list(got2),
    }


def killed_start_no_radj() -> dict:
    """Dual start is 2m-start: G(7,4) maps to start 5, not 6."""
    k, s, n, j, p = 2, 9, 7, 4, 16
    j2 = 2 * n - j
    p2 = 4
    m = n // 2
    got = g1_core_slot(n, j)
    got2 = g1_core_slot(n, j2)
    naive = (2 * m - got[0], got[1], 2 * got[1] - got[2])
    ok = (
        got == (0, 2, 4)
        and got2 == (5, 2, 0)
        and got2 == dual_core_slot(n, j)
        and naive == (6, 2, 0)
        and got2 != naive
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "slot": list(got),
        "dual": list(got2),
        "naive": list(naive),
    }


def killed_even_parent() -> dict:
    """Dual of even G=1 is a parent slot: G(2,0) vs G(2,4) have none."""
    k, s, n, j, p = 1, 7, 2, 0, 12
    j2 = 2 * n - j
    p2 = 4
    got = g1_core_slot(n, j)
    got2 = g1_core_slot(n, j2)
    ok = (
        n % 2 == 0
        and G(n, j) == 1
        and got == (0, 1, 0)
        and got2 == (0, 1, 2)
        and g1_slot(n, j) is None
        and g1_slot(n, j2) is None
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "slot": list(got),
        "dual": list(got2),
        "g1_slot": g1_slot(n, j),
        "g1_slot_dual": g1_slot(n, j2),
    }


def prefixes() -> dict:
    it = json.loads(IT_JSON.read_text())
    ok = (
        it["checks"]["all_ok"]
        and it["verdict"]["n_gt0_core_slot"] == "LEMMA"
        and it["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert dual_core_slot(1, 0) == g1_core_slot(1, 2) == (0, 1, 2)
    assert dual_core_slot(1, 1) == g1_core_slot(1, 1) == (0, 1, 1)
    assert dual_core_slot(0, 0) == "seed"
    assert dual_core_slot(2, 0) == g1_core_slot(2, 4) == (0, 1, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = dual_table()
    sc = dual_cover()
    k0 = killed_dual_changes_r()
    k1 = killed_start_no_radj()
    k2 = killed_even_parent()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dual_table": {k: rt[k] for k in rt if k != "ok"},
        "dual_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_dual_changes_r": {k: k0[k] for k in k0 if k != "ok"},
        "killed_start_no_radj": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_parent": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_core_slot": True,
            "center_self_dual": True,
            "covering_dual_slots": True,
            "dual_changes_r": False,
            "dual_start_no_radj": False,
            "even_dual_parent_slot": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_core_slot": "LEMMA",
            "center_self_dual": "LEMMA",
            "covering_dual_slots": "LEMMA",
            "dual_changes_r": "KILLED",
            "dual_start_no_radj": "KILLED",
            "even_dual_parent_slot": "KILLED",
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
    print("dual_table", dump["dual_table"])
    cov = dump["dual_cover"]
    print(
        "dual_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_pair",
        cov["n_pair"],
        "n_seed",
        cov["n_seed"],
        "n_center",
        cov["n_center"],
        "n_xor",
        cov["n_xor"],
    )
    print("killed_dual_changes_r", dump["killed_dual_changes_r"])
    print("killed_start_no_radj", dump["killed_start_no_radj"])
    print("killed_even_parent", dump["killed_even_parent"])


if __name__ == "__main__":
    main()
