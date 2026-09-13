#!/usr/bin/env python3
"""Cycle NJ: on q=10 for k<=8, NA's S on n>=7U/2 is 1 iff k%8 in (5, 6).

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n>=7U/2 (p=T-2j>=0; no packed
row) is 1 iff k%8 in (5, 6). Far-high companion of Cycle NE's
n>=3U/2 form (k%8 in (4, 6)). Not NE high (k=5: 1 vs 0); not
rest (k=5: 1 vs 0); not NA S (k=5: 1 vs 0); not NH 2U-3U (k=6:
1 vs 0); not NI 2U-5U/2 (k=5: 1 vs 0); not T (k=5: 1 vs 0); not
0; not empty (k=3 n_hi72=3); not the form on q=6 (empty, k=5
xor=0 want=1); not Green-only rest; not the form for all k. Do
not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nj.py --certify
Dump: research/cycle_nj.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
NI_JSON = Path(__file__).resolve().parent / "cycle_ni.json"
NH_JSON = Path(__file__).resolve().parent / "cycle_nh.json"
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_s_hi72(k: int) -> int:
    """S on n>=7U/2 on q=10 k<=8: 1 iff k%8 in (5, 6)."""
    return int(k % 8 in (5, 6))


def _walk_s_hi72(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with n>=7U/2; also hi/23/lo25/sall."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half3 = (3 * U) // 2
    twoU, five2, threeU, seven2 = 2 * U, (5 * U) // 2, 3 * U, (7 * U) // 2
    n_ok = n_g1 = n_hi72 = n_hi72g = n_23 = n_lo = 0
    xor_hi72 = xor_hi = xor_23 = xor_lo = xor_sall = xor_jgtn = 0
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
                    n_23 += 1
                if twoU <= n < five2:
                    xor_lo ^= jp1
                    n_lo += 1
                if n >= seven2:
                    xor_hi72 ^= jp1
                    n_hi72 += 1
                    n_hi72g += jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hi72": n_hi72,
        "n_hi72g": n_hi72g,
        "n_23": n_23,
        "n_lo": n_lo,
        "xor_hi72": xor_hi72,
        "xor_hi": xor_hi,
        "xor_23": xor_23,
        "xor_lo": xor_lo,
        "xor_sall": xor_sall,
        "xor_jgtn": xor_jgtn,
    }


def q10_s_hi72() -> dict:
    """k<=8 q=10: S on n>=7U/2 is 1 iff k%8 in (5, 6)."""
    n_ok = n_g1 = n_hi72 = n_hi72g = 0
    rows = {}
    ni = json.loads(NI_JSON.read_text())
    nh = json.loads(NH_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_s_hi72(k, 10)
        want = want_s_hi72(k)
        ni_row = ni["q10_s_2u25"]["rows"][str(k)]
        nh_row = nh["q10_s_2u3u"]["rows"][str(k)]
        ne_row = ne["q10_s_hi"]["rows"][str(k)]
        na_row = na["q10_green_rest"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_hi72"] != want
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
                "xor_hi72": w.get("xor_hi72"),
                "want": want,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_hi72 += w["n_hi72"]
        n_hi72g += w["n_hi72g"]
        rows[str(k)] = {
            "xor_hi72": w["xor_hi72"],
            "xor_hi": w["xor_hi"],
            "xor_23": w["xor_23"],
            "xor_lo": w["xor_lo"],
            "xor_sall": w["xor_sall"],
            "xor_t": na_row["xor_t"],
            "want": want,
            "rest": want_rest10(k, 10),
            "n_hi72": w["n_hi72"],
            "n_hi72g": w["n_hi72g"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_hi72"] == want_s_hi72(k) for k in range(0, 9))
        and rows["3"]["n_hi72"] == 3
        and rows["3"]["xor_hi72"] == 0
        and rows["5"]["xor_hi72"] == 1
        and rows["5"]["n_hi72"] == 31
        and rows["5"]["n_hi72g"] == 7
        and rows["6"]["xor_hi72"] == 1
        and rows["6"]["n_hi72"] == 76
        and rows["6"]["xor_23"] == 0
        and rows["8"]["xor_hi72"] == 0
        and rows["8"]["n_hi72"] == 874
        and want_s_hi72(5) == 1
        and want_s_hi72(6) == 1
        and want_s_hi72(4) == 0
        and want_s_hi(4) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hi72": n_hi72,
        "n_hi72g": n_hi72g,
        "rows": rows,
    }


def killed_eq_hi(q10: dict) -> dict:
    """n>=7U/2 S equals NE high: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_hi": r["xor_hi"]}


def killed_eq_rest(q10: dict) -> dict:
    """n>=7U/2 S equals rest: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "rest": r["rest"]}


def killed_eq_s(q10: dict) -> dict:
    """n>=7U/2 S equals NA S: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_sall": r["xor_sall"]}


def killed_eq_23(q10: dict) -> dict:
    """n>=7U/2 S equals NH 2U-3U: k=6 is 1 vs 0."""
    r = q10["rows"]["6"]
    ok = r["xor_hi72"] == 1 and r["xor_23"] == 0
    return {"ok": ok, "k": 6, "q": 10, "xor_hi72": r["xor_hi72"], "xor_23": r["xor_23"]}


def killed_eq_lo(q10: dict) -> dict:
    """n>=7U/2 S equals NI 2U-5U/2: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_lo"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_lo": r["xor_lo"]}


def killed_eq_t(q10: dict) -> dict:
    """n>=7U/2 S equals T: k=5 is 1 vs 0."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_t": r["xor_t"]}


def killed_zero(q10: dict) -> dict:
    """n>=7U/2 S vanishes: k=5 is 1."""
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"]}


def killed_empty(q10: dict) -> dict:
    """n>=7U/2 S empty: k=3 has n_hi72=3."""
    r = q10["rows"]["3"]
    ok = r["n_hi72"] == 3 and r["xor_hi72"] == 0
    return {"ok": ok, "k": 3, "q": 10, "n_hi72": r["n_hi72"]}


def killed_q6() -> dict:
    """n>=7U/2 S form on q=6: empty, k=5 xor=0 want=1."""
    w = _walk_s_hi72(5, 6)
    ok = w.get("ok") and w["xor_hi72"] == 0 and w["n_hi72"] == 0 and want_s_hi72(5) == 1
    return {
        "ok": ok,
        "k": 5,
        "q": 6,
        "xor_hi72": w.get("xor_hi72"),
        "want": want_s_hi72(5),
        "n_hi72": w.get("n_hi72"),
    }


def prefixes() -> dict:
    ni = json.loads(NI_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        ni["checks"]["all_ok"]
        and ne["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and ni["verdict"]["s_2u25"] == "LEMMA"
        and ne["verdict"]["s_hi"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and ni["verdict"]["prize"] == "unsolved"
        and want_s_hi72(5) == 1
        and want_s_hi72(6) == 1
        and want_s_hi72(4) == 0
        and want_s_hi(4) == 1
        and want_s_2u25(2) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kh: dict,
    kr: dict,
    ks: dict,
    k23: dict,
    klo: dict,
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
        and kh["ok"]
        and kr["ok"]
        and ks["ok"]
        and k23["ok"]
        and klo["ok"]
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
    q10 = q10_s_hi72()
    kh = killed_eq_hi(q10)
    kr = killed_eq_rest(q10)
    ks = killed_eq_s(q10)
    k23 = killed_eq_23(q10)
    klo = killed_eq_lo(q10)
    kt = killed_eq_t(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kh, kr, ks, k23, klo, kt, kz, kemp, kq6, sc, pref
    )
    dump = {
        "cycle": "NJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_hi72": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_23": {k: k23[k] for k in k23 if k != "ok"},
        "killed_eq_lo": {k: klo[k] for k in klo if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_hi72": True,
            "s_2u25": True,
            "s_2u3u": True,
            "s_hi": True,
            "green_rest": True,
            "eq_hi": False,
            "eq_rest": False,
            "eq_s": False,
            "eq_23": False,
            "eq_lo": False,
            "eq_t": False,
            "s_hi72_zero": False,
            "nhi72_empty": False,
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
            "s_hi72": "LEMMA",
            "s_2u25": "LEMMA",
            "s_2u3u": "LEMMA",
            "s_hi": "LEMMA",
            "green_rest": "LEMMA",
            "eq_hi": "KILLED",
            "eq_rest": "KILLED",
            "eq_s": "KILLED",
            "eq_23": "KILLED",
            "eq_lo": "KILLED",
            "eq_t": "KILLED",
            "s_hi72_zero": "KILLED",
            "nhi72_empty": "KILLED",
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
        "q10_s_hi72 n_ok",
        dump["q10_s_hi72"]["n_ok"],
        "n_g1",
        dump["q10_s_hi72"]["n_g1"],
        "n_hi72",
        dump["q10_s_hi72"]["n_hi72"],
        "n_hi72g",
        dump["q10_s_hi72"]["n_hi72g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_23", dump["killed_eq_23"])
    print("killed_eq_lo", dump["killed_eq_lo"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
