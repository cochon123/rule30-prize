#!/usr/bin/env python3
"""Cycle NH: on q=10 for k<=8, NA's S on 2U<=n<3U is 1 iff k%3==2.

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 2U<=n<3U (p=T-2j>=0; no packed
row) is 1 iff k%3==2. Same modulus as Cycle NF's outer T; a
different slice. Not rest (k=5: xor=1, rest=0); not NE high
(k=2: 1 vs 0); not NA S (k=2: 1 vs 0); not NC n<U (k=2: 1 vs 0);
not T (k=5: 1 vs 0); not 0; not empty (k=1 n_23=1); not the form
on q=6 (empty, k=2 xor=0 want=1); not Green-only rest; not the
form for all k. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_nh.py --certify
Dump: research/cycle_nh.json
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
from cycle_ne import want_s_hi
from cycle_nf import want_t_outer

OUT = Path(__file__).resolve().with_suffix(".json")
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
NC_JSON = Path(__file__).resolve().parent / "cycle_nc.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_s_2u3u(k: int) -> int:
    """S on 2U<=n<3U on q=10 k<=8: 1 iff k%3==2."""
    return int(k % 3 == 2)


def _walk_s_2u3u(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with 2U<=n<3U; also hi/nltu/sall."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half3 = (3 * U) // 2
    twoU, threeU = 2 * U, 3 * U
    n_ok = n_g1 = n_23 = n_23g = n_hi = 0
    xor_23 = xor_hi = xor_nltu = xor_sall = xor_mid = xor_jgtn = 0
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
                jp1 = G(n, j + 1)
                xor_sall ^= jp1
                if n < U:
                    xor_nltu ^= jp1
                elif n < half3:
                    xor_mid ^= jp1
                else:
                    xor_hi ^= jp1
                    n_hi += 1
                if twoU <= n < threeU:
                    xor_23 ^= jp1
                    n_23 += 1
                    n_23g += jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_23": n_23,
        "n_23g": n_23g,
        "n_hi": n_hi,
        "xor_23": xor_23,
        "xor_hi": xor_hi,
        "xor_nltu": xor_nltu,
        "xor_sall": xor_sall,
        "xor_mid": xor_mid,
        "xor_jgtn": xor_jgtn,
    }


def q10_s_2u3u() -> dict:
    """k<=8 q=10: S on 2U<=n<3U is 1 iff k%3==2."""
    n_ok = n_g1 = n_23 = n_23g = 0
    rows = {}
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    nc = json.loads(NC_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_s_2u3u(k, 10)
        want = want_s_2u3u(k)
        ne_row = ne["q10_s_hi"]["rows"][str(k)]
        nc_row = nc["bothq_s_nltu"]["rows"][str(k)]["j10"]
        na_row = na["q10_green_rest"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_23"] != want
            or w["xor_hi"] != want_s_hi(k)
            or w["xor_hi"] != ne_row["xor_hi"]
            or w["n_hi"] != ne_row["n_hi"]
            or w["xor_nltu"] != want_s_nltu(k)
            or w["xor_nltu"] != nc_row["xor"]
            or w["xor_sall"] != na_row["xor_s"]
            or w["xor_mid"] != 0
            or w["xor_jgtn"] != want_jgtn(k)
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_23": w.get("xor_23"),
                "want": want,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_23 += w["n_23"]
        n_23g += w["n_23g"]
        rows[str(k)] = {
            "xor_23": w["xor_23"],
            "xor_hi": w["xor_hi"],
            "xor_nltu": w["xor_nltu"],
            "xor_sall": w["xor_sall"],
            "xor_t": na_row["xor_t"],
            "xor_mid": w["xor_mid"],
            "want": want,
            "rest": want_rest10(k, 10),
            "n_23": w["n_23"],
            "n_23g": w["n_23g"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_23"] == want_s_2u3u(k) for k in range(0, 9))
        and rows["2"]["xor_23"] == 1
        and rows["2"]["n_23"] == 2
        and rows["2"]["n_23g"] == 1
        and rows["5"]["xor_23"] == 1
        and rows["5"]["xor_sall"] == 0
        and rows["5"]["n_23"] == 103
        and rows["8"]["xor_23"] == 1
        and rows["8"]["n_23"] == 3216
        and rows["1"]["n_23"] == 1
        and rows["1"]["xor_23"] == 0
        and want_s_2u3u(2) == 1
        and want_s_2u3u(5) == 1
        and want_t_outer(2) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_23": n_23,
        "n_23g": n_23g,
        "rows": rows,
    }


def killed_eq_rest(q10: dict) -> dict:
    """2U<=n<3U S equals rest: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_23"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_23": r["xor_23"], "rest": r["rest"]}


def killed_eq_hi(q10: dict) -> dict:
    """2U<=n<3U S equals NE high: k=2 is 1 vs 0."""
    r = q10["rows"]["2"]
    ok = r["xor_23"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_23": r["xor_23"], "xor_hi": r["xor_hi"]}


def killed_eq_s(q10: dict) -> dict:
    """2U<=n<3U S equals NA S: k=2 is 1 vs 0."""
    r = q10["rows"]["2"]
    ok = r["xor_23"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_23": r["xor_23"], "xor_sall": r["xor_sall"]}


def killed_eq_nltu(q10: dict) -> dict:
    """2U<=n<3U S equals NC n<U: k=2 is 1 vs 0."""
    r = q10["rows"]["2"]
    ok = r["xor_23"] == 1 and r["xor_nltu"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_23": r["xor_23"], "xor_nltu": r["xor_nltu"]}


def killed_eq_t(q10: dict) -> dict:
    """2U<=n<3U S equals T: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_23"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_23": r["xor_23"], "xor_t": r["xor_t"]}


def killed_zero(q10: dict) -> dict:
    """2U<=n<3U S vanishes: k=2 is 1."""
    r = q10["rows"]["2"]
    ok = r["xor_23"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_23": r["xor_23"]}


def killed_empty(q10: dict) -> dict:
    """2U<=n<3U S empty: k=1 has n_23=1."""
    r = q10["rows"]["1"]
    ok = r["n_23"] == 1 and r["xor_23"] == 0
    return {"ok": ok, "k": 1, "q": 10, "n_23": r["n_23"]}


def killed_q6() -> dict:
    """2U<=n<3U S form on q=6: empty, k=2 xor=0 want=1."""
    w = _walk_s_2u3u(2, 6)
    ok = w.get("ok") and w["xor_23"] == 0 and w["n_23"] == 0 and want_s_2u3u(2) == 1
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor_23": w.get("xor_23"),
        "want": want_s_2u3u(2),
        "n_23": w.get("n_23"),
    }


def prefixes() -> dict:
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        ne["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and ne["verdict"]["s_hi"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and ne["verdict"]["prize"] == "unsolved"
        and want_s_2u3u(2) == 1
        and want_s_2u3u(3) == 0
        and want_s_2u3u(5) == 1
        and want_t_outer(2) == 1
        and want_s_hi(4) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kr: dict,
    kh: dict,
    ks: dict,
    kn: dict,
    kt: dict,
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
        and kr["ok"]
        and kh["ok"]
        and ks["ok"]
        and kn["ok"]
        and kt["ok"]
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
    q10 = q10_s_2u3u()
    kr = killed_eq_rest(q10)
    kh = killed_eq_hi(q10)
    ks = killed_eq_s(q10)
    kn = killed_eq_nltu(q10)
    kt = killed_eq_t(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kr, kh, ks, kn, kt, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_2u3u": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_2u3u": True,
            "s_hi": True,
            "green_rest": True,
            "jgtn_even": True,
            "eq_rest": False,
            "eq_hi": False,
            "eq_s": False,
            "eq_nltu": False,
            "eq_t": False,
            "s_2u3u_zero": False,
            "n23_empty": False,
            "q6_form": False,
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
            "s_2u3u": "LEMMA",
            "s_hi": "LEMMA",
            "green_rest": "LEMMA",
            "jgtn_even": "LEMMA",
            "eq_rest": "KILLED",
            "eq_hi": "KILLED",
            "eq_s": "KILLED",
            "eq_nltu": "KILLED",
            "eq_t": "KILLED",
            "s_2u3u_zero": "KILLED",
            "n23_empty": "KILLED",
            "q6_form": "KILLED",
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
        "q10_s_2u3u n_ok",
        dump["q10_s_2u3u"]["n_ok"],
        "n_g1",
        dump["q10_s_2u3u"]["n_g1"],
        "n_23",
        dump["q10_s_2u3u"]["n_23"],
        "n_23g",
        dump["q10_s_2u3u"]["n_23g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
