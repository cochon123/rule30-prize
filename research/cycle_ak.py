#!/usr/bin/env python3
"""Cycle AK: Fermat-odd spines; leftmost-11 hit parity is always odd.

For every q=2^a+1, Cycle AI from t=2^k by 2^{k+a} has both extras off the
cone, so phi^{(q)}_k := c_{q 2^k} XOR c_{2^k} equals the Green remainder
on [2^k, q 2^k). Period 2^m forces every such phi to 0. The XOR of
leftmost-11 Green hits on that interval is 1 (pure G induction), so
phi^{(q)}_k = 1 XOR S^{(q)}_k for every Fermat-odd q, not only q=3.
S is not identically 0.

Not a prize claim: some phi=1 infinitely often remains open.

Run: python3 research/cycle_ak.py --certify
Dump: research/cycle_ak.json
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


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def spatial(row: int, t: int, j: int) -> int:
    if abs(j) > t:
        return 0
    return (row >> (j + t)) & 1


def xor_G(M: int, D: int) -> int:
    acc = 0
    for m in range(M):
        acc ^= G(m, D)
    return acc


def G_parity_lemmas(amax: int, extra: int) -> dict:
    """XOR_{m<2^b} G(m,2^b-1)=1; XOR_{m<2^n} G(m, 2^n+2^{n-a}-1)=1;
    G at s=U is 1 iff a odd.
    """
    mersenne_ok = True
    for b in range(0, amax + extra + 1):
        if xor_G(1 << b, (1 << b) - 1) != 1:
            mersenne_ok = False
    fermat_ok = True
    sU = {}
    counts = {}
    for a in range(1, amax + 1):
        sU[a] = []
        counts[a] = []
        for n in range(a, a + extra + 1):
            D = (1 << n) + (1 << (n - a)) - 1
            acc = n1 = 0
            for m in range(1 << n):
                g = G(m, D)
                acc ^= g
                n1 += g
            if acc != 1:
                fermat_ok = False
            counts[a].append(n1)
            sU[a].append(G((1 << n) - 1, D))
        # s=U hit is G(2^n-1, D), should equal a%2
        if any(g != (a % 2) for g in sU[a]):
            fermat_ok = False
    return {
        "mersenne_ok": mersenne_ok,
        "fermat_ok": fermat_ok,
        "sU_hit": sU,
        "p1_counts": counts,
    }


def and_J(rows: list[int], t0: int, t1: int, target_t: int) -> tuple[int, int]:
    acc = 0
    p1 = 0
    for s in range(t0, t1):
        A = (rows[s] << 1) & rows[s]
        delta = target_t - s - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(delta, target_t - p):
                acc ^= 1
                if p == 1:
                    p1 ^= 1
            tmp >>= 1
            p += 1
    return acc, p1


def synthetic_all_phi_zero() -> dict:
    T = 5
    recs = []
    all_ok = True
    qs = [3, 5, 9, 17]
    for m in range(0, 5):
        p = 1 << m
        seed = [((i * 3 + 1) % 2) for i in range(p)]
        N = 1 << 14
        c = [0] * N
        for i in range(T, N):
            c[i] = seed[(i - T) % p]
        k0 = m
        while (1 << k0) < T:
            k0 += 1
        ok = True
        n = 0
        for k in range(k0, 11):
            U = 1 << k
            for q in qs:
                if q * U >= N:
                    continue
                n += 1
                if c[q * U] ^ c[U]:
                    ok = False
        if not ok:
            all_ok = False
        recs.append({"m": m, "ok": ok, "n": n})
    return {"all_ok": all_ok, "rows": recs}


def self_checks(c20, glem: dict, ident_fail: int, p1_fail: int, synth: dict,
                phis: dict, not_all1: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert glem["mersenne_ok"] and glem["fermat_ok"]
    assert ident_fail == 0 and p1_fail == 0
    assert synth["all_ok"]
    assert not_all1
    for a, hits in glem["sU_hit"].items():
        assert all(g == (int(a) % 2) for g in hits)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    glem = G_parity_lemmas(4, 6)
    synth = synthetic_all_phi_zero()

    qs = [3, 5, 9]
    kmax = 7
    rows = evolve_rows(9 * (1 << kmax) + 2)
    ident_fail = 0
    p1_fail = 0
    phis = {q: [] for q in qs}
    for q in qs:
        a = (q - 1).bit_length() - 1
        for k in range(0, kmax + 1):
            U = 1 << k
            t1 = q * U
            J, p1 = and_J(rows, U, t1, t1)
            phi = spatial(rows[t1], t1, 0) ^ spatial(rows[U], U, 0)
            phis[q].append(phi)
            if J != phi:
                ident_fail += 1
            if p1 != 1:
                p1_fail += 1
    not_all1 = any(0 in phis[q] and 1 in phis[q] for q in qs)
    checks = self_checks(c20, glem, ident_fail, p1_fail, synth, phis, not_all1)
    dump = {
        "cycle": "AK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "G_parity": {
            "mersenne_ok": glem["mersenne_ok"],
            "fermat_ok": glem["fermat_ok"],
            "sU_hit": {str(a): v for a, v in glem["sU_hit"].items()},
            "p1_counts": {str(a): v for a, v in glem["p1_counts"].items()},
        },
        "identity_fail": ident_fail,
        "p1_parity_fail": p1_fail,
        "phi": {str(q): phis[q] for q in qs},
        "synthetic": synth,
        "lemmas": {
            "fermat_odd_identity": True,
            "p1_hit_parity_odd": True,
            "period_2m_forces_all_phi_0": True,
            "some_phi_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "fermat_odd_identity": "LEMMA",
            "p1_hit_parity_odd": "LEMMA",
            "period_2m_forces_all_phi_0": "LEMMA",
            "S_identically_0": "KILLED",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"], "phi", dump["phi"])


if __name__ == "__main__":
    main()
