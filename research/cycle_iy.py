#!/usr/bin/env python3
"""Cycle IY: dual of consecutive G=1 pairs swaps left/right, keeps iso.

Pair (j,j+1) dualizes to (2n-j-1, 2n-j). KIND_DUAL sends left to
right, right to left, iso to iso. Dual of left is not left; dual of
iso is not a triple; dual of a pair is still a pair. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_iy.py --certify
Dump: research/cycle_iy.json
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
from cycle_hu import and_clause
from cycle_in import g_run_kind
from cycle_ix import slot_kind
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IX_JSON = Path(__file__).resolve().parent / "cycle_ix.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

KIND_DUAL = {"left": "right", "right": "left", "iso": "iso"}


def dual_pair_start(n: int, j: int) -> int:
    """Start of the palindrome dual of pair (j, j+1)."""
    return 2 * n - j - 1


def dual_kind(kind: str) -> str:
    """KIND_DUAL image of a g_run_kind label."""
    return KIND_DUAL[kind]


def kind_dual_table() -> dict:
    """n<64: dual pair kind is KIND_DUAL[g_run_kind]."""
    n_ok = n_left = n_right = n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            if kind is None:
                continue
            j2 = dual_pair_start(n, j)
            kind2 = g_run_kind(n, j2)
            pred = dual_kind(kind)
            if kind2 != pred or slot_kind(n, j2) != pred:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "j2": j2,
                    "kind2": kind2,
                }
            n_ok += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
    ok = n_ok == 512 and n_left == 141 and n_right == 141 and n_iso == 230
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
    }


def _walk_dual(k: int, q: int) -> dict:
    """Dual pair kinds on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_pair = n_left = n_right = n_iso = n_xor = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits[j] = packed
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
                j2 = dual_pair_start(n, j)
                if j2 not in bits or (j2 + 1) not in bits:
                    continue
                kind2 = g_run_kind(n, j2)
                pred = dual_kind(kind)
                if kind2 != pred or slot_kind(n, j2) != pred:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                        "j2": j2,
                        "kind2": kind2,
                    }
                n_pair += 1
                if kind == "left":
                    n_left += 1
                elif kind == "right":
                    n_right += 1
                else:
                    n_iso += 1
                if bits[j] != bits[j2]:
                    n_xor += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_pair": n_pair,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "n_xor": n_xor,
        "xor_j": xor_j,
    }


def kind_dual_cover() -> dict:
    """Dual pair kinds on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_pair = n_left = n_right = n_iso = n_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dual(k, q)
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
            n_pair += w["n_pair"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso += w["n_iso"]
            n_xor += w["n_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_pair": w["n_pair"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso": w["n_iso"],
                "n_xor": w["n_xor"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_pair == 6968
        and n_left == 1942
        and n_right == 1942
        and n_iso == 3084
        and n_xor == 2586
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_pair": n_pair,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "n_xor": n_xor,
        "rows": rows,
    }


def killed_left_stays() -> dict:
    """Dual of left is left: G(1,0) left dualizes to right at j=1."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    j2 = dual_pair_start(n, j)
    p2 = 4
    kind = g_run_kind(n, j)
    kind2 = g_run_kind(n, j2)
    ok = (
        kind == "left"
        and kind2 == "right"
        and kind2 == dual_kind(kind)
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "kind": kind,
        "dual": kind2,
    }


def killed_iso_triple() -> dict:
    """Dual of iso is a triple: G(7,3) iso dualizes to iso at j=10."""
    k, s, n, j, p = 2, 9, 7, 3, 18
    j2 = dual_pair_start(n, j)
    p2 = 4
    kind = g_run_kind(n, j)
    kind2 = g_run_kind(n, j2)
    ok = kind == "iso" and kind2 == "iso" and kind2 == dual_kind(kind) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "kind": kind,
        "dual": kind2,
    }


def killed_dual_not_pair() -> dict:
    """Dual of a pair is not a pair: G(1,0) dualizes to a right pair."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    j2 = dual_pair_start(n, j)
    p2 = 4
    kind = g_run_kind(n, j)
    kind2 = g_run_kind(n, j2)
    ok = kind == "left" and kind2 == "right" and kind2 is not None and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "kind": kind,
        "dual": kind2,
    }


def prefixes() -> dict:
    ix = json.loads(IX_JSON.read_text())
    ok = (
        ix["checks"]["all_ok"]
        and ix["verdict"]["slot_kind"] == "LEMMA"
        and ix["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert dual_pair_start(1, 0) == 1
    assert dual_kind("left") == "right"
    assert dual_kind("iso") == "iso"
    assert g_run_kind(1, 1) == "right"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = kind_dual_table()
    sc = kind_dual_cover()
    k0 = killed_left_stays()
    k1 = killed_iso_triple()
    k2 = killed_dual_not_pair()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "kind_dual_table": {k: rt[k] for k in rt if k != "ok"},
        "kind_dual_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_left_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_iso_triple": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_not_pair": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_pair_kind": True,
            "kind_dual_swap": True,
            "covering_kind_dual": True,
            "left_stays_left": False,
            "iso_is_triple": False,
            "dual_not_pair": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_pair_kind": "LEMMA",
            "kind_dual_swap": "LEMMA",
            "covering_kind_dual": "LEMMA",
            "left_stays_left": "KILLED",
            "iso_is_triple": "KILLED",
            "dual_not_pair": "KILLED",
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
    print("kind_dual_table", dump["kind_dual_table"])
    cov = dump["kind_dual_cover"]
    print(
        "kind_dual_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_pair",
        cov["n_pair"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_iso",
        cov["n_iso"],
        "n_xor",
        cov["n_xor"],
    )
    print("killed_left_stays", dump["killed_left_stays"])
    print("killed_iso_triple", dump["killed_iso_triple"])
    print("killed_dual_not_pair", dump["killed_dual_not_pair"])


if __name__ == "__main__":
    main()
