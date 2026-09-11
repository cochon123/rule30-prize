#!/usr/bin/env python3
"""Cycle DC: sixteenth tail pair closed; (V',W') 10 or V'=>W' witness B.

(V',W') has a 10 on all but 24 even T0||not T0. Those 24 have V'=>W' and
are all |T0|=12. Each has a W' 11 carrying a V' 11 (X'_next=0!=1), Cycle
CN's witness B; none needs V' 00 on that 11. Skip-2 or B gives
X'!=reconstruct(W',X'). Not a prize claim. (V',W') does not always have a
10; V' and W' do not always have a 11.

Run: python3 research/cycle_dc.py --certify
Dump: research/cycle_dc.json
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


def V11_imp_gives_B() -> bool:
    """V'_t=V'_{t+1}=1 and V'=>W' force W'=11 and X'_next=not V'_t=0 != 1."""
    Vt = Vn = 1
    Xn = Vt ^ 1
    return Xn == 0 and Xn != Vn


def V00_Wp11_gives_B() -> bool:
    """V'=00 on a W' 11: X'_next=V' XOR 1=1 != 0."""
    Vt = 0
    Xn = Vt ^ 1
    return Xn == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_V11 = 0
    n_V00 = 0
    n_imp_n012 = 0
    for n0 in EVEN_N0:
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            seqs = scar_lift(T0, 17)
            if seqs is None or 19 not in seqs:
                return {"ok": False, "n_ok": n_ok, "why": "lift"}
            T = seqs[1]
            U = seqs[4]
            Vp, Wp, Xp, Yp = seqs[16], seqs[17], seqs[18], seqs[19]
            if not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok, "why": "reset"}
            if Xp == Yp:
                return {"ok": False, "n_ok": n_ok, "why": "XY"}
            A = has10(Vp, Wp)
            imp = all((not a) or b for a, b in zip(Vp, Wp))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if n0 != 12:
                    return {"ok": False, "n_ok": n_ok, "why": "n0"}
                n_imp_n012 += 1
                if not has11(Wp):
                    return {"ok": False, "n_ok": n_ok, "why": "Wp11"}
                V11 = False
                V00 = False
                B = False
                L = len(T)
                for t in range(L):
                    nxt = (t + 1) % L
                    if Wp[t] == 1 and Xp[t] != Vp[t]:
                        B = True
                    if Wp[t] == 1 and Wp[nxt] == 1:
                        if Vp[t] == 1 and Vp[nxt] == 1:
                            V11 = True
                            if Xp[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "V11X"}
                        if Vp[t] == 0 and Vp[nxt] == 0:
                            V00 = True
                            if Xp[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "V00X"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if V11:
                    n_V11 += 1
                elif V00:
                    n_V00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_V11": n_V11,
        "n_V00": n_V00,
        "n_imp_n012": n_imp_n012,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_imp"] == ids["n_imp_n012"] == 24
    assert ids["n_V11"] + ids["n_V00"] == ids["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), V11_imp_gives_B(), V00_Wp11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "DC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_V11": ids["n_V11"],
            "n_V00": ids["n_V00"],
            "n_imp_n012": ids["n_imp_n012"],
        },
        "lemmas": {
            "VW_10_or_imp": True,
            "imp_only_n0_12": True,
            "imp_Wp11_V11_or_V00": True,
            "sixteenth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "VW_10_or_imp": "LEMMA",
            "imp_only_n0_12": "LEMMA",
            "imp_Wp11_V11_or_V00": "LEMMA",
            "sixteenth_pair_never_equal": "LEMMA",
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
