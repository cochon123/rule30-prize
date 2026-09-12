#!/usr/bin/env python3
"""Cycle HC: in-support remainder Green is GX/GY from rho=T-p.

On the covering windows (T,t0,Q)=(18U,10U,4), (10U,6U,2), (6U,4U,1)
the in-support remainder to T uses the same clock n=UQ-t-1. Odd-s
even-rho Green is G(n,rho/2); odd-rho Green is 0. Even-s is the GY
coboundary. Odd-s G*AND XOR is AND on those G=1 even columns, not
J_tail (k=2: 0 vs 1). Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_hc.py --certify
Dump: research/cycle_hc.json
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
from cycle_gn import mer_one
from cycle_gu import odd_clock
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HB_JSON = Path(__file__).resolve().parent / "cycle_hb.json"
GX_JSON = Path(__file__).resolve().parent / "cycle_gx.json"
GY_JSON = Path(__file__).resolve().parent / "cycle_gy.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"

# Covering in-support remainders on the unified time windows.
WINDOWS = (("tail", 18, 10, 4), ("mid10", 10, 6, 2), ("j6slice", 6, 4, 1))


def _walk_in(k: int, Tmul: int, t0mul: int, Q: int) -> dict:
    U = 1 << k
    T, t0 = Tmul * U, t0mul * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    xor_direct = xor_j = xor_even = 0
    n_odd_r_g1 = n_g0and = 0
    n_odd = n_even = 0
    s = t0
    while s < T:
        A = (row << 1) & row
        t = (s - t0) // 2
        n = odd_clock(t, U, Q)
        m = T - s - 1
        lo = max(2 * s - T + 2, 0)
        if s % 2:
            for p in range(lo, T + 1):
                rho = T - p
                g = G(m, rho)
                on = (A >> p) & 1
                if rho % 2:
                    if g:
                        n_odd_r_g1 += 1
                    continue
                j = rho // 2
                gj = G(n, j)
                if g != gj:
                    return {
                        "ok": False,
                        "k": k,
                        "s": s,
                        "p": p,
                        "g": g,
                        "want": gj,
                    }
                n_odd += 1
                if on and g:
                    xor_direct ^= 1
                if on and gj:
                    xor_j ^= 1
                if on and not gj:
                    n_g0and += 1
        else:
            for p in range(lo, T + 1):
                rho = T - p
                g = G(m, rho)
                on = (A >> p) & 1
                if rho % 2 == 0:
                    j = rho // 2
                    want = G(n, j) ^ G(n, j - 1)
                else:
                    j = (rho - 1) // 2
                    want = G(n, j)
                if g != want:
                    return {
                        "ok": False,
                        "even": True,
                        "k": k,
                        "s": s,
                        "p": p,
                        "g": g,
                        "want": want,
                    }
                n_even += 1
                if on and g:
                    xor_even ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_odd_r_g1 == 0 and xor_direct == xor_j,
        "xor_odd": xor_direct,
        "xor_j": xor_j,
        "xor_even": xor_even,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_g0and": n_g0and,
        "n_odd_r_g1": n_odd_r_g1,
    }


def in_support_j() -> dict:
    """GX/GY in rho=T-p; odd-s XOR = AND on G(n,j)=1. k<=6, 21 windows."""
    n_ok = 0
    n_odd = n_even = n_g0 = 0
    rows = {}
    for k in range(0, 7):
        krow = {}
        for name, Tmul, t0mul, Q in WINDOWS:
            w = _walk_in(k, Tmul, t0mul, Q)
            if not w.get("ok"):
                return w
            n_ok += 1
            n_odd += w["n_odd"]
            n_even += w["n_even"]
            n_g0 += w["n_g0and"]
            krow[name] = {
                "xor_odd": w["xor_odd"],
                "xor_even": w["xor_even"],
                "n_g0and": w["n_g0and"],
            }
        rows[str(k)] = krow
    return {
        "ok": n_ok == 21,
        "n_ok": n_ok,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_g0and": n_g0,
        "rows": rows,
    }


def killed_mer_one() -> dict:
    """Off-hit Green is not mer_one(j): k=2, tail s=43, j=3."""
    k = 2
    U = 1 << k
    T, t0 = 18 * U, 10 * U
    s, p = 43, 66
    t = (s - t0) // 2
    n = odd_clock(t, U, 4)
    j = (T - p) // 2
    g = G(T - s - 1, T - p)
    mer = mer_one(j)
    ok = g == 0 and mer == 1 and n != U - 1
    return {"ok": ok, "k": k, "s": s, "j": j, "G": g, "mer_one": mer, "n": n}


def killed_odd_s_eq_Jtail() -> dict:
    """Odd-s in-support XOR is not J_tail: k=2, 0 vs 1."""
    w = _walk_in(2, 18, 10, 4)
    fr = json.loads(FR_JSON.read_text())
    jtail = fr["split"]["rows"]["2"]["Jtail"]
    ok = w["xor_odd"] == 0 and jtail == 1
    return {"ok": ok, "k": 2, "xor_odd": w["xor_odd"], "Jtail": jtail}


def killed_even_s_0() -> dict:
    """Even-s in-support XOR is not identically 0: k=2, tail."""
    w = _walk_in(2, 18, 10, 4)
    ok = w["xor_even"] == 1
    return {"ok": ok, "k": 2, "xor_even": w["xor_even"]}


def prefixes() -> dict:
    hb = json.loads(HB_JSON.read_text())
    gx = json.loads(GX_JSON.read_text())
    gy = json.loads(GY_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        hb["checks"]["all_ok"]
        and gx["checks"]["all_ok"]
        and gy["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and hb["verdict"]["Delta16_R_eq_W16U_band_xor"] == "LEMMA"
        and gx["verdict"]["odd_s_jth_even_r_G_eq_G_n_j"] == "LEMMA"
        and gy["verdict"]["even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1"]
        == "LEMMA"
        and hb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ins: dict, km: dict, kj: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ins["ok"] and km["ok"] and kj["ok"] and ke["ok"] and pref["ok"]
    fr = json.loads(FR_JSON.read_text())
    for k in ("2", "3", "4", "5"):
        tail = ins["rows"][k]["tail"]
        tot = tail["xor_odd"] ^ tail["xor_even"]
        assert tot == fr["split"]["rows"][k]["Jtail"]
        mid = ins["rows"][k]["mid10"]
        assert (mid["xor_odd"] ^ mid["xor_even"]) == fr["split"]["rows"][k][
            "Jmid10"
        ]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ins = in_support_j()
    km = killed_mer_one()
    kj = killed_odd_s_eq_Jtail()
    ke = killed_even_s_0()
    pref = prefixes()
    checks = self_checks(c20, ins, km, kj, ke, pref)
    dump = {
        "cycle": "HC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "in_support_j": {k: ins[k] for k in ins if k != "ok"},
        "killed_mer_one": {k: km[k] for k in km if k != "ok"},
        "killed_odd_s_eq_Jtail": {k: kj[k] for k in kj if k != "ok"},
        "killed_even_s_0": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "in_support_odd_s_even_rho_G_eq_G_n_j": True,
            "in_support_odd_s_odd_rho_G_eq_0": True,
            "in_support_even_s_GY_coboundary": True,
            "in_support_odd_s_XOR_eq_AND_on_G_n_j_eq_1": True,
            "in_support_eq_mer_one": False,
            "odd_s_XOR_eq_Jtail": False,
            "even_s_XOR_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "in_support_odd_s_even_rho_G_eq_G_n_j": "LEMMA",
            "in_support_odd_s_odd_rho_G_eq_0": "LEMMA",
            "in_support_even_s_GY_coboundary": "LEMMA",
            "in_support_odd_s_XOR_eq_AND_on_G_n_j_eq_1": "LEMMA",
            "in_support_eq_mer_one": "KILLED",
            "odd_s_XOR_eq_Jtail": "KILLED",
            "even_s_XOR_eq_0": "KILLED",
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
        "in_support_j n_ok",
        dump["in_support_j"]["n_ok"],
        "n_odd",
        dump["in_support_j"]["n_odd"],
        "n_even",
        dump["in_support_j"]["n_even"],
        "n_g0and",
        dump["in_support_j"]["n_g0and"],
    )
    print("killed_mer_one", dump["killed_mer_one"])
    print("killed_odd_s_eq_Jtail", dump["killed_odd_s_eq_Jtail"])
    print("killed_even_s_0", dump["killed_even_s_0"])


if __name__ == "__main__":
    main()
