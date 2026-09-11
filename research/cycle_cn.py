#!/usr/bin/env python3
"""Cycle CN: unique continuation always splits on B; fifth pair never equal.

Packed update C'=A XOR (B OR C) splits pointwise: if B=1 then C'=not A,
if B=0 then C'=A XOR C, hence DC=A. That is the same split used for U,V,W,X.
Y=reconstruct(W,X) equals X iff W=DX, iff V implies W and (W=1 implies X=V).
Every even T0||not T0 through length 16 has V=1 W=0 or W=1 with X!=V, so
Y!=X. Not a prize claim: later ident-0 and the Fermat covering remain
prefixes.

Run: python3 research/cycle_cn.py --certify
Dump: research/cycle_cn.json
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
from cycle_ca import KNOWN20, deriv, packed_center_bits, reconstruct
from cycle_ch import ham, shifted_not
from cycle_ci import EVEN_N0, reset_toggle_step

OUT = Path(__file__).resolve().with_suffix(".json")


def pointwise_split() -> bool:
    """C' = A XOR (B OR C): B=1 => C'=not A; B=0 => C XOR C' = A."""
    for A in (0, 1):
        for B in (0, 1):
            for C in (0, 1):
                Cp = A ^ (B | C)
                if B == 1 and Cp != (A ^ 1):
                    return False
                if B == 0 and (C ^ Cp) != A:
                    return False
    return True


def identities_even_n0() -> dict:
    n_ok = 0
    min_xy: dict[int, int] = {}
    n_A = 0
    n_B = 0
    n_neither = 0
    for n0 in EVEN_N0:
        minh = 10**9
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            T = T0 + [x ^ 1 for x in T0]
            L = len(T)
            S = shifted_not(T)
            U = reconstruct([1] * L, S)
            V = reconstruct(S, U)
            W = reconstruct(U, V)
            X = reconstruct(V, W)
            Y = reconstruct(W, X)
            if None in (U, V, W, X, Y) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            DX = deriv(X)
            if W == DX or X == Y:
                return {"ok": False, "n_ok": n_ok, "why": "equal"}
            A = False
            B = False
            for t in range(L):
                nxt = (t + 1) % L
                if W[t] == 0 and DX[t] != V[t]:
                    return {"ok": False, "n_ok": n_ok, "why": "W0_DX"}
                if Y[nxt] != (W[t] ^ (X[t] | Y[t])):
                    return {"ok": False, "n_ok": n_ok, "why": "Y_update"}
                if V[t] == 1 and W[t] == 0:
                    A = True
                if W[t] == 1 and X[t] != V[t]:
                    B = True
            if A:
                n_A += 1
            if B:
                n_B += 1
            if not (A or B):
                n_neither += 1
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            h = ham(X, Y)
            if h < minh:
                minh = h
            n_ok += 1
        min_xy[n0] = minh
    return {
        "ok": True,
        "n_ok": n_ok,
        "min_xy": min_xy,
        "n_A": n_A,
        "n_B": n_B,
        "n_neither": n_neither,
    }


def self_checks(c20, split: bool, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert split
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["n_neither"] == 0
    assert ids["min_xy"][2] >= 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    split = pointwise_split()
    ids = identities_even_n0()
    checks = self_checks(c20, split, ids)
    dump = {
        "cycle": "CN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "min_xy": ids["min_xy"],
            "n_A": ids["n_A"],
            "n_B": ids["n_B"],
            "n_neither": ids["n_neither"],
        },
        "lemmas": {
            "pointwise_split": True,
            "B0_implies_DC_eq_A": True,
            "fifth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "pointwise_split": "LEMMA",
            "B0_implies_DC_eq_A": "LEMMA",
            "fifth_pair_never_equal": "LEMMA",
            "all_T0_2power_hamming_ge_1": "PREFIX",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("identities", dump["identities"])


if __name__ == "__main__":
    main()
