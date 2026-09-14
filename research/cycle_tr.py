#!/usr/bin/env python3
"""Cycle TR: {d=1,d=2} count is J_{k+3}; complex rest tot is raw xor 1_{k<=1}.

The TG complex of pal-distances 1 and 2 has count
J_{k+2}+2 J_{k+1}=J_{k+3}. Forced corr of the complex is 1_{k<=1}
(Cycle TP on d=1, Cycle TQ on d=2), so complex rest tot equals
complex raw tot xor 1_{k<=1}. d=2 raw tot does not 2-fold parent
d=1 raw tot (dies at k=9). Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tr.py --certify
Dump: research/cycle_tr.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_su import covering_and_spat
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_tb import jacobsthal
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tl import d1_v2, d2_v2
from cycle_tp import want_d1_corr
from cycle_tq import want_even_d2_forced, want_odd_d2_forced
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TQ_JSON = Path(__file__).resolve().parent / "cycle_tq.json"
TP_JSON = Path(__file__).resolve().parent / "cycle_tp.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_SPAT = 10
Q = 10
PAT0011 = (0, 0, 1, 1)


def want_complex_n(k: int) -> int:
    """{d=1,d=2} pal-pair count: J_{k+3}."""
    return jacobsthal(k + 3)


def want_complex_corr(k: int) -> int:
    """Forced corr of the TG complex: 1 iff k<=1."""
    return want_d1_corr(k)


def tot_form() -> dict:
    """k<=64: J_{k+3}=J_{k+2}+2 J_{k+1}; complex corr is 1_{k<=1}."""
    n_ok = 0
    if jacobsthal(0) != 0 or jacobsthal(1) != 1 or jacobsthal(3) != 3:
        return {"ok": False, "J0": True}
    if want_complex_n(0) != 3 or want_d1_n(0) + want_d2_n(0) != 3:
        return {"ok": False, "base": True}
    if want_complex_corr(0) != 1 or want_complex_corr(2) != 0:
        return {"ok": False, "corr0": True}
    for k in range(0, K_ALG + 1):
        j1 = jacobsthal(k + 1)
        j2 = jacobsthal(k + 2)
        j3 = jacobsthal(k + 3)
        if j3 != (1 << (k + 1)) + j1:
            return {"ok": False, "Jsum": True, "k": k}
        if j3 != j2 + 2 * j1:
            return {"ok": False, "Jrec": True, "k": k}
        if want_complex_n(k) != j3:
            return {"ok": False, "cn": True, "k": k}
        if want_d1_n(k) + want_d2_n(k) != want_complex_n(k):
            return {"ok": False, "sum": True, "k": k}
        if want_complex_corr(k) != int(k <= 1):
            return {"ok": False, "corr": True, "k": k}
        if want_complex_corr(k) != want_d1_corr(k):
            return {"ok": False, "tp": True, "k": k}
        if want_even_d2_forced(k) or (
            k != 2 and want_odd_d2_forced(k)
        ):
            return {"ok": False, "tq": True, "k": k}
        if k == 2 and len(want_odd_d2_forced(k)) != 3:
            return {"ok": False, "tq2": True}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_complex_n(7) == 341
        and want_complex_n(12) == 10923
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def complex_count() -> dict:
    """k<=12: covering {d=1,d=2} count is J_{k+3}."""
    n_ok = 0
    n_cell = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        n_d1 = n_d2 = 0
        for n in range(0, 4 * u):
            if n >= 1 and d1_v2(n):
                n_d1 += 1
            if n >= 2 and d2_v2(n):
                n_d2 += 1
        if n_d1 != want_d1_n(k) or n_d2 != want_d2_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_d1": n_d1,
                "n_d2": n_d2,
            }
        if n_d1 + n_d2 != want_complex_n(k):
            return {"ok": False, "sum": True, "k": k}
        n_cell += n_d1 + n_d2
        n_ok += 1
        rows[str(k)] = {"n_d1": n_d1, "n_d2": n_d2, "n_cx": n_d1 + n_d2}
    ok = (
        n_ok == K_COUNT + 1
        and n_cell == sum(want_complex_n(k) for k in range(0, K_COUNT + 1))
        and rows["0"]["n_cx"] == 3
        and rows["7"]["n_cx"] == 341
        and rows["12"]["n_cx"] == 10923
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_cell": n_cell,
        "k_hi": K_COUNT,
        "rows": rows,
    }


def spat_fold() -> dict:
    """k<=10: d=2 raw tot is not parent d=1 tot, nor that xor 1_{k even}."""
    t_hi = Q * (1 << K_SPAT)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)

    def raw(k: int, n: int, d: int) -> int:
        t = covering_t(k, n)
        s = even_s(n, k)
        return covering_and_spat(packed[t], s, d) ^ covering_and_spat(
            packed[t], s, -d
        )

    n_ok = 0
    rows = {}
    d1_tot = []
    d2_tot = []
    for k in range(0, K_SPAT + 1):
        u = 1 << k
        t1 = t2 = 0
        for n in range(0, 4 * u):
            if n >= 1 and d1_v2(n):
                t1 ^= raw(k, n, 1)
            if n >= 2 and d2_v2(n):
                t2 ^= raw(k, n, 2)
        d1_tot.append(t1)
        d2_tot.append(t2)
        rec = {"d1": t1, "d2": t2}
        if k >= 1:
            rec["parent_d1"] = d1_tot[k - 1]
            rec["xor_even"] = d1_tot[k - 1] ^ int(k % 2 == 0)
            rec["eq_parent"] = int(t2 == d1_tot[k - 1])
            rec["eq_xor_even"] = int(t2 == rec["xor_even"])
        n_ok += 1
        rows[str(k)] = rec
    held = all(rows[str(k)]["eq_xor_even"] for k in range(1, 9))
    die_p = rows["2"]["eq_parent"] == 0 and rows["9"]["eq_parent"] == 0
    die_x = rows["9"]["eq_xor_even"] == 0 and rows["10"]["eq_xor_even"] == 0
    ok = (
        n_ok == K_SPAT + 1
        and held
        and die_p
        and die_x
        and rows["0"]["d2"] == 1
        and rows["3"]["d1"] == 1
        and rows["9"]["d2"] == 1
        and rows["10"]["d1"] == 1
        and want_rest_e0(1) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_SPAT,
        "rows": rows,
        "fold_parent": False,
        "fold_xor_even": False,
    }


def killed_eq() -> dict:
    """d=2 raw tot 2-folds parent d=1; d=1 never forced all k."""
    ok = (
        want_complex_n(0) == 3
        and want_complex_corr(0) == 1
        and want_complex_corr(9) == 0
        and want_d1_corr(1) == 1
        and not want_even_d2_forced(9)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tq = json.loads(TQ_JSON.read_text())
    tp = json.loads(TP_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    ok = (
        tq["checks"]["all_ok"]
        and tp["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and tq["verdict"]["d2_rest_eq_raw_tot_all_k"] == "LEMMA"
        and tp["verdict"]["d1_rest_eq_raw_xor_k_le_1"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and tq["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tq["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
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
    cnt = complex_count()
    spat = spat_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, spat, kl, sc, pref)
    dump = {
        "cycle": "TR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "complex_count": {k: cnt[k] for k in cnt if k != "ok"},
        "spat_fold": {k: spat[k] for k in spat if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "complex_count_eq_J_k3": True,
            "complex_rest_eq_raw_xor_k_le_1": True,
            "complex_rest_eq_raw_k_ge_2": True,
            "d2_raw_eq_parent_d1": False,
            "d2_raw_eq_parent_xor_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "complex_count_eq_J_k3": "LEMMA",
            "complex_rest_eq_raw_xor_k_le_1": "LEMMA",
            "complex_rest_eq_raw_k_ge_2": "LEMMA",
            "d2_raw_eq_parent_d1": "KILLED",
            "d2_raw_eq_parent_xor_even": "KILLED",
            "d1_never_forced_all_k": "KILLED",
            "d1_rest_eq_raw_all_k": "KILLED",
            "d2_rest_eq_raw_cellwise": "KILLED",
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
        "cx k12",
        dump["complex_count"]["rows"]["12"]["n_cx"],
        "fold9",
        dump["spat_fold"]["rows"]["9"]["eq_xor_even"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
