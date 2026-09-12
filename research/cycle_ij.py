#!/usr/bin/env python3
"""Cycle IJ: Green has no 4-run of ones; consecutive G=1 green4 is 3-shaped.

G(n,·) runs have length 1, 2, or 3 only (n<64). Consecutive G=1 never
has both outer neighbors 1, so green4 is (1,0,1,1-gm) and
(gp2,1-gp2,1,0) with (gm,gp2) in {(0,0),(0,1),(1,0)}. Green does
have run-3; consecutive G=1 is not always an isolated pair;
consecutive G=1 green4 is not always the isolated-pair shape.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ij.py --certify
Dump: research/cycle_ij.json
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
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
II_JSON = Path(__file__).resolve().parent / "cycle_ii.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

G11_NEIGH = ((0, 0), (0, 1), (1, 0))


def g11_green4(n: int, j: int):
    """green4 pair on G(j)=G(j+1)=1, else None."""
    if G(n, j) == 0 or G(n, j + 1) == 0:
        return None
    gm = G(n, j - 1)
    gp2 = G(n, j + 2)
    return ((1, 0, 1, 1 - gm), (gp2, 1 - gp2, 1, 0))


def g_run_table() -> dict:
    """n<64: no 4-run; consecutive G=1 green4 is g11_green4."""
    n_run1 = n_run2 = n_run3 = n_g11 = 0
    for n in range(0, 64):
        run = 0
        for j in range(0, 2 * n + 2):
            bit = G(n, j) if j <= 2 * n else 0
            if bit:
                run += 1
                continue
            if run == 1:
                n_run1 += 1
            elif run == 2:
                n_run2 += 1
            elif run == 3:
                n_run3 += 1
            elif run >= 4:
                return {"ok": False, "run4": True, "n": n, "run": run}
            run = 0
        for j in range(0, 2 * n):
            pred = g11_green4(n, j)
            if pred is None:
                continue
            gm, gp2 = G(n, j - 1), G(n, j + 2)
            if (gm, gp2) not in G11_NEIGH:
                return {"ok": False, "neigh": True, "n": n, "j": j}
            if green4(n, j) != pred[0] or green4(n, j + 1) != pred[1]:
                return {"ok": False, "g4": True, "n": n, "j": j}
            n_g11 += 1
    ok = n_g11 == 512 and n_run1 == 461 and n_run2 == 230 and n_run3 == 141
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_run1": n_run1,
        "n_run2": n_run2,
        "n_run3": n_run3,
    }


def _walk_g11(k: int, q: int) -> dict:
    """No 4-run on covering G; consecutive G=1 green4 matches g11_green4."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = 0
    n_iso = n_left = n_right = n_both_and = 0
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
                bits[j] = (four, packed, p)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                pred = g11_green4(n, j)
                if pred is None:
                    continue
                gm, gp2 = G(n, j - 1), G(n, j + 2)
                if (gm, gp2) not in G11_NEIGH:
                    return {"ok": False, "neigh": True, "k": k, "n": n, "j": j}
                if green4(n, j) != pred[0] or green4(n, j + 1) != pred[1]:
                    return {"ok": False, "g4": True, "k": k, "n": n, "j": j}
                if j not in bits or (j + 1) not in bits:
                    continue
                n_g11 += 1
                if (gm, gp2) == (0, 0):
                    n_iso += 1
                elif (gm, gp2) == (0, 1):
                    n_left += 1
                else:
                    n_right += 1
                if bits[j][1] and bits[j + 1][1]:
                    n_both_and += 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
        "n_both_and": n_both_and,
        "xor_j": xor_j,
    }


def g11_cover() -> dict:
    """Consecutive G=1 green4 on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_iso = n_left = n_right = n_both_and = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g11(k, q)
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
            n_iso += w["n_iso"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_both_and += w["n_both_and"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_iso": w["n_iso"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_both_and": w["n_both_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_iso == 3817
        and n_left == 2380
        and n_right == 2380
        and n_both_and == 463
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
        "n_both_and": n_both_and,
        "rows": rows,
    }


def _seed_n1():
    """k=0, s=3, n=1, j=0 vs 1 on q=6 (Green triple 111)."""
    k, s, n, j, j2, p, p2 = 0, 3, 1, 0, 1, 6, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    g4 = green4(n, j)
    g42 = green4(n, j2)
    gm, gp2 = G(n, j - 1), G(n, j + 2)
    return k, s, n, j, j2, p, p2, four, four2, g4, g42, gm, gp2


def killed_no_run3() -> dict:
    """Green has a run of 3: G(1)=(1,1,1)."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, gm, gp2 = _seed_n1()
    bits = [G(n, i) for i in range(0, 2 * n + 1)]
    ok = (
        bits == [1, 1, 1]
        and G(n, 0) == 1
        and G(n, 1) == 1
        and G(n, 2) == 1
        and p >= 4
        and p2 >= 4
        and j2 == j + 1
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
        "G": bits,
    }


def killed_g11_always_iso() -> dict:
    """Consecutive G=1 is not always an isolated pair: (gm,gp2)=(0,1)."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, gm, gp2 = _seed_n1()
    ok = (
        (gm, gp2) == (0, 1)
        and (gm, gp2) != (0, 0)
        and G(n, j) == 1
        and G(n, j2) == 1
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
        "gm": gm,
        "gp2": gp2,
    }


def killed_g11_always_iso_g4() -> dict:
    """Consecutive G=1 green4 is not always (1011, 0110): 1011 vs 1010."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, gm, gp2 = _seed_n1()
    iso = ((1, 0, 1, 1), (0, 1, 1, 0))
    ok = (
        g4 == (1, 0, 1, 1)
        and g42 == (1, 0, 1, 0)
        and (g4, g42) != iso
        and g11_green4(n, j) == (g4, g42)
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
        "g4": list(g4),
        "g42": list(g42),
        "iso": [list(iso[0]), list(iso[1])],
    }


def prefixes() -> dict:
    ii = json.loads(II_JSON.read_text())
    ok = (
        ii["checks"]["all_ok"]
        and ii["verdict"]["stride2_overlap_packed_green4_error"] == "LEMMA"
        and ii["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g11_green4(1, 0) == ((1, 0, 1, 1), (1, 0, 1, 0))
    assert g11_green4(2, 0) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = g_run_table()
    sc = g11_cover()
    k0 = killed_no_run3()
    k1 = killed_g11_always_iso()
    k2 = killed_g11_always_iso_g4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g_run_table": {k: rt[k] for k in rt if k != "ok"},
        "g11_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_no_run3": {k: k0[k] for k in k0 if k != "ok"},
        "killed_g11_always_iso": {k: k1[k] for k in k1 if k != "ok"},
        "killed_g11_always_iso_g4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "G_no_4run": True,
            "g11_green4_shape": True,
            "covering_g11_green4": True,
            "G_no_run3": False,
            "g11_always_iso": False,
            "g11_always_iso_g4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_no_4run": "LEMMA",
            "g11_green4_shape": "LEMMA",
            "covering_g11_green4": "LEMMA",
            "G_no_run3": "KILLED",
            "g11_always_iso": "KILLED",
            "g11_always_iso_g4": "KILLED",
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
    print("g_run_table", dump["g_run_table"])
    cov = dump["g11_cover"]
    print(
        "g11_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_iso",
        cov["n_iso"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_both_and",
        cov["n_both_and"],
    )
    print("killed_no_run3", dump["killed_no_run3"])
    print("killed_g11_always_iso", dump["killed_g11_always_iso"])
    print("killed_g11_always_iso_g4", dump["killed_g11_always_iso_g4"])


if __name__ == "__main__":
    main()
