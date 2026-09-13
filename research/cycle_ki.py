#!/usr/bin/env python3
"""Cycle KI: half_run_image contributes exactly 2 consecutive pairs.

Every parent ones-run lifts to two consecutive G=1 pairs, so
n_pairs(2m+1)=2*n_runs(m). Run counts lift as n_run3(child)=n_run1(m),
n_run1(child)=n_run3(m), n_run2(child)=2*(n_run2(m)+n_run3(m)). Even n
has n_pairs=0. This is the freshman mechanism for Cycle KH's even
pair count, not J. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_ki.py --certify
Dump: research/cycle_ki.json
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
from cycle_ip import g_runs, half_run_image
from cycle_kh import g4_row_xor, g4_xor_cover

OUT = Path(__file__).resolve().with_suffix(".json")
KH_JSON = Path(__file__).resolve().parent / "cycle_kh.json"

M_ALG = 128
N_EVEN = 256
IMAGE_PAIRS = 2


def n_pairs_of(bits) -> int:
    """Consecutive ones-pairs in a bit window, including flanking zeros."""
    return sum(1 for a, b in zip(bits, bits[1:]) if a and b)


def run_counts(n: int):
    """Ones-run counts by length; fail on a 4-run."""
    counts = [0, 0, 0, 0]
    for _, r in g_runs(n):
        if r >= 4:
            return None
        if r <= 3:
            counts[r] += 1
    return counts


def pair_lift_table() -> dict:
    """m<128: image has 2 pairs; n_pairs(2m+1)=2*n_runs(m); even n_pairs=0."""
    n_img = n_child = 0
    by_r = [0, 0, 0, 0]
    for r in (1, 2, 3):
        if n_pairs_of(half_run_image(r)) != IMAGE_PAIRS:
            return {"ok": False, "img": True, "r": r}
    for m in range(0, M_ALG):
        n = 2 * m + 1
        parent = g_runs(m)
        rc_m = run_counts(m)
        rc_n = run_counts(n)
        if rc_m is None or rc_n is None:
            return {"ok": False, "run4": True, "m": m}
        for start, r in parent:
            pred = half_run_image(r)
            got = tuple(G(n, 2 * start + i) for i in range(-1, 2 * r + 2))
            if got != pred:
                return {
                    "ok": False,
                    "lift": True,
                    "m": m,
                    "start": start,
                    "r": r,
                    "got": list(got),
                }
            if n_pairs_of(pred) != IMAGE_PAIRS:
                return {"ok": False, "pairs": True, "m": m, "r": r}
            n_img += 1
            by_r[r] += 1
        rec = g4_row_xor(n)
        if not rec.get("ok"):
            return rec
        if rec["n_pairs"] != 2 * len(parent):
            return {
                "ok": False,
                "n_pairs": True,
                "n": n,
                "got": rec["n_pairs"],
                "want": 2 * len(parent),
            }
        if rc_n[3] != rc_m[1] or rc_n[1] != rc_m[3] or rc_n[2] != 2 * (rc_m[2] + rc_m[3]):
            return {
                "ok": False,
                "counts": True,
                "m": m,
                "rc_m": rc_m,
                "rc_n": rc_n,
            }
        n_child += 1
    n_even = 0
    for n in range(0, N_EVEN, 2):
        rec = g4_row_xor(n)
        if not rec.get("ok"):
            return rec
        if rec["n_pairs"] != 0:
            return {"ok": False, "even": True, "n": n, "n_pairs": rec["n_pairs"]}
        n_even += 1
    ok = (
        n_child == M_ALG
        and n_even == N_EVEN // 2
        and n_img == sum(by_r)
        and by_r[1] > 0
        and by_r[2] > 0
        and by_r[3] > 0
        and half_run_image(1) == (0, 1, 1, 1, 0)
        and half_run_image(2) == (0, 1, 1, 0, 1, 1, 0)
        and half_run_image(3) == (0, 1, 1, 0, 1, 0, 1, 1, 0)
        and n_pairs_of(half_run_image(1)) == IMAGE_PAIRS
    )
    return {
        "ok": ok,
        "n_img": n_img,
        "n_child": n_child,
        "n_even": n_even,
        "n_r1": by_r[1],
        "n_r2": by_r[2],
        "n_r3": by_r[3],
        "image_pairs": IMAGE_PAIRS,
    }


def killed_zero_pairs() -> dict:
    """half_run_image has 0 consecutive pairs: r=1 is 01110 with 2."""
    bits = half_run_image(1)
    got = n_pairs_of(bits)
    ok = bits == (0, 1, 1, 1, 0) and got == IMAGE_PAIRS and got != 0
    return {"ok": ok, "r": 1, "bits": list(bits), "n_pairs": got}


def killed_eq_runs() -> dict:
    """n_pairs(2m+1) equals n_runs(m): n=1 has 2 pairs from 1 parent run."""
    m, n = 0, 1
    n_runs = len(g_runs(m))
    n_pairs = g4_row_xor(n)["n_pairs"]
    ok = n_runs == 1 and n_pairs == 2 and n_pairs != n_runs
    return {"ok": ok, "m": m, "n": n, "n_runs": n_runs, "n_pairs": n_pairs}


def killed_even_pairs() -> dict:
    """Even n has consecutive G=1 pairs: n=2 has three isolated ones."""
    n = 2
    rec = g4_row_xor(n)
    runs = g_runs(n)
    ok = rec["n_pairs"] == 0 and runs == [(0, 1), (2, 1), (4, 1)]
    return {"ok": ok, "n": n, "n_pairs": rec["n_pairs"], "runs": [list(x) for x in runs]}


def killed_r3_from_r2() -> dict:
    """Odd-n run-3 comes from parent run-2: n=5 has 3 triples from 3 run-1s."""
    m, n = 2, 5
    rc_m = run_counts(m)
    rc_n = run_counts(n)
    ok = rc_m[2] == 0 and rc_m[1] == 3 and rc_n[3] == 3 and rc_n[3] != rc_m[2]
    return {"ok": ok, "m": m, "n": n, "rc_m": rc_m, "rc_n": rc_n}


def prefixes() -> dict:
    kh = json.loads(KH_JSON.read_text())
    ok = (
        kh["checks"]["all_ok"]
        and kh["verdict"]["g4_row_xor_0111"] == "LEMMA"
        and kh["verdict"]["covering_clip_g4"] == "LEMMA"
        and kh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert n_pairs_of(half_run_image(2)) == IMAGE_PAIRS
    assert n_pairs_of(half_run_image(3)) == IMAGE_PAIRS
    assert g4_row_xor(1)["n_pairs"] == 2
    assert g4_row_xor(0)["n_pairs"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = pair_lift_table()
    sc = g4_xor_cover()
    k0 = killed_zero_pairs()
    k1 = killed_eq_runs()
    k2 = killed_even_pairs()
    k3 = killed_r3_from_r2()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "pair_lift_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_zero_pairs": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_runs": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_pairs": {k: k2[k] for k in k2 if k != "ok"},
        "killed_r3_from_r2": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "image_two_pairs": True,
            "n_pairs_twice_runs": True,
            "g4_row_xor_0111": True,
            "covering_clip_g4": True,
            "image_zero_pairs": False,
            "n_pairs_eq_runs": False,
            "even_has_pairs": False,
            "r3_from_r2": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "image_two_pairs": "LEMMA",
            "n_pairs_twice_runs": "LEMMA",
            "g4_row_xor_0111": "LEMMA",
            "covering_clip_g4": "LEMMA",
            "image_zero_pairs": "KILLED",
            "n_pairs_eq_runs": "KILLED",
            "even_has_pairs": "KILLED",
            "r3_from_r2": "KILLED",
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
    print("pair_lift_table", dump["pair_lift_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_zero_pairs", dump["killed_zero_pairs"])
    print("killed_eq_runs", dump["killed_eq_runs"])
    print("killed_even_pairs", dump["killed_even_pairs"])
    print("killed_r3_from_r2", dump["killed_r3_from_r2"])


if __name__ == "__main__":
    main()
