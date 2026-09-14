#!/usr/bin/env python3
"""Cycle VU: leftover-parent xor small/large F/L closed forms.

Small is 2^{k-3}(8 F_{k+1}+6 F_{k-1}-25)-2(-1)^k+3 for k>=3.
Large is (2^{k-3}(10 F_{k-1}+32 L_{k-1}-45)+15(-1)^k-1)/5 for k>=3.
They sum to leftover-parent xor tot. Small is xor_lo small minus
named_s. Dies at k=3 for both F/L forms with shift 0 (small got 5,
not 10; large got -4, not 9). Dies at k=8 without the small +3
(got 10398, not 10401) and without the large 15(-1)^k (got 6483,
not 6486). Dies at k=8 for small equals tot parent xor (got 10401,
not 16887). Census k=8: small 10401, large 6486. Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_vu.py --certify
Dump: research/cycle_vu.json
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
from cycle_tw import want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uo import (
    named_half_split,
    want_lo_parent_small_sum,
    want_named_l,
    want_named_s,
)
from cycle_up import lucas, want_lo_e
from cycle_uq import want_lo_parent_large_sum
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vt import want_xor_lo_l_fl, want_xor_lo_s_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VT_JSON = Path(__file__).resolve().parent / "cycle_vt.json"
UO_JSON = Path(__file__).resolve().parent / "cycle_uo.json"
UQ_JSON = Path(__file__).resolve().parent / "cycle_uq.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_lo_parent_s_fl(k: int) -> int:
    """leftover-parent xor small: F form for k>=3; special 1 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    return (
        (1 << (k - 3)) * (8 * fib(k + 1) + 6 * fib(k - 1) - 25)
        - 2 * ((-1) ** k)
        + 3
    )


def want_lo_parent_l_fl(k: int) -> int:
    """leftover-parent xor large: F/L form for k>=3; special 1 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (
        (1 << (k - 3)) * (10 * fib(k - 1) + 32 * lucas(k - 1) - 45)
        + 15 * ((-1) ** k)
        - 1
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: leftover-parent xor small/large F/L; dies at k=3 with shift 0.

    Do not call named_half_split / leftover_xor_split here.
    Census is parent_hl_fold for k<=8.
    """
    n_ok = 0
    raw_s3 = -2 * ((-1) ** 3) + 3
    raw_l3 = (15 * ((-1) ** 3) - 1) // 5
    miss_p3 = (1 << 5) * (8 * fib(9) + 6 * fib(7) - 25) - 2 * ((-1) ** 8)
    miss_sign = (
        (1 << 5) * (10 * fib(7) + 32 * lucas(7) - 45) - 1
    ) // 5
    if want_lo_parent_s_fl(0) != 0 or want_lo_parent_s_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_lo_parent_s_fl(2) != 1 or want_lo_parent_l_fl(2) != 1:
        return {"ok": False, "k2": True}
    if want_lo_parent_s_fl(3) != 10 or want_lo_parent_l_fl(3) != 9:
        return {"ok": False, "k3": True}
    if want_lo_parent_s_fl(8) != 10401 or want_lo_parent_l_fl(8) != 6486:
        return {"ok": False, "k8": True}
    if want_lo_parent_s_fl(3) == raw_s3:
        return {"ok": False, "k3s": True}
    if want_lo_parent_l_fl(3) == raw_l3:
        return {"ok": False, "k3l": True}
    if want_lo_parent_s_fl(8) == miss_p3:
        return {"ok": False, "p3": True}
    if want_lo_parent_l_fl(8) == miss_sign:
        return {"ok": False, "sg": True}
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
        if want_lo_parent_s_fl(k) != want_lo_parent_small_sum(k):
            return {"ok": False, "s": True, "k": k}
        if want_lo_parent_l_fl(k) != want_lo_parent_large_sum(k):
            return {"ok": False, "l": True, "k": k}
        if want_lo_parent_s_fl(k) != want_xor_lo_s_fl(k) - want_named_s(k):
            return {"ok": False, "xs": True, "k": k}
        if want_lo_parent_l_fl(k) != want_xor_lo_l_fl(k) - want_named_l(k):
            return {"ok": False, "xl": True, "k": k}
        if k >= 3:
            ns = (
                (1 << (k - 3)) * (8 * fib(k + 1) + 6 * fib(k - 1) - 25)
                - 2 * ((-1) ** k)
                + 3
            )
            nl = (
                (1 << (k - 3)) * (10 * fib(k - 1) + 32 * lucas(k - 1) - 45)
                + 15 * ((-1) ** k)
                - 1
            )
            if ns != want_lo_parent_s_fl(k):
                return {"ok": False, "ds": True, "k": k}
            if nl % 5 != 0 or nl // 5 != want_lo_parent_l_fl(k):
                return {"ok": False, "dl": True, "k": k}
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
    tot8 = want_lo_parent_s_fl(8) + want_lo_parent_l_fl(8)
    ok = (
        n_ok == K_ALG + 1
        and want_lo_parent_s_fl(3) != raw_s3
        and want_lo_parent_l_fl(3) != raw_l3
        and want_lo_parent_s_fl(8) != miss_p3
        and want_lo_parent_l_fl(8) != miss_sign
        and want_lo_parent_s_fl(8) != tot8
        and want_lo_parent_s_fl(8) == 10401
        and want_lo_parent_l_fl(8) == 6486
        and tot8 == 16887
        and want_j0_odd_lo(8) == 319
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
        and miss_p3 == 10398
        and miss_sign == 6483
        and raw_s3 == 5
        and raw_l3 == -4
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def parent_hl_fold() -> dict:
    """k<=8 leftover-parent xor halves vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        if r["n_bad"] != 0 or r["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        ps = r["plo_s"] + r["glo_s"]
        pl = r["plo_l"] + r["glo_l"]
        if ps != want_lo_parent_s_fl(k):
            return {"ok": False, "s": True, "k": k, "got": ps}
        if pl != want_lo_parent_l_fl(k):
            return {"ok": False, "l": True, "k": k, "got": pl}
        if ps != want_lo_parent_small_sum(k):
            return {"ok": False, "ss": True, "k": k}
        if pl != want_lo_parent_large_sum(k):
            return {"ok": False, "ll": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"ps": ps, "pl": pl}
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["ps"] == 0
        and rows["1"]["pl"] == 0
        and rows["2"]["ps"] == 1
        and rows["2"]["pl"] == 1
        and rows["3"]["ps"] == 10
        and rows["3"]["pl"] == 9
        and rows["8"]["ps"] == 10401
        and rows["8"]["pl"] == 6486
        and want_lo_parent_s_fl(4) == 55
        and want_lo_parent_l_fl(5) == 164
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=3 with shift 0; small +3 and large sign at k=8."""
    raw_s3 = -2 * ((-1) ** 3) + 3
    raw_l3 = (15 * ((-1) ** 3) - 1) // 5
    miss_p3 = (1 << 5) * (8 * fib(9) + 6 * fib(7) - 25) - 2 * ((-1) ** 8)
    miss_sign = (
        (1 << 5) * (10 * fib(7) + 32 * lucas(7) - 45) - 1
    ) // 5
    r8 = named_half_split(8)
    ps8 = r8["plo_s"] + r8["glo_s"]
    pl8 = r8["plo_l"] + r8["glo_l"]
    tot8 = want_lo_parent_s_fl(8) + want_lo_parent_l_fl(8)
    ok = (
        want_lo_parent_s_fl(3) != raw_s3
        and want_lo_parent_l_fl(3) != raw_l3
        and want_lo_parent_s_fl(8) != miss_p3
        and want_lo_parent_l_fl(8) != miss_sign
        and want_lo_parent_s_fl(8) != tot8
        and ps8 == 10401
        and pl8 == 6486
        and raw_s3 == 5
        and raw_l3 == -4
        and miss_p3 == 10398
        and miss_sign == 6483
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
    vt = json.loads(VT_JSON.read_text())
    uo = json.loads(UO_JSON.read_text())
    uq = json.loads(UQ_JSON.read_text())
    ok = (
        vt["checks"]["all_ok"]
        and uo["checks"]["all_ok"]
        and uq["checks"]["all_ok"]
        and vt["verdict"]["xor_lo_s_eq_FL_closed_k_ge_2"] == "LEMMA"
        and vt["verdict"]["xor_lo_l_eq_FL_closed_k_ge_2"] == "LEMMA"
        and uo["verdict"]["lo_parent_small_sum_eq_lo_small_minus_named_j0"]
        == "LEMMA"
        and uq["verdict"]["lo_parent_large_sum_eq_tot_minus_small"] == "LEMMA"
        and vt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vt["verdict"]["prize"] == "unsolved"
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
    cnt = parent_hl_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "parent_hl_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_parent_s_eq_FL_closed_k_ge_3": True,
            "lo_parent_l_eq_FL_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_parent_s_eq_FL_closed_k_ge_3": "LEMMA",
            "lo_parent_l_eq_FL_closed_k_ge_3": "LEMMA",
            "lo_parent_s_FL_shift0_at_k3": "KILLED",
            "lo_parent_l_FL_shift0_at_k3": "KILLED",
            "lo_parent_s_without_plus3_at_k8": "KILLED",
            "lo_parent_l_without_15sign_at_k8": "KILLED",
            "lo_parent_s_eq_tot": "KILLED",
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
        "parent k8 s",
        dump["parent_hl_fold"]["rows"]["8"]["ps"],
        "l",
        dump["parent_hl_fold"]["rows"]["8"]["pl"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
