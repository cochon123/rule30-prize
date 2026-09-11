#!/usr/bin/env python3
"""Cycle AO: two-point congruence for G(m, 3*2^k-1); unique leftmost-11 hits.

G(m, 3*2^k-1)=1 iff m ≡ 2^{k+1}-1 or 3*2^k-1 (mod 2^{k+2}). In the
3-fold annulus only the first residue appears, so θ_k has a unique
packed-bit-1 Green hit, at time t=2^k. The count N(q) of such hits on
[2^k, q 2^k) is independent of k and equals #{m<=q-2: G(m,q-1)=1};
its parity is Cycle AL's P(q). N(5)=1 locates the unique q=5 hit at
t=2^{k+1}. The two-point family p=3(2^k-2^j)+1 is bulk but its XOR is
not a formula for θ_k.

Not a prize claim: θ_k=1 infinitely often remains open.

Run: python3 research/cycle_ao.py --certify
Dump: research/cycle_ao.json
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


def two_point_pred(m: int, k: int) -> int:
    mod = 1 << (k + 2)
    r1 = (1 << (k + 1)) - 1
    r2 = 3 * (1 << k) - 1
    return int(m % mod in (r1 % mod, r2 % mod))


def congruence_ok(kmax: int, m_mult: int) -> bool:
    for k in range(0, kmax + 1):
        D = 3 * (1 << k) - 1
        mlim = m_mult * (1 << k)
        for m in range(0, mlim + 1):
            if G(m, D) != two_point_pred(m, k):
                return False
    return True


def N0(q: int) -> int:
    D = q - 1
    return sum(G(m, D) for m in range(0, q - 1))


def N_k(q: int, k: int) -> int:
    U = 1 << k
    D = q * U - 1
    mmax = (q - 1) * U - 1
    return sum(1 for m in range(0, mmax + 1) if G(m, D))


def N_independent_ok(qmax: int, kmax: int) -> tuple[bool, dict]:
    table = {}
    ok = True
    for q in range(2, qmax + 1):
        n0 = N0(q)
        table[q] = n0
        if (n0 & 1) != (1 ^ (bin(q).count("1") & 1)):
            ok = False
        for k in range(0, kmax + 1):
            if N_k(q, k) != n0:
                ok = False
    return ok, table


def p1_hits(rows: list[int], q: int, k: int) -> tuple[int, int, list[int]]:
    U = 1 << k
    n1 = xor1 = 0
    times = []
    for t in range(U, q * U):
        A = (rows[t] << 1) & rows[t]
        if (A >> 1) & 1 and G(q * U - t - 1, q * U - 1):
            n1 += 1
            xor1 ^= 1
            times.append(t)
    return n1, xor1, times


def family_xor(rows: list[int], k: int) -> int:
    U = 1 << k
    acc = 0
    for j in range(0, k + 1):
        p = 3 * (U - (1 << j)) + 1
        xor = 0
        for m in ((1 << (j + 1)) - 1, 3 * (1 << j) - 1):
            t = 3 * U - m - 1
            if U <= t < 3 * U:
                A = (rows[t] << 1) & rows[t]
                xor ^= (A >> p) & 1
        acc ^= xor
    return acc


def self_checks(
    c20,
    cong: bool,
    n_ok: bool,
    ntable: dict,
    recs: list[dict],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cong
    assert n_ok
    assert ntable[3] == 1 and ntable[5] == 1
    assert ntable[7] == 2 and ntable[9] == 3
    fam = []
    for rec in recs:
        assert rec["n1_q3"] == 1 and rec["xor1_q3"] == 1
        assert rec["t_q3"] == (1 << rec["k"])
        if "n1_q5" in rec:
            assert rec["n1_q5"] == 1 and rec["xor1_q5"] == 1
            assert rec["t_q5"] == (1 << (rec["k"] + 1))
        fam.append(rec["family_xor"])
    assert 0 in fam and 1 in fam, "two-point family XOR is not a formula for theta"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cong = congruence_ok(8, 16)
    n_ok, ntable = N_independent_ok(16, 6)
    kmax = 9
    rows = evolve_rows(3 * (1 << kmax))
    recs = []
    for k in range(1, kmax + 1):
        n1, xor1, times = p1_hits(rows, 3, k)
        rec = {
            "k": k,
            "n1_q3": n1,
            "xor1_q3": xor1,
            "t_q3": times[0] if times else None,
            "family_xor": family_xor(rows, k),
            "theta": ((rows[3 << k] >> (3 << k)) & 1)
            ^ ((rows[1 << k] >> (1 << k)) & 1),
        }
        if 5 * (1 << k) < len(rows):
            n5, x5, t5 = p1_hits(rows, 5, k)
            rec["n1_q5"] = n5
            rec["xor1_q5"] = x5
            rec["t_q5"] = t5[0] if t5 else None
        recs.append(rec)
    checks = self_checks(c20, cong, n_ok, ntable, recs)
    dump = {
        "cycle": "AO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "N_q": {str(q): ntable[q] for q in range(2, 17)},
        "annulus": recs,
        "lemmas": {
            "two_point_congruence": True,
            "unique_p1_q3": True,
            "N_q_independent_of_k": True,
            "unique_p1_q5_at_2U": True,
            "family_xor_formula_for_theta": False,
            "theta_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "two_point_congruence": "LEMMA",
            "unique_p1_q3": "LEMMA",
            "N_q_independent_of_k": "LEMMA",
            "unique_p1_q5_at_2U": "LEMMA",
            "family_xor_formula_for_theta": "KILLED",
            "theta_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("N_q", dump["N_q"])
    print("annulus", [
        {key: rec[key] for key in rec if key != "t_q3" or True}
        for rec in recs
    ])


if __name__ == "__main__":
    main()
