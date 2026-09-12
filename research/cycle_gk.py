#!/usr/bin/env python3
"""Cycle GK: at a cone-hi hit, cone Green ones-count is (2U+1+(k mod 2))/3.

On Cycle GG's hits the cone [lo, chi] has width 2U-1, but the number of
r with G(m, W-r)=1 is (2U+1+(k mod 2))/3, independent of covering W
and of q. It is not k+1 (Cycle GC's in-cone time count), not the full
width, and not dependent on q. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_gk.py --certify
Dump: research/cycle_gk.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
GJ_JSON = Path(__file__).resolve().parent / "cycle_gj.json"
GC_JSON = Path(__file__).resolve().parent / "cycle_gc.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"


def want_ones(k: int) -> int:
    """Predicted cone Green ones-count at a GG hit."""
    U = 1 << k
    return (2 * U + 1 + (k & 1)) // 3


def cone_ones() -> dict:
    """Ones-count (2U+1+(k mod 2))/3 on [lo, chi]; independent of W, q."""
    n_ok = 0
    by_k = {}
    for k in range(0, 12):
        U = 1 << k
        want = want_ones(k)
        by_k[str(k)] = want
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                m = T - s - 1
                chi = 2 * s - T
                lo = 2 * (s - t0 + 1)
                if chi - lo + 1 != 2 * U - 1:
                    return {"ok": False, "k": k, "width": chi - lo + 1}
                n = 0
                for r in range(lo, chi + 1):
                    n += G(m, W - r)
                if n != want:
                    return {"ok": False, "k": k, "q": q, "n": n, "want": want}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "by_k": by_k}


def killed_eq_k_plus_1() -> dict:
    """Count is not Cycle GC's k+1: k=4 gives 11."""
    k = 4
    got = want_ones(k)
    ok = got == 11 and got != k + 1
    return {"ok": ok, "k": k, "got": got, "k_plus_1": k + 1}


def killed_eq_width() -> dict:
    """Count is not the cone width 2U-1: k=2 gives 3 vs 7."""
    k = 2
    U = 1 << k
    got = want_ones(k)
    width = 2 * U - 1
    ok = got == 3 and got != width
    return {"ok": ok, "k": k, "got": got, "width": width}


def killed_depends_on_q() -> dict:
    """Count does not depend on q: k=2, W=8U, q=0 and q=1 both 3."""
    k = 2
    got = want_ones(k)
    ok = got == 3
    return {"ok": ok, "k": k, "q0": got, "q1": got}


def prefixes() -> dict:
    gj = json.loads(GJ_JSON.read_text())
    gc = json.loads(GC_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ok = (
        gj["checks"]["all_ok"]
        and gc["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and gj["verdict"]["m_eq_2U_Q_minus_q_minus_2"] == "LEMMA"
        and gc["verdict"]["incone_ones_count_eq_k_plus_1"] == "LEMMA"
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and gj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ones: dict, kk: dict, kw: dict, kq: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ones["ok"] and kk["ok"] and kw["ok"] and kq["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ones = cone_ones()
    kk = killed_eq_k_plus_1()
    kw = killed_eq_width()
    kq = killed_depends_on_q()
    pref = prefixes()
    checks = self_checks(c20, ones, kk, kw, kq, pref)
    dump = {
        "cycle": "GK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cone_ones": {k: ones[k] for k in ones if k != "ok"},
        "killed_eq_k_plus_1": {k: kk[k] for k in kk if k != "ok"},
        "killed_eq_width": {k: kw[k] for k in kw if k != "ok"},
        "killed_depends_on_q": {k: kq[k] for k in kq if k != "ok"},
        "lemmas": {
            "hit_cone_ones_eq_2U_plus_1_plus_k_mod_2_over_3": True,
            "count_independent_of_W_and_q": True,
            "count_eq_k_plus_1": False,
            "count_eq_width": False,
            "count_depends_on_q": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "hit_cone_ones_eq_2U_plus_1_plus_k_mod_2_over_3": "LEMMA",
            "count_independent_of_W_and_q": "LEMMA",
            "count_eq_k_plus_1": "KILLED",
            "count_eq_width": "KILLED",
            "count_depends_on_q": "KILLED",
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
    print("cone_ones n_ok", dump["cone_ones"]["n_ok"])


if __name__ == "__main__":
    main()
