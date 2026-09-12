#!/usr/bin/env python3
"""Cycle JJ: doubling n maps isolated-one LIFT1 by swapping palindromes.

iso1_lift5(2n,2j) equals lift5_double of iso1_lift5(n,j) for n>0.
Ends 00011 and 11000 stay; interiors swap 01110 with 10101. Odd-n
10101 doubles to 01110. Interiors do not stay; ends do not swap;
odd iso does not double to 10101. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jj.py --certify
Dump: research/cycle_jj.json
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
from cycle_ir import isolated_one
from cycle_jd import iso1_lift5
from cycle_ji import (
    LIFT1_HI,
    LIFT1_LO,
    LIFT1_MID_EVEN,
    LIFT1_MID_ODD,
    iso1_even,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JI_JSON = Path(__file__).resolve().parent / "cycle_ji.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def lift5_double(five):
    """LIFT1 image under n to 2n on the stretched column."""
    if five in (LIFT1_LO, LIFT1_HI):
        return five
    if five == LIFT1_MID_ODD:
        return LIFT1_MID_EVEN
    if five == LIFT1_MID_EVEN:
        return LIFT1_MID_ODD
    return None


def dbl_table() -> dict:
    """n<64: iso1_lift5(2n,2j) equals lift5_double of the parent."""
    n_iso = n_seed = n_stay_lo = n_stay_hi = 0
    n_swap_odd = n_swap_even = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            five = iso1_lift5(n, j)
            five2 = iso1_lift5(2 * n, 2 * j)
            pred = lift5_double(five)
            if not isolated_one(2 * n, 2 * j) or five2 != pred:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "five": list(five),
                    "five2": list(five2) if five2 else None,
                }
            if n % 2 == 0 and iso1_even(2 * n, 2 * j) != five2:
                return {"ok": False, "even": True, "n": n, "j": j}
            if five == five2:
                if five == LIFT1_LO:
                    n_stay_lo += 1
                else:
                    n_stay_hi += 1
            elif five == LIFT1_MID_ODD:
                n_swap_odd += 1
            else:
                n_swap_even += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_stay_lo == 115
        and n_stay_hi == 115
        and n_swap_odd == 141
        and n_swap_even == 89
        and lift5_double(LIFT1_LO) == LIFT1_LO
        and lift5_double(LIFT1_HI) == LIFT1_HI
        and lift5_double(LIFT1_MID_ODD) == LIFT1_MID_EVEN
        and lift5_double(LIFT1_MID_EVEN) == LIFT1_MID_ODD
        and iso1_lift5(4, 4) == lift5_double(iso1_lift5(2, 2))
        and iso1_lift5(6, 6) == lift5_double(iso1_lift5(3, 3)) == LIFT1_MID_ODD
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_stay_lo": n_stay_lo,
        "n_stay_hi": n_stay_hi,
        "n_swap_odd": n_swap_odd,
        "n_swap_even": n_swap_even,
    }


def _walk_dbl(k: int, q: int) -> dict:
    """Doubling identity on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_dbl = 0
    n_stay_lo = n_stay_hi = n_swap_odd = n_swap_even = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                if n == 0:
                    n_seed += 1
                    continue
                five = iso1_lift5(n, j)
                five2 = iso1_lift5(2 * n, 2 * j)
                if five2 != lift5_double(five):
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_dbl += 1
                if five == five2:
                    if five == LIFT1_LO:
                        n_stay_lo += 1
                    else:
                        n_stay_hi += 1
                elif five == LIFT1_MID_ODD:
                    n_swap_odd += 1
                else:
                    n_swap_even += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_dbl": n_dbl,
        "n_stay_lo": n_stay_lo,
        "n_stay_hi": n_stay_hi,
        "n_swap_odd": n_swap_odd,
        "n_swap_even": n_swap_even,
        "xor_j": xor_j,
    }


def dbl_cover() -> dict:
    """Doubling identity on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_dbl = 0
    n_stay_lo = n_stay_hi = n_swap_odd = n_swap_even = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dbl(k, q)
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
            n_iso += w["n_iso"]
            n_seed += w["n_seed"]
            n_dbl += w["n_dbl"]
            n_stay_lo += w["n_stay_lo"]
            n_stay_hi += w["n_stay_hi"]
            n_swap_odd += w["n_swap_odd"]
            n_swap_even += w["n_swap_even"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_dbl": w["n_dbl"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_dbl == 7771
        and n_stay_lo == 2011
        and n_stay_hi == 1912
        and n_swap_odd == 2373
        and n_swap_even == 1475
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_dbl": n_dbl,
        "n_stay_lo": n_stay_lo,
        "n_stay_hi": n_stay_hi,
        "n_swap_odd": n_swap_odd,
        "n_swap_even": n_swap_even,
        "rows": rows,
    }


def killed_mid_stays() -> dict:
    """Interiors stay: G(2,2) 01110 doubles to G(4,4) 10101."""
    k, s, n, j, p, p2 = 1, 15, 2, 2, 16, 12
    n2, j2 = 2 * n, 2 * j
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n2, j2)
    ok = (
        isolated_one(n, j)
        and isolated_one(n2, j2)
        and five == LIFT1_MID_ODD
        and five2 == lift5_double(five) == LIFT1_MID_EVEN
        and five2 != five
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def killed_end_swaps() -> dict:
    """Ends swap: G(2,0) 00011 doubles to G(4,0) 00011."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 20
    n2, j2 = 2 * n, 2 * j
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n2, j2)
    ok = (
        isolated_one(n, j)
        and isolated_one(n2, j2)
        and five == LIFT1_LO
        and five2 == lift5_double(five) == five
        and five2 != LIFT1_HI
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def killed_odd_stays_10101() -> dict:
    """Odd iso doubles to 10101: G(3,3) doubles to G(6,6) 01110."""
    k, s, n, j, p, p2 = 2, 17, 3, 3, 18, 12
    n2, j2 = 2 * n, 2 * j
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n2, j2)
    ok = (
        isolated_one(n, j)
        and n % 2 == 1
        and isolated_one(n2, j2)
        and five == LIFT1_MID_EVEN
        and five2 == lift5_double(five) == LIFT1_MID_ODD
        and five2 != five
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def prefixes() -> dict:
    ji = json.loads(JI_JSON.read_text())
    ok = (
        ji["checks"]["all_ok"]
        and ji["verdict"]["even_iso1_from_slot"] == "LEMMA"
        and ji["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert lift5_double(LIFT1_MID_ODD) == LIFT1_MID_EVEN
    assert iso1_lift5(4, 0) == iso1_lift5(2, 0) == LIFT1_LO
    assert iso1_lift5(6, 6) == LIFT1_MID_ODD
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = dbl_table()
    sc = dbl_cover()
    k0 = killed_mid_stays()
    k1 = killed_end_swaps()
    k2 = killed_odd_stays_10101()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dbl_table": {k: rt[k] for k in rt if k != "ok"},
        "dbl_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_mid_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_end_swaps": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_stays_10101": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "lift5_double": True,
            "iso1_double_col": True,
            "covering_lift5_double": True,
            "mid_stays": False,
            "end_swaps": False,
            "odd_stays_10101": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "lift5_double": "LEMMA",
            "iso1_double_col": "LEMMA",
            "covering_lift5_double": "LEMMA",
            "mid_stays": "KILLED",
            "end_swaps": "KILLED",
            "odd_stays_10101": "KILLED",
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
    print("dbl_table", dump["dbl_table"])
    cov = dump["dbl_cover"]
    print(
        "dbl_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_dbl",
        cov["n_dbl"],
        "n_stay_lo",
        cov["n_stay_lo"],
        "n_stay_hi",
        cov["n_stay_hi"],
        "n_swap_odd",
        cov["n_swap_odd"],
        "n_swap_even",
        cov["n_swap_even"],
    )
    print("killed_mid_stays", dump["killed_mid_stays"])
    print("killed_end_swaps", dump["killed_end_swaps"])
    print("killed_odd_stays_10101", dump["killed_odd_stays_10101"])


if __name__ == "__main__":
    main()
