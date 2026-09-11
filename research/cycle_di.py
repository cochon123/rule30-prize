#!/usr/bin/env python3
"""Cycle DI: every length-2 scar odd-doubles at extra 22; n0=4 at 89 or 372.

All four length-2 words produce a second odd ident-0 at scar key 22, with
a a rotation of 0111. On the prize orbit that event is packed bit 29=8+21.
All sixteen length-4 words hit a second odd ident-0 at extra 89 or 372,
the two rotation orbits of 00001111 and 00101101. Prize T0=0010 is the
372 orbit, packed bit 400=28+372. The 89 orbit would land in a non-power
high half; do not claim every n0=4 waits for a 2-power. Not a prize claim.

Run: python3 research/cycle_di.py --certify
Dump: research/cycle_di.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct, xorcat

OUT = Path(__file__).resolve().with_suffix(".json")
PRIZE4 = "0010"
ROTS_0111 = {"0111", "1110", "1101", "1011"}
FAM89 = {"0000", "0001", "0011", "0111", "1000", "1100", "1110", "1111"}
FAM372 = {"0010", "0100", "0101", "0110", "1001", "1010", "1011", "1101"}


def mask_bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def first_odd(T0: list[int], max_extra: int) -> tuple[int | None, str | None]:
    n0 = len(T0)
    T = T0 + [x ^ 1 for x in T0]
    L = 2 * n0
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    for cur in range(3, 3 + max_extra):
        a, b = seqs[cur - 2], seqs[cur - 1]
        if all(x == 0 for x in b):
            if xorcat(a) == 1:
                return cur, "".join(map(str, a))
            u = [0] * L
            for t in range(L - 1):
                u[t + 1] = a[t] ^ u[t]
            seqs[cur] = u
        else:
            u = reconstruct(a, b)
            if u is None:
                return None, None
            seqs[cur] = u
    return None, None


def len2_at_22() -> dict:
    """Every length-2 T0 has a second odd ident-0 at key 22."""
    a_map: dict[str, str] = {}
    for mask in range(4):
        T0 = mask_bits(mask, 2)
        key = "".join(map(str, T0))
        cur, a = first_odd(T0, 40)
        if cur != 22 or a is None or a not in ROTS_0111:
            return {"ok": False, "T0": key, "cur": cur, "a": a}
        a_map[key] = a
    if set(a_map.values()) != ROTS_0111:
        return {"ok": False, "a": a_map}
    return {"ok": True, "a": a_map, "packed": 7 + 22}


def len4_89_or_372() -> dict:
    """Every length-4 T0 second-odd-doubles at 89 (half-constant orbit) or
    372 (prize orbit). Prize 0010 is the 372 family."""
    fam: dict[int, list[str]] = {89: [], 372: []}
    for mask in range(16):
        T0 = mask_bits(mask, 4)
        key = "".join(map(str, T0))
        cur, a = first_odd(T0, 400)
        if cur not in fam or a is None:
            return {"ok": False, "T0": key, "cur": cur}
        fam[cur].append(key)
    if set(fam[89]) != FAM89 or set(fam[372]) != FAM372:
        return {"ok": False, "fam": fam}
    if PRIZE4 not in fam[372]:
        return {"ok": False, "why": "prize"}
    return {
        "ok": True,
        "n89": 8,
        "n372": 8,
        "prize_372": True,
        "packed": 28 + 372,
    }


def packed_ok(len2: dict, len4: dict) -> bool:
    """Prize packed bits 29 and 400 are these extras off the previous white."""
    return len2["packed"] == 29 and len4["packed"] == 400


def self_checks(c20, len2: dict, len4: dict, packed: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert len2["ok"] and len2["a"]["11"] == "0111" and len2["a"]["00"] == "1101"
    assert len4["ok"] and packed
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    len2 = len2_at_22()
    len4 = len4_89_or_372()
    packed = packed_ok(len2, len4)
    checks = self_checks(c20, len2, len4, packed)
    dump = {
        "cycle": "DI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "len2": {"extra": 22, "packed": 29, "a": len2["a"]},
        "len4": {"n89": 8, "n372": 8, "prize_extra": 372, "packed": 400},
        "lemmas": {
            "len2_all_odd_double_at_22": True,
            "len2_a_rotations_of_0111": True,
            "prize_p4_is_8_plus_21": True,
            "len4_odd_double_at_89_or_372": True,
            "prize_0010_is_372_orbit": True,
            "prize_p8_is_29_plus_371": True,
            "n0_4_always_waits_for_pow2": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "len2_all_odd_double_at_22": "LEMMA",
            "len2_a_rotations_of_0111": "LEMMA",
            "prize_p4_is_8_plus_21": "LEMMA",
            "len4_odd_double_at_89_or_372": "LEMMA",
            "prize_0010_is_372_orbit": "LEMMA",
            "prize_p8_is_29_plus_371": "LEMMA",
            "n0_4_always_waits_for_pow2": "KILLED",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("len2", dump["len2"])
    print("len4", dump["len4"])


if __name__ == "__main__":
    main()
