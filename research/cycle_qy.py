#!/usr/bin/env python3
"""Cycle QY: covering Green rest on n%4==3 is 1 for every k.

Cycle QH's odd clip identity clip_bit(2m+1,k)=clip_bit(m,k-1) splits
by m parity: child n%4==1 is even m and child n%4==3 is odd m, so
g1 on n%4==1 at k equals even-n G=1 xor at k-1 (1 iff k==2) and g1
on n%4==3 equals odd-n G=1 xor at k-1 (1 iff k<=2). Cycle PC's
forced sets for k>=3 have xor (0,1,1,1) by n%4. Green rest is g1
xor forced, so for k>=3 Green rest n%4 is (0,1,1,1) and Green
n%4==3 rest is 1. The same bit is 1 at k=0,1,2 from Cycle QX's
walk. Packed n%4 is not this tuple. Not rest=S xor T for all k.
Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qy.py --certify
Dump: research/cycle_qy.json
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
from cycle_pc import in_p4, in_p6, in_p14
from cycle_qh import clip_bit, want_clip_g1
from cycle_qv import even_slots
from cycle_qw import want_g1_even, want_green_even, want_green_odd
from cycle_qx import want_g_n0, want_g_n1, want_g_n2, want_g_n3

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"

N_PAL = 64
M_SLOTS = 64
K_CLIP = 8
K_ALG = 64


def want_g1_n1(k: int) -> int:
    """n%4==1 clipped G=1 xor: even-n G=1 xor at k-1."""
    if k < 1:
        return 1
    return want_g1_even(k - 1)


def want_g1_n3(k: int) -> int:
    """n%4==3 clipped G=1 xor: odd-n G=1 xor at k-1."""
    if k < 1:
        return 0
    return want_g1_even(k - 1) ^ want_clip_g1(k - 1)


def want_forced_nmod(k: int) -> list[int]:
    """Forced Green xor by n%4 for k>=3."""
    if k < 3:
        return [0, 0, 0, 0]
    return [0, 1, 1, 1]


def odd_clip_split() -> dict:
    """k=1..8: clip_bit(2m+1,k)=clip_bit(m,k-1); even/odd m are n%4==1,3."""
    n_ok = 0
    rows = {}
    for k in range(1, K_CLIP + 1):
        U = 1 << (k - 1)
        e = o = 0
        for m in range(0, 4 * U):
            if clip_bit(2 * m + 1, k) != clip_bit(m, k - 1):
                return {"ok": False, "id": True, "k": k, "m": m}
            bit = clip_bit(m, k - 1)
            if m % 2 == 0:
                e ^= bit
            else:
                o ^= bit
            n_ok += 1
        if e != want_g1_n1(k) or o != want_g1_n3(k):
            return {"ok": False, "split": True, "k": k, "e": e, "o": o}
        rows[str(k)] = {"e": e, "o": o}
    ok = (
        n_ok > 0
        and rows["1"]["e"] == 0
        and rows["1"]["o"] == 1
        and rows["2"]["e"] == 1
        and rows["2"]["o"] == 1
        and rows["3"]["e"] == 0
        and rows["3"]["o"] == 0
        and rows["8"]["e"] == 0
        and rows["8"]["o"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CLIP, "rows": rows}


def forced_cands(k: int) -> tuple[list[int], list[int], list[int]]:
    """O(k) PC candidates for p=4,6,14."""
    U = 1 << k
    p4 = [4 * U - 1, 3 * U - 1]
    p6 = [4 * U - 1, 3 * U - 1]
    p14 = [4 * U - 3, 3 * U - 1, 3 * U - 3]
    for i in range(0, k):
        p4.append((3 * U - 1) - (1 << i))
        if i >= 1:
            p6.append((3 * U - 1) - (1 << i))
            p14.append((3 * U - 3) - (1 << i))
    return p4, p6, p14


def forced_nmod() -> dict:
    """k>=3: PC forced sets xor to (0,1,1,1) by n%4."""
    n_ok = 0
    for k in range(3, K_ALG + 1):
        U = 1 << k
        acc = [0, 0, 0, 0]
        p4, p6, p14 = forced_cands(k)
        for n in p4:
            if 0 <= n < 4 * U and in_p4(n, k):
                acc[n % 4] ^= 1
        for n in p6:
            if 0 <= n < 4 * U and in_p6(n, k):
                acc[n % 4] ^= 1
        for n in p14:
            if 0 <= n < 4 * U and in_p14(n, k):
                acc[n % 4] ^= 1
        if acc != want_forced_nmod(k):
            return {"ok": False, "k": k, "acc": acc}
        n_ok += 1
    ok = n_ok == K_ALG - 2 and want_forced_nmod(3) == [0, 1, 1, 1]
    return {"ok": ok, "n_ok": n_ok, "k_lo": 3, "k_hi": K_ALG}


def tot_form() -> dict:
    """k<=64: Green n%4 from g1 fold xor forced; n3 is 1; k>=3 is (0,1,1,1)."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        n0 = want_g_n0(k)
        n1 = want_g_n1(k)
        n2 = want_g_n2(k)
        n3 = want_g_n3(k)
        if n3 != 1:
            return {"ok": False, "n3": True, "k": k}
        if (n0 ^ n2) != want_green_even(k) or (n1 ^ n3) != want_green_odd(k):
            return {"ok": False, "parity": True, "k": k}
        if k >= 1 and want_g1_n1(k) != want_g1_even(k - 1):
            return {"ok": False, "n1fold": True, "k": k}
        if k >= 1 and want_g1_n3(k) != (want_g1_even(k - 1) ^ want_clip_g1(k - 1)):
            return {"ok": False, "n3fold": True, "k": k}
        if k >= 3:
            g1 = [want_g1_n0_ge3(k), want_g1_n1(k), want_g1_n2_ge3(k), want_g1_n3(k)]
            forced = want_forced_nmod(k)
            got = [g1[i] ^ forced[i] for i in range(4)]
            if got != [0, 1, 1, 1] or [n0, n1, n2, n3] != [0, 1, 1, 1]:
                return {"ok": False, "tuple": True, "k": k, "got": got}
        n_ok += 1
    ok = n_ok == K_ALG + 1 and want_g_n3(10) == 1 and want_g1_n3(3) == 0
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def want_g1_n0_ge3(k: int) -> int:
    return 0


def want_g1_n2_ge3(k: int) -> int:
    return 0


def qx_walk() -> dict:
    """Cycle QX walk: Green n%4==3 is 1 on k<=8; k>=3 tuple is (0,1,1,1)."""
    qx = json.loads(QX_JSON.read_text())
    rows = qx["green_walk"]["rows"]
    n_ok = 0
    for k in range(0, 9):
        tot = rows[str(k)]["tot"]
        if tot[3] != 1:
            return {"ok": False, "n3": True, "k": k, "tot": tot}
        if k >= 3 and tot != [0, 1, 1, 1]:
            return {"ok": False, "tuple": True, "k": k, "tot": tot}
        n_ok += 1
    ok = n_ok == 9 and rows["0"]["tot"][3] == 1 and rows["2"]["tot"][3] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": 8}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qh = json.loads(QH_JSON.read_text())
    qw = json.loads(QW_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qh["checks"]["all_ok"]
        and qw["checks"]["all_ok"]
        and qx["verdict"]["green_n0_iff_k_le_2"] == "LEMMA"
        and qx["verdict"]["green_n2_iff_k_eq_1_or_ge_3"] == "LEMMA"
        and qx["verdict"]["green_n3_all_k"] == "PREFIX"
        and qx["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and qh["verdict"]["clip_g1_0_k_ge_1"] == "LEMMA"
        and qx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, clip, forced, tot, walk, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert clip["ok"] and forced["ok"] and tot["ok"] and walk["ok"]
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
    clip = odd_clip_split()
    forced = forced_nmod()
    tot = tot_form()
    walk = qx_walk()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, clip, forced, tot, walk, sc, pref)
    dump = {
        "cycle": "QY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "odd_clip_split": {k: clip[k] for k in clip if k != "ok"},
        "forced_nmod": {k: forced[k] for k in forced if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "qx_walk": {k: walk[k] for k in walk if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "green_n3_all_k": True,
            "green_nmod_0111_k_ge_3": True,
            "g1_n1_eq_parent_even": True,
            "g1_n3_eq_parent_odd": True,
            "green_nmod_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "green_n3_all_k": "LEMMA",
            "green_nmod_0111_k_ge_3": "LEMMA",
            "g1_n1_eq_parent_even": "LEMMA",
            "g1_n3_eq_parent_odd": "LEMMA",
            "green_nmod_eq_packed": "KILLED",
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
        "odd_clip n_ok",
        dump["odd_clip_split"]["n_ok"],
        "forced n_ok",
        dump["forced_nmod"]["n_ok"],
        "qx n3",
        dump["qx_walk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
