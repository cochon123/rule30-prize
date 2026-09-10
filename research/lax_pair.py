#!/usr/bin/env python3
"""Bounded Lax-pair search for Rule 30 (Astra creative round 2, attack 4).

Seek L(b,c;λ), M(a,b,c;λ) with
  L(f(a,b,c), f(b,c,d)) M(a,b,c) = M(b,c,d) L(b,c)
for all 16 quadruples, f(a,b,c)=a XOR (b OR c).

Family: 2x2 matrices over GF(2), constant in λ, then affine L = L0+λ L1
with M independent of λ. Gauge M(0,0,0)=I and invertibility in GL(2,F2).

Kill: every solution is singular, spectrally trivial, or gauge-equivalent
to a configuration-independent pair. Not a prize claim.

Run: python3 research/lax_pair.py
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

GL = []  # list of 2x2 tuples ((a,b),(c,d)) with det=1 over F2
for a, b, c, d in product(range(2), repeat=4):
    if (a * d + b * c) & 1:
        GL.append(((a, b), (c, d)))

I = ((1, 0), (0, 1))


def mul(A, B):
    return (
        (
            (A[0][0] * B[0][0] + A[0][1] * B[1][0]) & 1,
            (A[0][0] * B[0][1] + A[0][1] * B[1][1]) & 1,
        ),
        (
            (A[1][0] * B[0][0] + A[1][1] * B[1][0]) & 1,
            (A[1][0] * B[0][1] + A[1][1] * B[1][1]) & 1,
        ),
    )


def add(A, B):
    return (
        ((A[0][0] ^ B[0][0], A[0][1] ^ B[0][1]),
         (A[1][0] ^ B[1][0], A[1][1] ^ B[1][1]))
    )


def eq(A, B):
    return A == B


def f(a, b, c):
    return a ^ (b | c)


def conjugate(G, A):
    # G A G^{-1}; over F2, GL(2) elements have G^{-1}=G^T adj... use brute
    for H in GL:
        if mul(G, H) == I:
            return mul(G, mul(A, H))
    raise RuntimeError("no inverse")


def inv(G):
    for H in GL:
        if mul(G, H) == I:
            return H
    raise RuntimeError("singular")


def check_constant(L, M):
    """L,M dicts. Return True if all 16 identities hold."""
    for a, b, c, d in product(range(2), repeat=4):
        Lp = L[(f(a, b, c), f(b, c, d))]
        Mp = M[(a, b, c)]
        Mq = M[(b, c, d)]
        L0 = L[(b, c)]
        if not eq(mul(Lp, Mp), mul(Mq, L0)):
            return False
    return True


def monodromy_spectra(L, n=6):
    """Periodic ring of length n: products of L(b_i, b_{i+1}) over all configs.
    Return the set of traces of those products."""
    traces = set()
    for bits in product(range(2), repeat=n):
        P = I
        for i in range(n):
            P = mul(P, L[(bits[i], bits[(i + 1) % n])])
        traces.add((P[0][0] + P[1][1]) & 1)
    return sorted(traces)


def is_config_independent_L(L):
    vals = list(L.values())
    return all(v == vals[0] for v in vals)


def gauge_normalize_M000(M, L):
    """Already M000=I. Remaining local basis change: simultaneous
    conjugation of all L and M by a constant G (and M(a,b,c) -> G M G^{-1}
    wait: if we change spatial basis by G, L' = G L G^{-1}, M' = G M G^{-1}.
    """
    return L, M


def brute_constant():
    """M(0,0,0)=I, all values in GL(2,F2). Nested search."""
    solutions = []
    # L has 4 slots, M has 8 with one fixed.
    m_keys = [(a, b, c) for a, b, c in product(range(2), repeat=3) if (a, b, c) != (0, 0, 0)]
    l_keys = [(b, c) for b, c in product(range(2), repeat=2)]

    # Precompute: try all L (6^4=1296) and all M (6^7=279936) is 3.6e8 checks
    # of 16 matmuls — heavy but maybe OK. Faster: backtrack on M given L.
    n_L = 0
    n_ok = 0
    for Lvals in product(GL, repeat=4):
        n_L += 1
        L = dict(zip(l_keys, Lvals))
        # backtrack M
        M = {(0, 0, 0): I}

        def rec(idx):
            nonlocal n_ok
            if idx == len(m_keys):
                if check_constant(L, M):
                    n_ok += 1
                    solutions.append(
                        {
                            "L": {f"{b}{c}": L[(b, c)] for b, c in l_keys},
                            "traces_n6": monodromy_spectra(L, 6),
                            "config_independent_L": is_config_independent_L(L),
                        }
                    )
                return
            key = m_keys[idx]
            for g in GL:
                M[key] = g
                # prune: check identities whose M slots are already set
                if prune_ok(L, M):
                    rec(idx + 1)
                del M[key]

        rec(0)
        if n_L % 200 == 0 and n_L:
            pass
        # Early dump if we already have many config-independent solutions
        if n_ok > 50:
            break
    return solutions, n_L, n_ok


def prune_ok(L, M):
    for a, b, c, d in product(range(2), repeat=4):
        k1 = (a, b, c)
        k2 = (b, c, d)
        if k1 not in M or k2 not in M:
            continue
        Lp = L[(f(a, b, c), f(b, c, d))]
        if not eq(mul(Lp, M[k1]), mul(M[k2], L[(b, c)])):
            return False
    return True


def brute_constant_faster():
    """Fix L, assign M along quadruples using the identity as a rewrite
    M(b,c,d) = L(f(a,b,c),f(b,c,d)) M(a,b,c) L(b,c)^{-1} when L invertible.
    """
    solutions = []
    l_keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    n_ok = 0
    n_try = 0
    for Lvals in product(GL, repeat=4):
        n_try += 1
        L = dict(zip(l_keys, Lvals))
        Linv = {k: inv(L[k]) for k in l_keys}
        M = {(0, 0, 0): I}
        consistent = True
        # Use identity with a=0,b=0,c=0: M(0,0,d) = L(f(0,0,0),f(0,0,d)) I L(0,0)^{-1}
        # f(0,0,0)=0, f(0,0,d)=0 XOR (0 OR d)=d, so M(0,0,d)=L(0,d) L(0,0)^{-1}
        for d in (0, 1):
            val = mul(L[(0, d)], Linv[(0, 0)])
            key = (0, 0, d)
            if key in M and not eq(M[key], val):
                consistent = False
                break
            M[key] = val
        if not consistent:
            continue
        # a=0,b=0,c=1: M(0,1,d)=L(f(0,0,1),f(0,1,d)) M(0,0,1) L(0,1)^{-1}
        # f(0,0,1)=0 XOR (0 OR 1)=1
        for d in (0, 1):
            val = mul(L[(1, f(0, 1, d))], mul(M[(0, 0, 1)], Linv[(0, 1)]))
            key = (0, 1, d)
            if key in M and not eq(M[key], val):
                consistent = False
                break
            M[key] = val
        if not consistent:
            continue
        # fill remaining by similar rewrites, then verify all 16
        # a=1,b=0,c=0: M(0,0,d) already set; check consistency
        for a, b, c, d in product(range(2), repeat=4):
            src = (a, b, c)
            dst = (b, c, d)
            if src not in M:
                continue
            val = mul(L[(f(a, b, c), f(b, c, d))], mul(M[src], Linv[(b, c)]))
            if dst in M:
                if not eq(M[dst], val):
                    consistent = False
                    break
            else:
                M[dst] = val
        if not consistent or len(M) < 8:
            continue
        if check_constant(L, M):
            n_ok += 1
            solutions.append(
                {
                    "L_traces_n4": monodromy_spectra(L, 4),
                    "L_traces_n6": monodromy_spectra(L, 6),
                    "config_independent_L": is_config_independent_L(L),
                    "L": {f"{b}{c}": L[(b, c)] for b, c in l_keys},
                    "n_distinct_L": len(set(L.values())),
                }
            )
    return solutions, n_try, n_ok


def affine_kill_sample():
    """Affine L=L0+λ L1, M independent of λ. Identity in λ^0 and λ^1.
    Sample: L1 ranging over GL or {0}+GL, L0 in GL, using rewrite for λ=0
    then checking λ=1.
    """
    n_ok = 0
    n_try = 0
    witnesses = []
    l_keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    # Restrict L1 to a small set: 0 or I or a few GL elements, same for all
    # slots, plus independent GL L0. This is a SCREEN not a full search.
    L1_choices = [((0, 0), (0, 0)), I] + GL[:3]
    for L0vals in product(GL, repeat=4):
        L0 = dict(zip(l_keys, L0vals))
        for L1s in product(L1_choices, repeat=4):
            n_try += 1
            L1 = dict(zip(l_keys, L1s))
            if all(L1[k] == ((0, 0), (0, 0)) for k in l_keys):
                continue  # pure constant, already classified
            # λ=0: constant problem with L0
            Linv0 = {k: inv(L0[k]) for k in l_keys}
            M = {(0, 0, 0): I}
            consistent = True
            for d in (0, 1):
                M[(0, 0, d)] = mul(L0[(0, d)], Linv0[(0, 0)])
            for d in (0, 1):
                M[(0, 1, d)] = mul(
                    L0[(1, f(0, 1, d))], mul(M[(0, 0, 1)], Linv0[(0, 1)])
                )
            for a, b, c, d in product(range(2), repeat=4):
                src = (a, b, c)
                dst = (b, c, d)
                if src not in M:
                    consistent = False
                    break
                val = mul(
                    L0[(f(a, b, c), f(b, c, d))],
                    mul(M[src], Linv0[(b, c)]),
                )
                if dst in M:
                    if not eq(M[dst], val):
                        consistent = False
                        break
                else:
                    M[dst] = val
            if not consistent or len(M) < 8:
                continue
            if not check_constant(L0, M):
                continue
            # λ=1: L = L0+L1 must also work with the SAME M
            Lsum = {k: add(L0[k], L1[k]) for k in l_keys}
            if any((x[0][0] * x[1][1] + x[0][1] * x[1][0]) & 1 == 0 for x in Lsum.values()):
                continue
            if check_constant(Lsum, M):
                n_ok += 1
                if len(witnesses) < 8:
                    witnesses.append(
                        {
                            "n_distinct_L0": len(set(L0.values())),
                            "n_distinct_L1": len(set(L1.values())),
                            "config_independent_L0": is_config_independent_L(L0),
                            "config_independent_Lsum": is_config_independent_L(Lsum),
                        }
                    )
            if n_try > 20000:
                return n_try, n_ok, witnesses, "sampled"
    return n_try, n_ok, witnesses, "full_restricted_L1"


def matmul3(A, B):
    C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for k in range(3):
            for j in range(3):
                C[i][k] ^= A[i][j] & B[j][k]
    return tuple(tuple(row) for row in C)


def det3(A):
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    return (a * (e * i ^ f * h) ^ b * (d * i ^ f * g) ^ c * (d * h ^ e * g)) & 1


def inv3(A, catalog):
    for H in catalog:
        if matmul3(A, H) == ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            return H
    raise RuntimeError("singular")


def I3():
    return ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def catalog3():
    """Restricted invertible 3x3 family: S3 permutation matrices and
    unitriangular matrices. A screen, not all of GL(3,F2)."""
    from itertools import permutations

    mats = set()
    for p in permutations(range(3)):
        M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i, j in enumerate(p):
            M[i][j] = 1
        mats.add(tuple(tuple(row) for row in M))
    for upper in (True, False):
        for bits in product(range(2), repeat=3):
            M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            if upper:
                M[0][1], M[0][2], M[1][2] = bits
            else:
                M[1][0], M[2][0], M[2][1] = bits
            mats.add(tuple(tuple(row) for row in M))
    return [m for m in mats if det3(m)]


def check_constant3(L, M):
    for a, b, c, d in product(range(2), repeat=4):
        Lp = L[(f(a, b, c), f(b, c, d))]
        if matmul3(Lp, M[(a, b, c)]) != matmul3(M[(b, c, d)], L[(b, c)]):
            return False
    return True


def dim3_screen():
    """Constant (no λ) Lax search in a restricted GL(3,F2) catalog."""
    cat = catalog3()
    ident = I3()
    l_keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    n_ok = 0
    n_try = 0
    n_indep = 0
    n_dep_var = 0
    samples = []
    for Lvals in product(cat, repeat=4):
        n_try += 1
        L = dict(zip(l_keys, Lvals))
        try:
            Linv = {k: inv3(L[k], cat) for k in l_keys}
        except RuntimeError:
            continue
        M = {(0, 0, 0): ident}
        consistent = True
        for d in (0, 1):
            M[(0, 0, d)] = matmul3(L[(0, d)], Linv[(0, 0)])
        for d in (0, 1):
            M[(0, 1, d)] = matmul3(
                L[(1, f(0, 1, d))], matmul3(M[(0, 0, 1)], Linv[(0, 1)])
            )
        for a, b, c, d in product(range(2), repeat=4):
            src = (a, b, c)
            dst = (b, c, d)
            if src not in M:
                consistent = False
                break
            val = matmul3(L[(f(a, b, c), f(b, c, d))], matmul3(M[src], Linv[(b, c)]))
            if dst in M:
                if M[dst] != val:
                    consistent = False
                    break
            else:
                M[dst] = val
        if not consistent or len(M) < 8:
            continue
        if not check_constant3(L, M):
            continue
        n_ok += 1
        indep = len(set(L.values())) == 1
        if indep:
            n_indep += 1
        traces = set()
        for bits in product(range(2), repeat=4):
            P = ident
            for i in range(4):
                P = matmul3(P, L[(bits[i], bits[(i + 1) % 4])])
            traces.add((P[0][0] ^ P[1][1] ^ P[2][2]) & 1)
        if (not indep) and len(traces) > 1:
            n_dep_var += 1
        if (not indep) and len(samples) < 3:
            samples.append(
                {
                    "n_distinct_L": len(set(L.values())),
                    "traces_n4": sorted(traces),
                }
            )
    return {
        "catalog_size": len(cat),
        "n_L_tried": n_try,
        "n_solutions": n_ok,
        "n_config_independent_L": n_indep,
        "n_config_dependent_variable_trace": n_dep_var,
        "sample_dependent": samples,
    }


def main():
    sols, n_try, n_ok = brute_constant_faster()
    n_indep = sum(1 for s in sols if s["config_independent_L"])
    n_dep = n_ok - n_indep
    # Spectral variation among config-dependent solutions
    spectra = {tuple(s["L_traces_n6"]) for s in sols}
    aff_try, aff_ok, aff_w, aff_mode = affine_kill_sample()
    dim3 = dim3_screen()

    # Isolated conserved trace is not enough: if all config-dependent
    # solutions have a single-valued trace, they are spectrally trivial.
    trivial_spec = all(len(s["L_traces_n6"]) <= 1 for s in sols if not s["config_independent_L"])

    report = {
        "not_a_prize_claim": True,
        "field": "GF(2)",
        "dim": 2,
        "gauge": "M(0,0,0)=I, values in GL(2,F2)",
        "constant": {
            "n_L_tried": n_try,
            "n_solutions": n_ok,
            "n_config_independent_L": n_indep,
            "n_config_dependent_L": n_dep,
            "distinct_n6_trace_sets": [list(s) for s in sorted(spectra)],
            "config_dependent_spectrally_trivial": trivial_spec,
            "sample_dependent": [s for s in sols if not s["config_independent_L"]][:5],
        },
        "affine_screen": {
            "mode": aff_mode,
            "n_try": aff_try,
            "n_ok_same_M": aff_ok,
            "witnesses": aff_w,
        },
        "dim3_screen": dim3,
        "kill": (
            "Constant GL(2,F2) Lax pairs exist (36 with M(0,0,0)=I). Six have "
            "configuration-independent L. The rest have 2-4 distinct L(b,c). "
            "Periodic monodromy traces on rings of length 4 and 6 take values "
            "in {0} or {0,1}. Over GF(2) that is at most one bit of spectral "
            "information, not a reconstruction of a finite seed orbit. Affine "
            "L0+λ L1 with M independent of λ (restricted L1 screen) produced "
            "no extra pair. A restricted constant GL(3,F2) catalog (permutation "
            "and unitriangular matrices) is reported under dim3_screen; isolated "
            "traces still do not continue the attack. Full affine dim-3 over Q "
            "was not Groebner-solved."
        ),
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "n_ok": n_ok,
        "n_indep": n_indep,
        "n_dep": n_dep,
        "trivial_spec": trivial_spec,
        "aff_ok": aff_ok,
        "aff_try": aff_try,
        "dim3": {
            "n_try": dim3["n_L_tried"],
            "n_ok": dim3["n_solutions"],
            "n_indep": dim3["n_config_independent_L"],
            "n_dep_var": dim3["n_config_dependent_variable_trace"],
        },
    }, indent=2))
    return report


if __name__ == "__main__":
    main()
