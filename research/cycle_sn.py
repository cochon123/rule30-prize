#!/usr/bin/env python3
"""Cycle SN: packed rest on n%4==0 equals n2 AND-mismatch tot through k<=10.

Cycle RR n0 tot is parent even xor mis_n0. Cycle QV mismatch xor
equals parent even, so n0 tot equals mis_n2: 1 iff k in {2,4,8}
through k<=10. Cycle SH n3 even-j equals n0, hence the same bit.
Not those identities for all k. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sn.py --certify
Dump: research/cycle_sn.json
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
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_qx import want_g_n0
from cycle_rr import want_mis_n0, want_mis_n2
from cycle_sh import want_n1e
from cycle_si import want_g_n3e

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
RR_JSON = Path(__file__).resolve().parent / "cycle_rr.json"
SH_JSON = Path(__file__).resolve().parent / "cycle_sh.json"
SM_JSON = Path(__file__).resolve().parent / "cycle_sm.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_n0(k: int) -> int:
    """Packed rest on n%4==0, certified k<=10: 1 iff k in {2,4,8}."""
    return want_mis_n2(k)


def want_n3e_pack(k: int) -> int:
    """Packed rest on n%4==3 even j, certified k<=10: equals want_n0."""
    return want_n0(k)


def fold_split() -> dict:
    """k<=10: QO n0 equals want_n0 equals SH n3e equals RR mis2 (k>=1)."""
    qo = json.loads(QO_JSON.read_text())
    rr = json.loads(RR_JSON.read_text())
    sh = json.loads(SH_JSON.read_text())
    qo_rows = qo["rest_n0_walk"]["rows"]
    rr_rows = rr["fold_split"]["rows"]
    sh_rows = sh["nmodj_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        n0 = qo_rows[str(k)]["n0"]
        n3e = sh_rows[str(k)]["n3e"]
        if n0 != want_n0(k) or n3e != want_n3e_pack(k) or n3e != n0:
            return {"ok": False, "n0": True, "k": k, "n0": n0, "n3e": n3e}
        if k >= 1:
            r = rr_rows[str(k)]
            if r["n0"] != n0 or r["mis2"] != want_mis_n2(k):
                return {"ok": False, "rr": True, "k": k, "r": r}
            if r["n0"] != r["mis2"]:
                return {"ok": False, "n0_mis2": True, "k": k, "r": r}
            if (r["mis0"] ^ r["mis2"]) != r["pe"]:
                return {"ok": False, "qv": True, "k": k, "r": r}
            if r["n0"] != (r["pe"] ^ r["mis0"]):
                return {"ok": False, "rr0": True, "k": k, "r": r}
        n_ok += 1
        rows[str(k)] = {"n0": n0, "n3e": n3e}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["n0"] == 0
        and rows["2"]["n0"] == 1
        and rows["4"]["n0"] == 1
        and rows["8"]["n0"] == 1
        and rows["7"]["n0"] == 0
        and rows["10"]["n0"] == 0
        and rows["8"]["n3e"] == 1
        and want_n0(16) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """k<=64: want_n0 is mis_n2; silent n3e is Green n3e xor that bit."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_n0(k) != want_mis_n2(k) or want_n3e_pack(k) != want_n0(k):
            return {"ok": False, "alias": True, "k": k}
        if k >= 1 and (want_mis_n0(k) ^ want_mis_n2(k) ^ want_n0(k) ^ want_mis_n0(k)):
            return {"ok": False, "qv": True, "k": k}
        sil = want_g_n3e(k) ^ want_n3e_pack(k)
        if sil != (want_g_n3e(k) ^ want_n0(k)):
            return {"ok": False, "sil": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_n0(0) == 0
        and want_n0(2) == 1
        and want_n0(8) == 1
        and want_n0(9) == 0
        and (want_g_n3e(0) ^ want_n0(0)) == 1
        and (want_g_n3e(1) ^ want_n0(1)) == 0
        and (want_g_n3e(2) ^ want_n0(2)) == 0
        and (want_g_n3e(8) ^ want_n0(8)) == 0
        and want_n1e(3) == 0
        and want_rest_e0(2) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """n0 identically 0; n0 equals ST; n0 equals Green n0; n3e equals Green n3e."""
    ok = (
        want_n0(2) == 1
        and want_n0(0) == 0
        and want_n0(4) != want_rest_e0(4)
        and want_n0(0) != want_g_n0(0)
        and want_n0(2) == want_g_n0(2)
        and want_n3e_pack(1) != want_g_n3e(1)
        and want_n3e_pack(0) != want_g_n3e(0)
    )
    return {"ok": ok}


def prefixes() -> dict:
    qv = json.loads(QV_JSON.read_text())
    rr = json.loads(RR_JSON.read_text())
    sh = json.loads(SH_JSON.read_text())
    sm = json.loads(SM_JSON.read_text())
    ok = (
        qv["checks"]["all_ok"]
        and rr["checks"]["all_ok"]
        and sh["checks"]["all_ok"]
        and sm["checks"]["all_ok"]
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and rr["verdict"]["n2_eq_parent_odd_except_2_4_8_k_le_10"] == "CERTIFIED"
        and sh["verdict"]["packed_n0_eq_n3e_k_le_10"] == "CERTIFIED"
        and sm["verdict"]["green_n3e_iff_k_ne_1_all_k"] == "LEMMA"
        and sh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sm["verdict"]["prize"] == "unsolved"
        and want_n0(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, fold, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert fold["ok"] and tot["ok"] and kl["ok"]
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
    fold = fold_split()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, fold, tot, kl, sc, pref)
    dump = {
        "cycle": "SN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "fold_split": {k: fold[k] for k in fold if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n0_eq_mis_n2_k_le_10": True,
            "n3e_eq_mis_n2_k_le_10": True,
            "n0_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n0_eq_mis_n2_k_le_10": "CERTIFIED",
            "n3e_eq_mis_n2_k_le_10": "CERTIFIED",
            "n0_all_k": "PREFIX",
            "n0_identically_0": "KILLED",
            "n0_eq_ST": "KILLED",
            "n0_eq_green_n0": "KILLED",
            "n3e_eq_green_n3e": "KILLED",
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
        "fold n_ok",
        dump["fold_split"]["n_ok"],
        "k2 n0",
        dump["fold_split"]["rows"]["2"]["n0"],
        "k8 n3e",
        dump["fold_split"]["rows"]["8"]["n3e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
