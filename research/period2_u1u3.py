#!/usr/bin/env python3
"""F_k = A_k XOR u_1 u_3 C_k for every k>=8.

On a phase-01 period-2 centre, G_k is independent of u_1 for k>=8
(period2_gsilent). F_8 = u_1 u_3, and F_7 has no u_1. The fold
F_k = G_{k-1} XOR (F_{k-1} OR F_{k-2}) preserves the factorisation:
the u_1-part of an OR of two such polynomials is again a multiple of
u_3. Hence every monomial of F_k that contains u_1 also contains u_3.
On the slice u_3=0, F_k is independent of u_1 for k>=8, so extra,
kind, and stop of a ugap onset T>=8 are unchanged by flipping u_1.
This does not bound extra: the u_3=1 slice still sees u_1. Not a
prize claim.

Run: python3 research/period2_u1u3.py --certify
Dump: research/period2_u1u3.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import force
from period2_left_edge import anf_str, anf_vars, compute_columns
from period2_ugap_sat import ugap_ok, ugap_strings
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def fib_ok(u):
    return all(a + b < 2 for a, b in zip(u, u[1:]))


def flip_u1(u):
    v = list(u)
    v[1] = 1 - v[1]
    return v


def u1_without_u3(p: int) -> bool:
    """True if some monomial of p contains u_1 but not u_3."""
    m = 0
    pp = p
    while pp:
        if (pp & 1) and ((m >> 1) & 1) and not ((m >> 3) & 1):
            return True
        pp >>= 1
        m += 1
    return False


def certify_anf(kmax: int = 20):
    F, G = compute_columns(kmax, reduce=True)
    rows = []
    for k in range(0, kmax + 1):
        rec = {
            "k": k,
            "F_vars": anf_vars(F[k]),
            "G_vars": anf_vars(G[k]),
            "F_u1_without_u3": u1_without_u3(F[k]),
            "G_u1_without_u3": u1_without_u3(G[k]),
        }
        rows.append(rec)
        if k >= 8:
            assert not rec["F_u1_without_u3"], rec
            assert 1 not in rec["G_vars"], rec
    assert anf_str(F[8]) == "u1*u3"
    assert 1 not in anf_vars(F[7])
    assert u1_without_u3(F[5])  # F_5=1+u1+u2, not this identity
    return {
        "kmax": kmax,
        "ok": True,
        "rows": rows,
        "F7": anf_str(F[7]),
        "F8": anf_str(F[8]),
        "F5": anf_str(F[5]),
    }


def certify_slice(Tmin=8, Tmax=28):
    n_on = 0
    n_legal = 0
    n_match = 0
    n_F_same = 0
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        if n0 < 4:
            continue
        kneed = max(T + 2, 2 * n0 + 2)
        for u in ugap_strings(n0):
            if u[3] != 0:
                continue
            Fu, _ = F_of_u(u, kneed)
            if Fu[T] != 1:
                continue
            n_on += 1
            v = flip_u1(u)
            if not (fib_ok(v) and ugap_ok(v)):
                continue
            n_legal += 1
            Fv, _ = F_of_u(v, kneed)
            for k in range(8, min(len(Fu), len(Fv))):
                assert Fu[k] == Fv[k]
            n_F_same += 1
            r1 = force(u, T)
            r2 = force(v, T)
            assert r1 is not None and r2 is not None
            assert r1["extra"] == r2["extra"]
            assert r1["kind"] == r2["kind"]
            assert r1["stop"] == r2["stop"]
            n_match += 1
    assert n_legal > 0
    assert n_match == n_legal
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_onset_u3_zero": n_on,
        "n_legal_flip": n_legal,
        "n_F_k_ge_8_same": n_F_same,
        "n_extra_match": n_match,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    anf = certify_anf(20)
    checks["F_k_u1_implies_u3_k_ge_8"] = True
    checks["F8_is_u1_u3"] = True
    checks["F7_no_u1"] = True
    checks["F5_has_u1_without_u3"] = True
    sl = certify_slice(8, 28)
    checks["u3_zero_F_independent_of_u1"] = True
    checks["u3_zero_extra_kind_stop_match"] = True
    return {
        "checks": checks,
        "anf": {k: anf[k] for k in ("kmax", "ok", "F7", "F8", "F5")},
        "anf_support": [
            {
                "k": r["k"],
                "F_vars": r["F_vars"],
                "F_u1_without_u3": r["F_u1_without_u3"],
            }
            for r in anf["rows"]
            if 5 <= r["k"] <= 10
        ],
        "slice": sl,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("anf", report["anf"])
    print("anf_support", report["anf_support"])
    print("slice", report["slice"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
