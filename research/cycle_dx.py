#!/usr/bin/env python3
"""Cycle DX: pair invariants hold for every odd 2-copy, so ham(n3,n4)=n0.

P1: n4_t or n3_t or n3_{t+n0} = 1. P2: n4_t and n3_{t+n0} = 0. At any
n3=1 site complementary support forces n3_{t+n0}=0, so both hold. The
NOR / reconstruct recurrences send (P1,P2) at t to (P1,P2) at t+1 for
every bit s_t. O-type s is never all-1s, so reconstruct(1,s) is not
identically 0 and a seed exists. Hence P1,P2 hold at every t, for every
half-length. Cycle DW's bijection then gives ham(n3,n4)=n0 with no n0
bound. Pair invariants still fail for generic s and E-type. Do not
compute phi^{(3,5,9)} at k=16. Not a prize claim: Hamming n0 does not
fill an annulus.

Run: python3 research/cycle_dx.py --certify
Dump: research/cycle_dx.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_dv import mask_bits, odd_copy, n3n4_of
from cycle_dw import pair_invariants_fail_E, pair_invariants_fail_generic, xorv

OUT = Path(__file__).resolve().with_suffix(".json")
DW_JSON = Path(__file__).resolve().parent / "cycle_dw.json"


def p1(n3: int, n3p: int, n4: int) -> bool:
    return (n4 | n3 | n3p) == 1


def p2(n3: int, n3p: int, n4: int) -> bool:
    return (n4 & n3p) == 0


def step(s: int, n3: int, n3p: int, n4: int) -> tuple[int, int, int]:
    """n3'=NOR(s,n3); n3p'=s and not n3p; n4'=s xor (n3 or n4)."""
    n3n = 0 if (s or n3) else 1
    n3pn = s & (n3p ^ 1)
    n4n = s ^ (n3 | n4)
    return n3n, n3pn, n4n


def seed_ok() -> bool:
    """At n3=1, complementary n3p=0 makes P1 and P2 hold for both n4."""
    for n4 in (0, 1):
        if not (p1(1, 0, n4) and p2(1, 0, n4)):
            return False
    return True


def step_preserves() -> dict:
    """Every complementary (P1,P2) state steps to a complementary (P1,P2)."""
    n_hold = 0
    n_fail = 0
    n_comp_next = 0
    for n3 in (0, 1):
        for n3p in (0, 1):
            if n3 and n3p:
                continue
            for n4 in (0, 1):
                for s in (0, 1):
                    if not (p1(n3, n3p, n4) and p2(n3, n3p, n4)):
                        continue
                    n_hold += 1
                    nxt = step(s, n3, n3p, n4)
                    if nxt[0] and nxt[1]:
                        n_fail += 1
                        continue
                    n_comp_next += 1
                    if not (p1(*nxt) and p2(*nxt)):
                        n_fail += 1
    return {
        "ok": n_fail == 0 and n_hold == 8 and n_comp_next == 8,
        "n_hold": n_hold,
        "n_fail": n_fail,
    }


def n3_never_zero_O() -> bool:
    """O-type is not all-1s, and reconstruct(1,s) is 0 iff s is all-1s."""
    if twocopy_type([1, 1, 1, 1]) != "E":
        return False
    if reconstruct([1, 1, 1, 1], [1, 1, 1, 1]) != [0, 0, 0, 0]:
        return False
    for n0 in range(1, 9):
        L = 2 * n0
        ones = [1] * L
        if odd_copy([1] * n0) == ones:
            return False
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            if twocopy_type(s) != "O" or s == ones:
                return False
            n3 = reconstruct(ones, s)
            if n3 is None or not any(n3):
                return False
            for t in range(L):
                if n3[(t + 1) % L] != (1 ^ (s[t] | n3[t])):
                    return False
    return True


def p1p2_match_dw(n0_max: int = 8) -> bool:
    """P1,P2 at every t recover Cycle DW's pair invariants on small O-type."""
    for n0 in range(1, n0_max + 1):
        L = 2 * n0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(s)
            if pair is None:
                return False
            n3, n4 = pair
            d = xorv(n3, n4)
            for t in range(L):
                a, b, x = n3[t], n3[(t + n0) % L], n4[t]
                if a and b:
                    return False
                if not (p1(a, b, x) and p2(a, b, x)):
                    return False
            for t in range(n0):
                a, b = n3[t], n3[t + n0]
                x, y = d[t], d[t + n0]
                if a == 0 and b == 0 and not (x == 1 and y == 1):
                    return False
                if a == 1 and y != 0:
                    return False
                if b == 1 and x != 0:
                    return False
    return True


def dw_prefix() -> dict:
    dw = json.loads(DW_JSON.read_text())
    ok = (
        dw["checks"]["all_ok"]
        and dw["n0_max"] == 16
        and dw["lemmas"]["pair_invariants_n0_1_to_16"]
        and dw["lemmas"]["pair_invariants_imply_ham_n0"]
        and dw["lemmas"]["O_type_complementary_support"]
        and dw["prize_ham"]["16"]["ham_n3_n4"] == 16
        and dw["verdict"]["pair_invariants_all_n0"] == "PREFIX"
    )
    return {"ok": ok, "prize": dw["prize_ham"], "n0_max": dw["n0_max"]}


def self_checks(
    c20,
    seed: bool,
    pres: dict,
    nz: bool,
    match: bool,
    gen: bool,
    etype: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert seed and pres["ok"] and nz and match and gen and etype
    assert pref["ok"]
    assert pres["n_hold"] == 8 and pres["n_fail"] == 0
    assert pref["prize"]["4"]["ham_n3_n4"] == 4
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    seed = seed_ok()
    pres = step_preserves()
    nz = n3_never_zero_O()
    match = p1p2_match_dw()
    gen = pair_invariants_fail_generic()
    etype = pair_invariants_fail_E()
    pref = dw_prefix()
    checks = self_checks(c20, seed, pres, nz, match, gen, etype, pref)
    dump = {
        "cycle": "DX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "step": pres,
        "prize_ham": pref["prize"],
        "lemmas": {
            "seed_P1_P2_at_n3_one": True,
            "step_preserves_P1_P2": True,
            "O_type_n3_never_zero": True,
            "pair_invariants_all_n0": True,
            "ham_n3_n4_equals_n0_all_O_type": True,
            "pair_invariants_generic_s": False,
            "pair_invariants_E_type": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "seed_P1_P2_at_n3_one": "LEMMA",
            "step_preserves_P1_P2": "LEMMA",
            "O_type_n3_never_zero": "LEMMA",
            "pair_invariants_all_n0": "LEMMA",
            "ham_n3_n4_equals_n0_all_O_type": "LEMMA",
            "pair_invariants_generic_s": "KILLED",
            "pair_invariants_E_type": "KILLED",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("step", dump["step"])
    print("prize_ham", dump["prize_ham"])


if __name__ == "__main__":
    main()
