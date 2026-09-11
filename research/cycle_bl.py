#!/usr/bin/env python3
"""Cycle BL: exact unique through pentuple Green bits on the 3-fold annulus.

Cycles AP–AR listed four unique-Green bits, one double, five triples,
and four quadruples on the 3-fold (theta) annulus, with exhaustiveness
left as a prefix. The same C_le / Green-lift count used on the 5-fold
and 9-fold covering annuli (Cycles BG–BK) upgrades those prefixes to
lemmas and adds eight pentuples for every k>=5. Extra bits of those
multiplicities are identically 0. The classified bits are not
identically-1 productions, and unique+triple+pentuple XOR is not
theta_k. Septuples still grow with k.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bl.py --certify
Dump: research/cycle_bl.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]

# (r, M) families on the 3-fold annulus. M=-1 is j=k+1.
UNIQ = [(3, 0), (5, 1), (1, -1), (1, 0)]
DBL = [(3, 1)]
TRI = [(1, 1), (9, 2), (11, 2), (19, 3), (23, 3)]
QUAD = [(3, 2), (5, 2), (7, 2), (15, 3)]
PENT = [(17, 3), (21, 3), (37, 4), (39, 4), (45, 4), (47, 4), (79, 5), (95, 5)]
BA_Q = (12, 16, 18, 20, 26, 28, 34, 50)
AX_Q = (6, 8, 10, 14)


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


@lru_cache(maxsize=None)
def G_support(m: int) -> frozenset[int]:
    if m == 0:
        return frozenset({0})
    if m % 2 == 0:
        return frozenset(2 * e for e in G_support(m // 2))
    S = G_support(m // 2)
    out = {2 * j + 1 for j in S}
    cands = S | {x + 1 for x in S}
    for j in cands:
        if j < 0:
            continue
        if (j in S) ^ ((j - 1) in S):
            d = 2 * j
            if 0 <= d <= 2 * m:
                out.add(d)
    return frozenset(out)


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


def fires(row: int, p: int) -> int:
    return (((row << 1) & row) >> p) & 1


def census(k: int) -> dict[int, list[int]]:
    U = 1 << k
    target = 3 * U
    by_p: dict[int, list[int]] = defaultdict(list)
    for t in range(U, 3 * U):
        m = target - t - 1
        for d in G_support(m):
            p = target - d
            if 1 <= p <= 2 * t:
                by_p[p].append(t)
    return by_p


def N_ann(M: int, r: int) -> tuple[int, int, int]:
    W = (1 << (M + 1)) - 1
    ncone = (3 * (1 << M) + r - 3) // 2
    return min(W, ncone), W, ncone


def C_le(N: int, d: int) -> int:
    if N < 0:
        return 0
    return sum(G(n, d) for n in range(N + 1))


def window_N(k: int, r: int, M: int) -> int:
    U = 1 << k
    j = k - M
    if j < 0:
        return -1
    W = (2 << k) // (1 << j) - 1
    nmax = (3 * U + r * (1 << j) - 1) // (1 << (j + 1))
    return min(W, nmax - 1)


def family_p_times(k: int, r: int, M: int) -> tuple[int, list[int]] | None:
    if M > k:
        return None
    U = 1 << k
    j = k - M
    if j < 0:
        return None
    p = 3 * U + 1 - r * (1 << j)
    if p < 1:
        return None
    N = window_N(k, r, M)
    ts = []
    for n in range(max(0, N) + 1):
        if G(n, r - 1):
            t = 3 * U - (1 << j) * (n + 1)
            if 1 <= p <= 2 * t and U <= t < 3 * U:
                ts.append(t)
    ts.sort()
    return p, ts


def expected_bits(k: int, fam: list[tuple[int, int]]) -> list[int]:
    out = []
    for r, M in fam:
        if M > k:
            continue
        ft = family_p_times(k, r, M)
        if ft is not None:
            out.append(ft[0])
    return sorted(out)


def H(m: int) -> int:
    return sum(G(n, 2 * m) for n in range(m, 2 * m + 1))


def interval_ok() -> bool:
    if H(1) != 2 or H(2) != 2:
        return False
    if H(3) != 3 or H(6) != 3:
        return False
    if H(4) != 4 or H(7) != 4 or H(14) != 4:
        return False
    if H(5) != 5 or H(9) != 5 or H(15) != 5 or H(30) != 5:
        return False
    if [n for n in range(3, 7) if G(n, 6)] != [3, 5, 6]:
        return False
    if [n for n in range(6, 13) if G(n, 12)] != [6, 10, 12]:
        return False
    le5 = [m for m in range(1, 65) if H(m) <= 5]
    return le5 == [1, 2, 3, 4, 5, 6, 7, 9, 14, 15, 30]


def complementary_ok(mmax: int) -> bool:
    for m in range(8, mmax + 1):
        a = G(2 * m - 1, 2 * m)
        b = G(2 * m - 2, 2 * m)
        if a + b != 1:
            return False
        n2_cap = 3 * m // 2 + 1
        if n2_cap > 2 * m - 3:
            return False
        if H(m) < 4:
            return False
    return True


def G_diag_ok(nmax: int) -> bool:
    return all(G(n, n) == 1 for n in range(nmax + 1))


def ncone_dominates_d_ok() -> bool:
    for M in range(1, 12):
        for r in range(1, 3 * (1 << M) + 1, 2):
            _N, _W, ncone = N_ann(M, r)
            if r - 1 > ncone:
                return False
    return True


def C_le_eq(want: int, Mmax: int) -> list[tuple[int, int]]:
    found = []
    for M in range(0, Mmax + 1):
        for r in range(1, 3 * (1 << M) + 1, 2):
            N, _W, _nc = N_ann(M, r)
            if N < 0:
                continue
            if C_le(N, r - 1) == want:
                found.append((M, r))
    return found


def r1_surviving(k: int, j: int) -> int:
    U = 1 << k
    if j < 0:
        return 0
    p = 3 * U + 1 - (1 << j)
    if p < 1:
        return 0
    W = (2 << k) // (1 << j) - 1
    if W < 0:
        return 0
    nmax = (3 * U + (1 << j) - 1) // (1 << (j + 1))
    last = min(W, nmax - 1)
    return max(0, last + 1)


def lift_count(k: int, r: int, j: int) -> int:
    U = 1 << k
    p = 3 * U + 1 - r * (1 << j)
    if p < 1:
        return 0
    W = (2 << k) // (1 << j) - 1
    if W < 0:
        return 0
    nmax = (3 * U + r * (1 << j) - 1) // (1 << (j + 1))
    N = min(W, nmax - 1)
    return C_le(N, r - 1)


def negative_M_ok() -> bool:
    """j>k: only r=1, j=k+1 is unique; no doubles through pentuples."""
    for k in range(3, 8):
        if r1_surviving(k, k + 1) != 1:
            return False
        for j in range(k + 2, k + 5):
            if r1_surviving(k, j) != 0:
                return False
        for r in (3, 5, 7, 9, 11, 15, 17):
            for j in range(k + 1, k + 4):
                if lift_count(k, r, j) != 0:
                    return False
    return True


def r_bounds_ok() -> bool:
    """N=W even residues of Cycles AV–BA exceed rmax=3*2^M-1."""
    for M in range(2, 12):
        if (1 << (M + 2)) - 3 <= 3 * (1 << M) - 1:
            return False
    for M in range(4, 12):
        if (1 << (M + 2)) - 13 <= 3 * (1 << M) - 1:
            return False
    for M in range(6, 12):
        if (1 << (M + 2)) - 49 <= 3 * (1 << M) - 1:
            return False
    # M=3 even triples: only r=19,23 survive rmax=23
    a = 5
    rs = [(1 << a) - q + 1 for q in AX_Q]
    if sorted(r for r in rs if r <= 23) != [19, 23]:
        return False
    # M=5 even pentuples: only r=79,95 survive rmax=95
    a = 7
    rs = [(1 << a) - q + 1 for q in BA_Q]
    if sorted(r for r in rs if r <= 95) != [79, 95]:
        return False
    return True


def even_full_window_ok() -> bool:
    """N=W even C_le matches AW/AX/AZ/BA on small a=M+2."""
    # no even doubles for a>=4 (M>=2)
    for M in range(2, 7):
        W = (1 << (M + 1)) - 1
        ev = [D for D in range(0, 2 * W + 1, 2) if C_le(W, D) == 2]
        if ev:
            return False
    # even triples for a>=5 are 2^a - AX_Q
    for M in range(3, 7):
        a = M + 2
        W = (1 << (M + 1)) - 1
        ev = [D for D in range(0, 2 * W + 1, 2) if C_le(W, D) == 3]
        pred = sorted((1 << a) - q for q in AX_Q)
        if ev != pred:
            return False
    # no even quads for a>=6 (M>=4)
    for M in range(4, 7):
        W = (1 << (M + 1)) - 1
        ev = [D for D in range(0, 2 * W + 1, 2) if C_le(W, D) == 4]
        if ev:
            return False
    # even pentuples for a>=7 are 2^a - BA_Q
    for M in (5, 6):
        a = M + 2
        W = (1 << (M + 1)) - 1
        ev = [D for D in range(0, 2 * W + 1, 2) if C_le(W, D) == 5]
        pred = sorted((1 << a) - q for q in BA_Q)
        if ev != pred:
            return False
    return True


def truncated_small_d_ok() -> bool:
    """C_le thresholds for d=0,2,4 that kill extra truncated slots."""
    if [C_le(N, 0) for N in range(6)] != [1, 2, 3, 4, 5, 6]:
        return False
    c2 = [C_le(N, 2) for N in range(8)]
    if c2 != [0, 1, 2, 2, 2, 3, 4, 4]:
        return False
    c4 = [C_le(N, 4) for N in range(8)]
    if c4 != [0, 0, 1, 1, 2, 3, 3, 4]:
        return False
    # r=1 truncated N = 3*2^{M-1}-1, C_le=N+1 equals 1,2,3,4,5 only at small M
    for M in range(1, 8):
        N = 3 * (1 << (M - 1)) - 1
        cnt = N + 1
        if M == 1 and cnt != 3:
            return False
        if M >= 2 and cnt < 6:
            return False
    return True


def firing_xor_ok(kmax: int) -> dict:
    rows = evolve_rows(3 * (1 << kmax))
    xor_u, xor_d, xor_t, xor_q, xor_p = [], [], [], [], []
    theta = []
    n_pent = []
    for k in range(3, kmax + 1):
        U = 1 << k

        def xor_fam(fam, want_len):
            x = 0
            nbits = 0
            for r, M in fam:
                if M > k:
                    continue
                ft = family_p_times(k, r, M)
                if ft is None or len(ft[1]) != want_len:
                    return None
                p, ts = ft
                nbits += 1
                for t in ts:
                    x ^= fires(rows[t], p)
            return x, nbits

        u = xor_fam(UNIQ, 1)
        d = xor_fam(DBL, 2)
        t = xor_fam(TRI, 3)
        q = xor_fam(QUAD, 4)
        p5 = xor_fam(PENT, 5)
        if None in (u, d, t, q, p5):
            return {"ok": False}
        xor_u.append(u[0])
        xor_d.append(d[0])
        xor_t.append(t[0])
        xor_q.append(q[0])
        xor_p.append(p5[0])
        n_pent.append(p5[1])
        theta.append(((rows[3 * U] >> (3 * U)) & 1) ^ ((rows[U] >> U) & 1))
    odd = [xor_u[i] ^ xor_t[i] ^ xor_p[i] for i in range(len(theta))]
    return {
        "ok": True,
        "xor_u": xor_u,
        "xor_d": xor_d,
        "xor_t": xor_t,
        "xor_q": xor_q,
        "xor_p": xor_p,
        "theta": theta,
        "odd": odd,
        "n_pent": n_pent,
        "u_both": set(xor_u) == {0, 1},
        "d_both": set(xor_d) == {0, 1},
        "t_both": set(xor_t) == {0, 1},
        "q_both": set(xor_q) == {0, 1},
        "p_both": set(xor_p) == {0, 1},
        "odd_is_theta": odd == theta,
    }


def n_pent_for(k: int) -> int:
    if k <= 3:
        return 2
    if k == 4:
        return 6
    return 8


def self_checks(
    c20,
    interval: bool,
    comp: bool,
    diag: bool,
    ncone: bool,
    negM: bool,
    rb: bool,
    evenW: bool,
    trunc: bool,
    found: dict[int, list],
    recs: list[dict],
    fire: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert interval and comp and diag and ncone and negM and rb and evenW and trunc
    assert found[1] == [(0, 1), (0, 3), (1, 5)]
    assert found[2] == [(1, 3)]
    assert found[3] == [(1, 1), (2, 9), (2, 11), (3, 19), (3, 23)]
    assert found[4] == [(2, 3), (2, 5), (2, 7), (3, 15)]
    assert found[5] == [
        (3, 17),
        (3, 21),
        (4, 37),
        (4, 39),
        (4, 45),
        (4, 47),
        (5, 79),
        (5, 95),
    ]
    for rec in recs:
        k = rec["k"]
        U = 1 << k
        assert rec["uniq"] == sorted([1, (U >> 1) + 1, U + 1, 2 * U + 1])
        assert rec["dbl"] == [3 * (U >> 1) + 1]
        assert rec["n1"] == 4 and rec["n2"] == 1 and rec["n3"] == 5 and rec["n4"] == 4
        assert rec["n5"] == n_pent_for(k)
        assert rec["times_ok"]
        assert rec["uniq"] == rec["lift1"]
        assert rec["dbl"] == rec["lift2"]
        assert rec["tri"] == rec["lift3"]
        assert rec["quad"] == rec["lift4"]
        assert rec["pent"] == rec["lift5"]
    assert fire["ok"]
    assert fire["u_both"] and fire["d_both"] and fire["t_both"]
    assert fire["q_both"] and fire["p_both"]
    assert not fire["odd_is_theta"]
    assert fire["n_pent"] == [n_pent_for(k) for k in range(3, 10)]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    interval = interval_ok()
    comp = complementary_ok(64)
    diag = G_diag_ok(128)
    ncone = ncone_dominates_d_ok()
    negM = negative_M_ok()
    rb = r_bounds_ok()
    evenW = even_full_window_ok()
    trunc = truncated_small_d_ok()
    found = {w: C_le_eq(w, 8 if w <= 4 else 7) for w in (1, 2, 3, 4, 5)}
    recs = []
    for k in range(3, 8):
        by = census(k)
        buckets = {n: sorted(p for p, ts in by.items() if len(ts) == n) for n in (1, 2, 3, 4, 5)}
        lifts = {
            1: expected_bits(k, UNIQ),
            2: expected_bits(k, DBL),
            3: expected_bits(k, TRI),
            4: expected_bits(k, QUAD),
            5: expected_bits(k, PENT),
        }
        times_ok = True
        for fam, want in ((UNIQ, 1), (DBL, 2), (TRI, 3), (QUAD, 4), (PENT, 5)):
            for r, M in fam:
                if M > k:
                    continue
                ft = family_p_times(k, r, M)
                if ft is None or len(ft[1]) != want:
                    times_ok = False
                    continue
                if by.get(ft[0], []) != ft[1]:
                    times_ok = False
        recs.append({
            "k": k,
            "n1": len(buckets[1]),
            "n2": len(buckets[2]),
            "n3": len(buckets[3]),
            "n4": len(buckets[4]),
            "n5": len(buckets[5]),
            "uniq": buckets[1],
            "dbl": buckets[2],
            "tri": buckets[3],
            "quad": buckets[4],
            "pent": buckets[5],
            "lift1": lifts[1],
            "lift2": lifts[2],
            "lift3": lifts[3],
            "lift4": lifts[4],
            "lift5": lifts[5],
            "times_ok": times_ok,
        })
    fire = firing_xor_ok(9)
    checks = self_checks(
        c20, interval, comp, diag, ncone, negM, rb, evenW, trunc, found, recs, fire
    )
    dump = {
        "cycle": "BL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": [
            {key: rec[key] for key in ("k", "n1", "n2", "n3", "n4", "n5", "times_ok")}
            for rec in recs
        ],
        "C_le_Mge0": {str(w): found[w] for w in (1, 2, 3, 4, 5)},
        "firing": {
            "xor_u": fire["xor_u"],
            "xor_d": fire["xor_d"],
            "xor_t": fire["xor_t"],
            "xor_q": fire["xor_q"],
            "xor_p": fire["xor_p"],
            "odd": fire["odd"],
            "theta": fire["theta"],
        },
        "lemmas": {
            "exactly_four_unique_q3": True,
            "exactly_one_double_q3": True,
            "exactly_five_triples_q3": True,
            "exactly_four_quads_q3": True,
            "exactly_eight_pentuples_q3": True,
            "classified_always_fire": False,
            "odd_xor_is_theta": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "exactly_four_unique_q3": "LEMMA",
            "exactly_one_double_q3": "LEMMA",
            "exactly_five_triples_q3": "LEMMA",
            "exactly_four_quads_q3": "LEMMA",
            "exactly_eight_pentuples_q3": "LEMMA",
            "classified_always_fire": "KILLED",
            "odd_xor_is_theta": "KILLED",
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
    print("annulus", dump["annulus"])
    print("C_le", dump["C_le_Mge0"])


if __name__ == "__main__":
    main()
