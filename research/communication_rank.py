#!/usr/bin/env python3
"""Communication rank of the Rule 30 apex (prize problem 3).

f_h is the centre bit after h shrinking Rule 30 steps on an arbitrary word
of length 2h+1. Communication matrices are the three splits
(|u|,|v|) = (h,h+1), (h-1,h+2), (h+1,h). Exact GF(2) ranks for h=2..10.
XOR-of-products factorisation from a row-space basis at the smallest h.

Envelope: r_h <= 8h. Not a prize claim.
Lead: Goles, Meunier, Rapaport, Theyssier, arXiv:0906.3284 §4.4.

Run: python3 research/communication_rank.py
Does not modify experiment.py, strip_graph.py, or strip_extend.py.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


def packed_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def rule30(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def shrink_word(w: int, n: int) -> int:
    """One shrinking Rule 30 step; LSB is the leftmost cell."""
    return (w ^ ((w >> 1) | (w >> 2))) & ((1 << (n - 2)) - 1)


def f_h_packed(w: int, h: int) -> int:
    """Apex of a length-(2h+1) word after h shrinking steps."""
    n = 2 * h + 1
    for _ in range(h):
        w = shrink_word(w, n)
        n -= 2
    return w & 1


def f_h_tuple(bits: tuple[int, ...]) -> int:
    cur = list(bits)
    while len(cur) > 1:
        cur = [rule30(cur[i], cur[i + 1], cur[i + 2]) for i in range(len(cur) - 2)]
    return cur[0]


def pack_bits(bits: tuple[int, ...]) -> int:
    w = 0
    for i, b in enumerate(bits):
        w |= (b & 1) << i
    return w


def unpack_bits(w: int, n: int) -> tuple[int, ...]:
    return tuple((w >> i) & 1 for i in range(n))


def apex_table(h: int) -> list[int]:
    """f_h(w) for every word w of length 2h+1 (LSB = leftmost)."""
    width = 2 * h + 1
    vals = list(range(1 << width))
    for _ in range(h):
        mask = (1 << (width - 2)) - 1
        for i, w in enumerate(vals):
            vals[i] = (w ^ ((w >> 1) | (w >> 2))) & mask
        width -= 2
    return vals


def matrix_rows(apex: list[int], left: int, right: int) -> list[int]:
    """Row bitsets: rows[u] bit v is f(uv). LSB of u,v = leftmost of that half."""
    nL = 1 << left
    rows = [0] * nL
    mask = nL - 1
    for w, bit in enumerate(apex):
        if bit:
            rows[w & mask] |= 1 << (w >> left)
    return rows


def n_distinct_columns(rows: list[int], n_cols: int) -> int:
    seen: set[int] = set()
    nL = len(rows)
    for v in range(n_cols):
        col = 0
        for u in range(nL):
            if (rows[u] >> v) & 1:
                col |= 1 << u
        seen.add(col)
    return len(seen)


def gf2_rank(rows: list[int]) -> int:
    """Exact rank over GF(2); each row is a bitset integer."""
    mat = list(rows)
    n = len(mat)
    rank = 0
    width = 0
    for x in mat:
        bl = x.bit_length()
        if bl > width:
            width = bl
    for col in range(width - 1, -1, -1):
        mask = 1 << col
        piv = None
        for i in range(rank, n):
            if mat[i] & mask:
                piv = i
                break
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        pv = mat[rank]
        for i in range(n):
            if i != rank and mat[i] & mask:
                mat[i] ^= pv
        rank += 1
    return rank


def gf2_rank_transpose(rows: list[int], n_cols: int) -> int:
    nL = len(rows)
    cols = [0] * n_cols
    for v in range(n_cols):
        c = 0
        for u in range(nL):
            if (rows[u] >> v) & 1:
                c |= 1 << u
        cols[v] = c
    return gf2_rank(cols)


def gf2_invert(rows: list[int], n: int) -> list[int]:
    """Invert an n x n GF(2) matrix given as n n-bit row bitsets (LSB = col 0)."""
    aug = [rows[i] | (1 << (n + i)) for i in range(n)]
    rank = 0
    for col in range(n):
        mask = 1 << col
        piv = None
        for i in range(rank, n):
            if aug[i] & mask:
                piv = i
                break
        if piv is None:
            raise RuntimeError("singular GF(2) minor")
        aug[rank], aug[piv] = aug[piv], aug[rank]
        pv = aug[rank]
        for i in range(n):
            if i != rank and aug[i] & mask:
                aug[i] ^= pv
        rank += 1
    return [aug[i] >> n for i in range(n)]


def factorize_rows(rows: list[int], n_cols: int) -> dict:
    """Row-space factorisation M = A B over GF(2).

    B's rows are a basis of original rows. A[u] is an r-bit coefficient
    mask so that rows[u] = XOR_i A[u]_i * B[i].
    """
    n = len(rows)
    work = list(rows)
    orig = list(range(n))
    rank = 0
    pivot_cols: list[int] = []
    width = n_cols
    for col in range(width):
        mask = 1 << col
        piv = None
        for i in range(rank, n):
            if work[i] & mask:
                piv = i
                break
        if piv is None:
            continue
        work[rank], work[piv] = work[piv], work[rank]
        orig[rank], orig[piv] = orig[piv], orig[rank]
        pv = work[rank]
        for i in range(n):
            if i != rank and work[i] & mask:
                work[i] ^= pv
        pivot_cols.append(col)
        rank += 1
    basis_idx = orig[:rank]
    if rank == 0:
        return {
            "rank": 0,
            "basis_row_indices": [],
            "pivot_cols": [],
            "A": [0] * n,
            "B": [],
        }
    minor = []
    for bi in basis_idx:
        q = 0
        for j, c in enumerate(pivot_cols):
            if (rows[bi] >> c) & 1:
                q |= 1 << j
        minor.append(q)
    inv = gf2_invert(minor, rank)
    A = []
    for u in range(n):
        vec = 0
        for j, c in enumerate(pivot_cols):
            if (rows[u] >> c) & 1:
                vec |= 1 << j
        coef = 0
        for j in range(rank):
            if (vec >> j) & 1:
                coef ^= inv[j]
        A.append(coef)
    B = [rows[i] for i in basis_idx]
    return {
        "rank": rank,
        "basis_row_indices": basis_idx,
        "pivot_cols": pivot_cols,
        "A": A,
        "B": B,
    }


def reconstruct_row(coef: int, B: list[int]) -> int:
    acc = 0
    bit = 0
    c = coef
    while c:
        if c & 1:
            acc ^= B[bit]
        c >>= 1
        bit += 1
    return acc


def verify_factorization(rows: list[int], fact: dict) -> bool:
    B = fact["B"]
    for u, row in enumerate(rows):
        if reconstruct_row(fact["A"][u], B) != row:
            return False
    return True


def mobius(vals: list[int]) -> list[int]:
    a = list(vals)
    n = len(a)
    step = 1
    while step < n:
        for i in range(0, n, 2 * step):
            for j in range(step):
                a[i + j + step] ^= a[i + j]
        step *= 2
    return a


def anf_stats(vals: list[int]) -> dict:
    a = mobius(vals)
    degree = 0
    n_terms = 0
    for m, bit in enumerate(a):
        if bit:
            n_terms += 1
            pop = m.bit_count()
            if pop > degree:
                degree = pop
    return {"degree": degree, "n_terms": n_terms, "n_inputs": (len(vals) - 1).bit_length()}


def anf_string(vals: list[int], names: list[str]) -> str:
    a = mobius(vals)
    terms = []
    for m, bit in enumerate(a):
        if not bit:
            continue
        if m == 0:
            terms.append("1")
            continue
        parts = [names[i] for i in range(len(names)) if (m >> i) & 1]
        terms.append("".join(parts))
    return " + ".join(terms) if terms else "0"


def ceil_log2(n: int) -> int:
    if n <= 1:
        return 0
    return math.ceil(math.log2(n))


def seed_word(h: int) -> int:
    """Single 1 at the centre of a length-(2h+1) window."""
    return 1 << h


def self_check() -> dict:
    checks: dict = {}
    cb = experiment_center_bits(16)
    packed_centres = []
    row = 1
    packed_centres.append((row >> 0) & 1)
    for h in range(1, 13):
        row = packed_update(row)
        packed_centres.append((row >> h) & 1)
        fh = f_h_packed(seed_word(h), h)
        if fh != cb[h] or fh != packed_centres[h]:
            raise AssertionError(f"seed mismatch at h={h}: f_h={fh} center_bits={cb[h]} packed={packed_centres[h]}")
    checks["seed_triangle_agrees_h_1_12"] = True
    checks["center_bits_prefix"] = list(cb[:13])
    checks["packed_update_centres"] = packed_centres[:13]

    # Tuple shrinking vs packed, exhaustive small h and sampled larger.
    for h in (1, 2, 3, 4):
        n = 2 * h + 1
        for w in range(1 << n):
            bits = unpack_bits(w, n)
            if f_h_tuple(bits) != f_h_packed(w, h):
                raise AssertionError(f"tuple/packed mismatch h={h} w={w}")
    checks["tuple_equals_packed_h_1_4_exhaustive"] = True

    for h in (5, 6, 7):
        n = 2 * h + 1
        for w in (0, 1, seed_word(h), (1 << n) - 1, 0x15 << 2, 0x3A5):
            w &= (1 << n) - 1
            bits = unpack_bits(w, n)
            if f_h_tuple(bits) != f_h_packed(w, h):
                raise AssertionError(f"tuple/packed mismatch h={h} w={w}")
    checks["tuple_equals_packed_sampled_h_5_7"] = True

    # Apex table matches packed f_h.
    for h in (2, 3, 5):
        tab = apex_table(h)
        n = 2 * h + 1
        for w, bit in enumerate(tab):
            if bit != f_h_packed(w, h):
                raise AssertionError(f"apex_table mismatch h={h} w={w}")
        if len(tab) != 1 << n:
            raise AssertionError("apex table length")
    checks["apex_table_matches_f_h"] = True

    # Extra vacuum padding cannot affect the apex: the 2h+1 window is the
    # full neighbourhood, so shrinking never reads outside.
    for h in (2, 3, 4):
        n = 2 * h + 1
        for w in range(1 << n):
            bits = unpack_bits(w, n)
            padded = (0,) * 2 + bits + (0,) * 2
            cur = list(padded)
            for _ in range(h):
                nxt = []
                for j in range(len(cur)):
                    left = cur[j - 1] if j - 1 >= 0 else 0
                    mid = cur[j]
                    right = cur[j + 1] if j + 1 < len(cur) else 0
                    nxt.append(rule30(left, mid, right))
                cur = nxt
            centre = cur[2 + h]
            if centre != f_h_packed(w, h):
                raise AssertionError(f"pad mismatch h={h} w={w}")
    checks["zero_pad_agrees_with_shrinking"] = True
    return checks


def feature_degree_stats(fact: dict, n_left: int, n_right: int) -> dict:
    rank = fact["rank"]
    if rank == 0:
        return {"A": None, "B": None}
    A_degs = []
    A_terms = []
    B_degs = []
    B_terms = []
    nL = 1 << n_left
    nR = 1 << n_right
    for i in range(rank):
        a_vals = [(fact["A"][u] >> i) & 1 for u in range(nL)]
        st = anf_stats(a_vals)
        A_degs.append(st["degree"])
        A_terms.append(st["n_terms"])
        b_vals = [(fact["B"][i] >> v) & 1 for v in range(nR)]
        st = anf_stats(b_vals)
        B_degs.append(st["degree"])
        B_terms.append(st["n_terms"])
    return {
        "A": {
            "degree_min": min(A_degs),
            "degree_max": max(A_degs),
            "n_terms_min": min(A_terms),
            "n_terms_max": max(A_terms),
            "all_affine": max(A_degs) <= 1,
        },
        "B": {
            "degree_min": min(B_degs),
            "degree_max": max(B_degs),
            "n_terms_min": min(B_terms),
            "n_terms_max": max(B_terms),
            "all_affine": max(B_degs) <= 1,
        },
    }


def explicit_h2_factorization(fact: dict) -> dict:
    """Human-readable XOR-of-products for the central split at h=2."""
    names_u = ["u0", "u1"]
    names_v = ["v0", "v1", "v2"]
    products = []
    nL, nR = 4, 8
    rank = fact["rank"]
    for i in range(rank):
        a_vals = [(fact["A"][u] >> i) & 1 for u in range(nL)]
        b_vals = [(fact["B"][i] >> v) & 1 for v in range(nR)]
        products.append({
            "i": i,
            "A_anf": anf_string(a_vals, names_u),
            "B_anf": anf_string(b_vals, names_v),
            "A_truth": a_vals,
            "B_truth": b_vals,
        })
    matrix = []
    # Rebuild from A,B for the dump.
    for u in range(nL):
        row = reconstruct_row(fact["A"][u], fact["B"])
        matrix.append([(row >> v) & 1 for v in range(nR)])
    return {
        "h": 2,
        "split": {"left": 2, "right": 3},
        "packing": "LSB is the leftmost cell of that half",
        "rank": rank,
        "basis_row_indices": fact["basis_row_indices"],
        "matrix_rows": matrix,
        "products": products,
        "note": (
            "f_2(uv) = XOR_i A_i(u) B_i(v). A_i are affine in the two left "
            "bits; B_i are cubic in the three right bits. This is a 4 x 8 "
            "truth-table factorisation, not a recursive feature rule."
        ),
    }


def split_spec(h: int) -> list[tuple[int, int, str]]:
    return [
        (h - 1, h + 2, "left_of_centre"),
        (h, h + 1, "centre"),
        (h + 1, h, "right_of_centre"),
    ]


def analyse_h(h: int) -> dict:
    t0 = time.perf_counter()
    apex = apex_table(h)
    apex_time = time.perf_counter() - t0
    n = 2 * h + 1
    if len(apex) != 1 << n:
        raise RuntimeError("apex table size")
    # Seed consistency on this table.
    if apex[seed_word(h)] != experiment_center_bits(h + 1)[h]:
        raise AssertionError(f"table seed mismatch at h={h}")
    f_stats = anf_stats(apex)
    splits = []
    central_fact = None
    for left, right, name in split_spec(h):
        t1 = time.perf_counter()
        rows = matrix_rows(apex, left, right)
        rank = gf2_rank(rows)
        n_rows = len(set(rows))
        n_cols = n_distinct_columns(rows, 1 << right)
        rec = {
            "name": name,
            "left": left,
            "right": right,
            "n_rows": 1 << left,
            "n_cols": 1 << right,
            "rank": rank,
            "n_distinct_rows": n_rows,
            "n_distinct_cols": n_cols,
            "cc1": ceil_log2(min(n_rows, n_cols)),
            "eight_h": 8 * h,
            "rank_le_8h": rank <= 8 * h,
            "seconds": round(time.perf_counter() - t1, 6),
        }
        if name == "centre":
            fact = factorize_rows(rows, 1 << right)
            if fact["rank"] != rank:
                raise AssertionError("factor rank mismatch")
            if not verify_factorization(rows, fact):
                raise AssertionError(f"factorisation failed at h={h}")
            rec["factorization_verified"] = True
            rec["feature_anf"] = feature_degree_stats(fact, left, right)
            if h <= 4:
                rec["transpose_rank"] = gf2_rank_transpose(rows, 1 << right)
                if rec["transpose_rank"] != rank:
                    raise AssertionError("rank != transpose rank")
            if h == 2:
                central_fact = fact
        splits.append(rec)
    return {
        "h": h,
        "word_length": n,
        "eight_h": 8 * h,
        "f_h_anf": f_stats,
        "apex_seconds": round(apex_time, 6),
        "all_splits_le_8h": all(s["rank_le_8h"] for s in splits),
        "splits": splits,
        "central_fact": central_fact,
    }


def kill_record(results: list[dict]) -> dict:
    violations = []
    for rec in results:
        for spl in rec["splits"]:
            if not spl["rank_le_8h"]:
                violations.append({
                    "h": rec["h"],
                    "name": spl["name"],
                    "left": spl["left"],
                    "right": spl["right"],
                    "rank": spl["rank"],
                    "eight_h": spl["eight_h"],
                })
    fired = bool(violations)
    if fired:
        first = violations[0]
        text = (
            f"Kill fired: GF(2) rank exceeds 8h on a required split. "
            f"First violation is h={first['h']} split (|u|,|v|)=({first['left']},"
            f"{first['right']}) with rank {first['rank']} > {first['eight_h']}. "
            f"The prototype envelope r_h <= 8h is false. Features of the "
            f"surviving splits are still truth tables of the row/column space "
            f"(growing algebraic degree; evaluation is the original cone or a "
            f"2^Theta(h) ANF). Low communication with expensive computation "
            f"would also fail. This is not a prize claim."
        )
    else:
        text = (
            "Rank envelope r_h <= 8h held on every required split through "
            "h=10. Composition of feature spaces must still be checked; a "
            "factorisation whose features are exponentially indexed truth "
            "tables or cone simulations is also a kill."
        )
    return {
        "fired": fired,
        "criterion": "any required rank (any of the three splits, any h<=10) exceeds 8h",
        "violations": violations,
        "text": text,
        "other_kills_noted": [
            "exponentially indexed truth tables for A,B",
            "features evaluable only by simulating their original cones",
            "low communication with expensive computation",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parent / "communication_rank.json"),
    )
    parser.add_argument("--h-min", type=int, default=2)
    parser.add_argument("--h-max", type=int, default=10)
    args = parser.parse_args()
    if args.h_min < 2 or args.h_max > 12 or args.h_min > args.h_max:
        parser.error("require 2 <= h-min <= h-max <= 12")
    if args.h_max < 10:
        parser.error("h=10 is required; refusing to skip it")

    t0 = time.perf_counter()
    checks = self_check()
    results = []
    explicit = None
    for h in range(args.h_min, args.h_max + 1):
        rec = analyse_h(h)
        if rec["central_fact"] is not None:
            explicit = explicit_h2_factorization(rec["central_fact"])
            # Exhaustive check of the XOR-of-products on all 32 words.
            apex = apex_table(2)
            ok = True
            for w, bit in enumerate(apex):
                u = w & 3
                v = w >> 2
                pred = 0
                for prod in explicit["products"]:
                    pred ^= prod["A_truth"][u] & prod["B_truth"][v]
                if pred != bit:
                    ok = False
            explicit["verified_all_32_words"] = ok
            if not ok:
                raise AssertionError("h=2 XOR-of-products failed exhaustive check")
        rec.pop("central_fact")
        results.append(rec)

    kill = kill_record(results)
    dump = {
        "problem": 3,
        "source": "research/_astra_ideas6.md item 1",
        "lead": {
            "citation": "Goles, Meunier, Rapaport, Theyssier, Communications in cellular automata, arXiv:0906.3284 §4.4",
            "claim": (
                "Rule 30 was suggested experimentally as a candidate with high "
                "one-round communication complexity but low matrix rank; not a theorem."
            ),
        },
        "field": "GF(2)",
        "envelope": "r_h <= 8h",
        "packing": "LSB is the leftmost cell; next row bit i is x_i XOR (x_{i+1} OR x_{i+2})",
        "self_checks": checks,
        "h_range": list(range(args.h_min, args.h_max + 1)),
        "ranks": results,
        "all_ranks_le_8h": all(rec["all_splits_le_8h"] for rec in results),
        "factorization_smallest_h": explicit,
        "kill": kill,
        "seconds": round(time.perf_counter() - t0, 4),
        "prize_claim": False,
    }
    out = Path(args.output)
    out.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {out}")
    print(kill["text"])
    for rec in results:
        parts = [
            f"{s['name']}({s['left']},{s['right']}): rank {s['rank']}"
            f"{'' if s['rank_le_8h'] else ' > '+str(s['eight_h'])}"
            for s in rec["splits"]
        ]
        print(f"h={rec['h']} 8h={rec['eight_h']}  " + "  ".join(parts))


if __name__ == "__main__":
    main()
