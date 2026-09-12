#!/usr/bin/env python3
"""Cycle KV: family clip G=1 is an isolated-pair column; green4 by d mod 3.

Clipped G=1 on covering family clippers are never isolated ones and
never run-3. Each is a run-2 column: green4 is 1011 (left) iff
(2n-j)%3==1, and 0110 (right) iff (2n-j)%3==0. Not all the same
green4; not 0111; not 1010; not d%3==0 giving 1011. This is covering
geometry, not packed AND XOR J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_kv.py --certify
Dump: research/cycle_kv.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hj import green4
from cycle_ig import g1_green4
from cycle_in import g_run_kind
from cycle_ir import isolated_one
from cycle_kh import g4_xor_cover
from cycle_kr import want_clippers
from cycle_kt import clip_js

OUT = Path(__file__).resolve().with_suffix(".json")
KU_JSON = Path(__file__).resolve().parent / "cycle_ku.json"

K_MAX = 10
G4_LEFT = (1, 0, 1, 1)
G4_RIGHT = (0, 1, 1, 0)


def clip_g4_shape(n: int, j: int):
    """Predicted green4 of a clipped family G=1 at j; None if d%3==2."""
    d = 2 * n - j
    if d % 3 == 0:
        return G4_RIGHT
    if d % 3 == 1:
        return G4_LEFT
    return None


def clip_pair_side(n: int, j: int):
    """left/right isolated-pair side of G=1, else None."""
    if isolated_one(n, j):
        return None
    if g_run_kind(n, j) == "iso":
        return "left"
    if g_run_kind(n, j - 1) == "iso":
        return "right"
    return None


def clip_shape_table() -> dict:
    """k<=10: every clipped family G=1 matches clip_g4_shape and iso-pair."""
    n_ok = n_left = n_right = 0
    rows = {}
    for k in range(0, K_MAX + 1):
        krow = {}
        for q in (6, 10):
            n_l = n_r = 0
            for n in want_clippers(k, q):
                for j in clip_js(k, q, n):
                    want = clip_g4_shape(n, j)
                    got = green4(n, j)
                    side = clip_pair_side(n, j)
                    if (
                        want is None
                        or got != want
                        or got != g1_green4(n, j)
                        or isolated_one(n, j)
                        or side is None
                    ):
                        return {
                            "ok": False,
                            "miss": True,
                            "k": k,
                            "q": q,
                            "n": n,
                            "j": j,
                            "got": list(got),
                            "want": None if want is None else list(want),
                            "side": side,
                        }
                    if side == "left":
                        if want != G4_LEFT:
                            return {"ok": False, "left": True, "n": n, "j": j}
                        n_l += 1
                        n_left += 1
                    else:
                        if want != G4_RIGHT:
                            return {"ok": False, "right": True, "n": n, "j": j}
                        n_r += 1
                        n_right += 1
                    n_ok += 1
            krow[f"q{q}"] = {"n_left": n_l, "n_right": n_r}
        rows[str(k)] = krow
    ok = (
        n_ok == 6791
        and n_left == 3390
        and n_right == 3401
        and rows["0"]["q6"] == {"n_left": 0, "n_right": 0}
        and rows["0"]["q10"] == {"n_left": 0, "n_right": 1}
        and rows["2"]["q6"] == {"n_left": 1, "n_right": 1}
        and clip_g4_shape(7, 13) == G4_LEFT
        and clip_g4_shape(7, 14) == G4_RIGHT
        and clip_pair_side(3, 6) == "right"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_left": n_left,
        "n_right": n_right,
        "rows": rows,
    }


def killed_iso1() -> dict:
    """Clipped family G=1 are isolated ones: k=2 q=6 n=7 j=13,14 are run-2."""
    n, js = 7, (13, 14)
    ok = all(
        not isolated_one(n, j) and clip_pair_side(n, j) is not None for j in js
    ) and clip_js(2, 6, n) == js
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "n": n,
        "js": list(js),
        "iso1": [isolated_one(n, j) for j in js],
        "side": [clip_pair_side(n, j) for j in js],
    }


def killed_all_same() -> dict:
    """All clipped family green4 are equal: k=2 q=6 is 1011 and 0110."""
    n = 7
    got = [green4(n, j) for j in clip_js(2, 6, n)]
    ok = got == [G4_LEFT, G4_RIGHT] and got[0] != got[1]
    return {"ok": ok, "k": 2, "q": 6, "n": n, "g4": [list(g) for g in got]}


def killed_r3() -> dict:
    """Clipped family green4 is run-3 middle 1010: k=2 q=6 has no 1010."""
    n = 7
    got = [green4(n, j) for j in clip_js(2, 6, n)]
    ok = (1, 0, 1, 0) not in got and all(g in (G4_LEFT, G4_RIGHT) for g in got)
    return {"ok": ok, "k": 2, "q": 6, "n": n, "g4": [list(g) for g in got]}


def killed_d0_left() -> dict:
    """(2n-j)%3==0 gives left 1011: k=0 q=10 n=3 j=6 is right 0110."""
    n, j = 3, 6
    d = 2 * n - j
    ok = (
        d % 3 == 0
        and clip_g4_shape(n, j) == G4_RIGHT
        and green4(n, j) == G4_RIGHT
        and clip_pair_side(n, j) == "right"
    )
    return {"ok": ok, "k": 0, "q": 10, "n": n, "j": j, "d_mod3": d % 3}


def prefixes() -> dict:
    ku = json.loads(KU_JSON.read_text())
    ok = (
        ku["checks"]["all_ok"]
        and ku["verdict"]["family_clip_g4"] == "LEMMA"
        and ku["verdict"]["family_clip_js"] == "LEMMA"
        and ku["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert clip_g4_shape(15, 23) == G4_LEFT
    assert clip_g4_shape(3, 6) == G4_RIGHT
    assert clip_pair_side(7, 13) == "left"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_shape_table()
    sc = g4_xor_cover()
    k0 = killed_iso1()
    k1 = killed_all_same()
    k2 = killed_r3()
    k3 = killed_d0_left()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_shape_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_iso1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_all_same": {k: k1[k] for k in k1 if k != "ok"},
        "killed_r3": {k: k2[k] for k in k2 if k != "ok"},
        "killed_d0_left": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clip_iso2": True,
            "family_clip_g4": True,
            "family_clip_js": True,
            "clip_iso1": False,
            "clip_g4_all_same": False,
            "clip_r3": False,
            "d0_is_left": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clip_iso2": "LEMMA",
            "family_clip_g4": "LEMMA",
            "family_clip_js": "LEMMA",
            "clip_iso1": "KILLED",
            "clip_g4_all_same": "KILLED",
            "clip_r3": "KILLED",
            "d0_is_left": "KILLED",
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
    print(
        "clip_shape_table n_ok",
        dump["clip_shape_table"]["n_ok"],
        "left",
        dump["clip_shape_table"]["n_left"],
        "right",
        dump["clip_shape_table"]["n_right"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_iso1", dump["killed_iso1"])
    print("killed_all_same", dump["killed_all_same"])
    print("killed_r3", dump["killed_r3"])
    print("killed_d0_left", dump["killed_d0_left"])


if __name__ == "__main__":
    main()
