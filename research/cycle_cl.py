#!/usr/bin/env python3
"""Cycle CL: the third scar-tail pair is never equal; 00 forces U!=DV.

W=reconstruct(U,V) splits on V: if V_t=1 then W_{t+1}=not U_t, else
W_{t+1}=U_t XOR W_t. When U_t=0, DV_t=S_t. A 00 in T at (t-2,t-1)
gives U_t=0 and S_t=1, so U!=DV. Even T0||not T0 is not alternating
and therefore has a 00, hence W!=V for every even |T0|>=2. Not a
prize claim: later pairs and the Fermat covering remain prefixes.

Run: python3 research/cycle_cl.py --certify
Dump: research/cycle_cl.json
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


def has00(T: list[int]) -> bool:
    L = len(T)
    return any(T[i] == 0 and T[(i + 1) % L] == 0 for i in range(L))


def identities_even_n0() -> dict:
    n_ok = 0
    min_vw: dict[int, int] = {}
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
            if U is None or V is None or W is None or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if not has00(T):
                return {"ok": False, "n_ok": n_ok, "why": "no00"}
            DV = deriv(V)
            if U == DV or V == W:
                return {"ok": False, "n_ok": n_ok, "why": "equal"}
            hit = False
            for j in range(L):
                if T[j] == 0 and T[(j + 1) % L] == 0:
                    t = (j + 2) % L
                    if not (U[t] == 0 and S[t] == 1 and DV[t] == 1):
                        return {"ok": False, "n_ok": n_ok, "why": "witness"}
                    hit = True
                    break
            if not hit:
                return {"ok": False, "n_ok": n_ok, "why": "no_hit"}
            for t in range(L):
                nxt = (t + 1) % L
                if U[t] == 0 and DV[t] != S[t]:
                    return {"ok": False, "n_ok": n_ok, "why": "DV_S"}
                if V[t] == 1:
                    pred = U[t] ^ 1
                else:
                    pred = U[t] ^ W[t]
                if W[nxt] != pred:
                    return {"ok": False, "n_ok": n_ok, "why": "W_split"}
            h = ham(V, W)
            if h < minh:
                minh = h
            n_ok += 1
        min_vw[n0] = minh
    return {"ok": True, "n_ok": n_ok, "min_vw": min_vw}


def self_checks(c20, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["min_vw"][2] == 2
    assert ids["min_vw"][4] >= 3
    assert ids["min_vw"][8] >= 3
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
        "cycle": "CL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {"n_ok": ids["n_ok"], "min_vw": ids["min_vw"]},
        "lemmas": {
            "W_splits_on_V": True,
            "U0_implies_DV_eq_S": True,
            "00_witness_U_ne_DV": True,
            "third_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "W_splits_on_V": "LEMMA",
            "U0_implies_DV_eq_S": "LEMMA",
            "00_witness_U_ne_DV": "LEMMA",
            "third_pair_never_equal": "LEMMA",
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
