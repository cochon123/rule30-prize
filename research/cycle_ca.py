#!/usr/bin/env python3
"""Cycle CA: unique continuation equals B iff A is the cyclic derivative of B.

U_{t+1}=A_t xor (B_t or U_t). If U=B then A_t = B_t xor B_{t+1}. Conversely
that A makes B itself the unique period-pi continuation (B not identically
0). A second ident-0 in a lift is exactly A=DB for a later consecutive pair.
After an odd doubling T=T0||not T0, the scar pairs (0,T), (T,1), (1,not T)
are not derivative pairs. The rest of the k=4 and k=8 high halves also
avoid A=DB (prefix). Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_ca.py --certify
Dump: research/cycle_ca.json
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


def reconstruct(a: list[int], b: list[int]) -> list[int] | None:
    pi = len(a)
    if all(x == 0 for x in b):
        return None
    s0 = next(t for t in range(pi) if b[t] == 1)
    u = [0] * pi
    u[(s0 + 1) % pi] = a[s0] ^ 1
    t = (s0 + 1) % pi
    for _ in range(pi - 1):
        nxt = (t + 1) % pi
        u[nxt] = a[t] ^ (b[t] | u[t])
        t = nxt
    return u


def deriv(b: list[int]) -> list[int]:
    n = len(b)
    return [b[t] ^ b[(t + 1) % n] for t in range(n)]


def iff_ok(trials: int = 300) -> dict:
    rng = random.Random(2)
    n_iff = 0
    n_eq = 0
    n_built = 0
    for pi in (4, 8, 16):
        for _ in range(trials):
            a = [rng.randint(0, 1) for _ in range(pi)]
            b = [rng.randint(0, 1) for _ in range(pi)]
            u = reconstruct(a, b)
            if u is None:
                continue
            if (u == b) != (a == deriv(b)):
                return {"ok": False}
            n_iff += 1
            if u == b:
                n_eq += 1
        for _ in range(trials):
            b = [rng.randint(0, 1) for _ in range(pi)]
            if all(x == 0 for x in b):
                continue
            a = deriv(b)
            u = reconstruct(a, b)
            if u != b:
                return {"ok": False}
            n_built += 1
    return {"ok": True, "n_iff": n_iff, "n_eq": n_eq, "n_built": n_built}


def scar_not_deriv() -> bool:
    """(0, T||~T), (T, 1), (1, ~T) are never A=DB for T0 not constant."""
    for n0 in (2, 4, 8, 16):
        rng = random.Random(n0)
        for _ in range(40):
            T0 = [rng.randint(0, 1) for _ in range(n0)]
            if T0 == [0] * n0 or T0 == [1] * n0:
                continue
            T = T0 + [x ^ 1 for x in T0]
            ones = [1] * (2 * n0)
            zeros = [0] * (2 * n0)
            nT = [x ^ 1 for x in T]
            if zeros == deriv(T):
                return False
            if T == deriv(ones):
                return False
            if ones == deriv(nT):
                return False
            # closed form: deriv(ones)=0, T!=0; d(0,T)=wt(T)=n0>=2
            if deriv(ones) != zeros:
                return False
            if sum(T) != n0:
                return False
    return True


def post_scar_no_deriv(k: int) -> dict:
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
    hits = 0
    n = 0

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
            u = reconstruct(a, b)
            seqs[p] = u
            if odd_p is not None:
                n += 1
                aa = ext(seqs[p - 2], cur_pi)
                bb = ext(seqs[p - 1], cur_pi)
                if aa == deriv(bb):
                    hits += 1
        p += 1
    return {"k": k, "odd_p": odd_p, "n": n, "hits": hits, "ok": hits == 0 and odd_p is not None}


def diffs_full_rank(k: int) -> bool:
    """B xor U after the odd scar spans the whole F2^L; no linear syndrome."""
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
    diffs: list[int] = []

    def ext(seq: list[int], L: int) -> list[int]:
        return seq if L == len(seq) else seq * (L // len(seq))

    def to_int(seq: list[int]) -> int:
        v = 0
        for i, bit in enumerate(seq):
            if bit:
                v |= 1 << i
        return v

    p = W + 1
    prev = None
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
        if odd_p is not None:
            cur = to_int(ext(seqs[p], cur_pi))
            if prev is None:
                diffs.append(cur)  # vs 0
            else:
                diffs.append(cur ^ prev)
            prev = cur
        p += 1
    L = cur_pi
    a = list(diffs)
    r = 0
    for col in range(L):
        piv = None
        for i in range(r, len(a)):
            if (a[i] >> col) & 1:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        for i in range(len(a)):
            if i != r and (a[i] >> col) & 1:
                a[i] ^= a[r]
        r += 1
    return r == L


def self_checks(
    c20, iff: dict, scar: bool, ham4: dict, ham8: dict, fullrank: bool
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert iff["ok"] and iff["n_built"] > 0
    assert scar and ham4["ok"] and ham8["ok"]
    assert fullrank
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    iff = iff_ok()
    scar = scar_not_deriv()
    ham4 = post_scar_no_deriv(4)
    ham8 = post_scar_no_deriv(8)
    fullrank = diffs_full_rank(8)
    checks = self_checks(c20, iff, scar, ham4, ham8, fullrank)
    dump = {
        "cycle": "CA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "iff": {k: iff[k] for k in ("n_iff", "n_eq", "n_built")},
        "ham4": ham4,
        "ham8": ham8,
        "lemmas": {
            "U_eq_B_iff_A_eq_DB": True,
            "scar_not_derivative": True,
            "linear_syndrome_of_B_xor_U": False,
            "post_scar_A_ne_DB_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "U_eq_B_iff_A_eq_DB": "LEMMA",
            "scar_not_derivative": "LEMMA",
            "linear_syndrome_of_B_xor_U": "KILLED",
            "post_scar_A_ne_DB_all_k": "PREFIX",
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
    print("iff", dump["iff"])
    print("ham4", ham4)
    print("ham8", ham8)


if __name__ == "__main__":
    main()
