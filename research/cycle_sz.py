#!/usr/bin/env python3
"""Cycle SZ: odd-child covering snapshot doubles parent even snapshot.

On q=10, even snapshot s=10U-2n-2. Odd child n=2m+1 at k has
s_k(2m+1)=2 s_{k-1}(m). Covering times fold t_k(2m)=2 t_{k-1}(m)+1
and t_k(2m+1)=2 t_{k-1}(m)-1. Pal-center tot is the xor of
c_t and x(t,1) on every covering time, hence P(5U) xor P(U) with
P(M) the prefix xor of that bit on odd t=1,3,...,2M-1. Pal-center
even tot is xor of cand(2t+1) over parent covering times; odd tot
is xor of cand(2t-1). Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_sz.py --certify
Dump: research/cycle_sz.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_st import pal_center_p
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SY_JSON = Path(__file__).resolve().parent / "cycle_sy.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
ST_JSON = Path(__file__).resolve().parent / "cycle_st.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_PAL = 13
T_LOCAL = 4096
Q = 10
PAT0011 = (0, 0, 1, 1)
PER8_E = (1, 1, 1, 0, 1, 0, 1, 0)


def odd_child_s(m: int, k: int) -> int:
    """Even snapshot of odd child n=2m+1 at k: 2 * parent even snapshot."""
    return 2 * even_s(m, k - 1)


def even_child_t(m: int, k: int) -> int:
    """Odd covering time of even child n=2m: 2 * parent covering time + 1."""
    return 2 * covering_t(k - 1, m) + 1


def odd_child_t(m: int, k: int) -> int:
    """Odd covering time of odd child n=2m+1: 2 * parent covering time - 1."""
    return 2 * covering_t(k - 1, m) - 1


def even_child_pal_p(m: int, k: int) -> int:
    """Pal-center packed p of even child n=2m: 2 * parent covering time + 2."""
    return 2 * covering_t(k - 1, m) + 2


def odd_child_pal_p(m: int, k: int) -> int:
    """Pal-center packed p of odd child n=2m+1: 2 * parent covering time."""
    return 2 * covering_t(k - 1, m)


def want_pal_c_e_period8(k: int) -> int:
    """Killed at k=13: pal_c_e period 8 starting at k=3."""
    return PER8_E[(k - 3) % 8]


def want_pal_c_tot_even_ge10(k: int) -> int:
    """Killed at k=13: pal_c tot is 1 iff k even and k>=10."""
    return int(k % 2 == 0 and k >= 10)


def tot_form() -> dict:
    """k=1..64: odd-child s doubles; covering times and pal-center p fold."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        u = 1 << (k - 1)
        samples = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for m in samples:
            if m < 0 or m >= 4 * u:
                continue
            if odd_child_s(m, k) != even_s(2 * m + 1, k):
                return {"ok": False, "s": True, "k": k, "m": m}
            if odd_child_s(m, k) != 2 * even_s(m, k - 1):
                return {"ok": False, "s2": True, "k": k, "m": m}
            if even_child_t(m, k) != covering_t(k, 2 * m):
                return {"ok": False, "te": True, "k": k, "m": m}
            if odd_child_t(m, k) != covering_t(k, 2 * m + 1):
                return {"ok": False, "to": True, "k": k, "m": m}
            if even_child_t(m, k) != 2 * covering_t(k - 1, m) + 1:
                return {"ok": False, "te2": True, "k": k, "m": m}
            if odd_child_t(m, k) != 2 * covering_t(k - 1, m) - 1:
                return {"ok": False, "to2": True, "k": k, "m": m}
            if even_child_pal_p(m, k) != pal_center_p(2 * m, k):
                return {"ok": False, "pe": True, "k": k, "m": m}
            if odd_child_pal_p(m, k) != pal_center_p(2 * m + 1, k):
                return {"ok": False, "po": True, "k": k, "m": m}
            if pal_center_p(2 * m, k) != even_s(2 * m, k) + 2:
                return {"ok": False, "ps": True, "k": k, "m": m}
            if pal_center_p(2 * m + 1, k) != even_s(2 * m + 1, k) + 2:
                return {"ok": False, "pso": True, "k": k, "m": m}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and odd_child_s(0, 3) == even_s(1, 3)
        and even_child_t(0, 3) == covering_t(3, 0)
        and odd_child_t(0, 3) == covering_t(3, 1)
        and odd_child_pal_p(0, 3) == covering_t(2, 0) * 2
        and want_even(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
        and PAT0011 in AND_ONES
        and and_clause(1, 1, 1, 0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pal_c_ap() -> dict:
    """k=3..13: pal-center tot is P(5U) xor P(U); period-8 dies at 13."""
    t_hi = Q * (1 << K_PAL)
    row = 1
    cand = []
    p_acc = 0
    p_at = [0]
    for t in range(0, t_hi):
        bit = bit_at(row, t) & bit_at(row, t + 1)
        cand.append(bit)
        if t % 2 == 1:
            p_acc ^= bit
            p_at.append(p_acc)
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
        tot = xe ^ xo
        pref = p_at[5 * u] ^ p_at[u]
        if pref != tot:
            return {"ok": False, "P": True, "k": k, "pref": pref, "tot": tot}
        # fold: xor cand(2t±1) over parent covering odd times
        up = 1 << (k - 1)
        fe = fo = 0
        tp = 2 * up + 1
        while tp <= Q * up - 1:
            fe ^= cand[2 * tp + 1]
            fo ^= cand[2 * tp - 1]
            tp += 2
        if fe != xe or fo != xo:
            return {"ok": False, "fold": True, "k": k, "fe": fe, "xe": xe}
        n_ok += 1
        rows[str(k)] = {"pal_c_e": xe, "pal_c_o": xo, "pal_c": tot, "P": pref}
    ok = (
        n_ok == K_PAL - 2
        and rows["3"]["pal_c_e"] == 1
        and rows["12"]["pal_c_e"] == 1
        and rows["12"]["pal_c_e"] != (12 % 2)
        and rows["13"]["pal_c_e"] == 0
        and rows["13"]["pal_c_o"] == 1
        and rows["13"]["pal_c"] == 1
        and rows["13"]["pal_c_e"] != want_pal_c_e_period8(13)
        and rows["13"]["pal_c"] != want_pal_c_tot_even_ge10(13)
        and want_pal_c_e_period8(3) == 1
        and want_pal_c_tot_even_ge10(12) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_PAL, "rows": rows}


def killed_local() -> dict:
    """cand(2t+1) is not a function of the 5-tuple around the centre."""
    t_hi = 2 * T_LOCAL + 4
    row = 1
    bits = []
    for t in range(0, t_hi):
        bits.append(row)
        row = rule30_step(row)
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(lambda: [0, 0])
    mixed = 0
    for t in range(2, T_LOCAL):
        r = bits[t]
        key = (
            bit_at(r, t - 1),
            bit_at(r, t),
            bit_at(r, t + 1),
            bit_at(r, t + 2),
            bit_at(r, t + 3),
        )
        r2 = bits[2 * t + 1]
        cand = bit_at(r2, 2 * t + 1) & bit_at(r2, 2 * t + 2)
        buckets[key][cand] += 1
    for v in buckets.values():
        if v[0] and v[1]:
            mixed += 1
    ok = mixed > 0 and len(buckets) == 32
    return {"ok": ok, "mixed": mixed, "n_key": len(buckets), "t_hi": T_LOCAL}


def killed_eq() -> dict:
    """period-8 pal_c_e; pal_c tot even>=10; odd corr for k<3."""
    ok = (
        want_pal_c_e_period8(13) == 1
        and want_pal_c_tot_even_ge10(13) == 0
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and covering_t(3, 1) == odd_child_t(0, 3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    sy = json.loads(SY_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    st = json.loads(ST_JSON.read_text())
    ok = (
        sy["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and st["checks"]["all_ok"]
        and sy["verdict"]["odd_pair_rest_eq_raw_k_ge_3"] == "LEMMA"
        and sy["verdict"]["odd_forced_corr_0_k_ge_3"] == "LEMMA"
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and st["verdict"]["pal_center_and_eq_next_center_and_right"] == "LEMMA"
        and st["verdict"]["pal_center_s_mod4"] == "LEMMA"
        and sy["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sy["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, ap, loc, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and ap["ok"] and loc["ok"] and kl["ok"]
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
    ap = pal_c_ap()
    loc = killed_local()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, ap, loc, kl, sc, pref)
    dump = {
        "cycle": "SZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pal_c_ap": {k: ap[k] for k in ap if k != "ok"},
        "killed_local": {k: loc[k] for k in loc if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_child_s_doubles_parent_s": True,
            "covering_t_2fold": True,
            "pal_c_tot_eq_P5U_xor_PU": True,
            "pal_c_e_period8": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_child_s_doubles_parent_s": "LEMMA",
            "covering_t_2fold": "LEMMA",
            "pal_c_tot_eq_P5U_xor_PU": "LEMMA",
            "pal_c_fold_cand_2t_pm1": "LEMMA",
            "pal_c_e_period8": "KILLED",
            "pal_c_tot_even_ge10": "KILLED",
            "pal_c_e_eq_k_mod2": "KILLED",
            "cand_2t_pm1_local_5bit": "KILLED",
            "pal_c_eq_ST": "KILLED",
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
        "pal_c k13 e",
        dump["pal_c_ap"]["rows"]["13"]["pal_c_e"],
        "o",
        dump["pal_c_ap"]["rows"]["13"]["pal_c_o"],
        "local mixed",
        dump["killed_local"]["mixed"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
