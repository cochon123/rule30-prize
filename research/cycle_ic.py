#!/usr/bin/env python3
"""Cycle IC: both-non-cob AND xor is determined by Hamming slots.

Hamming 3 AND xor is copy_j on slots (z,a,c), NOT(copy XOR cob) on
(z,b,c), and copy XOR cob on (a,b,c). Together with Cycles IA/IB that
gives every both-non-cob pair. Hamming-3 XOR is not the Hamming-2 zab
formula, not copy_j, and not reverse. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ic.py --certify
Dump: research/cycle_ic.json
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
from cycle_ib import HAM3_SLOTS, ham2_and_xor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IB_JSON = Path(__file__).resolve().parent / "cycle_ib.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def ham3_and_xor(four, four2) -> int:
    """AND xor if Hamming 3 with bit c; else -1."""
    slots = tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)
    _z, _a, b, c = four
    if slots == (0, 1, 3):
        return b
    if slots == (0, 2, 3):
        return 1 - (b ^ c)
    if slots == (1, 2, 3):
        return b ^ c
    return -1


def bn_and_xor(four, four2) -> int:
    """AND xor for both-non-cob pairs from Hamming slots; else -1."""
    if cob_shaped(*four) or cob_shaped(*four2):
        return -1
    ham = sum(x != y for x, y in zip(four, four2))
    if ham == 0:
        return 0
    if ham == 1:
        return 1 - four[2]
    h2 = ham2_and_xor(four, four2)
    if h2 != -1:
        return h2
    return ham3_and_xor(four, four2)


def bn_xor_table() -> dict:
    """16x16: both-non-cob AND xor equals bn_and_xor; ham3 formulas."""
    n_ok = n_bn = n_h3 = 0
    for b1 in range(16):
        four = tuple((b1 >> i) & 1 for i in range(3, -1, -1))
        for b2 in range(16):
            four2 = tuple((b2 >> i) & 1 for i in range(3, -1, -1))
            n_ok += 1
            pred = bn_and_xor(four, four2)
            xor_a = and_clause(*four) ^ and_clause(*four2)
            c1, c2 = cob_shaped(*four), cob_shaped(*four2)
            if c1 or c2:
                if pred != -1:
                    return {"ok": False, "cob": True, "four": four, "four2": four2}
                continue
            n_bn += 1
            if pred != xor_a:
                return {
                    "ok": False,
                    "xor": True,
                    "four": four,
                    "four2": four2,
                    "pred": pred,
                    "xor_a": xor_a,
                }
            ham = sum(x != y for x, y in zip(four, four2))
            if ham == 3:
                n_h3 += 1
                slots = tuple(
                    i for i, (x, y) in enumerate(zip(four, four2)) if x != y
                )
                if slots not in HAM3_SLOTS or ham3_and_xor(four, four2) != xor_a:
                    return {"ok": False, "h3": True, "four": four, "slots": slots}
    ok = n_ok == 256 and n_bn == 64 and n_h3 == 24
    return {"ok": ok, "n_ok": n_ok, "n_bn": n_bn, "n_h3": n_h3}


def _walk_bn(k: int, q: int) -> dict:
    """bn_and_xor on covering both-non-cob; ham3 formulas."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_bn = n_bn_xor = n_h3 = n_h3_xor = 0
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
                    if mixed_oneside(f, g) != (a ^ b):
                        return {"ok": False, "oneside": True, "k": k}
                    if a ^ b:
                        xor_fold ^= 1
                    continue
                if c1 and c2:
                    continue
                n_bn += 1
                pred = bn_and_xor(f, g)
                if pred != (a ^ b):
                    return {
                        "ok": False,
                        "bn": True,
                        "k": k,
                        "four": f,
                        "four2": g,
                        "pred": pred,
                    }
                ham = sum(x != y for x, y in zip(f, g))
                if ham == 3:
                    n_h3 += 1
                    if ham3_and_xor(f, g) != (a ^ b):
                        return {"ok": False, "h3": True, "k": k, "four": f}
                    if a ^ b:
                        n_h3_xor += 1
                if a ^ b:
                    n_bn_xor += 1
                    xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bn": n_bn,
        "n_bn_xor": n_bn_xor,
        "n_h3": n_h3,
        "n_h3_xor": n_h3_xor,
        "xor_j": xor_j,
    }


def bn_cover() -> dict:
    """bn_and_xor on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_bn = n_bn_xor = n_h3 = n_h3_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_bn(k, q)
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
            n_bn_xor += w["n_bn_xor"]
            n_h3 += w["n_h3"]
            n_h3_xor += w["n_h3_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_bn": w["n_bn"],
                "n_bn_xor": w["n_bn_xor"],
                "n_h3": w["n_h3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_bn == 2123
        and n_bn_xor == 1030
        and n_h3 == 795
        and n_h3_xor == 372
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bn": n_bn,
        "n_bn_xor": n_bn_xor,
        "n_h3": n_h3,
        "n_h3_xor": n_h3_xor,
        "rows": rows,
    }


def killed_ham3_eq_ham2() -> dict:
    """Hamming-3 XOR is not the Hamming-2 zab formula: k=3, s=31, 0010 vs 1001."""
    k, s, n, j, j2, p, p2 = 3, 31, 8, 0, 16, 48, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    zab2 = (four2[0], four2[1], four2[2], four[3])
    h2 = ham2_and_xor(four, zab2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (1, 0, 0, 1)
        and (a ^ b) == 0
        and h2 == 1
        and ham3_and_xor(four, four2) == 0
        and bn_and_xor(four, four2) == 0
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
        "h2": h2,
    }


def killed_ham3_xor_eq_copy() -> dict:
    """Hamming-3 XOR is not copy(j): k=1, s=17, n=1, 0100 vs 1111."""
    k, s, n, j, j2, p, p2 = 1, 17, 1, 0, 2, 20, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (0, 1, 0, 0)
        and four2 == (1, 1, 1, 1)
        and four[2] == 0
        and (a ^ b) == 1
        and ham3_and_xor(four, four2) == 1
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


def killed_ham3_eq_reverse() -> dict:
    """Hamming-3 bn dual is not reverse: k=1, s=17, n=1, 0100 vs 1111."""
    k, s, n, j, j2, p, p2 = 1, 17, 1, 0, 2, 20, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (0, 1, 0, 0)
        and four2 == (1, 1, 1, 1)
        and reverse_four(*four) == (0, 0, 1, 0)
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
    ib = json.loads(IB_JSON.read_text())
    ok = (
        ib["checks"]["all_ok"]
        and ib["verdict"]["same_cob_iff_even_zab_Hamming"] == "LEMMA"
        and ib["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, bc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and bc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert ham3_and_xor((0, 0, 1, 0), (1, 0, 0, 1)) == 0
    assert bn_and_xor((0, 1, 0, 0), (1, 1, 1, 1)) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = bn_xor_table()
    bc = bn_cover()
    k0 = killed_ham3_eq_ham2()
    k1 = killed_ham3_xor_eq_copy()
    k2 = killed_ham3_eq_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, bc, k0, k1, k2, pref)
    dump = {
        "cycle": "IC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bn_xor_table": {k: rt[k] for k in rt if k != "ok"},
        "bn_cover": {k: bc[k] for k in bc if k != "ok"},
        "killed_ham3_eq_ham2": {k: k0[k] for k in k0 if k != "ok"},
        "killed_ham3_xor_eq_copy": {k: k1[k] for k in k1 if k != "ok"},
        "killed_ham3_eq_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "ham3_AND_xor_slot_formula": True,
            "bn_AND_xor_from_Hamming_slots": True,
            "covering_bn_xor_eq_bn_and_xor": True,
            "ham3_eq_ham2_zab": False,
            "ham3_xor_eq_copy": False,
            "ham3_eq_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "ham3_AND_xor_slot_formula": "LEMMA",
            "bn_AND_xor_from_Hamming_slots": "LEMMA",
            "covering_bn_xor_eq_bn_and_xor": "LEMMA",
            "ham3_eq_ham2_zab": "KILLED",
            "ham3_xor_eq_copy": "KILLED",
            "ham3_eq_reverse": "KILLED",
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
    print("bn_xor_table", dump["bn_xor_table"])
    cov = dump["bn_cover"]
    print(
        "bn_cover n_ok",
        cov["n_ok"],
        "n_bn",
        cov["n_bn"],
        "n_bn_xor",
        cov["n_bn_xor"],
        "n_h3",
        cov["n_h3"],
        "n_h3_xor",
        cov["n_h3_xor"],
    )
    print("killed_ham3_eq_ham2", dump["killed_ham3_eq_ham2"])
    print("killed_ham3_xor_eq_copy", dump["killed_ham3_xor_eq_copy"])
    print("killed_ham3_eq_reverse", dump["killed_ham3_eq_reverse"])


if __name__ == "__main__":
    main()
