#!/usr/bin/env python3
"""Cycle WB: leftover extra xor small/large F/L closed forms.

Small is (2^{k-3}(12 F_k+9 F_{k-2}-25)-2(-1)^{k-1}+3)/3 for k>=3.
Large is (2^{k-3}(5 F_{k-2}+16 L_{k-2}-10)+5(-1)^{k-1}-1)/5 for
k>=3. They sum to leftover extra xor tot. Equal xor_lo small/large
at k-1 for k>=3, not at k=2. Dies at k=3 for both F/L forms with
shift 0 (small got 0, not 3; large got 0, not 3). Dies at k=8
without the small +3 (got 3190, not 3191) and without the large
5(-1)^{k-1} (got 2035, not 2034). Do not kill without the large
-1 at k=8: floor-div masks it. Dies at k=2 for parent xor_lo
halves (small got 0, not 1; large got 1, not 0). Dies at k=8 for
small equals tot (got 3191, not 5225). Census k=8: small 3191,
large 2034. Do not PREFIX pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_wb.py --certify
Dump: research/cycle_wb.json
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
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vc import want_ej_xor_small
from cycle_vt import want_xor_lo_l_fl, want_xor_lo_s_fl
from cycle_vz import want_ej_xor_pg_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WA_JSON = Path(__file__).resolve().parent / "cycle_wa.json"
VT_JSON = Path(__file__).resolve().parent / "cycle_vt.json"
VC_JSON = Path(__file__).resolve().parent / "cycle_vc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ej_xor_s_fl(k: int) -> int:
    """leftover extra xor small: F form for k>=3; 0 at k<=2."""
    if k <= 2:
        return 0
    n = (
        (1 << (k - 3)) * (12 * fib(k) + 9 * fib(k - 2) - 25)
        - 2 * ((-1) ** (k - 1))
        + 3
    )
    return n // 3


def want_ej_xor_l_fl(k: int) -> int:
    """leftover extra xor large: F/L form for k>=3; 1 at k=2; 0 at k<=1."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (
        (1 << (k - 3)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 10)
        + 5 * ((-1) ** (k - 1))
        - 1
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: leftover extra xor small/large F/L; dies at k=3 with shift 0.

    Do not call leftover_extra_xor_split / leftover_xor_split here.
    Census is ej_hl_fold for k<=8.
    """
    n_ok = 0
    raw_s3 = (-2 * ((-1) ** 2) + 3) // 3
    raw_l3 = (5 * ((-1) ** 2) - 1) // 5
    miss_s3 = (
        (1 << 5) * (12 * fib(8) + 9 * fib(6) - 25) - 2 * ((-1) ** 7)
    ) // 3
    miss_lsign = (
        (1 << 5) * (5 * fib(6) + 16 * lucas(6) - 10) - 1
    ) // 5
    miss_lm1 = (
        (1 << 5) * (5 * fib(6) + 16 * lucas(6) - 10) + 5 * ((-1) ** 7)
    ) // 5
    if want_ej_xor_s_fl(0) != 0 or want_ej_xor_s_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_ej_xor_s_fl(2) != 0 or want_ej_xor_l_fl(2) != 1:
        return {"ok": False, "k2": True}
    if want_ej_xor_s_fl(3) != 3 or want_ej_xor_l_fl(3) != 3:
        return {"ok": False, "k3": True}
    if want_ej_xor_s_fl(8) != 3191 or want_ej_xor_l_fl(8) != 2034:
        return {"ok": False, "k8": True}
    if want_ej_xor_s_fl(3) == raw_s3:
        return {"ok": False, "k3s": True}
    if want_ej_xor_l_fl(3) == raw_l3:
        return {"ok": False, "k3l": True}
    if want_ej_xor_s_fl(8) == miss_s3:
        return {"ok": False, "s3": True}
    if want_ej_xor_l_fl(8) == miss_lsign:
        return {"ok": False, "ls": True}
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
        if want_ej_xor_s_fl(k) != want_ej_xor_small(k):
            return {"ok": False, "s": True, "k": k}
        if want_ej_xor_l_fl(k) != want_ej_xor_large(k):
            return {"ok": False, "l": True, "k": k}
        if want_ej_xor_s_fl(k) + want_ej_xor_l_fl(k) != want_ej_xor(k):
            return {"ok": False, "sum": True, "k": k}
        if k >= 3 and want_ej_xor_s_fl(k) != want_xor_lo_s_fl(k - 1):
            return {"ok": False, "vs": True, "k": k}
        if k >= 3 and want_ej_xor_l_fl(k) != want_xor_lo_l_fl(k - 1):
            return {"ok": False, "vl": True, "k": k}
        if k >= 3:
            ns = (
                (1 << (k - 3)) * (12 * fib(k) + 9 * fib(k - 2) - 25)
                - 2 * ((-1) ** (k - 1))
                + 3
            )
            nl = (
                (1 << (k - 3)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 10)
                + 5 * ((-1) ** (k - 1))
                - 1
            )
            if ns % 3 != 0 or ns // 3 != want_ej_xor_s_fl(k):
                return {"ok": False, "ds": True, "k": k}
            if nl % 5 != 0 or nl // 5 != want_ej_xor_l_fl(k):
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
    ok = (
        n_ok == K_ALG + 1
        and want_ej_xor_s_fl(3) != raw_s3
        and want_ej_xor_l_fl(3) != raw_l3
        and want_ej_xor_s_fl(8) != miss_s3
        and want_ej_xor_l_fl(8) != miss_lsign
        and want_ej_xor_l_fl(8) == miss_lm1
        and want_ej_xor_s_fl(2) != want_xor_lo_s_fl(1)
        and want_ej_xor_l_fl(2) != want_xor_lo_l_fl(1)
        and want_ej_xor_s_fl(8) != want_ej_xor(8)
        and want_ej_xor_s_fl(8) != want_ej_xor_pg_fl(8)
        and want_ej_xor_s_fl(8) == 3191
        and want_ej_xor_l_fl(8) == 2034
        and want_ej_xor(8) == 5225
        and want_j0_odd_lo(8) == 319
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
        and miss_s3 == 3190
        and miss_lsign == 2035
        and miss_lm1 == 2034
        and raw_s3 == 0
        and raw_l3 == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ej_hl_fold() -> dict:
    """k<=8 leftover extra xor small/large vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = leftover_extra_xor_split(k)
        if a["sign_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        sm = a["pg_s"] + a["gp_s"]
        lg = a["pg_l"] + a["gp_l"]
        if sm != want_ej_xor_s_fl(k):
            return {"ok": False, "s": True, "k": k, "got": sm}
        if lg != want_ej_xor_l_fl(k):
            return {"ok": False, "l": True, "k": k, "got": lg}
        if sm + lg != want_ej_xor(k):
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"ej_s": sm, "ej_l": lg}
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["ej_s"] == 0
        and rows["1"]["ej_l"] == 0
        and rows["2"]["ej_s"] == 0
        and rows["2"]["ej_l"] == 1
        and rows["3"]["ej_s"] == 3
        and rows["3"]["ej_l"] == 3
        and rows["8"]["ej_s"] == 3191
        and rows["8"]["ej_l"] == 2034
        and want_ej_xor_s_fl(4) == 15
        and want_ej_xor_l_fl(5) == 52
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=3 with shift 0; small +3 and large sign at k=8."""
    raw_s3 = (-2 * ((-1) ** 2) + 3) // 3
    raw_l3 = (5 * ((-1) ** 2) - 1) // 5
    miss_s3 = (
        (1 << 5) * (12 * fib(8) + 9 * fib(6) - 25) - 2 * ((-1) ** 7)
    ) // 3
    miss_lsign = (
        (1 << 5) * (5 * fib(6) + 16 * lucas(6) - 10) - 1
    ) // 5
    miss_lm1 = (
        (1 << 5) * (5 * fib(6) + 16 * lucas(6) - 10) + 5 * ((-1) ** 7)
    ) // 5
    a8 = leftover_extra_xor_split(8)
    sm = a8["pg_s"] + a8["gp_s"]
    lg = a8["pg_l"] + a8["gp_l"]
    ok = (
        want_ej_xor_s_fl(3) != raw_s3
        and want_ej_xor_l_fl(3) != raw_l3
        and want_ej_xor_s_fl(8) != miss_s3
        and want_ej_xor_l_fl(8) != miss_lsign
        and want_ej_xor_l_fl(8) == miss_lm1
        and want_ej_xor_s_fl(2) != want_xor_lo_s_fl(1)
        and want_ej_xor_l_fl(2) != want_xor_lo_l_fl(1)
        and want_ej_xor_s_fl(8) != want_ej_xor(8)
        and sm == 3191
        and lg == 2034
        and raw_s3 == 0
        and raw_l3 == 0
        and miss_s3 == 3190
        and miss_lsign == 2035
        and miss_lm1 == 2034
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
    wa = json.loads(WA_JSON.read_text())
    vt = json.loads(VT_JSON.read_text())
    vc = json.loads(VC_JSON.read_text())
    ok = (
        wa["checks"]["all_ok"]
        and vt["checks"]["all_ok"]
        and vc["checks"]["all_ok"]
        and wa["verdict"]["xor_pg_eq_FL_closed_k_ge_2"] == "LEMMA"
        and vt["verdict"]["xor_lo_s_eq_FL_closed_k_ge_2"] == "LEMMA"
        and vc["verdict"]["ej_xor_small_eq_lo_small_minus_j0_k_ge_3"] == "LEMMA"
        and wa["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wa["verdict"]["prize"] == "unsolved"
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
    cnt = ej_hl_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ej_hl_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_s_eq_FL_closed_k_ge_3": True,
            "ej_xor_l_eq_FL_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_s_eq_FL_closed_k_ge_3": "LEMMA",
            "ej_xor_l_eq_FL_closed_k_ge_3": "LEMMA",
            "ej_xor_s_FL_shift0_at_k3": "KILLED",
            "ej_xor_l_FL_shift0_at_k3": "KILLED",
            "ej_xor_s_without_plus3_at_k8": "KILLED",
            "ej_xor_l_without_sign_at_k8": "KILLED",
            "ej_xor_hl_eq_parent_xor_lo_hl_at_k2": "KILLED",
            "ej_xor_s_eq_ej_xor": "KILLED",
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
        "hl k8 s",
        dump["ej_hl_fold"]["rows"]["8"]["ej_s"],
        "l",
        dump["ej_hl_fold"]["rows"]["8"]["ej_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
