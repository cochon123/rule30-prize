#!/usr/bin/env python3
"""Cycle SJ: covering Green p=0 xor on odd n is 1 iff k==0 through k<=12.

Cycle QI clip-edge p=0 tot is 1 for every k. Split by n parity:
odd-n xor is 1 iff k==0 and even-n xor is 1 iff k>=1 through k<=12
(QI's k_hi). Many odd n still fire for k>=1; they cancel. Cycle QI
odd-n even-j clipped G=1 equals p=0 at k-1, so n%4==3 even-j clip
equals parent odd p=0 (1 iff k==1 for k>=1) through k<=8. Not empty
odd n at p=0. Not those identities for all k. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sj.py --certify
Dump: research/cycle_sj.json
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
from cycle_qi import clip_parity, want_p0_gxor
from cycle_qv import even_slots
from cycle_si import want_g_n3e

OUT = Path(__file__).resolve().with_suffix(".json")
QI_JSON = Path(__file__).resolve().parent / "cycle_qi.json"
SI_JSON = Path(__file__).resolve().parent / "cycle_si.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_FOLD = 8
K_ALG = 64


def want_p0_odd(k: int) -> int:
    """Covering Green p=0 xor on odd n, certified k<=12: 1 iff k==0."""
    return int(k == 0)


def want_p0_even(k: int) -> int:
    """Covering Green p=0 xor on even n, certified k<=12: 1 iff k>=1."""
    return int(k >= 1)


def want_g1_n3e(k: int) -> int:
    """Clipped G=1 on n%4==3 even j: 1 iff k<=1, certified k<=8."""
    return int(k <= 1)


def want_g1_n1e(k: int) -> int:
    """Clipped G=1 on n%4==1 even j: 1 iff k>=2, certified k<=8."""
    return int(k >= 2)


def p0_par(k: int) -> dict:
    """Green G=1 xor at packed p=0, split even/odd n."""
    U = 1 << k
    j = 5 * U
    e = o = 0
    n_odd = 0
    for n in range(live_lo(k, 0), 4 * U):
        if 0 <= j <= 2 * n and G(n, j):
            if n % 2 == 0:
                e ^= 1
            else:
                o ^= 1
                n_odd += 1
    tot = gxor_p(0, k)
    return {"e": e, "o": o, "tot": tot, "n_odd": n_odd}


def p0_walk() -> dict:
    """k<=12: odd-n p=0 xor equals want_p0_odd; even-n equals want_p0_even."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        w = p0_par(k)
        if w["tot"] != want_p0_gxor(k) or (w["e"] ^ w["o"]) != w["tot"]:
            return {"ok": False, "tot": True, "k": k, "w": w}
        if w["o"] != want_p0_odd(k) or w["e"] != want_p0_even(k):
            return {"ok": False, "par": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {"e": w["e"], "o": w["o"], "n_odd": w["n_odd"]}
    ok = (
        n_ok == K_G + 1
        and rows["0"]["o"] == 1
        and rows["0"]["e"] == 0
        and rows["0"]["n_odd"] == 1
        and rows["1"]["o"] == 0
        and rows["1"]["e"] == 1
        and rows["1"]["n_odd"] >= 2
        and rows["12"]["o"] == 0
        and rows["12"]["e"] == 1
        and rows["12"]["n_odd"] >= 2
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def g1_fold() -> dict:
    """1<=k<=8: n%4==3 even-j clip equals parent p=0 odd; n1 even-j equals even."""
    n_ok = 0
    rows = {}
    for k in range(1, K_FOLD + 1):
        n1e = n3e = 0
        U = 1 << k
        for n in range(0, 4 * U):
            e, _o = clip_parity(n, k)
            if n % 4 == 1:
                n1e ^= e
            elif n % 4 == 3:
                n3e ^= e
        if n3e != want_p0_odd(k - 1) or n3e != want_g1_n3e(k):
            return {"ok": False, "n3e": True, "k": k, "n3e": n3e}
        if n1e != want_p0_even(k - 1) or n1e != want_g1_n1e(k):
            return {"ok": False, "n1e": True, "k": k, "n1e": n1e}
        if (n1e ^ n3e) != want_p0_gxor(k - 1):
            return {"ok": False, "qi": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"n1e": n1e, "n3e": n3e}
    ok = (
        n_ok == K_FOLD
        and rows["1"]["n3e"] == 1
        and rows["2"]["n3e"] == 0
        and rows["8"]["n3e"] == 0
        and rows["1"]["n1e"] == 0
        and rows["2"]["n1e"] == 1
        and want_g1_n3e(0) == 1
        and want_g_n3e(0) == 1
        and want_g_n3e(1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FOLD, "rows": rows}


def tot_form() -> dict:
    """k<=64: p0 odd xor even is QI tot 1; g1_n3e xor g1_n1e is 1 for k>=1."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if (want_p0_odd(k) ^ want_p0_even(k)) != want_p0_gxor(k):
            return {"ok": False, "p0": True, "k": k}
        if k >= 1 and (want_g1_n3e(k) ^ want_g1_n1e(k)) != 1:
            return {"ok": False, "g1": True, "k": k}
        if k >= 1 and want_g1_n3e(k) != want_p0_odd(k - 1):
            return {"ok": False, "fold": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_p0_odd(0) == 1
        and want_p0_odd(1) == 0
        and want_p0_even(0) == 0
        and want_p0_even(1) == 1
        and want_g1_n3e(1) == 1
        and want_g1_n3e(2) == 0
        and want_g1_n1e(2) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Odd n at p=0 empty; identically 0; identically 1; rest n3e equals g1 n3e."""
    w1 = p0_par(1)
    ok = (
        w1["n_odd"] >= 2
        and want_p0_odd(0) == 1
        and want_p0_odd(1) == 0
        and want_g1_n3e(1) != want_g_n3e(1)
        and want_g1_n3e(0) == want_g_n3e(0)
    )
    return {"ok": ok, "n_odd_k1": w1["n_odd"]}


def prefixes() -> dict:
    qi = json.loads(QI_JSON.read_text())
    si = json.loads(SI_JSON.read_text())
    ok = (
        qi["checks"]["all_ok"]
        and si["checks"]["all_ok"]
        and qi["verdict"]["p0_gxor_1_all_k"] == "LEMMA"
        and qi["verdict"]["even_j_except_k1"] == "LEMMA"
        and si["verdict"]["green_n3e_iff_k_ne_1_k_le_10"] == "CERTIFIED"
        and si["verdict"]["green_n0_eq_n3e"] == "KILLED"
        and si["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and si["verdict"]["prize"] == "unsolved"
        and want_p0_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, walk, fold, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert walk["ok"] and fold["ok"] and tot["ok"] and kl["ok"]
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
    walk = p0_walk()
    fold = g1_fold()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, walk, fold, tot, kl, sc, pref)
    dump = {
        "cycle": "SJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "p0_walk": {k: walk[k] for k in walk if k != "ok"},
        "g1_fold": {k: fold[k] for k in fold if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "p0_odd_iff_k_eq_0_k_le_12": True,
            "p0_even_iff_k_ge_1_k_le_12": True,
            "g1_n3e_eq_parent_p0_odd_k_le_8": True,
            "p0_odd_all_k": False,
            "p0_odd_empty_k_ge_1": False,
            "g1_n3e_eq_rest_n3e": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "p0_odd_iff_k_eq_0_k_le_12": "CERTIFIED",
            "p0_even_iff_k_ge_1_k_le_12": "CERTIFIED",
            "g1_n3e_eq_parent_p0_odd_k_le_8": "CERTIFIED",
            "p0_odd_all_k": "PREFIX",
            "p0_odd_empty_k_ge_1": "KILLED",
            "g1_n3e_eq_rest_n3e": "KILLED",
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
        "p0 n_ok",
        dump["p0_walk"]["n_ok"],
        "k0 o",
        dump["p0_walk"]["rows"]["0"]["o"],
        "k12 n_odd",
        dump["p0_walk"]["rows"]["12"]["n_odd"],
        "fold n_ok",
        dump["g1_fold"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
