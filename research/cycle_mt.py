#!/usr/bin/env python3
"""Cycle MT: on q=6 for k<=8, palindrome-right even-d xor of G(n,j-1) on G=1 vanishes.

On covering J6 for k<=8, XOR of G(n,j-1) over covering G=1 cells
with j>n and (j-n) even (p=T-2j>=0; no packed row) is 0, so Cycle
MJ's even-k j>n xor is the odd-d slice. Not rest (k=2 q=10:
even=0, rest=1); not 0 on q=10 (k=1 xor=1); not empty (k=1
n_even=2); not pointwise 0 (k=2 n_gjm1=2); not jgtn; not
Green-only rest; not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do
not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mt.py --certify
Dump: research/cycle_mt.json
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
MS_JSON = Path(__file__).resolve().parent / "cycle_ms.json"


def _walk_even(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1) on j>n split by d parity; no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_even = n_gjm1 = xor_even = xor_odd = xor_jgtn = 0
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
            if (j - n) % 2 == 0:
                n_even += 1
                n_gjm1 += v
                xor_even ^= v
            else:
                xor_odd ^= v
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_even": n_even,
        "n_gjm1": n_gjm1,
        "xor_even": xor_even,
        "xor_odd": xor_odd,
        "xor_jgtn": xor_jgtn,
    }


def q6_even0() -> dict:
    """k<=8 q=6: even-d xor=0 and odd-d xor=want_jgtn=jgtn."""
    n_ok = n_g1 = n_even = n_gjm1 = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_even(k, 6)
        wj = want_jgtn(k)
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j6"]
        if (
            not w.get("ok")
            or w["xor_even"] != 0
            or w["xor_odd"] != wj
            or w["xor_jgtn"] != wj
            or w["xor_jgtn"] != mj_row["xor_jgtn"]
            or w["xor_even"] ^ w["xor_odd"] != w["xor_jgtn"]
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 6,
                "xor_even": w.get("xor_even"),
                "xor_odd": w.get("xor_odd"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_even += w["n_even"]
        n_gjm1 += w["n_gjm1"]
        rows[str(k)] = {
            "xor_even": w["xor_even"],
            "xor_odd": w["xor_odd"],
            "xor_jgtn": w["xor_jgtn"],
            "n_even": w["n_even"],
            "n_gjm1": w["n_gjm1"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_even"] == 0 for k in range(0, 9))
        and all(rows[str(k)]["xor_odd"] == want_jgtn(k) for k in range(0, 9))
        and rows["1"]["n_even"] > 0
        and rows["2"]["n_gjm1"] > 0
        and rows["2"]["n_gjm1"] % 2 == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_even": n_even,
        "n_gjm1": n_gjm1,
        "rows": rows,
    }


def killed_q10() -> dict:
    """even-d xor vanishes on q=10: k=1 has xor=1."""
    w = _walk_even(1, 10)
    ok = w.get("ok") and w["xor_even"] == 1
    return {
        "ok": ok,
        "k": 1,
        "q": 10,
        "xor_even": w.get("xor_even"),
        "n_even": w.get("n_even"),
        "n_gjm1": w.get("n_gjm1"),
        "n_ok": w.get("n_ok"),
    }


def killed_eq_rest() -> dict:
    """even-d xor equals rest: k=2 q=10 is 0 vs 1."""
    w = _walk_even(2, 10)
    wr = want_rest10(2, 10)
    ok = w.get("ok") and w["xor_even"] == 0 and wr == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_even": w.get("xor_even"), "rest": wr}


def killed_empty(q6: dict) -> dict:
    """even-d G=1 empty on q=6: k=1 has n_even=2."""
    r = q6["rows"]["1"]
    ok = r["n_even"] > 0 and r["xor_even"] == 0
    return {"ok": ok, "k": 1, "q": 6, "n_even": r["n_even"]}


def killed_pointwise(q6: dict) -> dict:
    """even-d G(j-1) identically 0 on q=6: k=2 has n_gjm1=2."""
    r = q6["rows"]["2"]
    ok = r["n_gjm1"] > 0 and r["n_gjm1"] % 2 == 0 and r["xor_even"] == 0
    return {"ok": ok, "k": 2, "q": 6, "n_gjm1": r["n_gjm1"]}


def killed_eq_jgtn(q6: dict) -> dict:
    """even-d xor equals jgtn: k=0 q=6 is 0 vs 1."""
    r = q6["rows"]["0"]
    ok = r["xor_even"] == 0 and r["xor_jgtn"] == 1
    return {"ok": ok, "k": 0, "q": 6, "xor_even": r["xor_even"], "xor_jgtn": r["xor_jgtn"]}


def prefixes() -> dict:
    mj = json.loads(MJ_JSON.read_text())
    ms = json.loads(MS_JSON.read_text())
    ok = (
        mj["checks"]["all_ok"]
        and ms["checks"]["all_ok"]
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and ms["verdict"]["d31_q6"] == "LEMMA"
        and mj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q6: dict,
    kq10: dict,
    keq: dict,
    kemp: dict,
    kpt: dict,
    kj: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q6["ok"]
        and kq10["ok"]
        and keq["ok"]
        and kemp["ok"]
        and kpt["ok"]
        and kj["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    n6 = sum(mj["bothq_jgtn"]["rows"][str(k)]["j6"]["n_ok"] for k in range(0, 9))
    assert q6["n_ok"] == n6
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q6 = q6_even0()
    kq10 = killed_q10()
    keq = killed_eq_rest()
    kemp = killed_empty(q6)
    kpt = killed_pointwise(q6)
    kj = killed_eq_jgtn(q6)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q6, kq10, keq, kemp, kpt, kj, sc, pref)
    dump = {
        "cycle": "MT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q6_even0": {k: q6[k] for k in q6 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_q10": {k: kq10[k] for k in kq10 if k != "ok"},
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpt[k] for k in kpt if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "even0_q6": True,
            "d31_q6": True,
            "jgtn_even": True,
            "rest10": True,
            "q10_even0": False,
            "eq_rest": False,
            "even_empty": False,
            "pointwise0": False,
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
            "even0_q6": "LEMMA",
            "d31_q6": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "q10_even0": "KILLED",
            "eq_rest": "KILLED",
            "even_empty": "KILLED",
            "pointwise0": "KILLED",
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
    print("q6_even0 n_ok", dump["q6_even0"]["n_ok"], "n_g1", dump["q6_even0"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_q10", dump["killed_q10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])


if __name__ == "__main__":
    main()
