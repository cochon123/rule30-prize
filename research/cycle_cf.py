#!/usr/bin/env python3
"""Cycle CF: ident-1 at p>=2 iff ident-0 at p-2; both implications not orbit-free.

Packed update at an identically-1 bit is 1 = lambda_{p-2} xor 1, so
ident-1 at p>=2 forces ident-0 at p-2. Twin gives the converse.
Consecutive ident-1 at p>=2 would force ident-0 at p+2 and then
ident-0 at p, a contradiction; the only consecutive ident-1 pair is
bits 0 and 1. Both implications with c not 0, and identically AND
with c not 0, occur on consistent length-4 windows (killed as
orbit-free). After the scar, both hold together only at c==0 (prefix).
Not a prize claim.

Run: python3 research/cycle_cf.py --certify
Dump: research/cycle_cf.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import (
    KNOWN20,
    packed_center_bits,
    prize_cycle,
    reconstruct,
    xorcat,
)
from cycle_cb import ext
from cycle_ce import implies, odd_lift

OUT = Path(__file__).resolve().with_suffix(".json")


def ident1_implies_ident0_pointwise() -> bool:
    """If bit p is 1 at t and t+1, then bit p-2 is 0 at t."""
    for lp in (1,):
        for lpm1 in (0, 1):
            for lpm2 in (0, 1):
                nxt = lpm2 ^ (lpm1 | lp)
                if lp == 1 and nxt == 1:
                    if lpm2 != 0:
                        return False
                if nxt == 1:
                    # 1 = lpm2 xor (lpm1 or lp); if lp=1 then 1=lpm2 xor 1 so lpm2=0
                    if lp == 1 and lpm2 != 0:
                        return False
    # all-1s update
    if 1 ^ (1 | 1) != 0:
        return False
    return True


def settled_twin_iff(kmax: int = 12) -> dict:
    rows = []
    all_ok = True
    cons_hi = []
    for k in range(3, kmax + 1):
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seq = [[(w >> p) & 1 for w in cyc] for p in range(W + 1)]
        z = {p for p in range(W + 1) if all(x == 0 for x in seq[p])}
        o = {p for p in range(W + 1) if all(x == 1 for x in seq[p])}
        for p in o:
            if p >= 2 and (p - 2) not in z:
                all_ok = False
        for p in z:
            if p + 2 <= W and (p + 2) not in o:
                all_ok = False
        cons = [p for p in o if p + 1 in o]
        if cons != [0]:
            all_ok = False
            cons_hi.append({"k": k, "cons": cons})
        rows.append({"k": k, "ok": all_ok})
    return {"ok": all_ok and not cons_hi, "n": len(rows), "cons_hi": cons_hi}


def abstract_windows() -> dict:
    """Length-4 consistent 5-windows: both implications / AND with c != 0."""
    L = 4
    n_ok = 0
    n_both_nz = 0
    n_and_nz = 0
    n_both_z = 0
    for flat in itertools.product((0, 1), repeat=20):
        e = list(flat[0:4])
        d = list(flat[4:8])
        c = list(flat[8:12])
        a = list(flat[12:16])
        b = list(flat[16:20])
        good = True
        for t in range(L):
            nt = (t + 1) % L
            if b[nt] != c[t] ^ (a[t] | b[t]):
                good = False
                break
            if a[nt] != d[t] ^ (c[t] | a[t]):
                good = False
                break
            if c[nt] != e[t] ^ (d[t] | c[t]):
                good = False
                break
        if not good:
            continue
        n_ok += 1
        ia, ib = implies(c, a), implies(c, b)
        if ia and ib:
            if any(c):
                n_both_nz += 1
                if c == [x & y for x, y in zip(a, b)]:
                    n_and_nz += 1
            else:
                n_both_z += 1
    return {
        "n_ok": n_ok,
        "n_both_nz": n_both_nz,
        "n_and_nz": n_and_nz,
        "n_both_z": n_both_z,
        "ok": n_both_nz > 0 and n_and_nz > 0,
    }


def self_checks(c20, pt: bool, twin: dict, absv: dict, ham4: dict, ham8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pt and twin["ok"] and absv["ok"]
    assert ham4["both"] == [31] and ham8["both"] == [402]
    assert not ham4["ands"] and not ham8["ands"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pt = ident1_implies_ident0_pointwise()
    twin = settled_twin_iff()
    absv = abstract_windows()
    ham4 = odd_lift(4)
    ham8 = odd_lift(8)
    checks = self_checks(c20, pt, twin, absv, ham4, ham8)
    dump = {
        "cycle": "CF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "twin": {"n": twin["n"]},
        "abstract": {k: absv[k] for k in ("n_ok", "n_both_nz", "n_and_nz", "n_both_z")},
        "ham4_both": ham4["both"],
        "ham8_both": ham8["both"],
        "lemmas": {
            "ident1_iff_ident0_shift2": True,
            "consecutive_ident1_only_01": True,
            "both_implies_c_eq_0_orbit_free": False,
            "AND_implies_c_eq_0_orbit_free": False,
            "both_implications_only_c_eq_0_all_k": None,
            "no_AND_triple_after_scar_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "ident1_iff_ident0_shift2": "LEMMA",
            "consecutive_ident1_only_01": "LEMMA",
            "both_implies_c_eq_0_orbit_free": "KILLED",
            "AND_implies_c_eq_0_orbit_free": "KILLED",
            "both_implications_only_c_eq_0_all_k": "PREFIX",
            "no_AND_triple_after_scar_all_k": "PREFIX",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("abstract", dump["abstract"])
    print("both", dump["ham4_both"], dump["ham8_both"])


if __name__ == "__main__":
    main()
