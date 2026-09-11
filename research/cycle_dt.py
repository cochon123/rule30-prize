#!/usr/bin/env python3
"""Cycle DT: if phi6=phi10=1 then phi18=0, through k=18; all-zero only at 14.

Cycle BO: covering at k+1 fails iff phi^{(6,10,18)}_k = I_{k+1}. Doubling
identifies all-equal even spines with an all-equal Fermat triple at k+1
(failure = all-zero Fermat; all-ones Fermat = all-equal-to-not-I).

On 2<=k<=18, phi6=phi10=1 forces phi18=0, so the even spines are never
all 1. The only all-equal row is k=14 (all 0, I_15=1), which produces
Fermat all-ones at k=15, not a covering failure. Hence I=1 dangerous is
empty on that prefix, and covering failure can only be all-zero spines
with I=0, which does not occur. The two-sided slice phi6=phi10 =>
phi18=not phi6 fails at k=14. Do not compute phi^{(3,5,9)} at k=16.
Not a prize claim: the one-sided implication remains a prefix.

Run: python3 research/cycle_dt.py --certify
Dump: research/cycle_dt.json
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
from cycle_ca import KNOWN20, packed_center_bits

OUT = Path(__file__).resolve().with_suffix(".json")
DS_JSON = Path(__file__).resolve().parent / "cycle_ds.json"
BO_JSON = Path(__file__).resolve().parent / "cycle_bo.json"
BE_JSON = Path(__file__).resolve().parent / "cycle_be.json"

I_THRU_21 = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
CANDIDATE_K = [5, 8, 11, 15, 18]
MATCH11_K = [5, 6, 7, 8, 11, 18]
MATCH00_K = [13, 14, 15, 17]
ALL_EQUAL_K = [14]
THETA_ZEROS = [2, 12, 14]


def all_equal_iff_fermat_all_equal() -> bool:
    """On every 0-1 triple (a,b,g) with I, even all-equal iff Fermat all-equal."""
    for a in (0, 1):
        for b in (0, 1):
            for g in (0, 1):
                for i in (0, 1):
                    even_eq = a == b == g
                    fermat_eq = (a ^ i) == (b ^ i) == (g ^ i)
                    if even_eq != fermat_eq:
                        return False
                    fail = even_eq and a == i
                    all_ones = even_eq and a == (i ^ 1)
                    if fail != ((a ^ i) == (b ^ i) == (g ^ i) == 0):
                        return False
                    if all_ones != ((a ^ i) == (b ^ i) == (g ^ i) == 1):
                        return False
                    # all-1 even spines with I=1 is dangerous of type I=1
                    if (a, b, g, i) == (1, 1, 1, 1) and not fail:
                        return False
                    # one-sided 11 => phi18=0 forbids that tuple
                    if a == b == 1 and g == 0:
                        if fail:
                            return False
    return True


def onesided_kills_I1_dangerous() -> bool:
    """If a=b=1 => g=0, then (a,b,g,I) never equals (1,1,1,1)."""
    for a in (0, 1):
        for b in (0, 1):
            for g in (0, 1):
                if a == b == 1 and g != 0:
                    continue
                for i in (0, 1):
                    if (a, b, g, i) == (1, 1, 1, 1):
                        return False
    return True


def ds_prefix() -> dict:
    ds = json.loads(DS_JSON.read_text())
    bo = json.loads(BO_JSON.read_text())
    be = json.loads(BE_JSON.read_text())
    p = ds["prefix"]
    ok = (
        ds["checks"]["all_ok"]
        and ds["empty_upto"] == 18
        and ds["dangerous_k"] == []
        and ds["candidate_k"] == CANDIDATE_K
        and all(p["phi18_known"])
        and bo["checks"]["all_ok"]
        and bo["dangerous_k"] == []
        and be["checks"]["all_ok"]
    )
    be_k2 = next(rec for rec in be["annulus"] if rec["k"] == 2)
    return {
        "ok": ok,
        "k": p["k"],
        "phi2": p["phi2"],
        "phi6": p["phi6"],
        "phi10": p["phi10"],
        "phi18": p["phi18"],
        "I": ds["I"],
        "bo": bo["prefix"],
        "be_k2_phi": be_k2["phi"],
        "be_k2_cover": be_k2["cover359"],
    }


def spine_facts(sp: dict) -> dict:
    ks, p2, p6, p10, p18 = sp["k"], sp["phi2"], sp["phi6"], sp["phi10"], sp["phi18"]
    all_eq = []
    match11 = []
    match00 = []
    theta_zero = []
    cover_next = []
    fermat_all_ones_next = []
    twosided_fail = []
    onesided_ok = True
    for i, k in enumerate(ks):
        a, b, g, i_next = p6[i], p10[i], p18[i], p2[i]
        if a == b == g:
            all_eq.append(k)
        if a == b == 1:
            match11.append(k)
            if g != 0:
                onesided_ok = False
        if a == b == 0:
            match00.append(k)
        if a == b and g != (a ^ 1):
            twosided_fail.append(k)
        if (g ^ a) == 0:
            theta_zero.append(k)
        p3, p5, p9 = a ^ i_next, b ^ i_next, g ^ i_next
        cover_next.append(p3 | p5 | p9)
        fermat_all_ones_next.append(int(p3 == p5 == p9 == 1))
    ones_at = [ks[i] + 1 for i, v in enumerate(fermat_all_ones_next) if v]
    return {
        "all_equal_k": all_eq,
        "match11_k": match11,
        "match00_k": match00,
        "twosided_fail_k": twosided_fail,
        "theta_zero_k": theta_zero,
        "cover_at_kplus1": cover_next,
        "fermat_all_ones_at": ones_at,
        "onesided_ok": onesided_ok,
        "i1_dangerous": [
            k for i, k in enumerate(ks)
            if p6[i] == p10[i] == p18[i] == p2[i] == 1
        ],
        "i0_dangerous": [
            k for i, k in enumerate(ks)
            if p6[i] == p10[i] == p18[i] == p2[i] == 0
        ],
    }


def self_checks(c20, sp: dict, facts: dict, taut1: bool, taut2: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert sp["ok"] and taut1 and taut2
    assert sp["I"] == I_THRU_21
    assert facts["all_equal_k"] == ALL_EQUAL_K
    assert facts["match11_k"] == MATCH11_K
    assert facts["match00_k"] == MATCH00_K
    assert facts["onesided_ok"] and facts["twosided_fail_k"] == [14]
    assert facts["theta_zero_k"] == THETA_ZEROS
    assert all(facts["cover_at_kplus1"])
    assert facts["fermat_all_ones_at"] == [15]
    assert facts["i1_dangerous"] == [] and facts["i0_dangerous"] == []
    bo = sp["bo"]
    nbo = len(bo["k"])
    assert sp["k"][:nbo] == bo["k"]
    assert sp["phi6"][:nbo] == bo["phi6"]
    assert sp["phi10"][:nbo] == bo["phi10"]
    assert sp["phi18"][:nbo] == bo["phi18"]
    for i in range(nbo - 1):
        assert (sp["phi6"][i] ^ sp["phi2"][i]) == bo["phi3"][i + 1]
        assert (sp["phi10"][i] ^ sp["phi2"][i]) == bo["phi5"][i + 1]
        assert (sp["phi18"][i] ^ sp["phi2"][i]) == bo["phi9"][i + 1]
        assert facts["cover_at_kplus1"][i] == bo["cover359"][i + 1]
    assert sp["be_k2_cover"] == 1
    assert sp["be_k2_phi"]["3"] == sp["be_k2_phi"]["5"] == sp["be_k2_phi"]["9"] == 1
    assert 0 in sp["I"][12:] and 1 in sp["I"][12:]
    assert sp["I"][12] == 0 and sp["I"][15] == 0 and sp["I"][19] == 0
    # k=14 all-zero even spines, I_15 = phi2_14 = 1
    i14 = sp["k"].index(14)
    assert sp["phi6"][i14] == sp["phi10"][i14] == sp["phi18"][i14] == 0
    assert sp["phi2"][i14] == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    taut1 = all_equal_iff_fermat_all_equal()
    taut2 = onesided_kills_I1_dangerous()
    sp = ds_prefix()
    facts = spine_facts(sp)
    checks = self_checks(c20, sp, facts, taut1, taut2)
    dump = {
        "cycle": "DT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "I_kmax": 21,
        "I": sp["I"],
        "all_equal_k": facts["all_equal_k"],
        "match11_k": facts["match11_k"],
        "match00_k": facts["match00_k"],
        "twosided_fail_k": facts["twosided_fail_k"],
        "theta_zero_k": facts["theta_zero_k"],
        "inferred_cover_k": list(range(3, 20)),
        "inferred_cover": facts["cover_at_kplus1"],
        "fermat_all_ones_k": [2] + facts["fermat_all_ones_at"],
        "i1_dangerous_k": facts["i1_dangerous"],
        "i0_dangerous_k": facts["i0_dangerous"],
        "lemmas": {
            "even_all_equal_iff_fermat_all_equal": True,
            "onesided_11_kills_I1_dangerous": True,
            "phi6_phi10_1_implies_phi18_0_k_2_to_18": True,
            "all_zero_even_spines_only_k14": True,
            "fermat_all_ones_at_2_and_15": True,
            "fermat_cover_3_to_19": True,
            "twosided_match_implies_complement": False,
            "even_spines_never_all_equal": False,
            "fermat_all_ones_only_k2": False,
            "Theta6U_identically_1": False,
            "I_identically_1_kge13": False,
            "phi6_phi10_1_implies_phi18_0_all_k": None,
            "fermat_cover_359_all_k": None,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "even_all_equal_iff_fermat_all_equal": "LEMMA",
            "onesided_11_kills_I1_dangerous": "LEMMA",
            "phi6_phi10_1_implies_phi18_0_k_2_to_18": "PREFIX",
            "all_zero_even_spines_only_k14": "PREFIX",
            "fermat_all_ones_at_2_and_15": "PREFIX",
            "fermat_cover_3_to_19": "PREFIX",
            "twosided_match_implies_complement": "KILLED",
            "even_spines_never_all_equal": "KILLED",
            "fermat_all_ones_only_k2": "KILLED",
            "Theta6U_identically_1": "KILLED",
            "I_identically_1_kge13": "KILLED",
            "phi6_phi10_1_implies_phi18_0_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "period_H_seed_all_k": "PREFIX",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("all_equal_k", facts["all_equal_k"])
    print("match11_k", facts["match11_k"])
    print("twosided_fail_k", facts["twosided_fail_k"])
    print("fermat_all_ones_k", dump["fermat_all_ones_k"])
    print("theta_zero_k", facts["theta_zero_k"])


if __name__ == "__main__":
    main()
