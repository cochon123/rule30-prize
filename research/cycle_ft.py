#!/usr/bin/env python3
"""Cycle FT: Green support [lo,W] is palindrome-symmetric about s-2U+1.

Cycle FS palindrome G(m,d)=G(m,2m-d) acts on r by r |-> 2mu-r with
mu=s-2U+1. On the unified T=2U+W band this swaps the Green endpoints:
2mu-W = lo = 2(s-t0+1) and 2mu-lo = W. So the Green interval [lo,W]
is palindrome-symmetric. The light-cone cut [lo, min(2s-T,W)] is not:
before clip, 2mu-lo = W != hi. Kills: cone-band palindrome-symmetric;
midpoint s-U. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ft.py --certify
Dump: research/cycle_ft.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def green_sym() -> dict:
    """2*mu-W = lo and 2*mu-lo = W on the unified band."""
    n_ok = 0
    n_cone_fail = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in (t0, t0 + max(U, 1), clip - 1, clip, clip + max(U, 1), T - 1):
                if not (t0 <= s < T):
                    continue
                mu = s - 2 * U + 1
                lo = 2 * (s - t0 + 1)
                hi = min(2 * s - T, W)
                if 2 * mu - W != lo or 2 * mu - lo != W:
                    return {"ok": False, "k": k, "W": W, "s": s, "mu": mu, "lo": lo}
                if not (2 * mu - hi == lo and 2 * mu - lo == hi):
                    n_cone_fail += 1
                n_ok += 1
    return {
        "ok": n_ok > 0 and n_cone_fail > 0,
        "n_ok": n_ok,
        "n_cone_not_sym": n_cone_fail,
    }


def killed_cone_sym() -> dict:
    """Cone band [lo,hi] is not palindrome-symmetric: k=2, W=8U, s=t0."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    s = t0
    mu = s - 2 * U + 1
    lo = 2 * (s - t0 + 1)
    hi = min(2 * s - T, W)
    ok = lo == 2 and hi != W and 2 * mu - lo == W
    return {"ok": ok, "k": k, "lo": lo, "hi": hi, "pal_lo": 2 * mu - lo, "W": W}


def killed_mid_s_minus_U() -> dict:
    """Midpoint is s-2U+1, not s-U."""
    k = 3
    U = 1 << k
    s = 6 * U
    mu = s - 2 * U + 1
    wrong = s - U
    ok = mu != wrong and mu == 4 * U + 1
    return {"ok": ok, "mu": mu, "s_minus_U": wrong}


def prefixes() -> dict:
    fs = json.loads(FS_JSON.read_text())
    fq = json.loads(FQ_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        fs["checks"]["all_ok"]
        and fq["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and fs["verdict"]["G_m_d_eq_G_m_2m_minus_d"] == "LEMMA"
        and fq["verdict"]["unified_T_eq_2U_plus_W_band"] == "LEMMA"
        and fr["verdict"]["band_lo_edge_eq_G_m_2m"] == "LEMMA"
        and fs["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, sym: dict, kc: dict, km: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert sym["ok"] and kc["ok"] and km["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    sym = green_sym()
    kc = killed_cone_sym()
    km = killed_mid_s_minus_U()
    pref = prefixes()
    checks = self_checks(c20, sym, kc, km, pref)
    dump = {
        "cycle": "FT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_sym": {k: sym[k] for k in sym if k != "ok"},
        "killed_cone_sym": {k: kc[k] for k in kc if k != "ok"},
        "killed_mid": {k: km[k] for k in km if k != "ok"},
        "lemmas": {
            "green_interval_palindrome_sym": True,
            "cone_band_palindrome_sym": False,
            "midpoint_eq_s_minus_U": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "green_interval_palindrome_sym": "LEMMA",
            "cone_band_palindrome_sym": "KILLED",
            "midpoint_eq_s_minus_U": "KILLED",
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
    print("green_sym", dump["green_sym"])


if __name__ == "__main__":
    main()
