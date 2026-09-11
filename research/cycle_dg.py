#!/usr/bin/env python3
"""Cycle DG: odd doubling for k>=3 needs type-N a; 4-bit post-toggle gap.

xorcat(s||s)=0 always. xorcat(s||~s)=|s| mod 2, so an odd 2-copy odd-doubles
iff the half-length is odd. pi_3=4 and nested restriction force pi_k>=4 for
every k>=3, hence every later odd ident-0 needs a type-N left neighbour.
After an odd doubling at even pi, the bits are (white 0, O, all-1, shifted-not
O); none of the next four packed bits is ident-0. Not a prize claim: the
4-bit gap does not fill a dyadic annulus, and the pi formula remains a prefix.

Run: python3 research/cycle_dg.py --certify
Dump: research/cycle_dg.json
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


def xorcat_twocopy() -> bool:
    """xorcat(s||s)=0; xorcat(s||~s)=|s| mod 2."""
    for n in range(1, 11):
        for mask in range(1 << n):
            s = [(mask >> i) & 1 for i in range(n)]
            if xorcat(s + s) != 0:
                return False
            if xorcat(s + [x ^ 1 for x in s]) != (n % 2):
                return False
    rng = random.Random(11)
    for n in (12, 16, 32):
        for _ in range(40):
            s = [rng.randint(0, 1) for _ in range(n)]
            if xorcat(s + s) != 0:
                return False
            if xorcat(s + [x ^ 1 for x in s]) != (n % 2):
                return False
    return True


def e_o_odd_double() -> bool:
    """E never odd-doubles. O odd-doubles iff |s| is odd."""
    rng = random.Random(13)
    for n in (1, 2, 4, 8, 16):
        for _ in range(30):
            s = [rng.randint(0, 1) for _ in range(n)]
            e = s + s
            o = s + [x ^ 1 for x in s]
            if twocopy_type(e) != "E" or xorcat(e) != 0:
                return False
            if twocopy_type(o) != "O":
                return False
            if (xorcat(o) == 1) != (n % 2 == 1):
                return False
    return True


def pi_ge_4() -> bool:
    """pi_3=4 and pi_{k+1} is a multiple of pi_k, so pi_k>=4 for k>=3."""
    pi3, _ = prize_cycle(3)
    if pi3 != 4:
        return False
    prev = pi3
    for k in range(4, 8):
        pi, _ = prize_cycle(k)
        if pi < 4 or pi % prev:
            return False
        prev = pi
    return True


def post_double_gap(trials: int = 60) -> bool:
    """After odd doubling at even n: (0, O, 1, shifted-not O); no ident-0
    in the next four packed bits. Twin all-1s holds for any non-zero b."""
    rng = random.Random(17)
    for n in (4, 8, 16):
        for _ in range(trials):
            a = [rng.randint(0, 1) for _ in range(n)]
            if xorcat(a) != 1:
                a[0] ^= 1
            u = unfold(a)
            U = u + [x ^ 1 for x in u]
            L = 2 * n
            zeros = [0] * L
            if twocopy_type(U) != "O" or xorcat(U) != 0:
                return False
            ones = reconstruct(zeros, U)
            if ones != [1] * L:
                return False
            nxt = reconstruct(U, ones)
            if nxt != shifted_not(U) or twocopy_type(nxt) != "O" or xorcat(nxt) != 0:
                return False
            nxt3 = reconstruct(ones, nxt)
            if nxt3 is None or all(x == 0 for x in nxt3):
                return False
            for s in (U, ones, nxt, nxt3):
                if all(x == 0 for x in s):
                    return False
            b = [rng.randint(0, 1) for _ in range(L)]
            if all(x == 0 for x in b):
                b[0] = 1
            if reconstruct(zeros, b) != [1] * L:
                return False
    return True


def prize_post_tuple() -> dict:
    """On the prize orbit, k=4,8,16 odd toggles have type-N a and the
    post-doubling 5-tuple (E a||a, 0, O, 1, shifted-not O)."""
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
        a_pre = seqs[found - 2]
        if twocopy_type(a_pre) != "N" or xorcat(a_pre) != 1:
            return {"ok": False, "k": k, "why": "a_pre"}
        for q in (found + 1, found + 2):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        bm2 = ext(seqs[found - 2], cur_pi)
        bm1 = ext(seqs[found - 1], cur_pi)
        b0 = ext(seqs[found], cur_pi)
        b1 = ext(seqs[found + 1], cur_pi)
        b2 = ext(seqs[found + 2], cur_pi)
        if twocopy_type(bm2) != "E" or xorcat(bm2) != 0:
            return {"ok": False, "k": k, "why": "-2"}
        if any(bm1) or twocopy_type(bm1) != "E":
            return {"ok": False, "k": k, "why": "white"}
        if twocopy_type(b0) != "O" or xorcat(b0) != 0:
            return {"ok": False, "k": k, "why": "O"}
        if b1 != [1] * cur_pi:
            return {"ok": False, "k": k, "why": "1"}
        if b2 != shifted_not(b0) or twocopy_type(b2) != "O" or xorcat(b2) != 0:
            return {"ok": False, "k": k, "why": "+2"}
        rows[k] = {"p": found, "a_type": "N"}
    return {"ok": True, "rows": rows}


def k2_O_odd() -> bool:
    """k=2 is the O-type odd ident-0: |s|=1 is odd, xorcat(01)=1."""
    pi, cyc = prize_cycle(2)
    W = 4
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    p = W + 1
    while p <= 2 * W:
        a = ext(seqs[p - 2], pi)
        b = ext(seqs[p - 1], pi)
        if all(x == 0 for x in b):
            return (
                p == 8
                and a == [0, 1]
                and twocopy_type(a) == "O"
                and xorcat(a) == 1
            )
        u = reconstruct(a, b)
        if u is None:
            return False
        seqs[p] = u
        p += 1
    return False


def self_checks(c20, copies: bool, eo: bool, pige: bool, gap: bool, tup: dict, k2: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert copies and eo and pige and gap and k2
    assert tup["ok"] and tup["rows"][8]["p"] == 400 and tup["rows"][16]["p"] == 87867
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    copies = xorcat_twocopy()
    eo = e_o_odd_double()
    pige = pi_ge_4()
    gap = post_double_gap()
    tup = prize_post_tuple()
    k2 = k2_O_odd()
    checks = self_checks(c20, copies, eo, pige, gap, tup, k2)
    dump = {
        "cycle": "DG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prize_tuple": tup["rows"],
        "lemmas": {
            "xorcat_s_cat_not_s_is_n_mod_2": True,
            "E_never_odd_double_O_iff_half_odd": True,
            "pi_k_ge_4_for_k_ge_3": True,
            "odd_ident0_k_ge_3_needs_type_N": True,
            "post_odd_double_4bit_gap": True,
            "k2_O_is_the_half_odd_exception": True,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "xorcat_s_cat_not_s_is_n_mod_2": "LEMMA",
            "E_never_odd_double_O_iff_half_odd": "LEMMA",
            "pi_k_ge_4_for_k_ge_3": "LEMMA",
            "odd_ident0_k_ge_3_needs_type_N": "LEMMA",
            "post_odd_double_4bit_gap": "LEMMA",
            "k2_O_is_the_half_odd_exception": "LEMMA",
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
    print("prize_tuple", dump["prize_tuple"])


if __name__ == "__main__":
    main()
