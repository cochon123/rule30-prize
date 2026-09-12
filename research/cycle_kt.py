#!/usr/bin/env python3
"""Cycle KT: clipped G=1 of family clippers is the palindrome dual of f_mod3.

Covering k<=6: on each family clipper, clipped G=1 columns are
j = 2n-d for d in a low prefix with d not 2 mod 3 (q=6 max Mersenne
and q=10 3U-1: d<U-2; q=10 max Mersenne: d<3U-2). Not every j>T/2;
not a suffix of the row; not the q=6 dual on q=10 max Mersenne; not
a single residue mod 3. This is covering geometry, not packed AND
XOR J. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_kt.py --certify
Dump: research/cycle_kt.json
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
from cycle_an import f_mod3
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_kr import want_clippers
from cycle_ks import clip_counts

OUT = Path(__file__).resolve().with_suffix(".json")
KS_JSON = Path(__file__).resolve().parent / "cycle_ks.json"


def clipped_g1(n: int, T: int) -> tuple[int, ...]:
    """G=1 columns with packed index p=T-2j < 0."""
    return tuple(j for j in range(0, 2 * n + 1) if T - 2 * j < 0 and G(n, j))


def clip_js(k: int, q: int, n: int) -> tuple[int, ...]:
    """Predicted clipped G=1 of family clipper n on covering (k,q)."""
    U = 1 << k
    if q == 6 and k >= 2 and n == (1 << (k + 1)) - 1:
        dual, hi = 4 * U - 2, U - 2
    elif q == 10 and n == (1 << (k + 2)) - 1:
        dual, hi = 8 * U - 2, 3 * U - 2
    elif q == 10 and k >= 2 and n == 3 * U - 1:
        dual, hi = 6 * U - 2, U - 2
    else:
        return ()
    return tuple(sorted(dual - d for d in range(0, hi) if f_mod3(d)))


def clip_js_table() -> dict:
    """Covering k<=6: clipped_g1 matches clip_js on every family clipper."""
    rows = {}
    n_ok = 0
    for k in range(0, 7):
        krow = {}
        for q in (6, 10):
            U = 1 << k
            T = q * U
            ns = want_clippers(k, q)
            counts = clip_counts(k, q)
            recs = []
            for i, n in enumerate(ns):
                got = clipped_g1(n, T)
                want = clip_js(k, q, n)
                if got != want:
                    return {
                        "ok": False,
                        "set": True,
                        "k": k,
                        "q": q,
                        "n": n,
                        "got": list(got),
                        "want": list(want),
                    }
                if len(got) != counts[i]:
                    return {
                        "ok": False,
                        "cnt": True,
                        "k": k,
                        "q": q,
                        "n": n,
                        "len": len(got),
                        "want": counts[i],
                    }
                recs.append({"n": n, "js": list(got), "clip": len(got)})
                n_ok += 1
            krow[f"q{q}"] = {"T": T, "n": recs}
        rows[str(k)] = krow
    ok = (
        n_ok == 17
        and rows["0"]["q6"]["n"] == []
        and rows["0"]["q10"]["n"][0]["js"] == [6]
        and rows["2"]["q6"]["n"][0]["js"] == [13, 14]
        and rows["2"]["q10"]["n"][0]["js"] == [21, 22]
        and rows["2"]["q10"]["n"][1]["js"] == [21, 23, 24, 26, 27, 29, 30]
        and clip_js(1, 6, 3) == ()
        and clip_js(4, 6, 31) == clipped_g1(31, 96)
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_all_high() -> dict:
    """Every j>T/2 on a clipper is G=1: k=3 q=6 n=15 has zeros at 25,28."""
    n, T = 15, 48
    high = [j for j in range(25, 31)]
    zeros = [j for j in high if G(n, j) == 0]
    ok = clipped_g1(n, T) == (26, 27, 29, 30) and zeros == [25, 28]
    return {"ok": ok, "k": 3, "q": 6, "n": n, "high": high, "zeros": zeros}


def killed_suffix() -> dict:
    """Clipped ones are a suffix of the row: k=2 q=10 n=15 last 7 is 24..30."""
    n, T = 15, 40
    got = clipped_g1(n, T)
    suffix = tuple(range(24, 31))
    ok = got == (21, 23, 24, 26, 27, 29, 30) and got != suffix
    return {"ok": ok, "k": 2, "q": 10, "n": n, "got": list(got), "suffix": list(suffix)}


def killed_q10_q6_dual() -> dict:
    """q=10 max Mersenne uses the q=6 dual 4U-2: k=2 n=15 would be 13,14."""
    U, n = 4, 15
    wrong = tuple(sorted(4 * U - 2 - d for d in range(0, U - 2) if f_mod3(d)))
    got = clip_js(2, 10, n)
    ok = wrong == (13, 14) and got == (21, 23, 24, 26, 27, 29, 30) and got != wrong
    return {"ok": ok, "k": 2, "q": 10, "n": n, "wrong": list(wrong), "got": list(got)}


def killed_one_res() -> dict:
    """Clipped j share a single residue mod 3: k=2 q=6 is 13,14."""
    got = clip_js(2, 6, 7)
    res = {j % 3 for j in got}
    ok = got == (13, 14) and len(res) == 2
    return {"ok": ok, "k": 2, "q": 6, "js": list(got), "res": sorted(res)}


def prefixes() -> dict:
    ks = json.loads(KS_JSON.read_text())
    ok = (
        ks["checks"]["all_ok"]
        and ks["verdict"]["family_clip_counts"] == "LEMMA"
        and ks["verdict"]["family_clippers"] == "LEMMA"
        and ks["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert covering_Q(6) == 2 and covering_Q(10) == 4
    assert clip_js(0, 10, 3) == (6,)
    assert clip_js(6, 6, 127) == clipped_g1(127, 384)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_js_table()
    sc = g4_xor_cover()
    k0 = killed_all_high()
    k1 = killed_suffix()
    k2 = killed_q10_q6_dual()
    k3 = killed_one_res()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_js_table": {
            "n_ok": rt["n_ok"],
            "rows": {
                k: {
                    q: {
                        "T": rec["T"],
                        "n": [{"n": x["n"], "clip": x["clip"]} for x in rec["n"]],
                    }
                    for q, rec in krow.items()
                }
                for k, krow in rt["rows"].items()
            },
        },
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_high": {k: k0[k] for k in k0 if k != "ok"},
        "killed_suffix": {k: k1[k] for k in k1 if k != "ok"},
        "killed_q10_q6_dual": {k: k2[k] for k in k2 if k != "ok"},
        "killed_one_res": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clip_js": True,
            "family_clip_counts": True,
            "family_clippers": True,
            "clip_all_high": False,
            "clip_suffix": False,
            "q10_uses_q6_dual": False,
            "clip_one_res": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clip_js": "LEMMA",
            "family_clip_counts": "LEMMA",
            "family_clippers": "LEMMA",
            "clip_all_high": "KILLED",
            "clip_suffix": "KILLED",
            "q10_uses_q6_dual": "KILLED",
            "clip_one_res": "KILLED",
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
    print("clip_js_table n_ok", dump["clip_js_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_high", dump["killed_all_high"])
    print("killed_suffix", dump["killed_suffix"])
    print("killed_q10_q6_dual", dump["killed_q10_q6_dual"])
    print("killed_one_res", dump["killed_one_res"])


if __name__ == "__main__":
    main()
