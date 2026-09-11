#!/usr/bin/env python3
"""Cycle BO: Fermat covering fails at k+1 iff the even spines match I.

Doubling (Cycle AL/AH) gives phi^{(q)}_{k+1} = phi^{(2q)}_k XOR I_{k+1}
for q=3,5,9, with I_{k+1}=phi^{(2)}_k. Hence covering at k+1 fails iff

    phi^{(6)}_k = phi^{(10)}_k = phi^{(18)}_k = I_{k+1}.

Equivalently, the dangerous alignment phi^{(6)}=phi^{(10)}=I together
with Theta(6*2^k)=0. That set is empty on 2<=k<=12 (covering through
k=13 stays a prefix). phi^{(6)}_k is not identically 1 for k>=5
(zero at k=13), and the pair {phi^{(5)}, phi^{(6)}} is not a covering.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bo.py --certify
Dump: research/cycle_bo.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def phi_row(c: bytearray, q: int, kmax: int) -> list[int]:
    out = []
    for k in range(2, kmax + 1):
        U = 1 << k
        out.append(c[q * U] ^ c[U])
    return out


def doubling_ok(p2, p3, p5, p6, p9, p10, p18) -> bool:
    for i in range(len(p2) - 1):
        if p3[i + 1] != p6[i] ^ p2[i]:
            return False
        if p5[i + 1] != p10[i] ^ p2[i]:
            return False
        if p9[i + 1] != p18[i] ^ p2[i]:
            return False
    return True


def fail_criterion_ok(p2, p3, p5, p6, p9, p10, p18) -> tuple[bool, list[int]]:
    """Covering at k+1 fails iff even spines equal I_{k+1}."""
    dangerous = []
    ks = list(range(2, 2 + len(p2)))
    for i in range(len(p2) - 1):
        I = p2[i]
        aligned = p6[i] == I and p10[i] == I and p18[i] == I
        cover_next = p3[i + 1] | p5[i + 1] | p9[i + 1]
        if aligned != (cover_next == 0):
            return False, dangerous
        if aligned:
            dangerous.append(ks[i])
        theta6 = p6[i] ^ p18[i]
        aligned_alt = p6[i] == I and p10[i] == I and theta6 == 0
        if aligned_alt != aligned:
            return False, dangerous
    return True, dangerous


def self_checks(
    c20,
    dbl: bool,
    crit: bool,
    dangerous: list[int],
    p3,
    p5,
    p6,
    p9,
    kmax: int,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dbl and crit
    assert dangerous == []
    # Fermat covering through this prefix (k<=13, inside Cycle BE's k=15)
    cover = [a | b | c for a, b, c in zip(p3, p5, p9)]
    assert all(cover)
    assert 0 in p6 and 1 in p6
    # k=13 is index 11 in rows starting at k=2
    assert kmax >= 13 and p6[13 - 2] == 0
    assert (p5[13 - 2] | p6[13 - 2]) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    kmax = 13
    qmax = 18
    c = packed_center_bits(qmax * (1 << kmax) + 2)
    c20 = c[:20]
    p2 = phi_row(c, 2, kmax)
    p3 = phi_row(c, 3, kmax)
    p5 = phi_row(c, 5, kmax)
    p6 = phi_row(c, 6, kmax)
    p9 = phi_row(c, 9, kmax)
    p10 = phi_row(c, 10, kmax)
    p18 = phi_row(c, 18, kmax)
    dbl = doubling_ok(p2, p3, p5, p6, p9, p10, p18)
    crit, dangerous = fail_criterion_ok(p2, p3, p5, p6, p9, p10, p18)
    checks = self_checks(c20, dbl, crit, dangerous, p3, p5, p6, p9, kmax)
    ks = list(range(2, kmax + 1))
    dump = {
        "cycle": "BO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prefix": {
            "k": ks,
            "phi2": p2,
            "phi3": p3,
            "phi5": p5,
            "phi6": p6,
            "phi9": p9,
            "phi10": p10,
            "phi18": p18,
            "cover359": [a | b | d for a, b, d in zip(p3, p5, p9)],
        },
        "dangerous_k": dangerous,
        "lemmas": {
            "doubling_359": True,
            "cover_fails_iff_even_spines_eq_I": True,
            "dangerous_set_k_2_to_12_empty": True,
            "phi6_identically_1_kge5": False,
            "phi5_or_phi6_all_k": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "doubling_359": "LEMMA",
            "cover_fails_iff_even_spines_eq_I": "LEMMA",
            "dangerous_set_k_2_to_12_empty": "PREFIX",
            "phi6_identically_1_kge5": "KILLED",
            "phi5_or_phi6_all_k": "KILLED",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("dangerous_k", dangerous)
    print("phi6", p6)


if __name__ == "__main__":
    main()
