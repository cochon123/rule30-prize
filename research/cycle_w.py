#!/usr/bin/env python3
"""Cycle W: coupled drain on T=20 models; c_{2^k} formulas; centre 11 production.

Attacks from research/_astra_ideas15.md items 1–2 (never run) and
research/_astra_ideas20.md. Not a prize claim unless a named lemma
excludes every eventual period.

1. Coupled (u,e,f) drain vs the three X-legal T=20, R=16 L_0 words.
   Kill if those words already contain a 4-zero drain and F still has
   16 zeros after a 1, or already disagree with vacuum on many odd
   columns. Survive only with a T-uniform identity.

2. Closed form for b_k = c_{2^k} (Rowland right-run, a(n) parity,
   v2, popcount). Kill if every template fails by k<=12. Aperiodicity
   of (b_k) would prove Problem 1.

3. Right diagonals from the centre: j |-> x(k+j, j) is periodic
   (Rowland). Hunt whether the period or the word determines c_k, or
   whether 11 is forced on the centre infinitely often at k=2^n.

Run: python3 research/cycle_w.py --certify
Dump: research/cycle_w.json
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
from period2_vacuum import F_of_u, nvars, vacuum_F

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]

# Cycle Q: X-legal last-sat models at T=20, R=16.
T20_X = [
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
]

# Rowland a(n) = λ_I(2^n), n=0..17 (paper, n<=40 published).
ROWLAND_A = [
    1, 3, 4, 6, 7, 9, 15, 16, 24, 25, 27, 29, 34, 36, 37, 39, 41, 43,
]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def max_zero_run(bits) -> int:
    m = z = 0
    for b in bits:
        if b:
            z = 0
        else:
            z += 1
            m = max(m, z)
    return m


def has_block(bits, block) -> bool:
    L = len(block)
    for i in range(len(bits) - L + 1):
        if list(bits[i : i + L]) == block:
            return True
    return False


def longest_1_then_zeros(F) -> tuple[int, int]:
    """Max R such that some T has F[T]=1 and F[T+1:T+1+R] all 0. Return (T,R)."""
    best_t, best_r = 0, 0
    n = len(F)
    for T in range(n):
        if F[T] != 1:
            continue
        r = 0
        while T + 1 + r < n and F[T + 1 + r] == 0:
            r += 1
        if r > best_r:
            best_t, best_r = T, r
    return best_t, best_r


def t20_drain_attack() -> dict:
    rows = []
    kill_vac = True
    for u in T20_X:
        # sound: nvars(20+16)=nvars(36)=18, word length 18.
        assert nvars(36) == len(u)
        F, G = F_of_u(u, 40)
        assert F[20] == 1
        assert all(F[20 + d] == 0 for d in range(1, 17))
        # F_37=1 on the unique extra 0 (Cycle Q)
        F2, _ = F_of_u(u + [0], 40)
        odd_dis = 0
        for k in range(41):
            if (k % 2 == 1) and F[k] != vacuum_F(k):
                odd_dis += 1
        rec = {
            "u": "".join(map(str, u)),
            "max_zero_run_u": max_zero_run(u),
            "has_0000": has_block(u, [0, 0, 0, 0]),
            "F20": int(F[20]),
            "R16": True,
            "F37_extra0": int(F2[37]),
            "odd_disagreements_with_vacuum": odd_dis,
            "best_1_then_zeros": longest_1_then_zeros(F),
        }
        rows.append(rec)
        if odd_dis < 8:
            kill_vac = False
    # ideas15.1: kill if the 4-zero drain can sit inside a last-sat model.
    n_with_drain = sum(1 for r in rows if r["has_0000"])
    kill_drain = n_with_drain > 0
    return {
        "models": rows,
        "n_with_0000": n_with_drain,
        "kill_coupled_drain": kill_drain,
        "kill_vacuum_odd": kill_vac,
        "gap3_model_exists": any(r["max_zero_run_u"] <= 3 for r in rows),
    }


def spacetime_rows(tmax: int):
    """rows[t] packed; bit j+t is x(t,j)."""
    row = 1
    out = []
    for t in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def x_of(rows, t, j) -> int:
    if t < 0 or t >= len(rows):
        return 0
    if j + t < 0:
        return 0
    return (rows[t] >> (j + t)) & 1


def right_run(rows, t: int) -> int:
    """Number of consecutive 1s inward from the right edge x(t,t)."""
    n = 0
    while t - n >= -t and x_of(rows, t, t - n) == 1:
        n += 1
        if n > 2 * t + 2:
            break
    return n


def diagonal_period(seq, min_repeats: int = 2) -> int | None:
    n = len(seq)
    for p in range(1, n // min_repeats + 1):
        if all(seq[i] == seq[i % p] for i in range(n)):
            return p
    return None


def centre_diagonals(rows, kmax: int, jmax: int) -> dict:
    recs = []
    for k in range(kmax + 1):
        seq = [x_of(rows, k + j, j) for j in range(jmax)]
        p = diagonal_period(seq)
        recs.append(
            {
                "k": k,
                "c": seq[0] if seq else None,
                "period": p,
                "word": "".join(map(str, seq[: p or 16])),
                "head": "".join(map(str, seq[:16])),
            }
        )
    # is period a closed function of k?
    periods = [r["period"] for r in recs]
    return {"rows": recs, "periods": periods}


def pow2_formulas(c) -> dict:
    N = len(c)
    ks = []
    k = 0
    while (1 << k) < N:
        ks.append(k)
        k += 1
    b = [int(c[1 << k]) for k in ks]
    # also c_{2^k-1} and pair (c_{2^k}, c_{2^k+1})
    pairs = []
    n11 = 0
    for k in ks:
        t = 1 << k
        a = int(c[t - 1]) if t >= 1 else None
        d = int(c[t + 1]) if t + 1 < N else None
        pair11 = b[k] == 1 and d == 1
        pair00 = b[k] == 0 and d == 0
        if pair11:
            n11 += 1
        pairs.append(
            {
                "k": k,
                "c_tm1": a,
                "c_t": b[k],
                "c_tp1": d,
                "11": pair11,
                "00": pair00,
            }
        )
    templates = {}
    # predicted b[k] from simple functions; skip k=0 if needed
    preds = {
        "k_mod2": lambda k: k & 1,
        "not_k_mod2": lambda k: 1 - (k & 1),
        "popcount_mod2": lambda k: k.bit_count() & 1,
        "v2_kplus1_mod2": lambda k: ((k + 1) & -(k + 1)).bit_length() & 1,
        "rowland_a_mod2": lambda k: ROWLAND_A[k] & 1 if k < len(ROWLAND_A) else None,
        "rowland_a_gt_k": lambda k: 1 if k < len(ROWLAND_A) and ROWLAND_A[k] > k else 0,
        "always1": lambda k: 1,
        "always0": lambda k: 0,
        "k_ge_2": lambda k: 1 if k >= 2 else 0,
    }
    for name, f in preds.items():
        fail = None
        for k in ks:
            pred = f(k)
            if pred is None:
                continue
            if pred != b[k]:
                fail = k
                break
        templates[name] = {"fail_k": fail, "killed": fail is not None}
    return {
        "b": b,
        "pairs": pairs,
        "n11_at_2k": n11,
        "templates": templates,
        "all_templates_killed": all(v["killed"] for v in templates.values()),
    }


def lc_at_pow2(rows, kmax: int) -> dict:
    """(l,c)=(0,1) is a centre 11. Check at t=2^k."""
    hits = []
    for k in range(kmax + 1):
        t = 1 << k
        if t >= len(rows):
            break
        l = x_of(rows, t, -1)
        c = x_of(rows, t, 0)
        r = x_of(rows, t, 1)
        hits.append(
            {
                "k": k,
                "t": t,
                "lcr": f"{l}{c}{r}",
                "is_11": l == 0 and c == 1,
            }
        )
    return {
        "rows": hits,
        "n11": sum(1 for h in hits if h["is_11"]),
        "uniform_11": all(h["is_11"] for h in hits),
    }


def self_checks(c20):
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    u = T20_X[0]
    F, _ = F_of_u(u, 40)
    assert F[20] == 1 and F[21] == 0
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 16)
    parser.add_argument("--tmax", type=int, default=256)
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    checks = self_checks(c20)
    drain = t20_drain_attack()
    c = packed_center_bits(args.bits)
    formulas = pow2_formulas(c)
    rows = spacetime_rows(args.tmax)
    diags = centre_diagonals(rows, kmax=64, jmax=128)
    lc = lc_at_pow2(rows, kmax=8)
    # right-run at 2^k vs b_k
    run_rows = []
    for k in range(0, min(8, (args.tmax).bit_length())):
        t = 1 << k
        if t > args.tmax:
            break
        rr = right_run(rows, t)
        run_rows.append({"k": k, "t": t, "right_run": rr, "c": int(c[t]) if t < len(c) else None})

    dump = {
        "cycle": "W",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "t20_drain": drain,
        "pow2": formulas,
        "diagonals_head": diags["rows"][:12],
        "diagonal_periods": diags["periods"][:33],
        "lc_pow2": lc,
        "right_run_pow2": run_rows,
        "verdict": {
            "coupled_drain": "KILLED" if drain["kill_coupled_drain"] else "OPEN",
            "gap3_without_0000": drain.get("gap3_model_exists"),
            "vacuum_odd": "KILLED" if drain["kill_vacuum_odd"] else "OPEN",
            "b_k_templates": "KILLED" if formulas["all_templates_killed"] else "OPEN",
            "uniform_11_at_2k": lc["uniform_11"],
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("t20", [{k: m[k] for k in ("u", "has_0000", "max_zero_run_u", "odd_disagreements_with_vacuum", "F37_extra0")} for m in drain["models"]])
    print("b", formulas["b"])
    print("n11_at_2k", formulas["n11_at_2k"], "pairs", formulas["pairs"][:8])
    print("templates", {n: v["fail_k"] for n, v in formulas["templates"].items()})
    print("diag periods", diags["periods"][:33])
    print("lc", lc)
    print("right_run", run_rows)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
