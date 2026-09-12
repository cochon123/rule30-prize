#!/usr/bin/env python3
"""Cycle LA: tri three specials are mer unique + palindrome dual + centre.

Even a: isolated ones of G(3U-1) are U-1 (Mersenne unique on the KP
prefix), 3U-1 (tri centre), 5U-1 (palindrome dual). Odd a: run-3
starts U-2, 3U-2, 5U-2 by the same split. Not prefix-only; not missing
the centre; not mer off-prefix; not odd-a different. This is
Green-only, not packed AND XOR J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_la.py --certify
Dump: research/cycle_la.json
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
from cycle_ir import isolated_one
from cycle_kh import g4_xor_cover
from cycle_kp import mer_n, tri_n
from cycle_kz import want_iso, want_r3

OUT = Path(__file__).resolve().with_suffix(".json")
KZ_JSON = Path(__file__).resolve().parent / "cycle_kz.json"

A_MAX = 8


def mer_special(a: int) -> int:
    """Mersenne unique iso column (a even) or r3 start (a odd)."""
    return (1 << a) - (1 if a % 2 == 0 else 2)


def pal_col(n: int, j: int) -> int:
    """Palindrome dual column 2n-j."""
    return 2 * n - j


def pal_r3_start(n: int, start: int) -> int:
    """Palindrome dual of a length-3 run start."""
    return 2 * n - start - 2


def from_mer(a: int) -> list:
    """Tri specials: mer unique, tri centre, palindrome dual."""
    U = 1 << a
    nt = tri_n(a)
    m = mer_special(a)
    if a % 2 == 0:
        return [m, nt, pal_col(nt, m)]
    return [m, nt - 1, pal_r3_start(nt, m)]


def mer_tri_table() -> dict:
    """a<=8: tri specials = mer unique + centre + dual; mer on KP prefix."""
    rows = {}
    n_ok = 0
    for a in range(0, A_MAX + 1):
        nm, nt = mer_n(a), tri_n(a)
        U = 1 << a
        pref = (1 << (a + 1)) - 2
        m = mer_special(a)
        got = from_mer(a)
        mer_iso = [j for j in range(0, 2 * nm + 1) if isolated_one(nm, j)]
        mer_r3 = [(s, r) for s, r in g_runs(nm) if r == 3]
        tri_iso = [j for j in range(0, 2 * nt + 1) if isolated_one(nt, j)]
        tri_r3 = [(s, r) for s, r in g_runs(nt) if r == 3]
        if m > pref:
            return {"ok": False, "off_pref": True, "a": a, "m": m, "pref_max": pref}
        if G(nm, m) != G(nt, m):
            return {"ok": False, "kp": True, "a": a, "m": m}
        if a % 2 == 0:
            if mer_iso != [nm] or mer_r3 != [] or mer_iso != [m]:
                return {"ok": False, "mer_even": True, "a": a, "iso": mer_iso}
            if got != want_iso(a) or got != [U - 1, 3 * U - 1, 5 * U - 1]:
                return {"ok": False, "tri_even": True, "a": a, "got": got}
            if tri_iso != got or tri_r3 != []:
                return {"ok": False, "match_even": True, "a": a, "iso": tri_iso}
        else:
            if mer_r3 != [(nm - 1, 3)] or mer_iso != [] or mer_r3 != [(m, 3)]:
                return {"ok": False, "mer_odd": True, "a": a, "r3": mer_r3}
            if got != [s for s, _ in want_r3(a)] or got != [U - 2, 3 * U - 2, 5 * U - 2]:
                return {"ok": False, "tri_odd": True, "a": a, "got": got}
            if [s for s, _ in tri_r3] != got or tri_iso != []:
                return {"ok": False, "match_odd": True, "a": a, "r3": tri_r3}
        rows[str(a)] = {
            "nm": nm,
            "nt": nt,
            "mer_special": m,
            "from_mer": got,
            "prefix": pref,
        }
        n_ok += 1
    ok = (
        n_ok == 9
        and rows["0"]["from_mer"] == [0, 2, 4]
        and rows["1"]["from_mer"] == [0, 4, 8]
        and rows["2"]["from_mer"] == [3, 11, 19]
        and rows["2"]["mer_special"] == 3
        and rows["3"]["from_mer"] == [6, 22, 38]
        and mer_special(4) == 15
        and from_mer(8) == [255, 767, 1279]
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_prefix_only() -> dict:
    """Tri specials are only the KP prefix copy: a=2 has three."""
    got = from_mer(2)
    ok = got == [3, 11, 19] and len(got) == 3 and got[0] == mer_special(2)
    return {"ok": ok, "a": 2, "got": got}


def killed_no_centre() -> dict:
    """Tri specials omit the centre: a=2 includes n=11."""
    nt = tri_n(2)
    ok = nt in from_mer(2) and nt == 11
    return {"ok": ok, "a": 2, "n": nt}


def killed_mer_off_prefix() -> dict:
    """Mersenne special sits off the KP prefix: a=2 is U-1=3 <= 6."""
    a = 2
    m = mer_special(a)
    pref = (1 << (a + 1)) - 2
    ok = m == 3 and m <= pref and G(mer_n(a), m) == G(tri_n(a), m) == 1
    return {"ok": ok, "a": a, "m": m, "pref": pref}


def killed_odd_not_mer() -> dict:
    """Odd-a run-3s are not mer+dual+centre: a=1 is 0,4,8."""
    got = from_mer(1)
    ok = got == [0, 4, 8] and got[0] == mer_special(1) == 0
    return {"ok": ok, "a": 1, "got": got}


def prefixes() -> dict:
    kz = json.loads(KZ_JSON.read_text())
    ok = (
        kz["checks"]["all_ok"]
        and kz["verdict"]["tri_three_iso"] == "LEMMA"
        and kz["verdict"]["mersenne_centre_iso"] == "LEMMA"
        and kz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert mer_special(0) == 0
    assert mer_special(5) == 30
    assert pal_col(11, 3) == 19
    assert pal_r3_start(5, 0) == 8
    assert tri_n(4) == 47
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mer_tri_table()
    sc = g4_xor_cover()
    k0 = killed_prefix_only()
    k1 = killed_no_centre()
    k2 = killed_mer_off_prefix()
    k3 = killed_odd_not_mer()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mer_tri_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_prefix_only": {k: k0[k] for k in k0 if k != "ok"},
        "killed_no_centre": {k: k1[k] for k in k1 if k != "ok"},
        "killed_mer_off_prefix": {k: k2[k] for k in k2 if k != "ok"},
        "killed_odd_not_mer": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "tri_from_mer": True,
            "tri_three_iso": True,
            "mersenne_centre_iso": True,
            "prefix_only": False,
            "no_centre": False,
            "mer_off_prefix": False,
            "odd_not_mer": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "tri_from_mer": "LEMMA",
            "tri_three_iso": "LEMMA",
            "mersenne_centre_iso": "LEMMA",
            "prefix_only": "KILLED",
            "no_centre": "KILLED",
            "mer_off_prefix": "KILLED",
            "odd_not_mer": "KILLED",
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
    print("mer_tri_table n_ok", dump["mer_tri_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_prefix_only", dump["killed_prefix_only"])
    print("killed_no_centre", dump["killed_no_centre"])
    print("killed_mer_off_prefix", dump["killed_mer_off_prefix"])
    print("killed_odd_not_mer", dump["killed_odd_not_mer"])


if __name__ == "__main__":
    main()
