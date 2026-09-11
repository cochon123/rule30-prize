#!/usr/bin/env python3
"""Cycle BY: ident0 twin; period is a 2-power; one odd toggle implies the seed.

Identically-0 packed bit p with a non-zero left neighbour forces identically-1
at p+2 (absorbing OR after the first toggle 1). The left-word period is a
2-power: resets preserve the period, toggles at most double it. Nested low
bits make pi_{k+1} a multiple of pi_k, hence pi_{k+1}=pi_k * 2^{r} with r
the number of odd-weight high toggles. If r<=1 at every scale then
pi_k | 2^{k-1} for every k, which is the Cycle BW seed. Through k=16 the
ratio is in {1,2}. Two ident-0 bits can occur (k=16) without doubling.
Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_by.py --certify
Dump: research/cycle_by.json
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


def xor_cat(seq: list[int]) -> int:
    acc = 0
    for x in seq:
        acc ^= x
    return acc


def two_copy_xor_ok() -> bool:
    """XOR of two copies of any GF(2) block is 0."""
    for seq in ([1], [1, 0], [1, 1, 0, 1], [1] * 8, [0, 1] * 8):
        if xor_cat(seq + seq) != 0:
            return False
        if xor_cat(seq) ^ xor_cat(seq) != 0:
            return False
    return True


def twins_ok(kmax: int) -> dict:
    """ident0 at p with lambda_{p-1} not ident0 => ident1 at p+2."""
    rows = []
    all_ok = True
    for k in range(3, kmax + 1):
        W = 1 << k
        pi, cyc = prize_cycle(k)
        seq = [[(w >> p) & 1 for w in cyc] for p in range(W + 1)]
        ident0 = [p for p in range(W + 1) if all(x == 0 for x in seq[p])]
        ident1 = {p for p in range(W + 1) if all(x == 1 for x in seq[p])}
        for p in ident0:
            if p >= 1 and all(x == 0 for x in seq[p - 1]):
                all_ok = False
            if p + 2 <= W and (p + 2) not in ident1:
                all_ok = False
            if p >= 2 and seq[p - 2] != seq[p - 1]:
                all_ok = False
        rows.append({"k": k, "ident0": ident0, "ok": all_ok})
    return {"ok": all_ok, "n": len(rows)}


def periods(kmax: int) -> dict:
    pis = []
    n0 = []
    for k in range(1, kmax + 1):
        W = 1 << k
        w = left_at_2W(k)
        pi = min_period(w, W)
        pis.append(pi)
        OR = 0
        s = w
        for _ in range(pi):
            OR |= s
            s = left_step(s, W)
        ident0 = [p for p in range(W + 1) if ((OR >> p) & 1) == 0]
        n0.append(len(ident0))
    ratios = [pis[i] // pis[i - 1] for i in range(1, len(pis))]
    H = [1 << (k - 1) for k in range(1, kmax + 1)]
    divides = [H[i] % pis[i] == 0 for i in range(kmax)]
    multiples = [pis[i] % pis[i - 1] == 0 for i in range(1, kmax)]
    two_powers = all(p & (p - 1) == 0 and p > 0 for p in pis)
    two_new_no_double = any(
        n0[i] - n0[i - 1] >= 2 and ratios[i - 1] == 1 for i in range(1, len(n0))
    )
    return {
        "pis": pis,
        "n0": n0,
        "ratios": ratios,
        "ratios_in_12": all(r in (1, 2) for r in ratios),
        "divides_H": all(divides),
        "nested_multiples": all(multiples),
        "two_powers": two_powers,
        "k4_half": pis[3] == 4 and H[3] == 8,
        "max_ratio": max(ratios),
        "two_new_no_double": two_new_no_double,
    }


def lift_odd_counts(kmin: int, kmax: int) -> dict:
    """High-half ident0-driven toggles and their a-XOR over current pi."""
    rows = []
    for k in range(kmin, kmax + 1):
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
        events = []
        cur_pi = pi

        def ext(seq: list[int], L: int) -> list[int]:
            if L == len(seq):
                return seq
            return seq * (L // len(seq))

        p = W + 1
        while p <= 2 * W:
            a = ext(seqs[p - 2], cur_pi)
            b = ext(seqs[p - 1], cur_pi)
            if all(x == 0 for x in b):
                sm = xor_cat(a)
                events.append({"p": p, "xor": sm, "pi": cur_pi})
                u = [0] * cur_pi
                for t in range(cur_pi - 1):
                    u[t + 1] = a[t] ^ u[t]
                if sm == 1:
                    u = u + [x ^ 1 for x in u]
                    cur_pi *= 2
                seqs[p] = u
            else:
                s0 = next(t for t in range(cur_pi) if b[t] == 1)
                u = [0] * cur_pi
                u[(s0 + 1) % cur_pi] = a[s0] ^ 1
                t = (s0 + 1) % cur_pi
                for _ in range(cur_pi - 1):
                    nxt = (t + 1) % cur_pi
                    u[nxt] = a[t] ^ (b[t] | u[t])
                    t = nxt
                seqs[p] = u
            p += 1
        n_odd = sum(1 for e in events if e["xor"] == 1)
        n_even = sum(1 for e in events if e["xor"] == 0)
        rows.append({"k": k, "n_odd": n_odd, "n_even": n_even, "events": events})
    return {
        "rows": rows,
        "max_odd": max(r["n_odd"] for r in rows),
        "some_two_ident0": any(r["n_even"] + r["n_odd"] >= 2 for r in rows),
    }


def self_checks(c20, copies: bool, twins: dict, per: dict, lifts: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert copies and twins["ok"]
    assert per["two_powers"] and per["nested_multiples"] and per["k4_half"]
    assert per["divides_H"] and per["ratios_in_12"]
    assert lifts["max_odd"] <= 1
    assert per["two_new_no_double"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    copies = two_copy_xor_ok()
    twins = twins_ok(12)
    per = periods(16)
    lifts = lift_odd_counts(4, 12)
    checks = self_checks(c20, copies, twins, per, lifts)
    dump = {
        "cycle": "BY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "periods": per["pis"],
        "ratios": per["ratios"],
        "n_ident0": per["n0"],
        "lift_odds": [r["n_odd"] for r in lifts["rows"]],
        "lift_evens": [r["n_even"] for r in lifts["rows"]],
        "lemmas": {
            "ident0_implies_ident1_plus2": True,
            "period_is_2_power": True,
            "nested_period_multiple": True,
            "two_copy_xor_vanishes": True,
            "k4_period_is_H_over_2": True,
            "seed_if_ratios_in_12": True,
            "at_most_one_odd_toggle_all_k": None,
            "at_most_one_ident0_per_lift": False,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "ident0_implies_ident1_plus2": "LEMMA",
            "period_is_2_power": "LEMMA",
            "nested_period_multiple": "LEMMA",
            "two_copy_xor_vanishes": "LEMMA",
            "k4_period_is_H_over_2": "LEMMA",
            "seed_if_ratios_in_12": "LEMMA",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "at_most_one_ident0_per_lift": "KILLED",
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
    print("periods", dump["periods"])
    print("ratios", dump["ratios"])
    print("lift_odds", dump["lift_odds"])


if __name__ == "__main__":
    main()
