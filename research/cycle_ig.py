#!/usr/bin/env python3
"""Cycle IG: G=1 AND is determined by Hamming slots vs green4(n,j).

On G(n,j)=1, green4=(G(j+1), NOT G(j+1), 1, NOT G(j-1)). Packed AND
is G(j+1) on slots (z)/(z,c); NOT G(j+1) on (a)/(a,c); G(j+1) XOR
G(j-1) on (b)/(z,a,b,c); G(j+1)==G(j-1) on (b,c)/(z,a,b); else 0.
Cycle IF is the G(j+1)=G(j-1) center case. G=1 AND is not G(j+1),
not G(j-1), and not identically 1. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ig.py --certify
Dump: research/cycle_ig.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hj import green4
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IF_JSON = Path(__file__).resolve().parent / "cycle_if.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

G1_NEVER = (
    (),
    (3,),
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 1, 3),
    (0, 2, 3),
    (1, 2, 3),
)
G1_GP = ((0,), (0, 3))
G1_NOT_GP = ((1,), (1, 3))
G1_XOR = ((2,), (0, 1, 2, 3))
G1_EQ = ((2, 3), (0, 1, 2))


def g1_green4(n: int, j: int) -> tuple[int, int, int, int]:
    """Even-s Green 4-tuple on G(n,j)=1: (gp, 1-gp, 1, 1-gm)."""
    gp = G(n, j + 1)
    gm = G(n, j - 1)
    return (gp, 1 - gp, 1, 1 - gm)


def _slots(four, four2):
    return tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)


def g1_and_from_slots(n: int, j: int, four) -> int:
    """Packed AND on G=1 from Hamming slots vs green4; else -1."""
    if G(n, j) == 0:
        return -1
    g4 = g1_green4(n, j)
    slots = _slots(g4, four)
    gp, gm = g4[0], 1 - g4[3]
    if slots in G1_NEVER:
        return 0
    if slots in G1_GP:
        return gp
    if slots in G1_NOT_GP:
        return 1 - gp
    if slots in G1_XOR:
        return gp ^ gm
    if slots in G1_EQ:
        return int(gp == gm)
    return -1


def g1_slots_table() -> dict:
    """n<64 G=1 green4 shape; 4x16 AND formula equals and_clause."""
    n_ok = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            if green4(n, j) != g1_green4(n, j):
                return {"ok": False, "g4": True, "n": n, "j": j}
            n_ok += 1
    n_row = 0
    for n, j in ((0, 0), (1, 0), (1, 1), (1, 2)):
        if G(n, j) == 0 or green4(n, j) != g1_green4(n, j):
            return {"ok": False, "rep": True, "n": n, "j": j}
        for bits in range(16):
            four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
            if g1_and_from_slots(n, j, four) != and_clause(*four):
                return {"ok": False, "row": True, "n": n, "j": j, "four": four}
            n_row += 1
    ok = n_ok > 0 and n_row == 64
    return {"ok": ok, "n_ok": n_ok, "n_row": n_row}


def _walk_g1(k: int, q: int) -> dict:
    """g1_and_from_slots on covering G=1; J XOR from G=1 AND."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g1_and = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                if packed != and_clause(*four):
                    return {"ok": False, "pack": True, "k": k, "four": four}
                n_ok += 1
                if packed and G(n, j):
                    xor_j ^= 1
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                pred = g1_and_from_slots(n, j, four)
                if pred != packed:
                    return {
                        "ok": False,
                        "g1": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "four": four,
                        "pred": pred,
                    }
                if packed:
                    n_g1_and += 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and n_g1 > 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g1_and": n_g1_and,
        "xor_j": xor_j,
    }


def g1_cover() -> dict:
    """G=1 slot formula on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g1_and = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g1(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_g1_and += w["n_g1_and"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g1_and": w["n_g1_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_ok == 95821 and n_g1 == 22659 and n_g1_and == 4522
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g1_and": n_g1_and,
        "rows": rows,
    }


def killed_g1_and_eq_gp() -> dict:
    """G=1 AND is not G(j+1): k=0, s=5, n=0, j=0, 0100 vs 0111."""
    k, s, n, j, p = 0, 5, 0, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    packed = and_clause(*four)
    gp = G(n, j + 1)
    ok = (
        four == (0, 1, 0, 0)
        and g4 == (0, 1, 1, 1)
        and packed == 1
        and gp == 0
        and packed != gp
        and G(n, j) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
        "gp": gp,
    }


def killed_g1_and_eq_gm() -> dict:
    """G=1 AND is not G(j-1): k=0, s=3, n=1, j=0, 0100 vs 1011."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    packed = and_clause(*four)
    gm = G(n, j - 1)
    ok = (
        four == (0, 1, 0, 0)
        and g4 == (1, 0, 1, 1)
        and packed == 1
        and gm == 0
        and packed != gm
        and G(n, j) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
        "gm": gm,
    }


def killed_g1_and_always_1() -> dict:
    """G=1 AND is not identically 1: k=0, s=3, n=3, j=0, 0000 vs 1011."""
    k, s, n, j, p = 0, 3, 3, 0, 10
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    packed = and_clause(*four)
    ok = (
        four == (0, 0, 0, 0)
        and g4 == (1, 0, 1, 1)
        and packed == 0
        and G(n, j) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
    }


def prefixes() -> dict:
    cif = json.loads(IF_JSON.read_text())
    ok = (
        cif["checks"]["all_ok"]
        and cif["verdict"]["center_AND_from_green4_slots"] == "LEMMA"
        and cif["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, gc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and gc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g1_and_from_slots(0, 0, (0, 1, 0, 0)) == 1
    assert g1_green4(1, 1) == (1, 0, 1, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = g1_slots_table()
    gc = g1_cover()
    k0 = killed_g1_and_eq_gp()
    k1 = killed_g1_and_eq_gm()
    k2 = killed_g1_and_always_1()
    pref = prefixes()
    checks = self_checks(c20, rt, gc, k0, k1, k2, pref)
    dump = {
        "cycle": "IG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g1_slots_table": {k: rt[k] for k in rt if k != "ok"},
        "g1_cover": {k: gc[k] for k in gc if k != "ok"},
        "killed_g1_and_eq_gp": {k: k0[k] for k in k0 if k != "ok"},
        "killed_g1_and_eq_gm": {k: k1[k] for k in k1 if k != "ok"},
        "killed_g1_and_always_1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g1_green4_shape": True,
            "g1_AND_from_green4_slots": True,
            "covering_g1_AND_eq_slots": True,
            "g1_and_eq_gp": False,
            "g1_and_eq_gm": False,
            "g1_and_always_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g1_green4_shape": "LEMMA",
            "g1_AND_from_green4_slots": "LEMMA",
            "covering_g1_AND_eq_slots": "LEMMA",
            "g1_and_eq_gp": "KILLED",
            "g1_and_eq_gm": "KILLED",
            "g1_and_always_1": "KILLED",
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
    print("g1_slots_table", dump["g1_slots_table"])
    cov = dump["g1_cover"]
    print(
        "g1_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g1_and",
        cov["n_g1_and"],
    )
    print("killed_g1_and_eq_gp", dump["killed_g1_and_eq_gp"])
    print("killed_g1_and_eq_gm", dump["killed_g1_and_eq_gm"])
    print("killed_g1_and_always_1", dump["killed_g1_and_always_1"])


if __name__ == "__main__":
    main()
