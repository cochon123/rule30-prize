#!/usr/bin/env python3
"""Cycle CJ: U is the run-parity of T; ham(S,U)=(3/2)(n0 - n_odd).

Reset-toggle unfolds to U_t = (length of the 1-run of T ending at t-2)
mod 2. Then ham(S,U)=(3/2)(n0 - n_odd) where n_odd is the number of
odd-length 1-runs of T. For even |T0|>=2, T=T0||not T0 is balanced and
not alternating, so n_odd <= n0-2 and ham(S,U)>=3. This is the closed
form of Cycle CI's multiple-of-3 count. Not a prize claim.

Run: python3 research/cycle_cj.py --certify
Dump: research/cycle_cj.json
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
from cycle_ch import ham, shifted_not
from cycle_ci import EVEN_N0, reset_toggle_step

OUT = Path(__file__).resolve().with_suffix(".json")


def run_ending(T: list[int], pos: int) -> int:
    """Length of the 1-run of T ending at pos; 0 if T[pos]=0."""
    L = len(T)
    if T[pos] == 0:
        return 0
    r = 0
    i = pos
    for _ in range(L):
        if T[i] == 0:
            break
        r += 1
        i = (i - 1) % L
    return r


def n_odd_runs(T: list[int]) -> int:
    L = len(T)
    n = 0
    for s in range(L):
        if T[s] == 1 and T[(s - 1) % L] == 0:
            r = 0
            j = s
            while T[j] == 1:
                r += 1
                j = (j + 1) % L
            if r % 2:
                n += 1
    return n


def identities_even_n0() -> dict:
    n_ok = 0
    su_vals: dict[int, list[int]] = {}
    for n0 in EVEN_N0:
        seen: set[int] = set()
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            T = T0 + [x ^ 1 for x in T0]
            L = len(T)
            S = shifted_not(T)
            U = reconstruct([1] * L, S)
            if U is None or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            for t in range(L):
                r = run_ending(T, (t - 2) % L)
                if U[t] != r % 2:
                    return {"ok": False, "n_ok": n_ok, "why": "run_parity"}
                if T[(t - 2) % L] == 0 and U[t] != 0:
                    return {"ok": False, "n_ok": n_ok, "why": "reset"}
                if U[t] == 0 and U[(t + 1) % L] != T[(t - 1) % L]:
                    return {"ok": False, "n_ok": n_ok, "why": "next_after_zero"}
            nodd = n_odd_runs(T)
            if nodd % 2:
                return {"ok": False, "n_ok": n_ok, "why": "n_odd_parity"}
            if nodd > n0 - 2:
                return {"ok": False, "n_ok": n_ok, "why": "n_odd_bound"}
            h = ham(S, U)
            pred = (3 * (n0 - nodd)) // 2
            if h != pred:
                return {"ok": False, "n_ok": n_ok, "why": "ham_formula", "h": h, "pred": pred}
            if h < 3 or h % 3:
                return {"ok": False, "n_ok": n_ok, "why": "ham_ge3"}
            seen.add(h)
            n_ok += 1
        su_vals[n0] = sorted(seen)
    return {"ok": True, "n_ok": n_ok, "su_vals": su_vals}


def self_checks(c20, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["su_vals"][2] == [3]
    assert ids["su_vals"][8][0] == 3
    assert ids["su_vals"][16][-1] == 24
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
        "cycle": "CJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {"n_ok": ids["n_ok"], "su_vals": ids["su_vals"]},
        "lemmas": {
            "U_is_run_parity": True,
            "T_zero_resets_U": True,
            "ham_SU_eq_3halves_n0_minus_nodd": True,
            "ham_SU_ge_3_all_even_n0": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "U_is_run_parity": "LEMMA",
            "T_zero_resets_U": "LEMMA",
            "ham_SU_eq_3halves_n0_minus_nodd": "LEMMA",
            "ham_SU_ge_3_all_even_n0": "LEMMA",
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
