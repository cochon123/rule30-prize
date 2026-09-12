#!/usr/bin/env python3
"""Cycle KK: Green weight is the product of binary 1-run Mersenne weights.

g_wt(n) equals the product over binary ones-runs of length L of
a_L=g_wt(2^L-1)=(2^{L+2} - (-1)^L)/3. No-adjacent-ones n have
g_wt=3^{popcount(n)}. Weight is not 3^{popcount} for all n; not the
sum of run weights; a_L is not 2^{L+1}-1. This is Green-only, not J.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kk.py --certify
Dump: research/cycle_kk.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
KJ_JSON = Path(__file__).resolve().parent / "cycle_kj.json"

N_ALG = 256
L_ALG = 12


def bin_one_runs(n: int) -> list:
    """Lengths of consecutive binary 1-runs in n, low bits first."""
    out = []
    while n:
        if n & 1:
            length = 0
            while n & 1:
                length += 1
                n >>= 1
            out.append(length)
        else:
            n >>= 1
    return out


def mersenne_a(L: int) -> int:
    """Closed form g_wt(2^L-1) = (2^{L+2} - (-1)^L) / 3."""
    pm = 1 if L % 2 == 0 else -1
    return ((1 << (L + 2)) - pm) // 3


def g_wt_prod(n: int) -> int:
    """Product of mersenne_a(L) over binary 1-runs of n."""
    prod = 1
    for length in bin_one_runs(n):
        prod *= mersenne_a(length)
    return prod


def wt_prod_table() -> dict:
    """n<256: g_wt equals the binary 1-run product; a_L matches Mersenne rows."""
    n_ok = n_no11 = n_adj = 0
    for L in range(0, L_ALG):
        got = g_wt((1 << L) - 1) if L < 10 else None
        want = mersenne_a(L)
        if L >= 2 and mersenne_a(L) != mersenne_a(L - 1) + 2 * mersenne_a(L - 2):
            return {"ok": False, "rec": True, "L": L}
        if L < 10 and got != want:
            return {"ok": False, "mersenne": True, "L": L, "got": got, "want": want}
    for n in range(0, N_ALG):
        got = g_wt(n)
        want = g_wt_prod(n)
        if got != want:
            return {"ok": False, "prod": True, "n": n, "got": got, "want": want}
        pc = bin(n).count("1")
        no11 = (n & (n << 1)) == 0
        if no11:
            n_no11 += 1
            if got != 3**pc:
                return {"ok": False, "no11": True, "n": n, "got": got, "want": 3**pc}
        else:
            n_adj += 1
            if got >= 3**pc:
                return {"ok": False, "adj": True, "n": n, "got": got, "pc3": 3**pc}
        n_ok += 1
    ok = (
        n_ok == N_ALG
        and n_no11 + n_adj == N_ALG
        and n_no11 == 55
        and g_wt_prod(0) == 1
        and g_wt_prod(1) == 3
        and g_wt_prod(3) == 5
        and g_wt_prod(11) == 15
        and mersenne_a(0) == 1
        and mersenne_a(1) == 3
        and mersenne_a(2) == 5
        and mersenne_a(3) == 11
        and bin_one_runs(0) == []
        and bin_one_runs(11) == [2, 1]
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_no11": n_no11,
        "n_adj": n_adj,
        "a": [mersenne_a(L) for L in range(0, 9)],
    }


def killed_all_3pc() -> dict:
    """g_wt is 3^{popcount} for all n: n=3 has weight 5, not 9."""
    n = 3
    got, want = g_wt(n), 3 ** bin(n).count("1")
    ok = got == 5 and want == 9 and got != want and (n & (n << 1)) != 0
    return {"ok": ok, "n": n, "g_wt": got, "three_pc": want, "runs": bin_one_runs(n)}


def killed_sum_runs() -> dict:
    """g_wt is the sum of run weights: n=11=1011 is 5*3=15, not 5+3=8."""
    n = 11
    runs = bin_one_runs(n)
    parts = [mersenne_a(L) for L in runs]
    ok = (
        runs == [2, 1]
        and parts == [5, 3]
        and g_wt(n) == 15
        and sum(parts) == 8
        and g_wt(n) != sum(parts)
    )
    return {"ok": ok, "n": n, "runs": runs, "parts": parts, "g_wt": g_wt(n)}


def killed_mersenne_ones() -> dict:
    """a_L is 2^{L+1}-1: L=3 gives 15, but g_wt(7)=11."""
    L = 3
    got, bad = mersenne_a(L), (1 << (L + 1)) - 1
    ok = got == 11 and bad == 15 and g_wt(7) == 11 and got != bad
    return {"ok": ok, "L": L, "a": got, "ones": bad, "n": 7}


def killed_times3() -> dict:
    """g_wt(2m+1) is always 3 g_wt(m): n=3 is 5, not 3*3=9."""
    m, n = 1, 3
    ok = g_wt(n) == 5 and 3 * g_wt(m) == 9 and g_wt(n) != 3 * g_wt(m)
    return {"ok": ok, "m": m, "n": n, "g_wt_n": g_wt(n), "three_parent": 3 * g_wt(m)}


def prefixes() -> dict:
    kj = json.loads(KJ_JSON.read_text())
    ok = (
        kj["checks"]["all_ok"]
        and kj["verdict"]["n_runs_eq_parent_wt"] == "LEMMA"
        and kj["verdict"]["g_wt_even_copy"] == "LEMMA"
        and kj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert g_wt_prod(21) == 27 and g_wt(21) == 27
    assert g_wt_prod(27) == 25 and bin_one_runs(27) == [2, 2]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = wt_prod_table()
    sc = g4_xor_cover()
    k0 = killed_all_3pc()
    k1 = killed_sum_runs()
    k2 = killed_mersenne_ones()
    k3 = killed_times3()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "wt_prod_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_3pc": {k: k0[k] for k in k0 if k != "ok"},
        "killed_sum_runs": {k: k1[k] for k in k1 if k != "ok"},
        "killed_mersenne_ones": {k: k2[k] for k in k2 if k != "ok"},
        "killed_times3": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "g_wt_run_product": True,
            "mersenne_a_closed": True,
            "no11_three_pc": True,
            "n_runs_eq_parent_wt": True,
            "all_3pc": False,
            "sum_run_weights": False,
            "a_L_ones": False,
            "odd_always_3parent": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g_wt_run_product": "LEMMA",
            "mersenne_a_closed": "LEMMA",
            "no11_three_pc": "LEMMA",
            "n_runs_eq_parent_wt": "LEMMA",
            "all_3pc": "KILLED",
            "sum_run_weights": "KILLED",
            "a_L_ones": "KILLED",
            "odd_always_3parent": "KILLED",
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
    print("wt_prod_table", dump["wt_prod_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_3pc", dump["killed_all_3pc"])
    print("killed_sum_runs", dump["killed_sum_runs"])
    print("killed_mersenne_ones", dump["killed_mersenne_ones"])
    print("killed_times3", dump["killed_times3"])


if __name__ == "__main__":
    main()
