#!/usr/bin/env python3
"""Cycle IW: center G=1 slot is v2 of the odd core.

n>0 center is (m,1,1) iff v2(odd_core(n)+1) is odd, else (m-1,3,3)
with m=core//2. n=0 stays seed. Even-n type is not v2(n+1); (1,1)
is not always w=1; the center is not never (3,3). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_iw.py --certify
Dump: research/cycle_iw.json
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
from cycle_al import G, v2
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_it import g1_core_slot, odd_core
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IV_JSON = Path(__file__).resolve().parent / "cycle_iv.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def center_core_slot(n: int):
    """g1_core_slot(n, n) from v2 of the odd core; seed at n=0."""
    if n == 0:
        return "seed"
    core, _v = odd_core(n)
    m = core // 2
    if v2(core + 1) % 2:
        return (m, 1, 1)
    return (m - 1, 3, 3)


def naive_from_n(n: int):
    """Wrong formula using v2(n+1) and m=n//2."""
    m = n // 2
    if v2(n + 1) % 2:
        return (m, 1, 1)
    return (m - 1, 3, 3)


def center_table() -> dict:
    """n<64: center slot is center_core_slot; never run-2."""
    n_ok = n_11 = n_33 = n_seed = 0
    for n in range(0, 64):
        pred = center_core_slot(n)
        got = g1_core_slot(n, n)
        if pred != got:
            return {"ok": False, "miss": True, "n": n, "pred": pred, "got": got}
        n_ok += 1
        if got == "seed":
            n_seed += 1
            continue
        if got[1] == 2:
            return {"ok": False, "r2": True, "n": n, "got": got}
        if got[1] == 1:
            n_11 += 1
        else:
            n_33 += 1
    ok = n_ok == 64 and n_11 == 42 and n_33 == 21 and n_seed == 1
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_11": n_11,
        "n_33": n_33,
        "n_seed": n_seed,
    }


def _walk_center(k: int, q: int) -> dict:
    """Center slots on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_ctr = n_seed = n_11 = n_33 = n_and = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if not G(n, j):
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                if j != n:
                    continue
                pred = center_core_slot(n)
                got = g1_core_slot(n, n)
                if pred != got:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "pred": pred,
                        "got": got,
                    }
                n_ctr += 1
                if packed:
                    n_and += 1
                if got == "seed":
                    n_seed += 1
                elif got[1] == 1:
                    n_11 += 1
                else:
                    n_33 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ctr": n_ctr,
        "n_seed": n_seed,
        "n_11": n_11,
        "n_33": n_33,
        "n_and": n_and,
        "xor_j": xor_j,
    }


def center_cover() -> dict:
    """Center slots on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_ctr = n_seed = n_11 = n_33 = n_and = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_center(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_ctr += w["n_ctr"]
            n_seed += w["n_seed"]
            n_11 += w["n_11"]
            n_33 += w["n_33"]
            n_and += w["n_and"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_ctr": w["n_ctr"],
                "n_seed": w["n_seed"],
                "n_11": w["n_11"],
                "n_33": w["n_33"],
                "n_and": w["n_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_ctr == 762
        and n_seed == 14
        and n_11 == 501
        and n_33 == 247
        and n_and == 232
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ctr": n_ctr,
        "n_seed": n_seed,
        "n_11": n_11,
        "n_33": n_33,
        "n_and": n_and,
        "rows": rows,
    }


def killed_even_from_n() -> dict:
    """Even-n type is v2(n+1): G(2,2) is (0,1,1), naive (0,3,3)."""
    k, s, n, p = 1, 7, 2, 8
    got = g1_core_slot(n, n)
    naive = naive_from_n(n)
    pred = center_core_slot(n)
    ok = (
        n % 2 == 0
        and v2(n + 1) % 2 == 0
        and got == (0, 1, 1)
        and naive == (0, 3, 3)
        and pred == got
        and got != naive
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": n,
        "p": p,
        "slot": list(got),
        "naive": list(naive),
        "w": v2(n + 1) % 2,
    }


def killed_11_always_w1() -> dict:
    """Center (1,1) always has w=1: G(2,2) is (1,1) with w=0."""
    k, s, n, p = 1, 7, 2, 8
    got = g1_core_slot(n, n)
    w = v2(n + 1) % 2
    ok = got == (0, 1, 1) and w == 0 and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": n,
        "p": p,
        "slot": list(got),
        "w": w,
    }


def killed_33_never() -> dict:
    """Center is never (3,3): G(3,3) is (0,3,3)."""
    k, s, n, p = 1, 5, 3, 6
    got = g1_core_slot(n, n)
    ok = got == (0, 3, 3) and got[1] == 3 and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": n,
        "p": p,
        "slot": list(got),
        "w": v2(n + 1) % 2,
    }


def prefixes() -> dict:
    iv = json.loads(IV_JSON.read_text())
    ok = (
        iv["checks"]["all_ok"]
        and iv["verdict"]["slot_neigh"] == "LEMMA"
        and iv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert center_core_slot(0) == "seed"
    assert center_core_slot(1) == (0, 1, 1)
    assert center_core_slot(2) == (0, 1, 1)
    assert center_core_slot(3) == (0, 3, 3)
    assert center_core_slot(7) == (3, 1, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = center_table()
    sc = center_cover()
    k0 = killed_even_from_n()
    k1 = killed_11_always_w1()
    k2 = killed_33_never()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "center_table": {k: rt[k] for k in rt if k != "ok"},
        "center_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_from_n": {k: k0[k] for k in k0 if k != "ok"},
        "killed_11_always_w1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_33_never": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "center_core_slot": True,
            "odd_center_from_v2": True,
            "covering_center_slots": True,
            "even_center_from_n": False,
            "center_11_always_w1": False,
            "center_never_33": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "center_core_slot": "LEMMA",
            "odd_center_from_v2": "LEMMA",
            "covering_center_slots": "LEMMA",
            "even_center_from_n": "KILLED",
            "center_11_always_w1": "KILLED",
            "center_never_33": "KILLED",
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
    print("center_table", dump["center_table"])
    cov = dump["center_cover"]
    print(
        "center_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_ctr",
        cov["n_ctr"],
        "n_seed",
        cov["n_seed"],
        "n_11",
        cov["n_11"],
        "n_33",
        cov["n_33"],
        "n_and",
        cov["n_and"],
    )
    print("killed_even_from_n", dump["killed_even_from_n"])
    print("killed_11_always_w1", dump["killed_11_always_w1"])
    print("killed_33_never", dump["killed_33_never"])


if __name__ == "__main__":
    main()
