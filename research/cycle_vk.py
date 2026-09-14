#!/usr/bin/env python3
"""Cycle VK: leftover extra xor COUNT gap n_pg/n_gp.

Cycle VI tot gap difference equals Cycle VE xor small gap for every
k, so n_pg=(gap+VE)/2 and n_gp=(gap-VE)/2. Small halves split the
same way. Large halves are equal, each gl/2. Dies at k=2,3 for the
UM large reconstruction of large n_pg/n_gp. Census k=8: tot 5910/5752,
small 3684/3526, large 2226/2226. Do not PREFIX pal-center tot. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_vk.py --certify
Dump: research/cycle_vk.json
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
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uo import named_half_split, want_lo_parent_small_sum
from cycle_up import lucas, want_lo_e, want_pg_lo, want_gp_lo
from cycle_uq import want_lo_parent_large_sum
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vd import want_lo_parent_small_diff
from cycle_ve import want_xor_small_gap
from cycle_vg import want_ej_xor_gp, want_ej_xor_pg
from cycle_vh import (
    want_ej_xor_gp_l,
    want_ej_xor_gp_s,
    want_ej_xor_pg_l,
    want_ej_xor_pg_s,
)
from cycle_vi import want_xor_count_gap
from cycle_vj import want_xor_count_gap_l, want_xor_count_gap_s
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VJ_JSON = Path(__file__).resolve().parent / "cycle_vj.json"
VE_JSON = Path(__file__).resolve().parent / "cycle_ve.json"
VG_JSON = Path(__file__).resolve().parent / "cycle_vg.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_count_gap_pg(k: int) -> int:
    """leftover-parent xor n_pg minus leftover extra xor n_pg."""
    return (want_xor_count_gap(k) + want_xor_small_gap(k)) // 2


def want_xor_count_gap_gp(k: int) -> int:
    """leftover-parent xor n_gp minus leftover extra xor n_gp."""
    return (want_xor_count_gap(k) - want_xor_small_gap(k)) // 2


def want_xor_count_gap_s_pg(k: int) -> int:
    """COUNT gap small n_pg: (small gap + xor small gap)/2."""
    return (want_xor_count_gap_s(k) + want_xor_small_gap(k)) // 2


def want_xor_count_gap_s_gp(k: int) -> int:
    """COUNT gap small n_gp: (small gap - xor small gap)/2."""
    return (want_xor_count_gap_s(k) - want_xor_small_gap(k)) // 2


def want_xor_count_gap_l_pg(k: int) -> int:
    """COUNT gap large n_pg: large gap / 2."""
    return want_xor_count_gap_l(k) // 2


def want_xor_count_gap_l_gp(k: int) -> int:
    """COUNT gap large n_gp: large gap / 2."""
    return want_xor_count_gap_l(k) // 2


def _alg_large_pg(k: int) -> int:
    plo_l = (
        want_lo_parent_large_sum(k) + want_lo_parent_large_diff(k)
    ) // 2
    return plo_l - want_ej_xor_pg_l(k)


def _alg_large_gp(k: int) -> int:
    glo_l = (
        want_lo_parent_large_sum(k) - want_lo_parent_large_diff(k)
    ) // 2
    return glo_l - want_ej_xor_gp_l(k)


def tot_form() -> dict:
    """k<=64: COUNT gap n_pg/n_gp; UM large recon dies at k=2,3.

    Do not call named_half_split / leftover_extra_xor_split here.
    Census is gap_pg_fold for k<=8.
    """
    n_ok = 0
    if want_xor_count_gap_pg(0) != 0 or want_xor_count_gap_pg(2) != 1:
        return {"ok": False, "k02": True}
    if want_xor_count_gap_pg(3) != 8 or want_xor_count_gap_gp(3) != 5:
        return {"ok": False, "k3": True}
    if want_xor_count_gap_pg(8) != 5910 or want_xor_count_gap_gp(8) != 5752:
        return {"ok": False, "k8t": True}
    if want_xor_count_gap_s_pg(8) != 3684 or want_xor_count_gap_s_gp(8) != 3526:
        return {"ok": False, "k8s": True}
    if want_xor_count_gap_l_pg(8) != 2226 or want_xor_count_gap_l_gp(8) != 2226:
        return {"ok": False, "k8l": True}
    if _alg_large_pg(2) == want_xor_count_gap_l_pg(2):
        return {"ok": False, "k2p": True}
    if _alg_large_gp(3) == want_xor_count_gap_l_gp(3):
        return {"ok": False, "k3g": True}
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
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        g = want_xor_count_gap(k)
        gs = want_xor_count_gap_s(k)
        gl = want_xor_count_gap_l(k)
        ve = want_xor_small_gap(k)
        if (g + ve) % 2 != 0 or (gs + ve) % 2 != 0 or gl % 2 != 0:
            return {"ok": False, "par": True, "k": k}
        if want_xor_count_gap_pg(k) + want_xor_count_gap_gp(k) != g:
            return {"ok": False, "sum": True, "k": k}
        if want_xor_count_gap_pg(k) - want_xor_count_gap_gp(k) != ve:
            return {"ok": False, "dif": True, "k": k}
        if want_xor_count_gap_pg(k) != want_pg_lo(k) - want_ej_xor_pg(k):
            return {"ok": False, "pg": True, "k": k}
        if want_xor_count_gap_gp(k) != want_gp_lo(k) - want_ej_xor_gp(k):
            return {"ok": False, "gp": True, "k": k}
        plo_s = (
            want_lo_parent_small_sum(k) + want_lo_parent_small_diff(k)
        ) // 2
        glo_s = (
            want_lo_parent_small_sum(k) - want_lo_parent_small_diff(k)
        ) // 2
        if want_xor_count_gap_s_pg(k) != plo_s - want_ej_xor_pg_s(k):
            return {"ok": False, "sp": True, "k": k}
        if want_xor_count_gap_s_gp(k) != glo_s - want_ej_xor_gp_s(k):
            return {"ok": False, "sg": True, "k": k}
        if want_xor_count_gap_s_pg(k) + want_xor_count_gap_s_gp(k) != gs:
            return {"ok": False, "ss": True, "k": k}
        if want_xor_count_gap_l_pg(k) != want_xor_count_gap_l_gp(k):
            return {"ok": False, "leq": True, "k": k}
        if want_xor_count_gap_l_pg(k) + want_xor_count_gap_l_gp(k) != gl:
            return {"ok": False, "ls": True, "k": k}
        if k >= 4:
            if _alg_large_pg(k) != want_xor_count_gap_l_pg(k):
                return {"ok": False, "lp": True, "k": k}
            if _alg_large_gp(k) != want_xor_count_gap_l_gp(k):
                return {"ok": False, "lg": True, "k": k}
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
        and want_xor_count_gap_pg(8) != want_xor_count_gap_s_pg(8)
        and want_xor_count_gap_l_pg(2) != _alg_large_pg(2)
        and want_xor_count_gap_l_gp(3) != _alg_large_gp(3)
        and want_xor_count_gap_pg(8) == 5910
        and want_xor_count_gap_gp(8) == 5752
        and want_xor_count_gap_s_pg(8) == 3684
        and want_xor_count_gap_l_pg(8) == 2226
        and want_xor_count_gap(8) == 11662
        and want_xor_small_gap(8) == 158
        and want_ej_xor(8) == 5225
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and lucas(8) == 47
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def gap_pg_fold() -> dict:
    """k<=8 leftover extra xor COUNT gap n_pg/n_gp tot and halves."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        a = leftover_extra_xor_split(k)
        gps = r["plo_s"] - a["pg_s"]
        ggs = r["glo_s"] - a["gp_s"]
        gpl = r["plo_l"] - a["pg_l"]
        ggl = r["glo_l"] - a["gp_l"]
        gpg = gps + gpl
        ggp = ggs + ggl
        if gpg != want_xor_count_gap_pg(k):
            return {"ok": False, "pg": True, "k": k, "got": gpg}
        if ggp != want_xor_count_gap_gp(k):
            return {"ok": False, "gp": True, "k": k, "got": ggp}
        if gps != want_xor_count_gap_s_pg(k):
            return {"ok": False, "sp": True, "k": k, "got": gps}
        if ggs != want_xor_count_gap_s_gp(k):
            return {"ok": False, "sg": True, "k": k, "got": ggs}
        if gpl != want_xor_count_gap_l_pg(k):
            return {"ok": False, "lp": True, "k": k, "got": gpl}
        if ggl != want_xor_count_gap_l_gp(k):
            return {"ok": False, "lg": True, "k": k, "got": ggl}
        if gpl != ggl:
            return {"ok": False, "neq": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "pg": gpg,
            "gp": ggp,
            "pg_s": gps,
            "gp_s": ggs,
            "pg_l": gpl,
            "gp_l": ggl,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["pg"] == 1
        and rows["2"]["gp"] == 0
        and rows["2"]["pg_l"] == 0
        and rows["3"]["pg"] == 8
        and rows["3"]["gp"] == 5
        and rows["3"]["pg_l"] == 3
        and rows["8"]["pg"] == 5910
        and rows["8"]["gp"] == 5752
        and rows["8"]["pg_s"] == 3684
        and rows["8"]["gp_s"] == 3526
        and rows["8"]["pg_l"] == 2226
        and want_xor_count_gap_pg(4) == 38
        and want_xor_count_gap_gp(4) == 30
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """UM large recon at k=2,3; small pg equals tot pg at k=8."""
    r8 = named_half_split(8)
    a8 = leftover_extra_xor_split(8)
    gps8 = r8["plo_s"] - a8["pg_s"]
    gpl8 = r8["plo_l"] - a8["pg_l"]
    ok = (
        want_xor_count_gap_l_pg(2) != _alg_large_pg(2)
        and want_xor_count_gap_l_gp(3) != _alg_large_gp(3)
        and want_xor_count_gap_s_pg(8) != want_xor_count_gap_pg(8)
        and gps8 == 3684
        and gpl8 == 2226
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
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
    vj = json.loads(VJ_JSON.read_text())
    ve = json.loads(VE_JSON.read_text())
    vg = json.loads(VG_JSON.read_text())
    ok = (
        vj["checks"]["all_ok"]
        and ve["checks"]["all_ok"]
        and vg["checks"]["all_ok"]
        and vj["verdict"]["xor_count_gap_small_eq_lo_small_named_j0_k_ge_3"]
        == "LEMMA"
        and ve["verdict"]["xor_small_gap_eq_5_2km3_minus_2_k_ge_3"] == "LEMMA"
        and vg["verdict"]["ej_xor_pg_eq_parent_leftover_pg"] == "LEMMA"
        and vj["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vj["verdict"]["prize"] == "unsolved"
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
    cnt = gap_pg_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "gap_pg_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_count_gap_pg_gp_eq_gap_pm_xor_small_gap": True,
            "xor_count_gap_large_pg_eq_gp": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_count_gap_pg_gp_eq_gap_pm_xor_small_gap": "LEMMA",
            "xor_count_gap_large_pg_eq_gp": "LEMMA",
            "xor_count_gap_large_UM_recon_at_k2": "KILLED",
            "xor_count_gap_large_UM_recon_at_k3": "KILLED",
            "xor_count_gap_small_pg_eq_tot_pg": "KILLED",
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
        "gap k8 pg",
        dump["gap_pg_fold"]["rows"]["8"]["pg"],
        "gp",
        dump["gap_pg_fold"]["rows"]["8"]["gp"],
        "s",
        dump["gap_pg_fold"]["rows"]["8"]["pg_s"],
        dump["gap_pg_fold"]["rows"]["8"]["gp_s"],
        "l",
        dump["gap_pg_fold"]["rows"]["8"]["pg_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
