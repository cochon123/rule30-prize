#!/usr/bin/env python3
"""Cycle GT: at k=4, AND at lo is dead on every covering hit.

Extras XOR therefore misses lo, and in fact extras XOR vanishes on
all covering W, so hit-cone XOR = Q mod 2 (Cycle GS). AND at lo is
not dead on all odd s (live at delta=17 on W=8U). Extras are not
empty (W=8U has {6,7} and {1,4}). Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gt.py --certify
Dump: research/cycle_gt.json
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
from cycle_gn import mer_one
from cycle_gs import scan_hits
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GS_JSON = Path(__file__).resolve().parent / "cycle_gs.json"
GQ_JSON = Path(__file__).resolve().parent / "cycle_gq.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"


def packed_k4() -> dict:
    """k=4: AND at lo dead on all 7 covering hits; extras XOR=0."""
    k = 4
    U = 1 << k
    n_ok = 0
    n_lo_dead = 0
    rows = {}
    for W in (4 * U, 8 * U, 16 * U):
        T = 2 * U + W
        t0 = T - W // 2
        Q = W // (4 * U)
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        s = t0
        hx = ex = 0
        for q in range(Q):
            target = t0 + 1 + q * (2 * U)
            while s < target:
                row = rule30_step(row)
                s += 1
            A = (row << 1) & row
            lo = 2 * (s - t0 + 1)
            if (A >> (T + lo)) & 1:
                return {"ok": False, "lo_live": True, "W": W, "q": q}
            nA = nE = 0
            for j in range(U):
                if not mer_one(j):
                    continue
                r = lo + 2 * j
                if ((A >> (T + r)) & 1) == 0:
                    continue
                nA ^= 1
                if j != U - 1:
                    nE ^= 1
            hx ^= nA
            ex ^= nE
            n_ok += 1
            n_lo_dead += 1
        if ex != 0 or hx != (Q & 1):
            return {"ok": False, "W": W, "hx": hx, "ex": ex, "Q": Q}
        rows[f"{W // U}U"] = {
            "hit_xor": hx,
            "extras_xor": ex,
            "Qmod2": Q & 1,
        }
    return {
        "ok": n_ok == 7 and n_lo_dead == 7,
        "n_ok": n_ok,
        "n_lo_dead": n_lo_dead,
        "rows": rows,
    }


def killed_lo_all_odd() -> dict:
    """AND at lo is not dead on all odd s: k=4, W=8U, delta=17."""
    k = 4
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    delta = 17
    s = t0 + delta
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    A = (row << 1) & row
    lo = 2 * (delta + 1)
    on = ((A >> (T + lo)) & 1) == 1
    hits = (1, 1 + 2 * U)
    ok = on and delta not in hits and delta % 2 == 1
    return {"ok": ok, "k": k, "W": "8U", "delta": delta, "AND_lo": int(on)}


def killed_extras_empty() -> dict:
    """Extras are not empty at k=4: W=8U, q=0, {6,7}."""
    k = 4
    U = 1 << k
    sc = scan_hits(k, 8 * U)
    extras = sc["extras_rows"][0]
    ok = extras == [6, 7]
    return {"ok": ok, "k": k, "W": "8U", "q": 0, "extras": extras}


def killed_extras_xor_all_k() -> dict:
    """Extras XOR does not vanish for all k: k=2, W=8U."""
    sc = scan_hits(2, 8 * 4)
    ok = sc["ex"] == 1
    return {"ok": ok, "k": 2, "W": "8U", "extras_xor": sc["ex"]}


def prefixes() -> dict:
    gs = json.loads(GS_JSON.read_text())
    gq = json.loads(GQ_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    ok = (
        gs["checks"]["all_ok"]
        and gq["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and gs["verdict"]["all_W_hit_cone_XOR_eq_extras_XOR_xor_Qmod2"]
        == "LEMMA"
        and gq["verdict"]["AND_at_j_U_minus_1_live_on_hits"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_XOR_eq_1_iff_W_eq_4U"] == "LEMMA"
        and gs["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, pk: dict, ko: dict, ke: dict, kx: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pk["ok"] and ko["ok"] and ke["ok"] and kx["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pk = packed_k4()
    ko = killed_lo_all_odd()
    ke = killed_extras_empty()
    kx = killed_extras_xor_all_k()
    pref = prefixes()
    checks = self_checks(c20, pk, ko, ke, kx, pref)
    dump = {
        "cycle": "GT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "packed_k4": {k: pk[k] for k in pk if k != "ok"},
        "killed_lo_all_odd": {k: ko[k] for k in ko if k != "ok"},
        "killed_extras_empty": {k: ke[k] for k in ke if k != "ok"},
        "killed_extras_xor_all_k": {k: kx[k] for k in kx if k != "ok"},
        "lemmas": {
            "k4_AND_lo_dead_on_covering_hits": True,
            "k4_extras_XOR_eq_0": True,
            "k4_hit_cone_XOR_eq_Qmod2": True,
            "k4_AND_lo_dead_on_all_odd_s": False,
            "k4_extras_empty": False,
            "extras_XOR_eq_0_all_k": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "k4_AND_lo_dead_on_covering_hits": "LEMMA",
            "k4_extras_XOR_eq_0": "LEMMA",
            "k4_hit_cone_XOR_eq_Qmod2": "LEMMA",
            "k4_AND_lo_dead_on_all_odd_s": "KILLED",
            "k4_extras_empty": "KILLED",
            "extras_XOR_eq_0_all_k": "KILLED",
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
    print("packed_k4", dump["packed_k4"])
    print("killed_lo_all_odd", dump["killed_lo_all_odd"])
    print("killed_extras_empty", dump["killed_extras_empty"])
    print("killed_extras_xor_all_k", dump["killed_extras_xor_all_k"])


if __name__ == "__main__":
    main()
