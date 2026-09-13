#!/usr/bin/env python3
"""Cycle MO: on q=10 for k<=8, leftover AND xor on j>n with d%3==1 is 1 iff k%4 in {2,3}.

On covering J10 for k<=8, XOR of leftover packed AND (G=1, p off
{4,6,14} and UNIQUE_REST) with j>n and (j-n)%3==1 is 1 iff k%4
in {2,3}. Dual of Cycle MM's Green d31 = k%4==0. At k=8 leftover
d31=0 while Green d31=1, so MN's proxy misses rest. Not rest
(k=3: 1 vs 0; k=8: 0 vs 1); not Green d31; not k%4 in {2,3} on
q=6 (k=4 d31=1); not Green-only rest; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mo.py --certify
Dump: research/cycle_mo.json
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
from cycle_mn import want_proxy
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ME_JSON = Path(__file__).resolve().parent / "cycle_me.json"
MN_JSON = Path(__file__).resolve().parent / "cycle_mn.json"


def want_lo_d31(k: int) -> int:
    """leftover AND xor on j>n d%3==1, q=10 k<=8: 1 iff k%4 in {2,3}."""
    return int(k % 4 in (2, 3))


def _walk_lo_d31(k: int, q: int) -> dict:
    """Covering leftover AND xor on palindrome-right d%3==1."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_lo = n_d31 = xor_lo = xor_d31 = 0
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
                    if j > n and (j - n) % 3 == 1:
                        n_d31 += 1
                        xor_d31 ^= 1
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
    }


def q10_lo_d31() -> dict:
    """k<=8 q=10: leftover d31 xor is 1 iff k%4 in {2,3}; leftover=rest."""
    n_ok = n_g1 = n_lo = n_d31 = 0
    rows = {}
    me = json.loads(ME_JSON.read_text())
    for k in range(0, 9):
        w = _walk_lo_d31(k, 10)
        wl = want_lo_d31(k)
        wr = want_rest10(k, 10)
        me_row = me["q10_left"]["rows"][str(k)]
        if (
            not w.get("ok")
            or w["xor_d31"] != wl
            or w["xor_lo"] != wr
            or w["n_ok"] != me_row["n_ok"]
            or w["n_g1"] != me_row["n_g1"]
            or w["xor_lo"] != me_row["xor_lo"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_d31": w.get("xor_d31"),
                "wl": wl,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_d31": w["xor_d31"],
            "xor_lo": w["xor_lo"],
            "n_d31": w["n_d31"],
            "n_lo": w["n_lo"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_d31"] == want_lo_d31(k) for k in range(0, 9))
        and rows["2"]["xor_d31"] == 1
        and rows["3"]["xor_d31"] == 1
        and rows["6"]["xor_d31"] == 1
        and rows["7"]["xor_d31"] == 1
        and rows["8"]["xor_d31"] == 0
        and rows["0"]["xor_d31"] == 0
        and rows["8"]["xor_lo"] == 1
        and want_d31(8) == 1
        and want_proxy(8) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_d31": n_d31,
        "rows": rows,
    }


def killed_eq_rest(q10: dict) -> dict:
    """leftover d31 xor equals rest: k=3 is 1 vs 0; k=8 is 0 vs 1."""
    r3 = q10["rows"]["3"]
    r8 = q10["rows"]["8"]
    ok = r3["xor_d31"] == 1 and want_rest10(3, 10) == 0 and r8["xor_d31"] == 0 and r8["xor_lo"] == 1
    return {
        "ok": ok,
        "k3_d31": r3["xor_d31"],
        "k8_d31": r8["xor_d31"],
        "k8_rest": r8["xor_lo"],
    }


def killed_eq_green(q10: dict) -> dict:
    """leftover d31 equals Green d31: k=2 leftover=1 Green=0."""
    r = q10["rows"]["2"]
    ok = r["xor_d31"] == 1 and want_d31(2) == 0
    return {"ok": ok, "k": 2, "q": 10, "lo_d31": r["xor_d31"], "green_d31": 0}


def killed_q6_mod() -> dict:
    """leftover d31 is k%4 in {2,3} on q=6: k=4 has xor=1 but 4%4==0."""
    w = _walk_lo_d31(4, 6)
    ok = w.get("ok") and w["xor_d31"] == 1 and want_lo_d31(4) == 0
    return {
        "ok": ok,
        "k": 4,
        "q": 6,
        "xor_d31": w.get("xor_d31"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d31": w.get("n_d31"),
    }


def prefixes() -> dict:
    me = json.loads(ME_JSON.read_text())
    mn = json.loads(MN_JSON.read_text())
    ok = (
        me["checks"]["all_ok"]
        and me["verdict"]["q10_left"] == "LEMMA"
        and mn["verdict"]["proxy_k8"] == "LEMMA"
        and mn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kg: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kg["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_lo_d31(2) == 1 and want_lo_d31(3) == 1 and want_lo_d31(4) == 0
    me = json.loads(ME_JSON.read_text())
    assert q10["n_ok"] == me["q10_left"]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_lo_d31()
    keq = killed_eq_rest(q10)
    kg = killed_eq_green(q10)
    kq6 = killed_q6_mod()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kg, kq6, sc, pref)
    dump = {
        "cycle": "MO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_lo_d31": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_eq_green": {k: kg[k] for k in kg if k != "ok"},
        "killed_q6_mod": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "lo_d31": True,
            "proxy_k8": True,
            "d31_mod4": True,
            "q10_left": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "eq_green": False,
            "q6_mod": False,
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
            "lo_d31": "LEMMA",
            "proxy_k8": "LEMMA",
            "d31_mod4": "LEMMA",
            "q10_left": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "eq_green": "KILLED",
            "q6_mod": "KILLED",
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
    print("q10_lo_d31 n_ok", dump["q10_lo_d31"]["n_ok"], "n_g1", dump["q10_lo_d31"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_green", dump["killed_eq_green"])
    print("killed_q6_mod", dump["killed_q6_mod"])


if __name__ == "__main__":
    main()
