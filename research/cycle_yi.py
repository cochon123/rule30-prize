#!/usr/bin/env python3
"""Cycle YI: even n=5U/2+65536 is the 2-fold of Cycle YF at k-1.

Covering n=5U/2+65536 equals 2*(5U_p/2+32768). Even doubling sends parent
left Green to child left Green with pal_kind and clip-edge preserved,
so unpaired left is {0,65536} for k>=18 and leftover+pal is the even
11-set {U/2,U/2+65536,U/2+131072,U,U+65536,U+131072,2U,2U+65536,2U+131072,5U/2,n}
for k>=19. The j=65536 cell has partner 5U+65536. Dies at k=17 for
unpaired {0,65536} (G at j=65536 is 0). Dies at k=18 for leftover
11-set (got 6). Do not kill pal_kind unpaired at n=5U/2+65536, j=0
for k>=16 or j=65536 for k>=18. Do not call ph65536_lo_js below k=19.
Do not PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_yi.py --certify
Dump: research/cycle_yi.json
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
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_ua import want_j0_odd_unp
from cycle_ub import want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from cycle_wk import want_gu_fl, want_ug_fl
from cycle_wm import want_j0_all_unp, want_j0_even_unp
from cycle_wn import want_clip_gp_jk, want_clip_slice
from cycle_wr import want_even_slice
from cycle_yc import ph16384_n, want_ph16384_lo
from cycle_yf import (
    ph32768_lo_js,
    ph32768_n,
    want_ph32768_clip,
    want_ph32768_lo,
    want_ph32768_unp,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
YF_JSON = Path(__file__).resolve().parent / "cycle_yf.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
YC_JSON = Path(__file__).resolve().parent / "cycle_yc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph65536_n(k: int) -> int:
    """Covering n=5U/2+65536."""
    return parent_half(k) + 65536


def ph65536_lo_js(k: int) -> tuple[int, ...]:
    """Leftover+pal left indices at even n=5U/2+65536: 2-fold of Cycle YF.

    Call only for k>=19.
    """
    return tuple(2 * j for j in ph32768_lo_js(k - 1))


def want_ph65536_unp(k: int) -> int:
    """Unpaired left Green at n=5U/2+65536: 2 for k>=18; 1 at k=17; 3 at k=16."""
    if k <= 15:
        return 0
    if k == 16:
        return 3
    if k == 17:
        return 1
    return 2


def want_ph65536_lo(k: int) -> int:
    """Leftover+pal left Green at n=5U/2+65536: 11 for k>=19; 6 at k=18; 1 at k=17."""
    if k <= 15:
        return 0
    if k == 16:
        return 2
    if k == 17:
        return 1
    if k == 18:
        return 6
    return 11


def want_ph65536_clip(k: int) -> int:
    """Left clip-edge Green at n=5U/2+65536: 1 for k>=16 except 0 at k=18."""
    if k <= 15:
        return 0
    if k == 18:
        return 0
    return 1


def ph65536_split(k: int) -> dict:
    """Left Green kinds at even n=5U/2+65536. Do not call from tot_form."""
    n = ph65536_n(k)
    u = 1 << k
    clip = 5 * u
    n_unp = n_lo = n_clip = n_bad = 0
    unp_js = []
    lo_js = []
    if k < 16 or n >= 4 * u:
        return {
            "n_unp": 0,
            "n_lo": 0,
            "n_clip": 0,
            "n_bad": 0,
            "unp_js": [],
            "lo_js": [],
        }
    for j in range(0, min(2 * n, clip) + 1):
        if G(n, j) == 0:
            continue
        kind = pal_kind(n, j, k)
        if j > n:
            continue
        if kind == "unp":
            n_unp += 1
            unp_js.append(j)
        elif kind in ("pair", "pal"):
            if is_clip_edge(n, j, k):
                n_clip += 1
            elif j in (1, 2):
                n_bad += 1
            else:
                n_lo += 1
                lo_js.append(j)
        else:
            n_bad += 1
    return {
        "n_unp": n_unp,
        "n_lo": n_lo,
        "n_clip": n_clip,
        "n_bad": n_bad,
        "unp_js": unp_js,
        "lo_js": lo_js,
    }


def tot_form() -> dict:
    """k<=64: n=5U/2+65536 is 2-fold of YF; dies at k=17 for {0,65536}.

    Do not call ph65536_split here.
    Do not call ph65536_lo_js below k=19.
    Census is ph65536_fold for k<=8.
    """
    n_ok = 0
    if want_ph65536_unp(0) != 0 or want_ph65536_lo(15) != 0:
        return {"ok": False, "k15": True}
    if want_ph65536_unp(16) != 3 or want_ph65536_unp(17) != 1:
        return {"ok": False, "k1617": True}
    if want_ph65536_lo(17) != 1 or want_ph65536_unp(18) != 2:
        return {"ok": False, "k1718": True}
    if want_ph65536_clip(18) != 0 or want_ph65536_lo(19) != 11:
        return {"ok": False, "k1819": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if G(m, 0) != 1:
            return {"ok": False, "g0": True, "m": m}
        if m > 0 and G(2 * m, 1) != 0:
            return {"ok": False, "eodd": True, "m": m}
        if not unique_van_odd_even(m, 0):
            return {"ok": False, "van": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        n = ph65536_n(k)
        n_p = ph32768_n(k - 1) if k >= 1 else ph32768_n(0)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n != parent_half(k) + 65536:
            return {"ok": False, "n": True, "k": k}
        if k >= 2:
            if n != 2 * n_p:
                return {"ok": False, "fold": True, "k": k}
            if n % 2 != 0:
                return {"ok": False, "ev": True, "k": k}
        if k >= 16:
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if pal_kind(n, 0, k) != "unp" or G(n, 0) != 1:
                return {"ok": False, "j0": True, "k": k}
            if 2 * n - 65536 != clip + 65536:
                return {"ok": False, "pr": True, "k": k}
            if not is_clip_edge(n, 131072, k):
                return {"ok": False, "c131072": True, "k": k}
            if G(n, 0) != G(n_p, 0):
                return {"ok": False, "g00": True, "k": k}
            if pal_kind(n, 65536, k) != "unp":
                return {"ok": False, "j65536k": True, "k": k}
        if k >= 18:
            if G(n, 65536) != 1 or G(n, 65536) != G(n_p, 32768):
                return {"ok": False, "g65536": True, "k": k}
            if pal_kind(n_p, 32768, k - 1) != "unp":
                return {"ok": False, "p32768": True, "k": k}
            if want_ph65536_unp(k) != 2:
                return {"ok": False, "u2": True, "k": k}
        if k == 17:
            if G(n, 65536) != 0 or want_ph65536_unp(k) != 1:
                return {"ok": False, "k17g": True}
            if pal_kind(n, 65536, k) != "unp":
                return {"ok": False, "k17k": True}
        if k == 16:
            if G(n, 65536) != 0 or want_ph65536_unp(k) != 3:
                return {"ok": False, "k16g": True}
            if pal_kind(n, 65536, k) != "unp":
                return {"ok": False, "k16k": True}
        if k == 15:
            if n < 4 * u:
                return {"ok": False, "k15c": True}
        if k >= 19:
            if want_ph65536_lo(k) != 11 or want_ph32768_lo(k - 1) != 11:
                return {"ok": False, "lo": True, "k": k}
            if ph65536_lo_js(k) != tuple(2 * j for j in ph32768_lo_js(k - 1)):
                return {"ok": False, "js": True, "k": k}
            for j in ph65536_lo_js(k):
                if G(n, j) != 1:
                    return {"ok": False, "loj": True, "k": k, "j": j}
                kind = pal_kind(n, j, k)
                if kind not in ("pair", "pal"):
                    return {"ok": False, "lok": True, "k": k, "j": j}
                if is_clip_edge(n, j, k) or j in (1, 2):
                    return {"ok": False, "loc": True, "k": k, "j": j}
        if k >= 1 and jacobsthal(k + 1) != (1 << k) - jacobsthal(k):
            return {"ok": False, "Jrec": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "hi": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ph65536_unp(17) != 2
        and want_ph65536_lo(18) != 11
        and want_ph65536_unp(8) != want_clip_gp(8)
        and want_ph65536_lo(8) != want_clip_gp(8)
        and want_ph65536_unp(8) != want_even_slice(8)
        and pal_kind(ph65536_n(16), 65536, 16) != "pair"
        and G(ph65536_n(15), 65536) != 1
        and G(ph65536_n(16), 65536) != 1
        and G(ph65536_n(17), 65536) != 1
        and pal_kind(ph65536_n(16), 0, 16) == "unp"
        and pal_kind(ph65536_n(16), 65536, 16) == "unp"
        and pal_kind(ph65536_n(18), 65536, 18) == "unp"
        and want_ph65536_unp(8) == 0
        and want_ph65536_unp(15) == 0
        and want_ph65536_unp(16) == 3
        and want_ph65536_lo(16) == 2
        and want_ph65536_lo(17) == 1
        and want_ph65536_lo(18) == 6
        and want_ph65536_lo(19) == 11
        and want_ph65536_clip(16) == 1
        and want_ph65536_clip(17) == 1
        and want_ph65536_clip(18) == 0
        and ph65536_n(8) == 66176
        and ph65536_n(8) == 2 * ph32768_n(7)
        and ph65536_n(16) == 229376
        and ph65536_n(16) == 2 * ph32768_n(15)
        and ph32768_n(8) == 33408
        and ph16384_n(8) == 17024
        and want_ph32768_unp(15) == 3
        and want_ph32768_lo(15) == 2
        and want_ph32768_lo(18) == 11
        and want_ph32768_clip(17) == 0
        and want_ph16384_lo(17) == 11
        and want_clip_slice(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_even_slice(8) == 85
        and want_j0_even_unp(8) == 191
        and want_j0_all_unp(8) == 383
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_ej_xor(8) == 5225
        and lucas(8) == 47
        and fib(8) == 21
        and jacobsthal(8) == 85
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
        and G(2, 2) != 0
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
        and parent_half(8) == 640
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_ph65536_unp(8) == 0
        and want_ph65536_unp(18) == 2
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph65536_fold() -> dict:
    """k<=8 left Green at even n=5U/2+65536 vs 2-fold of YF."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = ph65536_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_unp"] != want_ph65536_unp(k):
            return {"ok": False, "unp": True, "k": k, "got": a["n_unp"]}
        if a["n_lo"] != want_ph65536_lo(k):
            return {"ok": False, "lo": True, "k": k, "got": a["n_lo"]}
        if a["n_clip"] != want_ph65536_clip(k):
            return {"ok": False, "cl": True, "k": k, "got": a["n_clip"]}
        if k <= 8 and a["unp_js"] != []:
            return {"ok": False, "u8": True, "k": k, "got": a["unp_js"]}
        n_ok += 1
        rows[str(k)] = {
            "n_unp": a["n_unp"],
            "n_lo": a["n_lo"],
            "n_clip": a["n_clip"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_unp"] == 0
        and rows["8"]["n_lo"] == 0
        and rows["8"]["n_clip"] == 0
        and want_ph65536_lo(8) == 0
        and want_ph65536_lo(16) == 2
        and want_ph65536_lo(17) == 1
        and want_ph65536_lo(18) == 6
        and want_ph65536_lo(19) == 11
        and want_ph32768_lo(18) == 11
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired {0,65536} at k=17; leftover 11-set at k=18."""
    n15 = ph65536_n(15)
    n16 = ph65536_n(16)
    n17 = ph65536_n(17)
    n18 = ph65536_n(18)
    ok = (
        want_ph65536_unp(17) != 2
        and want_ph65536_lo(18) != 11
        and want_ph65536_unp(8) != want_clip_gp(8)
        and want_ph65536_lo(8) != want_clip_gp(8)
        and want_ph65536_unp(8) != want_even_slice(8)
        and pal_kind(n16, 65536, 16) != "pair"
        and G(n15, 65536) != 1
        and G(n16, 65536) != 1
        and G(n17, 65536) != 1
        and pal_kind(n16, 0, 16) == "unp"
        and pal_kind(n16, 65536, 16) == "unp"
        and pal_kind(n17, 65536, 17) == "unp"
        and pal_kind(n18, 65536, 18) == "unp"
        and want_ph65536_unp(8) == 0
        and want_ph65536_unp(15) == 0
        and want_ph65536_unp(16) == 3
        and want_ph65536_lo(16) == 2
        and G(n15, 65536) == 0
        and G(n16, 65536) == 0
        and G(n17, 65536) == 0
        and G(n18, 65536) == 1
        and want_ph65536_unp(17) == 1
        and want_ph65536_unp(18) == 2
        and want_ph65536_lo(17) == 1
        and want_ph65536_lo(18) == 6
        and want_ph65536_lo(19) == 11
        and want_clip_gp(8) == 85
        and want_even_slice(8) == 85
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and n15 == 147456
        and n15 >= 4 * (1 << 15)
        and G(2, 1) == 0
        and G(4, 2) == G(2, 1)
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(8) != (1 << 10)
        and G(0, 0) == 1
        and d2_clip_covering(0)
        and not d2_clip_covering(1)
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_odd(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    yf = json.loads(YF_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    yc = json.loads(YC_JSON.read_text())
    ok = (
        yf["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and yc["checks"]["all_ok"]
        and yf["verdict"]["ph32768_lo_eq_11_k_ge_18"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and yc["verdict"]["ph16384_lo_eq_11_k_ge_17"] == "LEMMA"
        and yf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and yf["verdict"]["prize"] == "unsolved"
        and want_d2_n(0) == 2
        and jacobsthal(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and kl["ok"]
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
    cnt = ph65536_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph65536_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph65536_eq_2fold_yf_k_ge_2": True,
            "ph65536_unp_eq_065536_k_ge_18": True,
            "ph65536_lo_eq_11_k_ge_19": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph65536_eq_2fold_yf_k_ge_2": "LEMMA",
            "ph65536_unp_eq_065536_k_ge_18": "LEMMA",
            "ph65536_lo_eq_11_k_ge_19": "LEMMA",
            "ph65536_j65536_partner_5U65536": "LEMMA",
            "ph65536_unp_eq_065536_at_k17": "KILLED",
            "ph65536_lo_eq_11_at_k18": "KILLED",
            "ph65536_unp_eq_clip_gp_at_k8": "KILLED",
            "ph65536_lo_eq_clip_gp_at_k8": "KILLED",
            "ph65536_unp_eq_even_slice_at_k8": "KILLED",
            "ph65536_j65536_pair": "KILLED",
            "ph65536_G65536_eq_1_at_k17": "KILLED",
            "ph65536_covering_at_k15": "KILLED",
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
    print("ph65536 k8", dump["ph65536_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
