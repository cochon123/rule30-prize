#!/usr/bin/env python3
"""u_0 is absent from F_k (k>=3) and from every G_k.

On a phase-01 period-2 centre, F_1=1+u_0 and F_2=u_0, but F_k for
k>=3 is independent of u_0 in the Fibonacci ring, and no G_k contains
u_0. Proof: F_1 OR F_2 = 1, so F_3=1+u_1; F_4=0 on the ring; G_k =
S F_{k-1} XOR (G_{k-1} OR G_{k-2}) never creates u_0 (S raises
indices); then F_k for k>=5 is assembled from G_{k-1} and F_{k-1},
F_{k-2}, all already free of u_0. Consequently every onset T>=3 is
unchanged by flipping u_0, and for odd T the leading-variable identity
forces the last prefix bit from u_1,...,u_{nvars(T)-2}. Not a prize
claim: extra is still not bounded.

Run: python3 research/period2_silent.py --certify
Dump: research/period2_silent.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import force
from period2_left_edge import anf_vars, compute_columns
from period2_ugap_sat import ugap_ok, ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def certify_anf(kmax: int = 20):
    F, G = compute_columns(kmax, reduce=True)
    rows = []
    for k in range(0, kmax + 1):
        fv = anf_vars(F[k])
        gv = anf_vars(G[k])
        rec = {
            "k": k,
            "F_vars": fv,
            "G_vars": gv,
            "F_has_u0": 0 in fv,
            "G_has_u0": 0 in gv,
        }
        rows.append(rec)
        assert 0 not in gv, rec
        if k >= 3:
            assert 0 not in fv, rec
        elif k in (1, 2):
            assert 0 in fv, rec
    # F_1 OR F_2 = 1 on the ring: F_3 = 1+u_1 has no u_0
    assert rows[3]["F_vars"] == [1]
    assert rows[4]["F_vars"] == []
    return {"kmax": kmax, "ok": True, "rows": rows}


def fib_ok(u):
    return all(a + b < 2 for a, b in zip(u, u[1:]))


def flip_u0(u):
    v = list(u)
    v[0] = 1 - v[0]
    return v


def certify_flip(Tmin=5, Tmax=32):
    n_on = 0
    n_legal_flip = 0
    n_match = 0
    n_F_same = 0
    n_words = 0
    odd_last = []
    for T in range(Tmin, Tmax + 1):
        if T == 4:
            continue
        n0 = nvars(T)
        kneed = max(T + 2, 2 * n0 + 2)
        last_by = defaultdict(set)
        for u in ugap_strings(n0):
            n_words += 1
            F, _ = F_of_u(u, kneed)
            v = flip_u0(u)
            if fib_ok(v):
                Fv, _ = F_of_u(v, kneed)
                assert F[T] == Fv[T]
                n_F_same += 1
            if F[T] != 1:
                continue
            n_on += 1
            rec = force(u, T)
            assert rec is not None
            if T % 2 == 1 and n0 >= 2:
                last_by[wstr(u[1:-1])].add(u[-1])
            if not (fib_ok(v) and ugap_ok(v)):
                continue
            n_legal_flip += 1
            rec2 = force(v, T)
            assert rec2 is not None
            assert rec2["kind"] == rec["kind"]
            assert rec2["stop"] == rec["stop"]
            assert rec2["extra"] == rec["extra"]
            n_match += 1
        if T % 2 == 1:
            n_unique = sum(1 for s in last_by.values() if len(s) == 1)
            n_groups = len(last_by)
            odd_last.append({"T": T, "n_groups": n_groups, "n_unique_last": n_unique})
            assert n_groups == n_unique
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_words": n_words,
        "n_F_T_same_on_flip": n_F_same,
        "n_onset": n_on,
        "n_legal_flip": n_legal_flip,
        "n_extra_match": n_match,
        "odd_T_last_bit": odd_last,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    anf = certify_anf(20)
    checks["anf_u0_absent_k_ge_3"] = True
    checks["G_never_has_u0"] = True
    checks["F3_is_1_plus_u1"] = True
    checks["F4_zero"] = True
    flip = certify_flip(5, 32)
    checks["F_T_independent_of_u0"] = True
    checks["extra_kind_stop_match_on_legal_flip"] = True
    checks["odd_T_last_prefix_bit_forced"] = True
    return {
        "checks": checks,
        "anf": {k: anf[k] for k in ("kmax", "ok")},
        "anf_support": [
            {"k": r["k"], "F_vars": r["F_vars"], "G_vars": r["G_vars"]}
            for r in anf["rows"]
            if r["k"] <= 8
        ],
        "flip": flip,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("anf_support", report["anf_support"])
    fl = report["flip"]
    print(
        "flip",
        {k: fl[k] for k in ("n_words", "n_onset", "n_legal_flip", "n_extra_match")},
    )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
