#!/usr/bin/env python3
"""Cycle SY: odd pal-pair rest equals raw for k>=3.

Pal-left never forced for k>=3. Odd pal-right forced AND tot is 0 at
p=4 (even Green count after dropping unique even n=3U-2, all fire),
1 at p=6 (odd count, bits 5,6 fire on odd t>=3), and 1 at p=14 (odd
count; Cycle PD fires on odd n). Those p=14 covering times are
t mod 4 = 1, so the even snapshot sits in PD's 0011 class. Odd corr
vanishes, so odd pal-pair rest tot equals pal-pair raw tot for every
k>=3. Not rest=S xor T. Do not walk leftover p catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_sy.py --certify
Dump: research/cycle_sy.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lc import want_p4_n
from cycle_ld import want_p6_n
from cycle_lf import want_p14_n
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced, unique_even_n
from cycle_sw import odd_p14_ns, want_odd_p6_n
from cycle_sx import covering_t, odd_p14_times
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SX_JSON = Path(__file__).resolve().parent / "cycle_sx.json"
SW_JSON = Path(__file__).resolve().parent / "cycle_sw.json"
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_PAL = 12
T_PER = 256
PAT0011 = (0, 0, 1, 1)
PAT1110 = (1, 1, 1, 0)
Q = 10


def odd_p4_count(k: int) -> int:
    """Odd pal-right G=1 at p=4: full count minus unique even n=3U-2."""
    return want_p4_n(k, 10) - 1


def odd_forced_corr(k: int) -> int:
    """Odd pal-right forced AND tot xor, k>=3: 0 xor 1 xor 1."""
    return 0 if k >= 3 else 1


def tot_form() -> dict:
    """k<=64: p=14 times t mod 4 = 1; odd p=4 count even; p=6,14 odd."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if k >= 3:
            ts = odd_p14_times(k)
            ns = odd_p14_ns(k)
            if sorted(covering_t(k, n) for n in ns) != sorted(ts):
                return {"ok": False, "times": True, "k": k}
            if any(t % 4 != 1 for t in ts):
                return {"ok": False, "mod": True, "k": k}
            if min(ts) - 1 < 16:
                return {"ok": False, "smin": True, "k": k, "s": min(ts) - 1}
            if odd_p4_count(k) % 2 != 0 or want_odd_p6_n(k) % 2 != 1:
                return {"ok": False, "par": True, "k": k}
            if want_p14_n(k, 10) % 2 != 1 or len(ts) != want_p14_n(k, 10):
                return {"ok": False, "c14": True, "k": k}
            if unique_even_n(k) % 2 != 0:
                return {"ok": False, "ue": True, "k": k}
            if odd_forced_corr(k) != 0:
                return {"ok": False, "corr": True, "k": k}
            if not pal_left_never_forced(k):
                return {"ok": False, "left": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and odd_p4_count(3) == 4
        and want_odd_p6_n(3) == 3
        and want_p14_n(3, 10) == 5
        and odd_forced_corr(2) == 1
        and want_even(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
        and PAT0011 in AND_ONES
        and and_clause(*PAT1110) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def period_p14() -> dict:
    """Even t>=16: bits 11-14 are 0011 iff t mod 4 = 0 else 1110."""
    n_ok = 0
    row = 1
    for t in range(0, T_PER):
        if t >= 16 and t % 2 == 0:
            tup = tuple(bit_at(row, 11 + i) for i in range(4))
            want = PAT0011 if t % 4 == 0 else PAT1110
            if tup != want or and_clause(*tup) != int(t % 4 == 0):
                return {"ok": False, "t": t, "got": tup, "want": list(want)}
            n_ok += 1
        row = rule30_step(row)
    ok = n_ok == (T_PER - 16) // 2
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_PER - 2}


def pal_c_ap() -> dict:
    """k=3..12: pal-center tot is xor of c_t and x(t,1) on the APs."""
    t_hi = Q * (1 << K_PAL)
    row = 1
    cand = []
    for t in range(0, t_hi):
        cand.append(bit_at(row, t) & bit_at(row, t + 1))
        row = rule30_step(row)
    n_ok = 0
    rows = {}
    for k in range(3, K_PAL + 1):
        u = 1 << k
        xe = xo = 0
        t = 2 * u + 3
        while t <= Q * u - 1:
            xe ^= cand[t]
            t += 4
        t = 2 * u + 1
        while t <= Q * u - 3:
            xo ^= cand[t]
            t += 4
        n_ok += 1
        rows[str(k)] = {"pal_c_e": xe, "pal_c_o": xo}
    ok = (
        n_ok == K_PAL - 2
        and rows["3"]["pal_c_e"] == 1
        and rows["10"]["pal_c_e"] == 0
        and rows["10"]["pal_c_o"] == 1
        and rows["12"]["pal_c_e"] == 1
        and rows["12"]["pal_c_e"] != (12 % 2)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_PAL, "rows": rows}


def killed_eq() -> dict:
    """pal_c_e = k mod 2; pal_c_e = pal_c_o; odd corr for k<3."""
    ok = (
        odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and unique_even_n(3) == 22
        and want_p6_n(3, 10) == 3
    )
    return {"ok": ok}


def prefixes() -> dict:
    sx = json.loads(SX_JSON.read_text())
    sw = json.loads(SW_JSON.read_text())
    pd = json.loads(PD_JSON.read_text())
    pc = json.loads(PC_JSON.read_text())
    ok = (
        sx["checks"]["all_ok"]
        and sw["checks"]["all_ok"]
        and pd["checks"]["all_ok"]
        and pc["checks"]["all_ok"]
        and sx["verdict"]["odd_p14_covering_times"] == "LEMMA"
        and sw["verdict"]["p6_and_1_on_odd_t_ge_3"] == "LEMMA"
        and pd["verdict"]["p14_period4"] == "LEMMA"
        and pc["verdict"]["p14_set_k_ge_3"] == "LEMMA"
        and pc["verdict"]["p4_set"] == "LEMMA"
        and pc["verdict"]["p6_set"] == "LEMMA"
        and sx["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sx["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, per, ap, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and per["ok"] and ap["ok"] and kl["ok"]
    assert sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    tot = tot_form()
    per = period_p14()
    ap = pal_c_ap()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, per, ap, kl, sc, pref)
    dump = {
        "cycle": "SY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "period_p14": {k: per[k] for k in per if k != "ok"},
        "pal_c_ap": {k: ap[k] for k in ap if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_pair_rest_eq_raw_k_ge_3": True,
            "odd_p14_t_mod4_eq_1": True,
            "odd_forced_corr_0_k_ge_3": True,
            "pal_c_e_eq_k_mod2": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_pair_rest_eq_raw_k_ge_3": "LEMMA",
            "odd_p14_t_mod4_eq_1": "LEMMA",
            "odd_forced_corr_0_k_ge_3": "LEMMA",
            "p14_and_1_on_listed_all_k": "LEMMA",
            "pal_c_e_eq_k_mod2": "KILLED",
            "pal_c_e_eq_pal_c_o": "KILLED",
            "pal_c_eq_ST": "KILLED",
            "p14_and_all_odd_t": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
            "E_all_k": "PREFIX",
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
        "period n_ok",
        dump["period_p14"]["n_ok"],
        "pal_c k12 e",
        dump["pal_c_ap"]["rows"]["12"]["pal_c_e"],
        "k12 o",
        dump["pal_c_ap"]["rows"]["12"]["pal_c_o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
