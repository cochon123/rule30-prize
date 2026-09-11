#!/usr/bin/env python3
"""Cycle CU: eighth tail pair closed; (Y,Z) 10 or Y=>Z witness B.

(Y,Z) has a 10 on all but 234 even T0||not T0. Those 234 have Y=>Z.
Then a Z 11 carries either Y 11 (P_next=0!=1) or Y 00 (P_next=1!=0),
Cycle CN's witness B. Skip-2 or B gives P!=reconstruct(Z,P). Not a
prize claim. (Y,Z) does not always have a 10; Y and Z do not always
have a 11.

Run: python3 research/cycle_cu.py --certify
Dump: research/cycle_cu.json
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


def y11_imp_gives_B() -> bool:
    """Y_t=Y_{t+1}=1 and Y=>Z force Z=11 and P_next=not Y_t=0 != 1."""
    Yt = Yn = 1
    Pn = Yt ^ 1
    return Pn == 0 and Pn != Yn


def y00_Z11_gives_B() -> bool:
    """Y=00 on a Z 11: P_next=Y XOR 1=1 != 0."""
    Yt = 0
    Pn = Yt ^ 1
    return Pn == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_Y11 = 0
    n_Y00 = 0
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
            Q = reconstruct(Z, P) if P is not None else None
            if None in (U, V, W, X, Y, Z, P, Q) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if P == Q:
                return {"ok": False, "n_ok": n_ok, "why": "PQ"}
            A = has10(Y, Z)
            imp = all((not y) or z for y, z in zip(Y, Z))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if not has11(Z):
                    return {"ok": False, "n_ok": n_ok, "why": "Z11"}
                Y11 = False
                Y00 = False
                B = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if Z[t] == 1 and P[t] != Y[t]:
                        B = True
                    if Z[t] == 1 and Z[nxt] == 1:
                        if Y[t] == 1 and Y[nxt] == 1:
                            Y11 = True
                            if P[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "Y11P"}
                        if Y[t] == 0 and Y[nxt] == 0:
                            Y00 = True
                            if P[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "Y00P"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if Y11:
                    n_Y11 += 1
                elif Y00:
                    n_Y00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_Y11": n_Y11,
        "n_Y00": n_Y00,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_Y11"] + ids["n_Y00"] == ids["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), y11_imp_gives_B(), y00_Z11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_Y11": ids["n_Y11"],
            "n_Y00": ids["n_Y00"],
        },
        "lemmas": {
            "YZ_10_or_imp": True,
            "imp_Z11_Y11_or_Y00": True,
            "eighth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "YZ_10_or_imp": "LEMMA",
            "imp_Z11_Y11_or_Y00": "LEMMA",
            "eighth_pair_never_equal": "LEMMA",
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
