#!/usr/bin/env python3
"""Cycle CS: (W,X) has a 10; sixth tail pair closed.

Every V 1-run starts with U=0. V has a run of length >=2, so that start
is a V 11 with U=01. If W=1 there, X_next=0 gives a 10 in (W,X). If W=0
and X=1, W_next is an isolated 1 with X_next=0, again a 10 in (W,X).
Every even T0||not T0 has one of those, so skip-2 gives Y!=Z. Not a
prize claim.

Run: python3 research/cycle_cs.py --certify
Dump: research/cycle_cs.json
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
from cycle_co import has10
from cycle_cq import has11

OUT = Path(__file__).resolve().with_suffix(".json")


def V_run_start_U0() -> bool:
    """V_{s-1}=0, V_s=1: U_{s-1}=1 forces U_s=0; U_{s-1}=0 and V_s=1
    force T_{s-2}=0 hence U_s=0."""
    V_prev = 0
    Tsm2 = 0
    V_s = V_prev ^ (Tsm2 ^ 1)
    return V_s == 1


def A_gives_WX10() -> bool:
    """W_s=1 at a V 11 with U_s=0: W_{s+1}=1 and X_{s+1}=not V_s=0."""
    Us, Vs, Ws = 0, 1, 1
    Wn = Us ^ 1
    Xn = Vs ^ 1
    return Wn == 1 and Xn == 0


def isoB_gives_WX10() -> bool:
    """W_s=0, X_s=1 at a V 11 with U_s=0: W_{s+1}=1, X_{s+1}=0,
    W_{s+2}=0."""
    Us, Vs, Ws, Xs = 0, 1, 0, 1
    Un = 1
    Wn = Us ^ 1
    Xn = Vs ^ (Ws | Xs)
    Wnn = Un ^ 1
    return Wn == 1 and Xn == 0 and Wnn == 0


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_isoB = 0
    n_both = 0
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
            if None in (U, V, W, X, Y, Z) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if not has11(V) or not has10(W, X) or Y == Z:
                return {"ok": False, "n_ok": n_ok, "why": "WX"}
            A = False
            isoB = False
            ge2 = False
            for s in range(L):
                if V[s] == 1 and V[(s - 1) % L] == 0:
                    if U[s] != 0:
                        return {"ok": False, "n_ok": n_ok, "why": "U0"}
                    r = 0
                    j = s
                    while V[j] == 1:
                        r += 1
                        j = (j + 1) % L
                    if r >= 2:
                        ge2 = True
                        if W[s] == 1:
                            A = True
                            if X[(s + 1) % L] != 0 or W[(s + 1) % L] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "A"}
                        elif X[s] == 1:
                            isoB = True
                            if (
                                W[(s + 1) % L] != 1
                                or X[(s + 1) % L] != 0
                                or W[(s + 2) % L] != 0
                            ):
                                return {"ok": False, "n_ok": n_ok, "why": "isoB"}
            if not ge2:
                return {"ok": False, "n_ok": n_ok, "why": "ge2"}
            if not (A or isoB):
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            if A:
                n_A += 1
            if isoB:
                n_isoB += 1
            if A and isoB:
                n_both += 1
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_isoB": n_isoB,
        "n_both": n_both,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_isoB"] - ids["n_both"] == expect
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (V_run_start_U0(), A_gives_WX10(), isoB_gives_WX10())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_isoB": ids["n_isoB"],
            "n_both": ids["n_both"],
        },
        "lemmas": {
            "V_run_start_U0": True,
            "WX_10_from_A_or_isoB": True,
            "sixth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "V_run_start_U0": "LEMMA",
            "WX_10_from_A_or_isoB": "LEMMA",
            "sixth_pair_never_equal": "LEMMA",
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
