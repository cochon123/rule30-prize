#!/usr/bin/env python3
"""Cycle SV: even pal-pair rest is raw xor 1 for k>=1 (unique p=4).

Pal-left packed p exceeds pal-center min 2U+2, so pal-left is never
forced for k>=3. Even n only meets forced pal-right at p=4, j=5U-2.
That Green cell is unique: n=3U-2. Packed AND at p=4 is bits 3 and 4
on the odd row; bit 4 is 1 for t>=2 and bit 3 equals t mod 2 for
t>=2, so AND=1 on every odd t>=3. Even pal-pair rest tot is therefore
raw spat-mismatch xor 1 for every k>=1. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sv.py --certify
Dump: research/cycle_sv.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s, packed_p
from cycle_st import min_pal_center_p, pal_center_never_forced
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SU_JSON = Path(__file__).resolve().parent / "cycle_su.json"
SR_JSON = Path(__file__).resolve().parent / "cycle_sr.json"
ST_JSON = Path(__file__).resolve().parent / "cycle_st.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_GREEN = 12
K_REST = 10
T_FREEZE = 128
Q = 10


def forced_right_j(p: int, k: int) -> int:
    """Packed p=10U-2j, so j=(10U-p)//2."""
    return (Q * (1 << k) - p) // 2


def unique_even_n(k: int) -> int:
    """Even covering pal-right at p=4: n=3U-2."""
    return 3 * (1 << k) - 2


def pal_left_never_forced(k: int) -> bool:
    return pal_center_never_forced(k)


def freeze_left() -> dict:
    """t>=2: bit2=0, bit3=t mod 2, bit4=1; t>=1: bits 0,1 are 1."""
    n_ok = 0
    row = 1
    for t in range(0, T_FREEZE):
        if t >= 1 and (bit_at(row, 0) != 1 or bit_at(row, 1) != 1):
            return {"ok": False, "lo": True, "t": t}
        if t >= 2:
            if bit_at(row, 2) != 0 or bit_at(row, 4) != 1:
                return {"ok": False, "b24": True, "t": t}
            if bit_at(row, 3) != (t % 2):
                return {"ok": False, "b3": True, "t": t}
            if t % 2 and (bit_at(row, 3) & bit_at(row, 4)) != 1:
                return {"ok": False, "and4": True, "t": t}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == T_FREEZE and (0, 0, 0, 0) not in AND_ONES
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_FREEZE - 1}


def tot_form() -> dict:
    """k<=64: pal-left bound; unique even n=3U-2; G=1; q-range unique k>=3."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if forced_right_j(4, k) != 5 * u - 2:
            return {"ok": False, "j4": True, "k": k}
        if forced_right_j(6, k) != 5 * u - 3:
            return {"ok": False, "j6": True, "k": k}
        if forced_right_j(14, k) != 5 * u - 7:
            return {"ok": False, "j14": True, "k": k}
        if pal_left_never_forced(k) != (k >= 3):
            return {"ok": False, "left": True, "k": k}
        if k >= 3 and min_pal_center_p(k) <= max(FORCED):
            return {"ok": False, "minp": True, "k": k}
        if k >= 1:
            n = unique_even_n(k)
            j = forced_right_j(4, k)
            if n != 3 * u - 2 or n % 2 != 0:
                return {"ok": False, "n": True, "k": k}
            if n >= 4 * u or j <= n or j > min(2 * n, 5 * u):
                return {"ok": False, "range": True, "k": k, "n": n, "j": j}
            jp = 2 * n - j
            if jp < 0 or jp > 5 * u:
                return {"ok": False, "jp": True, "k": k}
            if packed_p(j, k) != 4:
                return {"ok": False, "p": True, "k": k}
            if G(n, j) != 1:
                return {"ok": False, "g": True, "k": k}
            s = even_s(n, k)
            if s != 4 * u + 2:
                return {"ok": False, "s": True, "k": k, "s": s}
            if (s + 1) % 2 != 1:
                return {"ok": False, "odd": True, "k": k}
        if k >= 3:
            b = k - 2
            tmin = 5 * u // 8
            tmax = u - 1
            hits = []
            qmin = (tmin + 1 + (1 << b) - 1) >> b
            qmax = (tmax + 1) >> b
            for q in range(qmin, qmax + 1):
                if q % 2 == 0:
                    continue
                a = q * (1 << b) - 1
                if tmin <= a <= tmax:
                    hits.append(q)
            if hits != [3]:
                return {"ok": False, "q": True, "k": k, "hits": hits}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and unique_even_n(1) == 4
        and unique_even_n(10) == 3070
        and G(4, 8) == 1
        and pal_left_never_forced(3)
        and not pal_left_never_forced(2)
        and want_even(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def green_unique() -> dict:
    """k<=12 even covering pal-right at j=5U-2 is only n=3U-2."""
    n_ok = 0
    rows = {}
    for k in range(1, K_GREEN + 1):
        u = 1 << k
        j = forced_right_j(4, k)
        want = unique_even_n(k)
        hits = []
        for n in range(0, 4 * u, 2):
            if j <= n or j > min(2 * n, 5 * u):
                continue
            jp = 2 * n - j
            if jp < 0 or jp > 5 * u:
                continue
            if G(n, j) == 1:
                hits.append(n)
        if hits != [want] or G(want, j) != 1:
            return {"ok": False, "k": k, "hits": hits, "want": want}
        n_ok += 1
        rows[str(k)] = {"n": want, "j": j, "n_hit": 1}
    ok = (
        n_ok == K_GREEN
        and rows["1"]["n"] == 4
        and rows["10"]["n"] == 3070
        and rows["12"]["n"] == 12286
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def _forced_and(k: int) -> dict:
    """Packed AND on forced pal-right G=1 cells, split by n parity."""
    u = 1 << k
    t_hi, t0, qc = Q * u, 2 * u, covering_Q(Q)
    clip = 5 * u
    js = [(p, forced_right_j(p, k)) for p in (4, 6, 14)]
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    acc = {
        par: {"corr": 0, "n_fr": 0, "and_p": {str(p): 0 for p, _ in js}, "n_p": {str(p): 0 for p, _ in js}}
        for par in (0, 1)
    }
    s = t0
    prev = None
    while s < t_hi:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, u, qc)
            par = n % 2
            for p, j in js:
                if par == 0 and j % 2:
                    continue
                if j <= n or j > min(2 * n, clip):
                    continue
                jp = 2 * n - j
                if jp < 0 or jp > clip or G(n, j) == 0:
                    continue
                z, a, b, c = (bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(z, a, b, c)
                if p == 4 and packed != 1:
                    return {"ok": False, "and4": True, "k": k, "n": n}
                aacc = acc[par]
                aacc["n_fr"] += 1
                aacc["n_p"][str(p)] += 1
                aacc["and_p"][str(p)] ^= packed
                aacc["corr"] ^= packed
        row = rule30_step(row)
        s += 1
    return {"ok": True, "acc": acc}


def forced_and_walk() -> dict:
    """k<=10: even corr=1 for k>=1; odd corr=0 for k>=3."""
    sr = json.loads(SR_JSON.read_text())
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        got = _forced_and(k)
        if not got.get("ok"):
            return got
        e, o = got["acc"][0], got["acc"][1]
        if k >= 1 and (e["corr"] != 1 or e["n_p"]["4"] != 1 or e["n_p"]["6"] != 0 or e["n_p"]["14"] != 0):
            return {"ok": False, "even": True, "k": k, "e": e}
        if k >= 3 and o["corr"] != 0:
            return {"ok": False, "odd": True, "k": k, "o": o}
        if k == 0 and (e["corr"] != 0 or e["n_fr"] != 0):
            return {"ok": False, "k0": True, "e": e}
        sr_row = sr["fold_split"]["rows"][str(k)]
        rows[str(k)] = {
            "corr_e": e["corr"],
            "corr_o": o["corr"],
            "n_fr_e": e["n_fr"],
            "n_fr_o": o["n_fr"],
            "pair_e": sr_row["pair_e"],
            "pair_o": sr_row["pair_o"],
        }
        n_ok += 1
    ok = (
        n_ok == K_REST + 1
        and rows["1"]["corr_e"] == 1
        and rows["10"]["corr_e"] == 1
        and rows["3"]["corr_o"] == 0
        and rows["10"]["corr_o"] == 0
        and rows["1"]["pair_e"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """even pair rest equals raw; pal-c tot equals ST; p=4 AND at t=0."""
    ok = (
        want_even(0) != 0
        and want_rest_e0(1) == 0
        and unique_even_n(1) == 4
        and bit_at(1, 3) == 0
        and bit_at(1, 4) == 0
        and forced_right_j(4, 0) % 2 == 1
        and not pal_left_never_forced(2)
        and pal_left_never_forced(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    su = json.loads(SU_JSON.read_text())
    st = json.loads(ST_JSON.read_text())
    sr = json.loads(SR_JSON.read_text())
    ok = (
        su["checks"]["all_ok"]
        and st["checks"]["all_ok"]
        and sr["checks"]["all_ok"]
        and su["verdict"]["covering_and_eq_spat_2d"] == "LEMMA"
        and su["verdict"]["pair_raw_eq_spat_d_xor_minus_d"] == "LEMMA"
        and st["verdict"]["pal_center_never_forced_k_ge_3"] == "LEMMA"
        and su["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and su["verdict"]["prize"] == "unsolved"
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
    frz = freeze_left()
    tot = tot_form()
    gre = green_unique()
    walk = forced_and_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, frz, tot, gre, walk, kl, sc, pref)
    dump = {
        "cycle": "SV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "freeze_left": {k: frz[k] for k in frz if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "green_unique": {k: gre[k] for k in gre if k != "ok"},
        "forced_and_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pal_left_never_forced_k_ge_3": True,
            "unique_even_p4_n_eq_3u_minus_2": True,
            "p4_and_1_on_odd_t_ge_3": True,
            "even_pair_rest_eq_raw_xor_1_k_ge_1": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pal_left_never_forced_k_ge_3": "LEMMA",
            "unique_even_p4_n_eq_3u_minus_2": "LEMMA",
            "p4_and_1_on_odd_t_ge_3": "LEMMA",
            "even_pair_rest_eq_raw_xor_1_k_ge_1": "LEMMA",
            "odd_corr_0_k_ge_3": "CERTIFIED",
            "pal_c_eq_ST": "KILLED",
            "even_pair_rest_eq_raw": "KILLED",
            "p4_and_identically_1": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
            "odd_corr_0_all_k": "PREFIX",
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
        dump["green_unique"]["n_ok"],
        "walk n_ok",
        dump["forced_and_walk"]["n_ok"],
        "k1 corr_e",
        dump["forced_and_walk"]["rows"]["1"]["corr_e"],
        "k10 corr_o",
        dump["forced_and_walk"]["rows"]["10"]["corr_o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
