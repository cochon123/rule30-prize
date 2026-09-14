#!/usr/bin/env python3
"""Cycle TE: pal-distance 2 pairs partition odd n with d=1; count 2 J_{k+1}.

Pal-distance 2 pairs have d=2, so j=n-2 and partner n+2. For n=2m
or n=2m+1, G(n, n-2)=G(m, m-1), so the cell is a pal-pair iff
G(m, m-1)=1. Even and odd covering n each contribute J_{k+1} pairs,
total 2 J_{k+1}. On odd covering n, G(n, n-1) xor G(n, n-2)=1
(n=1 has only d=1), so d=1 and d=2 partition the odd covering
clocks: J_{k+1}+J_{k+2}=2^{k+1}. Partner n+2 is clipped except the
single clip-edge cell n=3 at k=0. Spat mismatch is not identically
0. Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_te.py --certify
Dump: research/cycle_te.json
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
from cycle_td import want_d1_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"
TC_JSON = Path(__file__).resolve().parent / "cycle_tc.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_CELL = 8
Q = 10
PAT0011 = (0, 0, 1, 1)


def want_d2_parity_n(k: int) -> int:
    """Even or odd covering d=2 pal-pair count: J_{k+1}."""
    return jacobsthal(k + 1)


def want_d2_n(k: int) -> int:
    """Pal-distance 2 pal-pair count: 2 J_{k+1}."""
    return 2 * jacobsthal(k + 1)


def tot_form() -> dict:
    """k<=64: J_n+J_{n+1}=2^n; G fold; partition; clip only k=0 n=3."""
    n_ok = 0
    if jacobsthal(0) != 0 or jacobsthal(1) != 1 or jacobsthal(2) != 1:
        return {"ok": False, "J0": True}
    if want_d2_n(0) != 2 or want_d2_parity_n(0) != 1:
        return {"ok": False, "base": True}
    for n in range(0, K_ALG + 3):
        if jacobsthal(n) + jacobsthal(n + 1) != (1 << n):
            return {"ok": False, "Jsum": True, "n": n}
    for k in range(0, K_ALG + 1):
        if want_d1_n(k) + want_d2_parity_n(k) != 1 << (k + 1):
            return {"ok": False, "part": True, "k": k}
        if want_d2_n(k) != 2 * want_d2_parity_n(k):
            return {"ok": False, "twice": True, "k": k}
        u = 1 << k
        clip = 5 * u
        edge_n = clip - 2
        in_cover = 0 <= edge_n < 4 * u
        if in_cover != (k == 0):
            return {"ok": False, "edge": True, "k": k, "n": edge_n}
        if k == 0 and (edge_n != 3 or clip_j(3, 0) != 1):
            return {"ok": False, "k0": True}
        samples = {0, 1, 2, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for n in samples:
            if n < 2 or n >= 4 * u:
                continue
            m = n // 2
            if G(n, n - 2) != G(m, m - 1):
                return {"ok": False, "fold": True, "k": k, "n": n}
            if n % 2 and G(n, n - 1) ^ G(n, n - 2) != 1:
                return {"ok": False, "xor": True, "k": k, "n": n}
            jp = n + 2
            if G(n, n - 2) == 1:
                kind = pal_kind(n, n - 2, k)
                if kind != "pair":
                    return {"ok": False, "kind": True, "k": k, "n": n}
                if jp > clip:
                    return {"ok": False, "clip": True, "k": k, "n": n}
                if clip_j(n, k) == n - 2 and not (k == 0 and n == 3):
                    return {"ok": False, "ov": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d2_n(0) == 2
        and want_d2_n(7) == 170
        and want_d2_n(8) == 342
        and want_d1_n(0) + want_d2_parity_n(0) == 2
        and G(1, 0) == 1
        and G(2, 0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def d2_count() -> dict:
    """k<=12: even/odd counts J_{k+1}; odd n d=1 xor d=2; always pair."""
    n_ok = 0
    n_cell = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        clip = 5 * u
        n_even = n_odd = n_d1 = n_part = n_edge = 0
        for n in range(0, 4 * u):
            if n % 2:
                g1 = G(n, n - 1) if n >= 1 else 0
                g2 = G(n, n - 2) if n >= 2 else 0
                if n == 1:
                    if g1 == 1 and g2 == 0:
                        n_part += 1
                elif g1 ^ g2 == 1:
                    n_part += 1
                if n >= 1 and g1 == 1 and pal_kind(n, n - 1, k) == "pair":
                    n_d1 += 1
            if n < 2 or G(n, n - 2) == 0:
                continue
            if pal_kind(n, n - 2, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            if n + 2 > clip:
                return {"ok": False, "clip": True, "k": k, "n": n}
            if clip_j(n, k) == n - 2:
                n_edge += 1
                if not (k == 0 and n == 3):
                    return {"ok": False, "edge": True, "k": k, "n": n}
            if n % 2:
                n_odd += 1
            else:
                n_even += 1
        want_p = want_d2_parity_n(k)
        if (
            n_even != want_p
            or n_odd != want_p
            or n_d1 != want_d1_n(k)
            or n_part != 1 << (k + 1)
            or n_edge != int(k == 0)
        ):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_even": n_even,
                "n_odd": n_odd,
                "n_d1": n_d1,
                "n_part": n_part,
                "n_edge": n_edge,
                "want": want_p,
            }
        n_cell += n_even + n_odd
        n_ok += 1
        rows[str(k)] = {
            "n_d2": n_even + n_odd,
            "n_even": n_even,
            "n_odd": n_odd,
            "n_d1": n_d1,
            "n_edge": n_edge,
        }
    ok = (
        n_ok == K_COUNT + 1
        and n_cell == sum(want_d2_n(k) for k in range(0, K_COUNT + 1))
        and rows["0"]["n_d2"] == 2
        and rows["0"]["n_edge"] == 1
        and rows["7"]["n_d2"] == 170
        and rows["12"]["n_d2"] == 5462
        and rows["1"]["n_edge"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_cell": n_cell,
        "k_hi": K_COUNT,
        "rows": rows,
    }


def d2_spat() -> dict:
    """k<=8 pal-distance 2 spat mismatch: not identically 0."""
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
        n_d2 = n_eq_c = 0
        for n in range(2, 4 * u):
            if G(n, n - 2) == 0:
                continue
            t = covering_t(k, n)
            s = even_s(n, k)
            left = covering_and_spat(packed[t], s, 2)
            right = covering_and_spat(packed[t], s, -2)
            raw = left ^ right
            tot ^= raw
            cand = pal_center_and(packed[t], s)
            pal_c ^= cand
            if raw == cand:
                n_eq_c += 1
            n_d2 += 1
        if n_d2 != want_d2_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_d2": n_d2,
                "want": want_d2_n(k),
            }
        n_fire += tot
        n_ok += 1
        rows[str(k)] = {
            "n_d2": n_d2,
            "tot": tot,
            "pal_c": pal_c,
            "n_eq_c": n_eq_c,
        }
    fired = any(rows[str(k)]["tot"] for k in range(0, K_CELL + 1))
    ne_pal = any(
        rows[str(k)]["tot"] != rows[str(k)]["pal_c"]
        for k in range(0, K_CELL + 1)
    )
    ok = (
        n_ok == K_CELL + 1
        and fired
        and ne_pal
        and rows["0"]["tot"] == 1
        and rows["1"]["tot"] == 0
        and rows["6"]["tot"] == 1
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
    """d=2 AND identically 0; d=2 cells equal clip-edge cells."""
    ok = (
        want_d2_n(0) != want_edge_n(0)
        and clip_j(3, 0) == 1
        and want_d2_n(1) == 2
        and want_edge_n(1) == 3
        and G(2, 0) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    td = json.loads(TD_JSON.read_text())
    tc = json.loads(TC_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        td["checks"]["all_ok"]
        and tc["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and td["verdict"]["d1_odd_iff_G_m_m1_0"] == "LEMMA"
        and tc["verdict"]["clip_pair_and_0_both_sides"] == "LEMMA"
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and td["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and td["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
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
    cnt = d2_count()
    spat = d2_spat()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, spat, kl, sc, pref)
    dump = {
        "cycle": "TE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "d2_count": {k: cnt[k] for k in cnt if k != "ok"},
        "d2_spat": {k: spat[k] for k in spat if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d2_fold_G_m_m1": True,
            "d2_parity_eq_jacobsthal": True,
            "d2_count_eq_2_jacobsthal": True,
            "odd_n_d1_xor_d2": True,
            "d2_and_identically_0": False,
            "d2_cells_eq_clip_edge": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d2_fold_G_m_m1": "LEMMA",
            "d2_parity_eq_jacobsthal": "LEMMA",
            "d2_count_eq_2_jacobsthal": "LEMMA",
            "odd_n_d1_xor_d2": "LEMMA",
            "d2_clipped_except_k0_n3": "LEMMA",
            "d2_and_identically_0": "KILLED",
            "d2_cells_eq_clip_edge": "KILLED",
            "d2_spat_eq_pal_center": "KILLED",
            "d1_and_identically_0": "KILLED",
            "d1_cells_eq_clip_edge": "KILLED",
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
        "d2 k12",
        dump["d2_count"]["rows"]["12"]["n_d2"],
        "spat k8 tot",
        dump["d2_spat"]["rows"]["8"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
