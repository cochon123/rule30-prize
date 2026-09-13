#!/usr/bin/env python3
"""Cycle MQ: on q=10 for k<=8, palindrome-right d%3==1 xor of G(n,j+1) on G=1 is 1 iff k%4 in (1, 2).

On covering J10 for k<=8, XOR of G(n,j+1) over covering G=1 cells
with j>n and (j-n)%3==1 (p=T-2j>=0; no packed row) is 1 iff
k%4 in (1, 2). Dual of Cycle MM's G(n,j-1) d31 = k%4==0. Not rest
(k=1: jp1=1, rest=0); not 0; not k%4 in (1, 2) on q=6 (k=1 jp1=0);
not Green d31; not leftover d31 G(j-1); not Green-only rest; not
the form for all k. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_mq.py --certify
Dump: research/cycle_mq.json
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
from cycle_mm import want_d31
from cycle_mp import want_d31_jm1

OUT = Path(__file__).resolve().with_suffix(".json")
MM_JSON = Path(__file__).resolve().parent / "cycle_mm.json"
MP_JSON = Path(__file__).resolve().parent / "cycle_mp.json"


def want_d31_jp1(k: int) -> int:
    """palindrome-right d%3==1 xor of G(n,j+1) on q=10 k<=8: 1 iff k%4 in (1, 2)."""
    return int(k % 4 in (1, 2))


def _walk_d31_jp1(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j+1) on j>n with (j-n)%3==1; no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_d31 = xor_jp1 = xor_jm1 = 0
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
            if (j - n) % 3 == 1:
                n_d31 += 1
                xor_jp1 ^= G(n, j + 1)
                xor_jm1 ^= G(n, j - 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d31": n_d31,
        "xor_jp1": xor_jp1,
        "xor_jm1": xor_jm1,
    }


def q10_d31_jp1() -> dict:
    """k<=8 q=10: d%3==1 G(j+1) xor is 1 iff k%4 in (1, 2); jm1 matches MM."""
    n_ok = n_g1 = n_d31 = 0
    rows = {}
    mm = json.loads(MM_JSON.read_text())
    for k in range(0, 9):
        w = _walk_d31_jp1(k, 10)
        wj = want_d31_jp1(k)
        mm_row = mm["q10_d31"]["rows"][str(k)]
        if (
            not w.get("ok")
            or w["xor_jp1"] != wj
            or w["xor_jm1"] != want_d31(k)
            or w["xor_jm1"] != mm_row["xor_d31"]
            or w["n_ok"] != mm_row["n_ok"]
            or w["n_g1"] != mm_row["n_g1"]
            or w["n_d31"] != mm_row["n_d31"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_jp1": w.get("xor_jp1"),
                "wj": wj,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_jp1": w["xor_jp1"],
            "xor_jm1": w["xor_jm1"],
            "n_d31": w["n_d31"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_jp1"] == want_d31_jp1(k) for k in range(0, 9))
        and rows["1"]["xor_jp1"] == 1
        and want_rest10(1, 10) == 0
        and rows["2"]["xor_jp1"] == 1
        and rows["5"]["xor_jp1"] == 1
        and rows["6"]["xor_jp1"] == 1
        and rows["0"]["xor_jp1"] == 0
        and rows["8"]["xor_jp1"] == 0
        and rows["0"]["xor_jm1"] == 1
        and rows["1"]["n_d31"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_d31": n_d31, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """d31 G(j+1) xor equals rest: k=1 q=10 is 1 vs 0."""
    r = q10["rows"]["1"]
    wr = want_rest10(1, 10)
    ok = r["xor_jp1"] == 1 and wr == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_jp1": r["xor_jp1"], "rest": wr}


def killed_zero(q10: dict) -> dict:
    """d31 G(j+1) xor vanishes on q=10: k=1 is 1."""
    r = q10["rows"]["1"]
    ok = r["xor_jp1"] == 1
    return {"ok": ok, "k": 1, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_eq_jm1(q10: dict) -> dict:
    """d31 G(j+1) equals Green d31 G(j-1): k=1 jp1=1 jm1=0."""
    r = q10["rows"]["1"]
    ok = r["xor_jp1"] == 1 and r["xor_jm1"] == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_jp1": r["xor_jp1"], "xor_jm1": r["xor_jm1"]}


def killed_eq_left(q10: dict) -> dict:
    """d31 G(j+1) equals leftover d31 G(j-1): leftover is rest, k=1 is 1 vs 0."""
    r = q10["rows"]["1"]
    ok = r["xor_jp1"] == 1 and want_d31_jm1(1) == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_jp1": r["xor_jp1"], "d31_jm1": 0}


def killed_q6_mod() -> dict:
    """d31 G(j+1) is k%4 in (1, 2) on q=6: k=1 has xor=0 but 1%4==1."""
    w = _walk_d31_jp1(1, 6)
    ok = w.get("ok") and w["xor_jp1"] == 0 and want_d31_jp1(1) == 1
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_jp1": w.get("xor_jp1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d31": w.get("n_d31"),
    }


def prefixes() -> dict:
    mm = json.loads(MM_JSON.read_text())
    mp = json.loads(MP_JSON.read_text())
    ok = (
        mm["checks"]["all_ok"]
        and mm["verdict"]["d31_mod4"] == "LEMMA"
        and mp["verdict"]["d31_jm1"] == "LEMMA"
        and mm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kz: dict,
    kjm: dict,
    kleft: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kz["ok"]
        and kjm["ok"]
        and kleft["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_d31_jp1(1) == 1 and want_d31_jp1(2) == 1 and want_d31_jp1(0) == 0
    mm = json.loads(MM_JSON.read_text())
    assert q10["n_ok"] == mm["q10_d31"]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_d31_jp1()
    keq = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kjm = killed_eq_jm1(q10)
    kleft = killed_eq_left(q10)
    kq6 = killed_q6_mod()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kz, kjm, kleft, kq6, sc, pref)
    dump = {
        "cycle": "MQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_d31_jp1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_eq_jm1": {k: kjm[k] for k in kjm if k != "ok"},
        "killed_eq_left": {k: kleft[k] for k in kleft if k != "ok"},
        "killed_q6_mod": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "d31_jp1": True,
            "d31_jm1": True,
            "d31_mod4": True,
            "rest10": True,
            "eq_rest": False,
            "d31_jp1_zero": False,
            "eq_jm1": False,
            "eq_left": False,
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
            "d31_jp1": "LEMMA",
            "d31_jm1": "LEMMA",
            "d31_mod4": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "d31_jp1_zero": "KILLED",
            "eq_jm1": "KILLED",
            "eq_left": "KILLED",
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
    print("q10_d31_jp1 n_ok", dump["q10_d31_jp1"]["n_ok"], "n_g1", dump["q10_d31_jp1"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_eq_jm1", dump["killed_eq_jm1"])
    print("killed_eq_left", dump["killed_eq_left"])
    print("killed_q6_mod", dump["killed_q6_mod"])


if __name__ == "__main__":
    main()
