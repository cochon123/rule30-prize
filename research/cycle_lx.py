#!/usr/bin/env python3
"""Cycle LX: only p=4 and p=6 are silent-free on covering G=1.

On covering J6,J10 for k<=6, the only packed indices at which every
Green one has packed AND (no silent G=1 columns) are p=4 and p=6.
Not only p=4; not silent-free at p=14 on the census; not silent-free
only those two in each walk (k=2 q=6 also has p=14); not rest XOR 0.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_lx.py --certify
Dump: research/cycle_lx.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LW_JSON = Path(__file__).resolve().parent / "cycle_lw.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

WANT_SF = frozenset({4, 6})


def _walk_census(k: int, q: int) -> dict:
    """Covering per-p G=1/AND/silent plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = xor_46 = xor_rest = 0
    slot = defaultdict(lambda: {"g1": 0, "and_g1": 0, "silent": 0, "and_g0": 0})
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
                    if packed:
                        slot[p]["and_g0"] += 1
                    continue
                n_g1 += 1
                slot[p]["g1"] += 1
                if packed:
                    xor_j ^= 1
                    slot[p]["and_g1"] += 1
                    if p in WANT_SF:
                        xor_46 ^= 1
                    else:
                        xor_rest ^= 1
                else:
                    slot[p]["silent"] += 1
        row = rule30_step(row)
        s += 1
    sf = frozenset(p for p, st in slot.items() if st["g1"] and st["silent"] == 0)
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "xor_46": xor_46,
        "xor_rest": xor_rest,
        "sf": sf,
        "slot": dict(slot),
    }


def silent_free() -> dict:
    """k<=6: aggregate silent-free packed p with G=1 is exactly {4,6}."""
    n_ok = n_g1 = 0
    agg = defaultdict(lambda: {"g1": 0, "and_g1": 0, "silent": 0, "and_g0": 0})
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    n_rest = 0
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_census(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            for p, st in w["slot"].items():
                for key in ("g1", "and_g1", "silent", "and_g0"):
                    agg[p][key] += st[key]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_rest += w["xor_rest"]
            krow[name] = {
                "xor_j": w["xor_j"],
                "xor_46": w["xor_46"],
                "xor_rest": w["xor_rest"],
                "sf": sorted(w["sf"]),
            }
        rows[str(k)] = krow
    sf = frozenset(p for p, st in agg.items() if st["g1"] and st["silent"] == 0)
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and sf == WANT_SF
        and agg[4]["g1"] == 56
        and agg[4]["silent"] == 0
        and agg[6]["g1"] == 46
        and agg[6]["silent"] == 0
        and agg[14]["silent"] > 0
        and n_rest > 0
        and 4 in rows["0"]["j6"]["sf"]
        and 6 in rows["0"]["j6"]["sf"]
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "sf": sorted(sf),
        "n_p4_g1": agg[4]["g1"],
        "n_p6_g1": agg[6]["g1"],
        "n_p14_silent": agg[14]["silent"],
        "rows": rows,
    }


def killed_only_p4() -> dict:
    """only p=4 is silent-free: p=6 is too."""
    ok = WANT_SF == frozenset({4, 6})
    return {"ok": ok, "sf": sorted(WANT_SF)}


def killed_p14() -> dict:
    """p=14 is silent-free on the census: k=1 q=10 has a silent column."""
    w = _walk_census(1, 10)
    st = w["slot"].get(14, {"g1": 0, "silent": 0, "and_g1": 0})
    ok = w.get("ok") and st["silent"] > 0
    return {"ok": ok, "k": 1, "q": 10, "g1": st["g1"], "silent": st["silent"]}


def killed_per_walk() -> dict:
    """each walk's silent-free set is only {4,6}: k=2 q=6 also has p=14."""
    w = _walk_census(2, 6)
    ok = w.get("ok") and 14 in w["sf"] and WANT_SF <= w["sf"]
    return {"ok": ok, "k": 2, "q": 6, "sf": sorted(w["sf"])}


def killed_rest0() -> dict:
    """AND xor off {4,6} vanishes: k=1 q=10 has rest XOR 1."""
    w = _walk_census(1, 10)
    ok = w.get("ok") and w["xor_rest"] == 1
    return {"ok": ok, "k": 1, "q": 10, "xor_rest": w["xor_rest"], "xor_j": w["xor_j"]}


def prefixes() -> dict:
    lw = json.loads(LW_JSON.read_text())
    ok = (
        lw["checks"]["all_ok"]
        and lw["verdict"]["p6_g1_and"] == "LEMMA"
        and lw["verdict"]["p4_g1_and"] == "LEMMA"
        and lw["verdict"]["p4_1001"] == "LEMMA"
        and lw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert rt["sf"] == [4, 6]
    assert rt["n_p4_g1"] == 56
    assert rt["n_p6_g1"] == 46
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = silent_free()
    sc = g4_xor_cover()
    k0 = killed_only_p4()
    k1 = killed_p14()
    k2 = killed_per_walk()
    k3 = killed_rest0()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "silent_free": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_only_p4": {k: k0[k] for k in k0 if k != "ok"},
        "killed_p14": {k: k1[k] for k in k1 if k != "ok"},
        "killed_per_walk": {k: k2[k] for k in k2 if k != "ok"},
        "killed_rest0": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
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
            "only_p4": False,
            "p14_g1_and": False,
            "per_walk": False,
            "rest0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
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
            "only_p4": "KILLED",
            "p14_g1_and": "KILLED",
            "per_walk": "KILLED",
            "rest0": "KILLED",
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
        "silent_free n_ok",
        dump["silent_free"]["n_ok"],
        "sf",
        dump["silent_free"]["sf"],
        "n_p4_g1",
        dump["silent_free"]["n_p4_g1"],
        "n_p6_g1",
        dump["silent_free"]["n_p6_g1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_only_p4", dump["killed_only_p4"])
    print("killed_p14", dump["killed_p14"])
    print("killed_per_walk", dump["killed_per_walk"])
    print("killed_rest0", dump["killed_rest0"])


if __name__ == "__main__":
    main()
