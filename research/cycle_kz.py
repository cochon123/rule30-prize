#!/usr/bin/env python3
"""Cycle KZ: G(3*2^a-1) has three isolated ones iff a even.

a even: isolated ones at U-1, 3U-1, 5U-1, no run-3, n_run2=2^{a+1}-2.
a odd: no isolated ones, run-3 starts at U-2, 3U-2, 5U-2, n_run2=2^{a+1}-4.
Not a unique isolated one; not a unique run-3; not even-a run-3; not
odd-a isolated ones. This is Green-only, not packed AND XOR J. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kz.py --certify
Dump: research/cycle_kz.json
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
from cycle_kp import tri_n

OUT = Path(__file__).resolve().with_suffix(".json")
KY_JSON = Path(__file__).resolve().parent / "cycle_ky.json"

A_MAX = 8


def want_iso(a: int) -> list:
    """Isolated-one columns of G(3*2^a-1)."""
    if a % 2:
        return []
    U = 1 << a
    return [U - 1, 3 * U - 1, 5 * U - 1]


def want_r3(a: int) -> list:
    """Run-3 starts of G(3*2^a-1)."""
    if a % 2 == 0:
        return []
    U = 1 << a
    return [(U - 2, 3), (3 * U - 2, 3), (5 * U - 2, 3)]


def want_n_run2(a: int) -> int:
    """n_run2 of G(3*2^a-1)."""
    return (1 << (a + 1)) - (2 if a % 2 == 0 else 4)


def tri_iso_table() -> dict:
    """a<=8: three iso iff a even; three run-3 iff a odd."""
    rows = {}
    n_ok = 0
    for a in range(0, A_MAX + 1):
        n = tri_n(a)
        runs = g_runs(n)
        r1 = [(s, r) for s, r in runs if r == 1]
        r2 = [(s, r) for s, r in runs if r == 2]
        r3 = [(s, r) for s, r in runs if r == 3]
        iso = [j for j in range(0, 2 * n + 1) if isolated_one(n, j)]
        wt = 3 * jacobsthal(a + 2)
        if wt != g_wt(n):
            return {"ok": False, "want_wt": True, "a": a, "want": wt, "g_wt": g_wt(n)}
        if r1 != [(j, 1) for j in want_iso(a)]:
            return {"ok": False, "r1": True, "a": a, "r1": r1, "want": want_iso(a)}
        if iso != want_iso(a):
            return {"ok": False, "iso": True, "a": a, "iso": iso, "want": want_iso(a)}
        if r3 != want_r3(a):
            return {"ok": False, "r3": True, "a": a, "r3": r3, "want": want_r3(a)}
        if len(r2) != want_n_run2(a):
            return {
                "ok": False,
                "r2": True,
                "a": a,
                "got": len(r2),
                "want": want_n_run2(a),
            }
        rows[str(a)] = {
            "n": n,
            "g_wt": wt,
            "n_run1": len(r1),
            "n_run2": len(r2),
            "n_run3": len(r3),
            "iso": iso,
            "r3": r3,
        }
        n_ok += 1
    ok = (
        n_ok == 9
        and rows["0"]["iso"] == [0, 2, 4]
        and rows["1"]["iso"] == []
        and rows["1"]["r3"] == [(0, 3), (4, 3), (8, 3)]
        and rows["2"]["iso"] == [3, 11, 19]
        and rows["2"]["n_run2"] == 6
        and rows["3"]["n_run3"] == 3
        and rows["8"]["iso"] == [255, 767, 1279]
        and want_n_run2(5) == 60
        and tri_n(4) == 47
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_one_iso() -> dict:
    """Tri row has a unique isolated one: a=2 n=11 has three."""
    iso = want_iso(2)
    got = [j for j in range(0, 2 * tri_n(2) + 1) if isolated_one(tri_n(2), j)]
    ok = iso == [3, 11, 19] and got == iso and len(iso) == 3
    return {"ok": ok, "a": 2, "n": 11, "iso": got}


def killed_one_r3() -> dict:
    """Tri row has a unique run-3: a=1 n=5 has three."""
    r3 = [(s, r) for s, r in g_runs(tri_n(1)) if r == 3]
    ok = r3 == [(0, 3), (4, 3), (8, 3)] and len(r3) == 3
    return {"ok": ok, "a": 1, "n": 5, "r3": r3}


def killed_odd_iso() -> dict:
    """Odd a has isolated ones: a=1 n=5 has none."""
    n = tri_n(1)
    iso = [j for j in range(0, 2 * n + 1) if isolated_one(n, j)]
    ok = iso == [] and n == 5
    return {"ok": ok, "a": 1, "n": n, "iso": iso}


def killed_even_r3() -> dict:
    """Even a has a run-3: a=2 n=11 has none."""
    r3 = [(s, r) for s, r in g_runs(tri_n(2)) if r == 3]
    ok = r3 == []
    return {"ok": ok, "a": 2, "n": 11, "r3": r3}


def prefixes() -> dict:
    ky = json.loads(KY_JSON.read_text())
    ok = (
        ky["checks"]["all_ok"]
        and ky["verdict"]["mersenne_centre_iso"] == "LEMMA"
        and ky["verdict"]["mer10_extra_j"] == "LEMMA"
        and ky["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_n_run2(0) == 0
    assert want_n_run2(4) == 30
    assert want_iso(0) == [0, 2, 4]
    assert tri_n(6) == 191
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = tri_iso_table()
    sc = g4_xor_cover()
    k0 = killed_one_iso()
    k1 = killed_one_r3()
    k2 = killed_odd_iso()
    k3 = killed_even_r3()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "tri_iso_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_one_iso": {k: k0[k] for k in k0 if k != "ok"},
        "killed_one_r3": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_iso": {k: k2[k] for k in k2 if k != "ok"},
        "killed_even_r3": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "tri_three_iso": True,
            "mersenne_centre_iso": True,
            "mer10_extra_j": True,
            "one_iso": False,
            "one_r3": False,
            "odd_has_iso": False,
            "even_has_r3": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "tri_three_iso": "LEMMA",
            "mersenne_centre_iso": "LEMMA",
            "mer10_extra_j": "LEMMA",
            "one_iso": "KILLED",
            "one_r3": "KILLED",
            "odd_has_iso": "KILLED",
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
    print("tri_iso_table n_ok", dump["tri_iso_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_one_iso", dump["killed_one_iso"])
    print("killed_one_r3", dump["killed_one_r3"])
    print("killed_odd_iso", dump["killed_odd_iso"])
    print("killed_even_r3", dump["killed_even_r3"])


if __name__ == "__main__":
    main()
