#!/usr/bin/env python3
"""Cycle ND: on q=6 and q=10 for k<=8, NA's S on U<=n<3U/2 vanishes.

On covering J6,J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and U<=n<3U/2 (p=T-2j>=0; no packed
row) is 0. So Cycle NA's S on n>=U is the n>=3U/2 slice. Both
covering q agree on xor and on n_mid. Not rest (k=2 q=10: xor=0,
rest=1); not empty (k=2 n_mid=1); not pointwise 0 (k=4 n_midg=4);
not NC n<U (k=4: 0 vs 1); not NA S (k=6 q=10: 0 vs 1); not S on
n>=U (k=3 q=6: 0 vs 1); not Green-only rest; not the form for all
k. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nd.py --certify
Dump: research/cycle_nd.json
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
from cycle_nc import want_s_nltu

OUT = Path(__file__).resolve().with_suffix(".json")
NC_JSON = Path(__file__).resolve().parent / "cycle_nc.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def _walk_s_mid(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with U<=n<3U/2; also n<U and n>=3U/2."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_mid = n_midg = n_hi = n_hig = 0
    xor_mid = xor_hi = xor_nltu = xor_sall = xor_jgtn = 0
    t = 0
    s = t0 + 1
    half3 = (3 * U) // 2
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
                jp1 = G(n, j + 1)
                xor_sall ^= jp1
                if n < U:
                    xor_nltu ^= jp1
                elif n < half3:
                    n_mid += 1
                    xor_mid ^= jp1
                    n_midg += jp1
                else:
                    n_hi += 1
                    xor_hi ^= jp1
                    n_hig += jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_mid": n_mid,
        "n_midg": n_midg,
        "n_hi": n_hi,
        "n_hig": n_hig,
        "xor_mid": xor_mid,
        "xor_hi": xor_hi,
        "xor_nltu": xor_nltu,
        "xor_sall": xor_sall,
        "xor_jgtn": xor_jgtn,
    }


def bothq_s_mid() -> dict:
    """k<=8 both q: S on U<=n<3U/2 vanishes; q agree."""
    n_ok = n_g1 = n_mid = n_midg = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    nc = json.loads(NC_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_s_mid(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            nc_row = nc["bothq_s_nltu"]["rows"][str(k)][name]
            if (
                not w.get("ok")
                or w["xor_mid"] != 0
                or w["xor_nltu"] != want_s_nltu(k)
                or w["xor_nltu"] != nc_row["xor"]
                or w["xor_jgtn"] != want_jgtn(k)
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
                or w["xor_sall"] != w["xor_nltu"] ^ w["xor_hi"]
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_mid": w.get("xor_mid"),
                }
            if q == 10:
                na_row = na["q10_green_rest"]["rows"][str(k)]
                if w["xor_sall"] != na_row["xor_s"]:
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_sall": w.get("xor_sall"),
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_mid += w["n_mid"]
            n_midg += w["n_midg"]
            krow[name] = {
                "xor_mid": w["xor_mid"],
                "xor_hi": w["xor_hi"],
                "xor_nltu": w["xor_nltu"],
                "xor_sall": w["xor_sall"],
                "rest": want_rest10(k, q),
                "n_mid": w["n_mid"],
                "n_midg": w["n_midg"],
                "n_hi": w["n_hi"],
                "n_hig": w["n_hig"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        if (
            krow["j6"]["xor_mid"] != krow["j10"]["xor_mid"]
            or krow["j6"]["n_mid"] != krow["j10"]["n_mid"]
            or krow["j6"]["n_midg"] != krow["j10"]["n_midg"]
        ):
            return {"ok": False, "k": k, "q": "disagree"}
        rows[str(k)] = krow
    ok = (
        all(rows[str(k)]["j6"]["xor_mid"] == 0 for k in range(0, 9))
        and rows["2"]["j10"]["n_mid"] == 1
        and rows["2"]["j10"]["n_midg"] == 0
        and rows["4"]["j10"]["n_mid"] == 13
        and rows["4"]["j10"]["n_midg"] == 4
        and rows["8"]["j10"]["n_mid"] == 1389
        and rows["4"]["j10"]["xor_nltu"] == 1
        and rows["3"]["j6"]["xor_hi"] == 1
        and rows["6"]["j10"]["xor_sall"] == 1
        and want_s_nltu(4) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_mid": n_mid,
        "n_midg": n_midg,
        "rows": rows,
    }


def killed_eq_rest(qboth: dict) -> dict:
    """mid S equals rest: k=2 q=10 is 0 vs 1."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor_mid"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_mid": r["xor_mid"], "rest": r["rest"]}


def killed_empty(qboth: dict) -> dict:
    """mid S empty: k=2 has n_mid=1."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["n_mid"] == 1 and r["n_midg"] == 0
    return {"ok": ok, "k": 2, "q": 10, "n_mid": r["n_mid"]}


def killed_pointwise(qboth: dict) -> dict:
    """mid S pointwise 0: k=4 has n_midg=4."""
    r = qboth["rows"]["4"]["j10"]
    ok = r["n_midg"] == 4 and r["xor_mid"] == 0
    return {"ok": ok, "k": 4, "q": 10, "n_midg": r["n_midg"]}


def killed_eq_nltu(qboth: dict) -> dict:
    """mid S equals NC n<U: k=4 is 0 vs 1."""
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_mid"] == 0 and r["xor_nltu"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_mid": r["xor_mid"], "xor_nltu": r["xor_nltu"]}


def killed_eq_s(qboth: dict) -> dict:
    """mid S equals NA S: k=6 q=10 is 0 vs 1."""
    r = qboth["rows"]["6"]["j10"]
    ok = r["xor_mid"] == 0 and r["xor_sall"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor_mid": r["xor_mid"], "xor_sall": r["xor_sall"]}


def killed_eq_hi(qboth: dict) -> dict:
    """mid S equals S on n>=U: k=3 q=6 is 0 vs 1."""
    r = qboth["rows"]["3"]["j6"]
    ok = r["xor_mid"] == 0 and r["xor_hi"] == 1
    return {"ok": ok, "k": 3, "q": 6, "xor_mid": r["xor_mid"], "xor_hi": r["xor_hi"]}


def killed_q6_die(qboth: dict) -> dict:
    """mid vanish dies on q=6: k=4 xor=0 and n_mid=13."""
    r = qboth["rows"]["4"]["j6"]
    ok = r["xor_mid"] == 0 and r["n_mid"] == 13
    return {"ok": ok, "k": 4, "q": 6, "xor_mid": r["xor_mid"], "n_mid": r["n_mid"]}


def prefixes() -> dict:
    nc = json.loads(NC_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nc["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nc["verdict"]["s_nltu"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and nc["verdict"]["prize"] == "unsolved"
        and want_s_nltu(4) == 1
        and want_s_nltu(0) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    qboth: dict,
    kr: dict,
    kemp: dict,
    kp: dict,
    kn: dict,
    ks: dict,
    kh: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        qboth["ok"]
        and kr["ok"]
        and kemp["ok"]
        and kp["ok"]
        and kn["ok"]
        and ks["ok"]
        and kh["ok"]
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
    qboth = bothq_s_mid()
    kr = killed_eq_rest(qboth)
    kemp = killed_empty(qboth)
    kp = killed_pointwise(qboth)
    kn = killed_eq_nltu(qboth)
    ks = killed_eq_s(qboth)
    kh = killed_eq_hi(qboth)
    kq6 = killed_q6_die(qboth)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, qboth, kr, kemp, kp, kn, ks, kh, kq6, sc, pref)
    dump = {
        "cycle": "ND",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_s_mid": {k: qboth[k] for k in qboth if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kp[k] for k in kp if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_q6_die": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_mid": True,
            "s_nltu": True,
            "green_rest": True,
            "jgtn_even": True,
            "eq_rest": False,
            "nmid_empty": False,
            "pointwise": False,
            "eq_nltu": False,
            "eq_s": False,
            "eq_hi": False,
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
            "s_mid": "LEMMA",
            "s_nltu": "LEMMA",
            "green_rest": "LEMMA",
            "jgtn_even": "LEMMA",
            "eq_rest": "KILLED",
            "nmid_empty": "KILLED",
            "pointwise": "KILLED",
            "eq_nltu": "KILLED",
            "eq_s": "KILLED",
            "eq_hi": "KILLED",
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
        "bothq_s_mid n_ok",
        dump["bothq_s_mid"]["n_ok"],
        "n_g1",
        dump["bothq_s_mid"]["n_g1"],
        "n_mid",
        dump["bothq_s_mid"]["n_mid"],
        "n_midg",
        dump["bothq_s_mid"]["n_midg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_q6_die", dump["killed_q6_die"])


if __name__ == "__main__":
    main()
