#!/usr/bin/env python3
"""Cycle DN: every n0=16 scar is ident-0-free in 43205 extras; k=16 leftover empty.

Bit-sliced unique continuation on Python integers certifies all 65536
length-16 T0 (including constants) have no ident-0 in the next 43205
extras after (0, T0||not T0, 1). Cycle DJ leftover at k=16 is 43205, so
that leftover is empty of ident-0 for every length-16 T0, not only the
prize orbit. Prize u_16=0000110011110011 is an instance. Do not claim a
closed form for a later extra, and do not claim the pi formula for all
k. Not a prize claim.

Run: python3 research/cycle_dn.py --certify
Dump: research/cycle_dn.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits
from cycle_di import mask_bits
from cycle_dj import leftover
from cycle_dk import PRIZE_U16
from cycle_dm import first_ident0_int, pack_bits, reconstruct_int

OUT = Path(__file__).resolve().with_suffix(".json")
N0 = 16
N_EXTRA = leftover(16)  # 43205
N_WORDS = 1 << N0


def index_bit(t: int, n_words: int) -> int:
    """Bitslice of bit t of each index in 0..n_words-1."""
    tile = 1 << t
    ones = ((1 << tile) - 1) << tile
    full = ones
    length = tile << 1
    while length < n_words:
        full |= full << length
        length <<= 1
    return full


def bitslice_T(n0: int) -> tuple[list[int], int, int, int]:
    n_words = 1 << n0
    L = 2 * n0
    mask = (1 << n_words) - 1
    T = [index_bit(t, n_words) for t in range(n0)]
    T += [(~sl) & mask for sl in T]
    return T, mask, n_words, L


def reconstruct_slice(A: list[int], B: list[int], mask: int, L: int) -> list[int]:
    """Bitsliced unique continuation; two guesses for U_0."""
    U0 = [0] * L
    u = 0
    for t in range(L - 1):
        u = A[t] ^ (B[t] | u)
        U0[t + 1] = u
    wrap0 = A[L - 1] ^ (B[L - 1] | u)
    ok0 = (~wrap0) & mask
    U1 = [0] * L
    U1[0] = mask
    u = mask
    for t in range(L - 1):
        u = A[t] ^ (B[t] | u)
        U1[t + 1] = u
    wrap1 = A[L - 1] ^ (B[L - 1] | u)
    ok1 = wrap1 & mask
    return [(ok0 & U0[t]) | (ok1 & U1[t]) for t in range(L)]


def alive_mask(B: list[int], mask: int) -> int:
    acc = 0
    for sl in B:
        acc |= sl
    return acc & mask


def pop_bits(w: int) -> list[int]:
    out: list[int] = []
    while w:
        lsb = w & -w
        out.append(lsb.bit_length() - 1)
        w ^= lsb
    return out


def census(n0: int, max_extra: int) -> dict:
    """First ident-0 extra for every T0 of length n0, or None if none."""
    T, mask, n_words, L = bitslice_T(n0)
    A, B = T, [mask] * L
    first: dict[int, tuple[int, int]] = {}
    remaining = mask
    for cur in range(3, 3 + max_extra):
        live = alive_mask(B, mask)
        newly = remaining & (~live) & mask
        if newly:
            xorA = 0
            for sl in A:
                xorA ^= sl
            for i in pop_bits(newly):
                first[i] = (cur, (xorA >> i) & 1)
            remaining &= ~newly
            if remaining == 0:
                break
        A, B = B, reconstruct_slice(A, B, mask, L)
    hits: Counter[tuple[int, int]] = Counter()
    for cur, sm in first.values():
        hits[(cur, sm)] += 1
    return {
        "n_words": n_words,
        "n_hit": len(first),
        "n_none": remaining.bit_count(),
        "hits": {str(cur): {"odd": sm, "n": n} for (cur, sm), n in sorted(hits.items())},
        "min_extra": min((cur for cur, _ in first.values()), default=None),
        "first": first,
        "remaining": remaining,
    }


def prize_mask(s: str) -> int:
    w = 0
    for i, ch in enumerate(s):
        w |= int(ch) << i
    return w


def slice_matches_scalar() -> bool:
    """Bitslice agrees with packed reconstruct on n0=4 all and n0=8/16 samples."""
    rng = random.Random(41)
    for n0, extra, n_check in ((4, 400, 16), (8, 400, 32), (16, 200, 16)):
        got = census(n0, extra)
        for mask in range(n_check) if n0 == 4 else [rng.randrange(1 << n0) for _ in range(n_check)]:
            t0 = mask_bits(mask, n0)
            cur, sm = first_ident0_int(t0, extra)
            if mask in got["first"]:
                if got["first"][mask] != (cur, sm):
                    return False
            elif cur is not None:
                return False
        T, bmask, _, L = bitslice_T(n0)
        U = reconstruct_slice(T, [bmask] * L, bmask, L)
        for i in range(min(1 << n0, 64)):
            t0 = mask_bits(i, n0)
            t = pack_bits(t0 + [x ^ 1 for x in t0])
            u = reconstruct_int(t, (1 << L) - 1, L)
            packed = 0
            for bit in range(L):
                packed |= ((U[bit] >> i) & 1) << bit
            if packed != u:
                return False
    return True


def self_checks(c20, match: bool, n4: dict, n8: dict, n16: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert match
    assert n4["n_hit"] == 16 and n4["hits"] == {"89": {"odd": 1, "n": 8}, "372": {"odd": 1, "n": 8}}
    assert n8["min_extra"] == 6344 and n8["n_none"] == 112 and leftover(8) == 112
    assert leftover(8) < n8["min_extra"]
    assert n16["n_hit"] == 0 and n16["n_none"] == N_WORDS
    assert n16["n_words"] == N_WORDS and N_EXTRA == 43205 and leftover(16) == 43205
    pz = prize_mask(PRIZE_U16)
    assert 0 <= pz < N_WORDS and pz not in n16["first"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    match = slice_matches_scalar()
    n4 = census(4, 400)
    n8 = census(8, 53000)
    n16 = census(16, N_EXTRA)
    checks = self_checks(c20, match, n4, n8, n16)
    dump = {
        "cycle": "DN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n16": {
            "n_extra": N_EXTRA,
            "n_words": n16["n_words"],
            "n_hit": n16["n_hit"],
            "n_none": n16["n_none"],
            "prize_u16": PRIZE_U16,
            "leftover16": leftover(16),
        },
        "n8": {
            "min_extra": n8["min_extra"],
            "n_none": n8["n_none"],
            "leftover8": leftover(8),
        },
        "lemmas": {
            "bitslice_matches_packed_reconstruct": True,
            "n0_16_no_ident0_in_43205": True,
            "k16_leftover_empty_all_T0": True,
            "prize_u16_in_that_window": True,
            "n0_16_extras_closed_form": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "bitslice_matches_packed_reconstruct": "LEMMA",
            "n0_16_no_ident0_in_43205": "LEMMA",
            "k16_leftover_empty_all_T0": "LEMMA",
            "prize_u16_in_that_window": "LEMMA",
            "n0_16_extras_closed_form": "KILLED",
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
    print("n16", dump["n16"])
    print("n8", dump["n8"])


if __name__ == "__main__":
    main()
