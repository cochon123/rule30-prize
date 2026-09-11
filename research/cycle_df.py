#!/usr/bin/env python3
"""Cycle DF: dyadic toggle T0s; prize scar is the k=8 u; even ident-0 is k=15.

Odd ident-0 is a white stripe (b=0) whose left neighbour has odd weight, which
doubles the period. At k=2^m<=16 those events produce u = 0, 00, 0010,
00000110, 0000110011110011. The k=8 string is the prize scar T0. The prize
even ident-0 at extra 52807 is the k=15 high-half even ident-0: white stripe
at packed bit 400+52807=53207 (detected at p=53208) with the same a.
Not a prize claim. The pi formula remains a prefix.

Run: python3 research/cycle_df.py --certify
Dump: research/cycle_df.json
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
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext
from cycle_ch import scar_lift
from cycle_dd import PRIZE_T0

OUT = Path(__file__).resolve().with_suffix(".json")
DYADIC = (1, 2, 4, 8, 16)
EXPECTED_P = {1: 3, 2: 8, 4: 29, 8: 400, 16: 87867}
EXPECTED_U = {
    1: "0",
    2: "00",
    4: "0010",
    8: "00000110",
    16: "0000110011110011",
}
EXPECTED_A = {
    1: "1",
    2: "01",
    4: "0111",
    8: "00001011",
    16: "0001010100010100",
}
K15_EVEN_P = 53208
K15_A = "1100001100010100"


def unfold(a: list[int]) -> list[int]:
    u = [0] * len(a)
    for t in range(len(a) - 1):
        u[t + 1] = a[t] ^ u[t]
    return u


def odd_ident0_doubles() -> bool:
    """b=0 and xorcat(a)=1: prefix-xor cannot close, so the block doubles."""
    for n in (2, 4, 8, 16):
        a = [0] * n
        a[-1] = 1
        if xorcat(a) != 1:
            return False
        u = unfold(a)
        if u[0] != 0 or xorcat(a) == 0:
            return False
        if unfold(a)[-1] ^ a[-1] != 1:
            return False
    return True


def high_hits(k: int) -> list[dict]:
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    hits: list[dict] = []
    p = W + 1
    while p <= 2 * W:
        a = ext(seqs[p - 2], cur_pi)
        b = ext(seqs[p - 1], cur_pi)
        if all(x == 0 for x in b):
            sm = xorcat(a)
            u = unfold(a)
            hits.append(
                {
                    "p": p,
                    "odd": sm == 1,
                    "a": "".join(map(str, a)),
                    "u": "".join(map(str, u)),
                }
            )
            if sm == 1:
                u = u + [x ^ 1 for x in u]
                cur_pi *= 2
            seqs[p] = u
        else:
            seqs[p] = reconstruct(a, b)
        p += 1
    return hits


def dyadic_toggles() -> dict:
    got_p: dict[int, int] = {}
    got_u: dict[int, str] = {}
    got_a: dict[int, str] = {}
    for k in DYADIC:
        hits = [h for h in high_hits(k) if h["odd"]]
        if len(hits) != 1:
            return {"ok": False, "k": k, "n_odd": len(hits)}
        h = hits[0]
        if h["u"] != "".join(map(str, unfold([int(c) for c in h["a"]]))):
            return {"ok": False, "k": k, "why": "unfold"}
        if xorcat([int(c) for c in h["a"]]) != 1:
            return {"ok": False, "k": k, "why": "xor"}
        got_p[k] = h["p"]
        got_u[k] = h["u"]
        got_a[k] = h["a"]
    if got_p != EXPECTED_P or got_u != EXPECTED_U or got_a != EXPECTED_A:
        return {"ok": False, "p": got_p, "u": got_u, "a": got_a}
    if got_u[8] != "".join(map(str, PRIZE_T0)):
        return {"ok": False, "why": "prize"}
    return {"ok": True, "p": got_p, "u": got_u, "a": got_a}


def k15_is_prize_even() -> dict:
    hits = [h for h in high_hits(15) if not h["odd"]]
    if len(hits) != 2 or hits[0]["p"] != K15_EVEN_P or hits[0]["a"] != K15_A:
        return {"ok": False, "hits": hits}
    s = scar_lift(PRIZE_T0, 52806)
    fail = scar_lift(PRIZE_T0, 52807)
    if s is None or fail is not None:
        return {"ok": False, "why": "lift"}
    mx = max(s)
    a, b = s[mx - 1], s[mx]
    if not all(x == 0 for x in b) or xorcat(a) != 0:
        return {"ok": False, "why": "parity"}
    if "".join(map(str, a)) != K15_A:
        return {"ok": False, "why": "a", "a": "".join(map(str, a))}
    white = 400 + 52807
    if white != K15_EVEN_P - 1:
        return {"ok": False, "white": white}
    return {"ok": True, "p": K15_EVEN_P, "white": white, "a": K15_A}


def self_checks(c20, loc: bool, tog: dict, k15: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert loc
    assert tog["ok"] and tog["u"][8] == "00000110"
    assert k15["ok"] and k15["white"] == 53207
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = odd_ident0_doubles()
    tog = dyadic_toggles()
    k15 = k15_is_prize_even()
    checks = self_checks(c20, loc, tog, k15)
    dump = {
        "cycle": "DF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "toggles": {"p": tog["p"], "u": tog["u"], "a": tog["a"]},
        "k15_even": {"p": k15["p"], "white": k15["white"], "a": k15["a"]},
        "lemmas": {
            "odd_ident0_iff_white_stripe_odd_left": True,
            "dyadic_u_strings": True,
            "k8_u_is_prize_T0": True,
            "prize_even_ident0_is_k15_white_53207": True,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_ident0_iff_white_stripe_odd_left": "LEMMA",
            "dyadic_u_strings": "LEMMA",
            "k8_u_is_prize_T0": "LEMMA",
            "prize_even_ident0_is_k15_white_53207": "LEMMA",
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
    print("toggles", dump["toggles"])
    print("k15_even", dump["k15_even"])


if __name__ == "__main__":
    main()
