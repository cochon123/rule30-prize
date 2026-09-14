#!/usr/bin/env python3
"""Cycle RR: covering n%4==2 rest tot equals parent odd tot except k in {2,4,8}.

Cycle QU even-n rest tot equals parent odd tot through k<=10. Parent
odd n 2-folds onto child n%4==2, so cellwise 2-fold AND would make
n2 tot equal parent odd tot. The 2-fold AND-mismatch tot on n%4==2
is 1 iff k in {2,4,8} through k<=10, and n2 tot equals parent odd
xor that bit. Dual: mismatch on n%4==0 is 1 iff k in {1,3,4,9},
and the two mismatch tots xor to parent even tot (Cycle QV). Unique
n2 tot is 0, so leftover n2 tot is the same fold. Not n2 tot equals
parent odd for all k<=10. Not the exception sets for all k. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rr.py --certify
Dump: research/cycle_rr.json
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
from cycle_rb import want_u_n2
from cycle_rc import want_lo_n2

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
RQ_JSON = Path(__file__).resolve().parent / "cycle_rq.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10


def want_mis_n2(k: int) -> int:
    """2-fold AND-mismatch tot on n%4==2, certified 1<=k<=10: 1 iff k in {2,4,8}."""
    return int(k in (2, 4, 8))


def want_mis_n0(k: int) -> int:
    """2-fold AND-mismatch tot on n%4==0, certified 1<=k<=10: 1 iff k in {1,3,4,9}."""
    return int(k in (1, 3, 4, 9))


def even_odd(tot: list[int]) -> tuple[int, int]:
    return tot[0] ^ tot[2], tot[1] ^ tot[3]


def fold_split() -> dict:
    """1<=k<=10: n2 tot is parent odd xor mis_n2; n0 is parent even xor mis_n0."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(1, K_REST + 1):
        tot = rows_in[str(k)]["tot"]
        ptot = rows_in[str(k - 1)]["tot"]
        e, o = even_odd(tot)
        pe, po = even_odd(ptot)
        n0, n2 = tot[0], tot[2]
        mis0 = n0 ^ pe
        mis2 = n2 ^ po
        if mis2 != want_mis_n2(k):
            return {"ok": False, "mis2": True, "k": k, "mis2": mis2}
        if mis0 != want_mis_n0(k):
            return {"ok": False, "mis0": True, "k": k, "mis0": mis0}
        if n2 != (po ^ want_mis_n2(k)):
            return {"ok": False, "n2": True, "k": k, "n2": n2, "po": po}
        if n0 != (pe ^ want_mis_n0(k)):
            return {"ok": False, "n0": True, "k": k, "n0": n0, "pe": pe}
        if (mis0 ^ mis2) != pe:
            return {"ok": False, "qv": True, "k": k, "pe": pe}
        if e != po:
            return {"ok": False, "qu": True, "k": k, "e": e, "po": po}
        if want_u_n2(k) != 0:
            return {"ok": False, "u2": True, "k": k}
        if want_lo_n2(k, n2) != n2:
            return {"ok": False, "lo2": True, "k": k}
        if (e ^ o) != want_rest_e0(k):
            return {"ok": False, "st": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n0": n0,
            "n2": n2,
            "pe": pe,
            "po": po,
            "mis0": mis0,
            "mis2": mis2,
        }
    ok = (
        n_ok == K_REST
        and rows["2"]["mis2"] == 1
        and rows["4"]["mis2"] == 1
        and rows["8"]["mis2"] == 1
        and rows["7"]["mis2"] == 0
        and rows["10"]["mis2"] == 0
        and rows["1"]["mis0"] == 1
        and rows["3"]["mis0"] == 1
        and rows["4"]["mis0"] == 1
        and rows["9"]["mis0"] == 1
        and rows["2"]["n2"] == 0
        and rows["2"]["po"] == 1
        and rows["8"]["n2"] == 0
        and rows["8"]["po"] == 1
        and want_mis_n2(16) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """n2 tot equals parent odd all k<=10; exception sets for all k."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n2_2 = rows_in["2"]["tot"][2]
    po_2 = rows_in["1"]["tot"][1] ^ rows_in["1"]["tot"][3]
    n2_4 = rows_in["4"]["tot"][2]
    po_4 = rows_in["3"]["tot"][1] ^ rows_in["3"]["tot"][3]
    ok = (
        n2_2 != po_2
        and n2_4 != po_4
        and want_mis_n2(2) == 1
        and want_mis_n2(7) == 0
        and want_mis_n2(16) == 0
        and want_mis_n0(9) == 1
        and want_mis_n0(8) == 0
        and want_mis_n0(16) == 0
    )
    return {"ok": ok, "n2_2": n2_2, "po_2": po_2, "n2_4": n2_4, "po_4": po_4}


def prefixes() -> dict:
    qu = json.loads(QU_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    rq = json.loads(RQ_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qu["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and rq["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and qu["verdict"]["n2_eq_parent_odd"] == "KILLED"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and rq["verdict"]["ue_g_eq_green_nmod_k_ge_6"] == "LEMMA"
        and qu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qu["verdict"]["even_rest_eq_parent_odd_all_k"] == "PREFIX"
        and rq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fold, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fold["ok"]
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
    fold = fold_split()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fold, kl, sc, pref)
    dump = {
        "cycle": "RR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "fold_split": {k: fold[k] for k in fold if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n2_eq_parent_odd_except_2_4_8_k_le_10": True,
            "mis_n2_iff_k_in_2_4_8_k_le_10": True,
            "mis_n0_iff_k_in_1_3_4_9_k_le_10": True,
            "n2_eq_parent_odd_k_le_10": False,
            "mis_n2_iff_k_in_2_4_8_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n2_eq_parent_odd_except_2_4_8_k_le_10": "CERTIFIED",
            "mis_n2_iff_k_in_2_4_8_k_le_10": "CERTIFIED",
            "mis_n0_iff_k_in_1_3_4_9_k_le_10": "CERTIFIED",
            "n2_eq_parent_odd_k_le_10": "KILLED",
            "mis_n2_iff_k_in_2_4_8_all_k": "PREFIX",
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
        "fold_split n_ok",
        dump["fold_split"]["n_ok"],
        "mis2",
        {k: dump["fold_split"]["rows"][k]["mis2"] for k in ("2", "4", "7", "8", "10")},
        "mis0",
        {k: dump["fold_split"]["rows"][k]["mis0"] for k in ("1", "3", "4", "9")},
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
