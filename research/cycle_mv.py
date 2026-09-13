#!/usr/bin/env python3
"""Cycle MV: on q=6 and q=10 for k<=8, inner palindrome-right even-d xor of G(n,j+1) vanishes.

On covering J6,J10 for k<=8, XOR of G(n,j+1) over covering G=1
cells with n<j<=n+n//2 and (j-n) even (p=T-2j>=0; no packed row)
is 0. Dual of Cycle MK's inner G(j-1) vanish (q=10 only): Cycle
MU's k-odd even-d G(j+1) on q=6 is the outer even-d slice. Not
rest (k=2 q=10: xor=0, rest=1); not empty (k=2 q=10 n_ine=5);
not pointwise 0 (k=2 q=10 n_gjp1=2); not MU even-d G(j+1)
(k=3 q=6: 0 vs 1); not MK inner G(j-1) (k=3 q=6 jm1=1);
not Green-only rest; not the form for all k. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mv.py --certify
Dump: research/cycle_mv.json
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
from cycle_mu import want_even_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
MU_JSON = Path(__file__).resolve().parent / "cycle_mu.json"
MK_JSON = Path(__file__).resolve().parent / "cycle_mk.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def _walk_inner_even_jp1(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j+1) on inner even d; also inner G(j-1)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_in = n_ine = n_gjp1 = n_even = 0
    xor_ine = xor_in_jm1 = xor_even_jp1 = 0
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
            if d % 2 == 0:
                n_even += 1
                xor_even_jp1 ^= G(n, j + 1)
            if d <= n // 2:
                n_in += 1
                xor_in_jm1 ^= G(n, j - 1)
                if d % 2 == 0:
                    n_ine += 1
                    xor_ine ^= G(n, j + 1)
                    n_gjp1 += G(n, j + 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_in": n_in,
        "n_ine": n_ine,
        "n_gjp1": n_gjp1,
        "n_even": n_even,
        "xor_ine": xor_ine,
        "xor_in_jm1": xor_in_jm1,
        "xor_even_jp1": xor_even_jp1,
    }


def bothq_inner_even() -> dict:
    """k<=8 both q: inner even-d G(j+1) xor vanishes."""
    n_ok = n_g1 = n_ine = n_gjp1 = 0
    rows = {}
    mu = json.loads(MU_JSON.read_text())
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_inner_even_jp1(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            if (
                not w.get("ok")
                or w["xor_ine"] != 0
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_ine": w.get("xor_ine"),
                }
            if q == 6:
                mu_row = mu["q6_even_jp1"]["rows"][str(k)]
                if (
                    w["xor_even_jp1"] != want_even_jp1(k)
                    or w["xor_even_jp1"] != mu_row["xor_jp1"]
                    or w["n_even"] != mu_row["n_even"]
                    or w["n_ok"] != mu_row["n_ok"]
                    or w["n_g1"] != mu_row["n_g1"]
                ):
                    return {
                        "ok": False,
                        "k": k,
                        "q": 6,
                        "xor_even_jp1": w.get("xor_even_jp1"),
                    }
            else:
                mk_row = mk["q10_inner0"]["rows"][str(k)]
                if (
                    w["xor_in_jm1"] != 0
                    or w["xor_in_jm1"] != mk_row["xor_in"]
                    or w["n_in"] != mk_row["n_in"]
                    or w["n_ok"] != mk_row["n_ok"]
                    or w["n_g1"] != mk_row["n_g1"]
                ):
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_in_jm1": w.get("xor_in_jm1"),
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_ine += w["n_ine"]
            n_gjp1 += w["n_gjp1"]
            krow[name] = {
                "xor_ine": w["xor_ine"],
                "xor_in_jm1": w["xor_in_jm1"],
                "xor_even_jp1": w["xor_even_jp1"],
                "n_ine": w["n_ine"],
                "n_gjp1": w["n_gjp1"],
                "n_in": w["n_in"],
                "n_even": w["n_even"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        rows[str(k)] = krow
    ok = (
        all(
            rows[str(k)][name]["xor_ine"] == 0
            for k in range(0, 9)
            for name in ("j6", "j10")
        )
        and rows["2"]["j10"]["n_ine"] == 5
        and rows["2"]["j10"]["n_gjp1"] == 2
        and rows["3"]["j6"]["n_ine"] == 6
        and rows["3"]["j6"]["n_gjp1"] == 2
        and rows["8"]["j10"]["n_ine"] == 14617
        and rows["3"]["j6"]["xor_in_jm1"] == 1
        and rows["3"]["j6"]["xor_even_jp1"] == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ine": n_ine,
        "n_gjp1": n_gjp1,
        "rows": rows,
    }


def killed_eq_rest(both: dict) -> dict:
    """inner even-d G(j+1) xor equals rest: k=2 q=10 is 0 vs 1."""
    r = both["rows"]["2"]["j10"]
    wr = want_rest10(2, 10)
    ok = r["xor_ine"] == 0 and wr == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_ine": r["xor_ine"], "rest": wr}


def killed_empty(both: dict) -> dict:
    """inner even-d G=1 empty: k=2 q=10 has n_ine=5."""
    r = both["rows"]["2"]["j10"]
    ok = r["n_ine"] == 5 and r["xor_ine"] == 0
    return {"ok": ok, "k": 2, "q": 10, "n_ine": r["n_ine"]}


def killed_pointwise(both: dict) -> dict:
    """inner even-d G(j+1) pointwise 0: k=2 q=10 has n_gjp1=2."""
    r = both["rows"]["2"]["j10"]
    ok = r["n_gjp1"] == 2 and r["xor_ine"] == 0
    return {"ok": ok, "k": 2, "q": 10, "n_gjp1": r["n_gjp1"]}


def killed_eq_mu(both: dict) -> dict:
    """inner even-d G(j+1) equals MU even-d: k=3 q=6 is 0 vs 1."""
    r = both["rows"]["3"]["j6"]
    wj = want_even_jp1(3)
    ok = r["xor_ine"] == 0 and r["xor_even_jp1"] == 1 and wj == 1
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_ine": r["xor_ine"],
        "xor_even_jp1": r["xor_even_jp1"],
    }


def killed_eq_mk(both: dict) -> dict:
    """inner even-d G(j+1) equals MK inner G(j-1): k=3 q=6 jp1=0 jm1=1."""
    r = both["rows"]["3"]["j6"]
    ok = r["xor_ine"] == 0 and r["xor_in_jm1"] == 1
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_ine": r["xor_ine"],
        "xor_in_jm1": r["xor_in_jm1"],
    }


def prefixes() -> dict:
    mu = json.loads(MU_JSON.read_text())
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mu["checks"]["all_ok"]
        and mk["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mu["verdict"]["even_jp1"] == "LEMMA"
        and mk["verdict"]["inner0"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    both: dict,
    keq: dict,
    kemp: dict,
    kpw: dict,
    kmu: dict,
    kmk: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        both["ok"]
        and keq["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kmu["ok"]
        and kmk["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    assert both["n_ok"] == mj["bothq_jgtn"]["n_ok"]
    assert both["n_g1"] == mj["bothq_jgtn"]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    both = bothq_inner_even()
    keq = killed_eq_rest(both)
    kemp = killed_empty(both)
    kpw = killed_pointwise(both)
    kmu = killed_eq_mu(both)
    kmk = killed_eq_mk(both)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, both, keq, kemp, kpw, kmu, kmk, sc, pref)
    dump = {
        "cycle": "MV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_inner_even": {k: both[k] for k in both if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_eq_mu": {k: kmu[k] for k in kmu if k != "ok"},
        "killed_eq_mk": {k: kmk[k] for k in kmk if k != "ok"},
        "lemmas": {
            "inner_even_jp1": True,
            "even_jp1": True,
            "inner0": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "inner_even_empty": False,
            "inner_even_pointwise": False,
            "eq_mu": False,
            "eq_mk": False,
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
            "inner_even_jp1": "LEMMA",
            "even_jp1": "LEMMA",
            "inner0": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "inner_even_empty": "KILLED",
            "inner_even_pointwise": "KILLED",
            "eq_mu": "KILLED",
            "eq_mk": "KILLED",
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
    print(
        "bothq_inner_even n_ok",
        dump["bothq_inner_even"]["n_ok"],
        "n_g1",
        dump["bothq_inner_even"]["n_g1"],
        "n_ine",
        dump["bothq_inner_even"]["n_ine"],
        "n_gjp1",
        dump["bothq_inner_even"]["n_gjp1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_mu", dump["killed_eq_mu"])
    print("killed_eq_mk", dump["killed_eq_mk"])


if __name__ == "__main__":
    main()
