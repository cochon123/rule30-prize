#!/usr/bin/env python3
"""Cycle BW: left-machine period H=2^{k-1}; Green shift; low-half induction.

The left W+1 packed bits (W=2^k) are autonomous (Cycle BV). For k=1 and
k=2 they are periodic with period H=W/2 for every t>=2. One seed equality
F^H(L_k(2W))=L_k(2W) then extends period H to all later times by autonomy,
which is stronger than BV's F^W=id and still forces J_B^{->2U}=0. The low
H+1 bits are the scale-(k-1) machine, so they inherit period H from P_{k-1}.
Green weights on a W-window at degrees d<H have period H because
G(m+2^a,d)=G(m,d) for m,d<2^a. The seed holds through k=12 (prefix).
Period H from time W fails at k=5 (high bits only). Not a prize claim.

Run: python3 research/cycle_bw.py --certify
Dump: research/cycle_bw.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
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


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def packed_bit(row: int, t: int, p: int) -> int:
    if p < 0 or p > 2 * t:
        return 0
    return (row >> p) & 1


def left_word(row: int, W: int) -> int:
    return row & ((1 << (W + 1)) - 1)


def left_step(word: int, W: int) -> int:
    """Packed update new_p = old_{p-2} xor (old_{p-1} or old_p); bit 0 stays 1."""
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


def green_xor(rows: list[int], t0: int, t1: int, Tbit: int) -> int:
    acc = 0
    for t in range(t0, t1):
        tmp = (rows[t] << 1) & rows[t]
        m = t1 - t - 1
        p = 0
        while tmp:
            if tmp & 1 and G(m, Tbit - p):
                acc ^= 1
            tmp >>= 1
            p += 1
    return acc


def evolve(tmax: int) -> list[int]:
    rows = []
    row = 1
    for _t in range(tmax + 1):
        rows.append(row)
        row = rule30_step(row)
    return rows


def green_shift_ok(amax: int) -> bool:
    for a in range(amax + 1):
        H = 1 << a
        for m in range(H):
            for d in range(H):
                if G(m + H, d) != G(m, d):
                    return False
    return True


def freshman_product_ok(amax: int) -> bool:
    for a in range(amax + 1):
        H = 1 << a
        mmax = min(H, 16)
        for m in range(mmax):
            for d in range(2 * (m + H) + 1):
                got = G(m + H, d)
                want = G(m, d) ^ G(m, d - H) ^ G(m, d - 2 * H)
                if got != want:
                    return False
    return True


def nested_low_ok(rows: list[int], kmax: int) -> bool:
    for k in range(2, kmax + 1):
        W = 1 << k
        H = W >> 1
        mask = (1 << (H + 1)) - 1
        tmax = min(len(rows) - 1, 8 * W)
        for t in range(tmax + 1):
            if left_word(rows[t], H) != (left_word(rows[t], W) & mask):
                return False
    return True


def packed_period_identity_ok(rows: list[int], kmax: int) -> bool:
    """lambda_p(t+H) xor lambda_p(t) = extras xor J on the H-window at t=2W."""
    for k in range(1, kmax + 1):
        W = 1 << k
        H = W >> 1
        t0 = 2 * W
        t1 = t0 + H
        if t1 >= len(rows):
            return False
        for p in range(W + 1):
            lhs = packed_bit(rows[t1], t1, p) ^ packed_bit(rows[t0], t0, p)
            extra = packed_bit(rows[t0], t0, p - H) ^ packed_bit(
                rows[t0], t0, p - W
            )
            J = green_xor(rows, t0, t1, p)
            if lhs != extra ^ J:
                return False
    return True


def k1_k2_period_ok(tmax: int) -> bool:
    """k=1 constant 110; k=2 period-2 from bit-3 flip. t>=2."""
    row = 1
    prev3 = None
    for t in range(tmax + 1):
        if t >= 2:
            if packed_bit(row, t, 0) != 1 or packed_bit(row, t, 1) != 1:
                return False
            if packed_bit(row, t, 2) != 0:
                return False
            if packed_bit(row, t, 4) != 1:
                return False
            b3 = packed_bit(row, t, 3)
            if t == 2 and b3 != 0:
                return False
            if prev3 is not None and b3 != (1 ^ prev3):
                return False
            w2 = left_word(row, 4)
            if t % 2 == 0:
                if w2 != 0b10011:  # LSB-first 11001
                    return False
            else:
                if w2 != 0b11011:  # LSB-first 11011
                    return False
            w1 = left_word(row, 2)
            if w1 != 0b011:  # 110
                return False
            prev3 = b3
        row = rule30_step(row)
    return True


def unique_cycle_ok(k: int, period: int) -> dict:
    """Affine space bits 0,1,2 = 1,1,0. Unique period-cycle of given length."""
    W = 1 << k
    nfree = W + 1 - 3
    hits = []
    for high in range(1 << nfree):
        w = 0b011 | (high << 3)
        if apply_n(w, W, period) == w:
            hits.append(w)
    hitset = set(hits)
    attract = True
    bound = 4 * W
    for high in range(1 << nfree):
        w = 0b011 | (high << 3)
        s = w
        ok = False
        for _ in range(bound):
            if s in hitset:
                ok = True
                break
            s = left_step(s, W)
        if not ok:
            attract = False
            break
    return {
        "k": k,
        "period": period,
        "n_fixed": len(hits),
        "unique_4": len(hits) == 4,
        "globally_attracting": attract,
        "hits": hits,
    }


def unique_driven_lift(low_hits: list[int], W: int, n_high: int) -> dict:
    """High n_high bits driven by a low cycle: unique attracting cycle?"""
    P = len(low_hits)
    H = W >> 1
    low_bits = H + 1
    LOWMASK = (1 << low_bits) - 1
    s = low_hits[0]
    cyc = [s]
    for _ in range(P - 1):
        s = left_step(s, H)
        cyc.append(s)
    if set(cyc) != set(low_hits):
        return {"unique": False, "n_cycles": -1, "period": 0, "hits": []}
    N = 1 << n_high
    tot = P * N

    def succ(sid: int) -> int:
        phase = sid % P
        high = sid // P
        word = cyc[phase] | (high << low_bits)
        nxt = left_step(word, W)
        nphase = (phase + 1) % P
        if (nxt & LOWMASK) != cyc[nphase]:
            raise RuntimeError("low bits drifted")
        nhigh = nxt >> low_bits
        return nphase + P * nhigh

    seen = bytearray(tot)
    cycles = []
    for start in range(tot):
        if seen[start]:
            continue
        trail: list[int] = []
        pos: dict[int, int] = {}
        s = start
        while not seen[s] and s not in pos:
            pos[s] = len(trail)
            trail.append(s)
            s = succ(s)
        if s in pos:
            cycles.append(trail[pos[s] :])
        for u in trail:
            seen[u] = 1
    hits = []
    if len(cycles) == 1:
        for sid in cycles[0]:
            phase = sid % P
            high = sid // P
            hits.append(cyc[phase] | (high << low_bits))
    return {
        "unique": len(cycles) == 1,
        "n_cycles": len(cycles),
        "period": len(cycles[0]) if cycles else 0,
        "n_states": tot,
        "hits": hits,
    }


def prize_on_cycle(k: int, t: int, hits: list[int]) -> bool:
    row = 1
    for _ in range(t):
        row = rule30_step(row)
    W = 1 << k
    return left_word(row, W) in set(hits)


def seed_period_H(kmax: int) -> dict:
    """L(2W)==L(2W+H) and hence L(2W)==L(3W), sampled from the prize orbit."""
    need: set[int] = set()
    for k in range(1, kmax + 1):
        W = 1 << k
        H = W >> 1
        need.update((2 * W, 2 * W + H, 3 * W))
    tmax = max(need)
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    seed = []
    eq23 = []
    for k in range(1, kmax + 1):
        W = 1 << k
        H = W >> 1
        a = left_word(samp[2 * W], W)
        b = left_word(samp[2 * W + H], W)
        c = left_word(samp[3 * W], W)
        seed.append(a == b)
        eq23.append(a == c)
        # autonomy check: F^H(a)==b
        if apply_n(a, W, H) != b:
            seed[-1] = False
    return {
        "seed": seed,
        "eq23": eq23,
        "all_seed": all(seed),
        "all_eq23": all(eq23),
    }


def fail_at_W_high_only(rows: list[int], kmax: int) -> dict:
    """Period H from t=W fails, and failures (when present) are bits > H."""
    killed = False
    high_only = True
    first = {}
    for k in range(3, kmax + 1):
        W = 1 << k
        H = W >> 1
        if W + H >= len(rows):
            continue
        a = left_word(rows[W], W)
        b = left_word(rows[W + H], W)
        xor = a ^ b
        fail = [p for p in range(W + 1) if (xor >> p) & 1]
        first[k] = fail
        if fail:
            killed = True
            if min(fail) <= H:
                high_only = False
    return {"killed_from_W": killed, "high_only": high_only, "fail_bits": first}


def whole_space_not_period_H() -> bool:
    """F^H is not the identity on the whole affine space (k=3)."""
    W = 8
    n_id = 0
    for high in range(1 << 6):
        w = 0b011 | (high << 3)
        if apply_n(w, W, 4) == w:
            n_id += 1
    return n_id == 4  # only the 4-cycle, not the whole space


def self_checks(
    c20,
    shift: bool,
    prod: bool,
    nested: bool,
    ident: bool,
    k12: bool,
    cyc3: dict,
    cyc4: dict,
    lift5: dict,
    on3: bool,
    on4: bool,
    on5: bool,
    seed: dict,
    failW: dict,
    not_whole: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert shift and prod and nested and ident and k12
    assert cyc3["unique_4"] and cyc3["globally_attracting"] and on3
    assert cyc4["unique_4"] and cyc4["globally_attracting"] and on4
    assert lift5["unique"] and lift5["period"] == 8 and on5
    assert seed["all_seed"] and seed["all_eq23"]
    assert failW["killed_from_W"] and failW["high_only"]
    assert not_whole
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    shift = green_shift_ok(8)
    prod = freshman_product_ok(6)
    rows = evolve(8 * (1 << 6))
    nested = nested_low_ok(rows, 6)
    ident = packed_period_identity_ok(rows, 6)
    k12 = k1_k2_period_ok(128)
    cyc3 = unique_cycle_ok(3, 4)
    cyc4 = unique_cycle_ok(4, 4)
    lift5 = unique_driven_lift(cyc4["hits"], 32, 16)
    on3 = prize_on_cycle(3, 2, cyc3["hits"])
    on4 = prize_on_cycle(4, 16, cyc4["hits"])
    on5 = prize_on_cycle(5, 64, lift5["hits"])
    seed = seed_period_H(12)
    failW = fail_at_W_high_only(rows, 6)
    not_whole = whole_space_not_period_H()
    checks = self_checks(
        c20,
        shift,
        prod,
        nested,
        ident,
        k12,
        cyc3,
        cyc4,
        lift5,
        on3,
        on4,
        on5,
        seed,
        failW,
        not_whole,
    )
    dump = {
        "cycle": "BW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "seed_k12": seed["seed"],
        "eq23_from_seed": seed["eq23"],
        "fail_at_W": failW["fail_bits"],
        "unique_cycles": {
            "k3_n_fixed": cyc3["n_fixed"],
            "k4_n_fixed": cyc4["n_fixed"],
            "k3_attracting": cyc3["globally_attracting"],
            "k4_attracting": cyc4["globally_attracting"],
            "k5_driven_unique": lift5["unique"],
            "k5_driven_period": lift5["period"],
            "k5_driven_states": lift5["n_states"],
            "prize_on_k3_at_t2": on3,
            "prize_on_k4_at_t16": on4,
            "prize_on_k5_at_t64": on5,
        },
        "lemmas": {
            "green_shift_small_degree": True,
            "freshman_product_shift": True,
            "low_half_is_previous_machine": True,
            "packed_period_H_identity": True,
            "k1_k2_period_H_for_t_ge_2": True,
            "seed_implies_global_period_H": True,
            "period_H_implies_BV_freeze": True,
            "unique_attractor_k3_k4": True,
            "unique_driven_lift_k5": True,
            "period_H_from_time_W_all_k": False,
            "F_H_id_on_whole_affine_space": False,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "green_shift_small_degree": "LEMMA",
            "freshman_product_shift": "LEMMA",
            "low_half_is_previous_machine": "LEMMA",
            "packed_period_H_identity": "LEMMA",
            "k1_k2_period_H_for_t_ge_2": "LEMMA",
            "seed_implies_global_period_H": "LEMMA",
            "period_H_implies_BV_freeze": "LEMMA",
            "unique_attractor_k3_k4": "LEMMA",
            "unique_driven_lift_k5": "LEMMA",
            "period_H_from_time_W_all_k": "KILLED",
            "F_H_id_on_whole_affine_space": "KILLED",
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
    print("seed", seed["seed"])
    print("fail_at_W", failW["fail_bits"])


if __name__ == "__main__":
    main()
