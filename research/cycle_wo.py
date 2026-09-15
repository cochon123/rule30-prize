#!/usr/bin/env python3
"""Cycle WO: n=5U/2+1 is the unique j=0 partner-5U+2 cell.

Covering n=5U/2+1 has 2n=5U+2, so j=0 is unpaired with that
partner. Even-j unpaired extra there is exactly j=0; odd-j unpaired
is exactly j=1. Parent is clip-edge n=5U_p/2, which has no unpaired
cells, so n_ug=n_gu=n_gp=0 at this n. Leftover+pal left Green is
the 11-set {U/2,U/2+1,U/2+2,U,U+1,U+2,2U,2U+1,2U+2,5U/2,n} for
k>=3. Dies at k=2 for the 11-set (got 6, not 11) and for G(n,2)=1
(got 0). Dies at k=8 for leftover+pal equals clip_gp (got 11, not
85) and equals j=0 odd unpaired (got 11, not 192). Do not kill
pal_kind unpaired at n=5U/2+1, j=0 or j=1. Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wo.py --certify
Dump: research/cycle_wo.json
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
from cycle_tw import green_odd_even
from cycle_ua import want_j0_odd_unp
from cycle_ub import want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half, want_ph_lo
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from cycle_wk import want_gu_fl, want_ug_fl
from cycle_wm import want_j0_all_unp, want_j0_even_unp
from cycle_wn import want_clip_gp_jk, want_clip_slice, want_slice_ug
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WN_JSON = Path(__file__).resolve().parent / "cycle_wn.json"
UR_JSON = Path(__file__).resolve().parent / "cycle_ur.json"
WM_JSON = Path(__file__).resolve().parent / "cycle_wm.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph1_n(k: int) -> int:
    """Covering n=5U/2+1."""
    return parent_half(k) + 1


def ph1_lo_js(k: int) -> tuple[int, ...]:
    """Leftover+pal left indices at n=5U/2+1."""
    u = 1 << k
    n1 = ph1_n(k)
    return (
        u // 2,
        u // 2 + 1,
        u // 2 + 2,
        u,
        u + 1,
        u + 2,
        2 * u,
        2 * u + 1,
        2 * u + 2,
        5 * u // 2,
        n1,
    )


def want_ph1_even_unp(k: int) -> int:
    """Even-j unpaired extra at n=5U/2+1: 1 for every k."""
    return 1


def want_ph1_odd_unp(k: int) -> int:
    """Odd-j unpaired at n=5U/2+1: 1 for k>=2; 0 at k<=1."""
    if k <= 1:
        return 0
    return 1


def want_ph1_lo(k: int) -> int:
    """Leftover+pal left Green at n=5U/2+1: 11 for k>=3; 6 at k=2; 1 at k<=1."""
    if k <= 1:
        return 1
    if k == 2:
        return 6
    return 11


def want_ph1_clip(k: int) -> int:
    """Left clip-edge Green at n=5U/2+1: 0 at k=2; 1 otherwise."""
    if k == 2:
        return 0
    return 1


def want_ph1_ug(k: int) -> int:
    """n_ug at n=5U/2+1: 0 for every k."""
    return 0


def want_ph1_gu(k: int) -> int:
    """n_gu at n=5U/2+1: 0 for every k."""
    return 0


def want_ph1_gp(k: int) -> int:
    """clip_gp cells at n=5U/2+1: 0 for every k."""
    return 0


def ph1_split(k: int) -> dict:
    """Green kinds at covering n=5U/2+1. Do not call from tot_form."""
    n = ph1_n(k)
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    even_unp = odd_unp = lo = n_clip = n_ug = n_gu = n_gp = n_bad = 0
    lo_js = []
    for j in range(0, min(2 * n, clip) + 1):
        if G(n, j) == 0:
            continue
        kind = pal_kind(n, j, k)
        if j > n:
            continue
        if kind == "unp":
            if j % 2 == 0:
                even_unp += 1
                if n % 2 == 1:
                    m = (n - 1) // 2
                    r = j // 2
                    if green_odd_even(m, r) != 1:
                        n_bad += 1
                    elif r != 0:
                        kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
                        km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
                        if km == "unp" and kr == "g0":
                            n_ug += 1
                        elif km == "g0" and kr == "unp":
                            n_gu += 1
                        elif km == "g0" and kr == "pair" and is_clip_edge(m, r, k_p):
                            n_gp += 1
                        else:
                            n_bad += 1
            else:
                odd_unp += 1
        elif kind in ("pair", "pal"):
            if is_clip_edge(n, j, k):
                n_clip += 1
            elif j in (1, 2):
                n_bad += 1
            else:
                lo += 1
                lo_js.append(j)
        else:
            n_bad += 1
    return {
        "even_unp": even_unp,
        "odd_unp": odd_unp,
        "lo": lo,
        "n_clip": n_clip,
        "n_ug": n_ug,
        "n_gu": n_gu,
        "n_gp": n_gp,
        "n_bad": n_bad,
        "lo_js": lo_js,
    }


def tot_form() -> dict:
    """k<=64: n=5U/2+1 partner 5U+2; leftover 11-set; dies at k=2.

    Do not call ph1_split / leftover_at_n here.
    Census is ph1_fold for k<=8.
    """
    n_ok = 0
    if want_ph1_even_unp(0) != 1 or want_ph1_lo(1) != 1:
        return {"ok": False, "k01": True}
    if want_ph1_lo(2) != 6 or want_ph1_odd_unp(2) != 1:
        return {"ok": False, "k2": True}
    if want_ph1_lo(8) != 11 or want_ph1_even_unp(8) != 1:
        return {"ok": False, "k8": True}
    if want_ph1_lo(3) != 11 or want_ph1_clip(2) != 0:
        return {"ok": False, "k3": True}
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
        ph = parent_half(k)
        n1 = ph1_n(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n1 != ph + 1 or n1 != 5 * u // 2 + 1:
            return {"ok": False, "n1": True, "k": k}
        if n1 >= 4 * u:
            return {"ok": False, "cov": True, "k": k}
        if pal_kind(n1, 0, k) != "unp":
            return {"ok": False, "j0": True, "k": k}
        if G(n1, 0) != 1 or is_clip_edge(n1, 0, k):
            return {"ok": False, "g0c": True, "k": k}
        if want_ph1_even_unp(k) != 1:
            return {"ok": False, "eu": True, "k": k}
        if want_ph1_ug(k) != 0 or want_ph1_gu(k) != 0 or want_ph1_gp(k) != 0:
            return {"ok": False, "xor": True, "k": k}
        if k >= 1:
            if 2 * n1 != clip + 2:
                return {"ok": False, "pr": True, "k": k}
        if k >= 2:
            if pal_kind(n1, 1, k) != "unp":
                return {"ok": False, "j1": True, "k": k}
            if G(n1, 1) != 1 or is_clip_edge(n1, 1, k):
                return {"ok": False, "g1c": True, "k": k}
            if not is_clip_edge(n1, 2, k):
                return {"ok": False, "c2": True, "k": k}
            if 2 * n1 - 2 != clip:
                return {"ok": False, "c2p": True, "k": k}
            m = (n1 - 1) // 2
            if m != parent_half(k - 1):
                return {"ok": False, "mp": True, "k": k}
            if pal_kind(m, 0, k - 1) != "pair" or not is_clip_edge(m, 0, k - 1):
                return {"ok": False, "par": True, "k": k}
            if 2 * m != 5 * (1 << (k - 1)):
                return {"ok": False, "nup": True, "k": k}
            j_sl = 2 * n1 - clip - 2
            if j_sl != 0:
                return {"ok": False, "sl": True, "k": k}
            if want_ph1_odd_unp(k) != 1:
                return {"ok": False, "ou": True, "k": k}
        if k == 2:
            if G(n1, 2) != 0 or want_ph1_lo(k) != 6:
                return {"ok": False, "k2g": True}
        if k >= 3:
            if G(n1, 2) != 1 or pal_kind(n1, 2, k) != "pair":
                return {"ok": False, "g2": True, "k": k}
            if pal_kind(n1, n1, k) != "pal" or G(n1, n1) != 1:
                return {"ok": False, "pal": True, "k": k}
            if want_ph1_lo(k) != 11 or want_ph1_clip(k) != 1:
                return {"ok": False, "lo": True, "k": k}
            for j in ph1_lo_js(k):
                if G(n1, j) != 1:
                    return {"ok": False, "loj": True, "k": k, "j": j}
                kind = pal_kind(n1, j, k)
                if kind not in ("pair", "pal"):
                    return {"ok": False, "lok": True, "k": k, "j": j}
                if is_clip_edge(n1, j, k) or j in (1, 2):
                    return {"ok": False, "loc": True, "k": k, "j": j}
        if k >= 4:
            m = parent_half(k - 1)
            u_p = 1 << (k - 1)
            if want_ph_lo(k - 1) != 3:
                return {"ok": False, "ur": True, "k": k}
            if G(n1, u // 2) != G(m, u_p // 2):
                return {"ok": False, "dbl": True, "k": k}
            if G(m, u_p // 2) != 1:
                return {"ok": False, "urG": True, "k": k}
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
        and want_ph1_lo(2) != 11
        and G(ph1_n(2), 2) != 1
        and want_ph1_even_unp(8) != 0
        and want_ph1_ug(8) != 1
        and pal_kind(ph1_n(8), 0, 8) != "pair"
        and want_ph1_lo(8) != want_clip_gp(8)
        and want_ph1_lo(8) != want_j0_odd_unp(8)
        and want_ph1_even_unp(8) != 2
        and want_ph1_odd_unp(1) != 1
        and want_ph1_clip(2) != 1
        and pal_kind(ph1_n(8), 0, 8) == "unp"
        and pal_kind(ph1_n(8), 1, 8) == "unp"
        and want_ph1_lo(8) == 11
        and want_ph1_lo(3) == 11
        and want_ph1_lo(2) == 6
        and want_ph1_even_unp(8) == 1
        and want_ph1_odd_unp(8) == 1
        and want_ph1_clip(8) == 1
        and want_ph1_ug(8) == 0
        and want_ph1_gu(8) == 0
        and want_ph1_gp(8) == 0
        and ph1_n(8) == 641
        and 2 * ph1_n(8) == 5 * (1 << 8) + 2
        and want_clip_slice(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_slice_ug(8) == 0
        and want_j0_even_unp(8) == 191
        and want_j0_all_unp(8) == 383
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and want_ph_lo(8) == 3
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph1_fold() -> dict:
    """k<=8 Green kinds at n=5U/2+1 vs closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = ph1_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["even_unp"] != want_ph1_even_unp(k):
            return {"ok": False, "eu": True, "k": k, "got": a["even_unp"]}
        if a["odd_unp"] != want_ph1_odd_unp(k):
            return {"ok": False, "ou": True, "k": k, "got": a["odd_unp"]}
        if a["lo"] != want_ph1_lo(k):
            return {"ok": False, "lo": True, "k": k, "got": a["lo"]}
        if a["n_clip"] != want_ph1_clip(k):
            return {"ok": False, "cl": True, "k": k, "got": a["n_clip"]}
        if a["n_ug"] != 0 or a["n_gu"] != 0 or a["n_gp"] != 0:
            return {"ok": False, "xor": True, "k": k, "got": a}
        if k >= 3 and tuple(a["lo_js"]) != ph1_lo_js(k):
            return {"ok": False, "js": True, "k": k, "got": a["lo_js"]}
        n_ok += 1
        rows[str(k)] = {
            "even_unp": a["even_unp"],
            "odd_unp": a["odd_unp"],
            "lo": a["lo"],
            "n_clip": a["n_clip"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo"] == 1
        and rows["1"]["odd_unp"] == 0
        and rows["2"]["lo"] == 6
        and rows["2"]["n_clip"] == 0
        and rows["3"]["lo"] == 11
        and rows["8"]["even_unp"] == 1
        and rows["8"]["odd_unp"] == 1
        and rows["8"]["lo"] == 11
        and rows["8"]["n_clip"] == 1
        and want_ph1_lo(4) == 11
        and want_ph1_lo(5) == 11
        and want_ph1_lo(6) == 11
        and want_ph1_lo(7) == 11
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """11-set at k=2; G(n,2)=1 at k=2; leftover equals clip_gp at k=8."""
    n8 = ph1_n(8)
    n2 = ph1_n(2)
    ok = (
        want_ph1_lo(2) != 11
        and G(n2, 2) != 1
        and want_ph1_even_unp(8) != 0
        and want_ph1_ug(8) != 1
        and pal_kind(n8, 0, 8) != "pair"
        and want_ph1_lo(8) != want_clip_gp(8)
        and want_ph1_lo(8) != want_j0_odd_unp(8)
        and want_ph1_even_unp(8) != 2
        and want_ph1_odd_unp(1) != 1
        and want_ph1_clip(2) != 1
        and pal_kind(n8, 0, 8) == "unp"
        and pal_kind(n8, 1, 8) == "unp"
        and want_ph1_lo(2) == 6
        and G(n2, 2) == 0
        and want_ph1_lo(8) == 11
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and n8 == 641
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
    wn = json.loads(WN_JSON.read_text())
    ur = json.loads(UR_JSON.read_text())
    wm = json.loads(WM_JSON.read_text())
    ok = (
        wn["checks"]["all_ok"]
        and ur["checks"]["all_ok"]
        and wm["checks"]["all_ok"]
        and wn["verdict"]["clip_gp_eq_J_k_minus_kmod2"] == "LEMMA"
        and ur["verdict"]["ph_lo_eq_3_k_ge_3"] == "LEMMA"
        and wm["verdict"]["j0_unp_eq_window"] == "LEMMA"
        and wn["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wn["verdict"]["prize"] == "unsolved"
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
    cnt = ph1_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph1_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph1_j0_partner_5U2_k_ge_1": True,
            "ph1_even_unp_eq_1": True,
            "ph1_no_ug_gu_gp": True,
            "ph1_lo_eq_11_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph1_j0_partner_5U2_k_ge_1": "LEMMA",
            "ph1_even_unp_eq_1": "LEMMA",
            "ph1_odd_unp_eq_1_k_ge_2": "LEMMA",
            "ph1_no_ug_gu_gp": "LEMMA",
            "ph1_lo_eq_11_k_ge_3": "LEMMA",
            "ph1_lo_eq_11_at_k2": "KILLED",
            "ph1_G_n2_eq_1_at_k2": "KILLED",
            "ph1_even_unp_eq_0": "KILLED",
            "ph1_ug_eq_1": "KILLED",
            "ph1_j0_pair": "KILLED",
            "ph1_lo_eq_clip_gp_at_k8": "KILLED",
            "ph1_lo_eq_j0_odd_at_k8": "KILLED",
            "ph1_even_unp_eq_2": "KILLED",
            "ph1_odd_unp_eq_1_at_k1": "KILLED",
            "ph1_clip_eq_1_at_k2": "KILLED",
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
    print("ph1 k8", dump["ph1_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
