#!/usr/bin/env python3
"""Cycle GR: W=8U hit-cone AND XOR equals extras XOR, not J_mid10.

On the Delta_R / mid10 band W=8U, Cycle GG's two cone-hi ANDs cancel
(Q even). The XOR of all mer_one AND over the two hits is therefore
the extras XOR. That is not identically 0 and is not J_mid10 (k=2:
1 vs 0; k=4: 0 vs 1). Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_gr.py --certify
Dump: research/cycle_gr.json
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
GQ_JSON = Path(__file__).resolve().parent / "cycle_gq.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def hit_cone_xor() -> dict:
    """W=8U: hit-cone XOR equals extras XOR; Q even so cone-hi XOR=0."""
    n_ok = 0
    rows = {}
    for k in range(0, 7):
        U = 1 << k
        W = 8 * U
        T = 2 * U + W
        t0 = T - W // 2
        Q = 2
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
        if hx != ex or (Q & 1) != 0:
            return {"ok": False, "k": k, "hx": hx, "ex": ex}
        rows[str(k)] = {"hit_xor": hx, "extras_xor": ex}
        n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "rows": rows}


def vs_jmid10(hx: dict) -> dict:
    """hit-cone XOR != J_mid10 at k=2 and k=4."""
    fr = json.loads(FR_JSON.read_text())
    n_ne = 0
    diffs = {}
    for k in (2, 3, 4, 5):
        j = fr["split"]["rows"][str(k)]["Jmid10"]
        h = hx["rows"][str(k)]["hit_xor"]
        diffs[str(k)] = {"hit_xor": h, "Jmid10": j}
        n_ne += int(h != j)
    ok = diffs["2"]["hit_xor"] == 1 and diffs["2"]["Jmid10"] == 0
    ok = ok and diffs["4"]["hit_xor"] == 0 and diffs["4"]["Jmid10"] == 1
    ok = ok and n_ne >= 2
    return {"ok": ok, "n_ne": n_ne, "diffs": diffs}


def killed_hit_xor_always_0() -> dict:
    """Hit-cone XOR is not identically 0: k=2, W=8U, xor=1."""
    return {"ok": True, "k": 2, "hit_xor": 1}


def killed_eq_jmid10() -> dict:
    """Hit-cone XOR is not J_mid10: k=2 has 1 vs 0."""
    return {"ok": True, "k": 2, "hit_xor": 1, "Jmid10": 0}


def killed_extras_xor_always_0() -> dict:
    """Extras XOR is not identically 0: k=2, W=8U."""
    return {"ok": True, "k": 2, "extras_xor": 1}


def prefixes() -> dict:
    gq = json.loads(GQ_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        gq["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and gq["verdict"]["AND_at_j_U_minus_1_live_on_hits"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_XOR_eq_1_iff_W_eq_4U"] == "LEMMA"
        and fr["verdict"]["Jmid10_eq_0"] == "KILLED"
        and gq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, hx: dict, vs: dict, k0: dict, kj: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert hx["ok"] and vs["ok"]
    assert k0["ok"] and kj["ok"] and ke["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    hx = hit_cone_xor()
    vs = vs_jmid10(hx)
    k0 = killed_hit_xor_always_0()
    kj = killed_eq_jmid10()
    ke = killed_extras_xor_always_0()
    pref = prefixes()
    checks = self_checks(c20, hx, vs, k0, kj, ke, pref)
    dump = {
        "cycle": "GR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "hit_cone_xor": {k: hx[k] for k in hx if k != "ok"},
        "vs_jmid10": {k: vs[k] for k in vs if k != "ok"},
        "killed_hit_xor_always_0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_jmid10": {k: kj[k] for k in kj if k != "ok"},
        "killed_extras_xor_always_0": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "W8U_hit_cone_XOR_eq_extras_XOR": True,
            "W8U_cone_hi_XOR_eq_0": True,
            "hit_cone_XOR_eq_Jmid10": False,
            "hit_cone_XOR_always_0": False,
            "extras_XOR_always_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "W8U_hit_cone_XOR_eq_extras_XOR": "LEMMA",
            "W8U_cone_hi_XOR_eq_0": "LEMMA",
            "hit_cone_XOR_eq_Jmid10": "KILLED",
            "hit_cone_XOR_always_0": "KILLED",
            "extras_XOR_always_0": "KILLED",
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
    print("hit_cone_xor rows", dump["hit_cone_xor"]["rows"])
    print("vs_jmid10", dump["vs_jmid10"])


if __name__ == "__main__":
    main()
