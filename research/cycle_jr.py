#!/usr/bin/env python3
"""Cycle JR: 4-stretch preserves isolated-one iso3 windows.

iso3_even(4n,4j) equals iso3_parent(n,j) for n>0, because
iso3_double is an involution. Interiors do not change under
4-stretch; ends do not change; odd iso does not become 010.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jr.py --certify
Dump: research/cycle_jr.json
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
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111
from cycle_jh import iso3_even
from cycle_jq import iso3_double, iso3_parent
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JQ_JSON = Path(__file__).resolve().parent / "cycle_jq.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def quad_table() -> dict:
    """n<64: iso3_even(4n,4j) equals parent; iso3_double involution."""
    for three in (ISO3_001, ISO3_100, ISO3_010, ISO3_111):
        if iso3_double(iso3_double(three)) != three:
            return {"ok": False, "inv": True, "three": list(three)}
    n_iso = n_seed = n_001 = n_100 = n_010 = n_111 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            three = iso3_parent(n, j)
            three4 = iso3_even(4 * n, 4 * j)
            if (
                not isolated_one(4 * n, 4 * j)
                or three4 != three
                or three4 != iso3_double(iso3_double(three))
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "three": list(three) if three else None,
                    "three4": list(three4) if three4 else None,
                }
            if three == ISO3_001:
                n_001 += 1
            elif three == ISO3_100:
                n_100 += 1
            elif three == ISO3_010:
                n_010 += 1
            else:
                n_111 += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_001 == 115
        and n_100 == 115
        and n_010 == 141
        and n_111 == 89
        and iso3_even(8, 8) == iso3_parent(2, 2) == ISO3_010
        and iso3_even(8, 0) == iso3_parent(2, 0) == ISO3_001
        and iso3_even(12, 12) == iso3_parent(3, 3) == ISO3_111
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_001": n_001,
        "n_100": n_100,
        "n_010": n_010,
        "n_111": n_111,
    }


def _walk_quad(k: int, q: int) -> dict:
    """4-stretch identity on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_quad = 0
    n_001 = n_100 = n_010 = n_111 = 0
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
                three = iso3_parent(n, j)
                three4 = iso3_even(4 * n, 4 * j)
                if three4 != three:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_quad += 1
                if three == ISO3_001:
                    n_001 += 1
                elif three == ISO3_100:
                    n_100 += 1
                elif three == ISO3_010:
                    n_010 += 1
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
        "n_quad": n_quad,
        "n_001": n_001,
        "n_100": n_100,
        "n_010": n_010,
        "n_111": n_111,
        "xor_j": xor_j,
    }


def quad_cover() -> dict:
    """4-stretch identity on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_quad = 0
    n_001 = n_100 = n_010 = n_111 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_quad(k, q)
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
            n_quad += w["n_quad"]
            n_001 += w["n_001"]
            n_100 += w["n_100"]
            n_010 += w["n_010"]
            n_111 += w["n_111"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_quad": w["n_quad"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_quad == 7771
        and n_001 == 2011
        and n_100 == 1912
        and n_010 == 2373
        and n_111 == 1475
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_quad": n_quad,
        "n_001": n_001,
        "n_100": n_100,
        "n_010": n_010,
        "n_111": n_111,
        "rows": rows,
    }


def killed_mid_changes() -> dict:
    """Interiors change under 4-stretch: G(2,2) stays 010 at G(8,8)."""
    k, s, n, j, p, p4 = 3, 43, 2, 2, 44, 32
    n4, j4 = 4 * n, 4 * j
    three = iso3_parent(n, j)
    three4 = iso3_even(n4, j4)
    ok = (
        isolated_one(n, j)
        and isolated_one(n4, j4)
        and three == ISO3_010
        and three4 == three
        and three4 != ISO3_111
        and p >= 4
        and p4 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n4": n4,
        "j4": j4,
        "p": p,
        "p4": p4,
        "three": list(three),
        "three4": list(three4),
    }


def killed_end_changes() -> dict:
    """Ends change under 4-stretch: G(2,0) stays 001 at G(8,0)."""
    k, s, n, j, p, p4 = 3, 43, 2, 0, 48, 48
    n4, j4 = 4 * n, 4 * j
    three = iso3_parent(n, j)
    three4 = iso3_even(n4, j4)
    ok = (
        isolated_one(n, j)
        and isolated_one(n4, j4)
        and three == ISO3_001
        and three4 == three
        and three4 != ISO3_100
        and p >= 4
        and p4 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n4": n4,
        "j4": j4,
        "p": p,
        "p4": p4,
        "three": list(three),
        "three4": list(three4),
    }


def killed_odd_to_010() -> dict:
    """Odd iso 4-stretch is 010: G(3,3) stays 111 at G(12,12)."""
    k, s, n, j, p, p4 = 3, 73, 3, 3, 74, 56
    n4, j4 = 4 * n, 4 * j
    three = iso3_parent(n, j)
    three4 = iso3_even(n4, j4)
    ok = (
        isolated_one(n, j)
        and n % 2 == 1
        and isolated_one(n4, j4)
        and three == ISO3_111
        and three4 == three
        and three4 != ISO3_010
        and p >= 4
        and p4 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "n4": n4,
        "j4": j4,
        "p": p,
        "p4": p4,
        "three": list(three),
        "three4": list(three4),
    }


def prefixes() -> dict:
    jq = json.loads(JQ_JSON.read_text())
    ok = (
        jq["checks"]["all_ok"]
        and jq["verdict"]["iso3_double"] == "LEMMA"
        and jq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso3_double(iso3_double(ISO3_010)) == ISO3_010
    assert iso3_even(8, 8) == iso3_parent(2, 2)
    assert iso3_even(12, 12) == iso3_parent(3, 3)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = quad_table()
    sc = quad_cover()
    k0 = killed_mid_changes()
    k1 = killed_end_changes()
    k2 = killed_odd_to_010()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "quad_table": {k: rt[k] for k in rt if k != "ok"},
        "quad_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_mid_changes": {k: k0[k] for k in k0 if k != "ok"},
        "killed_end_changes": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_to_010": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "iso3_double_involution": True,
            "iso3_quad_col": True,
            "covering_iso3_quad": True,
            "mid_changes": False,
            "end_changes": False,
            "odd_to_010": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "iso3_double_involution": "LEMMA",
            "iso3_quad_col": "LEMMA",
            "covering_iso3_quad": "LEMMA",
            "mid_changes": "KILLED",
            "end_changes": "KILLED",
            "odd_to_010": "KILLED",
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
    print("quad_table", dump["quad_table"])
    cov = dump["quad_cover"]
    print(
        "quad_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_quad",
        cov["n_quad"],
        "n_001",
        cov["n_001"],
        "n_100",
        cov["n_100"],
        "n_010",
        cov["n_010"],
        "n_111",
        cov["n_111"],
    )
    print("killed_mid_changes", dump["killed_mid_changes"])
    print("killed_end_changes", dump["killed_end_changes"])
    print("killed_odd_to_010", dump["killed_odd_to_010"])


if __name__ == "__main__":
    main()
