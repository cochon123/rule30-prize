#!/usr/bin/env python3
"""Cycle SL: covering Green p=0 on even n at k equals p=0 tot at k-1.

G(2m, 5*2^k)=G(m, 5*2^{k-1}) for k>=1, and the covering even-n
window at packed p=0 is exactly the parent covering window. Cycle
QI tot at p=0 is 1 for every k, so even-n xor is 1 for k>=1 and
odd-n xor is 0. At k=0, j=5 is odd, even n vanish, tot 1, odd-n
is 1. Lifts Cycle SJ's split to all k. Cycle SI rest n3e remains
PREFIX (clip fold still certified k<=8). Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sl.py --certify
Dump: research/cycle_sl.json
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
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import live_lo
from cycle_qg import gxor_p
from cycle_qi import want_p0_gxor
from cycle_qv import even_slots
from cycle_sj import p0_par, want_g1_n3e, want_p0_even, want_p0_odd
from cycle_sk import want_f_n3e
from cycle_si import want_g_n3e

OUT = Path(__file__).resolve().with_suffix(".json")
QI_JSON = Path(__file__).resolve().parent / "cycle_qi.json"
SJ_JSON = Path(__file__).resolve().parent / "cycle_sj.json"
SK_JSON = Path(__file__).resolve().parent / "cycle_sk.json"

N_PAL = 64
M_SLOTS = 64
K_WALK = 12
K_DBL = 8
K_ALG = 64


def dbl_window() -> dict:
    """k>=1: G(2m, 5U)=G(m, 5U/2) on the covering even-n p=0 window."""
    n_ok = 0
    rows = {}
    for k in range(1, K_DBL + 1):
        U = 1 << k
        j = 5 * U
        jp = 5 * (U // 2)
        lo = live_lo(k, 0)
        e = 0
        n_even = 0
        for n in range(lo, 4 * U):
            if n % 2:
                continue
            m = n // 2
            g = G(n, j) if 0 <= j <= 2 * n else 0
            gp = G(m, jp) if 0 <= jp <= 2 * m else 0
            if g != gp:
                return {"ok": False, "cell": True, "k": k, "n": n, "g": g, "gp": gp}
            e ^= g
            n_even += 1
        if e != gxor_p(0, k - 1) or e != want_p0_gxor(k - 1):
            return {"ok": False, "parent": True, "k": k, "e": e}
        if e != want_p0_even(k):
            return {"ok": False, "even": True, "k": k, "e": e}
        n_ok += 1
        rows[str(k)] = {"e": e, "n_even": n_even}
    ok = (
        n_ok == K_DBL
        and rows["1"]["e"] == 1
        and rows["8"]["e"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_DBL, "rows": rows}


def p0_walk() -> dict:
    """k<=12: odd-n p=0 xor equals want_p0_odd; even-n equals want_p0_even."""
    n_ok = 0
    rows = {}
    for k in range(0, K_WALK + 1):
        w = p0_par(k)
        if w["tot"] != want_p0_gxor(k) or (w["e"] ^ w["o"]) != w["tot"]:
            return {"ok": False, "tot": True, "k": k, "w": w}
        if w["o"] != want_p0_odd(k) or w["e"] != want_p0_even(k):
            return {"ok": False, "par": True, "k": k, "w": w}
        if k >= 1 and w["e"] != gxor_p(0, k - 1):
            return {"ok": False, "fold": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {"e": w["e"], "o": w["o"], "n_odd": w["n_odd"]}
    ok = (
        n_ok == K_WALK + 1
        and rows["0"]["o"] == 1
        and rows["0"]["e"] == 0
        and rows["1"]["o"] == 0
        and rows["12"]["o"] == 0
        and rows["12"]["e"] == 1
        and rows["1"]["n_odd"] >= 2
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_WALK, "rows": rows}


def tot_form() -> dict:
    """k<=64: even-n p=0 is 1 for k>=1; odd-n is 1 iff k==0; SI helpers."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if (want_p0_odd(k) ^ want_p0_even(k)) != want_p0_gxor(k):
            return {"ok": False, "p0": True, "k": k}
        if k >= 1 and want_p0_even(k) != want_p0_gxor(k - 1):
            return {"ok": False, "fold": True, "k": k}
        if k >= 1 and want_p0_odd(k) != 0:
            return {"ok": False, "odd": True, "k": k}
        if k >= 1 and (want_g1_n3e(k) ^ want_f_n3e(k)) != want_g_n3e(k):
            return {"ok": False, "si": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_p0_odd(0) == 1
        and want_p0_odd(1) == 0
        and want_p0_even(0) == 0
        and want_p0_even(1) == 1
        and want_g1_n3e(1) == 1
        and want_f_n3e(1) == 1
        and want_g_n3e(1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Odd n at p=0 empty; even n identically 0; SI rest n3e for all k."""
    w1 = p0_par(1)
    ok = (
        w1["n_odd"] >= 2
        and want_p0_odd(0) == 1
        and want_p0_odd(1) == 0
        and want_p0_even(0) == 0
        and want_g1_n3e(8) == 0
    )
    return {"ok": ok, "n_odd_k1": w1["n_odd"]}


def prefixes() -> dict:
    qi = json.loads(QI_JSON.read_text())
    sj = json.loads(SJ_JSON.read_text())
    sk = json.loads(SK_JSON.read_text())
    ok = (
        qi["checks"]["all_ok"]
        and sj["checks"]["all_ok"]
        and sk["checks"]["all_ok"]
        and qi["verdict"]["p0_gxor_1_all_k"] == "LEMMA"
        and sj["verdict"]["p0_odd_iff_k_eq_0_k_le_12"] == "CERTIFIED"
        and sj["verdict"]["p0_odd_all_k"] == "PREFIX"
        and sk["verdict"]["f_n3e_iff_k_ge_1"] == "LEMMA"
        and sk["verdict"]["si_rest_n3e_via_g1_xor_forced_all_k"] == "PREFIX"
        and sk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sk["verdict"]["prize"] == "unsolved"
        and want_p0_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, dbl, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert dbl["ok"] and walk["ok"] and tot["ok"] and kl["ok"]
    assert sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    dbl = dbl_window()
    walk = p0_walk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, dbl, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "SL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "dbl_window": {k: dbl[k] for k in dbl if k != "ok"},
        "p0_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "p0_even_eq_parent_tot_all_k": True,
            "p0_odd_iff_k_eq_0_all_k": True,
            "si_rest_n3e_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "p0_even_eq_parent_tot_all_k": "LEMMA",
            "p0_odd_iff_k_eq_0_all_k": "LEMMA",
            "walk_k_le_12": "CERTIFIED",
            "si_rest_n3e_all_k": "PREFIX",
            "p0_odd_empty_k_ge_1": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
            "E_all_k": "PREFIX",
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
        "dbl n_ok",
        dump["dbl_window"]["n_ok"],
        "walk n_ok",
        dump["p0_walk"]["n_ok"],
        "k0 o",
        dump["p0_walk"]["rows"]["0"]["o"],
        "k12 o",
        dump["p0_walk"]["rows"]["12"]["o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
