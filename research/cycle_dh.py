#!/usr/bin/env python3
"""Cycle DH: reconstruct(1,O) is type N; 6-bit post-toggle ident-0 gap.

Unique continuation of (A,B) is identically 0 iff A=B (B not 0). For even
half-length, reconstruct(all-1s, O) is type N, so bit p+3 after an odd
doubling is N. Then p+3 != p+4 because NOR(S,U)=XOR(S,U) would force S=U=1.
Hence bits p through p+5 are nonzero: no ident-0 at p+1,...,p+6. A later
odd ident-0 at even period needs two consecutive equal type-N odd-weight
bits. Not a prize claim: the 6-bit gap does not fill an annulus.

Run: python3 research/cycle_dh.py --certify
Dump: research/cycle_dh.json
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
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext, twocopy_type
from cycle_ch import shifted_not

OUT = Path(__file__).resolve().with_suffix(".json")
EXPECTED_P = {4: 29, 8: 400, 16: 87867}


def unfold(a: list[int]) -> list[int]:
    u = [0] * len(a)
    for t in range(len(a) - 1):
        u[t + 1] = a[t] ^ u[t]
    return u


def mask_bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def odd_copy(s: list[int]) -> list[int]:
    return s + [x ^ 1 for x in s]


def reconstruct_zero_iff_equal() -> bool:
    """reconstruct(A,A)=0; A!=B and B not 0 implies U not 0."""
    for n in range(2, 9):
        for mask in range(1 << n):
            a = mask_bits(mask, n)
            if not any(a):
                continue
            if reconstruct(a, a) != [0] * n:
                return False
            b = a[:]
            b[0] ^= 1
            if not any(b):
                b[1] = 1
            u = reconstruct(a, b)
            if u is None or all(x == 0 for x in u):
                return False
    return True


def ones_O_is_N() -> bool:
    """reconstruct(all-1s, O) is type N iff the half-length is even.
    n=1 (odd) yields type O; even n<=8 exhaustive, n=16 random."""
    for s in ([0], [1]):
        o = odd_copy(s)
        if twocopy_type(reconstruct([1, 1], o)) != "O":
            return False
    for n in (2, 4, 6, 8):
        ones = [1] * (2 * n)
        for mask in range(1 << n):
            o = odd_copy(mask_bits(mask, n))
            if twocopy_type(reconstruct(ones, o)) != "N":
                return False
    rng = random.Random(23)
    ones = [1] * 32
    for _ in range(40):
        o = odd_copy([rng.randint(0, 1) for _ in range(16)])
        if twocopy_type(reconstruct(ones, o)) != "N":
            return False
    return True


def chain_from_O(o: list[int]) -> list[list[int]] | None:
    """(O, all-1s, shifted-not O, N3, N4, N5) after a white stripe."""
    L = len(o)
    zeros = [0] * L
    ones = reconstruct(zeros, o)
    if ones != [1] * L:
        return None
    s = reconstruct(o, ones)
    if s != shifted_not(o) or twocopy_type(s) != "O":
        return None
    n3 = reconstruct(ones, s)
    if n3 is None or twocopy_type(n3) != "N":
        return None
    n4 = reconstruct(s, n3)
    if n4 is None or n3 == n4 or all(x == 0 for x in n4):
        return None
    n5 = reconstruct(n3, n4)
    if n5 is None or all(x == 0 for x in n5):
        return None
    return [o, ones, s, n3, n4, n5]


def six_bit_gap() -> bool:
    """Bits p..p+5 nonzero after odd doubling at even half-length."""
    for n in (2, 4, 6, 8):
        for mask in range(1 << n):
            ch = chain_from_O(odd_copy(mask_bits(mask, n)))
            if ch is None:
                return False
            if any(all(x == 0 for x in s) for s in ch):
                return False
    rng = random.Random(29)
    for n in (10, 16):
        for _ in range(40):
            ch = chain_from_O(odd_copy([rng.randint(0, 1) for _ in range(n)]))
            if ch is None or any(all(x == 0 for x in s) for s in ch):
                return False
    return True


def odd_equal_is_N() -> bool:
    """At length divisible by 4, xorcat=1 forces type N, and A=A unfolds to 0."""
    rng = random.Random(31)
    for n in (4, 8, 16):
        for _ in range(50):
            a = [rng.randint(0, 1) for _ in range(n)]
            if xorcat(a) != 1:
                a[0] ^= 1
            if twocopy_type(a) != "N":
                return False
            if reconstruct(a, a) != [0] * n:
                return False
    return True


def prize_six_gap() -> dict:
    """Prize k=4,8,16: p+3 is N; k=8,16 have the 6-bit gap inside (W,2W]."""
    rows: dict[int, dict] = {}
    for k, p_odd in EXPECTED_P.items():
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
        cur_pi = pi
        found = None
        p = W + 1
        while p <= 2 * W:
            a = ext(seqs[p - 2], cur_pi)
            b = ext(seqs[p - 1], cur_pi)
            if all(x == 0 for x in b):
                sm = xorcat(a)
                u = unfold(a)
                if sm == 1:
                    found = p
                    seqs[p] = u + [x ^ 1 for x in u]
                    cur_pi *= 2
                    break
                seqs[p] = u
            else:
                seqs[p] = reconstruct(a, b)
            p += 1
        if found != p_odd:
            return {"ok": False, "k": k, "p": found}
        end = min(found + 5, 2 * W)
        for q in range(found + 1, end + 1):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        n3 = ext(seqs[found + 3], cur_pi) if found + 3 in seqs else None
        if n3 is None or twocopy_type(n3) != "N":
            return {"ok": False, "k": k, "why": "n3"}
        info = {"p": found, "n3": "N", "upto": end}
        if found + 4 in seqs and found + 5 in seqs:
            n4 = ext(seqs[found + 4], cur_pi)
            n5 = ext(seqs[found + 5], cur_pi)
            if n3 == n4 or all(x == 0 for x in n4) or all(x == 0 for x in n5):
                return {"ok": False, "k": k, "why": "n45"}
            info["six_gap"] = True
        rows[k] = info
    if "six_gap" not in rows[8] or "six_gap" not in rows[16]:
        return {"ok": False, "why": "range"}
    return {"ok": True, "rows": rows}


def self_checks(c20, iff0: bool, ntype: bool, gap: bool, oddn: bool, prize: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert iff0 and ntype and gap and oddn
    assert prize["ok"] and prize["rows"][16]["p"] == 87867 and prize["rows"][8]["six_gap"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    iff0 = reconstruct_zero_iff_equal()
    ntype = ones_O_is_N()
    gap = six_bit_gap()
    oddn = odd_equal_is_N()
    prize = prize_six_gap()
    checks = self_checks(c20, iff0, ntype, gap, oddn, prize)
    dump = {
        "cycle": "DH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prize_gap": prize["rows"],
        "lemmas": {
            "reconstruct_zero_iff_A_eq_B": True,
            "ones_O_type_N_even_half": True,
            "post_odd_double_6bit_gap": True,
            "odd_ident0_after_double_needs_equal_N": True,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reconstruct_zero_iff_A_eq_B": "LEMMA",
            "ones_O_type_N_even_half": "LEMMA",
            "post_odd_double_6bit_gap": "LEMMA",
            "odd_ident0_after_double_needs_equal_N": "LEMMA",
            "pi_formula_all_k": "PREFIX",
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
    print("prize_gap", dump["prize_gap"])


if __name__ == "__main__":
    main()
