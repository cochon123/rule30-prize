#!/usr/bin/env python3
"""Cycle TD: pal-adjacent d=1 pal-pairs are odd n with Jacobsthal count.

Pal-adjacent pairs have d=1, so j=n-1 and partner n+1. Even covering
n never has a d=1 pal-pair (G(even, odd)=0). Odd n=2m+1 is a pal-pair
iff G(m, m-1)=0. Partner n+1<=4U<5U, so the pair is always clipped.
Count A(k)=#{m in [0, 2^{k+1}): G(m, m-1)=0} equals Jacobsthal
J_{k+2}: even m all contribute and odd m=2l+1 contribute iff
G(l, l-1)=1, hence A(k)=2^{k+1}-A(k-1) with A(0)=1. Same integer as
clip-edge count, disjoint cells (j=n-1 vs j=2n-5U). Spat mismatch is
not identically 0. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_td.py --certify
Dump: research/cycle_td.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_st import pal_center_and
from cycle_su import covering_and_spat
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_tc import clip_j
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TC_JSON = Path(__file__).resolve().parent / "cycle_tc.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"
SU_JSON = Path(__file__).resolve().parent / "cycle_su.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_CELL = 8
Q = 10
PAT0011 = (0, 0, 1, 1)


def want_d1_n(k: int) -> int:
    """Pal-adjacent d=1 pal-pair count: J_{k+2}."""
    return jacobsthal(k + 2)


def tot_form() -> dict:
    """k<=64: J_{n+1}=2^n-J_n; A(k)=2^{k+1}-A(k-1); G fold; disjoint."""
    n_ok = 0
    if jacobsthal(0) != 0 or jacobsthal(1) != 1 or jacobsthal(2) != 1:
        return {"ok": False, "J0": True}
    if want_d1_n(0) != 1 or want_d1_n(1) != 3:
        return {"ok": False, "base": True}
    for n in range(0, K_ALG + 3):
        if jacobsthal(n + 1) != (1 << n) - jacobsthal(n):
            return {"ok": False, "Jrec": True, "n": n}
    for k in range(0, K_ALG + 1):
        if want_d1_n(k) != want_edge_n(k):
            return {"ok": False, "int": True, "k": k}
        if k >= 1 and want_d1_n(k) != (1 << (k + 1)) - want_d1_n(k - 1):
            return {"ok": False, "Arec": True, "k": k}
        u = 1 << k
        clip = 5 * u
        if 4 * u - 1 >= clip - 1:
            return {"ok": False, "cover": True, "k": k}
        samples = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for m in samples:
            if m < 0 or m >= 2 * u:
                continue
            n = 2 * m + 1
            j = n - 1
            jp = n + 1
            if n >= 4 * u:
                continue
            fold = 1 ^ G(m, m - 1)
            if G(n, j) != fold:
                return {"ok": False, "fold": True, "k": k, "m": m}
            if jp > 4 * u or jp > clip:
                return {"ok": False, "clip": True, "k": k, "m": m}
            if pal_kind(n, j, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "m": m}
            if clip_j(n, k) == j:
                return {"ok": False, "edge": True, "k": k, "n": n}
            if n % 2 == 0:
                return {"ok": False, "odd": True, "k": k, "n": n}
        for n in (0, 2, u if u % 2 == 0 else u + 1, 4 * u - 2):
            if n < 0 or n >= 4 * u or n % 2:
                continue
            if n >= 1 and G(n, n - 1) != 0:
                return {"ok": False, "even": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d1_n(0) == 1
        and want_d1_n(7) == 171
        and want_d1_n(8) == 341
        and G(1, 0) == 1
        and G(0, -1) == 0
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def d1_count() -> dict:
    """k<=12: even n empty; odd n pal-pair iff G(m,m-1)=0; count J_{k+2}."""
    n_ok = 0
    n_cell = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        clip = 5 * u
        n_even = n_odd = n_bad = 0
        for n in range(0, 4 * u):
            j = n - 1
            if j < 0:
                continue
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            if n + 1 > clip or clip_j(n, k) == j:
                return {"ok": False, "edge": True, "k": k, "n": n}
            if n % 2 == 0:
                n_even += 1
                continue
            m = n // 2
            if G(m, m - 1) != 0:
                n_bad += 1
                continue
            n_odd += 1
        if n_even or n_bad or n_odd != want_d1_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_even": n_even,
                "n_odd": n_odd,
                "n_bad": n_bad,
                "want": want_d1_n(k),
            }
        n_cell += n_odd
        n_ok += 1
        rows[str(k)] = {"n_d1": n_odd, "n_even": n_even}
    ok = (
        n_ok == K_COUNT + 1
        and n_cell == sum(want_d1_n(k) for k in range(0, K_COUNT + 1))
        and rows["0"]["n_d1"] == 1
        and rows["7"]["n_d1"] == 171
        and rows["12"]["n_d1"] == 5461
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_cell": n_cell,
        "k_hi": K_COUNT,
        "rows": rows,
    }


def d1_spat() -> dict:
    """k<=8 pal-adjacent spat mismatch: not identically 0, disjoint cells."""
    t_hi = Q * (1 << K_CELL)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    n_fire = 0
    rows = {}
    for k in range(0, K_CELL + 1):
        u = 1 << k
        tot = pal_c = 0
        n_d1 = n_eq_c = 0
        for n in range(1, 4 * u, 2):
            j = n - 1
            if G(n, j) == 0:
                continue
            t = covering_t(k, n)
            s = even_s(n, k)
            left = covering_and_spat(packed[t], s, 1)
            right = covering_and_spat(packed[t], s, -1)
            raw = left ^ right
            tot ^= raw
            cand = pal_center_and(packed[t], s)
            pal_c ^= cand
            if raw == cand:
                n_eq_c += 1
            n_d1 += 1
            if clip_j(n, k) == j:
                return {"ok": False, "edge": True, "k": k, "n": n}
        if n_d1 != want_d1_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_d1": n_d1,
                "want": want_d1_n(k),
            }
        n_fire += tot
        n_ok += 1
        rows[str(k)] = {
            "n_d1": n_d1,
            "tot": tot,
            "pal_c": pal_c,
            "n_eq_c": n_eq_c,
        }
    fired = any(rows[str(k)]["tot"] for k in range(0, K_CELL + 1))
    ne_pal = any(
        rows[str(k)]["tot"] != rows[str(k)]["pal_c"]
        for k in range(0, K_CELL + 1)
    )
    ne_cell = any(
        rows[str(k)]["n_eq_c"] != rows[str(k)]["n_d1"]
        for k in range(0, K_CELL + 1)
    )
    ok = (
        n_ok == K_CELL + 1
        and fired
        and ne_pal
        and ne_cell
        and rows["0"]["tot"] == 0
        and rows["3"]["tot"] == 1
        and rows["6"]["tot"] == 1
        and rows["7"]["tot"] == 1
        and n_fire >= 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_fire": n_fire,
        "k_hi": K_CELL,
        "rows": rows,
        "ident0": False,
    }


def killed_eq() -> dict:
    """d=1 AND identically 0; d=1 cells equal clip-edge cells."""
    ok = (
        want_d1_n(0) == want_edge_n(0)
        and clip_j(1, 0) != 0
        and G(2, 1) == 0
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tc = json.loads(TC_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    su = json.loads(SU_JSON.read_text())
    ok = (
        tc["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and su["checks"]["all_ok"]
        and tc["verdict"]["clip_pair_and_0_both_sides"] == "LEMMA"
        and tc["verdict"]["clip_edge_raw_tot_0"] == "LEMMA"
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and su["verdict"]["covering_and_eq_spat_2d"] == "LEMMA"
        and su["verdict"]["pair_raw_eq_spat_d_xor_minus_d"] == "LEMMA"
        and tc["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tc["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, spat, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and spat["ok"] and kl["ok"]
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
    cnt = d1_count()
    spat = d1_spat()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, spat, kl, sc, pref)
    dump = {
        "cycle": "TD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "d1_count": {k: cnt[k] for k in cnt if k != "ok"},
        "d1_spat": {k: spat[k] for k in spat if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d1_even_n_empty": True,
            "d1_odd_iff_G_m_m1_0": True,
            "d1_count_eq_jacobsthal": True,
            "d1_disjoint_clip_edge": True,
            "d1_and_identically_0": False,
            "d1_cells_eq_clip_edge": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d1_even_n_empty": "LEMMA",
            "d1_odd_iff_G_m_m1_0": "LEMMA",
            "d1_count_eq_jacobsthal": "LEMMA",
            "d1_always_clipped_pair": "LEMMA",
            "d1_disjoint_clip_edge": "LEMMA",
            "d1_and_identically_0": "KILLED",
            "d1_cells_eq_clip_edge": "KILLED",
            "d1_spat_eq_pal_center": "KILLED",
            "pal_c_e_period8": "KILLED",
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
        "d1 k12",
        dump["d1_count"]["rows"]["12"]["n_d1"],
        "spat k8 tot",
        dump["d1_spat"]["rows"]["8"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
