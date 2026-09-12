#!/usr/bin/env python3
"""Cycle JM: dual of half_neigh3 is the bit-reverse of the half 3-window.

Palindrome dual j -> 2n-j-1 reverses the half 3-neighborhood. 010
is a palindrome (left/right); iso even 011 swaps with iso odd 110.
Dual of 010 is not 011; dual of 011 is not 011; dual half is the
reverse. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jm.py --certify
Dump: research/cycle_jm.json
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
from cycle_hu import and_clause
from cycle_in import g_run_kind
from cycle_iy import dual_kind, dual_pair_start
from cycle_jc import (
    HALF_ISO_EVEN,
    HALF_ISO_ODD,
    HALF_LR,
    half_neigh3,
    kind_half3,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JL_JSON = Path(__file__).resolve().parent / "cycle_jl.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def half3_rev(three):
    """Bit-reverse of a half 3-neighborhood."""
    return three[::-1]


def half_rev_table() -> dict:
    """n<64: dual half_neigh3 is reverse; 010 palindrome, 011 swaps 110."""
    if half3_rev(HALF_LR) != HALF_LR:
        return {"ok": False, "lr": True}
    if half3_rev(HALF_ISO_EVEN) != HALF_ISO_ODD:
        return {"ok": False, "iso": True}
    if half3_rev(HALF_ISO_ODD) != HALF_ISO_EVEN:
        return {"ok": False, "iso2": True}
    n_g11 = n_left = n_right = n_iso_even = n_iso_odd = n_pal = n_swap = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = kind_half3(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            j2 = dual_pair_start(n, j)
            three = half_neigh3(n, j)
            three2 = half_neigh3(n, j2)
            if (
                three != pred
                or three2 != half3_rev(three)
                or kind_half3(n, j2) != half3_rev(pred)
                or g_run_kind(n, j2) != dual_kind(kind)
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "j2": j2,
                }
            n_g11 += 1
            if three == three[::-1]:
                n_pal += 1
            else:
                n_swap += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            elif j % 2 == 0:
                n_iso_even += 1
            else:
                n_iso_odd += 1
    ok = (
        n_g11 == 512
        and n_left == 141
        and n_right == 141
        and n_iso_even == 115
        and n_iso_odd == 115
        and n_pal == 282
        and n_swap == 230
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_pal": n_pal,
        "n_swap": n_swap,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support half_neigh3 reverse on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_dual = 0
    n_left = n_right = n_iso_even = n_iso_odd = n_pal = n_swap = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                pred = kind_half3(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                got = half_neigh3(n, j)
                if got != pred:
                    return {"ok": False, "lift": True, "k": k, "n": n, "j": j}
                n_g11 += 1
                j2 = dual_pair_start(n, j)
                if j2 not in bits or (j2 + 1) not in bits:
                    continue
                three2 = half_neigh3(n, j2)
                if three2 != half3_rev(got) or kind_half3(n, j2) != half3_rev(pred):
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if got == got[::-1]:
                    n_pal += 1
                else:
                    n_swap += 1
                if kind == "left":
                    n_left += 1
                elif kind == "right":
                    n_right += 1
                elif j % 2 == 0:
                    n_iso_even += 1
                else:
                    n_iso_odd += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "xor_j": xor_j,
    }


def half_rev_cover() -> dict:
    """Dual-in-support reverse on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_dual = 0
    n_left = n_right = n_iso_even = n_iso_odd = n_pal = n_swap = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rev(k, q)
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
            n_g11 += w["n_g11"]
            n_dual += w["n_dual"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso_even += w["n_iso_even"]
            n_iso_odd += w["n_iso_odd"]
            n_pal += w["n_pal"]
            n_swap += w["n_swap"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_dual": w["n_dual"],
                "n_pal": w["n_pal"],
                "n_swap": w["n_swap"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_dual == 6968
        and n_left == 1942
        and n_right == 1942
        and n_iso_even == 1542
        and n_iso_odd == 1542
        and n_pal == 3884
        and n_swap == 3084
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "rows": rows,
    }


def killed_010_is_011() -> dict:
    """Dual of 010 is 011: G(1,0) left 010 dualizes to right 010."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    three = half_neigh3(n, j)
    three2 = half_neigh3(n, j2)
    ok = (
        g_run_kind(n, j) == "left"
        and three == HALF_LR
        and three2 == half3_rev(three) == HALF_LR
        and three2 != HALF_ISO_EVEN
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def killed_011_stays() -> dict:
    """Dual of 011 is 011: G(3,0) iso even 011 dualizes to 110."""
    k, s, n, j, p, p2 = 1, 13, 3, 0, 20, 10
    j2 = dual_pair_start(n, j)
    three = half_neigh3(n, j)
    three2 = half_neigh3(n, j2)
    ok = (
        g_run_kind(n, j) == "iso"
        and j % 2 == 0
        and three == HALF_ISO_EVEN
        and three2 == half3_rev(three) == HALF_ISO_ODD
        and three2 != three
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def killed_dual_not_reverse() -> dict:
    """Dual half is not reverse: G(1,0) dual equals reverse."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    three = half_neigh3(n, j)
    three2 = half_neigh3(n, j2)
    ok = three2 == half3_rev(three) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def prefixes() -> dict:
    jl = json.loads(JL_JSON.read_text())
    ok = (
        jl["checks"]["all_ok"]
        and jl["verdict"]["pair_dbl_split"] == "LEMMA"
        and jl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert half3_rev(HALF_LR) == HALF_LR
    assert half3_rev(HALF_ISO_EVEN) == HALF_ISO_ODD
    assert half_neigh3(1, 1) == half3_rev(half_neigh3(1, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = half_rev_table()
    sc = half_rev_cover()
    k0 = killed_010_is_011()
    k1 = killed_011_stays()
    k2 = killed_dual_not_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "half_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "half_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_010_is_011": {k: k0[k] for k in k0 if k != "ok"},
        "killed_011_stays": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_not_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "half3_rev": True,
            "half_neigh3_dual_rev": True,
            "covering_half3_rev": True,
            "pal_is_011": False,
            "iso_stays": False,
            "dual_not_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "half3_rev": "LEMMA",
            "half_neigh3_dual_rev": "LEMMA",
            "covering_half3_rev": "LEMMA",
            "pal_is_011": "KILLED",
            "iso_stays": "KILLED",
            "dual_not_reverse": "KILLED",
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
    print("half_rev_table", dump["half_rev_table"])
    cov = dump["half_rev_cover"]
    print(
        "half_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_dual",
        cov["n_dual"],
        "n_pal",
        cov["n_pal"],
        "n_swap",
        cov["n_swap"],
    )
    print("killed_010_is_011", dump["killed_010_is_011"])
    print("killed_011_stays", dump["killed_011_stays"])
    print("killed_dual_not_reverse", dump["killed_dual_not_reverse"])


if __name__ == "__main__":
    main()
