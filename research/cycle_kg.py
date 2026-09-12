#!/usr/bin/env python3
"""Cycle KG: packed vs green4 on G=1 fills all 64 cells.

Covering G=1 packed 4-tuples take all 16 values on each of the four
g1_green4 shapes. Packed is not always green4; not a function of
green4; cob packed is not only on 0111. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kg.py --certify
Dump: research/cycle_kg.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from cycle_ig import g1_green4
from cycle_ir import isolated_one
from cycle_kb import G1_SHAPES, die_g4_table
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KF_JSON = Path(__file__).resolve().parent / "cycle_kf.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

PACK_KEYS = tuple(f"{i:04b}" for i in range(16))
WANT_G4 = {"0110": 6197, "0111": 7785, "1010": 2380, "1011": 6297}
WANT_CELL = {
    "0111": {"0000": 1892, "0010": 354, "0100": 385, "0111": 356},
    "1010": {"0000": 577, "1010": 128, "1111": 134},
    "1011": {"1111": 361, "0011": 288},
    "0110": {"0011": 364, "1111": 313},
}


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def _empty_g4() -> dict:
    return {
        "n": 0,
        "n_cob": 0,
        "types": {key: 0 for key in PACK_KEYS},
    }


def _walk_grid(k: int, q: int) -> dict:
    """Packed vs green4 census on covering G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    g4s = {sh: _empty_g4() for sh in G1_SHAPES}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                g4 = green4(n, j)
                if g4 != g1_green4(n, j):
                    return {"ok": False, "g4": True, "n": n, "j": j}
                rec = g4s[_fmt(g4)]
                rec["n"] += 1
                rec["types"][_fmt(four)] += 1
                if cob_shaped(*four):
                    rec["n_cob"] += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "g4s": g4s,
        "xor_j": xor_j,
    }


def _add_g4(dst: dict, src: dict) -> None:
    dst["n"] += src["n"]
    dst["n_cob"] += src["n_cob"]
    for key in PACK_KEYS:
        dst["types"][key] += src["types"][key]


def pack_g4_cover() -> dict:
    """Packed vs green4 16x4 on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = 0
    g4s = {sh: _empty_g4() for sh in G1_SHAPES}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_grid(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            for sh in G1_SHAPES:
                _add_g4(g4s[sh], w["g4s"][sh])
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    n_cells = 0
    n_cob = 0
    for sh in G1_SHAPES:
        rec = g4s[sh]
        rec["n_types"] = sum(1 for v in rec["types"].values() if v)
        n_cells += rec["n_types"]
        n_cob += rec["n_cob"]
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g1 == sum(WANT_G4.values())
        and n_cells == 64
        and n_cob == 13628
        and all(g4s[sh]["n"] == WANT_G4[sh] for sh in G1_SHAPES)
        and all(g4s[sh]["n"] == sum(g4s[sh]["types"].values()) for sh in G1_SHAPES)
        and all(g4s[sh]["n_types"] == 16 for sh in G1_SHAPES)
        and all(g4s[sh]["n_cob"] > 0 for sh in G1_SHAPES)
        and all(
            g4s[sh]["types"][fk] == cnt
            for sh, cells in WANT_CELL.items()
            for fk, cnt in cells.items()
        )
        and all(g4s[sh]["types"][fk] > 0 for sh in G1_SHAPES for fk in PACK_KEYS)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_cells": n_cells,
        "n_cob": n_cob,
        "g4s": g4s,
        "rows": rows,
    }


def _kill_four(k: int, s_hit: int, n_hit: int, j_hit: int, p_hit: int):
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p_hit - 3 + i) for i in range(4))
    return k, s_hit, n_hit, j_hit, p_hit, four


def killed_eq_g4() -> dict:
    """Packed always equals green4: G(1,1) is 0000 vs 1010."""
    k, s, n, j, p, four = _kill_four(0, 7, 1, 1, 8)
    g4 = green4(n, j)
    ok = (
        G(n, j) == 1
        and g4 == g1_green4(n, j) == (1, 0, 1, 0)
        and four == (0, 0, 0, 0)
        and four != g4
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
    }


def killed_fn_of_g4() -> dict:
    """Packed is a function of green4: isolated 0111 takes 0010 and 0100."""
    k0, s0, n0, j0, p0, four0 = _kill_four(2, 39, 0, 0, 40)
    k1, s1, n1, j1, p1, four1 = _kill_four(1, 5, 3, 3, 6)
    g40 = green4(n0, j0)
    g41 = green4(n1, j1)
    ok = (
        isolated_one(n0, j0)
        and isolated_one(n1, j1)
        and g40 == g41 == (0, 1, 1, 1)
        and four0 == (0, 0, 1, 0)
        and four1 == (0, 1, 0, 0)
        and four0 != four1
        and p0 >= 4
        and p1 >= 4
    )
    return {
        "ok": ok,
        "a": {"k": k0, "s": s0, "n": n0, "j": j0, "p": p0, "four": list(four0)},
        "b": {"k": k1, "s": s1, "n": n1, "j": j1, "p": p1, "four": list(four1)},
        "g4": list(g40),
    }


def killed_cob_only_0111() -> dict:
    """Cob packed only on green4 0111: G(1,1) is cob 0000 vs 1010."""
    k, s, n, j, p, four = _kill_four(0, 7, 1, 1, 8)
    g4 = green4(n, j)
    ok = (
        G(n, j) == 1
        and cob_shaped(*four)
        and four == (0, 0, 0, 0)
        and g4 == (1, 0, 1, 0)
        and g4 != (0, 1, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
    }


def prefixes() -> dict:
    kf = json.loads(KF_JSON.read_text())
    ok = (
        kf["checks"]["all_ok"]
        and kf["verdict"]["fresh_dual_all_16"] == "LEMMA"
        and kf["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g1_green4(0, 0) == (0, 1, 1, 1)
    assert cob_shaped(0, 0, 0, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = die_g4_table()
    sc = pack_g4_cover()
    k0 = killed_eq_g4()
    k1 = killed_fn_of_g4()
    k2 = killed_cob_only_0111()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "die_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "pack_g4_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_eq_g4": {k: k0[k] for k in k0 if k != "ok"},
        "killed_fn_of_g4": {k: k1[k] for k in k1 if k != "ok"},
        "killed_cob_only_0111": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g1_four_shapes": True,
            "pack_g4_all_64": True,
            "covering_pack_g4": True,
            "eq_g4": False,
            "fn_of_g4": False,
            "cob_only_0111": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g1_four_shapes": "LEMMA",
            "pack_g4_all_64": "LEMMA",
            "covering_pack_g4": "LEMMA",
            "eq_g4": "KILLED",
            "fn_of_g4": "KILLED",
            "cob_only_0111": "KILLED",
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
    print("die_g4_table", dump["die_g4_table"])
    cov = dump["pack_g4_cover"]
    print(
        "pack_g4_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_cells",
        cov["n_cells"],
        "n_cob",
        cov["n_cob"],
        "g4s",
        {sh: {k: cov["g4s"][sh][k] for k in ("n", "n_cob", "n_types")} for sh in G1_SHAPES},
    )
    print("killed_eq_g4", dump["killed_eq_g4"])
    print("killed_fn_of_g4", dump["killed_fn_of_g4"])
    print("killed_cob_only_0111", dump["killed_cob_only_0111"])


if __name__ == "__main__":
    main()
