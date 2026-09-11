#!/usr/bin/env python3
"""Cycle CC: A=DB iff the next-right packed bit is the spatial AND.

On a Rule 30 orbit, lambda_{p-1}(t+1)=lambda_{p-3}(t) xor
(lambda_{p-2}(t) or lambda_{p-1}(t)). The 3-bit identity
a = b xor b' iff c = a and b holds on every triple, so the time
series of (p-2, p-1) is a derivative pair iff lambda_{p-3} equals
the AND of those two bits at every time. Later ident-0 is exactly
a later AND-triple. Always-011 as a witness is false. No AND-triple
after the scar on the k=4 and k=8 odd lifts (prefix). Not a prize
claim.

Run: python3 research/cycle_cc.py --certify
Dump: research/cycle_cc.json
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


def truth_table_ok() -> bool:
    """a == b xor b' iff c == a and b, with b' = c xor (a or b)."""
    for c in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                bp = c ^ (a | b)
                left = a == (b ^ bp)
                right = c == (a & b)
                if left != right:
                    return False
    return True


def and_closed() -> set[tuple[int, int, int]]:
    return {(c, a, b) for c in (0, 1) for a in (0, 1) for b in (0, 1) if c == (a & b)}


def odd_lift_and(k: int) -> dict:
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
    n011_zero = []
    and_hits = []
    adb_hits = []
    mismatch = 0
    n = 0
    min_bad = None
    S = and_closed()
    q0 = odd_p
    while q0 <= 2 * W:
        c = ext(seqs[q0 - 3], L)
        a = ext(seqs[q0 - 2], L)
        b = ext(seqs[q0 - 1], L)
        and_eq = c == [a[t] & b[t] for t in range(L)]
        adb = a == deriv(b)
        if and_eq != adb:
            mismatch += 1
        if and_eq:
            and_hits.append(q0)
        if adb:
            adb_hits.append(q0)
        n011 = sum(1 for t in range(L) if (c[t], a[t], b[t]) == (0, 1, 1))
        if n011 == 0:
            n011_zero.append(q0)
        n_bad = sum(1 for t in range(L) if (c[t], a[t], b[t]) not in S)
        if min_bad is None or n_bad < min_bad:
            min_bad = n_bad
        n += 1
        q0 += 1
    return {
        "k": k,
        "odd_p": odd_p,
        "n": n,
        "mismatch": mismatch,
        "and_hits": and_hits,
        "adb_hits": adb_hits,
        "n011_zero": n011_zero,
        "min_bad": min_bad,
        "ok": mismatch == 0 and not and_hits and not adb_hits and min_bad is not None and min_bad > 0,
    }


def self_checks(c20, tt: bool, ham4: dict, ham8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert tt and len(and_closed()) == 4
    assert ham4["ok"] and ham4["odd_p"] == 29
    assert ham8["ok"] and ham8["odd_p"] == 400
    assert ham8["n011_zero"]  # always-011 is false
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    tt = truth_table_ok()
    ham4 = odd_lift_and(4)
    ham8 = odd_lift_and(8)
    checks = self_checks(c20, tt, ham4, ham8)
    dump = {
        "cycle": "CC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "ham4": {
            "odd_p": ham4["odd_p"],
            "n": ham4["n"],
            "min_bad": ham4["min_bad"],
            "n011_zero": ham4["n011_zero"],
        },
        "ham8": {
            "odd_p": ham8["odd_p"],
            "n": ham8["n"],
            "min_bad": ham8["min_bad"],
            "n_n011_zero": len(ham8["n011_zero"]),
        },
        "lemmas": {
            "A_eq_DB_iff_spatial_AND": True,
            "later_ident0_iff_AND_triple": True,
            "always_011_witness": False,
            "no_AND_triple_after_scar_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "A_eq_DB_iff_spatial_AND": "LEMMA",
            "later_ident0_iff_AND_triple": "LEMMA",
            "always_011_witness": "KILLED",
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
