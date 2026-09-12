#!/usr/bin/env python3
"""Cycle HD: even-s in-support XOR is coboundary-1 even AND plus G=1 odd AND.

Cycle HC's GY index. AND can fire on coboundary-0 even rho and on G=0
odd rho but those contribute 0. Even-s XOR is not J_tail (k=5: 0 vs 1)
and is not the even-rho slice alone (k=2: odd-rho XOR=1). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hd.py --certify
Dump: research/cycle_hd.json
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
from cycle_hc import WINDOWS
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HC_JSON = Path(__file__).resolve().parent / "cycle_hc.json"
HA_JSON = Path(__file__).resolve().parent / "cycle_ha.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"
GY_JSON = Path(__file__).resolve().parent / "cycle_gy.json"


def _walk_even_in(k: int, Tmul: int, t0mul: int, Q: int) -> dict:
    U = 1 << k
    T, t0 = Tmul * U, t0mul * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    xor_direct = xor_j = xor_even_r = xor_odd_r = 0
    n_cob0and = n_odd_r_g1and = n_odd_r_g0and = 0
    s = t0
    while s < T:
        A = (row << 1) & row
        if s % 2 == 0:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            m = T - s - 1
            lo = max(2 * s - T + 2, 0)
            for p in range(lo, T + 1):
                rho = T - p
                on = (A >> p) & 1
                g = G(m, rho)
                if on and g:
                    xor_direct ^= 1
                if rho % 2 == 0:
                    j = rho // 2
                    cob = G(n, j) ^ G(n, j - 1)
                    if on and cob:
                        xor_j ^= 1
                        xor_even_r ^= 1
                    if on and not cob:
                        n_cob0and += 1
                else:
                    j = (rho - 1) // 2
                    gj = G(n, j)
                    if on and gj:
                        xor_j ^= 1
                        xor_odd_r ^= 1
                        n_odd_r_g1and += 1
                    if on and not gj:
                        n_odd_r_g0and += 1
        row = rule30_step(row)
        s += 1
    return {
        "xor_even": xor_direct,
        "xor_j": xor_j,
        "xor_even_r": xor_even_r,
        "xor_odd_r": xor_odd_r,
        "n_cob0and": n_cob0and,
        "n_odd_r_g1and": n_odd_r_g1and,
        "n_odd_r_g0and": n_odd_r_g0and,
    }


def even_s_in() -> dict:
    """even-s in-support XOR = cob1 even AND XOR G=1 odd AND. k<=6."""
    n_ok = 0
    n_cob0 = n_odd_g1 = 0
    rows = {}
    for k in range(0, 7):
        krow = {}
        for name, Tmul, t0mul, Q in WINDOWS:
            w = _walk_even_in(k, Tmul, t0mul, Q)
            if w["xor_even"] != w["xor_j"]:
                return {"ok": False, "k": k, "name": name, **w}
            n_ok += 1
            n_cob0 += w["n_cob0and"]
            n_odd_g1 += w["n_odd_r_g1and"]
            krow[name] = {
                "xor_even": w["xor_even"],
                "xor_even_r": w["xor_even_r"],
                "xor_odd_r": w["xor_odd_r"],
                "n_cob0and": w["n_cob0and"],
                "n_odd_r_g1and": w["n_odd_r_g1and"],
                "n_odd_r_g0and": w["n_odd_r_g0and"],
            }
        rows[str(k)] = krow
    return {
        "ok": n_ok == 21,
        "n_ok": n_ok,
        "n_cob0and": n_cob0,
        "n_odd_r_g1and": n_odd_g1,
        "rows": rows,
    }


def killed_and_only_cob1() -> dict:
    """AND is not only on coboundary-1 even rho: k=1, tail."""
    w = _walk_even_in(1, 18, 10, 4)
    ok = w["n_cob0and"] > 0
    return {"ok": ok, "k": 1, "window": "tail", "n_cob0and": w["n_cob0and"]}


def killed_even_r_only() -> dict:
    """Even-s XOR is not the even-rho coboundary slice: k=2, tail."""
    w = _walk_even_in(2, 18, 10, 4)
    ok = w["xor_even_r"] != w["xor_even"] and w["xor_odd_r"] == 1
    return {
        "ok": ok,
        "k": 2,
        "window": "tail",
        "xor_even": w["xor_even"],
        "xor_even_r": w["xor_even_r"],
        "xor_odd_r": w["xor_odd_r"],
    }


def killed_even_s_eq_Jtail() -> dict:
    """Even-s XOR is not J_tail: k=5, 0 vs 1."""
    w = _walk_even_in(5, 18, 10, 4)
    fr = json.loads(FR_JSON.read_text())
    jtail = fr["split"]["rows"]["5"]["Jtail"]
    ok = w["xor_even"] == 0 and jtail == 1
    return {"ok": ok, "k": 5, "xor_even": w["xor_even"], "Jtail": jtail}


def prefixes() -> dict:
    hc = json.loads(HC_JSON.read_text())
    ha = json.loads(HA_JSON.read_text())
    gy = json.loads(GY_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        hc["checks"]["all_ok"]
        and ha["checks"]["all_ok"]
        and gy["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and hc["verdict"]["in_support_odd_s_XOR_eq_AND_on_G_n_j_eq_1"]
        == "LEMMA"
        and ha["verdict"]["even_s_band_XOR_eq_cob1_even_AND_xor_G1_odd_AND"]
        == "LEMMA"
        and gy["verdict"]["even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1"]
        == "LEMMA"
        and hc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ev: dict, ka: dict, ke: dict, kj: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ev["ok"] and ka["ok"] and ke["ok"] and kj["ok"] and pref["ok"]
    hc = json.loads(HC_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    for k in ("2", "3", "4", "5"):
        even = ev["rows"][k]["tail"]["xor_even"]
        odd = hc["in_support_j"]["rows"][k]["tail"]["xor_odd"]
        assert even == hc["in_support_j"]["rows"][k]["tail"]["xor_even"]
        assert (odd ^ even) == fr["split"]["rows"][k]["Jtail"]
        even_m = ev["rows"][k]["mid10"]["xor_even"]
        odd_m = hc["in_support_j"]["rows"][k]["mid10"]["xor_odd"]
        assert (odd_m ^ even_m) == fr["split"]["rows"][k]["Jmid10"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ev = even_s_in()
    ka = killed_and_only_cob1()
    ke = killed_even_r_only()
    kj = killed_even_s_eq_Jtail()
    pref = prefixes()
    checks = self_checks(c20, ev, ka, ke, kj, pref)
    dump = {
        "cycle": "HD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_s_in": {k: ev[k] for k in ev if k != "ok"},
        "killed_and_only_cob1": {k: ka[k] for k in ka if k != "ok"},
        "killed_even_r_only": {k: ke[k] for k in ke if k != "ok"},
        "killed_even_s_eq_Jtail": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "even_s_in_support_XOR_eq_cob1_even_AND_xor_G1_odd_AND": True,
            "AND_only_on_coboundary_1": False,
            "even_s_XOR_eq_even_rho_slice": False,
            "even_s_XOR_eq_Jtail": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_in_support_XOR_eq_cob1_even_AND_xor_G1_odd_AND": "LEMMA",
            "AND_only_on_coboundary_1": "KILLED",
            "even_s_XOR_eq_even_rho_slice": "KILLED",
            "even_s_XOR_eq_Jtail": "KILLED",
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
        "even_s_in n_ok",
        dump["even_s_in"]["n_ok"],
        "n_cob0and",
        dump["even_s_in"]["n_cob0and"],
        "n_odd_r_g1and",
        dump["even_s_in"]["n_odd_r_g1and"],
    )
    print("killed_and_only_cob1", dump["killed_and_only_cob1"])
    print("killed_even_r_only", dump["killed_even_r_only"])
    print("killed_even_s_eq_Jtail", dump["killed_even_s_eq_Jtail"])


if __name__ == "__main__":
    main()
