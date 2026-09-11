#!/usr/bin/env python3
"""Cycle AJ: theta_k = c_{3*2^k} XOR c_{2^k}; leftmost 11 hits it.

AI's dyadic step from t=2^k by 2^{k+1} has both extras outside the cone, so

    theta_k := c_{3*2^k} XOR c_{2^k}

equals the Green AND remainder on [2^k, 3*2^k) targeting time 3*2^k.
Eventual period 2^m forces theta_k = 0 (both indices are 0 mod 2^m).
The leftmost 11 at time 2^k always Green-hits this remainder
(G(2^{k+1}-1, 3*2^k-1)=1 by induction), so theta_k = 1 XOR S_k.
Infinitely many theta_k=1 would kill every power-of-2 period even if
I_k vanishes. S_k is not identically 0.

Not a prize claim: theta=1 i.o. and I_k not eventually 0 remain open.

Run: python3 research/cycle_aj.py --certify
Dump: research/cycle_aj.json
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


def and_hits(rows: list[int], t0: int, t1: int, target_t: int) -> dict:
    acc = 0
    n_cr = 0
    n_other = 0
    n_p1 = 0
    n_cr_bits = 0
    for s in range(t0, t1):
        A = (rows[s] << 1) & rows[s]
        c = spatial(rows[s], s, 0)
        r = spatial(rows[s], s, 1)
        n_cr_bits += c & r
        delta = target_t - s - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(delta, target_t - p):
                acc ^= 1
                if p == s + 1:
                    n_cr += 1
                else:
                    n_other += 1
                if p == 1:
                    n_p1 += 1
            tmp >>= 1
            p += 1
    return {
        "J": acc,
        "n_cr_hits": n_cr,
        "n_other": n_other,
        "n_p1": n_p1,
        "n_cr_bits": n_cr_bits,
    }


def coboundary(rows: list[int], t0: int, t1: int) -> dict:
    acc_d = 0
    acc_cr = 0
    for s in range(t0, t1):
        ell = spatial(rows[s], s, -1)
        c = spatial(rows[s], s, 0)
        r = spatial(rows[s], s, 1)
        acc_d ^= ell ^ r
        acc_cr ^= c & r
    th = spatial(rows[t0], t0, 0) ^ spatial(rows[t1], t1, 0)
    return {"theta": th, "xor_d": acc_d, "xor_cr": acc_cr, "ok": th == (acc_d ^ acc_cr)}


def G_leftmost_hits(kmax: int) -> bool:
    """G(2^{k+1}-1, 3*2^k-1)=1 by the odd doubling G(2m+1,2j+1)=G(m,j)."""
    for k in range(0, kmax + 1):
        if G((1 << (k + 1)) - 1, 3 * (1 << k) - 1) != 1:
            return False
    return True


def synthetic_theta_vanishes() -> dict:
    T = 5
    recs = []
    all_ok = True
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
        for k in range(k0, 12):
            U = 1 << k
            if 3 * U >= N:
                break
            n += 1
            if c[3 * U] ^ c[U]:
                ok = False
        if not ok:
            all_ok = False
        recs.append({"m": m, "p": p, "k0": k0, "n": n, "ok": ok})
    return {"all_ok": all_ok, "rows": recs}


def self_checks(c20, g_ok: bool, ident_fail: int, cob_fail: int, cr_mismatch: int,
                p1_ok: bool, synth: dict, theta: list[int], not_all1: bool,
                formula_kills: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert g_ok
    assert ident_fail == 0
    assert cob_fail == 0
    assert cr_mismatch == 0
    assert p1_ok
    assert synth["all_ok"]
    assert not_all1
    assert formula_kills["I"] and formula_kills["xor_d"] and formula_kills["xor_cr"]
    assert formula_kills["last_not_only_other"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    g_ok = G_leftmost_hits(16)
    synth = synthetic_theta_vanishes()

    kmax = 8
    rows = evolve_rows(3 * (1 << kmax) + 2)
    ident_fail = 0
    cob_fail = 0
    cr_mismatch = 0
    p1_ok = True
    theta = []
    recs = []
    xor_d_eq = []
    xor_cr_eq = []
    I_eq = []
    b = []
    for k in range(0, kmax + 1):
        U = 1 << k
        bk = spatial(rows[U], U, 0)
        ak = spatial(rows[3 * U], 3 * U, 0)
        th = ak ^ bk
        b.append(bk)
        theta.append(th)
        hits = and_hits(rows, U, 3 * U, 3 * U)
        if hits["J"] != th:
            ident_fail += 1
        cob = coboundary(rows, U, 3 * U)
        if not cob["ok"] or cob["theta"] != th:
            cob_fail += 1
        if hits["n_cr_hits"] != hits["n_cr_bits"]:
            cr_mismatch += 1
        if hits["n_p1"] < 1:
            p1_ok = False
        xor_d_eq.append(cob["xor_d"] == th)
        xor_cr_eq.append(cob["xor_cr"] == th)
        recs.append({
            "k": k,
            "theta": th,
            "n_cr": hits["n_cr_hits"],
            "n_other": hits["n_other"],
            "n_p1": hits["n_p1"],
            "xor_d": cob["xor_d"],
            "xor_cr": cob["xor_cr"],
        })
    I = [b[k] ^ b[k - 1] for k in range(1, len(b))]
    I_eq = [I[k] == theta[k] for k in range(min(len(I), len(theta)))]
    not_all1 = 0 in theta
    formula_kills = {
        "I": not all(I_eq),
        "xor_d": not all(xor_d_eq),
        "xor_cr": not all(xor_cr_eq),
        "last_not_only_other": any(r["n_other"] > 1 for r in recs),
    }
    checks = self_checks(
        c20, g_ok, ident_fail, cob_fail, cr_mismatch, p1_ok, synth,
        theta, not_all1, formula_kills,
    )
    dump = {
        "cycle": "AJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "G_leftmost": g_ok,
        "identity_fail": ident_fail,
        "coboundary_fail": cob_fail,
        "cr_hit_mismatch": cr_mismatch,
        "p1_always_hits": p1_ok,
        "theta": theta,
        "I": I,
        "synthetic": synth,
        "formula_kills": formula_kills,
        "rows": recs,
        "lemmas": {
            "theta_equals_J": True,
            "period_2m_forces_theta_0": True,
            "leftmost_11_hits_theta": True,
            "theta_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "theta_J_identity": "LEMMA",
            "period_2m_forces_theta_0": "LEMMA",
            "leftmost_11_hits": "LEMMA",
            "S_identically_0_or_local_formula": "KILLED",
            "theta_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"], "theta", theta)


if __name__ == "__main__":
    main()
