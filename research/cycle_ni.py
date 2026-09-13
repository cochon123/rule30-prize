#!/usr/bin/env python3
"""Cycle NI: on q=10 for k<=8, NA's S on 2U<=n<5U/2 is 1 iff k%4 in (2, 3).

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 2U<=n<5U/2 (p=T-2j>=0; no packed
row) is 1 iff k%4 in (2, 3). Lower half of Cycle NH's 2U<=n<3U
band. Not NH (k=3: 1 vs 0); not rest (k=3: 1 vs 0); not NE high
(k=2: 1 vs 0); not NA S (k=2: 1 vs 0); not T (k=3: 1 vs 0); not
0; not empty (k=1 n_lo=1); not the form on q=6 (empty, k=2 xor=0
want=1); not Green-only rest; not the form for all k. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ni.py --certify
Dump: research/cycle_ni.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
NH_JSON = Path(__file__).resolve().parent / "cycle_nh.json"
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_s_2u25(k: int) -> int:
    """S on 2U<=n<5U/2 on q=10 k<=8: 1 iff k%4 in (2, 3)."""
    return int(k % 4 in (2, 3))


def _walk_s_2u25(k: int, q: int) -> dict:
    """Pal-right d31 G(j+1) on jm1=0 with 2U<=n<5U/2; also 2U-3U and hi."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half3 = (3 * U) // 2
    twoU, five2, threeU = 2 * U, (5 * U) // 2, 3 * U
    n_ok = n_g1 = n_lo = n_log = n_23 = 0
    xor_lo = xor_hi25 = xor_23 = xor_hi = xor_sall = xor_jgtn = 0
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
                    if n < five2:
                        xor_lo ^= jp1
                        n_lo += 1
                        n_log += jp1
                    else:
                        xor_hi25 ^= jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_log": n_log,
        "n_23": n_23,
        "xor_lo": xor_lo,
        "xor_hi25": xor_hi25,
        "xor_23": xor_23,
        "xor_hi": xor_hi,
        "xor_sall": xor_sall,
        "xor_jgtn": xor_jgtn,
    }


def q10_s_2u25() -> dict:
    """k<=8 q=10: S on 2U<=n<5U/2 is 1 iff k%4 in (2, 3)."""
    n_ok = n_g1 = n_lo = n_log = 0
    rows = {}
    nh = json.loads(NH_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_s_2u25(k, 10)
        want = want_s_2u25(k)
        nh_row = nh["q10_s_2u3u"]["rows"][str(k)]
        ne_row = ne["q10_s_hi"]["rows"][str(k)]
        na_row = na["q10_green_rest"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_lo"] != want
            or w["xor_23"] != want_s_2u3u(k)
            or w["xor_23"] != nh_row["xor_23"]
            or w["n_23"] != nh_row["n_23"]
            or w["xor_lo"] ^ w["xor_hi25"] != w["xor_23"]
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
                "xor_lo": w.get("xor_lo"),
                "want": want,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        n_log += w["n_log"]
        rows[str(k)] = {
            "xor_lo": w["xor_lo"],
            "xor_hi25": w["xor_hi25"],
            "xor_23": w["xor_23"],
            "xor_hi": w["xor_hi"],
            "xor_sall": w["xor_sall"],
            "xor_t": na_row["xor_t"],
            "want": want,
            "rest": want_rest10(k, 10),
            "n_lo": w["n_lo"],
            "n_log": w["n_log"],
            "n_23": w["n_23"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_lo"] == want_s_2u25(k) for k in range(0, 9))
        and rows["1"]["n_lo"] == 1
        and rows["1"]["xor_lo"] == 0
        and rows["2"]["xor_lo"] == 1
        and rows["2"]["n_lo"] == 1
        and rows["2"]["n_log"] == 1
        and rows["3"]["xor_lo"] == 1
        and rows["3"]["xor_23"] == 0
        and rows["6"]["xor_lo"] == 1
        and rows["6"]["n_lo"] == 123
        and rows["8"]["xor_lo"] == 0
        and rows["8"]["n_lo"] == 1319
        and want_s_2u25(2) == 1
        and want_s_2u25(3) == 1
        and want_s_2u25(4) == 0
        and want_s_2u3u(2) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_log": n_log,
        "rows": rows,
    }


def killed_eq_23(q10: dict) -> dict:
    """2U<=n<5U/2 S equals NH 2U-3U: k=3 is 1 vs 0."""
    r = q10["rows"]["3"]
    ok = r["xor_lo"] == 1 and r["xor_23"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lo": r["xor_lo"], "xor_23": r["xor_23"]}


def killed_eq_rest(q10: dict) -> dict:
    """2U<=n<5U/2 S equals rest: k=3 is 1 vs 0."""
    r = q10["rows"]["3"]
    ok = r["xor_lo"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lo": r["xor_lo"], "rest": r["rest"]}


def killed_eq_hi(q10: dict) -> dict:
    """2U<=n<5U/2 S equals NE high: k=2 is 1 vs 0."""
    r = q10["rows"]["2"]
    ok = r["xor_lo"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_lo": r["xor_lo"], "xor_hi": r["xor_hi"]}


def killed_eq_s(q10: dict) -> dict:
    """2U<=n<5U/2 S equals NA S: k=2 is 1 vs 0."""
    r = q10["rows"]["2"]
    ok = r["xor_lo"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_lo": r["xor_lo"], "xor_sall": r["xor_sall"]}


def killed_eq_t(q10: dict) -> dict:
    """2U<=n<5U/2 S equals T: k=3 is 1 vs 0."""
    r = q10["rows"]["3"]
    ok = r["xor_lo"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_lo": r["xor_lo"], "xor_t": r["xor_t"]}


def killed_zero(q10: dict) -> dict:
    """2U<=n<5U/2 S vanishes: k=2 is 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo": r["xor_lo"]}


def killed_empty(q10: dict) -> dict:
    """2U<=n<5U/2 S empty: k=1 has n_lo=1."""
    r = q10["rows"]["1"]
    ok = r["n_lo"] == 1 and r["xor_lo"] == 0
    return {"ok": ok, "k": 1, "q": 10, "n_lo": r["n_lo"]}


def killed_q6() -> dict:
    """2U<=n<5U/2 S form on q=6: empty, k=2 xor=0 want=1."""
    w = _walk_s_2u25(2, 6)
    ok = w.get("ok") and w["xor_lo"] == 0 and w["n_lo"] == 0 and want_s_2u25(2) == 1
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor_lo": w.get("xor_lo"),
        "want": want_s_2u25(2),
        "n_lo": w.get("n_lo"),
    }


def prefixes() -> dict:
    nh = json.loads(NH_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nh["checks"]["all_ok"]
        and ne["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nh["verdict"]["s_2u3u"] == "LEMMA"
        and ne["verdict"]["s_hi"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and nh["verdict"]["prize"] == "unsolved"
        and want_s_2u25(2) == 1
        and want_s_2u25(3) == 1
        and want_s_2u25(4) == 0
        and want_s_2u3u(2) == 1
        and want_s_hi(4) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    k23: dict,
    kr: dict,
    kh: dict,
    ks: dict,
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
        and k23["ok"]
        and kr["ok"]
        and kh["ok"]
        and ks["ok"]
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
    q10 = q10_s_2u25()
    k23 = killed_eq_23(q10)
    kr = killed_eq_rest(q10)
    kh = killed_eq_hi(q10)
    ks = killed_eq_s(q10)
    kt = killed_eq_t(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, k23, kr, kh, ks, kt, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_2u25": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_23": {k: k23[k] for k in k23 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_2u25": True,
            "s_2u3u": True,
            "s_hi": True,
            "green_rest": True,
            "eq_23": False,
            "eq_rest": False,
            "eq_hi": False,
            "eq_s": False,
            "eq_t": False,
            "s_2u25_zero": False,
            "nlo_empty": False,
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
            "s_2u25": "LEMMA",
            "s_2u3u": "LEMMA",
            "s_hi": "LEMMA",
            "green_rest": "LEMMA",
            "eq_23": "KILLED",
            "eq_rest": "KILLED",
            "eq_hi": "KILLED",
            "eq_s": "KILLED",
            "eq_t": "KILLED",
            "s_2u25_zero": "KILLED",
            "nlo_empty": "KILLED",
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
        "q10_s_2u25 n_ok",
        dump["q10_s_2u25"]["n_ok"],
        "n_g1",
        dump["q10_s_2u25"]["n_g1"],
        "n_lo",
        dump["q10_s_2u25"]["n_lo"],
        "n_log",
        dump["q10_s_2u25"]["n_log"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_23", dump["killed_eq_23"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
