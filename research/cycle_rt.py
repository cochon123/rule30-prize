#!/usr/bin/env python3
"""Cycle RT: covering Green even tot xor parent Green rest tot is 1 iff k in {2,3}.

Cycle QV packed 2-fold AND-mismatch tot equals parent even rest iff
even rest equals parent odd rest (the QU lift). The Green analogue
is Green even tot xor parent Green rest tot. Cycle QW Green even tot
is 1 iff k!=1 and Cycle QH Green rest tot is 1 iff k>=3, so that xor
is 1 iff k in {2,3}. Dual of Cycle RS's Green QU kill: mismatch tot
equals parent Green even tot dies (parent even tot is 1 iff k!=2).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rt.py --certify
Dump: research/cycle_rt.json
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
from cycle_qh import want_green_rest
from cycle_qw import want_green_even, want_green_odd
from cycle_rs import want_g_n2_xor_parent_odd

OUT = Path(__file__).resolve().with_suffix(".json")
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
RS_JSON = Path(__file__).resolve().parent / "cycle_rs.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_g_even_xor_parent_rest(k: int) -> int:
    """Green even tot xor parent Green rest tot, all k: 1 iff k in {2,3}."""
    if k < 1:
        return 0
    return want_green_even(k) ^ want_green_rest(k - 1)


def tot_form() -> dict:
    """k<=K_ALG: mismatch tot is even xor parent rest; 1 iff k in {2,3}."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        rest_p = want_green_even(k - 1) ^ want_green_odd(k - 1)
        if rest_p != want_green_rest(k - 1):
            return {"ok": False, "rest": True, "k": k, "rest_p": rest_p}
        got = want_green_even(k) ^ rest_p
        if got != want_g_even_xor_parent_rest(k):
            return {"ok": False, "xor": True, "k": k, "got": got}
        if got != int(k in (2, 3)):
            return {"ok": False, "form": True, "k": k, "got": got}
        pe = want_green_even(k - 1)
        if got == pe and k != 3:
            return {"ok": False, "qv_alive": True, "k": k, "got": got, "pe": pe}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and want_g_even_xor_parent_rest(1) == 0
        and want_g_even_xor_parent_rest(2) == 1
        and want_g_even_xor_parent_rest(3) == 1
        and want_g_even_xor_parent_rest(4) == 0
        and want_g_even_xor_parent_rest(64) == 0
        and want_green_even(1) != want_green_odd(0)
        and want_g_n2_xor_parent_odd(4) == 1
        and want_green_even(2) != want_green_rest(1)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Green mismatch tot equals parent Green even tot; Green even equals parent odd."""
    ok = (
        want_g_even_xor_parent_rest(1) != want_green_even(0)
        and want_g_even_xor_parent_rest(2) != want_green_even(1)
        and want_g_even_xor_parent_rest(3) == want_green_even(2)
        and want_g_even_xor_parent_rest(4) != want_green_even(3)
        and want_green_even(1) != want_green_odd(0)
        and want_green_even(4) != want_green_odd(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    qh = json.loads(QH_JSON.read_text())
    qw = json.loads(QW_JSON.read_text())
    rs = json.loads(RS_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    ok = (
        qh["checks"]["all_ok"]
        and qw["checks"]["all_ok"]
        and rs["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and qh["verdict"]["green_rest_iff_k_ge_3"] == "LEMMA"
        and qw["verdict"]["green_even_rest_iff_k_ne_1"] == "LEMMA"
        and rs["verdict"]["g_even_eq_parent_odd"] == "KILLED"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and rs["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rs["verdict"]["prize"] == "unsolved"
        and want_g_even_xor_parent_rest(2) == 1
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
        "cycle": "RT",
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
            "g_even_xor_parent_rest_iff_k_in_2_3": True,
            "g_mis_eq_parent_even": False,
            "g_even_eq_parent_odd": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "g_even_xor_parent_rest_iff_k_in_2_3": "LEMMA",
            "g_mis_eq_parent_even": "KILLED",
            "g_even_eq_parent_odd": "KILLED",
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
        "mis2",
        want_g_even_xor_parent_rest(2),
        "mis3",
        want_g_even_xor_parent_rest(3),
        "mis4",
        want_g_even_xor_parent_rest(4),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
