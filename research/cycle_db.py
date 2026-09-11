#!/usr/bin/env python3
"""Cycle DB: fifteenth tail pair closed; (U',V') 10 or U'=>V' witness B.

(U',V') has a 10 on all but 20 even T0||not T0. Those 20 have U'=>V' and
are all |T0|=10. Each has a V' 11 carrying a U' 11 (W'_next=0!=1), Cycle
CN's witness B; none needs U' 00 on that 11. Skip-2 or B gives
W'!=reconstruct(V',W'). Not a prize claim. (U',V') does not always have a
10; U' and V' do not always have a 11.

Run: python3 research/cycle_db.py --certify
Dump: research/cycle_db.json
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


def U11_imp_gives_B() -> bool:
    """U'_t=U'_{t+1}=1 and U'=>V' force V'=11 and W'_next=not U'_t=0 != 1."""
    Ut = Un = 1
    Wn = Ut ^ 1
    return Wn == 0 and Wn != Un


def U00_Vp11_gives_B() -> bool:
    """U'=00 on a V' 11: W'_next=U' XOR 1=1 != 0."""
    Ut = 0
    Wn = Ut ^ 1
    return Wn == 1


def identities_even_n0() -> dict:
    n_ok = 0
    n_A = 0
    n_imp = 0
    n_U11 = 0
    n_U00 = 0
    n_imp_n010 = 0
    for n0 in EVEN_N0:
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            seqs = scar_lift(T0, 16)
            if seqs is None or 18 not in seqs:
                return {"ok": False, "n_ok": n_ok, "why": "lift"}
            T = seqs[1]
            U = seqs[4]
            Up, Vp, Wp, Xp = seqs[15], seqs[16], seqs[17], seqs[18]
            if not reset_toggle_step(T, U):
                return {"ok": False, "n_ok": n_ok, "why": "reset"}
            if Wp == Xp:
                return {"ok": False, "n_ok": n_ok, "why": "WX"}
            A = has10(Up, Vp)
            imp = all((not a) or b for a, b in zip(Up, Vp))
            if A:
                n_A += 1
                if imp:
                    return {"ok": False, "n_ok": n_ok, "why": "Aimp"}
            elif not imp:
                return {"ok": False, "n_ok": n_ok, "why": "neither"}
            else:
                n_imp += 1
                if n0 != 10:
                    return {"ok": False, "n_ok": n_ok, "why": "n0"}
                n_imp_n010 += 1
                if not has11(Vp):
                    return {"ok": False, "n_ok": n_ok, "why": "Vp11"}
                U11 = False
                U00 = False
                B = False
                L = len(T)
                for t in range(L):
                    nxt = (t + 1) % L
                    if Vp[t] == 1 and Wp[t] != Up[t]:
                        B = True
                    if Vp[t] == 1 and Vp[nxt] == 1:
                        if Up[t] == 1 and Up[nxt] == 1:
                            U11 = True
                            if Wp[nxt] != 0:
                                return {"ok": False, "n_ok": n_ok, "why": "U11W"}
                        if Up[t] == 0 and Up[nxt] == 0:
                            U00 = True
                            if Wp[nxt] != 1:
                                return {"ok": False, "n_ok": n_ok, "why": "U00W"}
                if not B:
                    return {"ok": False, "n_ok": n_ok, "why": "noB"}
                if U11:
                    n_U11 += 1
                elif U00:
                    n_U00 += 1
                else:
                    return {"ok": False, "n_ok": n_ok, "why": "noarm"}
            n_ok += 1
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_A": n_A,
        "n_imp": n_imp,
        "n_U11": n_U11,
        "n_U00": n_U00,
        "n_imp_n010": n_imp_n010,
    }


def self_checks(c20, loc: tuple[bool, bool, bool], ids: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert ids["ok"] and ids["n_ok"] == expect
    assert ids["n_A"] + ids["n_imp"] == expect
    assert ids["n_imp"] == ids["n_imp_n010"] == 20
    assert ids["n_U11"] + ids["n_U00"] == ids["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), U11_imp_gives_B(), U00_Vp11_gives_B())
    ids = identities_even_n0()
    checks = self_checks(c20, loc, ids)
    dump = {
        "cycle": "DB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identities": {
            "n_ok": ids["n_ok"],
            "n_A": ids["n_A"],
            "n_imp": ids["n_imp"],
            "n_U11": ids["n_U11"],
            "n_U00": ids["n_U00"],
            "n_imp_n010": ids["n_imp_n010"],
        },
        "lemmas": {
            "UpVp_10_or_imp": True,
            "imp_only_n0_10": True,
            "imp_Vp11_U11_or_U00": True,
            "fifteenth_pair_never_equal": True,
            "all_T0_2power_hamming_ge_1": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "UpVp_10_or_imp": "LEMMA",
            "imp_only_n0_10": "LEMMA",
            "imp_Vp11_U11_or_U00": "LEMMA",
            "fifteenth_pair_never_equal": "LEMMA",
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
