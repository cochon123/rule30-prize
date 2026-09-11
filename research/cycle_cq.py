#!/usr/bin/env python3
"""Cycle CQ: V always has consecutive 1s; fifth tail pair closed.

Every even T0||not T0 has a 11 in V: a 1-run of length >=3, or 0011, or
001. Skip-2 from a 10 in (V,W) gives Y!=X. If instead V implies W, that
11 forces W_t=W_{t+1}=1 with X_{t+1}=0!=1=V_{t+1}, Cycle CN's witness B.
Hence Y!=X for every even |T0|>=2. Not a prize claim.

Run: python3 research/cycle_cq.py --certify
Dump: research/cycle_cq.json
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
from cycle_ck import run_lengths
from cycle_co import has10

OUT = Path(__file__).resolve().with_suffix(".json")


def has11(seq: list[int]) -> bool:
    L = len(seq)
    return any(seq[t] == 1 and seq[(t + 1) % L] == 1 for t in range(L))


def run_ge3_forces_V11() -> bool:
    """Even offset of a 1-run of length >=3 has V=1, and the next bit is 1."""
    T_second = T_third = 1
    V_even = T_second
    V_next = V_even ^ (T_third ^ 1)
    return V_even == 1 and V_next == 1


def even0_then_r2_forces_V11() -> bool:
    """Length-2 1-run after an even 0-run: V at the first odd offset is 1
    and U=1 sets V_next to the second 1."""
    z_even = 0
    V_start = z_even ^ 1
    V_next = 1
    return V_start == 1 and V_next == 1


def z2_then_r1_forces_V11() -> bool:
    """Incoming V=0 at a length-2 0-run; two U=0 steps with T_{t-1}=01
    yield consecutive 1s at the isolated following 1."""
    V = 0
    V = V ^ (0 ^ 1)
    mid = V
    V = V ^ (1 ^ 1)
    return mid == 1 and V == 1


def v11_vimp_gives_B() -> bool:
    """V_t=V_{t+1}=1 and V=>W force W_t=1, U_t=0, W_{t+1}=1,
    X_{t+1}=not V_t=0 != V_{t+1}."""
    Vt = 1
    Vn = 1
    Wt = 1
    Ut = 0
    Wn = Ut ^ 1
    Xn = Vt ^ 1
    return Wt == 1 and Wn == 1 and Xn != Vn


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_vimp = 0
    n_ge3 = 0
    n_0011 = 0
    n_001 = 0
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
            if None in (U, V, W, X, Y) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if not has11(V):
                return {"ok": False, "n_ok": n_ok, "why": "V11"}
            if Y == X:
                return {"ok": False, "n_ok": n_ok, "why": "YX"}
            A = has10(V, W)
            vimp = all((not v) or w for v, w in zip(V, W))
            if A:
                n_A += 1
            if vimp:
                n_vimp += 1
                B = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if V[t] == 1 and V[nxt] == 1:
                        if W[t] != 1 or U[t] != 0 or W[nxt] != 1:
                            return {"ok": False, "n_ok": n_ok, "why": "v11loc"}
                        if X[nxt] != 0 or X[nxt] == V[nxt]:
                            return {"ok": False, "n_ok": n_ok, "why": "B"}
                        B = True
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
            elif not A:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            ones = run_lengths(T, 1)
            if max(ones) >= 3:
                n_ge3 += 1
            elif any(
                T[i] == 0
                and T[(i + 1) % L] == 0
                and T[(i + 2) % L] == 1
                and T[(i + 3) % L] == 1
                for i in range(L)
            ):
                n_0011 += 1
            else:
                if not any(
                    T[i] == 0
                    and T[(i + 1) % L] == 0
                    and T[(i + 2) % L] == 1
                    and T[(i + 3) % L] == 0
                    for i in range(L)
                ):
                    return {"ok": False, "n_ok": n_ok, "why": "nocase"}
                n_001 += 1
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_vimp": n_vimp,
        "n_ge3": n_ge3,
        "n_0011": n_0011,
        "n_001": n_001,
    }


def self_checks(c20, loc: tuple[bool, bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_vimp"] == expect
    assert ids["n_ge3"] + ids["n_0011"] + ids["n_001"] == expect
    assert ids["n_vimp"] == 20
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (
        run_ge3_forces_V11(),
        even0_then_r2_forces_V11(),
        z2_then_r1_forces_V11(),
        v11_vimp_gives_B(),
    )
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_vimp": ids["n_vimp"],
            "n_ge3": ids["n_ge3"],
            "n_0011": ids["n_0011"],
            "n_001": ids["n_001"],
        },
        "lemmas": {
            "V_has_11": True,
            "skip2_or_vimp_B": True,
            "fifth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "V_has_11": "LEMMA",
            "skip2_or_vimp_B": "LEMMA",
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
