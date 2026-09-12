#!/usr/bin/env python3
"""Cycle HU: odd-s AND iff non-coboundary and a XOR (b OR c).

Packed AND fires iff the even-s 4-tuple (z,a,b,c) is not
coboundary-shaped and a XOR (b OR c) = 1. That is AND_ONES as two
Boolean clauses: Cycle HT kills cob; the leftover 8 non-cob tuples
fire iff the first AND factor a^(b|c) is 1. Not AND iff non-cob;
not AND iff a^(b|c)=1; not G=1 AND iff FRESH. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hu.py --certify
Dump: research/cycle_hu.json
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
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_hi import CONT, FRESH
from cycle_ht import cob_shaped
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HT_JSON = Path(__file__).resolve().parent / "cycle_ht.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def and_clause(z: int, a: int, b: int, c: int) -> int:
    """Odd-s AND: non-coboundary and a XOR (b OR c)."""
    return int((not cob_shaped(z, a, b, c)) and (a != (b | c)))


def and_clause_table() -> dict:
    """16-row: AND iff and_clause; equals AND_ONES; non-cob np=1 => npm=1."""
    n_ok = n_and = 0
    got = []
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        z, a, b, c = four
        cl = and_clause(*four)
        an = and_from_tuple(*four)
        new_p = a ^ (b | c)
        new_pm1 = z ^ (a | b)
        if cl != an:
            return {"ok": False, "clause": True, "four": four, "cl": cl, "an": an}
        if an != int(four in AND_ONES):
            return {"ok": False, "ones": True, "four": four}
        if an != (new_p & new_pm1):
            return {"ok": False, "factors": True, "four": four}
        if (not cob_shaped(*four)) and new_p and not new_pm1:
            return {"ok": False, "redundant": True, "four": four}
        if cl:
            got.append(four)
            n_and += 1
        n_ok += 1
    ok = n_ok == 16 and n_and == 4 and tuple(got) == AND_ONES
    return {"ok": ok, "n_ok": n_ok, "n_and": n_and}


def _walk_clause(k: int, q: int) -> dict:
    """and_clause on packed covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_and = n_g1 = n_fresh = n_cont = xor_all = 0
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
                cl = and_clause(*four)
                if packed != cl:
                    return {"ok": False, "pack": True, "k": k, "four": four}
                n_ok += 1
                if packed:
                    n_and += 1
                    if four in FRESH:
                        n_fresh += 1
                    elif four == CONT:
                        n_cont += 1
                    else:
                        return {"ok": False, "ones": True, "k": k, "four": four}
                    if G(n, j):
                        n_g1 += 1
                        xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_and": n_and,
        "n_g1": n_g1,
        "n_fresh": n_fresh,
        "n_cont": n_cont,
        "xor_all": xor_all,
    }


def clause_cover() -> dict:
    """and_clause on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_and = n_g1 = n_fresh = n_cont = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_clause(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_all"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_all"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_all"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_and += w["n_and"]
            n_g1 += w["n_g1"]
            n_fresh += w["n_fresh"]
            n_cont += w["n_cont"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_and": w["n_and"],
                "n_g1": w["n_g1"],
                "n_fresh": w["n_fresh"],
                "n_cont": w["n_cont"],
                "xor_all": w["xor_all"],
            }
        rows[str(k)] = krow
    ok = n_and == n_fresh + n_cont
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_and": n_and,
        "n_g1": n_g1,
        "n_fresh": n_fresh,
        "n_cont": n_cont,
        "rows": rows,
    }


def killed_and_iff_noncob() -> dict:
    """AND is not iff non-cob: k=1, s=11, four=1111."""
    k, s, n, j, p = 1, 11, 4, 3, 14
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = four == (1, 1, 1, 1) and (not cob_shaped(*four)) and packed == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
    }


def killed_and_iff_a_xor_borc() -> dict:
    """AND is not iff a XOR (b OR c): k=0, s=5, four=0001 cob."""
    k, s, n, j, p = 0, 5, 2, 1, 8
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    z, a, b, c = four
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = (
        four == (0, 0, 0, 1)
        and cob_shaped(*four)
        and a != (b | c)
        and packed == 0
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
    }


def killed_g1_and_iff_fresh() -> dict:
    """G=1 AND is not iff FRESH: k=1, s=13, four=0011 CONT."""
    k, s, n, j, p = 1, 13, 3, 1, 18
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = four == (0, 0, 1, 1) and four not in FRESH and packed == 1 and G(n, j) == 1
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


def prefixes() -> dict:
    ht = json.loads(HT_JSON.read_text())
    ok = (
        ht["checks"]["all_ok"]
        and ht["verdict"]["cob_shaped_AND_identically_0"] == "LEMMA"
        and ht["verdict"]["AND_ONES_not_cob_shaped"] == "LEMMA"
        and ht["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, at: dict, ac: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert at["ok"] and ac["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert and_clause(0, 1, 0, 0) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    at = and_clause_table()
    ac = clause_cover()
    k0 = killed_and_iff_noncob()
    k1 = killed_and_iff_a_xor_borc()
    k2 = killed_g1_and_iff_fresh()
    pref = prefixes()
    checks = self_checks(c20, at, ac, k0, k1, k2, pref)
    dump = {
        "cycle": "HU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "and_clause_table": {k: at[k] for k in at if k != "ok"},
        "clause_cover": {k: ac[k] for k in ac if k != "ok"},
        "killed_and_iff_noncob": {k: k0[k] for k in k0 if k != "ok"},
        "killed_and_iff_a_xor_borc": {k: k1[k] for k in k1 if k != "ok"},
        "killed_g1_and_iff_fresh": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "AND_iff_noncob_and_a_xor_bORc": True,
            "AND_clause_eq_AND_ONES": True,
            "AND_iff_noncob": False,
            "AND_iff_a_xor_bORc": False,
            "G1_AND_iff_FRESH": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "AND_iff_noncob_and_a_xor_bORc": "LEMMA",
            "AND_clause_eq_AND_ONES": "LEMMA",
            "AND_iff_noncob": "KILLED",
            "AND_iff_a_xor_bORc": "KILLED",
            "G1_AND_iff_FRESH": "KILLED",
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
    print("and_clause_table", dump["and_clause_table"])
    print(
        "clause_cover n_ok",
        dump["clause_cover"]["n_ok"],
        "n_and",
        dump["clause_cover"]["n_and"],
        "n_g1",
        dump["clause_cover"]["n_g1"],
        "n_fresh",
        dump["clause_cover"]["n_fresh"],
        "n_cont",
        dump["clause_cover"]["n_cont"],
    )
    print("killed_and_iff_noncob", dump["killed_and_iff_noncob"])
    print("killed_and_iff_a_xor_borc", dump["killed_and_iff_a_xor_borc"])
    print("killed_g1_and_iff_fresh", dump["killed_g1_and_iff_fresh"])


if __name__ == "__main__":
    main()
