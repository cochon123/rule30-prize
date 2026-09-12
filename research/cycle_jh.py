#!/usr/bin/env python3
"""Cycle JH: even-n iso_half3 interiors are 010 iff v2(n) is odd.

On even n>0, core-slot offset 0 is 001 and offset 2r is 100 for
every v2. Interiors are 010 when v2(n) is odd and 111 when v2(n) is
even. Cycle JG is the v2=1 case. v2-even interiors are not 010;
v2-odd interiors are not 111; v2-even ends are not 111. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jh.py --certify
Dump: research/cycle_jh.json
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
from cycle_ir import isolated_one
from cycle_it import g1_core_slot
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111, iso_half3
from cycle_jg import iso3_from_slot
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JG_JSON = Path(__file__).resolve().parent / "cycle_jg.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def iso3_even(n: int, j: int):
    """Predicted iso_half3 on even n>0 from slot ends and v2 parity."""
    if n % 2 or n <= 0 or not isolated_one(n, j):
        return None
    got = g1_core_slot(n, j)
    if not isinstance(got, tuple):
        return None
    _start, r, d = got
    if d == 0:
        return ISO3_001
    if d == 2 * r:
        return ISO3_100
    return ISO3_010 if (v2(n) & 1) else ISO3_111


def v2_table() -> dict:
    """n<64: even iso_half3 equals iso3_even; JG agrees on n%4==2."""
    n_iso = n_seed = n_odd = n_even = 0
    n_001 = n_010 = n_100 = n_111 = 0
    n_v2odd = n_v2even = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                if iso3_even(n, j) is not None:
                    return {"ok": False, "seed": True}
                continue
            three = iso_half3(n, j)
            pred = iso3_even(n, j)
            if n % 2:
                n_odd += 1
                if pred is not None:
                    return {"ok": False, "odd": True, "n": n, "j": j}
                continue
            n_even += 1
            if pred != three:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "pred": list(pred) if pred else None,
                    "three": list(three),
                }
            if n % 4 == 2 and iso3_from_slot(n, j) != three:
                return {"ok": False, "jg": True, "n": n, "j": j}
            if v2(n) & 1:
                n_v2odd += 1
            else:
                n_v2even += 1
            if three == ISO3_001:
                n_001 += 1
            elif three == ISO3_010:
                n_010 += 1
            elif three == ISO3_100:
                n_100 += 1
            else:
                n_111 += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_odd == 45
        and n_even == 415
        and n_001 == 115
        and n_010 == 141
        and n_100 == 115
        and n_111 == 44
        and n_v2odd == 319
        and n_v2even == 96
        and iso3_even(2, 0) == ISO3_001
        and iso3_even(2, 2) == ISO3_010
        and iso3_even(2, 4) == ISO3_100
        and iso3_even(4, 4) == ISO3_111
        and iso3_even(4, 0) == ISO3_001
        and iso3_even(3, 3) is None
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "n_v2odd": n_v2odd,
        "n_v2even": n_v2even,
    }


def _walk_v2(k: int, q: int) -> dict:
    """iso3_even on covering even isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = 0
    n_001 = n_010 = n_100 = n_111 = 0
    n_v2odd = n_v2even = 0
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
                pred = iso3_even(n, j)
                if n % 2:
                    n_odd += 1
                    if pred is not None:
                        return {"ok": False, "odd": True, "k": k, "n": n, "j": j}
                    continue
                if pred != three:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_even += 1
                if v2(n) & 1:
                    n_v2odd += 1
                else:
                    n_v2even += 1
                if three == ISO3_001:
                    n_001 += 1
                elif three == ISO3_010:
                    n_010 += 1
                elif three == ISO3_100:
                    n_100 += 1
                else:
                    n_111 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "n_v2odd": n_v2odd,
        "n_v2even": n_v2even,
        "xor_j": xor_j,
    }


def v2_cover() -> dict:
    """iso3_even on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = 0
    n_001 = n_010 = n_100 = n_111 = 0
    n_v2odd = n_v2even = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_v2(k, q)
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
            n_even += w["n_even"]
            n_001 += w["n_001"]
            n_010 += w["n_010"]
            n_100 += w["n_100"]
            n_111 += w["n_111"]
            n_v2odd += w["n_v2odd"]
            n_v2even += w["n_v2even"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_even": w["n_even"],
                "n_v2odd": w["n_v2odd"],
                "n_v2even": w["n_v2even"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_odd == 741
        and n_even == 7030
        and n_001 == 2011
        and n_010 == 2373
        and n_100 == 1912
        and n_111 == 734
        and n_v2odd == 5365
        and n_v2even == 1665
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "n_v2odd": n_v2odd,
        "n_v2even": n_v2even,
        "rows": rows,
    }


def killed_v2even_mid_010() -> dict:
    """v2-even interiors are 010: G(4,4) is 111."""
    k, s, n, j, p = 1, 11, 4, 4, 12
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and (v2(n) & 1) == 0
        and d not in (0, 2 * r)
        and three == ISO3_111
        and three != ISO3_010
        and iso3_even(n, j) == three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "v2": v2(n),
        "slot": list(got),
        "three": list(three),
    }


def killed_v2odd_mid_111() -> dict:
    """v2-odd interiors are 111: G(2,2) is 010."""
    k, s, n, j, p = 0, 5, 2, 2, 6
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    _start, r, d = got
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and (v2(n) & 1) == 1
        and d not in (0, 2 * r)
        and three == ISO3_010
        and three != ISO3_111
        and iso3_even(n, j) == three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "v2": v2(n),
        "slot": list(got),
        "three": list(three),
    }


def killed_v2even_end_111() -> dict:
    """v2-even ends are 111: G(4,0) is 001."""
    k, s, n, j, p = 1, 11, 4, 0, 20
    three = iso_half3(n, j)
    got = g1_core_slot(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and (v2(n) & 1) == 0
        and got[2] == 0
        and three == ISO3_001
        and three != ISO3_111
        and iso3_even(n, j) == three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "v2": v2(n),
        "slot": list(got),
        "three": list(three),
    }


def prefixes() -> dict:
    jg = json.loads(JG_JSON.read_text())
    ok = (
        jg["checks"]["all_ok"]
        and jg["verdict"]["n2_slot_iso3"] == "LEMMA"
        and jg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso3_even(2, 2) == ISO3_010
    assert iso3_even(4, 4) == ISO3_111
    assert iso3_even(4, 0) == ISO3_001
    assert iso3_from_slot(2, 2) == iso3_even(2, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = v2_table()
    sc = v2_cover()
    k0 = killed_v2even_mid_010()
    k1 = killed_v2odd_mid_111()
    k2 = killed_v2even_end_111()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "v2_table": {k: rt[k] for k in rt if k != "ok"},
        "v2_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_v2even_mid_010": {k: k0[k] for k in k0 if k != "ok"},
        "killed_v2odd_mid_111": {k: k1[k] for k in k1 if k != "ok"},
        "killed_v2even_end_111": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "even_iso3_v2": True,
            "v2_odd_mid_010": True,
            "covering_even_iso3_v2": True,
            "v2even_mid_010": False,
            "v2odd_mid_111": False,
            "v2even_end_111": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_iso3_v2": "LEMMA",
            "v2_odd_mid_010": "LEMMA",
            "covering_even_iso3_v2": "LEMMA",
            "v2even_mid_010": "KILLED",
            "v2odd_mid_111": "KILLED",
            "v2even_end_111": "KILLED",
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
    print("v2_table", dump["v2_table"])
    cov = dump["v2_cover"]
    print(
        "v2_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_even",
        cov["n_even"],
        "n_v2odd",
        cov["n_v2odd"],
        "n_v2even",
        cov["n_v2even"],
        "n_010",
        cov["n_010"],
        "n_111",
        cov["n_111"],
    )
    print("killed_v2even_mid_010", dump["killed_v2even_mid_010"])
    print("killed_v2odd_mid_111", dump["killed_v2odd_mid_111"])
    print("killed_v2even_end_111", dump["killed_v2even_end_111"])


if __name__ == "__main__":
    main()
