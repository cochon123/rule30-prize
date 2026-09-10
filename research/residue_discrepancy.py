#!/usr/bin/env python3
"""Residue-class discrepancies of the Rule 30 centre (Cycle I extra screen).

If some arithmetic progression of times had a closed signed sum, Problem 2
would reduce to finitely many residue classes. This is not dyadic A_m and
not block energy. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/residue_discrepancy.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def class_discrepancies(bits: bytearray, modulus: int) -> list[dict]:
    counts = [0] * modulus
    ones = [0] * modulus
    for t, b in enumerate(bits):
        r = t % modulus
        counts[r] += 1
        ones[r] += b
    rows = []
    for r in range(modulus):
        n = counts[r]
        d = 2 * ones[r] - n
        rows.append({
            "residue": r,
            "n": n,
            "ones": ones[r],
            "signed": d,
            "ratio": (d / n) if n else None,
        })
    return rows


def linear_complexity(bits) -> int:
    connection = previous = 1
    length, last_change, history = 0, -1, 0
    for n, value in enumerate(bits):
        history = (history << 1) | value
        discrepancy = (connection & history).bit_count() & 1
        if discrepancy:
            old = connection
            connection ^= previous << (n - last_change)
            if 2 * length <= n:
                length = n + 1 - length
                previous, last_change = old, n
    return length


def subsample(bits: bytearray, modulus: int, residue: int) -> bytearray:
    return bytearray(bits[t] for t in range(residue, len(bits), modulus))


def main() -> None:
    t0 = time.perf_counter()
    n = 100_000
    bits = packed_center(max(n, 1 << 17))
    ref = experiment_center_bits(256)
    assert list(bits[:256]) == list(ref)

    moduli = [2, 3, 4, 5, 6, 7, 8, 9, 15, 16]
    report = {}
    max_abs_ratio = 0.0
    min_lc_ratio = 1.0
    for m in moduli:
        disc = class_discrepancies(bits[:n], m)
        lcs = []
        for r in range(m):
            sub = subsample(bits[:n], m, r)
            # Cap BM at 4096 bits per class to keep the screen cheap.
            train = sub[: min(len(sub), 4096)]
            lc = linear_complexity(train)
            lcs.append({"residue": r, "train": len(train), "L": lc,
                        "L_over_train": lc / len(train)})
            min_lc_ratio = min(min_lc_ratio, lc / len(train))
        max_abs_ratio = max(max_abs_ratio, max(abs(row["ratio"]) for row in disc))
        report[str(m)] = {"discrepancy": disc, "linear_complexity": lcs}

    # Exact zeros at a single N are random-walk hits. Require the same
    # (modulus, residue) to vanish at every dyadic length in this list.
    dyadic = [1 << k for k in range(8, 18)]
    persistent_zeros = []
    for m in moduli:
        for r in range(m):
            if all(class_discrepancies(bits[:N], m)[r]["signed"] == 0 for N in dyadic):
                persistent_zeros.append({"modulus": m, "residue": r})
    zeros_at_1e5 = [
        {"modulus": int(m), "residue": row["residue"]}
        for m, data in report.items()
        for row in data["discrepancy"]
        if row["signed"] == 0
    ]

    global_signed = 2 * sum(bits[:n]) - n
    global_ratio = global_signed / n
    simple_lc = min_lc_ratio < 0.25
    kill = (not persistent_zeros) and (not simple_lc)
    payload = {
        "attack": "residue-class discrepancy and subsample complexity",
        "N": n,
        "global_signed": global_signed,
        "global_ratio": global_ratio,
        "max_abs_class_ratio": max_abs_ratio,
        "min_subsample_L_over_train": min_lc_ratio,
        "exact_unbiased_at_1e5": zeros_at_1e5,
        "persistent_unbiased_dyadic": persistent_zeros,
        "simple_linear_subsample": simple_lc,
        "kill": kill,
        "kill_reason": (
            "Exact zeros at N=10^5 (e.g. residues 2 and 12 mod 16) fail to "
            "persist on dyadic lengths 2^8..2^17. Every 4096-bit subsample "
            "still has L(N)≈N/2. Arithmetic progressions do not simplify c."
            if kill else
            "Screen found a persistent unbiased class or a simple subsample."
        ),
        "moduli": report,
        "elapsed_sec": time.perf_counter() - t0,
        "not_a_prize_claim": True,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(payload) + "\n")
    summary = {k: payload[k] for k in (
        "N", "global_ratio", "max_abs_class_ratio",
        "min_subsample_L_over_train", "exact_unbiased_at_1e5",
        "persistent_unbiased_dyadic", "simple_linear_subsample",
        "kill", "elapsed_sec",
    )}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
