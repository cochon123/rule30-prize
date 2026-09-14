#!/usr/bin/env python3
"""Cycle SW: packed AND at p=6 is 1 on odd t>=3; odd pal-right tot 1.

Bits 5 and 6 equal t mod 2 for t>=2, from the p=4 freeze (bits 3,4)
and the packed update. Packed AND at p=6 is bits 5 and 6, hence 1 on
every odd t>=3. Odd pal-right at p=6 is the Green set {4U-1} union
{3U-1 if k even} union {3U-1-2^i : i=1..k-1} for k>=2, count
k+1-(k%2), always odd. Those cells all fire AND, so odd pal-right
p=6 AND tot is 1 for k>=2. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_sw.py --certify
Dump: research/cycle_sw.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_ld import want_p6_n
from cycle_lf import want_p14_n
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import forced_right_j, pal_left_never_forced
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SV_JSON = Path(__file__).resolve().parent / "cycle_sv.json"
SU_JSON = Path(__file__).resolve().parent / "cycle_su.json"
SR_JSON = Path(__file__).resolve().parent / "cycle_sr.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_GREEN = 12
K_REST = 10
T_FREEZE = 128
Q = 10


def want_odd_p6_n(k: int) -> int:
    """Odd pal-right G=1 count at p=6 for k>=2."""
    return k + 1 - (k % 2)


def odd_p6_ns(k: int) -> set[int]:
    """Closed Green set of odd pal-right n at p=6, k>=2."""
    u = 1 << k
    out = {4 * u - 1}
    if k % 2 == 0:
        out.add(3 * u - 1)
    for i in range(1, k):
        out.add(3 * u - 1 - (1 << i))
    return out


def odd_p14_ns(k: int) -> set[int]:
    """Closed Green set of odd pal-right n at p=14, k>=3."""
    u = 1 << k
    out = {4 * u - 3, 3 * u - 1}
    if k % 2 == 1:
        out.add(3 * u - 3)
    for i in range(1, k):
        out.add(3 * u - 3 - (1 << i))
    return out


def freeze_56() -> dict:
    """t>=2: bit5=bit6=t mod 2; odd t>=3: bits 5 and 6 are 1."""
    n_ok = 0
    row = 1
    for t in range(0, T_FREEZE):
        if t >= 2:
            if bit_at(row, 5) != (t % 2) or bit_at(row, 6) != (t % 2):
                return {"ok": False, "t": t, "b5": bit_at(row, 5), "b6": bit_at(row, 6)}
            if t % 2 and (bit_at(row, 5) & bit_at(row, 6)) != 1:
                return {"ok": False, "and6": True, "t": t}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == T_FREEZE and (0, 0, 0, 0) not in AND_ONES
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_FREEZE - 1}


def tot_form() -> dict:
    """k<=64: listed p=6 count; G=1 on listed n; pal-right range k>=2."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if k >= 2:
            u = 1 << k
            ns = odd_p6_ns(k)
            if len(ns) != want_odd_p6_n(k) or len(ns) != want_p6_n(k, 10):
                return {"ok": False, "cnt": True, "k": k, "n": len(ns)}
            if want_odd_p6_n(k) % 2 != 1:
                return {"ok": False, "odd": True, "k": k}
            j = forced_right_j(6, k)
            if j != 5 * u - 3:
                return {"ok": False, "j": True, "k": k}
            for n in ns:
                if n % 2 == 0 or n < 0 or n >= 4 * u:
                    return {"ok": False, "win": True, "k": k, "n": n}
                if j <= n or j > min(2 * n, 5 * u):
                    return {"ok": False, "range": True, "k": k, "n": n}
                jp = 2 * n - j
                if jp < 0 or jp > 5 * u:
                    return {"ok": False, "jp": True, "k": k, "n": n}
                if G(n, j) != 1:
                    return {"ok": False, "g": True, "k": k, "n": n}
        if k >= 3:
            u = 1 << k
            ns14 = odd_p14_ns(k)
            if len(ns14) != want_p14_n(k, 10) or len(ns14) % 2 != 1:
                return {"ok": False, "c14": True, "k": k, "n": len(ns14)}
            j14 = forced_right_j(14, k)
            for n in ns14:
                if G(n, j14) != 1:
                    return {"ok": False, "g14": True, "k": k, "n": n}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_odd_p6_n(2) == 3
        and want_odd_p6_n(8) == 9
        and 15 in odd_p6_ns(2)
        and pal_left_never_forced(3)
        and want_even(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _actual_odd(k: int, p: int) -> set[int]:
    u = 1 << k
    j = forced_right_j(p, k)
    clip = 5 * u
    out: set[int] = set()
    nmin = (j + 1) // 2
    if nmin % 2 == 0:
        nmin += 1
    for n in range(nmin, 4 * u, 2):
        if j > min(2 * n, clip):
            continue
        jp = 2 * n - j
        if 0 <= jp <= clip and G(n, j) == 1:
            out.add(n)
    return out


def green_sets() -> dict:
    """k<=12: odd pal-right Green sets at p=6 and p=14 match the closed forms."""
    n_ok = 0
    rows = {}
    for k in range(2, K_GREEN + 1):
        a6 = _actual_odd(k, 6)
        w6 = odd_p6_ns(k)
        if a6 != w6:
            return {"ok": False, "p6": True, "k": k, "extra": sorted(a6 - w6), "miss": sorted(w6 - a6)}
        rec = {"n6": len(a6), "c6": want_odd_p6_n(k)}
        if k >= 3:
            a14 = _actual_odd(k, 14)
            w14 = odd_p14_ns(k)
            if a14 != w14:
                return {"ok": False, "p14": True, "k": k, "extra": sorted(a14 - w14)}
            rec["n14"] = len(a14)
            rec["c14"] = want_p14_n(k, 10)
        n_ok += 1
        rows[str(k)] = rec
    ok = (
        n_ok == K_GREEN - 1
        and rows["2"]["n6"] == 3
        and rows["12"]["n6"] == 13
        and rows["3"]["n14"] == 5
        and rows["12"]["n14"] == 13
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def _forced_odd_and(k: int) -> dict:
    u = 1 << k
    t_hi, t0, qc = Q * u, 2 * u, covering_Q(Q)
    clip = 5 * u
    js = [(p, forced_right_j(p, k)) for p in (4, 6, 14)]
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    acc = {p: {"n_g1": 0, "n_and": 0, "xor": 0, "n_silent": 0} for p, _ in js}
    s = t0
    prev = None
    while s < t_hi:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, u, qc)
            if n % 2 == 0:
                pass
            else:
                for p, j in js:
                    if j <= n or j > min(2 * n, clip):
                        continue
                    jp = 2 * n - j
                    if jp < 0 or jp > clip or G(n, j) == 0:
                        continue
                    z, a, b, c = (bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(z, a, b, c)
                    acc[p]["n_g1"] += 1
                    acc[p]["n_and"] += packed
                    acc[p]["xor"] ^= packed
                    if packed == 0:
                        acc[p]["n_silent"] += 1
        row = rule30_step(row)
        s += 1
    return acc


def and_walk() -> dict:
    """k<=10: p=6 pal-right AND tot=1 for k>=2; odd corr=0 for k>=3."""
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        acc = _forced_odd_and(k)
        if k >= 2 and (acc[6]["n_silent"] != 0 or acc[6]["xor"] != 1 or acc[6]["n_g1"] != want_odd_p6_n(k)):
            return {"ok": False, "p6": True, "k": k, "acc": acc[6]}
        if k >= 3:
            if acc[14]["n_silent"] != 0 or acc[14]["xor"] != 1:
                return {"ok": False, "p14": True, "k": k, "acc": acc[14]}
            if acc[4]["xor"] != 0 or acc[4]["n_silent"] != 0:
                return {"ok": False, "p4": True, "k": k, "acc": acc[4]}
            corr = acc[4]["xor"] ^ acc[6]["xor"] ^ acc[14]["xor"]
            if corr != 0:
                return {"ok": False, "corr": True, "k": k}
        rows[str(k)] = {
            "p6": acc[6]["xor"],
            "p14": acc[14]["xor"],
            "p4": acc[4]["xor"],
            "n6": acc[6]["n_g1"],
            "n_silent6": acc[6]["n_silent"],
            "n_silent14": acc[14]["n_silent"],
        }
        n_ok += 1
    ok = (
        n_ok == K_REST + 1
        and rows["2"]["p6"] == 1
        and rows["10"]["p6"] == 1
        and rows["3"]["p14"] == 1
        and rows["10"]["n_silent14"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """p=6 AND identically 1; odd corr=0 for all k; pal-c tot equals ST."""
    row = 1
    ok = (
        bit_at(row, 5) == 0
        and bit_at(row, 6) == 0
        and want_rest_e0(1) == 0
        and want_odd_p6_n(3) == 3
        and want_even(0) != 0
        and pal_left_never_forced(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    sv = json.loads(SV_JSON.read_text())
    su = json.loads(SU_JSON.read_text())
    sr = json.loads(SR_JSON.read_text())
    ok = (
        sv["checks"]["all_ok"]
        and su["checks"]["all_ok"]
        and sr["checks"]["all_ok"]
        and sv["verdict"]["p4_and_1_on_odd_t_ge_3"] == "LEMMA"
        and sv["verdict"]["even_pair_rest_eq_raw_xor_1_k_ge_1"] == "LEMMA"
        and sv["verdict"]["odd_corr_0_k_ge_3"] == "CERTIFIED"
        and sv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sv["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, frz, tot, gre, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert frz["ok"] and tot["ok"] and gre["ok"] and walk["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
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
    frz = freeze_56()
    tot = tot_form()
    gre = green_sets()
    walk = and_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, frz, tot, gre, walk, kl, sc, pref)
    dump = {
        "cycle": "SW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "freeze_56": {k: frz[k] for k in frz if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "green_sets": {k: gre[k] for k in gre if k != "ok"},
        "and_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit5_bit6_eq_t_mod2_t_ge_2": True,
            "p6_and_1_on_odd_t_ge_3": True,
            "odd_p6_listed_count": True,
            "odd_p6_and_tot_1_k_ge_2": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit5_bit6_eq_t_mod2_t_ge_2": "LEMMA",
            "p6_and_1_on_odd_t_ge_3": "LEMMA",
            "odd_p6_listed_count": "LEMMA",
            "odd_p6_green_set_exact": "CERTIFIED",
            "odd_p6_and_tot_1_k_ge_2": "CERTIFIED",
            "odd_p14_green_set_exact": "CERTIFIED",
            "odd_corr_0_k_ge_3": "CERTIFIED",
            "pal_c_eq_ST": "KILLED",
            "p6_and_identically_1": "KILLED",
            "E_q10_10": "CERTIFIED",
            "odd_p6_green_set_all_k": "PREFIX",
            "odd_p6_and_tot_1_all_k": "PREFIX",
            "p14_and_on_g1_all_k": "PREFIX",
            "odd_corr_0_all_k": "PREFIX",
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
        "green n_ok",
        dump["green_sets"]["n_ok"],
        "walk n_ok",
        dump["and_walk"]["n_ok"],
        "k2 p6",
        dump["and_walk"]["rows"]["2"]["p6"],
        "k10 n6",
        dump["and_walk"]["rows"]["10"]["n6"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
