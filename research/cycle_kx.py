#!/usr/bin/env python3
"""Cycle KX: q=10 max-Mersenne extra right is the first clipped column j=5U+1.

k<=10: on n=2^{k+2}-1 the KW extra right is min(clip_js)=5*2^k+1,
green4 0110. Not the last clipped column; not j=5U (in support);
not a left; not q=6 first-clipped as an extra. This is covering
geometry, not packed AND XOR J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_kx.py --certify
Dump: research/cycle_kx.json
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
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_kt import clip_js, clipped_g1
from cycle_kv import G4_LEFT, G4_RIGHT, clip_g4_shape
from cycle_kw import got_clip_lr, want_clip_lr

OUT = Path(__file__).resolve().with_suffix(".json")
KW_JSON = Path(__file__).resolve().parent / "cycle_kw.json"

K_MAX = 10


def mer10_n(k: int) -> int:
    return (1 << (k + 2)) - 1


def mer10_extra_j(k: int) -> int:
    """First clipped column of n=2^{k+2}-1 on q=10: 5U+1."""
    return 5 * (1 << k) + 1


def extra_j_table() -> dict:
    """k<=10: mer10 extra right is min(clip_js)=5U+1; rest is balanced."""
    rows = {}
    n_ok = 0
    for k in range(0, K_MAX + 1):
        n = mer10_n(k)
        js = clip_js(k, 10, n)
        extra = mer10_extra_j(k)
        U = 1 << k
        T = 10 * U
        if not js or js[0] != extra:
            return {"ok": False, "first": True, "k": k, "got": js[0] if js else None, "want": extra}
        if clip_g4_shape(n, extra) != G4_RIGHT or G(n, extra) != 1:
            return {"ok": False, "g4": True, "k": k, "j": extra}
        if extra <= T // 2:
            return {"ok": False, "clip": True, "k": k, "j": extra, "T": T}
        rest = js[1:]
        n_l = sum(clip_g4_shape(n, j) == G4_LEFT for j in rest)
        n_r = sum(clip_g4_shape(n, j) == G4_RIGHT for j in rest)
        L, R = want_clip_lr(k, 10, n)
        if n_l != n_r or n_l != L or n_r != R - 1:
            return {
                "ok": False,
                "rest": True,
                "k": k,
                "rest": [n_l, n_r],
                "want": [L, R],
            }
        if clipped_g1(n, T) != js:
            return {"ok": False, "g1": True, "k": k}
        rows[str(k)] = {"n": n, "extra": extra, "lr": [L, R], "T": T}
        n_ok += 1
    ok = (
        n_ok == 11
        and rows["0"]["extra"] == 6
        and rows["1"]["extra"] == 11
        and rows["2"]["extra"] == 21
        and rows["6"]["extra"] == 321
        and mer10_extra_j(4) == 81
        and covering_Q(10) == 4
        and got_clip_lr(0, 10, 3) == (0, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_last() -> dict:
    """Extra is the last clipped column: k=2 n=15 last is 30, extra is 21."""
    js = clip_js(2, 10, 15)
    extra = mer10_extra_j(2)
    ok = extra == 21 and js[-1] == 30 and extra != js[-1] and js[0] == extra
    return {"ok": ok, "k": 2, "n": 15, "extra": extra, "last": js[-1]}


def killed_j5U() -> dict:
    """Extra is j=5U: k=2 U=4 j=20 is in support (p=0) and G=1."""
    k, U = 2, 4
    j = 5 * U
    extra = mer10_extra_j(k)
    T = 10 * U
    p = T - 2 * j
    ok = j == 20 and extra == 21 and p == 0 and G(15, j) == 1 and extra != j
    return {"ok": ok, "k": k, "j5U": j, "extra": extra, "p": p}


def killed_left() -> dict:
    """Extra is a left 1011: k=2 j=21 is right 0110."""
    extra = mer10_extra_j(2)
    ok = extra == 21 and clip_g4_shape(15, extra) == G4_RIGHT != G4_LEFT
    return {"ok": ok, "k": 2, "n": 15, "j": extra, "g4": list(clip_g4_shape(15, extra))}


def killed_q6_extra() -> dict:
    """q=6 first clipped is an extra: k=2 n=7 is balanced 1,1."""
    js = clip_js(2, 6, 7)
    lr = want_clip_lr(2, 6, 7)
    ok = js[0] == 13 and lr == (1, 1) and lr[0] == lr[1]
    return {"ok": ok, "k": 2, "q": 6, "n": 7, "first": js[0], "lr": list(lr)}


def prefixes() -> dict:
    kw = json.loads(KW_JSON.read_text())
    ok = (
        kw["checks"]["all_ok"]
        and kw["verdict"]["family_clip_lr"] == "LEMMA"
        and kw["verdict"]["family_clip_iso2"] == "LEMMA"
        and kw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert mer10_extra_j(0) == 6
    assert mer10_n(3) == 31
    assert clip_js(5, 10, mer10_n(5))[0] == mer10_extra_j(5)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = extra_j_table()
    sc = g4_xor_cover()
    k0 = killed_last()
    k1 = killed_j5U()
    k2 = killed_left()
    k3 = killed_q6_extra()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "extra_j_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_last": {k: k0[k] for k in k0 if k != "ok"},
        "killed_j5U": {k: k1[k] for k in k1 if k != "ok"},
        "killed_left": {k: k2[k] for k in k2 if k != "ok"},
        "killed_q6_extra": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "mer10_extra_j": True,
            "family_clip_lr": True,
            "family_clip_iso2": True,
            "extra_is_last": False,
            "extra_is_5U": False,
            "extra_is_left": False,
            "q6_first_is_extra": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mer10_extra_j": "LEMMA",
            "family_clip_lr": "LEMMA",
            "family_clip_iso2": "LEMMA",
            "extra_is_last": "KILLED",
            "extra_is_5U": "KILLED",
            "extra_is_left": "KILLED",
            "q6_first_is_extra": "KILLED",
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
    print("extra_j_table n_ok", dump["extra_j_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_last", dump["killed_last"])
    print("killed_j5U", dump["killed_j5U"])
    print("killed_left", dump["killed_left"])
    print("killed_q6_extra", dump["killed_q6_extra"])


if __name__ == "__main__":
    main()
