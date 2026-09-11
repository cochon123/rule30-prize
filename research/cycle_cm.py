#!/usr/bin/env python3
"""Cycle CM: the fourth scar-tail pair is never equal; V=0 implies DW=U.

X=reconstruct(V,W) splits on W. When V_t=0, DW_t=U_t, so V=DW iff
U implies V and (V=1 implies W=U). Every even T0||not T0 has a witness
against that: some U=1 V=0, or some V=1 with W!=U. Hence X!=W for every
even |T0|>=2, including |T0|=2 where ham(W,X)=1. Not a prize claim:
later ident-0 and the Fermat covering remain prefixes.

Run: python3 research/cycle_cm.py --certify
Dump: research/cycle_cm.json
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


def identities_even_n0() -> dict:
    n_ok = 0
    min_wx: dict[int, int] = {}
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
            if None in (U, V, W, X) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            DW = deriv(W)
            if V == DW or W == X:
                return {"ok": False, "n_ok": n_ok, "why": "equal"}
            A = False
            B = False
            for t in range(L):
                nxt = (t + 1) % L
                if V[t] == 0 and DW[t] != U[t]:
                    return {"ok": False, "n_ok": n_ok, "why": "DW_U"}
                if W[t] == 1:
                    pred = V[t] ^ 1
                else:
                    pred = V[t] ^ X[t]
                if X[nxt] != pred:
                    return {"ok": False, "n_ok": n_ok, "why": "X_split"}
                if U[t] == 1 and V[t] == 0:
                    A = True
                if V[t] == 1 and W[t] != U[t]:
                    B = True
            if A:
                n_A += 1
            if B:
                n_B += 1
            if not (A or B):
                n_neither += 1
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            h = ham(W, X)
            if h < n0 // 2:
                return {"ok": False, "n_ok": n_ok, "why": "ham", "h": h}
            if h < minh:
                minh = h
            n_ok += 1
        min_wx[n0] = minh
    return {
        "ok": True,
        "n_ok": n_ok,
        "min_wx": min_wx,
        "n_A": n_A,
        "n_B": n_B,
        "n_neither": n_neither,
    }


def self_checks(c20, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["n_neither"] == 0
    for n0, m in ids["min_wx"].items():
        assert m == n0 // 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ids = identities_even_n0()
    checks = self_checks(c20, ids)
    dump = {
        "cycle": "CM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "min_wx": ids["min_wx"],
            "n_A": ids["n_A"],
            "n_B": ids["n_B"],
            "n_neither": ids["n_neither"],
        },
        "lemmas": {
            "X_splits_on_W": True,
            "V0_implies_DW_eq_U": True,
            "complementary_witnesses_A_or_B": True,
            "fourth_pair_never_equal": True,
            "ham_WX_ge_n0_half": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "X_splits_on_W": "LEMMA",
            "V0_implies_DW_eq_U": "LEMMA",
            "complementary_witnesses_A_or_B": "LEMMA",
            "fourth_pair_never_equal": "LEMMA",
            "ham_WX_ge_n0_half": "LEMMA",
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
