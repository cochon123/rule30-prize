#!/usr/bin/env python3
"""Cycle QV: covering clipped G=1 on even n at k is the 2-fold of k-1.

Green even doubling is G(2m,2r)=G(m,r) and G(2m,odd)=0. Covering even
n=2m at child k (U'=2U) runs m through the parent covering window
n in {0,...,4U-1}. Clip matches: parent j<=5U iff child 2j<=5U'.
Packed column doubles (child p=2*parent p) and the covering even
snapshot time doubles the parent odd covering time. Packed AND is
not cellwise 2-fold (k=3: 31 of 110 parent G=1 cells mismatch).
Even-n rest xor parent rest tot equals that mismatch tot, so
even rest(k)=parent odd rest iff the mismatch tot equals parent
even rest; that is Cycle QU's all-k lift, not a packed identity.
Not rest=S xor T for all k. Do not walk leftover p catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_qv.py --certify
Dump: research/cycle_qv.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qo import _walk_cells

OUT = Path(__file__).resolve().with_suffix(".json")
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"

N_PAL = 64
M_SLOTS = 64
K_FOLD = 8
K_ALG = 64
Q = 10


def even_slots(m_hi: int) -> dict:
    """G(2m, 2r)=G(m,r) and G(2m, 2r+1)=0."""
    n_ok = 0
    for m in range(0, m_hi):
        n = 2 * m
        for r in range(0, 2 * m + 1):
            if G(n, 2 * r) != G(m, r):
                return {"ok": False, "even": True, "m": m, "r": r}
            if G(n, 2 * r + 1) != 0:
                return {"ok": False, "odd": True, "m": m, "r": r}
            n_ok += 1
    return {"ok": True, "m_hi": m_hi, "n_ok": n_ok}


def covering_geom() -> dict:
    """k>=1: clip, packed column, and covering even snapshot all 2-fold."""
    n_ok = 0
    rows = {}
    for k in range(1, K_ALG + 1):
        U = 1 << (k - 1)
        Up = 2 * U
        T = Q * U
        Tp = Q * Up
        t0 = 2 * U
        Qc = covering_Q(Q)
        if Tp != 2 * T or 5 * Up != 2 * (5 * U) or Qc != 4:
            return {"ok": False, "scale": True, "k": k}
        sample_m = (0, 1, U, 4 * U - 1)
        for m in sample_m:
            if m < 0 or m >= 4 * U:
                continue
            n = 2 * m
            if n >= 4 * Up or n % 2 != 0:
                return {"ok": False, "range": True, "k": k, "m": m}
            s_even = Tp - 2 * n - 2
            s_po = T - 2 * m - 1
            t = U * Qc - m - 1
            s_walk = t0 + 1 + 2 * t
            if odd_clock(t, U, Qc) != m:
                return {"ok": False, "clock": True, "k": k, "m": m}
            if s_even != 2 * s_po or s_walk != s_po:
                return {
                    "ok": False,
                    "time": True,
                    "k": k,
                    "m": m,
                    "s_even": s_even,
                    "s_po": s_po,
                    "s_walk": s_walk,
                }
            rs = {0, min(2 * m, 5 * U)}
            if 2 * m >= 1:
                rs.add(1)
            for r in rs:
                p = T - 2 * r
                pp = Tp - 4 * r
                if pp != 2 * p or ((r <= 5 * U) != (2 * r <= 5 * Up)):
                    return {"ok": False, "col": True, "k": k, "m": m, "r": r}
        n_ok += 1
        if k <= 4:
            rows[str(k)] = {"U": U, "Up": Up, "T": T, "Tp": Tp}
    ok = n_ok == K_ALG and rows["1"]["Tp"] == 20 and rows["1"]["T"] == 10
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def g1_fold() -> dict:
    """k=1..8: clipped even-n G=1 at k is the 2-fold of clipped G=1 at k-1."""
    n_ok = 0
    rows = {}
    want = {
        1: 11,
        2: 36,
        3: 110,
        4: 352,
        5: 1122,
        6: 3608,
        7: 11618,
        8: 37496,
    }
    for k in range(1, K_FOLD + 1):
        U = 1 << (k - 1)
        clip = 5 * U
        n_parent = n_pe = n_po = 0
        for m in range(0, 4 * U):
            hi = min(2 * m, clip)
            for r in range(0, hi + 1):
                if G(m, r) == 0:
                    continue
                n_parent += 1
                if m % 2 == 0:
                    n_pe += 1
                else:
                    n_po += 1
                if G(2 * m, 2 * r) != 1:
                    return {"ok": False, "image": True, "k": k, "m": m, "r": r}
        Up = 2 * U
        clipc = 5 * Up
        n_child = n0 = n2 = 0
        for n in range(0, 4 * Up, 2):
            hi = min(2 * n, clipc)
            for j in range(0, hi + 1):
                if G(n, j) == 0:
                    continue
                n_child += 1
                if j % 2 or G(n // 2, j // 2) != 1:
                    return {"ok": False, "pre": True, "k": k, "n": n, "j": j}
                if n % 4 == 0:
                    n0 += 1
                else:
                    n2 += 1
        if n_child != n_parent or n_child != want[k]:
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_child": n_child,
                "n_parent": n_parent,
            }
        if n0 != n_pe or n2 != n_po:
            return {
                "ok": False,
                "slice": True,
                "k": k,
                "n0": n0,
                "n_pe": n_pe,
                "n2": n2,
                "n_po": n_po,
            }
        n_ok += 1
        rows[str(k)] = {
            "n_child": n_child,
            "n_parent": n_parent,
            "n0": n0,
            "n2": n2,
            "n_pe": n_pe,
            "n_po": n_po,
        }
    ok = (
        n_ok == K_FOLD
        and rows["1"]["n_child"] == 11
        and rows["3"]["n_child"] == 110
        and rows["8"]["n_child"] == 37496
        and rows["3"]["n0"] == rows["2"]["n_child"]
        and rows["4"]["n0"] == rows["3"]["n_child"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FOLD, "rows": rows}


def cellwise_fold() -> dict:
    """k=3: packed AND at (2m,2r) is not parent AND at (m,r) on G=1."""
    child = _walk_cells(3)
    parent = _walk_cells(2)
    n_g1 = n_mis = n_child = n_parent = n_both = 0
    U = 4
    clip_p = 5 * U
    for m in range(0, 4 * U):
        hi = min(2 * m, clip_p)
        for r in range(0, hi + 1):
            if G(m, r) == 0:
                continue
            n_g1 += 1
            pc = child.get((2 * m, 2 * r), 0)
            pp = parent.get((m, r), 0)
            if pc and pp:
                n_both += 1
            elif pc != pp:
                n_mis += 1
                if pc:
                    n_child += 1
                else:
                    n_parent += 1
    ok = (
        n_g1 == 110
        and n_mis == 31
        and n_child == 19
        and n_parent == 12
        and n_both == 7
    )
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_mis": n_mis,
        "n_child_only": n_child,
        "n_parent_only": n_parent,
        "n_both": n_both,
    }


def qu_lift() -> dict:
    """Boolean: even rest = parent odd iff 2-fold mismatch tot = parent even."""
    n_ok = 0
    for e in (0, 1):
        for pe in (0, 1):
            for po in (0, 1):
                err = e ^ pe ^ po
                if (e == po) != (err == pe):
                    return {"ok": False, "e": e, "pe": pe, "po": po}
                n_ok += 1
    ok = n_ok == 8
    return {"ok": ok, "n_ok": n_ok}


def prefixes() -> dict:
    qu = json.loads(QU_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qu["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and qu["verdict"]["even_rest_eq_ST_k_minus_1"] == "KILLED"
        and qo["verdict"]["cellwise_4fold_and"] == "KILLED"
        and qu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, geom, fold, cell, lift, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"] and geom["ok"]
    assert fold["ok"] and cell["ok"] and lift["ok"] and sc["ok"] and pref["ok"]
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
    geom = covering_geom()
    fold = g1_fold()
    cell = cellwise_fold()
    lift = qu_lift()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, geom, fold, cell, lift, sc, pref)
    dump = {
        "cycle": "QV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "covering_geom": {k: geom[k] for k in geom if k != "ok"},
        "g1_fold": {k: fold[k] for k in fold if k != "ok"},
        "cellwise_fold": {k: cell[k] for k in cell if k != "ok"},
        "qu_lift": {k: lift[k] for k in lift if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "g1_2fold_covering_bijection": True,
            "covering_time_col_2fold": True,
            "cellwise_2fold_and": False,
            "even_rest_eq_ST_k_minus_1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "g1_2fold_covering_bijection": "LEMMA",
            "covering_time_col_2fold": "LEMMA",
            "cellwise_2fold_and": "KILLED",
            "even_rest_eq_ST_k_minus_1": "KILLED",
            "even_rest_eq_parent_odd_k_le_10": "CERTIFIED",
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
        "g1_fold n_ok",
        dump["g1_fold"]["n_ok"],
        "k8",
        dump["g1_fold"]["rows"]["8"]["n_child"],
        "fold_mis",
        dump["cellwise_fold"]["n_mis"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
