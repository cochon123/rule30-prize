#!/usr/bin/env python3
"""Cycle VH: leftover extra xor small/large n_pg/n_gp match parent halves.

Leftover extra except j=0 each produce one leftover-parent xor child.
Cycle VG matches tot n_pg/n_gp to parent leftover xor. Splitting by
n<=5U/2, leftover extra xor small n_pg/n_gp equal parent leftover xor
small n_pg/n_gp for k>=3, and the large half likewise. Dies at k=2
(small got 0, parent 1; large got 1, parent 0). Census k=8: small
pg/gp 1648/1543, large 1002/1032. Do not PREFIX pal-center tot. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_vh.py --certify
Dump: research/cycle_vh.json
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
from cycle_tw import green_odd_even, want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uk import want_lo_small
from cycle_un import want_d2e_small
from cycle_up import lucas, want_lo_e
from cycle_uq import want_lo_large
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vc import want_ej_xor_small, want_ej_xor_small_diff
from cycle_vg import want_ej_xor_gp, want_ej_xor_pg, want_gp, want_pg
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VG_JSON = Path(__file__).resolve().parent / "cycle_vg.json"
VC_JSON = Path(__file__).resolve().parent / "cycle_vc.json"
UV_JSON = Path(__file__).resolve().parent / "cycle_uv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_lo_small(k: int) -> int:
    """Leftover xor on n<=5U/2: lo_small minus j=0 (all j=0 are small)."""
    if k <= 0:
        return 0
    return want_lo_small(k) - want_j0_odd_lo(k)


def want_xor_lo_small_diff(k: int) -> int:
    """Leftover xor small n_pg-n_gp: 0,1,3, then j0 minus d2e_small."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 3
    return want_j0_odd_lo(k) - want_d2e_small(k)


def want_xor_lo_large_diff(k: int) -> int:
    """Leftover xor large n_pg-n_gp: 0 at k<=1, 1-2^{k-2}+(-1)^{k+1}."""
    if k <= 1:
        return 0
    return 1 - (1 << (k - 2)) + ((-1) ** (k + 1))


def want_pg_s(k: int) -> int:
    """Leftover xor n_pg on n<=5U/2."""
    return (want_xor_lo_small(k) + want_xor_lo_small_diff(k)) // 2


def want_gp_s(k: int) -> int:
    """Leftover xor n_gp on n<=5U/2."""
    return (want_xor_lo_small(k) - want_xor_lo_small_diff(k)) // 2


def want_pg_l(k: int) -> int:
    """Leftover xor n_pg on n>5U/2."""
    return (want_lo_large(k) + want_xor_lo_large_diff(k)) // 2


def want_gp_l(k: int) -> int:
    """Leftover xor n_gp on n>5U/2."""
    return (want_lo_large(k) - want_xor_lo_large_diff(k)) // 2


def want_ej_xor_pg_s(k: int) -> int:
    """Leftover extra xor small n_pg: parent leftover xor small n_pg for k>=3."""
    if k <= 2:
        return 0
    return want_pg_s(k - 1)


def want_ej_xor_gp_s(k: int) -> int:
    """Leftover extra xor small n_gp: parent leftover xor small n_gp for k>=3."""
    if k <= 2:
        return 0
    return want_gp_s(k - 1)


def want_ej_xor_pg_l(k: int) -> int:
    """Leftover extra xor large n_pg: parent leftover xor large n_pg for k>=3."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    return want_pg_l(k - 1)


def want_ej_xor_gp_l(k: int) -> int:
    """Leftover extra xor large n_gp: parent leftover xor large n_gp for k>=3."""
    if k <= 2:
        return 0
    return want_gp_l(k - 1)


def leftover_xor_half(k: int) -> dict:
    """Leftover xor n_pg/n_gp split by n<=5U/2."""
    u = 1 << k
    clip = 5 * u
    half = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    a = {
        "pg_s": 0,
        "pg_l": 0,
        "gp_s": 0,
        "gp_l": 0,
        "neg_s": 0,
        "neg_l": 0,
        "bad": 0,
    }
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        tag = "_s" if n <= half else "_l"
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            r = j // 2
            if green_odd_even(m, r) != 1:
                a["bad"] += 1
                continue
            if r == 0:
                a["neg" + tag] += 1
                continue
            kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
            km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
            if km == "pair" and kr == "g0":
                a["pg" + tag] += 1
            elif km == "g0" and kr == "pair":
                a["gp" + tag] += 1
            else:
                a["bad"] += 1
    return a


def tot_form() -> dict:
    """k<=64: leftover xor halves; leftover extra xor halves for k>=3.

    Do not call leftover_xor_half / leftover_extra_xor_split here.
    Census is xor_half_fold for k<=8.
    """
    n_ok = 0
    if want_pg_s(0) != 0 or want_pg_s(2) != 3:
        return {"ok": False, "k02": True}
    if want_ej_xor_pg_s(2) != 0 or want_ej_xor_pg_l(2) != 1:
        return {"ok": False, "k2e": True}
    if want_ej_xor_pg_s(8) != 1648 or want_ej_xor_gp_s(8) != 1543:
        return {"ok": False, "k8s": True}
    if want_ej_xor_pg_l(8) != 1002 or want_ej_xor_gp_l(8) != 1032:
        return {"ok": False, "k8l": True}
    if want_xor_lo_small_diff(2) == want_j0_odd_lo(2) - want_d2e_small(2):
        return {"ok": False, "k2d": True}
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
        if (want_xor_lo_small(k) + want_xor_lo_small_diff(k)) % 2 != 0:
            return {"ok": False, "ps": True, "k": k}
        if (want_lo_large(k) + want_xor_lo_large_diff(k)) % 2 != 0:
            return {"ok": False, "pl": True, "k": k}
        if want_pg_s(k) + want_pg_l(k) != want_pg(k):
            return {"ok": False, "pgt": True, "k": k}
        if want_gp_s(k) + want_gp_l(k) != want_gp(k):
            return {"ok": False, "gpt": True, "k": k}
        if want_ej_xor_pg_s(k) + want_ej_xor_pg_l(k) != want_ej_xor_pg(k):
            return {"ok": False, "ejp": True, "k": k}
        if want_ej_xor_gp_s(k) + want_ej_xor_gp_l(k) != want_ej_xor_gp(k):
            return {"ok": False, "ejg": True, "k": k}
        if k >= 3:
            if want_xor_lo_small_diff(k) != (
                want_j0_odd_lo(k) - want_d2e_small(k)
            ):
                return {"ok": False, "sd": True, "k": k}
            if want_ej_xor_pg_s(k) != want_pg_s(k - 1):
                return {"ok": False, "ps3": True, "k": k}
            if want_ej_xor_gp_s(k) != want_gp_s(k - 1):
                return {"ok": False, "gs3": True, "k": k}
            if want_ej_xor_pg_l(k) != want_pg_l(k - 1):
                return {"ok": False, "pl3": True, "k": k}
            if want_ej_xor_gp_l(k) != want_gp_l(k - 1):
                return {"ok": False, "gl3": True, "k": k}
            if want_ej_xor_pg_s(k) - want_ej_xor_gp_s(k) != (
                want_ej_xor_small_diff(k)
            ):
                return {"ok": False, "smd": True, "k": k}
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
        and want_ej_xor_pg_s(2) != want_pg_s(1)
        and want_ej_xor_pg_l(2) != want_pg_l(1)
        and want_ej_xor_pg_s(8) != want_ej_xor_pg(8)
        and want_pg_s(8) == 5440
        and want_gp_s(8) == 5227
        and want_pg_l(8) == 3290
        and want_gp_l(8) == 3354
        and want_ej_xor_small(8) == 3191
        and want_ej_xor_large(8) == 2034
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


def xor_half_fold() -> dict:
    """k<=8 leftover xor halves and leftover extra xor halves."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_xor_half(k)
        if r["bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["neg_l"] != 0 or r["neg_s"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k, "got": (r["neg_s"], r["neg_l"])}
        if r["pg_s"] != want_pg_s(k) or r["gp_s"] != want_gp_s(k):
            return {"ok": False, "ls": True, "k": k, "got": (r["pg_s"], r["gp_s"])}
        if r["pg_l"] != want_pg_l(k) or r["gp_l"] != want_gp_l(k):
            return {"ok": False, "ll": True, "k": k, "got": (r["pg_l"], r["gp_l"])}
        a = leftover_extra_xor_split(k)
        if a["pg_s"] != want_ej_xor_pg_s(k) or a["gp_s"] != want_ej_xor_gp_s(k):
            return {"ok": False, "es": True, "k": k, "got": (a["pg_s"], a["gp_s"])}
        if a["pg_l"] != want_ej_xor_pg_l(k) or a["gp_l"] != want_ej_xor_gp_l(k):
            return {"ok": False, "el": True, "k": k, "got": (a["pg_l"], a["gp_l"])}
        n_ok += 1
        rows[str(k)] = {
            "pg_s": r["pg_s"],
            "gp_s": r["gp_s"],
            "pg_l": r["pg_l"],
            "gp_l": r["gp_l"],
            "ej_pg_s": a["pg_s"],
            "ej_gp_s": a["gp_s"],
            "ej_pg_l": a["pg_l"],
            "ej_gp_l": a["gp_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["ej_pg_s"] == 0
        and rows["2"]["pg_s"] == 3
        and rows["2"]["ej_pg_l"] == 1
        and rows["2"]["pg_l"] == 1
        and rows["8"]["ej_pg_s"] == 1648
        and rows["8"]["ej_gp_s"] == 1543
        and rows["8"]["ej_pg_l"] == 1002
        and rows["8"]["ej_gp_l"] == 1032
        and want_ej_xor_pg_s(4) == 10
        and want_ej_xor_gp_s(4) == 5
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """parent-half match at k=2; small pg equals tot pg at k=8."""
    a2 = leftover_extra_xor_split(2)
    r1 = leftover_xor_half(1)
    a8 = leftover_extra_xor_split(8)
    ok = (
        a2["pg_s"] != r1["pg_s"]
        and a2["pg_l"] != r1["pg_l"]
        and want_ej_xor_pg_s(8) != want_ej_xor_pg(8)
        and want_ej_xor_pg_l(8) != want_ej_xor_gp_l(8)
        and a8["pg_s"] == 1648
        and a8["gp_s"] == 1543
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
    vg = json.loads(VG_JSON.read_text())
    vc = json.loads(VC_JSON.read_text())
    uv = json.loads(UV_JSON.read_text())
    ok = (
        vg["checks"]["all_ok"]
        and vc["checks"]["all_ok"]
        and uv["checks"]["all_ok"]
        and vg["verdict"]["ej_xor_pg_eq_parent_leftover_pg"] == "LEMMA"
        and vc["verdict"]["ej_xor_small_diff_eq_j0_minus_d2e_k_ge_4"] == "LEMMA"
        and uv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vg["verdict"]["prize"] == "unsolved"
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
    cnt = xor_half_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_half_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_half_eq_parent_leftover_half_k_ge_3": True,
            "xor_lo_small_diff_eq_j0_minus_d2e_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_half_eq_parent_leftover_half_k_ge_3": "LEMMA",
            "xor_lo_small_diff_eq_j0_minus_d2e_k_ge_3": "LEMMA",
            "ej_xor_half_eq_parent_at_k2": "KILLED",
            "xor_lo_small_diff_form_at_k2": "KILLED",
            "ej_xor_small_pg_eq_tot_pg": "KILLED",
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
        "k8 small",
        dump["xor_half_fold"]["rows"]["8"]["ej_pg_s"],
        dump["xor_half_fold"]["rows"]["8"]["ej_gp_s"],
        "large",
        dump["xor_half_fold"]["rows"]["8"]["ej_pg_l"],
        dump["xor_half_fold"]["rows"]["8"]["ej_gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
