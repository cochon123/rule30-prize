#!/usr/bin/env python3
"""Cycle MJ: on q=6 and q=10 for k<=8, Green-only xor of G(n,j-1) on G=1 with j>n is 1 iff k even.

On covering J6,J10 for k<=8, XOR of G(n,j-1) over covering G=1
cells with j>n (p=T-2j>=0; no packed row) is 1 iff k is even.
Xor at j=n of G(n,n-1) is identically 1. Not rest (k=0 q=10:
jgtn=1, rest=0); not 0; not all-G=1 xor on q=6 (Cycle MI);
not j<n xor identically 1 on q=6 (k=0 q=6 jltn=0); not
Green-only rest; not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do
not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mj.py --certify
Dump: research/cycle_mj.json
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
from cycle_mi import want_jm1

OUT = Path(__file__).resolve().with_suffix(".json")
MI_JSON = Path(__file__).resolve().parent / "cycle_mi.json"


def want_jgtn(k: int) -> int:
    """Green-only xor of G(n,j-1) on G=1 with j>n: 1 iff k even."""
    return int(k % 2 == 0)


def _walk_half(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1) split by j vs n; no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = xor_jm1 = xor_jltn = xor_jgtn = xor_jeqn = 0
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
            v = G(n, j - 1)
            xor_jm1 ^= v
            if j < n:
                xor_jltn ^= v
            elif j > n:
                xor_jgtn ^= v
            else:
                xor_jeqn ^= v
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_jm1": xor_jm1,
        "xor_jltn": xor_jltn,
        "xor_jgtn": xor_jgtn,
        "xor_jeqn": xor_jeqn,
    }


def bothq_jgtn() -> dict:
    """k<=8 both q: j>n xor is 1 iff k even; j=n xor is 1."""
    n_ok = n_g1 = 0
    rows = {}
    mi = json.loads(MI_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_half(k, q)
            wj = want_jgtn(k)
            if (
                not w.get("ok")
                or w["xor_jgtn"] != wj
                or w["xor_jeqn"] != 1
                or w["xor_jm1"] != w["xor_jltn"] ^ w["xor_jgtn"] ^ w["xor_jeqn"]
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_jgtn": w.get("xor_jgtn"),
                    "xor_jeqn": w.get("xor_jeqn"),
                    "wj": wj,
                }
            if q == 10:
                mi_row = mi["q10_jm1"]["rows"][str(k)]
                if (
                    w["xor_jm1"] != mi_row["xor_jm1"]
                    or w["n_ok"] != mi_row["n_ok"]
                    or w["n_g1"] != mi_row["n_g1"]
                    or w["xor_jltn"] != 1
                ):
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_jm1": w["xor_jm1"],
                        "mi": mi_row["xor_jm1"],
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "xor_jgtn": w["xor_jgtn"],
                "xor_jeqn": w["xor_jeqn"],
                "xor_jltn": w["xor_jltn"],
                "xor_jm1": w["xor_jm1"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        rows[str(k)] = krow
    ok = (
        rows["0"]["j6"]["xor_jltn"] == 0
        and rows["0"]["j10"]["xor_jltn"] == 1
        and rows["0"]["j6"]["xor_jm1"] == 0
        and rows["0"]["j10"]["xor_jm1"] == 1
        and all(rows[str(k)]["j6"]["xor_jgtn"] == want_jgtn(k) for k in range(0, 9))
        and all(rows[str(k)]["j10"]["xor_jgtn"] == want_jgtn(k) for k in range(0, 9))
        and all(rows[str(k)][name]["xor_jeqn"] == 1 for k in range(0, 9) for name in ("j6", "j10"))
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_eq_rest(both: dict) -> dict:
    """j>n xor equals rest: k=0 q=10 is 1 vs 0."""
    r = both["rows"]["0"]["j10"]
    wr = want_rest10(0, 10)
    ok = r["xor_jgtn"] == 1 and wr == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_jgtn": r["xor_jgtn"], "rest": wr}


def killed_zero(both: dict) -> dict:
    """j>n xor vanishes: k=0 both q are 1."""
    a = both["rows"]["0"]["j6"]["xor_jgtn"]
    b = both["rows"]["0"]["j10"]["xor_jgtn"]
    ok = a == 1 and b == 1
    return {"ok": ok, "k": 0, "xor_j6": a, "xor_j10": b}


def killed_all_g1(both: dict) -> dict:
    """all G=1 xor is k%2 on q=6: k=0 even but jm1=0 (Cycle MI)."""
    r = both["rows"]["0"]["j6"]
    ok = r["xor_jm1"] == 0 and r["xor_jgtn"] == 1 and want_jm1(0) == 1
    return {"ok": ok, "k": 0, "q": 6, "xor_jm1": r["xor_jm1"], "xor_jgtn": r["xor_jgtn"]}


def killed_jltn_one(both: dict) -> dict:
    """j<n xor identically 1 on q=6: k=0 q=6 is 0."""
    r = both["rows"]["0"]["j6"]
    ok = r["xor_jltn"] == 0
    return {"ok": ok, "k": 0, "q": 6, "xor_jltn": r["xor_jltn"]}


def prefixes() -> dict:
    mi = json.loads(MI_JSON.read_text())
    ok = (
        mi["checks"]["all_ok"]
        and mi["verdict"]["q10_jm1"] == "LEMMA"
        and mi["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    both: dict,
    keq: dict,
    kz: dict,
    kall: dict,
    klt: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        both["ok"]
        and keq["ok"]
        and kz["ok"]
        and kall["ok"]
        and klt["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_jgtn(0) == 1 and want_jgtn(1) == 0 and want_jgtn(8) == 1
    mi = json.loads(MI_JSON.read_text())
    n10 = sum(both["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    g10 = sum(both["rows"][str(k)]["j10"]["n_g1"] for k in range(0, 9))
    assert n10 == mi["q10_jm1"]["n_ok"]
    assert g10 == mi["q10_jm1"]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    both = bothq_jgtn()
    keq = killed_eq_rest(both)
    kz = killed_zero(both)
    kall = killed_all_g1(both)
    klt = killed_jltn_one(both)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, both, keq, kz, kall, klt, sc, pref)
    dump = {
        "cycle": "MJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_jgtn": {k: both[k] for k in both if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_all_g1": {k: kall[k] for k in kall if k != "ok"},
        "killed_jltn_one": {k: klt[k] for k in klt if k != "ok"},
        "lemmas": {
            "jgtn_even": True,
            "jeqn_one": True,
            "q10_jm1": True,
            "q10_gj1": True,
            "q10_left": True,
            "rest10": True,
            "eq_rest": False,
            "jgtn_zero": False,
            "all_g1": False,
            "jltn_one": False,
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
            "jgtn_even": "LEMMA",
            "jeqn_one": "LEMMA",
            "q10_jm1": "LEMMA",
            "q10_gj1": "LEMMA",
            "q10_left": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "jgtn_zero": "KILLED",
            "all_g1": "KILLED",
            "jltn_one": "KILLED",
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
    print("bothq_jgtn n_ok", dump["bothq_jgtn"]["n_ok"], "n_g1", dump["bothq_jgtn"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_all_g1", dump["killed_all_g1"])
    print("killed_jltn_one", dump["killed_jltn_one"])


if __name__ == "__main__":
    main()
