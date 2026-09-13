#!/usr/bin/env python3
"""Cycle LY: G=1 at p=14 has packed AND except two t=0 cells.

On covering J6,J10 for k<=6, every Green one at packed p=14 has
packed AND except (k,q)=(1,10) and (2,10), each with one silent 0000
at t=0. The AND count is still want_p14_n (Cycle LF); the G=1 count
is that plus the two silents. Not silent-free; not only k=1; not
silent on q=6; not AND at those cells. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ly.py --certify
Dump: research/cycle_ly.json
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
from cycle_lf import PAT0011, want_p14_n, want_p14_xor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LX_JSON = Path(__file__).resolve().parent / "cycle_lx.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

SILENT_KQ = frozenset({(1, 10), (2, 10)})


def want_p14_silent(k: int, q: int) -> int:
    """Covering G=1 silent count at p=14."""
    return int((k, q) in SILENT_KQ)


def want_p14_g1(k: int, q: int) -> int:
    """Covering G=1 column count at p=14."""
    return want_p14_n(k, q) + want_p14_silent(k, q)


def _walk_p14(k: int, q: int) -> dict:
    """Covering G=1/AND/silent at p=14, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    g1 = and_g1 = silent = silent_t0 = and_g0 = n_other = xor_slot = 0
    silent_four = "none"
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
                    if p == 14 and packed:
                        and_g0 += 1
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                if p != 14:
                    continue
                g1 += 1
                if packed:
                    and_g1 += 1
                    xor_slot ^= 1
                    if four != PAT0011:
                        n_other += 1
                else:
                    silent += 1
                    if t == 0:
                        silent_t0 += 1
                    silent_four = "".join(map(str, four))
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
        "silent_t0": silent_t0,
        "silent_four": silent_four,
        "and_g0": and_g0,
        "n_other": n_other,
        "xor_slot": xor_slot,
    }


def p14_except() -> dict:
    """k<=6: G=1 at p=14 has AND except two t=0 silents."""
    n_ok = n_g1 = n_p14_g1 = n_silent = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p14(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p14_n(k, q)
            wantg = want_p14_g1(k, q)
            wants = want_p14_silent(k, q)
            wantx = want_p14_xor(k, q)
            if (
                w["g1"] != wantg
                or w["and_g1"] != wantn
                or w["silent"] != wants
                or w["silent_t0"] != wants
                or w["n_other"] != 0
                or w["xor_slot"] != wantx
                or (wants and w["silent_four"] != "0000")
            ):
                return {
                    "ok": False,
                    "p14": True,
                    "k": k,
                    "q": q,
                    "g1": w["g1"],
                    "and_g1": w["and_g1"],
                    "silent": w["silent"],
                    "silent_t0": w["silent_t0"],
                    "silent_four": w["silent_four"],
                    "xor_slot": w["xor_slot"],
                    "wantn": wantn,
                    "wantg": wantg,
                    "wants": wants,
                    "wantx": wantx,
                }
            n_p14_g1 += w["g1"]
            n_silent += w["silent"]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "g1": w["g1"],
                "and_g1": w["and_g1"],
                "silent": w["silent"],
                "silent_t0": w["silent_t0"],
                "silent_four": w["silent_four"],
                "xor_slot": w["xor_slot"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p14_g1 == 52
        and n_silent == 2
        and rows["1"]["j10"]["silent"] == 1
        and rows["2"]["j10"]["silent"] == 1
        and rows["1"]["j6"]["silent"] == 0
        and rows["3"]["j10"]["silent"] == 0
        and want_p14_g1(1, 10) == 2
        and PAT0011 == (0, 0, 1, 1)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_p14_g1": n_p14_g1,
        "n_silent": n_silent,
        "rows": rows,
    }


def killed_silent_free() -> dict:
    """G=1 at p=14 always has packed AND: k=1 q=10 is silent."""
    w = _walk_p14(1, 10)
    ok = w.get("ok") and w["silent"] == 1
    return {"ok": ok, "k": 1, "q": 10, "silent": w["silent"], "g1": w["g1"]}


def killed_k1_only() -> dict:
    """silent only at k=1: k=2 q=10 is also silent."""
    w = _walk_p14(2, 10)
    ok = w.get("ok") and w["silent"] == 1
    return {"ok": ok, "k": 2, "q": 10, "silent": w["silent"], "g1": w["g1"]}


def killed_q6() -> dict:
    """silent on q=6: k=1 q=6 has no silent."""
    w = _walk_p14(1, 6)
    ok = w.get("ok") and w["silent"] == 0
    return {"ok": ok, "k": 1, "q": 6, "silent": w["silent"], "g1": w["g1"]}


def killed_and_silent() -> dict:
    """the silent cells have packed AND: k=1 q=10 is 0000."""
    w = _walk_p14(1, 10)
    ok = w.get("ok") and w["silent_four"] == "0000" and w["and_g1"] == 1
    return {"ok": ok, "k": 1, "q": 10, "silent_four": w["silent_four"], "and_g1": w["and_g1"]}


def prefixes() -> dict:
    lx = json.loads(LX_JSON.read_text())
    ok = (
        lx["checks"]["all_ok"]
        and lx["verdict"]["only_p4_p6"] == "LEMMA"
        and lx["verdict"]["p6_g1_and"] == "LEMMA"
        and lx["verdict"]["p4_1001"] == "LEMMA"
        and lx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0011 == (0, 0, 1, 1)
    assert want_p14_silent(1, 10) == 1
    assert want_p14_silent(2, 10) == 1
    assert want_p14_silent(3, 10) == 0
    assert want_p14_g1(2, 10) == 4
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p14_except()
    sc = g4_xor_cover()
    k0 = killed_silent_free()
    k1 = killed_k1_only()
    k2 = killed_q6()
    k3 = killed_and_silent()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p14_except": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_silent_free": {k: k0[k] for k in k0 if k != "ok"},
        "killed_k1_only": {k: k1[k] for k in k1 if k != "ok"},
        "killed_q6": {k: k2[k] for k in k2 if k != "ok"},
        "killed_and_silent": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
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
            "silent_free": False,
            "k1_only": False,
            "q6": False,
            "and_silent": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
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
            "silent_free": "KILLED",
            "k1_only": "KILLED",
            "q6": "KILLED",
            "and_silent": "KILLED",
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
        "p14_except n_ok",
        dump["p14_except"]["n_ok"],
        "n_p14_g1",
        dump["p14_except"]["n_p14_g1"],
        "n_silent",
        dump["p14_except"]["n_silent"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_silent_free", dump["killed_silent_free"])
    print("killed_k1_only", dump["killed_k1_only"])
    print("killed_q6", dump["killed_q6"])
    print("killed_and_silent", dump["killed_and_silent"])


if __name__ == "__main__":
    main()
