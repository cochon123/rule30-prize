#!/usr/bin/env python3
"""Cycle NO: both q through k<=10, outer T-cell G(j+1) is 1 iff k>0 and k%3==0.

On covering J6,J10 through k<=10, XOR of G(n,j+1) over palindrome-right
G=1 cells with n<U/2 and j>n+n//2 (p=T-2j>=0; no packed row) is 1
iff k>0 and k%3==0. Outer slice of Cycle NN's T-cell G(j+1); companion
modulus of Cycle NF's outer G(j-1) (k%3==2). Prefix NF n_out and NN
xor_jp1 for k<=8; walk k=9 and k=10 on q=10. Not a death at k=9
(xor=1=want); not a death at k=10 (xor=0=want); not NN jp1 (k=4: 0 vs
1); not T (k=3: 1 vs 0); not outer T (k=3: 1 vs 0); not inner T
(k=3: 1 vs 0); not rest (k=3 q=10: 1 vs 0); not 0; not 1; not empty
(k=2 n_out=1); not pointwise 0 (k=3 n_outg=1); not dies on q=6; not
the form for all k. Do not claim T is 1 iff k=2; do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_no.py --certify
Dump: research/cycle_no.json
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
from cycle_ng import want_t_inner
from cycle_nn import want_t_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
NN_JSON = Path(__file__).resolve().parent / "cycle_nn.json"
NF_JSON = Path(__file__).resolve().parent / "cycle_nf.json"
NG_JSON = Path(__file__).resolve().parent / "cycle_ng.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_t": 6912,
        "n_out": 4296,
        "n_outg": 1629,
        "n_in": 2616,
        "xor_out": 1,
        "xor_in": 0,
        "xor_jp1": 1,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_t": 22528,
        "n_out": 13873,
        "n_outg": 5280,
        "n_in": 8655,
        "xor_out": 0,
        "xor_in": 1,
        "xor_jp1": 1,
    },
}


def want_t_jp1_out(k: int) -> int:
    """outer pal-right G(j+1) on n<U/2 both q: 1 iff k>0 and k%3==0."""
    return int(k > 0 and k % 3 == 0)


def _walk_t_jp1_out(k: int, q: int) -> dict:
    """Pal-right n<U/2 outer/inner xor of G(j+1); also T G(j-1)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    half = U // 2
    n_ok = n_g1 = n_t = n_out = n_outg = n_in = 0
    xor_jp1 = xor_out = xor_in = xor_t = xor_jm1_out = xor_jm1_in = xor_jgtn = 0
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
            jp1 = G(n, j + 1)
            xor_t ^= jm1
            xor_jp1 ^= jp1
            n_t += 1
            if j > n + n // 2:
                xor_out ^= jp1
                xor_jm1_out ^= jm1
                n_out += 1
                n_outg += jp1
            else:
                xor_in ^= jp1
                xor_jm1_in ^= jm1
                n_in += 1
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_t": n_t,
        "n_out": n_out,
        "n_outg": n_outg,
        "n_in": n_in,
        "xor_jp1": xor_jp1,
        "xor_out": xor_out,
        "xor_in": xor_in,
        "xor_t": xor_t,
        "xor_jm1_out": xor_jm1_out,
        "xor_jm1_in": xor_jm1_in,
        "xor_jgtn": xor_jgtn,
    }


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_t"] == want["n_t"]
        and w["n_out"] == want["n_out"]
        and w["n_outg"] == want["n_outg"]
        and w["n_in"] == want["n_in"]
        and w["xor_out"] == want["xor_out"] == want_t_jp1_out(k)
        and w["xor_in"] == want["xor_in"]
        and w["xor_jp1"] == want["xor_jp1"] == want_t_jp1(k)
        and w["xor_out"] ^ w["xor_in"] == w["xor_jp1"]
        and w["xor_jm1_out"] == want_t_outer(k)
        and w["xor_jm1_in"] == want_t_inner(k)
    )


def bothq_t_jp1_out() -> dict:
    n_ok = n_g1 = n_out = n_outg = 0
    rows = {}
    nn = json.loads(NN_JSON.read_text())
    nf = json.loads(NF_JSON.read_text())
    ng = json.loads(NG_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        want = want_t_jp1_out(k)
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_t_jp1_out(k, q)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            nn_row = nn["bothq_t_jp1"]["rows"][str(k)][name]
            nf_row = nf["bothq_t_outer"]["rows"][str(k)][name]
            ng_row = ng["bothq_t_inner"]["rows"][str(k)][name]
            if (
                not w.get("ok")
                or w["xor_out"] != want
                or w["xor_jp1"] != want_t_jp1(k)
                or w["xor_jp1"] != nn_row["xor_jp1"]
                or w["xor_out"] ^ w["xor_in"] != w["xor_jp1"]
                or w["n_t"] != nn_row["n_t"]
                or w["n_out"] != nf_row["n_out"]
                or w["xor_jm1_out"] != want_t_outer(k)
                or w["xor_jm1_out"] != nf_row["xor_out"]
                or w["xor_jm1_in"] != want_t_inner(k)
                or w["xor_jm1_in"] != ng_row["xor_in"]
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
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_out += w["n_out"]
            n_outg += w["n_outg"]
            krow[name] = {
                "xor_out": w["xor_out"],
                "xor_in": w["xor_in"],
                "xor_jp1": w["xor_jp1"],
                "xor_t": w["xor_t"],
                "xor_jm1_out": w["xor_jm1_out"],
                "xor_jm1_in": w["xor_jm1_in"],
                "want": want,
                "rest": want_rest10(k, q),
                "n_out": w["n_out"],
                "n_outg": w["n_outg"],
                "n_in": w["n_in"],
                "n_t": w["n_t"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "src": "walk",
            }
        if (
            krow["j6"]["xor_out"] != krow["j10"]["xor_out"]
            or krow["j6"]["n_out"] != krow["j10"]["n_out"]
            or krow["j6"]["n_outg"] != krow["j10"]["n_outg"]
        ):
            return {"ok": False, "k": k, "q": "disagree"}
        rows[str(k)] = krow
    for k in (9, 10):
        w = _walk_t_jp1_out(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_out": w.get("xor_out"),
                "want": want_t_jp1_out(k),
                "n_ok": w.get("n_ok"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_out += w["n_out"]
        n_outg += w["n_outg"]
        rec = {
            "xor_out": w["xor_out"],
            "xor_in": w["xor_in"],
            "xor_jp1": w["xor_jp1"],
            "xor_t": w["xor_t"],
            "xor_jm1_out": w["xor_jm1_out"],
            "xor_jm1_in": w["xor_jm1_in"],
            "want": want_t_jp1_out(k),
            "rest": want_rest10(k, 10),
            "n_out": w["n_out"],
            "n_outg": w["n_outg"],
            "n_in": w["n_in"],
            "n_t": w["n_t"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
        rows[str(k)] = {"j10": rec}
    ok = (
        all(rows[str(k)]["j10"]["xor_out"] == want_t_jp1_out(k) for k in range(0, 11))
        and all(rows[str(k)]["j6"]["xor_out"] == want_t_jp1_out(k) for k in range(0, 9))
        and rows["2"]["j10"]["n_out"] == 1
        and rows["2"]["j10"]["n_outg"] == 0
        and rows["2"]["j10"]["xor_out"] == 0
        and rows["3"]["j10"]["n_out"] == 4
        and rows["3"]["j10"]["n_outg"] == 1
        and rows["3"]["j10"]["xor_out"] == 1
        and rows["6"]["j10"]["xor_out"] == 1
        and rows["6"]["j10"]["n_out"] == 130
        and rows["8"]["j10"]["n_out"] == 1333
        and rows["8"]["j10"]["n_outg"] == 502
        and rows["9"]["j10"]["xor_out"] == 1
        and rows["9"]["j10"]["n_out"] == 4296
        and rows["10"]["j10"]["xor_out"] == 0
        and rows["10"]["j10"]["n_out"] == 13873
        and want_t_jp1_out(3) == 1
        and want_t_jp1_out(9) == 1
        and want_t_jp1_out(2) == 0
        and want_t_jp1(10) == 1
        and nn["checks"]["all_ok"]
        and nn["verdict"]["t_jp1"] == "LEMMA"
        and nf["verdict"]["t_outer"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_outg": n_outg,
        "rows": rows,
    }


def killed_die_k9(qboth: dict) -> dict:
    r = qboth["rows"]["9"]["j10"]
    ok = r["xor_out"] == 1 and r["want"] == 1 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"], "want": r["want"]}


def killed_die_k10(qboth: dict) -> dict:
    r = qboth["rows"]["10"]["j10"]
    ok = r["xor_out"] == 0 and r["want"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_out": r["xor_out"], "want": r["want"]}


def killed_eq_jp1(qboth: dict) -> dict:
    r = qboth["rows"]["4"]["j10"]
    ok = r["xor_out"] == 0 and r["xor_jp1"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_out": r["xor_out"], "xor_jp1": r["xor_jp1"]}


def killed_eq_t(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_out"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_out": r["xor_out"], "xor_t": r["xor_t"]}


def killed_eq_outer(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_out"] == 1 and r["xor_jm1_out"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_out": r["xor_out"], "xor_jm1_out": r["xor_jm1_out"]}


def killed_eq_inner(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_out"] == 1 and r["xor_jm1_in"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_out": r["xor_out"], "xor_jm1_in": r["xor_jm1_in"]}


def killed_eq_rest(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_out"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 3, "q": 10, "xor_out": r["xor_out"], "rest": r["rest"]}


def killed_zero(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["xor_out"] == 1
    return {"ok": ok, "k": 3, "q": 10, "xor_out": r["xor_out"]}


def killed_one(qboth: dict) -> dict:
    r = qboth["rows"]["2"]["j10"]
    ok = r["xor_out"] == 0 and r["n_out"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_out": r["xor_out"]}


def killed_empty(qboth: dict) -> dict:
    r = qboth["rows"]["2"]["j10"]
    ok = r["n_out"] == 1 and r["n_outg"] == 0
    return {"ok": ok, "k": 2, "q": 10, "n_out": r["n_out"]}


def killed_pointwise(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j10"]
    ok = r["n_outg"] == 1 and r["n_out"] == 4
    return {"ok": ok, "k": 3, "q": 10, "n_outg": r["n_outg"], "n_out": r["n_out"]}


def killed_q6_die(qboth: dict) -> dict:
    r = qboth["rows"]["3"]["j6"]
    ok = r["xor_out"] == 1 and want_t_jp1_out(3) == 1 and r["n_out"] == 4
    return {"ok": ok, "k": 3, "q": 6, "xor_out": r["xor_out"]}


def prefixes() -> dict:
    nn = json.loads(NN_JSON.read_text())
    nf = json.loads(NF_JSON.read_text())
    ng = json.loads(NG_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nn["checks"]["all_ok"]
        and nf["checks"]["all_ok"]
        and ng["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nn["verdict"]["t_jp1"] == "LEMMA"
        and nf["verdict"]["t_outer"] == "LEMMA"
        and ng["verdict"]["t_inner"] == "LEMMA"
        and nn["verdict"]["prize"] == "unsolved"
        and want_t_jp1_out(3) == 1
        and want_t_jp1_out(6) == 1
        and want_t_jp1_out(9) == 1
        and want_t_jp1_out(2) == 0
        and want_t_outer(2) == 1
        and want_t_jp1(10) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    qboth: dict,
    kd9: dict,
    kd10: dict,
    kj: dict,
    kt: dict,
    ko: dict,
    ki: dict,
    kr: dict,
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
        and kt["ok"]
        and ko["ok"]
        and ki["ok"]
        and kr["ok"]
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
    qboth = bothq_t_jp1_out()
    kd9 = killed_die_k9(qboth)
    kd10 = killed_die_k10(qboth)
    kj = killed_eq_jp1(qboth)
    kt = killed_eq_t(qboth)
    ko = killed_eq_outer(qboth)
    ki = killed_eq_inner(qboth)
    kr = killed_eq_rest(qboth)
    kz = killed_zero(qboth)
    kone = killed_one(qboth)
    kemp = killed_empty(qboth)
    kpw = killed_pointwise(qboth)
    kq6 = killed_q6_die(qboth)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, qboth, kd9, kd10, kj, kt, ko, ki, kr, kz, kone, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "NO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_t_jp1_out": {k: qboth[k] for k in qboth if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_jp1": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_outer": {k: ko[k] for k in ko if k != "ok"},
        "killed_eq_inner": {k: ki[k] for k in ki if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_one": {k: kone[k] for k in kone if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6_die": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "t_jp1_out": True,
            "t_jp1": True,
            "t_outer": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_jp1": False,
            "eq_t": False,
            "eq_outer": False,
            "eq_inner": False,
            "eq_rest": False,
            "t_jp1_out_zero": False,
            "t_jp1_out_one": False,
            "nout_empty": False,
            "nout_pointwise": False,
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
            "t_jp1_out": "LEMMA",
            "t_jp1": "LEMMA",
            "t_outer": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_jp1": "KILLED",
            "eq_t": "KILLED",
            "eq_outer": "KILLED",
            "eq_inner": "KILLED",
            "eq_rest": "KILLED",
            "t_jp1_out_zero": "KILLED",
            "t_jp1_out_one": "KILLED",
            "nout_empty": "KILLED",
            "nout_pointwise": "KILLED",
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
        "bothq_t_jp1_out n_ok",
        dump["bothq_t_jp1_out"]["n_ok"],
        "n_g1",
        dump["bothq_t_jp1_out"]["n_g1"],
        "n_out",
        dump["bothq_t_jp1_out"]["n_out"],
        "n_outg",
        dump["bothq_t_jp1_out"]["n_outg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_eq_outer", dump["killed_eq_outer"])
    print("killed_eq_inner", dump["killed_eq_inner"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_one", dump["killed_one"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6_die", dump["killed_q6_die"])


if __name__ == "__main__":
    main()
