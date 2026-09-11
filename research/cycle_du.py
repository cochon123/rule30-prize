#!/usr/bin/env python3
"""Cycle DU: at-most-one-odd per annulus implies the period-H seed for all k.

pi_1=1, and unique continuation multiplies the left-word period by 2 on an
odd ident-0 and preserves it on reconstruct / even ident-0. Odds that sit
in the k-word are those in (2^m, 2^{m+1}] for 1<=m<k. If each of those
k-1 annuli has at most one odd, then pi_k | 2^{k-1}, i.e. the period-H
seed holds. The exact formula 2^{ceil(log2 k)} is strictly stronger than
this bound. On the prize orbit the hypothesis holds through k=19 (Cycles
DE/DO). Do not push pi past 19.

Separately, Cycle DT's one-sided 11=>0 reduces covering failure to the
I=0 all-zero even-spine kernel c_U=c_{2U}=c_{6U}=c_{10U}=c_{18U}. That
kernel is empty through k=18. Do not compute phi^{(3,5,9)} at k=16.
Not a prize claim: at-most-one-odd for all k remains open.

Run: python3 research/cycle_du.py --certify
Dump: research/cycle_du.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_de import formula_divides_H, pi_formula
from cycle_dg import unfold
from cycle_dt import onesided_kills_I1_dangerous

OUT = Path(__file__).resolve().with_suffix(".json")
DE_JSON = Path(__file__).resolve().parent / "cycle_de.json"
DO_JSON = Path(__file__).resolve().parent / "cycle_do.json"
DT_JSON = Path(__file__).resolve().parent / "cycle_dt.json"


def pi_from_odds(n_odd: list[int]) -> int:
    """pi after scanning annuli with the given odd counts; start pi_1=1."""
    pi = 1
    for n in n_odd:
        if n < 0:
            raise ValueError("n_odd")
        pi *= 1 << n
    return pi


def seed_from_at_most_one(kmax: int = 64) -> bool:
    """At most k-1 doublings from pi_1=1 gives pi_k | 2^{k-1}."""
    if prize_cycle(1)[0] != 1:
        return False
    for k in range(1, kmax + 1):
        h = 1 << (k - 1)
        for e in range(k):
            if h % (1 << e):
                return False
    return True


def two_odds_kills_seed_at_k2() -> bool:
    """Two odds in (2,4] would give pi_2=4, which does not divide H=2."""
    return (1 << 1) % pi_from_odds([2]) != 0


def period_mechanism() -> bool:
    """reconstruct preserves length; even unfold closes; odd unfold 2-copies."""
    for n in range(2, 9):
        for mask in range(1 << n):
            a = [(mask >> i) & 1 for i in range(n)]
            b = a[:]
            b[0] ^= 1
            if not any(b):
                b[1] = 1
            u = reconstruct(a, b)
            if u is None or len(u) != n:
                return False
            un = unfold(a)
            if len(un) != n or un[0] != 0:
                return False
            sm = xorcat(a)
            wrap = a[-1] ^ un[-1]
            if sm == 0:
                if wrap != un[0]:
                    return False
            else:
                a2 = a + a
                u2 = un + [x ^ 1 for x in un]
                if len(u2) != 2 * n:
                    return False
                for t in range(2 * n):
                    nxt = a2[t] ^ u2[t]
                    if u2[(t + 1) % (2 * n)] != nxt:
                        return False
    return True


def onesided_reduces_to_i0_kernel() -> bool:
    """Under a=b=1 => g=0, covering fail a=b=g=I iff all four bits are 0."""
    for a, b, g, i in product((0, 1), repeat=4):
        if a == b == 1 and g != 0:
            continue
        fail = a == b == g == i
        kernel = a == b == g == i == 0
        if fail != kernel:
            return False
    return True


def five_equal_iff_i0_allzero() -> bool:
    """c_U=c_2U=c_6U=c_10U=c_18U iff I=phi6=phi10=phi18=0."""
    for c1, c2, c6, c10, c18 in product((0, 1), repeat=5):
        i = c2 ^ c1
        p6 = c6 ^ c1
        p10 = c10 ^ c1
        p18 = c18 ^ c1
        equal = c1 == c2 == c6 == c10 == c18
        kernel = i == p6 == p10 == p18 == 0
        if equal != kernel:
            return False
    return True


def de_do_dt_prefix() -> dict:
    de = json.loads(DE_JSON.read_text())
    do = json.loads(DO_JSON.read_text())
    dt = json.loads(DT_JSON.read_text())
    pis = de["pis"] + [do["pi_19"]]
    odd = {int(k): v for k, v in de["odd_high_p"].items()}
    ok = (
        de["checks"]["all_ok"]
        and do["checks"]["all_ok"]
        and dt["checks"]["all_ok"]
        and pis == [pi_formula(k) for k in range(1, 20)]
        and do["high"]["17"]["n_odd"] == 0
        and do["high"]["18"]["n_odd"] == 0
        and do["high"]["19"]["n_odd"] == 0
        and dt["i0_dangerous_k"] == []
        and dt["i1_dangerous_k"] == []
        and dt["match11_k"] == [5, 6, 7, 8, 11, 18]
        and formula_divides_H()
    )
    # m=1,2,4,8,16 odd; 17..19 empty (DO); other non-powers 0 (DE)
    expected = [1 if m in odd else 0 for m in range(1, 20)]
    return {
        "ok": ok,
        "pis": pis,
        "n_odd_1_to_19": expected,
        "hypothesis_through_19": max(expected) <= 1 and expected.count(1) == 5,
        "dt_i0_empty": dt["i0_dangerous_k"] == [],
        "dt_onesided": dt["lemmas"]["phi6_phi10_1_implies_phi18_0_k_2_to_18"],
    }


def self_checks(
    c20,
    mech: bool,
    seed_ok: bool,
    two: bool,
    taut1: bool,
    taut2: bool,
    taut3: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mech and seed_ok and two and taut1 and taut2 and taut3
    assert pref["ok"] and pref["hypothesis_through_19"]
    assert pref["pis"][0] == 1 and pref["pis"][-1] == 32
    assert pref["n_odd_1_to_19"][0] == 1  # k=1 packed bit 3
    assert sum(pref["n_odd_1_to_19"]) == 5
    # constructed pi from prize n_odd matches DE/DO pis
    for k in range(1, 20):
        got = pi_from_odds(pref["n_odd_1_to_19"][: k - 1])
        assert got == pref["pis"][k - 1]
        h = 1 << (k - 1)
        assert h % got == 0
    assert pref["dt_i0_empty"] and pref["dt_onesided"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mech = period_mechanism()
    seed_ok = seed_from_at_most_one()
    two = two_odds_kills_seed_at_k2()
    taut1 = onesided_kills_I1_dangerous()
    taut2 = onesided_reduces_to_i0_kernel()
    taut3 = five_equal_iff_i0_allzero()
    pref = de_do_dt_prefix()
    checks = self_checks(c20, mech, seed_ok, two, taut1, taut2, taut3, pref)
    dump = {
        "cycle": "DU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n_odd_1_to_19": pref["n_odd_1_to_19"],
        "pis_1_to_19": pref["pis"],
        "lemmas": {
            "pi1_is_1": True,
            "odd_doubles_even_preserves": True,
            "at_most_one_odd_implies_seed": True,
            "two_odds_can_kill_seed": True,
            "seed_requires_exact_pi_formula": False,
            "onesided_11_reduces_fail_to_i0_kernel": True,
            "five_equal_iff_i0_allzero": True,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "phi6_phi10_1_implies_phi18_0_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "pi1_is_1": "LEMMA",
            "odd_doubles_even_preserves": "LEMMA",
            "at_most_one_odd_implies_seed": "LEMMA",
            "two_odds_can_kill_seed": "LEMMA",
            "seed_requires_exact_pi_formula": "KILLED",
            "onesided_11_reduces_fail_to_i0_kernel": "LEMMA",
            "five_equal_iff_i0_allzero": "LEMMA",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "phi6_phi10_1_implies_phi18_0_all_k": "PREFIX",
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
    print("n_odd_1_to_19", pref["n_odd_1_to_19"])
    print("pis_1_to_19", pref["pis"])


if __name__ == "__main__":
    main()
