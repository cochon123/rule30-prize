#!/usr/bin/env python3
"""Cycle DM: every n0=8 scar waits at least 6344 extras; k=8 leftover empty.

All 256 length-8 T0 have a first ident-0 extra in
{6344,18827,26357,29168,34855,40805,44842,49733,52809} or none in 53000
(112 words). The minimum among nonconstant T0 is 6344 (even). The two
odd families are 26357 and 44842 (16 words each). Prize T0=00000110 is
the even 52809 family. Cycle DJ leftover at k=8 is 112<6344, so that
leftover is empty of ident-0 for every length-8 T0, not only the prize.
Do not claim a closed form for those extras, and do not claim the k=16
leftover 43205 is clean for every n0=16. Not a prize claim.

Run: python3 research/cycle_dm.py --certify
Dump: research/cycle_dm.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_di import FAM372, PRIZE4, first_odd, mask_bits
from cycle_dj import leftover

OUT = Path(__file__).resolve().with_suffix(".json")
PRIZE8 = "00000110"
MAX_EXTRA = 53000
N8_HITS = {
    6344: (0, 16),
    18827: (0, 16),
    26357: (1, 16),
    29168: (0, 16),
    34855: (0, 16),
    40805: (0, 16),
    44842: (1, 16),
    49733: (0, 16),
    52809: (0, 16),
}
N8_NONE = 112
ODD_EXTRAS = (26357, 44842)
MIN_NONCONST = 6344
PRIZE_EXTRA = 52809


def pack_bits(xs: list[int]) -> int:
    w = 0
    for i, b in enumerate(xs):
        w |= (b & 1) << i
    return w


def reconstruct_int(a: int, b: int, n: int) -> int | None:
    """Packed unique continuation; bit 0 is t=0. Matches cycle_ca.reconstruct."""
    if b == 0:
        return None
    s0 = (b & -b).bit_length() - 1
    u = 0
    t = (s0 + 1) % n
    u |= (((a >> s0) & 1) ^ 1) << t
    for _ in range(n - 1):
        nxt = (t + 1) % n
        u |= (((a >> t) & 1) ^ (((b >> t) & 1) | ((u >> t) & 1))) << nxt
        t = nxt
    return u


def reconstruct_int_matches() -> bool:
    """Packed reconstruct agrees with the list form on n0=4 and n0=8."""
    for n0 in (4, 8):
        L = 2 * n0
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            t = t0 + [x ^ 1 for x in t0]
            ones = [1] * L
            u_list = reconstruct(t, ones)
            u_int = reconstruct_int(pack_bits(t), (1 << L) - 1, L)
            if u_list is None or u_int != pack_bits(u_list):
                return False
            u2_list = reconstruct(ones, u_list)
            u2_int = reconstruct_int((1 << L) - 1, u_int, L)
            if u2_list is None or u2_int != pack_bits(u2_list):
                return False
    return True


def first_ident0_int(t0: list[int], max_extra: int) -> tuple[int | None, int | None]:
    """First ident-0 extra after (0, T0||not T0, 1)."""
    n0 = len(t0)
    L = 2 * n0
    t = pack_bits(t0 + [x ^ 1 for x in t0])
    a, b = t, (1 << L) - 1
    for cur in range(3, 3 + max_extra):
        if b == 0:
            return cur, a.bit_count() & 1
        u = reconstruct_int(a, b, L)
        if u is None:
            return None, None
        a, b = b, u
    return None, None


def n0_4_sanity() -> bool:
    """Length-4 first ident-0 extras remain 89 (odd) and 372 (odd)."""
    counts: Counter[tuple[int | None, int | None]] = Counter()
    for mask in range(16):
        t0 = mask_bits(mask, 4)
        cur, sm = first_ident0_int(t0, 400)
        counts[(cur, sm)] += 1
        odd_cur, _ = first_odd(t0, 400)
        if cur != odd_cur:
            return False
    prize = [int(c) for c in PRIZE4]
    cur, sm = first_ident0_int(prize, 400)
    if cur != 372 or sm != 1:
        return False
    if "".join(map(str, prize)) not in FAM372:
        return False
    return counts[(89, 1)] == 8 and counts[(372, 1)] == 8


def n0_8_census() -> dict:
    """All 256 length-8 T0, first ident-0 extra up to MAX_EXTRA."""
    hits: Counter[tuple[int | None, int | None]] = Counter()
    prize_hit: tuple[int | None, int | None] | None = None
    min_nonconst = None
    n_const_49733 = 0
    for mask in range(256):
        t0 = mask_bits(mask, 8)
        key = "".join(map(str, t0))
        cur, sm = first_ident0_int(t0, MAX_EXTRA)
        hits[(cur, sm)] += 1
        const = all(x == t0[0] for x in t0)
        if key == PRIZE8:
            prize_hit = (cur, sm)
        if not const and cur is not None:
            if min_nonconst is None or cur < min_nonconst:
                min_nonconst = cur
        if const and cur == 49733 and sm == 0:
            n_const_49733 += 1
    got = {cur: (sm, n) for (cur, sm), n in hits.items() if cur is not None}
    n_none = hits[(None, None)]
    odd = sorted(cur for cur, (sm, n) in got.items() if sm == 1)
    return {
        "ok": (
            got == N8_HITS
            and n_none == N8_NONE
            and min_nonconst == MIN_NONCONST
            and tuple(odd) == ODD_EXTRAS
            and prize_hit == (PRIZE_EXTRA, 0)
            and n_const_49733 == 2
            and leftover(8) == 112
            and leftover(8) < MIN_NONCONST
        ),
        "hits": {str(cur): {"odd": sm, "n": n} for cur, (sm, n) in sorted(got.items())},
        "n_none": n_none,
        "min_nonconst": min_nonconst,
        "odd_extras": odd,
        "prize": {"T0": PRIZE8, "extra": prize_hit[0] if prize_hit else None, "odd": prize_hit[1] if prize_hit else None},
        "leftover8": leftover(8),
    }


def self_checks(c20, packed_ok: bool, n4: bool, n8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert packed_ok and n4 and n8["ok"]
    assert n8["min_nonconst"] == 6344 and n8["leftover8"] == 112
    assert n8["prize"]["extra"] == 52809 and n8["prize"]["odd"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    packed_ok = reconstruct_int_matches()
    n4 = n0_4_sanity()
    n8 = n0_8_census()
    checks = self_checks(c20, packed_ok, n4, n8)
    dump = {
        "cycle": "DM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n8": {
            "hits": n8["hits"],
            "n_none": n8["n_none"],
            "min_nonconst": n8["min_nonconst"],
            "odd_extras": n8["odd_extras"],
            "prize": n8["prize"],
            "leftover8": n8["leftover8"],
        },
        "lemmas": {
            "packed_reconstruct_matches_list": True,
            "n0_4_first_ident0_89_or_372": True,
            "n0_8_min_ident0_extra_6344": True,
            "n0_8_odd_extras_26357_44842": True,
            "prize_T0_first_ident0_52809_even": True,
            "k8_leftover_empty_all_T0": True,
            "k16_leftover_all_T0": None,
            "n0_8_extras_closed_form": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "packed_reconstruct_matches_list": "LEMMA",
            "n0_4_first_ident0_89_or_372": "LEMMA",
            "n0_8_min_ident0_extra_6344": "LEMMA",
            "n0_8_odd_extras_26357_44842": "LEMMA",
            "prize_T0_first_ident0_52809_even": "LEMMA",
            "k8_leftover_empty_all_T0": "LEMMA",
            "k16_leftover_all_T0": "PREFIX",
            "n0_8_extras_closed_form": "KILLED",
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
    print("n8", dump["n8"])


if __name__ == "__main__":
    main()
