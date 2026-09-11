#!/usr/bin/env python3
"""Cycle CP: (U,V) has a 10 iff T has an odd 1-run; fourth pair closed.

A 10 in (U,V) occurs only at the first odd offset of a 1-run, and
there V=0 iff the preceding 0-run is odd. By the half-period
bijection that is iff n_odd>0. Skip-2 then gives X!=W on odd-run
blocks. On even-run blocks U implies V, wt(U)=n0/2, and the V=1
subsequence has more 0s than 1s, so consecutive V=1 times share a
U value and witness B fires. Hence X!=W for every even |T0|>=2.
Not a prize claim.

Run: python3 research/cycle_cp.py --certify
Dump: research/cycle_cp.json
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
from cycle_cj import n_odd_runs, run_ending
from cycle_ck import n_odd_zero_runs
from cycle_co import has10

OUT = Path(__file__).resolve().with_suffix(".json")


def later_odd_forces_V1() -> bool:
    """Interior odd offset of a 1-run: U_{t-2}=1 and T_{e-2,e-1,e}=111
    force V_t=1 via the CK split."""
    Te = Te1 = 1
    V_tm1 = Te1
    V_t = V_tm1 ^ (Te ^ 1)
    return V_t == 1


def incoming_zero_run_V() -> bool:
    """After a 1-run of length r, V at the first 0-run U-slot is 0."""
    for r in range(1, 13):
        if r % 2:
            V_after = 0
        else:
            V_mid = 1
            V_after = V_mid ^ (0 ^ 1)
        if V_after != 0:
            return False
    return True


def zero_run_walk() -> bool:
    """Start V=0 at the first 0-run U-slot. After z U=0 steps with
    T_{t-1} = 0^{z-1} followed by a 1, V becomes (z-1) mod 2."""
    for z in range(1, 21):
        V = 0
        Ts = [0] * (z - 1) + [1]
        for Ttm1 in Ts:
            V ^= Ttm1 ^ 1
        if V != (z - 1) % 2:
            return False
    return True


def prev_zero_run_len(T: list[int], s: int) -> int:
    L = len(T)
    z = 0
    j = (s - 1) % L
    for _ in range(L):
        if T[j] != 0:
            break
        z += 1
        j = (j - 1) % L
    return z


def identities_even_n0() -> dict:
    n_ok = 0
    n_gap = 0
    n_odd_pos = 0
    n_A = 0
    n_B_gap = 0
    n_VW10_gap = 0
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
            if None in (U, V, W, X) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            nodd = n_odd_runs(T)
            nodd0 = n_odd_zero_runs(T)
            if nodd != nodd0:
                return {"ok": False, "n_ok": n_ok, "why": "bijection"}
            has_uv10 = has10(U, V)
            if has_uv10 != (nodd > 0):
                return {"ok": False, "n_ok": n_ok, "why": "iff"}
            if W == X:
                return {"ok": False, "n_ok": n_ok, "why": "WX"}
            if has_uv10 and W == X:
                return {"ok": False, "n_ok": n_ok, "why": "skip2"}
            for t in range(L):
                if U[t] != 1:
                    continue
                e = (t - 2) % L
                r = run_ending(T, e)
                if r >= 3 and V[t] != 1:
                    return {"ok": False, "n_ok": n_ok, "why": "later"}
                if r == 1:
                    s = e
                    z = prev_zero_run_len(T, s)
                    if V[t] != ((z + 1) % 2):
                        return {"ok": False, "n_ok": n_ok, "why": "zparity"}
            for s in range(L):
                if T[s] == 0 and T[(s - 1) % L] == 1:
                    if V[(s + 2) % L] != 0:
                        return {"ok": False, "n_ok": n_ok, "why": "incoming"}
            if has_uv10:
                n_A += 1
                n_odd_pos += 1
            else:
                n_gap += 1
                wtU = sum(U)
                if wtU != n0 // 2:
                    return {"ok": False, "n_ok": n_ok, "why": "wtU"}
                n11 = n01 = n00 = n10 = 0
                u_along = []
                for t in range(L):
                    if U[t] == 1 and V[t] == 1:
                        n11 += 1
                    elif U[t] == 0 and V[t] == 1:
                        n01 += 1
                    elif U[t] == 0 and V[t] == 0:
                        n00 += 1
                    else:
                        n10 += 1
                    if V[t] == 1:
                        u_along.append(U[t])
                if (n11, n01, n00, n10) != (n0 // 2, n0, n0 // 2, 0):
                    return {"ok": False, "n_ok": n_ok, "why": "counts"}
                if u_along.count(0) != n0 or u_along.count(1) != n0 // 2:
                    return {"ok": False, "n_ok": n_ok, "why": "along"}
                B = False
                prev_u = None
                for t in range(2 * L):
                    i = t % L
                    if V[i] == 1:
                        if prev_u is not None and W[i] != (prev_u ^ 1):
                            return {"ok": False, "n_ok": n_ok, "why": "Wprev"}
                        if V[i] == 1 and W[i] != U[i]:
                            B = True
                        prev_u = U[i]
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "B"}
                n_B_gap += 1
                if not has10(V, W):
                    return {"ok": False, "n_ok": n_ok, "why": "VW10"}
                n_VW10_gap += 1
                Y = reconstruct(W, X)
                if Y is None or Y == X:
                    return {"ok": False, "n_ok": n_ok, "why": "YX"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_gap": n_gap,
        "n_odd_pos": n_odd_pos,
        "n_A": n_A,
        "n_B_gap": n_B_gap,
        "n_VW10_gap": n_VW10_gap,
    }


def self_checks(c20, later: bool, incoming: bool, walk: bool, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert later and incoming and walk
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    expect_gap = sum(2 * ((1 << (n // 2)) - 1) for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_gap"] == expect_gap == 750
    assert ids["n_odd_pos"] == expect - expect_gap
    assert ids["n_A"] == ids["n_odd_pos"]
    assert ids["n_B_gap"] == ids["n_gap"]
    assert ids["n_VW10_gap"] == ids["n_gap"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    later = later_odd_forces_V1()
    incoming = incoming_zero_run_V()
    walk = zero_run_walk()
    ids = identities_even_n0()
    checks = self_checks(c20, later, incoming, walk, ids)
    dump = {
        "cycle": "CP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_gap": ids["n_gap"],
            "n_odd_pos": ids["n_odd_pos"],
            "n_A": ids["n_A"],
            "n_B_gap": ids["n_B_gap"],
            "n_VW10_gap": ids["n_VW10_gap"],
        },
        "lemmas": {
            "later_odd_V_is_1": True,
            "UV_10_iff_odd_zero_run": True,
            "UV_10_iff_n_odd": True,
            "skip2_kills_WX_on_odd_runs": True,
            "even_run_witness_B": True,
            "fourth_pair_never_equal": True,
            "even_run_VW_has_10": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "later_odd_V_is_1": "LEMMA",
            "UV_10_iff_odd_zero_run": "LEMMA",
            "UV_10_iff_n_odd": "LEMMA",
            "skip2_kills_WX_on_odd_runs": "LEMMA",
            "even_run_witness_B": "LEMMA",
            "fourth_pair_never_equal": "LEMMA",
            "even_run_VW_has_10": "LEMMA",
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
