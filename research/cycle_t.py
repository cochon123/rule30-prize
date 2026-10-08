#!/usr/bin/env python3
"""Cycle T: isolated-one strips, packed D current, kernel φ_k / square k=10.

Attacks from ideas17 plus the isolated-one dual of isolated zeros.
Not a prize claim.

1. Isolated-one words 10^q at radius 6. Survive only if some tail of q
   has a unique recurrent SCC with a forced periodic neighbor (Jen).
   Kill if every q=1..17 has a residual SCC.

2. ideas17 packed current: D(N) equals popcount-excess of the packed
   row, or any of popcount / XOR-popcount / AND-popcount, or a bounded
   local current of (ℓ,c,r). Kill if correlations are O(1) and |D|
   grows (no bounded J with e=ΔJ).

3. Kernel: φ_k(r)=first i with c_{i 2^k}≠c_{r+i 2^k} injective would
   prove distinct columns. Kill that template if φ_k is not injective
   for some k≤8. Separately check square columns at k=10 if N allows.

Run: python3 research/cycle_t.py --certify
Dump: research/cycle_t.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step
from strip_graph import analyze

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def isolated_one_scan(qmax=17, radius=6):
    rows = []
    all_residual = True
    for q in range(1, qmax + 1):
        word = [1] + [0] * q
        a = analyze(radius, word)
        rec = a["recurrent_components"]
        res = a["components_without_forced_periodic_neighbor"]
        rows.append(
            {
                "q": q,
                "word": a["center_word"],
                "n_recurrent": rec,
                "n_residual": res,
                "residual_sizes": a["residual_sizes"][:6],
            }
        )
        if res == 0:
            all_residual = False
    return {
        "qmax": qmax,
        "radius": radius,
        "rows": rows,
        "all_have_residual": all_residual,
        "kill": all_residual,
    }


def corr(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def packed_D_current(N: int):
    row = 1
    Ds = []
    excess = []
    pcs = []
    ones = 0
    e_id_ok = True
    n11 = n00 = 0
    prev = None
    for t in range(N):
        bit = (row >> t) & 1
        ones += bit
        D = 2 * ones - (t + 1)
        width = 2 * t + 1
        pc = row.bit_count()
        Ds.append(D)
        excess.append(pc - (width + 1) // 2)
        pcs.append(pc)
        if prev is not None:
            e = prev + bit - 1  # c_t + c_{t+1} - 1 at time t-1
            if prev == 1 and bit == 1:
                n11 += 1
            if prev == 0 and bit == 0:
                n00 += 1
            # running: sum e = n11-n00 after t pairs? pairs among 0..t
        prev = bit
        row = rule30_step(row)
    # identity over Z: e_t = c_t + c_{t+1} - 1
    # sum_{t<N-1} e = n11-n00; D(N)=n11-n00+c_{N-1}
    c_last = prev
    rhs = n11 - n00 + c_last
    D_N = Ds[-1]
    id_ok = D_N == rhs
    return {
        "N": N,
        "D": D_N,
        "n11": n11,
        "n00": n00,
        "e_sum_identity": id_ok,
        "corr_excess": round(corr(Ds, excess), 4),
        "corr_popcount": round(corr(Ds, pcs), 4),
        "corr_t": round(corr(Ds, list(range(N))), 4),
        "n_D_eq_excess": sum(a == b for a, b in zip(Ds, excess)),
        "kill_packed_current": abs(corr(Ds, excess)) < 0.2 and D_N != 0,
        "kill_bounded_J": abs(D_N) > 10,  # |D| grows; no bounded local current
    }


def phi_injective(c: bytearray, kmax=8):
    rows = []
    first_fail = None
    for k in range(1, kmax + 1):
        R = 1 << k
        Imax = min(4 * R, (len(c) - R) // R)
        ph = []
        for r in range(1, R):
            found = None
            for i in range(Imax):
                if c[i * R] != c[r + i * R]:
                    found = i
                    break
            ph.append(found)
        inj = len(set(ph)) == len(ph) and None not in ph
        if not inj and first_fail is None:
            first_fail = k
        rows.append(
            {
                "k": k,
                "injective": inj,
                "n_unique": len(set(ph)),
                "n_r": R - 1,
                "n_missing": sum(v is None for v in ph),
                "max_phi": max((v for v in ph if v is not None), default=None),
            }
        )
    return {
        "rows": rows,
        "first_fail": first_fail,
        "kill_template": first_fail is not None,
    }


def square_columns(c: bytearray, k: int):
    R = 1 << k
    need = (R - 1) * R + (R - 1)
    if need >= len(c):
        return {"k": k, "supported": False}
    cols = set()
    for r in range(R):
        w = 0
        for i in range(R):
            w = (w << 1) | c[r + i * R]
        cols.add(w)
    return {
        "k": k,
        "supported": True,
        "distinct": len(cols) == R,
        "n_distinct": len(cols),
        "n": R,
    }


def self_checks():
    c = packed_center_bits(20)
    assert list(c) == KNOWN20
    assert list(c) == list(experiment_center_bits(20))
    # e_t = c_t + c_{t+1} - 1
    for t in range(19):
        e = (1 if c[t] == 1 and c[t + 1] == 1 else 0) - (
            1 if c[t] == 0 and c[t + 1] == 0 else 0
        )
        assert e == c[t] + c[t + 1] - 1
    a = analyze(6, [1, 0])
    assert a["components_without_forced_periodic_neighbor"] >= 1
    return {"all_ok": True, "e_identity": True, "period2_residual": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 18)
    args = parser.parse_args()
    t0 = time.perf_counter()
    checks = self_checks()
    iso = isolated_one_scan()
    packed = packed_D_current(1 << 12)
    c = packed_center_bits(args.bits)
    phi = phi_injective(c)
    squares = [square_columns(c, k) for k in range(0, 10)]
    # k=10 needs ~2^20; only if bits large enough
    sq10 = square_columns(c, 10)
    dump = {
        "cycle": "T",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "isolated_one": iso,
        "packed_D": packed,
        "phi": phi,
        "square": squares,
        "square_k10": sq10,
        "verdict": {
            "isolated_one": "KILLED" if iso["kill"] else "OPEN",
            "packed_D": "KILLED" if packed["kill_packed_current"] else "OPEN",
            "phi_template": "KILLED" if phi["kill_template"] else "OPEN",
            "square_k9": "distinct"
            if all(s.get("distinct") for s in squares if s.get("supported"))
            else "collision",
            "square_k10": sq10,
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2, default=str))
    print("iso q residual", [r["n_residual"] for r in iso["rows"]])
    print("packed", {k: packed[k] for k in packed if k != "N"})
    print("phi first_fail", phi["first_fail"], phi["rows"][:4])
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
