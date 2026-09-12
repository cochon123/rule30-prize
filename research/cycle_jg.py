#!/usr/bin/env python3
"""Cycle JG: on n%4==2, iso_half3 is the core-slot end formula.

n=2m with m odd: offset 0 is 001, offset 2r is 100, interiors are
010. No 111 on n%4==2. Offset 0 is not 010; offset 2r is not 001;
n%4==0 interiors are not all 010 (G(4,4) is 111). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jg.py --certify
Dump: research/cycle_jg.json
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
from cycle_ir import isolated_one
from cycle_it import g1_core_slot
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111, iso_half3
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JF_JSON = Path(__file__).resolve().parent / "cycle_jf.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def iso3_from_slot(n: int, j: int):
    """Predicted iso_half3 from core-slot ends; None unless n%4==2."""
    if n % 4 != 2 or not isolated_one(n, j):
        return None
    got = g1_core_slot(n, j)
    if not isinstance(got, tuple):
        return None
    _start, r, d = got
    if d == 0:
        return ISO3_001
    if d == 2 * r:
        return ISO3_100
    return ISO3_010


def slot3_table() -> dict:
    """n<64: n%4==2 iso_half3 equals iso3_from_slot; no 111."""
    n_iso = n_seed = n_odd = n_n2 = n_n0 = 0
    n_n2_001 = n_n2_010 = n_n2_100 = n_n2_111 = 0
    n_n0_111 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            three = iso_half3(n, j)
            pred = iso3_from_slot(n, j)
            if n % 4 == 2:
                n_n2 += 1
                if pred != three:
                    return {
                        "ok": False,
                        "miss": True,
                        "n": n,
                        "j": j,
                        "pred": list(pred) if pred else None,
                        "three": list(three),
                    }
                if three == ISO3_001:
                    n_n2_001 += 1
                elif three == ISO3_010:
                    n_n2_010 += 1
                elif three == ISO3_100:
                    n_n2_100 += 1
                else:
                    n_n2_111 += 1
            elif n % 4 == 0:
                n_n0 += 1
                if pred is not None:
                    return {"ok": False, "n0pred": True, "n": n, "j": j}
                if three == ISO3_111:
                    n_n0_111 += 1
            else:
                n_odd += 1
                if pred is not None:
                    return {"ok": False, "oddpred": True, "n": n, "j": j}
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_odd == 45
        and n_n2 == 288
        and n_n0 == 127
        and n_n2_001 == 80
        and n_n2_010 == 128
        and n_n2_100 == 80
        and n_n2_111 == 0
        and n_n0_111 == 44
        and iso3_from_slot(2, 0) == ISO3_001
        and iso3_from_slot(2, 2) == ISO3_010
        and iso3_from_slot(2, 4) == ISO3_100
        and iso3_from_slot(4, 4) is None
        and iso3_from_slot(3, 3) is None
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_n2": n_n2,
        "n_n0": n_n0,
        "n_n2_001": n_n2_001,
        "n_n2_010": n_n2_010,
        "n_n2_100": n_n2_100,
        "n_n2_111": n_n2_111,
        "n_n0_111": n_n0_111,
    }


def _walk_slot3(k: int, q: int) -> dict:
    """Slot-end iso_half3 on covering n%4==2 isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_n2 = n_n0 = 0
    n_n2_001 = n_n2_010 = n_n2_100 = n_n2_111 = 0
    n_n0_111 = 0
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
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                if n == 0:
                    n_seed += 1
                    continue
                three = iso_half3(n, j)
                pred = iso3_from_slot(n, j)
                if n % 4 == 2:
                    n_n2 += 1
                    if pred != three:
                        return {
                            "ok": False,
                            "miss": True,
                            "k": k,
                            "n": n,
                            "j": j,
                        }
                    if three == ISO3_001:
                        n_n2_001 += 1
                    elif three == ISO3_010:
                        n_n2_010 += 1
                    elif three == ISO3_100:
                        n_n2_100 += 1
                    else:
                        n_n2_111 += 1
                elif n % 4 == 0:
                    n_n0 += 1
                    if pred is not None:
                        return {"ok": False, "n0pred": True, "k": k, "n": n, "j": j}
                    if three == ISO3_111:
                        n_n0_111 += 1
                else:
                    n_odd += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_n2": n_n2,
        "n_n0": n_n0,
        "n_n2_001": n_n2_001,
        "n_n2_010": n_n2_010,
        "n_n2_100": n_n2_100,
        "n_n2_111": n_n2_111,
        "n_n0_111": n_n0_111,
        "xor_j": xor_j,
    }


def slot3_cover() -> dict:
    """Slot-end formula on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_n2 = n_n0 = 0
    n_n2_001 = n_n2_010 = n_n2_100 = n_n2_111 = 0
    n_n0_111 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_slot3(k, q)
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
            n_iso += w["n_iso"]
            n_seed += w["n_seed"]
            n_odd += w["n_odd"]
            n_n2 += w["n_n2"]
            n_n0 += w["n_n0"]
            n_n2_001 += w["n_n2_001"]
            n_n2_010 += w["n_n2_010"]
            n_n2_100 += w["n_n2_100"]
            n_n2_111 += w["n_n2_111"]
            n_n0_111 += w["n_n0_111"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_n2": w["n_n2"],
                "n_n0": w["n_n0"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_odd == 741
        and n_n2 == 4846
        and n_n0 == 2184
        and n_n2_001 == 1376
        and n_n2_010 == 2146
        and n_n2_100 == 1324
        and n_n2_111 == 0
        and n_n0_111 == 734
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_n2": n_n2,
        "n_n0": n_n0,
        "n_n2_001": n_n2_001,
        "n_n2_010": n_n2_010,
        "n_n2_100": n_n2_100,
        "n_n2_111": n_n2_111,
        "n_n0_111": n_n0_111,
        "rows": rows,
    }


def killed_off0_010() -> dict:
    """Offset 0 is 010: G(2,0) is 001."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    ok = (
        isolated_one(n, j)
        and n % 4 == 2
        and got[2] == 0
        and three == ISO3_001
        and three != ISO3_010
        and iso3_from_slot(n, j) == three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "three": list(three),
    }


def killed_end_001() -> dict:
    """Offset 2r is 001: G(2,4) is 100."""
    k, s, n, j, p = 1, 7, 2, 4, 4
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 4 == 2
        and d == 2 * r
        and three == ISO3_100
        and three != ISO3_001
        and iso3_from_slot(n, j) == three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "three": list(three),
    }


def killed_n0_interior_010() -> dict:
    """n%4==0 interiors are 010: G(4,4) is 111."""
    k, s, n, j, p = 1, 11, 4, 4, 12
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 4 == 0
        and d not in (0, 2 * r)
        and three == ISO3_111
        and three != ISO3_010
        and iso3_from_slot(n, j) is None
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "three": list(three),
    }


def prefixes() -> dict:
    jf = json.loads(JF_JSON.read_text())
    ok = (
        jf["checks"]["all_ok"]
        and jf["verdict"]["iso_half3_stretch"] == "LEMMA"
        and jf["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso3_from_slot(2, 0) == ISO3_001
    assert iso3_from_slot(2, 4) == ISO3_100
    assert iso3_from_slot(4, 4) is None
    assert iso_half3(4, 4) == ISO3_111
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = slot3_table()
    sc = slot3_cover()
    k0 = killed_off0_010()
    k1 = killed_end_001()
    k2 = killed_n0_interior_010()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "slot3_table": {k: rt[k] for k in rt if k != "ok"},
        "slot3_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_off0_010": {k: k0[k] for k in k0 if k != "ok"},
        "killed_end_001": {k: k1[k] for k in k1 if k != "ok"},
        "killed_n0_interior_010": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "n2_slot_iso3": True,
            "n2_no_111": True,
            "covering_n2_slot_iso3": True,
            "off0_010": False,
            "end_001": False,
            "n0_interior_010": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n2_slot_iso3": "LEMMA",
            "n2_no_111": "LEMMA",
            "covering_n2_slot_iso3": "LEMMA",
            "off0_010": "KILLED",
            "end_001": "KILLED",
            "n0_interior_010": "KILLED",
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
    print("slot3_table", dump["slot3_table"])
    cov = dump["slot3_cover"]
    print(
        "slot3_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_n2",
        cov["n_n2"],
        "n_n0",
        cov["n_n0"],
        "n_n2_001",
        cov["n_n2_001"],
        "n_n2_010",
        cov["n_n2_010"],
        "n_n2_100",
        cov["n_n2_100"],
        "n_n0_111",
        cov["n_n0_111"],
    )
    print("killed_off0_010", dump["killed_off0_010"])
    print("killed_end_001", dump["killed_end_001"])
    print("killed_n0_interior_010", dump["killed_n0_interior_010"])


if __name__ == "__main__":
    main()
