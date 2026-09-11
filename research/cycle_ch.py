#!/usr/bin/env python3
"""Cycle CH: next scar bit is shifted-not T; Hamming gap 2 on |T0|=8.

After ident-0, T=T0||not T0, ident-1, packed update forces
lambda_{I+1,t} = not T_{t-1}. That equals the ident-1 continuation iff T
is alternating. Even |T0|>=2 never makes T0||not T0 alternating (junction
repeat), so the first tail pair is never equal. Consecutive Hamming along
the unique-continuation tail is at least 2 for every nonconstant T0 of
length 8 on 130 bits (covers the prize k=8 lift). Length 4 reaches
Hamming 1 at q=43 on an 80-bit window; the prize k=4 lift is only four
high bits and stays at Hamming >=2. A blanket gap of 3 does not hold.
Not a prize claim.

Run: python3 research/cycle_ch.py --certify
Dump: research/cycle_ch.json
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
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext

OUT = Path(__file__).resolve().with_suffix(".json")


def scar_lift(T0: list[int], n_extra: int) -> dict[int, list[int]] | None:
    n0 = len(T0)
    T = T0 + [x ^ 1 for x in T0]
    L = 2 * n0
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    for cur in range(3, 3 + n_extra):
        a, b = seqs[cur - 2], seqs[cur - 1]
        if all(x == 0 for x in b):
            return None
        u = reconstruct(a, b)
        if u is None:
            return None
        seqs[cur] = u
    return seqs


def ham(xs: list[int], ys: list[int]) -> int:
    return sum(x ^ y for x, y in zip(xs, ys))


def shifted_not(T: list[int]) -> list[int]:
    L = len(T)
    return [T[(t - 1) % L] ^ 1 for t in range(L)]


def is_alternating(seq: list[int]) -> bool:
    n = len(seq)
    return n >= 2 and all(seq[t] != seq[(t + 1) % n] for t in range(n))


def even_block_never_alternating() -> bool:
    """T=T0||not T0 is never alternating for even |T0|>=2."""
    for n0 in (2, 4, 6, 8, 10, 12, 16):
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            T = T0 + [x ^ 1 for x in T0]
            if is_alternating(T):
                return False
    return True


def closed_form_ok() -> bool:
    """lambda_{I+1,t} = not T_{t-1}; next continuation differs iff T
    is not alternating, which even |T0|>=2 guarantees."""
    for n0 in (2, 4, 6, 8, 10, 12, 16):
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            T = T0 + [x ^ 1 for x in T0]
            ones = [1] * len(T)
            u = reconstruct(T, ones)
            if u != shifted_not(T):
                return False
            if is_alternating(T):
                return False
            S = shifted_not(T)
            u4 = reconstruct(ones, S)
            if u4 is None or ham(S, u4) == 0:
                return False
    return True


def tail_ham(n0: int, n_extra: int) -> dict:
    min_h = 10**9
    min_su = 10**9
    n_ok = 0
    n_h1 = 0
    n_h2 = 0
    n_odd = 0
    first_h1 = None
    h1_masks: list[int] = []
    for mask in range(1 << n0):
        T0 = [(mask >> i) & 1 for i in range(n0)]
        if sum(T0) in (0, n0):
            continue
        seqs = scar_lift(T0, n_extra)
        if seqs is None:
            return {"ok": False, "n0": n0, "n_extra": n_extra}
        n_ok += 1
        T = seqs[1]
        S = seqs[3]
        if S != shifted_not(T):
            return {"ok": False, "n0": n0, "n_extra": n_extra}
        su = ham(S, seqs[4])
        if su < min_su:
            min_su = su
        saw_h1 = False
        for q in range(1, max(seqs) + 1):
            h = ham(seqs[q - 1], seqs[q])
            if h < min_h:
                min_h = h
            if h == 0:
                return {"ok": False, "n0": n0, "n_extra": n_extra}
            if h == 1:
                n_h1 += 1
                saw_h1 = True
                if first_h1 is None:
                    first_h1 = {"mask": mask, "q": q, "T0": T0}
            if h == 2:
                n_h2 += 1
            if h % 2:
                n_odd += 1
        if saw_h1:
            h1_masks.append(mask)
    return {
        "n0": n0,
        "n_extra": n_extra,
        "n_ok": n_ok,
        "min_h": min_h,
        "min_su": min_su,
        "n_h1": n_h1,
        "n_h2": n_h2,
        "n_odd": n_odd,
        "first_h1": first_h1,
        "n_h1_T0": len(h1_masks),
        "ok": n_ok > 0 and min_h >= 1 and min_su >= 3,
    }


def n0_2_none() -> bool:
    for T0 in ([0, 1], [1, 0]):
        if scar_lift(T0, 20) is not None:
            return False
    return True


def prize_orbit_ham(k: int) -> dict:
    """Consecutive Hamming on prize bits from the first odd ident-0."""
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
    hs = []
    for q in range(odd_p + 1, 2 * W + 1):
        prev = ext(seqs[q - 1], L)
        cur = ext(seqs[q], L)
        hs.append(ham(prev, cur))
    return {
        "k": k,
        "odd_p": odd_p,
        "n_pairs": len(hs),
        "min_h": min(hs) if hs else None,
        "n_h1": sum(1 for h in hs if h == 1),
    }


def self_checks(
    c20,
    closed: bool,
    never_alt: bool,
    h4: dict,
    h8: dict,
    n2: bool,
    pk4: dict,
    pk8: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert closed and never_alt and n2 and h4["ok"] and h8["ok"]
    assert h4["n_h1"] > 0 and h4["min_h"] == 1
    assert h4["first_h1"] is not None and h4["first_h1"]["q"] == 43
    assert h8["min_h"] >= 2 and h8["n_h1"] == 0
    assert h8["n_odd"] > 0
    assert h4["min_su"] >= 3 and h8["min_su"] >= 3
    assert pk4["min_h"] >= 2 and pk8["min_h"] >= 2
    assert pk4["odd_p"] == 29 and pk8["odd_p"] == 400
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    closed = closed_form_ok()
    never_alt = even_block_never_alternating()
    n2 = n0_2_none()
    h4 = tail_ham(4, 80)
    h8 = tail_ham(8, 130)
    pk4 = prize_orbit_ham(4)
    pk8 = prize_orbit_ham(8)
    checks = self_checks(c20, closed, never_alt, h4, h8, n2, pk4, pk8)
    dump = {
        "cycle": "CH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "h4": {
            k: h4[k]
            for k in (
                "n0",
                "n_extra",
                "n_ok",
                "min_h",
                "min_su",
                "n_h1",
                "n_h2",
                "n_odd",
                "n_h1_T0",
                "first_h1",
            )
        },
        "h8": {
            k: h8[k]
            for k in (
                "n0",
                "n_extra",
                "n_ok",
                "min_h",
                "min_su",
                "n_h1",
                "n_h2",
                "n_odd",
                "n_h1_T0",
            )
        },
        "prize_k4_ham": pk4,
        "prize_k8_ham": pk8,
        "lemmas": {
            "next_bit_is_shifted_not_T": True,
            "even_T0_not_T0_never_alternating": True,
            "SU_unequal_all_even_n0": True,
            "SU_hamming_ge_3_n0_4_8": True,
            "tail_hamming_ge_2_n0_8": True,
            "tail_hamming_ge_2_n0_4_long": False,
            "tail_hamming_ge_3": False,
            "tail_hamming_always_even": False,
            "all_T0_2power_hamming_ge_2": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "next_bit_is_shifted_not_T": "LEMMA",
            "even_T0_not_T0_never_alternating": "LEMMA",
            "SU_unequal_all_even_n0": "LEMMA",
            "SU_hamming_ge_3_n0_4_8": "LEMMA",
            "tail_hamming_ge_2_n0_8": "LEMMA",
            "tail_hamming_ge_2_n0_4_long": "KILLED",
            "tail_hamming_ge_3": "KILLED",
            "tail_hamming_always_even": "KILLED",
            "all_T0_2power_hamming_ge_2": "PREFIX",
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
    print("h4", dump["h4"])
    print("h8", dump["h8"])
    print("prize_k4_ham", pk4)
    print("prize_k8_ham", pk8)


if __name__ == "__main__":
    main()
