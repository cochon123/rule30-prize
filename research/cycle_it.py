#!/usr/bin/env python3
"""Cycle IT: n>0 G=1 is a stretched odd-core IMAGE_ONES slot.

n=2^v*odd sends G(n, 2^v * j') = G(odd, j'). Every G=1 with n>0 is
g1_slot(odd, j'). n=0 is the seed exception, not a core slot. Even
G=1 is a core slot after stretch; g1_slot on even n is not the
formula. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_it.py --certify
Dump: research/cycle_it.json
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
from cycle_is import g1_slot
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IS_JSON = Path(__file__).resolve().parent / "cycle_is.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

WANT_ALG = {
    (1, 0): 206,
    (1, 1): 206,
    (1, 2): 206,
    (2, 0): 100,
    (2, 1): 100,
    (2, 3): 100,
    (2, 4): 100,
    (3, 0): 65,
    (3, 1): 65,
    (3, 3): 65,
    (3, 5): 65,
    (3, 6): 65,
}

WANT_COV = {
    (1, 0): 3560,
    (1, 1): 3467,
    (1, 2): 3467,
    (2, 0): 1713,
    (2, 1): 1668,
    (2, 3): 1659,
    (2, 4): 1659,
    (3, 0): 1129,
    (3, 1): 1087,
    (3, 3): 1087,
    (3, 5): 1078,
    (3, 6): 1071,
}


def odd_core(n: int):
    """(odd, v) with n = odd << v, else None for n<=0."""
    if n <= 0:
        return None
    v = v2(n)
    return n >> v, v


def g1_core_slot(n: int, j: int):
    """Unique core slot of G=1 for n>0; 'seed' at n=0; else None/bad."""
    if G(n, j) == 0:
        return None
    if n == 0:
        return "seed"
    core, v = odd_core(n)
    if j % (1 << v):
        return "bad"
    return g1_slot(core, j >> v)


def _slot_key(slots: dict) -> dict:
    return {f"{r},{d}": slots[(r, d)] for r, d in sorted(WANT_ALG)}


def core_table() -> dict:
    """n<64: n>0 G=1 is a unique core slot; n=0 is seed."""
    n_g1 = n_hit = n_seed = 0
    slots = {k: 0 for k in WANT_ALG}
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_g1 += 1
            got = g1_core_slot(n, j)
            if got == "seed":
                n_seed += 1
                continue
            if got is None or got == "bad":
                return {"ok": False, "miss": True, "n": n, "j": j, "got": got}
            _start, r, d = got
            slots[(r, d)] += 1
            n_hit += 1
    ok = n_g1 == 1344 and n_hit == 1343 and n_seed == 1 and slots == WANT_ALG
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "slots": _slot_key(slots),
    }


def _walk_core(k: int, q: int) -> dict:
    """Core slots on covering G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_hit = n_seed = 0
    slots = {key: 0 for key in WANT_ALG}
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
                got = g1_core_slot(n, j)
                if got == "seed":
                    n_seed += 1
                    continue
                if got is None or got == "bad":
                    return {"ok": False, "miss": True, "k": k, "n": n, "j": j, "got": got}
                _start, r, d = got
                slots[(r, d)] += 1
                n_hit += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "slots": _slot_key(slots),
        "xor_j": xor_j,
        "_slots": slots,
    }


def core_cover() -> dict:
    """Core slots on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_hit = n_seed = 0
    slots = {k: 0 for k in WANT_ALG}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_core(k, q)
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
            n_hit += w["n_hit"]
            n_seed += w["n_seed"]
            for key in slots:
                slots[key] += w["_slots"][key]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_hit": w["n_hit"],
                "n_seed": w["n_seed"],
                "slots": w["slots"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_hit == 22645
        and n_seed == 14
        and slots == WANT_COV
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "slots": _slot_key(slots),
        "rows": rows,
    }


def killed_even_not_core() -> dict:
    """Even G=1 is not a core slot: G(2,0) is slot (0,1,0) of core 1."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    got = g1_core_slot(n, j)
    ok = (
        n % 2 == 0
        and G(n, j) == 1
        and odd_core(n) == (1, 1)
        and got == (0, 1, 0)
        and g1_slot(n, j) is None
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "core": list(odd_core(n)),
        "slot": list(got) if isinstance(got, tuple) else got,
    }


def killed_even_direct_slot() -> dict:
    """g1_slot on even n is the formula: G(2,0) has g1_slot None."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    ok = g1_slot(n, j) is None and g1_core_slot(n, j) == (0, 1, 0) and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "g1_slot": g1_slot(n, j),
        "core_slot": list(g1_core_slot(n, j)),
    }


def killed_seed_is_core() -> dict:
    """n=0 G=1 is a core slot: seed, not IMAGE_ONES."""
    k, s, n, j, p = 0, 5, 0, 0, 6
    ok = n == 0 and G(n, j) == 1 and g1_core_slot(n, j) == "seed" and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": g1_core_slot(n, j),
        "G": G(n, j),
    }


def prefixes() -> dict:
    iss = json.loads(IS_JSON.read_text())
    ok = (
        iss["checks"]["all_ok"]
        and iss["verdict"]["odd_g1_unique_slot"] == "LEMMA"
        and iss["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g1_core_slot(1, 0) == g1_slot(1, 0) == (0, 1, 0)
    assert g1_core_slot(2, 0) == (0, 1, 0)
    assert g1_core_slot(0, 0) == "seed"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = core_table()
    sc = core_cover()
    k0 = killed_even_not_core()
    k1 = killed_even_direct_slot()
    k2 = killed_seed_is_core()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "core_table": {k: rt[k] for k in rt if k != "ok"},
        "core_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_not_core": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_direct_slot": {k: k1[k] for k in k1 if k != "ok"},
        "killed_seed_is_core": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "n_gt0_core_slot": True,
            "seed_n0_exception": True,
            "covering_core_slots": True,
            "even_g1_not_core": False,
            "even_g1_slot_direct": False,
            "seed_is_core": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n_gt0_core_slot": "LEMMA",
            "seed_n0_exception": "LEMMA",
            "covering_core_slots": "LEMMA",
            "even_g1_not_core": "KILLED",
            "even_g1_slot_direct": "KILLED",
            "seed_is_core": "KILLED",
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
    print("core_table", dump["core_table"])
    cov = dump["core_cover"]
    print(
        "core_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_hit",
        cov["n_hit"],
        "n_seed",
        cov["n_seed"],
    )
    print("killed_even_not_core", dump["killed_even_not_core"])
    print("killed_even_direct_slot", dump["killed_even_direct_slot"])
    print("killed_seed_is_core", dump["killed_seed_is_core"])


if __name__ == "__main__":
    main()
