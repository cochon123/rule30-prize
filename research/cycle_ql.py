#!/usr/bin/env python3
"""Cycle QL: covering leftover even-j Green xor on even n is 1 iff k in {0,2,4,5}.

Cycle QK leftover even-j odd-n tot is 1 iff k>=1. Cycle QJ leftover even-j
tot is 1 iff k<=1 or k==3 or k>=6. Their xor is leftover even-j even-n tot.
For k>=1 that also equals Cycle QI even-n even-j tot A(k-1) xor unique even
tot xor Cycle PC p=4 even-n xor (which is 1). Closed form: 1 iff k in
{0,2,4,5}. Not rest=S xor T (k=4: leftover even-n even-j=1, rest=0; k=6:
0 vs 1). Not leftover even-j even-n tot equals leftover even-j tot. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ql.py --certify
Dump: research/cycle_ql.json
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
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qh import want_clip_g1
from cycle_qj import want_lo_even, want_unique_even
from cycle_qk import leftover_npar, want_lo_ee as want_lo_ee_xor, want_lo_oe

OUT = Path(__file__).resolve().with_suffix(".json")
QK_JSON = Path(__file__).resolve().parent / "cycle_qk.json"
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64


def want_lo_ee(k: int) -> int:
    """Covering leftover even-j Green xor on even n, all k: 1 iff k in {0,2,4,5}."""
    return int(k in (0, 2, 4, 5))


def lo_even_n() -> dict:
    """k<=K_CHK: leftover even-j even-n tot matches want_lo_ee; doubling identity."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = leftover_npar(k)
        if w["lo_ee"] != want_lo_ee(k) or w["lo_oe"] != want_lo_oe(k):
            return {
                "ok": False,
                "lo": True,
                "k": k,
                "lo_ee": w["lo_ee"],
                "lo_oe": w["lo_oe"],
            }
        if (w["lo_ee"] ^ w["lo_oe"]) != want_lo_even(k):
            return {"ok": False, "qj": True, "k": k}
        if w["lo_ee"] != want_lo_ee_xor(k):
            return {"ok": False, "xor": True, "k": k}
        if k >= 1:
            all_ee = w["lo_ee"] ^ w["u_ee"] ^ w["f_ee"]
            if all_ee != want_clip_g1(k - 1):
                return {"ok": False, "qi": True, "k": k, "all_ee": all_ee}
            if w["u_ee"] != want_unique_even(k):
                return {"ok": False, "u": True, "k": k, "u_ee": w["u_ee"]}
            if w["f_ee"] != 1:
                return {"ok": False, "p4e": True, "k": k}
            alg = want_clip_g1(k - 1) ^ want_unique_even(k) ^ 1
            if w["lo_ee"] != alg:
                return {"ok": False, "alg": True, "k": k, "got": w["lo_ee"]}
            n_ok += 1
        rows[str(k)] = {
            "lo_ee": w["lo_ee"],
            "lo_oe": w["lo_oe"],
            "u_ee": w["u_ee"],
            "f_ee": w["f_ee"],
        }
    ok = (
        rows["0"]["lo_ee"] == 1
        and rows["1"]["lo_ee"] == 0
        and rows["2"]["lo_ee"] == 1
        and rows["3"]["lo_ee"] == 0
        and rows["4"]["lo_ee"] == 1
        and rows["5"]["lo_ee"] == 1
        and rows["6"]["lo_ee"] == 0
        and rows["8"]["lo_ee"] == 0
        and rows["8"]["lo_oe"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: closed form equals QK xor and the doubling identity."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        bit = want_lo_ee(k)
        if bit != want_lo_ee_xor(k):
            return {"ok": False, "xor": True, "k": k, "got": bit}
        if bit != (want_lo_even(k) ^ want_lo_oe(k)):
            return {"ok": False, "qj": True, "k": k}
        if k >= 1:
            alg = want_clip_g1(k - 1) ^ want_unique_even(k) ^ 1
            if bit != alg:
                return {"ok": False, "alg": True, "k": k, "alg": alg}
            if want_lo_oe(k) != 1:
                return {"ok": False, "oe": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_ee(0) == 1
        and want_lo_ee(1) == 0
        and want_lo_ee(2) == 1
        and want_lo_ee(4) == 1
        and want_lo_ee(5) == 1
        and want_lo_ee(6) == 0
        and want_lo_ee(7) == 0
        and want_lo_ee(64) == 0
        and want_unique_even(6) == 1
        and want_clip_g1(0) == 1
        and want_clip_g1(1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_ee_eq_st() -> dict:
    """Leftover even-j even-n tot equals ST / leftover even tot."""
    ok = (
        want_lo_ee(4) == 1
        and want_rest_e0(4) == 0
        and want_rest10(4, 10) == 0
        and want_lo_ee(6) == 0
        and want_rest_e0(6) == 1
        and want_lo_ee(7) == 0
        and want_lo_even(7) == 1
        and want_lo_ee(2) == 1
        and want_lo_even(2) == 0
    )
    return {"ok": ok, "k4": 1, "ST4": 0, "k6": 0, "ST6": 1}


def prefixes() -> dict:
    qk = json.loads(QK_JSON.read_text())
    qj = json.loads(QJ_JSON.read_text())
    ok = (
        qk["checks"]["all_ok"]
        and qj["checks"]["all_ok"]
        and qk["verdict"]["lo_oe_iff_k_ge_1"] == "LEMMA"
        and qj["verdict"]["lo_even_iff_le1_or_k3_or_ge6"] == "LEMMA"
        and qk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qk["verdict"]["prize"] == "unsolved"
        and want_lo_oe(1) == 1
        and want_lo_even(7) == 1
        and want_clip_g1(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, lo, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and lo["ok"] and tot["ok"]
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
    lo = lo_even_n()
    tot = tot_form()
    kl = killed_ee_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, lo, tot, kl, sc, pref)
    dump = {
        "cycle": "QL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "lo_even_n": {k: lo[k] for k in lo if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_ee_iff_k_in_0_2_4_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "lo_ee_eq_ST": False,
            "lo_ee_eq_lo_even": False,
            "prize": False,
        },
        "verdict": {
            "lo_ee_iff_k_in_0_2_4_5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "lo_ee_eq_ST": "KILLED",
            "lo_ee_eq_lo_even": "KILLED",
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
        "lo_even_n n_ok",
        dump["lo_even_n"]["n_ok"],
        "k_hi",
        dump["lo_even_n"]["k_hi"],
        "lo_ee8",
        dump["lo_even_n"]["rows"]["8"]["lo_ee"],
        "lo_oe8",
        dump["lo_even_n"]["rows"]["8"]["lo_oe"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
