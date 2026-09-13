#!/usr/bin/env python3
"""Cycle QO: covering packed rest xor on n%4==0 equals ST at k-2 dies at k=10.

G(4t,4r)=G(t,r) maps covering n%4==0 onto the parent window at k-2,
and for k>=3 Green rest on n%4==0 is A(k-2)=0. Packed AND is not
cellwise 4-fold: at k=3 already 14 G=1 mismatches. Packed rest xor
on n%4==0 equals S xor T at k-2 (equivalently parent rest tot) on
3<=k<=9 and dies at k=10 (got 0, ST(8)=1). Leftover packed n%4==0
equals that bit xor unique packed n%4==0, so leftover n0 equals
ST(k-2) xor 1 for k>=6 also dies at k=10. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qo.py --certify
Dump: research/cycle_qo.json
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
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qn import want_unique_pack_n0
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QN_JSON = Path(__file__).resolve().parent / "cycle_qn.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10


def want_st_n0(k: int) -> int:
    """S xor T at k-2; rest n%4==0 equals this on 3<=k<=9, not k=10."""
    if k < 2:
        return 0
    return want_rest_e0(k - 2)


def _walk_rest_nmod(k: int) -> dict:
    """Covering q=10 packed rest xor split by n%4, plus unique/leftover n0."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    tot = [0, 0, 0, 0]
    u_n0 = lo_n0 = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                if not packed or p in FORCED:
                    continue
                tot[n % 4] ^= 1
                if n % 4 == 0:
                    if p in UNIQUE_REST:
                        u_n0 ^= 1
                    else:
                        lo_n0 ^= 1
        row = rule30_step(row)
        s += 1
    rest = tot[0] ^ tot[1] ^ tot[2] ^ tot[3]
    return {
        "tot": tot,
        "rest": rest,
        "n0": tot[0],
        "u_n0": u_n0,
        "lo_n0": lo_n0,
    }


def _walk_cells(k: int) -> dict:
    """Covering packed rest cells keyed by (n, j)."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    cells = {}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                if not packed or p in FORCED:
                    continue
                cells[(n, j)] = 1
        row = rule30_step(row)
        s += 1
    return cells


def rest_n0_walk() -> dict:
    """k<=10: rest tot=ST; n0=ST(k-2) on 3..9; dies at k=10."""
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        w = _walk_rest_nmod(k)
        if w["rest"] != want_rest10(k, 10) or w["rest"] != want_rest_e0(k):
            return {"ok": False, "rest": True, "k": k, "w": w}
        if (w["n0"] ^ w["u_n0"] ^ w["lo_n0"]) != 0:
            return {"ok": False, "split": True, "k": k, "w": w}
        if k >= 6 and w["u_n0"] != want_unique_pack_n0(k):
            return {"ok": False, "u": True, "k": k, "u": w["u_n0"]}
        if 3 <= k <= 9 and w["n0"] != want_st_n0(k):
            return {"ok": False, "prefix": True, "k": k, "n0": w["n0"]}
        if k == 10 and w["n0"] == want_st_n0(k):
            return {"ok": False, "alive": True, "k": k, "n0": w["n0"]}
        rows[str(k)] = {
            "tot": w["tot"],
            "rest": w["rest"],
            "n0": w["n0"],
            "st_n0": want_st_n0(k),
            "u_n0": w["u_n0"],
            "lo_n0": w["lo_n0"],
        }
        n_ok += 1
    ok = (
        rows["4"]["n0"] == 1
        and rows["4"]["st_n0"] == 1
        and rows["8"]["n0"] == 1
        and rows["8"]["st_n0"] == 1
        and rows["9"]["n0"] == 0
        and rows["9"]["st_n0"] == 0
        and rows["10"]["n0"] == 0
        and rows["10"]["st_n0"] == 1
        and rows["10"]["rest"] == 0
        and rows["10"]["u_n0"] == 1
        and rows["10"]["lo_n0"] == 1
        and rows["10"]["tot"] == [0, 1, 0, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def cellwise_fold() -> dict:
    """k=3: packed AND at (4t,4r) is not parent AND at (t,r) on G=1."""
    child = _walk_cells(3)
    parent = _walk_cells(1)
    n_g1 = n_mis = n_child = n_parent = 0
    U = 8
    clip_p = 5 << 1
    for t in range(0, U):
        hi = min(2 * t, clip_p)
        for r in range(0, hi + 1):
            if G(t, r) == 0:
                continue
            n_g1 += 1
            pc = child.get((4 * t, 4 * r), 0)
            pp = parent.get((t, r), 0)
            if pc != pp:
                n_mis += 1
                if pc and not pp:
                    n_child += 1
                else:
                    n_parent += 1
    ok = n_g1 == 36 and n_mis == 14 and n_child == 9 and n_parent == 5
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_mis": n_mis,
        "n_child_only": n_child,
        "n_parent_only": n_parent,
    }


def killed_n0_eq_st() -> dict:
    """rest n%4==0 tot equals ST at k-2 / leftover n0 equals ST(k-2) xor 1."""
    ok = (
        want_st_n0(10) == 1
        and want_rest_e0(8) == 1
        and want_rest10(8, 10) == 1
        and want_rest_e0(10) == 0
        and want_unique_pack_n0(10) == 1
        and want_st_n0(8) == 1
        and want_st_n0(9) == 0
        and want_st_n0(4) == 1
    )
    return {"ok": ok, "st10": 1, "ST8": 1, "ST10": 0}


def prefixes() -> dict:
    qn = json.loads(QN_JSON.read_text())
    ok = (
        qn["checks"]["all_ok"]
        and qn["verdict"]["p16_n0_iff_k_ge_3"] == "LEMMA"
        and qn["verdict"]["unique_pack_n0_k_ge_6"] == "LEMMA"
        and qn["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qn["verdict"]["prize"] == "unsolved"
        and want_unique_pack_n0(6) == 1
        and want_rest_e0(8) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, walk, fold, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and walk["ok"] and fold["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    walk = rest_n0_walk()
    fold = cellwise_fold()
    kl = killed_n0_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, walk, fold, kl, sc, pref)
    dump = {
        "cycle": "QO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "rest_n0_walk": {k: walk[k] for k in walk if k != "ok"},
        "cellwise_fold": {k: fold[k] for k in fold if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "rest_n0_eq_ST_k_minus_2": False,
            "cellwise_4fold_and": False,
            "lo_n0_eq_ST_xor_1_k_ge_6": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "rest_n0_eq_ST_k_minus_2": "KILLED",
            "cellwise_4fold_and": "KILLED",
            "lo_n0_eq_ST_xor_1_k_ge_6": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
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
        "rest_n0_walk n_ok",
        dump["rest_n0_walk"]["n_ok"],
        "k10_n0",
        dump["rest_n0_walk"]["rows"]["10"]["n0"],
        "k10_st",
        dump["rest_n0_walk"]["rows"]["10"]["st_n0"],
        "fold_mis",
        dump["cellwise_fold"]["n_mis"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
