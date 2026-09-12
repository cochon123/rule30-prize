#!/usr/bin/env python3
"""Cycle JT: dual of pair_dbl_threes is reverse-swap of the two iso3 windows.

Palindrome dual j -> 2n-j-1 sends even-j 001/010 to odd-j 010/100.
Dual of even-j windows is not even-j; dual of odd-j windows is not
odd-j; dual pair_dbl is the reverse-swap. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jt.py --certify
Dump: research/cycle_jt.json
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
from cycle_iy import dual_pair_start
from cycle_jh import iso3_even
from cycle_js import PAIR_EVEN, PAIR_ODD, pair_dbl_threes
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JS_JSON = Path(__file__).resolve().parent / "cycle_js.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def pair_dbl_rev(threes):
    """Reverse-swap of a pair of iso3 windows."""
    a, b = threes
    return (b[::-1], a[::-1])


def dbl_rev_table() -> dict:
    """n<64: dual pair_dbl_threes is reverse-swap; even maps to odd."""
    if pair_dbl_rev(PAIR_EVEN) != PAIR_ODD:
        return {"ok": False, "even": True}
    if pair_dbl_rev(PAIR_ODD) != PAIR_EVEN:
        return {"ok": False, "odd": True}
    if pair_dbl_rev(pair_dbl_rev(PAIR_EVEN)) != PAIR_EVEN:
        return {"ok": False, "inv": True}
    n_g11 = n_even = n_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = pair_dbl_threes(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            j2 = dual_pair_start(n, j)
            f2 = pair_dbl_threes(n, j2)
            n2 = 2 * n
            threeL2 = iso3_even(n2, 2 * j2)
            threeR2 = iso3_even(n2, 2 * j2 + 2)
            if f2 != pair_dbl_rev(pred) or (threeL2, threeR2) != f2:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "j2": j2,
                }
            n_g11 += 1
            if j % 2 == 0:
                n_even += 1
            else:
                n_odd += 1
    ok = (
        n_g11 == 512
        and n_even == 256
        and n_odd == 256
        and pair_dbl_threes(1, 1) == pair_dbl_rev(pair_dbl_threes(1, 0))
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support pair_dbl_threes reverse-swap; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_dual = n_even = n_odd = 0
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
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                pred = pair_dbl_threes(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                n_g11 += 1
                j2 = dual_pair_start(n, j)
                if j2 not in bits or (j2 + 1) not in bits:
                    continue
                f2 = pair_dbl_threes(n, j2)
                if f2 != pair_dbl_rev(pred):
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if j % 2 == 0:
                    n_even += 1
                else:
                    n_odd += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_even": n_even,
        "n_odd": n_odd,
        "xor_j": xor_j,
    }


def dbl_rev_cover() -> dict:
    """Dual-in-support reverse-swap on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_dual = n_even = n_odd = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rev(k, q)
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
            n_dual += w["n_dual"]
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_dual": w["n_dual"],
                "n_even": w["n_even"],
                "n_odd": w["n_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_dual == 6968
        and n_even == 3484
        and n_odd == 3484
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_even": n_even,
        "n_odd": n_odd,
        "rows": rows,
    }


def killed_even_stays() -> dict:
    """Dual of even-j windows stays even-j: G(1,0) 001/010 maps to 010/100."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    f = pair_dbl_threes(n, j)
    f2 = pair_dbl_threes(n, j2)
    ok = (
        j % 2 == 0
        and f == PAIR_EVEN
        and f2 == pair_dbl_rev(f) == PAIR_ODD
        and f2 != PAIR_EVEN
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
        "threes": [list(f[0]), list(f[1])],
        "threes2": [list(f2[0]), list(f2[1])],
    }


def killed_odd_stays() -> dict:
    """Dual of odd-j windows stays odd-j: G(1,1) 010/100 maps to 001/010."""
    k, s, n, j, p, p2 = 0, 3, 1, 1, 4, 6
    j2 = dual_pair_start(n, j)
    f = pair_dbl_threes(n, j)
    f2 = pair_dbl_threes(n, j2)
    ok = (
        j % 2 == 1
        and f == PAIR_ODD
        and f2 == pair_dbl_rev(f) == PAIR_EVEN
        and f2 != PAIR_ODD
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
        "threes": [list(f[0]), list(f[1])],
        "threes2": [list(f2[0]), list(f2[1])],
    }


def killed_not_revswap() -> dict:
    """Dual pair_dbl is not reverse-swap: G(1,0) dual equals reverse-swap."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    f = pair_dbl_threes(n, j)
    f2 = pair_dbl_threes(n, j2)
    ok = f2 == pair_dbl_rev(f) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "threes": [list(f[0]), list(f[1])],
        "threes2": [list(f2[0]), list(f2[1])],
    }


def prefixes() -> dict:
    js = json.loads(JS_JSON.read_text())
    ok = (
        js["checks"]["all_ok"]
        and js["verdict"]["pair_dbl_threes"] == "LEMMA"
        and js["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert pair_dbl_rev(PAIR_EVEN) == PAIR_ODD
    assert pair_dbl_rev(PAIR_ODD) == PAIR_EVEN
    assert pair_dbl_threes(1, 1) == pair_dbl_rev(pair_dbl_threes(1, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = dbl_rev_table()
    sc = dbl_rev_cover()
    k0 = killed_even_stays()
    k1 = killed_odd_stays()
    k2 = killed_not_revswap()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dbl_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "dbl_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_odd_stays": {k: k1[k] for k in k1 if k != "ok"},
        "killed_not_revswap": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "pair_dbl_rev": True,
            "pair_dbl_dual_rev": True,
            "covering_pair_dbl_rev": True,
            "even_stays": False,
            "odd_stays": False,
            "not_revswap": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "pair_dbl_rev": "LEMMA",
            "pair_dbl_dual_rev": "LEMMA",
            "covering_pair_dbl_rev": "LEMMA",
            "even_stays": "KILLED",
            "odd_stays": "KILLED",
            "not_revswap": "KILLED",
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
    print("dbl_rev_table", dump["dbl_rev_table"])
    cov = dump["dbl_rev_cover"]
    print(
        "dbl_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_dual",
        cov["n_dual"],
        "n_even",
        cov["n_even"],
        "n_odd",
        cov["n_odd"],
    )
    print("killed_even_stays", dump["killed_even_stays"])
    print("killed_odd_stays", dump["killed_odd_stays"])
    print("killed_not_revswap", dump["killed_not_revswap"])


if __name__ == "__main__":
    main()
