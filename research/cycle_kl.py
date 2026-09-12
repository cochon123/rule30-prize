#!/usr/bin/env python3
"""Cycle KL: Mersenne Green weight is the Jacobsthal cardinality |S_{L+2}|.

a_L=g_wt(2^L-1) equals jacobsthal(L+2)=|S_{L+2}| from Cycle AT, so
g_wt(n) is the product of |S_{L+2}| over binary 1-runs. a_L is not
|S_L| or |S_{L+1}|; g_wt(n) is not jacobsthal(n). This is Green-only,
not J. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_kl.py --certify
Dump: research/cycle_kl.json
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
from cycle_at import S as jacobsthal_S
from cycle_at import jacobsthal
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_kk import bin_one_runs, g_wt_prod, mersenne_a

OUT = Path(__file__).resolve().with_suffix(".json")
KK_JSON = Path(__file__).resolve().parent / "cycle_kk.json"

N_ALG = 256
L_MAX = 10


def jac_wt_prod(n: int) -> int:
    """Product of jacobsthal(L+2) over binary 1-runs of n."""
    prod = 1
    for length in bin_one_runs(n):
        prod *= jacobsthal(length + 2)
    return prod


def jac_wt_table() -> dict:
    """a_L = |S_{L+2}| = g_wt(2^L-1); n<256 product matches g_wt."""
    n_L = 0
    for L in range(0, L_MAX + 1):
        a = mersenne_a(L)
        j = jacobsthal(L + 2)
        s = len(jacobsthal_S(L + 2))
        if a != j or j != s:
            return {
                "ok": False,
                "card": True,
                "L": L,
                "a": a,
                "jac": j,
                "S": s,
            }
        if L <= 8:
            got = g_wt((1 << L) - 1)
            if got != a:
                return {"ok": False, "g_wt": True, "L": L, "got": got, "want": a}
        n_L += 1
    n_ok = 0
    for n in range(0, N_ALG):
        if g_wt(n) != jac_wt_prod(n) or jac_wt_prod(n) != g_wt_prod(n):
            return {
                "ok": False,
                "prod": True,
                "n": n,
                "g_wt": g_wt(n),
                "jac": jac_wt_prod(n),
            }
        n_ok += 1
    ok = (
        n_L == L_MAX + 1
        and n_ok == N_ALG
        and jacobsthal(2) == 1
        and jacobsthal(3) == 3
        and jacobsthal(4) == 5
        and jacobsthal(5) == 11
        and len(jacobsthal_S(3)) == 3
        and jac_wt_prod(0) == 1
        and jac_wt_prod(7) == 11
        and jac_wt_prod(11) == 15
    )
    return {
        "ok": ok,
        "n_L": n_L,
        "n_ok": n_ok,
        "a": [mersenne_a(L) for L in range(0, 9)],
        "jac": [jacobsthal(L) for L in range(0, 11)],
    }


def killed_eq_S_L() -> dict:
    """a_L equals |S_L|: L=3 has a=11, |S_3|=3."""
    L = 3
    a, s = mersenne_a(L), len(jacobsthal_S(L))
    ok = a == 11 and s == 3 and a != s and jacobsthal(L) == 3
    return {"ok": ok, "L": L, "a": a, "S": s}


def killed_eq_S_Lp1() -> dict:
    """a_L equals |S_{L+1}|: L=3 has a=11, |S_4|=5."""
    L = 3
    a, s = mersenne_a(L), len(jacobsthal_S(L + 1))
    ok = a == 11 and s == 5 and a != s
    return {"ok": ok, "L": L, "a": a, "S": s}


def killed_eq_jac_n() -> dict:
    """g_wt(n) equals jacobsthal(n): n=7 has weight 11, J_7=43."""
    n = 7
    got, j = g_wt(n), jacobsthal(n)
    ok = got == 11 and j == 43 and got != j
    return {"ok": ok, "n": n, "g_wt": got, "jac": j}


def killed_eq_jac_pc() -> dict:
    """g_wt(n) equals jacobsthal(popcount+2): n=5 has 9, J_4=5."""
    n = 5
    pc = bin(n).count("1")
    got, j = g_wt(n), jacobsthal(pc + 2)
    ok = got == 9 and j == 5 and got != j and bin_one_runs(n) == [1, 1]
    return {"ok": ok, "n": n, "g_wt": got, "jac": j, "pc": pc}


def prefixes() -> dict:
    kk = json.loads(KK_JSON.read_text())
    ok = (
        kk["checks"]["all_ok"]
        and kk["verdict"]["g_wt_run_product"] == "LEMMA"
        and kk["verdict"]["mersenne_a_closed"] == "LEMMA"
        and kk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert mersenne_a(0) == jacobsthal(2) == len(jacobsthal_S(2))
    assert jac_wt_prod(21) == 27
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = jac_wt_table()
    sc = g4_xor_cover()
    k0 = killed_eq_S_L()
    k1 = killed_eq_S_Lp1()
    k2 = killed_eq_jac_n()
    k3 = killed_eq_jac_pc()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "jac_wt_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_S_L": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_S_Lp1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_jac_n": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_jac_pc": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "a_L_eq_jac_Lp2": True,
            "g_wt_jac_product": True,
            "g_wt_run_product": True,
            "mersenne_a_closed": True,
            "a_L_eq_S_L": False,
            "a_L_eq_S_Lp1": False,
            "g_wt_eq_jac_n": False,
            "g_wt_eq_jac_pc": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "a_L_eq_jac_Lp2": "LEMMA",
            "g_wt_jac_product": "LEMMA",
            "g_wt_run_product": "LEMMA",
            "mersenne_a_closed": "LEMMA",
            "a_L_eq_S_L": "KILLED",
            "a_L_eq_S_Lp1": "KILLED",
            "g_wt_eq_jac_n": "KILLED",
            "g_wt_eq_jac_pc": "KILLED",
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
    print("jac_wt_table", dump["jac_wt_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_S_L", dump["killed_eq_S_L"])
    print("killed_eq_S_Lp1", dump["killed_eq_S_Lp1"])
    print("killed_eq_jac_n", dump["killed_eq_jac_n"])
    print("killed_eq_jac_pc", dump["killed_eq_jac_pc"])


if __name__ == "__main__":
    main()
