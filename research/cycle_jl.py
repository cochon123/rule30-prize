#!/usr/bin/env python3
"""Cycle JL: doubling a consecutive G=1 pair splits into two isolated ones.

iso1_lift5(2n,2j) and iso1_lift5(2n,2j+2) are (00011,01110) for even
j and (01110,11000) for odd j. The pair does not stay a pair; even j
does not take the odd-j windows; the two windows do not determine
kind. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jl.py --certify
Dump: research/cycle_jl.json
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
from cycle_ir import isolated_one
from cycle_jd import iso1_lift5
from cycle_ji import LIFT1_HI, LIFT1_LO, LIFT1_MID_ODD
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JK_JSON = Path(__file__).resolve().parent / "cycle_jk.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

PAIR_EVEN = (LIFT1_LO, LIFT1_MID_ODD)
PAIR_ODD = (LIFT1_MID_ODD, LIFT1_HI)


def pair_dbl_fives(n: int, j: int):
    """Predicted LIFT1 windows of the two isolated ones at 2n."""
    if g_run_kind(n, j) is None:
        return None
    if j % 2 == 0:
        return PAIR_EVEN
    return PAIR_ODD


def split_table() -> dict:
    """n<64: a pair doubles to two isolated ones with pair_dbl_fives windows."""
    n_g11 = n_left = n_right = n_iso = n_iso_even = n_iso_odd = 0
    n_even = n_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = pair_dbl_fives(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            n2, jL, jR = 2 * n, 2 * j, 2 * j + 2
            fiveL = iso1_lift5(n2, jL)
            fiveR = iso1_lift5(n2, jR)
            if (
                n % 2 == 0
                or not isolated_one(n2, jL)
                or not isolated_one(n2, jR)
                or G(n2, jL + 1) != 0
                or g_run_kind(n2, jL) is not None
                or (fiveL, fiveR) != pred
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "fiveL": list(fiveL) if fiveL else None,
                    "fiveR": list(fiveR) if fiveR else None,
                }
            n_g11 += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
                if j % 2 == 0:
                    n_iso_even += 1
                else:
                    n_iso_odd += 1
            if j % 2 == 0:
                n_even += 1
            else:
                n_odd += 1
    ok = (
        n_g11 == 512
        and n_left == 141
        and n_right == 141
        and n_iso == 230
        and n_iso_even == 115
        and n_iso_odd == 115
        and n_even == 256
        and n_odd == 256
        and pair_dbl_fives(5, 0) == PAIR_EVEN
        and pair_dbl_fives(5, 1) == PAIR_ODD
        and pair_dbl_fives(7, 0) == PAIR_EVEN
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_even": n_even,
        "n_odd": n_odd,
    }


def _walk_split(k: int, q: int) -> dict:
    """Pair-split identity on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
    n_iso_even = n_iso_odd = n_even = n_odd = 0
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
                pred = pair_dbl_fives(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                n2, jL, jR = 2 * n, 2 * j, 2 * j + 2
                fiveL = iso1_lift5(n2, jL)
                fiveR = iso1_lift5(n2, jR)
                if (
                    not isolated_one(n2, jL)
                    or not isolated_one(n2, jR)
                    or (fiveL, fiveR) != pred
                ):
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_g11 += 1
                if kind == "left":
                    n_left += 1
                elif kind == "right":
                    n_right += 1
                else:
                    n_iso += 1
                    if j % 2 == 0:
                        n_iso_even += 1
                    else:
                        n_iso_odd += 1
                if j % 2 == 0:
                    n_even += 1
                else:
                    n_odd += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_even": n_even,
        "n_odd": n_odd,
        "xor_j": xor_j,
    }


def split_cover() -> dict:
    """Pair-split identity on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
    n_iso_even = n_iso_odd = n_even = n_odd = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_split(k, q)
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
            n_iso += w["n_iso"]
            n_iso_even += w["n_iso_even"]
            n_iso_odd += w["n_iso_odd"]
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_even": w["n_even"],
                "n_odd": w["n_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_left == 2380
        and n_right == 2380
        and n_iso == 3817
        and n_iso_even == 1912
        and n_iso_odd == 1905
        and n_even == 4292
        and n_odd == 4285
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "n_even": n_even,
        "n_odd": n_odd,
        "rows": rows,
    }


def killed_pair_stays() -> dict:
    """Pair stays a pair: G(5,0)G(5,1)=11 splits to isolated ones at G(10,0), G(10,2)."""
    k, s, n, j, p, pL, pR = 1, 9, 5, 0, 20, 20, 16
    n2, jL, jR = 2 * n, 2 * j, 2 * j + 2
    fiveL = iso1_lift5(n2, jL)
    fiveR = iso1_lift5(n2, jR)
    ok = (
        g_run_kind(n, j) == "left"
        and isolated_one(n2, jL)
        and isolated_one(n2, jR)
        and g_run_kind(n2, jL) is None
        and (fiveL, fiveR) == PAIR_EVEN
        and p >= 4
        and pL >= 4
        and pR >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "jL": jL,
        "jR": jR,
        "p": p,
        "pL": pL,
        "pR": pR,
        "fiveL": list(fiveL),
        "fiveR": list(fiveR),
    }


def killed_even_odd_windows() -> dict:
    """Even j takes odd-j windows: G(5,0) splits to 00011/01110, not 01110/11000."""
    k, s, n, j, p, pL, pR = 1, 9, 5, 0, 20, 20, 16
    n2, jL, jR = 2 * n, 2 * j, 2 * j + 2
    fiveL = iso1_lift5(n2, jL)
    fiveR = iso1_lift5(n2, jR)
    ok = (
        j % 2 == 0
        and (fiveL, fiveR) == PAIR_EVEN
        and (fiveL, fiveR) != PAIR_ODD
        and p >= 4
        and pL >= 4
        and pR >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "jL": jL,
        "jR": jR,
        "p": p,
        "pL": pL,
        "pR": pR,
        "fiveL": list(fiveL),
        "fiveR": list(fiveR),
    }


def killed_kind_from_fives() -> dict:
    """Windows determine kind: left G(5,0) and iso G(7,0) share 00011/01110."""
    k, s_left, s_iso, p = 1, 9, 5, 20
    nL, jL, nI, jI = 5, 0, 7, 0
    f_left = (
        iso1_lift5(2 * nL, 2 * jL),
        iso1_lift5(2 * nL, 2 * jL + 2),
    )
    f_iso = (
        iso1_lift5(2 * nI, 2 * jI),
        iso1_lift5(2 * nI, 2 * jI + 2),
    )
    ok = (
        g_run_kind(nL, jL) == "left"
        and g_run_kind(nI, jI) == "iso"
        and f_left == f_iso == PAIR_EVEN
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s_left": s_left,
        "s_iso": s_iso,
        "n_left": nL,
        "j_left": jL,
        "n_iso": nI,
        "j_iso": jI,
        "p": p,
        "five_left": [list(f_left[0]), list(f_left[1])],
        "five_iso": [list(f_iso[0]), list(f_iso[1])],
    }


def prefixes() -> dict:
    jk = json.loads(JK_JSON.read_text())
    ok = (
        jk["checks"]["all_ok"]
        and jk["verdict"]["lift5_double_involution"] == "LEMMA"
        and jk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert pair_dbl_fives(5, 0) == PAIR_EVEN
    assert pair_dbl_fives(5, 1) == PAIR_ODD
    assert isolated_one(10, 0) and isolated_one(10, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = split_table()
    sc = split_cover()
    k0 = killed_pair_stays()
    k1 = killed_even_odd_windows()
    k2 = killed_kind_from_fives()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "split_table": {k: rt[k] for k in rt if k != "ok"},
        "split_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_pair_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_odd_windows": {k: k1[k] for k in k1 if k != "ok"},
        "killed_kind_from_fives": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "pair_dbl_split": True,
            "pair_dbl_fives": True,
            "covering_pair_dbl": True,
            "pair_stays": False,
            "even_odd_windows": False,
            "kind_from_fives": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "pair_dbl_split": "LEMMA",
            "pair_dbl_fives": "LEMMA",
            "covering_pair_dbl": "LEMMA",
            "pair_stays": "KILLED",
            "even_odd_windows": "KILLED",
            "kind_from_fives": "KILLED",
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
    print("split_table", dump["split_table"])
    cov = dump["split_cover"]
    print(
        "split_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_even",
        cov["n_even"],
        "n_odd",
        cov["n_odd"],
    )
    print("killed_pair_stays", dump["killed_pair_stays"])
    print("killed_even_odd_windows", dump["killed_even_odd_windows"])
    print("killed_kind_from_fives", dump["killed_kind_from_fives"])


if __name__ == "__main__":
    main()
