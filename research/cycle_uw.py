#!/usr/bin/env python3
"""Cycle UW: leftover extra on n=1 mod 4 is sign-balanced; empty at 3U+1.

Covering n=3U has pal-left G=1 only at j=0 (unpaired) and j=U
(clip-edge), plus pal-center, so no leftover. Even parent leftover
union d=2 therefore produces no leftover extra at child n=3U+1.
On n=1 mod 4, s is even, so leftover extra has G(s,t)=1 iff j=0
mod 4 and G(s,t)=0 iff j=2 mod 4; those cells pair as (j,j+2) from
even parent leftover union d=2, so signs balance and leftover extra
on n=1 mod 4 contributes 0 to leftover-parent xor large difference.
The imbalance lives on n=3 mod 4. Dies at k=1 for equal
j mod 4 counts. Dies at k=0 for leftover empty at 3U (d=2 clip
overlap). Do not PREFIX leftover-parent xor large
difference or pal-center tot. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uw.py --certify
Dump: research/cycle_uw.json
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
from cycle_up import lucas, want_lo_e
from cycle_ur import leftover_at_n, parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor, want_ej_xor_large
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UV_JSON = Path(__file__).resolve().parent / "cycle_uv.json"
UU_JSON = Path(__file__).resolve().parent / "cycle_uu.json"
UT_JSON = Path(__file__).resolve().parent / "cycle_ut.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
K_MISS = 16
PAT0011 = (0, 0, 1, 1)


def want_3u(k: int) -> int:
    """Covering n=3U."""
    return 3 * (1 << k)


def want_miss_n(k: int) -> int:
    """Large covering n=3U+1 with no leftover extra."""
    return want_3u(k) + 1


def leftover_cell(n: int, j: int, k: int) -> bool:
    if G(n, j) == 0:
        return False
    if pal_kind(n, j, k) != "pair":
        return False
    if j >= 2 * n - j:
        return False
    d = n - j
    if d in (1, 2) or is_clip_edge(n, j, k):
        return False
    return True


def leftover_extra_n(n: int, k: int) -> int:
    """Leftover pal-pairs at even j on odd covering n."""
    if n % 2 == 0:
        return 0
    clip = 5 * (1 << k)
    c = 0
    for j in range(0, min(2 * n, clip) + 1, 2):
        if leftover_cell(n, j, k):
            c += 1
    return c


def leftover_extra_n1_split(k: int) -> dict:
    """Leftover extra on n=1 mod 4: j mod 4 counts; large n=3 empties."""
    u = 1 << k
    clip = 5 * u
    ph = parent_half(k)
    miss = want_miss_n(k)
    z = {
        "j0": 0,
        "j2": 0,
        "j0_lg": 0,
        "j2_lg": 0,
        "g_bad": 0,
        "n1_lg": 0,
        "n3_lg": 0,
        "n1_empty": 0,
        "n3_empty": 0,
        "miss_hit": 0,
        "bad_empty": 0,
    }
    for n in range(1, 4 * u, 2):
        extra_j0 = extra_j2 = extra = 0
        s = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if not leftover_cell(n, j, k):
                continue
            extra += 1
            if n % 4 != 1:
                continue
            t = j // 2
            gs = G(s, t)
            if j % 4 == 0:
                extra_j0 += 1
                if gs != 1:
                    z["g_bad"] += 1
            else:
                extra_j2 += 1
                if gs != 0:
                    z["g_bad"] += 1
        if n % 4 == 1:
            z["j0"] += extra_j0
            z["j2"] += extra_j2
            if n > ph:
                z["j0_lg"] += extra_j0
                z["j2_lg"] += extra_j2
                if extra:
                    z["n1_lg"] += 1
                else:
                    z["n1_empty"] += 1
                    if n == miss:
                        z["miss_hit"] += 1
                    else:
                        z["bad_empty"] += 1
        elif n % 4 == 3 and n > ph:
            if extra:
                z["n3_lg"] += 1
            else:
                z["n3_empty"] += 1
    return z


def tot_form() -> dict:
    """k<=64: n=3U pal-left G=1; n=1 mod 4 sign; miss n large covering."""
    n_ok = 0
    if want_3u(0) != 3 or want_miss_n(0) != 4:
        return {"ok": False, "k0": True}
    if want_3u(8) != 768 or want_miss_n(8) != 769:
        return {"ok": False, "k8": True}
    if G(3, 0) != 1 or G(3, 1) != 1 or G(3, 2) != 0 or G(3, 3) != 1:
        return {"ok": False, "g3": True}
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
        if m % 2 == 0:
            n = 2 * m + 1
            for t in range(0, m + 1):
                j = 2 * t
                if G(n, j) != 1:
                    continue
                gs = G(m, t)
                want = 1 if j % 4 == 0 else 0
                if gs != want:
                    return {"ok": False, "n1s": True, "m": m, "t": t}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        n = want_3u(k)
        miss = want_miss_n(k)
        ph = parent_half(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n != 3 * u:
            return {"ok": False, "3u": True, "k": k}
        if miss != n + 1:
            return {"ok": False, "ms": True, "k": k}
        if G(n, 0) != 1:
            return {"ok": False, "n0": True, "k": k}
        if G(n, n) != 1:
            return {"ok": False, "nn": True, "k": k}
        if k >= 1:
            if pal_kind(n, 0, k) != "unp":
                return {"ok": False, "unp": True, "k": k}
            if G(n, u) != 1:
                return {"ok": False, "gu": True, "k": k}
            if is_clip_edge(n, u, k) is not True:
                return {"ok": False, "clip": True, "k": k}
            if pal_kind(n, u, k) != "pair":
                return {"ok": False, "pu": True, "k": k}
            if G(n, 2 * u) != 0:
                return {"ok": False, "g2u": True, "k": k}
            if k >= 2 and n % 4 != 0:
                return {"ok": False, "n4": True, "k": k}
            if 2 * n - u != clip:
                return {"ok": False, "5u": True, "k": k}
            if pal_kind(n, 1, k) == "pair" and G(n, 1) != 0:
                return {"ok": False, "godd": True, "k": k}
            if G(n, u + 1) != 0:
                return {"ok": False, "up1": True, "k": k}
        if k >= 2:
            if miss <= ph or miss >= 4 * u:
                return {"ok": False, "mcov": True, "k": k}
            if miss % 4 != 1:
                return {"ok": False, "m1": True, "k": k}
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
        and want_miss_n(8) == 769
        and want_3u(8) == 768
        and want_ej_xor_large(8) == 2034
        and want_ej_xor(8) == 5225
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
        and want_lo_e(8) == 14114
        and want_even_j0_sm(8) == 318
        and leftover_at_n(want_3u(0), 0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def n1_bal_fold() -> dict:
    """k<=16 leftover empty at 3U and extra empty at 3U+1; k<=8 n1 split."""
    n_miss = 0
    miss_rows = {}
    for k in range(0, K_MISS + 1):
        n3 = want_3u(k)
        miss = want_miss_n(k)
        u = 1 << k
        lo = leftover_at_n(n3, k) if n3 < 4 * u else -1
        ex = leftover_extra_n(miss, k) if miss < 4 * u else -1
        if k >= 1 and lo != 0:
            return {"ok": False, "lo3": True, "k": k, "got": lo}
        if k >= 1 and miss < 4 * u and ex != 0:
            return {"ok": False, "ex": True, "k": k, "got": ex}
        n_miss += 1
        miss_rows[str(k)] = {"lo3": lo, "ex": ex}
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        z = leftover_extra_n1_split(k)
        if z["g_bad"] != 0:
            return {"ok": False, "g": True, "k": k}
        if k >= 2:
            if z["j0"] != z["j2"]:
                return {"ok": False, "bal": True, "k": k, "got": z}
            if z["j0_lg"] != z["j2_lg"]:
                return {"ok": False, "blg": True, "k": k, "got": z}
            if z["n3_empty"] != 0:
                return {"ok": False, "n3e": True, "k": k, "got": z}
            if z["n1_empty"] != 1 or z["miss_hit"] != 1:
                return {"ok": False, "n1e": True, "k": k, "got": z}
            if z["bad_empty"] != 0:
                return {"ok": False, "bad": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "j0": z["j0"],
            "j2": z["j2"],
            "j0_lg": z["j0_lg"],
            "j2_lg": z["j2_lg"],
            "n1_lg": z["n1_lg"],
            "n3_lg": z["n3_lg"],
            "n1_empty": z["n1_empty"],
        }
    ok = (
        n_miss == K_MISS + 1
        and n_ok == K_COUNT + 1
        and miss_rows["8"]["lo3"] == 0
        and miss_rows["8"]["ex"] == 0
        and miss_rows["16"]["lo3"] == 0
        and miss_rows["16"]["ex"] == 0
        and rows["8"]["j0"] == rows["8"]["j2"]
        and rows["8"]["j0_lg"] == 1645
        and rows["8"]["j2_lg"] == 1645
        and rows["7"]["j0_lg"] == 501
        and rows["7"]["n1_empty"] == 1
        and rows["7"]["n3_lg"] == 48
        and rows["1"]["j0"] != rows["1"]["j2"]
        and want_miss_n(8) != want_3u(8)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_miss": n_miss,
        "k_hi": K_COUNT,
        "rows": rows,
        "miss_rows": miss_rows,
    }


def killed_eq() -> dict:
    """leftover at 3U; extra at 3U+1; n=1 unbalanced."""
    z1 = leftover_extra_n1_split(1)
    z8 = leftover_extra_n1_split(8)
    ok = (
        leftover_at_n(want_3u(8), 8) == 0
        and leftover_extra_n(want_miss_n(8), 8) == 0
        and leftover_at_n(want_3u(0), 0) == 0
        and z1["j0"] != z1["j2"]
        and z8["j0"] == z8["j2"]
        and z8["j0_lg"] == z8["j2_lg"]
        and z8["n1_empty"] == 1
        and z8["n3_empty"] == 0
        and z8["j0_lg"] != 0
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and want_ph_check()
        and G(2, 1) == 0
        and G(3, 2) == 0
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


def want_ph_check() -> bool:
    return parent_half(2) == 10 and parent_half(8) == 640


def prefixes() -> dict:
    uv = json.loads(UV_JSON.read_text())
    uu = json.loads(UU_JSON.read_text())
    ut = json.loads(UT_JSON.read_text())
    ok = (
        uv["checks"]["all_ok"]
        and uu["checks"]["all_ok"]
        and ut["checks"]["all_ok"]
        and uv["verdict"]["odd_even_unique_van"] == "LEMMA"
        and uv["verdict"]["ej_xor_large_eq_lo_large_parent_k_ge_3"] == "LEMMA"
        and uv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uv["verdict"]["prize"] == "unsolved"
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
    cnt = n1_bal_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "n1_bal_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n_3u_no_leftover": True,
            "extra_empty_at_3u_plus_1": True,
            "n1_extra_sign_balanced_k_ge_2": True,
            "n1_extra_large_xor_diff_0": True,
            "lo_parent_large_diff_closed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n_3u_no_leftover": "LEMMA",
            "extra_empty_at_3u_plus_1": "LEMMA",
            "n1_extra_sign_balanced_k_ge_2": "LEMMA",
            "n1_bal_at_k1": "KILLED",
            "n1_extra_large_xor_diff_0": "LEMMA",
            "leftover_at_3u_k0_d2": "KILLED",
            "extra_at_3u_plus_1": "KILLED",
            "n1_unbalanced": "KILLED",
            "large_diff_from_n1": "KILLED",
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
            "lo_parent_large_diff_closed": "PREFIX",
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
        "n1_lg j0/j2 k8",
        dump["n1_bal_fold"]["rows"]["8"]["j0_lg"],
        dump["n1_bal_fold"]["rows"]["8"]["j2_lg"],
        "miss16",
        dump["n1_bal_fold"]["miss_rows"]["16"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
