#!/usr/bin/env python3
"""Cycle IB: cob-shape lives on (z,a,b); same class iff even zab Hamming.

cob_shaped ignores c, so same cob class iff the Hamming weight of
(z,a,b) differences is even. Covering both-non-cob Hamming 2 never
includes bit c; Hamming 3 always includes c and never (z,a,b) alone.
Hamming-2 AND xor is a slot formula, not always 1; Hamming-3 XOR is
not always 1; Hamming-2 dual is not reverse. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ib.py --certify
Dump: research/cycle_ib.json
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
IA_JSON = Path(__file__).resolve().parent / "cycle_ia.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

HAM2_SLOTS = ((0, 1), (0, 2), (1, 2))
HAM3_SLOTS = ((0, 1, 3), (0, 2, 3), (1, 2, 3))


def zab_parity(four, four2) -> int:
    """XOR of differences on (z,a,b); ignores c."""
    return (four[0] ^ four2[0]) ^ (four[1] ^ four2[1]) ^ (four[2] ^ four2[2])


def ham2_and_xor(four, four2) -> int:
    """AND xor if Hamming 2 on {z,a,b} with equal c; else -1."""
    slots = tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)
    if slots == (0, 1):
        return 1
    if slots == (0, 2):
        return 1 - four[3]
    if slots == (1, 2):
        return four[3]
    return -1


def zab_parity_table() -> dict:
    """16x16: same cob class iff zab_parity=0; ham2 XOR formulas."""
    n_ok = n_same = n_ham2 = 0
    for b1 in range(16):
        four = tuple((b1 >> i) & 1 for i in range(3, -1, -1))
        for b2 in range(16):
            four2 = tuple((b2 >> i) & 1 for i in range(3, -1, -1))
            n_ok += 1
            same = cob_shaped(*four) == cob_shaped(*four2)
            even = zab_parity(four, four2) == 0
            if same != even:
                return {
                    "ok": False,
                    "parity": True,
                    "four": four,
                    "four2": four2,
                }
            if same:
                n_same += 1
            pred = ham2_and_xor(four, four2)
            ham = sum(x != y for x, y in zip(four, four2))
            if ham == 2 and (not cob_shaped(*four)) and (not cob_shaped(*four2)):
                n_ham2 += 1
                xor_a = and_clause(*four) ^ and_clause(*four2)
                if pred != xor_a:
                    return {
                        "ok": False,
                        "ham2": True,
                        "four": four,
                        "four2": four2,
                        "pred": pred,
                        "xor_a": xor_a,
                    }
    ok = n_ok == 256 and n_same == 128 and n_ham2 == 24
    return {"ok": ok, "n_ok": n_ok, "n_same": n_same, "n_ham2": n_ham2}


def _walk_zab(k: int, q: int) -> dict:
    """Even zab Hamming iff same cob class; ham2/ham3 slot restrictions."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_h2 = n_h3 = n_h2_xor = n_h3_xor = 0
    n_h2_01 = n_h2_02 = n_h2_12 = 0
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
                even = zab_parity(f, g) == 0
                if even != (c1 == c2):
                    return {"ok": False, "zab": True, "k": k, "four": f, "four2": g}
                if c1 != c2:
                    if mixed_oneside(f, g) != (a ^ b):
                        return {"ok": False, "oneside": True, "k": k}
                    if a ^ b:
                        xor_fold ^= 1
                    continue
                if c1 and c2:
                    continue
                ham = sum(x != y for x, y in zip(f, g))
                slots = tuple(i for i, (x, y) in enumerate(zip(f, g)) if x != y)
                if ham == 2:
                    n_h2 += 1
                    if slots not in HAM2_SLOTS or 3 in slots:
                        return {"ok": False, "h2slot": True, "k": k, "slots": slots}
                    pred = ham2_and_xor(f, g)
                    if pred != (a ^ b):
                        return {"ok": False, "h2xor": True, "k": k, "pred": pred}
                    if slots == (0, 1):
                        n_h2_01 += 1
                    elif slots == (0, 2):
                        n_h2_02 += 1
                    else:
                        n_h2_12 += 1
                    if a ^ b:
                        n_h2_xor += 1
                        xor_fold ^= 1
                elif ham == 3:
                    n_h3 += 1
                    if slots not in HAM3_SLOTS or 3 not in slots:
                        return {"ok": False, "h3slot": True, "k": k, "slots": slots}
                    if a ^ b:
                        n_h3_xor += 1
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
        "n_h2": n_h2,
        "n_h2_01": n_h2_01,
        "n_h2_02": n_h2_02,
        "n_h2_12": n_h2_12,
        "n_h2_xor": n_h2_xor,
        "n_h3": n_h3,
        "n_h3_xor": n_h3_xor,
        "xor_j": xor_j,
    }


def zab_cover() -> dict:
    """zab parity / ham2-ham3 slots on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_h2 = n_h3 = n_h2_xor = n_h3_xor = 0
    n_h2_01 = n_h2_02 = n_h2_12 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_zab(k, q)
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
            n_h2 += w["n_h2"]
            n_h2_01 += w["n_h2_01"]
            n_h2_02 += w["n_h2_02"]
            n_h2_12 += w["n_h2_12"]
            n_h2_xor += w["n_h2_xor"]
            n_h3 += w["n_h3"]
            n_h3_xor += w["n_h3_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_h2": w["n_h2"],
                "n_h3": w["n_h3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_h2 == 771
        and n_h2_01 == 284
        and n_h2_02 == 220
        and n_h2_12 == 267
        and n_h2_xor == 533
        and n_h3 == 795
        and n_h3_xor == 372
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_h2": n_h2,
        "n_h2_01": n_h2_01,
        "n_h2_02": n_h2_02,
        "n_h2_12": n_h2_12,
        "n_h2_xor": n_h2_xor,
        "n_h3": n_h3,
        "n_h3_xor": n_h3_xor,
        "rows": rows,
    }


def killed_ham2_xor_always_1() -> dict:
    """Hamming-2 bn AND xor is not always 1: k=0, s=7, n=1, 0010 vs 0100."""
    k, s, n, j, j2, p, p2 = 0, 7, 1, 0, 2, 10, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (0, 1, 0, 0)
        and ham2_and_xor(four, four2) == 0
        and (a ^ b) == 0
        and (not cob_shaped(*four))
        and (not cob_shaped(*four2))
        and zab_parity(four, four2) == 0
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


def killed_ham3_xor_always_1() -> dict:
    """Hamming-3 bn AND xor is not always 1: k=3, s=31, n=8, 0010 vs 1001."""
    k, s, n, j, j2, p, p2 = 3, 31, 8, 0, 16, 48, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (1, 0, 0, 1)
        and (a ^ b) == 0
        and (not cob_shaped(*four))
        and (not cob_shaped(*four2))
        and zab_parity(four, four2) == 0
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


def killed_ham2_eq_reverse() -> dict:
    """Hamming-2 bn dual is not reverse: k=2, s=33, n=3, 0100 vs 1000."""
    k, s, n, j, j2, p, p2 = 2, 33, 3, 0, 6, 40, 28
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (0, 1, 0, 0)
        and four2 == (1, 0, 0, 0)
        and reverse_four(*four) == (0, 0, 1, 0)
        and four2 != reverse_four(*four)
        and ham2_and_xor(four, four2) == 1
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
    ia = json.loads(IA_JSON.read_text())
    ok = (
        ia["checks"]["all_ok"]
        and ia["verdict"]["nc_ham1_neighbor_is_flip_c"] == "LEMMA"
        and ia["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, zc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and zc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert zab_parity((0, 0, 1, 0), (0, 1, 0, 0)) == 0
    assert ham2_and_xor((0, 0, 1, 0), (0, 1, 0, 0)) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = zab_parity_table()
    zc = zab_cover()
    k0 = killed_ham2_xor_always_1()
    k1 = killed_ham3_xor_always_1()
    k2 = killed_ham2_eq_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, zc, k0, k1, k2, pref)
    dump = {
        "cycle": "IB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "zab_parity_table": {k: rt[k] for k in rt if k != "ok"},
        "zab_cover": {k: zc[k] for k in zc if k != "ok"},
        "killed_ham2_xor_always_1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_ham3_xor_always_1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_ham2_eq_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "same_cob_iff_even_zab_Hamming": True,
            "bn_ham2_slots_no_c": True,
            "bn_ham3_slots_always_c": True,
            "ham2_xor_always_1": False,
            "ham3_xor_always_1": False,
            "ham2_eq_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "same_cob_iff_even_zab_Hamming": "LEMMA",
            "bn_ham2_slots_no_c": "LEMMA",
            "bn_ham3_slots_always_c": "LEMMA",
            "ham2_xor_always_1": "KILLED",
            "ham3_xor_always_1": "KILLED",
            "ham2_eq_reverse": "KILLED",
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
    print("zab_parity_table", dump["zab_parity_table"])
    cov = dump["zab_cover"]
    print(
        "zab_cover n_ok",
        cov["n_ok"],
        "n_h2",
        cov["n_h2"],
        "n_h2_xor",
        cov["n_h2_xor"],
        "n_h3",
        cov["n_h3"],
        "n_h3_xor",
        cov["n_h3_xor"],
    )
    print("killed_ham2_xor_always_1", dump["killed_ham2_xor_always_1"])
    print("killed_ham3_xor_always_1", dump["killed_ham3_xor_always_1"])
    print("killed_ham2_eq_reverse", dump["killed_ham2_eq_reverse"])


if __name__ == "__main__":
    main()
