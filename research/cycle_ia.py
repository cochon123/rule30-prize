#!/usr/bin/env python3
"""Cycle IA: both-non-cob Hamming 1 differs only in cob(j); AND xor is NOT copy(j).

Among non-cob 4-tuples the unique Hamming-1 non-cob neighbor is the
flip of bit c. AND xor equals NOT b. Covering both-non-cob Hamming 0
pairs are identical so they drop out of J. Hamming-1 XOR is not
always 1 or 0; Hamming-1 dual is not reverse. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ia.py --certify
Dump: research/cycle_ia.json
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
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from cycle_hx import reverse_four
from cycle_hy import mixed_oneside
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HZ_JSON = Path(__file__).resolve().parent / "cycle_hz.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def flip_c(z: int, a: int, b: int, c: int) -> tuple[int, int, int, int]:
    return (z, a, b, 1 - c)


def nc_ham1_table() -> dict:
    """8 non-cob: unique Hamming-1 non-cob neighbor is flip_c; XOR is NOT b."""
    n_ok = n_nc = n_ham1 = 0
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        n_ok += 1
        if cob_shaped(*four):
            continue
        n_nc += 1
        neigh = []
        for i in range(4):
            fl = list(four)
            fl[i] ^= 1
            fl = tuple(fl)
            if not cob_shaped(*fl):
                neigh.append((i, fl))
        if neigh != [(3, flip_c(*four))]:
            return {"ok": False, "neigh": True, "four": four, "got": neigh}
        xor_a = and_clause(*four) ^ and_clause(*flip_c(*four))
        if xor_a != (1 - four[2]):
            return {"ok": False, "xor": True, "four": four, "xor_a": xor_a}
        n_ham1 += 1
    ok = n_ok == 16 and n_nc == 8 and n_ham1 == 8
    return {"ok": ok, "n_ok": n_ok, "n_nc": n_nc, "n_ham1": n_ham1}


def _walk_ham1(k: int, q: int) -> dict:
    """Hamming 0 bn XOR 0; Hamming 1 bn is flip_c and XOR NOT copy_j."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_bn = n_ham0 = n_ham1 = n_ham1_xor = 0
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
                bits[j] = (four, packed, p)
                n_ok += 1
                if packed and G(n, j):
                    xor_j ^= 1
            if n in bits and bits[n][1]:
                xor_fold ^= 1
            for j in range(0, n):
                j2 = 2 * n - j
                if j not in bits or j2 not in bits:
                    continue
                if G(n, j) == 0:
                    continue
                f, a, p = bits[j]
                g, b, p2 = bits[j2]
                n_pair += 1
                c1, c2 = cob_shaped(*f), cob_shaped(*g)
                if c1 != c2:
                    mo = mixed_oneside(f, g)
                    if mo != (a ^ b):
                        return {"ok": False, "oneside": True, "k": k}
                    if a ^ b:
                        xor_fold ^= 1
                    continue
                if c1 and c2:
                    continue
                n_bn += 1
                ham = sum(x != y for x, y in zip(f, g))
                if ham == 0:
                    n_ham0 += 1
                    if f != g or (a ^ b):
                        return {"ok": False, "ham0": True, "k": k, "four": f}
                elif ham == 1:
                    n_ham1 += 1
                    if g != flip_c(*f) and f != flip_c(*g):
                        return {"ok": False, "flip": True, "k": k, "four": f, "four2": g}
                    if (a ^ b) != (1 - f[2]):
                        return {
                            "ok": False,
                            "notb": True,
                            "k": k,
                            "four": f,
                            "xor_a": a ^ b,
                        }
                    if a ^ b:
                        n_ham1_xor += 1
                        xor_fold ^= 1
                elif a ^ b:
                    xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bn": n_bn,
        "n_ham0": n_ham0,
        "n_ham1": n_ham1,
        "n_ham1_xor": n_ham1_xor,
        "xor_j": xor_j,
    }


def ham1_cover() -> dict:
    """Hamming-1 bn split on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_bn = n_ham0 = n_ham1 = n_ham1_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_ham1(k, q)
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
            n_pair += w["n_pair"]
            n_bn += w["n_bn"]
            n_ham0 += w["n_ham0"]
            n_ham1 += w["n_ham1"]
            n_ham1_xor += w["n_ham1_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_bn": w["n_bn"],
                "n_ham0": w["n_ham0"],
                "n_ham1": w["n_ham1"],
                "n_ham1_xor": w["n_ham1_xor"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_bn == 2123
        and n_ham0 == 299
        and n_ham1 == 258
        and n_ham1_xor == 125
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bn": n_bn,
        "n_ham0": n_ham0,
        "n_ham1": n_ham1,
        "n_ham1_xor": n_ham1_xor,
        "rows": rows,
    }


def killed_ham1_xor_always_1() -> dict:
    """Hamming-1 bn AND xor is not always 1: k=3, s=51, n=14, 0010 vs 0011."""
    k, s, n, j, j2, p, p2 = 3, 51, 14, 12, 16, 56, 48
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (0, 0, 1, 1)
        and four2 == flip_c(*four)
        and (not cob_shaped(*four))
        and (not cob_shaped(*four2))
        and a == 1
        and b == 1
        and (a ^ b) == 0
        and (a ^ b) == (1 - four[2])
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "four": list(four),
        "four2": list(four2),
    }


def killed_ham1_xor_always_0() -> dict:
    """Hamming-1 bn AND xor is not always 0: k=4, s=67, n=46, 1000 vs 1001."""
    k, s, n, j, j2, p, p2 = 4, 67, 46, 20, 72, 120, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (1, 0, 0, 0)
        and four2 == (1, 0, 0, 1)
        and four2 == flip_c(*four)
        and (not cob_shaped(*four))
        and (not cob_shaped(*four2))
        and a == 0
        and b == 1
        and (a ^ b) == 1
        and (a ^ b) == (1 - four[2])
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "four": list(four),
        "four2": list(four2),
    }


def killed_ham1_eq_reverse() -> dict:
    """Hamming-1 bn dual is not reverse: k=3, s=51, n=14, 0010 vs 0011."""
    k, s, n, j, j2, p, p2 = 3, 51, 14, 12, 16, 56, 48
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (0, 0, 1, 1)
        and reverse_four(*four) == (0, 1, 0, 0)
        and four2 != reverse_four(*four)
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "four": list(four),
        "four2": list(four2),
        "rev": list(reverse_four(*four)),
    }


def prefixes() -> dict:
    hz = json.loads(HZ_JSON.read_text())
    ok = (
        hz["checks"]["all_ok"]
        and hz["verdict"]["same_class_duals_never_hamming4"] == "LEMMA"
        and hz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, hc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and hc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert flip_c(0, 0, 1, 0) == (0, 0, 1, 1)
    assert flip_c(1, 0, 0, 0) == (1, 0, 0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = nc_ham1_table()
    hc = ham1_cover()
    k0 = killed_ham1_xor_always_1()
    k1 = killed_ham1_xor_always_0()
    k2 = killed_ham1_eq_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, hc, k0, k1, k2, pref)
    dump = {
        "cycle": "IA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "nc_ham1_table": {k: rt[k] for k in rt if k != "ok"},
        "ham1_cover": {k: hc[k] for k in hc if k != "ok"},
        "killed_ham1_xor_always_1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_ham1_xor_always_0": {k: k1[k] for k in k1 if k != "ok"},
        "killed_ham1_eq_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "nc_ham1_neighbor_is_flip_c": True,
            "nc_ham1_AND_xor_is_NOT_copy": True,
            "bn_ham0_AND_xor_0": True,
            "ham1_xor_always_1": False,
            "ham1_xor_always_0": False,
            "ham1_eq_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "nc_ham1_neighbor_is_flip_c": "LEMMA",
            "nc_ham1_AND_xor_is_NOT_copy": "LEMMA",
            "bn_ham0_AND_xor_0": "LEMMA",
            "ham1_xor_always_1": "KILLED",
            "ham1_xor_always_0": "KILLED",
            "ham1_eq_reverse": "KILLED",
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
    print("nc_ham1_table", dump["nc_ham1_table"])
    cov = dump["ham1_cover"]
    print(
        "ham1_cover n_ok",
        cov["n_ok"],
        "n_bn",
        cov["n_bn"],
        "n_ham0",
        cov["n_ham0"],
        "n_ham1",
        cov["n_ham1"],
        "n_ham1_xor",
        cov["n_ham1_xor"],
    )
    print("killed_ham1_xor_always_1", dump["killed_ham1_xor_always_1"])
    print("killed_ham1_xor_always_0", dump["killed_ham1_xor_always_0"])
    print("killed_ham1_eq_reverse", dump["killed_ham1_eq_reverse"])


if __name__ == "__main__":
    main()
