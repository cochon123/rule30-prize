#!/usr/bin/env python3
"""Cycle RS: covering Green n%4==2 tot xor parent Green odd tot is 1 iff k>=4.

Cycle QX Green n2 tot is 1 iff k==1 or k>=3. Cycle QW Green odd tot
is 1 iff k in {0,2}, so parent odd tot at k-1 is 1 iff k in {1,3}.
Their xor is 0 at k=1,2,3 and 1 for k>=4. Dual: Green n0 tot xor
parent Green even tot is 1 iff k>=2. Not Green n2 tot equals parent
Green odd tot (fails k>=4). Not Green even tot equals parent Green
odd tot (the Green QU analogue). Not packed n2 mismatch equals this
bit (Cycle RR is {2,4,8} through k<=10). Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rs.py --certify
Dump: research/cycle_rs.json
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
from cycle_qx import want_g_n0, want_g_n2
from cycle_rr import want_mis_n2

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
RR_JSON = Path(__file__).resolve().parent / "cycle_rr.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_g_n2_xor_parent_odd(k: int) -> int:
    """Green n2 tot xor parent Green odd tot, all k: 1 iff k>=4."""
    if k < 1:
        return 0
    return want_g_n2(k) ^ want_green_odd(k - 1)


def want_g_n0_xor_parent_even(k: int) -> int:
    """Green n0 tot xor parent Green even tot, all k: 1 iff k>=2."""
    if k < 1:
        return 0
    return want_g_n0(k) ^ want_green_even(k - 1)


def tot_form() -> dict:
    """k<=K_ALG: Green n2 xor parent odd is 1 iff k>=4; n0 xor parent even iff k>=2."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        got2 = want_g_n2(k) ^ want_green_odd(k - 1)
        if got2 != want_g_n2_xor_parent_odd(k):
            return {"ok": False, "n2": True, "k": k, "got2": got2}
        if got2 != int(k >= 4):
            return {"ok": False, "n2form": True, "k": k, "got2": got2}
        got0 = want_g_n0(k) ^ want_green_even(k - 1)
        if got0 != want_g_n0_xor_parent_even(k):
            return {"ok": False, "n0": True, "k": k, "got0": got0}
        if got0 != int(k >= 2):
            return {"ok": False, "n0form": True, "k": k, "got0": got0}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and want_g_n2_xor_parent_odd(1) == 0
        and want_g_n2_xor_parent_odd(3) == 0
        and want_g_n2_xor_parent_odd(4) == 1
        and want_g_n2_xor_parent_odd(64) == 1
        and want_g_n0_xor_parent_even(1) == 0
        and want_g_n0_xor_parent_even(2) == 1
        and want_g_n2(2) == 0
        and want_green_odd(1) == 0
        and want_g_n2(4) == 1
        and want_green_odd(3) == 0
        and want_green_even(1) != want_green_odd(0)
        and want_mis_n2(4) == 1
        and want_g_n2_xor_parent_odd(5) != want_mis_n2(5)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Green n2 equals parent Green odd; Green even equals parent Green odd; packed mis_n2 equals this bit."""
    ok = (
        want_g_n2(4) != want_green_odd(3)
        and want_g_n2_xor_parent_odd(4) == 1
        and want_green_even(1) != want_green_odd(0)
        and want_green_even(3) == want_green_odd(2)
        and want_mis_n2(2) == 1
        and want_g_n2_xor_parent_odd(2) == 0
        and want_mis_n2(5) == 0
        and want_g_n2_xor_parent_odd(5) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qw = json.loads(QW_JSON.read_text())
    rr = json.loads(RR_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qw["checks"]["all_ok"]
        and rr["checks"]["all_ok"]
        and qx["verdict"]["green_n2_iff_k_eq_1_or_ge_3"] == "LEMMA"
        and qw["verdict"]["green_odd_rest_iff_k_in_0_2"] == "LEMMA"
        and qw["verdict"]["green_even_rest_iff_k_ne_1"] == "LEMMA"
        and rr["verdict"]["mis_n2_iff_k_in_2_4_8_k_le_10"] == "CERTIFIED"
        and qx["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and rr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rr["verdict"]["prize"] == "unsolved"
        and want_g_n2_xor_parent_odd(4) == 1
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
        "cycle": "RS",
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
            "g_n2_xor_parent_odd_iff_k_ge_4": True,
            "g_n0_xor_parent_even_iff_k_ge_2": True,
            "g_n2_eq_parent_odd": False,
            "g_even_eq_parent_odd": False,
            "g_n2_xor_eq_packed_mis_n2": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "g_n2_xor_parent_odd_iff_k_ge_4": "LEMMA",
            "g_n0_xor_parent_even_iff_k_ge_2": "LEMMA",
            "g_n2_eq_parent_odd": "KILLED",
            "g_even_eq_parent_odd": "KILLED",
            "g_n2_xor_eq_packed_mis_n2": "KILLED",
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
        "n2xor4",
        want_g_n2_xor_parent_odd(4),
        "n0xor2",
        want_g_n0_xor_parent_even(2),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
