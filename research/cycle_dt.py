#!/usr/bin/env python3
"""Cycle DT: even spines never all equal through k=18 (covers through 19).

Cycle BO: covering at k+1 fails iff phi^{(6,10,18)}_k = I_{k+1}. Cycle DS
found that dangerous set empty through k=18. Algebra of doubling says the
three even spines are all equal iff the Fermat triple at k+1 is all equal,
so covering failure is the all-zero case and Fermat all-ones is the
all-equal-to-not-I case. On 2<=k<=18 the even spines are never all equal,
which is strictly stronger than dangerous-empty: it also forbids Fermat
all-ones at k=3..19 (k=2 is the unique all-ones in that range). Equivalent
slice: phi6=phi10 implies phi18 = phi6 xor 1, i.e. Theta(6*2^k)=1 on that
slice. Do not compute phi^{(3,5,9)} at k=16. Not a prize claim: never-equal
and covering for all k remain prefixes.

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
THETA_ZEROS = [2, 12]


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
                    if fail != ((a ^ i) == 0 and (b ^ i) == 0 and (g ^ i) == 0):
                        return False
                    if all_ones != ((a ^ i) == 1 and (b ^ i) == 1 and (g ^ i) == 1):
                        return False
    return True


def match_implies_complement_iff_never_all_equal() -> bool:
    """(a==b => g==a^1) is exactly not (a==b==g)."""
    for a in (0, 1):
        for b in (0, 1):
            for g in (0, 1):
                impl = (a != b) or (g == (a ^ 1))
                never = not (a == b == g)
                if impl != never:
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
    match610 = []
    theta = []
    cover_next = []
    fermat_all_ones_next = []
    for i, k in enumerate(ks):
        a, b, g, i_next = p6[i], p10[i], p18[i], p2[i]
        eq = a == b == g
        all_eq.append(k if eq else None)
        if a == b:
            match610.append(k)
        th = g ^ a
        theta.append(th)
        p3 = a ^ i_next
        p5 = b ^ i_next
        p9 = g ^ i_next
        cover_next.append(p3 | p5 | p9)
        fermat_all_ones_next.append(int(p3 == 1 and p5 == 1 and p9 == 1))
    return {
        "all_equal_k": [k for k in all_eq if k is not None],
        "match610_k": match610,
        "theta": theta,
        "theta_zero_k": [ks[i] for i, th in enumerate(theta) if th == 0],
        "cover_at_kplus1": cover_next,
        "fermat_all_ones_at_kplus1": fermat_all_ones_next,
        "impl_ok": all(
            p18[i] == (p6[i] ^ 1) for i, k in enumerate(ks) if k in match610
        ),
    }


def self_checks(c20, sp: dict, facts: dict, taut1: bool, taut2: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert sp["ok"] and taut1 and taut2
    assert sp["I"] == I_THRU_21
    assert facts["all_equal_k"] == []
    assert facts["impl_ok"]
    assert facts["match610_k"] == [5, 6, 7, 8, 11, 13, 14, 15, 17, 18]
    assert facts["theta_zero_k"] == THETA_ZEROS
    assert all(facts["cover_at_kplus1"])
    assert facts["fermat_all_ones_at_kplus1"] == [0] * len(sp["k"])
    # doubling matches BO Fermat values through k=13, without a new table
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
    assert sp["be_k2_phi"]["3"] == 1
    assert sp["be_k2_phi"]["5"] == 1
    assert sp["be_k2_phi"]["9"] == 1
    assert 0 in sp["I"][12:] and 1 in sp["I"][12:]
    assert sp["I"][12] == 0 and sp["I"][15] == 0 and sp["I"][19] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    taut1 = all_equal_iff_fermat_all_equal()
    taut2 = match_implies_complement_iff_never_all_equal()
    sp = ds_prefix()
    facts = spine_facts(sp)
    checks = self_checks(c20, sp, facts, taut1, taut2)
    dump = {
        "cycle": "DT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "I_kmax": 21,
        "I": sp["I"],
        "never_all_equal_k": [2, 18],
        "match610_k": facts["match610_k"],
        "theta_zero_k": facts["theta_zero_k"],
        "inferred_cover_k": list(range(3, 20)),
        "inferred_cover": facts["cover_at_kplus1"],
        "fermat_all_ones_k": [2],
        "lemmas": {
            "even_all_equal_iff_fermat_all_equal": True,
            "match610_implies_complement_iff_never_all_equal": True,
            "even_spines_never_all_equal_k_2_to_18": True,
            "fermat_all_ones_only_k2_through_19": True,
            "fermat_cover_3_to_19": True,
            "Theta6U_identically_1": False,
            "phi6_equals_phi10_all_k": False,
            "phi18_equals_not_phi6_all_k": False,
            "I_identically_1_kge13": False,
            "even_spines_never_all_equal_all_k": None,
            "fermat_cover_359_all_k": None,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "even_all_equal_iff_fermat_all_equal": "LEMMA",
            "match610_implies_complement_iff_never_all_equal": "LEMMA",
            "even_spines_never_all_equal_k_2_to_18": "PREFIX",
            "fermat_all_ones_only_k2_through_19": "PREFIX",
            "fermat_cover_3_to_19": "PREFIX",
            "Theta6U_identically_1": "KILLED",
            "phi6_equals_phi10_all_k": "KILLED",
            "phi18_equals_not_phi6_all_k": "KILLED",
            "I_identically_1_kge13": "KILLED",
            "even_spines_never_all_equal_all_k": "PREFIX",
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
    print("never_all_equal", facts["all_equal_k"])
    print("match610_k", facts["match610_k"])
    print("theta_zero_k", facts["theta_zero_k"])
    print("fermat_all_ones_next", facts["fermat_all_ones_at_kplus1"])


if __name__ == "__main__":
    main()
