#!/usr/bin/env python3
"""Cycle NL: on q=10 for k<=8, NA's S on 2U<=n<9U/4 vanishes.

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 2U<=n<9U/4 (p=T-2j>=0; no packed
row) is 0. Lower quarter of Cycle NI's 2U<=n<5U/2 band, so NI's
xor lives in [9U/4, 5U/2). Not NI (k=2: 0 vs 1); not rest (k=2:
0 vs 1); not NE high (k=4: 0 vs 1); not NJ (k=5: 0 vs 1); not NH
(k=2: 0 vs 1); not NA S (k=6: 0 vs 1); not T (k=2: 0 vs 1); not
empty (k=3 n_lo9=1); not pointwise 0 (k=4 n_lo9g=2); not the form
on q=6 (empty, k=4 n_lo9=0 vs q=10 n_lo9=3); not Green-only rest;
not the form for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_nl.py --certify
Dump: research/cycle_nl.json
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
from cycle_ne import want_s_hi
from cycle_nh import want_s_2u3u
from cycle_ni import want_s_2u25
from cycle_nj import want_s_hi72

OUT = Path(__file__).resolve().with_suffix(".json")
NI_JSON = Path(__file__).resolve().parent / "cycle_ni.json"
NH_JSON = Path(__file__).resolve().parent / "cycle_nh.json"
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
NJ_JSON = Path(__file__).resolve().parent / "cycle_nj.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def _walk_s_2u94(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with 2U<=n<9U/4; also NI lo and up."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half3 = (3 * U) // 2
    twoU, nine4, five2, threeU = 2 * U, (9 * U) // 4, (5 * U) // 2, 3 * U
    n_ok = n_g1 = n_lo9 = n_lo9g = n_lo = n_up = 0
    xor_lo9 = xor_up = xor_lo = xor_23 = xor_hi = xor_sall = xor_jgtn = 0
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
                if n >= half3:
                    xor_hi ^= jp1
                if twoU <= n < threeU:
                    xor_23 ^= jp1
                if twoU <= n < five2:
                    xor_lo ^= jp1
                    n_lo += 1
                    if n < nine4:
                        xor_lo9 ^= jp1
                        n_lo9 += 1
                        n_lo9g += jp1
                    else:
                        xor_up ^= jp1
                        n_up += 1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo9": n_lo9,
        "n_lo9g": n_lo9g,
        "n_lo": n_lo,
        "n_up": n_up,
        "xor_lo9": xor_lo9,
        "xor_up": xor_up,
        "xor_lo": xor_lo,
        "xor_23": xor_23,
        "xor_hi": xor_hi,
        "xor_sall": xor_sall,
        "xor_jgtn": xor_jgtn,
    }


def q10_s_2u94() -> dict:
    """k<=8 q=10: S on 2U<=n<9U/4 vanishes."""
    n_ok = n_g1 = n_lo9 = n_lo9g = 0
    rows = {}
    ni = json.loads(NI_JSON.read_text())
    nh = json.loads(NH_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    nj = json.loads(NJ_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_s_2u94(k, 10)
        ni_row = ni["q10_s_2u25"]["rows"][str(k)]
        nh_row = nh["q10_s_2u3u"]["rows"][str(k)]
        ne_row = ne["q10_s_hi"]["rows"][str(k)]
        na_row = na["q10_green_rest"]["rows"][str(k)]
        nj_row = nj["q10_s_hi72"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_lo9"] != 0
            or w["xor_lo9"] ^ w["xor_up"] != w["xor_lo"]
            or w["xor_lo"] != want_s_2u25(k)
            or w["xor_lo"] != ni_row["xor_lo"]
            or w["n_lo"] != ni_row["n_lo"]
            or w["xor_23"] != want_s_2u3u(k)
            or w["xor_23"] != nh_row["xor_23"]
            or w["xor_hi"] != want_s_hi(k)
            or w["xor_hi"] != ne_row["xor_hi"]
            or w["xor_sall"] != na_row["xor_s"]
            or w["xor_jgtn"] != want_jgtn(k)
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_lo9": w.get("xor_lo9"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo9 += w["n_lo9"]
        n_lo9g += w["n_lo9g"]
        rows[str(k)] = {
            "xor_lo9": w["xor_lo9"],
            "xor_up": w["xor_up"],
            "xor_lo": w["xor_lo"],
            "xor_23": w["xor_23"],
            "xor_hi": w["xor_hi"],
            "xor_sall": w["xor_sall"],
            "xor_hi72": nj_row["xor_hi72"],
            "xor_t": na_row["xor_t"],
            "rest": want_rest10(k, 10),
            "n_lo9": w["n_lo9"],
            "n_lo9g": w["n_lo9g"],
            "n_lo": w["n_lo"],
            "n_up": w["n_up"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_lo9"] == 0 for k in range(0, 9))
        and rows["2"]["n_lo9"] == 0
        and rows["2"]["xor_lo"] == 1
        and rows["2"]["xor_up"] == 1
        and rows["3"]["n_lo9"] == 1
        and rows["3"]["n_lo9g"] == 0
        and rows["4"]["n_lo9"] == 3
        and rows["4"]["n_lo9g"] == 2
        and rows["6"]["xor_lo"] == 1
        and rows["6"]["n_lo9"] == 35
        and rows["8"]["n_lo9"] == 389
        and rows["8"]["n_lo9g"] == 200
        and rows["8"]["n_lo"] == 1319
        and want_s_2u25(2) == 1
        and want_s_hi(4) == 1
        and want_s_hi72(5) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo9": n_lo9,
        "n_lo9g": n_lo9g,
        "rows": rows,
    }


def killed_eq_ni(q10: dict) -> dict:
    """2U<=n<9U/4 S equals NI 2U-5U/2: k=2 is 0 vs 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo9"] == 0 and r["xor_lo"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo9": r["xor_lo9"], "xor_lo": r["xor_lo"]}


def killed_eq_rest(q10: dict) -> dict:
    """2U<=n<9U/4 S equals rest: k=2 is 0 vs 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo9"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo9": r["xor_lo9"], "rest": r["rest"]}


def killed_eq_hi(q10: dict) -> dict:
    """2U<=n<9U/4 S equals NE high: k=4 is 0 vs 1."""
    r = q10["rows"]["4"]
    ok = r["xor_lo9"] == 0 and r["xor_hi"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_lo9": r["xor_lo9"], "xor_hi": r["xor_hi"]}


def killed_eq_nj(q10: dict) -> dict:
    """2U<=n<9U/4 S equals NJ n>=7U/2: k=5 is 0 vs 1."""
    r = q10["rows"]["5"]
    ok = r["xor_lo9"] == 0 and r["xor_hi72"] == 1
    return {"ok": ok, "k": 5, "q": 10, "xor_lo9": r["xor_lo9"], "xor_hi72": r["xor_hi72"]}


def killed_eq_nh(q10: dict) -> dict:
    """2U<=n<9U/4 S equals NH 2U-3U: k=2 is 0 vs 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo9"] == 0 and r["xor_23"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo9": r["xor_lo9"], "xor_23": r["xor_23"]}


def killed_eq_s(q10: dict) -> dict:
    """2U<=n<9U/4 S equals NA S: k=6 is 0 vs 1."""
    r = q10["rows"]["6"]
    ok = r["xor_lo9"] == 0 and r["xor_sall"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor_lo9": r["xor_lo9"], "xor_sall": r["xor_sall"]}


def killed_eq_t(q10: dict) -> dict:
    """2U<=n<9U/4 S equals T: k=2 is 0 vs 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo9"] == 0 and r["xor_t"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo9": r["xor_lo9"], "xor_t": r["xor_t"]}


def killed_empty(q10: dict) -> dict:
    """2U<=n<9U/4 S empty: k=3 has n_lo9=1."""
    r = q10["rows"]["3"]
    ok = r["n_lo9"] == 1 and r["xor_lo9"] == 0
    return {"ok": ok, "k": 3, "q": 10, "n_lo9": r["n_lo9"]}


def killed_pointwise(q10: dict) -> dict:
    """2U<=n<9U/4 S pointwise 0: k=4 has n_lo9g=2."""
    r = q10["rows"]["4"]
    ok = r["n_lo9g"] == 2 and r["n_lo9"] == 3
    return {"ok": ok, "k": 4, "q": 10, "n_lo9g": r["n_lo9g"], "n_lo9": r["n_lo9"]}


def killed_q6() -> dict:
    """2U<=n<9U/4 S vanish on q=6 as a non-empty census: empty, k=4 n_lo9=0."""
    w = _walk_s_2u94(4, 6)
    ok = w.get("ok") and w["xor_lo9"] == 0 and w["n_lo9"] == 0
    return {
        "ok": ok,
        "k": 4,
        "q": 6,
        "xor_lo9": w.get("xor_lo9"),
        "n_lo9": w.get("n_lo9"),
    }


def prefixes() -> dict:
    ni = json.loads(NI_JSON.read_text())
    nk = json.loads(Path(__file__).resolve().parent.joinpath("cycle_nk.json").read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        ni["checks"]["all_ok"]
        and nk["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and ni["verdict"]["s_2u25"] == "LEMMA"
        and nk["verdict"]["s_2u25_10"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and ni["verdict"]["prize"] == "unsolved"
        and want_s_2u25(2) == 1
        and want_s_2u25(10) == 1
        and want_s_hi(4) == 1
        and want_s_hi72(5) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kni: dict,
    kr: dict,
    kh: dict,
    knj: dict,
    knh: dict,
    ks: dict,
    kt: dict,
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
        and kni["ok"]
        and kr["ok"]
        and kh["ok"]
        and knj["ok"]
        and knh["ok"]
        and ks["ok"]
        and kt["ok"]
        and kemp["ok"]
        and kpw["ok"]
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
    q10 = q10_s_2u94()
    kni = killed_eq_ni(q10)
    kr = killed_eq_rest(q10)
    kh = killed_eq_hi(q10)
    knj = killed_eq_nj(q10)
    knh = killed_eq_nh(q10)
    ks = killed_eq_s(q10)
    kt = killed_eq_t(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kni, kr, kh, knj, knh, ks, kt, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "NL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_2u94": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_ni": {k: kni[k] for k in kni if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_eq_nj": {k: knj[k] for k in knj if k != "ok"},
        "killed_eq_nh": {k: knh[k] for k in knh if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_2u94": True,
            "s_2u25_10": True,
            "s_2u25": True,
            "eq_ni": False,
            "eq_rest": False,
            "eq_hi": False,
            "eq_nj": False,
            "eq_nh": False,
            "eq_s": False,
            "eq_t": False,
            "nlo9_empty": False,
            "nlo9_pointwise": False,
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
            "s_2u94": "LEMMA",
            "s_2u25_10": "LEMMA",
            "s_2u25": "LEMMA",
            "eq_ni": "KILLED",
            "eq_rest": "KILLED",
            "eq_hi": "KILLED",
            "eq_nj": "KILLED",
            "eq_nh": "KILLED",
            "eq_s": "KILLED",
            "eq_t": "KILLED",
            "nlo9_empty": "KILLED",
            "nlo9_pointwise": "KILLED",
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
        "q10_s_2u94 n_ok",
        dump["q10_s_2u94"]["n_ok"],
        "n_g1",
        dump["q10_s_2u94"]["n_g1"],
        "n_lo9",
        dump["q10_s_2u94"]["n_lo9"],
        "n_lo9g",
        dump["q10_s_2u94"]["n_lo9g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_ni", dump["killed_eq_ni"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_nj", dump["killed_eq_nj"])
    print("killed_eq_nh", dump["killed_eq_nh"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
