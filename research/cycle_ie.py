#!/usr/bin/env python3
"""Cycle IE: mixed Hamming-1 AND xor is a slot formula.

Flip z: XOR is a XOR (b OR c). Flip a: cob-bit (z XOR b) equals
(b OR c). Flip b: a XOR ((a==z) OR c). mix_and_xor stitches Hamming
1-4 so every mixed pair is determined. Mixed Hamming-1 XOR is not
always 1, not the left AND factor, and not NOT copy(j). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ie.py --certify
Dump: research/cycle_ie.json
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
from cycle_hy import mixed_oneside
from cycle_id import MIX_HAM1_SLOTS
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ID_JSON = Path(__file__).resolve().parent / "cycle_id.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _slots(four, four2):
    return tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)


def mix_ham1_and_xor(four, four2) -> int:
    """AND xor if mixed Hamming 1; else -1."""
    slots = _slots(four, four2)
    z, a, b, c = four
    if slots == (0,):
        return int(a != (b | c))
    if slots == (1,):
        return int((z ^ b) == (b | c))
    if slots == (2,):
        return int(a != (int(a == z) | c))
    return -1


def mix_and_xor(four, four2) -> int:
    """AND xor for mixed pairs from Hamming slots; else -1."""
    if cob_shaped(*four) == cob_shaped(*four2):
        return -1
    h1 = mix_ham1_and_xor(four, four2)
    if h1 != -1:
        return h1
    z, a, b, c = four
    cob = int(cob_shaped(*four))
    slots = _slots(four, four2)
    if slots == (0, 3):
        return int(a != (b | (c ^ cob)))
    if slots == (1, 3):
        return int((a ^ cob) != (b | (c ^ cob)))
    if slots == (2, 3):
        return int(a != ((b ^ cob) | (c ^ cob)))
    if slots == (0, 1, 2):
        return int((a ^ cob) != ((b ^ cob) | c))
    if slots == (0, 1, 2, 3):
        return int((a ^ cob) != ((b ^ cob) | (c ^ cob)))
    return -1


def mix_xor_table() -> dict:
    """16x16: mixed AND xor equals mix_and_xor; ham1 formulas."""
    n_ok = n_mix = n_h1 = 0
    for b1 in range(16):
        four = tuple((b1 >> i) & 1 for i in range(3, -1, -1))
        for b2 in range(16):
            four2 = tuple((b2 >> i) & 1 for i in range(3, -1, -1))
            n_ok += 1
            pred = mix_and_xor(four, four2)
            xor_a = and_clause(*four) ^ and_clause(*four2)
            c1, c2 = cob_shaped(*four), cob_shaped(*four2)
            if c1 == c2:
                if pred != -1:
                    return {"ok": False, "same": True, "four": four, "four2": four2}
                continue
            n_mix += 1
            if pred != xor_a or pred != mixed_oneside(four, four2):
                return {
                    "ok": False,
                    "xor": True,
                    "four": four,
                    "four2": four2,
                    "pred": pred,
                    "xor_a": xor_a,
                }
            slots = _slots(four, four2)
            if slots in MIX_HAM1_SLOTS:
                n_h1 += 1
                if mix_ham1_and_xor(four, four2) != xor_a:
                    return {"ok": False, "h1": True, "four": four, "slots": slots}
    ok = n_ok == 256 and n_mix == 128 and n_h1 == 48
    return {"ok": ok, "n_ok": n_ok, "n_mix": n_mix, "n_h1": n_h1}


def _walk_mix(k: int, q: int) -> dict:
    """mix_and_xor on covering mixed pairs; ham1 formulas."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_mix = n_mix_xor = n_h1 = n_h1_xor = 0
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
                if c1 == c2:
                    if a ^ b:
                        xor_fold ^= 1
                    continue
                n_mix += 1
                pred = mix_and_xor(f, g)
                if pred != (a ^ b) or pred != mixed_oneside(f, g):
                    return {
                        "ok": False,
                        "mix": True,
                        "k": k,
                        "four": f,
                        "four2": g,
                        "pred": pred,
                    }
                slots = _slots(f, g)
                if slots in MIX_HAM1_SLOTS:
                    n_h1 += 1
                    if mix_ham1_and_xor(f, g) != (a ^ b):
                        return {"ok": False, "h1": True, "k": k, "four": f}
                    if a ^ b:
                        n_h1_xor += 1
                if a ^ b:
                    n_mix_xor += 1
                    xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_h1": n_h1,
        "n_h1_xor": n_h1_xor,
        "xor_j": xor_j,
    }


def mix_cover() -> dict:
    """mix_and_xor on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_mix = n_mix_xor = n_h1 = n_h1_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_mix(k, q)
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
            n_mix += w["n_mix"]
            n_mix_xor += w["n_mix_xor"]
            n_h1 += w["n_h1"]
            n_h1_xor += w["n_h1_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_mix": w["n_mix"],
                "n_mix_xor": w["n_mix_xor"],
                "n_h1": w["n_h1"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_mix == 4383
        and n_mix_xor == 2216
        and n_h1 == 1666
        and n_h1_xor == 846
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_h1": n_h1,
        "n_h1_xor": n_h1_xor,
        "rows": rows,
    }


def killed_mix_ham1_xor_always_1() -> dict:
    """Mixed Hamming-1 XOR is not always 1: k=2, s=23, 1000 vs 0000."""
    k, s, n, j, j2, p, p2 = 2, 23, 8, 0, 16, 40, 8
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    xor_a = and_clause(*four) ^ and_clause(*four2)
    ok = (
        four == (1, 0, 0, 0)
        and four2 == (0, 0, 0, 0)
        and _slots(four, four2) == (0,)
        and xor_a == 0
        and cob_shaped(*four) != cob_shaped(*four2)
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
        "xor": xor_a,
    }


def killed_mix_ham1_xor_eq_np() -> dict:
    """Mixed Hamming-1 XOR is not left a XOR (b OR c): k=2, s=9, 0000 vs 0100."""
    k, s, n, j, j2, p, p2 = 2, 9, 15, 13, 17, 14, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    z, a, b, c = four
    xor_a = and_clause(*four) ^ and_clause(*four2)
    np = int(a != (b | c))
    ok = (
        four == (0, 0, 0, 0)
        and four2 == (0, 1, 0, 0)
        and _slots(four, four2) == (1,)
        and xor_a == 1
        and np == 0
        and cob_shaped(*four) != cob_shaped(*four2)
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
        "xor": xor_a,
        "np": np,
    }


def killed_mix_ham1_xor_eq_not_b() -> dict:
    """Mixed Hamming-1 XOR is not NOT copy(j): k=1, s=13, 0011 vs 0111."""
    k, s, n, j, j2, p, p2 = 1, 13, 3, 1, 5, 18, 10
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    xor_a = and_clause(*four) ^ and_clause(*four2)
    not_b = 1 - four[2]
    ok = (
        four == (0, 0, 1, 1)
        and four2 == (0, 1, 1, 1)
        and _slots(four, four2) == (1,)
        and xor_a == 1
        and not_b == 0
        and cob_shaped(*four) != cob_shaped(*four2)
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
        "xor": xor_a,
        "not_b": not_b,
    }


def prefixes() -> dict:
    cid = json.loads(ID_JSON.read_text())
    ok = (
        cid["checks"]["all_ok"]
        and cid["verdict"]["mix_ham1_slots_no_c"] == "LEMMA"
        and cid["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, mc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and mc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert mix_ham1_and_xor((1, 0, 0, 0), (0, 0, 0, 0)) == 0
    assert mix_and_xor((0, 0, 0, 0), (0, 1, 0, 0)) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mix_xor_table()
    mc = mix_cover()
    k0 = killed_mix_ham1_xor_always_1()
    k1 = killed_mix_ham1_xor_eq_np()
    k2 = killed_mix_ham1_xor_eq_not_b()
    pref = prefixes()
    checks = self_checks(c20, rt, mc, k0, k1, k2, pref)
    dump = {
        "cycle": "IE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mix_xor_table": {k: rt[k] for k in rt if k != "ok"},
        "mix_cover": {k: mc[k] for k in mc if k != "ok"},
        "killed_mix_ham1_xor_always_1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_mix_ham1_xor_eq_np": {k: k1[k] for k in k1 if k != "ok"},
        "killed_mix_ham1_xor_eq_not_b": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "mix_ham1_AND_xor_slot_formula": True,
            "mix_AND_xor_from_Hamming_slots": True,
            "covering_mix_xor_eq_mix_and_xor": True,
            "mix_ham1_xor_always_1": False,
            "mix_ham1_xor_eq_np": False,
            "mix_ham1_xor_eq_not_b": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mix_ham1_AND_xor_slot_formula": "LEMMA",
            "mix_AND_xor_from_Hamming_slots": "LEMMA",
            "covering_mix_xor_eq_mix_and_xor": "LEMMA",
            "mix_ham1_xor_always_1": "KILLED",
            "mix_ham1_xor_eq_np": "KILLED",
            "mix_ham1_xor_eq_not_b": "KILLED",
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
    print("mix_xor_table", dump["mix_xor_table"])
    cov = dump["mix_cover"]
    print(
        "mix_cover n_ok",
        cov["n_ok"],
        "n_mix",
        cov["n_mix"],
        "n_mix_xor",
        cov["n_mix_xor"],
        "n_h1",
        cov["n_h1"],
        "n_h1_xor",
        cov["n_h1_xor"],
    )
    print("killed_mix_ham1_xor_always_1", dump["killed_mix_ham1_xor_always_1"])
    print("killed_mix_ham1_xor_eq_np", dump["killed_mix_ham1_xor_eq_np"])
    print("killed_mix_ham1_xor_eq_not_b", dump["killed_mix_ham1_xor_eq_not_b"])


if __name__ == "__main__":
    main()
