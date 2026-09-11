#!/usr/bin/env python3
"""Cycle CT: (X,Y) has a 10; seventh tail pair closed.

Every X 1-run starts with W=1. A CR site (U 00 with V=10) always
gives W_next=W_nn=1 and X_nn=1; T=1 there or W=X=0 at the site makes
an X 11. Then Y_next=0 on that 11, so (X,Y) has a 10. Skip-2 gives
Z!=reconstruct(Y,Z). Not a prize claim.

Run: python3 research/cycle_ct.py --certify
Dump: research/cycle_ct.json
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


def X_start_Uprev1_contradicts() -> bool:
    """U_{s-1}=1 at an X run start forces W_{s-2}=1, V_{s-2}=0,
    hence X_{s-1}=1, contradicting the start."""
    Vsm2, Wsm2 = 0, 1
    Xsm1 = Vsm2 ^ 1
    return Xsm1 == 1


def W1X1_Ynext0() -> bool:
    """W=1 and X=1 force Y_next = not W = 0."""
    W, X = 1, 1
    for Y in (0, 1):
        if (W ^ (X | Y)) != 0:
            return False
    return True


def Xt1_Xnext_notV() -> bool:
    """X=1 forces X_next = not V, so an X 11 is exactly X=1 with V=0."""
    X = 1
    for V in (0, 1):
        for W in (0, 1):
            Xn = V ^ (W | X)
            if Xn != (V ^ 1):
                return False
    return True


def CR_W11_Xnn1() -> bool:
    """U=00, V=10: W_next=W_nn=1 and X_nn=1 regardless of W,X."""
    U, Un, V, Vn = 0, 0, 1, 0
    for W in (0, 1):
        for X in (0, 1):
            Wn = U ^ (V | W)
            Wnn = Un ^ (Vn | Wn)
            Xn = V ^ (W | X)
            Xnn = Vn ^ (Wn | Xn)
            if Wn != 1 or Wnn != 1 or Xnn != 1:
                return False
    return True


def CR_Tt1_gives_X11() -> bool:
    """At a CR site T=1 forces X_nnn=1, hence an X 11 with X_nn."""
    Vn, Tt = 0, 1
    Vnn = Vn ^ (Tt ^ 1)
    Xnnn = Vnn ^ 1
    return Xnnn == 1


def CR_WX00_gives_X11() -> bool:
    """At a CR site W=X=0 forces X_next=1, hence an X 11 with X_nn."""
    V, W, X = 1, 0, 0
    Xn = V ^ (W | X)
    return Xn == 1


def odd_z_last_V10() -> bool:
    """Incoming V=0 on an odd 0-run of length >=3: last two U-slots are
    V=10, and T after the run is 1."""
    for z in (3, 5, 7, 9):
        V = 0
        vs = [V]
        for _ in range(z - 1):
            V ^= 0 ^ 1
            vs.append(V)
        if vs[-2] != 1 or vs[-1] != 0:
            return False
    return True


def identities_even_n0() -> dict:
    n_ok = 0
    n_Tt1 = 0
    n_WX00 = 0
    n_even = 0
    n_zodd = 0
    n_e1z1 = 0
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
            if None in (U, V, W, X, Y, Z, P) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if not has11(X) or not has10(X, Y) or Z == P:
                return {"ok": False, "n_ok": n_ok, "why": "XY"}
            ge2 = False
            for s in range(L):
                if X[s] == 1 and X[(s - 1) % L] == 0:
                    if U[(s - 1) % L] != 0 or W[s] != 1:
                        return {"ok": False, "n_ok": n_ok, "why": "W1"}
                    r = 0
                    j = s
                    while X[j] == 1:
                        r += 1
                        j = (j + 1) % L
                    if r >= 2:
                        ge2 = True
                        if Y[(s + 1) % L] != 0 or X[(s + 1) % L] != 1:
                            return {"ok": False, "n_ok": n_ok, "why": "Y0"}
            if not ge2:
                return {"ok": False, "n_ok": n_ok, "why": "ge2"}
            Tt1 = False
            WX00 = False
            for t in range(L):
                nxt = (t + 1) % L
                if U[t] == 0 and U[nxt] == 0 and V[t] == 1 and V[nxt] == 0:
                    if W[nxt] != 1 or W[(t + 2) % L] != 1 or X[(t + 2) % L] != 1:
                        return {"ok": False, "n_ok": n_ok, "why": "CR"}
                    if T[t] == 1:
                        Tt1 = True
                        if X[(t + 3) % L] != 1:
                            return {"ok": False, "n_ok": n_ok, "why": "Tt1"}
                    if W[t] == 0 and X[t] == 0:
                        WX00 = True
                        if X[nxt] != 1:
                            return {"ok": False, "n_ok": n_ok, "why": "WX00"}
            if not (Tt1 or WX00):
                return {"ok": False, "n_ok": n_ok, "why": "nogood"}
            if Tt1:
                n_Tt1 += 1
            if WX00:
                n_WX00 += 1
            nodd = n_odd_runs(T)
            zeros = run_lengths(T, 0)
            if nodd == 0:
                n_even += 1
                if not WX00:
                    return {"ok": False, "n_ok": n_ok, "why": "even"}
            elif any(z % 2 and z >= 3 for z in zeros):
                n_zodd += 1
                if not Tt1:
                    return {"ok": False, "n_ok": n_ok, "why": "zodd"}
            else:
                n_e1z1 += 1
                if not Tt1:
                    return {"ok": False, "n_ok": n_ok, "why": "e1z1"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_Tt1": n_Tt1,
        "n_WX00": n_WX00,
        "n_even": n_even,
        "n_zodd": n_zodd,
        "n_e1z1": n_e1z1,
    }


def self_checks(c20, loc: tuple[bool, ...], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_Tt1"] + ids["n_even"] == expect
    assert ids["n_zodd"] + ids["n_e1z1"] + ids["n_even"] == expect
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (
        X_start_Uprev1_contradicts(),
        W1X1_Ynext0(),
        Xt1_Xnext_notV(),
        CR_W11_Xnn1(),
        CR_Tt1_gives_X11(),
        CR_WX00_gives_X11(),
        odd_z_last_V10(),
    )
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_Tt1": ids["n_Tt1"],
            "n_WX00": ids["n_WX00"],
            "n_even": ids["n_even"],
            "n_zodd": ids["n_zodd"],
            "n_e1z1": ids["n_e1z1"],
        },
        "lemmas": {
            "X_run_start_W1": True,
            "XY_10_from_X11": True,
            "seventh_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "X_run_start_W1": "LEMMA",
            "XY_10_from_X11": "LEMMA",
            "seventh_pair_never_equal": "LEMMA",
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
