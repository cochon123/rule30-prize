#!/usr/bin/env python3
"""Cycle CK: ham(U,V)=|T0| because +n0 pairs 1-runs with 0-runs.

U never has consecutive 1s. Packed update of V splits on U:
if U_t=1 then V_{t+1}=T_{t-1}, else V_{t+1}=V_t XOR not T_{t-1}.
Then delta=U XOR V toggles after U=0 and resets to T_{t-1} after U=1.
Odd 2-copy T=T0||not T0 sends each 1-run to a 0-run of the same length
by a half-period shift, so n_odd 0-runs equals n_odd 1-runs and
ham(U,V)=sum floor(r/2)+sum ceil(z/2)=|T0|. Closed form of Cycle CI's
exhaustive ham(U,V)=n0. Not a prize claim.

Run: python3 research/cycle_ck.py --certify
Dump: research/cycle_ck.json
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
from cycle_cj import n_odd_runs

OUT = Path(__file__).resolve().with_suffix(".json")


def n_odd_zero_runs(T: list[int]) -> int:
    L = len(T)
    n = 0
    for s in range(L):
        if T[s] == 0 and T[(s - 1) % L] == 1:
            r = 0
            j = s
            while T[j] == 0:
                r += 1
                j = (j + 1) % L
            if r % 2:
                n += 1
    return n


def run_lengths(T: list[int], bit: int) -> list[int]:
    L = len(T)
    out = []
    for s in range(L):
        if T[s] == bit and T[(s - 1) % L] != bit:
            r = 0
            j = s
            while T[j] == bit:
                r += 1
                j = (j + 1) % L
            out.append(r)
    return out


def identities_even_n0() -> dict:
    n_ok = 0
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
            if U is None or V is None or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            ones = run_lengths(T, 1)
            zeros = run_lengths(T, 0)
            if sorted(ones) != sorted(zeros):
                return {"ok": False, "n_ok": n_ok, "why": "run_bijection"}
            if n_odd_runs(T) != n_odd_zero_runs(T):
                return {"ok": False, "n_ok": n_ok, "why": "n_odd"}
            pred = sum(r // 2 for r in ones) + sum((z + 1) // 2 for z in zeros)
            if ham(U, V) != n0 or pred != n0:
                return {"ok": False, "n_ok": n_ok, "why": "ham", "pred": pred}
            for t in range(L):
                nxt = (t + 1) % L
                if U[t] == 1:
                    if U[nxt] != 0:
                        return {"ok": False, "n_ok": n_ok, "why": "U11"}
                    if V[nxt] != T[(t - 1) % L]:
                        return {"ok": False, "n_ok": n_ok, "why": "V_reset"}
                else:
                    if V[nxt] != (V[t] ^ T[(t - 1) % L] ^ 1):
                        return {"ok": False, "n_ok": n_ok, "why": "V_toggle"}
                d = U[t] ^ V[t]
                dn = U[nxt] ^ V[nxt]
                if U[t] == 0:
                    if dn != (d ^ 1):
                        return {"ok": False, "n_ok": n_ok, "why": "delta_toggle"}
                else:
                    if dn != T[(t - 1) % L]:
                        return {"ok": False, "n_ok": n_ok, "why": "delta_reset"}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def self_checks(c20, ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
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
        "cycle": "CK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {"n_ok": ids["n_ok"]},
        "lemmas": {
            "U_no_consecutive_ones": True,
            "V_splits_on_U": True,
            "delta_toggle_reset": True,
            "half_period_pairs_runs": True,
            "ham_UV_eq_n0_closed": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "U_no_consecutive_ones": "LEMMA",
            "V_splits_on_U": "LEMMA",
            "delta_toggle_reset": "LEMMA",
            "half_period_pairs_runs": "LEMMA",
            "ham_UV_eq_n0_closed": "LEMMA",
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
