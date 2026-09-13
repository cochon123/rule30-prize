#!/usr/bin/env python3
"""Cycle MP: on q=10 for k<=8, leftover AND xor of G(n,j-1) on j>n d%3==1 equals rest.

On covering J10 for k<=8, XOR of G(n,j-1) on leftover packed AND
(G=1, p off {4,6,14} and UNIQUE_REST) with j>n and (j-n)%3==1
equals rest. Dual of Cycle MM's Green d31 and Cycle MO's leftover
AND d31. Not leftover AND d31 xor (k=3: 0 vs 1; k=8: 1 vs 0);
not Green d31; not leftover all G(j-1); not rest on q=6 (k=5
d31_gjm1=1); not Green-only rest; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mp.py --certify
Dump: research/cycle_mp.json
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
from cycle_mm import want_d31
from cycle_mo import want_lo_d31
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ME_JSON = Path(__file__).resolve().parent / "cycle_me.json"
MO_JSON = Path(__file__).resolve().parent / "cycle_mo.json"


def want_d31_jm1(k: int) -> int:
    """leftover AND xor of G(n,j-1) on j>n d%3==1, q=10 k<=8: equals rest."""
    return want_rest10(k, 10)


def _walk_d31_jm1(k: int, q: int) -> dict:
    """Covering leftover AND xor of G(n,j-1) on palindrome-right d%3==1."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_lo = n_d31 = 0
    xor_lo = xor_d31 = xor_d31_gjm1 = xor_lo_gjm1 = 0
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
                    xor_lo_gjm1 ^= G(n, j - 1)
                    if j > n and (j - n) % 3 == 1:
                        n_d31 += 1
                        xor_d31 ^= 1
                        xor_d31_gjm1 ^= G(n, j - 1)
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_d31": n_d31,
        "xor_lo": xor_lo,
        "xor_d31": xor_d31,
        "xor_d31_gjm1": xor_d31_gjm1,
        "xor_lo_gjm1": xor_lo_gjm1,
    }


def q10_d31_jm1() -> dict:
    """k<=8 q=10: leftover d31 G(j-1) xor equals rest; AND d31 is MO."""
    n_ok = n_g1 = n_lo = n_d31 = 0
    rows = {}
    me = json.loads(ME_JSON.read_text())
    mo = json.loads(MO_JSON.read_text())
    for k in range(0, 9):
        w = _walk_d31_jm1(k, 10)
        wr = want_d31_jm1(k)
        me_row = me["q10_left"]["rows"][str(k)]
        mo_row = mo["q10_lo_d31"]["rows"][str(k)]
        if (
            not w.get("ok")
            or w["xor_d31_gjm1"] != wr
            or w["xor_lo"] != wr
            or w["xor_d31"] != want_lo_d31(k)
            or w["n_ok"] != me_row["n_ok"]
            or w["n_g1"] != me_row["n_g1"]
            or w["xor_lo"] != me_row["xor_lo"]
            or w["xor_d31"] != mo_row["xor_d31"]
            or w["n_d31"] != mo_row["n_d31"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_d31_gjm1": w.get("xor_d31_gjm1"),
                "wr": wr,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_d31_gjm1": w["xor_d31_gjm1"],
            "xor_d31": w["xor_d31"],
            "xor_lo": w["xor_lo"],
            "xor_lo_gjm1": w["xor_lo_gjm1"],
            "n_d31": w["n_d31"],
            "n_lo": w["n_lo"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_d31_gjm1"] == want_d31_jm1(k) for k in range(0, 9))
        and rows["2"]["xor_d31_gjm1"] == 1
        and rows["6"]["xor_d31_gjm1"] == 1
        and rows["8"]["xor_d31_gjm1"] == 1
        and rows["3"]["xor_d31_gjm1"] == 0
        and rows["3"]["xor_d31"] == 1
        and rows["8"]["xor_d31"] == 0
        and rows["3"]["xor_lo_gjm1"] == 1
        and want_d31(2) == 0
        and rows["2"]["n_d31"] == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_d31": n_d31,
        "rows": rows,
    }


def killed_eq_and(q10: dict) -> dict:
    """leftover d31 G(j-1) xor equals leftover AND d31 xor: k=3 is 0 vs 1."""
    r3 = q10["rows"]["3"]
    r8 = q10["rows"]["8"]
    ok = (
        r3["xor_d31_gjm1"] == 0
        and r3["xor_d31"] == 1
        and r8["xor_d31_gjm1"] == 1
        and r8["xor_d31"] == 0
    )
    return {
        "ok": ok,
        "k3_gjm1": r3["xor_d31_gjm1"],
        "k3_and": r3["xor_d31"],
        "k8_gjm1": r8["xor_d31_gjm1"],
        "k8_and": r8["xor_d31"],
    }


def killed_eq_green(q10: dict) -> dict:
    """leftover d31 G(j-1) equals Green d31: k=2 leftover=1 Green=0."""
    r = q10["rows"]["2"]
    ok = r["xor_d31_gjm1"] == 1 and want_d31(2) == 0
    return {"ok": ok, "k": 2, "q": 10, "d31_gjm1": r["xor_d31_gjm1"], "green_d31": 0}


def killed_eq_all_g(q10: dict) -> dict:
    """leftover all G(j-1) xor equals rest: k=3 is 1 vs 0."""
    r = q10["rows"]["3"]
    ok = r["xor_lo_gjm1"] == 1 and r["xor_d31_gjm1"] == 0
    return {
        "ok": ok,
        "k": 3,
        "q": 10,
        "xor_lo_gjm1": r["xor_lo_gjm1"],
        "xor_d31_gjm1": r["xor_d31_gjm1"],
    }


def killed_q6_rest() -> dict:
    """leftover d31 G(j-1) equals rest on q=6: k=5 has xor=1 rest=0."""
    w = _walk_d31_jm1(5, 6)
    ok = w.get("ok") and w["xor_d31_gjm1"] == 1 and want_rest10(5, 6) == 0
    return {
        "ok": ok,
        "k": 5,
        "q": 6,
        "xor_d31_gjm1": w.get("xor_d31_gjm1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d31": w.get("n_d31"),
    }


def prefixes() -> dict:
    me = json.loads(ME_JSON.read_text())
    mo = json.loads(MO_JSON.read_text())
    ok = (
        me["checks"]["all_ok"]
        and me["verdict"]["q10_left"] == "LEMMA"
        and mo["verdict"]["lo_d31"] == "LEMMA"
        and mo["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kand: dict,
    kg: dict,
    kall: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kand["ok"]
        and kg["ok"]
        and kall["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_d31_jm1(2) == 1 and want_d31_jm1(3) == 0 and want_d31_jm1(8) == 1
    me = json.loads(ME_JSON.read_text())
    assert q10["n_ok"] == me["q10_left"]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_d31_jm1()
    kand = killed_eq_and(q10)
    kg = killed_eq_green(q10)
    kall = killed_eq_all_g(q10)
    kq6 = killed_q6_rest()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kand, kg, kall, kq6, sc, pref)
    dump = {
        "cycle": "MP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_d31_jm1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_and": {k: kand[k] for k in kand if k != "ok"},
        "killed_eq_green": {k: kg[k] for k in kg if k != "ok"},
        "killed_eq_all_g": {k: kall[k] for k in kall if k != "ok"},
        "killed_q6_rest": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "d31_jm1": True,
            "lo_d31": True,
            "d31_mod4": True,
            "q10_left": True,
            "rest10": True,
            "eq_and": False,
            "eq_green": False,
            "eq_all_g": False,
            "q6_rest": False,
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
            "d31_jm1": "LEMMA",
            "lo_d31": "LEMMA",
            "d31_mod4": "LEMMA",
            "q10_left": "LEMMA",
            "rest10": "LEMMA",
            "eq_and": "KILLED",
            "eq_green": "KILLED",
            "eq_all_g": "KILLED",
            "q6_rest": "KILLED",
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
    print("q10_d31_jm1 n_ok", dump["q10_d31_jm1"]["n_ok"], "n_g1", dump["q10_d31_jm1"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_and", dump["killed_eq_and"])
    print("killed_eq_green", dump["killed_eq_green"])
    print("killed_eq_all_g", dump["killed_eq_all_g"])
    print("killed_q6_rest", dump["killed_q6_rest"])


if __name__ == "__main__":
    main()
