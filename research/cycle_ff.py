#!/usr/bin/env python3
"""Cycle FF: Green translation G(n+q*2^a, d+q*2^a)=G(n,d) for n<2^{a-1}.

Freshman: (1+x+x^2)^{q 2^a} = Q_q(x^{2^a}) with Q_q=(1+x+x^2)^q.
The coefficient of x^{q 2^a} is G(q,q)=1. Hence

    G(n+q*2^a, d+q*2^a)
    = XOR_{i: G(q,i)=1} G(n, d+(q-i)*2^a).

If n<2^{a-1} and 0<=d<=2n then 2n<2^a, so every i!=q shifts d off
the support [0,2n] and only i=q survives. Thus
G(n+q*2^a, d+q*2^a)=G(n,d). This is the q=1 2^a-shift and the q=3
12U-shift used to compare covering targets. Kills: n<2^a (cex n=2^{a-1}).
Do not claim J6=J10=0 implies J18=1 for all k; do not claim covering
never-fail; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_ff.py --certify
Dump: research/cycle_ff.json
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
AL_JSON = Path(__file__).resolve().parent / "cycle_al.json"
AI_JSON = Path(__file__).resolve().parent / "cycle_ai.json"
FE_JSON = Path(__file__).resolve().parent / "cycle_fe.json"


def diag_one(nmax: int = 256) -> dict:
    """G(n,n)=1 for every n."""
    n_ok = 0
    for n in range(nmax):
        if G(n, n) != 1:
            return {"ok": False, "n": n}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def translation(amax: int = 8, qmax: int = 6) -> dict:
    """G(n+q*2^a, d+q*2^a)=G(n,d) on n<2^{a-1}, d in [0,2n]."""
    n_ok = 0
    by_a: dict[str, int] = {}
    for a in range(1, amax + 1):
        nmax = 1 << (a - 1)
        ok_a = 0
        for q in range(1, qmax + 1):
            shift = q << a
            for n in range(nmax):
                for d in range(2 * n + 1):
                    if G(n + shift, d + shift) != G(n, d):
                        return {"ok": False, "a": a, "q": q, "n": n, "d": d}
                    n_ok += 1
                    ok_a += 1
        by_a[str(a)] = ok_a
    return {"ok": n_ok > 0, "n_ok": n_ok, "amax": amax, "qmax": qmax, "by_a": by_a}


def killed_n_lt_2a() -> dict:
    """n<2^a is false: a=4, n=8=2^{a-1}, d=0."""
    a = 4
    n = 1 << (a - 1)
    d = 0
    shift = 1 << a
    g0 = G(n, d)
    g1 = G(n + shift, d + shift)
    ok = g0 != g1 and g0 == 1 and g1 == 0 and n < (1 << a)
    return {"ok": ok, "a": a, "n": n, "d": d, "G_n": g0, "G_shifted": g1}


def prefixes() -> dict:
    al = json.loads(AL_JSON.read_text())
    ai = json.loads(AI_JSON.read_text())
    fe = json.loads(FE_JSON.read_text())
    ok = (
        al["checks"]["all_ok"]
        and ai["checks"]["all_ok"]
        and fe["checks"]["all_ok"]
        and al["verdict"]["all_q_identity"] == "LEMMA"
        and ai["verdict"]["dyadic_step"] == "LEMMA"
        and fe["verdict"]["cover_fails_iff_J6_J10_J18_vanish"] == "LEMMA"
        and fe["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, diag: dict, trans: dict, killed: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert diag["ok"] and trans["ok"] and killed["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    diag = diag_one()
    trans = translation()
    killed = killed_n_lt_2a()
    pref = prefixes()
    checks = self_checks(c20, diag, trans, killed, pref)
    dump = {
        "cycle": "FF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "diag": {k: diag[k] for k in diag if k != "ok"},
        "translation": {k: trans[k] for k in trans if k != "ok"},
        "killed": {k: killed[k] for k in killed if k != "ok"},
        "lemmas": {
            "G_nn_eq_1": True,
            "G_shift_q_2a_n_lt_2a_minus_1": True,
            "G_shift_n_lt_2a": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_nn_eq_1": "LEMMA",
            "G_shift_q_2a_n_lt_2a_minus_1": "LEMMA",
            "G_shift_n_lt_2a": "KILLED",
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
    print("diag", dump["diag"])
    print("translation", dump["translation"])
    print("killed", dump["killed"])


if __name__ == "__main__":
    main()
