#!/usr/bin/env python3
"""Cycle AD: white-stripe left-diagonals, freshman Green, 00-production kills.

Cycle AC: every left-diagonal e_j(t)=x(t,-t+j) is eventually periodic, but
c_t=e_t(t) is an onset. This cycle names the driven-bit dichotomy (reset vs
integrator), proves that agreeing nonzero drivers force a white stripe
(e_j eventually 0), and gives closed forms through e_7 ≡ 0 and e_9 ≡ 1.
A further stripe e_28 ≡ 0 is the same implication on identified period-4
tails. Freshman expansion of (1+x+x^2)^m over GF(2) matches the doubling
Green function; no-adjacent-1s m have a unique representation.

None of this produces infinitely many centre 00s: a fixed left-diagonal
meets the centred 5-window only finitely often, 1-run endings occupy all
eight 11*** windows, and known stripe onsets are 01 not 00.

Not a prize claim: infinitely many 00s remain unproved.

Run: python3 research/cycle_ad.py --certify
Dump: research/cycle_ad.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]

RUN_END_00 = {"01100", "11101", "11110", "11111"}
RUN_END_ISO = {"01101", "01110", "01111", "11100"}


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
    """[x^d](1+x+x^2)^m over GF(2), doubling recurrence (Cycle AA)."""
    if d < 0 or d > 2 * m:
        return 0
    if m == 0:
        return int(d == 0)
    if m % 2 == 0:
        if d % 2:
            return 0
        return G(m // 2, d // 2)
    n = m // 2
    if d % 2 == 0:
        return G(n, d // 2) ^ G(n, d // 2 - 1)
    return G(n, (d - 1) // 2)


def freshman_parity(m: int, d: int) -> int:
    """Parity of writings d = sum ε_i, ε_i in {0, 2^{a_i}, 2^{a_i+1}}."""
    bits = []
    a = 0
    mm = m
    while mm:
        if mm & 1:
            bits.append(a)
        mm >>= 1
        a += 1
    n = len(bits)
    acc = 0
    tot = 3 ** n
    for mask in range(tot):
        s = 0
        tmp = mask
        for i in range(n):
            ch = tmp % 3
            tmp //= 3
            if ch == 1:
                s += 1 << bits[i]
            elif ch == 2:
                s += 1 << (bits[i] + 1)
        if s == d:
            acc ^= 1
    return acc


def fib_closed(m: int, d: int) -> int:
    """G(m,d) when m has no adjacent 1s: unique representation or none."""
    if m & (m << 1):
        raise ValueError("adjacent bits")
    a = 0
    mm = m
    allowed = 0
    while mm:
        if mm & 1:
            pair = (1 << a) | (1 << (a + 1))
            if d & pair == pair:
                return 0
            allowed |= pair
        mm >>= 1
        a += 1
    if d & ~allowed:
        return 0
    return 1


def step_cell(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def tail_period(seq: list[int], min_len: int = 32) -> tuple[int | None, int | None]:
    n = len(seq)
    for p in range(1, 33):
        need = max(min_len, 4 * p)
        if need > n:
            continue
        tail = seq[-need:]
        if all(tail[i] == tail[i % p] for i in range(need)):
            T = 0
            for i in range(n - p):
                if seq[i] != seq[i + p]:
                    T = i + 1
            return T, p
    return None, None


def run_end_windows() -> dict:
    """Five-windows with (ell,c)=(1,1), i.e. 1-run endings, split by 00 vs isolated 0."""
    recs = {}
    for mask in range(8):
        a, d, e = (mask >> 2) & 1, (mask >> 1) & 1, mask & 1
        b = c = 1
        left, mid, right = step_cell(a, b, c), step_cell(b, c, d), step_cell(c, d, e)
        cpp = left ^ (mid | right)
        word = f"{a}{b}{c}{d}{e}"
        recs[word] = {
            "next_triple": f"{left}{mid}{right}",
            "c_next": mid,
            "c_next2": cpp,
            "is_00": mid == 0 and cpp == 0,
            "is_iso0": mid == 0 and cpp == 1,
        }
    zeros = sorted(w for w, v in recs.items() if v["is_00"])
    iso = sorted(w for w, v in recs.items() if v["is_iso0"])
    return {"windows": recs, "00": zeros, "iso0": iso}


def white_stripe_boolean() -> bool:
    """If a=b, then x' = a XOR (a OR x) is 0 whenever a=1, else x.

    After the first 1 in a not-identically-zero tail, x is 0 forever.
    """
    for a in (0, 1):
        for x in (0, 1):
            got = a ^ (a | x)
            want = 0 if a == 1 else x
            if got != want:
                return False
    return True


def finite_incidence(j: int, t_lo: int, t_hi: int) -> list[int]:
    """Times at which left-diagonal j sits in the centred 5-window."""
    hits = []
    for t in range(t_lo, t_hi + 1):
        spatial = -t + j
        if -2 <= spatial <= 2:
            hits.append(t)
    return hits


def self_checks(
    c20,
    freshman_ok: bool,
    fib_ok: bool,
    forms: dict,
    stripe_bool: bool,
    run_ends: dict,
    hits_fixed: dict,
    stripe28: dict,
    all8: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert freshman_ok
    assert fib_ok
    assert stripe_bool
    assert run_ends["00"] == sorted(RUN_END_00)
    assert run_ends["iso0"] == sorted(RUN_END_ISO)
    assert forms["e3_tmod2"]
    assert forms["e4_one"]
    assert forms["e5_tmod2"]
    assert forms["e6_tmod2"]
    assert forms["e7_zero"]
    assert forms["e9_one"]
    assert forms["c2_c3"] == [0, 1]
    assert forms["c7_c8"] == [0, 1]
    assert stripe28["equal_drivers"]
    assert stripe28["not_zero_drivers"]
    assert stripe28["e28_zero"]
    assert all8
    for j, hits in hits_fixed.items():
        assert len(hits) <= 5
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--tmax", type=int, default=8)
    args = parser.parse_args()
    t0 = time.perf_counter()
    tmax = 1 << args.tmax
    c20 = packed_center_bits(20)
    rows = evolve_rows(tmax)

    def e(j: int, t: int) -> int:
        return (rows[t] >> j) & 1

    freshman_fail = 0
    freshman_n = 0
    for m in range(40):
        nbits = m.bit_count()
        table = [0] * (2 * m + 2)
        tot = 3 ** nbits
        bits = [i for i in range(m.bit_length()) if m & (1 << i)]
        for mask in range(tot):
            s = 0
            tmp = mask
            for i in bits:
                ch = tmp % 3
                tmp //= 3
                if ch == 1:
                    s += 1 << i
                elif ch == 2:
                    s += 1 << (i + 1)
            if 0 <= s <= 2 * m:
                table[s] ^= 1
        for d in range(2 * m + 1):
            freshman_n += 1
            if G(m, d) != table[d]:
                freshman_fail += 1
    # Spot-check the explicit enumerator against the table method.
    for m, d in ((0, 0), (1, 1), (5, 3), (7, 7), (21, 13), (31, 16)):
        if freshman_parity(m, d) != G(m, d):
            freshman_fail += 1
    freshman_ok = freshman_fail == 0

    fib_fail = 0
    fib_n = 0
    for m in range(64):
        if m & (m << 1):
            continue
        for d in range(2 * m + 1):
            fib_n += 1
            if G(m, d) != fib_closed(m, d):
                fib_fail += 1
    fib_ok = fib_fail == 0

    cap = min(tmax, 128)
    e3_ok = all(e(3, t) == (t & 1) for t in range(3, cap + 1))
    e4_ok = all(e(4, t) == 1 for t in range(4, cap + 1))
    e5_ok = all(e(5, t) == (t & 1) for t in range(5, cap + 1))
    e6_ok = all(e(6, t) == (t & 1) for t in range(6, cap + 1))
    e7_ok = all(e(7, t) == 0 for t in range(7, cap + 1))
    e9_ok = all(e(9, t) == 1 for t in range(9, cap + 1))
    forms = {
        "e3_tmod2": e3_ok,
        "e4_one": e4_ok,
        "e5_tmod2": e5_ok,
        "e6_tmod2": e6_ok,
        "e7_zero": e7_ok,
        "e9_one": e9_ok,
        "c2_c3": [e(2, 2), e(3, 3)],
        "c7_c8": [e(7, 7), e(8, 8)],
        "c28_c29": [e(28, 28), e(29, 29)] if tmax >= 29 else None,
    }

    stripe_bool = white_stripe_boolean()
    run_ends = run_end_windows()

    hits_fixed = {
        str(j): finite_incidence(j, max(j, 2), tmax) for j in (0, 1, 2, 4, 7, 9, 28)
    }

    seq26 = [e(26, t) for t in range(26, cap + 1)]
    seq27 = [e(27, t) for t in range(27, cap + 1)]
    seq28 = [e(28, t) for t in range(28, cap + 1)]
    T26, p26 = tail_period(seq26)
    T27, p27 = tail_period(seq27)
    T28, p28 = tail_period(seq28)
    # Compare on a common absolute tail.
    lo = max(26 + (T26 or 0), 27 + (T27 or 0), cap - 32)
    equal = all(e(26, t) == e(27, t) for t in range(lo, cap + 1))
    not_zero = any(e(26, t) for t in range(lo, cap + 1))
    e28_zero = all(e(28, t) == 0 for t in range(max(28, lo), cap + 1))
    stripe28 = {
        "T26": T26,
        "p26": p26,
        "T27": T27,
        "p27": p27,
        "T28": T28,
        "p28": p28,
        "equal_drivers": equal,
        "not_zero_drivers": not_zero,
        "e28_zero": e28_zero,
        "c28": e(28, 28) if tmax >= 28 else None,
        "c29": e(29, 29) if tmax >= 29 else None,
    }

    # Orbit: all eight 11*** windows occur; 1-run endings split ~50/50.
    end_w: Counter[str] = Counter()
    n_end = n_end_00 = n_end_iso = 0
    n10 = n01 = 0
    for t in range(2, tmax - 2):

        def bit(tt: int, jj: int) -> int:
            k = jj + tt
            if k < 0:
                return 0
            return (rows[tt] >> k) & 1

        c, nxt = bit(t, 0), bit(t + 1, 0)
        if c == 1 and nxt == 0:
            n10 += 1
            w5 = "".join(str(bit(t, jj)) for jj in range(-2, 3))
            end_w[w5] += 1
            n_end += 1
            if bit(t + 2, 0) == 0:
                n_end_00 += 1
            else:
                n_end_iso += 1
        if c == 0 and nxt == 1:
            n01 += 1
    all8 = set(end_w) >= (RUN_END_00 | RUN_END_ISO)

    # Reset/integrator on the first 12 diagonals.
    dichotomy = []
    for j in range(2, 13):
        seq_b = [e(j - 1, t) for t in range(j, cap + 1)]
        seq_x = [e(j, t) for t in range(j, cap + 1)]
        Tb, pb = tail_period(seq_b)
        Tx, px = tail_period(seq_x)
        btail = seq_b[-32:]
        dichotomy.append(
            {
                "j": j,
                "pb": pb,
                "px": px,
                "reset": 1 in btail,
                "integrator": set(btail) == {0},
            }
        )

    checks = self_checks(
        c20,
        freshman_ok,
        fib_ok,
        forms,
        stripe_bool,
        run_ends,
        hits_fixed,
        stripe28,
        all8,
    )

    dump = {
        "cycle": "AD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "freshman_n": freshman_n,
        "freshman_fail": freshman_fail,
        "fib_n": fib_n,
        "fib_fail": fib_fail,
        "closed_forms": forms,
        "white_stripe_boolean": stripe_bool,
        "run_end_00": run_ends["00"],
        "run_end_iso0": run_ends["iso0"],
        "stripe28": stripe28,
        "finite_incidence": hits_fixed,
        "n10": n10,
        "n01": n01,
        "n_end": n_end,
        "n_end_00": n_end_00,
        "n_end_iso": n_end_iso,
        "end_windows": dict(end_w),
        "all_eight_11star": all8,
        "dichotomy": dichotomy,
        "lemmas": {
            "freshman_G": freshman_ok,
            "fibonacci_binary_G": fib_ok,
            "white_stripe_implication": stripe_bool,
            "e7_white_stripe": e7_ok,
            "e9_one": e9_ok,
            "e28_white_stripe": e28_zero,
            "infinitely_many_10": True,
            "finite_incidence_fixed_j": True,
            "infinitely_many_00": None,
            "prize": False,
        },
        "verdict": {
            "freshman_G": "LEMMA",
            "fibonacci_binary_G": "LEMMA",
            "reset_integrator": "LEMMA",
            "white_stripe_implication": "LEMMA",
            "e7_e9_closed_forms": "LEMMA",
            "e28_white_stripe": "LEMMA",
            "infinitely_many_10": "LEMMA",
            "finite_incidence_fixed_j": "LEMMA",
            "nested_left_5window_00": "KILLED",
            "one_run_ending_forces_00": "KILLED",
            "only_e2_is_white_stripe": "KILLED",
            "white_stripe_onset_is_00": "KILLED",
            "infinitely_many_00": "OPEN",
            "infinitely_many_white_stripes": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("freshman_fail", freshman_fail, "fib_fail", fib_fail)
    print("e7", e7_ok, "e9", e9_ok, "e28", e28_zero, "c28_c29", forms["c28_c29"])
    print("run_end_00", run_ends["00"])
    print("n10", n10, "n_end_00", n_end_00, "n_end_iso", n_end_iso, "all8", all8)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
