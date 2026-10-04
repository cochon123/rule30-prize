#!/usr/bin/env python3
"""Cycle OK: the S-bit vanishes on every even row.

If n is even and G(n,j)=1, then j is even, so j-1 and j+1 are odd
and G(n,j-1)=G(n,j+1)=0. Palindrome-right T-bits are already silent
on even n (Cycle OI). The S-bit G(n,j+1) is silent for the same
reason, at every live cell, clipped or not. Covering S and the
even-row part of E therefore receive no S-bit and no T-bit from
even n: on those rows the error bit equals the packed rest bit.

This does not prove E_k=0. Odd rows still have to cancel that
even-row rest. Do not catalogue further S/T subregions. Do not
claim E_k=0 for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ok.py --certify
Dump: research/cycle_ok.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover

OUT = Path(__file__).resolve().with_suffix(".json")
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OI_JSON = Path(__file__).resolve().parent / "cycle_oi.json"

N_EVEN = 2048


def even_neighbors(n: int, j: int) -> tuple[int, int]:
    """Even n and G(n,j)=1 imply both neighbor Green bits are 0."""
    if n % 2:
        raise ValueError("even n required")
    if G(n, j) == 0:
        return 0, 0
    if j % 2:
        raise AssertionError("even n cannot have G=1 at odd j")
    return G(n, j - 1), G(n, j + 1)


def walk_even(n_hi: int) -> dict:
    """Every live cell on even n<n_hi has S-bit and T-bit 0."""
    n_live = n_s_filter = n_rows = 0
    witness = None
    for n in range(0, n_hi, 2):
        row_live = 0
        for j in range(n + 1, 2 * n + 1):
            if G(n, j) == 0:
                continue
            left, right = even_neighbors(n, j)
            if left != 0 or right != 0 or j % 2:
                return {"ok": False, "n": n, "j": j, "left": left, "right": right}
            row_live += 1
            n_live += 1
            d = j - n
            if d % 3 == 1:
                n_s_filter += 1
                if witness is None:
                    witness = {"n": n, "j": j, "d": d, "G_j": 1, "G_jm1": left, "G_jp1": right}
        if row_live:
            n_rows += 1
    ok = (
        n_live > 0
        and n_s_filter > 0
        and n_rows > 0
        and witness is not None
        and witness["G_jp1"] == 0
        and witness["G_jm1"] == 0
    )
    return {
        "ok": ok,
        "n_hi": n_hi,
        "n_even": n_hi // 2,
        "n_rows": n_rows,
        "n_live": n_live,
        "n_s_filter": n_s_filter,
        "witness": witness,
    }


def killed_s_fires(walk: dict) -> dict:
    """An even row can meet the S filter and still have S-bit 0."""
    w = walk["witness"]
    ok = w is not None and w["G_jp1"] == 0 and w["d"] % 3 == 1 and G(w["n"], w["j"]) == 1
    return {"ok": ok, "witness": w}


def prefixes() -> dict:
    oj = json.loads(OJ_JSON.read_text())
    oi = json.loads(OI_JSON.read_text())
    ok = (
        oj["checks"]["all_ok"]
        and oi["checks"]["all_ok"]
        and oj["verdict"]["odd_t_xor_all_n"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and oj["verdict"]["prize"] == "unsolved"
        and oi["verdict"]["even_t_vanish"] == "LEMMA"
    )
    return {"ok": ok}


def self_checks(c20, walk, dead, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert walk["ok"] and dead["ok"] and sc["ok"] and pref["ok"]
    assert walk["n_live"] > 0 and walk["n_s_filter"] > 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    walk = walk_even(N_EVEN)
    dead = killed_s_fires(walk)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, walk, dead, sc, pref)
    dump = {
        "cycle": "OK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_neighbors": {k: walk[k] for k in walk if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_s_fire": {k: dead[k] for k in dead if k != "ok"},
        "lemmas": {
            "even_s_bit": True,
            "even_t_bit": True,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_s_bit": "LEMMA",
            "even_t_bit": "LEMMA",
            "s_fire_on_even": "KILLED",
            "E_all_k": "OPEN",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
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
    print("even", dump["even_neighbors"])


if __name__ == "__main__":
    main()
