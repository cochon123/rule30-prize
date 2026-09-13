#!/usr/bin/env python3
"""Cycle MH: on q=10 for k<=8, leftover AND xor of G(n,j+1) is 1 iff k even.

On covering J10 for k<=8, XOR of G(n,j+1) on leftover packed AND
(G=1, p off {4,6,14} and off UNIQUE_REST) is 1 iff k is even.
Not rest (k=0 q=10: gj1=1, rest=0); not 0 on q=10; not k%2 on
q=6 (k=6 q=6 even but xor=0); not Green-only rest (still filters
leftover AND by the packed row); not the form for all k. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mh.py --certify
Dump: research/cycle_mh.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ME_JSON = Path(__file__).resolve().parent / "cycle_me.json"


def want_gj1(k: int) -> int:
    """leftover AND xor of G(n,j+1) on q=10 k<=8: 1 iff k even."""
    return int(k % 2 == 0)


def _walk_lo_gj1(k: int, q: int) -> dict:
    """Covering leftover AND xor of G(n,j+1)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_lo = xor_lo = xor_gj1 = 0
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
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "xor_lo": xor_lo,
        "xor_gj1": xor_gj1,
    }


def q10_gj1() -> dict:
    """k<=8 q=10: leftover AND xor of G(n,j+1) is 1 iff k even."""
    n_ok = n_g1 = n_lo = 0
    rows = {}
    for k in range(0, 9):
        w = _walk_lo_gj1(k, 10)
        wg = want_gj1(k)
        wr = want_rest10(k, 10)
        if (
            not w.get("ok")
            or w["xor_gj1"] != wg
            or w["xor_lo"] != wr
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_gj1": w.get("xor_gj1"),
                "xor_lo": w.get("xor_lo"),
                "wg": wg,
                "wr": wr,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        rows[str(k)] = {
            "xor_gj1": w["xor_gj1"],
            "xor_lo": w["xor_lo"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "n_lo": w["n_lo"],
        }
    ok = (
        all(rows[str(k)]["xor_gj1"] == want_gj1(k) for k in range(0, 9))
        and rows["0"]["xor_gj1"] == 1
        and rows["0"]["xor_lo"] == 0
        and rows["4"]["xor_gj1"] == 1
        and rows["4"]["xor_lo"] == 0
        and rows["2"]["xor_gj1"] == 1
        and rows["2"]["xor_lo"] == 1
        and rows["1"]["xor_gj1"] == 0
        and rows["7"]["xor_gj1"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_lo": n_lo, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """leftover AND xor of G(n,j+1) equals rest: k=0 q=10 is 1 vs 0."""
    r = q10["rows"]["0"]
    ok = r["xor_gj1"] == 1 and r["xor_lo"] == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_gj1": r["xor_gj1"], "xor_lo": r["xor_lo"]}


def killed_zero(q10: dict) -> dict:
    """leftover AND xor of G(n,j+1) vanishes on q=10: k=0 is 1."""
    r = q10["rows"]["0"]
    ok = r["xor_gj1"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_gj1": r["xor_gj1"]}


def killed_q6_parity() -> dict:
    """leftover AND xor of G(n,j+1) is k%2 on q=6: k=6 even but xor=0."""
    w = _walk_lo_gj1(6, 6)
    ok = w.get("ok") and w["xor_gj1"] == 0 and want_gj1(6) == 1
    return {
        "ok": ok,
        "k": 6,
        "q": 6,
        "xor_gj1": w.get("xor_gj1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_lo": w.get("n_lo"),
    }


def prefixes() -> dict:
    me = json.loads(ME_JSON.read_text())
    ok = (
        me["checks"]["all_ok"]
        and me["verdict"]["q10_left"] == "LEMMA"
        and me["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kz: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert q10["ok"] and keq["ok"] and kz["ok"] and kq6["ok"] and sc["ok"] and pref["ok"]
    assert want_gj1(0) == 1 and want_gj1(1) == 0 and want_gj1(8) == 1
    me = json.loads(ME_JSON.read_text())
    assert q10["n_ok"] == me["q10_left"]["n_ok"]
    assert q10["n_g1"] == me["q10_left"]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_gj1()
    keq = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kq6 = killed_q6_parity()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kz, kq6, sc, pref)
    dump = {
        "cycle": "MH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_gj1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_q6_parity": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "q10_gj1": True,
            "q10_left": True,
            "k10_u0": True,
            "q10_u0": True,
            "k9_u0": True,
            "rest10": True,
            "forced10": True,
            "q6_rest0": True,
            "j_form": True,
            "p4_g1_and": True,
            "p6_g1_and": True,
            "eq_rest": False,
            "gj1_zero": False,
            "q6_parity": False,
            "green_only": False,
            "all_k": False,
            "u_vs_j": False,
            "unique0": False,
            "left_eq": False,
            "rest8_all": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "q10_gj1": "LEMMA",
            "q10_left": "LEMMA",
            "k10_u0": "LEMMA",
            "q10_u0": "LEMMA",
            "k9_u0": "LEMMA",
            "rest10": "LEMMA",
            "forced10": "LEMMA",
            "q6_rest0": "LEMMA",
            "j_form": "LEMMA",
            "p4_g1_and": "LEMMA",
            "p6_g1_and": "LEMMA",
            "eq_rest": "KILLED",
            "gj1_zero": "KILLED",
            "q6_parity": "KILLED",
            "green_only": "KILLED",
            "all_k": "KILLED",
            "u_vs_j": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
            "rest8_all": "KILLED",
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
    print("q10_gj1 n_ok", dump["q10_gj1"]["n_ok"], "n_g1", dump["q10_gj1"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_q6_parity", dump["killed_q6_parity"])


if __name__ == "__main__":
    main()
