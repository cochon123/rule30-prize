#!/usr/bin/env python3
"""Cycle GS: all covering W, hit-cone XOR = extras XOR XOR (Q mod 2).

Cycle GR was the even-Q (W=8U) case. Cone-hi AND is live on every
hit (GQ), so hi XOR = Q mod 2 (GG) and the mer_one AND XOR over hits
is extras XOR XOR (Q mod 2). Equals extras XOR iff Q is even. On W=4U
extras are still only lo through k=4, not at k=5. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gs.py --certify
Dump: research/cycle_gs.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GR_JSON = Path(__file__).resolve().parent / "cycle_gr.json"
GQ_JSON = Path(__file__).resolve().parent / "cycle_gq.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"


def scan_hits(k: int, W: int) -> dict:
    """XOR of mer_one AND / extras / lo over Cycle GG hits."""
    U = 1 << k
    T = 2 * U + W
    t0 = T - W // 2
    Q = W // (4 * U)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    s = t0
    hx = ex = lx = 0
    extras_rows = []
    for q in range(Q):
        target = t0 + 1 + q * (2 * U)
        while s < target:
            row = rule30_step(row)
            s += 1
        A = (row << 1) & row
        lo = 2 * (s - t0 + 1)
        extras = []
        nA = nE = nL = 0
        for j in range(U):
            if not mer_one(j):
                continue
            r = lo + 2 * j
            if ((A >> (T + r)) & 1) == 0:
                continue
            nA ^= 1
            if j != U - 1:
                nE ^= 1
                if j != 0:
                    extras.append(j)
            if j == 0:
                nL ^= 1
        hx ^= nA
        ex ^= nE
        lx ^= nL
        extras_rows.append(extras)
    return {
        "hx": hx,
        "ex": ex,
        "lx": lx,
        "Q": Q,
        "extras_rows": extras_rows,
    }


def all_w_xor() -> dict:
    """hit-cone XOR = extras XOR XOR (Q mod 2) on every covering W."""
    n_ok = 0
    rows = {}
    for k in range(0, 7):
        U = 1 << k
        krow = {}
        for W in (4 * U, 8 * U, 16 * U):
            sc = scan_hits(k, W)
            if sc["hx"] != (sc["ex"] ^ (sc["Q"] & 1)):
                return {
                    "ok": False,
                    "k": k,
                    "W": W,
                    "hx": sc["hx"],
                    "ex": sc["ex"],
                    "Q": sc["Q"],
                }
            krow[f"{W // U}U"] = {
                "hit_xor": sc["hx"],
                "extras_xor": sc["ex"],
                "Qmod2": sc["Q"] & 1,
            }
            n_ok += 1
        rows[str(k)] = krow
    return {"ok": n_ok == 21, "n_ok": n_ok, "rows": rows}


def w4u_extras_lo() -> dict:
    """On W=4U, extras subseteq {0} through k=4."""
    n_ok = 0
    for k in range(0, 5):
        U = 1 << k
        sc = scan_hits(k, 4 * U)
        if any(ex for ex in sc["extras_rows"]):
            return {"ok": False, "k": k, "extras": sc["extras_rows"]}
        n_ok += 1
    return {"ok": n_ok == 5, "n_ok": n_ok}


def killed_eq_extras_w4() -> dict:
    """Hit-cone XOR is not extras XOR on W=4U: k=0, hx=1, ex=0."""
    sc = scan_hits(0, 4)
    ok = sc["hx"] == 1 and sc["ex"] == 0 and sc["Q"] == 1
    return {"ok": ok, "k": 0, "W": "4U", "hit_xor": sc["hx"], "extras_xor": sc["ex"]}


def killed_eq_lo_qmod() -> dict:
    """Not lo XOR XOR (Q mod 2) for all k: k=5, W=8U, lo_xor=1, hx=0."""
    k = 5
    U = 1 << k
    sc = scan_hits(k, 8 * U)
    ok = sc["hx"] == 0 and sc["lx"] == 1 and (sc["Q"] & 1) == 0
    ok = ok and sc["hx"] != (sc["lx"] ^ (sc["Q"] & 1))
    return {
        "ok": ok,
        "k": k,
        "W": "8U",
        "hit_xor": sc["hx"],
        "lo_xor": sc["lx"],
    }


def killed_w4u_extras_k5() -> dict:
    """W=4U extras are not only lo at k=5: {9,12}."""
    k = 5
    U = 1 << k
    sc = scan_hits(k, 4 * U)
    extras = sc["extras_rows"][0]
    ok = extras == [9, 12]
    return {"ok": ok, "k": k, "W": "4U", "extras": extras}


def prefixes() -> dict:
    gr = json.loads(GR_JSON.read_text())
    gq = json.loads(GQ_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    ok = (
        gr["checks"]["all_ok"]
        and gq["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and gr["verdict"]["W8U_hit_cone_XOR_eq_extras_XOR"] == "LEMMA"
        and gq["verdict"]["AND_at_j_U_minus_1_live_on_hits"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_XOR_eq_1_iff_W_eq_4U"] == "LEMMA"
        and gr["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, aw: dict, w4: dict, ke: dict, kl: dict, k5: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert aw["ok"] and w4["ok"]
    assert ke["ok"] and kl["ok"] and k5["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    aw = all_w_xor()
    w4 = w4u_extras_lo()
    ke = killed_eq_extras_w4()
    kl = killed_eq_lo_qmod()
    k5 = killed_w4u_extras_k5()
    pref = prefixes()
    checks = self_checks(c20, aw, w4, ke, kl, k5, pref)
    dump = {
        "cycle": "GS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "all_w_xor": {k: aw[k] for k in aw if k != "ok"},
        "w4u_extras_lo": {k: w4[k] for k in w4 if k != "ok"},
        "killed_eq_extras_w4": {k: ke[k] for k in ke if k != "ok"},
        "killed_eq_lo_qmod": {k: kl[k] for k in kl if k != "ok"},
        "killed_w4u_extras_k5": {k: k5[k] for k in k5 if k != "ok"},
        "lemmas": {
            "all_W_hit_cone_XOR_eq_extras_XOR_xor_Qmod2": True,
            "W4U_extras_subseteq_0_through_k4": True,
            "hit_cone_XOR_eq_extras_XOR_on_W4U": False,
            "hit_cone_XOR_eq_lo_XOR_xor_Qmod2_all_k": False,
            "W4U_extras_only_lo_at_k5": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "all_W_hit_cone_XOR_eq_extras_XOR_xor_Qmod2": "LEMMA",
            "W4U_extras_subseteq_0_through_k4": "LEMMA",
            "hit_cone_XOR_eq_extras_XOR_on_W4U": "KILLED",
            "hit_cone_XOR_eq_lo_XOR_xor_Qmod2_all_k": "KILLED",
            "W4U_extras_only_lo_at_k5": "KILLED",
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
    print("all_w_xor n_ok", dump["all_w_xor"]["n_ok"])
    print("killed_eq_extras_w4", dump["killed_eq_extras_w4"])
    print("killed_eq_lo_qmod", dump["killed_eq_lo_qmod"])
    print("killed_w4u_extras_k5", dump["killed_w4u_extras_k5"])


if __name__ == "__main__":
    main()
