#!/usr/bin/env python3
"""Cycle KJ: child ones-run count equals parent Green weight.

n_runs(2m)=n_runs(2m+1)=g_wt(m), and g_wt(2m)=g_wt(m). Odd child run
count is not n_runs(m); not g_wt of itself; even double is not twice
parent runs or twice parent weight. This is Green-only, not J. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kj.py --certify
Dump: research/cycle_kj.json
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
from cycle_ip import g_runs
from cycle_kh import g4_xor_cover
from cycle_ki import n_pairs_of

OUT = Path(__file__).resolve().with_suffix(".json")
KI_JSON = Path(__file__).resolve().parent / "cycle_ki.json"

M_ALG = 128


def g_wt(n: int) -> int:
    """Hamming weight of Green row n, columns 0..2n."""
    return sum(G(n, j) for j in range(0, 2 * n + 1))


def run_wt_table() -> dict:
    """m<128: n_runs(2m)=n_runs(2m+1)=g_wt(m) and g_wt(2m)=g_wt(m)."""
    n_ok = 0
    for m in range(0, M_ALG):
        w = g_wt(m)
        r_even = len(g_runs(2 * m))
        r_odd = len(g_runs(2 * m + 1))
        w_even = g_wt(2 * m)
        w_odd = g_wt(2 * m + 1)
        n_parent_runs = len(g_runs(m))
        if r_even != w or r_odd != w:
            return {
                "ok": False,
                "runs": True,
                "m": m,
                "w": w,
                "r_even": r_even,
                "r_odd": r_odd,
            }
        if w_even != w:
            return {"ok": False, "wt_even": True, "m": m, "w": w, "w_even": w_even}
        if w_odd != w + 2 * n_parent_runs:
            return {
                "ok": False,
                "wt_odd": True,
                "m": m,
                "w": w,
                "w_odd": w_odd,
                "n_runs": n_parent_runs,
            }
        n_ok += 1
    ok = (
        n_ok == M_ALG
        and g_wt(0) == 1
        and len(g_runs(0)) == 1
        and len(g_runs(1)) == 1
        and g_wt(1) == 3
        and len(g_runs(2)) == 3
        and len(g_runs(3)) == 3
    )
    return {"ok": ok, "n_ok": n_ok, "g_wt0": g_wt(0), "g_wt1": g_wt(1)}


def killed_r_eq_parent() -> dict:
    """n_runs(2m+1) equals n_runs(m): n=3 has 3 runs, parent n=1 has 1."""
    m, n = 1, 3
    r_m = len(g_runs(m))
    r_n = len(g_runs(n))
    ok = r_m == 1 and r_n == 3 and r_n != r_m
    return {"ok": ok, "m": m, "n": n, "r_m": r_m, "r_n": r_n}


def killed_r_eq_self_wt() -> dict:
    """n_runs(n) equals g_wt(n) on odd n: n=1 has 1 run and weight 3."""
    n = 1
    r, w = len(g_runs(n)), g_wt(n)
    ok = r == 1 and w == 3 and r != w
    return {"ok": ok, "n": n, "n_runs": r, "g_wt": w}


def killed_even_twice_runs() -> dict:
    """n_runs(2m) is twice n_runs(m): n=2 has 3 runs, parent has 1."""
    m, n = 1, 2
    r_m, r_n = len(g_runs(m)), len(g_runs(n))
    ok = r_m == 1 and r_n == 3 and r_n != 2 * r_m
    return {"ok": ok, "m": m, "n": n, "r_m": r_m, "r_n": r_n}


def killed_even_twice_wt() -> dict:
    """g_wt(2m) is twice g_wt(m): n=2 has weight 3, parent has 3."""
    m, n = 1, 2
    w_m, w_n = g_wt(m), g_wt(n)
    ok = w_m == 3 and w_n == 3 and w_n != 2 * w_m
    return {"ok": ok, "m": m, "n": n, "w_m": w_m, "w_n": w_n}


def prefixes() -> dict:
    ki = json.loads(KI_JSON.read_text())
    ok = (
        ki["checks"]["all_ok"]
        and ki["verdict"]["n_pairs_twice_runs"] == "LEMMA"
        and ki["verdict"]["image_two_pairs"] == "LEMMA"
        and ki["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert g_wt(2 * 4) == g_wt(4) == len(g_runs(8)) == len(g_runs(9))
    assert n_pairs_of((0, 1, 1, 1, 0)) == 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = run_wt_table()
    sc = g4_xor_cover()
    k0 = killed_r_eq_parent()
    k1 = killed_r_eq_self_wt()
    k2 = killed_even_twice_runs()
    k3 = killed_even_twice_wt()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "run_wt_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_r_eq_parent": {k: k0[k] for k in k0 if k != "ok"},
        "killed_r_eq_self_wt": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_twice_runs": {k: k2[k] for k in k2 if k != "ok"},
        "killed_even_twice_wt": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "n_runs_eq_parent_wt": True,
            "g_wt_even_copy": True,
            "n_pairs_twice_runs": True,
            "image_two_pairs": True,
            "n_runs_eq_parent_runs": False,
            "n_runs_eq_self_wt": False,
            "even_twice_runs": False,
            "even_twice_wt": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n_runs_eq_parent_wt": "LEMMA",
            "g_wt_even_copy": "LEMMA",
            "n_pairs_twice_runs": "LEMMA",
            "image_two_pairs": "LEMMA",
            "n_runs_eq_parent_runs": "KILLED",
            "n_runs_eq_self_wt": "KILLED",
            "even_twice_runs": "KILLED",
            "even_twice_wt": "KILLED",
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
    print("run_wt_table", dump["run_wt_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_r_eq_parent", dump["killed_r_eq_parent"])
    print("killed_r_eq_self_wt", dump["killed_r_eq_self_wt"])
    print("killed_even_twice_runs", dump["killed_even_twice_runs"])
    print("killed_even_twice_wt", dump["killed_even_twice_wt"])


if __name__ == "__main__":
    main()
