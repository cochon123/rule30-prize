#!/usr/bin/env python3
"""Cycle MY: on q=10 for k<=8, leftover palindrome-right odd-d xor of G(n,j+1) vanishes.

On covering J10 for k<=8, XOR of G(n,j+1) on leftover packed AND
(G=1, p off {4,6,14} and UNIQUE_REST) with j>n and (j-n) odd is
0. Dual of Cycle MH's leftover all-cell G(j+1) even-k xor: the
odd palindrome-right slice vanishes so MH even-k is leftover
j<=n plus even-d pal-right. Not rest (k=2: xor=0, rest=1); not
empty (k=3 n_odd=4); not pointwise 0 (k=3 n_gjp1=2); not vanish
on q=6 (k=7 xor=1); not MH leftover G(j+1); not Green-only rest;
not the form for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_my.py --certify
Dump: research/cycle_my.json
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
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_mh import want_gj1
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
MH_JSON = Path(__file__).resolve().parent / "cycle_mh.json"
MX_JSON = Path(__file__).resolve().parent / "cycle_mx.json"


def _walk_lo_odd_jp1(k: int, q: int) -> dict:
    """Covering leftover AND xor of G(n,j+1) on palindrome-right odd d."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_lo = n_odd = n_gjp1 = 0
    xor_lo = xor_gj1 = xor_odd = 0
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
                if packed and p not in FORCED and p not in UNIQUE_REST:
                    n_lo += 1
                    xor_lo ^= 1
                    xor_gj1 ^= G(n, j + 1)
                    if j > n and (j - n) % 2 == 1:
                        n_odd += 1
                        xor_odd ^= G(n, j + 1)
                        n_gjp1 += G(n, j + 1)
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_odd": n_odd,
        "n_gjp1": n_gjp1,
        "xor_lo": xor_lo,
        "xor_gj1": xor_gj1,
        "xor_odd": xor_odd,
    }


def q10_lo_odd_jp1() -> dict:
    """k<=8 q=10: leftover pal-right odd-d G(j+1) xor vanishes."""
    n_ok = n_g1 = n_lo = n_odd = n_gjp1 = 0
    rows = {}
    mh = json.loads(MH_JSON.read_text())
    for k in range(0, 9):
        w = _walk_lo_odd_jp1(k, 10)
        mh_row = mh["q10_gj1"]["rows"][str(k)]
        wr = want_rest10(k, 10)
        if (
            not w.get("ok")
            or w["xor_odd"] != 0
            or w["xor_gj1"] != want_gj1(k)
            or w["xor_gj1"] != mh_row["xor_gj1"]
            or w["xor_lo"] != wr
            or w["xor_lo"] != mh_row["xor_lo"]
            or w["n_ok"] != mh_row["n_ok"]
            or w["n_g1"] != mh_row["n_g1"]
            or w["n_lo"] != mh_row["n_lo"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_odd": w.get("xor_odd"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        n_odd += w["n_odd"]
        n_gjp1 += w["n_gjp1"]
        rows[str(k)] = {
            "xor_odd": w["xor_odd"],
            "xor_gj1": w["xor_gj1"],
            "xor_lo": w["xor_lo"],
            "n_odd": w["n_odd"],
            "n_gjp1": w["n_gjp1"],
            "n_lo": w["n_lo"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_odd"] == 0 for k in range(0, 9))
        and rows["3"]["n_odd"] == 4
        and rows["3"]["n_gjp1"] == 2
        and rows["8"]["n_odd"] == 3964
        and rows["0"]["xor_gj1"] == 1
        and rows["2"]["xor_lo"] == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_odd": n_odd,
        "n_gjp1": n_gjp1,
        "rows": rows,
    }


def killed_eq_rest(q10: dict) -> dict:
    """leftover odd-d G(j+1) xor equals rest: k=2 q=10 is 0 vs 1."""
    r = q10["rows"]["2"]
    wr = want_rest10(2, 10)
    ok = r["xor_odd"] == 0 and wr == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_odd": r["xor_odd"], "rest": wr}


def killed_empty(q10: dict) -> dict:
    """leftover odd-d G=1 empty: k=3 q=10 has n_odd=4."""
    r = q10["rows"]["3"]
    ok = r["n_odd"] == 4 and r["xor_odd"] == 0
    return {"ok": ok, "k": 3, "q": 10, "n_odd": r["n_odd"]}


def killed_pointwise(q10: dict) -> dict:
    """leftover odd-d G(j+1) pointwise 0: k=3 q=10 has n_gjp1=2."""
    r = q10["rows"]["3"]
    ok = r["n_gjp1"] == 2 and r["xor_odd"] == 0
    return {"ok": ok, "k": 3, "q": 10, "n_gjp1": r["n_gjp1"]}


def killed_eq_mh(q10: dict) -> dict:
    """leftover odd-d G(j+1) equals MH leftover G(j+1): k=0 is 0 vs 1."""
    r = q10["rows"]["0"]
    ok = r["xor_odd"] == 0 and r["xor_gj1"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_odd": r["xor_odd"], "xor_gj1": r["xor_gj1"]}


def killed_q6() -> dict:
    """leftover odd-d G(j+1) vanishes on q=6: k=7 xor=1."""
    w = _walk_lo_odd_jp1(7, 6)
    ok = w.get("ok") and w["xor_odd"] == 1 and w["n_odd"] == 403 and w["n_gjp1"] == 179
    return {
        "ok": ok,
        "k": 7,
        "q": 6,
        "xor_odd": w.get("xor_odd"),
        "n_odd": w.get("n_odd"),
        "n_gjp1": w.get("n_gjp1"),
        "n_lo": w.get("n_lo"),
        "n_ok": w.get("n_ok"),
    }


def prefixes() -> dict:
    mh = json.loads(MH_JSON.read_text())
    mx = json.loads(MX_JSON.read_text())
    ok = (
        mh["checks"]["all_ok"]
        and mx["checks"]["all_ok"]
        and mh["verdict"]["q10_gj1"] == "LEMMA"
        and mx["verdict"]["inner_odd_jm1"] == "LEMMA"
        and mh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kemp: dict,
    kpw: dict,
    kmh: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kmh["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mh = json.loads(MH_JSON.read_text())
    assert q10["n_ok"] == mh["q10_gj1"]["n_ok"]
    assert q10["n_g1"] == mh["q10_gj1"]["n_g1"]
    assert q10["n_lo"] == mh["q10_gj1"]["n_lo"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_lo_odd_jp1()
    keq = killed_eq_rest(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kmh = killed_eq_mh(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kemp, kpw, kmh, kq6, sc, pref)
    dump = {
        "cycle": "MY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_lo_odd_jp1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_eq_mh": {k: kmh[k] for k in kmh if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "lo_odd_jp1": True,
            "gj1": True,
            "inner_odd_jm1": True,
            "rest10": True,
            "eq_rest": False,
            "lo_odd_empty": False,
            "lo_odd_pointwise": False,
            "eq_mh": False,
            "q6_zero": False,
            "green_only_rest": False,
            "all_k": False,
            "u_vs_j": False,
            "unique0": False,
            "left_eq": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "lo_odd_jp1": "LEMMA",
            "gj1": "LEMMA",
            "inner_odd_jm1": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "lo_odd_empty": "KILLED",
            "lo_odd_pointwise": "KILLED",
            "eq_mh": "KILLED",
            "q6_zero": "KILLED",
            "green_only_rest": "KILLED",
            "all_k": "KILLED",
            "u_vs_j": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
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
        "q10_lo_odd_jp1 n_ok",
        dump["q10_lo_odd_jp1"]["n_ok"],
        "n_g1",
        dump["q10_lo_odd_jp1"]["n_g1"],
        "n_lo",
        dump["q10_lo_odd_jp1"]["n_lo"],
        "n_odd",
        dump["q10_lo_odd_jp1"]["n_odd"],
        "n_gjp1",
        dump["q10_lo_odd_jp1"]["n_gjp1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_mh", dump["killed_eq_mh"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
