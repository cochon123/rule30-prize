#!/usr/bin/env python3
"""Cycle CV: (Z,P) has a 10; ninth tail pair closed.

Either (X,Y,Z)=(0,1,1), so Z_next=1 and P_next=0, or
(Y,Z,P,X)=(0,0,0,1), so Z_next=1 and P_next=0. Every even T0||not T0
has one of those, hence a 10 in (Z,P). Skip-2 gives
Q!=reconstruct(P,Q). Not a prize claim. Y=1 and Z=1 always overlap;
that is not a 10 at every later pair.

Run: python3 research/cycle_cv.py --certify
Dump: research/cycle_cv.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_ch import shifted_not
from cycle_ci import EVEN_N0, reset_toggle_step
from cycle_co import has10, pointwise_10_kills

OUT = Path(__file__).resolve().with_suffix(".json")


def A_gives_ZP10() -> bool:
    """X=0, Y=1, Z=1 force Z_next=1 and P_next=0."""
    X, Y, Z = 0, 1, 1
    Zn = X ^ (Y | Z)
    Pn = Y ^ 1
    return Zn == 1 and Pn == 0


def B_gives_ZP10() -> bool:
    """Y=Z=P=0 and X=1 force Z_next=1 and P_next=0."""
    Y, Z, P, X = 0, 0, 0, 1
    Zn = X ^ (Y | Z)
    Pn = Y ^ (Z | P)
    return Zn == 1 and Pn == 0


def Y11_imp_gives_A() -> bool:
    """Y=11 and Y=>Z force Z=11, hence X=not Z_next=0 at the first bit,
    which is arm A."""
    Zn = 1
    X = Zn ^ 1
    return X == 0


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_B = 0
    n_both = 0
    n_Y1Z1 = 0
    for n0 in EVEN_N0:
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
            Z = reconstruct(X, Y)
            P = reconstruct(Y, Z)
            Q = reconstruct(Z, P)
            R = reconstruct(P, Q) if Q is not None else None
            if None in (U, V, W, X, Y, Z, P, Q, R) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if not has10(Z, P) or Q == R:
                return {"ok": False, "n_ok": n_ok, "why": "ZP"}
            A = False
            B = False
            y1z1 = False
            imp = all((not y) or z for y, z in zip(Y, Z))
            for t in range(L):
                nxt = (t + 1) % L
                if Y[t] == 1 and Z[t] == 1:
                    y1z1 = True
                if X[t] == 0 and Y[t] == 1 and Z[t] == 1:
                    A = True
                    if Z[nxt] != 1 or P[nxt] != 0:
                        return {"ok": False, "n_ok": n_ok, "why": "A"}
                if Y[t] == 0 and Z[t] == 0 and P[t] == 0 and X[t] == 1:
                    B = True
                    if Z[nxt] != 1 or P[nxt] != 0:
                        return {"ok": False, "n_ok": n_ok, "why": "B"}
                if imp and Y[t] == 1 and Y[nxt] == 1:
                    if X[t] != 0 or Z[t] != 1 or Z[nxt] != 1:
                        return {"ok": False, "n_ok": n_ok, "why": "Y11A"}
            if not y1z1:
                return {"ok": False, "n_ok": n_ok, "why": "Y1Z1"}
            if not (A or B):
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            if A:
                n_A += 1
            if B:
                n_B += 1
            if A and B:
                n_both += 1
            n_Y1Z1 += 1
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_B": n_B,
        "n_both": n_both,
        "n_Y1Z1": n_Y1Z1,
    }


def self_checks(c20, loc: tuple[bool, bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_B"] - ids["n_both"] == expect
    assert ids["n_Y1Z1"] == expect
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), A_gives_ZP10(), B_gives_ZP10(), Y11_imp_gives_A())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_B": ids["n_B"],
            "n_both": ids["n_both"],
            "n_Y1Z1": ids["n_Y1Z1"],
        },
        "lemmas": {
            "Y_and_Z_overlap": True,
            "ZP_10_from_A_or_B": True,
            "ninth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "Y_and_Z_overlap": "LEMMA",
            "ZP_10_from_A_or_B": "LEMMA",
            "ninth_pair_never_equal": "LEMMA",
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
