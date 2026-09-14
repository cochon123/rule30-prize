#!/usr/bin/env python3
"""Cycle SI: Green rest on n%4==3 even-j is 1 iff k!=1 through k<=10.

Covering Green rest split by n%4 and j parity. Even-n G=1 lives
only on even j (Cycle QV). Green rest on n%4==3 even j is 1 iff
k!=1 through k<=10, and odd j is 1 iff k==1, refining Cycle QY's
n%4==3 tot 1. Green rest on n%4==1 even j is 1 iff k<=1, and odd
j is 1 iff k==0 or k>=3. Green n%4==0 tot is not Green n%4==3
even-j (Cycle SH analogue dies at k=1). Packed n3 even-j is not
this bit. Not the identities for all k. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_si.py --certify
Dump: research/cycle_si.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_qx import want_g_n0, want_g_n1, want_g_n2, want_g_n3
from cycle_sh import want_n1e
from cycle_qw import want_green_even, want_green_odd

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
SH_JSON = Path(__file__).resolve().parent / "cycle_sh.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"

N_PAL = 64
M_SLOTS = 64
K_GREEN = 10
K_ALG = 64
Q = 10


def want_g_n1e(k: int) -> int:
    """Green rest on n%4==1 even j, certified k<=10: 1 iff k<=1."""
    return int(k <= 1)


def want_g_n1o(k: int) -> int:
    """Green rest on n%4==1 odd j, certified k<=10: 1 iff k==0 or k>=3."""
    return int(k == 0 or k >= 3)


def want_g_n3e(k: int) -> int:
    """Green rest on n%4==3 even j, certified k<=10: 1 iff k!=1."""
    return int(k != 1)


def want_g_n3o(k: int) -> int:
    """Green rest on n%4==3 odd j, certified k<=10: 1 iff k==1."""
    return int(k == 1)


def green_nmodj(k: int) -> dict:
    """Clipped G=1 xor split by n%4 and j parity, off forced."""
    U = 1 << k
    clip = 5 * U
    tot = [[0, 0] for _ in range(4)]
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = Q * U - 2 * j
            if p in FORCED:
                continue
            tot[n % 4][j % 2] ^= 1
    n0e, n1e, n1o = tot[0][0], tot[1][0], tot[1][1]
    n2e, n3e, n3o = tot[2][0], tot[3][0], tot[3][1]
    return {
        "n0e": n0e,
        "n0o": tot[0][1],
        "n1e": n1e,
        "n1o": n1o,
        "n2e": n2e,
        "n2o": tot[2][1],
        "n3e": n3e,
        "n3o": n3o,
    }


def nmodj_walk() -> dict:
    """k<=10: Green n3 even-j equals want_g_n3e; n1 even-j equals want_g_n1e."""
    qx = json.loads(QX_JSON.read_text())
    qx_rows = qx["green_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_GREEN + 1):
        w = green_nmodj(k)
        if w["n0o"] != 0 or w["n2o"] != 0:
            return {"ok": False, "even_oddj": True, "k": k, "w": w}
        if w["n0e"] != want_g_n0(k) or w["n2e"] != want_g_n2(k):
            return {"ok": False, "even": True, "k": k, "w": w}
        if w["n1e"] != want_g_n1e(k) or w["n1o"] != want_g_n1o(k):
            return {"ok": False, "n1": True, "k": k, "w": w}
        if w["n3e"] != want_g_n3e(k) or w["n3o"] != want_g_n3o(k):
            return {"ok": False, "n3": True, "k": k, "w": w}
        if (w["n1e"] ^ w["n1o"]) != want_g_n1(k):
            return {"ok": False, "n1xor": True, "k": k, "w": w}
        if (w["n3e"] ^ w["n3o"]) != want_g_n3(k):
            return {"ok": False, "n3xor": True, "k": k, "w": w}
        if (w["n0e"] ^ w["n2e"]) != want_green_even(k):
            return {"ok": False, "even_tot": True, "k": k}
        if (w["n1e"] ^ w["n1o"] ^ w["n3e"] ^ w["n3o"]) != want_green_odd(k):
            return {"ok": False, "odd_tot": True, "k": k}
        if k <= 8:
            qt = qx_rows[str(k)]["tot"]
            if w["n0e"] != qt[0] or (w["n1e"] ^ w["n1o"]) != qt[1]:
                return {"ok": False, "qx": True, "k": k, "w": w, "qt": qt}
            if w["n2e"] != qt[2] or (w["n3e"] ^ w["n3o"]) != qt[3]:
                return {"ok": False, "qx3": True, "k": k, "w": w, "qt": qt}
        n_ok += 1
        rows[str(k)] = {
            "n0e": w["n0e"],
            "n1e": w["n1e"],
            "n1o": w["n1o"],
            "n2e": w["n2e"],
            "n3e": w["n3e"],
            "n3o": w["n3o"],
        }
    ok = (
        n_ok == K_GREEN + 1
        and rows["0"]["n3e"] == 1
        and rows["1"]["n3e"] == 0
        and rows["2"]["n3e"] == 1
        and rows["10"]["n3e"] == 1
        and rows["1"]["n3o"] == 1
        and rows["0"]["n3o"] == 0
        and rows["10"]["n3o"] == 0
        and rows["0"]["n1e"] == 1
        and rows["1"]["n1e"] == 1
        and rows["2"]["n1e"] == 0
        and rows["0"]["n1o"] == 1
        and rows["1"]["n1o"] == 0
        and rows["3"]["n1o"] == 1
        and rows["0"]["n0e"] == 1
        and rows["1"]["n0e"] != rows["1"]["n3e"]
        and rows["3"]["n0e"] != rows["3"]["n3e"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def tot_form() -> dict:
    """Helpers xor to QX/QY nmod tots for k<=64; n3e xor n3o is 1."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if (want_g_n1e(k) ^ want_g_n1o(k)) != want_g_n1(k):
            return {"ok": False, "n1": True, "k": k}
        if (want_g_n3e(k) ^ want_g_n3o(k)) != want_g_n3(k):
            return {"ok": False, "n3": True, "k": k}
        if (want_g_n0(k) ^ want_g_n2(k)) != want_green_even(k):
            return {"ok": False, "even": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_g_n3e(0) == 1
        and want_g_n3e(1) == 0
        and want_g_n3e(2) == 1
        and want_g_n3o(1) == 1
        and want_g_n3o(3) == 0
        and want_g_n1e(1) == 1
        and want_g_n1e(2) == 0
        and want_g_n1o(0) == 1
        and want_g_n1o(2) == 0
        and want_g_n1o(3) == 1
        and want_g_n0(1) != want_g_n3e(1)
        and want_g_n0(3) != want_g_n3e(3)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Green n0 equals n3e; n3e identically 1; packed n3e equals Green n3e."""
    qo = json.loads(QO_JSON.read_text())
    n0_0 = qo["rest_n0_walk"]["rows"]["0"]["tot"][0]
    n0_1 = qo["rest_n0_walk"]["rows"]["1"]["tot"][0]
    ok = (
        want_g_n0(1) != want_g_n3e(1)
        and want_g_n0(3) != want_g_n3e(3)
        and want_g_n3e(1) == 0
        and want_g_n3o(1) == 1
        and n0_0 != want_g_n3e(0)
        and n0_1 == want_g_n3e(1)
        and want_n1e(2) != want_g_n1e(2)
        and want_g_n1e(0) == 1
    )
    return {"ok": ok, "packed_n0_k0": n0_0, "packed_n0_k1": n0_1}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    sh = json.loads(SH_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and sh["checks"]["all_ok"]
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and sh["verdict"]["packed_n0_eq_n3e_k_le_10"] == "CERTIFIED"
        and sh["verdict"]["packed_n0_eq_n3_tot"] == "KILLED"
        and sh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sh["verdict"]["prize"] == "unsolved"
        and want_g_n3e(1) == 0
        and want_n1e(3) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert walk["ok"] and tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
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
    walk = nmodj_walk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "SI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "nmodj_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "green_n3e_iff_k_ne_1_k_le_10": True,
            "green_n3o_iff_k_eq_1_k_le_10": True,
            "green_n1e_iff_k_le_1_k_le_10": True,
            "green_n1o_iff_k_0_or_ge_3_k_le_10": True,
            "green_n3e_all_k": False,
            "green_n0_eq_n3e": False,
            "packed_n3e_eq_green_n3e": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "green_n3e_iff_k_ne_1_k_le_10": "CERTIFIED",
            "green_n3o_iff_k_eq_1_k_le_10": "CERTIFIED",
            "green_n1e_iff_k_le_1_k_le_10": "CERTIFIED",
            "green_n1o_iff_k_0_or_ge_3_k_le_10": "CERTIFIED",
            "green_n3e_all_k": "PREFIX",
            "green_n0_eq_n3e": "KILLED",
            "packed_n3e_eq_green_n3e": "KILLED",
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
        "nmodj n_ok",
        dump["nmodj_walk"]["n_ok"],
        "k1 n3e",
        dump["nmodj_walk"]["rows"]["1"]["n3e"],
        "k10 n3e",
        dump["nmodj_walk"]["rows"]["10"]["n3e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
