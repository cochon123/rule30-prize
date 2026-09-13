#!/usr/bin/env python3
"""Cycle MU: on q=6 for k<=8, palindrome-right even-d xor of G(n,j+1) on G=1 is 1 iff k odd.

On covering J6 for k<=8, XOR of G(n,j+1) over covering G=1 cells
with j>n and (j-n) even (p=T-2j>=0; no packed row) is 1 iff k is
odd. Dual of Cycle MT's even-d G(j-1) vanish. Not rest (k=1 q=6:
jp1=1, rest=0); not 0; not jgtn; not MT vanish; not k odd on
q=10 (k=0 jp1=1); not Green-only rest; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mu.py --certify
Dump: research/cycle_mu.json
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
MT_JSON = Path(__file__).resolve().parent / "cycle_mt.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_even_jp1(k: int) -> int:
    """palindrome-right even-d xor of G(n,j+1) on q=6 k<=8: 1 iff k odd."""
    return int(k % 2 == 1)


def _walk_even_jp1(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j+1) on j>n even d; also G(j-1) even xor."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_even = xor_jp1 = xor_jm1 = xor_jgtn = 0
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
            xor_jgtn ^= G(n, j - 1)
            if (j - n) % 2 == 0:
                n_even += 1
                xor_jp1 ^= G(n, j + 1)
                xor_jm1 ^= G(n, j - 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_even": n_even,
        "xor_jp1": xor_jp1,
        "xor_jm1": xor_jm1,
        "xor_jgtn": xor_jgtn,
    }


def q6_even_jp1() -> dict:
    """k<=8 q=6: even-d G(j+1) xor is 1 iff k odd; G(j-1) even xor=0."""
    n_ok = n_g1 = n_even = 0
    rows = {}
    mt = json.loads(MT_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_even_jp1(k, 6)
        wj = want_even_jp1(k)
        mt_row = mt["q6_even0"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j6"]
        if (
            not w.get("ok")
            or w["xor_jp1"] != wj
            or w["xor_jm1"] != 0
            or w["xor_jm1"] != mt_row["xor_even"]
            or w["xor_jgtn"] != want_jgtn(k)
            or w["xor_jgtn"] != mj_row["xor_jgtn"]
            or w["n_ok"] != mt_row["n_ok"]
            or w["n_g1"] != mt_row["n_g1"]
            or w["n_even"] != mt_row["n_even"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 6,
                "xor_jp1": w.get("xor_jp1"),
                "wj": wj,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_even += w["n_even"]
        rows[str(k)] = {
            "xor_jp1": w["xor_jp1"],
            "xor_jm1": w["xor_jm1"],
            "xor_jgtn": w["xor_jgtn"],
            "n_even": w["n_even"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_jp1"] == want_even_jp1(k) for k in range(0, 9))
        and rows["1"]["xor_jp1"] == 1
        and rows["0"]["xor_jp1"] == 0
        and rows["2"]["xor_jp1"] == 0
        and rows["7"]["xor_jp1"] == 1
        and rows["8"]["xor_jp1"] == 0
        and rows["1"]["n_even"] > 0
        and all(rows[str(k)]["xor_jm1"] == 0 for k in range(0, 9))
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_even": n_even, "rows": rows}


def killed_eq_rest(q6: dict) -> dict:
    """even-d G(j+1) xor equals rest: k=1 q=6 is 1 vs 0."""
    r = q6["rows"]["1"]
    wr = want_rest10(1, 6)
    ok = r["xor_jp1"] == 1 and wr == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_jp1": r["xor_jp1"], "rest": wr}


def killed_zero(q6: dict) -> dict:
    """even-d G(j+1) xor vanishes on q=6: k=1 is 1."""
    r = q6["rows"]["1"]
    ok = r["xor_jp1"] == 1
    return {"ok": ok, "k": 1, "q": 6, "xor_jp1": r["xor_jp1"]}


def killed_eq_jgtn(q6: dict) -> dict:
    """even-d G(j+1) equals jgtn: k=1 jp1=1 jgtn=0."""
    r = q6["rows"]["1"]
    ok = r["xor_jp1"] == 1 and r["xor_jgtn"] == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_jp1": r["xor_jp1"], "xor_jgtn": r["xor_jgtn"]}


def killed_eq_mt(q6: dict) -> dict:
    """even-d G(j+1) equals MT G(j-1) vanish: k=1 jp1=1 jm1=0."""
    r = q6["rows"]["1"]
    ok = r["xor_jp1"] == 1 and r["xor_jm1"] == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_jp1": r["xor_jp1"], "xor_jm1": r["xor_jm1"]}


def killed_q10_odd() -> dict:
    """k-odd form on q=10: k=0 even-d G(j+1) xor=1 but 0 is even."""
    w = _walk_even_jp1(0, 10)
    ok = w.get("ok") and w["xor_jp1"] == 1 and want_even_jp1(0) == 0
    return {
        "ok": ok,
        "k": 0,
        "q": 10,
        "xor_jp1": w.get("xor_jp1"),
        "n_even": w.get("n_even"),
        "n_ok": w.get("n_ok"),
    }


def prefixes() -> dict:
    mt = json.loads(MT_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mt["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mt["verdict"]["even0_q6"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mt["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q6: dict,
    keq: dict,
    kz: dict,
    kj: dict,
    kmt: dict,
    kq10: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q6["ok"]
        and keq["ok"]
        and kz["ok"]
        and kj["ok"]
        and kmt["ok"]
        and kq10["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_even_jp1(1) == 1 and want_even_jp1(0) == 0 and want_even_jp1(8) == 0
    mt = json.loads(MT_JSON.read_text())
    assert q6["n_ok"] == mt["q6_even0"]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q6 = q6_even_jp1()
    keq = killed_eq_rest(q6)
    kz = killed_zero(q6)
    kj = killed_eq_jgtn(q6)
    kmt = killed_eq_mt(q6)
    kq10 = killed_q10_odd()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q6, keq, kz, kj, kmt, kq10, sc, pref)
    dump = {
        "cycle": "MU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q6_even_jp1": {k: q6[k] for k in q6 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_mt": {k: kmt[k] for k in kmt if k != "ok"},
        "killed_q10_odd": {k: kq10[k] for k in kq10 if k != "ok"},
        "lemmas": {
            "even_jp1": True,
            "even0_q6": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "even_jp1_zero": False,
            "eq_jgtn": False,
            "eq_mt": False,
            "q10_odd": False,
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
            "even_jp1": "LEMMA",
            "even0_q6": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "even_jp1_zero": "KILLED",
            "eq_jgtn": "KILLED",
            "eq_mt": "KILLED",
            "q10_odd": "KILLED",
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
    print("q6_even_jp1 n_ok", dump["q6_even_jp1"]["n_ok"], "n_g1", dump["q6_even_jp1"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_eq_mt", dump["killed_eq_mt"])
    print("killed_q10_odd", dump["killed_q10_odd"])


if __name__ == "__main__":
    main()
