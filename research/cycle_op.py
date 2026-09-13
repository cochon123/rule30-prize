#!/usr/bin/env python3
"""Cycle OP: even-parent S is residue-2 xor of m/2.

For even m=2p, S(2m+1)=xor G(m, m+4+6i) equals pal-right residue
2 of G(p). Even rows swap residues: R1(2p)=R2(p) and
R2(2p)=R1(p). Hence S(8t+1)=R1(t) and S(8t+5)=R2(2t+1). Not a
0-1 evaluation of those residues. Not covering S (clip remains).
Not E_k=0 for all k. Do not catalogue further S/T subregions
unless the experiment answers why E_k=0. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_op.py --certify
Dump: research/cycle_op.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_ok import pal_right_s
from cycle_ol import even_m_s

OUT = Path(__file__).resolve().with_suffix(".json")
OO_JSON = Path(__file__).resolve().parent / "cycle_oo.json"
ON_JSON = Path(__file__).resolve().parent / "cycle_on.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

M_HI = 128
T_HI = 64
N_PAL = 64
M_SLOTS = 64


def pal_right_R(t: int) -> list[int]:
    """Xor of G(t, t+d) by d%3 for d=1..t."""
    r = [0, 0, 0]
    for j in range(t + 1, 2 * t + 1):
        r[(j - t) % 3] ^= G(t, j)
    return r


def b_eq_r2() -> dict:
    """Even m=2p<M_HI: even_m_s(m)==R2(p); odd offsets silent."""
    n_ok = n_odd_d = n_one = 0
    sample = {}
    for m in range(0, M_HI, 2):
        p = m // 2
        for d in range(1, m + 2, 2):
            if d <= m and G(m, m + d) != 0:
                return {"ok": False, "odd_d": m, "d": d}
            n_odd_d += 1
        got = even_m_s(m)
        want = pal_right_R(p)[2]
        if got != want or pal_right_s(2 * m + 1)[0] != got:
            return {"ok": False, "m": m, "got": got, "want": want}
        n_ok += 1
        n_one += got
        if m <= 8:
            sample[str(m)] = {"B": got, "R2": want, "n": 2 * m + 1, "p": p}
    ok = (
        n_ok == M_HI // 2
        and sample["0"]["B"] == 0
        and sample["4"]["B"] == 1
        and n_one > 0
        and n_one < n_ok
        and n_odd_d > 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_one": n_one,
        "n_odd_d": n_odd_d,
        "sample": sample,
    }


def residue_swap() -> dict:
    """p<M_HI: R1(2p)=R2(p) and R2(2p)=R1(p)."""
    n_ok = 0
    sample = {}
    for p in range(0, M_HI):
        a = pal_right_R(2 * p)
        b = pal_right_R(p)
        if a[1] != b[2] or a[2] != b[1]:
            return {"ok": False, "p": p, "R2p": a, "Rp": b}
        n_ok += 1
        if p <= 4:
            sample[str(p)] = {"R_2p": a, "R_p": b}
    ok = (
        n_ok == M_HI
        and sample["0"]["R_2p"] == [0, 0, 0]
        and sample["1"]["R_p"][1] == 1
        and sample["1"]["R_2p"][2] == 1
        and sample["2"]["R_p"][2] == 1
        and sample["2"]["R_2p"][1] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "sample": sample}


def n15_res() -> dict:
    """t<T_HI: S(8t+1)=R1(t), S(8t+5)=R2(2t+1), B(4t)=R1(t)."""
    n_ok = n_one1 = n_one5 = 0
    sample = {}
    for t in range(0, T_HI):
        s1 = pal_right_s(8 * t + 1)[0]
        s5 = pal_right_s(8 * t + 5)[0]
        r1 = pal_right_R(t)[1]
        r2 = pal_right_R(2 * t + 1)[2]
        b4 = even_m_s(4 * t)
        if s1 != r1 or s5 != r2 or b4 != r1:
            return {
                "ok": False,
                "t": t,
                "s1": s1,
                "r1": r1,
                "s5": s5,
                "r2": r2,
                "b4": b4,
            }
        n_ok += 1
        n_one1 += s1
        n_one5 += s5
        if t <= 4:
            sample[str(t)] = {
                "n1": 8 * t + 1,
                "s1": s1,
                "n5": 8 * t + 5,
                "s5": s5,
            }
    ok = (
        n_ok == T_HI
        and sample["0"]["s1"] == 0
        and sample["0"]["s5"] == 0
        and sample["1"]["s1"] == 1
        and sample["1"]["s5"] == 1
        and n_one1 > 0
        and n_one5 > 0
        and n_one1 < n_ok
        and n_one5 < n_ok
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_one1": n_one1,
        "n_one5": n_one5,
        "t_hi": T_HI,
        "sample": sample,
    }


def killed_r1_one(swap: dict) -> dict:
    ok = swap["sample"]["2"]["R_p"][1] == 0
    return {"ok": ok, "t": 2, "R1": 0}


def killed_b_zero(beq: dict) -> dict:
    ok = beq["sample"]["4"]["B"] == 1
    return {"ok": ok, "m": 4, "n": 9, "B": 1}


def killed_odd_closed(n15: dict) -> dict:
    ok = n15["sample"]["0"]["s1"] == 0 and n15["sample"]["1"]["s1"] == 1
    return {"ok": ok, "n1": 0, "n9": 1}


def prefixes() -> dict:
    oo = json.loads(OO_JSON.read_text())
    on = json.loads(ON_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oo["checks"]["all_ok"]
        and on["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oo["verdict"]["n3_one_all_t"] == "LEMMA"
        and on["verdict"]["s4_fold"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oo["verdict"]["odd_s_closed"] == "PREFIX"
        and oo["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, beq, swap, n15, k1, kb, kc, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and beq["ok"]
        and swap["ok"]
        and n15["ok"]
        and k1["ok"]
        and kb["ok"]
        and kc["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    beq = b_eq_r2()
    swap = residue_swap()
    n15 = n15_res()
    k1 = killed_r1_one(swap)
    kb = killed_b_zero(beq)
    kc = killed_odd_closed(n15)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, beq, swap, n15, k1, kb, kc, sc, pref)
    dump = {
        "cycle": "OP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "b_eq_r2": {k: beq[k] for k in beq if k != "ok"},
        "residue_swap": {k: swap[k] for k in swap if k != "ok"},
        "n15_res": {k: n15[k] for k in n15 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_r1_one": {k: k1[k] for k in k1 if k != "ok"},
        "killed_b_zero": {k: kb[k] for k in kb if k != "ok"},
        "killed_odd_closed": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "b_eq_r2": True,
            "residue_swap": True,
            "s81_R1": True,
            "s85_R2": True,
            "n3_one_all_t": True,
            "s4_fold": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "r1_all_one": False,
            "b_zero": False,
            "odd_s_closed": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "b_eq_r2": "LEMMA",
            "residue_swap": "LEMMA",
            "s81_R1": "LEMMA",
            "s85_R2": "LEMMA",
            "n3_one_all_t": "LEMMA",
            "s4_fold": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "r1_all_one": "KILLED",
            "b_zero": "KILLED",
            "odd_s_closed": "PREFIX",
            "covering_S": "PREFIX",
            "E_all_k": "PREFIX",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
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
    print("b_eq_r2 n_ok", dump["b_eq_r2"]["n_ok"], "n_one", dump["b_eq_r2"]["n_one"])
    print("residue_swap n_ok", dump["residue_swap"]["n_ok"])
    print("n15_res", dump["n15_res"]["n_ok"], "n_one1", dump["n15_res"]["n_one1"], "n_one5", dump["n15_res"]["n_one5"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_r1_one", dump["killed_r1_one"])
    print("killed_b_zero", dump["killed_b_zero"])
    print("killed_odd_closed", dump["killed_odd_closed"])


if __name__ == "__main__":
    main()
