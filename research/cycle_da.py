#!/usr/bin/env python3
"""Cycle DA: fourteenth tail pair closed; (T',U') 10 or T'=>U' witness B.

(T',U') has a 10 on all but 16 even T0||not T0. Those 16 have T'=>U' and
are all |T0|=8. Each has a U' 11 carrying a T' 11 (V'_next=0!=1), Cycle
CN's witness B; none needs T' 00 on that 11. Skip-2 or B gives
V'!=reconstruct(U',V'). Not a prize claim. (T',U') does not always have a
10; U' does not always have a 11.

Run: python3 research/cycle_da.py --certify
Dump: research/cycle_da.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_ch import scar_lift
from cycle_ci import EVEN_N0, reset_toggle_step
from cycle_co import has10, pointwise_10_kills
from cycle_cq import has11

OUT = Path(__file__).resolve().with_suffix(".json")


def T11_imp_gives_B() -> bool:
    """T'_t=T'_{t+1}=1 and T'=>U' force U'=11 and V'_next=not T'_t=0 != 1."""
    Tt = Tn = 1
    Vn = Tt ^ 1
    return Vn == 0 and Vn != Tn


def T00_Up11_gives_B() -> bool:
    """T'=00 on a U' 11: V'_next=T' XOR 1=1 != 0."""
    Tt = 0
    Vn = Tt ^ 1
    return Vn == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_T11 = 0
    n_T00 = 0
    n_imp_n08 = 0
    for n0 in EVEN_N0:
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            seqs = scar_lift(T0, 15)
            if seqs is None or 17 not in seqs:
                return {"ok": False, "n_ok": n_ok, "why": "lift"}
            T = seqs[1]
            U = seqs[4]
            Tp, Up, Vp, Wp = seqs[14], seqs[15], seqs[16], seqs[17]
            if not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok, "why": "reset"}
            if Vp == Wp:
                return {"ok": False, "n_ok": n_ok, "why": "VW"}
            A = has10(Tp, Up)
            imp = all((not a) or b for a, b in zip(Tp, Up))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if n0 != 8:
                    return {"ok": False, "n_ok": n_ok, "why": "n0"}
                n_imp_n08 += 1
                if not has11(Up):
                    return {"ok": False, "n_ok": n_ok, "why": "Up11"}
                T11 = False
                T00 = False
                B = False
                L = len(T)
                for t in range(L):
                    nxt = (t + 1) % L
                    if Up[t] == 1 and Vp[t] != Tp[t]:
                        B = True
                    if Up[t] == 1 and Up[nxt] == 1:
                        if Tp[t] == 1 and Tp[nxt] == 1:
                            T11 = True
                            if Vp[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "T11V"}
                        if Tp[t] == 0 and Tp[nxt] == 0:
                            T00 = True
                            if Vp[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "T00V"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if T11:
                    n_T11 += 1
                elif T00:
                    n_T00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_T11": n_T11,
        "n_T00": n_T00,
        "n_imp_n08": n_imp_n08,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_imp"] == ids["n_imp_n08"] == 16
    assert ids["n_T11"] + ids["n_T00"] == ids["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), T11_imp_gives_B(), T00_Up11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "DA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_T11": ids["n_T11"],
            "n_T00": ids["n_T00"],
            "n_imp_n08": ids["n_imp_n08"],
        },
        "lemmas": {
            "TU_10_or_imp": True,
            "imp_only_n0_8": True,
            "imp_Up11_T11_or_T00": True,
            "fourteenth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "TU_10_or_imp": "LEMMA",
            "imp_only_n0_8": "LEMMA",
            "imp_Up11_T11_or_T00": "LEMMA",
            "fourteenth_pair_never_equal": "LEMMA",
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
