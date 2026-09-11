#!/usr/bin/env python3
"""Cycle CE: d=Da iff c implies a; c implies b forbids consecutive 11s in c.

Packed update a' = d xor (c or a) makes d = a xor a' iff a = c or a iff
c implies a, pointwise. Identically AND therefore requires c implies a
(hence d=Da) and c implies b. If c_t = b_t = 1 then b' = 0, so c implies b
at the next time forces c_{t+1}=0: no consecutive 11s in c. Both
implications hold together only at the ident-0/ident-1 scar triple on
the k=4 and k=8 odd lifts, where 011 kills AND (prefix). Not a prize
claim.

Run: python3 research/cycle_ce.py --certify
Dump: research/cycle_ce.json
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
from cycle_ca import (
    KNOWN20,
    deriv,
    packed_center_bits,
    prize_cycle,
    reconstruct,
    xorcat,
)
from cycle_cb import ext

OUT = Path(__file__).resolve().with_suffix(".json")


def implies(xs: list[int], ys: list[int]) -> bool:
    return all((not xs[t]) or ys[t] for t in range(len(xs)))


def has11(xs: list[int]) -> bool:
    n = len(xs)
    return any(xs[t] == 1 and xs[(t + 1) % n] == 1 for t in range(n))


def da_iff_c_le_a() -> bool:
    """Pointwise: d == a xor a' iff c implies a, with a' = d xor (c or a)."""
    for d in (0, 1):
        for c in (0, 1):
            for a in (0, 1):
                ap = d ^ (c | a)
                left = d == (a ^ ap)
                right = (not c) or a
                if left != right:
                    return False
    return True


def c_le_b_kills_11() -> bool:
    """If c=b=1 then b'=0, so a next c=1 would violate c implies b."""
    for a in (0, 1):
        c, b = 1, 1
        bp = c ^ (a | b)
        if bp != 0:
            return False
    return True


def odd_lift(k: int) -> dict:
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
    p = W + 1
    while p <= 2 * W:
        a = ext(seqs[p - 2], cur_pi)
        b = ext(seqs[p - 1], cur_pi)
        if all(x == 0 for x in b):
            sm = xorcat(a)
            u = [0] * cur_pi
            for t in range(cur_pi - 1):
                u[t + 1] = a[t] ^ u[t]
            if sm == 1:
                if odd_p is None:
                    odd_p = p
                u = u + [x ^ 1 for x in u]
                cur_pi *= 2
            seqs[p] = u
        else:
            seqs[p] = reconstruct(a, b)
        p += 1
    L = cur_pi
    cia, cib, both, ands, no11, mismatch = [], [], [], [], [], 0
    q = odd_p
    while q <= 2 * W:
        c = ext(seqs[q - 3], L)
        a = ext(seqs[q - 2], L)
        b = ext(seqs[q - 1], L)
        d = ext(seqs[q - 4], L)
        imp_a = implies(c, a)
        imp_b = implies(c, b)
        da = d == deriv(a)
        if imp_a != da:
            mismatch += 1
        if imp_a:
            cia.append(q)
        if imp_b:
            cib.append(q)
        if imp_a and imp_b:
            both.append(q)
        if c == [x & y for x, y in zip(a, b)]:
            ands.append(q)
        if not has11(c):
            no11.append(q)
        if imp_b and has11(c):
            mismatch += 1
        q += 1
    c0 = all(x == 0 for x in ext(seqs[odd_p + 2 - 3], L))  # q = odd_p+2 should be ident-0 as c
    return {
        "k": k,
        "odd_p": odd_p,
        "n": 2 * W - odd_p + 1,
        "cia": cia,
        "cib": cib,
        "both": both,
        "ands": ands,
        "no11": no11,
        "mismatch": mismatch,
        "ok": mismatch == 0 and not ands and both == [odd_p + 2],
    }


def self_checks(c20, idA: bool, idB: bool, ham4: dict, ham8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert idA and idB
    assert ham4["ok"] and ham4["odd_p"] == 29 and ham4["both"] == [31]
    assert ham8["ok"] and ham8["odd_p"] == 400 and ham8["both"] == [402]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    idA = da_iff_c_le_a()
    idB = c_le_b_kills_11()
    ham4 = odd_lift(4)
    ham8 = odd_lift(8)
    checks = self_checks(c20, idA, idB, ham4, ham8)
    dump = {
        "cycle": "CE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "ham4": {k: ham4[k] for k in ("odd_p", "n", "cia", "cib", "both", "ands", "no11")},
        "ham8": {k: ham8[k] for k in ("odd_p", "n", "cia", "cib", "both", "ands", "no11")},
        "lemmas": {
            "d_eq_Da_iff_c_implies_a": True,
            "c_implies_b_forbids_11": True,
            "both_implications_only_c_eq_0_all_k": None,
            "no_AND_triple_after_scar_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "d_eq_Da_iff_c_implies_a": "LEMMA",
            "c_implies_b_forbids_11": "LEMMA",
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
    print("ham4", dump["ham4"])
    print("ham8", dump["ham8"])


if __name__ == "__main__":
    main()
