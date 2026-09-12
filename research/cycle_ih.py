#!/usr/bin/env python3
"""Cycle IH: dual columns swap Green neighbors G(j+1) and G(j-1).

G palindrome sends (G(n,j+1), G(n,j-1)) to (G(n,j-1), G(n,j+1)) on
the dual j2=2n-j. On G=1, dual g1_green4 is the swapped-neighborhood
shape (gm, 1-gm, 1, 1-gp). Dual does not preserve neighbor order;
dual g1_green4 is not primal; dual G=1 AND xor is not always 0.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_ih.py --certify
Dump: research/cycle_ih.json
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
from cycle_hx import reverse_four
from cycle_ig import g1_and_from_slots, g1_green4
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IG_JSON = Path(__file__).resolve().parent / "cycle_ig.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def g_neigh(n: int, j: int) -> tuple[int, int]:
    """Green neighbors (G(n,j+1), G(n,j-1))."""
    return (G(n, j + 1), G(n, j - 1))


def g1_green4_swap(n: int, j: int) -> tuple[int, int, int, int]:
    """g1_green4 at dual 2n-j: (gm, 1-gm, 1, 1-gp)."""
    gp, gm = g_neigh(n, j)
    return (gm, 1 - gm, 1, 1 - gp)


def neigh_swap_table() -> dict:
    """n<64: dual swaps g_neigh; G=1 dual g1_green4 is swapped shape."""
    n_ok = n_g1 = 0
    for n in range(0, 64):
        if g_neigh(n, n)[0] != g_neigh(n, n)[1]:
            return {"ok": False, "center": True, "n": n}
        for j in range(0, n):
            j2 = 2 * n - j
            a, b = g_neigh(n, j)
            if g_neigh(n, j2) != (b, a):
                return {"ok": False, "swap": True, "n": n, "j": j}
            n_ok += 1
            if G(n, j) == 0:
                continue
            n_g1 += 1
            if g1_green4(n, j2) != g1_green4_swap(n, j):
                return {"ok": False, "g4": True, "n": n, "j": j}
            if g1_green4(n, j) != (a, 1 - a, 1, 1 - b):
                return {"ok": False, "primal": True, "n": n, "j": j}
    ok = n_ok == 2016 and g_neigh(0, 0) == (0, 0)
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1}


def _walk_swap(k: int, q: int) -> dict:
    """Dual g_neigh swap on G=1 pairs; AND xor from Cycle IG slots."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_pair_xor = 0
    xor_j = xor_fold = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                if packed != and_clause(*four):
                    return {"ok": False, "pack": True, "k": k, "four": four}
                bits[j] = (four, packed, p)
                n_ok += 1
                if packed and G(n, j):
                    xor_j ^= 1
            if n in bits and bits[n][1]:
                xor_fold ^= 1
            for j in range(0, n):
                j2 = 2 * n - j
                if j not in bits or j2 not in bits:
                    continue
                if G(n, j) == 0:
                    continue
                f, a, p = bits[j]
                g, b, p2 = bits[j2]
                n_pair += 1
                gp, gm = g_neigh(n, j)
                if g_neigh(n, j2) != (gm, gp):
                    return {"ok": False, "swap": True, "k": k, "n": n, "j": j}
                if g1_green4(n, j2) != g1_green4_swap(n, j):
                    return {"ok": False, "g4": True, "k": k, "n": n, "j": j}
                pred = g1_and_from_slots(n, j, f)
                pred2 = g1_and_from_slots(n, j2, g)
                if pred != a or pred2 != b:
                    return {"ok": False, "ig": True, "k": k, "four": f}
                if a ^ b:
                    n_pair_xor += 1
                    xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_pair_xor": n_pair_xor,
        "xor_j": xor_j,
    }


def swap_cover() -> dict:
    """Dual neighbor swap on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_pair_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_swap(k, q)
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
            n_pair += w["n_pair"]
            n_pair_xor += w["n_pair_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_pair": w["n_pair"],
                "n_pair_xor": w["n_pair_xor"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_ok == 95821 and n_pair == 8944 and n_pair_xor == 3246
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_pair_xor": n_pair_xor,
        "rows": rows,
    }


def killed_dual_preserves_neigh() -> dict:
    """Dual does not preserve (gp,gm): k=0, s=7, n=1, j=0 vs 2."""
    k, s, n, j, j2, p, p2 = 0, 7, 1, 0, 2, 10, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    gp, gm = g_neigh(n, j)
    gp2, gm2 = g_neigh(n, j2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (0, 1, 0, 0)
        and (gp, gm) == (1, 0)
        and (gp2, gm2) == (0, 1)
        and (gp, gm) != (gp2, gm2)
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "four": list(four),
        "four2": list(four2),
        "gp": gp,
        "gm": gm,
        "gp2": gp2,
        "gm2": gm2,
    }


def killed_dual_g4_eq_primal() -> dict:
    """Dual g1_green4 is not primal: k=0, s=7, 1011 vs 0110."""
    k, s, n, j, j2, p, p2 = 0, 7, 1, 0, 2, 10, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    g4 = g1_green4(n, j)
    g42 = g1_green4(n, j2)
    ok = (
        g4 == (1, 0, 1, 1)
        and g42 == (0, 1, 1, 0)
        and g4 != g42
        and g42 != reverse_four(*g4)
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "rev": list(reverse_four(*g4)),
    }


def killed_dual_g1_and_xor_0() -> dict:
    """Dual G=1 AND xor is not always 0: k=1, s=5, n=7, 0001 vs 1001."""
    k, s, n, j, j2, p, p2 = 1, 5, 7, 6, 8, 8, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    xor_a = and_clause(*four) ^ and_clause(*four2)
    ok = (
        four == (0, 0, 0, 1)
        and four2 == (1, 0, 0, 1)
        and xor_a == 1
        and g1_and_from_slots(n, j, four) == 0
        and g1_and_from_slots(n, j2, four2) == 1
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "four": list(four),
        "four2": list(four2),
        "xor": xor_a,
    }


def prefixes() -> dict:
    ig = json.loads(IG_JSON.read_text())
    ok = (
        ig["checks"]["all_ok"]
        and ig["verdict"]["g1_AND_from_green4_slots"] == "LEMMA"
        and ig["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g_neigh(1, 0) == (1, 0)
    assert g_neigh(1, 2) == (0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = neigh_swap_table()
    sc = swap_cover()
    k0 = killed_dual_preserves_neigh()
    k1 = killed_dual_g4_eq_primal()
    k2 = killed_dual_g1_and_xor_0()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "neigh_swap_table": {k: rt[k] for k in rt if k != "ok"},
        "swap_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_dual_preserves_neigh": {k: k0[k] for k in k0 if k != "ok"},
        "killed_dual_g4_eq_primal": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_g1_and_xor_0": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_swaps_G_neighbors": True,
            "dual_g1_green4_swapped": True,
            "covering_g1_pair_xor_from_IG": True,
            "dual_preserves_neigh": False,
            "dual_g4_eq_primal": False,
            "dual_g1_and_xor_always_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_swaps_G_neighbors": "LEMMA",
            "dual_g1_green4_swapped": "LEMMA",
            "covering_g1_pair_xor_from_IG": "LEMMA",
            "dual_preserves_neigh": "KILLED",
            "dual_g4_eq_primal": "KILLED",
            "dual_g1_and_xor_always_0": "KILLED",
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
    print("neigh_swap_table", dump["neigh_swap_table"])
    cov = dump["swap_cover"]
    print(
        "swap_cover n_ok",
        cov["n_ok"],
        "n_pair",
        cov["n_pair"],
        "n_pair_xor",
        cov["n_pair_xor"],
    )
    print("killed_dual_preserves_neigh", dump["killed_dual_preserves_neigh"])
    print("killed_dual_g4_eq_primal", dump["killed_dual_g4_eq_primal"])
    print("killed_dual_g1_and_xor_0", dump["killed_dual_g1_and_xor_0"])


if __name__ == "__main__":
    main()
