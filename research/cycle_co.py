#!/usr/bin/env python3
"""Cycle CO: a 10 two pairs back forces inequality; seed 10s at (1,S) and (S,U).

If A=1 and B=0 at any time, the split B=0 => DC=A gives DC=1!=0=B, so
D=reconstruct(B,C) differs from C. A 10 in (A,B) therefore makes the pair
two steps later unequal. (1,S) always has a 10 (T has a 1) and (S,U)
always has a 10 (T has a 00), so U!=V and V!=W for every even |T0|>=2.
(0,T) and (T,1) never have a 10. Not a prize claim: 10 does not persist
at every later pair.

Run: python3 research/cycle_co.py --certify
Dump: research/cycle_co.json
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
from cycle_cl import has00

OUT = Path(__file__).resolve().with_suffix(".json")


def has10(A: list[int], B: list[int]) -> bool:
    return any(a == 1 and b == 0 for a, b in zip(A, B))


def pointwise_10_kills() -> bool:
    """A=1, B=0 => C XOR C' = 1 != B, so B cannot equal DC as sequences."""
    A, B = 1, 0
    for C in (0, 1):
        Cp = A ^ (B | C)
        if (C ^ Cp) != A:
            return False
        if (C ^ Cp) == B:
            return False
    return True


def identities_even_n0() -> dict:
    n_ok = 0
    n_skip = 0
    for n0 in EVEN_N0:
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            T = T0 + [x ^ 1 for x in T0]
            L = len(T)
            zeros = [0] * L
            ones = [1] * L
            S = shifted_not(T)
            U = reconstruct(ones, S)
            V = reconstruct(S, U)
            W = reconstruct(U, V)
            if None in (U, V, W) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if has10(zeros, T) or has10(T, ones):
                return {"ok": False, "n_ok": n_ok, "why": "ident_10"}
            if not has10(ones, S) or not has10(S, U):
                return {"ok": False, "n_ok": n_ok, "why": "seed"}
            if not has00(T):
                return {"ok": False, "n_ok": n_ok, "why": "no00"}
            if U == V or V == W:
                return {"ok": False, "n_ok": n_ok, "why": "equal"}
            chain = [zeros, T, ones, S, U, V, W]
            X = reconstruct(V, W)
            if X is not None:
                chain.append(X)
            for j in range(len(chain) - 3):
                if has10(chain[j], chain[j + 1]):
                    n_skip += 1
                    if chain[j + 2] == chain[j + 3]:
                        return {"ok": False, "n_ok": n_ok, "why": "skip2", "j": j}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "n_skip": n_skip}


def self_checks(c20, pt: bool, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pt
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["n_skip"] > 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pt = pointwise_10_kills()
    ids = identities_even_n0()
    checks = self_checks(c20, pt, ids)
    dump = {
        "cycle": "CO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {"n_ok": ids["n_ok"], "n_skip": ids["n_skip"]},
        "lemmas": {
            "skip2_from_10": True,
            "seed_10_1S_and_SU": True,
            "UV_and_VW_from_seed_10": True,
            "ident0_and_ident1_never_10": True,
            "every_pair_has_10": False,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "skip2_from_10": "LEMMA",
            "seed_10_1S_and_SU": "LEMMA",
            "UV_and_VW_from_seed_10": "LEMMA",
            "ident0_and_ident1_never_10": "LEMMA",
            "every_pair_has_10": "KILLED",
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
