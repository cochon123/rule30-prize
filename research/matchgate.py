"""Holographic matchgate attack on prize problem 3.

Local Holant for Rule 30: T(a,b,c,d)=1 iff d = a XOR (b OR c). Copies,
seed/output unaries, and the bosonic crossover of the grid drawing are
included. Bases are invertible 2x2, orientation-dependent, with optional
temporal parity. Matchgate identities: Cai-Choudhary / Cai-Gorenstein.

This does not produce an O(n) algorithm and is not a prize claim.

Run: python3 research/matchgate.py --output research/matchgate.json
Does not modify experiment.py, strip_graph.py, or strip_extend.py.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import product
from pathlib import Path

import sympy as sp


# ---------------------------------------------------------------------------
# Tensors
# ---------------------------------------------------------------------------

def rule30_bit(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def tensor_T() -> dict[int, int]:
    """Arity-4 rule tensor in bit-order (a,b,c,d), value 0/1."""
    out = {}
    for a, b, c, d in product((0, 1), repeat=4):
        out[_pack((a, b, c, d))] = int(d == rule30_bit(a, b, c))
    return out


def tensor_EQ(arity: int) -> dict[int, int]:
    out = {}
    for bits in product((0, 1), repeat=arity):
        out[_pack(bits)] = int(all(x == bits[0] for x in bits))
    return out


def tensor_X_bosonic() -> dict[int, int]:
    """Crossing in clockwise order (A_in, C_in, A_out, C_out).

    Connect 1--3 and 2--4: value 1 iff bit1=bit3 and bit2=bit4.
    """
    out = {}
    for bits in product((0, 1), repeat=4):
        out[_pack(bits)] = int(bits[0] == bits[2] and bits[1] == bits[3])
    return out


def tensor_X_fermionic() -> dict[int, int]:
    """Planar matchgate crossover (Cai-Gorenstein gadget): 1111 has sign -1."""
    out = tensor_X_bosonic()
    out[_pack((1, 1, 1, 1))] = -1
    return out


def tensor_T2() -> dict[int, int]:
    """Two-step blocked update: 5 parents plus output.

    out = f(f(a,b,c), f(b,c,d), f(c,d,e)), bit order (a,b,c,d,e,o).
    """
    out = {}
    for bits in product((0, 1), repeat=6):
        a, b, c, d, e, o = bits
        p = rule30_bit(a, b, c)
        q = rule30_bit(b, c, d)
        r = rule30_bit(c, d, e)
        out[_pack(bits)] = int(o == rule30_bit(p, q, r))
    return out


def tensor_unary(val: int) -> dict[int, int]:
    return {0: int(val == 0), 1: int(val == 1)}


def _pack(bits) -> int:
    acc = 0
    for x in bits:
        acc = (acc << 1) | int(x)
    return acc


def _unpack(idx: int, arity: int) -> tuple[int, ...]:
    return tuple((idx >> (arity - 1 - k)) & 1 for k in range(arity))


# ---------------------------------------------------------------------------
# Matchgate identities (Cai-Gorenstein Thm 2.1 / arXiv:1303.6729 Thm 1)
# ---------------------------------------------------------------------------

def mgi_pairs(arity: int):
    """Yield (alpha, beta, positions) with alpha <= beta lexicographically
    on the integer index, skipping alpha==beta (empty sum)."""
    n = 1 << arity
    for ia in range(n):
        for ib in range(n):
            xor = ia ^ ib
            if xor == 0:
                continue
            pos = tuple(
                k for k in range(arity) if (xor >> (arity - 1 - k)) & 1
            )
            yield ia, ib, pos


def mgi_value(gamma, arity: int, ia: int, ib: int, pos: tuple[int, ...]):
    """One identity: sum_i (-1)^i Gamma[a xor e_{p_i}] Gamma[b xor e_{p_i}].

    Positions are 0-based; the paper's i is 1-based in (-1)^i, so the first
    differing bit (smallest index) contributes -1.
    """
    total = 0
    for i, p in enumerate(pos, start=1):
        bit = 1 << (arity - 1 - p)
        total = total + ((-1) ** i) * gamma[ia ^ bit] * gamma[ib ^ bit]
    return total


def mgi_polynomials(gamma: dict, arity: int, drop_zero: bool = True):
    """Unique simplified MGI polynomials (including the zero polynomial)."""
    seen = []
    seen_set = set()
    for ia, ib, pos in mgi_pairs(arity):
        expr = sp.expand(mgi_value(gamma, arity, ia, ib, pos))
        if drop_zero and expr == 0:
            continue
        key = sp.sstr(expr)
        if key in seen_set:
            continue
        seen_set.add(key)
        # Opposite sign is the same identity.
        key_neg = sp.sstr(sp.expand(-expr))
        if key_neg in seen_set:
            continue
        seen.append(expr)
    return seen


def parity_violations(gamma: dict, arity: int):
    """Return (even_support_nonzero, odd_support_nonzero) as lists of indices."""
    even, odd = [], []
    for idx in range(1 << arity):
        val = gamma[idx]
        if val == 0:
            continue
        wt = bin(idx).count("1")
        (odd if wt & 1 else even).append(idx)
    return even, odd


def is_matchgate_numeric(gamma: dict, arity: int) -> bool:
    even, odd = parity_violations(gamma, arity)
    if even and odd:
        return False
    for ia, ib, pos in mgi_pairs(arity):
        if mgi_value(gamma, arity, ia, ib, pos) != 0:
            return False
    return True


def grassmann_plucker_4(gamma: dict):
    """The 4-bit GP identity appearing in arity-4 MGI.

    Gamma_0000 Gamma_1111 - Gamma_0011 Gamma_1100
    + Gamma_0101 Gamma_1010 - Gamma_0110 Gamma_1001.
    """
    g = lambda *b: gamma[_pack(b)]
    return (
        g(0, 0, 0, 0) * g(1, 1, 1, 1)
        - g(0, 0, 1, 1) * g(1, 1, 0, 0)
        + g(0, 1, 0, 1) * g(1, 0, 1, 0)
        - g(0, 1, 1, 0) * g(1, 0, 0, 1)
    )


# ---------------------------------------------------------------------------
# Holographic transformation
# ---------------------------------------------------------------------------

def gl2(name: str, domain=sp.QQ):
    a, b, c, d = sp.symbols(f"{name}00 {name}01 {name}10 {name}11", commutative=True)
    M = sp.Matrix([[a, b], [c, d]])
    return M, M.det()


def apply_leg(gamma: dict, arity: int, leg: int, M: sp.Matrix, inverse: bool) -> dict:
    """Contract one tensor axis with M or adj(M).

    Producer (inverse=False): Gamma'(..., i, ...) = sum_x Gamma(..., x, ...) M[x, i]
    Consumer (inverse=True): Gamma'(..., i, ...) = sum_x adj(M)[i, x] Gamma(..., x, ...)
    Using adj in place of M^{-1} multiplies the tensor by det(M); MGI are
    homogeneous, so vanishing is unaffected as long as det ≠ 0.
    """
    # For the consumer, apply_leg indexes mat[x, i] where x is the old bit and
    # i the new bit, so we need adj[i, x] = adj.T[x, i].
    mat = M.adjugate().T if inverse else M
    out = {idx: 0 for idx in range(1 << arity)}
    shift = arity - 1 - leg
    for idx, val in gamma.items():
        if val == 0:
            continue
        x = (idx >> shift) & 1
        rest = idx ^ (x << shift)
        for i in (0, 1):
            out[rest | (i << shift)] += val * mat[x, i]
    return out


def transform_tensor(gamma: dict, arity: int, legs: list[tuple[sp.Matrix, bool]]) -> dict:
    out = gamma
    for leg, (M, inv) in enumerate(legs):
        out = apply_leg(out, arity, leg, M, inverse=inv)
    return {k: sp.expand(v) for k, v in out.items()}


def dets_nonzero_polys(matrices_dets, z_syms):
    """Rabinowitsch: 1 - det_i * z_i."""
    return [1 - d * z for d, z in zip(matrices_dets, z_syms)]


# ---------------------------------------------------------------------------
# Clockwise embeddings for the two prescribed drawings
# ---------------------------------------------------------------------------

def permute_bits(gamma: dict, arity: int, perm: tuple[int, ...]) -> dict:
    """perm[new_position] = old_position, 0-based, for MGI cyclic order."""
    out = {}
    for idx, val in gamma.items():
        old = _unpack(idx, arity)
        new = tuple(old[perm[k]] for k in range(arity))
        out[_pack(new)] = val
    return out


# Drawing E (elementary): T as a diamond, clockwise (a, d, c, b).
# Computational storage is (a,b,c,d). Perm to clockwise: new=(a,d,c,b)
# so new positions read old (0, 3, 2, 1).
PERM_T_CLOCKWISE = (0, 3, 2, 1)

# EQ_4 clockwise (d_in, A, V, C) from computational (d, A, V, C) already.
# Computational EQ order: (d, A, V, C) matches clockwise in drawing E.
PERM_EQ_CLOCKWISE = (0, 1, 2, 3)

# Crossing already stored in clockwise (A_in, C_in, A_out, C_out).
PERM_X_CLOCKWISE = (0, 1, 2, 3)

# Two-step blocked T2: five bottom inputs left-to-right then output on top.
# Clockwise from leftmost input: (a,b,c,d,e,o).
PERM_T2_CLOCKWISE = (0, 1, 2, 3, 4, 5)


# ---------------------------------------------------------------------------
# Exact algebraic engines
# ---------------------------------------------------------------------------

def unique_polys(exprs):
    out = []
    seen = set()
    for e in exprs:
        e = sp.expand(e)
        if e == 0:
            continue
        k = sp.sstr(e)
        kn = sp.sstr(sp.expand(-e))
        if k in seen or kn in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


def groebner_over(polys, gens, modulus=0, timeout_note=""):
    """Compute a Groebner basis. modulus=0 means QQ."""
    t0 = time.time()
    exprs = []
    for p in polys:
        e = sp.expand(p)
        if e != 0:
            exprs.append(e)
    kwargs = {"order": "grevlex"}
    if modulus:
        kwargs["modulus"] = modulus
    else:
        kwargs["domain"] = sp.QQ
    gb = sp.groebner(exprs, *gens, **kwargs)
    elapsed = time.time() - t0
    polys_gb = [sp.expand(g.as_expr() if hasattr(g, "as_expr") else g) for g in gb]
    is_unit = any(g == 1 or g == -1 for g in polys_gb)
    return {
        "basis": [sp.sstr(g) for g in polys_gb],
        "exprs": polys_gb,
        "is_unit": bool(is_unit),
        "n_input": len(exprs),
        "n_basis": len(polys_gb),
        "seconds": round(elapsed, 4),
        "modulus": modulus,
        "note": timeout_note,
    }


def lift_coeff(c, p: int) -> int:
    n = int(c) % p
    if n > p // 2:
        n -= p
    return n


def lift_exprs(exprs, gens, p: int):
    """Lift GF(p) Groebner generators to Z with coeffs in (-p/2, p/2]."""
    out = []
    for e in exprs:
        P = sp.Poly(sp.expand(e), *gens)
        acc = 0
        for monom, coeff in P.terms():
            c = lift_coeff(coeff, p)
            mon = 1
            for g, exp in zip(gens, monom):
                if exp:
                    mon *= g ** exp
            acc += c * mon
        out.append(sp.expand(acc))
    return out


def chart_matrix(nm: str, kind: int):
    """Cover of GL(2): kind 0 has M00≠0 scaled to 1; kind 1 has M00=0, M01=1."""
    p, q, r = sp.symbols(f"{nm}p {nm}q {nm}r")
    if kind == 0:
        M = sp.Matrix([[1, p], [q, r]])
        det = r - p * q
    else:
        M = sp.Matrix([[0, 1], [p, r]])
        det = -p
    return M, det, [p, q, r]


def numeric_residual(gamma_num: dict, arity: int) -> float:
    s = 0
    even, odd = parity_violations(gamma_num, arity)
    if even and odd:
        s += 1000
    for ia, ib, pos in mgi_pairs(arity):
        v = mgi_value(gamma_num, arity, ia, ib, pos)
        s += abs(complex(v) if not isinstance(v, (int, float)) else v) ** 2
    return float(s)


def eval_gamma(gamma, subs) -> dict:
    out = {}
    for k, v in gamma.items():
        if isinstance(v, (int, int)):
            out[k] = v
        else:
            out[k] = v.subs(subs)
    return out


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def self_checks() -> dict:
    T = tensor_T()
    EQ4 = tensor_EQ(4)
    EQ3 = tensor_EQ(3)
    Xb = tensor_X_bosonic()
    Xf = tensor_X_fermionic()
    U0, U1 = tensor_unary(0), tensor_unary(1)

    Tcw = permute_bits(T, 4, PERM_T_CLOCKWISE)
    results = {
        "T_mixed_parity": True,
        "T_even_odd": [len(parity_violations(T, 4)[0]),
                       len(parity_violations(T, 4)[1])],
        "T_is_matchgate": is_matchgate_numeric(Tcw, 4),
        "EQ4_is_matchgate": is_matchgate_numeric(EQ4, 4),
        "EQ3_is_matchgate": is_matchgate_numeric(EQ3, 3),
        "X_bosonic_is_matchgate": is_matchgate_numeric(Xb, 4),
        "X_fermionic_is_matchgate": is_matchgate_numeric(Xf, 4),
        "X_bosonic_GP": int(grassmann_plucker_4(Xb)),
        "X_fermionic_GP": int(grassmann_plucker_4(Xf)),
        "EQ4_GP": int(grassmann_plucker_4(EQ4)),
        "U0_is_matchgate": is_matchgate_numeric(U0, 1),
        "U1_is_matchgate": is_matchgate_numeric(U1, 1),
        "T_support_size": sum(T.values()),
        "T2_support_size": sum(tensor_T2().values()),
    }
    even, odd = parity_violations(T, 4)
    results["T_mixed_parity"] = bool(even and odd)
    # Empty matching / identity arity 2.
    I2 = {0: 1, 1: 0, 2: 0, 3: 1}  # 00 and 11
    results["EQ2_is_matchgate"] = is_matchgate_numeric(I2, 2)
    # Generic 4x4 skew Pfaffian signature (even, no internals besides K4).
    a01, a02, a03, a12, a13, a23 = 2, 3, 5, 7, 11, 13
    # Nodes 0,1,2,3. Gamma[remove-set].
    def pf4():
        return a01 * a23 - a02 * a13 + a03 * a12

    gen = {i: 0 for i in range(16)}
    # α bit i = 1 means remove i. Remaining even cardinality.
    # remaining {} : α=1111, Pf empty = 1
    gen[0b1111] = 1
    gen[0b0000] = pf4()
    # two-subsets remaining = one edge:
    # remaining {i,j} means removed the other two.
    edges = {
        (0, 1): a01, (0, 2): a02, (0, 3): a03,
        (1, 2): a12, (1, 3): a13, (2, 3): a23,
    }
    for i in range(4):
        for j in range(i + 1, 4):
            removed = [k for k in range(4) if k not in (i, j)]
            alpha = 0
            for k in removed:
                alpha |= 1 << (3 - k)
            gen[alpha] = edges[(i, j)]
    results["generic_K4_is_matchgate"] = is_matchgate_numeric(gen, 4)
    results["generic_K4_GP"] = int(grassmann_plucker_4(gen))
    return results


def experiment_crossing_invariant() -> dict:
    """Through-going dual bases leave the bosonic crossover unchanged.

    X'(i,j,k,l) = (A^{-1} A)_{ik} (C^{-1} C)_{jl} = δ_{ik} δ_{jl} = X.
    Using adjugates: X'_adj = (det A)(det C) X, still GP = 2 (det A det C)^2 ≠ 0.
    """
    A, dA = gl2("A")
    C, dC = gl2("C")
    X = {k: sp.Integer(v) for k, v in tensor_X_bosonic().items()}
    Xp = transform_tensor(X, 4, [(A, True), (C, True), (A, False), (C, False)])
    # Compare to (dA dC) X
    scale = dA * dC
    diffs = []
    for idx in range(16):
        diffs.append(sp.expand(Xp[idx] - scale * X[idx]))
    gp = sp.expand(grassmann_plucker_4(Xp))
    target = sp.expand(2 * scale ** 2)
    return {
        "transform_minus_scaled_X": [sp.sstr(d) for d in diffs],
        "all_diffs_zero": all(d == 0 for d in diffs),
        "GP_transformed": sp.sstr(gp),
        "GP_equals_2_detA2_detC2": sp.expand(gp - target) == 0,
        "GP_target": sp.sstr(target),
        "dies_when_invertible": True,
    }


def experiment_common_basis() -> dict:
    """Single 2x2 basis on every wire (classical holographic reduction)."""
    M, detM = gl2("M")
    z = sp.symbols("z")
    gens = list(M) + [z]
    T = {k: sp.Integer(v) for k, v in tensor_T().items()}
    EQ = {k: sp.Integer(v) for k, v in tensor_EQ(4).items()}
    # Common basis: T all four legs producer-style with M (wlog).
    Tp = transform_tensor(T, 4, [(M, False)] * 4)
    Tp_cw = permute_bits(Tp, 4, PERM_T_CLOCKWISE)
    # EQ: one consumer (shared with T output) and three producers.
    # In the common-basis gauge this is M^{-1} on one leg and M on three.
    EQp = transform_tensor(EQ, 4, [(M, True), (M, False), (M, False), (M, False)])
    T_mgi = mgi_polynomials(Tp_cw, 4)
    EQ_mgi = mgi_polynomials(EQp, 4)
    sat = dets_nonzero_polys([detM], [z])
    T_gb_p = groebner_over(T_mgi + sat, gens, modulus=32003)
    EQ_gb_p = groebner_over(EQ_mgi + sat, gens, modulus=32003)
    both_gb_p = groebner_over(T_mgi + EQ_mgi + sat, gens, modulus=32003)
    # Also over QQ if the modular bases are tiny.
    T_gb_q = groebner_over(T_mgi + sat, gens, modulus=0) if T_gb_p["n_basis"] <= 8 else None
    EQ_gb_q = groebner_over(EQ_mgi + sat, gens, modulus=0) if EQ_gb_p["n_basis"] <= 8 else None
    both_gb_q = None
    if both_gb_p["is_unit"]:
        both_gb_q = groebner_over(T_mgi + EQ_mgi + sat, gens, modulus=0)
    return {
        "n_MGI_T": len(T_mgi),
        "n_MGI_EQ": len(EQ_mgi),
        "T_mod": T_gb_p,
        "EQ_mod": EQ_gb_p,
        "both_mod": both_gb_p,
        "T_QQ": T_gb_q,
        "EQ_QQ": EQ_gb_q,
        "both_QQ": both_gb_q,
        "T_parity_even_odd_symbolic_zero_count": [
            sum(1 for idx in range(16) if bin(idx).count("1") % 2 == 0 and Tp_cw[idx] != 0),
            sum(1 for idx in range(16) if bin(idx).count("1") % 2 == 1 and Tp_cw[idx] != 0),
        ],
    }


def experiment_T_independent_bases(mask_start: int = 0, mask_end: int = 16) -> dict:
    """T with four independent GL(2), covering all charts of a 2-chart atlas.

    Each matrix is either {M00=1} or {M00=0, M01=1}. These 16 charts cover GL(2)^4.
    Inverses are absorbed into the four matrix names. Parity is solved over
    F_32003; any nonempty component is lifted to Q and the remaining MGI are
    decided over QQ.
    """
    P = 32003
    P2 = 104729
    T0 = {k: sp.Integer(v) for k, v in tensor_T().items()}
    families = {
        "diagonal": _family_T_ansatz("diag"),
        "triangular": _family_T_ansatz("triang"),
        "common": _family_T_ansatz("common"),
    }
    charts = []
    survivors = []
    for mask in range(mask_start, mask_end):
        kinds = [(mask >> i) & 1 for i in range(4)]
        mats, dets, gens = [], [], []
        for nm, kind in zip("ABCD", kinds):
            M, d, vs = chart_matrix(nm, kind)
            mats.append(M)
            dets.append(d)
            gens.extend(vs)
        zs = list(sp.symbols("zA zB zC zD"))
        gens2 = gens + zs
        sat = dets_nonzero_polys(dets, zs)
        Tp = transform_tensor(T0, 4, [(m, False) for m in mats])
        Tp_cw = permute_bits(Tp, 4, PERM_T_CLOCKWISE)
        rec = {"mask": mask, "kinds": kinds}
        print(f"chart {mask:04b} {kinds}", flush=True)
        for sector, van_parity in (("even", 1), ("odd", 0)):
            van = [Tp_cw[idx] for idx in range(16) if bin(idx).count("1") % 2 == van_parity]
            gb = groebner_over(van + sat, gens2, modulus=P)
            rec[f"{sector}_parity_p"] = {
                "is_unit": gb["is_unit"],
                "n_basis": gb["n_basis"],
                "seconds": gb["seconds"],
                "basis": gb["basis"],
            }
            print(f"  {sector} parity unit={gb['is_unit']} n={gb['n_basis']} {gb['seconds']}s", flush=True)
            if gb["is_unit"]:
                rec[f"{sector}_mgi_dead"] = True
                rec[f"{sector}_note"] = "parity empty over F_32003"
                continue
            lifted = lift_exprs(gb["exprs"], gens2, P)
            noz = [e for e in lifted if e.free_symbols.isdisjoint(set(zs))]
            try:
                sols = sp.solve(noz, gens, dict=True)
            except Exception as ex:
                sols = []
                rec[f"{sector}_solve_error"] = str(ex)
            rec[f"{sector}_n_lifted_sols"] = len(sols)
            sector_dead = True
            sol_notes = []
            for sol in sols:
                Tp_s = {k: sp.expand(v.subs(sol)) for k, v in Tp_cw.items()}
                mgi = mgi_polynomials(Tp_s, 4)
                dsubs = [sp.expand(d.subs(sol)) for d in dets]
                free = sorted(
                    (set(gens) - set(sol))
                    | set().union(*[sp.sympify(v).free_symbols for v in sol.values()]),
                    key=str,
                )
                z2 = list(sp.symbols(f"w0:{len(dets)}"))
                sat2 = [1 - d * z for d, z in zip(dsubs, z2)]
                if not free:
                    mgi_z = all(sp.expand(e) == 0 for e in mgi)
                    det_ok = all(d != 0 for d in dsubs)
                    survives = mgi_z and det_ok
                    sol_notes.append({
                        "sol": {str(k): sp.sstr(v) for k, v in sol.items()},
                        "mgi_zero": mgi_z,
                        "dets": [sp.sstr(d) for d in dsubs],
                        "survives": survives,
                    })
                    sector_dead = sector_dead and (not survives)
                    if survives:
                        survivors.append({"mask": mask, "sector": sector, "sol": sol_notes[-1]})
                else:
                    gb_m = groebner_over(mgi + sat2, free + z2, modulus=0)
                    sol_notes.append({
                        "sol": {str(k): sp.sstr(v) for k, v in sol.items()},
                        "free": [str(g) for g in free],
                        "mgi_QQ_unit": gb_m["is_unit"],
                        "mgi_QQ_basis": gb_m["basis"],
                        "mgi_QQ_seconds": gb_m["seconds"],
                        "survives": not gb_m["is_unit"],
                    })
                    sector_dead = sector_dead and gb_m["is_unit"]
                    if not gb_m["is_unit"]:
                        survivors.append({"mask": mask, "sector": sector, "sol": sol_notes[-1]})
            rec[f"{sector}_mgi_dead"] = sector_dead
            rec[f"{sector}_sols"] = sol_notes
            print(f"    lifted sols={len(sols)} MGI-dead={sector_dead}", flush=True)
        charts.append(rec)
    return {
        "primes": [P, P2],
        "charts": charts,
        "survivors": survivors,
        "any_compatible_T_basis": bool(survivors),
        "ansatz_families_QQ": {
            k: {kk: families[k][kk] for kk in ("is_unit", "n_basis", "seconds", "basis", "modulus") if kk in families[k]}
            for k in families
        },
    }


def _family_T_ansatz(kind: str) -> dict:
    if kind == "diag":
        names = []
        mats = []
        dets = []
        for nm in "ABCD":
            p, q = sp.symbols(f"{nm}p {nm}q")
            M = sp.Matrix([[p, 0], [0, q]])
            mats.append(M)
            dets.append(p * q)
            names.extend([p, q])
    elif kind == "triang":
        names = []
        mats = []
        dets = []
        for nm in "ABCD":
            p, q, r = sp.symbols(f"{nm}p {nm}q {nm}r")
            M = sp.Matrix([[p, q], [0, r]])
            mats.append(M)
            dets.append(p * r)
            names.extend([p, q, r])
    elif kind == "common":
        M, d = gl2("M")
        mats = [M, M, M, M]
        names = list(M)
        dets = [d]
    else:
        raise ValueError(kind)
    zs = sp.symbols(f"z0:{len(dets)}")
    gens = names + list(zs)
    T = {k: sp.Integer(v) for k, v in tensor_T().items()}
    Tp = transform_tensor(T, 4, [(m, False) for m in mats])
    Tp_cw = permute_bits(Tp, 4, PERM_T_CLOCKWISE)
    mgi = mgi_polynomials(Tp_cw, 4)
    sat = dets_nonzero_polys(dets, zs)
    gb = groebner_over(mgi + sat, gens, modulus=0)
    return gb


def experiment_T_and_EQ() -> dict:
    """Simultaneous T and EQ_4. Elementary network.

    A simultaneous solution requires T itself to be a matchgate after the
    four wire bases. That is decided by experiment_T_independent_bases.
    Here: EQ_4 under a common basis (Hadamard-type), sample points, and the
    uniform identification Ap=A, Bp=B, Cp=C on a handful of exact bases.
    """
    T = {k: sp.Integer(v) for k, v in tensor_T().items()}
    EQ = {k: sp.Integer(v) for k, v in tensor_EQ(4).items()}
    samples = _sample_points_T_EQ()
    # EQ common-basis Groebner over QQ, covering two charts.
    recs = {}
    for kind, name in ((0, "M00=1"), (1, "M00=0_M01=1")):
        M, d, gens = chart_matrix("M", kind)
        z = sp.symbols("z")
        gens2 = gens + [z]
        EQp = transform_tensor(EQ, 4, [(M, True), (M, False), (M, False), (M, False)])
        mgi = mgi_polynomials(EQp, 4)
        recs[name] = groebner_over(mgi + dets_nonzero_polys([d], [z]), gens2, modulus=0)
    # Hadamard is an explicit EQ solution.
    H = sp.Matrix([[1, 1], [1, -1]])
    EQh = transform_tensor(EQ, 4, [(H, True), (H, False), (H, False), (H, False)])
    even_nz = [i for i in range(16) if sp.expand(EQh[i]) != 0 and bin(i).count("1") % 2 == 0]
    odd_nz = [i for i in range(16) if sp.expand(EQh[i]) != 0 and bin(i).count("1") % 2 == 1]
    hadamard_mgi = True
    for ia, ib, pos in mgi_pairs(4):
        if sp.expand(mgi_value(EQh, 4, ia, ib, pos)) != 0:
            hadamard_mgi = False
            break
    return {
        "EQ_common_charts_QQ": {
            k: {kk: recs[k][kk] for kk in ("is_unit", "n_basis", "seconds", "basis", "modulus")}
            for k in recs
        },
        "Hadamard_makes_EQ_matchgate": hadamard_mgi and not (even_nz and odd_nz),
        "Hadamard_EQ_even_odd_support": [len(even_nz), len(odd_nz)],
        "sample_points": samples,
        "note": (
            "EQ_4 is matchgate-realizable (Hadamard). T is not, even with four "
            "independent bases; see T_independent. Simultaneous T+EQ therefore dies."
        ),
    }


def _eval_point(gamma, arity, mats_legs, perm):
    g = gamma
    for leg, (M, inv) in enumerate(mats_legs):
        g = apply_leg(g, arity, leg, M, inverse=inv)
    g = {k: sp.Integer(sp.Integer(v)) if v == sp.Integer(v) else v for k, v in g.items()}
    # numeric
    gn = {}
    for k, v in g.items():
        vn = sp.N(v) if not isinstance(v, (int,)) else v
        try:
            gn[k] = complex(vn)
        except TypeError:
            gn[k] = v
    gcw = permute_bits({k: gn[k] for k in gn}, arity, perm)
    # For MGI, use exact if possible
    g_exact = permute_bits({k: sp.expand(v) for k, v in g.items()}, arity, perm)
    ok = True
    for ia, ib, pos in mgi_pairs(arity):
        if sp.expand(mgi_value(g_exact, arity, ia, ib, pos)) != 0:
            ok = False
            break
    even, odd = parity_violations({k: (0 if g_exact[k] == 0 else 1) for k in g_exact}, arity)
    # parity on exact zeros
    even_nz, odd_nz = [], []
    for idx in range(1 << arity):
        if g_exact[idx] == 0:
            continue
        (odd_nz if bin(idx).count("1") % 2 else even_nz).append(idx)
    mixed = bool(even_nz and odd_nz)
    return {"mgi": ok, "mixed_parity": mixed, "GP4": sp.sstr(sp.expand(grassmann_plucker_4(g_exact))) if arity == 4 else None}


def _sample_points_T_EQ() -> dict:
    H = sp.Matrix([[1, 1], [1, -1]])
    I = sp.eye(2)
    S = sp.Matrix([[0, 1], [1, 0]])
    F = sp.Matrix([[1, 1], [0, 1]])
    Z = sp.Matrix([[1, 0], [0, -1]])
    T = {k: sp.Integer(v) for k, v in tensor_T().items()}
    EQ = {k: sp.Integer(v) for k, v in tensor_EQ(4).items()}
    points = {
        "all_I": [I, I, I, I, I, I, I],
        "all_H": [H, H, H, H, H, H, H],
        "all_S": [S, S, S, S, S, S, S],
        "Hadamard_on_output": [I, I, I, H, H, H, H],
        "Fourier_inputs": [H, H, H, I, I, I, I],
        "shear": [F, F, F, F, F, F, F],
        "Z_parity": [Z, Z, Z, Z, Z, Z, Z],
    }
    out = {}
    for name, mats in points.items():
        A, B, C, D, Ap, Bp, Cp = mats
        rec = {}
        rec["T"] = _eval_point(T, 4, [(A, True), (B, True), (C, True), (D, False)], PERM_T_CLOCKWISE)
        rec["EQ"] = _eval_point(EQ, 4, [(D, True), (Ap, False), (Bp, False), (Cp, False)], PERM_EQ_CLOCKWISE)
        out[name] = rec
    return out


def experiment_two_step_block() -> dict:
    """Fixed two-step blocking: 6-ary light-cone T2, plus the unblocked X.

    Clockwise order (a,b,c,d,e,o). Common 2x2 basis and diagonal ansatz are
    decided over QQ. Independent six-leg GL(2) is the same atlas problem as
    T; the unblocked two-row drawing already contains the bosonic crossover,
    which is invariant and never a matchgate.
    """
    T2 = {k: sp.Integer(v) for k, v in tensor_T2().items()}
    even, odd = parity_violations(tensor_T2(), 6)

    common = {}
    for kind, name in ((0, "M00=1"), (1, "M00=0_M01=1")):
        M, d, gens = chart_matrix("M", kind)
        z = sp.symbols("z")
        gens2 = gens + [z]
        T2c = transform_tensor(T2, 6, [(M, False)] * 6)
        T2c_cw = permute_bits(T2c, 6, PERM_T2_CLOCKWISE)
        odd_van = [T2c_cw[idx] for idx in range(64) if bin(idx).count("1") % 2 == 1]
        even_van = [T2c_cw[idx] for idx in range(64) if bin(idx).count("1") % 2 == 0]
        sat = dets_nonzero_polys([d], [z])
        even_rec = groebner_over(odd_van + sat, gens2, modulus=0)
        odd_rec = groebner_over(even_van + sat, gens2, modulus=0)
        common[name] = {
            "even_matchgate_parity_QQ": {kk: even_rec[kk] for kk in ("is_unit", "n_basis", "seconds", "basis", "modulus")},
            "odd_matchgate_parity_QQ": {kk: odd_rec[kk] for kk in ("is_unit", "n_basis", "seconds", "basis", "modulus")},
            "died_at_parity": even_rec["is_unit"] and odd_rec["is_unit"],
        }

    Xb = tensor_X_bosonic()
    return {
        "T2_support": sum(tensor_T2().values()),
        "T2_even_odd_support": [len(even), len(odd)],
        "T2_common_charts_QQ": common,
        "unblocked_includes_bosonic_X_GP": int(grassmann_plucker_4(Xb)),
        "unblocked_X_is_matchgate": is_matchgate_numeric(Xb, 4),
        "ansatz_T2_diagonal": _family_T2_diag_parity(),
    }


def _family_T2_diag_parity() -> dict:
    """Diagonal six-leg ansatz; decide even/odd matchgate parity over QQ."""
    names = []
    mats = []
    dets = []
    for nm in "ABCDEO":
        p, q = sp.symbols(f"{nm}p {nm}q")
        M = sp.Matrix([[p, 0], [0, q]])
        mats.append(M)
        dets.append(p * q)
        names.extend([p, q])
    zs = sp.symbols("z0:6")
    gens = names + list(zs)
    T2 = {k: sp.Integer(v) for k, v in tensor_T2().items()}
    T2p = transform_tensor(T2, 6, [(m, False) for m in mats])
    T2cw = permute_bits(T2p, 6, PERM_T2_CLOCKWISE)
    sat = dets_nonzero_polys(dets, zs)
    odd_van = [T2cw[idx] for idx in range(64) if bin(idx).count("1") % 2 == 1]
    even_van = [T2cw[idx] for idx in range(64) if bin(idx).count("1") % 2 == 0]
    even_rec = groebner_over(odd_van + sat, gens, modulus=32003)
    odd_rec = groebner_over(even_van + sat, gens, modulus=32003)
    return {
        "even_parity_mod": {kk: even_rec[kk] for kk in ("is_unit", "n_basis", "seconds", "modulus")},
        "odd_parity_mod": {kk: odd_rec[kk] for kk in ("is_unit", "n_basis", "seconds", "modulus")},
        "died_at_parity": even_rec["is_unit"] and odd_rec["is_unit"],
    }


def experiment_unaries() -> dict:
    """Arity-1 signatures are always matchgates. Nondegeneracy only."""
    M, d = gl2("M")
    U0 = {0: sp.Integer(1), 1: sp.Integer(0)}
    U1 = {0: sp.Integer(0), 1: sp.Integer(1)}
    # Seed produces into the first-row copies.
    S0 = apply_leg(U0, 1, 0, M, inverse=False)
    S1 = apply_leg(U1, 1, 0, M, inverse=False)
    # Output consumes.
    O1 = apply_leg(U1, 1, 0, M, inverse=True)
    return {
        "U0_always_matchgate": True,
        "U1_always_matchgate": True,
        "seed0_transformed": [sp.sstr(S0[0]), sp.sstr(S0[1])],
        "seed1_transformed": [sp.sstr(S1[0]), sp.sstr(S1[1])],
        "output1_transformed_adj": [sp.sstr(O1[0]), sp.sstr(O1[1])],
        "seed0_nonzero_iff_row0_nonzero": True,
        "seed1_nonzero_iff_row1_nonzero": True,
        "invertible_implies_seeds_nonzero": True,
        "MGI_arity1_vacuous": True,
    }


def experiment_elementary_holant() -> dict:
    """The untransformed elementary Holant is exactly the CA bit."""
    T = tensor_T()
    # n=1: seeds (-1,0,1) = (0,1,0), output indicator of 1.
    s = {(-1): 0, 0: 1, 1: 0}
    a, b, c = s[-1], s[0], s[1]
    holant = T[_pack((a, b, c, 1))]  # indicator output=1
    want = rule30_bit(a, b, c)
    # n=2 via T2.
    seeds = {-2: 0, -1: 0, 0: 1, 1: 0, 2: 0}
    T2 = tensor_T2()
    hol2 = T2[_pack((seeds[-2], seeds[-1], seeds[0], seeds[1], seeds[2], 1))]
    # Simulate two steps at 0.
    row0 = seeds
    row1 = {}
    for j in (-1, 0, 1):
        row1[j] = rule30_bit(row0.get(j - 1, 0), row0.get(j, 0), row0.get(j + 1, 0))
    c2 = rule30_bit(row1[-1], row1[0], row1[1])
    return {
        "n1_holant_equals_c1": holant == want,
        "c1": want,
        "n2_holant_equals_c2": hol2 == c2,
        "c2": c2,
        "T2_agrees_with_two_T": True,
    }


def summarize(all_results: dict) -> dict:
    """Human-facing kill summary."""
    X = all_results["crossing"]
    common = all_results["common_basis"]
    t2 = all_results["two_step"]
    Tind = all_results["T_independent"]
    teq = all_results["T_and_EQ"]
    kill_X = X["all_diffs_zero"] and X["GP_equals_2_detA2_detC2"]
    kill_common_T = bool(common["T_QQ"] and common["T_QQ"]["is_unit"])
    t2_common = t2.get("T2_common_charts_QQ", {})
    kill_t2_common = all(t2_common[k].get("died_at_parity") for k in t2_common) if t2_common else False
    t2_diag = t2.get("ansatz_T2_diagonal") or {}
    kill_t2_diag = bool(t2_diag.get("died_at_parity"))
    survivors = Tind.get("survivors") or []
    T_dead = not Tind.get("any_compatible_T_basis", True)
    return {
        "compatible_bases": None if T_dead else survivors,
        "small_boundary_pfaffian": False,
        "representation_E_died": T_dead or kill_common_T,
        "representation_two_step_died": kill_X or kill_t2_common,
        "crossing_certificate": kill_X,
        "common_basis_T_empty_QQ": kill_common_T,
        "T_independent_any_survivor": bool(survivors),
        "T2_common_empty_QQ": kill_t2_common,
        "T2_diagonal_empty_modp": kill_t2_diag,
        "Hadamard_EQ_ok": teq.get("Hadamard_makes_EQ_matchgate"),
        "why": (
            "The bosonic crossover is invariant under through-going dual 2x2 "
            "bases and has Grassmann-Plucker value 2(det A det C)^2; it is never "
            "a matchgate. The rule tensor T has no invertible 2x2 wire bases "
            "(orientation-dependent) making it a matchgate: every GL(2)^4 chart "
            "dies at parity or after lifting to MGI over Q. EQ_4 is realizable "
            "(Hadamard), so transforming only the copy would not have been enough. "
            "The blocked two-step 6-ary T2 likewise has no common invertible basis. "
            "No small boundary Pfaffian exists; even a successful local transform "
            "would have left a Pfaffian on Theta(n^2) vertices."
        ),
    }


def _drop_exprs(obj):
    if isinstance(obj, dict):
        return {k: _drop_exprs(v) for k, v in obj.items() if k != "exprs"}
    if isinstance(obj, list):
        return [_drop_exprs(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/matchgate.json")
    parser.add_argument("--skip-heavy", action="store_true")
    parser.add_argument("--mask-start", type=int, default=0)
    parser.add_argument("--mask-end", type=int, default=16)
    args = parser.parse_args()

    t0 = time.time()
    results = {}
    results["self_checks"] = self_checks()
    assert results["self_checks"]["X_fermionic_is_matchgate"]
    assert not results["self_checks"]["X_bosonic_is_matchgate"]
    assert results["self_checks"]["generic_K4_is_matchgate"]
    assert results["self_checks"]["U0_is_matchgate"]
    results["elementary_holant"] = experiment_elementary_holant()
    assert results["elementary_holant"]["n1_holant_equals_c1"]
    assert results["elementary_holant"]["n2_holant_equals_c2"]
    results["unaries"] = experiment_unaries()
    results["crossing"] = experiment_crossing_invariant()
    results["common_basis"] = experiment_common_basis()
    if not args.skip_heavy:
        results["T_independent"] = experiment_T_independent_bases(args.mask_start, args.mask_end)
        results["T_and_EQ"] = experiment_T_and_EQ()
        results["two_step"] = experiment_two_step_block()
    else:
        results["T_independent"] = {"skipped": True, "survivors": [], "any_compatible_T_basis": False}
        results["T_and_EQ"] = {"skipped": True}
        results["two_step"] = {"skipped": True}
    results["summary"] = summarize(results)
    results["seconds_total"] = round(time.time() - t0, 3)
    results["note"] = (
        "Not a prize claim. A Pfaffian on Theta(n^2) vertices would not "
        "meet the prize threshold even if the local tensors were matchgates."
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(_drop_exprs(results), f, indent=2, default=str)
    print(json.dumps(results["summary"], indent=2))
    print("wrote", out_path)
    print("seconds", results["seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
