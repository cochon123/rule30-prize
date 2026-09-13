#!/usr/bin/env python3
"""Cycle OG: E_k = R_k xor S_k xor T_k vanishes on q=10 through k<=10.

R_k is odd-s packed AND xor on G=1 off {4,6,14}. S_k and T_k are
Cycle NA's Green-only pieces. E_k=0 is odd-s rest, not FR full
remainder tot = xor_odd xor xor_even. Certified q=10 k<=10, not
an all-k theorem. Not pointwise (k=0 n_e=2); not palindrome
pairing of all errors; not R on S/T with R off=0 (k=8 R_T=1
T=0); not E=0 on q=6 (k=2 E=1; also k=3,9); not E=0 on q=18
(k=1 E=1); not E=0 implies J_full=0 (k=2 q=10: E=0, J10=1);
not S xor T equals J_odd or J_full; not the form for all k.
Do not catalogue further S/T subregions unless the experiment
answers why E_k=0. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_og.py --certify
Dump: research/cycle_og.json
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
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import want_rest10
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
NB_JSON = Path(__file__).resolve().parent / "cycle_nb.json"
MD_JSON = Path(__file__).resolve().parent / "cycle_md.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_e": 83722,
        "n_s": 29820,
        "xor_e": 0,
        "xor_r": 0,
        "xor_s": 0,
        "xor_t": 0,
        "xor_j_odd": 1,
        "xor_r_t": 1,
        "xor_r_off": 1,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_e": 271350,
        "n_s": 96773,
        "xor_e": 0,
        "xor_r": 0,
        "xor_s": 0,
        "xor_t": 0,
        "xor_j_odd": 1,
        "xor_r_t": 0,
        "xor_r_off": 1,
    },
}

WANT_K8 = {
    0: {"n_ok": 15, "n_g1": 11, "n_e": 2, "n_s": 0, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 0, "xor_r_t": 0, "xor_r_off": 0},
    1: {"n_ok": 58, "n_g1": 36, "n_e": 6, "n_s": 2, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 0, "xor_r_t": 0, "xor_r_off": 0},
    2: {"n_ok": 226, "n_g1": 110, "n_e": 20, "n_s": 5, "xor_e": 0, "xor_r": 1, "xor_s": 0, "xor_t": 1, "xor_j_odd": 0, "xor_r_s": 0, "xor_r_t": 1, "xor_r_off": 0},
    3: {"n_ok": 892, "n_g1": 352, "n_e": 68, "n_s": 21, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 1, "xor_r_t": 1, "xor_r_off": 0},
    4: {"n_ok": 3544, "n_g1": 1122, "n_e": 214, "n_s": 67, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 1, "xor_r_t": 1, "xor_r_off": 0},
    5: {"n_ok": 14128, "n_g1": 3608, "n_e": 710, "n_s": 244, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 1, "xor_r_t": 0, "xor_r_off": 1},
    6: {"n_ok": 56416, "n_g1": 11618, "n_e": 2412, "n_s": 793, "xor_e": 0, "xor_r": 1, "xor_s": 1, "xor_t": 0, "xor_j_odd": 0, "xor_r_s": 1, "xor_r_t": 0, "xor_r_off": 0},
    7: {"n_ok": 225472, "n_g1": 37496, "n_e": 7806, "n_s": 2737, "xor_e": 0, "xor_r": 0, "xor_s": 0, "xor_t": 0, "xor_j_odd": 1, "xor_r_s": 1, "xor_r_t": 0, "xor_r_off": 1},
    8: {"n_ok": 901504, "n_g1": 121122, "n_e": 25738, "n_s": 8895, "xor_e": 0, "xor_r": 1, "xor_s": 1, "xor_t": 0, "xor_j_odd": 0, "xor_r_s": 1, "xor_r_t": 1, "xor_r_off": 1},
}


def _walk_E(k: int, q: int, *, pal: bool = False) -> dict:
    """Odd-s packed AND rest xor NA S xor NA T. Optional pal-dual errors."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    half = U // 2
    xor_r = xor_s = xor_t = xor_j_odd = xor_f = 0
    xor_r_s = xor_r_t = xor_r_off = 0
    n_ok = n_g1 = n_e = n_s = 0
    e_cells: list[tuple[int, int]] = []
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j_odd ^= 1
                    if p in FORCED:
                        xor_f ^= 1
                    else:
                        xor_r ^= 1
                is_s = is_t_fire = False
                sbit = tbit = 0
                if j > n:
                    d = j - n
                    is_s = d % 3 == 1 and G(n, j - 1) == 0
                    tbit = G(n, j - 1) if n < half else 0
                    is_t_fire = tbit == 1
                    if is_s:
                        sbit = G(n, j + 1)
                        xor_s ^= sbit
                        n_s += 1
                    if is_t_fire:
                        xor_t ^= 1
                rbit = packed if p not in FORCED else 0
                if rbit:
                    if is_s:
                        xor_r_s ^= 1
                    elif is_t_fire:
                        xor_r_t ^= 1
                    else:
                        xor_r_off ^= 1
                e = rbit ^ sbit ^ tbit
                if e:
                    n_e += 1
                    if pal:
                        e_cells.append((n, j))
        row = rule30_step(row)
        s += 1
    n_pal = 0
    if pal:
        eset = set(e_cells)
        n_pal = sum(1 for n, j in e_cells if (n, 2 * n - j) in eset)
    xor_e = xor_r ^ xor_s ^ xor_t
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_e": n_e,
        "n_s": n_s,
        "n_pal": n_pal,
        "xor_e": xor_e,
        "xor_r": xor_r,
        "xor_s": xor_s,
        "xor_t": xor_t,
        "xor_j_odd": xor_j_odd,
        "xor_f": xor_f,
        "xor_r_s": xor_r_s,
        "xor_r_t": xor_r_t,
        "xor_r_off": xor_r_off,
    }


def _row_ok10(k: int, w: dict, want: dict) -> bool:
    wr = want_rest10(k, 10)
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_e"] == want["n_e"]
        and w["n_s"] == want["n_s"]
        and w["xor_e"] == want["xor_e"] == 0
        and w["xor_r"] == want["xor_r"] == wr
        and w["xor_s"] == want["xor_s"]
        and w["xor_t"] == want["xor_t"]
        and w["xor_e"] == w["xor_r"] ^ w["xor_s"] ^ w["xor_t"]
        and w["xor_j_odd"] == want["xor_j_odd"]
        and w["xor_r_t"] == want["xor_r_t"]
        and w["xor_r_off"] == want["xor_r_off"]
        and w["n_e"] % 2 == 0
        and w["n_e"] > 0
    )


def q10_E_10() -> dict:
    """q=10 k<=10: packed R xor S xor T is 0; R equals rest10."""
    mj = json.loads(MJ_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_e = 0
    for k in range(0, 9):
        w = _walk_E(k, 10)
        pk = WANT_K8[k]
        mj_n = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"]
        mj_g = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_g1"]
        if (
            not _row_ok10(k, w, pk)
            or w["n_ok"] != mj_n
            or w["n_g1"] != mj_g
            or w["xor_r_s"] != pk["xor_r_s"]
        ):
            return {"ok": False, "k": k, "q": 10, "xor_e": w.get("xor_e")}
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_e += w["n_e"]
        rows[str(k)] = {
            "xor_e": w["xor_e"],
            "xor_r": w["xor_r"],
            "xor_s": w["xor_s"],
            "xor_t": w["xor_t"],
            "xor_j_odd": w["xor_j_odd"],
            "xor_r_s": w["xor_r_s"],
            "xor_r_t": w["xor_r_t"],
            "xor_r_off": w["xor_r_off"],
            "rest": want_rest10(k, 10),
            "n_e": w["n_e"],
            "n_s": w["n_s"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    for k in (9, 10):
        w = _walk_E(k, 10)
        if not _row_ok10(k, w, WANT_WALK[k]):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_e": w.get("xor_e"),
                "n_ok": w.get("n_ok"),
                "n_e": w.get("n_e"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_e += w["n_e"]
        rows[str(k)] = {
            "xor_e": w["xor_e"],
            "xor_r": w["xor_r"],
            "xor_s": w["xor_s"],
            "xor_t": w["xor_t"],
            "xor_j_odd": w["xor_j_odd"],
            "xor_r_s": None,
            "xor_r_t": w["xor_r_t"],
            "xor_r_off": w["xor_r_off"],
            "rest": want_rest10(k, 10),
            "n_e": w["n_e"],
            "n_s": w["n_s"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_e"] == 0 for k in range(0, 11))
        and all(rows[str(k)]["xor_r"] == want_rest10(k, 10) for k in range(0, 11))
        and rows["0"]["n_e"] == 2
        and rows["2"]["xor_r"] == 1
        and rows["2"]["xor_s"] == 0
        and rows["2"]["xor_t"] == 1
        and rows["2"]["xor_j_odd"] == 0
        and rows["8"]["xor_r_t"] == 1
        and rows["8"]["xor_t"] == 0
        and rows["8"]["n_e"] == 25738
        and rows["9"]["n_e"] == 83722
        and rows["10"]["n_e"] == 271350
        and n_e == 392048
        and n_ok == 19226959
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_e": n_e,
        "rows": rows,
    }


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["0"]
    ok = r["xor_e"] == 0 and r["n_e"] == 2
    return {"ok": ok, "k": 0, "q": 10, "n_e": r["n_e"]}


def killed_pal() -> dict:
    w = _walk_E(0, 10, pal=True)
    ok = w["xor_e"] == 0 and w["n_e"] == 2 and w["n_pal"] == 0
    return {"ok": ok, "k": 0, "q": 10, "n_e": w["n_e"], "n_pal": w["n_pal"]}


def killed_region(q10: dict) -> dict:
    r = q10["rows"]["8"]
    ok = r["xor_r_t"] == 1 and r["xor_t"] == 0 and r["xor_r_off"] == 1
    return {
        "ok": ok,
        "k": 8,
        "q": 10,
        "xor_r_t": r["xor_r_t"],
        "xor_t": r["xor_t"],
        "xor_r_off": r["xor_r_off"],
    }


def killed_q6() -> dict:
    w2 = _walk_E(2, 6)
    w3 = _walk_E(3, 6)
    w9 = _walk_E(9, 6)
    ok = (
        w2["xor_e"] == 1
        and w2["n_e"] == 7
        and w2["xor_r"] == 0
        and w2["xor_t"] == 1
        and w3["xor_e"] == 1
        and w3["n_e"] == 31
        and w9["xor_e"] == 1
        and w9["n_ok"] == 983296
        and w9["n_e"] == 34629
    )
    return {
        "ok": ok,
        "k2": {"xor_e": w2["xor_e"], "n_e": w2["n_e"]},
        "k3": {"xor_e": w3["xor_e"], "n_e": w3["n_e"]},
        "k9": {"xor_e": w9["xor_e"], "n_e": w9["n_e"], "n_ok": w9["n_ok"]},
    }


def killed_q18() -> dict:
    w = _walk_E(1, 18)
    ok = w["xor_e"] == 1 and w["n_e"] == 17 and w["xor_s"] == 1 and w["xor_r"] == 0
    return {"ok": ok, "k": 1, "q": 18, "xor_e": w["xor_e"], "n_e": w["n_e"]}


def killed_jodd_eq_full() -> dict:
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    r6 = hf["j6_j_index"]["rows"]["0"]
    r10 = hg["j10_j18_index"]["rows"]["0"]
    ok = (
        r6["xor_odd"] == 1
        and r6["tot"] == 0
        and r6["xor_even"] == 1
        and r10["xor_odd10"] == 1
        and r10["J10"] == 0
        and r10["xor_even10"] == 1
    )
    return {
        "ok": ok,
        "k": 0,
        "J6_odd": r6["xor_odd"],
        "J6_full": r6["tot"],
        "J10_odd": r10["xor_odd10"],
        "J10_full": r10["J10"],
    }


def killed_e_implies_jfull(q10: dict) -> dict:
    hg = json.loads(HG_JSON.read_text())
    r = q10["rows"]["2"]
    j10 = hg["j10_j18_index"]["rows"]["2"]["J10"]
    ok = r["xor_e"] == 0 and j10 == 1 and r["xor_j_odd"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_e": r["xor_e"], "J10_full": j10, "J10_odd": r["xor_j_odd"]}


def killed_st_eq_jodd(q10: dict) -> dict:
    r = q10["rows"]["2"]
    st = r["xor_s"] ^ r["xor_t"]
    ok = st == 1 and r["xor_j_odd"] == 0
    return {"ok": ok, "k": 2, "q": 10, "SxorT": st, "J_odd": r["xor_j_odd"]}


def prefixes() -> dict:
    nb = json.loads(NB_JSON.read_text())
    md = json.loads(MD_JSON.read_text())
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    ok = (
        nb["checks"]["all_ok"]
        and md["checks"]["all_ok"]
        and hf["checks"]["all_ok"]
        and hg["checks"]["all_ok"]
        and nb["verdict"]["green_rest10"] == "LEMMA"
        and nb["verdict"]["prize"] == "unsolved"
        and want_rest10(2, 10) == 1
        and want_rest10(9, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kpt: dict,
    kpal: dict,
    kreg: dict,
    kq6: dict,
    kq18: dict,
    kj: dict,
    kimp: dict,
    kst: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kpt["ok"]
        and kpal["ok"]
        and kreg["ok"]
        and kq6["ok"]
        and kq18["ok"]
        and kj["ok"]
        and kimp["ok"]
        and kst["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    q10_8 = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == q10_8 + WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    assert q10["n_e"] == 392048
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_E_10()
    kpt = killed_pointwise(q10)
    kpal = killed_pal()
    kreg = killed_region(q10)
    kq6 = killed_q6()
    kq18 = killed_q18()
    kj = killed_jodd_eq_full()
    kimp = killed_e_implies_jfull(q10)
    kst = killed_st_eq_jodd(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kpt, kpal, kreg, kq6, kq18, kj, kimp, kst, sc, pref
    )
    dump = {
        "cycle": "OG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_E_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_pointwise": {k: kpt[k] for k in kpt if k != "ok"},
        "killed_pal": {k: kpal[k] for k in kpal if k != "ok"},
        "killed_region": {k: kreg[k] for k in kreg if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_q18": {k: kq18[k] for k in kq18 if k != "ok"},
        "killed_jodd_eq_full": {k: kj[k] for k in kj if k != "ok"},
        "killed_e_implies_jfull": {k: kimp[k] for k in kimp if k != "ok"},
        "killed_st_eq_jodd": {k: kst[k] for k in kst if k != "ok"},
        "lemmas": {
            "E_q10_10": True,
            "green_rest10": True,
            "rest10": True,
            "j_odd_ne_full": True,
            "pointwise": False,
            "pal_all": False,
            "region": False,
            "e_q6": False,
            "e_q18": False,
            "e_implies_jfull0": False,
            "st_eq_jodd": False,
            "all_k": False,
            "u_vs_j": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "prize": False,
        },
        "verdict": {
            "E_q10_10": "CERTIFIED",
            "green_rest10": "LEMMA",
            "rest10": "LEMMA",
            "j_odd_ne_full": "CERTIFIED",
            "pointwise": "KILLED",
            "pal_all": "KILLED",
            "region": "KILLED",
            "e_q6": "KILLED",
            "e_q18": "KILLED",
            "e_implies_jfull0": "KILLED",
            "st_eq_jodd": "KILLED",
            "all_k": "KILLED",
            "u_vs_j": "KILLED",
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
        "q10_E_10 n_ok",
        dump["q10_E_10"]["n_ok"],
        "n_g1",
        dump["q10_E_10"]["n_g1"],
        "n_e",
        dump["q10_E_10"]["n_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_pal", dump["killed_pal"])
    print("killed_region", dump["killed_region"])
    print("killed_q6", dump["killed_q6"])
    print("killed_q18", dump["killed_q18"])
    print("killed_jodd_eq_full", dump["killed_jodd_eq_full"])
    print("killed_e_implies_jfull", dump["killed_e_implies_jfull"])
    print("killed_st_eq_jodd", dump["killed_st_eq_jodd"])


if __name__ == "__main__":
    main()
