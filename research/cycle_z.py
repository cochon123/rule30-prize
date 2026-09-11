#!/usr/bin/env python3
"""Cycle Z: dyadic half-step for b_k = c_{2^k}.

Cycle Y: packed Rule 30 is Rule 150 XOR adjacent ANDs, and v_k=v_{k+1}
forces (b_j)_{j>=k} constant. This cycle unfolds one doubling:
    b_k = b_{k-1} XOR I_k,
where the Rule-150 image of the row at time T=2^{k-1} contributes
exactly b_{k-1} (both light-cone edges are 1), and I_k is the Green
parity of AND injections in the time interval [T, 2T).

Not a prize claim unless I_k is proved not eventually 0 (equivalently,
(b_k) not eventually constant). Local formulas for I_k are killed.

Run: python3 research/cycle_z.py --certify
Dump: research/cycle_z.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def r150_step(row: int) -> int:
    return (row << 2) ^ (row << 1) ^ row


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
    for _t in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def trinom_step(p: int) -> int:
    return p ^ (p << 1) ^ (p << 2)


def linear_half_step(P: int, T: int) -> dict:
    """[x^{2T}] P(1+x^T+x^{2T}) = P_0 XOR P_T XOR P_{2T}."""
    e0 = P & 1
    eT = (P >> T) & 1
    e2T = (P >> (2 * T)) & 1
    return {
        "left_edge": e0,
        "centre": eT,
        "right_edge": e2T,
        "lin": e0 ^ eT ^ e2T,
    }


def independent_I(rows: list[int], k: int) -> dict:
    """I_k = XOR_j [x^{2T}] A_{T+j} (1+x+x^2)^{T-1-j}."""
    T = 1 << (k - 1)
    acc = 0
    n_contrib = 0
    n11 = 0
    for j in range(T):
        R = rows[T + j]
        A = (R << 1) & R
        n11 += A.bit_count()
        m = T - 1 - j
        p = A
        for _ in range(m):
            p = trinom_step(p)
        bit = (p >> (2 * T)) & 1
        if bit:
            n_contrib += 1
        acc ^= bit
    return {"I": acc, "n_contrib": n_contrib, "n11": n11}


def local_I_candidates(rows: list[int], k: int) -> dict:
    T = 1 << (k - 1)
    R = rows[T]
    def x(j: int) -> int:
        bit = j + T
        if bit < 0:
            return 0
        return (R >> bit) & 1

    l, c, r = x(-1), x(0), x(1)
    inward = x(T - 1)  # one cell in from the right edge
    return {
        "l": l,
        "c": c,
        "r": r,
        "c_and_r": c & r,
        "l_xor_r": l ^ r,
        "right_inward": inward,
    }


def sparse_power_hits(rows: list[int], k: int) -> dict:
    """For m=2^a, G(2^a,d)=1 iff d in {0, 2^a, 2^{a+1}}.

    Time t = 2T-1-2^a, packed bits p in {2T, 2T-2^a, 2T-2^{a+1}}.
    """
    T = 1 << (k - 1)
    hits = []
    xor = 0
    for a in range(0, k - 1):
        m = 1 << a
        tm = 2 * T - 1 - m
        if tm < T or tm >= 2 * T:
            continue
        R = rows[tm]
        A = (R << 1) & R
        ps = (2 * T, 2 * T - m, 2 * T - 2 * m)
        bits = [((A >> p) & 1) if p >= 0 else 0 for p in ps]
        s = bits[0] ^ bits[1] ^ bits[2]
        xor ^= s
        hits.append({"a": a, "time": tm, "bits": bits, "xor": s})
    return {"n": len(hits), "xor": xor, "head": hits[:8]}


def self_checks(c20, rows, b, lin_rows, I_rows) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    row = 1
    for _ in range(20):
        assert rule30_step(row) == r150_step(row) ^ ((row << 1) & row)
        row = rule30_step(row)
    for rec in lin_rows:
        assert rec["left_edge"] == 1 and rec["right_edge"] == 1
        assert rec["lin"] == rec["b_prev"]
    for rec in I_rows:
        assert rec["I_ind"] == rec["I_xor"]
    # k=1: second half is a single step, I_1 = b_1 XOR b_0
    assert (b[1] ^ b[0]) == I_rows[0]["I_ind"]
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--kmax", type=int, default=12)
    parser.add_argument("--Imax", type=int, default=10)
    args = parser.parse_args()
    t0 = time.perf_counter()
    kmax = args.kmax
    tmax = 1 << kmax
    c20 = packed_center_bits(20)
    rows = evolve_rows(tmax)
    b = [(rows[1 << k] >> (1 << k)) & 1 for k in range(0, kmax + 1)]

    lin_rows = []
    for k in range(1, kmax + 1):
        T = 1 << (k - 1)
        rec = linear_half_step(rows[T], T)
        rec["k"] = k
        rec["b_prev"] = b[k - 1]
        rec["b"] = b[k]
        rec["I_xor"] = b[k] ^ b[k - 1]
        rec["match_lin_b_prev"] = rec["lin"] == b[k - 1]
        lin_rows.append(rec)

    I_rows = []
    for k in range(1, min(args.Imax, kmax) + 1):
        ind = independent_I(rows, k)
        loc = local_I_candidates(rows, k)
        Ix = b[k] ^ b[k - 1]
        loc_vals = {
            "l": loc["l"],
            "c": loc["c"],
            "r": loc["r"],
            "c_and_r": loc["c_and_r"],
            "l_xor_r": loc["l_xor_r"],
        }
        named_eq = {name: (val == Ix) for name, val in loc_vals.items()}
        I_rows.append(
            {
                "k": k,
                "I_ind": ind["I"],
                "I_xor": Ix,
                "match": ind["I"] == Ix,
                "n_contrib": ind["n_contrib"],
                "n11": ind["n11"],
                "n11_parity": ind["n11"] & 1,
                "n11_parity_eq_I": (ind["n11"] & 1) == Ix,
                "local": loc,
                "named_eq": named_eq,
                "right_inward": loc["right_inward"],
                "right_and_fires": loc["right_inward"] == 1,
            }
        )

    # Universality of named local bits
    names = ("l", "c", "r", "c_and_r", "l_xor_r")
    universal_local = {}
    for name in names:
        universal_local[name] = all(rec["named_eq"][name] for rec in I_rows)
    any_universal_local = any(universal_local.values())
    n11_universal = all(rec["n11_parity_eq_I"] for rec in I_rows)
    right_and_universal = all(rec["right_and_fires"] == rec["I_xor"] for rec in I_rows)

    sparse = []
    for k in range(2, min(8, kmax) + 1):
        sp = sparse_power_hits(rows, k)
        sp["k"] = k
        sp["I"] = b[k] ^ b[k - 1]
        sp["equals_I"] = sp["xor"] == (b[k] ^ b[k - 1])
        sparse.append(sp)

    checks = self_checks(c20, rows, b, lin_rows, I_rows)

    n_I_ones = sum(1 for rec in lin_rows if rec["I_xor"] == 1)
    n_I_zeros = sum(1 for rec in lin_rows if rec["I_xor"] == 0)

    dump = {
        "cycle": "Z",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "b": b,
        "I": [rec["I_xor"] for rec in lin_rows],
        "n_I_ones": n_I_ones,
        "n_I_zeros": n_I_zeros,
        "linear": lin_rows,
        "I_independent": I_rows,
        "universal_local": universal_local,
        "any_universal_local": any_universal_local,
        "n11_parity_universal": n11_universal,
        "right_and_universal": right_and_universal,
        "sparse_power": sparse,
        "sparse_equals_I_any": any(s["equals_I"] for s in sparse),
        "lemmas": {
            "half_step": True,
            "linear_part_is_b_prev": all(r["match_lin_b_prev"] for r in lin_rows),
            "edges_are_one": all(r["left_edge"] == 1 and r["right_edge"] == 1 for r in lin_rows),
            "I_independently_certified": all(r["match"] for r in I_rows),
            "b_not_eventually_constant": None,
        },
        "verdict": {
            "half_step": "LEMMA",
            "local_I": "KILLED" if not any_universal_local else "OPEN",
            "n11_parity": "KILLED" if not n11_universal else "OPEN",
            "right_edge_and": "KILLED" if not right_and_universal else "OPEN",
            "sparse_m_pow2": "PARTIAL" if not all(s["equals_I"] for s in sparse) else "EQUALS_I",
            "b_k_eventual_constancy": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("b", b)
    print("I", dump["I"])
    print("n_I_ones", n_I_ones, "n_I_zeros", n_I_zeros)
    print("universal_local", universal_local)
    print("n11_universal", n11_universal, "right_and", right_and_universal)
    print("sparse_eq", [s["equals_I"] for s in sparse])
    print("n_contrib", [r["n_contrib"] for r in I_rows])
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
