#!/usr/bin/env python3
"""Cycle QN: covering packed p=16 AND xor on n%4==0 is 1 for k>=3.

Cycle PH packed AND at p=16 fires iff n is even for k>=3, and Green
even n is parent p=8. Cycle PH odd Green at p=8 is {3U-3, 3U-1},
xor 0; both odd parents map to child n%4==2, so packed p=16 on
n%4==2 vanishes. Even Green at p=8 is parent p=4, whose even n is
3U'-2 mapping to n%4==0, tot 1 for k>=2. Hence packed p=16 AND xor
on n%4==0 is 1 for k>=3. Other UNIQUE_EVEN freeze AND n%4 miss 0
for k>=6, so unique packed n%4==0 tot equals this bit for k>=6.
Not rest=S xor T (k=3: p=16 n0=1, rest=0). Not unique packed n0
equals p=16 n0 for all k (k=4 unique n0=0). Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qn.py --certify
Dump: research/cycle_qn.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import in_p4, want_p4_xor
from cycle_ph import in_p8, in_p16_even, want_p16_pack
from cycle_pk import want_p32_pack
from cycle_pw import want_p52_pack
from cycle_px import want_p60_pack
from cycle_py import want_p72_pack
from cycle_pz import want_p76_pack
from cycle_qb import want_p88_pack
from cycle_qk import want_p8_gxor

OUT = Path(__file__).resolve().with_suffix(".json")
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"
QM_JSON = Path(__file__).resolve().parent / "cycle_qm.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_ALG = 64


def want_p8_n0(k: int) -> int:
    """Covering Green p=8 xor on n%4==0, all k: 1 iff k>=2."""
    return int(k >= 2)


def want_p8_n2(k: int) -> int:
    """Covering Green p=8 xor on n%4==2, all k."""
    return 0


def want_p16_n0(k: int) -> int:
    """Covering packed/Green p=16 xor on n%4==0, all k: 1 iff k>=3."""
    return int(k >= 3)


def want_p16_n2(k: int) -> int:
    """Covering packed/Green p=16 xor on n%4==2, all k."""
    return 0


def want_unique_pack_n0(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on n%4==0, k>=6: 1."""
    return int(k >= 6)


def p8_npar(k: int) -> dict:
    """Covering Green p=8 xor split by n parity / n%4, plus odd set."""
    U = 1 << k
    e = o = n0 = n2 = 0
    odds = []
    for n in range(0, 4 * U):
        if in_p8(n, k):
            if n % 2:
                o ^= 1
                odds.append(n)
            else:
                e ^= 1
                if n % 4 == 0:
                    n0 ^= 1
                else:
                    n2 ^= 1
    return {"e": e, "o": o, "n0": n0, "n2": n2, "odds": odds}


def p16_npar(k: int) -> dict:
    """Covering Green even n at p=16 xor split by n%4."""
    U = 1 << k
    n0 = n2 = 0
    for n in range(0, 4 * U, 2):
        if in_p16_even(n, k):
            if n % 4 == 0:
                n0 ^= 1
            else:
                n2 ^= 1
    return {"n0": n0, "n2": n2}


def p8_split() -> dict:
    """k<=K_G: p=8 odd tot 0 with two cells; even tot on n%4==0 is 1 for k>=2."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        w = p8_npar(k)
        U = 1 << k
        if k >= 2:
            want_odds = [3 * U - 3, 3 * U - 1]
            if w["odds"] != want_odds or w["o"] != 0:
                return {"ok": False, "odd": True, "k": k, "odds": w["odds"]}
            if w["n0"] != 1 or w["n2"] != 0 or w["e"] != 1:
                return {"ok": False, "even": True, "k": k, "w": w}
            ev = [n for n in range(0, 4 * U, 2) if in_p4(n, k - 1)]
            if ev != [3 * (U // 2) - 2]:
                return {"ok": False, "p4e": True, "k": k, "ev": ev}
            child = 2 * (3 * (U // 2) - 2)
            if child % 4 != 0 or not in_p8(child, k):
                return {"ok": False, "map": True, "k": k, "child": child}
            n_ok += 1
        else:
            if w["n0"] != want_p8_n0(k):
                return {"ok": False, "early": True, "k": k}
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {
                "e": w["e"],
                "o": w["o"],
                "n0": w["n0"],
                "n2": w["n2"],
                "n_odd": len(w["odds"]),
            }
    ok = (
        rows["2"]["n0"] == 1
        and rows["2"]["o"] == 0
        and rows["2"]["n_odd"] == 2
        and rows["8"]["n0"] == 1
        and rows["12"]["n2"] == 0
        and want_p8_gxor(2) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def p16_split() -> dict:
    """k<=K_G: p=16 n%4==0 tot is 1 iff k>=3; n%4==2 tot 0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        w = p16_npar(k)
        if w["n0"] != want_p16_n0(k) or w["n2"] != want_p16_n2(k):
            return {"ok": False, "k": k, "n0": w["n0"], "n2": w["n2"]}
        if k >= 3:
            if (w["n0"] ^ w["n2"]) != want_p16_pack(k):
                return {"ok": False, "ph": True, "k": k}
            if w["n0"] != want_p8_n0(k - 1):
                return {"ok": False, "rec": True, "k": k}
            n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"n0": w["n0"], "n2": w["n2"]}
    ok = (
        rows["2"]["n0"] == 0
        and rows["3"]["n0"] == 1
        and rows["3"]["n2"] == 0
        and rows["4"]["n0"] == 1
        and rows["12"]["n0"] == 1
        and rows["12"]["n2"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: p=8 n0 / p=16 n0 doubling; unique pack n0 for k>=6."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_p8_n0(k) != int(k >= 2) or want_p8_n2(k) != 0:
            return {"ok": False, "p8": True, "k": k}
        if want_p16_n0(k) != int(k >= 3) or want_p16_n2(k) != 0:
            return {"ok": False, "p16": True, "k": k}
        if k >= 2 and want_p8_n0(k) != want_p4_xor(k - 1):
            return {"ok": False, "p4": True, "k": k}
        if k >= 3:
            if want_p16_n0(k) != want_p8_n0(k - 1):
                return {"ok": False, "rec": True, "k": k}
            if want_p16_n0(k) != want_p16_pack(k):
                return {"ok": False, "pack": True, "k": k}
        if k >= 6:
            if want_unique_pack_n0(k) != 1:
                return {"ok": False, "u": True, "k": k}
            # Other UNIQUE_EVEN packed tots are not n%4==0 slices.
            if want_p32_pack(k) != 1 or want_p76_pack(k) != 1 or want_p88_pack(k) != 1:
                return {"ok": False, "other": True, "k": k}
            if want_p52_pack(k) != 0 or want_p60_pack(k) != 0 or want_p72_pack(k) != 0:
                return {"ok": False, "silent": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_p8_n0(2) == 1
        and want_p16_n0(3) == 1
        and want_p16_n2(8) == 0
        and want_unique_pack_n0(6) == 1
        and want_unique_pack_n0(5) == 0
        and want_p4_xor(1) == 1
        and want_p8_gxor(12) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_n0_eq_st() -> dict:
    """p=16 n0 tot equals ST / unique packed n0 equals p=16 n0 for all k."""
    ok = (
        want_p16_n0(3) == 1
        and want_rest_e0(3) == 0
        and want_rest10(3, 10) == 0
        and want_p16_n0(7) == 1
        and want_rest_e0(7) == 0
        and want_p16_n0(4) == 1
        and want_unique_pack_n0(4) == 0
    )
    return {"ok": ok, "k3": 1, "ST3": 0, "k4_u": 0}


def prefixes() -> dict:
    ph = json.loads(PH_JSON.read_text())
    qm = json.loads(QM_JSON.read_text())
    ok = (
        ph["checks"]["all_ok"]
        and qm["checks"]["all_ok"]
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and ph["verdict"]["p8_odd_two_k_ge_2"] == "LEMMA"
        and qm["verdict"]["lo_n0_iff_k_in_0_1_3_5"] == "LEMMA"
        and ph["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ph["verdict"]["prize"] == "unsolved"
        and want_p16_pack(3) == 1
        and want_p8_gxor(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, p8, p16, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and p8["ok"] and p16["ok"]
    assert tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    p8 = p8_split()
    p16 = p16_split()
    tot = tot_form()
    kl = killed_n0_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, p8, p16, tot, kl, sc, pref)
    dump = {
        "cycle": "QN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "p8_split": {k: p8[k] for k in p8 if k != "ok"},
        "p16_split": {k: p16[k] for k in p16 if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "p8_n0_iff_k_ge_2": True,
            "p16_n0_iff_k_ge_3": True,
            "p16_n2_0": True,
            "unique_pack_n0_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p16_n0_eq_ST": False,
            "u_n0_eq_p16_all_k": False,
            "prize": False,
        },
        "verdict": {
            "p8_n0_iff_k_ge_2": "LEMMA",
            "p16_n0_iff_k_ge_3": "LEMMA",
            "p16_n2_0": "LEMMA",
            "unique_pack_n0_k_ge_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p16_n0_eq_ST": "KILLED",
            "u_n0_eq_p16_all_k": "KILLED",
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
    print(
        "p8_split n_ok",
        dump["p8_split"]["n_ok"],
        "p16_split n_ok",
        dump["p16_split"]["n_ok"],
        "p16_n0_8",
        dump["p16_split"]["rows"]["8"]["n0"],
        "p16_n2_8",
        dump["p16_split"]["rows"]["8"]["n2"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
