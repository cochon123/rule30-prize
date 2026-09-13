#!/usr/bin/env python3
"""Cycle MK: on q=10 for k<=8, inner palindrome-right xor of G(n,j-1) on G=1 vanishes.

On covering J10 for k<=8, XOR of G(n,j-1) over covering G=1 cells
with n < j <= n + n//2 (p=T-2j>=0; no packed row) is 0, so Cycle
MJ's even-k j>n xor is the outer slice j > n + n//2. Not rest;
not inner empty (k>=1 has inner G=1); not inner vanish on q=6
(k=3 q=6 xor=1); not Green-only rest; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mk.py --certify
Dump: research/cycle_mk.json
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
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10
from cycle_mj import want_jgtn

OUT = Path(__file__).resolve().with_suffix(".json")
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def _walk_inner(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1) on inner vs outer palindrome-right."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_in = n_out = 0
    xor_in = xor_out = xor_jgtn = 0
    t = 0
    s = t0 + 1
    while s < T:
        n = odd_clock(t, U, Q)
        for j in range(0, 2 * n + 1):
            p = T - 2 * j
            if p < 0:
                continue
            n_ok += 1
            if G(n, j) == 0:
                continue
            n_g1 += 1
            if j <= n:
                continue
            v = G(n, j - 1)
            xor_jgtn ^= v
            if j - n <= n // 2:
                n_in += 1
                xor_in ^= v
            else:
                n_out += 1
                xor_out ^= v
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_in": n_in,
        "n_out": n_out,
        "xor_in": xor_in,
        "xor_out": xor_out,
        "xor_jgtn": xor_jgtn,
    }


def q10_inner0() -> dict:
    """k<=8 q=10: inner xor=0 and outer xor=want_jgtn=jgtn."""
    n_ok = n_g1 = n_in = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_inner(k, 10)
        wj = want_jgtn(k)
        mj_jgtn = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["xor_jgtn"]
        if (
            not w.get("ok")
            or w["xor_in"] != 0
            or w["xor_out"] != wj
            or w["xor_jgtn"] != wj
            or w["xor_jgtn"] != mj_jgtn
            or w["xor_jgtn"] != w["xor_in"] ^ w["xor_out"]
            or w["n_ok"] != mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"]
            or w["n_g1"] != mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_in": w.get("xor_in"),
                "xor_out": w.get("xor_out"),
                "wj": wj,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_in += w["n_in"]
        rows[str(k)] = {
            "xor_in": w["xor_in"],
            "xor_out": w["xor_out"],
            "xor_jgtn": w["xor_jgtn"],
            "n_in": w["n_in"],
            "n_out": w["n_out"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_in"] == 0 for k in range(0, 9))
        and all(rows[str(k)]["xor_out"] == want_jgtn(k) for k in range(0, 9))
        and rows["1"]["n_in"] > 0
        and rows["8"]["n_in"] > 0
        and rows["0"]["xor_out"] == 1
        and want_rest10(0, 10) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_in": n_in, "rows": rows}


def killed_q6_inner() -> dict:
    """inner xor vanishes on q=6: k=3 q=6 is 1."""
    w = _walk_inner(3, 6)
    ok = w.get("ok") and w["xor_in"] == 1 and w["n_in"] > 0
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_in": w.get("xor_in"),
        "n_in": w.get("n_in"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def killed_eq_rest(q10: dict) -> dict:
    """inner xor equals rest: inner is 0, rest is 1 at k=2 q=10."""
    r = q10["rows"]["2"]
    wr = want_rest10(2, 10)
    ok = r["xor_in"] == 0 and wr == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_in": r["xor_in"], "rest": wr}


def killed_empty(q10: dict) -> dict:
    """inner G=1 empty on q=10: k=1 has n_in>0."""
    r = q10["rows"]["1"]
    ok = r["n_in"] > 0 and r["xor_in"] == 0
    return {"ok": ok, "k": 1, "q": 10, "n_in": r["n_in"]}


def prefixes() -> dict:
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mj["checks"]["all_ok"]
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kq6: dict,
    keq: dict,
    kemp: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kq6["ok"]
        and keq["ok"]
        and kemp["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_jgtn(8) == 1 and want_rest10(8, 10) == 1
    mj = json.loads(MJ_JSON.read_text())
    n10 = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == n10
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_inner0()
    kq6 = killed_q6_inner()
    keq = killed_eq_rest(q10)
    kemp = killed_empty(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kq6, keq, kemp, sc, pref)
    dump = {
        "cycle": "MK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_inner0": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_q6_inner": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "lemmas": {
            "inner0": True,
            "outer_even": True,
            "jgtn_even": True,
            "jeqn_one": True,
            "q10_jm1": True,
            "q10_gj1": True,
            "rest10": True,
            "q6_inner0": False,
            "eq_rest": False,
            "inner_empty": False,
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
            "inner0": "LEMMA",
            "outer_even": "LEMMA",
            "jgtn_even": "LEMMA",
            "jeqn_one": "LEMMA",
            "q10_jm1": "LEMMA",
            "q10_gj1": "LEMMA",
            "rest10": "LEMMA",
            "q6_inner0": "KILLED",
            "eq_rest": "KILLED",
            "inner_empty": "KILLED",
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
    print("q10_inner0 n_ok", dump["q10_inner0"]["n_ok"], "n_g1", dump["q10_inner0"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_q6_inner", dump["killed_q6_inner"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
