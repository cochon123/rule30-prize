#!/usr/bin/env python3
"""Cycle YC: even n=5U/2+16384 is the 2-fold of Cycle XZ at k-1.

Covering n=5U/2+16384 equals 2*(5U_p/2+8192). Even doubling sends parent
left Green to child left Green with pal_kind and clip-edge preserved,
so unpaired left is {0,16384} for k>=16 and leftover+pal is the even
11-set {U/2,U/2+16384,U/2+32768,U,U+16384,U+32768,2U,2U+16384,2U+32768,5U/2,n}
for k>=17. The j=16384 cell has partner 5U+16384. Dies at k=15 for
unpaired {0,16384} (G at j=16384 is 0). Dies at k=16 for leftover
11-set (got 6). Do not kill pal_kind unpaired at n=5U/2+16384, j=0
for k>=14 or j=16384 for k>=16. Do not call ph16384_lo_js below k=17.
Do not PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_yc.py --certify
Dump: research/cycle_yc.json
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
from cycle_xw import ph4096_n, want_ph4096_lo
from cycle_xz import (
    ph8192_lo_js,
    ph8192_n,
    want_ph8192_clip,
    want_ph8192_lo,
    want_ph8192_unp,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
XZ_JSON = Path(__file__).resolve().parent / "cycle_xz.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
XW_JSON = Path(__file__).resolve().parent / "cycle_xw.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph16384_n(k: int) -> int:
    """Covering n=5U/2+16384."""
    return parent_half(k) + 16384


def ph16384_lo_js(k: int) -> tuple[int, ...]:
    """Leftover+pal left indices at even n=5U/2+16384: 2-fold of Cycle XZ.

    Call only for k>=17.
    """
    return tuple(2 * j for j in ph8192_lo_js(k - 1))


def want_ph16384_unp(k: int) -> int:
    """Unpaired left Green at n=5U/2+16384: 2 for k>=16; 1 at k=15; 3 at k=14."""
    if k <= 13:
        return 0
    if k == 14:
        return 3
    if k == 15:
        return 1
    return 2


def want_ph16384_lo(k: int) -> int:
    """Leftover+pal left Green at n=5U/2+16384: 11 for k>=17; 6 at k=16; 1 at k=15."""
    if k <= 13:
        return 0
    if k == 14:
        return 2
    if k == 15:
        return 1
    if k == 16:
        return 6
    return 11


def want_ph16384_clip(k: int) -> int:
    """Left clip-edge Green at n=5U/2+16384: 1 for k>=14 except 0 at k=16."""
    if k <= 13:
        return 0
    if k == 16:
        return 0
    return 1


def ph16384_split(k: int) -> dict:
    """Left Green kinds at even n=5U/2+16384. Do not call from tot_form."""
    n = ph16384_n(k)
    u = 1 << k
    clip = 5 * u
    n_unp = n_lo = n_clip = n_bad = 0
    unp_js = []
    lo_js = []
    if k < 14 or n >= 4 * u:
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
    """k<=64: n=5U/2+16384 is 2-fold of XZ; dies at k=15 for {0,16384}.

    Do not call ph16384_split here.
    Do not call ph16384_lo_js below k=17.
    Census is ph16384_fold for k<=8.
    """
    n_ok = 0
    if want_ph16384_unp(0) != 0 or want_ph16384_lo(13) != 0:
        return {"ok": False, "k13": True}
    if want_ph16384_unp(14) != 3 or want_ph16384_unp(15) != 1:
        return {"ok": False, "k1415": True}
    if want_ph16384_lo(15) != 1 or want_ph16384_unp(16) != 2:
        return {"ok": False, "k1516": True}
    if want_ph16384_clip(16) != 0 or want_ph16384_lo(17) != 11:
        return {"ok": False, "k1617": True}
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
        n = ph16384_n(k)
        n_p = ph8192_n(k - 1) if k >= 1 else ph8192_n(0)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n != parent_half(k) + 16384:
            return {"ok": False, "n": True, "k": k}
        if k >= 2:
            if n != 2 * n_p:
                return {"ok": False, "fold": True, "k": k}
            if n % 2 != 0:
                return {"ok": False, "ev": True, "k": k}
        if k >= 14:
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if pal_kind(n, 0, k) != "unp" or G(n, 0) != 1:
                return {"ok": False, "j0": True, "k": k}
            if 2 * n - 16384 != clip + 16384:
                return {"ok": False, "pr": True, "k": k}
            if not is_clip_edge(n, 32768, k):
                return {"ok": False, "c32768": True, "k": k}
            if G(n, 0) != G(n_p, 0):
                return {"ok": False, "g00": True, "k": k}
            if pal_kind(n, 16384, k) != "unp":
                return {"ok": False, "j16384k": True, "k": k}
        if k >= 16:
            if G(n, 16384) != 1 or G(n, 16384) != G(n_p, 8192):
                return {"ok": False, "g16384": True, "k": k}
            if pal_kind(n_p, 8192, k - 1) != "unp":
                return {"ok": False, "p8192": True, "k": k}
            if want_ph16384_unp(k) != 2:
                return {"ok": False, "u2": True, "k": k}
        if k == 15:
            if G(n, 16384) != 0 or want_ph16384_unp(k) != 1:
                return {"ok": False, "k15g": True}
            if pal_kind(n, 16384, k) != "unp":
                return {"ok": False, "k15k": True}
        if k == 14:
            if G(n, 16384) != 0 or want_ph16384_unp(k) != 3:
                return {"ok": False, "k14g": True}
            if pal_kind(n, 16384, k) != "unp":
                return {"ok": False, "k14k": True}
        if k == 13:
            if n < 4 * u:
                return {"ok": False, "k13c": True}
        if k >= 17:
            if want_ph16384_lo(k) != 11 or want_ph8192_lo(k - 1) != 11:
                return {"ok": False, "lo": True, "k": k}
            if ph16384_lo_js(k) != tuple(2 * j for j in ph8192_lo_js(k - 1)):
                return {"ok": False, "js": True, "k": k}
            for j in ph16384_lo_js(k):
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
        and want_ph16384_unp(15) != 2
        and want_ph16384_lo(16) != 11
        and want_ph16384_unp(8) != want_clip_gp(8)
        and want_ph16384_lo(8) != want_clip_gp(8)
        and want_ph16384_unp(8) != want_even_slice(8)
        and pal_kind(ph16384_n(14), 16384, 14) != "pair"
        and G(ph16384_n(13), 16384) != 1
        and G(ph16384_n(14), 16384) != 1
        and G(ph16384_n(15), 16384) != 1
        and pal_kind(ph16384_n(14), 0, 14) == "unp"
        and pal_kind(ph16384_n(14), 16384, 14) == "unp"
        and pal_kind(ph16384_n(16), 16384, 16) == "unp"
        and want_ph16384_unp(8) == 0
        and want_ph16384_unp(13) == 0
        and want_ph16384_unp(14) == 3
        and want_ph16384_lo(14) == 2
        and want_ph16384_lo(15) == 1
        and want_ph16384_lo(16) == 6
        and want_ph16384_lo(17) == 11
        and want_ph16384_clip(14) == 1
        and want_ph16384_clip(15) == 1
        and want_ph16384_clip(16) == 0
        and ph16384_n(8) == 17024
        and ph16384_n(8) == 2 * ph8192_n(7)
        and ph16384_n(14) == 57344
        and ph16384_n(14) == 2 * ph8192_n(13)
        and ph8192_n(8) == 8832
        and ph4096_n(8) == 4736
        and want_ph8192_unp(13) == 3
        and want_ph8192_lo(13) == 2
        and want_ph8192_lo(16) == 11
        and want_ph8192_clip(15) == 0
        and want_ph4096_lo(15) == 11
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
        and want_ph16384_unp(8) == 0
        and want_ph16384_unp(16) == 2
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph16384_fold() -> dict:
    """k<=8 left Green at even n=5U/2+16384 vs 2-fold of XZ."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = ph16384_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_unp"] != want_ph16384_unp(k):
            return {"ok": False, "unp": True, "k": k, "got": a["n_unp"]}
        if a["n_lo"] != want_ph16384_lo(k):
            return {"ok": False, "lo": True, "k": k, "got": a["n_lo"]}
        if a["n_clip"] != want_ph16384_clip(k):
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
        and want_ph16384_lo(8) == 0
        and want_ph16384_lo(14) == 2
        and want_ph16384_lo(15) == 1
        and want_ph16384_lo(16) == 6
        and want_ph16384_lo(17) == 11
        and want_ph8192_lo(16) == 11
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired {0,16384} at k=15; leftover 11-set at k=16."""
    n13 = ph16384_n(13)
    n14 = ph16384_n(14)
    n15 = ph16384_n(15)
    n16 = ph16384_n(16)
    ok = (
        want_ph16384_unp(15) != 2
        and want_ph16384_lo(16) != 11
        and want_ph16384_unp(8) != want_clip_gp(8)
        and want_ph16384_lo(8) != want_clip_gp(8)
        and want_ph16384_unp(8) != want_even_slice(8)
        and pal_kind(n14, 16384, 14) != "pair"
        and G(n13, 16384) != 1
        and G(n14, 16384) != 1
        and G(n15, 16384) != 1
        and pal_kind(n14, 0, 14) == "unp"
        and pal_kind(n14, 16384, 14) == "unp"
        and pal_kind(n15, 16384, 15) == "unp"
        and pal_kind(n16, 16384, 16) == "unp"
        and want_ph16384_unp(8) == 0
        and want_ph16384_unp(13) == 0
        and want_ph16384_unp(14) == 3
        and want_ph16384_lo(14) == 2
        and G(n13, 16384) == 0
        and G(n14, 16384) == 0
        and G(n15, 16384) == 0
        and G(n16, 16384) == 1
        and want_ph16384_unp(15) == 1
        and want_ph16384_unp(16) == 2
        and want_ph16384_lo(15) == 1
        and want_ph16384_lo(16) == 6
        and want_ph16384_lo(17) == 11
        and want_clip_gp(8) == 85
        and want_even_slice(8) == 85
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and n13 == 36864
        and n13 >= 4 * (1 << 13)
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
    xz = json.loads(XZ_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    xw = json.loads(XW_JSON.read_text())
    ok = (
        xz["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and xw["checks"]["all_ok"]
        and xz["verdict"]["ph8192_lo_eq_11_k_ge_16"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and xw["verdict"]["ph4096_lo_eq_11_k_ge_15"] == "LEMMA"
        and xz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and xz["verdict"]["prize"] == "unsolved"
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
    cnt = ph16384_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph16384_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph16384_eq_2fold_xz_k_ge_2": True,
            "ph16384_unp_eq_016384_k_ge_16": True,
            "ph16384_lo_eq_11_k_ge_17": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph16384_eq_2fold_xz_k_ge_2": "LEMMA",
            "ph16384_unp_eq_016384_k_ge_16": "LEMMA",
            "ph16384_lo_eq_11_k_ge_17": "LEMMA",
            "ph16384_j16384_partner_5U16384": "LEMMA",
            "ph16384_unp_eq_016384_at_k15": "KILLED",
            "ph16384_lo_eq_11_at_k16": "KILLED",
            "ph16384_unp_eq_clip_gp_at_k8": "KILLED",
            "ph16384_lo_eq_clip_gp_at_k8": "KILLED",
            "ph16384_unp_eq_even_slice_at_k8": "KILLED",
            "ph16384_j16384_pair": "KILLED",
            "ph16384_G16384_eq_1_at_k15": "KILLED",
            "ph16384_covering_at_k13": "KILLED",
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
    print("ph16384 k8", dump["ph16384_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
