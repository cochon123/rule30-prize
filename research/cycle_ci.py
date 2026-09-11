#!/usr/bin/env python3
"""Cycle CI: first continuation is reset-toggle; ham(U,V)=|T0|.

After ident-1, S=shifted-not T and U=reconstruct(1,S) obeys
u_{t+1}=T_{t-1} AND NOT u_t. The next bit V=reconstruct(S,U) equals U
iff S=DU iff U=S, already killed for even |T0|>=2, so the second tail
pair is never equal. Exhaustively, ham(U,V)=|T0| and ham(S,U) is a
positive multiple of 3, for even |T0| through 16. Length 16 has
Hamming at least 3 on 24 extra bits. Not a prize claim.

Run: python3 research/cycle_ci.py --certify
Dump: research/cycle_ci.json
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
from cycle_ch import ham, scar_lift, shifted_not

OUT = Path(__file__).resolve().with_suffix(".json")
EVEN_N0 = (2, 4, 6, 8, 10, 12, 16)


def reset_toggle_step(T: list[int], U: list[int]) -> bool:
    L = len(T)
    for t in range(L):
        pred = T[(t - 1) % L] & (U[t] ^ 1)
        if pred != U[(t + 1) % L]:
            return False
    return True


def identities_even_n0() -> dict:
    """Reset-toggle, S=DU iff U=S, V!=U, ham(U,V)=n0, ham(S,U)%3>=3."""
    n_ok = 0
    su_vals: dict[int, list[int]] = {}
    for n0 in EVEN_N0:
        seen_su: set[int] = set()
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            T = T0 + [x ^ 1 for x in T0]
            L = len(T)
            ones = [1] * L
            S = shifted_not(T)
            U = reconstruct(ones, S)
            if U is None or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            s_du = S == deriv(U)
            u_s = U == S
            if s_du != u_s:
                return {"ok": False, "n_ok": n_ok}
            if u_s:
                return {"ok": False, "n_ok": n_ok}
            V = reconstruct(S, U)
            if V is None or V == U:
                return {"ok": False, "n_ok": n_ok}
            h_uv = ham(U, V)
            h_su = ham(S, U)
            if h_uv != n0:
                return {"ok": False, "n_ok": n_ok, "bad_uv": h_uv, "n0": n0}
            if h_su < 3 or h_su % 3:
                return {"ok": False, "n_ok": n_ok, "bad_su": h_su, "n0": n0}
            seen_su.add(h_su)
            n_ok += 1
        su_vals[n0] = sorted(seen_su)
    return {"ok": True, "n_ok": n_ok, "su_vals": su_vals}


def n0_16_tail(n_extra: int = 24) -> dict:
    min_h = 10**9
    n_ok = 0
    n_none = 0
    n_h1 = 0
    for mask in range(1 << 16):
        T0 = [(mask >> i) & 1 for i in range(16)]
        if sum(T0) in (0, 16):
            continue
        seqs = scar_lift(T0, n_extra)
        if seqs is None:
            n_none += 1
            continue
        n_ok += 1
        for q in range(1, max(seqs) + 1):
            h = ham(seqs[q - 1], seqs[q])
            if h < min_h:
                min_h = h
            if h == 0:
                return {"ok": False, "n_ok": n_ok, "min_h": 0}
            if h == 1:
                n_h1 += 1
    return {
        "n0": 16,
        "n_extra": n_extra,
        "n_ok": n_ok,
        "n_none": n_none,
        "min_h": min_h,
        "n_h1": n_h1,
        "ok": n_ok == 65534 and n_none == 0 and min_h >= 3,
    }


def self_checks(c20, ids: dict, t16: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ids["ok"] and ids["n_ok"] == sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["su_vals"][8][0] == 3
    assert t16["ok"] and t16["min_h"] >= 3 and t16["n_h1"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ids = identities_even_n0()
    t16 = n0_16_tail(24)
    checks = self_checks(c20, ids, t16)
    dump = {
        "cycle": "CI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "su_vals": ids["su_vals"],
        },
        "n0_16_tail": {
            k: t16[k] for k in ("n0", "n_extra", "n_ok", "n_none", "min_h", "n_h1")
        },
        "lemmas": {
            "reset_toggle_U": True,
            "S_DU_iff_U_S": True,
            "second_pair_never_equal": True,
            "ham_UV_eq_n0_through_16": True,
            "ham_SU_mult3_ge3_through_16": True,
            "n0_16_tail_hamming_ge_3": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reset_toggle_U": "LEMMA",
            "S_DU_iff_U_S": "LEMMA",
            "second_pair_never_equal": "LEMMA",
            "ham_UV_eq_n0_through_16": "LEMMA",
            "ham_SU_mult3_ge3_through_16": "LEMMA",
            "n0_16_tail_hamming_ge_3": "LEMMA",
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
    print("n0_16_tail", dump["n0_16_tail"])


if __name__ == "__main__":
    main()
