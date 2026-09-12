#!/usr/bin/env python3
"""Cycle FS: G(m,d)=G(m,2m-d); unclipped cone-hi is G(m, 2U-2).

(1+x+x^2)^m is reciprocal of degree 2m, so G(m,d)=G(m,2m-d). Cycle
FK's corners G(n,0)=G(n,2n)=1 are the palindrome of each other, and
Cycle FR's band lo-edge G(m,2m)=1 is the palindrome of G(m,0)=1.
On the unclipped unified band (s<=U+W) the cone-upper degree
W-(2s-T) palindromes to the constant 2U-2, so that edge is G(m,2U-2).
It is not identically 1. Kills: palindrome about m (G(m,d)=G(m,m-d));
unclipped hi-edge Green identically 1. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fs.py --certify
Dump: research/cycle_fs.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"
FK_JSON = Path(__file__).resolve().parent / "cycle_fk.json"


def palindrome(mmax: int = 64) -> dict:
    """G(m,d)=G(m,2m-d) for 0<=d<=2m."""
    n_ok = 0
    for m in range(0, mmax):
        for d in range(0, 2 * m + 1):
            if G(m, d) != G(m, 2 * m - d):
                return {"ok": False, "m": m, "d": d}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "mmax": mmax}


def cone_hi_to_2U_minus_2() -> dict:
    """Unclipped cone-hi Green equals G(m, 2U-2). Palindrome degree is 2U-2."""
    n_ok = 0
    n_one = 0
    n_zero = 0
    for k in range(0, 8):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in (t0, t0 + max(U, 1), clip - 1, clip):
                if not (t0 <= s <= clip and s < T):
                    continue
                m = T - s - 1
                pal = 2 * m - (W - (2 * s - T))
                if pal != 2 * U - 2:
                    return {"ok": False, "k": k, "s": s, "got_pal": pal, "want": 2 * U - 2}
                if s < clip:
                    r_hi = 2 * s - T
                    g = G(m, W - r_hi)
                    g2 = G(m, 2 * U - 2)
                    if g != g2:
                        return {"ok": False, "k": k, "W": W, "s": s, "g": g, "g2": g2}
                    n_ok += 1
                    if g:
                        n_one += 1
                    else:
                        n_zero += 1
    return {"ok": n_ok > 0 and n_zero > 0, "n_ok": n_ok, "n_one": n_one, "n_zero": n_zero}


def killed_about_m() -> dict:
    """Palindrome about m fails: G(5,2)=1 != G(5,3)=0."""
    ok = G(5, 2) == 1 and G(5, 3) == 0 and G(5, 5 - 2) == 0
    return {"ok": ok, "m": 5, "d": 2, "G_d": G(5, 2), "G_m_minus_d": G(5, 3)}


def killed_hi_eq_1() -> dict:
    """Unclipped hi-edge Green is not identically 1."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    s = clip - 1
    m = T - s - 1
    g = G(m, W - (2 * s - T))
    ok = t0 <= s < clip and g == 0
    return {"ok": ok, "k": k, "s": s, "G": g}


def prefixes() -> dict:
    fr = json.loads(FR_JSON.read_text())
    fq = json.loads(FQ_JSON.read_text())
    fk = json.loads(FK_JSON.read_text())
    ok = (
        fr["checks"]["all_ok"]
        and fq["checks"]["all_ok"]
        and fk["checks"]["all_ok"]
        and fr["verdict"]["band_lo_edge_eq_G_m_2m"] == "LEMMA"
        and fr["verdict"]["band_hi_after_clip_eq_G_m_0"] == "LEMMA"
        and fq["verdict"]["unified_T_eq_2U_plus_W_band"] == "LEMMA"
        and fk["verdict"]["G_n0_eq_G_n2n_eq_1"] == "LEMMA"
        and fr["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, pal: dict, hi: dict, km: dict, k1: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and hi["ok"] and km["ok"] and k1["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = palindrome()
    hi = cone_hi_to_2U_minus_2()
    km = killed_about_m()
    k1 = killed_hi_eq_1()
    pref = prefixes()
    checks = self_checks(c20, pal, hi, km, k1, pref)
    dump = {
        "cycle": "FS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "palindrome": {k: pal[k] for k in pal if k != "ok"},
        "cone_hi": {k: hi[k] for k in hi if k != "ok"},
        "killed_about_m": {k: km[k] for k in km if k != "ok"},
        "killed_hi_eq_1": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "G_m_d_eq_G_m_2m_minus_d": True,
            "unclipped_cone_hi_eq_G_m_2U_minus_2": True,
            "palindrome_about_m": False,
            "unclipped_hi_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_m_d_eq_G_m_2m_minus_d": "LEMMA",
            "unclipped_cone_hi_eq_G_m_2U_minus_2": "LEMMA",
            "palindrome_about_m": "KILLED",
            "unclipped_hi_eq_1": "KILLED",
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
    print("palindrome", dump["palindrome"])
    print("cone_hi", dump["cone_hi"])


if __name__ == "__main__":
    main()
