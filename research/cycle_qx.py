#!/usr/bin/env python3
"""Cycle QX: covering Green rest n%4 is (0,1,1,1) for k>=3.

Cycle QV twice sends n%4==0 clipped G=1 at k to all clipped G=1 at
k-2, so that xor is Cycle QH clip xor at k-2, 1 iff k==2. Forced
p=6 and p=14 have odd j for k>=1, and Cycle PC's even-n p=4 is
n=3U-2, which has n%4==2 for k>=2 (at k=1 it is n%4==0), so n%4==0
has no forced cell for k>=2. Green rest on n%4==0 is 1 iff k<=2.
n%4==2 G=1 xor is odd G=1 xor at k-1, and xor the unique p=4 cell
for k>=2 gives Green n%4==2 rest 1 iff k==1 or k>=3.
For 3<=k<=8 Green rest n%4 is (0,1,1,1): each of n%4 in {1,2,3} has
xor 1, and n%4==3 is 1 at every k<=8. Packed n%4 is not this tuple
(k=3 packed is (0,0,0,0)). Not rest=S xor T for all k. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qx.py --certify
Dump: research/cycle_qx.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qh import want_clip_g1, want_green_rest
from cycle_qv import even_slots
from cycle_qw import want_g1_even, want_green_even, want_green_odd, want_p4_even

OUT = Path(__file__).resolve().with_suffix(".json")
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"

N_PAL = 64
M_SLOTS = 64
K_GREEN = 8
K_ALG = 64
Q = 10


def want_g_n0(k: int) -> int:
    """Green rest on n%4==0: 1 iff k<=2, all k."""
    return int(k <= 2)


def want_g_n1(k: int) -> int:
    """Green rest on n%4==1: 1 iff k==1 or k>=3, certified k<=8."""
    return int(k == 1 or k >= 3)


def want_g_n2(k: int) -> int:
    """Green rest on n%4==2: 1 iff k==1 or k>=3, all k."""
    return int(k == 1 or k >= 3)


def want_g_n3(k: int) -> int:
    """Green rest on n%4==3: 1 at every k<=8."""
    return 1


def want_g1_n0(k: int) -> int:
    """n%4==0 clipped G=1 xor: clip xor at k-2 for k>=2."""
    if k < 2:
        return int(k == 0)
    return want_clip_g1(k - 2)


def want_g1_n2(k: int) -> int:
    """n%4==2 clipped G=1 xor: odd G=1 xor at k-1."""
    if k < 1:
        return 1
    return want_g1_even(k - 1) ^ want_clip_g1(k - 1)


def green_nmod(k: int) -> dict:
    """Clipped G=1 xor split by n%4, off forced and raw."""
    U = 1 << k
    clip = 5 * U
    tot = [0, 0, 0, 0]
    g1 = [0, 0, 0, 0]
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = Q * U - 2 * j
            g1[n % 4] ^= 1
            if p in FORCED:
                continue
            tot[n % 4] ^= 1
    return {"tot": tot, "g1": g1}


def green_walk() -> dict:
    """k<=8: Green rest n%4 matches the closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_GREEN + 1):
        w = green_nmod(k)
        tot, g1 = w["tot"], w["g1"]
        want = [want_g_n0(k), want_g_n1(k), want_g_n2(k), want_g_n3(k)]
        if tot != want:
            return {"ok": False, "form": True, "k": k, "tot": tot, "want": want}
        if (tot[0] ^ tot[2]) != want_green_even(k):
            return {"ok": False, "even": True, "k": k}
        if (tot[1] ^ tot[3]) != want_green_odd(k):
            return {"ok": False, "odd": True, "k": k}
        if (tot[0] ^ tot[1] ^ tot[2] ^ tot[3]) != want_green_rest(k):
            return {"ok": False, "qh": True, "k": k}
        if k >= 2 and g1[0] != want_g1_n0(k):
            return {"ok": False, "g1n0": True, "k": k, "g1": g1[0]}
        if k >= 1 and g1[2] != want_g1_n2(k):
            return {"ok": False, "g1n2": True, "k": k, "g1": g1[2]}
        if k >= 2 and tot[2] != (g1[2] ^ want_p4_even(k)):
            return {"ok": False, "p4": True, "k": k}
        if k == 1 and tot[2] != g1[2]:
            return {"ok": False, "p4k1": True, "tot": tot[2], "g1": g1[2]}
        if k == 1 and tot[0] != (g1[0] ^ want_p4_even(1)):
            return {"ok": False, "p4n0": True, "tot": tot[0], "g1": g1[0]}
        n_ok += 1
        rows[str(k)] = {"tot": tot, "g1": g1}
    ok = (
        n_ok == K_GREEN + 1
        and rows["0"]["tot"] == [1, 0, 0, 1]
        and rows["2"]["tot"] == [1, 0, 0, 1]
        and rows["3"]["tot"] == [0, 1, 1, 1]
        and rows["8"]["tot"] == [0, 1, 1, 1]
        and all(rows[str(k)]["tot"][3] == 1 for k in range(0, K_GREEN + 1))
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def tot_form() -> dict:
    """k<=64: n0 xor n2 is QW even; n1 xor n3 is QW odd; n0 is clip at k-2."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        n0 = want_g_n0(k)
        n1 = want_g_n1(k)
        n2 = want_g_n2(k)
        n3 = want_g_n3(k)
        if (n0 ^ n2) != want_green_even(k):
            return {"ok": False, "even": True, "k": k}
        if (n1 ^ n3) != want_green_odd(k):
            return {"ok": False, "odd": True, "k": k}
        if (n0 ^ n1 ^ n2 ^ n3) != want_green_rest(k):
            return {"ok": False, "qh": True, "k": k}
        if k >= 2 and n0 != want_clip_g1(k - 2):
            return {"ok": False, "fold": True, "k": k}
        if k >= 3 and [n0, n1, n2, n3] != [0, 1, 1, 1]:
            return {"ok": False, "tuple": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_g_n0(2) == 1
        and want_g_n0(3) == 0
        and want_g_n3(0) == 1
        and want_g_n1(3) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def packed_kill() -> dict:
    """Packed rest n%4 is not Green rest n%4 (k=3 and k=4)."""
    qo = json.loads(QO_JSON.read_text())
    rows = qo["rest_n0_walk"]["rows"]
    p3 = rows["3"]["tot"]
    p4 = rows["4"]["tot"]
    g3 = [want_g_n0(3), want_g_n1(3), want_g_n2(3), want_g_n3(3)]
    g4 = [want_g_n0(4), want_g_n1(4), want_g_n2(4), want_g_n3(4)]
    ok = (
        p3 == [0, 0, 0, 0]
        and g3 == [0, 1, 1, 1]
        and p3 != g3
        and p4 == [1, 1, 1, 1]
        and g4 == [0, 1, 1, 1]
        and p4 != g4
        and rows["2"]["tot"][0] == 1
        and want_g_n0(2) == 1
        and rows["10"]["tot"][0] == 0
        and want_g_n0(10) == 0
        and rows["8"]["tot"][0] == 1
        and want_g_n0(8) == 0
    )
    return {"ok": ok, "p3": p3, "g3": g3, "p4": p4, "g4": g4}


def prefixes() -> dict:
    qw = json.loads(QW_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qw["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qw["verdict"]["green_even_rest_iff_k_ne_1"] == "LEMMA"
        and qw["verdict"]["green_even_eq_packed_even"] == "KILLED"
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and qw["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, walk, tot, kill, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert walk["ok"] and tot["ok"] and kill["ok"] and sc["ok"] and pref["ok"]
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
    walk = green_walk()
    tot = tot_form()
    kill = packed_kill()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, walk, tot, kill, sc, pref)
    dump = {
        "cycle": "QX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "green_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "packed_kill": {k: kill[k] for k in kill if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "green_n0_iff_k_le_2": True,
            "green_n2_iff_k_eq_1_or_ge_3": True,
            "green_nmod_0111_k_ge_3": True,
            "green_nmod_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "green_n0_iff_k_le_2": "LEMMA",
            "green_n2_iff_k_eq_1_or_ge_3": "LEMMA",
            "green_nmod_0111_k_ge_3": "CERTIFIED",
            "green_n3_all_k": "PREFIX",
            "green_nmod_eq_packed": "KILLED",
            "rest_n0_eq_ST_k_minus_2": "KILLED",
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
        "green_walk n_ok",
        dump["green_walk"]["n_ok"],
        "k3",
        dump["green_walk"]["rows"]["3"]["tot"],
        "k8",
        dump["green_walk"]["rows"]["8"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
