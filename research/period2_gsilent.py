#!/usr/bin/env python3
"""u_1 is absent from G_k for every k>=8.

On a phase-01 period-2 centre, silent u_0 means F_j has no u_0 for
j>=3, so S F_{k-1} has no u_1 for k>=4. Thus G_k = S F_{k-1} XOR
(G_{k-1} OR G_{k-2}) can contain u_1 only through the OR. On the
Fibonacci ring G_6 OR G_7 = 1, hence G_8 = S F_7 XOR 1 = u_3+u_4;
G_7 OR G_8 = 1, hence G_9 = S F_8 XOR 1 = 1+u_2 u_4. Neither has
u_1, so every later G_k is free of u_1 by induction. F_k still
sees u_1 (F_8 = u_1 u_3), so Q is not a sliding window and extra
is not invariant under flipping u_1. Not a prize claim.

Run: python3 research/period2_gsilent.py --certify
Dump: research/period2_gsilent.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import force
from period2_left_edge import (
    anf_str,
    anf_vars,
    bor,
    compute_columns,
    reduce_no_consec,
    shift_anf,
)
from period2_ugap_sat import ugap_ok, ugap_strings
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def fib_ok(u):
    return all(a + b < 2 for a, b in zip(u, u[1:]))


def flip_u1(u):
    v = list(u)
    v[1] = 1 - v[1]
    return v


def certify_anf(kmax: int = 20):
    F, G = compute_columns(kmax, reduce=True)
    rows = []
    for k in range(0, kmax + 1):
        fv = anf_vars(F[k])
        gv = anf_vars(G[k])
        rec = {
            "k": k,
            "F_vars": fv,
            "G_vars": gv,
            "G_has_u1": 1 in gv,
            "F_has_u1": 1 in fv,
        }
        rows.append(rec)
        if k >= 8:
            assert 1 not in gv, rec
        if k == 7:
            assert 1 in gv, rec
    # engine identities
    or67 = reduce_no_consec(bor(G[6], G[7]))
    or78 = reduce_no_consec(bor(G[7], G[8]))
    assert or67 == 1
    assert or78 == 1
    sf7 = reduce_no_consec(shift_anf(F[7], 1))
    sf8 = reduce_no_consec(shift_anf(F[8], 1))
    assert 1 not in anf_vars(sf7)
    assert G[8] == sf7 ^ 1
    assert G[9] == sf8 ^ 1
    assert anf_str(G[8]) == "u3 + u4"
    assert anf_str(G[9]) == "1 + u2*u4"
    assert anf_str(F[8]) == "u1*u3"
    assert 1 in anf_vars(F[8])
    return {
        "kmax": kmax,
        "ok": True,
        "rows": rows,
        "G6_or_G7": anf_str(or67),
        "G7_or_G8": anf_str(or78),
        "G8": anf_str(G[8]),
        "G9": anf_str(G[9]),
        "F8": anf_str(F[8]),
    }


def certify_flip_G(kmin=8, kmax=16, nlen=8):
    """G_k(u)=G_k(flip u_1) on Fibonacci-legal flips, k>=8."""
    n_words = 0
    n_fib_flip = 0
    n_match = 0
    for u in ugap_strings(nlen):
        n_words += 1
        v = flip_u1(u)
        if not fib_ok(v):
            continue
        n_fib_flip += 1
        Fu, Gu = F_of_u(u, kmax)
        Fv, Gv = F_of_u(v, kmax)
        for k in range(kmin, kmax + 1):
            assert Gu[k] == Gv[k]
        n_match += 1
    return {
        "nlen": nlen,
        "kmin": kmin,
        "kmax": kmax,
        "n_words": n_words,
        "n_fib_flip": n_fib_flip,
        "n_G_match": n_match,
        "ok": True,
    }


def certify_extra_not_invariant(Tmin=5, Tmax=16):
    """Flipping u_1 does not preserve extra in general (killed)."""
    n_on = 0
    n_legal = 0
    n_match = 0
    n_mismatch = 0
    sample_mismatch = None
    for T in range(Tmin, Tmax + 1):
        if T == 4:
            continue
        n0 = nvars(T)
        if n0 < 2:
            continue
        kneed = max(T + 2, 2 * n0 + 2)
        for u in ugap_strings(n0):
            F, _ = F_of_u(u, kneed)
            if F[T] != 1:
                continue
            n_on += 1
            v = flip_u1(u)
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
                if sample_mismatch is None:
                    sample_mismatch = {"T": T, "u": "".join(map(str, u))}
    assert n_mismatch > 0
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_onset": n_on,
        "n_legal_flip": n_legal,
        "n_extra_match": n_match,
        "n_extra_mismatch": n_mismatch,
        "sample_mismatch": sample_mismatch,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    anf = certify_anf(20)
    checks["G_u1_absent_k_ge_8"] = True
    checks["G7_has_u1"] = True
    checks["G6_or_G7_is_1"] = True
    checks["G7_or_G8_is_1"] = True
    checks["G8_is_u3_plus_u4"] = True
    checks["G9_is_1_plus_u2_u4"] = True
    checks["F8_still_has_u1"] = True
    flip = certify_flip_G()
    checks["G_k_independent_of_u1_on_fib_flip"] = True
    extra = certify_extra_not_invariant()
    checks["extra_not_invariant_under_u1_flip"] = True
    return {
        "checks": checks,
        "anf": {
            k: anf[k]
            for k in ("kmax", "ok", "G6_or_G7", "G7_or_G8", "G8", "G9", "F8")
        },
        "anf_support": [
            {"k": r["k"], "F_vars": r["F_vars"], "G_vars": r["G_vars"]}
            for r in anf["rows"]
            if 6 <= r["k"] <= 9
        ],
        "flip": flip,
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
    print("flip", report["flip"])
    print("extra_not_invariant", {k: report["extra_not_invariant"][k] for k in ("n_onset", "n_legal_flip", "n_extra_match", "n_extra_mismatch")})
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
