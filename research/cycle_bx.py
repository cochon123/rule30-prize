#!/usr/bin/env python3
"""Cycle BX: reset lift of the left machine; frozen bits; period doubling.

If packed bit p-1 is not identically 0 on a period-pi orbit of the lower
bits, bit p has a unique period-pi continuation: the first 1-reset forces
it, and wrap-around is automatic. If bit p-1 is identically 0, bit p
toggles by bit p-2 and the period is pi or 2pi according to the XOR of
that driver. Reconstructing high bits this way matches the prize word at
time 2W on every unblocked lift k->k+1 through k=12. Period 8 for all
k>=5 is false (k=9 has period 16). Frozen zeros 2,7,28 grow at k=9.
Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bx.py --certify
Dump: research/cycle_bx.json
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


def reconstruct_bit(a: list[int], b: list[int]) -> tuple[bool, list[int] | None, object]:
    pi = len(a)
    if all(x == 0 for x in b):
        sm = 0
        for x in a:
            sm ^= x
        return False, None, ("b_ident0", sm)
    s0 = next(t for t in range(pi) if b[t] == 1)
    u = [0] * pi
    u[(s0 + 1) % pi] = a[s0] ^ 1
    t = (s0 + 1) % pi
    for _ in range(pi - 1):
        nxt = (t + 1) % pi
        u[nxt] = a[t] ^ (b[t] | u[t])
        t = nxt
    nxt = (t + 1) % pi
    expect = a[t] ^ (b[t] | u[t])
    if expect != u[nxt]:
        return False, u, "inconsistent"
    return True, u, "unique"


def wrap_automatic(trials: int = 400) -> bool:
    rng = random.Random(0)
    for pi in (4, 8, 16):
        for _ in range(trials):
            a = [rng.randint(0, 1) for _ in range(pi)]
            b = [rng.randint(0, 1) for _ in range(pi)]
            ok, _u, note = reconstruct_bit(a, b)
            if note == "inconsistent":
                return False
            if all(x == 0 for x in b):
                if ok:
                    return False
            elif not ok:
                return False
    return True


def toggle_ok(kmax: int = 8) -> bool:
    """On prize cycles, bits with ident0 driver obey u' = a xor u."""
    for k in range(3, kmax + 1):
        W = 1 << k
        pi, cyc = prize_cycle(k)
        seq = [[(w >> p) & 1 for w in cyc] for p in range(W + 1)]
        for p in range(2, W + 1):
            b = seq[p - 1]
            if any(b):
                continue
            a = seq[p - 2]
            u = seq[p]
            for t in range(pi):
                if u[(t + 1) % pi] != a[t] ^ u[t]:
                    return False
            sm = 0
            for x in a:
                sm ^= x
            if sm == 1 and pi % 2:
                return False
    return True


def frozen_and_period(kmax: int) -> dict:
    rows = []
    prev0: set[int] = set()
    prev1: set[int] = set()
    for k in range(1, kmax + 1):
        W = 1 << k
        pi, cyc = prize_cycle(k)
        AND = (1 << (W + 1)) - 1
        OR = 0
        for w in cyc:
            AND &= w
            OR |= w
        ident0 = [p for p in range(W + 1) if ((OR >> p) & 1) == 0]
        ident1 = [p for p in range(W + 1) if ((AND >> p) & 1) == 1]
        H = W >> 1
        high0 = [p for p in ident0 if p > H]
        new0 = [p for p in ident0 if p not in prev0]
        new1 = [p for p in ident1 if p not in prev1]
        rows.append(
            {
                "k": k,
                "minp": pi,
                "ident0": ident0,
                "ident1": ident1,
                "high0": high0,
                "new0": new0,
                "new1": new1,
                "divides_H": H % pi == 0 if pi else False,
            }
        )
        prev0, prev1 = set(ident0), set(ident1)
    return {
        "rows": rows,
        "all_divides_H": all(r["divides_H"] for r in rows),
        "period8_all_k_ge5": all(r["minp"] == 8 for r in rows if r["k"] >= 5),
        "ident0_stable_28": all(
            r["ident0"] == [2, 7, 28] for r in rows if r["k"] >= 5
        ),
        "high0_without_double": any(
            rows[i]["high0"] and rows[i]["minp"] == rows[i - 1]["minp"]
            for i in range(1, len(rows))
        ),
    }


def lift_k_to_k1(k: int) -> dict:
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    blocked = None
    n_unique = 0
    for p in range(W + 1, 2 * W + 1):
        ok, u, note = reconstruct_bit(seqs[p - 2], seqs[p - 1])
        if not ok:
            blocked = {"p": p, "note": list(note) if isinstance(note, tuple) else note}
            break
        seqs[p] = u
        n_unique += 1
    match = False
    if blocked is None:
        _pi2, cyc2 = prize_cycle(k + 1)
        lowmask = (1 << (W + 1)) - 1
        for ph, w2 in enumerate(cyc2):
            lw = w2 & lowmask
            if lw not in cyc:
                continue
            j = cyc.index(lw)
            if all(((w2 >> p) & 1) == seqs[p][j] for p in range(W + 1, 2 * W + 1)):
                match = True
                break
    return {
        "k": k,
        "pi": pi,
        "n_unique": n_unique,
        "need": W,
        "blocked": blocked,
        "prize_match": match,
    }


def lifts_ok(kmin: int, kmax: int) -> dict:
    out = []
    for k in range(kmin, kmax + 1):
        out.append(lift_k_to_k1(k))
    unblocked = [r for r in out if r["blocked"] is None]
    blocked = [r for r in out if r["blocked"] is not None]
    return {
        "rows": out,
        "unblocked_all_match": all(r["prize_match"] and r["n_unique"] == r["need"] for r in unblocked),
        "n_unblocked": len(unblocked),
        "n_blocked": len(blocked),
        "blocked_ps": [r["blocked"]["p"] for r in blocked],
    }


def self_checks(c20, wrap: bool, tog: bool, frozen: dict, lifts: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert wrap and tog
    assert frozen["all_divides_H"]
    assert not frozen["period8_all_k_ge5"]
    assert not frozen["ident0_stable_28"]
    assert frozen["high0_without_double"]
    assert lifts["unblocked_all_match"]
    assert lifts["n_unblocked"] >= 6
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    wrap = wrap_automatic()
    tog = toggle_ok(8)
    frozen = frozen_and_period(16)
    lifts = lifts_ok(4, 11)
    checks = self_checks(c20, wrap, tog, frozen, lifts)
    dump = {
        "cycle": "BX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "periods": [r["minp"] for r in frozen["rows"]],
        "ident0": [r["ident0"] for r in frozen["rows"]],
        "blocked_ps": lifts["blocked_ps"],
        "n_unblocked": lifts["n_unblocked"],
        "lemmas": {
            "reset_unique_continuation": True,
            "wrap_automatic_if_some_b_1": True,
            "toggle_when_b_ident0": True,
            "unblocked_lift_matches_prize": True,
            "period_divides_H_on_prefix": True,
            "period_8_for_all_k_ge_5": False,
            "ident0_stable_2_7_28": False,
            "high_ident0_iff_period_doubles": False,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reset_unique_continuation": "LEMMA",
            "wrap_automatic_if_some_b_1": "LEMMA",
            "toggle_when_b_ident0": "LEMMA",
            "unblocked_lift_matches_prize": "LEMMA",
            "period_divides_H_on_prefix": "PREFIX",
            "period_8_for_all_k_ge_5": "KILLED",
            "ident0_stable_2_7_28": "KILLED",
            "high_ident0_iff_period_doubles": "KILLED",
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
    print("blocked_ps", dump["blocked_ps"])


if __name__ == "__main__":
    main()
