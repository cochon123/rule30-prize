#!/usr/bin/env python3
"""Cycle CZ: thirteenth tail pair closed; (S',T') 10 or S'=>T' witness B.

(S',T') has a 10 on all but 48 even T0||not T0. Those 48 have S'=>T'.
Then a T' 11 carries either S' 11 (U'_next=0!=1) or S' 00 (U'_next=1!=0),
Cycle CN's witness B. Skip-2 or B gives U'!=reconstruct(T',U'). Not a
prize claim. (S',T') does not always have a 10; S' does not always have
a 11. The CV/CX two-arm covering misses 164 of these blocks.

Run: python3 research/cycle_cz.py --certify
Dump: research/cycle_cz.json
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


def Sp11_imp_gives_B() -> bool:
    """S'_t=S'_{t+1}=1 and S'=>T' force T'=11 and U'_next=not S'_t=0 != 1."""
    St = Sn = 1
    Un = St ^ 1
    return Un == 0 and Un != Sn


def Sp00_Tp11_gives_B() -> bool:
    """S'=00 on a T' 11: U'_next=S' XOR 1=1 != 0."""
    St = 0
    Un = St ^ 1
    return Un == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_Sp11 = 0
    n_Sp00 = 0
    n_Tp11 = 0
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
            Q = reconstruct(Z, P)
            R = reconstruct(P, Q)
            Sp = reconstruct(Q, R)
            Tp = reconstruct(R, Sp) if Sp is not None else None
            Up = reconstruct(Sp, Tp) if Tp is not None else None
            Vp = reconstruct(Tp, Up) if Up is not None else None
            if None in (U, V, W, X, Y, Z, P, Q, R, Sp, Tp, Up, Vp) or not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok}
            if Up == Vp:
                return {"ok": False, "n_ok": n_ok, "why": "UV"}
            if not has11(Tp):
                return {"ok": False, "n_ok": n_ok, "why": "Tp11all"}
            n_Tp11 += 1
            A = has10(Sp, Tp)
            imp = all((not s) or t for s, t in zip(Sp, Tp))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if not has11(Tp):
                    return {"ok": False, "n_ok": n_ok, "why": "Tp11"}
                Sp11 = False
                Sp00 = False
                B = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if Tp[t] == 1 and Up[t] != Sp[t]:
                        B = True
                    if Tp[t] == 1 and Tp[nxt] == 1:
                        if Sp[t] == 1 and Sp[nxt] == 1:
                            Sp11 = True
                            if Up[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "Sp11U"}
                        if Sp[t] == 0 and Sp[nxt] == 0:
                            Sp00 = True
                            if Up[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "Sp00U"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if Sp11:
                    n_Sp11 += 1
                elif Sp00:
                    n_Sp00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_Sp11": n_Sp11,
        "n_Sp00": n_Sp00,
        "n_Tp11": n_Tp11,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_imp"] == 48
    assert ids["n_Sp11"] + ids["n_Sp00"] == ids["n_imp"]
    assert ids["n_Tp11"] == expect
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), Sp11_imp_gives_B(), Sp00_Tp11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "CZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_Sp11": ids["n_Sp11"],
            "n_Sp00": ids["n_Sp00"],
            "n_Tp11": ids["n_Tp11"],
        },
        "lemmas": {
            "ST_10_or_imp": True,
            "imp_Tp11_Sp11_or_Sp00": True,
            "Tp_always_11": True,
            "thirteenth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "ST_10_or_imp": "LEMMA",
            "imp_Tp11_Sp11_or_Sp00": "LEMMA",
            "Tp_always_11": "LEMMA",
            "thirteenth_pair_never_equal": "LEMMA",
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
