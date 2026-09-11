#!/usr/bin/env python3
"""Cycle CW: tenth tail pair closed; (P,Q) 10 or P=>Q with P 11.

(P,Q) has a 10 on all but 14 even T0||not T0. Those 14 have P=>Q and
a P 11, hence a Q 11 with R_next=0!=1 (Cycle CN's witness B). Skip-2
or B gives R!=reconstruct(Q,R). Not a prize claim. (P,Q) does not
always have a 10; Q does not always have a 11.

Run: python3 research/cycle_cw.py --certify
Dump: research/cycle_cw.json
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
from cycle_cq import has11
from cycle_cj import n_odd_runs

OUT = Path(__file__).resolve().with_suffix(".json")


def P11_imp_gives_B() -> bool:
    """P_t=P_{t+1}=1 and P=>Q force Q=11 and R_next=not P_t=0 != 1."""
    Pt = Pn = 1
    Rn = Pt ^ 1
    return Rn == 0 and Rn != Pn


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_even_imp = 0
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
            R = reconstruct(P, Q)
            S2 = reconstruct(Q, R) if R is not None else None
            if None in (U, V, W, X, Y, Z, P, Q, R, S2) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if R == S2:
                return {"ok": False, "n_ok": n_ok, "why": "RS"}
            A = has10(P, Q)
            imp = all((not p) or q for p, q in zip(P, Q))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if n_odd_runs(T) != 0:
                    return {"ok": False, "n_ok": n_ok, "why": "odd"}
                n_even_imp += 1
                if not has11(P) or not has11(Q):
                    return {"ok": False, "n_ok": n_ok, "why": "P11"}
                B = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if Q[t] == 1 and R[t] != P[t]:
                        B = True
                    if P[t] == 1 and P[nxt] == 1:
                        if Q[t] != 1 or Q[nxt] != 1:
                            return {"ok": False, "n_ok": n_ok, "why": "Q11"}
                        if R[nxt] != 0:
                            return {"ok": False, "n_ok": n_ok, "why": "R0"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_even_imp": n_even_imp,
    }


def self_checks(c20, loc: tuple[bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_imp"] == ids["n_even_imp"] == 14
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), P11_imp_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_even_imp": ids["n_even_imp"],
        },
        "lemmas": {
            "PQ_10_or_imp": True,
            "imp_P11_gives_B": True,
            "tenth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "PQ_10_or_imp": "LEMMA",
            "imp_P11_gives_B": "LEMMA",
            "tenth_pair_never_equal": "LEMMA",
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
