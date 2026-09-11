#!/usr/bin/env python3
"""Cycle DK: every nonconstant length-16 scar has no ident-0 in 130 extras.

Cycle CG gave 80 (resp. 130) ident-0-free extras for every nonconstant
T0 of length 4 (resp. 8). The same 130-extra window is clean for every
nonconstant T0 of length 16 (65534 words). Prize u_16=0000110011110011
is an instance. Do not claim the k=16 leftover 43205 is clean for all
such T0. Not a prize claim.

Run: python3 research/cycle_dk.py --certify
Dump: research/cycle_dk.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
N0 = 16
N_EXTRA = 130
PRIZE_U16 = "0000110011110011"
EXPECT_OK = (1 << N0) - 2


def window_clean(T0: list[int], n_extra: int) -> bool:
    """No ident-0 in n_extra unique-continuation steps after (0, T, 1)."""
    T = T0 + [x ^ 1 for x in T0]
    a = T
    b = [1] * len(T)
    for _ in range(n_extra):
        if all(x == 0 for x in b):
            return False
        u = reconstruct(a, b)
        if u is None:
            return False
        a, b = b, u
    return True


def exhaust16() -> dict:
    n_ok = 0
    n_hit = 0
    prize_ok = False
    for mask in range(1 << N0):
        T0 = [(mask >> i) & 1 for i in range(N0)]
        s = sum(T0)
        if s in (0, N0):
            continue
        ok = window_clean(T0, N_EXTRA)
        if ok:
            n_ok += 1
            if "".join(map(str, T0)) == PRIZE_U16:
                prize_ok = True
        else:
            n_hit += 1
            return {"ok": False, "mask": mask, "n_ok": n_ok, "n_hit": n_hit}
    return {
        "ok": n_ok == EXPECT_OK and n_hit == 0 and prize_ok,
        "n_ok": n_ok,
        "n_hit": n_hit,
        "prize_ok": prize_ok,
        "n_extra": N_EXTRA,
    }


def self_checks(c20, ex: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ex["ok"] and ex["n_ok"] == EXPECT_OK and ex["prize_ok"]
    assert window_clean([int(c) for c in PRIZE_U16], N_EXTRA)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ex = exhaust16()
    checks = self_checks(c20, ex)
    dump = {
        "cycle": "DK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n0": N0,
        "n_extra": N_EXTRA,
        "n_ok": ex["n_ok"],
        "n_hit": ex["n_hit"],
        "prize_u16": PRIZE_U16,
        "lemmas": {
            "n0_16_no_ident0_in_130": True,
            "prize_u16_in_that_window": True,
            "k16_leftover_43205_all_T0": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n0_16_no_ident0_in_130": "LEMMA",
            "prize_u16_in_that_window": "LEMMA",
            "k16_leftover_43205_all_T0": "PREFIX",
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
    print("n_ok", dump["n_ok"], "n_hit", dump["n_hit"])


if __name__ == "__main__":
    main()
