#!/usr/bin/env python3
"""Cycle AL: all-q spines; edges cancel; leftmost-11 parity is 1 XOR wt(q).

For every integer q>=1 and U=2^k, Freshman factorisation gives
(1+x+x^2)^{(q-1)U}=Q_{q-1}(x^U). Only the three indices i in {q-2,q-1,q}
land in packed bits [0,2U]. The centre coefficient is G(q-1,q-1)=1. The
two edges have coefficient G(q-1,q)=G(q-1,q-2)=v_2(q) mod 2, so they
cancel (both 0 or both 1). Hence

    c_{q U} = c_U XOR J_{[U, qU) -> qU},

i.e. phi^{(q)}_k := c_{q U} XOR c_U equals that Green remainder, for
every q, not only Fermat-odd q=2^a+1. Cycle Z is q=2; Cycle AJ/AK are
the Fermat-odd cases. For odd q, low-bits-first chaining of Cycle AI
has extras strictly outside the cone at every step.

The XOR of leftmost-11 Green hits on [U, qU) is independent of k and
equals 1 XOR popcount(q) (mod 2). So phi^{(q)}_k = P(q) XOR S^{(q)}_k
with P(q)=1 XOR wt(q). Fermat-odd q have even weight, recovering Cycle
AK's forced 1; q=7 has P=0, so odd p=1 parity is not a general-q
production. Period 2^m forces phi^{(q)}_k=0 for every q.

Not a prize claim: some phi=1 infinitely often remains open.

Run: python3 research/cycle_al.py --certify
Dump: research/cycle_al.json
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


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 of non-positive")
    return (n & -n).bit_length() - 1


def popcount(n: int) -> int:
    return n.bit_count()


def P_pop(q: int) -> int:
    """Leftmost-11 hit parity: 1 XOR popcount(q) mod 2."""
    return (popcount(q) & 1) ^ 1


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


def and_J_p1(rows: list[int], t0: int, t1: int, target_t: int) -> tuple[int, int]:
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


def xor_G_prefix(M: int, D: int) -> int:
    acc = 0
    for m in range(M):
        acc ^= G(m, D)
    return acc


def near_diag_ok(mmax: int) -> bool:
    for m in range(0, mmax + 1):
        if G(m, m) != 1:
            return False
        want = v2(m + 1) & 1
        if G(m, m + 1) != want:
            return False
        if m >= 1 and G(m, m - 1) != want:
            return False
    return True


def P_recurrence_ok(qmax: int) -> bool:
    P = [0] * (qmax + 1)
    P[1] = 0
    for q in range(2, qmax + 1):
        if q % 2 == 0:
            P[q] = P[q // 2]
        else:
            P[q] = P[(q - 1) // 2] ^ 1
        if P[q] != P_pop(q):
            return False
        if xor_G_prefix(q - 1, q - 1) != P[q]:
            return False
    return True


def P_independent_of_k(qmax: int, kmax: int) -> bool:
    for q in range(1, qmax + 1):
        want = P_pop(q)
        for k in range(0, kmax + 1):
            U = 1 << k
            if xor_G_prefix((q - 1) * U, q * U - 1) != want:
                return False
    return True


def extras_chain(q: int, k: int) -> list[dict]:
    """Low-bits-first Cycle-AI chain from U to qU."""
    U = 1 << k
    t = U
    recs = []
    bits = q - 1
    j = 0
    while bits:
        if bits & 1:
            step = (1 << j) * U
            recs.append({
                "t": t,
                "step": step,
                "strictly_outside": step > t,
            })
            t += step
        bits >>= 1
        j += 1
    if t != q * U:
        recs.append({"t": t, "expected": q * U, "mismatch": True})
    return recs


def extras_odd_q_outside(qmax: int, kmax: int) -> dict:
    all_out = True
    n = 0
    even_inside = False
    for q in range(3, qmax + 1, 2):
        for k in range(0, kmax + 1):
            recs = extras_chain(q, k)
            n += 1
            if not all(r.get("strictly_outside") for r in recs):
                all_out = False
    # q=2: extras sit on the cone (Cycle Z)
    rec2 = extras_chain(2, 3)
    if rec2 and rec2[0]["strictly_outside"]:
        even_inside = True
    return {
        "odd_all_outside": all_out,
        "n": n,
        "q2_on_cone": (not rec2[0]["strictly_outside"]) and not even_inside,
    }


def synthetic_all_phi_zero() -> dict:
    T = 5
    recs = []
    all_ok = True
    qs = list(range(1, 13))
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


def self_checks(
    c20,
    diag_ok: bool,
    prec_ok: bool,
    pind_ok: bool,
    ident_fail: int,
    lin_fail: int,
    p1_fail: int,
    extras: dict,
    synth: dict,
    not_all1: bool,
    q7_p1_zero: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert diag_ok and prec_ok and pind_ok
    assert ident_fail == 0 and lin_fail == 0 and p1_fail == 0
    assert extras["odd_all_outside"] and extras["q2_on_cone"]
    assert synth["all_ok"]
    assert not_all1 and q7_p1_zero
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    diag_ok = near_diag_ok(80)
    prec_ok = P_recurrence_ok(80)
    pind_ok = P_independent_of_k(20, 5)
    extras = extras_odd_q_outside(31, 4)
    synth = synthetic_all_phi_zero()

    qs = list(range(1, 13))
    kmax = 6
    rows = evolve_rows(max(qs) * (1 << kmax) + 2)
    ident_fail = 0
    lin_fail = 0
    p1_fail = 0
    phis: dict[int, list[int]] = {q: [] for q in qs}
    p1s: dict[int, list[int]] = {q: [] for q in qs}
    for q in qs:
        edge = v2(q) & 1
        want_p1 = P_pop(q)
        for k in range(0, kmax + 1):
            U = 1 << k
            t1 = q * U
            J, p1 = and_J_p1(rows, U, t1, t1)
            cU = spatial(rows[U], U, 0)
            cq = spatial(rows[t1], t1, 0)
            phi = cq ^ cU
            left = spatial(rows[U], U, -U)
            right = spatial(rows[U], U, U)
            lin = (edge & left) ^ cU ^ (edge & right)
            phis[q].append(phi)
            p1s[q].append(p1)
            if J != phi:
                ident_fail += 1
            if lin != cU:
                lin_fail += 1
            if p1 != want_p1:
                p1_fail += 1

    even_wt = [q for q in qs if P_pop(q) == 1]
    not_all1 = any(0 in phis[q] and 1 in phis[q] for q in even_wt)
    q7_p1_zero = all(x == 0 for x in p1s.get(7, [1])) if 7 in p1s else True
    # q=7 is outside qs=1..12; compute a short p1 row for q=7
    p1_q7 = []
    for k in range(0, 5):
        U = 1 << k
        t1 = 7 * U
        _, p1 = and_J_p1(rows, U, t1, t1)
        p1_q7.append(p1)
    q7_p1_zero = all(x == 0 for x in p1_q7)

    checks = self_checks(
        c20, diag_ok, prec_ok, pind_ok, ident_fail, lin_fail, p1_fail,
        extras, synth, not_all1, q7_p1_zero,
    )
    dump = {
        "cycle": "AL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "G_near_diag_ok": diag_ok,
        "P_recurrence_and_popcount_ok": prec_ok,
        "P_independent_of_k_ok": pind_ok,
        "identity_fail": ident_fail,
        "linear_image_fail": lin_fail,
        "p1_fail": p1_fail,
        "phi": {str(q): phis[q] for q in qs},
        "p1": {str(q): p1s[q] for q in qs},
        "p1_q7": p1_q7,
        "P_pop": {str(q): P_pop(q) for q in list(range(1, 17))},
        "extras": extras,
        "synthetic": synth,
        "lemmas": {
            "all_q_identity": True,
            "edges_cancel": True,
            "P_eq_1_xor_popcount": True,
            "period_2m_forces_all_integer_phi_0": True,
            "odd_q_extras_outside": True,
            "p1_odd_for_every_odd_q": False,
            "some_phi_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "all_q_identity": "LEMMA",
            "edges_cancel": "LEMMA",
            "P_eq_1_xor_popcount": "LEMMA",
            "period_2m_forces_all_integer_phi_0": "LEMMA",
            "odd_q_extras_outside": "LEMMA",
            "p1_odd_for_every_odd_q": "KILLED",
            "S_identically_0_even_weight": "KILLED",
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
