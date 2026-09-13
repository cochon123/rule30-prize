#!/usr/bin/env python3
"""Cycle NC: on q=6 and q=10 for k<=8, NA's S restricted to n<U is 1 iff k>0 and k%4==0.

On covering J6,J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n<U (p=T-2j>=0; no packed row)
is 1 iff k>0 and k%4==0. This is the n<U slice of Cycle NA's S,
and the two covering q agree cellwise on counts. Not rest (k=4
q=10: xor=1, rest=0); not Green d31 (k=0: 0 vs 1); not MQ d31
G(j+1) (k=4: 1 vs 0); not jgtn (k=2: 0 vs 1); not NA S (k=6
q=10: 0 vs 1); not 0; not empty (k=3 n_s=2); not Green-only rest;
not the form for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_nc.py --certify
Dump: research/cycle_nc.json
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
from cycle_mm import want_d31
from cycle_mq import want_d31_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
NB_JSON = Path(__file__).resolve().parent / "cycle_nb.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"
MQ_JSON = Path(__file__).resolve().parent / "cycle_mq.json"


def want_s_nltu(k: int) -> int:
    """S on n<U both covering q k<=8: 1 iff k>0 and k%4==0."""
    return int(k > 0 and k % 4 == 0)


def _walk_s_nltu(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with n<U; also full S."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_s = n_sg = 0
    xor = xor_sall = xor_jgtn = 0
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
            d = j - n
            if d % 3 == 1 and G(n, j - 1) == 0:
                xor_sall ^= G(n, j + 1)
                if n < U:
                    n_s += 1
                    xor ^= G(n, j + 1)
                    n_sg += G(n, j + 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "n_sg": n_sg,
        "xor": xor,
        "xor_sall": xor_sall,
        "xor_jgtn": xor_jgtn,
    }


def bothq_s_nltu() -> dict:
    """k<=8 both q: S on n<U is 1 iff k>0 and k%4==0; q agree."""
    n_ok = n_g1 = n_s = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mq = json.loads(MQ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        want = want_s_nltu(k)
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_s_nltu(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            if (
                not w.get("ok")
                or w["xor"] != want
                or w["xor_jgtn"] != want_jgtn(k)
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor": w.get("xor"),
                    "want": want,
                }
            if q == 10:
                na_row = na["q10_green_rest"]["rows"][str(k)]
                mq_row = mq["q10_d31_jp1"]["rows"][str(k)]
                if (
                    w["xor_sall"] != na_row["xor_s"]
                    or w["n_ok"] != na_row["n_ok"]
                    or w["n_g1"] != na_row["n_g1"]
                    or want_d31_jp1(k) != mq_row["xor_jp1"]
                ):
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_sall": w.get("xor_sall"),
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_s += w["n_s"]
            krow[name] = {
                "xor": w["xor"],
                "xor_sall": w["xor_sall"],
                "xor_jgtn": w["xor_jgtn"],
                "want": want,
                "rest": want_rest10(k, q),
                "n_s": w["n_s"],
                "n_sg": w["n_sg"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        if krow["j6"]["xor"] != krow["j10"]["xor"] or krow["j6"]["n_s"] != krow["j10"]["n_s"]:
            return {"ok": False, "k": k, "q": "disagree"}
        rows[str(k)] = krow
    ok = (
        all(
            rows[str(k)]["j6"]["xor"] == want_s_nltu(k)
            and rows[str(k)]["j10"]["xor"] == want_s_nltu(k)
            for k in range(0, 9)
        )
        and rows["0"]["j10"]["n_s"] == 0
        and rows["3"]["j10"]["n_s"] == 2
        and rows["3"]["j10"]["n_sg"] == 0
        and rows["4"]["j10"]["n_s"] == 6
        and rows["4"]["j10"]["n_sg"] == 3
        and rows["4"]["j10"]["xor"] == 1
        and rows["8"]["j10"]["n_s"] == 1222
        and want_s_nltu(0) == 0
        and want_d31(0) == 1
        and want_s_nltu(4) == 1
        and want_d31_jp1(4) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "rows": rows,
    }


def killed_eq_rest(qboth: dict) -> dict:
    """S on n<U equals rest: k=4 q=10 is 1 vs 0."""
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"], "rest": r["rest"]}


def killed_eq_d31(qboth: dict) -> dict:
    """S on n<U equals Green d31: k=0 is 0 vs 1."""
    r = qboth["rows"]["0"]["j10"]
    ok = r["xor"] == 0 and want_d31(0) == 1
    return {"ok": ok, "k": 0, "q": 10, "xor": r["xor"], "d31": 1}


def killed_eq_jp1(qboth: dict) -> dict:
    """S on n<U equals MQ d31 G(j+1): k=4 is 1 vs 0."""
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor"] == 1 and want_d31_jp1(4) == 0
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"], "d31_jp1": 0}


def killed_eq_jgtn(qboth: dict) -> dict:
    """S on n<U equals jgtn: k=2 is 0 vs 1."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor"] == 0 and r["xor_jgtn"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor": r["xor"], "xor_jgtn": r["xor_jgtn"]}


def killed_eq_s(qboth: dict) -> dict:
    """S on n<U equals NA S: k=6 q=10 is 0 vs 1."""
    r = qboth["rows"]["6"]["j10"]
    ok = r["xor"] == 0 and r["xor_sall"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor": r["xor"], "xor_sall": r["xor_sall"]}


def killed_zero(qboth: dict) -> dict:
    """S on n<U vanishes: k=4 is 1."""
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"]}


def killed_empty(qboth: dict) -> dict:
    """n<U S empty: k=3 has n_s=2."""
    r = qboth["rows"]["3"]["j10"]
    ok = r["n_s"] == 2 and r["n_sg"] == 0 and r["xor"] == 0
    return {"ok": ok, "k": 3, "q": 10, "n_s": r["n_s"]}


def killed_q6_die(qboth: dict) -> dict:
    """form dies on q=6: k=4 xor=1 equals want."""
    r = qboth["rows"]["4"]["j6"]
    ok = r["xor"] == 1 and want_s_nltu(4) == 1
    return {"ok": ok, "k": 4, "q": 6, "xor": r["xor"]}


def prefixes() -> dict:
    nb = json.loads(NB_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    mq = json.loads(MQ_JSON.read_text())
    ok = (
        nb["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mq["checks"]["all_ok"]
        and nb["verdict"]["green_rest10"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mq["verdict"]["d31_jp1"] == "LEMMA"
        and nb["verdict"]["prize"] == "unsolved"
        and want_s_nltu(4) == 1
        and want_d31(0) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    qboth: dict,
    kr: dict,
    kd: dict,
    kj: dict,
    kjg: dict,
    ks: dict,
    kz: dict,
    kemp: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        qboth["ok"]
        and kr["ok"]
        and kd["ok"]
        and kj["ok"]
        and kjg["ok"]
        and ks["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    both_ok = sum(
        mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
        for k in range(0, 9)
        for name in ("j6", "j10")
    )
    assert qboth["n_ok"] == both_ok
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    qboth = bothq_s_nltu()
    kr = killed_eq_rest(qboth)
    kd = killed_eq_d31(qboth)
    kj = killed_eq_jp1(qboth)
    kjg = killed_eq_jgtn(qboth)
    ks = killed_eq_s(qboth)
    kz = killed_zero(qboth)
    kemp = killed_empty(qboth)
    kq6 = killed_q6_die(qboth)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, qboth, kr, kd, kj, kjg, ks, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_s_nltu": {k: qboth[k] for k in qboth if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_d31": {k: kd[k] for k in kd if k != "ok"},
        "killed_eq_jp1": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_jgtn": {k: kjg[k] for k in kjg if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6_die": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_nltu": True,
            "green_rest10": True,
            "green_rest": True,
            "jgtn_even": True,
            "d31_jp1": True,
            "eq_rest": False,
            "eq_d31": False,
            "eq_jp1": False,
            "eq_jgtn": False,
            "eq_s": False,
            "s_nltu_zero": False,
            "nltu_empty": False,
            "q6_die": False,
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
            "s_nltu": "LEMMA",
            "green_rest10": "LEMMA",
            "green_rest": "LEMMA",
            "jgtn_even": "LEMMA",
            "d31_jp1": "LEMMA",
            "eq_rest": "KILLED",
            "eq_d31": "KILLED",
            "eq_jp1": "KILLED",
            "eq_jgtn": "KILLED",
            "eq_s": "KILLED",
            "s_nltu_zero": "KILLED",
            "nltu_empty": "KILLED",
            "q6_die": "KILLED",
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
    print(
        "bothq_s_nltu n_ok",
        dump["bothq_s_nltu"]["n_ok"],
        "n_g1",
        dump["bothq_s_nltu"]["n_g1"],
        "n_s",
        dump["bothq_s_nltu"]["n_s"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_d31", dump["killed_eq_d31"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6_die", dump["killed_q6_die"])


if __name__ == "__main__":
    main()
