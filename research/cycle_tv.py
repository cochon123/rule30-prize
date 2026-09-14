#!/usr/bin/env python3
"""Cycle TV: odd-j leftover count equals even leftover count.

Even leftover is even-j (G(2m,odd)=0). Odd-j pal-pairs 2-fold
parent pal-pairs dropping clip-edge (Cycle TB), so odd-j leftover
at k>=2 is parent leftover plus parent d=2, matching even leftover
(Cycle TU). The two families are disjoint. Dies at k=1 for the
same d=2/clip-edge overlap. Odd leftover is strictly larger.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tv.py --certify
Dump: research/cycle_tv.json
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
from cycle_sv import forced_right_j, pal_left_never_forced, unique_even_n
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering, want_even_lo_inc
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def leftover_j_split(k: int) -> dict:
    """Leftover pal-pairs split by n-parity and j-parity."""
    u = 1 << k
    clip = 5 * u
    lo = lo_e = lo_o = 0
    lo_oj = lo_ej = 0
    lo_oj_e = lo_oj_o = lo_ej_e = lo_ej_o = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            lo += 1
            even_n = n % 2 == 0
            even_j = j % 2 == 0
            if even_n:
                lo_e += 1
            else:
                lo_o += 1
            if even_j:
                lo_ej += 1
                if even_n:
                    lo_ej_e += 1
                else:
                    lo_ej_o += 1
            else:
                lo_oj += 1
                if even_n:
                    lo_oj_e += 1
                else:
                    lo_oj_o += 1
    return {
        "lo": lo,
        "lo_e": lo_e,
        "lo_o": lo_o,
        "lo_oj": lo_oj,
        "lo_ej": lo_ej,
        "lo_oj_e": lo_oj_e,
        "lo_oj_o": lo_oj_o,
        "lo_ej_e": lo_ej_e,
        "lo_ej_o": lo_ej_o,
    }


def tot_form() -> dict:
    """k<=64: even leftover even-j; odd-j 2-fold increment; G even n."""
    n_ok = 0
    if leftover_j_split(0)["lo_oj"] != 0:
        return {"ok": False, "k0": True}
    if leftover_j_split(1)["lo_oj"] != 1:
        return {"ok": False, "k1": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2 and want_even_lo_inc(k) != 2 * jacobsthal(k):
            return {"ok": False, "inc": True, "k": k}
        samples_m = {0, 1, u // 2 if u >= 2 else 0, u, 2 * u - 1}
        for m in samples_m:
            n = 2 * m
            if n >= 4 * u:
                continue
            for j in (1, 3, min(2 * n - 1, 5 * u) if 2 * n >= 1 else 1):
                if 0 <= j <= min(2 * n, 5 * u) and j % 2 == 1 and G(n, j) != 0:
                    return {"ok": False, "godd": True, "k": k, "n": n, "j": j}
        if k >= 1:
            if not unique_even_leftover(k):
                return {"ok": False, "u": True, "k": k}
            j4 = forced_right_j(4, k)
            if j4 % 2 != 0 or unique_even_n(k) % 2 != 0:
                return {"ok": False, "uj": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def leftover_j_fold() -> dict:
    """k<=8: odd-j leftover equals even leftover; 2-fold k>=2."""
    n_ok = 0
    rows = {}
    prev_lo = None
    for k in range(0, K_COUNT + 1):
        r = leftover_j_split(k)
        if r["lo"] != r["lo_e"] + r["lo_o"] or r["lo"] != r["lo_oj"] + r["lo_ej"]:
            return {"ok": False, "sum": True, "k": k}
        if r["lo_oj_e"] != 0 or r["lo_oj"] != r["lo_oj_o"]:
            return {"ok": False, "oje": True, "k": k}
        if r["lo_oj"] != r["lo_e"] or r["lo_ej"] != r["lo_o"]:
            return {"ok": False, "eq": True, "k": k, **r}
        if r["lo_ej_e"] != r["lo_e"]:
            return {"ok": False, "eje": True, "k": k}
        if k >= 2:
            want = prev_lo + want_even_lo_inc(k)
            if r["lo_oj"] != want or r["lo_e"] != want:
                return {"ok": False, "fold": True, "k": k, "lo_oj": r["lo_oj"], "want": want}
        if k == 1:
            if r["lo_oj"] != 1 or prev_lo + want_d2_n(0) == r["lo_oj"]:
                return {"ok": False, "k1": True, "lo_oj": r["lo_oj"]}
        if k >= 1 and r["lo_o"] == r["lo_e"] and r["lo"] != 0:
            return {"ok": False, "odd_eq_even": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "lo": r["lo"],
            "lo_e": r["lo_e"],
            "lo_o": r["lo_o"],
            "lo_oj": r["lo_oj"],
            "lo_ej": r["lo_ej"],
            "lo_ej_o": r["lo_ej_o"],
        }
        prev_lo = r["lo"]
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo_oj"] == 0
        and rows["1"]["lo_oj"] == 1
        and rows["2"]["lo_oj"] == 6
        and rows["8"]["lo_oj"] == 14114
        and rows["8"]["lo_e"] == 14114
        and rows["8"]["lo_o"] == 31744
        and rows["8"]["lo_o"] != rows["8"]["lo_e"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """odd leftover equals even leftover; odd-j 2-fold all k."""
    r1 = leftover_j_split(1)
    ok = (
        r1["lo_oj"] == r1["lo_e"]
        and r1["lo_o"] != r1["lo_e"]
        and d2_clip_covering(0)
        and not d2_clip_covering(1)
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    tu = json.loads(TU_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    ok = (
        tu["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and tu["verdict"]["even_lo_eq_parent_lo_plus_d2_k_ge_2"] == "LEMMA"
        and tu["verdict"]["pair_types_partition_k_ge_1"] == "LEMMA"
        and tb["verdict"]["oddj_pairs_drop_clip_edge"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and tu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tu["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d2_n(0) == 2
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
    cnt = leftover_j_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_j_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "oddj_lo_eq_even_lo": True,
            "oddj_lo_eq_parent_lo_plus_d2_k_ge_2": True,
            "odd_lo_eq_even_lo": False,
            "oddj_lo_fold_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "oddj_lo_eq_even_lo": "LEMMA",
            "oddj_lo_eq_parent_lo_plus_d2_k_ge_2": "LEMMA",
            "odd_lo_eq_even_lo": "KILLED",
            "oddj_lo_fold_all_k": "KILLED",
            "even_lo_eq_parent_lo": "KILLED",
            "pair_types_partition_all_k": "KILLED",
            "leftover_pairs_empty": "KILLED",
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
        "oj k8",
        dump["leftover_j_fold"]["rows"]["8"]["lo_oj"],
        "lo_e",
        dump["leftover_j_fold"]["rows"]["8"]["lo_e"],
        "lo_o",
        dump["leftover_j_fold"]["rows"]["8"]["lo_o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
