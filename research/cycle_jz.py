#!/usr/bin/env python3
"""Cycle JZ: cob_pair commutes with reverse-swap.

cob_pair of pair_dbl_rev(threes) equals pair_dbl_rev of cob_pair,
and that is pair_dbl_rev of pair_dbl_fives. Cob of reverse-swap
even-j is not even-j fives; cob of reverse-swap 001/010 is not
00011/01110; cob of reverse-swap is the reverse-swap of cob. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jz.py --certify
Dump: research/cycle_jz.json
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
from cycle_jl import PAIR_EVEN as FIVE_EVEN
from cycle_jl import PAIR_ODD as FIVE_ODD
from cycle_jl import pair_dbl_fives
from cycle_jn import pair_dbl_rev as five_rev
from cycle_js import PAIR_EVEN as THREE_EVEN
from cycle_js import PAIR_ODD as THREE_ODD
from cycle_js import pair_dbl_threes
from cycle_jt import pair_dbl_rev as three_rev
from cycle_jv import cob_pair
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JY_JSON = Path(__file__).resolve().parent / "cycle_jy.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def cob_revsw(threes):
    """cob_pair after reverse-swap of iso3 windows."""
    if threes is None:
        return None
    return cob_pair(three_rev(threes))


def cob_revsw_table() -> dict:
    """n<64: cob_pair commutes with reverse-swap; dual is reverse-swap."""
    if cob_revsw(THREE_EVEN) != FIVE_ODD:
        return {"ok": False, "even": True}
    if cob_revsw(THREE_ODD) != FIVE_EVEN:
        return {"ok": False, "odd": True}
    if cob_revsw(THREE_EVEN) != five_rev(cob_pair(THREE_EVEN)):
        return {"ok": False, "commute_even": True}
    if cob_revsw(THREE_ODD) != five_rev(cob_pair(THREE_ODD)):
        return {"ok": False, "commute_odd": True}
    n_g11 = n_even = n_odd = n_dual = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            th = pair_dbl_threes(n, j)
            fv = pair_dbl_fives(n, j)
            if kind is None:
                if th is not None or fv is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            got = cob_revsw(th)
            want = five_rev(cob_pair(th))
            j2 = dual_pair_start(n, j)
            fv2 = pair_dbl_fives(n, j2)
            if got != want or got != five_rev(fv) or fv2 != got:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "j2": j2,
                }
            n_g11 += 1
            n_dual += 1
            if j % 2 == 0:
                n_even += 1
            else:
                n_odd += 1
    ok = (
        n_g11 == 512
        and n_even == 256
        and n_odd == 256
        and n_dual == 512
        and cob_revsw(pair_dbl_threes(5, 0)) == FIVE_ODD
        and cob_revsw(pair_dbl_threes(5, 1)) == FIVE_EVEN
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_dual": n_dual,
    }


def _walk_revsw(k: int, q: int) -> dict:
    """cob_revsw identity on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_even = n_odd = n_dual = 0
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
                th = pair_dbl_threes(n, j)
                fv = pair_dbl_fives(n, j)
                if kind is None:
                    if th is not None or fv is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                got = cob_revsw(th)
                want = five_rev(cob_pair(th))
                if got != want or got != five_rev(fv):
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_g11 += 1
                if j % 2 == 0:
                    n_even += 1
                else:
                    n_odd += 1
                j2 = dual_pair_start(n, j)
                if j2 in bits and (j2 + 1) in bits:
                    n_dual += 1
                    if cob_revsw(th) != pair_dbl_fives(n, j2):
                        return {
                            "ok": False,
                            "dual": True,
                            "k": k,
                            "n": n,
                            "j": j,
                            "j2": j2,
                        }
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_dual": n_dual,
        "xor_j": xor_j,
    }


def cob_revsw_cover() -> dict:
    """cob_revsw on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_even = n_odd = n_dual = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_revsw(k, q)
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
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            n_dual += w["n_dual"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_even": w["n_even"],
                "n_odd": w["n_odd"],
                "n_dual": w["n_dual"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_even == 4292
        and n_odd == 4285
        and n_dual == 6968
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_dual": n_dual,
        "rows": rows,
    }


def killed_stays_even() -> dict:
    """Cob of reverse-swap even-j is even-j fives: G(5,0) is 01110/11000."""
    k, s, n, j, p = 1, 9, 5, 0, 20
    th = pair_dbl_threes(n, j)
    got = cob_revsw(th)
    ok = (
        j % 2 == 0
        and th == THREE_EVEN
        and got == FIVE_ODD
        and got != FIVE_EVEN
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "threes": [list(th[0]), list(th[1])],
        "fives": [list(got[0]), list(got[1])],
    }


def killed_no_rev() -> dict:
    """Cob of reverse-swap 001/010 is 00011/01110: it is 01110/11000."""
    got = cob_revsw(THREE_EVEN)
    ok = got == FIVE_ODD and got != FIVE_EVEN
    return {
        "ok": ok,
        "threes": [list(THREE_EVEN[0]), list(THREE_EVEN[1])],
        "fives": [list(got[0]), list(got[1])],
    }


def killed_not_commute() -> dict:
    """Cob of reverse-swap is not reverse-swap of cob: G(5,0) matches."""
    k, s, n, j, p = 1, 9, 5, 0, 20
    th = pair_dbl_threes(n, j)
    got = cob_revsw(th)
    ok = got == five_rev(cob_pair(th)) == FIVE_ODD and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "threes": [list(th[0]), list(th[1])],
        "fives": [list(got[0]), list(got[1])],
    }


def prefixes() -> dict:
    jy = json.loads(JY_JSON.read_text())
    ok = (
        jy["checks"]["all_ok"]
        and jy["verdict"]["center_all_16"] == "LEMMA"
        and jy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert cob_revsw(THREE_EVEN) == FIVE_ODD
    assert cob_revsw(THREE_ODD) == FIVE_EVEN
    assert five_rev(FIVE_EVEN) == FIVE_ODD
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = cob_revsw_table()
    sc = cob_revsw_cover()
    k0 = killed_stays_even()
    k1 = killed_no_rev()
    k2 = killed_not_commute()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cob_revsw_table": {k: rt[k] for k in rt if k != "ok"},
        "cob_revsw_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_stays_even": {k: k0[k] for k in k0 if k != "ok"},
        "killed_no_rev": {k: k1[k] for k in k1 if k != "ok"},
        "killed_not_commute": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "cob_revsw_map": True,
            "cob_commute_revsw": True,
            "covering_cob_revsw": True,
            "stays_even": False,
            "no_rev": False,
            "not_commute": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cob_revsw_map": "LEMMA",
            "cob_commute_revsw": "LEMMA",
            "covering_cob_revsw": "LEMMA",
            "stays_even": "KILLED",
            "no_rev": "KILLED",
            "not_commute": "KILLED",
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
    print("cob_revsw_table", dump["cob_revsw_table"])
    cov = dump["cob_revsw_cover"]
    print(
        "cob_revsw_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_even",
        cov["n_even"],
        "n_odd",
        cov["n_odd"],
        "n_dual",
        cov["n_dual"],
    )
    print("killed_stays_even", dump["killed_stays_even"])
    print("killed_no_rev", dump["killed_no_rev"])
    print("killed_not_commute", dump["killed_not_commute"])


if __name__ == "__main__":
    main()
