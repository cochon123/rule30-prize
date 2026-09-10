"""q=8: search for a local invariant K excluding the vacuum quotient I.

Does not modify strip_graph.py, strip_extend.py, or period9_sigma.py.

Question: does there exist a set K given by relations on 2 or 3 neighboring
S-symbols with
    all initial streams ⊆ K,  H(K) ⊆ K,  K contains no symbol in I?
If yes, consistent reconstruction never enters I, uniformly in depth.

This file mines candidate relations from consistent blocks, then checks
preservation on every locally compatible block of the candidate — not only
on observed streams. If short-block closure already admits I, the abstraction
fails and extending the depth table is not progress.

Run: python3 research/period9_invariant.py
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period9_sigma import (
    W0,
    W1,
    bit,
    bits9_lsb,
    build_succ,
    build_Z,
    decode,
    encode,
    pair_step,
)

NSTATE = 1 << 18
MASK9 = 0x1FF


def H(s, t):
    """S_{k+1}(n) = H(S_k(n), S_k(n+1)). Uses only wrap = curr[0] of t."""
    prev, curr = decode(s)
    wrap = t & 1
    return encode(curr, pair_step(prev, curr, wrap))


def init_symbol(sigma):
    return encode(W0(), W1(sigma))


def gf2_nullspace(rows, nbits):
    """rows: iterable of ints < 2^{nbits}. Return list of nullspace basis vectors."""
    A = list(rows)
    if not A:
        return [1 << i for i in range(nbits)]
    pivots = []
    used = []
    for col in range(nbits):
        mask = 1 << col
        piv = None
        for i, r in enumerate(A):
            if i in used:
                continue
            if r & mask:
                piv = i
                break
        if piv is None:
            continue
        used.append(piv)
        pivots.append(col)
        rp = A[piv]
        for i, r in enumerate(A):
            if i != piv and (r & mask):
                A[i] ^= rp
    pivot_set = set(pivots)
    basis = []
    for col in range(nbits):
        if col in pivot_set:
            continue
        v = 1 << col
        for pcol, piv in zip(pivots, used):
            if A[piv] & (1 << col):
                v |= 1 << pcol
        basis.append(v)
    return basis


def pack2(a, b):
    return (a << 18) | b


def unpack2(p):
    return (p >> 18) & (NSTATE - 1), p & (NSTATE - 1)


def collect_consistent(kmax, nsites=3):
    """All n-site S-blocks at each depth k=1..kmax.

    Length needed: L = k + nsites. Enumerate all 2^L sigma strings.
    """
    t0 = time.monotonic()
    by_depth = []
    for k in range(1, kmax + 1):
        L = k + nsites
        ncfg = 1 << L
        blocks2 = set()
        blocks3 = set() if nsites >= 3 else None
        symbols = set()
        in_I = 0
        # iterative reconstruction: W[d][n] as 9-bit ints
        # For each sigma mask, build the triangle.
        w0 = W0()
        for mask in range(ncfg):
            sig = [(mask >> n) & 1 for n in range(L)]
            # W[0][n] = w0 for all n
            # W[1][n] = W1(sig[n]) for n < L
            prev_row = [w0] * (L + 1)
            curr_row = [W1(sig[n]) if n < L else 0 for n in range(L + 1)]
            for d in range(1, k):
                nxt = [0] * (L + 1)
                for n in range(L - d):
                    nxt[n] = pair_step(prev_row[n], curr_row[n], bit(curr_row[n + 1], 0))
                prev_row, curr_row = curr_row, nxt
            # now prev_row = W_{k-1}, curr_row = W_k
            ss = [encode(prev_row[n], curr_row[n]) for n in range(nsites)]
            for s in ss:
                symbols.add(s)
            blocks2.add((ss[0], ss[1]))
            if nsites >= 3:
                blocks3.add((ss[0], ss[1], ss[2]))
        by_depth.append(
            {
                "k": k,
                "n_symbols": len(symbols),
                "n_2blocks": len(blocks2),
                "n_3blocks": len(blocks3) if blocks3 is not None else None,
                "blocks2": blocks2,
                "blocks3": blocks3,
                "symbols": symbols,
            }
        )
        print(
            f"  collect k={k} L={L} |S|={len(symbols)} |P2|={len(blocks2)} "
            f"|P3|={len(blocks3) if blocks3 is not None else '-'} "
            f"t={time.monotonic()-t0:.2f}s",
            flush=True,
        )
    return by_depth


def wraps_into_I(s, I):
    """Which wrap bits send s into I."""
    out = []
    for w in (0, 1):
        t = w  # any t with t&1 == w; H only reads that bit
        if I[H(s, t)]:
            out.append(w)
    return out


def analyze_I_entry(I, succ0, succ1):
    """For each s, which wraps land in I; and the function f on I."""
    f = [-1] * 512
    I_states = []
    for s in range(NSTATE):
        if I[s]:
            p, c = decode(s)
            I_states.append(s)
            f[p] = c
    assert all(x >= 0 for x in f)
    n_enter0 = n_enter1 = n_enter_both = n_enter_none = 0
    enter = [0] * NSTATE  # bitmask of wraps into I
    for s in range(NSTATE):
        m = 0
        if I[succ0[s]]:
            m |= 1
        if I[succ1[s]]:
            m |= 2
        enter[s] = m
        if m == 0:
            n_enter_none += 1
        elif m == 1:
            n_enter0 += 1
        elif m == 2:
            n_enter1 += 1
        else:
            n_enter_both += 1
    return {
        "f": f,
        "enter": enter,
        "n_enter_none": n_enter_none,
        "n_enter_wrap0_only": n_enter0,
        "n_enter_wrap1_only": n_enter1,
        "n_enter_both": n_enter_both,
        "n_in_I": 512,
    }


def linear_on_blocks(blocks, nbits_per, nparts):
    rows = []
    for blk in blocks:
        v = 0
        for i, s in enumerate(blk):
            v |= s << (i * nbits_per)
        rows.append(v)
    ns = gf2_nullspace(rows, nbits_per * nparts)
    return ns


def bits_of(s, n=18):
    return [(s >> i) & 1 for i in range(n)]


def describe_linear(basis, nbits_per, nparts, labels=None):
    """Human-readable XOR relations."""
    if labels is None:
        labels = []
        for p in range(nparts):
            tag = ["L", "M", "R"][p] if nparts <= 3 else str(p)
            for i in range(nbits_per):
                which = "p" if i < 9 else "c"
                labels.append(f"{tag}.{which}{i % 9}")
    rels = []
    for v in basis:
        terms = [labels[i] for i in range(len(labels)) if (v >> i) & 1]
        rels.append(" ⊕ ".join(terms) + " = 0")
    return rels


def affine_hull_size(blocks, nbits):
    """Dimension of affine hull of the packed blocks."""
    blocks = list(blocks)
    if not blocks:
        return 0, 0
    origin = blocks[0]
    rows = [b ^ origin for b in blocks]
    ns = gf2_nullspace(rows, nbits)
    dim = nbits - len(ns)
    return dim, len(ns)


def close_2blocks(pairs, I, max_new=5_000_000, max_rounds=20):
    """Iterate R |-> {(H(a,b), H(b,c)) : (a,b),(b,c) in R} union R.

    Returns whether I is hit, new symbol counts, and whether it stabilized.
    """
    R = set(pairs)
    symbols = set()
    for a, b in R:
        symbols.add(a)
        symbols.add(b)
    hit_I = any(I[s] for s in symbols)
    history = [
        {
            "round": 0,
            "n_pairs": len(R),
            "n_symbols": len(symbols),
            "n_in_I": sum(1 for s in symbols if I[s]),
        }
    ]
    if hit_I:
        return True, history, R, symbols, "seed already meets I"

    # index: left -> list of right
    for rnd in range(1, max_rounds + 1):
        succ = defaultdict(list)
        for a, b in R:
            succ[a].append(b)
        new_pairs = []
        new_sym = []
        hit = False
        # locally compatible triples: (a,b) and (b,c) in R
        # group by middle b
        rights_of = succ
        lefts_of = defaultdict(list)
        for a, b in R:
            lefts_of[b].append(a)
        middles = set(rights_of.keys()) & set(lefts_of.keys())
        for b in middles:
            lefts = lefts_of[b]
            rights = rights_of[b]
            for a in lefts:
                hab = H(a, b)
                for c in rights:
                    hbc = H(b, c)
                    pair = (hab, hbc)
                    if pair not in R:
                        new_pairs.append(pair)
                        if I[hab] or I[hbc]:
                            hit = True
                        if hab not in symbols:
                            new_sym.append(hab)
                        if hbc not in symbols:
                            new_sym.append(hbc)
        # also include images even if pair already known? we care about union-close
        # The invariant H(K)⊆K for the 2-shift of R requires the IMAGE pairs
        # to already lie in R. So we add them.
        uniq_new = []
        seen_add = set()
        for p in new_pairs:
            if p not in R and p not in seen_add:
                seen_add.add(p)
                uniq_new.append(p)
        for p in uniq_new:
            R.add(p)
            a, b = p
            symbols.add(a)
            symbols.add(b)
        nI = sum(1 for s in symbols if I[s])
        history.append(
            {
                "round": rnd,
                "n_new_pairs": len(uniq_new),
                "n_pairs": len(R),
                "n_symbols": len(symbols),
                "n_in_I": nI,
                "hit_I": hit or nI > 0,
            }
        )
        print(
            f"    close2 round {rnd}: new_pairs={len(uniq_new)} |R|={len(R)} "
            f"|S|={len(symbols)} nI={nI}",
            flush=True,
        )
        if hit or nI > 0:
            return True, history, R, symbols, "H-closure admits I"
        if not uniq_new:
            return False, history, R, symbols, "stabilized I-free"
        if len(R) > max_new:
            return False, history, R, symbols, "aborted: pair set too large (still I-free)"
    return False, history, R, symbols, "max rounds, still I-free, not stabilized"


def close_3blocks(triples, I, max_new=2_000_000, max_rounds=12):
    """4-site local compatibility: (a,b,c) and (b,c,d) in T
    produce (H(a,b), H(b,c), H(c,d)).
    """
    T = set(triples)
    symbols = set()
    for a, b, c in T:
        symbols.add(a)
        symbols.add(b)
        symbols.add(c)
    history = [
        {
            "round": 0,
            "n_triples": len(T),
            "n_symbols": len(symbols),
            "n_in_I": sum(1 for s in symbols if I[s]),
        }
    ]
    if any(I[s] for s in symbols):
        return True, history, T, symbols, "seed already meets I"

    for rnd in range(1, max_rounds + 1):
        by_bc = defaultdict(list)  # (b,c) -> list of a such that (a,b,c) in T
        by_ab = defaultdict(list)  # (a,b) wait: (b,c) -> list of d with (b,c,d)
        for a, b, c in T:
            by_bc[(b, c)].append(a)
        rights = defaultdict(list)
        for a, b, c in T:
            rights[(a, b)].append(c)  # not quite
        # (b,c,d) in T: index by (b,c)
        tail = defaultdict(list)
        for a, b, c in T:
            tail[(a, b)].append(c)
        # better: tail of (b,c) is d with (b,c,d)
        tail = defaultdict(list)
        for x, y, z in T:
            tail[(x, y)].append(z)

        new = []
        hit = False
        for a, b, c in T:
            for d in tail.get((b, c), ()):
                ha, hb, hc = H(a, b), H(b, c), H(c, d)
                trip = (ha, hb, hc)
                if trip not in T:
                    new.append(trip)
                    if I[ha] or I[hb] or I[hc]:
                        hit = True
        uniq = []
        seen_add = set()
        for t in new:
            if t not in T and t not in seen_add:
                seen_add.add(t)
                uniq.append(t)
        for t in uniq:
            T.add(t)
            for s in t:
                symbols.add(s)
        nI = sum(1 for s in symbols if I[s])
        history.append(
            {
                "round": rnd,
                "n_new_triples": len(uniq),
                "n_triples": len(T),
                "n_symbols": len(symbols),
                "n_in_I": nI,
                "hit_I": hit or nI > 0,
            }
        )
        print(
            f"    close3 round {rnd}: new={len(uniq)} |T|={len(T)} "
            f"|S|={len(symbols)} nI={nI}",
            flush=True,
        )
        if hit or nI > 0:
            return True, history, T, symbols, "H-closure admits I"
        if not uniq:
            return False, history, T, symbols, "stabilized I-free"
        if len(T) > max_new:
            return False, history, T, symbols, "aborted: triple set too large (still I-free)"
    return False, history, T, symbols, "max rounds, still I-free, not stabilized"


def candidate_from_linear(basis, nbits, observed_origin=0):
    """All vectors in the linear (actually affine if we use observed as check)
    nullspace. Too big to enumerate unless codim is high.
    """
    return len(basis), nbits - len(basis)


def wrap_function_of_left(blocks2):
    """For each left symbol, the set of wraps (right.curr[0]) seen."""
    by_left = defaultdict(set)
    for a, b in blocks2:
        by_left[a].add(b & 1)
    n1 = sum(1 for v in by_left.values() if len(v) == 1)
    n2 = sum(1 for v in by_left.values() if len(v) == 2)
    return {"n_left": len(by_left), "n_unique_wrap": n1, "n_both_wraps": n2}


def check_linear_preservation(basis, nparts, I, sample_limit=20000):
    """If dim is small enough, enumerate the affine space of n-blocks and
    test H-preservation and I-exclusion. nparts=2 or 3, each 18 bits.
    """
    nbits = 18 * nparts
    dim = nbits - len(basis)
    return {"n_relations": len(basis), "dim": dim, "enumerable": dim <= 22}


def enumerate_kernel_and_test(basis, nparts, I, origin=0, max_dim=20):
    """Enumerate affine space origin + ker(basis) of n-blocks.
    For 2-blocks: check every compatible triple in the 2-shift, whether
    H-image pair still satisfies the relations and avoids I.
    For 3-blocks: check every compatible 4-tuple.
    """
    nbits = 18 * nparts
    dim = nbits - len(basis)
    if dim > max_dim:
        return {"skipped": True, "dim": dim}
    free = []
    for i in range(nbits):
        if all(((b >> i) & 1) == 0 for b in basis) or True:
            pass
    # Reconstruct free variables: columns without a pivot in the basis-as-rows
    # of the dual. We have basis of the NULLSPACE of observed rows.
    # A vector v is in the span-orthogonal, i.e. observed satisfy b·x=0.
    # Allowed x: b·x = 0 for all b in basis, AND we should pin affine:
    # actually observed may be affine. Use origin: allowed = origin + linear
    # solutions of b·x = b·origin for each b. If relations are linear homogeneous
    # on the raw bits, origin=0.
    # Find free vars and express pivots.
    # Gaussian-elim the basis rows themselves to get a parametrization of {x: Bx=0}.
    B = list(basis)
    nrel = len(B)
    # row-reduce B
    pivots = []
    used = []
    for col in range(nbits):
        mask = 1 << col
        piv = None
        for i, r in enumerate(B):
            if i in used:
                continue
            if r & mask:
                piv = i
                break
        if piv is None:
            continue
        used.append(piv)
        pivots.append(col)
        rp = B[piv]
        for i, r in enumerate(B):
            if i != piv and (r & mask):
                B[i] ^= rp
    pivot_set = set(pivots)
    free_cols = [c for c in range(nbits) if c not in pivot_set]
    assert len(free_cols) == dim, (len(free_cols), dim, len(pivots))
    # x_pivot = linear function of free, from reduced B
    # For each pivot row, B[piv] has 1 at pivot and some free cols
    pivot_row = {col: B[piv] for col, piv in zip(pivots, used)}

    def vec_from_free(fv):
        x = 0
        for j, col in enumerate(free_cols):
            if (fv >> j) & 1:
                x |= 1 << col
        for col, row in pivot_row.items():
            # row · x = 0, row has 1 at col
            sbit = 0
            r = row ^ (1 << col)
            y = x
            while r:
                lsb = r & -r
                bitpos = lsb.bit_length() - 1
                sbit ^= (x >> bitpos) & 1
                r ^= lsb
            if sbit:
                x |= 1 << col
        return x

    n = 1 << dim
    # parse n-blocks
    def parse(x):
        return tuple((x >> (18 * i)) & (NSTATE - 1) for i in range(nparts))

    allowed = [parse(vec_from_free(fv) ^ origin) for fv in range(n)]
    # if origin is used as affine shift, vec_from_free already in linear kernel;
    # observed live in affine space. We'll pass origin=0 and use homogeneous
    # relations that actually hold.

    symbols = set()
    for blk in allowed:
        for s in blk:
            symbols.add(s)
    nI = sum(1 for s in symbols if I[s])
    if nI:
        return {
            "skipped": False,
            "dim": dim,
            "n_blocks": n,
            "n_symbols": len(symbols),
            "n_in_I": nI,
            "admits_I": True,
            "preserved": False,
            "reason": "linear space already contains I",
        }

    if nparts == 2:
        pairset = set(allowed)
        # index
        succ = defaultdict(list)
        for a, b in pairset:
            succ[a].append(b)
        fail_pres = 0
        fail_I = 0
        n_comp = 0
        lefts_of = defaultdict(list)
        for a, b in pairset:
            lefts_of[b].append(a)
        for b, lefts in lefts_of.items():
            rights = succ.get(b, [])
            for a in lefts:
                hab = H(a, b)
                for c in rights:
                    n_comp += 1
                    hbc = H(b, c)
                    if I[hab] or I[hbc]:
                        fail_I += 1
                    if (hab, hbc) not in pairset:
                        fail_pres += 1
        return {
            "skipped": False,
            "dim": dim,
            "n_blocks": n,
            "n_symbols": len(symbols),
            "n_in_I": nI,
            "n_compatible_triples": n_comp,
            "n_image_not_in_R": fail_pres,
            "n_image_in_I": fail_I,
            "admits_I": fail_I > 0,
            "preserved": fail_pres == 0 and fail_I == 0,
        }

    if nparts == 3:
        tripset = set(allowed)
        tail = defaultdict(list)
        for a, b, c in tripset:
            tail[(a, b)].append(c)
        fail_pres = 0
        fail_I = 0
        n_comp = 0
        for a, b, c in tripset:
            for d in tail.get((b, c), ()):
                n_comp += 1
                ha, hb, hc = H(a, b), H(b, c), H(c, d)
                if I[ha] or I[hb] or I[hc]:
                    fail_I += 1
                if (ha, hb, hc) not in tripset:
                    fail_pres += 1
        return {
            "skipped": False,
            "dim": dim,
            "n_blocks": n,
            "n_symbols": len(symbols),
            "n_in_I": nI,
            "n_compatible_4tuples": n_comp,
            "n_image_not_in_T": fail_pres,
            "n_image_in_I": fail_I,
            "admits_I": fail_I > 0,
            "preserved": fail_pres == 0 and fail_I == 0,
        }
    return {"skipped": True, "reason": "nparts"}


def mine_boolean_2sat_style(blocks2):
    """For each pair of bit positions among 36 bits, record the observed
    support (which of 00,01,10,11 appear). A relation is a missing tuple.
    """
    nbits = 36
    # too heavy to store 36^2 * 4 if we iterate all blocks many times;
    # accumulate as 4-bit masks per (i,j), i<=j
    masks = [[0] * nbits for _ in range(nbits)]
    for a, b in blocks2:
        x = (a << 18) | b
        bits = [(x >> i) & 1 for i in range(nbits)]
        for i in range(nbits):
            bi = bits[i]
            for j in range(i, nbits):
                masks[i][j] |= 1 << (bi | (bits[j] << 1))
    rels = []
    for i in range(nbits):
        for j in range(i, nbits):
            m = masks[i][j]
            if m != 15:
                rels.append((i, j, m))
    return rels


def lab36(i):
    site = "L" if i < 18 else "R"
    ii = i % 18
    which = "p" if ii < 9 else "c"
    return f"{site}.{which}{ii % 9}"


def format_pair_rel(i, j, m):
    names = []
    for ab in range(4):
        if (m >> ab) & 1:
            names.append(f"{(ab & 1)}{(ab >> 1) & 1}")
    return f"({lab36(i)},{lab36(j)}) in {{{','.join(names)}}}"


def check_boolean_rels_preservation(rels, blocks2, I):
    """rels = missing patterns. Define K as 2-blocks satisfying all rels.
    If too many, we cannot enumerate. Instead: take every locally compatible
    OBSERVED triple (so this is incomplete) — no, we must check EVERY locally
    compatible input of the candidate.

    If the boolean constraints leave a huge set, report dimension-like size
    via sampling / SAT count.

    Here: if we can bound the allowed pairs by enumerating... 2^18^2 is impossible.
    We check whether the IMAGE of every observed-compatible triple stays in the
    relation (necessary but the assignment wants every locally compatible block
    of the CANDIDATE, i.e. all pairs satisfying rels, not only observed).

    Fallback: try to satisfy rels ∪ {left in I or right in I} — if SAT, admits I.
    And try to find a triple satisfying rels whose H-image violates rels or hits I.
    """
    return None


def sat_admits_I_from_rels(pair_masks, I, n_check=None):
    """pair_masks[i][j] = allowed 2-bit combinations for bits i<=j of the 36-bit pair.
    Does any pair with a in I or b in I satisfy all pairwise supports?

    That's a necessary check: if even pairwise projections already forbid I
    as a symbol, good; if they allow I, the pairwise abstraction admits I
    as a symbol (unless higher-arity constraints save us).
    """
    # Check every I-state as left (resp. right) against some partner in 2^18
    # is too much. Instead: for each s in I, check whether the 18 bits of s
    # as L (resp R) have internally allowed pairwise patterns, AND whether
    # there exists an 18-bit partner (search).
    I_states = [s for s in range(NSTATE) if I[s]]
    assert len(I_states) == 512

    def ok_internal(s, offset):
        bits = [(s >> k) & 1 for k in range(18)]
        for i in range(18):
            for j in range(i, 18):
                m = pair_masks[i + offset][j + offset]
                ab = bits[i] | (bits[j] << 1)
                if ((m >> ab) & 1) == 0:
                    return False
        return True

    left_ok = [s for s in I_states if ok_internal(s, 0)]
    right_ok = [s for s in I_states if ok_internal(s, 18)]
    return {
        "n_I_left_pairwise_ok": len(left_ok),
        "n_I_right_pairwise_ok": len(right_ok),
        "pairwise_forbids_I_as_symbol": len(left_ok) == 0 and len(right_ok) == 0,
    }


def observed_union_close(by_depth, I, nsites):
    """Union of observed blocks through kmax, then H-close."""
    if nsites == 2:
        U = set()
        for d in by_depth:
            U |= d["blocks2"]
        print(f"  union 2-blocks through k={by_depth[-1]['k']}: {len(U)}", flush=True)
        return close_2blocks(U, I)
    U = set()
    for d in by_depth:
        U |= d["blocks3"]
    print(f"  union 3-blocks through k={by_depth[-1]['k']}: {len(U)}", flush=True)
    return close_3blocks(U, I)


def one_site_full_shift_closure(symbols, I, max_sym=200000):
    """K = full 2-shift on a symbol set J. Preservation: H(J,J) ⊆ J, J∩I=∅.
    Iterate J := J ∪ H(J,J) starting from initial two symbols, vs from observed.
    The iterate from initials is exactly consistent symbols at increasing depth
    IF we allow all pairs — which we do for 1-site. That's the depth table.
    Closing ALL pairs of the union of depths is the 1-site over-approx.
    """
    J = set(symbols)
    history = [{"round": 0, "n": len(J), "nI": sum(1 for s in J if I[s])}]
    if any(I[s] for s in J):
        return True, history, J, "already I"
    lst = list(J)
    for rnd in range(1, 8):
        new = []
        hit = False
        for a in lst:
            for b in lst:
                h = H(a, b)
                if h not in J:
                    new.append(h)
                    if I[h]:
                        hit = True
        uniq = []
        seen = set()
        for h in new:
            if h not in J and h not in seen:
                seen.add(h)
                uniq.append(h)
        for h in uniq:
            J.add(h)
        lst = list(J)
        nI = sum(1 for s in J if I[s])
        history.append({"round": rnd, "n_new": len(uniq), "n": len(J), "nI": nI})
        print(f"    1site round {rnd}: new={len(uniq)} |J|={len(J)} nI={nI}", flush=True)
        if hit or nI:
            return True, history, J, "admits I"
        if not uniq:
            return False, history, J, "stabilized I-free"
        if len(J) > max_sym:
            return False, history, J, "too large, still I-free"
    return False, history, J, "max rounds"


def enter_I_on_observed(by_depth, enter):
    """On observed 2-blocks, is the actual wrap an entering wrap?"""
    rows = []
    for d in by_depth:
        n_enter = 0
        n_avoid = 0
        n_forced_enter = 0
        for a, b in d["blocks2"]:
            w = b & 1
            m = enter[a]
            if m & (1 << w):
                n_enter += 1
            else:
                n_avoid += 1
            if m == 3:
                n_forced_enter += 1  # both wraps enter, doomed
            elif m == 0:
                pass
            else:
                # unique dangerous wrap
                pass
        rows.append(
            {
                "k": d["k"],
                "n_blocks": len(d["blocks2"]),
                "n_wrap_would_enter_I": n_enter,
                "n_wrap_avoids_I": n_avoid,
            }
        )
    return rows


def mine_depth_union_linear(by_depth, nparts):
    if nparts == 2:
        U = set()
        for d in by_depth:
            U |= d["blocks2"]
        packed = [(a << 18) | b for a, b in U]
        basis = gf2_nullspace(rows := packed, 36)
        rels = describe_linear(basis, 18, 2)
        dim, nrel = 36 - len(basis), len(basis)
        return {"n_blocks": len(U), "n_relations": nrel, "dim": dim, "relations": rels, "basis": basis, "packed": packed}
    U = set()
    for d in by_depth:
        U |= d["blocks3"]
    packed = [a | (b << 18) | (c << 36) for a, b, c in U]
    basis = gf2_nullspace(packed, 54)
    rels = describe_linear(basis, 18, 3)
    return {
        "n_blocks": len(U),
        "n_relations": len(basis),
        "dim": 54 - len(basis),
        "relations": rels,
        "basis": basis,
        "packed": packed,
    }


def find_I_witness_in_2shift(pairs, I, enter):
    """Among pairs in R, any with left in I or right in I, or H(a,b) in I."""
    n_leftI = n_rightI = n_H_I = 0
    wit = None
    for a, b in pairs:
        if I[a]:
            n_leftI += 1
            if wit is None:
                wit = ("left", a, b)
        if I[b]:
            n_rightI += 1
            if wit is None:
                wit = ("right", a, b)
        h = H(a, b)
        if I[h]:
            n_H_I += 1
            if wit is None:
                wit = ("H", a, b, h)
    return {"n_leftI": n_leftI, "n_rightI": n_rightI, "n_H_in_I": n_H_I, "witness": wit}


def bit_implications_init_preserved(I):
    """Hand relations that hold on all initial 2-blocks, test max extension.

    Initial S = (W0=011111111, W1=σ00000001).
    Two neighbors: prev identical, curr = σ 00000001.
    """
    s0, s1 = init_symbol(0), init_symbol(1)
    inits = [(x, y) for x in (s0, s1) for y in (s0, s1)]
    return {
        "n_init_symbols": 2,
        "n_init_2blocks": 4,
        "symbols": [bits9_lsb(decode(s)[0]) + "|" + bits9_lsb(decode(s)[1]) for s in (s0, s1)],
        "in_I": [bool(I[s0]), bool(I[s1])],
    }


def main():
    t0 = time.monotonic()
    report = {
        "excluded": False,
        "K_exists": None,
        "abstraction_failed": False,
        "notes": [],
    }

    print("===== build I =====", flush=True)
    succ0, succ1 = build_succ()
    layers, sizes = build_Z(succ0, succ1)
    I = layers[8]
    assert sum(I) == 512
    info = analyze_I_entry(I, succ0, succ1)
    report["I_entry"] = {k: info[k] for k in info if k not in ("f", "enter")}
    print(json.dumps(report["I_entry"]), flush=True)
    enter = info["enter"]
    f = info["f"]
    # sanity: I is graph of f
    for p in range(512):
        assert I[encode(p, f[p])]
        for c in range(512):
            if c != f[p]:
                assert not I[encode(p, c)]

    print("===== initial =====", flush=True)
    report["initial"] = bit_implications_init_preserved(I)
    print(json.dumps(report["initial"]), flush=True)

    # Depth for exact collection. kmax=12, nsites=3 => L=15, 2^15=32k, fine.
    # kmax=14, L=17, 128k. kmax=16, L=19, 512k reconstructions.
    KMAX = 12
    print(f"===== collect consistent blocks k=1..{KMAX} =====", flush=True)
    by_depth = collect_consistent(KMAX, nsites=3)
    report["collect"] = []
    for d in by_depth:
        nI = sum(1 for s in d["symbols"] if I[s])
        row = {
            "k": d["k"],
            "n_symbols": d["n_symbols"],
            "n_2blocks": d["n_2blocks"],
            "n_3blocks": d["n_3blocks"],
            "n_symbols_in_I": nI,
        }
        report["collect"].append(row)
        print(json.dumps(row), flush=True)
        assert nI == 0, ("consistent entered I at", d["k"])

    print("===== wrap vs enter-I on observed 2-blocks =====", flush=True)
    report["observed_enter"] = enter_I_on_observed(by_depth, enter)
    print(json.dumps(report["observed_enter"]), flush=True)

    print("===== wrap as function of left =====", flush=True)
    report["wrap_fn"] = []
    for d in by_depth:
        w = wrap_function_of_left(d["blocks2"])
        w["k"] = d["k"]
        report["wrap_fn"].append(w)
    print(json.dumps(report["wrap_fn"]), flush=True)

    print("===== linear relations, union of depths =====", flush=True)
    lin2 = mine_depth_union_linear(by_depth, 2)
    report["linear_2"] = {
        "n_blocks": lin2["n_blocks"],
        "n_relations": lin2["n_relations"],
        "dim": lin2["dim"],
        "relations": lin2["relations"],
    }
    print(json.dumps(report["linear_2"]), flush=True)

    lin3 = mine_depth_union_linear(by_depth, 3)
    report["linear_3"] = {
        "n_blocks": lin3["n_blocks"],
        "n_relations": lin3["n_relations"],
        "dim": lin3["dim"],
        "relations": lin3["relations"][:80],
        "n_relations_shown": min(80, len(lin3["relations"])),
    }
    print("linear_3 dim", lin3["dim"], "nrel", lin3["n_relations"], flush=True)

    print("===== per-depth linear dims =====", flush=True)
    report["linear_per_depth"] = []
    for d in by_depth:
        packed2 = [(a << 18) | b for a, b in d["blocks2"]]
        b2 = gf2_nullspace(packed2 := packed2 if False else packed2, 36)
        packed3 = [a | (b << 18) | (c << 36) for a, b, c in d["blocks3"]]
        b3 = gf2_nullspace(packed3, 54)
        row = {
            "k": d["k"],
            "dim2": 36 - len(b2),
            "nrel2": len(b2),
            "dim3": 54 - len(b3),
            "nrel3": len(b3),
        }
        report["linear_per_depth"].append(row)
        print(json.dumps(row), flush=True)

    print("===== enumerate linear 2-block space if small =====", flush=True)
    report["linear2_test"] = enumerate_kernel_and_test(lin2["basis"], 2, I, origin=0, max_dim=22)
    print(json.dumps({k: v for k, v in report["linear2_test"].items() if k != "x"}), flush=True)

    print("===== enumerate linear 3-block space if small =====", flush=True)
    report["linear3_test"] = enumerate_kernel_and_test(lin3["basis"], 3, I, origin=0, max_dim=20)
    print(json.dumps({k: v for k, v in report["linear3_test"].items() if k != "x"}), flush=True)

    print("===== pairwise boolean supports on union 2-blocks =====", flush=True)
    U2 = set()
    for d in by_depth:
        U2 |= d["blocks2"]
    rels = mine_boolean_2sat_style(U2)
    report["pairwise"] = {
        "n_constrained_pairs": len(rels),
        "n_unconstrained": 36 * 37 // 2 - len(rels),
        "sample_rels": [format_pair_rel(i, j, m) for i, j, m in rels[:40]],
    }
    print("n constrained bit-pairs", len(rels), flush=True)
    # build mask matrix
    pair_masks = [[15] * 36 for _ in range(36)]
    for i, j, m in rels:
        pair_masks[i][j] = m
        if i != j:
            # symmetric encode: bits (bi,bj) with ab = bi | (bj<<1)
            # mask for (j,i) uses aj = bj, ai = bi so ba = bj | (bi<<1)
            m2 = 0
            for ab in range(4):
                if (m >> ab) & 1:
                    bi, bj = ab & 1, (ab >> 1) & 1
                    m2 |= 1 << (bj | (bi << 1))
            pair_masks[j][i] = m2
    report["pairwise_I"] = sat_admits_I_from_rels(pair_masks, I)
    print(json.dumps(report["pairwise_I"]), flush=True)

    print("===== H-close union of observed 2-blocks =====", flush=True)
    hit2, hist2, R2, S2, msg2 = observed_union_close(by_depth, I, 2)
    report["close2"] = {"hit_I": hit2, "msg": msg2, "history": hist2}
    print(json.dumps(report["close2"]), flush=True)

    print("===== H-close union of observed 3-blocks =====", flush=True)
    hit3, hist3, T3, S3, msg3 = observed_union_close(by_depth, I, 3)
    report["close3"] = {"hit_I": hit3, "msg": msg3, "history": hist3}
    print(json.dumps(report["close3"]), flush=True)

    print("===== 1-site full-shift closure of union symbols =====", flush=True)
    Usym = set()
    for d in by_depth:
        Usym |= d["symbols"]
    hit1, hist1, J, msg1 = one_site_full_shift_closure(Usym, I)
    report["close1"] = {"hit_I": hit1, "msg": msg1, "history": hist1}
    print(json.dumps(report["close1"]), flush=True)

    # Also: H-close of INITIAL 2-blocks only (exact consistent evolution of
    # the 2-shift). That is NOT an over-approx — it is the depth table itself.
    print("===== close initial 2-blocks (exact consistent 2-shift) =====", flush=True)
    s0, s1 = init_symbol(0), init_symbol(1)
    init_pairs = [(x, y) for x in (s0, s1) for y in (s0, s1)]
    hitI, histI, RI, SI, msgI = close_2blocks(init_pairs, I, max_new=8_000_000, max_rounds=KMAX + 2)
    report["close_from_init"] = {"hit_I": hitI, "msg": msgI, "history": histI}
    print(json.dumps(report["close_from_init"]), flush=True)

    # Stronger failure: take linear hull of union 2-blocks (all pairs in the
    # affine space), close. If dim is large we skip enumeration; if linear2_test
    # already admits I, that's the failure of the linear abstraction.

    # Candidate: rank<=7 (everything except I which is rank 8). That's 1-site.
    # Z7 has 1024 states. Check whether H of two Z7-avoiding? No: not-I is
    # complement of 512 states, huge, free wrap enters I.

    print("===== not-I as 1-site: does some pair of non-I states enter I? =====", flush=True)
    # We already know free wrap can enter I. Count.
    n_nonI_enter = 0
    wit = None
    for s in range(NSTATE):
        if I[s]:
            continue
        for w in (0, 1):
            if I[H(s, w)]:
                n_nonI_enter += 1
                if wit is None:
                    wit = (s, w, H(s, w))
                break
        if n_nonI_enter and wit and n_nonI_enter > 0:
            pass
    report["notI_1site"] = {
        "n_nonI_states_with_a_wrap_into_I": n_nonI_enter,
        "witness_s": wit[0] if wit else None,
        "witness_wrap": wit[1] if wit else None,
        "fails": n_nonI_enter > 0,
    }
    print(json.dumps(report["notI_1site"]), flush=True)

    # Decide
    lin_admits = bool(report["linear2_test"].get("admits_I") or report["linear3_test"].get("admits_I"))
    short_admits = hit2 or hit3 or hit1
    if report["linear2_test"].get("admits_I"):
        report["notes"].append(
            "Linear span of observed 2-blocks already contains a symbol in I "
            "or its H-image on compatible triples enters I."
        )
    if hit2:
        report["notes"].append(
            "H-closure of the union of observed 2-blocks (k<=%d) admits I. "
            "Any 2-site K containing all those blocks is not I-free-invariant."
            % KMAX
        )
    if hit3:
        report["notes"].append(
            "H-closure of the union of observed 3-blocks admits I. "
            "Any 3-site K containing all those blocks fails."
        )
    if hit1:
        report["notes"].append("1-site full 2-shift on observed symbols closes into I.")

    # If close of observed union admits I, then NO superset-of-observed short
    # block language works. A K specified by relations must contain all initial
    # streams, hence all consistent blocks at every depth, hence the observed
    # union. So if that union's H-closure (which any invariant K must contain)
    # meets I, then no such K exists on 2-site (resp. 3-site) alphabets.
    #
    # Careful: H-closure of the UNION is the smallest 2-site invariant containing
    # all observed blocks. Invariant K could be SMALLER than the full 2-shift
    # of the union if it uses 3-site constraints to forbid some gluings that
    # the 2-site union allows. That's why we also close 3-blocks.
    #
    # If even 3-block closure of the observed union admits I, no 3-site K
    # containing all consistent 3-blocks can stay I-free.
    #
    # One caveat: the union is only through finite KMAX. If closure of the
    # finite union admits I, that is already fatal for any K containing those
    # observed blocks — which any K containing all initial streams AND invariant
    # under H must, after KMAX applications of H. YES: invariant + initial
    # ⇒ contains all consistent blocks at all depths. So contains the finite
    # union. If the smallest invariant 2-site (resp 3-site) language containing
    # that union meets I, no I-free invariant K of that locality exists.

    report["abstraction_failed"] = bool(hit2 or hit3)
    report["K_exists"] = False if (hit2 and hit3) else (
        True if (report.get("linear2_test", {}).get("preserved") or report.get("linear3_test", {}).get("preserved")) else None
    )
    if report["linear2_test"].get("preserved"):
        report["K_exists"] = True
        report["notes"].append("Linear 2-block kernel is H-invariant and I-free.")
    if report["linear3_test"].get("preserved"):
        report["K_exists"] = True
        report["notes"].append("Linear 3-block kernel is H-invariant and I-free.")

    report["excluded"] = False  # never claim q=8 excluded unless K_exists True and proved
    if report["K_exists"] is True:
        report["excluded"] = True
        report["notes"].append("K exists by machine-checked init+preservation; q=8 would be excluded. Verify dump.")

    report["elapsed"] = round(time.monotonic() - t0, 3)
    report["strongest"] = (
        "q=8 is not claimed excluded unless K_exists is true. "
        f"K_exists={report['K_exists']}, abstraction_failed={report['abstraction_failed']}, "
        f"close2={msg2}, close3={msg3}."
    )

    # drop huge objects
    path = Path(__file__).resolve().parent / "period9_invariant.json"
    dump = {k: v for k, v in report.items()}
    path.write_text(json.dumps(dump, indent=2) + "\n")
    print("wrote", path, "total", report["elapsed"], "s", flush=True)
    print("EXCLUDED", report["excluded"])
    print("K_EXISTS", report["K_exists"])
    print("STRONGEST", report["strongest"])
    return report


if __name__ == "__main__":
    main()
