#!/usr/bin/env python3
"""Cycle SP: packed n1e equals 1 xor UNIQUE_EVEN packed tot through k<=10.

Cycle SH packed rest on n%4==1 even j is 1 iff k not in {3,4,5}.
Cycle QP UNIQUE_EVEN packed tot is 1 iff k in {3,4,5} for all k, so
n1e equals 1 xor that tot through k<=10 (same bit as UNIQUE_ODD
packed tot and unique Green tot). If this lifts with Cycle SO's odd
form, n0 xor oo must fire at k=11. Not n1e for all k. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sp.py --certify
Dump: research/cycle_sp.json
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
from cycle_qg import want_unique_gxor_tot_closed
from cycle_qp import want_unique_even_pack, want_unique_odd_pack
from cycle_qv import even_slots
from cycle_qj import want_unique_even
from cycle_sg import want_oo
from cycle_sh import want_n1e
from cycle_sn import want_n0
from cycle_so import want_odd

OUT = Path(__file__).resolve().with_suffix(".json")
SH_JSON = Path(__file__).resolve().parent / "cycle_sh.json"
QP_JSON = Path(__file__).resolve().parent / "cycle_qp.json"
SO_JSON = Path(__file__).resolve().parent / "cycle_so.json"
QG_JSON = Path(__file__).resolve().parent / "cycle_qg.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_n1e_ue(k: int) -> int:
    """Packed n1e as 1 xor UNIQUE_EVEN packed tot, certified k<=10."""
    return 1 ^ want_unique_even_pack(k)


def fold_split() -> dict:
    """k<=10: SH n1e equals want_n1e_ue equals 1 xor unique odd/Green tots."""
    sh = json.loads(SH_JSON.read_text())
    sh_rows = sh["nmodj_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        n1e = sh_rows[str(k)]["n1e"]
        if (
            n1e != want_n1e(k)
            or n1e != want_n1e_ue(k)
            or n1e != (1 ^ want_unique_odd_pack(k))
            or n1e != (1 ^ want_unique_gxor_tot_closed(k))
        ):
            return {"ok": False, "k": k, "n1e": n1e}
        n_ok += 1
        rows[str(k)] = {"n1e": n1e, "ue": want_unique_even_pack(k)}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["n1e"] == 1
        and rows["2"]["n1e"] == 1
        and rows["3"]["n1e"] == 0
        and rows["4"]["n1e"] == 0
        and rows["5"]["n1e"] == 0
        and rows["6"]["n1e"] == 1
        and rows["10"]["n1e"] == 1
        and rows["3"]["ue"] == 1
        and rows["6"]["ue"] == 0
        and want_n1e_ue(11) == 1
        and want_odd(11) == 0
        and (want_n0(11) ^ want_oo(11)) == 0
        and (want_odd(11) ^ want_n1e_ue(11)) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """k<=64: want_n1e is 1 xor unique even/odd packed and unique Green tots."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        bit = want_n1e_ue(k)
        if bit != want_n1e(k):
            return {"ok": False, "n1e": True, "k": k}
        if bit != (1 ^ want_unique_odd_pack(k)):
            return {"ok": False, "uo": True, "k": k}
        if bit != (1 ^ want_unique_gxor_tot_closed(k)):
            return {"ok": False, "ug": True, "k": k}
        if (want_odd(k) ^ bit) != (want_n0(k) ^ want_oo(k)) and k <= K_REST:
            return {"ok": False, "so": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_n1e_ue(0) == 1
        and want_n1e_ue(3) == 0
        and want_n1e_ue(11) == 1
        and want_n1e_ue(16) == 1
        and want_unique_even_pack(5) == 1
        and want_unique_even_pack(6) == 0
        and want_rest_e0(2) == 1
        and (want_odd(11) ^ want_n1e_ue(11) ^ want_n0(11) ^ want_oo(11)) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """n1e equals unique even pack; equals Green unique even; identically 1."""
    ok = (
        want_n1e_ue(3) != want_unique_even_pack(3)
        and want_n1e_ue(0) != want_unique_even_pack(0)
        and want_n1e_ue(0) != want_unique_even(0)
        and want_n1e_ue(3) != want_unique_even(3)
        and want_n1e_ue(6) == want_unique_even(6)
        and want_n1e_ue(3) == 0
        and want_n1e_ue(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    sh = json.loads(SH_JSON.read_text())
    qp = json.loads(QP_JSON.read_text())
    so = json.loads(SO_JSON.read_text())
    qg = json.loads(QG_JSON.read_text())
    ok = (
        sh["checks"]["all_ok"]
        and qp["checks"]["all_ok"]
        and so["checks"]["all_ok"]
        and qg["checks"]["all_ok"]
        and sh["verdict"]["packed_n1e_eq_want_n1e_k_le_10"] == "CERTIFIED"
        and qp["verdict"]["unique_even_pack_iff_k_in_3_4_5"] == "LEMMA"
        and qp["verdict"]["unique_odd_pack_iff_k_in_3_4_5"] == "LEMMA"
        and qg["verdict"]["unique_gxor_tot_iff_k_in_3_4_5"] == "LEMMA"
        and so["verdict"]["odd_eq_want_odd_k_le_10"] == "CERTIFIED"
        and so["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and so["verdict"]["prize"] == "unsolved"
        and want_n1e_ue(2) == 1
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
        "cycle": "SP",
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
            "n1e_eq_1_xor_ue_pack_k_le_10": True,
            "n1e_all_k": False,
            "n1e_eq_ue_pack": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n1e_eq_1_xor_ue_pack_k_le_10": "CERTIFIED",
            "n1e_all_k": "PREFIX",
            "n1e_eq_ue_pack": "KILLED",
            "n1e_eq_green_unique_even": "KILLED",
            "n1e_identically_1": "KILLED",
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
        "k3 n1e",
        dump["fold_split"]["rows"]["3"]["n1e"],
        "k6 n1e",
        dump["fold_split"]["rows"]["6"]["n1e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
