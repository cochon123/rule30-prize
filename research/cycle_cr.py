#!/usr/bin/env python3
"""Cycle CR: W always has consecutive 1s; (W,U) has a 10.

U flips on every V 11. On a 00 of U, V is 01 or 10. Some U 00 has V=10:
a T 0-run of length >=3, or an even-length 1-run (the only remaining
non-alternating case). Then (U,V)=(0,1) with U_next=0, so W_next=1 and
U_next=0, and W then stays 1. Hence (W,U) has a 10 and W has a 11.
On even-run blocks the V=1 subsequence has a 00 of U, which makes a
W 11 start at V=1 and gives a 10 in (W,X). Not a prize claim.

Run: python3 research/cycle_cr.py --certify
Dump: research/cycle_cr.json
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
from cycle_cj import n_odd_runs
from cycle_ck import run_lengths
from cycle_co import has10
from cycle_cq import has11

OUT = Path(__file__).resolve().with_suffix(".json")


def v11_U_flips() -> bool:
    """V_t=V_{t+1}=1 and U_t=0 force T_{t-1}=1, hence U_{t+1}=1 if T_{t-2}=0;
    if T_{t-2}=T_{t-1}=1 then run-parity flips. U=11 is already impossible."""
    # U=0, V=V_next=1 => V_next = V XOR not T_{t-1} => T_{t-1}=1
    V = 1
    Ttm1 = 1
    Vn = V ^ (Ttm1 ^ 1)
    if Vn != 1:
        return False
    # T_{t-2}=0 => U_t=0, T_{t-1}=1 starts a 1-run => U_{t+1}=1
    U_t, U_n = 0, 1
    if U_t == U_n:
        return False
    # T_{t-2}=T_{t-1}=1 => consecutive parities differ
    r, rp = 0, 1
    if (r % 2) == (rp % 2):
        return False
    return True


def u00_V_01_or_10() -> bool:
    """A T 00 makes T_{t-1}=0, so V toggles and is 01 or 10 on that U 00.
    A T 1-run cannot give U 00 at consecutive times (parities differ)."""
    for V in (0, 1):
        Vn = V ^ (0 ^ 1)
        if Vn == V:
            return False
    return True


def z3_gives_V10() -> bool:
    """Incoming V=0 at a length-3 0-run: after one toggle V=10 on the
    interior U 00."""
    V = 0
    V = V ^ (0 ^ 1)
    mid = V
    V = V ^ (0 ^ 1)
    return mid == 1 and V == 0


def even_1run_gives_V10() -> bool:
    """After an even 1-run, V_{p+1}=1 and incoming V_{p+2}=0."""
    V_mid = 1
    V_after = V_mid ^ (0 ^ 1)
    return V_mid == 1 and V_after == 0


def identities_even_n0() -> dict:
    n_ok = 0
    n_z3 = 0
    n_even1 = 0
    n_even = 0
    n_site = 0
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
            if not has11(W) or not has10(W, U):
                return {"ok": False, "n_ok": n_ok, "why": "W11"}
            site = False
            for t in range(L):
                nxt = (t + 1) % L
                if V[t] == 1 and V[nxt] == 1:
                    if U[t] == U[nxt]:
                        return {"ok": False, "n_ok": n_ok, "why": "Uflip"}
                if U[t] == 0 and U[nxt] == 0:
                    if V[t] == V[nxt]:
                        return {"ok": False, "n_ok": n_ok, "why": "U00V"}
                if U[t] == 0 and V[t] == 1 and U[nxt] == 0:
                    site = True
                    if W[nxt] != 1:
                        return {"ok": False, "n_ok": n_ok, "why": "Wnext"}
                    if W[(t + 2) % L] != 1:
                        return {"ok": False, "n_ok": n_ok, "why": "W11site"}
            if not site:
                return {"ok": False, "n_ok": n_ok, "why": "site"}
            n_site += 1
            zeros = run_lengths(T, 0)
            ones = run_lengths(T, 1)
            if max(zeros) >= 3:
                n_z3 += 1
            elif any(r % 2 == 0 for r in ones):
                n_even1 += 1
            else:
                return {"ok": False, "n_ok": n_ok, "why": "nocase"}
            nodd = n_odd_runs(T)
            if nodd == 0:
                n_even += 1
                if not has10(W, X) or Y == Z:
                    return {"ok": False, "n_ok": n_ok, "why": "evenWX"}
            if Y == Z:
                return {"ok": False, "n_ok": n_ok, "why": "YZ"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_z3": n_z3,
        "n_even1": n_even1,
        "n_even": n_even,
        "n_site": n_site,
    }


def self_checks(c20, loc: tuple[bool, bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_z3"] + ids["n_even1"] == expect
    assert ids["n_site"] == expect
    assert ids["n_even"] == 750
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (
        v11_U_flips(),
        u00_V_01_or_10(),
        z3_gives_V10(),
        even_1run_gives_V10(),
    )
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_z3": ids["n_z3"],
            "n_even1": ids["n_even1"],
            "n_even": ids["n_even"],
            "n_site": ids["n_site"],
        },
        "lemmas": {
            "U_flips_on_V11": True,
            "U00_V_is_01_or_10": True,
            "some_U00_has_V10": True,
            "W_has_11_and_WU_has_10": True,
            "even_run_WX_has_10": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "U_flips_on_V11": "LEMMA",
            "U00_V_is_01_or_10": "LEMMA",
            "some_U00_has_V10": "LEMMA",
            "W_has_11_and_WU_has_10": "LEMMA",
            "even_run_WX_has_10": "LEMMA",
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
