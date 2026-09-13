#!/usr/bin/env python3
"""Cycle OF: on q=10 through k<=10, S on 3U/2<=n<2U is 1 iff k>0 and k%4 in (0, 3).

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 3U/2<=n<2U (p=T-2j>=0; no packed
row) is 1 iff k>0 and k%4 in (0, 3). Complementary low-high slice
of Cycle NY's n>=3U/2; disjoint from NH 2U-3U and NJ n>=7U/2.
Not a death at k=9 (xor=0=want); not a death at k=10 (xor=0=want);
not NY high (k=3: 1 vs 0); not NH 2U-3U (k=2: 0 vs 1); not NJ
n>=7U/2 (k=5: 0 vs 1); not rest (k=3: 1 vs 0); not OA n<U
(k=3: 1 vs 0); not empty (k=9 n_lohi=5315); not pointwise 0
(k=9 n_lohig=2522); not 0 (k=3: 1); not the form on q=6 (k=7
xor=0 want=1); not the form for all k. Do not claim T is 1 iff
k=2; do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_of.py --certify
Dump: research/cycle_of.json
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
from cycle_nc import want_s_nltu
from cycle_ne import want_s_hi
from cycle_nh import want_s_2u3u
from cycle_nj import want_s_hi72

OUT = Path(__file__).resolve().with_suffix(".json")
OE_JSON = Path(__file__).resolve().parent / "cycle_oe.json"
NY_JSON = Path(__file__).resolve().parent / "cycle_ny.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_lohi": 5315,
        "n_lohig": 2522,
        "xor_lohi": 0,
        "xor_hi": 0,
        "xor_23": 1,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_lohi": 19097,
        "n_lohig": 7496,
        "xor_lohi": 0,
        "xor_hi": 0,
        "xor_23": 1,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
}

WANT_K8 = {
    0: {"n_lohi": 0, "n_lohig": 0, "xor_lohi": 0},
    1: {"n_lohi": 0, "n_lohig": 0, "xor_lohi": 0},
    2: {"n_lohi": 1, "n_lohig": 0, "xor_lohi": 0},
    3: {"n_lohi": 1, "n_lohig": 1, "xor_lohi": 1},
    4: {"n_lohi": 13, "n_lohig": 1, "xor_lohi": 1},
    5: {"n_lohi": 31, "n_lohig": 18, "xor_lohi": 0},
    6: {"n_lohi": 157, "n_lohig": 40, "xor_lohi": 0},
    7: {"n_lohi": 443, "n_lohig": 223, "xor_lohi": 1},
    8: {"n_lohi": 1761, "n_lohig": 609, "xor_lohi": 1},
}


def want_s_lohi(k: int) -> int:
    """S on 3U/2<=n<2U on q=10 k<=10: 1 iff k>0 and k%4 in (0, 3)."""
    return int(k > 0 and k % 4 in (0, 3))


def _walk_s_lohi(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with 3U/2<=n<2U; also hi/23/nltu/sall."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half3, twoU = (3 * U) // 2, 2 * U
    n_ok = n_g1 = n_lohi = n_lohig = 0
    xor_lohi = xor_hi = xor_23 = xor_nltu = xor_sall = 0
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
            d = j - n
            if d % 3 == 1 and G(n, j - 1) == 0:
                jp1 = G(n, j + 1)
                xor_sall ^= jp1
                if n < U:
                    xor_nltu ^= jp1
                if n >= half3:
                    xor_hi ^= jp1
                if twoU <= n < 3 * U:
                    xor_23 ^= jp1
                if half3 <= n < twoU:
                    xor_lohi ^= jp1
                    n_lohi += 1
                    n_lohig += jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lohi": n_lohi,
        "n_lohig": n_lohig,
        "xor_lohi": xor_lohi,
        "xor_hi": xor_hi,
        "xor_23": xor_23,
        "xor_nltu": xor_nltu,
        "xor_sall": xor_sall,
    }


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_lohi"] == want["n_lohi"]
        and w["n_lohig"] == want["n_lohig"]
        and w["xor_lohi"] == want["xor_lohi"] == want_s_lohi(k)
        and w["xor_hi"] == want["xor_hi"] == want_s_hi(k)
        and w["xor_23"] == want["xor_23"] != want_s_2u3u(k)
        and w["xor_nltu"] == want["xor_nltu"] == want_s_nltu(k)
        and w["xor_sall"] == want["xor_sall"]
    )


def q10_s_lohi_10() -> dict:
    """q=10 k<=10: walk k<=8 and k=9,10; xor_lohi = want_s_lohi."""
    mj = json.loads(MJ_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_lohi = n_lohig = 0
    for k in range(0, 9):
        w = _walk_s_lohi(k, 10)
        wh = want_s_lohi(k)
        pk = WANT_K8[k]
        mj_n = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"]
        mj_g = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_g1"]
        if (
            not w.get("ok")
            or w["xor_lohi"] != wh == pk["xor_lohi"]
            or w["n_lohi"] != pk["n_lohi"]
            or w["n_lohig"] != pk["n_lohig"]
            or w["n_ok"] != mj_n
            or w["n_g1"] != mj_g
        ):
            return {"ok": False, "k": k, "q": 10, "xor_lohi": w.get("xor_lohi")}
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lohi += w["n_lohi"]
        n_lohig += w["n_lohig"]
        rows[str(k)] = {
            "xor_lohi": w["xor_lohi"],
            "xor_hi": w["xor_hi"],
            "xor_23": w["xor_23"],
            "xor_nltu": w["xor_nltu"],
            "xor_sall": w["xor_sall"],
            "want": wh,
            "rest": want_rest10(k, 10),
            "n_lohi": w["n_lohi"],
            "n_lohig": w["n_lohig"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    for k in (9, 10):
        w = _walk_s_lohi(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_lohi": w.get("xor_lohi"),
                "n_ok": w.get("n_ok"),
                "n_lohi": w.get("n_lohi"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lohi += w["n_lohi"]
        n_lohig += w["n_lohig"]
        rows[str(k)] = {
            "xor_lohi": w["xor_lohi"],
            "xor_hi": w["xor_hi"],
            "xor_23": w["xor_23"],
            "xor_nltu": w["xor_nltu"],
            "xor_sall": w["xor_sall"],
            "want": want_s_lohi(k),
            "rest": want_rest10(k, 10),
            "n_lohi": w["n_lohi"],
            "n_lohig": w["n_lohig"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_lohi"] == want_s_lohi(k) for k in range(0, 11))
        and rows["2"]["n_lohi"] == 1
        and rows["2"]["xor_lohi"] == 0
        and rows["2"]["xor_23"] == 1
        and rows["3"]["n_lohi"] == 1
        and rows["3"]["n_lohig"] == 1
        and rows["3"]["xor_lohi"] == 1
        and rows["3"]["xor_hi"] == 0
        and rows["8"]["n_lohi"] == 1761
        and rows["8"]["xor_lohi"] == 1
        and rows["9"]["xor_lohi"] == 0
        and rows["9"]["n_lohi"] == 5315
        and rows["9"]["n_lohig"] == 2522
        and rows["10"]["xor_lohi"] == 0
        and rows["10"]["n_lohi"] == 19097
        and rows["10"]["n_lohig"] == 7496
        and want_s_lohi(9) == 0
        and want_s_lohi(10) == 0
        and want_s_lohi(8) == 1
        and want_s_lohi(0) == 0
        and want_s_lohi(3) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lohi": n_lohi,
        "n_lohig": n_lohig,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_lohi"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_lohi": r["xor_lohi"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_lohi"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_lohi": r["xor_lohi"]}


def killed_eq_hi(q10: dict) -> dict:
    r = q10["rows"]["3"]
    ok = r["xor_lohi"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lohi": r["xor_lohi"], "xor_hi": r["xor_hi"]}


def killed_eq_23(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor_lohi"] == 0 and r["xor_23"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lohi": r["xor_lohi"], "xor_23": r["xor_23"]}


def killed_eq_hi72(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_lohi"] == 0 and want_s_hi72(5) == 1
    return {"ok": ok, "k": 5, "q": 10, "xor_lohi": r["xor_lohi"], "want_hi72": 1}


def killed_eq_nltu(q10: dict) -> dict:
    r = q10["rows"]["3"]
    ok = r["xor_lohi"] == 1 and r["xor_nltu"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lohi": r["xor_lohi"], "xor_nltu": r["xor_nltu"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["3"]
    ok = r["xor_lohi"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lohi": r["xor_lohi"], "rest": r["rest"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["3"]
    ok = r["xor_lohi"] == 1
    return {"ok": ok, "k": 3, "q": 10, "xor_lohi": r["xor_lohi"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_lohi"] == 5315
    return {"ok": ok, "k": 9, "q": 10, "n_lohi": r["n_lohi"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_lohig"] == 2522 and r["xor_lohi"] == 0
    return {"ok": ok, "k": 9, "q": 10, "n_lohig": r["n_lohig"]}


def killed_q6() -> dict:
    w = _walk_s_lohi(7, 6)
    ok = (
        w.get("ok")
        and w["xor_lohi"] == 0
        and want_s_lohi(7) == 1
        and w["n_lohi"] == 287
    )
    return {
        "ok": ok,
        "k": 7,
        "q": 6,
        "xor_lohi": w.get("xor_lohi"),
        "want": want_s_lohi(7),
        "n_lohi": w.get("n_lohi"),
    }


def prefixes() -> dict:
    oe = json.loads(OE_JSON.read_text())
    ny = json.loads(NY_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        oe["checks"]["all_ok"]
        and ny["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and oe["verdict"]["s_hi72_dies_k9"] == "LEMMA"
        and ny["verdict"]["s_hi_10"] == "LEMMA"
        and oe["verdict"]["prize"] == "unsolved"
        and want_s_lohi(3) == 1
        and want_s_hi(3) == 0
        and want_s_2u3u(2) == 1
        and want_rest10(3, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    khi: dict,
    k23: dict,
    k72: dict,
    kn: dict,
    kr: dict,
    kz: dict,
    kemp: dict,
    kpw: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kd9["ok"]
        and kd10["ok"]
        and khi["ok"]
        and k23["ok"]
        and k72["ok"]
        and kn["ok"]
        and kr["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    q10_8 = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == q10_8 + WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_s_lohi_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    khi = killed_eq_hi(q10)
    k23 = killed_eq_23(q10)
    k72 = killed_eq_hi72(q10)
    kn = killed_eq_nltu(q10)
    kr = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, khi, k23, k72, kn, kr, kz, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "OF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_lohi_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_hi": {k: khi[k] for k in khi if k != "ok"},
        "killed_eq_23": {k: k23[k] for k in k23 if k != "ok"},
        "killed_eq_hi72": {k: k72[k] for k in k72 if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_lohi_10": True,
            "s_hi_10": True,
            "s_hi72_dies_k9": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_hi": False,
            "eq_23": False,
            "eq_hi72": False,
            "eq_nltu": False,
            "eq_rest": False,
            "s_lohi_zero": False,
            "nlohi_empty": False,
            "nlohi_pointwise": False,
            "q6_lohi": False,
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
            "s_lohi_10": "LEMMA",
            "s_hi_10": "LEMMA",
            "s_hi72_dies_k9": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_hi": "KILLED",
            "eq_23": "KILLED",
            "eq_hi72": "KILLED",
            "eq_nltu": "KILLED",
            "eq_rest": "KILLED",
            "s_lohi_zero": "KILLED",
            "nlohi_empty": "KILLED",
            "nlohi_pointwise": "KILLED",
            "q6_lohi": "KILLED",
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
        "q10_s_lohi_10 n_ok",
        dump["q10_s_lohi_10"]["n_ok"],
        "n_g1",
        dump["q10_s_lohi_10"]["n_g1"],
        "n_lohi",
        dump["q10_s_lohi_10"]["n_lohi"],
        "n_lohig",
        dump["q10_s_lohi_10"]["n_lohig"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_23", dump["killed_eq_23"])
    print("killed_eq_hi72", dump["killed_eq_hi72"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
