#!/usr/bin/env python3
"""Cycle RB: covering UNIQUE_REST packed AND xor on n%4==2 is 0 for every k.

UNIQUE_EVEN n%4 xor UNIQUE_ODD n%4 is unique packed tot by n%4.
Cycle RA n2 tot is 0 and Cycle QR UNIQUE_ODD even tot is 0, so
unique n2 tot is 0. Unique n0 tot equals UNIQUE_EVEN even tot
(1 iff k==3 or k>=5). Unique n1 tot equals unique even packed tot
(1 iff k in {3,4,5}). Unique n3 tot equals UNIQUE_EVEN odd tot
(1 iff k==4 or k>=6). They xor to Cycle QF unique packed tot 0.
Not unique n0 tot equals unique even packed tot (k=4: 0 vs 1).
Not unique n3 tot equals unique odd packed tot (k=6: 1 vs 0).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rb.py --certify
Dump: research/cycle_rb.json
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
from cycle_qp import want_unique_even_pack, want_unique_odd_pack
from cycle_qs import want_ue_even, want_ue_odd
from cycle_qz import want_uo_n1, want_uo_n3
from cycle_ra import want_ue_n0, want_ue_n1, want_ue_n2, want_ue_n3

OUT = Path(__file__).resolve().with_suffix(".json")
RA_JSON = Path(__file__).resolve().parent / "cycle_ra.json"
QZ_JSON = Path(__file__).resolve().parent / "cycle_qz.json"
QP_JSON = Path(__file__).resolve().parent / "cycle_qp.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_ALG = 64


def want_u_n0(k: int) -> int:
    """UNIQUE_REST packed AND xor on n%4==0, all k: 1 iff k==3 or k>=5."""
    return want_ue_even(k)


def want_u_n1(k: int) -> int:
    """UNIQUE_REST packed AND xor on n%4==1, all k: 1 iff k in {3,4,5}."""
    return want_unique_even_pack(k)


def want_u_n2(k: int) -> int:
    """UNIQUE_REST packed AND xor on n%4==2, all k: 0."""
    return 0


def want_u_n3(k: int) -> int:
    """UNIQUE_REST packed AND xor on n%4==3, all k: 1 iff k==4 or k>=6."""
    return want_ue_odd(k)


def want_u_nmod(k: int) -> list[int]:
    return [want_u_n0(k), want_u_n1(k), want_u_n2(k), want_u_n3(k)]


def tot_form() -> dict:
    """k<=K_ALG: unique n%4 is UE n%4 xor UO n%4; closed forms; tot 0."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        got = [
            want_ue_n0(k) ^ 0,
            want_ue_n1(k) ^ want_uo_n1(k),
            want_ue_n2(k),
            want_ue_n3(k) ^ want_uo_n3(k),
        ]
        want = want_u_nmod(k)
        if got != want:
            return {"ok": False, "xor": True, "k": k, "got": got, "want": want}
        if want[0] != want_ue_even(k) or want[2] != 0:
            return {"ok": False, "even": True, "k": k}
        if want[1] != want_unique_even_pack(k):
            return {"ok": False, "n1": True, "k": k}
        if want[1] != want_unique_odd_pack(k):
            return {"ok": False, "n1o": True, "k": k}
        if want[3] != want_ue_odd(k):
            return {"ok": False, "n3": True, "k": k}
        if want[0] ^ want[1] ^ want[2] ^ want[3] != 0:
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_u_n0(3) == 1
        and want_u_n0(4) == 0
        and want_u_n0(6) == 1
        and want_u_n1(3) == 1
        and want_u_n1(6) == 0
        and want_u_n2(6) == 0
        and want_u_n3(4) == 1
        and want_u_n3(5) == 0
        and want_u_n3(6) == 1
        and want_u_nmod(6) == [1, 0, 0, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def dump_xor() -> dict:
    """RA xor QZ packed n%4 dumps: unique n%4 through k<=8; freeze k>=6."""
    ra = json.loads(RA_JSON.read_text())
    qz = json.loads(QZ_JSON.read_text())
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        ue = ra["thin_pack"]["rows"][str(k)]["tot"]
        uo = qz["thin_pack"]["rows"][str(k)]["tot"]
        tot = [ue[i] ^ uo[i] for i in range(4)]
        if tot != want_u_nmod(k):
            return {"ok": False, "thin": True, "k": k, "tot": tot}
        n_ok += 1
        rows[str(k)] = {"tot": tot, "ue": ue, "uo": uo}
    freeze_ok = 0
    freeze_rows = {}
    for k in (6, 7, 8, 10, 12):
        ue = ra["even_n_split"]["rows"][str(k)]["tot"]
        w = qz["odd_n_split"]["rows"][str(k)]
        uo = [0, w["n1"], 0, w["n3"]]
        tot = [ue[i] ^ uo[i] for i in range(4)]
        if tot != want_u_nmod(k) or tot != [1, 0, 0, 1]:
            return {"ok": False, "freeze": True, "k": k, "tot": tot}
        freeze_ok += 1
        freeze_rows[str(k)] = {"tot": tot}
    ok = (
        n_ok == K_THIN + 1
        and freeze_ok == 5
        and rows["0"]["tot"] == [0, 0, 0, 0]
        and rows["3"]["tot"] == [1, 1, 0, 0]
        and rows["4"]["tot"] == [0, 1, 0, 1]
        and rows["6"]["tot"] == [1, 0, 0, 1]
        and freeze_rows["12"]["tot"] == [1, 0, 0, 1]
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_THIN,
        "rows": rows,
        "freeze_ok": freeze_ok,
        "freeze_rows": freeze_rows,
    }


def killed_eq() -> dict:
    """Unique n0 equals unique even packed tot; unique n3 equals unique odd tot."""
    ok = (
        want_u_n0(4) == 0
        and want_unique_even_pack(4) == 1
        and want_u_n3(6) == 1
        and want_unique_odd_pack(6) == 0
        and want_u_n1(6) == 0
        and want_ue_n1(6) == 1
    )
    return {"ok": ok, "n0_4": 0, "pack_4": 1, "n3_6": 1, "odd_6": 0, "n1_6": 0}


def prefixes() -> dict:
    ra = json.loads(RA_JSON.read_text())
    qz = json.loads(QZ_JSON.read_text())
    qp = json.loads(QP_JSON.read_text())
    ok = (
        ra["checks"]["all_ok"]
        and qz["checks"]["all_ok"]
        and qp["checks"]["all_ok"]
        and ra["verdict"]["unique_even_n2_0"] == "LEMMA"
        and ra["verdict"]["unique_even_n1_iff_k_ge_2"] == "LEMMA"
        and qz["verdict"]["unique_odd_n3_iff_k_ge_2"] == "LEMMA"
        and qp["verdict"]["unique_even_pack_iff_k_in_3_4_5"] == "LEMMA"
        and ra["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ra["verdict"]["prize"] == "unsolved"
        and want_u_n2(6) == 0
        and want_u_nmod(4) == [0, 1, 0, 1]
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, dump, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and dump["ok"]
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
    dumpx = dump_xor()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, dumpx, kl, sc, pref)
    dump = {
        "cycle": "RB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "dump_xor": {k: dumpx[k] for k in dumpx if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_n2_0": True,
            "unique_n0_iff_k_eq_3_or_ge_5": True,
            "unique_n1_iff_k_in_3_4_5": True,
            "unique_n3_iff_k_eq_4_or_ge_6": True,
            "unique_n0_eq_even_pack": False,
            "unique_n3_eq_odd_pack": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_n2_0": "LEMMA",
            "unique_n0_iff_k_eq_3_or_ge_5": "LEMMA",
            "unique_n1_iff_k_in_3_4_5": "LEMMA",
            "unique_n3_iff_k_eq_4_or_ge_6": "LEMMA",
            "unique_n0_eq_even_pack": "KILLED",
            "unique_n3_eq_odd_pack": "KILLED",
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
        "dump_xor n_ok",
        dump["dump_xor"]["n_ok"],
        "k4",
        dump["dump_xor"]["rows"]["4"]["tot"],
        "k6",
        dump["dump_xor"]["rows"]["6"]["tot"],
        "freeze12",
        dump["dump_xor"]["freeze_rows"]["12"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
