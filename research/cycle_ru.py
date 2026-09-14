#!/usr/bin/env python3
"""Cycle RU: covering Green n%4==1 tot equals parent Green even tot.

Cycle QX Green n1 tot is 1 iff k==1 or k>=3. Cycle QW Green even tot
is 1 iff k!=1, so parent even tot at k-1 is 1 iff k!=2. Those bits
agree for every k>=1. Dual: Green n3 tot xor parent Green odd tot
is 1 iff k==2 or k>=4 (QY n3 tot is 1; parent odd tot is 1 iff
k in {1,3}). Green odd tot xor parent Green even tot is 1 for every
k>=1, so the odd-n Green QU analogue dies. Packed n1 tot equals
parent even tot dies at k=1 (Cycle QO). Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ru.py --certify
Dump: research/cycle_ru.json
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
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qw import want_green_even, want_green_odd
from cycle_qx import want_g_n1, want_g_n3
from cycle_rs import want_g_n0_xor_parent_even, want_g_n2_xor_parent_odd

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
RT_JSON = Path(__file__).resolve().parent / "cycle_rt.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_g_n1_xor_parent_even(k: int) -> int:
    """Green n1 tot xor parent Green even tot, all k: 0 for k>=1."""
    if k < 1:
        return 0
    return want_g_n1(k) ^ want_green_even(k - 1)


def want_g_n3_xor_parent_odd(k: int) -> int:
    """Green n3 tot xor parent Green odd tot, all k: 1 iff k==2 or k>=4."""
    if k < 1:
        return 0
    return want_g_n3(k) ^ want_green_odd(k - 1)


def want_g_odd_xor_parent_even(k: int) -> int:
    """Green odd tot xor parent Green even tot, all k: 1 for k>=1."""
    if k < 1:
        return 0
    return want_green_odd(k) ^ want_green_even(k - 1)


def tot_form() -> dict:
    """k<=K_ALG: n1 equals parent even; n3 xor parent odd iff k==2 or k>=4."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        got1 = want_g_n1(k) ^ want_green_even(k - 1)
        if got1 != want_g_n1_xor_parent_even(k):
            return {"ok": False, "n1": True, "k": k, "got1": got1}
        if got1 != 0:
            return {"ok": False, "n1form": True, "k": k, "got1": got1}
        got3 = want_g_n3(k) ^ want_green_odd(k - 1)
        if got3 != want_g_n3_xor_parent_odd(k):
            return {"ok": False, "n3": True, "k": k, "got3": got3}
        if got3 != int(k == 2 or k >= 4):
            return {"ok": False, "n3form": True, "k": k, "got3": got3}
        got_o = want_green_odd(k) ^ want_green_even(k - 1)
        if got_o != want_g_odd_xor_parent_even(k):
            return {"ok": False, "odd": True, "k": k, "got_o": got_o}
        if got_o != 1:
            return {"ok": False, "oddform": True, "k": k, "got_o": got_o}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and want_g_n1_xor_parent_even(1) == 0
        and want_g_n1_xor_parent_even(2) == 0
        and want_g_n1_xor_parent_even(64) == 0
        and want_g_n3_xor_parent_odd(1) == 0
        and want_g_n3_xor_parent_odd(2) == 1
        and want_g_n3_xor_parent_odd(3) == 0
        and want_g_n3_xor_parent_odd(4) == 1
        and want_g_n3_xor_parent_odd(64) == 1
        and want_g_odd_xor_parent_even(1) == 1
        and want_g_odd_xor_parent_even(2) == 1
        and want_g_n0_xor_parent_even(2) == 1
        and want_g_n2_xor_parent_odd(4) == 1
        and want_g_n1(1) == want_green_even(0)
        and want_g_n3(2) != want_green_odd(1)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Green n3 equals parent odd; Green odd equals parent even; packed n1 equals parent even."""
    qo = json.loads(QO_JSON.read_text())
    rows = qo["rest_n0_walk"]["rows"]
    tot0 = rows["0"]["tot"]
    tot1 = rows["1"]["tot"]
    pe0 = tot0[0] ^ tot0[2]
    pack_n1 = tot1[1]
    ok = (
        want_g_n3(2) != want_green_odd(1)
        and want_g_n3_xor_parent_odd(2) == 1
        and want_green_odd(1) != want_green_even(0)
        and want_green_odd(2) != want_green_even(1)
        and want_g_odd_xor_parent_even(1) == 1
        and pack_n1 != pe0
        and pack_n1 == 0
        and pe0 == 1
        and want_g_n1(1) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    qw = json.loads(QW_JSON.read_text())
    rt = json.loads(RT_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and qw["checks"]["all_ok"]
        and rt["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and qy["verdict"]["g1_n1_eq_parent_even"] == "LEMMA"
        and qw["verdict"]["green_even_rest_iff_k_ne_1"] == "LEMMA"
        and qw["verdict"]["green_odd_rest_iff_k_in_0_2"] == "LEMMA"
        and rt["verdict"]["g_even_eq_parent_odd"] == "KILLED"
        and qy["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and rt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rt["verdict"]["prize"] == "unsolved"
        and want_g_n1_xor_parent_even(2) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, kl, sc, pref)
    dump = {
        "cycle": "RU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "g_n1_eq_parent_even": True,
            "g_n3_xor_parent_odd_iff_k_eq_2_or_ge_4": True,
            "g_odd_xor_parent_even_all_k_ge_1": True,
            "g_n3_eq_parent_odd": False,
            "g_odd_eq_parent_even": False,
            "pack_n1_eq_parent_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "g_n1_eq_parent_even": "LEMMA",
            "g_n3_xor_parent_odd_iff_k_eq_2_or_ge_4": "LEMMA",
            "g_odd_xor_parent_even_all_k_ge_1": "LEMMA",
            "g_n3_eq_parent_odd": "KILLED",
            "g_odd_eq_parent_even": "KILLED",
            "pack_n1_eq_parent_even": "KILLED",
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
        "tot_form n_ok",
        dump["tot_form"]["n_ok"],
        "n1eq",
        int(want_g_n1_xor_parent_even(2) == 0),
        "n3xor2",
        want_g_n3_xor_parent_odd(2),
        "n3xor4",
        want_g_n3_xor_parent_odd(4),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
