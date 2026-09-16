#!/usr/bin/env python3
"""G_k = D_k XOR u_2 u_4 E_k for every k>=9.

On a phase-01 period-2 centre, F_j = A XOR u_1 u_3 C for j>=8
(period2_u1u3), so S F_j = S A XOR u_2 u_4 (S C). G_8 has no u_2 and
G_8 OR G_7 = 1, hence G_9 = S F_8 XOR 1 = 1 + u_2 u_4. The OR of two
polynomials of the form D XOR u_2 u_4 E stays in that form, so every
later G_k has it. On the slice u_4=0, G_k is independent of u_2 for
k>=9. F still has a linear u_2 (F_10 = u_2+u_4+u_2 u_4), so extra is
not invariant under flipping u_2. Not a prize claim.

Run: python3 research/period2_gu2u4.py --certify
Dump: research/period2_gu2u4.json
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


def flip_u2(u):
    v = list(u)
    v[2] = 1 - v[2]
    return v


def u2_without_u4(p: int) -> bool:
    m = 0
    pp = p
    while pp:
        if (pp & 1) and ((m >> 2) & 1) and not ((m >> 4) & 1):
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
            "G_vars": anf_vars(G[k]),
            "F_vars": anf_vars(F[k]),
            "G_u2_without_u4": u2_without_u4(G[k]),
            "F_u2_without_u4": u2_without_u4(F[k]),
        }
        rows.append(rec)
        if k >= 8:
            assert not rec["G_u2_without_u4"], rec
    assert 2 not in anf_vars(G[8])
    assert anf_str(G[9]) == "1 + u2*u4"
    assert u2_without_u4(G[4])  # G_4=u2, identity does not start earlier
    assert u2_without_u4(F[10])  # F keeps a linear u_2
    return {
        "kmax": kmax,
        "ok": True,
        "rows": rows,
        "G8": anf_str(G[8]),
        "G9": anf_str(G[9]),
        "G4": anf_str(G[4]),
        "F10": anf_str(F[10]),
    }


def certify_slice_G(kmin=9, kmax=16, nlen=8):
    n_words = 0
    n_fib_flip = 0
    n_match = 0
    for u in ugap_strings(nlen):
        n_words += 1
        if u[4] != 0:
            continue
        v = flip_u2(u)
        if not fib_ok(v):
            continue
        n_fib_flip += 1
        _, Gu = F_of_u(u, kmax)
        _, Gv = F_of_u(v, kmax)
        for k in range(kmin, kmax + 1):
            assert Gu[k] == Gv[k]
        n_match += 1
    assert n_fib_flip > 0
    return {
        "nlen": nlen,
        "kmin": kmin,
        "kmax": kmax,
        "n_words": n_words,
        "n_u4_zero_fib_flip": n_fib_flip,
        "n_G_match": n_match,
        "ok": True,
    }


def certify_extra_not_invariant(Tmin=9, Tmax=20):
    n_on = 0
    n_legal = 0
    n_match = 0
    n_mismatch = 0
    sample = None
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        if n0 < 5:
            continue
        kneed = max(T + 2, 2 * n0 + 2)
        for u in ugap_strings(n0):
            if u[4] != 0:
                continue
            Fu, _ = F_of_u(u, kneed)
            if Fu[T] != 1:
                continue
            n_on += 1
            v = flip_u2(u)
            if not (fib_ok(v) and ugap_ok(v)):
                continue
            n_legal += 1
            r1 = force(u, T)
            r2 = force(v, T)
            if (
                r1 is not None
                and r2 is not None
                and r1["extra"] == r2["extra"]
                and r1["kind"] == r2["kind"]
                and r1["stop"] == r2["stop"]
            ):
                n_match += 1
            else:
                n_mismatch += 1
                if sample is None:
                    sample = {"T": T, "u": "".join(map(str, u))}
    assert n_mismatch > 0
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_onset_u4_zero": n_on,
        "n_legal_flip": n_legal,
        "n_extra_match": n_match,
        "n_extra_mismatch": n_mismatch,
        "sample_mismatch": sample,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    anf = certify_anf(20)
    checks["G_u2_implies_u4_k_ge_8"] = True
    checks["G8_no_u2"] = True
    checks["G9_is_1_plus_u2_u4"] = True
    checks["G4_has_u2_without_u4"] = True
    checks["F10_has_linear_u2"] = True
    sl = certify_slice_G()
    checks["u4_zero_G_independent_of_u2"] = True
    extra = certify_extra_not_invariant()
    checks["extra_not_invariant_under_u2_flip"] = True
    return {
        "checks": checks,
        "anf": {k: anf[k] for k in ("kmax", "ok", "G8", "G9", "G4", "F10")},
        "anf_support": [
            {
                "k": r["k"],
                "G_vars": r["G_vars"],
                "G_u2_without_u4": r["G_u2_without_u4"],
            }
            for r in anf["rows"]
            if 4 <= r["k"] <= 12
        ],
        "slice": sl,
        "extra_not_invariant": extra,
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
    print(
        "extra_not_invariant",
        {
            k: report["extra_not_invariant"][k]
            for k in (
                "n_onset_u4_zero",
                "n_legal_flip",
                "n_extra_match",
                "n_extra_mismatch",
            )
        },
    )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
