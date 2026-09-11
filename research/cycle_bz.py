#!/usr/bin/env python3
"""Cycle BZ: ident-0 iff consecutive equal bits; no consecutive ident-0.

If two consecutive packed-bit strings are equal and not identically 0,
the unique reset continuation is identically 0: the first 1-reset has
a=b=1, so it forces u=0, and 0 is invariant under u' = a xor (b or u)
when a=b. Hence ident-0 at p iff lambda_{p-2} equals lambda_{p-1}, on
any orbit with packed bit 0 equal to 1 (a leftward cascade of ident-0
would reach bit 0). Consecutive ident-0 is therefore impossible. After
an odd high toggle the Hamming distance between consecutive high bits
stays positive through the rest of the lift (prefix). Even weight is
not invariant under unique continuation. Not a prize claim.

Run: python3 research/cycle_bz.py --certify
Dump: research/cycle_bz.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def left_step(word: int, W: int) -> int:
    mask = (1 << (W + 1)) - 1
    hi = word & mask
    mid = (word << 1) & mask
    lo = (word << 2) & mask
    new = (lo ^ (mid | hi)) & mask
    return (new & ~1) | 1


def apply_n(word: int, W: int, n: int) -> int:
    for _ in range(n):
        word = left_step(word, W)
    return word


def left_at_2W(k: int) -> int:
    W = 1 << k
    s = 1
    for _ in range(2 * W):
        s = left_step(s, W)
    return s


def min_period(word: int, W: int) -> int:
    for n in (1, 2, 4, 8, 16, 32, 64):
        if apply_n(word, W, n) == word:
            return n
    raise AssertionError("period not a small 2-power")


def prize_cycle(k: int) -> tuple[int, list[int]]:
    W = 1 << k
    w = left_at_2W(k)
    pi = min_period(w, W)
    cyc = []
    x = w
    for _ in range(pi):
        cyc.append(x)
        x = left_step(x, W)
    return pi, cyc


def xorcat(seq: list[int]) -> int:
    acc = 0
    for x in seq:
        acc ^= x
    return acc


def reconstruct_bit(a: list[int], b: list[int]):
    pi = len(a)
    if all(x == 0 for x in b):
        return False, None, ("ident0", xorcat(a))
    s0 = next(t for t in range(pi) if b[t] == 1)
    u = [0] * pi
    u[(s0 + 1) % pi] = a[s0] ^ 1
    t = (s0 + 1) % pi
    for _ in range(pi - 1):
        nxt = (t + 1) % pi
        u[nxt] = a[t] ^ (b[t] | u[t])
        t = nxt
    return True, u, "unique"


def a_eq_b_implies_zero(trials: int = 300) -> bool:
    rng = random.Random(1)
    for pi in (4, 8, 16):
        for _ in range(trials):
            a = [rng.randint(0, 1) for _ in range(pi)]
            b = list(a)
            if all(x == 0 for x in b):
                continue
            ok, u, _note = reconstruct_bit(a, b)
            if not ok or u is None or any(u):
                return False
    return True


def ident0_iff_equal(kmax: int) -> dict:
    all_ok = True
    n_ident0 = []
    consec = False
    some_odd_wt = False
    for k in range(3, kmax + 1):
        W = 1 << k
        pi, cyc = prize_cycle(k)
        seq = [[(w >> p) & 1 for w in cyc] for p in range(W + 1)]
        ident0 = [p for p in range(W + 1) if all(x == 0 for x in seq[p])]
        aeqb = [p for p in range(2, W + 1) if seq[p - 2] == seq[p - 1]]
        if ident0 != aeqb:
            all_ok = False
        for i in range(len(ident0) - 1):
            if ident0[i + 1] == ident0[i] + 1:
                consec = True
        n_ident0.append(len(ident0))
        for p in range(W + 1):
            if xorcat(seq[p]) == 1:
                some_odd_wt = True
    return {
        "ok": all_ok,
        "no_consecutive": not consec,
        "n_ident0": n_ident0,
        "some_odd_weight": some_odd_wt,
    }


def post_odd_hamming(k: int) -> dict:
    """After first odd high toggle, min Hamming distance of consecutive bits."""
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
    dists: list[int] = []

    def ext(seq: list[int], L: int) -> list[int]:
        return seq if L == len(seq) else seq * (L // len(seq))

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
            _ok, u, _note = reconstruct_bit(a, b)
            seqs[p] = u
        if odd_p is not None:
            prev = ext(seqs[p - 1], cur_pi)
            dists.append(sum(x ^ y for x, y in zip(prev, seqs[p])))
        p += 1
    return {
        "k": k,
        "odd_p": odd_p,
        "n": len(dists),
        "min_d": min(dists) if dists else None,
        "zeros": sum(d == 0 for d in dists),
        "some_odd_post_wt": False,
    }


def post_odd_weights_not_all_even(k: int) -> bool:
    """Unique continuation after an odd doubling produces some odd 2pi-weight."""
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    seen_odd = False
    doubled = False

    def ext(seq: list[int], L: int) -> list[int]:
        return seq if L == len(seq) else seq * (L // len(seq))

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
                u = u + [x ^ 1 for x in u]
                cur_pi *= 2
                doubled = True
            seqs[p] = u
        else:
            _ok, u, _note = reconstruct_bit(a, b)
            seqs[p] = u
            if doubled and xorcat(u) == 1:
                seen_odd = True
        p += 1
    return seen_odd


def self_checks(c20, impl: bool, iff: dict, ham4: dict, ham8: dict, oddwt: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert impl
    assert iff["ok"] and iff["no_consecutive"] and iff["some_odd_weight"]
    assert ham4["zeros"] == 0 and ham4["min_d"] and ham4["min_d"] > 0
    assert ham8["zeros"] == 0 and ham8["min_d"] and ham8["min_d"] > 0
    assert oddwt
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    impl = a_eq_b_implies_zero()
    iff = ident0_iff_equal(12)
    ham4 = post_odd_hamming(4)
    ham8 = post_odd_hamming(8)
    oddwt = post_odd_weights_not_all_even(8)
    checks = self_checks(c20, impl, iff, ham4, ham8, oddwt)
    dump = {
        "cycle": "BZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n_ident0": iff["n_ident0"],
        "ham4": {"odd_p": ham4["odd_p"], "min_d": ham4["min_d"], "n": ham4["n"]},
        "ham8": {"odd_p": ham8["odd_p"], "min_d": ham8["min_d"], "n": ham8["n"]},
        "lemmas": {
            "a_eq_b_implies_ident0": True,
            "ident0_iff_consecutive_equal": True,
            "no_consecutive_ident0": True,
            "post_odd_hamming_positive_all_k": None,
            "even_weight_invariant": False,
            "all_bits_even_pi_weight_k_ge_3": False,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "a_eq_b_implies_ident0": "LEMMA",
            "ident0_iff_consecutive_equal": "LEMMA",
            "no_consecutive_ident0": "LEMMA",
            "post_odd_hamming_positive_all_k": "PREFIX",
            "even_weight_invariant": "KILLED",
            "all_bits_even_pi_weight_k_ge_3": "KILLED",
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
