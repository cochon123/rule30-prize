#!/usr/bin/env python3
"""Cycle KW: family clip left/right counts are equal except q=10 max Mersenne.

k<=10: clipped isolated-pair left and right counts are equal on q=6
max Mersenne and q=10 3U-1. The q=10 max Mersenne has one extra right
((c-1)/2 left, (c+1)/2 right with c=2^{k+1}-1). Not mer10 balanced;
not extra left; not q=6 unbalanced; not tri extra right. This is
covering geometry, not packed AND XOR J. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kw.py --certify
Dump: research/cycle_kw.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_kr import want_clippers
from cycle_ks import clip_counts
from cycle_kt import clip_js
from cycle_kv import G4_LEFT, G4_RIGHT, clip_g4_shape

OUT = Path(__file__).resolve().with_suffix(".json")
KV_JSON = Path(__file__).resolve().parent / "cycle_kv.json"

K_MAX = 10


def want_clip_lr(k: int, q: int, n: int) -> tuple[int, int]:
    """(n_left, n_right) of clipped family G=1 on clipper n."""
    ns = want_clippers(k, q)
    if n not in ns:
        return (0, 0)
    c = clip_counts(k, q)[ns.index(n)]
    if q == 10 and n == (1 << (k + 2)) - 1:
        return (c - 1) // 2, (c + 1) // 2
    return c // 2, c // 2


def got_clip_lr(k: int, q: int, n: int) -> tuple[int, int]:
    """Count left/right from clip_g4_shape on clip_js."""
    n_l = n_r = 0
    for j in clip_js(k, q, n):
        g4 = clip_g4_shape(n, j)
        if g4 == G4_LEFT:
            n_l += 1
        elif g4 == G4_RIGHT:
            n_r += 1
        else:
            return (-1, -1)
    return (n_l, n_r)


def clip_lr_table() -> dict:
    """k<=10: got_clip_lr matches want_clip_lr on every family clipper."""
    rows = {}
    n_ok = 0
    for k in range(0, K_MAX + 1):
        krow = {}
        for q in (6, 10):
            recs = []
            for n in want_clippers(k, q):
                got = got_clip_lr(k, q, n)
                want = want_clip_lr(k, q, n)
                if got != want:
                    return {
                        "ok": False,
                        "lr": True,
                        "k": k,
                        "q": q,
                        "n": n,
                        "got": list(got),
                        "want": list(want),
                    }
                recs.append({"n": n, "lr": list(got)})
                n_ok += 1
            krow[f"q{q}"] = recs
        rows[str(k)] = krow
    ok = (
        n_ok == 29
        and rows["0"]["q6"] == []
        and rows["0"]["q10"][0]["lr"] == [0, 1]
        and rows["2"]["q6"][0]["lr"] == [1, 1]
        and rows["2"]["q10"][0]["lr"] == [1, 1]
        and rows["2"]["q10"][1]["lr"] == [3, 4]
        and rows["6"]["q10"][1]["lr"] == [63, 64]
        and want_clip_lr(4, 6, 31) == (5, 5)
        and want_clip_lr(1, 10, 7) == (1, 2)
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_mer10_bal() -> dict:
    """q=10 max Mersenne is balanced: k=0 n=3 is 0 left, 1 right."""
    got = want_clip_lr(0, 10, 3)
    ok = got == (0, 1) and got[0] != got[1]
    return {"ok": ok, "k": 0, "q": 10, "n": 3, "lr": list(got)}


def killed_extra_left() -> dict:
    """The mer10 extra is a left: k=0 n=3 extra is a right."""
    got = want_clip_lr(0, 10, 3)
    ok = got == (0, 1) and got[1] == got[0] + 1
    return {"ok": ok, "k": 0, "q": 10, "n": 3, "lr": list(got)}


def killed_q6_unbal() -> dict:
    """q=6 max Mersenne is unbalanced: k=2 n=7 is 1,1."""
    got = want_clip_lr(2, 6, 7)
    ok = got == (1, 1) and got[0] == got[1]
    return {"ok": ok, "k": 2, "q": 6, "n": 7, "lr": list(got)}


def killed_tri_extra() -> dict:
    """q=10 3U-1 has an extra right: k=2 n=11 is 1,1."""
    got = want_clip_lr(2, 10, 11)
    ok = got == (1, 1) and got[0] == got[1]
    return {"ok": ok, "k": 2, "q": 10, "n": 11, "lr": list(got)}


def prefixes() -> dict:
    kv = json.loads(KV_JSON.read_text())
    ok = (
        kv["checks"]["all_ok"]
        and kv["verdict"]["family_clip_iso2"] == "LEMMA"
        and kv["verdict"]["family_clip_g4"] == "LEMMA"
        and kv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_clip_lr(0, 6, 1) == (0, 0)
    assert want_clip_lr(5, 10, 127) == (31, 32)
    assert got_clip_lr(3, 6, 15) == (2, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_lr_table()
    sc = g4_xor_cover()
    k0 = killed_mer10_bal()
    k1 = killed_extra_left()
    k2 = killed_q6_unbal()
    k3 = killed_tri_extra()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_lr_table": {
            "n_ok": rt["n_ok"],
            "rows": {
                k: {q: recs for q, recs in krow.items()} for k, krow in rt["rows"].items()
            },
        },
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_mer10_bal": {k: k0[k] for k in k0 if k != "ok"},
        "killed_extra_left": {k: k1[k] for k in k1 if k != "ok"},
        "killed_q6_unbal": {k: k2[k] for k in k2 if k != "ok"},
        "killed_tri_extra": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clip_lr": True,
            "family_clip_iso2": True,
            "family_clip_g4": True,
            "mer10_balanced": False,
            "extra_is_left": False,
            "q6_unbalanced": False,
            "tri_extra_right": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clip_lr": "LEMMA",
            "family_clip_iso2": "LEMMA",
            "family_clip_g4": "LEMMA",
            "mer10_balanced": "KILLED",
            "extra_is_left": "KILLED",
            "q6_unbalanced": "KILLED",
            "tri_extra_right": "KILLED",
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
    print("clip_lr_table n_ok", dump["clip_lr_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_mer10_bal", dump["killed_mer10_bal"])
    print("killed_extra_left", dump["killed_extra_left"])
    print("killed_q6_unbal", dump["killed_q6_unbal"])
    print("killed_tri_extra", dump["killed_tri_extra"])


if __name__ == "__main__":
    main()
