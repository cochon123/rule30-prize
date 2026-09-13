#!/usr/bin/env python3
"""Cycle MI: on q=10 for k<=8, Green-only xor of G(n,j-1) on G=1 is 1 iff k even.

On covering J10 for k<=8, XOR of G(n,j-1) over covering cells with
G(n,j)=1 (p=T-2j>=0; no packed row) is 1 iff k is even. Equals
Cycle MH leftover AND xor of G(n,j+1). Not rest (k=0 q=10: jm1=1,
rest=0); not 0 on q=10; not k%2 on q=6 (k=0 q=6 even but xor=0);
not leftover jp1 on q=6 (k=6 q=6: jm1=1, MH leftover=0); not
Green-only rest; not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mi.py --certify
Dump: research/cycle_mi.json
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
from cycle_mh import want_gj1

OUT = Path(__file__).resolve().with_suffix(".json")
MH_JSON = Path(__file__).resolve().parent / "cycle_mh.json"


def want_jm1(k: int) -> int:
    """Green-only xor of G(n,j-1) on G=1, q=10 k<=8: 1 iff k even."""
    return int(k % 2 == 0)


def _walk_g1_jm1(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j-1); no packed row."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = xor_jm1 = 0
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
            xor_jm1 ^= G(n, j - 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_jm1": xor_jm1,
    }


def q10_jm1() -> dict:
    """k<=8 q=10: Green-only G=1 xor of G(n,j-1) is 1 iff k even."""
    n_ok = n_g1 = 0
    rows = {}
    mh = json.loads(MH_JSON.read_text())
    for k in range(0, 9):
        w = _walk_g1_jm1(k, 10)
        wj = want_jm1(k)
        wr = want_rest10(k, 10)
        mh_gj1 = mh["q10_gj1"]["rows"][str(k)]["xor_gj1"]
        if (
            not w.get("ok")
            or w["xor_jm1"] != wj
            or w["xor_jm1"] != mh_gj1
            or w["n_ok"] != mh["q10_gj1"]["rows"][str(k)]["n_ok"]
            or w["n_g1"] != mh["q10_gj1"]["rows"][str(k)]["n_g1"]
            or wr != mh["q10_gj1"]["rows"][str(k)]["xor_lo"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_jm1": w.get("xor_jm1"),
                "wj": wj,
                "mh_gj1": mh_gj1,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[str(k)] = {
            "xor_jm1": w["xor_jm1"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_jm1"] == want_jm1(k) for k in range(0, 9))
        and rows["0"]["xor_jm1"] == 1
        and want_rest10(0, 10) == 0
        and rows["4"]["xor_jm1"] == 1
        and want_rest10(4, 10) == 0
        and rows["2"]["xor_jm1"] == 1
        and want_rest10(2, 10) == 1
        and rows["1"]["xor_jm1"] == 0
        and rows["7"]["xor_jm1"] == 0
        and want_jm1(8) == want_gj1(8) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """Green-only G(n,j-1) xor equals rest: k=0 q=10 is 1 vs 0."""
    r = q10["rows"]["0"]
    wr = want_rest10(0, 10)
    ok = r["xor_jm1"] == 1 and wr == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_jm1": r["xor_jm1"], "rest": wr}


def killed_zero(q10: dict) -> dict:
    """Green-only G(n,j-1) xor vanishes on q=10: k=0 is 1."""
    r = q10["rows"]["0"]
    ok = r["xor_jm1"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_jm1": r["xor_jm1"]}


def killed_q6_parity() -> dict:
    """Green-only G(n,j-1) xor is k%2 on q=6: k=0 even but xor=0."""
    w = _walk_g1_jm1(0, 6)
    ok = w.get("ok") and w["xor_jm1"] == 0 and want_jm1(0) == 1
    return {
        "ok": ok,
        "k": 0,
        "q": 6,
        "xor_jm1": w.get("xor_jm1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def killed_eq_lo_q6() -> dict:
    """Green-only jm1 equals leftover jp1 on q=6: k=6 jm1=1 leftover=0."""
    w = _walk_g1_jm1(6, 6)
    mh = json.loads(MH_JSON.read_text())
    lo = mh["killed_q6_parity"]["xor_gj1"]
    ok = w.get("ok") and w["xor_jm1"] == 1 and lo == 0
    return {
        "ok": ok,
        "k": 6,
        "q": 6,
        "xor_jm1": w.get("xor_jm1"),
        "xor_lo_jp1": lo,
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def prefixes() -> dict:
    mh = json.loads(MH_JSON.read_text())
    ok = (
        mh["checks"]["all_ok"]
        and mh["verdict"]["q10_gj1"] == "LEMMA"
        and mh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kz: dict,
    kq6: dict,
    klo: dict,
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
        and klo["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_jm1(0) == 1 and want_jm1(1) == 0 and want_jm1(8) == 1
    mh = json.loads(MH_JSON.read_text())
    assert q10["n_ok"] == mh["q10_gj1"]["n_ok"]
    assert q10["n_g1"] == mh["q10_gj1"]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_jm1()
    keq = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kq6 = killed_q6_parity()
    klo = killed_eq_lo_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kz, kq6, klo, sc, pref)
    dump = {
        "cycle": "MI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_jm1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_q6_parity": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_eq_lo_q6": {k: klo[k] for k in klo if k != "ok"},
        "lemmas": {
            "q10_jm1": True,
            "eq_mh": True,
            "q10_gj1": True,
            "q10_left": True,
            "k10_u0": True,
            "rest10": True,
            "forced10": True,
            "j_form": True,
            "eq_rest": False,
            "jm1_zero": False,
            "q6_parity": False,
            "eq_lo_q6": False,
            "green_only_rest": False,
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
            "q10_jm1": "LEMMA",
            "eq_mh": "LEMMA",
            "q10_gj1": "LEMMA",
            "q10_left": "LEMMA",
            "k10_u0": "LEMMA",
            "rest10": "LEMMA",
            "forced10": "LEMMA",
            "j_form": "LEMMA",
            "eq_rest": "KILLED",
            "jm1_zero": "KILLED",
            "q6_parity": "KILLED",
            "eq_lo_q6": "KILLED",
            "green_only_rest": "KILLED",
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
    print("q10_jm1 n_ok", dump["q10_jm1"]["n_ok"], "n_g1", dump["q10_jm1"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_q6_parity", dump["killed_q6_parity"])
    print("killed_eq_lo_q6", dump["killed_eq_lo_q6"])


if __name__ == "__main__":
    main()
