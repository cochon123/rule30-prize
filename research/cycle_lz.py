#!/usr/bin/env python3
"""Cycle LZ: covering J on k<=6 is a closed (k,q) form.

On covering J6,J10 for k<=6, packed AND xor off {p=4,p=6,p=14} is 1
iff q==10 and k%4==2. The {4,6,14} XOR is 1_{k==0} xor want_p14_xor,
so J equals want_j(k,q). Not rest always 0; not the LB 1001 remainder
(that is q==6 and k%4==2); not J identically 1; not the formula for
all k. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_lz.py --certify
Dump: research/cycle_lz.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lb import want_1001_rem
from cycle_ld import want_p6_xor
from cycle_lf import want_p14_xor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LY_JSON = Path(__file__).resolve().parent / "cycle_ly.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

FORCED = frozenset({4, 6, 14})


def want_rest(k: int, q: int) -> int:
    """AND xor off {4,6,14}: 1 iff q==10 and k%4==2."""
    return int(q == 10 and k % 4 == 2)


def want_forced(k: int, q: int) -> int:
    """AND xor at {4,6,14} from Cycles LC/LD/LF."""
    return (1 if k == 0 else 0) ^ want_p14_xor(k, q)


def want_j(k: int, q: int) -> int:
    """Covering odd-s J on k<=6."""
    return want_forced(k, q) ^ want_rest(k, q)


def _walk_rest(k: int, q: int) -> dict:
    """Covering J, forced {4,6,14} XOR, and rest XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = xor_f = xor_rest = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                    if p in FORCED:
                        xor_f ^= 1
                    else:
                        xor_rest ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "xor_f": xor_f,
        "xor_rest": xor_rest,
    }


def j_form() -> dict:
    """k<=6: rest=want_rest, forced=want_forced, J=want_j."""
    n_ok = n_g1 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rest(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            wr, wf, wj = want_rest(k, q), want_forced(k, q), want_j(k, q)
            if (
                w["xor_j"] != jwant
                or w["xor_rest"] != wr
                or w["xor_f"] != wf
                or w["xor_j"] != wj
                or w["xor_j"] != w["xor_f"] ^ w["xor_rest"]
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_j": w["xor_j"],
                    "jwant": jwant,
                    "xor_f": w["xor_f"],
                    "xor_rest": w["xor_rest"],
                    "wr": wr,
                    "wf": wf,
                    "wj": wj,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "xor_j": w["xor_j"],
                "xor_f": w["xor_f"],
                "xor_rest": w["xor_rest"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and rows["2"]["j10"]["xor_rest"] == 1
        and rows["6"]["j10"]["xor_rest"] == 1
        and rows["2"]["j6"]["xor_rest"] == 0
        and rows["0"]["j6"]["xor_j"] == 1
        and rows["2"]["j6"]["xor_j"] == 0
        and rows["2"]["j10"]["xor_j"] == 0
        and want_j(6, 10) == 0
        and want_j(6, 6) == 1
        and want_rest(2, 10) == 1
        and want_1001_rem(2, 6) == 1
        and want_p6_xor(0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_rest0() -> dict:
    """rest XOR always 0: k=2 q=10 is 1."""
    ok = want_rest(2, 10) == 1
    return {"ok": ok, "k": 2, "q": 10, "rest": want_rest(2, 10)}


def killed_eq_lb() -> dict:
    """rest equals LB 1001 rem: k=2 q=6 rem=1 rest=0."""
    ok = want_1001_rem(2, 6) == 1 and want_rest(2, 6) == 0
    return {"ok": ok, "rem": want_1001_rem(2, 6), "rest": want_rest(2, 6)}


def killed_j1() -> dict:
    """J identically 1: k=1 q=6 is 0."""
    ok = want_j(1, 6) == 0
    return {"ok": ok, "k": 1, "q": 6, "j": want_j(1, 6)}


def killed_eq_j() -> dict:
    """rest equals J: k=0 q=6 has rest=0 and J=1."""
    ok = want_rest(0, 6) == 0 and want_j(0, 6) == 1
    return {"ok": ok, "rest": want_rest(0, 6), "j": want_j(0, 6)}


def prefixes() -> dict:
    ly = json.loads(LY_JSON.read_text())
    ok = (
        ly["checks"]["all_ok"]
        and ly["verdict"]["p14_except"] == "LEMMA"
        and ly["verdict"]["only_p4_p6"] == "LEMMA"
        and ly["verdict"]["p4_1001"] == "LEMMA"
        and ly["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_j(0, 10) == 1
    assert want_j(2, 10) == 0
    assert want_rest(6, 10) == 1
    assert want_forced(2, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = j_form()
    sc = g4_xor_cover()
    k0 = killed_rest0()
    k1 = killed_eq_lb()
    k2 = killed_j1()
    k3 = killed_eq_j()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "j_form": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_rest0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_lb": {k: k1[k] for k in k1 if k != "ok"},
        "killed_j1": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_j": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "p114_0100": True,
            "p76_0011": True,
            "p86_0011": True,
            "p58_0011": True,
            "p88_0100": True,
            "p72_1001": True,
            "p42_0011": True,
            "p38_0100": True,
            "p52_1001": True,
            "p60_0100": True,
            "p30_0011": True,
            "p98_0010": True,
            "p106_1001": True,
            "p54_0100": True,
            "p32_0100": True,
            "p16_1001": True,
            "p14_0011": True,
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "rest0": False,
            "eq_lb": False,
            "j1": False,
            "eq_j": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "p114_0100": "LEMMA",
            "p76_0011": "LEMMA",
            "p86_0011": "LEMMA",
            "p58_0011": "LEMMA",
            "p88_0100": "LEMMA",
            "p72_1001": "LEMMA",
            "p42_0011": "LEMMA",
            "p38_0100": "LEMMA",
            "p52_1001": "LEMMA",
            "p60_0100": "LEMMA",
            "p30_0011": "LEMMA",
            "p98_0010": "LEMMA",
            "p106_1001": "LEMMA",
            "p54_0100": "LEMMA",
            "p32_0100": "LEMMA",
            "p16_1001": "LEMMA",
            "p14_0011": "LEMMA",
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "rest0": "KILLED",
            "eq_lb": "KILLED",
            "j1": "KILLED",
            "eq_j": "KILLED",
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
    print(
        "j_form n_ok",
        dump["j_form"]["n_ok"],
        "n_g1",
        dump["j_form"]["n_g1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_rest0", dump["killed_rest0"])
    print("killed_eq_lb", dump["killed_eq_lb"])
    print("killed_j1", dump["killed_j1"])
    print("killed_eq_j", dump["killed_eq_j"])


if __name__ == "__main__":
    main()
