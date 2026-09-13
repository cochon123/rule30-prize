#!/usr/bin/env python3
"""Cycle MM: on q=10 for k<=8, palindrome-right d%3==1 xor of G(n,j-1) on G=1 is 1 iff k%4==0.

On covering J10 for k<=8, XOR of G(n,j-1) over covering G=1 cells
with j>n and (j-n)%3==1 (p=T-2j>=0; no packed row) is 1 iff k%4==0.
Not rest (k=0: d31=1, rest=0); not 0; not k%4==0 on q=6 (k=1
d31=1); not j>n even-k (k=2: jgtn=1, d31=0); not Green-only rest;
not the form for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_mm.py --certify
Dump: research/cycle_mm.json
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
ML_JSON = Path(__file__).resolve().parent / "cycle_ml.json"


def want_d31(k: int) -> int:
    """palindrome-right d%3==1 xor of G(n,j-1) on q=10 k<=8: 1 iff k%4==0."""
    return int(k % 4 == 0)


def _walk_d31(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1) on j>n with (j-n)%3==1; no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_d31 = xor_d31 = xor_jgtn = 0
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
            if (j - n) % 3 == 1:
                n_d31 += 1
                xor_d31 ^= v
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d31": n_d31,
        "xor_d31": xor_d31,
        "xor_jgtn": xor_jgtn,
    }


def q10_d31() -> dict:
    """k<=8 q=10: d%3==1 xor is 1 iff k%4==0; jgtn matches MJ."""
    n_ok = n_g1 = n_d31 = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_d31(k, 10)
        wd = want_d31(k)
        wj = want_jgtn(k)
        mj_jgtn = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["xor_jgtn"]
        if (
            not w.get("ok")
            or w["xor_d31"] != wd
            or w["xor_jgtn"] != wj
            or w["xor_jgtn"] != mj_jgtn
            or w["n_ok"] != mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"]
            or w["n_g1"] != mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_d31": w.get("xor_d31"),
                "wd": wd,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_d31": w["xor_d31"],
            "xor_jgtn": w["xor_jgtn"],
            "n_d31": w["n_d31"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_d31"] == want_d31(k) for k in range(0, 9))
        and rows["0"]["xor_d31"] == 1
        and want_rest10(0, 10) == 0
        and rows["2"]["xor_d31"] == 0
        and want_rest10(2, 10) == 1
        and rows["8"]["xor_d31"] == 1
        and rows["2"]["xor_jgtn"] == 1
        and rows["1"]["n_d31"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_d31": n_d31, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """d31 xor equals rest: k=0 q=10 is 1 vs 0."""
    r = q10["rows"]["0"]
    wr = want_rest10(0, 10)
    ok = r["xor_d31"] == 1 and wr == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_d31": r["xor_d31"], "rest": wr}


def killed_zero(q10: dict) -> dict:
    """d31 xor vanishes on q=10: k=0 is 1."""
    r = q10["rows"]["0"]
    ok = r["xor_d31"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_d31": r["xor_d31"]}


def killed_q6_mod4() -> dict:
    """d31 xor is k%4==0 on q=6: k=1 has d31=1 but 1%4!=0."""
    w = _walk_d31(1, 6)
    ok = w.get("ok") and w["xor_d31"] == 1 and want_d31(1) == 0
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_d31": w.get("xor_d31"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d31": w.get("n_d31"),
    }


def killed_eq_jgtn(q10: dict) -> dict:
    """d31 xor equals j>n even-k: k=2 q=10 has jgtn=1 d31=0."""
    r = q10["rows"]["2"]
    ok = r["xor_jgtn"] == 1 and r["xor_d31"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_jgtn": r["xor_jgtn"], "xor_d31": r["xor_d31"]}


def prefixes() -> dict:
    mj = json.loads(MJ_JSON.read_text())
    ml = json.loads(ML_JSON.read_text())
    ok = (
        mj["checks"]["all_ok"]
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and ml["verdict"]["d2_zero"] == "LEMMA"
        and mj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kz: dict,
    kq6: dict,
    kj: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kz["ok"]
        and kq6["ok"]
        and kj["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_d31(0) == 1 and want_d31(1) == 0 and want_d31(4) == 1 and want_d31(8) == 1
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
    q10 = q10_d31()
    keq = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kq6 = killed_q6_mod4()
    kj = killed_eq_jgtn(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kz, kq6, kj, sc, pref)
    dump = {
        "cycle": "MM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_d31": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_q6_mod4": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "d31_mod4": True,
            "d2_zero": True,
            "inner0": True,
            "jgtn_even": True,
            "q10_jm1": True,
            "rest10": True,
            "eq_rest": False,
            "d31_zero": False,
            "q6_mod4": False,
            "eq_jgtn": False,
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
            "d31_mod4": "LEMMA",
            "d2_zero": "LEMMA",
            "inner0": "LEMMA",
            "jgtn_even": "LEMMA",
            "q10_jm1": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "d31_zero": "KILLED",
            "q6_mod4": "KILLED",
            "eq_jgtn": "KILLED",
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
    print("q10_d31 n_ok", dump["q10_d31"]["n_ok"], "n_g1", dump["q10_d31"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_q6_mod4", dump["killed_q6_mod4"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])


if __name__ == "__main__":
    main()
