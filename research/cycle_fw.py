#!/usr/bin/env python3
"""Cycle FW: G(2^n-1, 2^n)=n mod 2; G(r, 2^a-2)=1 on {2^a-1-2^j} (+ all-ones iff a odd).

Palindrome sends G(2^n-1, 2^n-2) to G(2^n-1, 2^n). The odd-m recursion
gives G(2^n-1, 2^n)=1 XOR G(2^{n-1}-1, 2^{n-1}) with G(1,2)=1, hence
n mod 2. Cycle FQ reduces G(m, 2^a-2) to r=m mod 2^a. On 0<=r<2^a the
value is 1 iff r=2^a-1-2^j for some 0<=j<a, or r=2^a-1 with a odd.
That is a closed form for Cycle FS's unclipped cone-hi G(m,2U-2).
Kills: the identity for all n; all Hamming-weight >=a-1; remainder J
equals the center-AND XOR. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_fw.py --certify
Dump: research/cycle_fw.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"
FV_JSON = Path(__file__).resolve().parent / "cycle_fv.json"


def want_one(r: int, a: int) -> int:
    """Predicted G(r, 2^a-2) for 0<=r<2^a."""
    pa = 1 << a
    ones = pa - 1
    if r == ones:
        return a & 1
    x = ones - r
    return int(x > 0 and (x & (x - 1)) == 0)


def mersenne_power(nmax: int = 16) -> dict:
    """G(2^n-1, 2^n)=n mod 2; palindrome G(2^n-1, 2^n-2) matches."""
    n_ok = 0
    for n in range(1, nmax + 1):
        m = (1 << n) - 1
        g = G(m, 1 << n)
        g2 = G(m, (1 << n) - 2)
        if g != (n & 1) or g2 != (n & 1) or g != g2:
            return {"ok": False, "n": n, "G": g, "G_pal": g2}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok, "nmax": nmax}


def bit_pattern(amax: int = 10) -> dict:
    """G(r, 2^a-2)=want_one(r,a) for 0<=r<2^a."""
    n_ok = 0
    for a in range(1, amax + 1):
        pa = 1 << a
        for r in range(pa):
            g = G(r, pa - 2)
            if g != want_one(r, a):
                return {"ok": False, "a": a, "r": r, "G": g, "want": want_one(r, a)}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "amax": amax}


def fq_reduce(amax: int = 8) -> dict:
    """G(m, 2^a-2)=G(m mod 2^a, 2^a-2)."""
    n_ok = 0
    for a in range(1, amax + 1):
        pa = 1 << a
        for q in range(0, 5):
            for r in range(pa):
                m = q * pa + r
                if G(m, pa - 2) != G(r, pa - 2):
                    return {"ok": False, "a": a, "m": m}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok, "amax": amax}


def killed_all_n() -> dict:
    """G(2^n-1, 2^n)=1 fails at n=2: G(3,4)=0."""
    g = G(3, 4)
    return {"ok": g == 0 and (2 & 1) == 0, "n": 2, "G": g}


def killed_all_high_wt() -> dict:
    """wt>=a-1 is not enough: a=4, r=15=2^4-1, G(15,14)=0."""
    g = G(15, 14)
    return {"ok": g == 0 and want_one(15, 4) == 0, "a": 4, "r": 15, "G": g}


def killed_j_eq_center() -> dict:
    """Remainder J equals center-AND XOR fails at k=4, J6."""
    k = 4
    U = 1 << k
    t0, t1, T = 2 * U, 6 * U, 6 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    J = ctr = 0
    for s in range(t0, t1):
        A = (row << 1) & row
        tmp, p = A, 0
        while tmp:
            if tmp & 1:
                J ^= G(T - s - 1, T - p)
            tmp >>= 1
            p += 1
        if (A >> (s + 1)) & 1:
            ctr ^= G(T - s - 1, T - (s + 1))
        row = rule30_step(row)
    return {"ok": J != ctr, "k": k, "J6": J, "center": ctr}


def prefixes() -> dict:
    fs = json.loads(FS_JSON.read_text())
    fq = json.loads(FQ_JSON.read_text())
    fv = json.loads(FV_JSON.read_text())
    ok = (
        fs["checks"]["all_ok"]
        and fq["checks"]["all_ok"]
        and fv["checks"]["all_ok"]
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and fq["verdict"]["G_n_plus_2a_d_eq_G_n_d_for_d_lt_2a"] == "LEMMA"
        and fv["verdict"]["remainder_center_s_plus_1_always_in_support"] == "LEMMA"
        and fs["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, mer: dict, bits: dict, red: dict, kn: dict, kw: dict, kj: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mer["ok"] and bits["ok"] and red["ok"]
    assert kn["ok"] and kw["ok"] and kj["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mer = mersenne_power()
    bits = bit_pattern()
    red = fq_reduce()
    kn = killed_all_n()
    kw = killed_all_high_wt()
    kj = killed_j_eq_center()
    pref = prefixes()
    checks = self_checks(c20, mer, bits, red, kn, kw, kj, pref)
    dump = {
        "cycle": "FW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mersenne_power": {k: mer[k] for k in mer if k != "ok"},
        "bit_pattern": {k: bits[k] for k in bits if k != "ok"},
        "fq_reduce": {k: red[k] for k in red if k != "ok"},
        "killed_all_n": {k: kn[k] for k in kn if k != "ok"},
        "killed_high_wt": {k: kw[k] for k in kw if k != "ok"},
        "killed_j_eq_center": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "G_2n_minus_1_2n_eq_n_mod_2": True,
            "G_r_2a_minus_2_bit_pattern": True,
            "G_m_2a_minus_2_eq_G_m_mod_2a": True,
            "G_2n_minus_1_2n_eq_1_all_n": False,
            "all_wt_ge_a_minus_1": False,
            "J_eq_remainder_center": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_2n_minus_1_2n_eq_n_mod_2": "LEMMA",
            "G_r_2a_minus_2_bit_pattern": "LEMMA",
            "G_m_2a_minus_2_eq_G_m_mod_2a": "LEMMA",
            "G_2n_minus_1_2n_eq_1_all_n": "KILLED",
            "all_wt_ge_a_minus_1": "KILLED",
            "J_eq_remainder_center": "KILLED",
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
    print("bit_pattern", dump["bit_pattern"])


if __name__ == "__main__":
    main()
