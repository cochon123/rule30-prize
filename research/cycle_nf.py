#!/usr/bin/env python3
"""Cycle NF: on q=6 and q=10 for k<=8, outer NA T xor of G(n,j-1) is 1 iff k%3==2.

On covering J6,J10 for k<=8, XOR of G(n,j-1) over palindrome-right
G=1 cells with n<U/2 and j>n+n//2 (p=T-2j>=0; no packed row) is 1
iff k%3==2. Both covering q agree on xor and on n_outer. This is
the outer slice of Cycle NA's T; not T (k=5: xor=1, T=0); not rest
(k=5 q=10: 1 vs 0); not inner T (k=2: 1 vs 0); not 0; not empty
(k=2 n_outer=1); not Green-only rest; not the form for all k. Do
not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nf.py --certify
Dump: research/cycle_nf.json
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
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_t_outer(k: int) -> int:
    """outer pal-right n<U/2 xor of G(n,j-1) both q k<=8: 1 iff k%3==2."""
    return int(k % 3 == 2)


def _walk_t_outer(k: int, q: int) -> dict:
    """Pal-right n<U/2 xor of G(j-1) split inner/outer."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half = U // 2
    n_ok = n_g1 = n_t = n_tg = n_out = n_outg = n_in = n_ing = 0
    xor_t = xor_out = xor_in = xor_jgtn = 0
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
            if n >= half:
                continue
            jm1 = G(n, j - 1)
            xor_t ^= jm1
            n_t += 1
            n_tg += jm1
            if j > n + n // 2:
                xor_out ^= jm1
                n_out += 1
                n_outg += jm1
            else:
                xor_in ^= jm1
                n_in += 1
                n_ing += jm1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_t": n_t,
        "n_tg": n_tg,
        "n_out": n_out,
        "n_outg": n_outg,
        "n_in": n_in,
        "n_ing": n_ing,
        "xor_t": xor_t,
        "xor_out": xor_out,
        "xor_in": xor_in,
        "xor_jgtn": xor_jgtn,
    }


def bothq_t_outer() -> dict:
    """k<=8 both q: outer T xor is 1 iff k%3==2; q agree."""
    n_ok = n_g1 = n_out = n_outg = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        want = want_t_outer(k)
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_t_outer(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            if (
                not w.get("ok")
                or w["xor_out"] != want
                or w["xor_t"] != w["xor_in"] ^ w["xor_out"]
                or w["xor_jgtn"] != want_jgtn(k)
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_out": w.get("xor_out"),
                    "want": want,
                }
            if q == 10:
                na_row = na["q10_green_rest"]["rows"][str(k)]
                if w["xor_t"] != na_row["xor_t"] or w["n_t"] != na_row["n_t"]:
                    return {
                        "ok": False,
                        "k": k,
                        "q": 10,
                        "xor_t": w.get("xor_t"),
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_out += w["n_out"]
            n_outg += w["n_outg"]
            krow[name] = {
                "xor_out": w["xor_out"],
                "xor_in": w["xor_in"],
                "xor_t": w["xor_t"],
                "want": want,
                "rest": want_rest10(k, q),
                "n_out": w["n_out"],
                "n_outg": w["n_outg"],
                "n_in": w["n_in"],
                "n_t": w["n_t"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        if (
            krow["j6"]["xor_out"] != krow["j10"]["xor_out"]
            or krow["j6"]["n_out"] != krow["j10"]["n_out"]
            or krow["j6"]["n_outg"] != krow["j10"]["n_outg"]
        ):
            return {"ok": False, "k": k, "q": "disagree"}
        rows[str(k)] = krow
    ok = (
        all(
            rows[str(k)]["j6"]["xor_out"] == want_t_outer(k)
            and rows[str(k)]["j10"]["xor_out"] == want_t_outer(k)
            for k in range(0, 9)
        )
        and rows["2"]["j10"]["xor_out"] == 1
        and rows["2"]["j10"]["n_out"] == 1
        and rows["2"]["j10"]["xor_t"] == 1
        and rows["5"]["j10"]["xor_out"] == 1
        and rows["5"]["j10"]["xor_t"] == 0
        and rows["5"]["j10"]["n_out"] == 41
        and rows["8"]["j10"]["xor_out"] == 1
        and rows["8"]["j10"]["n_out"] == 1333
        and want_t_outer(2) == 1
        and want_t_outer(3) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_outg": n_outg,
        "rows": rows,
    }


def killed_eq_t(qboth: dict) -> dict:
    """outer T equals T: k=5 is 1 vs 0."""
    r = qboth["rows"]["5"]["j10"]
    ok = r["xor_out"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_out": r["xor_out"], "xor_t": r["xor_t"]}


def killed_eq_rest(qboth: dict) -> dict:
    """outer T equals rest: k=5 q=10 is 1 vs 0."""
    r = qboth["rows"]["5"]["j10"]
    ok = r["xor_out"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_out": r["xor_out"], "rest": r["rest"]}


def killed_eq_inner(qboth: dict) -> dict:
    """outer T equals inner T: k=2 is 1 vs 0."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor_out"] == 1 and r["xor_in"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_out": r["xor_out"], "xor_in": r["xor_in"]}


def killed_zero(qboth: dict) -> dict:
    """outer T vanishes: k=2 is 1."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor_out"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_out": r["xor_out"]}


def killed_empty(qboth: dict) -> dict:
    """outer T empty: k=2 has n_out=1."""
    r = qboth["rows"]["2"]["j10"]
    ok = r["n_out"] == 1 and r["n_outg"] == 1
    return {"ok": ok, "k": 2, "q": 10, "n_out": r["n_out"]}


def killed_q6_die(qboth: dict) -> dict:
    """outer form dies on q=6: k=2 xor=1 equals want."""
    r = qboth["rows"]["2"]["j6"]
    ok = r["xor_out"] == 1 and want_t_outer(2) == 1
    return {"ok": ok, "k": 2, "q": 6, "xor_out": r["xor_out"]}


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
        and want_t_outer(2) == 1
        and want_t_outer(5) == 1
        and want_t_outer(8) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    qboth: dict,
    kt: dict,
    kr: dict,
    ki: dict,
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
        and kt["ok"]
        and kr["ok"]
        and ki["ok"]
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
    qboth = bothq_t_outer()
    kt = killed_eq_t(qboth)
    kr = killed_eq_rest(qboth)
    ki = killed_eq_inner(qboth)
    kz = killed_zero(qboth)
    kemp = killed_empty(qboth)
    kq6 = killed_q6_die(qboth)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, qboth, kt, kr, ki, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_t_outer": {k: qboth[k] for k in qboth if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_inner": {k: ki[k] for k in ki if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6_die": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "t_outer": True,
            "s_hi": True,
            "green_rest": True,
            "jgtn_even": True,
            "eq_t": False,
            "eq_rest": False,
            "eq_inner": False,
            "t_outer_zero": False,
            "nout_empty": False,
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
            "t_outer": "LEMMA",
            "s_hi": "LEMMA",
            "green_rest": "LEMMA",
            "jgtn_even": "LEMMA",
            "eq_t": "KILLED",
            "eq_rest": "KILLED",
            "eq_inner": "KILLED",
            "t_outer_zero": "KILLED",
            "nout_empty": "KILLED",
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
        "bothq_t_outer n_ok",
        dump["bothq_t_outer"]["n_ok"],
        "n_g1",
        dump["bothq_t_outer"]["n_g1"],
        "n_out",
        dump["bothq_t_outer"]["n_out"],
        "n_outg",
        dump["bothq_t_outer"]["n_outg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_inner", dump["killed_eq_inner"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6_die", dump["killed_q6_die"])


if __name__ == "__main__":
    main()
