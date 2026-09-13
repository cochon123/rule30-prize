#!/usr/bin/env python3
"""Cycle NA: on q=10 for k<=8, Green-only (d31 G(j+1) on G(j-1)=0) xor (pal-right G(j-1) on n<U/2) equals rest.

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0, xor XOR of G(n,j-1) over
palindrome-right cells with n<U/2 (p=T-2j>=0; no packed row)
equals rest. Closes Cycle MN's k=8 proxy miss. Not proxy (k=8:
xor=1, proxy=0); not jgtn; not d31; not 0; not empty (k=2 n_t=1);
not the form on q=6 (k=2 xor=1, rest=0); not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_na.py --certify
Dump: research/cycle_na.json
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
from cycle_mn import want_proxy

OUT = Path(__file__).resolve().with_suffix(".json")
MN_JSON = Path(__file__).resolve().parent / "cycle_mn.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"
MZ_JSON = Path(__file__).resolve().parent / "cycle_mz.json"


def _walk_green_rest(k: int, q: int) -> dict:
    """Green-only rest walk: d31 jp1 on jm1=0, xor pal-right jm1 on n<U/2."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_s = n_sg = n_t = n_tg = 0
    xor_s = xor_t = xor_jgtn = 0
    t = 0
    s = t0 + 1
    half = U // 2
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
                n_s += 1
                xor_s ^= G(n, j + 1)
                n_sg += G(n, j + 1)
            if n < half:
                n_t += 1
                xor_t ^= G(n, j - 1)
                n_tg += G(n, j - 1)
        t += 1
        s += 2
    xor = xor_s ^ xor_t
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "n_sg": n_sg,
        "n_t": n_t,
        "n_tg": n_tg,
        "xor_s": xor_s,
        "xor_t": xor_t,
        "xor": xor,
        "xor_jgtn": xor_jgtn,
    }


def q10_green_rest() -> dict:
    """k<=8 q=10: green-only S xor T equals rest; closes MN k=8."""
    n_ok = n_g1 = n_s = n_t = 0
    rows = {}
    mn = json.loads(MN_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_green_rest(k, 10)
        wr = want_rest10(k, 10)
        wp = want_proxy(k)
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        mn_row = mn["q10_proxy"]["rows"][str(k)]
        if (
            not w.get("ok")
            or w["xor"] != wr
            or w["xor_jgtn"] != want_jgtn(k)
            or w["xor_jgtn"] != mj_row["xor_jgtn"]
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
            or wp != mn_row["proxy"]
            or wr != mn_row["rest"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor": w.get("xor"),
                "wr": wr,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_s += w["n_s"]
        n_t += w["n_t"]
        rows[str(k)] = {
            "xor": w["xor"],
            "xor_s": w["xor_s"],
            "xor_t": w["xor_t"],
            "xor_jgtn": w["xor_jgtn"],
            "rest": wr,
            "proxy": wp,
            "n_s": w["n_s"],
            "n_sg": w["n_sg"],
            "n_t": w["n_t"],
            "n_tg": w["n_tg"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor"] == want_rest10(k, 10) for k in range(0, 9))
        and rows["8"]["xor"] == 1
        and rows["8"]["proxy"] == 0
        and rows["8"]["xor_s"] == 1
        and rows["8"]["xor_t"] == 0
        and rows["2"]["xor"] == 1
        and rows["2"]["xor_s"] == 0
        and rows["2"]["xor_t"] == 1
        and rows["2"]["n_t"] == 1
        and rows["2"]["n_tg"] == 1
        and rows["6"]["xor_s"] == 1
        and rows["8"]["n_s"] == 8895
        and want_proxy(8) == 0
        and want_rest10(8, 10) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "n_t": n_t,
        "rows": rows,
    }


def killed_eq_proxy(q10: dict) -> dict:
    """green rest equals MN proxy: k=8 is 1 vs 0."""
    r = q10["rows"]["8"]
    ok = r["xor"] == 1 and r["proxy"] == 0
    return {"ok": ok, "k": 8, "q": 10, "xor": r["xor"], "proxy": r["proxy"]}


def killed_eq_jgtn(q10: dict) -> dict:
    """green rest equals jgtn: k=0 is 0 vs 1."""
    r = q10["rows"]["0"]
    ok = r["xor"] == 0 and r["xor_jgtn"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor": r["xor"], "xor_jgtn": r["xor_jgtn"]}


def killed_eq_d31(q10: dict) -> dict:
    """green rest equals Green d31: k=0 is 0 vs 1."""
    r = q10["rows"]["0"]
    ok = r["xor"] == 0 and want_d31(0) == 1
    return {"ok": ok, "k": 0, "q": 10, "xor": r["xor"], "d31": 1}


def killed_zero(q10: dict) -> dict:
    """green rest vanishes on q=10: k=2 is 1."""
    r = q10["rows"]["2"]
    ok = r["xor"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor": r["xor"]}


def killed_empty(q10: dict) -> dict:
    """n<U/2 pal-right empty: k=2 has n_t=1."""
    r = q10["rows"]["2"]
    ok = r["n_t"] == 1 and r["xor_t"] == 1
    return {"ok": ok, "k": 2, "q": 10, "n_t": r["n_t"]}


def killed_q6() -> dict:
    """green rest form on q=6: k=2 xor=1 but rest=0."""
    w = _walk_green_rest(2, 6)
    wr = want_rest10(2, 6)
    ok = w.get("ok") and w["xor"] == 1 and wr == 0 and w["n_t"] == 1
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor": w.get("xor"),
        "rest": wr,
        "n_t": w.get("n_t"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def prefixes() -> dict:
    mn = json.loads(MN_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    mz = json.loads(MZ_JSON.read_text())
    ok = (
        mn["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mz["checks"]["all_ok"]
        and mn["verdict"]["proxy_k8"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mz["verdict"]["inner_par"] == "LEMMA"
        and mn["verdict"]["prize"] == "unsolved"
        and want_proxy(8) == 0
        and want_rest10(8, 10) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kp: dict,
    kj: dict,
    kd: dict,
    kz: dict,
    kemp: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kp["ok"]
        and kj["ok"]
        and kd["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    j10_ok = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == j10_ok
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_green_rest()
    kp = killed_eq_proxy(q10)
    kj = killed_eq_jgtn(q10)
    kd = killed_eq_d31(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kp, kj, kd, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_green_rest": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_proxy": {k: kp[k] for k in kp if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_d31": {k: kd[k] for k in kd if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "green_rest": True,
            "proxy_k8": True,
            "inner_par": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_proxy": False,
            "eq_jgtn": False,
            "eq_d31": False,
            "green_rest_zero": False,
            "nlt_empty": False,
            "q6_rest": False,
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
            "green_rest": "LEMMA",
            "proxy_k8": "LEMMA",
            "inner_par": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_proxy": "KILLED",
            "eq_jgtn": "KILLED",
            "eq_d31": "KILLED",
            "green_rest_zero": "KILLED",
            "nlt_empty": "KILLED",
            "q6_rest": "KILLED",
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
        "q10_green_rest n_ok",
        dump["q10_green_rest"]["n_ok"],
        "n_g1",
        dump["q10_green_rest"]["n_g1"],
        "n_s",
        dump["q10_green_rest"]["n_s"],
        "n_t",
        dump["q10_green_rest"]["n_t"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_proxy", dump["killed_eq_proxy"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_eq_d31", dump["killed_eq_d31"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
