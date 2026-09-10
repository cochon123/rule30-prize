#!/usr/bin/env python3
"""Bias-preserving coarse-graining of Rule 30 (Astra ideas7 item 3).

Search block projections P, additive radius-1 G, and a radius-2 coboundary
ψ such that PF^b = G P and the signed centre sum over a block is g((Px)_0)
plus a coboundary. Finite local identities. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/coarse_bias.py
"""
from __future__ import annotations

import json
import sys
import time
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def f(a, b, c):
    return a ^ (b | c)


def evolve_word(bits: tuple[int, ...], steps: int) -> tuple[int, ...]:
    cur = bits
    for _ in range(steps):
        nxt = []
        for j in range(len(cur) - 2):
            nxt.append(f(cur[j], cur[j + 1], cur[j + 2]))
        cur = tuple(nxt)
        if len(cur) < 3:
            break
    return cur


def signed(bit: int) -> int:
    return 1 if bit else -1


def all_maps(n_in: int, n_out_bits: int):
    """Functions {0,1}^{n_in} -> {0,1}^{n_out_bits} as tuples of length 2^{n_in}."""
    n_out = 1 << n_out_bits
    for table in product(range(n_out), repeat=(1 << n_in)):
        yield table


def eval_table(table, bits):
    idx = 0
    for b in bits:
        idx = (idx << 1) | b
    return table[idx]


def additive_G_tables(n_state_bits: int):
    """Radius-1 additive maps over F2^{k}: G(x,y,z) = Ax+By+Cz (matrix  k×k each).
    k=1 or 2. Number of maps: 2^{3 k^2}: k=1 → 8, k=2 → 2^{12}=4096.
    """
    k = n_state_bits
    mats = product(range(1 << (k * k)), repeat=3)
    for A, B, C in mats:
        yield (A, B, C)


def apply_lin(mat, vec, k):
    """mat packed k×k row-major, vec as int in 0..2^k-1."""
    out = 0
    for i in range(k):
        acc = 0
        for j in range(k):
            if (mat >> (i * k + j)) & 1:
                acc ^= (vec >> j) & 1
        out |= acc << i
    return out


def apply_G(ABC, xyz, k):
    A, B, C = ABC
    x, y, z = xyz
    return apply_lin(A, x, k) ^ apply_lin(B, y, k) ^ apply_lin(C, z, k)


def search_b(b: int, k: int, deadline: float) -> dict:
    """P reads a centre block of b bits plus one neighbour each side:  b+2 bits
    -> k-bit coarse cell. Factor identity on words of length b+4 (one extra
    neighbour for G's radius 1). Coboundary ψ radius 2 on bits, |ψ|≤32,
    g on the coarse centre cell.

    Enumeration is truncated: all additive G (small), all P for k=1 b=2
    (2^{3*2}=64? P: 2^{b+2} inputs -> k bits, table size 2^{b+2} values in
    2^k. For b=2,k=1: 16-bit table = 2^16, too many. Freeze P to
    *linear* projections plus a few nonlinear samples.
    """
    stats = {"b": b, "k": k, "n_G": 0, "n_P": 0, "n_factor": 0, "n_both": 0}
    survivors = []
    # Linear P: k×(b+2) matrices over F2.
    n_in = b + 2
    n_P = 1 << (k * n_in)
    G_list = list(additive_G_tables(k))
    stats["n_G_family"] = len(G_list)
    stats["n_P_family"] = n_P

    def P_lin(mat, word):
        # word length n_in, output k-bit int
        idx = 0
        for j, bit in enumerate(word):
            if bit:
                idx |= bit << j  # already 0/1
        # interpret word as int with bit j = word[j]
        v = 0
        for j, bit in enumerate(word):
            v |= (bit & 1) << j
        return apply_lin(mat, v, k)

    # Factor identity: on a word of length n_in+2 = b+4, evolve b steps to
    # a word of length (b+4)-2b = 4-b. Need leftover ≥ n_in = b+2, so
    # (b+4) - 2b = 4-b ≥ b+2 ⇒ 2 ≥ 2b. Only b=1. Wrong.

    # Local factor: P of the image block equals G of the P-triple of
    # overlapping source blocks.
    # Source window: 3 overlapping (b+2)-windows covering a region that maps
    # under F^b to a (b+2)-window.
    # F^b on a word of length (b+2)+2b = 3b+2 yields length b+2. That word
    # is exactly the image window. The three source blocks of length b+2
    # sit at offsets 0, b, 2b inside the 3b+2 word? Overlap of spatial
    # shift 1 on coarse cells: coarse cells correspond to b-blocks, so
    # adjacent coarse cells are shifted by b, not 1.
    # Three coarse cells: source length  b+2 + 2b = 3b+2, yes.
    src_len = 3 * b + 2
    n_src = 1 << src_len
    if n_src > (1 << 14):
        stats["skipped"] = "source window too large"
        return stats

    for Pmat in range(n_P):
        if time.monotonic() >= deadline:
            stats["budget"] = True
            break
        stats["n_P"] += 1
        # Precompute P on all (b+2)-windows
        nwin = 1 << n_in
        Ptab = [0] * nwin
        for w in range(nwin):
            word = tuple((w >> j) & 1 for j in range(n_in))
            Ptab[w] = P_lin(Pmat, word)
        if k == 1 and all(v == Ptab[0] for v in Ptab):
            continue  # constant projection
        if k == 2 and len(set(Ptab)) <= 1:
            continue

        # Image of F^b on src_len -> length src_len-2b = b+2. Check.
        img_len = src_len - 2 * b
        assert img_len == b + 2

        for G in G_list:
            if time.monotonic() >= deadline:
                stats["budget"] = True
                break
            stats["n_G"] += 1
            ok_factor = True
            for mask in range(n_src):
                src = tuple((mask >> j) & 1 for j in range(src_len))
                img = evolve_word(src, b)
                if len(img) != img_len:
                    ok_factor = False
                    break
                # three source windows at 0, b, 2b
                def win_at(off):
                    wbits = src[off : off + n_in]
                    wv = 0
                    for j, bit in enumerate(wbits):
                        wv |= bit << j
                    return Ptab[wv]
                Px = win_at(0)
                Py = win_at(b)
                Pz = win_at(2 * b)
                Gp = apply_G(G, (Px, Py, Pz), k)
                iv = 0
                for j, bit in enumerate(img):
                    iv |= bit << j
                if Ptab[iv] != Gp:
                    ok_factor = False
                    break
            if not ok_factor:
                continue
            stats["n_factor"] += 1
            # Coboundary: sum_{s=0}^{b-1} σ(F^s x)_centre = g(P x_centre) + ψ(F^b x)-ψ(x)
            # On the source word, centre of F^s is bit offset b + (something).
            # Seed-local: the centre bit of a (3b+2)-window after s steps is
            # at position b+s in the shrinking word... step s shrinks by s on
            # each side, original centre index = b (if we place the middle
            # coarse cell's centre at index b+1?).
            # Take original centre index = b  (0-based) in src of length 3b+2:
            # for b=2, len=8, centre index 2. After 1 step len=6, centre 1;
            # after 2 steps len=4, centre 0. Messy.
            # Use the middle b-block's first bit as the "centre stream"
            # along the middle coarse cell: positions b, b+1, ... 
            # For identity on ALL inputs, pick the bit at index b of src as
            # x_0, F maps that site to index b-1 of the next word, etc.
            # Simpler coboundary screen: ψ is a function of a radius-2
            # neighbourhood of the original centre, integer-valued |ψ|≤32,
            # g is a function of the k-bit coarse centre (2^k values in -b..b).
            # Too many ψ: radius-2 is 5 bits, 33^32 impossible.
            # Freeze ψ linear in the 5 bits with integer coeffs in -8..8,
            # plus a constant, |ψ| auto-bounded, and g arbitrary on 2^k values
            # in -64..64.
            # Even linear ψ: 9^5 * 9 = 531441 plus g. Feasible for one G,P.
            centre = b  # x_0 = src[b] if 0<=b<src_len
            cob_ok = False
            # g table
            g_range = range(-b, b + 1) if k == 1 else range(-2 * b, 2 * b + 1)
            # ψ(x) = c0 + sum_{j=-2..2} c_j x_{centre+j}, coeffs -4..4
            coeff_vals = range(-4, 5)
            found_psi = False
            for coeffs in product(coeff_vals, repeat=6):  # c0 and 5 bit coeffs
                if time.monotonic() >= deadline:
                    break
                def psi(word, cidx):
                    s = coeffs[0]
                    for j in range(-2, 3):
                        p = cidx + j
                        bit = word[p] if 0 <= p < len(word) else 0
                        s += coeffs[j + 3] * bit
                    return s
                # Fit g from one equation per coarse value if possible;
                # check consistency on all src.
                g_assign = {}
                ok = True
                for mask in range(n_src):
                    src = tuple((mask >> j) & 1 for j in range(src_len))
                    # evolve storing centres
                    cur = src
                    acc = 0
                    cidx = centre
                    for s in range(b):
                        acc += signed(cur[cidx])
                        nxt = []
                        for j in range(len(cur) - 2):
                            nxt.append(f(cur[j], cur[j + 1], cur[j + 2]))
                        cur = tuple(nxt)
                        cidx -= 1
                    # F^b x
                    rhs_psi = psi(cur, cidx) - psi(src, centre)
                    # Px middle
                    mid = src[b : b + n_in]
                    if len(mid) < n_in:
                        ok = False
                        break
                    mv = 0
                    for j, bit in enumerate(mid):
                        mv |= bit << j
                    pmid = Ptab[mv]
                    need = acc - rhs_psi
                    if pmid in g_assign and g_assign[pmid] != need:
                        ok = False
                        break
                    g_assign[pmid] = need
                if not ok:
                    continue
                # g must be a local function of the coarse cell only; already
                # keyed by pmid. Bound.
                if any(abs(v) > 32 for v in g_assign.values()):
                    continue
                found_psi = True
                cob_ok = True
                stats["n_both"] += 1
                if len(survivors) < 8:
                    survivors.append({
                        "Pmat": Pmat,
                        "G": G,
                        "psi_coeffs": list(coeffs),
                        "g": {str(k_): v for k_, v in g_assign.items()},
                    })
                break
            if cob_ok:
                # one survivor is enough to try simplification; record and
                # continue counting a few
                if stats["n_both"] >= 3:
                    stats["survivors"] = survivors
                    return stats
        if time.monotonic() >= deadline:
            break
    stats["survivors"] = survivors
    return stats


def main():
    t0 = time.monotonic()
    deadline = t0 + 7200
    checks = {}
    # f identity
    checks["f_110"] = f(1, 1, 0) == 1
    results = []
    # Ranked small cases first.
    for b, k in ((2, 1), (3, 1), (2, 2)):
        if time.monotonic() >= deadline:
            break
        rec = search_b(b, k, deadline)
        rec["elapsed_so_far"] = round(time.monotonic() - t0, 3)
        results.append(rec)
        print(json.dumps({k2: rec[k2] for k2 in rec if k2 != "survivors"}), flush=True)
        if rec.get("n_both", 0):
            break
    n_both = sum(r.get("n_both", 0) for r in results)
    n_factor = sum(r.get("n_factor", 0) for r in results)
    kill = n_both == 0
    payload = {
        "not_a_prize_claim": True,
        "freeze": {
            "b": [2, 3],
            "coarse_bits": [1, 2],
            "G": "additive radius-1 over F2^k",
            "P": "linear maps on a (b+2)-window",
            "psi": "affine in a radius-2 neighbourhood, coeffs -4..4",
        },
        "self_check": checks,
        "results": results,
        "kill": {
            "no_nonconstant_projection_with_both_identities": kill,
            "n_factor_diagrams": n_factor,
            "n_with_coboundary": n_both,
            "fired": True,
            "text": (
                "No nonconstant linear P and additive G in the freeze satisfy "
                "both the factor diagram and the bias coboundary. A factor "
                "diagram alone is insufficient. Not a prize claim."
                if kill
                else "A local identity survived the freeze; the coarse trace "
                "still needs a demonstrated simplification."
            ),
        },
        "elapsed_sec": round(time.monotonic() - t0, 3),
    }
    if n_both:
        payload["kill"]["fired"] = True  # still need simplification of G-trace
        payload["kill"]["needs_coarse_simplification"] = True
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "n_factor": n_factor,
        "n_both": n_both,
        "kill": payload["kill"]["text"][:160],
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
