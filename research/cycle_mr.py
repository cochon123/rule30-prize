#!/usr/bin/env python3
"""Cycle MR: on q=6 and q=10 for k<=8, palindrome-right d%3==0 xor of G(n,j-1) is 1 iff k%4 in (1, 2).

On covering J6,J10 for k<=8, XOR of G(n,j-1) over covering G=1
cells with j>n and (j-n)%3==0 (p=T-2j>=0; no packed row) is 1 iff
k%4 in (1, 2). Holds on both covering q; dual of Cycle MM d%3==1
and Cycle MQ G(j+1) d%3==1 (q=10 only). Not rest (k=1: d30=1,
rest=0); not 0; not Green d31; not MQ G(j+1) on q=6 (k=1 d30=1,
MQ jp1=0); not empty on q=10; not Green-only rest; not the form
for all k. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not
a prize claim.

Run: python3 research/cycle_mr.py --certify
Dump: research/cycle_mr.json
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
from cycle_mq import want_d31_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
MM_JSON = Path(__file__).resolve().parent / "cycle_mm.json"
MQ_JSON = Path(__file__).resolve().parent / "cycle_mq.json"


def want_d30(k: int) -> int:
    """palindrome-right d%3==0 xor of G(n,j-1) on both q k<=8: 1 iff k%4 in (1, 2)."""
    return int(k % 4 in (1, 2))


def _walk_d30(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1) on j>n with (j-n)%3==0; no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_d30 = n_d31 = xor_d30 = xor_d31 = xor_jgtn = 0
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
            r = (j - n) % 3
            if r == 0:
                n_d30 += 1
                xor_d30 ^= v
            elif r == 1:
                n_d31 += 1
                xor_d31 ^= v
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d30": n_d30,
        "n_d31": n_d31,
        "xor_d30": xor_d30,
        "xor_d31": xor_d31,
        "xor_jgtn": xor_jgtn,
    }


def bothq_d30() -> dict:
    """k<=8 both q: d%3==0 G(j-1) xor is 1 iff k%4 in (1, 2)."""
    n_ok = n_g1 = n_d30 = 0
    rows = {}
    mm = json.loads(MM_JSON.read_text())
    mq = json.loads(MQ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_d30(k, q)
            wd = want_d30(k)
            if not w.get("ok") or w["xor_d30"] != wd:
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_d30": w.get("xor_d30"),
                    "wd": wd,
                }
            if q == 10:
                mm_row = mm["q10_d31"]["rows"][str(k)]
                mq_row = mq["q10_d31_jp1"]["rows"][str(k)]
                if (
                    w["xor_d31"] != want_d31(k)
                    or w["xor_d31"] != mm_row["xor_d31"]
                    or w["xor_d30"] != want_d31_jp1(k)
                    or w["xor_d30"] != mq_row["xor_jp1"]
                    or w["n_ok"] != mm_row["n_ok"]
                    or w["n_g1"] != mm_row["n_g1"]
                    or w["n_d31"] != mm_row["n_d31"]
                    or w["n_d31"] != mq_row["n_d31"]
                ):
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_d30": w["xor_d30"],
                        "xor_d31": w["xor_d31"],
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_d30 += w["n_d30"]
            krow[name] = {
                "xor_d30": w["xor_d30"],
                "xor_d31": w["xor_d31"],
                "n_d30": w["n_d30"],
                "n_d31": w["n_d31"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        rows[str(k)] = krow
    ok = (
        all(rows[str(k)]["j6"]["xor_d30"] == want_d30(k) for k in range(0, 9))
        and all(rows[str(k)]["j10"]["xor_d30"] == want_d30(k) for k in range(0, 9))
        and rows["1"]["j6"]["xor_d30"] == 1
        and rows["1"]["j10"]["xor_d30"] == 1
        and rows["0"]["j6"]["xor_d30"] == 0
        and rows["0"]["j10"]["xor_d31"] == 1
        and rows["1"]["j10"]["n_d30"] > 0
        and rows["1"]["j6"]["n_d30"] > 0
        and want_d30(1) == want_d31_jp1(1)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_d30": n_d30, "rows": rows}


def killed_eq_rest(both: dict) -> dict:
    """d30 xor equals rest: k=1 q=10 is 1 vs 0."""
    r = both["rows"]["1"]["j10"]
    wr = want_rest10(1, 10)
    ok = r["xor_d30"] == 1 and wr == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_d30": r["xor_d30"], "rest": wr}


def killed_zero(both: dict) -> dict:
    """d30 xor vanishes: k=1 both q are 1."""
    a = both["rows"]["1"]["j6"]["xor_d30"]
    b = both["rows"]["1"]["j10"]["xor_d30"]
    ok = a == 1 and b == 1
    return {"ok": ok, "k": 1, "xor_j6": a, "xor_j10": b}


def killed_eq_d31(both: dict) -> dict:
    """d30 xor equals Green d31: k=0 q=10 has d30=0 d31=1."""
    r = both["rows"]["0"]["j10"]
    ok = r["xor_d30"] == 0 and r["xor_d31"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_d30": r["xor_d30"], "xor_d31": r["xor_d31"]}


def killed_eq_mq() -> dict:
    """d30 xor equals MQ G(j+1) d31 on q=6: k=1 d30=1 MQ jp1=0."""
    mq = json.loads(MQ_JSON.read_text())
    jp1 = mq["killed_q6_mod"]["xor_jp1"]
    w = _walk_d30(1, 6)
    ok = w.get("ok") and w["xor_d30"] == 1 and jp1 == 0
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_d30": w.get("xor_d30"),
        "xor_jp1": jp1,
        "n_d30": w.get("n_d30"),
    }


def killed_empty(both: dict) -> dict:
    """d%3==0 G=1 empty on q=10: k=1 has n_d30=3."""
    r = both["rows"]["1"]["j10"]
    ok = r["n_d30"] > 0 and r["xor_d30"] == 1
    return {"ok": ok, "k": 1, "q": 10, "n_d30": r["n_d30"]}


def prefixes() -> dict:
    mm = json.loads(MM_JSON.read_text())
    mq = json.loads(MQ_JSON.read_text())
    ok = (
        mm["checks"]["all_ok"]
        and mq["checks"]["all_ok"]
        and mm["verdict"]["d31_mod4"] == "LEMMA"
        and mq["verdict"]["d31_jp1"] == "LEMMA"
        and mm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    both: dict,
    keq: dict,
    kz: dict,
    kd: dict,
    kmq: dict,
    kemp: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        both["ok"]
        and keq["ok"]
        and kz["ok"]
        and kd["ok"]
        and kmq["ok"]
        and kemp["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_d30(1) == 1 and want_d30(2) == 1 and want_d30(0) == 0
    assert want_d30(5) == want_d31_jp1(5)
    mm = json.loads(MM_JSON.read_text())
    n10 = sum(both["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert n10 == mm["q10_d31"]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    both = bothq_d30()
    keq = killed_eq_rest(both)
    kz = killed_zero(both)
    kd = killed_eq_d31(both)
    kmq = killed_eq_mq()
    kemp = killed_empty(both)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, both, keq, kz, kd, kmq, kemp, sc, pref)
    dump = {
        "cycle": "MR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_d30": {k: both[k] for k in both if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_eq_d31": {k: kd[k] for k in kd if k != "ok"},
        "killed_eq_mq": {k: kmq[k] for k in kmq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "lemmas": {
            "d30_both": True,
            "d31_jp1": True,
            "d31_mod4": True,
            "rest10": True,
            "eq_rest": False,
            "d30_zero": False,
            "eq_d31": False,
            "eq_mq": False,
            "d30_empty": False,
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
            "d30_both": "LEMMA",
            "d31_jp1": "LEMMA",
            "d31_mod4": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "d30_zero": "KILLED",
            "eq_d31": "KILLED",
            "eq_mq": "KILLED",
            "d30_empty": "KILLED",
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
    print("bothq_d30 n_ok", dump["bothq_d30"]["n_ok"], "n_g1", dump["bothq_d30"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_eq_d31", dump["killed_eq_d31"])
    print("killed_eq_mq", dump["killed_eq_mq"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
