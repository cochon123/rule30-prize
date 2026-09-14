#!/usr/bin/env python3
"""Cycle RP: UNIQUE_EVEN Green n%4 is (0,1,1,1) for every k>=6.

Cycle RN unique Green n%4 is (0,1,1,0) for k>=6. Cycle RO UNIQUE_ODD
Green n%4 is (0,0,0,1). Their xor is UNIQUE_EVEN Green (0,1,1,1).
Cycle QK UNIQUE_EVEN odd-n tot is 0, so n%4==1 tot equals n%4==3 tot,
1 iff k>=2 and k!=4. Even tot is UNIQUE_EVEN tot, 1 iff k==3 or k>=6.
Not that tuple for all k (k=2 is (1,1,1,1); k=4 is (0,0,0,0)). Not
UNIQUE_EVEN Green n%4 equals packed UNIQUE_EVEN n%4 (packed k>=6 is
(1,1,0,0)). Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_rp.py --certify
Dump: research/cycle_rp.json
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
from cycle_qj import UNIQUE_EVEN, want_unique_even
from cycle_ra import want_ue_n0, want_ue_n1, want_ue_n2, want_ue_n3
from cycle_rk import want_u_even_n
from cycle_rm import want_u_g_n0, want_u_g_n2, want_u_g_nmod
from cycle_ro import (
    gxor_nmod,
    want_ue_g_nmod,
    want_uo_g_nmod,
)

OUT = Path(__file__).resolve().with_suffix(".json")
RO_JSON = Path(__file__).resolve().parent / "cycle_ro.json"
RN_JSON = Path(__file__).resolve().parent / "cycle_rn.json"
QK_JSON = Path(__file__).resolve().parent / "cycle_qk.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64


def want_ue_g_n0(k: int) -> int:
    """UNIQUE_EVEN Green xor on n%4==0: 1 iff k in {2,3,5}."""
    return want_u_g_n0(k)


def want_ue_g_n1(k: int) -> int:
    """UNIQUE_EVEN Green xor on n%4==1: 1 iff k>=2 and k!=4."""
    return int(k >= 2 and k != 4)


def want_ue_g_n2(k: int) -> int:
    """UNIQUE_EVEN Green xor on n%4==2: 1 iff k==2 or k>=5."""
    return want_u_g_n2(k)


def want_ue_g_n3(k: int) -> int:
    """UNIQUE_EVEN Green xor on n%4==3: equals n1 tot (QK odd-n tot 0)."""
    return want_ue_g_n1(k)


def want_ue_g_parts(k: int) -> list[int]:
    return [want_ue_g_n0(k), want_ue_g_n1(k), want_ue_g_n2(k), want_ue_g_n3(k)]


def want_ue_pack_nmod(k: int) -> list[int]:
    return [want_ue_n0(k), want_ue_n1(k), want_ue_n2(k), want_ue_n3(k)]


def tot_form() -> dict:
    """k<=K_ALG: UNIQUE_EVEN Green n%4 is unique xor UO; k>=6 is (0,1,1,1)."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        ue = want_ue_g_nmod(k)
        parts = want_ue_g_parts(k)
        if ue != parts:
            return {"ok": False, "parts": True, "k": k, "ue": ue, "parts": parts}
        u = want_u_g_nmod(k)
        uo = want_uo_g_nmod(k)
        xor = [u[i] ^ uo[i] for i in range(4)]
        if ue != xor:
            return {"ok": False, "xor": True, "k": k, "ue": ue}
        if ue[1] != ue[3]:
            return {"ok": False, "n13": True, "k": k, "ue": ue}
        if (ue[0] ^ ue[2]) != want_unique_even(k):
            return {"ok": False, "even": True, "k": k, "ue": ue}
        if (ue[0] ^ ue[2]) != want_u_even_n(k):
            return {"ok": False, "rk": True, "k": k}
        if k >= 6 and ue != [0, 1, 1, 1]:
            return {"ok": False, "ge6": True, "k": k, "ue": ue}
        if k >= 6 and u != [0, 1, 1, 0]:
            return {"ok": False, "rn": True, "k": k}
        if k >= 6 and uo != [0, 0, 0, 1]:
            return {"ok": False, "ro": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ue_g_nmod(0) == [0, 0, 0, 0]
        and want_ue_g_nmod(2) == [1, 1, 1, 1]
        and want_ue_g_nmod(4) == [0, 0, 0, 0]
        and want_ue_g_nmod(5) == [1, 1, 1, 1]
        and want_ue_g_nmod(6) == [0, 1, 1, 1]
        and want_ue_g_n1(4) == 0
        and want_ue_g_n1(6) == 1
        and want_ue_pack_nmod(6) == [1, 1, 0, 0]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ue_walk() -> dict:
    """k<=K_CHK: UNIQUE_EVEN Green n%4 matches the closed form."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        tot = [0, 0, 0, 0]
        for p in UNIQUE_EVEN:
            got = gxor_nmod(p, k)
            for i in range(4):
                tot[i] ^= got[i]
        if tot != want_ue_g_nmod(k):
            return {"ok": False, "form": True, "k": k, "tot": tot}
        n_ok += 1
        rows[str(k)] = tot
    ok = (
        n_ok == K_CHK + 1
        and rows["0"] == [0, 0, 0, 0]
        and rows["2"] == [1, 1, 1, 1]
        and rows["3"] == [1, 1, 0, 1]
        and rows["4"] == [0, 0, 0, 0]
        and rows["5"] == [1, 1, 1, 1]
        and rows["6"] == [0, 1, 1, 1]
        and rows["8"] == [0, 1, 1, 1]
        and UNIQUE_EVEN == (16, 32, 52, 60, 72, 76, 88)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def killed_eq() -> dict:
    """UNIQUE_EVEN Green n%4==(0,1,1,1) all k; Green n%4 equals packed."""
    g2 = want_ue_g_nmod(2)
    g4 = want_ue_g_nmod(4)
    g6 = want_ue_g_nmod(6)
    p6 = want_ue_pack_nmod(6)
    ok = (
        g2 == [1, 1, 1, 1]
        and g2 != [0, 1, 1, 1]
        and g4 == [0, 0, 0, 0]
        and g4 != [0, 1, 1, 1]
        and g6 == [0, 1, 1, 1]
        and p6 == [1, 1, 0, 0]
        and g6 != p6
        and want_ue_g_nmod(8) != want_ue_pack_nmod(8)
    )
    return {"ok": ok, "g2": g2, "g4": g4, "g6": g6, "p6": p6}


def prefixes() -> dict:
    ro = json.loads(RO_JSON.read_text())
    rn = json.loads(RN_JSON.read_text())
    qk = json.loads(QK_JSON.read_text())
    ok = (
        ro["checks"]["all_ok"]
        and rn["checks"]["all_ok"]
        and qk["checks"]["all_ok"]
        and ro["verdict"]["uo_g_nmod_0001_k_ge_6"] == "LEMMA"
        and rn["verdict"]["u_g_nmod_0110_k_ge_6"] == "LEMMA"
        and qk["verdict"]["unique_even_odd_n_0"] == "LEMMA"
        and ro["verdict"]["uo_g_nmod_0001_all_k"] == "KILLED"
        and rn["verdict"]["u_g_nmod_eq_packed"] == "KILLED"
        and ro["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ro["verdict"]["prize"] == "unsolved"
        and want_ue_g_nmod(6) == [0, 1, 1, 1]
        and want_u_g_nmod(6) == [0, 1, 1, 0]
        and want_uo_g_nmod(6) == [0, 0, 0, 1]
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and walk["ok"]
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
    walk = ue_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "RP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ue_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ue_g_nmod_0111_k_ge_6": True,
            "ue_g_n1_eq_n3": True,
            "ue_g_n1_iff_k_ge_2_ne_4": True,
            "ue_g_nmod_0111_all_k": False,
            "ue_g_nmod_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ue_g_nmod_0111_k_ge_6": "LEMMA",
            "ue_g_n1_eq_n3": "LEMMA",
            "ue_g_n1_iff_k_ge_2_ne_4": "LEMMA",
            "ue_g_nmod_0111_all_k": "KILLED",
            "ue_g_nmod_eq_packed": "KILLED",
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
        "ue_walk n_ok",
        dump["ue_walk"]["n_ok"],
        "ue6",
        dump["ue_walk"]["rows"]["6"],
        "ue2",
        dump["ue_walk"]["rows"]["2"],
        "ue4",
        dump["ue_walk"]["rows"]["4"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
