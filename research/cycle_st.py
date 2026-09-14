#!/usr/bin/env python3
"""Cycle ST: pal-center packed AND is next-row center AND right neighbor.

Covering pal-center j=n has packed p=s+2 on even snapshot
s=10U-2n-2. Cycle HH packed AND is odd-s bits p and p-1, so
AND = c_{s+1} and x(s+1,1). For k>=3 min pal-center p=2U+2>=18,
never forced, so pal-center rest bit equals that AND. Time
residues for k>=1: even n at s mod 4 = 2 in [2U+2, 10U-2];
odd n at s mod 4 = 0 in [2U, 10U-4]. Not pal-center tot equals
S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_st.py --certify
Dump: research/cycle_st.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sr import pal_center_count
from cycle_ss import even_s, packed_p
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SS_JSON = Path(__file__).resolve().parent / "cycle_ss.json"
SR_JSON = Path(__file__).resolve().parent / "cycle_sr.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_REST = 10
Q = 10


def pal_center_p(n: int, k: int) -> int:
    """Packed column of covering pal-center j=n."""
    return packed_p(n, k)


def pal_center_and(row_odd: int, s_even: int) -> int:
    """Packed AND at pal-center: c_{s+1} and x(s+1,1)."""
    return bit_at(row_odd, s_even + 1) & bit_at(row_odd, s_even + 2)


def min_pal_center_p(k: int) -> int:
    """Largest covering n=4U-1: p=2U+2."""
    return 2 * (1 << k) + 2


def pal_center_never_forced(k: int) -> bool:
    """k>=3: min pal-center p sits past {4,6,14}."""
    return k >= 3 and min_pal_center_p(k) > max(FORCED)


def pal_center_s_mod4(n: int, k: int) -> int:
    return even_s(n, k) % 4


def t0_center_right() -> dict:
    """t=0: c_0=1 and x(0,1)=0, so AND is not the center bit alone."""
    row = 1
    ok = bit_at(row, 0) == 1 and bit_at(row, 1) == 0 and pal_center_and(row, -1) == 0
    return {"ok": ok, "c0": bit_at(row, 0), "x01": bit_at(row, 1)}


def tot_form() -> dict:
    """k<=64: pal-center p=s+2; min p=2U+2; residues; never forced k>=3."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if pal_center_count(k) != 2 * u:
            return {"ok": False, "count": True, "k": k}
        if min_pal_center_p(k) != 2 * u + 2:
            return {"ok": False, "minp": True, "k": k}
        if pal_center_never_forced(k) != (k >= 3):
            return {"ok": False, "forced": True, "k": k}
        if k >= 3 and min_pal_center_p(k) <= 14:
            return {"ok": False, "past": True, "k": k}
        sample_n = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for n in sample_n:
            if n < 0 or n >= 4 * u:
                continue
            s = even_s(n, k)
            p = pal_center_p(n, k)
            if p != s + 2 or p != packed_p(n, k):
                return {"ok": False, "p": True, "k": k, "n": n, "p": p, "s": s}
            if n == 4 * u - 1 and p != min_pal_center_p(k):
                return {"ok": False, "nmax": True, "k": k, "p": p}
            if n == 0 and p != Q * u:
                return {"ok": False, "n0": True, "k": k, "p": p}
            if k >= 1:
                want_m = 2 if n % 2 == 0 else 0
                if pal_center_s_mod4(n, k) != want_m:
                    return {"ok": False, "mod": True, "k": k, "n": n}
                lo = 2 * u + 2 if n % 2 == 0 else 2 * u
                hi = Q * u - 2 if n % 2 == 0 else Q * u - 4
                if s < lo or s > hi:
                    return {"ok": False, "band": True, "k": k, "n": n, "s": s}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and pal_center_never_forced(3)
        and not pal_center_never_forced(2)
        and min_pal_center_p(0) == 4
        and min_pal_center_p(1) == 6
        and min_pal_center_p(2) == 10
        and pal_center_p(13, 2) == 14
        and pal_center_p(7, 1) == 6
        and pal_center_p(3, 0) == 4
        and pal_center_count(10) == 2048
        and (0, 0, 0, 0) not in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _walk_pal_c(k: int) -> dict:
    """Pal-center-only covering walk: AND equals next center and right."""
    U = 1 << k
    T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    acc = {
        par: {"pal_c": 0, "n_pal": 0, "n_pal_and": 0, "n_eq": 0}
        for par in (0, 1)
    }
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Qc)
            par = n % 2
            pcol = pal_center_p(n, k)
            s_even = s - 1
            if pcol != s_even + 2 or s_even != even_s(n, k):
                return {
                    "ok": False,
                    "clock": True,
                    "k": k,
                    "n": n,
                    "s": s,
                    "pcol": pcol,
                }
            if k >= 1:
                want_m = 2 if par == 0 else 0
                if s_even % 4 != want_m:
                    return {"ok": False, "mod": True, "k": k, "n": n, "s": s_even}
            if k >= 3 and pcol in FORCED:
                return {"ok": False, "forced": True, "k": k, "n": n, "p": pcol}
            z, aa, b, c = (bit_at(prev, pcol - 3 + i) for i in range(4))
            packed = and_clause(z, aa, b, c)
            hh = bit_at(row, pcol) & bit_at(row, pcol - 1)
            neigh = pal_center_and(row, s_even)
            if packed != hh or packed != neigh or packed != and_from_tuple(z, aa, b, c):
                return {
                    "ok": False,
                    "and": True,
                    "k": k,
                    "n": n,
                    "packed": packed,
                    "hh": hh,
                    "neigh": neigh,
                }
            rest = int(bool(packed) and pcol not in FORCED)
            a = acc[par]
            a["pal_c"] ^= rest
            a["n_pal"] += 1
            a["n_pal_and"] += rest
            a["n_eq"] += 1
        row = rule30_step(row)
        s += 1
    for par in (0, 1):
        if acc[par]["n_pal"] != pal_center_count(k):
            return {"ok": False, "count": True, "k": k, "par": par, "r": acc[par]}
        if acc[par]["n_eq"] != pal_center_count(k):
            return {"ok": False, "eq": True, "k": k, "par": par, "r": acc[par]}
    acc["ok"] = True
    return acc


def pal_center_walk() -> dict:
    """k<=10 pal-centers: AND = c_{s+1} and x(s+1,1); match SR pal_c tots."""
    sr = json.loads(SR_JSON.read_text())
    sr_rows = sr["fold_split"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        acc = _walk_pal_c(k)
        if not acc.get("ok"):
            return acc
        for par in (0, 1):
            r = acc[par]
            if r["n_pal"] != pal_center_count(k) or r["n_eq"] != r["n_pal"]:
                return {"ok": False, "n": True, "k": k, "par": par, "r": r}
        e, o = acc[0], acc[1]
        want = sr_rows[str(k)]
        if (
            e["pal_c"] != want["pal_c_e"]
            or o["pal_c"] != want["pal_c_o"]
            or e["n_pal_and"] != want["n_pal_and_e"]
            or o["n_pal_and"] != want["n_pal_and_o"]
        ):
            return {"ok": False, "sr": True, "k": k, "e": e, "o": o, "want": want}
        n_ok += 1
        rows[str(k)] = {
            "pal_c_e": e["pal_c"],
            "pal_c_o": o["pal_c"],
            "n_pal_and_e": e["n_pal_and"],
            "n_pal_and_o": o["n_pal_and"],
            "n_pal": e["n_pal"],
        }
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["pal_c_e"] == 0
        and rows["0"]["pal_c_o"] == 0
        and rows["1"]["pal_c_e"] == 1
        and rows["1"]["n_pal_and_e"] == 1
        and rows["6"]["pal_c_e"] == 0
        and rows["10"]["pal_c_e"] == 0
        and rows["10"]["pal_c_o"] == 1
        and pal_center_never_forced(3)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """pal-c tot equals ST; AND identically 0; AND equals center alone."""
    ok = (
        want_even(0) != 0
        and want_rest_e0(1) == 0
        and want_rest_e0(6) == 1
        and pal_center_count(1) == 4
        and bit_at(1, 0) == 1
        and bit_at(1, 1) == 0
        and pal_center_and(1, -1) != bit_at(1, 0)
        and and_from_tuple(0, 0, 0, 0) == 0
        and not pal_center_never_forced(2)
    )
    return {"ok": ok}


def prefixes() -> dict:
    ss = json.loads(SS_JSON.read_text())
    sr = json.loads(SR_JSON.read_text())
    ok = (
        ss["checks"]["all_ok"]
        and sr["checks"]["all_ok"]
        and ss["verdict"]["unpaired_packed_and_0_all_k"] == "LEMMA"
        and ss["verdict"]["rest_eq_pal_c_xor_pair_mis_all_k"] == "LEMMA"
        and ss["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ss["verdict"]["pal_c_eq_ST"] == "KILLED"
        and ss["verdict"]["prize"] == "unsolved"
        and sr["verdict"]["rest_eq_pal_c_xor_pair_mis_k_le_10"] == "CERTIFIED"
        and want_even(7) == 1
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, t0, tot, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert t0["ok"] and tot["ok"] and walk["ok"] and kl["ok"]
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
    t0c = t0_center_right()
    tot = tot_form()
    walk = pal_center_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, t0c, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "ST",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "t0_center_right": {k: t0c[k] for k in t0c if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pal_center_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pal_center_and_eq_next_center_and_right": True,
            "pal_center_p_eq_s_plus_2": True,
            "pal_center_never_forced_k_ge_3": True,
            "pal_center_s_mod4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pal_center_and_eq_next_center_and_right": "LEMMA",
            "pal_center_p_eq_s_plus_2": "LEMMA",
            "pal_center_never_forced_k_ge_3": "LEMMA",
            "pal_center_s_mod4": "LEMMA",
            "pal_c_eq_ST": "KILLED",
            "pal_c_and_identically_0": "KILLED",
            "pal_c_and_eq_center_alone": "KILLED",
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
        "walk n_ok",
        dump["pal_center_walk"]["n_ok"],
        "k0 pal_c_e",
        dump["pal_center_walk"]["rows"]["0"]["pal_c_e"],
        "k10 pal_c_o",
        dump["pal_center_walk"]["rows"]["10"]["pal_c_o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
