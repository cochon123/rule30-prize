#!/usr/bin/env python3
"""Cycle SO: odd-n packed rest tot matches the QU+ST recurrence through k<=10.

If even rest(k)=odd rest(k-1) and rest=S xor T, odd tot is forced:
odd(0)=1 and odd(k)=odd(k-1) xor ST(k). That closed form is 1 iff
k<=1 or (k>=6 and k%8 in (6, 7)). Packed odd tot matches through
k<=10, and equals n1e xor n0 xor oo (Cycles SH/SN/SG). Those three
exception-set helpers cannot all hold at k=11 if this form lifts.
Not the form for all k. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_so.py --certify
Dump: research/cycle_so.json
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
from cycle_sh import want_n1e
from cycle_sn import want_n0

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
SG_JSON = Path(__file__).resolve().parent / "cycle_sg.json"
SH_JSON = Path(__file__).resolve().parent / "cycle_sh.json"
SN_JSON = Path(__file__).resolve().parent / "cycle_sn.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_odd(k: int) -> int:
    """Packed odd-n rest tot, certified k<=10: 1 iff k<=1 or (k>=6 and k%8 in (6, 7))."""
    return int(k <= 1 or (k >= 6 and k % 8 in (6, 7)))


def want_even(k: int) -> int:
    """Packed even-n rest tot, certified k<=10: 1 iff k<=2 or (k>=7 and k%8 in (0, 7))."""
    return int(k <= 2 or (k >= 7 and k % 8 in (0, 7)))


def even_odd(tot: list[int]) -> tuple[int, int]:
    return tot[0] ^ tot[2], tot[1] ^ tot[3]


def fold_split() -> dict:
    """k<=10: QO even/odd tots equal want_even/want_odd; odd is n1e xor n0 xor oo."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        e, o = even_odd(rows_in[str(k)]["tot"])
        pieces = want_n1e(k) ^ want_n0(k) ^ want_oo(k)
        if o != want_odd(k) or e != want_even(k) or o != pieces:
            return {
                "ok": False,
                "k": k,
                "e": e,
                "o": o,
                "pieces": pieces,
            }
        if (e ^ o) != want_rest_e0(k) or (e ^ o) != rows_in[str(k)]["rest"]:
            return {"ok": False, "st": True, "k": k, "e": e, "o": o}
        if k >= 1:
            pe, po = even_odd(rows_in[str(k - 1)]["tot"])
            if e != po or e != want_odd(k - 1):
                return {"ok": False, "qu": True, "k": k, "e": e, "po": po}
            if o != (po ^ want_rest_e0(k)):
                return {"ok": False, "rec": True, "k": k, "o": o, "po": po}
        n_ok += 1
        rows[str(k)] = {"even": e, "odd": o, "rest": e ^ o}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["odd"] == 1
        and rows["1"]["odd"] == 1
        and rows["2"]["odd"] == 0
        and rows["6"]["odd"] == 1
        and rows["7"]["odd"] == 1
        and rows["8"]["odd"] == 0
        and rows["10"]["odd"] == 0
        and rows["0"]["even"] == 1
        and rows["2"]["even"] == 1
        and rows["6"]["even"] == 0
        and rows["7"]["even"] == 1
        and rows["8"]["rest"] == 1
        and want_odd(11) == 0
        and want_odd(14) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """k<=64: want_odd xor parent is ST; want_even is parent want_odd."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if k >= 1:
            if want_odd(k) != (want_odd(k - 1) ^ want_rest_e0(k)):
                return {"ok": False, "rec": True, "k": k}
            if want_even(k) != want_odd(k - 1):
                return {"ok": False, "qu": True, "k": k}
        if (want_even(k) ^ want_odd(k)) != want_rest_e0(k) and k >= 1:
            return {"ok": False, "st": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_odd(0) == 1
        and want_odd(1) == 1
        and want_odd(6) == 1
        and want_odd(8) == 0
        and want_odd(11) == 0
        and want_odd(14) == 1
        and want_odd(16) == 0
        and want_even(0) == 1
        and want_even(2) == 1
        and want_even(7) == 1
        and want_even(16) == 1
        and want_rest_e0(2) == 1
        and want_rest_e0(16) == 1
        and (want_n1e(11) ^ want_n0(11) ^ want_oo(11)) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """odd equals ST; SH/SN/SG helpers xor equals want_odd at k=11; odd==0."""
    pieces11 = want_n1e(11) ^ want_n0(11) ^ want_oo(11)
    ok = (
        want_odd(0) != want_rest_e0(0)
        and want_odd(7) != want_rest_e0(7)
        and want_even(0) != want_rest_e0(0)
        and want_odd(0) == 1
        and pieces11 != want_odd(11)
        and pieces11 == 1
        and want_odd(11) == 0
        and want_n1e(11) == 1
        and want_n0(11) == 0
        and want_oo(11) == 0
    )
    return {"ok": ok, "pieces11": pieces11, "odd11": want_odd(11)}


def prefixes() -> dict:
    qo = json.loads(QO_JSON.read_text())
    qu = json.loads(QU_JSON.read_text())
    sg = json.loads(SG_JSON.read_text())
    sh = json.loads(SH_JSON.read_text())
    sn = json.loads(SN_JSON.read_text())
    ok = (
        qo["checks"]["all_ok"]
        and qu["checks"]["all_ok"]
        and sg["checks"]["all_ok"]
        and sh["checks"]["all_ok"]
        and sn["checks"]["all_ok"]
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and sg["verdict"]["packed_oo_eq_want_oo_k_le_10"] == "CERTIFIED"
        and sh["verdict"]["packed_n1e_eq_want_n1e_k_le_10"] == "CERTIFIED"
        and sn["verdict"]["n0_eq_mis_n2_k_le_10"] == "CERTIFIED"
        and qu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sn["verdict"]["prize"] == "unsolved"
        and want_odd(6) == 1
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
        "cycle": "SO",
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
            "odd_eq_want_odd_k_le_10": True,
            "odd_xor_parent_eq_ST_helpers": True,
            "odd_eq_n1e_xor_n0_xor_oo_k_le_10": True,
            "odd_all_k": False,
            "sh_sn_sg_helpers_eq_odd_at_11": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_eq_want_odd_k_le_10": "CERTIFIED",
            "odd_xor_parent_eq_ST_helpers": "LEMMA",
            "odd_eq_n1e_xor_n0_xor_oo_k_le_10": "CERTIFIED",
            "odd_all_k": "PREFIX",
            "odd_eq_ST": "KILLED",
            "odd_identically_0": "KILLED",
            "sh_sn_sg_helpers_eq_odd_at_11": "KILLED",
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
        "k0 odd",
        dump["fold_split"]["rows"]["0"]["odd"],
        "k6 odd",
        dump["fold_split"]["rows"]["6"]["odd"],
        "k11 helpers",
        dump["killed_eq"]["pieces11"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
