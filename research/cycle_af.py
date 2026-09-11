#!/usr/bin/env python3
"""Cycle AF: two-step Green support; 1-run AND hits c_{s+2}; I_k parity kills.

Every 1-run ending fires the centre-left AND, and G(1,0..2)=1, so that AND
Green-hits c_{s+2}. The only time-s ANDs that hit c_{s+2} are the three
pairs (ell,c), (c,r), (r,e). Including the time-(s+1) centre-right AND
(which vanishes at a 1-run ending) and the older Green remainder O_s,

    c_{s+2} = 1 XOR (ell AND c) XOR (c AND r) XOR (r AND e) XOR (c' AND r') XOR O_s

and at a 1-run ending this is (r AND NOT e) XOR O_s. O_s is not identically
0, so the three local ANDs do not force 00. Annulus parities of 10/00/11
and of (r AND NOT e) at 10s are not I_k.

Not a prize claim: infinitely many 00s and non-eventual-vanishing of I_k
remain unproved.

Run: python3 research/cycle_af.py --certify
Dump: research/cycle_af.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
    """[x^d](1+x+x^2)^m over GF(2), doubling recurrence (Cycle AA)."""
    if d < 0 or d > 2 * m:
        return 0
    if m == 0:
        return int(d == 0)
    if m % 2 == 0:
        if d % 2:
            return 0
        return G(m // 2, d // 2)
    n = m // 2
    if d % 2 == 0:
        return G(n, d // 2) ^ G(n, d // 2 - 1)
    return G(n, (d - 1) // 2)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def and_hit_parity(rows: list[int], s: int, target_t: int) -> int:
    A = (rows[s] << 1) & rows[s]
    delta = target_t - s - 1
    acc = 0
    tmp, p = A, 0
    while tmp:
        if tmp & 1 and G(delta, target_t - p):
            acc ^= 1
        tmp >>= 1
        p += 1
    return acc


def older_parity(rows: list[int], t: int, target_t: int) -> int:
    acc = 0
    for s in range(t):
        acc ^= and_hit_parity(rows, s, target_t)
    return acc


def self_checks(
    c20,
    g1: list[int],
    twostep_ok: bool,
    ending_ok: bool,
    o_both: bool,
    ik_mismatches: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert g1 == [1, 1, 1, 0, 0]
    assert twostep_ok
    assert ending_ok
    assert o_both
    for name, rec in ik_mismatches.items():
        assert rec["first_fail"] is not None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)

    g1 = [G(1, d) for d in range(5)]
    # Support: time-s AND at packed p hits c_{s+2} iff s+2-p in {0,1,2}.
    support_p = [d for d in range(-2, 6) if G(1, d)]
    assert support_p == [0, 1, 2]

    gcap = 36
    rows = evolve_rows(gcap + 4)

    def bits_at(t: int) -> tuple[int, int, int, int]:
        R = rows[t]
        ell = (R >> (t - 1)) & 1 if t >= 1 else 0
        c = (R >> t) & 1
        r = (R >> (t + 1)) & 1
        e = (R >> (t + 2)) & 1
        return ell, c, r, e

    twostep_fail = 0
    ending_fail = 0
    n10 = 0
    O_ending = []
    O_all = []
    for t in range(0, gcap):
        ell, c, r, e = bits_at(t)
        cp = (rows[t + 1] >> (t + 1)) & 1
        rp = (rows[t + 1] >> (t + 2)) & 1
        local = (ell & c) ^ (c & r) ^ (r & e) ^ (cp & rp)
        older = older_parity(rows, t, t + 2)
        pred = 1 ^ local ^ older
        got = (rows[t + 2] >> (t + 2)) & 1
        O_all.append(older)
        if pred != got:
            twostep_fail += 1
        if c == 1 and cp == 0:
            n10 += 1
            # time t+1 AND vanishes; local reduces to (r AND NOT e) XOR 1? :
            # 1 XOR (ell AND c) XOR r XOR (r AND e) XOR 0 XOR older
            # = (r AND NOT e) XOR older
            pred10 = (r & (1 - e)) ^ older
            if pred10 != got:
                ending_fail += 1
            O_ending.append(older)
            # (ell,c) fires and G(1,2)=1
            if (ell & c) != 1 or G(1, 2) != 1:
                ending_fail += 1
    twostep_ok = twostep_fail == 0
    ending_ok = ending_fail == 0
    o_both = (0 in O_ending) and (1 in O_ending)

    # I_k vs annulus parities.
    N = 1 << 11
    row = 1
    cbits = bytearray(N)
    rb = bytearray(N)
    eb = bytearray(N)
    abits = bytearray(N)
    for t in range(N):
        cbits[t] = (row >> t) & 1
        rb[t] = (row >> (t + 1)) & 1
        eb[t] = (row >> (t + 2)) & 1
        if t >= 2:
            abits[t] = (row >> (t - 2)) & 1
        row = rule30_step(row)

    families = {
        "parity_10": [],
        "parity_00": [],
        "parity_11": [],
        "parity_rne_at_10": [],
        "parity_ae_at_10": [],
    }
    I_list = []
    for k in range(1, 11):
        T = 1 << (k - 1)
        I = cbits[2 * T] ^ cbits[T]
        I_list.append(I)
        p10 = p00 = p11 = prne = pae = 0
        for t in range(T, min(2 * T, N - 2)):
            if cbits[t] == 1 and cbits[t + 1] == 0:
                p10 ^= 1
                r, e = rb[t], eb[t]
                prne ^= r & (1 - e)
                pae ^= int(abits[t] == (r | e))
            if cbits[t] == 0 and cbits[t + 1] == 0:
                p00 ^= 1
            if cbits[t] == 1 and cbits[t + 1] == 1:
                p11 ^= 1
        families["parity_10"].append(p10)
        families["parity_00"].append(p00)
        families["parity_11"].append(p11)
        families["parity_rne_at_10"].append(prne)
        families["parity_ae_at_10"].append(pae)

    ik_mismatches = {}
    for name, vals in families.items():
        first = None
        disagrees = []
        for k, v in enumerate(vals, start=1):
            if v != I_list[k - 1]:
                disagrees.append(k)
                if first is None:
                    first = k
        ik_mismatches[name] = {"first_fail": first, "fail_k": disagrees, "values": vals}

    checks = self_checks(c20, g1, twostep_ok, ending_ok, o_both, ik_mismatches)

    dump = {
        "cycle": "AF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "G1": g1,
        "twostep_fail": twostep_fail,
        "ending_fail": ending_fail,
        "n10_gcap": n10,
        "O_ending_values": sorted(set(O_ending)),
        "O_all_ones": int(sum(O_all)),
        "O_all_n": len(O_all),
        "I_k": I_list,
        "ik_mismatches": ik_mismatches,
        "lemmas": {
            "G1_support": g1[:3] == [1, 1, 1],
            "twostep_identity": twostep_ok,
            "run_end_AND_hits_c_s2": ending_ok,
            "O_not_identically_zero": o_both,
            "infinitely_many_00": None,
            "I_k_not_eventually_zero": None,
            "prize": False,
        },
        "verdict": {
            "G1_support": "LEMMA",
            "twostep_identity": "LEMMA",
            "run_end_AND_hits_c_s2": "LEMMA",
            "O_not_identically_zero": "LEMMA",
            "local_three_ANDs_force_00": "KILLED",
            "I_k_annulus_10_00_11": "KILLED",
            "I_k_rne_or_ae_at_10": "KILLED",
            "infinitely_many_00": "OPEN",
            "I_k_not_eventually_zero": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("twostep_fail", twostep_fail, "ending_fail", ending_fail, "O_ending", sorted(set(O_ending)))
    print("I_k", I_list)
    print("first fails", {n: ik_mismatches[n]["first_fail"] for n in ik_mismatches})
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
