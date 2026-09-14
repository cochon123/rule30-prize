#!/usr/bin/env python3
"""Cycle TB: odd-j pal-pairs drop clip-edge; edge count is Jacobsthal.

Odd-j pal-pairs at k are the 2-fold of parent pal-pairs with
pal-partner <=5U-1. Parent clip-edge pal-pairs (partner=5U) map to
unpaired at the child. Clip-edge count is Jacobsthal J_{k+2}:
even-n edge 2-folds all parent edge, and each of n=1,3 mod 4 folds
onto edge at k-2, so E(k)=E(k-1)+2 E(k-2). Odd-j distance doubles
and the covering time is Cycle SZ's odd-child 2-fold. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tb.py --certify
Dump: research/cycle_tb.json
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
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_sz import odd_child_t
from cycle_ta import pal_kind, pal_split

OUT = Path(__file__).resolve().with_suffix(".json")
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
SZ_JSON = Path(__file__).resolve().parent / "cycle_sz.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_FOLD = 8
K_EDGE = 12
Q = 10
PAT0011 = (0, 0, 1, 1)


def jacobsthal(n: int) -> int:
    """J_n = (2^n - (-1)^n)/3."""
    return (pow(2, n) - (-1) ** n) // 3


def want_edge_n(k: int) -> int:
    """Clip-edge pal-pair count: J_{k+2}."""
    return jacobsthal(k + 2)


def edge_count(k: int) -> dict:
    """Clip-edge pal-pairs split by n mod 2 and n mod 4."""
    u = 1 << k
    clip = 5 * u
    even = odd = n1 = n3 = 0
    for n in range(0, 4 * u):
        j = 2 * n - clip
        if j < 0 or j >= n or G(n, j) == 0:
            continue
        if n % 2 == 0:
            even += 1
        else:
            odd += 1
            if n % 4 == 1:
                n1 += 1
            else:
                n3 += 1
    return {"even": even, "odd": odd, "n1": n1, "n3": n3, "tot": even + odd}


def tot_form() -> dict:
    """k<=64: Jacobsthal recurrence; G fold samples; odd-j d and time."""
    n_ok = 0
    if jacobsthal(0) != 0 or jacobsthal(1) != 1 or jacobsthal(2) != 1:
        return {"ok": False, "J0": True}
    if want_edge_n(0) != 1 or want_edge_n(1) != 3:
        return {"ok": False, "base": True}
    for k in range(0, K_ALG + 1):
        if k >= 2 and want_edge_n(k) != want_edge_n(k - 1) + 2 * want_edge_n(k - 2):
            return {"ok": False, "rec": True, "k": k}
        if k >= 1:
            u = 1 << (k - 1)
            clip = 5 * u
            clipc = 5 * (1 << k)
            samples = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
            for m in samples:
                if m < 0 or m >= 4 * u:
                    continue
                for r in (0, m) if m else (0,):
                    if r > 2 * m:
                        continue
                    n = 2 * m + 1
                    j = 2 * r + 1
                    if j >= n or j < 0:
                        continue
                    jp = 2 * n - j
                    jp_p = 2 * m - r
                    if j % 2 == 1 and (n - j) != 2 * (m - r):
                        return {"ok": False, "d": True, "k": k, "m": m, "r": r}
                    if odd_child_t(m, k) != covering_t(k, n):
                        return {"ok": False, "t": True, "k": k, "m": m}
                    if jp_p == clip and jp <= clipc:
                        return {"ok": False, "edge": True, "k": k, "m": m, "r": r}
                    if jp_p == clip and pal_kind(n, j, k) != "unp" and G(m, r) == 1:
                        return {"ok": False, "kind": True, "k": k, "m": m, "r": r}
        if k >= 2:
            u2 = 1 << (k - 2)
            for l in {0, 1, u2, 4 * u2 - 1}:
                if l < 0 or l >= 4 * u2:
                    continue
                u = 1 << k
                g2 = G(l, 5 * u2)
                if G(4 * l + 1, 5 * u) != g2:
                    return {"ok": False, "g1": True, "k": k, "l": l}
                if G(4 * l + 3, 5 * u) != g2:
                    return {"ok": False, "g3": True, "k": k, "l": l}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_edge_n(12) == 5461
        and want_even(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
        and PAT0011 in AND_ONES
        and and_clause(1, 1, 1, 0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def oddj_fold() -> dict:
    """k=1..8: odd-j pal-pairs equal parent pal-pairs with jp<=5U-1."""
    n_ok = 0
    rows = {}
    for k in range(1, K_FOLD + 1):
        u = 1 << (k - 1)
        clip = 5 * u
        n_strict = n_edge = 0
        for m in range(0, 4 * u):
            hi = min(2 * m, clip)
            for r in range(0, m):
                if G(m, r) == 0:
                    continue
                jp = 2 * m - r
                if jp > clip:
                    continue
                n = 2 * m + 1
                j = 2 * r + 1
                if jp == clip:
                    n_edge += 1
                    if pal_kind(n, j, k) != "unp":
                        return {"ok": False, "unp": True, "k": k, "m": m, "r": r}
                    continue
                n_strict += 1
                if G(n, j) != 1:
                    return {"ok": False, "g": True, "k": k, "m": m, "r": r}
                if pal_kind(n, j, k) != "pair":
                    return {"ok": False, "kind": True, "k": k, "m": m, "r": r}
                if (n - j) != 2 * (m - r):
                    return {"ok": False, "d": True, "k": k}
                if odd_child_t(m, k) != covering_t(k, n):
                    return {"ok": False, "t": True, "k": k}
        oddj = 0
        up = 1 << k
        clipc = 5 * up
        for n in range(1, 4 * up, 2):
            for j in range(1, n, 2):
                jp = 2 * n - j
                if jp > clipc or G(n, j) == 0:
                    continue
                oddj += 1
        if oddj != n_strict:
            return {
                "ok": False,
                "count": True,
                "k": k,
                "oddj": oddj,
                "n_strict": n_strict,
            }
        parent = pal_split(k - 1, None)
        if n_strict + n_edge != parent["n_pair"]:
            return {"ok": False, "sum": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "oddj": oddj,
            "n_strict": n_strict,
            "n_edge": n_edge,
            "parent_pair": parent["n_pair"],
        }
    ok = (
        n_ok == K_FOLD
        and rows["1"]["oddj"] == 2
        and rows["1"]["n_edge"] == 1
        and rows["7"]["oddj"] == 4365
        and rows["7"]["n_edge"] == 85
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FOLD, "rows": rows}


def edge_walk() -> dict:
    """k<=12: clip-edge count is J_{k+2}; even=parent tot; odd n1=n3=E(k-2)."""
    n_ok = 0
    rows = {}
    prev = None
    prev2 = None
    for k in range(0, K_EDGE + 1):
        r = edge_count(k)
        if r["tot"] != want_edge_n(k):
            return {"ok": False, "J": True, "k": k, "got": r["tot"]}
        if k >= 1 and r["even"] != prev:
            return {"ok": False, "even": True, "k": k}
        if k >= 2 and (
            r["odd"] != 2 * prev2 or r["n1"] != prev2 or r["n3"] != prev2
        ):
            return {"ok": False, "odd": True, "k": k, "r": r, "prev2": prev2}
        n_ok += 1
        rows[str(k)] = r
        prev2 = prev
        prev = r["tot"]
    ok = (
        n_ok == K_EDGE + 1
        and rows["0"]["tot"] == 1
        and rows["1"]["tot"] == 3
        and rows["12"]["tot"] == 5461
        and rows["12"]["even"] == 2731
        and rows["12"]["n1"] == 1365
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_EDGE, "rows": rows}


def killed_eq() -> dict:
    """odd pal-pairs 2-fold all parent pal-pairs; pal_c_e period 8."""
    ok = (
        pal_split(1, None)["n_pair"] == 12
        and pal_split(1, 1)["n_pair"] == 9
        and want_edge_n(0) == 1
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    ta = json.loads(TA_JSON.read_text())
    sz = json.loads(SZ_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    ok = (
        ta["checks"]["all_ok"]
        and sz["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and ta["verdict"]["even_pair_d_doubles"] == "LEMMA"
        and sz["verdict"]["odd_child_s_doubles_parent_s"] == "LEMMA"
        and sz["verdict"]["covering_t_2fold"] == "LEMMA"
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and ta["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ta["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, fold, edge, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and fold["ok"] and edge["ok"] and kl["ok"]
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
    fold = oddj_fold()
    edge = edge_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, fold, edge, kl, sc, pref)
    dump = {
        "cycle": "TB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "oddj_fold": {k: fold[k] for k in fold if k != "ok"},
        "edge_walk": {k: edge[k] for k in edge if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "oddj_pairs_drop_clip_edge": True,
            "clip_edge_eq_jacobsthal": True,
            "odd_pairs_2fold_all_parent": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "oddj_pairs_drop_clip_edge": "LEMMA",
            "oddj_d_doubles": "LEMMA",
            "clip_edge_eq_jacobsthal": "LEMMA",
            "odd_pairs_2fold_all_parent": "KILLED",
            "even_pair_raw_eq_parent_raw": "KILLED",
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
        "edge k12",
        dump["edge_walk"]["rows"]["12"]["tot"],
        "oddj k7",
        dump["oddj_fold"]["rows"]["7"]["oddj"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
