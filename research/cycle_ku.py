#!/usr/bin/env python3
"""Cycle KU: family clip green4 XOR is 1101/0000 or 0110/1011.

On covering family clippers, XOR of green4 over clipped G=1 is:
q=6 max Mersenne and q=10 3U-1: 1101 if k even >=2 else 0000;
q=10 max Mersenne: 0110 if k=0 else 1011. Not clip_want; not
independent of k; not mer10=mer6; not row-XOR 0111. This is covering
geometry, not packed AND XOR J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_ku.py --certify
Dump: research/cycle_ku.json
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
from cycle_hj import green4
from cycle_kh import ROW_XOR, clip_want, g4_xor_cover, xor4
from cycle_kr import want_clippers
from cycle_kt import clip_js

OUT = Path(__file__).resolve().with_suffix(".json")
KT_JSON = Path(__file__).resolve().parent / "cycle_kt.json"

K_MAX = 10
G4_EVEN = (1, 1, 0, 1)
G4_ODD = (0, 0, 0, 0)
G4_MER0 = (0, 1, 1, 0)
G4_MER = (1, 0, 1, 1)


def want_clip_g4(k: int, q: int, n: int) -> tuple[int, int, int, int]:
    """Closed-form XOR of green4 over clipped G=1 of family clipper n."""
    U = 1 << k
    if q == 6 and k >= 2 and n == (1 << (k + 1)) - 1:
        return G4_EVEN if k % 2 == 0 else G4_ODD
    if q == 10 and k >= 2 and n == 3 * U - 1:
        return G4_EVEN if k % 2 == 0 else G4_ODD
    if q == 10 and n == (1 << (k + 2)) - 1:
        return G4_MER0 if k == 0 else G4_MER
    return (0, 0, 0, 0)


def clip_g4_xor(k: int, q: int, n: int) -> tuple[int, int, int, int]:
    """XOR of green4 over clip_js(k,q,n)."""
    acc = (0, 0, 0, 0)
    for j in clip_js(k, q, n):
        acc = xor4(acc, green4(n, j))
    return acc


def clip_g4_table() -> dict:
    """k<=10: clip_g4_xor matches want_clip_g4 on every family clipper."""
    rows = {}
    n_ok = 0
    for k in range(0, K_MAX + 1):
        krow = {}
        for q in (6, 10):
            recs = []
            for n in want_clippers(k, q):
                got = clip_g4_xor(k, q, n)
                want = want_clip_g4(k, q, n)
                if got != want:
                    return {
                        "ok": False,
                        "xor": True,
                        "k": k,
                        "q": q,
                        "n": n,
                        "got": list(got),
                        "want": list(want),
                    }
                recs.append({"n": n, "xor": list(got), "clip": len(clip_js(k, q, n))})
                n_ok += 1
            krow[f"q{q}"] = recs
        rows[str(k)] = krow
    ok = (
        n_ok == 29
        and rows["0"]["q6"] == []
        and rows["0"]["q10"][0]["xor"] == [0, 1, 1, 0]
        and rows["1"]["q10"][0]["xor"] == [1, 0, 1, 1]
        and rows["2"]["q6"][0]["xor"] == [1, 1, 0, 1]
        and rows["3"]["q6"][0]["xor"] == [0, 0, 0, 0]
        and rows["2"]["q10"][0]["xor"] == [1, 1, 0, 1]
        and rows["2"]["q10"][1]["xor"] == [1, 0, 1, 1]
        and rows["10"]["q6"][0]["xor"] == [1, 1, 0, 1]
        and want_clip_g4(4, 6, 31) == G4_EVEN
        and want_clip_g4(5, 10, 95) == G4_ODD
        and want_clip_g4(5, 10, 127) == G4_MER
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_eq_clip_want() -> dict:
    """Family clip green4 XOR equals covering clip_want: k=1 q=10 is 1011 vs 1100."""
    n = (1 << 3) - 1
    got = want_clip_g4(1, 10, n)
    want = clip_want(1, 10)
    ok = got == G4_MER and want == (1, 1, 0, 0) and got != want
    return {"ok": ok, "k": 1, "q": 10, "n": n, "got": list(got), "clip_want": list(want)}


def killed_mer6_indep_k() -> dict:
    """q=6 max mer clip green4 is independent of k: k=2 is 1101, k=3 is 0000."""
    a = want_clip_g4(2, 6, 7)
    b = want_clip_g4(3, 6, 15)
    ok = a == G4_EVEN and b == G4_ODD and a != b
    return {"ok": ok, "k2": list(a), "k3": list(b)}


def killed_mer10_eq_mer6() -> dict:
    """q=10 max mer clip green4 equals q=6 max mer: k=2 is 1011 vs 1101."""
    a = want_clip_g4(2, 10, 15)
    b = want_clip_g4(2, 6, 7)
    ok = a == G4_MER and b == G4_EVEN and a != b
    return {"ok": ok, "k": 2, "mer10": list(a), "mer6": list(b)}


def killed_eq_row() -> dict:
    """Family clip green4 XOR equals row-XOR 0111: k=2 q=6 is 1101."""
    got = want_clip_g4(2, 6, 7)
    ok = got == G4_EVEN and got != ROW_XOR
    return {"ok": ok, "k": 2, "q": 6, "got": list(got), "row": list(ROW_XOR)}


def prefixes() -> dict:
    kt = json.loads(KT_JSON.read_text())
    ok = (
        kt["checks"]["all_ok"]
        and kt["verdict"]["family_clip_js"] == "LEMMA"
        and kt["verdict"]["family_clip_counts"] == "LEMMA"
        and kt["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_clip_g4(0, 6, 1) == (0, 0, 0, 0)
    assert want_clip_g4(0, 10, 3) == G4_MER0
    assert clip_g4_xor(6, 6, 127) == G4_EVEN
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_g4_table()
    sc = g4_xor_cover()
    k0 = killed_eq_clip_want()
    k1 = killed_mer6_indep_k()
    k2 = killed_mer10_eq_mer6()
    k3 = killed_eq_row()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_g4_table": {
            "n_ok": rt["n_ok"],
            "rows": {
                k: {
                    q: [{"n": x["n"], "xor": x["xor"]} for x in recs]
                    for q, recs in krow.items()
                }
                for k, krow in rt["rows"].items()
            },
        },
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_clip_want": {k: k0[k] for k in k0 if k != "ok"},
        "killed_mer6_indep_k": {k: k1[k] for k in k1 if k != "ok"},
        "killed_mer10_eq_mer6": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_row": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clip_g4": True,
            "family_clip_js": True,
            "family_clip_counts": True,
            "clip_g4_eq_clip_want": False,
            "mer6_indep_k": False,
            "mer10_eq_mer6": False,
            "clip_g4_eq_row": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clip_g4": "LEMMA",
            "family_clip_js": "LEMMA",
            "family_clip_counts": "LEMMA",
            "clip_g4_eq_clip_want": "KILLED",
            "mer6_indep_k": "KILLED",
            "mer10_eq_mer6": "KILLED",
            "clip_g4_eq_row": "KILLED",
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
    print("clip_g4_table n_ok", dump["clip_g4_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_clip_want", dump["killed_eq_clip_want"])
    print("killed_mer6_indep_k", dump["killed_mer6_indep_k"])
    print("killed_mer10_eq_mer6", dump["killed_mer10_eq_mer6"])
    print("killed_eq_row", dump["killed_eq_row"])


if __name__ == "__main__":
    main()
