#!/usr/bin/env python3
"""Cycle NQ: both q through k<=10, T-cell d%3==1 G(j+1) is 1 iff k>2 and k even.

On covering J6,J10 through k<=10, XOR of G(n,j+1) over palindrome-right
G=1 cells with n<U/2 and (j-n)%3==1 (p=T-2j>=0; no packed row) is 1
iff k>2 and k is even. Prefix NN n_t / xor_jp1 and NP xor_odd for
k<=8; walk k=9 and k=10 on q=10. Not a death at k=9 (xor=0=want);
not a death at k=10 (xor=1=want); not NN jp1 (k=3: 0 vs 1); not NP
vanish (k=4: 1 vs 0); not T (k=4: 1 vs 0); not outer T (k=4: 1 vs
0); not rest (k=4 q=10: 1 vs 0); not NO outer jp1 (k=3: 0 vs 1);
not 0; not 1; not empty (k=2 n_d31=1); not pointwise 0 (k=4
n_d31g=1); not dies on q=6; not T-cell d%3==0 as a standalone
cycle (same xor); not T-cell d%3==2 as a standalone cycle; not the
form for all k. Do not claim T is 1 iff k=2; do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nq.py --certify
Dump: research/cycle_nq.json
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
from cycle_nf import want_t_outer
from cycle_nn import want_t_jp1
from cycle_no import want_t_jp1_out
from cycle_np import want_t_odd_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
NN_JSON = Path(__file__).resolve().parent / "cycle_nn.json"
NP_JSON = Path(__file__).resolve().parent / "cycle_np.json"
NO_JSON = Path(__file__).resolve().parent / "cycle_no.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_t": 6912,
        "n_d31": 2111,
        "n_d31g": 760,
        "xor_d31": 0,
        "xor_d30": 0,
        "xor_jp1": 1,
        "xor_odd": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_t": 22528,
        "n_d31": 7780,
        "n_d31g": 2573,
        "xor_d31": 1,
        "xor_d30": 1,
        "xor_jp1": 1,
        "xor_odd": 0,
    },
}


def want_t_d31_jp1(k: int) -> int:
    """T-cell pal-right d%3==1 G(j+1) both q: 1 iff k>2 and k even."""
    return int(k > 2 and k % 2 == 0)


def _walk_t_d31_jp1(k: int, q: int) -> dict:
    """Pal-right n<U/2 d%3==1 xor of G(j+1); also d30 and NN/NP."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half = U // 2
    n_ok = n_g1 = n_t = n_d31 = n_d31g = n_d30 = 0
    xor_jp1 = xor_odd = xor_d31 = xor_d30 = xor_d32 = xor_t = xor_jgtn = 0
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
            jp1 = G(n, j + 1)
            jm1 = G(n, j - 1)
            xor_t ^= jm1
            xor_jp1 ^= jp1
            n_t += 1
            d = j - n
            if d % 2 == 1:
                xor_odd ^= jp1
            r = d % 3
            if r == 1:
                xor_d31 ^= jp1
                n_d31 += 1
                n_d31g += jp1
            elif r == 0:
                xor_d30 ^= jp1
                n_d30 += 1
            else:
                xor_d32 ^= jp1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_t": n_t,
        "n_d31": n_d31,
        "n_d31g": n_d31g,
        "n_d30": n_d30,
        "xor_d31": xor_d31,
        "xor_d30": xor_d30,
        "xor_d32": xor_d32,
        "xor_jp1": xor_jp1,
        "xor_odd": xor_odd,
        "xor_t": xor_t,
        "xor_jgtn": xor_jgtn,
    }


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_t"] == want["n_t"]
        and w["n_d31"] == want["n_d31"]
        and w["n_d31g"] == want["n_d31g"]
        and w["xor_d31"] == want["xor_d31"] == want_t_d31_jp1(k)
        and w["xor_d30"] == want["xor_d30"] == want_t_d31_jp1(k)
        and w["xor_jp1"] == want["xor_jp1"] == want_t_jp1(k)
        and w["xor_odd"] == want["xor_odd"] == want_t_odd_jp1(k)
        and w["xor_d31"] ^ w["xor_d30"] ^ w["xor_d32"] == w["xor_jp1"]
    )


def bothq_t_d31_jp1() -> dict:
    n_ok = n_g1 = n_d31 = n_d31g = 0
    rows = {}
    nn = json.loads(NN_JSON.read_text())
    np_ = json.loads(NP_JSON.read_text())
    no = json.loads(NO_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        want = want_t_d31_jp1(k)
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_t_d31_jp1(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            nn_row = nn["bothq_t_jp1"]["rows"][str(k)][name]
            np_row = np_["bothq_t_odd_jp1"]["rows"][str(k)][name]
            if (
                not w.get("ok")
                or w["xor_d31"] != want
                or w["xor_d30"] != want
                or w["xor_jp1"] != want_t_jp1(k)
                or w["xor_jp1"] != nn_row["xor_jp1"]
                or w["xor_odd"] != want_t_odd_jp1(k)
                or w["xor_odd"] != np_row["xor_odd"]
                or w["xor_d31"] ^ w["xor_d30"] ^ w["xor_d32"] != w["xor_jp1"]
                or w["n_t"] != nn_row["n_t"]
                or w["xor_jgtn"] != want_jgtn(k)
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_d31": w.get("xor_d31"),
                    "want": want,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_d31 += w["n_d31"]
            n_d31g += w["n_d31g"]
            krow[name] = {
                "xor_d31": w["xor_d31"],
                "xor_d30": w["xor_d30"],
                "xor_d32": w["xor_d32"],
                "xor_jp1": w["xor_jp1"],
                "xor_odd": w["xor_odd"],
                "xor_t": w["xor_t"],
                "want": want,
                "rest": want_rest10(k, q),
                "n_d31": w["n_d31"],
                "n_d31g": w["n_d31g"],
                "n_d30": w["n_d30"],
                "n_t": w["n_t"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "src": "walk",
            }
        if (
            krow["j6"]["xor_d31"] != krow["j10"]["xor_d31"]
            or krow["j6"]["n_d31"] != krow["j10"]["n_d31"]
            or krow["j6"]["n_d31g"] != krow["j10"]["n_d31g"]
        ):
            return {"ok": False, "k": k, "q": "disagree"}
        rows[str(k)] = krow
    for k in (9, 10):
        w = _walk_t_d31_jp1(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_d31": w.get("xor_d31"),
                "want": want_t_d31_jp1(k),
                "n_ok": w.get("n_ok"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d31 += w["n_d31"]
        n_d31g += w["n_d31g"]
        rec = {
            "xor_d31": w["xor_d31"],
            "xor_d30": w["xor_d30"],
            "xor_d32": w["xor_d32"],
            "xor_jp1": w["xor_jp1"],
            "xor_odd": w["xor_odd"],
            "xor_t": w["xor_t"],
            "want": want_t_d31_jp1(k),
            "rest": want_rest10(k, 10),
            "n_d31": w["n_d31"],
            "n_d31g": w["n_d31g"],
            "n_d30": w["n_d30"],
            "n_t": w["n_t"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
        rows[str(k)] = {"j10": rec}
    ok = (
        all(rows[str(k)]["j10"]["xor_d31"] == want_t_d31_jp1(k) for k in range(0, 11))
        and all(rows[str(k)]["j6"]["xor_d31"] == want_t_d31_jp1(k) for k in range(0, 9))
        and rows["2"]["j10"]["n_d31"] == 1
        and rows["2"]["j10"]["n_d31g"] == 0
        and rows["2"]["j10"]["xor_d31"] == 0
        and rows["3"]["j10"]["xor_d31"] == 0
        and rows["3"]["j10"]["xor_jp1"] == 1
        and rows["4"]["j10"]["n_d31"] == 8
        and rows["4"]["j10"]["n_d31g"] == 1
        and rows["4"]["j10"]["xor_d31"] == 1
        and rows["6"]["j10"]["xor_d31"] == 1
        and rows["6"]["j10"]["n_d31"] == 76
        and rows["8"]["j10"]["n_d31"] == 760
        and rows["8"]["j10"]["n_d31g"] == 221
        and rows["9"]["j10"]["xor_d31"] == 0
        and rows["9"]["j10"]["n_d31"] == 2111
        and rows["9"]["j10"]["n_d31g"] == 760
        and rows["10"]["j10"]["xor_d31"] == 1
        and rows["10"]["j10"]["n_d31"] == 7780
        and rows["10"]["j10"]["n_d31g"] == 2573
        and want_t_d31_jp1(10) == 1
        and want_t_d31_jp1(9) == 0
        and want_t_d31_jp1(4) == 1
        and nn["checks"]["all_ok"]
        and np_["verdict"]["t_odd_jp1"] == "LEMMA"
        and no["verdict"]["t_jp1_out"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d31": n_d31,
        "n_d31g": n_d31g,
        "rows": rows,
    }


def killed_die_k9(qboth: dict) -> dict:
    r = qboth["rows"]["9"]["j10"]
    ok = r["xor_d31"] == 0 and r["want"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_d31": r["xor_d31"], "want": r["want"]}


def killed_die_k10(qboth: dict) -> dict:
    r = qboth["rows"]["10"]["j10"]
    ok = r["xor_d31"] == 1 and r["want"] == 1 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_d31": r["xor_d31"], "want": r["want"]}


def killed_eq_jp1(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_d31"] == 0 and r["xor_jp1"] == 1
    return {"ok": ok, "k": 3, "q": 10, "xor_d31": r["xor_d31"], "xor_jp1": r["xor_jp1"]}


def killed_eq_odd(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_d31"] == 1 and r["xor_odd"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_d31": r["xor_d31"], "xor_odd": r["xor_odd"]}


def killed_eq_t(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_d31"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_d31": r["xor_d31"], "xor_t": r["xor_t"]}


def killed_eq_outer(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_d31"] == 1 and want_t_jp1_out(4) == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_d31": r["xor_d31"]}


def killed_eq_rest(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_d31"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_d31": r["xor_d31"], "rest": r["rest"]}


def killed_eq_out_jp1(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_d31"] == 0 and want_t_jp1_out(3) == 1
    return {"ok": ok, "k": 3, "q": 10, "xor_d31": r["xor_d31"]}


def killed_zero(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_d31"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_d31": r["xor_d31"]}


def killed_one(qboth: dict) -> dict:
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor_d31"] == 0 and r["n_d31"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_d31": r["xor_d31"]}


def killed_empty(qboth: dict) -> dict:
    r = qboth["rows"]["2"]["j10"]
    ok = r["n_d31"] == 1 and r["n_d31g"] == 0
    return {"ok": ok, "k": 2, "q": 10, "n_d31": r["n_d31"]}


def killed_pointwise(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["n_d31g"] == 1 and r["n_d31"] == 8
    return {"ok": ok, "k": 4, "q": 10, "n_d31g": r["n_d31g"], "n_d31": r["n_d31"]}


def killed_q6_die(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j6"]
    ok = r["xor_d31"] == 1 and r["n_d31"] == 8
    return {"ok": ok, "k": 4, "q": 6, "xor_d31": r["xor_d31"]}


def prefixes() -> dict:
    nn = json.loads(NN_JSON.read_text())
    np_ = json.loads(NP_JSON.read_text())
    no = json.loads(NO_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nn["checks"]["all_ok"]
        and np_["checks"]["all_ok"]
        and no["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nn["verdict"]["t_jp1"] == "LEMMA"
        and np_["verdict"]["t_odd_jp1"] == "LEMMA"
        and no["verdict"]["t_jp1_out"] == "LEMMA"
        and nn["verdict"]["prize"] == "unsolved"
        and want_t_d31_jp1(4) == 1
        and want_t_d31_jp1(9) == 0
        and want_t_d31_jp1(10) == 1
        and want_t_jp1(3) == 1
        and want_t_odd_jp1(4) == 0
        and want_t_jp1_out(3) == 1
        and want_t_outer(2) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    qboth: dict,
    kd9: dict,
    kd10: dict,
    kj: dict,
    kodd: dict,
    kt: dict,
    ko: dict,
    kr: dict,
    kout: dict,
    kz: dict,
    kone: dict,
    kemp: dict,
    kpw: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        qboth["ok"]
        and kd9["ok"]
        and kd10["ok"]
        and kj["ok"]
        and kodd["ok"]
        and kt["ok"]
        and ko["ok"]
        and kr["ok"]
        and kout["ok"]
        and kz["ok"]
        and kone["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    both8 = sum(
        mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
        for k in range(0, 9)
        for name in ("j6", "j10")
    )
    assert qboth["n_ok"] == both8 + WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    qboth = bothq_t_d31_jp1()
    kd9 = killed_die_k9(qboth)
    kd10 = killed_die_k10(qboth)
    kj = killed_eq_jp1(qboth)
    kodd = killed_eq_odd(qboth)
    kt = killed_eq_t(qboth)
    ko = killed_eq_outer(qboth)
    kr = killed_eq_rest(qboth)
    kout = killed_eq_out_jp1(qboth)
    kz = killed_zero(qboth)
    kone = killed_one(qboth)
    kemp = killed_empty(qboth)
    kpw = killed_pointwise(qboth)
    kq6 = killed_q6_die(qboth)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20,
        qboth,
        kd9,
        kd10,
        kj,
        kodd,
        kt,
        ko,
        kr,
        kout,
        kz,
        kone,
        kemp,
        kpw,
        kq6,
        sc,
        pref,
    )
    dump = {
        "cycle": "NQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_t_d31_jp1": {k: qboth[k] for k in qboth if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_jp1": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_odd": {k: kodd[k] for k in kodd if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_outer": {k: ko[k] for k in ko if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_out_jp1": {k: kout[k] for k in kout if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_one": {k: kone[k] for k in kone if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6_die": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "t_d31_jp1": True,
            "t_jp1": True,
            "t_odd_jp1": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_jp1": False,
            "eq_odd": False,
            "eq_t": False,
            "eq_outer": False,
            "eq_rest": False,
            "eq_out_jp1": False,
            "t_d31_jp1_zero": False,
            "t_d31_jp1_one": False,
            "nd31_empty": False,
            "nd31_pointwise": False,
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
            "t_d31_jp1": "LEMMA",
            "t_jp1": "LEMMA",
            "t_odd_jp1": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_jp1": "KILLED",
            "eq_odd": "KILLED",
            "eq_t": "KILLED",
            "eq_outer": "KILLED",
            "eq_rest": "KILLED",
            "eq_out_jp1": "KILLED",
            "t_d31_jp1_zero": "KILLED",
            "t_d31_jp1_one": "KILLED",
            "nd31_empty": "KILLED",
            "nd31_pointwise": "KILLED",
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
        "bothq_t_d31_jp1 n_ok",
        dump["bothq_t_d31_jp1"]["n_ok"],
        "n_g1",
        dump["bothq_t_d31_jp1"]["n_g1"],
        "n_d31",
        dump["bothq_t_d31_jp1"]["n_d31"],
        "n_d31g",
        dump["bothq_t_d31_jp1"]["n_d31g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_eq_odd", dump["killed_eq_odd"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_eq_outer", dump["killed_eq_outer"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_out_jp1", dump["killed_eq_out_jp1"])
    print("killed_zero", dump["killed_zero"])
    print("killed_one", dump["killed_one"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6_die", dump["killed_q6_die"])


if __name__ == "__main__":
    main()
