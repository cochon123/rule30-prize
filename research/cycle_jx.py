#!/usr/bin/env python3
"""Cycle JX: consecutive G=1 packed pair-shapes take all 64 values.

Given slot_kind (which fixes KIND_GREEN4), covering packed 4-tuple
pairs hit every 64 stride-2-overlapping shapes per kind; pair-start
4-tuples hit all 16 rows per kind; AND fires all four AND_ONES per
kind. Pair packed is not a function of kind; not always green4;
pair-start AND does not vanish. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_jx.py --certify
Dump: research/cycle_jx.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_ii import stride2_overlap
from cycle_in import g_run_kind
from cycle_iz import KIND_GREEN4
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JW_JSON = Path(__file__).resolve().parent / "cycle_jw.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

KINDS = ("left", "right", "iso")


def pair_shape(left, right):
    """6-window of stride-2 overlapped 4-tuples: right[:2]+left."""
    return right[:2] + left


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def g4_pair_table() -> dict:
    """n<64: consecutive G=1 green4 is KIND_GREEN4 and overlaps."""
    n_g11 = n_left = n_right = n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            if kind is None:
                continue
            g0, g1 = green4(n, j), green4(n, j + 1)
            pred = KIND_GREEN4[kind]
            if (g0, g1) != pred or not stride2_overlap(g0, g1):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "got": [_fmt(g0), _fmt(g1)],
                }
            n_g11 += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
    ok = n_g11 == 512 and n_left == 141 and n_right == 141 and n_iso == 230
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
    }


def _walk_pair(k: int, q: int) -> dict:
    """Consecutive G=1 packed pair census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_ov = 0
    n_kind = {kind: 0 for kind in KINDS}
    n_and_kind = {kind: 0 for kind in KINDS}
    n_both = 0
    n_and_ones = {kind: {four: 0 for four in AND_ONES} for kind in KINDS}
    types = {kind: set() for kind in KINDS}
    shapes = {kind: set() for kind in KINDS}
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            fours = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                fours[j] = four
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                if kind is None:
                    continue
                left, right = fours[j], fours[j + 1]
                if not stride2_overlap(left, right):
                    return {
                        "ok": False,
                        "ov": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                g0, g1 = green4(n, j), green4(n, j + 1)
                if (g0, g1) != KIND_GREEN4[kind]:
                    return {
                        "ok": False,
                        "g4": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                    }
                n_ov += 1
                n_g11 += 1
                n_kind[kind] += 1
                types[kind].add(_fmt(left))
                shapes[kind].add(_fmt(pair_shape(left, right)))
                a0, a1 = and_clause(*left), and_clause(*right)
                if a0:
                    n_and_kind[kind] += 1
                    n_and_ones[kind][left] += 1
                if a0 and a1:
                    n_both += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_ov": n_ov,
        "n_both": n_both,
        "n_kind": n_kind,
        "n_and_kind": n_and_kind,
        "n_and_ones": {
            kind: {_fmt(f): n_and_ones[kind][f] for f in AND_ONES} for kind in KINDS
        },
        "n_types": {kind: len(types[kind]) for kind in KINDS},
        "n_shapes": {kind: len(shapes[kind]) for kind in KINDS},
        "types": {kind: sorted(types[kind]) for kind in KINDS},
        "shapes": {kind: sorted(shapes[kind]) for kind in KINDS},
        "xor_j": xor_j,
    }


def pair_four_cover() -> dict:
    """Pair packed census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_ov = n_and = n_both = 0
    n_kind = {kind: 0 for kind in KINDS}
    n_and_kind = {kind: 0 for kind in KINDS}
    n_and_ones = {kind: {_fmt(f): 0 for f in AND_ONES} for kind in KINDS}
    types = {kind: set() for kind in KINDS}
    shapes = {kind: set() for kind in KINDS}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_pair(k, q)
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
            n_g11 += w["n_g11"]
            n_ov += w["n_ov"]
            n_both += w["n_both"]
            for kind in KINDS:
                n_kind[kind] += w["n_kind"][kind]
                n_and_kind[kind] += w["n_and_kind"][kind]
                n_and += w["n_and_kind"][kind]
                types[kind].update(w["types"][kind])
                shapes[kind].update(w["shapes"][kind])
                for key, val in w["n_and_ones"][kind].items():
                    n_and_ones[kind][key] += val
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_ov": w["n_ov"],
                "n_both": w["n_both"],
                "n_kind": w["n_kind"],
                "n_and_kind": w["n_and_kind"],
                "n_types": w["n_types"],
                "n_shapes": w["n_shapes"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    n_types = {kind: len(types[kind]) for kind in KINDS}
    n_shapes = {kind: len(shapes[kind]) for kind in KINDS}
    and_all4 = all(
        all(n_and_ones[kind][_fmt(f)] > 0 for f in AND_ONES) for kind in KINDS
    )
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_ov == 8577
        and n_kind["left"] == 2380
        and n_kind["right"] == 2380
        and n_kind["iso"] == 3817
        and n_and == 1711
        and n_and_kind["left"] == 431
        and n_and_kind["right"] == 534
        and n_and_kind["iso"] == 746
        and n_both == 463
        and n_and == sum(n_and_kind.values())
        and all(n_types[kind] == 16 for kind in KINDS)
        and all(n_shapes[kind] == 64 for kind in KINDS)
        and and_all4
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_ov": n_ov,
        "n_and": n_and,
        "n_both": n_both,
        "n_kind": n_kind,
        "n_and_kind": n_and_kind,
        "n_types": n_types,
        "n_shapes": n_shapes,
        "n_and_ones": n_and_ones,
        "rows": rows,
    }


def _kill_pair(s_hit: int, n_hit: int, j_hit: int):
    """Packed pair at covering k=1, q=10 (T=20) after s_hit steps."""
    k, T = 1, 20
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    p = T - 2 * j_hit
    left = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    p2 = T - 2 * (j_hit + 1)
    right = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    kind = g_run_kind(n_hit, j_hit)
    return k, s_hit, n_hit, j_hit, p, p2, left, right, kind


def killed_fn_of_kind() -> dict:
    """Packed pair is a function of kind: left G(7,6) is 0001/0100."""
    k, s, n, j, p, p2, left, right, kind = _kill_pair(5, 7, 6)
    pred = KIND_GREEN4["left"]
    ok = (
        kind == "left"
        and (left, right) == ((0, 0, 0, 1), (0, 1, 0, 0))
        and (left, right) != pred
        and pred == ((1, 0, 1, 1), (1, 0, 1, 0))
        and stride2_overlap(left, right)
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "p2": p2,
        "left": list(left),
        "right": list(right),
    }


def killed_always_green4() -> dict:
    """Pair packed always equals green4: same left witness."""
    k, s, n, j, p, p2, left, right, kind = _kill_pair(5, 7, 6)
    pred = KIND_GREEN4["left"]
    ok = (
        kind == "left"
        and (green4(n, j), green4(n, j + 1)) == pred
        and (left, right) != pred
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "p2": p2,
        "left": list(left),
        "right": list(right),
    }


def killed_and_vanishes() -> dict:
    """Pair-start AND vanishes: left G(1,0) is 0100."""
    k, s, n, j, p, p2, left, right, kind = _kill_pair(17, 1, 0)
    ok = (
        kind == "left"
        and left == (0, 1, 0, 0)
        and left in AND_ONES
        and and_clause(*left) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "p2": p2,
        "left": list(left),
        "right": list(right),
    }


def prefixes() -> dict:
    jw = json.loads(JW_JSON.read_text())
    ok = (
        jw["checks"]["all_ok"]
        and jw["verdict"]["iso_all_16"] == "LEMMA"
        and jw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert KIND_GREEN4["left"] == ((1, 0, 1, 1), (1, 0, 1, 0))
    assert (0, 1, 0, 0) in AND_ONES
    assert stride2_overlap((0, 0, 0, 1), (0, 1, 0, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = g4_pair_table()
    sc = pair_four_cover()
    k0 = killed_fn_of_kind()
    k1 = killed_always_green4()
    k2 = killed_and_vanishes()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g4_pair_table": {k: rt[k] for k in rt if k != "ok"},
        "pair_four_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_fn_of_kind": {k: k0[k] for k in k0 if k != "ok"},
        "killed_always_green4": {k: k1[k] for k in k1 if k != "ok"},
        "killed_and_vanishes": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "kind_green4_overlap": True,
            "pair_all_64": True,
            "covering_pair_four": True,
            "fn_of_kind": False,
            "always_green4": False,
            "and_vanishes": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "kind_green4_overlap": "LEMMA",
            "pair_all_64": "LEMMA",
            "covering_pair_four": "LEMMA",
            "fn_of_kind": "KILLED",
            "always_green4": "KILLED",
            "and_vanishes": "KILLED",
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
    print("g4_pair_table", dump["g4_pair_table"])
    cov = dump["pair_four_cover"]
    print(
        "pair_four_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_ov",
        cov["n_ov"],
        "n_and",
        cov["n_and"],
        "n_both",
        cov["n_both"],
        "n_kind",
        cov["n_kind"],
        "n_and_kind",
        cov["n_and_kind"],
        "n_types",
        cov["n_types"],
        "n_shapes",
        cov["n_shapes"],
    )
    print("killed_fn_of_kind", dump["killed_fn_of_kind"])
    print("killed_always_green4", dump["killed_always_green4"])
    print("killed_and_vanishes", dump["killed_and_vanishes"])


if __name__ == "__main__":
    main()
