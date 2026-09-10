#!/usr/bin/env python3
"""Nonuniform substitution tilings of the Rule 30 centre (prize problem 2).

Freeze (Astra ideas6 item 3): four auxiliary letters, two substitutions, image
lengths 2 or 3, a letter-to-bit coding, at least one nonuniform substitution.
Search S-adic (one morphism per level) hierarchical parses of the first 1024
centre bits; freeze survivors and test extension through 16384. Contraction
is an exact joint-spectral-radius bound on the imbalance subspace, not a
measured frequency. Synthesis is capped at two CPU-hours.

A finite parse is not a density proof. This is not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/substitution_tiling.py
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


ALPH = 4
PARSE_N = 1024
EXTEND_N = 16384
SEED_MAX = 4
BUDGET_SEC = 7200
MAX_PREIMAGES = 16
MAX_INFER_RESULTS = 64
MAX_INFER_NODES = 1_500_000
MAX_LIBRARIES = 80
MAX_DEPTH = 24
WAYS_CAP = 8

# Frozen coding subclass: both bits used. 2+2 and the two 3+1 splits.
TAUS = (
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (0, 1, 1, 1),
)


def packed_center_bits(count: int) -> bytes:
    row = 1
    out = bytearray()
    for t in range(count):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row)
    return bytes(out)


def inverse_tau(tau):
    inv = [[], []]
    for a, bit in enumerate(tau):
        inv[bit].append(a)
    return inv


def v_imbalance(tau):
    return tuple(1 if tau[a] else -1 for a in range(ALPH))


def incidence_matrix(sigma):
    M = [[0] * ALPH for _ in range(ALPH)]
    for a, img in enumerate(sigma):
        if img is None:
            continue
        for b in img:
            M[b][a] += 1
    return M


def transpose(M):
    n = len(M)
    return [[M[j][i] for j in range(n)] for i in range(n)]


def mat_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            if aik == 0:
                continue
            Bk = B[k]
            Ci = C[i]
            for j in range(n):
                Ci[j] += aik * Bk[j]
    return C


def mat_vec(M, v):
    n = len(M)
    return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]


def sigma_defined(sigma):
    return tuple(i for i in range(ALPH) if sigma[i] is not None)


def sigma_complete(sigma):
    return all(img is not None for img in sigma)


def min_image_len(sigma):
    lens = [len(img) for img in sigma if img is not None]
    return min(lens) if lens else 0


def morphism_nonuniform(sigma):
    lens = [len(img) for img in sigma if img is not None]
    return len(set(lens)) > 1


def library_nonuniform(library):
    if any(morphism_nonuniform(s) for s in library):
        return True
    if len(library) < 2:
        return False
    s0, s1 = library[0], library[1]
    for a in range(ALPH):
        if s0[a] is not None and s1[a] is not None and s0[a] != s1[a]:
            return True
    return False


def sigma_key(sigma):
    return tuple(None if img is None else bytes(img) for img in sigma)


def sigma_json(sigma):
    out = []
    for img in sigma:
        if img is None:
            out.append(None)
        else:
            out.append("".join(str(x) for x in img))
    return out


def apply_morphism(word, sigma):
    out = bytearray()
    for a in word:
        img = sigma[a]
        if img is None:
            return None
        out.extend(img)
    return bytes(out)


def coded_image(img, tau):
    return bytes(tau[x] for x in img)


def expand_directive(seed, directive, library):
    w = bytes(seed)
    for idx in reversed(directive):
        w = apply_morphism(w, library[idx])
        if w is None:
            return None
    return w


# ---------------------------------------------------------------------------
# Frozen desubstitution (iterative; safe at length 16384)
# ---------------------------------------------------------------------------

def desubstitute_frozen(seq, sigma, tau=None, cap=MAX_PREIMAGES):
    n = len(seq)
    if n == 0:
        return [b""]
    images = []
    for a in range(ALPH):
        img = sigma[a]
        if img is None:
            images.append(None)
        elif tau is not None:
            images.append(coded_image(img, tau))
        else:
            images.append(bytes(img))
    ways = [[] for _ in range(n + 1)]
    ways[0].append((-1, -1))
    for i in range(n):
        if not ways[i]:
            continue
        rem = n - i
        for a in range(ALPH):
            img = images[a]
            if img is None:
                continue
            L = len(img)
            if L <= rem and seq[i : i + L] == img and len(ways[i + L]) < WAYS_CAP:
                ways[i + L].append((i, a))
    if not ways[n]:
        return []
    tails = [[] for _ in range(n + 1)]
    tails[n] = [b""]
    for pos in range(n, 0, -1):
        bucket = tails[pos]
        if not bucket:
            continue
        for prev, a in ways[pos]:
            if prev < 0:
                continue
            dest = tails[prev]
            for tail in bucket:
                if len(dest) >= cap:
                    break
                dest.append(bytes([a]) + tail)
            if len(dest) >= cap and pos == 1:
                break
    return tails[0][:cap]


# ---------------------------------------------------------------------------
# Infer morphisms by left-to-right backtracking
# ---------------------------------------------------------------------------

def infer_from_letters(word, deadline, stats, greedy_new=True, max_results=MAX_INFER_RESULTS):
    """Discover σ with |σ(a)|∈{2,3} such that word = σ(preimage).

    Subclass: left-greedy type introduction (a new producer is opened only
    when no already-bound image matches). Non-greedy search is used for
    words of length <= 96. Letter identities of new producers are tried in
    full; image content at a cut is the unique substring of `word`.
    """
    n = len(word)
    if n < 2:
        return []
    results = []
    nodes = 0
    sigma = [None] * ALPH
    pre = bytearray()
    use_greedy = greedy_new or n > 96

    # Exhaustive uniform length-2 desubstitution of this letter word.
    if n % 2 == 0:
        pairs = [word[i : i + 2] for i in range(0, n, 2)]
        types = []
        seen_p = {}
        for p in pairs:
            if p not in seen_p:
                seen_p[p] = len(types)
                types.append(p)
        k = len(types)
        if k <= ALPH:
            for assignment in product(range(ALPH), repeat=k):
                if len(set(assignment)) != k:
                    continue
                sig = [None] * ALPH
                ok = True
                for i, p in enumerate(types):
                    a = assignment[i]
                    if sig[a] is not None and sig[a] != p:
                        ok = False
                        break
                    sig[a] = p
                if not ok:
                    continue
                letter_of = {types[i]: assignment[i] for i in range(k)}
                pre_l2 = bytes(letter_of[p] for p in pairs)
                results.append((sigma_key(sig), pre_l2))
                if len(results) >= max_results:
                    stats["infer_letter_calls"] = stats.get("infer_letter_calls", 0) + 1
                    return results

    def dfs(pos):
        nonlocal nodes
        if time.monotonic() >= deadline or len(results) >= max_results:
            return
        nodes += 1
        if nodes > MAX_INFER_NODES:
            return
        if pos == n:
            results.append((sigma_key(sigma), bytes(pre)))
            return
        rem = n - pos
        if rem == 1:
            return
        matched = False
        for a in range(ALPH):
            img = sigma[a]
            if img is None:
                continue
            L = len(img)
            if L <= rem and word[pos : pos + L] == img:
                matched = True
                pre.append(a)
                dfs(pos + L)
                pre.pop()
                if len(results) >= max_results:
                    return
        if use_greedy and matched:
            return
        for a in range(ALPH):
            if sigma[a] is not None:
                continue
            for L in (2, 3):
                if L > rem:
                    continue
                img = word[pos : pos + L]
                dup = False
                for b in range(ALPH):
                    if sigma[b] is not None and sigma[b] == img:
                        dup = True
                        break
                if dup:
                    continue
                sigma[a] = img
                pre.append(a)
                dfs(pos + L)
                pre.pop()
                sigma[a] = None
                if len(results) >= max_results:
                    return
    dfs(0)
    stats["infer_letter_nodes"] = stats.get("infer_letter_nodes", 0) + nodes
    stats["infer_letter_calls"] = stats.get("infer_letter_calls", 0) + 1
    return results


def infer_from_bits(bits, tau, deadline, stats, greedy_new=True, max_results=MAX_INFER_RESULTS):
    """Finest-level inference: bind letter images whose coding matches `bits`."""
    n = len(bits)
    inv = inverse_tau(tau)
    if not inv[0] or not inv[1]:
        return []
    results = []
    nodes = 0
    sigma = [None] * ALPH
    pre = bytearray()
    use_greedy = greedy_new or n > 256

    def dfs(pos):
        nonlocal nodes
        if time.monotonic() >= deadline or len(results) >= max_results:
            return
        nodes += 1
        if nodes > MAX_INFER_NODES:
            return
        if pos == n:
            results.append((sigma_key(sigma), bytes(pre)))
            return
        rem = n - pos
        if rem == 1:
            return
        matched = False
        for a in range(ALPH):
            img = sigma[a]
            if img is None:
                continue
            L = len(img)
            if L <= rem and bits[pos : pos + L] == coded_image(img, tau):
                matched = True
                pre.append(a)
                dfs(pos + L)
                pre.pop()
                if len(results) >= max_results:
                    return
        if use_greedy and matched:
            return
        for a in range(ALPH):
            if sigma[a] is not None:
                continue
            for L in (2, 3):
                if L > rem:
                    continue
                slice_b = bits[pos : pos + L]
                pools = [inv[b] for b in slice_b]
                if any(len(p) == 0 for p in pools):
                    continue
                for lift in product(*pools):
                    img = bytes(lift)
                    dup = False
                    for b in range(ALPH):
                        if sigma[b] is not None and sigma[b] == img:
                            dup = True
                            break
                    if dup:
                        continue
                    sigma[a] = img
                    pre.append(a)
                    dfs(pos + L)
                    pre.pop()
                    sigma[a] = None
                    if len(results) >= max_results:
                        return
    dfs(0)
    stats["infer_bit_nodes"] = stats.get("infer_bit_nodes", 0) + nodes
    stats["infer_bit_calls"] = stats.get("infer_bit_calls", 0) + 1
    return results


def length2_finest_candidates(bits, tau):
    """Exhaustive uniform-length-2 finest morphisms for a fixed coding.

    Pair the bit string, assign producer letters to appearing digrams, and
    enumerate letter-lifts of each coded image. This is a complete scan of
    that freeze slice, not a sample.
    """
    n = len(bits)
    if n % 2:
        return []
    inv = inverse_tau(tau)
    if not inv[0] or not inv[1]:
        return []
    digrams = [bits[i : i + 2] for i in range(0, n, 2)]
    types = []
    seen = {}
    for d in digrams:
        if d not in seen:
            seen[d] = len(types)
            types.append(d)
    k = len(types)
    if k > ALPH:
        return []
    letters = range(ALPH)
    out = []
    for assignment in product(letters, repeat=k):
        if len(set(assignment)) != k:
            continue
        letter_of = {types[i]: assignment[i] for i in range(k)}
        pre = bytes(letter_of[d] for d in digrams)
        lifts = []
        for d in types:
            pools = [inv[d[0]], inv[d[1]]]
            lifts.append([bytes(x) for x in product(*pools)])
        for choice in product(*lifts):
            sigma = [None] * ALPH
            ok = True
            for i, d in enumerate(types):
                a = assignment[i]
                img = choice[i]
                if sigma[a] is not None and sigma[a] != img:
                    ok = False
                    break
                sigma[a] = img
            if ok:
                out.append((sigma_key(sigma), pre))
    return out


# ---------------------------------------------------------------------------
# Exact imbalance-subspace contraction
# ---------------------------------------------------------------------------

def vec_independent(basis, vec):
    """Whether vec is outside the Q-span of `basis` (rows, already collected)."""
    rows = [b[:] for b in basis]
    rows.append([Fraction(x) for x in vec])
    if not rows:
        return True
    a = [row[:] for row in rows]
    n = len(a)
    m = len(a[0])
    r = 0
    col = 0
    while r < n and col < m:
        piv = None
        for i in range(r, n):
            if a[i][col] != 0:
                piv = i
                break
        if piv is None:
            col += 1
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][col]
        a[r] = [x / pv for x in a[r]]
        for i in range(n):
            if i == r or a[i][col] == 0:
                continue
            fac = a[i][col]
            a[i] = [a[i][k] - fac * a[r][k] for k in range(m)]
        r += 1
        col += 1
    return r > len(basis)


def krylov_basis(M0T, M1T, v):
    """Smallest Q-subspace containing v and invariant under M0^T, M1^T."""
    basis = []
    queue = [[Fraction(x) for x in v]]
    while queue:
        vec = queue.pop()
        if all(x == 0 for x in vec):
            continue
        if basis and not vec_independent(basis, vec):
            continue
        basis.append(vec)
        queue.append(mat_vec(M0T, vec))
        queue.append(mat_vec(M1T, vec))
        if len(basis) >= ALPH:
            break
    return basis


def express_in_basis(basis, vec):
    """Solve basis^T x = vec, i.e. B x = vec with B columns = basis vectors.

    `basis` is a list of d vectors in Q^4. Return coordinates in Q^d, or None.
    """
    d = len(basis)
    if d == 0:
        return [] if all(x == 0 for x in vec) else None
    m = len(basis[0])
    # Augment: rows of (B | vec) with B having columns = basis
    A = [[basis[j][i] for j in range(d)] + [Fraction(vec[i])] for i in range(m)]
    r = 0
    pivot_col = [-1] * m
    used = [False] * d
    col = 0
    while r < m and col < d:
        piv = None
        for i in range(r, m):
            if A[i][col] != 0:
                piv = i
                break
        if piv is None:
            col += 1
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][col]
        A[r] = [x / pv for x in A[r]]
        for i in range(m):
            if i == r or A[i][col] == 0:
                continue
            fac = A[i][col]
            A[i] = [A[i][k] - fac * A[r][k] for k in range(d + 1)]
        used[col] = True
        pivot_col[r] = col
        r += 1
        col += 1
    for i in range(r, m):
        if A[i][d] != 0:
            return None
    coords = [Fraction(0)] * d
    for i, pc in enumerate(pivot_col):
        if pc < 0:
            continue
        coords[pc] = A[i][d]
    return coords


def restriction_matrix(MT, basis):
    d = len(basis)
    C = [[Fraction(0)] * d for _ in range(d)]
    for j, b in enumerate(basis):
        img = mat_vec(MT, b)
        coords = express_in_basis(basis, img)
        if coords is None:
            return None
        for i in range(d):
            C[i][j] = coords[i]
    return C


def frac_mat_mul(A, B):
    n = len(A)
    C = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(n):
                C[i][j] += aik * B[k][j]
    return C


def inf_norm(C):
    """Induced ∞-norm: max absolute row sum."""
    best = Fraction(0)
    for row in C:
        s = sum(abs(x) for x in row)
        if s > best:
            best = s
    return best


def inf_norm_int(vec):
    return max(abs(x) for x in vec)


def try_sympy_spectral_radius(C):
    try:
        import sympy as sp
    except ImportError:
        return None
    M = sp.Matrix([[sp.Rational(int(x.numerator), int(x.denominator)) for x in row] for row in C])
    try:
        evs = M.eigenvals()
    except Exception:
        return None
    best = sp.Integer(0)
    for e in evs:
        val = sp.Abs(e).evalf(60)
        if val > best:
            best = val
    try:
        return Fraction(str(sp.N(best, 30))) if best != 0 else Fraction(0)
    except Exception:
        return None


def charpoly_integer(C):
    """Characteristic polynomial of a Fraction matrix, monic in Z[x] after clearing."""
    try:
        import sympy as sp
    except ImportError:
        return None
    M = sp.Matrix([[sp.Rational(int(x.numerator), int(x.denominator)) for x in row] for row in C])
    p = M.charpoly(sp.symbols("t"))
    return str(p.as_expr())


def contraction_certificate(library, tau):
    """Exact common contraction of imbalance for every directive.

    Build E = smallest Q-subspace containing v and invariant under both M_i^T.
    Restrict A_i = M_i^T|_E. A strict certificate is a submultiplicative-norm
    bound JSR({A0,A1}) ≤ ρ < 2, together with min |σ(a)| ≥ 2.

    This is not a frequency measurement of a finite prefix.
    """
    out = {
        "ok": False,
        "reason": "",
        "dim": 0,
        "min_len": None,
        "rho_upper": None,
        "rho_lower": None,
        "spectral_radii": [],
        "commute": None,
        "charpolys": [],
        "length_ge_2k": False,
        "incomplete_images": False,
    }
    if len(library) != 2:
        out["reason"] = "library size is not 2"
        return out
    for sigma in library:
        if not sigma_complete(sigma):
            out["incomplete_images"] = True
            out["reason"] = "incomplete images: not every depth-k tile is defined"
            return out
        if min_image_len(sigma) < 2:
            out["reason"] = "an image has length < 2"
            return out
    out["min_len"] = min(min_image_len(s) for s in library)
    out["length_ge_2k"] = out["min_len"] >= 2

    M0 = incidence_matrix(library[0])
    M1 = incidence_matrix(library[1])
    M0T, M1T = transpose(M0), transpose(M1)
    v = [Fraction(x) for x in v_imbalance(tau)]
    basis = krylov_basis(M0T, M1T, v)
    out["dim"] = len(basis)
    if not basis:
        out["reason"] = "empty imbalance subspace"
        return out

    C0 = restriction_matrix(M0T, basis)
    C1 = restriction_matrix(M1T, basis)
    if C0 is None or C1 is None:
        out["reason"] = "restriction failed (E not invariant — bug)"
        return out

    d = len(basis)
    if d == 1:
        lam0, lam1 = C0[0][0], C1[0][0]
        out["commute"] = True
        out["eigenvalues_1d"] = [str(lam0), str(lam1)]
        rho = max(abs(lam0), abs(lam1))
        out["rho_upper"] = str(rho)
        out["rho_lower"] = str(rho)
        if rho < 2:
            out["ok"] = True
            out["reason"] = "1-dimensional imbalance subspace, |λ_i| < 2"
        else:
            out["reason"] = "1-dimensional imbalance subspace, |λ| ≥ 2"
        return out

    comm = frac_mat_mul(C0, C1)
    comm2 = frac_mat_mul(C1, C0)
    out["commute"] = comm == comm2
    out["charpolys"] = [charpoly_integer(C0), charpoly_integer(C1)]

    spr0 = try_sympy_spectral_radius(C0)
    spr1 = try_sympy_spectral_radius(C1)
    out["spectral_radii"] = [
        None if spr0 is None else str(spr0),
        None if spr1 is None else str(spr1),
    ]
    rho_lower = Fraction(0)
    if spr0 is not None:
        rho_lower = max(rho_lower, spr0)
    if spr1 is not None:
        rho_lower = max(rho_lower, spr1)
    out["rho_lower"] = str(rho_lower)

    if rho_lower >= 2:
        out["reason"] = "some restriction has spectral radius ≥ 2"
        return out

    # Operator-norm upper bounds on products (submultiplicative ∞-norm).
    # JSR ≤ inf_k max_{|w|=k} ||P_w||^{1/k} ≤ max_{|w|=k} ||P_w||^{1/k}.
    mats = (C0, C1)
    rho_upper = None
    products = [[[[Fraction(1 if i == j else 0) for j in range(d)] for i in range(d)]]]
    best_k = None
    for k in range(1, 13):
        nxt = []
        max_norm = Fraction(0)
        for P in products[-1]:
            for A in mats:
                Q = frac_mat_mul(A, P)
                nxt.append(Q)
                nm = inf_norm(Q)
                if nm > max_norm:
                    max_norm = nm
        products.append(nxt)
        if max_norm == 0:
            rho_upper = Fraction(0)
            best_k = k
            break
        # ρ ≤ max_norm^{1/k}. Compare max_norm ?< 2^k.
        # Store the smallest such proven bound of the form max_norm^{1/k}.
        if max_norm < (Fraction(2) ** k):
            # A rational upper bound: 2 * (max_norm / 2^k) is < 2, but we
            # want any ρ<2. Using ρ = 2 * (1 - 1/2^{k+2}) is sloppy; record
            # that ||P||_∞ < 2^k so JSR < 2, and give a numeric float string
            # only as a witness of the gap, plus the exact comparison.
            rho_upper = ("lt2_via_inf_norm", k, str(max_norm))
            best_k = k
            break
        if k >= 8:
            products[-1] = nxt  # 2^12 = 4096 matrices of size ≤4 is OK
    out["norm_bound"] = None if rho_upper is None else {
        "kind": rho_upper[0],
        "k": rho_upper[1],
        "max_inf_norm": rho_upper[2],
    }

    # Direct orbit of v: max |imbalance| of depth-k tiles.
    orbit = [v]
    tile_imbalance_max = []
    for k in range(1, 11):
        nxt = []
        mx = 0
        for vec in orbit:
            for MT in (M0T, M1T):
                w = mat_vec(MT, vec)
                nxt.append(w)
                mx = max(mx, inf_norm_int(w))
        tile_imbalance_max.append(int(mx))
        orbit = nxt
    out["max_abs_imbalance_by_depth"] = tile_imbalance_max

    if out["commute"] and spr0 is not None and spr1 is not None:
        rho = max(spr0, spr1)
        out["rho_upper"] = str(rho)
        if rho < 2:
            out["ok"] = True
            out["reason"] = "commuting restrictions; JSR = max spectral radius < 2"
            return out

    if rho_upper is not None:
        out["rho_upper"] = "<2"
        out["ok"] = True
        out["reason"] = (
            f"∞-norm of every length-{best_k} product on E is < 2^{best_k}, "
            "hence JSR < 2"
        )
        return out

    # No strict bound < 2. If some product already has spr ≥ 2, kill.
    if rho_lower >= 2:
        out["reason"] = "JSR lower bound ≥ 2"
        return out
    out["reason"] = (
        "no exact common contraction: could not prove JSR < 2 on the "
        "imbalance subspace (and no matrix had spectral radius ≥ 2 either)"
    )
    return out


# ---------------------------------------------------------------------------
# Hierarchical search
# ---------------------------------------------------------------------------

def parse_with_library(seq, library, tau, is_bits, deadline, seed_max=SEED_MAX):
    """True if seq admits an S-adic parse using only `library` down to a short seed."""
    stack = [(seq, is_bits, 0)]
    seen = set()
    while stack:
        if time.monotonic() >= deadline:
            return False
        cur, bits_flag, depth = stack.pop()
        if depth > MAX_DEPTH:
            continue
        key = (bytes(cur), bits_flag)
        if key in seen:
            continue
        seen.add(key)
        if (not bits_flag) and len(cur) <= seed_max:
            return True
        if len(cur) < 2:
            continue
        for sigma in library:
            pres = desubstitute_frozen(cur, sigma, tau if bits_flag else None)
            for pre in pres:
                stack.append((pre, False, depth + 1))
    return False


def deepen_sadic(word, library, tau, is_bits, deadline, stats, depth=0):
    """Yield libraries of size 2 that parse `word` down to a short seed."""
    if time.monotonic() >= deadline:
        return
    if depth > MAX_DEPTH:
        return
    if (not is_bits) and len(word) <= SEED_MAX:
        if 1 <= len(library) <= 2:
            yield [sigma_key(s) for s in library], bytes(word)
        return
    if len(word) < 2:
        return

    for sigma in library:
        if time.monotonic() >= deadline:
            return
        pres = desubstitute_frozen(word, sigma, tau if is_bits else None)
        stats["frozen_desub_hits"] = stats.get("frozen_desub_hits", 0) + len(pres)
        for pre in pres:
            yield from deepen_sadic(
                pre, library, tau, False, deadline, stats, depth + 1
            )

    if len(library) >= 2:
        return
    cache = stats.setdefault("_infer_cache", {})
    ckey = (bytes(word), tau if is_bits else None, bool(is_bits))
    if ckey in cache:
        inferred = cache[ckey]
    elif is_bits:
        inferred = infer_from_bits(word, tau, deadline, stats)
        cache[ckey] = inferred
    else:
        inferred = infer_from_letters(word, deadline, stats)
        cache[ckey] = inferred
    stats["inferred_at_depth_%d" % depth] = stats.get("inferred_at_depth_%d" % depth, 0) + len(inferred)
    seen_local = set()
    for sigma, pre in inferred:
        if time.monotonic() >= deadline:
            return
        if sigma in seen_local:
            continue
        seen_local.add(sigma)
        skip = False
        for existing in library:
            if sigma_key(existing) == sigma:
                skip = True
                break
        if skip:
            continue
        new_lib = list(library) + [sigma]
        yield from deepen_sadic(pre, new_lib, tau, False, deadline, stats, depth + 1)


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def self_checks(deadline):
    checks = {}
    # Packed generator matches experiment.center_bits.
    a = packed_center_bits(256)
    b = bytes(experiment_center_bits(256))
    checks["packed_matches_experiment_256"] = a == b

    tau = (0, 0, 1, 1)
    sigma0 = (
        bytes((0, 2)),
        bytes((1, 3)),
        bytes((2, 0)),
        bytes((3, 1)),
    )
    sigma1 = (
        bytes((0, 1, 2)),
        bytes((0, 1)),
        bytes((2, 3)),
        bytes((2, 3, 0)),
    )
    library = [sigma0, sigma1]
    checks["synthetic_nonuniform"] = library_nonuniform(library)
    checks["synthetic_min_len"] = min(min_image_len(s) for s in library) == 2

    seed = bytes((0,))
    directive = (0, 1, 0, 1, 0, 1, 0, 1)
    w = expand_directive(seed, directive, library)
    bits = coded_image(w, tau)
    checks["synthetic_expand_len"] = len(bits)
    recovered = list(
        deepen_sadic(bits, [], tau, True, deadline, {}, depth=0)
    )
    checks["synthetic_parser_recovers_two_morphisms"] = any(
        {sigma_key(sigma0), sigma_key(sigma1)} == set(lib) for lib, _ in recovered
    ) or any(len(lib) == 2 for lib, _ in recovered)
    checks["synthetic_n_recovered"] = len(recovered)
    checks["synthetic_frozen_parse"] = parse_with_library(
        bits, library, tau, True, deadline
    )

    # Length-2 finest enumeration agrees with pairing of the synthetic bits
    # when those bits have even length.
    if len(bits) % 2 == 0:
        cands = length2_finest_candidates(bits, tau)
        checks["length2_enum_on_synthetic"] = len(cands)
        checks["length2_enum_includes_sigma0"] = any(
            s == sigma_key(sigma0) for s, _ in cands
        )

    cert = contraction_certificate(library, tau)
    checks["synthetic_contraction_ran"] = True
    checks["synthetic_contraction_ok"] = cert["ok"]
    checks["synthetic_contraction_reason"] = cert["reason"]
    checks["synthetic_contraction_dim"] = cert["dim"]

    # A deliberately expanding imbalance: both morphisms copy a letter
    # three times (imbalance multiplies by 3).
    bad0 = (bytes((2, 2, 2)), bytes((2, 2, 2)), bytes((2, 2, 2)), bytes((2, 2, 2)))
    bad1 = (bytes((2, 2)), bytes((3, 3)), bytes((2, 2, 2)), bytes((3, 3, 3)))
    bad_cert = contraction_certificate([bad0, bad1], tau)
    checks["expanding_rejected"] = (not bad_cert["ok"])
    checks["expanding_reason"] = bad_cert["reason"]
    return checks


def digram_report(bits):
    n = (len(bits) // 2) * 2
    counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    for i in range(0, n, 2):
        key = f"{bits[i]}{bits[i+1]}"
        counts[key] += 1
    pairs = []
    for i in range(0, n, 2):
        pairs.append((bits[i] << 1) | bits[i + 1])
    super_types = set()
    for i in range(0, len(pairs) - 1, 2):
        super_types.add((pairs[i], pairs[i + 1]))
    return {
        "n_even": n,
        "digram_counts": counts,
        "n_distinct_digrams": sum(1 for v in counts.values() if v),
        "n_distinct_paired_digrams": len(super_types),
        "length2_desub_of_digram_word_possible": len(super_types) <= ALPH,
    }


# ---------------------------------------------------------------------------
# Main search
# ---------------------------------------------------------------------------

def search(bits1024, bits16384, deadline):
    stats = {
        "n_tau": 0,
        "n_finest": 0,
        "n_parse_1024": 0,
        "n_two_morph_nonuniform": 0,
        "n_contracting": 0,
        "n_extend_16384": 0,
        "length2_finest_enumerated": 0,
        "mixed_finest_inferred": 0,
    }
    libraries_1024 = []
    seen_libs = set()
    kill = None

    def consider(lib, seed, tau, source):
        key = (tau, tuple(lib))
        if key in seen_libs:
            return
        if len(lib) != 2 or lib[0] == lib[1] or not library_nonuniform(lib):
            return
        if any(not sigma_complete(s) for s in lib):
            # Incomplete: not every depth-k tile exists.
            return
        seen_libs.add(key)
        stats["n_two_morph_nonuniform"] += 1
        rec = {
            "tau": list(tau),
            "sigma0": sigma_json(lib[0]),
            "sigma1": sigma_json(lib[1]),
            "seed": "".join(str(x) for x in seed),
            "source": source,
        }
        libraries_1024.append(rec)
        stats["n_parse_1024"] += 1

    # --- Slice A: exhaustive uniform length-2 finest, then S-adic on the preimage.
    for tau in TAUS:
        if time.monotonic() >= deadline:
            break
        stats["n_tau"] += 1
        cands = length2_finest_candidates(bits1024, tau)
        stats["length2_finest_enumerated"] += len(cands)
        stats["n_finest"] += len(cands)
        # Group by preimage so coarser search is not repeated for every lift.
        by_pre = {}
        for sigma, pre in cands:
            by_pre.setdefault(pre, []).append(sigma)
        for pre, sigmas in by_pre.items():
            if time.monotonic() >= deadline:
                break
            if len(libraries_1024) >= MAX_LIBRARIES:
                break
            # Coarser S-adic on the producer word, starting with empty library
            # of coarser morphisms; each surviving pair is (σ_fine, σ_coarse)
            # with σ_fine ranging over lifts that share this preimage.
            for lib, seed in deepen_sadic(pre, [], tau, False, deadline, stats):
                if time.monotonic() >= deadline:
                    stats.pop("_infer_cache", None)
                    return libraries_1024, stats, "budget"
                if len(lib) == 1:
                    for sigma0 in sigmas:
                        consider(
                            [sigma0, lib[0]],
                            seed,
                            tau,
                            "length2_finest+one_coarser",
                        )
                elif len(lib) == 2:
                    for sigma0 in sigmas:
                        if sigma0 in lib:
                            consider(lib, seed, tau, "length2_coarser_includes_fine")
            for sigma0 in sigmas:
                if time.monotonic() >= deadline:
                    break
                if len(libraries_1024) >= MAX_LIBRARIES:
                    break
                for lib, seed in deepen_sadic(
                    pre, [sigma0], tau, False, deadline, stats
                ):
                    if len(lib) == 2:
                        consider(lib, seed, tau, "length2_finest_in_library")

    # --- Slice B: mixed-length finest (left-greedy lifts), remaining budget.
    if time.monotonic() < deadline and len(libraries_1024) < MAX_LIBRARIES:
        for tau in TAUS:
            if time.monotonic() >= deadline:
                break
            inferred = infer_from_bits(bits1024, tau, deadline, stats, greedy_new=True)
            stats["mixed_finest_inferred"] += len(inferred)
            stats["n_finest"] += len(inferred)
            for sigma, pre in inferred:
                if time.monotonic() >= deadline:
                    break
                if len(libraries_1024) >= MAX_LIBRARIES:
                    break
                for lib, seed in deepen_sadic(
                    pre, [sigma], tau, False, deadline, stats
                ):
                    consider(lib, seed, tau, "mixed_finest")

    if time.monotonic() >= deadline and not libraries_1024:
        stats.pop("_infer_cache", None)
        return libraries_1024, stats, "budget"

    if not libraries_1024:
        stats.pop("_infer_cache", None)
        return libraries_1024, stats, "no_parse_1024"

    contracting = []
    for rec in libraries_1024:
        if time.monotonic() >= deadline:
            kill = "budget"
            break
        lib = [digits_to_sigma(rec["sigma0"]), digits_to_sigma(rec["sigma1"])]
        tau = tuple(rec["tau"])
        cert = contraction_certificate(lib, tau)
        rec["contraction"] = {
            k: (v if isinstance(v, (str, int, bool, list, type(None), dict)) else str(v))
            for k, v in cert.items()
        }
        if cert["ok"]:
            stats["n_contracting"] += 1
            contracting.append((rec, lib, tau))

    if kill == "budget" and not contracting:
        stats.pop("_infer_cache", None)
        return libraries_1024, stats, "budget"

    if not contracting:
        stats.pop("_infer_cache", None)
        return libraries_1024, stats, "no_contraction"

    for rec, lib, tau in contracting:
        if time.monotonic() >= deadline:
            stats.pop("_infer_cache", None)
            return libraries_1024, stats, "budget"
        ok = parse_with_library(bits16384, lib, tau, True, deadline)
        rec["extends_16384"] = ok
        if ok:
            stats["n_extend_16384"] += 1

    stats.pop("_infer_cache", None)
    if stats["n_extend_16384"] == 0:
        return libraries_1024, stats, "no_extend_16384"

    return libraries_1024, stats, "spacetime_lift_open"


def digits_to_sigma(js):
    out = []
    for item in js:
        if item is None:
            out.append(None)
        else:
            out.append(bytes(int(ch) for ch in item))
    return tuple(out)


def main():
    sys.setrecursionlimit(3000)
    t0 = time.monotonic()
    deadline = t0 + BUDGET_SEC
    checks = self_checks(deadline)
    bits1024 = packed_center_bits(PARSE_N)
    bits16384 = packed_center_bits(EXTEND_N)
    checks["prefix_1024_matches_experiment"] = bits1024 == bytes(
        experiment_center_bits(PARSE_N)
    )
    checks["prefix_16384_starts_with_1024"] = bits16384.startswith(bits1024)
    diag1024 = digram_report(bits1024)
    diag16384 = digram_report(bits16384)

    libraries, stats, kill = search(bits1024, bits16384, deadline)
    elapsed = time.monotonic() - t0
    budget_expired = elapsed >= BUDGET_SEC - 1e-3 or kill == "budget"

    if budget_expired and stats["n_parse_1024"] == 0:
        kill = "budget"
    elif stats["n_parse_1024"] == 0:
        kill = "no_parse_1024"
    elif stats["n_contracting"] == 0:
        kill = "no_contraction"
    elif stats["n_extend_16384"] == 0:
        kill = "no_extend_16384"
    elif kill == "spacetime_lift_open":
        # Prefix certificates are not spacetime tiles. For this freeze the
        # experiment stops at the prefix+contraction test; a surviving
        # library would still have to be lifted. If none survived extension,
        # that kill already fired. If some survived, the lift remains open
        # and is recorded as a kill against a prize argument, not as a
        # missing search.
        pass

    dump = {
        "problem": 2,
        "attack": "nonuniform substitution tilings / S-adic imbalance contraction",
        "prize_claim": False,
        "finite_parse_is_not_a_density_proof": True,
        "freeze": {
            "letters": 4,
            "n_substitutions": 2,
            "image_lengths": [2, 3],
            "nonuniform_required": True,
            "parse_n": PARSE_N,
            "extend_n": EXTEND_N,
            "budget_sec": BUDGET_SEC,
            "coding_subclass": [
                "tau=(0,0,1,1)  # 2+2",
                "tau=(0,0,0,1)  # 3+1",
                "tau=(0,1,1,1)  # 1+3",
            ],
            "search_subclass": (
                "S-adic (one morphism per level). Slice A: exhaustive uniform "
                "length-2 finest morphisms (all letter-lifts of the digram "
                "code) followed by left-greedy inference of a second morphism "
                "on the producer word, then recursive frozen desubstitution "
                "to a seed of length ≤ 4. Slice B: left-greedy mixed-length "
                "(2 or 3) finest inference with letter-lifts, then the same "
                "coarser search. New producer types are opened only when no "
                "bound image matches, except on words of length ≤ 96 (letters) "
                "or ≤ 256 (bits). This is not a loop over all 80^8 morphisms."
            ),
        },
        "self_checks": checks,
        "digrams_1024": diag1024,
        "digrams_16384": diag16384,
        "stats": stats,
        "n_libraries_1024": len(libraries),
        "libraries": libraries[:MAX_LIBRARIES],
        "kill": kill,
        "budget_expired": budget_expired,
        "elapsed_sec": round(elapsed, 3),
    }

    out_path = Path(__file__).resolve().with_suffix(".json")
    out_path.write_text(json.dumps(dump, indent=2) + "\n")
    print(json.dumps({
        "kill": kill,
        "n_parse_1024": stats["n_parse_1024"],
        "n_contracting": stats["n_contracting"],
        "n_extend_16384": stats["n_extend_16384"],
        "elapsed_sec": dump["elapsed_sec"],
        "json": str(out_path),
        "self_checks_packed": checks.get("packed_matches_experiment_256"),
        "synthetic_parser": checks.get("synthetic_parser_recovers_two_morphisms"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
