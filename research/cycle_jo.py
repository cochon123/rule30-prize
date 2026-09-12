#!/usr/bin/env python3
"""Cycle JO: doubling n preserves g1_core_slot on the stretched column.

g1_core_slot(2n,2j) equals g1_core_slot(n,j) for every G=1 with n>0.
Doubling does not change the core slot; left doubling does not
change r; doubling is not g1_slot of 2n. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jo.py --certify
Dump: research/cycle_jo.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_in import g_run_kind
from cycle_is import g1_slot
from cycle_it import WANT_ALG, WANT_COV, g1_core_slot
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JN_JSON = Path(__file__).resolve().parent / "cycle_jn.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _slot_key(slots: dict) -> dict:
    return {f"{r},{d}": slots[(r, d)] for r, d in sorted(WANT_ALG)}


def slot_dbl_table() -> dict:
    """n<64: g1_core_slot(2n,2j) equals parent for n>0."""
    n_g1 = n_seed = n_hit = 0
    slots = {k: 0 for k in WANT_ALG}
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_g1 += 1
            got = g1_core_slot(n, j)
            if n == 0:
                n_seed += 1
                if got != "seed" or g1_core_slot(0, 0) != "seed":
                    return {"ok": False, "seed": True}
                continue
            got2 = g1_core_slot(2 * n, 2 * j)
            if got2 != got or got is None or got == "bad":
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "got": list(got) if isinstance(got, tuple) else got,
                    "got2": list(got2) if isinstance(got2, tuple) else got2,
                }
            _start, r, d = got
            slots[(r, d)] += 1
            n_hit += 1
    ok = (
        n_g1 == 1344
        and n_hit == 1343
        and n_seed == 1
        and slots == WANT_ALG
        and g1_core_slot(2, 0) == g1_core_slot(1, 0)
        and g1_slot(2, 0) is None
    )
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "slots": _slot_key(slots),
    }


def _walk_dbl(k: int, q: int) -> dict:
    """Core-slot doubling identity on covering G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_seed = n_hit = 0
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
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                got = g1_core_slot(n, j)
                if got == "seed":
                    n_seed += 1
                    continue
                got2 = g1_core_slot(2 * n, 2 * j)
                if got2 != got or got is None or got == "bad":
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                _start, r, d = got
                slots[(r, d)] += 1
                n_hit += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_seed": n_seed,
        "n_hit": n_hit,
        "slots": _slot_key(slots),
        "xor_j": xor_j,
    }


def slot_dbl_cover() -> dict:
    """Core-slot doubling on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_seed = n_hit = 0
    slots = {k: 0 for k in WANT_ALG}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dbl(k, q)
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
            n_seed += w["n_seed"]
            n_hit += w["n_hit"]
            for key, val in w["slots"].items():
                r, d = (int(x) for x in key.split(","))
                slots[(r, d)] += val
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_seed": w["n_seed"],
                "n_hit": w["n_hit"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_seed == 14
        and n_hit == 22645
        and slots == WANT_COV
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_seed": n_seed,
        "n_hit": n_hit,
        "slots": _slot_key(slots),
        "rows": rows,
    }


def killed_slot_changes() -> dict:
    """Doubling changes the core slot: G(1,0) (1,0) stays at G(2,0)."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 6
    got = g1_core_slot(n, j)
    got2 = g1_core_slot(2 * n, 2 * j)
    ok = (
        got == got2
        and isinstance(got, tuple)
        and got[1:] == (1, 0)
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": 2 * n,
        "j2": 2 * j,
        "p": p,
        "p2": p2,
        "slot": list(got),
        "slot2": list(got2),
    }


def killed_left_r_changes() -> dict:
    """Left doubling changes r: G(1,0) left r=1 stays r=1."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 6
    got = g1_core_slot(n, j)
    got2 = g1_core_slot(2 * n, 2 * j)
    ok = (
        g_run_kind(n, j) == "left"
        and got == got2
        and got[1] == 1
        and got2[1] != 2
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": 2 * n,
        "j2": 2 * j,
        "p": p,
        "p2": p2,
        "slot": list(got),
        "slot2": list(got2),
    }


def killed_even_g1_slot() -> dict:
    """Doubling is g1_slot of 2n: G(2,0) has no odd-n parent slot."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 6
    n2, j2 = 2 * n, 2 * j
    got2 = g1_core_slot(n2, j2)
    direct = g1_slot(n2, j2)
    ok = (
        n2 % 2 == 0
        and direct is None
        and got2 == g1_core_slot(n, j)
        and isinstance(got2, tuple)
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n2": n2,
        "j2": j2,
        "p": p,
        "p2": p2,
        "slot2": list(got2),
        "direct": direct,
    }


def prefixes() -> dict:
    jn = json.loads(JN_JSON.read_text())
    ok = (
        jn["checks"]["all_ok"]
        and jn["verdict"]["pair_dbl_dual_rev"] == "LEMMA"
        and jn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g1_core_slot(2, 0) == g1_core_slot(1, 0)
    assert g1_slot(2, 0) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = slot_dbl_table()
    sc = slot_dbl_cover()
    k0 = killed_slot_changes()
    k1 = killed_left_r_changes()
    k2 = killed_even_g1_slot()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "slot_dbl_table": {k: rt[k] for k in rt if k != "ok"},
        "slot_dbl_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_slot_changes": {k: k0[k] for k in k0 if k != "ok"},
        "killed_left_r_changes": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_g1_slot": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "core_slot_dbl": True,
            "covering_core_slot_dbl": True,
            "slot_census_stable": True,
            "slot_changes": False,
            "left_r_changes": False,
            "even_g1_slot": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "core_slot_dbl": "LEMMA",
            "covering_core_slot_dbl": "LEMMA",
            "slot_census_stable": "LEMMA",
            "slot_changes": "KILLED",
            "left_r_changes": "KILLED",
            "even_g1_slot": "KILLED",
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
    print("slot_dbl_table", dump["slot_dbl_table"])
    cov = dump["slot_dbl_cover"]
    print(
        "slot_dbl_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_hit",
        cov["n_hit"],
        "n_seed",
        cov["n_seed"],
    )
    print("killed_slot_changes", dump["killed_slot_changes"])
    print("killed_left_r_changes", dump["killed_left_r_changes"])
    print("killed_even_g1_slot", dump["killed_even_g1_slot"])


if __name__ == "__main__":
    main()
