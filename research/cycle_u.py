#!/usr/bin/env python3
"""Cycle U: de Bruijn factors of the centre; v2 kernel-index templates.

A prefix that contains every binary word of length n proves p(n)=2^n
for the infinite sequence, hence T+p >= 2^n if eventually periodic.
Not a prize claim unless this holds for all n (disjunctive).

Also kill simple predicted disagreement indices for square 2-kernel
columns (v2, popcount, i=0/1).

Run: python3 research/cycle_u.py --certify
Dump: research/cycle_u.json
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


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def missing_words(c, n: int) -> list[str]:
    s = bytes(c)
    have = set()
    # pack sliding n-bit words as ints
    if n > 30 or len(c) < n:
        # fallback
        t = "".join(map(str, c))
        have = {t[i : i + n] for i in range(len(t) - n + 1)}
        return [format(i, f"0{n}b") for i in range(1 << n) if format(i, f"0{n}b") not in have]
    w = 0
    mask = (1 << n) - 1
    for i, b in enumerate(s):
        w = ((w << 1) | b) & mask
        if i >= n - 1:
            have.add(w)
    return [format(i, f"0{n}b") for i in range(1 << n) if i not in have]


def de_bruijn_scan(c) -> dict:
    rows = []
    first_incomplete = None
    for n in range(1, 17):
        miss = missing_words(c, n)
        rec = {
            "n": n,
            "n_missing": len(miss),
            "p_max": 1 << n,
            "complete": len(miss) == 0,
            "missing_head": miss[:8],
        }
        rows.append(rec)
        if miss and first_incomplete is None:
            first_incomplete = n
    complete_through = (first_incomplete - 1) if first_incomplete else 16
    return {
        "N": len(c),
        "complete_through": complete_through,
        "rows": rows,
        "period_lower_bound": (1 << complete_through) if complete_through else 1,
    }


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def kernel_formulas(c) -> dict:
    formulas = {
        "i=0": lambda r, s, k: 0,
        "i=1": lambda r, s, k: 1,
        "v2": lambda r, s, k: v2(s - r),
        "popcount": lambda r, s, k: (r ^ s).bit_count(),
        "k-1": lambda r, s, k: k - 1,
    }
    out = {}
    for name, f in formulas.items():
        fail_k = None
        for k in range(1, 7):
            R = 1 << k
            Imax = min(R, (len(c) - R) // R)
            good = True
            for r in range(R):
                for s in range(r + 1, R):
                    i = f(r, s, k)
                    if i < 0 or i >= Imax or c[r + i * R] == c[s + i * R]:
                        good = False
                        break
                if not good:
                    break
            if not good:
                fail_k = k
                break
        out[name] = {"fail_k": fail_k, "killed": fail_k is not None}
    return {"formulas": out, "kill": all(v["killed"] for v in out.values())}


def self_checks(c20):
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    # length 1 and 2 appear
    s = "".join(map(str, c20))
    assert "0" in s and "1" in s and "00" in s and "11" in s
    return {"all_ok": True, "known20": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 18)
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    checks = self_checks(c20)
    c = packed_center_bits(args.bits)
    db = de_bruijn_scan(c)
    kern = kernel_formulas(c)
    dump = {
        "cycle": "U",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "de_bruijn": db,
        "kernel_formulas": kern,
        "verdict": {
            "de_bruijn_complete_through": db["complete_through"],
            "period_lower_bound": db["period_lower_bound"],
            "kernel_formulas": "KILLED" if kern["kill"] else "OPEN",
            "disjunctive": "NOT_PROVED",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("complete_through", db["complete_through"], "N", db["N"])
    for r in db["rows"]:
        if r["n"] >= 12:
            print(f"  n={r['n']} missing={r['n_missing']} complete={r['complete']} head={r['missing_head'][:4]}")
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
