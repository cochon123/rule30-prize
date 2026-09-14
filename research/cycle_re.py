#!/usr/bin/env python3
"""Cycle RE: covering silent xor leftover n%4 is (1,1,1,0) for every k>=6.

Silent xor leftover on a residue is Green xor unique. Cycle QY Green
n%4 is (0,1,1,1) for k>=3 and Cycle RB unique n%4 is (1,0,0,1) for
k>=6, so the xor is (1,1,1,0). Unique n2 tot is 0, so silent xor
leftover on n%4==2 equals Green n2 tot for every k. Not the tuple
(1,1,1,0) for all k (k=0 is (1,0,0,1)). Not silent equals leftover
on all residues for k>=6 (only n%4==3 agrees). Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_re.py --certify
Dump: research/cycle_re.json
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
from cycle_qx import want_g_n0, want_g_n1, want_g_n2, want_g_n3
from cycle_rb import want_u_n0, want_u_n1, want_u_n2, want_u_n3, want_u_nmod
from cycle_rc import want_lo_n0, want_lo_n1, want_lo_n2, want_lo_n3
from cycle_rd import want_sil_eq_lo_n3

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
RD_JSON = Path(__file__).resolve().parent / "cycle_rd.json"
RB_JSON = Path(__file__).resolve().parent / "cycle_rb.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_g_nmod(k: int) -> list[int]:
    return [want_g_n0(k), want_g_n1(k), want_g_n2(k), want_g_n3(k)]


def want_sil_xor_lo(k: int) -> list[int]:
    """Silent xor leftover n%4: Green xor unique."""
    return [want_g_nmod(k)[i] ^ want_u_nmod(k)[i] for i in range(4)]


def tot_form() -> dict:
    """k<=K_ALG: xor is Green xor unique; k>=6 is (1,1,1,0); n2 equals Green n2."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        got = want_sil_xor_lo(k)
        want = [
            want_g_n0(k) ^ want_u_n0(k),
            want_g_n1(k) ^ want_u_n1(k),
            want_g_n2(k) ^ want_u_n2(k),
            want_g_n3(k) ^ want_u_n3(k),
        ]
        if got != want:
            return {"ok": False, "xor": True, "k": k, "got": got}
        if got[0] != int(k != 4):
            return {"ok": False, "n0": True, "k": k}
        if got[1] != int(k == 1 or k >= 6):
            return {"ok": False, "n1": True, "k": k}
        if got[2] != want_g_n2(k):
            return {"ok": False, "n2": True, "k": k}
        if got[3] != (1 ^ want_u_n3(k)):
            return {"ok": False, "n3": True, "k": k}
        if got[3] != (1 ^ want_sil_eq_lo_n3(k)):
            return {"ok": False, "rd": True, "k": k}
        if k >= 6 and got != [1, 1, 1, 0]:
            return {"ok": False, "ge6": True, "k": k, "got": got}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_sil_xor_lo(0) == [1, 0, 0, 1]
        and want_sil_xor_lo(4) == [0, 0, 1, 0]
        and want_sil_xor_lo(6) == [1, 1, 1, 0]
        and want_g_nmod(6) == [0, 1, 1, 1]
        and want_u_nmod(6) == [1, 0, 0, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def rest_split() -> dict:
    """k<=10: QO packed rest, Green, unique give silent xor leftover."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        tot = rows_in[str(k)]["tot"]
        g = want_g_nmod(k)
        u = want_u_nmod(k)
        sil = [g[i] ^ tot[i] for i in range(4)]
        lo = [
            want_lo_n0(k, tot[0]),
            want_lo_n1(k, tot[1]),
            want_lo_n2(k, tot[2]),
            want_lo_n3(k, tot[3]),
        ]
        xor = [sil[i] ^ lo[i] for i in range(4)]
        if xor != want_sil_xor_lo(k):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        if xor != [g[i] ^ u[i] for i in range(4)]:
            return {"ok": False, "gu": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"sil": sil, "lo": lo, "xor": xor}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["xor"] == [1, 0, 0, 1]
        and rows["4"]["xor"] == [0, 0, 1, 0]
        and rows["6"]["xor"] == [1, 1, 1, 0]
        and rows["10"]["xor"] == [1, 1, 1, 0]
        and rows["6"]["sil"][3] == rows["6"]["lo"][3]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """Tuple (1,1,1,0) for all k; silent equals leftover on all residues k>=6."""
    x0 = want_sil_xor_lo(0)
    x3 = want_sil_xor_lo(3)
    x6 = want_sil_xor_lo(6)
    ok = (
        x0 == [1, 0, 0, 1]
        and x0 != [1, 1, 1, 0]
        and x3 == [1, 0, 1, 1]
        and x3 != [1, 1, 1, 0]
        and x6 == [1, 1, 1, 0]
        and x6[0] == 1
        and x6[3] == 0
        and want_sil_eq_lo_n3(6) == 1
    )
    return {"ok": ok, "x0": x0, "x3": x3, "x6": x6}


def prefixes() -> dict:
    qy = json.loads(QY_JSON.read_text())
    rb = json.loads(RB_JSON.read_text())
    rd = json.loads(RD_JSON.read_text())
    ok = (
        qy["checks"]["all_ok"]
        and rb["checks"]["all_ok"]
        and rd["checks"]["all_ok"]
        and qy["verdict"]["green_nmod_0111_k_ge_3"] == "LEMMA"
        and rb["verdict"]["unique_n2_0"] == "LEMMA"
        and rd["verdict"]["sil_n3_eq_lo_n3_iff_k_eq_4_or_ge_6"] == "LEMMA"
        and qy["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and rb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rb["verdict"]["prize"] == "unsolved"
        and want_sil_xor_lo(6) == [1, 1, 1, 0]
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, split, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and split["ok"]
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
    split = rest_split()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, split, kl, sc, pref)
    dump = {
        "cycle": "RE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "rest_split": {k: split[k] for k in split if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "sil_xor_lo_1110_k_ge_6": True,
            "sil_xor_lo_n2_eq_green_n2": True,
            "sil_xor_lo_1110_all_k": False,
            "sil_eq_lo_all_res_k_ge_6": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "sil_xor_lo_1110_k_ge_6": "LEMMA",
            "sil_xor_lo_n2_eq_green_n2": "LEMMA",
            "sil_xor_lo_1110_all_k": "KILLED",
            "sil_eq_lo_all_res_k_ge_6": "KILLED",
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
        "rest_split n_ok",
        dump["rest_split"]["n_ok"],
        "k0",
        dump["rest_split"]["rows"]["0"]["xor"],
        "k6",
        dump["rest_split"]["rows"]["6"]["xor"],
        "k10",
        dump["rest_split"]["rows"]["10"]["xor"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
