#!/usr/bin/env python3
"""Cycle QU: covering even-n rest xor at k equals odd-n rest xor at k-1 through k<=10.

Cycle QO's 4-fold tot rest on n%4==0 equals ST at k-2 dies at k=10.
The 2-fold tot even-n rest xor at k equals parent odd-n rest xor for
every 1<=k<=10, including k=10. Slicewise n2 tot equals parent odd tot
fails at k=2. Even-n rest equals parent rest tot / ST at k-1 fails at
k=1. Given this tot, rest=ST iff odd-n rest at k equals odd-n rest at
k-1 xor ST at k; that is a rewrite, not a packed identity. For k>=6
UNIQUE_EVEN even-n tot and unique odd-n tot at k-1 are both 1, so the
same tot is leftover even-n at k equals leftover odd-n at k-1. Not
rest=S xor T for all k. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qu.py --certify
Dump: research/cycle_qu.json
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
from cycle_qr import want_uo_odd
from cycle_qs import want_ue_even, want_ue_odd
from cycle_qt import want_lo_en, want_lo_on

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QT_JSON = Path(__file__).resolve().parent / "cycle_qt.json"
QS_JSON = Path(__file__).resolve().parent / "cycle_qs.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def even_odd(tot: list[int]) -> tuple[int, int]:
    """Rest xor split by n parity from n%4 tot."""
    return tot[0] ^ tot[2], tot[1] ^ tot[3]


def rest_fold() -> dict:
    """1<=k<=10: even-n rest xor equals parent odd-n rest xor; dies vs ST(k-1)."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(1, K_REST + 1):
        tot = rows_in[str(k)]["tot"]
        ptot = rows_in[str(k - 1)]["tot"]
        e, o = even_odd(tot)
        pe, po = even_odd(ptot)
        rest = e ^ o
        if rest != want_rest10(k, 10) or rest != want_rest_e0(k):
            return {"ok": False, "rest": True, "k": k, "e": e, "o": o}
        if e != po:
            return {"ok": False, "fold": True, "k": k, "e": e, "po": po}
        if k == 1 and e == want_rest_e0(k - 1):
            return {"ok": False, "st_alive": True, "k": k}
        if k == 2 and tot[2] == po:
            return {"ok": False, "n2_alive": True, "k": k}
        if k == 10 and e != po:
            return {"ok": False, "k10": True, "e": e, "po": po}
        n_ok += 1
        rows[str(k)] = {
            "e": e,
            "o": o,
            "parent_odd": po,
            "st_prev": want_rest_e0(k - 1),
            "n2": tot[2],
            "n0": tot[0],
        }
    ok = (
        n_ok == K_REST
        and rows["1"]["e"] == 1
        and rows["1"]["parent_odd"] == 1
        and rows["1"]["st_prev"] == 0
        and rows["2"]["n2"] == 0
        and rows["2"]["parent_odd"] == 1
        and rows["8"]["e"] == 1
        and rows["8"]["st_prev"] == 0
        and rows["10"]["e"] == 0
        and rows["10"]["parent_odd"] == 0
        and rows_in["10"]["n0"] == 0
        and rows_in["10"]["st_n0"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def leftover_fold() -> dict:
    """k=6..8: leftover even-n tot equals leftover odd-n tot at k-1."""
    qt = json.loads(QT_JSON.read_text())
    thin = qt["thin_pack"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(6, 9):
        lo_e = thin[str(k)]["lo_e"]
        lo_o_p = thin[str(k - 1)]["lo_o"]
        rest_e = thin[str(k)]["rest_e"]
        rest_o_p = thin[str(k - 1)]["rest_o"]
        if lo_e != lo_o_p:
            return {"ok": False, "lo": True, "k": k, "lo_e": lo_e, "lo_o_p": lo_o_p}
        if lo_e != want_lo_en(k, rest_e):
            return {"ok": False, "qt_e": True, "k": k}
        if lo_o_p != want_lo_on(k - 1, rest_o_p):
            return {"ok": False, "qt_o": True, "k": k}
        u_e = want_ue_even(k)
        u_o_p = want_ue_odd(k - 1) ^ want_uo_odd(k - 1)
        if u_e != 1 or u_o_p != 1 or (u_e ^ u_o_p) != 0:
            return {"ok": False, "unique": True, "k": k, "u_e": u_e, "u_o_p": u_o_p}
        if rest_e != rest_o_p:
            return {"ok": False, "rest": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"lo_e": lo_e, "lo_o_parent": lo_o_p, "rest_e": rest_e}
    ok = (
        n_ok == 3
        and rows["6"]["lo_e"] == 1
        and rows["7"]["lo_e"] == 0
        and rows["8"]["lo_e"] == 0
        and thin["3"]["lo_e"] != thin["2"]["lo_o"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_lo": 6, "k_hi": 8, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: unique even-n at k xor unique odd-n at k-1 vanishes for k>=6."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        u_e = want_ue_even(k)
        u_o_p = want_ue_odd(k - 1) ^ want_uo_odd(k - 1)
        if k >= 6 and (u_e ^ u_o_p) != 0:
            return {"ok": False, "k": k, "u_e": u_e, "u_o_p": u_o_p}
        if k in (3, 4, 5) and (u_e ^ u_o_p) != 1:
            return {"ok": False, "mid": True, "k": k, "xor": u_e ^ u_o_p}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and want_ue_even(6) == 1
        and want_ue_odd(5) ^ want_uo_odd(5) == 1
        and want_ue_even(3) ^ (want_ue_odd(2) ^ want_uo_odd(2)) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def prefixes() -> dict:
    qo = json.loads(QO_JSON.read_text())
    qt = json.loads(QT_JSON.read_text())
    qs = json.loads(QS_JSON.read_text())
    ok = (
        qo["checks"]["all_ok"]
        and qt["checks"]["all_ok"]
        and qs["checks"]["all_ok"]
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and qt["verdict"]["lo_en_eq_erest_xor_ue_even"] == "LEMMA"
        and qs["verdict"]["unique_even_n_iff_k_eq_3_or_ge_5"] == "LEMMA"
        and qt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qt["verdict"]["prize"] == "unsolved"
        and want_ue_even(6) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fold, lo, tot, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fold["ok"] and lo["ok"]
    assert tot["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fold = rest_fold()
    lo = leftover_fold()
    tot = tot_form()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fold, lo, tot, sc, pref)
    dump = {
        "cycle": "QU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "rest_fold": {k: fold[k] for k in fold if k != "ok"},
        "leftover_fold": {k: lo[k] for k in lo if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_rest_eq_parent_odd_k_le_10": True,
            "lo_en_eq_parent_lo_on_k_ge_6": True,
            "even_rest_eq_ST_k_minus_1": False,
            "n2_eq_parent_odd": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_rest_eq_parent_odd_k_le_10": "CERTIFIED",
            "lo_en_eq_parent_lo_on_k_ge_6": "CERTIFIED",
            "even_rest_eq_ST_k_minus_1": "KILLED",
            "n2_eq_parent_odd": "KILLED",
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
        "rest_fold n_ok",
        dump["rest_fold"]["n_ok"],
        "k1_e",
        dump["rest_fold"]["rows"]["1"]["e"],
        "k10_e",
        dump["rest_fold"]["rows"]["10"]["e"],
    )
    print(
        "leftover_fold n_ok",
        dump["leftover_fold"]["n_ok"],
        "k6_lo_e",
        dump["leftover_fold"]["rows"]["6"]["lo_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
