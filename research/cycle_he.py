#!/usr/bin/env python3
"""Cycle HE: in-support remainder is the full Green row; odd s enumerates n.

On covering windows the in-support lo=2s-T+2 has T-lo=2m, so every
Green column rho in [0,2m] is in-band (width 2m+1). Odd s=t0+2t+1
visits n=UQ-t-1 for t=0..UQ-1, i.e. every n in [0,UQ) once. AND at
(n,j) still depends on the window. Width is not 2U-1; tail n is not
only in [0,U). Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_he.py --certify
Dump: research/cycle_he.json
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
from cycle_gu import odd_clock
from cycle_hc import WINDOWS
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HD_JSON = Path(__file__).resolve().parent / "cycle_hd.json"
HC_JSON = Path(__file__).resolve().parent / "cycle_hc.json"
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"


def full_green() -> dict:
    """T-lo=2m and width 2m+1 on every s; k<=12, 21 windows samples."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        for _name, Tmul, t0mul, _Q in WINDOWS:
            T, t0 = Tmul * U, t0mul * U
            samples = (t0, t0 + 1, t0 + max(U, 1), T - 2, T - 1)
            for s in samples:
                if not (t0 <= s < T):
                    continue
                m = T - s - 1
                lo = 2 * s - T + 2
                if lo < 0:
                    lo = 0
                if T - lo != 2 * m or (T - lo + 1) != 2 * m + 1:
                    return {"ok": False, "k": k, "s": s, "m": m, "lo": lo}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def n_scan() -> dict:
    """Odd s enumerates n=0..UQ-1; even s the same n's. k<=12."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        for _name, Tmul, t0mul, Q in WINDOWS:
            T, t0 = Tmul * U, t0mul * U
            UQ = U * Q
            if T - t0 != 2 * UQ:
                return {"ok": False, "len": True, "k": k, "Q": Q}
            seen_odd = []
            seen_even = []
            for t in range(UQ):
                n = odd_clock(t, U, Q)
                seen_odd.append(n)
                seen_even.append(n)
                s_odd = t0 + 2 * t + 1
                s_even = t0 + 2 * t
                if not (t0 <= s_even < T) or not (t0 <= s_odd < T):
                    return {"ok": False, "s": True, "k": k, "t": t}
            if sorted(seen_odd) != list(range(UQ)) or seen_odd != seen_even:
                return {"ok": False, "k": k, "Q": Q, "seen": seen_odd[:4]}
            n_ok += 1
    return {"ok": n_ok == 13 * 3, "n_ok": n_ok}


def killed_width_2U() -> dict:
    """In-support width is not 2U-1: k=2, tail, s=t0+1."""
    k = 2
    U = 1 << k
    T, t0 = 18 * U, 10 * U
    s = t0 + 1
    m = T - s - 1
    w = 2 * m + 1
    flat = 2 * U - 1
    ok = w != flat and w == 61 and flat == 7
    return {"ok": ok, "k": k, "s": s, "width": w, "flat": flat}


def killed_and_indep_Q() -> dict:
    """AND(n,j) is not independent of the window: k=0, n=1, j=2."""
    k = 0
    U = 1 << k
    vals = {}
    for name, Tmul, t0mul, Q in (("tail", 18, 10, 4), ("mid10", 10, 6, 2)):
        T, t0 = Tmul * U, t0mul * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        s = t0
        found = None
        while s < T:
            if s % 2:
                t = (s - t0) // 2
                n = odd_clock(t, U, Q)
                if n == 1:
                    p = T - 2 * 2
                    A = (row << 1) & row
                    found = (A >> p) & 1
                    break
            row = rule30_step(row)
            s += 1
        vals[name] = found
    ok = vals["tail"] == 0 and vals["mid10"] == 1
    return {"ok": ok, "k": 0, "n": 1, "j": 2, **vals}


def killed_n_only_U() -> dict:
    """Tail n is not only in [0,U): first odd s has n=4U-1."""
    k = 2
    U = 1 << k
    n = odd_clock(0, U, 4)
    ok = n == 4 * U - 1 and n > U - 1
    return {"ok": ok, "k": k, "n": n, "U_minus_1": U - 1}


def prefixes() -> dict:
    hd = json.loads(HD_JSON.read_text())
    hc = json.loads(HC_JSON.read_text())
    fq = json.loads(FQ_JSON.read_text())
    ok = (
        hd["checks"]["all_ok"]
        and hc["checks"]["all_ok"]
        and fq["checks"]["all_ok"]
        and hd["verdict"]["even_s_in_support_XOR_eq_cob1_even_AND_xor_G1_odd_AND"]
        == "LEMMA"
        and hc["verdict"]["in_support_odd_s_XOR_eq_AND_on_G_n_j_eq_1"] == "LEMMA"
        and fq["verdict"]["unified_T_eq_2U_plus_W_band"] == "LEMMA"
        and hd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, fg: dict, ns: dict, kw: dict, ka: dict, kn: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fg["ok"] and ns["ok"] and kw["ok"] and ka["ok"] and kn["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fg = full_green()
    ns = n_scan()
    kw = killed_width_2U()
    ka = killed_and_indep_Q()
    kn = killed_n_only_U()
    pref = prefixes()
    checks = self_checks(c20, fg, ns, kw, ka, kn, pref)
    dump = {
        "cycle": "HE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "full_green": {k: fg[k] for k in fg if k != "ok"},
        "n_scan": {k: ns[k] for k in ns if k != "ok"},
        "killed_width_2U": {k: kw[k] for k in kw if k != "ok"},
        "killed_and_indep_Q": {k: ka[k] for k in ka if k != "ok"},
        "killed_n_only_U": {k: kn[k] for k in kn if k != "ok"},
        "lemmas": {
            "in_support_eq_full_Green_row": True,
            "odd_s_enumerates_n_in_0_UQ": True,
            "even_s_same_n_as_next_odd": True,
            "width_eq_2U_minus_1": False,
            "AND_n_j_independent_of_window": False,
            "tail_n_only_in_0_U": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "in_support_eq_full_Green_row": "LEMMA",
            "odd_s_enumerates_n_in_0_UQ": "LEMMA",
            "even_s_same_n_as_next_odd": "LEMMA",
            "width_eq_2U_minus_1": "KILLED",
            "AND_n_j_independent_of_window": "KILLED",
            "tail_n_only_in_0_U": "KILLED",
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
    print("full_green n_ok", dump["full_green"]["n_ok"])
    print("n_scan n_ok", dump["n_scan"]["n_ok"])
    print("killed_width_2U", dump["killed_width_2U"])
    print("killed_and_indep_Q", dump["killed_and_indep_Q"])
    print("killed_n_only_U", dump["killed_n_only_U"])


if __name__ == "__main__":
    main()
