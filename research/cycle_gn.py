#!/usr/bin/env python3
"""Cycle GN: G(2^k-1, f)=1 iff f ≢ 2 (mod 3) on 0<=f<2^k.

Mersenne Green on the low interval [0, U) is the period-3 bit f%3!=2.
Ones-count is (2U+1+(k mod 2))/3, matching Cycle GK. The rule fails at
f=U (Cycle FW: G(U-1,U)=k mod 2). It is not 'f even' and not 'f≢1
mod 3'. Last-hit even-r Green palindromes onto this interval. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gn.py --certify
Dump: research/cycle_gn.json
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
from cycle_gk import want_ones

OUT = Path(__file__).resolve().with_suffix(".json")
GM_JSON = Path(__file__).resolve().parent / "cycle_gm.json"
GK_JSON = Path(__file__).resolve().parent / "cycle_gk.json"
FW_JSON = Path(__file__).resolve().parent / "cycle_fw.json"


def mer_one(f: int) -> int:
    """Predicted G(2^k-1, f) for 0<=f<2^k."""
    return int(f % 3 != 2)


def mersenne_mod3() -> dict:
    """G(U-1, f)=mer_one(f) on [0, U); ones-count matches GK."""
    n_ok = 0
    by_k = {}
    for k in range(0, 13):
        U = 1 << k
        n_one = 0
        for f in range(U):
            g = G(U - 1, f)
            if g != mer_one(f):
                return {"ok": False, "k": k, "f": f, "G": g}
            n_one += g
            n_ok += 1
        want = want_ones(k)
        if n_one != want:
            return {"ok": False, "k": k, "n_one": n_one, "want": want}
        by_k[str(k)] = n_one
    return {"ok": n_ok > 0, "n_ok": n_ok, "by_k": by_k}


def last_hit_pal() -> dict:
    """Last-hit even-r G equals mer_one(2U-2 - (W/2 - r/2))."""
    n_ok = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            q = Q - 1
            s = t0 + 1 + q * (2 * U)
            m = T - s - 1
            chi = 2 * s - T
            lo = 2 * (s - t0 + 1)
            if m != 2 * U - 2:
                return {"ok": False, "k": k, "m": m}
            for r in range(lo, chi + 1, 2):
                e = W // 2 - r // 2
                f = 2 * U - 2 - e
                g = G(m, W - r)
                if not (0 <= f < U) or g != mer_one(f) or g != G(U - 1, f):
                    return {"ok": False, "k": k, "r": r, "f": f, "G": g}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_at_U() -> dict:
    """Mod-3 rule fails at f=U: k=1, G(1,2)=1 but 2≡2."""
    k = 1
    U = 1 << k
    g = G(U - 1, U)
    ok = g == 1 and mer_one(U) == 0 and (k & 1) == 1
    return {"ok": ok, "k": k, "f": U, "G": g, "pred": mer_one(U)}


def killed_iff_even() -> dict:
    """Not G=1 iff f even: k=1, f=1 is odd and G=1."""
    g = G(1, 1)
    ok = g == 1 and (1 & 1) == 1
    return {"ok": ok, "f": 1, "G": g}


def killed_iff_ne_1_mod3() -> dict:
    """Not G=1 iff f≢1 mod 3: k=1, f=1, G=1."""
    g = G(1, 1)
    ok = g == 1 and (1 % 3) == 1
    return {"ok": ok, "f": 1, "G": g, "f_mod3": 1 % 3}


def prefixes() -> dict:
    gm = json.loads(GM_JSON.read_text())
    gk = json.loads(GK_JSON.read_text())
    fw = json.loads(FW_JSON.read_text())
    ok = (
        gm["checks"]["all_ok"]
        and gk["checks"]["all_ok"]
        and fw["checks"]["all_ok"]
        and gm["verdict"]["even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2"]
        == "LEMMA"
        and gk["verdict"]["hit_cone_ones_eq_2U_plus_1_plus_k_mod_2_over_3"]
        == "LEMMA"
        and fw["verdict"]["G_2n_minus_1_2n_eq_n_mod_2"] == "LEMMA"
        and gm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, mer: dict, pal: dict, ku: dict, ke: dict, k1: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mer["ok"] and pal["ok"]
    assert ku["ok"] and ke["ok"] and k1["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mer = mersenne_mod3()
    pal = last_hit_pal()
    ku = killed_at_U()
    ke = killed_iff_even()
    k1 = killed_iff_ne_1_mod3()
    pref = prefixes()
    checks = self_checks(c20, mer, pal, ku, ke, k1, pref)
    dump = {
        "cycle": "GN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mersenne_mod3": {k: mer[k] for k in mer if k != "ok"},
        "last_hit_pal": {k: pal[k] for k in pal if k != "ok"},
        "killed_at_U": {k: ku[k] for k in ku if k != "ok"},
        "killed_iff_even": {k: ke[k] for k in ke if k != "ok"},
        "killed_iff_ne_1_mod3": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "G_2k_minus_1_f_eq_1_iff_f_ne_2_mod_3_on_0_U": True,
            "last_hit_palindromes_to_low_mersenne": True,
            "mod3_rule_at_f_eq_U": False,
            "G_eq_1_iff_f_even": False,
            "G_eq_1_iff_f_ne_1_mod_3": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_2k_minus_1_f_eq_1_iff_f_ne_2_mod_3_on_0_U": "LEMMA",
            "last_hit_palindromes_to_low_mersenne": "LEMMA",
            "mod3_rule_at_f_eq_U": "KILLED",
            "G_eq_1_iff_f_even": "KILLED",
            "G_eq_1_iff_f_ne_1_mod_3": "KILLED",
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
    print("mersenne_mod3 n_ok", dump["mersenne_mod3"]["n_ok"])
    print("last_hit_pal n_ok", dump["last_hit_pal"]["n_ok"])


if __name__ == "__main__":
    main()
