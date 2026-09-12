#!/usr/bin/env python3
"""Cycle HI: odd-s AND splits into 0011 continuation and three fresh patterns.

On covering (n,j), odd-s AND is the even-s 4-tuple at p=T-2j. It
equals even-s AND at the same p iff the tuple is 0011 (continuation);
otherwise it is a fresh 0010, 0100, or 1001. Odd-s AND is not even-s
AND; even-s AND live does not imply odd-s AND; 0011 XOR is not odd-s
J6. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_hi.py --certify
Dump: research/cycle_hi.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HH_JSON = Path(__file__).resolve().parent / "cycle_hh.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

FRESH = ((0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1))
CONT = (0, 0, 1, 1)


def _walk_split(k: int, q: int) -> dict:
    """4-tuple lift + continuation/fresh split on odd-s even-rho columns."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_cont = n_fresh = n_die = 0
    xor_all = xor_cont = 0
    fire = {t: 0 for t in AND_ONES}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            Aeven = (prev << 1) & prev
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                tup = (
                    bit_at(prev, p - 3),
                    bit_at(prev, p - 2),
                    bit_at(prev, p - 1),
                    bit_at(prev, p),
                )
                o = (Aodd >> p) & 1
                e = (Aeven >> p) & 1
                if and_from_tuple(*tup) != o:
                    return {"ok": False, "lift": True, "k": k, "q": q, "s": s, "p": p}
                if (o and e) != (tup == CONT):
                    return {"ok": False, "cont": True, "k": k, "q": q, "tup": tup, "o": o, "e": e}
                if (o and not e) != (tup in FRESH):
                    return {"ok": False, "fresh": True, "k": k, "q": q, "tup": tup}
                n_ok += 1
                if o and e:
                    n_cont += 1
                if o and not e:
                    n_fresh += 1
                if e and not o:
                    n_die += 1
                if o:
                    fire[tup] += 1
                if o and G(n, j):
                    xor_all ^= 1
                    if tup == CONT:
                        xor_cont ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_cont": n_cont,
        "n_fresh": n_fresh,
        "n_die": n_die,
        "xor_all": xor_all,
        "xor_cont": xor_cont,
        "fire": {str(t): fire[t] for t in AND_ONES},
    }


def and_split() -> dict:
    """Lift + split on J6/J10, k<=6."""
    n_ok = n_cont = n_fresh = n_die = 0
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
                if w["xor_all"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_all"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor10": True, "k": k, "got": w["xor_all"], "want": want}
            n_ok += w["n_ok"]
            n_cont += w["n_cont"]
            n_fresh += w["n_fresh"]
            n_die += w["n_die"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_cont": w["n_cont"],
                "n_fresh": w["n_fresh"],
                "n_die": w["n_die"],
                "xor_all": w["xor_all"],
                "xor_cont": w["xor_cont"],
            }
        rows[str(k)] = krow
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_cont": n_cont,
        "n_fresh": n_fresh,
        "n_die": n_die,
        "rows": rows,
    }


def killed_odd_eq_even() -> dict:
    """Odd-s AND is not even-s AND at the same p: k=0, J6, 3 vs 0."""
    w = _walk_split(0, 6)
    ok = w["n_fresh"] == 3 and w["n_cont"] == 0 and w["n_die"] == 0
    return {
        "ok": ok,
        "k": 0,
        "n_fresh": w["n_fresh"],
        "n_cont": w["n_cont"],
        "n_die": w["n_die"],
    }


def killed_even_implies_odd() -> dict:
    """Even-s AND live does not imply odd-s AND: k=2, s=9, tup=0111."""
    k = 2
    U = 1 << k
    T, t0 = 6 * U, 2 * U
    row = 1
    for _ in range(9):
        prev = row
        row = rule30_step(row)
    s, n, j, p = 9, 7, 7, 10
    tup = (
        bit_at(prev, p - 3),
        bit_at(prev, p - 2),
        bit_at(prev, p - 1),
        bit_at(prev, p),
    )
    Aodd = (row << 1) & row
    Aeven = (prev << 1) & prev
    o, e = (Aodd >> p) & 1, (Aeven >> p) & 1
    ok = tup == (0, 1, 1, 1) and e == 1 and o == 0 and G(n, j) == 1
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "tup": list(tup), "e": e, "o": o}


def killed_cont_xor_eq_J() -> dict:
    """0011-slice XOR is not odd-s J6: k=0, 0 vs 1."""
    w = _walk_split(0, 6)
    hf = json.loads(HF_JSON.read_text())
    want = hf["j6_j_index"]["rows"]["0"]["xor_odd"]
    ok = w["xor_cont"] == 0 and want == 1 and w["xor_all"] == 1
    return {"ok": ok, "k": 0, "xor_cont": w["xor_cont"], "xor_odd": want}


def prefixes() -> dict:
    hh = json.loads(HH_JSON.read_text())
    hf = json.loads(HF_JSON.read_text())
    ok = (
        hh["checks"]["all_ok"]
        and hf["checks"]["all_ok"]
        and hh["verdict"]["AND_step_eq_4tuple_ones"] == "LEMMA"
        and hh["verdict"]["odd_s_eq_T_minus_2n_minus_1"] == "LEMMA"
        and hf["verdict"]["J6_eq_in_support_j_index_Q2"] == "LEMMA"
        and hh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, sp: dict, ke: dict, ki: dict, kc: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert sp["ok"] and ke["ok"] and ki["ok"] and kc["ok"] and pref["ok"]
    assert CONT in AND_ONES and all(t in AND_ONES for t in FRESH)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    sp = and_split()
    ke = killed_odd_eq_even()
    ki = killed_even_implies_odd()
    kc = killed_cont_xor_eq_J()
    pref = prefixes()
    checks = self_checks(c20, sp, ke, ki, kc, pref)
    dump = {
        "cycle": "HI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "and_split": {k: sp[k] for k in sp if k != "ok"},
        "killed_odd_eq_even": {k: ke[k] for k in ke if k != "ok"},
        "killed_even_implies_odd": {k: ki[k] for k in ki if k != "ok"},
        "killed_cont_xor_eq_J": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "odd_s_AND_eq_even_s_4tuple": True,
            "continuation_iff_0011": True,
            "fresh_iff_0010_or_0100_or_1001": True,
            "odd_s_AND_eq_even_s_AND": False,
            "even_s_AND_implies_odd_s_AND": False,
            "0011_XOR_eq_odd_s_J6": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_AND_eq_even_s_4tuple": "LEMMA",
            "continuation_iff_0011": "LEMMA",
            "fresh_iff_0010_or_0100_or_1001": "LEMMA",
            "odd_s_AND_eq_even_s_AND": "KILLED",
            "even_s_AND_implies_odd_s_AND": "KILLED",
            "0011_XOR_eq_odd_s_J6": "KILLED",
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
    print(
        "and_split n_ok",
        dump["and_split"]["n_ok"],
        "n_cont",
        dump["and_split"]["n_cont"],
        "n_fresh",
        dump["and_split"]["n_fresh"],
        "n_die",
        dump["and_split"]["n_die"],
    )
    print("killed_odd_eq_even", dump["killed_odd_eq_even"])
    print("killed_even_implies_odd", dump["killed_even_implies_odd"])
    print("killed_cont_xor_eq_J", dump["killed_cont_xor_eq_J"])


if __name__ == "__main__":
    main()
