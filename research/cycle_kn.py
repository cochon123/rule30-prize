#!/usr/bin/env python3
"""Cycle KN: G(3*2^a-1, d) is the AN cube divided by 1+x+x^2.

For U=2^a and n=3U-1, G(n,d) equals XOR of f_mod3(d-rU) over
r in {0,1,3,5,6}, with f_mod3(t)=1 iff t>=0 and t%3 != 2. The 6U
term vanishes on the row (d<=6U-2). Not f(d) alone; not the 2U
freshman term; not Mersenne G(2^a-1,d); not zeros at min(j,2n-j)%3==2.
This is Green-only, not J. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_kn.py --certify
Dump: research/cycle_kn.json
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
from cycle_an import G_mersenne, f_mod3
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_km import has_00

OUT = Path(__file__).resolve().with_suffix(".json")
KM_JSON = Path(__file__).resolve().parent / "cycle_km.json"

A_MAX = 8
TRI_SHIFTS = (0, 1, 3, 5, 6)
ROW_SHIFTS = (0, 1, 3, 5)


def g_tri(a: int, d: int) -> int:
    """G(3*2^a-1, d) from AN's (1+x^U+x^{3U}+x^{5U}+x^{6U})/(1+x+x^2)."""
    U = 1 << a
    acc = 0
    for r in TRI_SHIFTS:
        acc ^= f_mod3(d - r * U)
    return acc


def g_tri_row(a: int, d: int) -> int:
    """In-range form: the 6U term is off the row d<=6U-2."""
    U = 1 << a
    acc = 0
    for r in ROW_SHIFTS:
        acc ^= f_mod3(d - r * U)
    return acc


def g_tri_2U(a: int, d: int) -> int:
    """Wrong formula that keeps the cancelled x^{2U} freshman term."""
    U = 1 << a
    acc = 0
    for r in (0, 1, 2, 3, 5, 6):
        acc ^= f_mod3(d - r * U)
    return acc


def mer_mod3_zero(n: int, j: int) -> bool:
    """Mersenne palindrome zero: min(j, 2n-j) % 3 == 2."""
    return min(j, 2 * n - j) % 3 == 2


def tri_table() -> dict:
    """a<=8: G(3*2^a-1,d)=g_tri=g_tri_row; no 00; 6U term off-row."""
    n_a = n_ok = n_no00 = 0
    ns = []
    wts = []
    for a in range(0, A_MAX + 1):
        U = 1 << a
        n = 3 * U - 1
        ns.append(n)
        n_g1 = 0
        for d in range(0, 2 * n + 1):
            got = G(n, d)
            pred = g_tri(a, d)
            row = g_tri_row(a, d)
            if pred != got or row != got:
                return {
                    "ok": False,
                    "g": True,
                    "a": a,
                    "n": n,
                    "d": d,
                    "got": got,
                    "pred": pred,
                    "row": row,
                }
            if d - 6 * U >= 0:
                return {"ok": False, "six": True, "a": a, "d": d}
            n_g1 += got
            n_ok += 1
        if n_g1 != g_wt(n):
            return {"ok": False, "wt": True, "a": a, "n": n, "got": n_g1, "want": g_wt(n)}
        if has_00(n):
            return {"ok": False, "00": True, "a": a, "n": n}
        n_no00 += 1
        wts.append(n_g1)
        n_a += 1
    ok = (
        n_a == A_MAX + 1
        and n_no00 == A_MAX + 1
        and ns[0] == 2
        and ns[1] == 5
        and ns[8] == 767
        and wts[0] == 3
        and wts[1] == 9
        and wts[2] == 15
        and not has_00(5)
        and has_00(9)
        and g_tri(1, 3) == 0
        and G(5, 3) == 0
        and g_tri(0, 1) == 0
        and G(2, 1) == 0
    )
    return {
        "ok": ok,
        "n_a": n_a,
        "n_ok": n_ok,
        "n_no00": n_no00,
        "n": ns,
        "g_wt": wts,
    }


def killed_f_only() -> dict:
    """G(3*2^a-1,d)=f_mod3(d): n=5 d=2 is 1, f(2)=0."""
    a, d = 1, 2
    n = 3 * (1 << a) - 1
    got, f = G(n, d), f_mod3(d)
    ok = n == 5 and got == 1 and f == 0 and got != f and g_tri(a, d) == 1
    return {"ok": ok, "n": n, "d": d, "G": got, "f": f}


def killed_with_2U() -> dict:
    """Formula includes the cancelled x^{2U} term: n=5 d=4 is 1 vs 0."""
    a, d = 1, 4
    n = 3 * (1 << a) - 1
    got, wrong = G(n, d), g_tri_2U(a, d)
    ok = n == 5 and got == 1 and wrong == 0 and got != wrong and g_tri(a, d) == 1
    return {"ok": ok, "n": n, "d": d, "G": got, "with_2U": wrong}


def killed_eq_mersenne() -> dict:
    """Equals Mersenne G(2^a-1,d): n=5 d=4 is 1, G_mersenne(1,4)=0."""
    a, d = 1, 4
    n = 3 * (1 << a) - 1
    got, mer = G(n, d), G_mersenne(a, d)
    ok = n == 5 and got == 1 and mer == 0 and got != mer
    return {"ok": ok, "n": n, "d": d, "G": got, "mersenne": mer}


def killed_eq_mer_mod3() -> dict:
    """Zeros iff min(j,2n-j)%3==2: n=5 d=2 has G=1 but min=2."""
    n, d = 5, 2
    got = G(n, d)
    mz = mer_mod3_zero(n, d)
    ok = got == 1 and mz and g_tri(1, d) == 1
    return {"ok": ok, "n": n, "d": d, "G": got, "mer_zero": mz}


def prefixes() -> dict:
    km = json.loads(KM_JSON.read_text())
    ok = (
        km["checks"]["all_ok"]
        and km["verdict"]["odd_no00_char"] == "LEMMA"
        and km["verdict"]["odd_no00_family"] == "LEMMA"
        and km["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert g_tri(1, 0) == g_tri_row(1, 0) == G(5, 0) == 1
    assert TRI_SHIFTS == (0, 1, 3, 5, 6)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = tri_table()
    sc = g4_xor_cover()
    k0 = killed_f_only()
    k1 = killed_with_2U()
    k2 = killed_eq_mersenne()
    k3 = killed_eq_mer_mod3()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "tri_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_f_only": {k: k0[k] for k in k0 if k != "ok"},
        "killed_with_2U": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_mersenne": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_mer_mod3": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "g_tri_closed": True,
            "g_tri_row_no6U": True,
            "odd_no00_char": True,
            "odd_no00_family": True,
            "g_tri_eq_f": False,
            "g_tri_with_2U": False,
            "g_tri_eq_mersenne": False,
            "g_tri_eq_mer_mod3": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g_tri_closed": "LEMMA",
            "g_tri_row_no6U": "LEMMA",
            "odd_no00_char": "LEMMA",
            "odd_no00_family": "LEMMA",
            "g_tri_eq_f": "KILLED",
            "g_tri_with_2U": "KILLED",
            "g_tri_eq_mersenne": "KILLED",
            "g_tri_eq_mer_mod3": "KILLED",
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
    print("tri_table", dump["tri_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_f_only", dump["killed_f_only"])
    print("killed_with_2U", dump["killed_with_2U"])
    print("killed_eq_mersenne", dump["killed_eq_mersenne"])
    print("killed_eq_mer_mod3", dump["killed_eq_mer_mod3"])


if __name__ == "__main__":
    main()
