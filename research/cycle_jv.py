#!/usr/bin/env python3
"""Cycle JV: cob-stretch of pair_dbl_threes recovers pair_dbl_fives.

cob_lift5 of 001/010 is 00011/01110; cob_lift5 of 010/100 is
01110/11000. So cob of pair_dbl_threes equals pair_dbl_fives.
Cob of even-j is not the odd-j fives; cob of 001 is not 01110;
cob of pair_dbl_threes is pair_dbl_fives. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jv.py --certify
Dump: research/cycle_jv.json
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
from cycle_jd import iso1_lift5
from cycle_jl import PAIR_EVEN as FIVE_EVEN
from cycle_jl import PAIR_ODD as FIVE_ODD
from cycle_jl import pair_dbl_fives
from cycle_js import PAIR_EVEN as THREE_EVEN
from cycle_js import PAIR_ODD as THREE_ODD
from cycle_js import pair_dbl_threes
from cycle_ju import cob_lift5
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JU_JSON = Path(__file__).resolve().parent / "cycle_ju.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def cob_pair(threes):
    """Cob-stretch of a pair of iso3 windows onto LIFT1."""
    if threes is None:
        return None
    a, b = threes
    return (cob_lift5(a), cob_lift5(b))


def cob_pair_table() -> dict:
    """n<64: cob_pair of pair_dbl_threes equals pair_dbl_fives."""
    if cob_pair(THREE_EVEN) != FIVE_EVEN:
        return {"ok": False, "even": True}
    if cob_pair(THREE_ODD) != FIVE_ODD:
        return {"ok": False, "odd": True}
    n_g11 = n_even = n_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            th = pair_dbl_threes(n, j)
            fv = pair_dbl_fives(n, j)
            if kind is None:
                if th is not None or fv is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            got = cob_pair(th)
            n2, jL, jR = 2 * n, 2 * j, 2 * j + 2
            fiveL = iso1_lift5(n2, jL)
            fiveR = iso1_lift5(n2, jR)
            if got != fv or (fiveL, fiveR) != fv:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                }
            n_g11 += 1
            if j % 2 == 0:
                n_even += 1
            else:
                n_odd += 1
    ok = (
        n_g11 == 512
        and n_even == 256
        and n_odd == 256
        and cob_pair(pair_dbl_threes(5, 0)) == FIVE_EVEN
        and cob_pair(pair_dbl_threes(5, 1)) == FIVE_ODD
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
    }


def _walk_cob(k: int, q: int) -> dict:
    """cob_pair identity on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_even = n_odd = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                th = pair_dbl_threes(n, j)
                fv = pair_dbl_fives(n, j)
                if kind is None:
                    if th is not None or fv is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                if cob_pair(th) != fv:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_g11 += 1
                if j % 2 == 0:
                    n_even += 1
                else:
                    n_odd += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
        "xor_j": xor_j,
    }


def cob_pair_cover() -> dict:
    """cob_pair on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_even = n_odd = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_cob(k, q)
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
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_even": w["n_even"],
                "n_odd": w["n_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_even == 4292
        and n_odd == 4285
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
        "rows": rows,
    }


def killed_even_odd_fives() -> dict:
    """Cob of even-j is odd-j fives: G(5,0) cob 001/010 is 00011/01110."""
    k, s, n, j, p = 1, 9, 5, 0, 20
    th = pair_dbl_threes(n, j)
    fv = cob_pair(th)
    ok = (
        j % 2 == 0
        and th == THREE_EVEN
        and fv == FIVE_EVEN
        and fv != FIVE_ODD
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "threes": [list(th[0]), list(th[1])],
        "fives": [list(fv[0]), list(fv[1])],
    }


def killed_001_is_01110() -> dict:
    """Cob of 001 is 01110: cob_lift5(001)=00011."""
    five = cob_lift5(THREE_EVEN[0])
    ok = five == FIVE_EVEN[0] and five != FIVE_EVEN[1]
    return {
        "ok": ok,
        "three": list(THREE_EVEN[0]),
        "five": list(five),
    }


def killed_not_fives() -> dict:
    """Cob of pair_dbl_threes is not pair_dbl_fives: G(5,0) matches."""
    k, s, n, j, p = 1, 9, 5, 0, 20
    th = pair_dbl_threes(n, j)
    fv = cob_pair(th)
    ok = fv == pair_dbl_fives(n, j) == FIVE_EVEN and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "threes": [list(th[0]), list(th[1])],
        "fives": [list(fv[0]), list(fv[1])],
    }


def prefixes() -> dict:
    ju = json.loads(JU_JSON.read_text())
    ok = (
        ju["checks"]["all_ok"]
        and ju["verdict"]["cob_commute_rev"] == "LEMMA"
        and ju["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert cob_pair(THREE_EVEN) == FIVE_EVEN
    assert cob_pair(THREE_ODD) == FIVE_ODD
    assert cob_pair(pair_dbl_threes(5, 0)) == pair_dbl_fives(5, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = cob_pair_table()
    sc = cob_pair_cover()
    k0 = killed_even_odd_fives()
    k1 = killed_001_is_01110()
    k2 = killed_not_fives()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cob_pair_table": {k: rt[k] for k in rt if k != "ok"},
        "cob_pair_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_odd_fives": {k: k0[k] for k in k0 if k != "ok"},
        "killed_001_is_01110": {k: k1[k] for k in k1 if k != "ok"},
        "killed_not_fives": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "cob_pair": True,
            "cob_pair_col": True,
            "covering_cob_pair": True,
            "even_odd_fives": False,
            "001_is_01110": False,
            "not_fives": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cob_pair": "LEMMA",
            "cob_pair_col": "LEMMA",
            "covering_cob_pair": "LEMMA",
            "even_odd_fives": "KILLED",
            "001_is_01110": "KILLED",
            "not_fives": "KILLED",
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
    print("cob_pair_table", dump["cob_pair_table"])
    cov = dump["cob_pair_cover"]
    print(
        "cob_pair_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_even",
        cov["n_even"],
        "n_odd",
        cov["n_odd"],
    )
    print("killed_even_odd_fives", dump["killed_even_odd_fives"])
    print("killed_001_is_01110", dump["killed_001_is_01110"])
    print("killed_not_fives", dump["killed_not_fives"])


if __name__ == "__main__":
    main()
