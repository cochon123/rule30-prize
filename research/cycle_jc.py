#!/usr/bin/env python3
"""Cycle JC: pair_lift6 is the freshman stretch of the half 3-neighborhood.

On odd n=2m+1, the parent 6-window is G(m) stretched onto even
indices of n-1=2m. Left/right have half 3-neigh 010; iso even j has
011; iso odd j has 110. Iso half-neigh is not 010; left half-neigh
is not 011; stretch of 010 at even start is right, not left. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jc.py --certify
Dump: research/cycle_jc.json
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
from cycle_ja import (
    ISO_EVEN_J,
    ISO_ODD_J,
    LIFT_LEFT,
    LIFT_RIGHT,
    kind_lift6,
    pair_lift6,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JB_JSON = Path(__file__).resolve().parent / "cycle_jb.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

HALF_LR = (0, 1, 0)
HALF_ISO_EVEN = (0, 1, 1)
HALF_ISO_ODD = (1, 1, 0)


def half_pair_k(n: int, j: int) -> int:
    """Half index k for a consecutive G=1 pair at j on odd n."""
    if j % 2 == 0:
        return j // 2
    return (j - 1) // 2


def half_neigh3(n: int, j: int):
    """(G(m,k-1), G(m,k), G(m,k+1)) for a pair; None if no pair."""
    if n % 2 == 0 or g_run_kind(n, j) is None:
        return None
    m = n // 2
    k = half_pair_k(n, j)
    return (G(m, k - 1), G(m, k), G(m, k + 1))


def freshman_lift6(three, start_even: bool):
    """Stretch a 3-neigh onto even indices of an even-n 6-window."""
    a, b, c = three
    if start_even:
        return (a, 0, b, 0, c, 0)
    return (0, a, 0, b, 0, c)


def kind_half3(n: int, j: int):
    """Predicted half 3-neigh from g_run_kind and j parity."""
    kind = g_run_kind(n, j)
    if kind is None:
        return None
    if kind != "iso":
        return HALF_LR
    return HALF_ISO_EVEN if j % 2 == 0 else HALF_ISO_ODD


def half_table() -> dict:
    """n<64: pair_lift6 equals freshman_lift6 of kind_half3."""
    n_g11 = n_left = n_right = n_iso_even = n_iso_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            three = kind_half3(n, j)
            if kind is None:
                if three is not None or half_neigh3(n, j) is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            got = half_neigh3(n, j)
            start_even = j % 2 == 1
            pred6 = freshman_lift6(three, start_even)
            if (
                got != three
                or pair_lift6(n, j) != pred6
                or pred6 != kind_lift6(n, j)
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "got": got,
                    "three": three,
                }
            n_g11 += 1
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
        and freshman_lift6(HALF_LR, False) == LIFT_LEFT
        and freshman_lift6(HALF_LR, True) == LIFT_RIGHT
        and freshman_lift6(HALF_ISO_EVEN, False) == ISO_EVEN_J
        and freshman_lift6(HALF_ISO_ODD, True) == ISO_ODD_J
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
    }


def _walk_half(k: int, q: int) -> dict:
    """Half 3-neigh stretch on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso_even = n_iso_odd = 0
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
                three = kind_half3(n, j)
                if kind is None:
                    if three is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                got = half_neigh3(n, j)
                start_even = j % 2 == 1
                pred6 = freshman_lift6(three, start_even)
                if got != three or pair_lift6(n, j) != pred6:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                    }
                n_g11 += 1
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
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "xor_j": xor_j,
    }


def half_cover() -> dict:
    """Half 3-neigh stretch on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso_even = n_iso_odd = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_half(k, q)
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
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso_even += w["n_iso_even"]
            n_iso_odd += w["n_iso_odd"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso_even": w["n_iso_even"],
                "n_iso_odd": w["n_iso_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_left == 2380
        and n_right == 2380
        and n_iso_even == 1912
        and n_iso_odd == 1905
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "rows": rows,
    }


def killed_iso_half_010() -> dict:
    """Iso half-neigh is 010: G(3,0) has 011."""
    k, s, n, j, p = 1, 5, 3, 0, 12
    three = half_neigh3(n, j)
    ok = (
        g_run_kind(n, j) == "iso"
        and three == HALF_ISO_EVEN
        and three != HALF_LR
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "iso",
        "three": list(three),
    }


def killed_left_half_011() -> dict:
    """Left half-neigh is 011: G(1,0) has 010."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    three = half_neigh3(n, j)
    ok = (
        g_run_kind(n, j) == "left"
        and three == HALF_LR
        and three != HALF_ISO_EVEN
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "left",
        "three": list(three),
    }


def killed_stretch_010_even_left() -> dict:
    """Stretch of 010 at even start is left: it is right 001000."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    six = freshman_lift6(HALF_LR, True)
    ok = (
        g_run_kind(n, j) == "right"
        and six == LIFT_RIGHT
        and six != LIFT_LEFT
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "right",
        "six": list(six),
    }


def prefixes() -> dict:
    jb = json.loads(JB_JSON.read_text())
    ok = (
        jb["checks"]["all_ok"]
        and jb["verdict"]["dual_lift6_rev"] == "LEMMA"
        and jb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert kind_half3(1, 0) == HALF_LR
    assert kind_half3(1, 1) == HALF_LR
    assert kind_half3(3, 0) == HALF_ISO_EVEN
    assert kind_half3(3, 5) == HALF_ISO_ODD
    assert kind_half3(2, 0) is None
    assert freshman_lift6(HALF_ISO_ODD, True) == ISO_ODD_J
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = half_table()
    sc = half_cover()
    k0 = killed_iso_half_010()
    k1 = killed_left_half_011()
    k2 = killed_stretch_010_even_left()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "half_table": {k: rt[k] for k in rt if k != "ok"},
        "half_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_iso_half_010": {k: k0[k] for k in k0 if k != "ok"},
        "killed_left_half_011": {k: k1[k] for k in k1 if k != "ok"},
        "killed_stretch_010_even_left": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "half_neigh3_stretch": True,
            "kind_half3": True,
            "covering_half_lift6": True,
            "iso_half_010": False,
            "left_half_011": False,
            "stretch_010_even_left": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "half_neigh3_stretch": "LEMMA",
            "kind_half3": "LEMMA",
            "covering_half_lift6": "LEMMA",
            "iso_half_010": "KILLED",
            "left_half_011": "KILLED",
            "stretch_010_even_left": "KILLED",
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
    print("half_table", dump["half_table"])
    cov = dump["half_cover"]
    print(
        "half_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_iso_even",
        cov["n_iso_even"],
        "n_iso_odd",
        cov["n_iso_odd"],
    )
    print("killed_iso_half_010", dump["killed_iso_half_010"])
    print("killed_left_half_011", dump["killed_left_half_011"])
    print("killed_stretch_010_even_left", dump["killed_stretch_010_even_left"])


if __name__ == "__main__":
    main()
