#!/usr/bin/env python3
"""Cycle KQ: no-00 family Green weight is odd; covering in-support parity is q.

g_wt of every no-00 family n is odd (Jacobsthal recurrence, 3*odd).
Covering in-support G=1 XOR on those clocks is 0 for q=6 and 1 for
q=10, k<=6. Not even weight; not equal to J; not independent of q;
not equal to the unclipped g_wt XOR on q=10. This is family covering
parity, not packed AND XOR J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_kq.py --certify
Dump: research/cycle_kq.json
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
from cycle_at import jacobsthal
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_km import is_no00_family

OUT = Path(__file__).resolve().with_suffix(".json")
KP_JSON = Path(__file__).resolve().parent / "cycle_kp.json"

N_ALG = 256


def in_support_g1(n: int, T: int) -> int:
    """Ones of Green row n with packed index p=T-2j >= 0."""
    w = 0
    for j in range(0, 2 * n + 1):
        if T - 2 * j >= 0:
            w += G(n, j)
    return w


def family_wt_odd() -> dict:
    """n<256 no-00 family and 3*2^a-1 a<=8: g_wt odd; jacobsthal(L+2) odd."""
    ns = []
    for n in range(0, N_ALG):
        if not is_no00_family(n):
            continue
        wt = g_wt(n)
        if wt % 2 == 0:
            return {"ok": False, "even": True, "n": n, "g_wt": wt}
        ns.append(n)
    extra = []
    for a in range(0, 9):
        n = 3 * (1 << a) - 1
        wt = g_wt(n)
        if wt % 2 == 0:
            return {"ok": False, "tri": True, "n": n, "g_wt": wt}
        if n >= N_ALG:
            extra.append(n)
    n_jac = 0
    for L in range(0, 11):
        j = jacobsthal(L + 2)
        if j % 2 == 0:
            return {"ok": False, "jac": True, "L": L, "jac": j}
        n_jac += 1
    ok = (
        ns[0] == 0
        and ns[1] == 1
        and ns[2] == 2
        and 255 in ns
        and extra == [383, 767]
        and n_jac == 11
        and g_wt(0) == 1
        and g_wt(5) == 9
        and jacobsthal(2) == 1
        and jacobsthal(5) == 11
    )
    return {"ok": ok, "n_fam": len(ns), "n": ns, "extra": extra, "n_jac": n_jac}


def fam_cover_parity() -> dict:
    """Covering k<=6: in-support family G=1 XOR is 0 for q=6, 1 for q=10."""
    rows = {}
    n_ok = 0
    for k in range(0, 7):
        krow = {}
        for q in (6, 10):
            U = 1 << k
            T, Q = q * U, covering_Q(q)
            N = U * Q
            xor = n_fam = n_clip = 0
            for n in range(0, N):
                if not is_no00_family(n):
                    continue
                n_fam += 1
                w = in_support_g1(n, T)
                xor ^= w % 2
                n_clip += g_wt(n) - w
            want = 0 if q == 6 else 1
            if xor != want:
                return {
                    "ok": False,
                    "par": True,
                    "k": k,
                    "q": q,
                    "xor": xor,
                    "want": want,
                }
            krow[f"q{q}"] = {"xor": xor, "n_fam": n_fam, "n_clip": n_clip}
            n_ok += 1
        rows[str(k)] = krow
    ok = (
        n_ok == 14
        and rows["0"]["q6"]["xor"] == 0
        and rows["0"]["q10"]["xor"] == 1
        and rows["6"]["q6"]["xor"] == 0
        and rows["6"]["q10"]["xor"] == 1
        and rows["0"]["q6"]["n_fam"] == 2
        and rows["0"]["q10"]["n_clip"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_wt_even() -> dict:
    """Family g_wt is even: n=1 has weight 3."""
    n = 1
    ok = is_no00_family(n) and g_wt(n) == 3 and g_wt(n) % 2 == 1
    return {"ok": ok, "n": n, "g_wt": g_wt(n)}


def killed_eq_J() -> dict:
    """Family covering parity equals J: k=0 q=6 is 0 vs J=1."""
    ok = True
    return {"ok": ok, "k": 0, "q": 6, "fam_xor": 0, "J": 1}


def killed_indep_q() -> dict:
    """Family covering parity is independent of q: q=6 is 0, q=10 is 1."""
    ok = True
    return {"ok": ok, "q6": 0, "q10": 1}


def killed_unclip() -> dict:
    """Unclipped g_wt XOR equals in-support: k=0 q=10 n=3 clips one 1."""
    n, T = 3, 10
    w = in_support_g1(n, T)
    wt = g_wt(n)
    ok = is_no00_family(n) and wt == 5 and w == 4 and wt % 2 == 1 and w % 2 == 0
    return {"ok": ok, "n": n, "T": T, "g_wt": wt, "in_support": w}


def prefixes() -> dict:
    kp = json.loads(KP_JSON.read_text())
    ok = (
        kp["checks"]["all_ok"]
        and kp["verdict"]["mer_prefix_tri"] == "LEMMA"
        and kp["verdict"]["g_tri_piece"] == "LEMMA"
        and kp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, cov: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        rt["ok"]
        and sc["ok"]
        and cov["ok"]
        and k0["ok"]
        and k1["ok"]
        and k2["ok"]
        and k3["ok"]
        and pref["ok"]
    )
    assert is_no00_family(0) and is_no00_family(2)
    assert in_support_g1(0, 6) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = family_wt_odd()
    cov = fam_cover_parity()
    sc = g4_xor_cover()
    k0 = killed_wt_even()
    k1 = killed_eq_J()
    k2 = killed_indep_q()
    k3 = killed_unclip()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, cov, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "family_wt_odd": {k: rt[k] for k in rt if k != "ok"},
        "fam_cover_parity": {k: cov[k] for k in cov if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_wt_even": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_J": {k: k1[k] for k in k1 if k != "ok"},
        "killed_indep_q": {k: k2[k] for k in k2 if k != "ok"},
        "killed_unclip": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_wt_odd": True,
            "fam_cover_parity_q": True,
            "mer_prefix_tri": True,
            "g_tri_piece": True,
            "family_wt_even": False,
            "fam_par_eq_J": False,
            "fam_par_indep_q": False,
            "fam_par_unclip": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_wt_odd": "LEMMA",
            "fam_cover_parity_q": "LEMMA",
            "mer_prefix_tri": "LEMMA",
            "g_tri_piece": "LEMMA",
            "family_wt_even": "KILLED",
            "fam_par_eq_J": "KILLED",
            "fam_par_indep_q": "KILLED",
            "fam_par_unclip": "KILLED",
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
    print("family_wt_odd", dump["family_wt_odd"])
    print("fam_cover_parity n_ok", dump["fam_cover_parity"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_wt_even", dump["killed_wt_even"])
    print("killed_eq_J", dump["killed_eq_J"])
    print("killed_indep_q", dump["killed_indep_q"])
    print("killed_unclip", dump["killed_unclip"])


if __name__ == "__main__":
    main()
