#!/usr/bin/env python3
"""Cycle DL: even ident-0 has two lifts; prize k=16 high half has only the odd.

When xorcat(a)=0 and b=0, the recurrence u_{t+1}=a_t xor u_t has exactly two
period-pi solutions, complements of each other. The prize k=16 high half
(W,2W] contains exactly one ident-0: the odd toggle at packed bit 87867.
There is no ident-0 at Rowland's third fork 72577, and the leftover 43205
bits after 87867 contain neither even nor odd ident-0. Do not claim that
leftover is clean for every length-16 T0. Not a prize claim.

Run: python3 research/cycle_dl.py --certify
Dump: research/cycle_dl.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext
from cycle_df import unfold

OUT = Path(__file__).resolve().with_suffix(".json")
ODD_P16 = 87867
ROWLAND_FORK = 72577
LEFTOVER16 = (1 << 17) - ODD_P16  # 43205


def even_two_lifts(trials: int = 40) -> bool:
    """xorcat(a)=0 implies unfold(u0=0) and its complement both close."""
    rng = random.Random(47)
    for n in (4, 8, 16, 32):
        for _ in range(trials):
            a = [rng.randint(0, 1) for _ in range(n)]
            if xorcat(a) != 0:
                a[0] ^= 1
            u0 = unfold(a)
            u1 = [x ^ 1 for x in u0]
            if (u0[-1] ^ a[-1]) != u0[0]:
                return False
            if (u1[-1] ^ a[-1]) != u1[0]:
                return False
            if u1 == u0 or xorcat(a) != 0:
                return False
    return True


def k16_high_ident0s() -> dict:
    """Exactly one ident-0 in (W,2W] at k=16: odd at 87867, leftover empty."""
    k = 16
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
            hits.append({"p": p, "odd": sm == 1, "pi": cur_pi})
            if sm == 1:
                u = u + [x ^ 1 for x in u]
                cur_pi *= 2
            seqs[p] = u
        else:
            seqs[p] = reconstruct(a, b)
        p += 1
    if pi != 16 or cur_pi != 32:
        return {"ok": False, "pi": pi, "cur_pi": cur_pi}
    if len(hits) != 1 or hits[0]["p"] != ODD_P16 or not hits[0]["odd"]:
        return {"ok": False, "hits": hits}
    if any(h["p"] == ROWLAND_FORK or h["p"] == ROWLAND_FORK + 1 for h in hits):
        return {"ok": False, "why": "72577"}
    leftover_hits = [h for h in hits if h["p"] > ODD_P16]
    if leftover_hits or LEFTOVER16 != 43205:
        return {"ok": False, "leftover": leftover_hits}
    return {
        "ok": True,
        "n_hits": 1,
        "odd_p": ODD_P16,
        "n_even": 0,
        "leftover": LEFTOVER16,
        "no_72577": True,
    }


def self_checks(c20, lifts: bool, high: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert lifts and high["ok"] and high["n_even"] == 0 and high["no_72577"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    lifts = even_two_lifts()
    high = k16_high_ident0s()
    checks = self_checks(c20, lifts, high)
    dump = {
        "cycle": "DL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "k16": {
            "odd_p": high["odd_p"],
            "n_even": high["n_even"],
            "leftover": high["leftover"],
            "no_72577": high["no_72577"],
        },
        "lemmas": {
            "even_ident0_two_complement_lifts": True,
            "k16_high_only_odd_87867": True,
            "k16_leftover_no_ident0_prize": True,
            "prize_hits_rowland_72577": False,
            "k16_leftover_all_T0": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_ident0_two_complement_lifts": "LEMMA",
            "k16_high_only_odd_87867": "LEMMA",
            "k16_leftover_no_ident0_prize": "LEMMA",
            "prize_hits_rowland_72577": "KILLED",
            "k16_leftover_all_T0": "PREFIX",
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
    print("k16", dump["k16"])


if __name__ == "__main__":
    main()
