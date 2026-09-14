#!/usr/bin/env python3
"""Cycle VN: leftover extra xor COUNT gap halves F/L closed forms.

Large gap is 2^{k-3}(L_{k-2}+16 F_{k-2}-7)+4(-1)^k for k>=3. Small
gap is (2^{k-3}(27 L_{k-2}+30 F_{k-2}-50)-8(-1)^k+6)/3 for k>=3.
They sum to Cycle VM tot. Dies at k=2 for both F/L forms with shift
0 (large got 4, not 0; small got -1, not 1). Census k=8: small 7210,
large 4452. Do not PREFIX pal-center tot. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk leftover d catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_vn.py --certify
Dump: research/cycle_vn.json
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
from cycle_uo import named_half_split
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vj import want_xor_count_gap_l, want_xor_count_gap_s
from cycle_vm import want_xor_count_gap_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VM_JSON = Path(__file__).resolve().parent / "cycle_vm.json"
VJ_JSON = Path(__file__).resolve().parent / "cycle_vj.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_count_gap_l_fl(k: int) -> int:
    """COUNT gap large: F/L form for k>=3; 0 at k<=2."""
    if k <= 2:
        return 0
    return (1 << (k - 3)) * (
        lucas(k - 2) + 16 * fib(k - 2) - 7
    ) + 4 * ((-1) ** k)


def want_xor_count_gap_s_fl(k: int) -> int:
    """COUNT gap small: F/L form for k>=3; special 1 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (
        (1 << (k - 3)) * (27 * lucas(k - 2) + 30 * fib(k - 2) - 50)
        - 8 * ((-1) ** k)
        + 6
    )
    return n // 3


def tot_form() -> dict:
    """k<=64: COUNT gap half F/L forms; dies at k=2 with shift 0.

    Do not call named_half_split / leftover_extra_xor_split here.
    Census is gap_hl_fl_fold for k<=8.
    """
    n_ok = 0
    raw_l2 = 4 * ((-1) ** 2)
    raw_s2 = (-8 * ((-1) ** 2) + 6) // 3
    if want_xor_count_gap_s_fl(0) != 0 or want_xor_count_gap_s_fl(2) != 1:
        return {"ok": False, "k02": True}
    if want_xor_count_gap_l_fl(3) != 6 or want_xor_count_gap_s_fl(3) != 7:
        return {"ok": False, "k3": True}
    if want_xor_count_gap_s_fl(8) != 7210 or want_xor_count_gap_l_fl(8) != 4452:
        return {"ok": False, "k8": True}
    if want_xor_count_gap_l_fl(2) == raw_l2:
        return {"ok": False, "k2l": True}
    if want_xor_count_gap_s_fl(2) == raw_s2:
        return {"ok": False, "k2s": True}
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
        if want_xor_count_gap_s_fl(k) != want_xor_count_gap_s(k):
            return {"ok": False, "s": True, "k": k}
        if want_xor_count_gap_l_fl(k) != want_xor_count_gap_l(k):
            return {"ok": False, "l": True, "k": k}
        if want_xor_count_gap_s_fl(k) + want_xor_count_gap_l_fl(k) != (
            want_xor_count_gap_fl(k)
        ):
            return {"ok": False, "sum": True, "k": k}
        if k >= 3:
            ns = (
                (1 << (k - 3))
                * (27 * lucas(k - 2) + 30 * fib(k - 2) - 50)
                - 8 * ((-1) ** k)
                + 6
            )
            if ns % 3 != 0 or ns // 3 != want_xor_count_gap_s_fl(k):
                return {"ok": False, "div": True, "k": k}
            if want_xor_count_gap_l_fl(k) != (
                (1 << (k - 3)) * (lucas(k - 2) + 16 * fib(k - 2) - 7)
                + 4 * ((-1) ** k)
            ):
                return {"ok": False, "lf": True, "k": k}
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
        and want_xor_count_gap_l_fl(2) != raw_l2
        and want_xor_count_gap_s_fl(2) != raw_s2
        and want_xor_count_gap_s_fl(8) != want_xor_count_gap_fl(8)
        and want_xor_count_gap_s_fl(8) == 7210
        and want_xor_count_gap_l_fl(8) == 4452
        and want_xor_count_gap_fl(8) == 11662
        and want_ej_xor(8) == 5225
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and lucas(8) == 47
        and fib(8) == 21
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
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def gap_hl_fl_fold() -> dict:
    """k<=8 COUNT gap halves vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        a = leftover_extra_xor_split(k)
        gs = r["plo_s"] + r["glo_s"] - a["pg_s"] - a["gp_s"]
        gl = r["plo_l"] + r["glo_l"] - a["pg_l"] - a["gp_l"]
        if gs != want_xor_count_gap_s_fl(k):
            return {"ok": False, "s": True, "k": k, "got": gs}
        if gl != want_xor_count_gap_l_fl(k):
            return {"ok": False, "l": True, "k": k, "got": gl}
        if gs + gl != want_xor_count_gap_fl(k):
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"gs": gs, "gl": gl}
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["gs"] == 1
        and rows["2"]["gl"] == 0
        and rows["3"]["gs"] == 7
        and rows["3"]["gl"] == 6
        and rows["8"]["gs"] == 7210
        and rows["8"]["gl"] == 4452
        and want_xor_count_gap_s_fl(4) == 40
        and want_xor_count_gap_l_fl(4) == 28
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=2 with shift 0; small gap equals tot gap at k=8."""
    raw_l2 = 4 * ((-1) ** 2)
    raw_s2 = (-8 * ((-1) ** 2) + 6) // 3
    r8 = named_half_split(8)
    a8 = leftover_extra_xor_split(8)
    gs8 = r8["plo_s"] + r8["glo_s"] - a8["pg_s"] - a8["gp_s"]
    gl8 = r8["plo_l"] + r8["glo_l"] - a8["pg_l"] - a8["gp_l"]
    ok = (
        want_xor_count_gap_l_fl(2) != raw_l2
        and want_xor_count_gap_s_fl(2) != raw_s2
        and want_xor_count_gap_s_fl(8) != want_xor_count_gap_fl(8)
        and gs8 == 7210
        and gl8 == 4452
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
    vm = json.loads(VM_JSON.read_text())
    vj = json.loads(VJ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    ok = (
        vm["checks"]["all_ok"]
        and vj["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and vm["verdict"]["xor_count_gap_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vj["verdict"]["xor_count_gap_small_eq_lo_small_named_j0_k_ge_3"]
        == "LEMMA"
        and up["verdict"]["pg_lo_eq_2_parent_even_lo"] == "LEMMA"
        and vm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vm["verdict"]["prize"] == "unsolved"
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
    cnt = gap_hl_fl_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "gap_hl_fl_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_count_gap_large_eq_FL_closed_k_ge_3": True,
            "xor_count_gap_small_eq_FL_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_count_gap_large_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_count_gap_small_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_count_gap_large_FL_shift0_at_k2": "KILLED",
            "xor_count_gap_small_FL_shift0_at_k2": "KILLED",
            "xor_count_gap_small_eq_tot": "KILLED",
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
        "gap k8 s",
        dump["gap_hl_fl_fold"]["rows"]["8"]["gs"],
        "l",
        dump["gap_hl_fl_fold"]["rows"]["8"]["gl"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
