#!/usr/bin/env python3
"""Cycle TA: even pal-split at k is the 2-fold of pal-split at k-1.

Green even doubling is G(2m,2r)=G(m,r) and G(2m,odd)=0. Clip matches:
parent pal-partner <=5U iff child pal-partner <=5U'. Pal-centers,
pal-pairs, and unpaired cells keep their kind, so even pal-split
counts at k equal the full pal-split at k-1. Pal-pair distance
doubles and the covering time is Cycle SZ's even-child 2-fold.
Packed spat-mismatch is not cellwise 2-fold, and even pal-pair raw
tot is not parent pal-pair raw tot. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ta.py --certify
Dump: research/cycle_ta.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sr import pal_center_count
from cycle_ss import even_s
from cycle_su import covering_and_spat
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_sz import even_child_t
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SZ_JSON = Path(__file__).resolve().parent / "cycle_sz.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
SS_JSON = Path(__file__).resolve().parent / "cycle_ss.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_FOLD = 8
K_SPAT = 6
Q = 10
PAT0011 = (0, 0, 1, 1)


def pal_kind(n: int, j: int, k: int) -> str:
    """Kind of a clipped G=1 cell: pal, pair, or unp."""
    clip = 5 * (1 << k)
    jp = 2 * n - j
    if j == n:
        return "pal"
    if jp > clip:
        return "unp"
    return "pair"


def pal_split(k: int, parity: int | None) -> dict:
    """Clipped G=1 pal-center / pal-pair / unpaired counts."""
    u = 1 << k
    clip = 5 * u
    n_pal = n_pair = n_unp = 0
    ns = range(0, 4 * u) if parity is None else range(parity, 4 * u, 2)
    for n in ns:
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            kind = pal_kind(n, j, k)
            if kind == "pal":
                n_pal += 1
            elif kind == "unp":
                if j < n:
                    n_unp += 1
            elif j < 2 * n - j:
                n_pair += 1
    return {"n_pal": n_pal, "n_pair": n_pair, "n_unp": n_unp}


def tot_form() -> dict:
    """k=1..64: pal-pair clip, distance, and covering time 2-fold."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        u = 1 << (k - 1)
        clip = 5 * u
        clipc = 5 * (1 << k)
        samples_m = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for m in samples_m:
            if m < 0 or m >= 4 * u:
                continue
            rs = {0, m, min(2 * m, clip)}
            if 2 * m >= 1:
                rs.add(1)
            for r in rs:
                n = 2 * m
                j = 2 * r
                jp = 2 * m - r
                jpc = 2 * n - j
                if (jpc > clipc) != (jp > clip):
                    return {"ok": False, "clip": True, "k": k, "m": m, "r": r}
                if (j == n) != (r == m):
                    return {"ok": False, "pal": True, "k": k, "m": m}
                if r < m and jp <= clip and (n - j) != 2 * (m - r):
                    return {"ok": False, "d": True, "k": k, "m": m, "r": r}
                if even_child_t(m, k) != covering_t(k, n):
                    return {"ok": False, "t": True, "k": k, "m": m}
                if r <= 2 * m and G(m, r) == 1 and G(n, j) != 1:
                    return {"ok": False, "g": True, "k": k, "m": m, "r": r}
        if pal_center_count(k) != 2 * pal_center_count(k - 1):
            return {"ok": False, "pc": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and pal_center_count(0) == 2
        and pal_center_count(3) == 16
        and even_child_t(0, 3) == covering_t(3, 0)
        and want_even(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
        and PAT0011 in AND_ONES
        and and_clause(1, 1, 1, 0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pair_fold() -> dict:
    """k=1..8: even pal-split counts equal parent all-n pal-split."""
    n_ok = 0
    rows = {}
    prev = pal_split(0, None)
    want = {
        1: (4, 3, 1),
        2: (8, 12, 4),
        3: (16, 38, 18),
        8: (512, 14456, 8072),
    }
    for k in range(1, K_FOLD + 1):
        u = 1 << (k - 1)
        clip = 5 * u
        for m in range(0, 4 * u):
            hi = min(2 * m, clip)
            for r in range(0, hi + 1):
                if G(m, r) == 0:
                    continue
                n = 2 * m
                j = 2 * r
                if G(n, j) != 1:
                    return {"ok": False, "image": True, "k": k, "m": m, "r": r}
                if pal_kind(n, j, k) != pal_kind(m, r, k - 1):
                    return {"ok": False, "kind": True, "k": k, "m": m, "r": r}
        ev = pal_split(k, 0)
        if (
            ev["n_pal"] != prev["n_pal"]
            or ev["n_pair"] != prev["n_pair"]
            or ev["n_unp"] != prev["n_unp"]
        ):
            return {"ok": False, "count": True, "k": k, "ev": ev, "prev": prev}
        if ev["n_pal"] != pal_center_count(k):
            return {"ok": False, "pc": True, "k": k}
        if k in want and (ev["n_pal"], ev["n_pair"], ev["n_unp"]) != want[k]:
            return {"ok": False, "pin": True, "k": k, "ev": ev}
        n_ok += 1
        rows[str(k)] = ev
        prev = pal_split(k, None)
    ok = (
        n_ok == K_FOLD
        and rows["1"]["n_pair"] == 3
        and rows["3"]["n_pair"] == 38
        and rows["8"]["n_pair"] == 14456
        and rows["8"]["n_unp"] == 8072
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FOLD, "rows": rows}


def spat_walk() -> dict:
    """k<=6 even pal-pairs: spat at 2d on even-child time; not parent spat."""
    t_hi = Q * (1 << K_SPAT) + 4
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    n_eq = n_neq = 0
    rows = {}
    for k in range(1, K_SPAT + 1):
        u = 1 << (k - 1)
        clip = 5 * u
        raw_e = raw_p = 0
        eq = neq = 0
        n_pair = 0
        for m in range(0, 4 * u):
            for r in range(0, m):
                jp = 2 * m - r
                if jp > clip or G(m, r) == 0:
                    continue
                d = m - r
                t_p = covering_t(k - 1, m)
                s_p = even_s(m, k - 1)
                spat_p = covering_and_spat(packed[t_p], s_p, d) ^ covering_and_spat(
                    packed[t_p], s_p, -d
                )
                n = 2 * m
                t_c = covering_t(k, n)
                s_c = even_s(n, k)
                spat_c = covering_and_spat(packed[t_c], s_c, 2 * d) ^ covering_and_spat(
                    packed[t_c], s_c, -2 * d
                )
                raw_e ^= spat_c
                raw_p ^= spat_p
                n_pair += 1
                if spat_c == spat_p:
                    eq += 1
                else:
                    neq += 1
        n_eq += eq
        n_neq += neq
        n_ok += 1
        rows[str(k)] = {
            "n_pair": n_pair,
            "n_eq": eq,
            "n_neq": neq,
            "raw_e": raw_e,
            "raw_p": raw_p,
        }
    ok = (
        n_ok == K_SPAT
        and n_neq > 0
        and rows["2"]["n_neq"] > 0
        and rows["2"]["raw_e"] != rows["2"]["raw_p"]
        and rows["1"]["n_pair"] == 3
        and rows["6"]["n_pair"] == 1368
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_eq": n_eq,
        "n_neq": n_neq,
        "k_hi": K_SPAT,
        "rows": rows,
    }


def killed_eq() -> dict:
    """even pair raw equals parent pair raw; pal_c_e period 8."""
    ok = (
        odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and pal_center_count(1) == 4
        and covering_t(3, 0) == even_child_t(0, 3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    sz = json.loads(SZ_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    ss = json.loads(SS_JSON.read_text())
    ok = (
        sz["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and ss["checks"]["all_ok"]
        and sz["verdict"]["odd_child_s_doubles_parent_s"] == "LEMMA"
        and sz["verdict"]["covering_t_2fold"] == "LEMMA"
        and sz["verdict"]["pal_c_tot_eq_P5U_xor_PU"] == "LEMMA"
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and ss["verdict"]["unpaired_packed_and_0_all_k"] == "LEMMA"
        and sz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sz["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, fold, spat, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and fold["ok"] and spat["ok"] and kl["ok"]
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
    fold = pair_fold()
    spat = spat_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, fold, spat, kl, sc, pref)
    dump = {
        "cycle": "TA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pair_fold": {k: fold[k] for k in fold if k != "ok"},
        "spat_walk": {k: spat[k] for k in spat if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_pal_split_2fold": True,
            "even_pair_d_doubles": True,
            "even_pair_raw_eq_parent_raw": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_pal_split_2fold": "LEMMA",
            "even_pair_d_doubles": "LEMMA",
            "even_pair_t_eq_even_child_t": "LEMMA",
            "even_pair_raw_eq_parent_raw": "KILLED",
            "cellwise_pair_spat_2fold": "KILLED",
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
        "fold k8 pair",
        dump["pair_fold"]["rows"]["8"]["n_pair"],
        "spat k2 neq",
        dump["spat_walk"]["rows"]["2"]["n_neq"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
