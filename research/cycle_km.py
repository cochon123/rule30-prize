#!/usr/bin/env python3
"""Cycle KM: odd Green rows have no 00 iff Mersenne or 3*2^k-1.

Odd n has no consecutive Green zeros iff g_wt(n//2)+g_wt(n//4)=2(n//2+1).
For n<256 those n are 2^k-1 or 3*2^k-1. Even n without 00 are only 0 and 2.
Not all odd n; not all fibbinary; not all even n. This is Green-only, not
J. Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_km.py --certify
Dump: research/cycle_km.json
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
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_kk import bin_one_runs

OUT = Path(__file__).resolve().with_suffix(".json")
KL_JSON = Path(__file__).resolve().parent / "cycle_kl.json"

N_ALG = 256
WANT_ODD = (1, 3, 5, 7, 11, 15, 23, 31, 47, 63, 95, 127, 191, 255)
WANT_EVEN = (0, 2)


def has_00(n: int) -> bool:
    """True if Green row n has two consecutive zeros."""
    prev = 1
    for j in range(0, 2 * n + 1):
        bit = G(n, j)
        if bit == 0 and prev == 0:
            return True
        prev = bit
    return False


def no00_odd_pred(n: int) -> bool:
    """Odd n has no 00 iff g_wt(m)+g_wt(m//2)=2(m+1) for m=n//2."""
    m = n // 2
    return g_wt(m) + g_wt(m // 2) == 2 * (m + 1)


def is_pow2(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def is_no00_family(n: int) -> bool:
    """n=2^k-1 or n=3*2^k-1."""
    p = n + 1
    if is_pow2(p):
        return True
    if p % 3 == 0 and is_pow2(p // 3):
        return True
    return False


def no00_table() -> dict:
    """n<256: odd no-00 iff weight pred iff Mersenne or 3*2^k-1; even only 0,2."""
    odd = []
    even = []
    for n in range(0, N_ALG):
        h = has_00(n)
        if n % 2 == 1:
            pred = no00_odd_pred(n)
            fam = is_no00_family(n)
            if h == pred:
                return {"ok": False, "char": True, "n": n, "has_00": h, "pred": pred}
            if (not h) != fam:
                return {"ok": False, "fam": True, "n": n, "has_00": h, "fam": fam}
            if not h:
                odd.append(n)
        else:
            if not h:
                even.append(n)
    ok = (
        tuple(odd) == WANT_ODD
        and tuple(even) == WANT_EVEN
        and not has_00(0)
        and not has_00(1)
        and not has_00(2)
        and has_00(4)
        and has_00(9)
        and not has_00(7)
        and not has_00(5)
        and is_no00_family(5)
        and is_no00_family(255)
        and not is_no00_family(9)
        and no00_odd_pred(7)
        and not no00_odd_pred(9)
    )
    return {
        "ok": ok,
        "n_odd": len(odd),
        "n_even": len(even),
        "odd": odd,
        "even": even,
    }


def killed_all_odd() -> dict:
    """Every odd n has no 00: n=9 is 1001 and has 00."""
    n = 9
    ok = n % 2 == 1 and has_00(n) and not no00_odd_pred(n) and not is_no00_family(n)
    return {"ok": ok, "n": n, "runs": bin_one_runs(n), "g_wt": g_wt(n)}


def killed_all_fib() -> dict:
    """Every fibbinary n has no 00: n=9=1001 has no adjacent 11 but has Green 00."""
    n = 9
    ok = (n & (n << 1)) == 0 and has_00(n) and bin_one_runs(n) == [1, 1]
    return {"ok": ok, "n": n, "runs": bin_one_runs(n)}


def killed_all_even_00() -> dict:
    """Every even n has 00: n=2 is 10101 with isolated zeros."""
    n = 2
    ok = n % 2 == 0 and not has_00(n) and g_wt(n) == 3
    return {"ok": ok, "n": n, "g_wt": g_wt(n)}


def killed_only_mersenne() -> dict:
    """Only Mersenne odd n lack 00: n=5=3*2-1 is not Mersenne."""
    n = 5
    ok = (
        not has_00(n)
        and is_no00_family(n)
        and not is_pow2(n + 1)
        and n == 3 * 2 - 1
        and g_wt(n) == 9
    )
    return {"ok": ok, "n": n, "g_wt": g_wt(n)}


def prefixes() -> dict:
    kl = json.loads(KL_JSON.read_text())
    ok = (
        kl["checks"]["all_ok"]
        and kl["verdict"]["a_L_eq_jac_Lp2"] == "LEMMA"
        and kl["verdict"]["g_wt_jac_product"] == "LEMMA"
        and kl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert not has_00(15) and has_00(27)
    assert is_no00_family(191) and not is_no00_family(27)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = no00_table()
    sc = g4_xor_cover()
    k0 = killed_all_odd()
    k1 = killed_all_fib()
    k2 = killed_all_even_00()
    k3 = killed_only_mersenne()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "no00_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_odd": {k: k0[k] for k in k0 if k != "ok"},
        "killed_all_fib": {k: k1[k] for k in k1 if k != "ok"},
        "killed_all_even_00": {k: k2[k] for k in k2 if k != "ok"},
        "killed_only_mersenne": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "odd_no00_char": True,
            "odd_no00_family": True,
            "a_L_eq_jac_Lp2": True,
            "g_wt_jac_product": True,
            "all_odd_no00": False,
            "all_fib_no00": False,
            "all_even_has00": False,
            "only_mersenne_no00": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_no00_char": "LEMMA",
            "odd_no00_family": "LEMMA",
            "a_L_eq_jac_Lp2": "LEMMA",
            "g_wt_jac_product": "LEMMA",
            "all_odd_no00": "KILLED",
            "all_fib_no00": "KILLED",
            "all_even_has00": "KILLED",
            "only_mersenne_no00": "KILLED",
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
    print("no00_table", dump["no00_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_odd", dump["killed_all_odd"])
    print("killed_all_fib", dump["killed_all_fib"])
    print("killed_all_even_00", dump["killed_all_even_00"])
    print("killed_only_mersenne", dump["killed_only_mersenne"])


if __name__ == "__main__":
    main()
