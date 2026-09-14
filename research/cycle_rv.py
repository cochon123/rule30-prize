#!/usr/bin/env python3
"""Cycle RV: covering Green forced n%4 is (0,1,1,1) except k=1,2.

Green rest is clipped G=1 xor forced. Cycle QY G=1 on n%4==1 at k
equals even-n G=1 at k-1, so Cycle RU's n1 rest equals parent even
rest iff forced n1 tot equals parent even forced tot. Forced n1 tot
is 1 for every k, and parent even forced tot is 1 for every k>=0, so
they agree. Dual: forced n3 tot is 1 iff k not in {1,2}; xor parent
odd forced tot is 1 iff k==2 or k>=4, the same bit as Cycle RU's
n3 rest xor. Forced nmod is (0,1,1,1) at k=0 and every k>=3, but
(1,1,0,0) at k=1 and (0,1,1,0) at k=2. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rv.py --certify
Dump: research/cycle_rv.json
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
from cycle_qx import want_g1_n0, want_g1_n2
from cycle_qy import want_g1_n1, want_g1_n3
from cycle_ru import want_g_n1_xor_parent_even, want_g_n3_xor_parent_odd

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
RU_JSON = Path(__file__).resolve().parent / "cycle_ru.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_WALK = 8


def want_f_n0(k: int) -> int:
    """Green forced xor on n%4==0: 1 iff k==1, all k."""
    return int(k == 1)


def want_f_n1(k: int) -> int:
    """Green forced xor on n%4==1: 1 for every k."""
    return 1


def want_f_n2(k: int) -> int:
    """Green forced xor on n%4==2: 1 iff k!=1, all k."""
    return int(k != 1)


def want_f_n3(k: int) -> int:
    """Green forced xor on n%4==3: 1 iff k not in {1,2}, all k."""
    return int(k not in (1, 2))


def want_f_nmod(k: int) -> list[int]:
    """Green forced xor by n%4, all k."""
    return [want_f_n0(k), want_f_n1(k), want_f_n2(k), want_f_n3(k)]


def want_f_n1_xor_parent_even(k: int) -> int:
    """Forced n1 tot xor parent even forced tot, all k: 0 for k>=1."""
    if k < 1:
        return 0
    return want_f_n1(k) ^ want_f_n0(k - 1) ^ want_f_n2(k - 1)


def want_f_n3_xor_parent_odd(k: int) -> int:
    """Forced n3 tot xor parent odd forced tot, all k: 1 iff k==2 or k>=4."""
    if k < 1:
        return 0
    return want_f_n3(k) ^ want_f_n1(k - 1) ^ want_f_n3(k - 1)


def g1_of(k: int) -> list[int]:
    return [want_g1_n0(k), want_g1_n1(k), want_g1_n2(k), want_g1_n3(k)]


def rest_of(k: int) -> list[int]:
    return [want_g_n0(k), want_g_n1(k), want_g_n2(k), want_g_n3(k)]


def walk_chk() -> dict:
    """k<=8: QX walk g1 xor rest equals forced nmod closed form."""
    qx = json.loads(QX_JSON.read_text())
    rows_in = qx["green_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_WALK + 1):
        tot = rows_in[str(k)]["tot"]
        g1 = rows_in[str(k)]["g1"]
        got = [g1[i] ^ tot[i] for i in range(4)]
        want = want_f_nmod(k)
        if got != want:
            return {"ok": False, "form": True, "k": k, "got": got, "want": want}
        if got != [a ^ b for a, b in zip(g1_of(k), rest_of(k))]:
            return {"ok": False, "closed": True, "k": k, "got": got}
        n_ok += 1
        rows[str(k)] = {"forced": got}
    ok = (
        n_ok == K_WALK + 1
        and rows["0"]["forced"] == [0, 1, 1, 1]
        and rows["1"]["forced"] == [1, 1, 0, 0]
        and rows["2"]["forced"] == [0, 1, 1, 0]
        and rows["3"]["forced"] == [0, 1, 1, 1]
        and rows["8"]["forced"] == [0, 1, 1, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_WALK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: forced = g1 xor rest; n1 equals parent even forced."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        got = [a ^ b for a, b in zip(g1_of(k), rest_of(k))]
        want = want_f_nmod(k)
        if got != want:
            return {"ok": False, "form": True, "k": k, "got": got, "want": want}
        if k >= 1:
            pe = want_f_n0(k - 1) ^ want_f_n2(k - 1)
            if want_f_n1(k) != pe:
                return {"ok": False, "n1": True, "k": k, "pe": pe}
            if want_f_n1_xor_parent_even(k) != 0:
                return {"ok": False, "n1xor": True, "k": k}
            po = want_f_n1(k - 1) ^ want_f_n3(k - 1)
            got3 = want_f_n3(k) ^ po
            if got3 != want_f_n3_xor_parent_odd(k):
                return {"ok": False, "n3": True, "k": k, "got3": got3}
            if got3 != int(k == 2 or k >= 4):
                return {"ok": False, "n3form": True, "k": k, "got3": got3}
            if got3 != want_g_n3_xor_parent_odd(k):
                return {"ok": False, "ru": True, "k": k, "got3": got3}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_f_n1(0) == 1
        and want_f_n1(1) == 1
        and want_f_n1(64) == 1
        and want_f_n0(1) == 1
        and want_f_n0(2) == 0
        and want_f_n2(0) == 1
        and want_f_n2(1) == 0
        and want_f_n3(0) == 1
        and want_f_n3(1) == 0
        and want_f_n3(2) == 0
        and want_f_n3(3) == 1
        and want_f_n1_xor_parent_even(1) == 0
        and want_f_n3_xor_parent_odd(2) == 1
        and want_f_n3_xor_parent_odd(3) == 0
        and want_f_n3_xor_parent_odd(4) == 1
        and want_g_n1_xor_parent_even(2) == 0
        and want_f_nmod(1) != [0, 1, 1, 1]
        and want_f_nmod(2) != [0, 1, 1, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Forced nmod is (0,1,1,1) for all k; n3 forced equals parent odd forced."""
    po1 = want_f_n1(1) ^ want_f_n3(1)
    ok = (
        want_f_nmod(1) != [0, 1, 1, 1]
        and want_f_nmod(2) != [0, 1, 1, 1]
        and want_f_n3(2) != po1
        and want_f_n3(4) != (want_f_n1(3) ^ want_f_n3(3))
        and want_f_n1_xor_parent_even(2) == 0
        and want_g_n3_xor_parent_odd(2) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    ru = json.loads(RU_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and ru["checks"]["all_ok"]
        and qx["verdict"]["green_n0_iff_k_le_2"] == "LEMMA"
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and qy["verdict"]["g1_n1_eq_parent_even"] == "LEMMA"
        and qy["verdict"]["g1_n3_eq_parent_odd"] == "LEMMA"
        and ru["verdict"]["g_n1_eq_parent_even"] == "LEMMA"
        and qy["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and ru["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ru["verdict"]["prize"] == "unsolved"
        and want_f_n1(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and walk["ok"] and tot["ok"]
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
    walk = walk_chk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "RV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "walk_chk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "f_n1_all_k": True,
            "f_n1_eq_parent_even": True,
            "f_n3_xor_parent_odd_iff_k_eq_2_or_ge_4": True,
            "f_nmod_0111_all_k": False,
            "f_n3_eq_parent_odd": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "f_n1_all_k": "LEMMA",
            "f_n1_eq_parent_even": "LEMMA",
            "f_n3_xor_parent_odd_iff_k_eq_2_or_ge_4": "LEMMA",
            "f_nmod_0111_all_k": "KILLED",
            "f_n3_eq_parent_odd": "KILLED",
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
        "tot_form n_ok",
        dump["tot_form"]["n_ok"],
        "walk n_ok",
        dump["walk_chk"]["n_ok"],
        "f1",
        want_f_n1(0),
        "n3xor2",
        want_f_n3_xor_parent_odd(2),
        "n3xor3",
        want_f_n3_xor_parent_odd(3),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
