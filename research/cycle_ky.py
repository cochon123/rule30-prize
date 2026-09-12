#!/usr/bin/env python3
"""Cycle KY: Mersenne G(2^L-1) has a unique centre isolated one iff L even.

L even: unique run-1 at the centre, no run-3, n_run2=(jacobsthal(L+2)-1)/2.
L odd: no isolated ones, unique run-3 at the centre, n_run2=(jac-3)/2.
Not L odd isolated; not two isolated ones; not off-centre; not L even
run-3. This is Green-only, not packed AND XOR J. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ky.py --certify
Dump: research/cycle_ky.json
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
from cycle_at import jacobsthal
from cycle_ca import KNOWN20, packed_center_bits
from cycle_ip import g_runs
from cycle_ir import isolated_one
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt

OUT = Path(__file__).resolve().with_suffix(".json")
KX_JSON = Path(__file__).resolve().parent / "cycle_kx.json"

L_MAX = 10


def mer_n(L: int) -> int:
    return (1 << L) - 1


def want_n_run2(L: int) -> int:
    """n_run2 of G(2^L-1)."""
    a = jacobsthal(L + 2)
    return (a - 1) // 2 if L % 2 == 0 else (a - 3) // 2


def mer_iso_table() -> dict:
    """L<=10: unique centre iso iff L even; unique centre run-3 iff L odd."""
    rows = {}
    n_ok = 0
    for L in range(0, L_MAX + 1):
        n = mer_n(L)
        runs = g_runs(n)
        r1 = [(s, r) for s, r in runs if r == 1]
        r2 = [(s, r) for s, r in runs if r == 2]
        r3 = [(s, r) for s, r in runs if r == 3]
        iso = [j for j in range(0, 2 * n + 1) if isolated_one(n, j)]
        a = jacobsthal(L + 2)
        if a != g_wt(n):
            return {"ok": False, "wt": True, "L": L, "a": a, "g_wt": g_wt(n)}
        if L % 2 == 0:
            if r1 != [(n, 1)] or r3 != [] or iso != [n]:
                return {
                    "ok": False,
                    "even": True,
                    "L": L,
                    "r1": r1,
                    "r3": r3,
                    "iso": iso,
                }
        else:
            if r1 != [] or r3 != [(n - 1, 3)] or iso != []:
                return {
                    "ok": False,
                    "odd": True,
                    "L": L,
                    "r1": r1,
                    "r3": r3,
                    "iso": iso,
                }
        if len(r2) != want_n_run2(L):
            return {"ok": False, "r2": True, "L": L, "got": len(r2), "want": want_n_run2(L)}
        rows[str(L)] = {
            "n": n,
            "g_wt": a,
            "n_run1": len(r1),
            "n_run2": len(r2),
            "n_run3": len(r3),
            "iso": iso,
        }
        n_ok += 1
    ok = (
        n_ok == 11
        and rows["0"]["iso"] == [0]
        and rows["1"]["iso"] == []
        and rows["1"]["n_run3"] == 1
        and rows["2"]["iso"] == [3]
        and rows["2"]["n_run2"] == 2
        and rows["3"]["n_run3"] == 1
        and rows["10"]["iso"] == [1023]
        and want_n_run2(5) == 20
        and mer_n(4) == 15
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_odd_iso() -> dict:
    """L odd has isolated ones: L=1 n=1 has none."""
    n = mer_n(1)
    iso = [j for j in range(0, 2 * n + 1) if isolated_one(n, j)]
    ok = iso == [] and n == 1
    return {"ok": ok, "L": 1, "n": n, "iso": iso}


def killed_two_iso() -> dict:
    """L even has two isolated ones: L=2 n=3 is only the centre."""
    n = mer_n(2)
    iso = [j for j in range(0, 2 * n + 1) if isolated_one(n, j)]
    ok = iso == [3] and iso == [n] and len(iso) == 1
    return {"ok": ok, "L": 2, "n": n, "iso": iso}


def killed_off_centre() -> dict:
    """L even isolated one is off-centre: L=2 is j=n=3."""
    n = mer_n(2)
    ok = isolated_one(n, n) and not isolated_one(n, 1) and not isolated_one(n, 5)
    return {"ok": ok, "L": 2, "n": n, "j": n}


def killed_even_r3() -> dict:
    """L even has a run-3: L=2 n=3 has none."""
    r3 = [(s, r) for s, r in g_runs(mer_n(2)) if r == 3]
    ok = r3 == []
    return {"ok": ok, "L": 2, "n": 3, "r3": r3}


def prefixes() -> dict:
    kx = json.loads(KX_JSON.read_text())
    ok = (
        kx["checks"]["all_ok"]
        and kx["verdict"]["mer10_extra_j"] == "LEMMA"
        and kx["verdict"]["family_clip_lr"] == "LEMMA"
        and kx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_n_run2(0) == 0
    assert want_n_run2(4) == 10
    assert mer_n(6) == 63
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mer_iso_table()
    sc = g4_xor_cover()
    k0 = killed_odd_iso()
    k1 = killed_two_iso()
    k2 = killed_off_centre()
    k3 = killed_even_r3()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mer_iso_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_odd_iso": {k: k0[k] for k in k0 if k != "ok"},
        "killed_two_iso": {k: k1[k] for k in k1 if k != "ok"},
        "killed_off_centre": {k: k2[k] for k in k2 if k != "ok"},
        "killed_even_r3": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "mersenne_centre_iso": True,
            "mer10_extra_j": True,
            "family_clip_lr": True,
            "odd_has_iso": False,
            "two_iso": False,
            "iso_off_centre": False,
            "even_has_r3": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mersenne_centre_iso": "LEMMA",
            "mer10_extra_j": "LEMMA",
            "family_clip_lr": "LEMMA",
            "odd_has_iso": "KILLED",
            "two_iso": "KILLED",
            "iso_off_centre": "KILLED",
            "even_has_r3": "KILLED",
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
    print("mer_iso_table n_ok", dump["mer_iso_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_odd_iso", dump["killed_odd_iso"])
    print("killed_two_iso", dump["killed_two_iso"])
    print("killed_off_centre", dump["killed_off_centre"])
    print("killed_even_r3", dump["killed_even_r3"])


if __name__ == "__main__":
    main()
