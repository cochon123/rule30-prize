#!/usr/bin/env python3
"""Cycle HW: covering J folds through Green palindrome; unpaired is 0000.

G(n,j)=G(n,2n-j). Covering odd-s J is the XOR of AND at the Green
center j=n plus AND disagreements on in-support dual pairs. G=1
columns whose dual is clipped have even-s 4-tuple 0000, so they drop
out of J. AND is not palindromic; center AND is not always live;
unpaired is not green4. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_hw.py --certify
Dump: research/cycle_hw.json
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
HV_JSON = Path(__file__).resolve().parent / "cycle_hv.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def g_palindrome_table() -> dict:
    """G(n,j)=G(n,2n-j) and G(n,n)=1 for n<64."""
    n_ok = 0
    for n in range(0, 64):
        if G(n, n) != 1:
            return {"ok": False, "center": True, "n": n}
        for j in range(0, 2 * n + 1):
            if G(n, j) != G(n, 2 * n - j):
                return {"ok": False, "n": n, "j": j, "a": G(n, j), "b": G(n, 2 * n - j)}
            n_ok += 1
    return {"ok": n_ok == 4096, "n_ok": n_ok}


def _walk_fold(k: int, q: int) -> dict:
    """J = center XOR pair disagreements; unpaired four=0000."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_center = n_center_and = 0
    n_pair = n_pair_xor = n_unp = 0
    xor_j = xor_fold = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                if packed != and_clause(*four):
                    return {"ok": False, "pack": True, "k": k, "four": four}
                bits[j] = (four, packed)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            if n not in bits:
                return {"ok": False, "center_clip": True, "k": k, "n": n}
            n_center += 1
            four_c, packed_c = bits[n]
            if G(n, n) != 1:
                return {"ok": False, "Gnn": True, "k": k, "n": n}
            if packed_c:
                n_center_and += 1
                xor_fold ^= 1
            for j in range(0, n):
                j2 = 2 * n - j
                if j in bits and j2 in bits:
                    if G(n, j) != G(n, j2):
                        return {"ok": False, "pal": True, "k": k, "n": n, "j": j}
                    if G(n, j):
                        n_pair += 1
                        a, b = bits[j][1], bits[j2][1]
                        if a ^ b:
                            n_pair_xor += 1
                            xor_fold ^= 1
                elif j in bits and G(n, j):
                    four_u, packed_u = bits[j]
                    if four_u != (0, 0, 0, 0) or packed_u:
                        return {
                            "ok": False,
                            "unp": True,
                            "k": k,
                            "n": n,
                            "j": j,
                            "four": four_u,
                        }
                    n_unp += 1
                elif j2 in bits and G(n, j2):
                    return {"ok": False, "unp_hi": True, "k": k, "n": n, "j": j2}
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_j == xor_fold
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_center": n_center,
        "n_center_and": n_center_and,
        "n_pair": n_pair,
        "n_pair_xor": n_pair_xor,
        "n_unp": n_unp,
        "xor_j": xor_j,
        "xor_fold": xor_fold,
    }


def fold_cover() -> dict:
    """Palindrome fold on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_center = n_center_and = 0
    n_pair = n_pair_xor = n_unp = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_fold(k, q)
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
            n_center += w["n_center"]
            n_center_and += w["n_center_and"]
            n_pair += w["n_pair"]
            n_pair_xor += w["n_pair_xor"]
            n_unp += w["n_unp"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_center_and": w["n_center_and"],
                "n_pair_xor": w["n_pair_xor"],
                "n_unp": w["n_unp"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_g1 == 22659 and n_center == 762 and n_unp == 4009 and n_center_and == 232
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_center": n_center,
        "n_center_and": n_center_and,
        "n_pair": n_pair,
        "n_pair_xor": n_pair_xor,
        "n_unp": n_unp,
        "rows": rows,
    }


def killed_and_palindrome() -> dict:
    """AND is not palindromic on G=1: k=1, s=5, n=7, j=6 vs 8."""
    k, s, n, j, j2, p, p2 = 1, 5, 7, 6, 8, 8, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    packed2 = (Aodd >> p2) & 1
    ok = (
        four == (0, 0, 0, 1)
        and four2 == (1, 0, 0, 1)
        and packed == 0
        and packed2 == 1
        and G(n, j) == 1
        and G(n, j2) == 1
        and j2 == 2 * n - j
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
        "four": list(four),
        "four2": list(four2),
        "packed": packed,
        "packed2": packed2,
    }


def killed_center_and_always() -> dict:
    """Center AND is not always live: k=0, s=7, n=1, j=1, four=0000."""
    k, s, n, j, p = 0, 7, 1, 1, 8
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = j == n and four == (0, 0, 0, 0) and packed == 0 and G(n, j) == 1
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
        "G": G(n, j),
    }


def killed_unp_eq_green4() -> dict:
    """Unpaired G=1 is not green4: k=0, s=3, n=3, j=0, four=0000 vs 1011."""
    k, s, n, j, p = 0, 3, 3, 0, 10
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    j2 = 2 * n - j
    T = 10
    p2 = T - 2 * j2
    ok = (
        four == (0, 0, 0, 0)
        and g4 == (1, 0, 1, 1)
        and four != g4
        and G(n, j) == 1
        and p2 < 0
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
        "four": list(four),
        "g4": list(g4),
        "G": G(n, j),
    }


def prefixes() -> dict:
    hv = json.loads(HV_JSON.read_text())
    ok = (
        hv["checks"]["all_ok"]
        and hv["verdict"]["covering_J_eq_G1_FRESH_XOR_CONT"] == "LEMMA"
        and hv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gp: dict, fc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gp["ok"] and fc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert G(0, 0) == 1 and G(5, 1) == G(5, 9)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gp = g_palindrome_table()
    fc = fold_cover()
    k0 = killed_and_palindrome()
    k1 = killed_center_and_always()
    k2 = killed_unp_eq_green4()
    pref = prefixes()
    checks = self_checks(c20, gp, fc, k0, k1, k2, pref)
    dump = {
        "cycle": "HW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g_palindrome_table": {k: gp[k] for k in gp if k != "ok"},
        "fold_cover": {k: fc[k] for k in fc if k != "ok"},
        "killed_and_palindrome": {k: k0[k] for k in k0 if k != "ok"},
        "killed_center_and_always": {k: k1[k] for k in k1 if k != "ok"},
        "killed_unp_eq_green4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "G_palindrome": True,
            "covering_J_eq_center_XOR_pair_disagreements": True,
            "unpaired_G1_four_0000": True,
            "AND_palindrome_on_G1": False,
            "center_AND_always_live": False,
            "unpaired_eq_green4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_palindrome": "LEMMA",
            "covering_J_eq_center_XOR_pair_disagreements": "LEMMA",
            "unpaired_G1_four_0000": "LEMMA",
            "AND_palindrome_on_G1": "KILLED",
            "center_AND_always_live": "KILLED",
            "unpaired_eq_green4": "KILLED",
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
    print("g_palindrome_table", dump["g_palindrome_table"])
    cov = dump["fold_cover"]
    print(
        "fold_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_center_and",
        cov["n_center_and"],
        "n_pair_xor",
        cov["n_pair_xor"],
        "n_unp",
        cov["n_unp"],
    )
    print("killed_and_palindrome", dump["killed_and_palindrome"])
    print("killed_center_and_always", dump["killed_center_and_always"])
    print("killed_unp_eq_green4", dump["killed_unp_eq_green4"])


if __name__ == "__main__":
    main()
