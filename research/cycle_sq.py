#!/usr/bin/env python3
"""Cycle SQ: n0 xor oo matches the SO+SP remainder through k<=10.

Cycle SO odd tot equals n1e xor n0 xor oo through k<=10. Cycle SP
n1e equals 1 xor UNIQUE_EVEN packed tot. The remainder n0 xor oo is
1 iff k==2 or (k>=8 and k%8 not in (6, 7)) through k<=10. Helpers
odd xor n1e equal that form for all k. SN/SG exception-set helpers
xor to 0 at k=11, so they cannot both lift if this form lifts. Not
the form for all k. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_sq.py --certify
Dump: research/cycle_sq.json
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
from cycle_sg import want_oo
from cycle_sn import want_n0
from cycle_so import want_odd
from cycle_sp import want_n1e_ue

OUT = Path(__file__).resolve().with_suffix(".json")
SH_JSON = Path(__file__).resolve().parent / "cycle_sh.json"
SG_JSON = Path(__file__).resolve().parent / "cycle_sg.json"
SN_JSON = Path(__file__).resolve().parent / "cycle_sn.json"
SO_JSON = Path(__file__).resolve().parent / "cycle_so.json"
SP_JSON = Path(__file__).resolve().parent / "cycle_sp.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_n0_oo(k: int) -> int:
    """n0 xor oo, certified k<=10: 1 iff k==2 or (k>=8 and k%8 not in (6, 7))."""
    return int(k == 2 or (k >= 8 and k % 8 not in (6, 7)))


def fold_split() -> dict:
    """k<=10: SH n0 xor oo equals want_n0_oo equals odd xor n1e."""
    sh = json.loads(SH_JSON.read_text())
    sh_rows = sh["nmodj_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        r = sh_rows[str(k)]
        bit = r["n0e"] ^ r["n1o"] ^ r["n3o"]
        pieces = want_n0(k) ^ want_oo(k)
        rec = want_odd(k) ^ want_n1e_ue(k)
        if bit != want_n0_oo(k) or bit != pieces or bit != rec:
            return {
                "ok": False,
                "k": k,
                "bit": bit,
                "pieces": pieces,
                "rec": rec,
            }
        n_ok += 1
        rows[str(k)] = {"n0_oo": bit, "n0": r["n0e"], "oo": r["n1o"] ^ r["n3o"]}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["n0_oo"] == 0
        and rows["2"]["n0_oo"] == 1
        and rows["4"]["n0_oo"] == 0
        and rows["7"]["n0_oo"] == 0
        and rows["8"]["n0_oo"] == 1
        and rows["9"]["n0_oo"] == 1
        and rows["10"]["n0_oo"] == 1
        and rows["4"]["n0"] == 1
        and rows["4"]["oo"] == 1
        and want_n0_oo(11) == 1
        and (want_n0(11) ^ want_oo(11)) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """k<=64: want_n0_oo equals odd xor n1e; SN/SG xor dies at k=11."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_n0_oo(k) != (want_odd(k) ^ want_n1e_ue(k)):
            return {"ok": False, "rec": True, "k": k}
        if k <= K_REST and want_n0_oo(k) != (want_n0(k) ^ want_oo(k)):
            return {"ok": False, "pieces": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_n0_oo(2) == 1
        and want_n0_oo(8) == 1
        and want_n0_oo(11) == 1
        and want_n0_oo(14) == 0
        and want_n0_oo(16) == 1
        and want_odd(11) == 0
        and want_n1e_ue(11) == 1
        and (want_n0(11) ^ want_oo(11)) == 0
        and want_rest_e0(2) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """n0 xor oo identically 0; equals ST; SN/SG helpers at k=11."""
    ok = (
        want_n0_oo(2) == 1
        and want_n0_oo(0) == 0
        and want_n0_oo(2) == want_rest_e0(2)
        and want_n0_oo(8) == want_rest_e0(8)
        and want_n0_oo(9) != want_rest_e0(9)
        and (want_n0(11) ^ want_oo(11)) != want_n0_oo(11)
        and want_n0_oo(4) != want_n0(4)
        and want_n0_oo(4) != want_oo(4)
    )
    return {"ok": ok}


def prefixes() -> dict:
    sh = json.loads(SH_JSON.read_text())
    sg = json.loads(SG_JSON.read_text())
    sn = json.loads(SN_JSON.read_text())
    so = json.loads(SO_JSON.read_text())
    sp = json.loads(SP_JSON.read_text())
    ok = (
        sh["checks"]["all_ok"]
        and sg["checks"]["all_ok"]
        and sn["checks"]["all_ok"]
        and so["checks"]["all_ok"]
        and sp["checks"]["all_ok"]
        and so["verdict"]["odd_eq_want_odd_k_le_10"] == "CERTIFIED"
        and sp["verdict"]["n1e_eq_1_xor_ue_pack_k_le_10"] == "CERTIFIED"
        and sn["verdict"]["n0_eq_mis_n2_k_le_10"] == "CERTIFIED"
        and sg["verdict"]["packed_oo_eq_want_oo_k_le_10"] == "CERTIFIED"
        and so["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sp["verdict"]["prize"] == "unsolved"
        and want_n0_oo(2) == 1
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
        "cycle": "SQ",
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
            "n0_oo_eq_want_n0_oo_k_le_10": True,
            "n0_oo_eq_odd_xor_n1e_helpers": True,
            "n0_oo_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n0_oo_eq_want_n0_oo_k_le_10": "CERTIFIED",
            "n0_oo_eq_odd_xor_n1e_helpers": "LEMMA",
            "n0_oo_all_k": "PREFIX",
            "n0_oo_identically_0": "KILLED",
            "n0_oo_eq_ST": "KILLED",
            "sn_sg_helpers_eq_n0_oo_at_11": "KILLED",
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
        "k2",
        dump["fold_split"]["rows"]["2"]["n0_oo"],
        "k8",
        dump["fold_split"]["rows"]["8"]["n0_oo"],
        "k11 form",
        want_n0_oo(11),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
