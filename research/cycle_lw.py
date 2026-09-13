#!/usr/bin/env python3
"""Cycle LW: covering G=1 at p=6 always has packed AND.

On covering J6,J10 for k<=6, every Green one at packed p=6 has
packed AND (no silent G=1 columns). The G=1 count equals Cycle LD's
AND count want_p6_n, so the p=6 contribution to J is the Green-ones
XOR at p=6: 0 at k=0, else 1. Not AND iff G=1 (AND still fires on
G=0); not silent-free at p=14; not equal to J; not the p=4 count.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_lw.py --certify
Dump: research/cycle_lw.json
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
from cycle_lc import want_p4_n
from cycle_ld import PAT0100, want_p6_n, want_p6_xor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LV_JSON = Path(__file__).resolve().parent / "cycle_lv.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _walk_slot(k: int, q: int, slot: int) -> dict:
    """Covering G=1/AND/silent/G=0 at one packed p, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    g1 = and_g1 = silent = and_g0 = n_other = xor_slot = 0
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
                    if p == slot and packed:
                        and_g0 += 1
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                if p != slot:
                    continue
                g1 += 1
                if packed:
                    and_g1 += 1
                    xor_slot ^= 1
                    if four != PAT0100:
                        n_other += 1
                else:
                    silent += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "g1": g1,
        "and_g1": and_g1,
        "silent": silent,
        "and_g0": and_g0,
        "n_other": n_other,
        "xor_slot": xor_slot,
    }


def p6_g1_and() -> dict:
    """k<=6: every G=1 column at p=6 has packed AND, count want_p6_n."""
    n_ok = n_g1 = n_p6_g1 = n_silent = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_slot(k, q, 6)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p6_n(k, q)
            wantx = want_p6_xor(k)
            if (
                w["g1"] != wantn
                or w["and_g1"] != wantn
                or w["silent"] != 0
                or w["n_other"] != 0
                or w["xor_slot"] != wantx
            ):
                return {
                    "ok": False,
                    "p6": True,
                    "k": k,
                    "q": q,
                    "g1": w["g1"],
                    "and_g1": w["and_g1"],
                    "silent": w["silent"],
                    "n_other": w["n_other"],
                    "xor_slot": w["xor_slot"],
                    "want": wantn,
                    "wantx": wantx,
                }
            n_p6_g1 += w["g1"]
            n_silent += w["silent"]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "g1": w["g1"],
                "and_g1": w["and_g1"],
                "silent": w["silent"],
                "and_g0": w["and_g0"],
                "xor_slot": w["xor_slot"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p6_g1 == 46
        and n_silent == 0
        and rows["0"]["j6"]["xor_slot"] == 0
        and rows["0"]["j10"]["and_g0"] > 0
        and rows["1"]["j6"]["xor_j"] == 0
        and want_p6_n(6, 10) == 7
        and PAT0100 == (0, 1, 0, 0)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_p6_g1": n_p6_g1,
        "n_silent": n_silent,
        "rows": rows,
    }


def killed_iff() -> dict:
    """AND at p=6 fires iff G=1: k=0 q=10 has AND on G=0."""
    w = _walk_slot(0, 10, 6)
    ok = w.get("ok") and w["and_g0"] > 0 and w["silent"] == 0
    return {"ok": ok, "k": 0, "q": 10, "and_g0": w["and_g0"], "silent": w["silent"]}


def killed_p14() -> dict:
    """G=1 at p=14 always has packed AND: k=1 q=10 has a silent column."""
    w = _walk_slot(1, 10, 14)
    ok = w.get("ok") and w["silent"] > 0
    return {"ok": ok, "k": 1, "q": 10, "g1": w["g1"], "and_g1": w["and_g1"], "silent": w["silent"]}


def killed_eq_j() -> dict:
    """p=6 Green-ones XOR is J: k=1 q=6 has xor_slot=1 and J=0."""
    w = _walk_slot(1, 6, 6)
    ok = w.get("ok") and w["xor_slot"] == 1 and w["xor_j"] == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_slot": w["xor_slot"], "xor_j": w["xor_j"]}


def killed_eq_p4() -> dict:
    """p=6 G=1 count equals p=4 count: k=0 q=6 is 2 vs 1."""
    ok = want_p6_n(0, 6) == 2 and want_p4_n(0, 6) == 1
    return {"ok": ok, "p6": want_p6_n(0, 6), "p4": want_p4_n(0, 6)}


def prefixes() -> dict:
    lv = json.loads(LV_JSON.read_text())
    ok = (
        lv["checks"]["all_ok"]
        and lv["verdict"]["p4_g1_and"] == "LEMMA"
        and lv["verdict"]["p114_0100"] == "LEMMA"
        and lv["verdict"]["p4_1001"] == "LEMMA"
        and lv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0100 == (0, 1, 0, 0)
    assert want_p6_n(0, 6) == 2
    assert want_p6_xor(0) == 0
    assert want_p6_xor(1) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p6_g1_and()
    sc = g4_xor_cover()
    k0 = killed_iff()
    k1 = killed_p14()
    k2 = killed_eq_j()
    k3 = killed_eq_p4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p6_g1_and": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_iff": {k: k0[k] for k in k0 if k != "ok"},
        "killed_p14": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_j": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_p4": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
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
            "iff": False,
            "p14_g1_and": False,
            "eq_j": False,
            "eq_p4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
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
            "iff": "KILLED",
            "p14_g1_and": "KILLED",
            "eq_j": "KILLED",
            "eq_p4": "KILLED",
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
        "p6_g1_and n_ok",
        dump["p6_g1_and"]["n_ok"],
        "n_p6_g1",
        dump["p6_g1_and"]["n_p6_g1"],
        "n_silent",
        dump["p6_g1_and"]["n_silent"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_iff", dump["killed_iff"])
    print("killed_p14", dump["killed_p14"])
    print("killed_eq_j", dump["killed_eq_j"])
    print("killed_eq_p4", dump["killed_eq_p4"])


if __name__ == "__main__":
    main()
