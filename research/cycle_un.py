#!/usr/bin/env python3
"""Cycle UN: even covering d=2 on each half is parent d=1.

Even n=2m has G(n,n-2)=G(m,m-1), so d=2 iff parent d=1. For k>=1
the small half n<=5U/2 is m<=5 U_p/2, hence even d=2 small/large
equals Cycle UK's d=1 small/large at k-1. Odd n=2m+1 has the same
Green fold, and for k>=3 parent_half is even so odd m never sits on
the boundary: odd d=2 matches parent d=1 on each half. Dies at k=2
(parent_half=5 is odd). Do not PREFIX leftover extra or unpaired
extra or leftover-parent xor sum. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_un.py --certify
Dump: research/cycle_un.json
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
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n, want_d2_parity_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uk import want_d1_large, want_d1_small, want_lo_small
from cycle_um import want_lo_parent_diff
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UM_JSON = Path(__file__).resolve().parent / "cycle_um.json"
UK_JSON = Path(__file__).resolve().parent / "cycle_uk.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def want_d2e_small(k: int) -> int:
    """Even covering d=2 on n<=5U/2: 1 at k=0, parent d=1 small for k>=1."""
    if k <= 0:
        return 1
    return want_d1_small(k - 1)


def want_d2e_large(k: int) -> int:
    """Even covering d=2 on n>5U/2: 0 at k=0, parent d=1 large for k>=1."""
    if k <= 0:
        return 0
    return want_d1_large(k - 1)


def want_d2o_small(k: int) -> int:
    """Odd covering d=2 on n<=5U/2: 0,1,1, then parent d=1 small."""
    if k <= 0:
        return 0
    if k == 2:
        return 1
    return want_d1_small(k - 1)


def want_d2o_large(k: int) -> int:
    """Odd covering d=2 on n>5U/2: 1,0,2, then parent d=1 large."""
    if k <= 0:
        return 1
    if k == 2:
        return 2
    return want_d1_large(k - 1)


def want_d2_small(k: int) -> int:
    """Covering d=2 on n<=5U/2: even plus odd halves."""
    return want_d2e_small(k) + want_d2o_small(k)


def want_d2_large(k: int) -> int:
    """Covering d=2 on n>5U/2: even plus odd halves."""
    return want_d2e_large(k) + want_d2o_large(k)


def d2_half_split(k: int) -> dict:
    """Covering d=2 pal-pairs split by n<=5U/2 versus n>5U/2."""
    u = 1 << k
    half = (5 * u) // 2
    a = {
        "e_s": 0,
        "e_l": 0,
        "o_s": 0,
        "o_l": 0,
    }
    for n in range(1, 4 * u):
        if G(n, n - 2) == 0:
            continue
        tag = "_s" if n <= half else "_l"
        par = "e" if n % 2 == 0 else "o"
        a[par + tag] += 1
    return a


def tot_form() -> dict:
    """k<=64: even d=2 halves follow parent d=1; odd halves for k>=3."""
    n_ok = 0
    if want_d2e_small(0) != 1 or want_d2e_large(0) != 0:
        return {"ok": False, "k0e": True}
    if want_d2o_small(0) != 0 or want_d2o_large(0) != 1:
        return {"ok": False, "k0o": True}
    if want_d2e_small(8) != 106 or want_d2e_large(8) != 65:
        return {"ok": False, "k8e": True}
    if want_d2o_small(8) != 106 or want_d2o_large(8) != 65:
        return {"ok": False, "k8o": True}
    if want_d2_small(8) != 212 or want_d2_large(8) != 130:
        return {"ok": False, "k8t": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if G(2 * m, 2 * m - 2) != G(m, m - 1):
            return {"ok": False, "ge": True, "m": m}
        if G(2 * m + 1, 2 * m - 1) != G(m, m - 1):
            return {"ok": False, "go": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        half = (5 * u) // 2
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_d2e_small(k) + want_d2e_large(k) != want_d2_parity_n(k):
            return {"ok": False, "ep": True, "k": k}
        if want_d2o_small(k) + want_d2o_large(k) != want_d2_parity_n(k):
            return {"ok": False, "op": True, "k": k}
        if want_d2_small(k) + want_d2_large(k) != want_d2_n(k):
            return {"ok": False, "tp": True, "k": k}
        if k >= 1:
            if want_d2e_small(k) != want_d1_small(k - 1):
                return {"ok": False, "es": True, "k": k}
            if want_d2e_large(k) != want_d1_large(k - 1):
                return {"ok": False, "el": True, "k": k}
        if k >= 3:
            if want_d2o_small(k) != want_d1_small(k - 1):
                return {"ok": False, "os": True, "k": k}
            if want_d2o_large(k) != want_d1_large(k - 1):
                return {"ok": False, "ol": True, "k": k}
            if want_d2_small(k) != 2 * want_d1_small(k - 1):
                return {"ok": False, "ds": True, "k": k}
            if want_d2_large(k) != 2 * want_d1_large(k - 1):
                return {"ok": False, "dl": True, "k": k}
            parent_half = 5 * (1 << (k - 2))
            if parent_half % 2 != 0:
                return {"ok": False, "ph": True, "k": k}
            n_last = 2 * (parent_half - 1) + 1
            if n_last > half:
                return {"ok": False, "bd": True, "k": k}
            n_next = 2 * parent_half + 1
            if n_next <= half:
                return {"ok": False, "nx": True, "k": k}
        if k >= 2:
            if half % 2 != 0:
                return {"ok": False, "he": True, "k": k}
            parent_u = u // 2
            parent_half = (5 * parent_u) // 2
            if half // 2 != parent_half:
                return {"ok": False, "eh": True, "k": k}
        if k == 2:
            if want_d2o_small(k) == want_d1_small(k - 1):
                return {"ok": False, "k2s": True}
            if want_d2o_large(k) == want_d1_large(k - 1):
                return {"ok": False, "k2l": True}
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
        if 4 * u <= half:
            return {"ok": False, "hi": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d2e_small(2) != want_d2o_small(2)
        and want_d2e_large(2) != want_d2o_large(2)
        and want_d2_small(8) != want_d2_large(8)
        and want_d2_small(8) != want_d1_small(8)
        and want_d2o_small(2) != want_d1_small(1)
        and want_lo_small(8) == 10986
        and want_lo_parent_diff(8) == 233
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
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def d2_half_fold() -> dict:
    """k<=12: even/odd d=2 halves match closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = d2_half_split(k)
        if r["e_s"] != want_d2e_small(k) or r["e_l"] != want_d2e_large(k):
            return {"ok": False, "e": True, "k": k, "got": r}
        if r["o_s"] != want_d2o_small(k) or r["o_l"] != want_d2o_large(k):
            return {"ok": False, "o": True, "k": k, "got": r}
        tot = r["e_s"] + r["e_l"] + r["o_s"] + r["o_l"]
        if tot != want_d2_n(k):
            return {"ok": False, "t": True, "k": k, "got": tot}
        if r["e_s"] + r["o_s"] != want_d2_small(k):
            return {"ok": False, "s": True, "k": k}
        if r["e_l"] + r["o_l"] != want_d2_large(k):
            return {"ok": False, "l": True, "k": k}
        if k >= 3 and (r["e_s"] != r["o_s"] or r["e_l"] != r["o_l"]):
            return {"ok": False, "eo": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "e_s": r["e_s"],
            "e_l": r["e_l"],
            "o_s": r["o_s"],
            "o_l": r["o_l"],
            "s": r["e_s"] + r["o_s"],
            "l": r["e_l"] + r["o_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["e_s"] == 1
        and rows["0"]["o_l"] == 1
        and rows["2"]["o_s"] == 1
        and rows["2"]["o_l"] == 2
        and rows["8"]["e_s"] == 106
        and rows["8"]["e_l"] == 65
        and rows["8"]["o_s"] == 106
        and rows["8"]["o_l"] == 65
        and rows["8"]["s"] == 212
        and rows["8"]["l"] == 130
        and rows["2"]["e_s"] != rows["2"]["o_s"]
        and rows["8"]["s"] != rows["8"]["l"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """even d=2 small equals odd; odd halves follow parent at k=2."""
    ok = (
        want_d2e_small(2) != want_d2o_small(2)
        and want_d2e_large(2) != want_d2o_large(2)
        and want_d2o_small(2) != want_d1_small(1)
        and want_d2o_large(2) != want_d1_large(1)
        and want_d2_small(8) != want_d2_large(8)
        and want_d2_small(8) != want_d1_small(8)
        and want_d2e_small(8) != want_d2e_large(8)
        and G(2, 2) != 2 % 2
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
    um = json.loads(UM_JSON.read_text())
    uk = json.loads(UK_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    ok = (
        um["checks"]["all_ok"]
        and uk["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and um["verdict"]["lo_parent_diff_eq_3_2km1_J"] == "LEMMA"
        and uk["verdict"]["lo_small_eq_tot_minus_d1"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and um["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and um["verdict"]["prize"] == "unsolved"
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
    cnt = d2_half_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "d2_half_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d2e_half_eq_parent_d1": True,
            "d2o_half_eq_parent_d1_kge3": True,
            "d2_small_eq_2_parent_d1_small": True,
            "d2e_small_eq_d2o_small": False,
            "d2o_half_eq_parent_at_k2": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d2e_half_eq_parent_d1": "LEMMA",
            "d2o_half_eq_parent_d1_kge3": "LEMMA",
            "d2_small_eq_2_parent_d1_small": "LEMMA",
            "d2e_small_eq_d2o_small": "KILLED",
            "d2o_half_eq_parent_at_k2": "KILLED",
            "d2_small_eq_d2_large": "KILLED",
            "d2_small_eq_d1_small": "KILLED",
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
        "d2_small k8",
        dump["d2_half_fold"]["rows"]["8"]["s"],
        "e_s",
        dump["d2_half_fold"]["rows"]["8"]["e_s"],
        "o_s",
        dump["d2_half_fold"]["rows"]["8"]["o_s"],
        "l",
        dump["d2_half_fold"]["rows"]["8"]["l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
