#!/usr/bin/env python3
"""Cycle FE: covering fails iff three off-cone J from time 2U vanish.

Cycle AI: c_{t+2^m}=c_t XOR x(t,±2^m) XOR J_{[t,t+2^m)->t+2^m}, with
x(t,j)=0 for |j|>t. From t=2U=2^{k+1} the steps 4U,8U,16U have
|j|=2t,4t,8t > t, so extras vanish and

    phi^{(q)}_k = I_{k+1} XOR J_{[2U, qU) -> qU}

for q in {6,10,18}. Covering fails at k+1 iff those three J vanish
(equivalent to Cycle BO's even spines equal I). On Cycle DS spines
through k=18, J6=J10=0 implies J18=1 (the five candidates), so the
three J are never all 0. Kills: J6=J10=1 implies J18=0 (cex k=14).
Do not claim never-fail for all k; do not push even-spine past k=18;
do not compute phi^{(3,5,9)} at k=16; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_fe.py --certify
Dump: research/cycle_fe.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
AI_JSON = Path(__file__).resolve().parent / "cycle_ai.json"
BO_JSON = Path(__file__).resolve().parent / "cycle_bo.json"
DS_JSON = Path(__file__).resolve().parent / "cycle_ds.json"
FD_JSON = Path(__file__).resolve().parent / "cycle_fd.json"


def off_cone() -> dict:
    """From t=2U, steps 4U,8U,16U have |j|>t for every k>=0."""
    n_ok = 0
    for k in range(0, 41):
        t = 2 << k  # 2U = 2^{k+1}
        for m in (2, 3, 4):
            w = 1 << (k + m)  # 4U, 8U, 16U
            if w <= t:
                return {"ok": False, "k": k, "w": w, "t": t}
            n_ok += 1
    return {"ok": n_ok == 41 * 3, "n_ok": n_ok}


def j_from_ds() -> dict:
    """J_q = phi^{(q)} XOR I_{k+1}; fail iff all three vanish."""
    ds = json.loads(DS_JSON.read_text())
    pref = ds["prefix"]
    ks = pref["k"]
    p2, p6, p10, p18 = pref["phi2"], pref["phi6"], pref["phi10"], pref["phi18"]
    rows = []
    n_all0 = 0
    n_j6j10_0 = 0
    n_impl = 0
    n_j6j10_1_j18_0 = 0
    cex_j11 = []
    for i, k in enumerate(ks):
        I = p2[i]
        j6, j10, j18 = p6[i] ^ I, p10[i] ^ I, p18[i] ^ I
        fail = j6 == 0 and j10 == 0 and j18 == 0
        aligned = p6[i] == I and p10[i] == I and p18[i] == I
        if fail != aligned:
            return {"ok": False, "k": k, "eq": True}
        if fail:
            n_all0 += 1
        if j6 == 0 and j10 == 0:
            n_j6j10_0 += 1
            if j18 == 1:
                n_impl += 1
            else:
                return {"ok": False, "k": k, "impl": True}
        if j6 == 1 and j10 == 1:
            if j18 == 0:
                n_j6j10_1_j18_0 += 1
            else:
                cex_j11.append(k)
        rows.append(
            {
                "k": k,
                "I": I,
                "J6": j6,
                "J10": j10,
                "J18": j18,
                "fail": fail,
            }
        )
    candidates = [r["k"] for r in rows if r["J6"] == 0 and r["J10"] == 0]
    ok = (
        n_all0 == 0
        and n_j6j10_0 == 5
        and n_impl == 5
        and candidates == ds["candidate_k"]
        and 14 in cex_j11
        and ds["dangerous_k"] == []
    )
    return {
        "ok": ok,
        "n_all0": n_all0,
        "n_j6j10_0": n_j6j10_0,
        "n_impl": n_impl,
        "candidates": candidates,
        "cex_j6j10_1_implies_j18_0": cex_j11,
        "n_j6j10_1_j18_0": n_j6j10_1_j18_0,
        "k14": next(r for r in rows if r["k"] == 14),
        "k15": next(r for r in rows if r["k"] == 15),
        "k18": next(r for r in rows if r["k"] == 18),
    }


def prefixes() -> dict:
    ai = json.loads(AI_JSON.read_text())
    bo = json.loads(BO_JSON.read_text())
    ds = json.loads(DS_JSON.read_text())
    fd = json.loads(FD_JSON.read_text())
    ok = (
        ai["checks"]["all_ok"]
        and bo["checks"]["all_ok"]
        and ds["checks"]["all_ok"]
        and fd["checks"]["all_ok"]
        and ai["verdict"]["dyadic_step"] == "LEMMA"
        and bo["verdict"]["cover_fails_iff_even_spines_eq_I"] == "LEMMA"
        and ds["verdict"]["cover_fails_iff_even_spines_eq_I"] == "LEMMA"
        and fd["verdict"]["cons00_iff_U0_and_A_eq_B"] == "LEMMA"
        and fd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, cone: dict, js: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cone["ok"] and js["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cone = off_cone()
    js = j_from_ds()
    pref = prefixes()
    checks = self_checks(c20, cone, js, pref)
    dump = {
        "cycle": "FE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "off_cone": {k: cone[k] for k in cone if k != "ok"},
        "J": {k: js[k] for k in js if k != "ok"},
        "lemmas": {
            "off_cone_extras_from_2U": True,
            "phi_q_eq_I_xor_J_2U_qU": True,
            "cover_fails_iff_J6_J10_J18_vanish": True,
            "J6_J10_0_implies_J18_1_k_2_18": True,
            "J6_J10_1_implies_J18_0": False,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "off_cone_extras_from_2U": "LEMMA",
            "phi_q_eq_I_xor_J_2U_qU": "LEMMA",
            "cover_fails_iff_J6_J10_J18_vanish": "LEMMA",
            "J6_J10_0_implies_J18_1_k_2_18": "PREFIX",
            "J6_J10_1_implies_J18_0": "KILLED",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("off_cone", dump["off_cone"])
    print("J", dump["J"])


if __name__ == "__main__":
    main()
