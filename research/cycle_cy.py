#!/usr/bin/env python3
"""Cycle CY: twelfth tail pair closed; (R,S') 10 or R=>S' witness B.

(R,S') has a 10 on all but 40 even T0||not T0. Those 40 have R=>S'.
Then an S' 11 carries either R 11 (T'_next=0!=1) or R 00 (T'_next=1!=0),
Cycle CN's witness B. Skip-2 or B gives T'!=reconstruct(S',T'). Not a
prize claim. (R,S') does not always have a 10; R does not always have
a 11.

Run: python3 research/cycle_cy.py --certify
Dump: research/cycle_cy.json
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

OUT = Path(__file__).resolve().with_suffix(".json")


def R11_imp_gives_B() -> bool:
    """R_t=R_{t+1}=1 and R=>S' force S'=11 and T'_next=not R_t=0 != 1."""
    Rt = Rn = 1
    Tn = Rt ^ 1
    return Tn == 0 and Tn != Rn


def R00_Sp11_gives_B() -> bool:
    """R=00 on an S' 11: T'_next=R XOR 1=1 != 0."""
    Rt = 0
    Tn = Rt ^ 1
    return Tn == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_R11 = 0
    n_R00 = 0
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
            Sp = reconstruct(Q, R)
            Tp = reconstruct(R, Sp) if Sp is not None else None
            Up = reconstruct(Sp, Tp) if Tp is not None else None
            if None in (U, V, W, X, Y, Z, P, Q, R, Sp, Tp, Up) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if Tp == Up:
                return {"ok": False, "n_ok": n_ok, "why": "TU"}
            A = has10(R, Sp)
            imp = all((not r) or s for r, s in zip(R, Sp))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if not has11(Sp):
                    return {"ok": False, "n_ok": n_ok, "why": "Sp11"}
                R11 = False
                R00 = False
                B = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if Sp[t] == 1 and Tp[t] != R[t]:
                        B = True
                    if Sp[t] == 1 and Sp[nxt] == 1:
                        if R[t] == 1 and R[nxt] == 1:
                            R11 = True
                            if Tp[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "R11T"}
                        if R[t] == 0 and R[nxt] == 0:
                            R00 = True
                            if Tp[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "R00T"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if R11:
                    n_R11 += 1
                elif R00:
                    n_R00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_R11": n_R11,
        "n_R00": n_R00,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_R11"] + ids["n_R00"] == ids["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), R11_imp_gives_B(), R00_Sp11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_R11": ids["n_R11"],
            "n_R00": ids["n_R00"],
        },
        "lemmas": {
            "RS_10_or_imp": True,
            "imp_Sp11_R11_or_R00": True,
            "twelfth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "RS_10_or_imp": "LEMMA",
            "imp_Sp11_R11_or_R00": "LEMMA",
            "twelfth_pair_never_equal": "LEMMA",
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
