#!/usr/bin/env python3
"""Cycle GO: every cone-hi hit palindromes onto G(U-1,f) with f≢2 mod 3.

Palindrome sends e=W/2-r/2 to f=2(U(Q-q)-1)-e in [0,U) at every
Cycle GG hit, and G equals Cycle GN's mod-3 bit G(U-1,f). Q-q is not
always a 2-power (W=16U has n=3). Raw e need not lie in [0,U);
G(Un-1,f) need not equal G(U-1,f) for f>=U; the palindrome is not
last-hit only. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_go.py --certify
Dump: research/cycle_go.json
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
from cycle_gn import mer_one

OUT = Path(__file__).resolve().with_suffix(".json")
GN_JSON = Path(__file__).resolve().parent / "cycle_gn.json"
GM_JSON = Path(__file__).resolve().parent / "cycle_gm.json"
GK_JSON = Path(__file__).resolve().parent / "cycle_gk.json"


def all_hit_pal() -> dict:
    """Every hit: palindrome f in [0,U); G=mer_one(f). n=Q-q in 1..4."""
    n_ok = 0
    n_hits = 0
    n_pre = 0
    seen_n = set()
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                m = T - s - 1
                n = Q - q
                seen_n.add(n)
                chi = 2 * s - T
                lo = 2 * (s - t0 + 1)
                n_one = 0
                for r in range(lo, chi + 1, 2):
                    e = W // 2 - r // 2
                    f = 2 * (U * n - 1) - e
                    g = G(m, W - r)
                    if not (0 <= f < U):
                        return {"ok": False, "k": k, "q": q, "f": f}
                    if g != mer_one(f) or g != G(U - 1, f):
                        return {"ok": False, "k": k, "q": q, "r": r, "G": g, "f": f}
                    n_one += g
                    n_ok += 1
                if n_one != want_ones(k):
                    return {"ok": False, "k": k, "n_one": n_one}
                n_hits += 1
                n_pre += int(n > 1)
    if seen_n != {1, 2, 3, 4}:
        return {"ok": False, "seen_n": sorted(seen_n)}
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_hits": n_hits,
        "n_pre": n_pre,
        "n_values": sorted(seen_n),
    }


def killed_n_always_pow2() -> dict:
    """Q-q is not always a 2-power: W=16U, q=1 has n=3."""
    k = 2
    U = 1 << k
    W = 16 * U
    Q = 4
    n = Q - 1
    ok = n == 3 and (n & (n - 1)) != 0
    return {"ok": ok, "k": k, "n": n}


def killed_raw_e_in_0_U() -> dict:
    """Raw e=W/2-r/2 need not lie in [0,U)."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    lo = 2 * (s - t0 + 1)
    e = W // 2 - lo // 2
    ok = e == 14 and not (0 <= e < U)
    return {"ok": ok, "k": k, "e": e, "U": U}


def killed_G_eq_low_past_U() -> dict:
    """G(Un-1, f) != G(U-1, f) for some f>=U: k=2, n=2, f=U."""
    k = 2
    U = 1 << k
    g_hi = G(2 * U - 1, U)
    g_lo = G(U - 1, U)
    ok = g_hi != g_lo
    return {"ok": ok, "k": k, "f": U, "G_2U_minus_1": g_hi, "G_U_minus_1": g_lo}


def prefixes() -> dict:
    gn = json.loads(GN_JSON.read_text())
    gm = json.loads(GM_JSON.read_text())
    gk = json.loads(GK_JSON.read_text())
    ok = (
        gn["checks"]["all_ok"]
        and gm["checks"]["all_ok"]
        and gk["checks"]["all_ok"]
        and gn["verdict"]["G_2k_minus_1_f_eq_1_iff_f_ne_2_mod_3_on_0_U"]
        == "LEMMA"
        and gn["verdict"]["last_hit_palindromes_to_low_mersenne"] == "LEMMA"
        and gm["verdict"]["even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2"]
        == "LEMMA"
        and gn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, pal: dict, kl: dict, ke: dict, kg: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and kl["ok"] and ke["ok"] and kg["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = all_hit_pal()
    kn = killed_n_always_pow2()
    ke = killed_raw_e_in_0_U()
    kg = killed_G_eq_low_past_U()
    pref = prefixes()
    checks = self_checks(c20, pal, kn, ke, kg, pref)
    dump = {
        "cycle": "GO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "all_hit_pal": {k: pal[k] for k in pal if k != "ok"},
        "killed_n_always_pow2": {k: kn[k] for k in kn if k != "ok"},
        "killed_raw_e_in_0_U": {k: ke[k] for k in ke if k != "ok"},
        "killed_G_eq_low_past_U": {k: kg[k] for k in kg if k != "ok"},
        "lemmas": {
            "every_hit_palindromes_to_low_mersenne_mod3": True,
            "n_values_1_through_4": True,
            "n_always_power_of_2": False,
            "raw_e_in_0_U": False,
            "G_Un_minus_1_eq_G_U_minus_1_past_U": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "every_hit_palindromes_to_low_mersenne_mod3": "LEMMA",
            "n_values_1_through_4": "LEMMA",
            "n_always_power_of_2": "KILLED",
            "raw_e_in_0_U": "KILLED",
            "G_Un_minus_1_eq_G_U_minus_1_past_U": "KILLED",
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
    print("all_hit_pal", dump["all_hit_pal"])


if __name__ == "__main__":
    main()
