#!/usr/bin/env python3
"""Cycle JI: even-n iso1_lift5 is the cob-stretch of iso3_even.

On even n>0 the parent 5-window is freshman_lift5(iso3_even, odd
parent): offset 0 maps to 00011, offset 2r to 11000, v2-odd
interiors to 01110, v2-even interiors to 10101. v2-odd interiors
are not 10101; offset 0 is not 11000; v2-even interiors are not
01110. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ji.py --certify
Dump: research/cycle_ji.json
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
from cycle_al import G, v2
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_ir import isolated_one
from cycle_it import g1_core_slot
from cycle_jd import LIFT1_ODD, iso1_lift5
from cycle_jf import freshman_lift5
from cycle_jh import iso3_even
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JH_JSON = Path(__file__).resolve().parent / "cycle_jh.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT1_LO = (0, 0, 0, 1, 1)
LIFT1_HI = (1, 1, 0, 0, 0)
LIFT1_MID_ODD = (0, 1, 1, 1, 0)
LIFT1_MID_EVEN = LIFT1_ODD


def iso1_even(n: int, j: int):
    """Predicted iso1_lift5 on even n>0 from iso3_even cob-stretch."""
    three = iso3_even(n, j)
    if three is None:
        return None
    return freshman_lift5(three, False)


def lift_table() -> dict:
    """n<64: even iso1_lift5 equals iso1_even cob-stretch."""
    n_iso = n_seed = n_odd = n_even = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            pred = iso1_even(n, j)
            if n == 0:
                n_seed += 1
                if pred is not None:
                    return {"ok": False, "seed": True}
                continue
            five = iso1_lift5(n, j)
            if n % 2:
                n_odd += 1
                if pred is not None:
                    return {"ok": False, "odd": True, "n": n, "j": j}
                continue
            n_even += 1
            if pred != five:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "pred": list(pred) if pred else None,
                    "five": list(five),
                }
            if five == LIFT1_LO:
                n_lo += 1
            elif five == LIFT1_HI:
                n_hi += 1
            elif five == LIFT1_MID_ODD:
                n_mid_odd += 1
            else:
                n_mid_even += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_odd == 45
        and n_even == 415
        and n_lo == 115
        and n_hi == 115
        and n_mid_odd == 141
        and n_mid_even == 44
        and iso1_even(2, 0) == LIFT1_LO
        and iso1_even(2, 2) == LIFT1_MID_ODD
        and iso1_even(2, 4) == LIFT1_HI
        and iso1_even(4, 4) == LIFT1_MID_EVEN
        and iso1_even(3, 3) is None
        and freshman_lift5((0, 0, 1), False) == LIFT1_LO
        and freshman_lift5((1, 0, 0), False) == LIFT1_HI
        and freshman_lift5((0, 1, 0), False) == LIFT1_MID_ODD
        and freshman_lift5((1, 1, 1), False) == LIFT1_MID_EVEN
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
    }


def _walk_lift(k: int, q: int) -> dict:
    """iso1_even on covering even isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
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
                pred = iso1_even(n, j)
                five = iso1_lift5(n, j)
                if n % 2:
                    n_odd += 1
                    if pred is not None:
                        return {"ok": False, "odd": True, "k": k, "n": n, "j": j}
                    continue
                if pred != five:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_even += 1
                if five == LIFT1_LO:
                    n_lo += 1
                elif five == LIFT1_HI:
                    n_hi += 1
                elif five == LIFT1_MID_ODD:
                    n_mid_odd += 1
                else:
                    n_mid_even += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "xor_j": xor_j,
    }


def lift_cover() -> dict:
    """iso1_even on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_lift(k, q)
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
            n_odd += w["n_odd"]
            n_even += w["n_even"]
            n_lo += w["n_lo"]
            n_hi += w["n_hi"]
            n_mid_odd += w["n_mid_odd"]
            n_mid_even += w["n_mid_even"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_even": w["n_even"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_odd == 741
        and n_even == 7030
        and n_lo == 2011
        and n_hi == 1912
        and n_mid_odd == 2373
        and n_mid_even == 734
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "rows": rows,
    }


def killed_v2odd_mid_10101() -> dict:
    """v2-odd interiors lift from 10101: G(2,2) is 01110."""
    k, s, n, j, p = 0, 5, 2, 2, 6
    five = iso1_even(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and (v2(n) & 1) == 1
        and d not in (0, 2 * r)
        and five == LIFT1_MID_ODD
        and five != LIFT1_MID_EVEN
        and five == iso1_lift5(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "v2": v2(n),
        "slot": list(got),
        "five": list(five),
    }


def killed_off0_11000() -> dict:
    """Offset 0 lifts from 11000: G(2,0) is 00011."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    five = iso1_even(n, j)
    got = g1_core_slot(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and got[2] == 0
        and five == LIFT1_LO
        and five != LIFT1_HI
        and five == iso1_lift5(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "five": list(five),
    }


def killed_v2even_mid_01110() -> dict:
    """v2-even interiors lift from 01110: G(4,4) is 10101."""
    k, s, n, j, p = 1, 11, 4, 4, 12
    five = iso1_even(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and (v2(n) & 1) == 0
        and d not in (0, 2 * r)
        and five == LIFT1_MID_EVEN
        and five != LIFT1_MID_ODD
        and five == iso1_lift5(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "v2": v2(n),
        "slot": list(got),
        "five": list(five),
    }


def prefixes() -> dict:
    jh = json.loads(JH_JSON.read_text())
    ok = (
        jh["checks"]["all_ok"]
        and jh["verdict"]["even_iso3_v2"] == "LEMMA"
        and jh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso1_even(2, 0) == iso1_lift5(2, 0) == LIFT1_LO
    assert iso1_even(2, 2) == LIFT1_MID_ODD
    assert iso1_even(4, 4) == LIFT1_MID_EVEN
    assert iso1_even(0, 0) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift_table()
    sc = lift_cover()
    k0 = killed_v2odd_mid_10101()
    k1 = killed_off0_11000()
    k2 = killed_v2even_mid_01110()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift_table": {k: rt[k] for k in rt if k != "ok"},
        "lift_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_v2odd_mid_10101": {k: k0[k] for k in k0 if k != "ok"},
        "killed_off0_11000": {k: k1[k] for k in k1 if k != "ok"},
        "killed_v2even_mid_01110": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "even_iso1_from_slot": True,
            "cob_iso3_LIFT1": True,
            "covering_even_iso1_slot": True,
            "v2odd_mid_10101": False,
            "off0_11000": False,
            "v2even_mid_01110": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_iso1_from_slot": "LEMMA",
            "cob_iso3_LIFT1": "LEMMA",
            "covering_even_iso1_slot": "LEMMA",
            "v2odd_mid_10101": "KILLED",
            "off0_11000": "KILLED",
            "v2even_mid_01110": "KILLED",
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
    print("lift_table", dump["lift_table"])
    cov = dump["lift_cover"]
    print(
        "lift_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_even",
        cov["n_even"],
        "n_lo",
        cov["n_lo"],
        "n_hi",
        cov["n_hi"],
        "n_mid_odd",
        cov["n_mid_odd"],
        "n_mid_even",
        cov["n_mid_even"],
    )
    print("killed_v2odd_mid_10101", dump["killed_v2odd_mid_10101"])
    print("killed_off0_11000", dump["killed_off0_11000"])
    print("killed_v2even_mid_01110", dump["killed_v2even_mid_01110"])


if __name__ == "__main__":
    main()
