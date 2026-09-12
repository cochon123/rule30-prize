#!/usr/bin/env python3
"""Cycle JQ: doubling n maps isolated-one iso3 by flipping interiors.

iso3_even(2n,2j) equals iso3_double of the parent 3-window for n>0.
Ends 001 and 100 stay; interiors swap 010 with 111. Odd-n 111
doubles to 010. Interiors do not stay; ends do not swap; odd iso
does not stay 111. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_jq.py --certify
Dump: research/cycle_jq.json
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
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111, iso_half3
from cycle_jh import iso3_even
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JP_JSON = Path(__file__).resolve().parent / "cycle_jp.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def iso3_parent(n: int, j: int):
    """Parent 3-window of an isolated one; None for n=0."""
    if n <= 0 or not isolated_one(n, j):
        return None
    if n % 2 == 0:
        return iso3_even(n, j)
    return iso_half3(n, j)


def iso3_double(three):
    """iso3 image under n to 2n on the stretched column."""
    if three in (ISO3_001, ISO3_100):
        return three
    if three == ISO3_010:
        return ISO3_111
    if three == ISO3_111:
        return ISO3_010
    return None


def dbl_table() -> dict:
    """n<64: iso3_even(2n,2j) equals iso3_double of the parent."""
    n_iso = n_seed = n_stay_001 = n_stay_100 = n_flip_010 = n_flip_111 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            three = iso3_parent(n, j)
            pred = iso3_double(three)
            got = iso3_even(2 * n, 2 * j)
            if not isolated_one(2 * n, 2 * j) or got != pred:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "three": list(three) if three else None,
                    "got": list(got) if got else None,
                }
            if three == ISO3_001:
                n_stay_001 += 1
            elif three == ISO3_100:
                n_stay_100 += 1
            elif three == ISO3_010:
                n_flip_010 += 1
            else:
                n_flip_111 += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_stay_001 == 115
        and n_stay_100 == 115
        and n_flip_010 == 141
        and n_flip_111 == 89
        and iso3_even(4, 4) == iso3_double(iso3_even(2, 2)) == ISO3_111
        and iso3_even(6, 6) == iso3_double(ISO3_111) == ISO3_010
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_stay_001": n_stay_001,
        "n_stay_100": n_stay_100,
        "n_flip_010": n_flip_010,
        "n_flip_111": n_flip_111,
    }


def _walk_dbl(k: int, q: int) -> dict:
    """iso3 doubling identity on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_dbl = 0
    n_stay_001 = n_stay_100 = n_flip_010 = n_flip_111 = 0
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
                pred = iso3_double(three)
                got = iso3_even(2 * n, 2 * j)
                if got != pred:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_dbl += 1
                if three == ISO3_001:
                    n_stay_001 += 1
                elif three == ISO3_100:
                    n_stay_100 += 1
                elif three == ISO3_010:
                    n_flip_010 += 1
                else:
                    n_flip_111 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_dbl": n_dbl,
        "n_stay_001": n_stay_001,
        "n_stay_100": n_stay_100,
        "n_flip_010": n_flip_010,
        "n_flip_111": n_flip_111,
        "xor_j": xor_j,
    }


def dbl_cover() -> dict:
    """iso3 doubling on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_dbl = 0
    n_stay_001 = n_stay_100 = n_flip_010 = n_flip_111 = 0
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
            n_iso += w["n_iso"]
            n_seed += w["n_seed"]
            n_dbl += w["n_dbl"]
            n_stay_001 += w["n_stay_001"]
            n_stay_100 += w["n_stay_100"]
            n_flip_010 += w["n_flip_010"]
            n_flip_111 += w["n_flip_111"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_dbl": w["n_dbl"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_dbl == 7771
        and n_stay_001 == 2011
        and n_stay_100 == 1912
        and n_flip_010 == 2373
        and n_flip_111 == 1475
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_dbl": n_dbl,
        "n_stay_001": n_stay_001,
        "n_stay_100": n_stay_100,
        "n_flip_010": n_flip_010,
        "n_flip_111": n_flip_111,
        "rows": rows,
    }


def killed_mid_stays() -> dict:
    """Interiors stay: G(2,2) 010 doubles to G(4,4) 111."""
    k, s, n, j, p, p2 = 1, 15, 2, 2, 16, 12
    n2, j2 = 2 * n, 2 * j
    three = iso3_parent(n, j)
    three2 = iso3_even(n2, j2)
    ok = (
        isolated_one(n, j)
        and isolated_one(n2, j2)
        and three == ISO3_010
        and three2 == iso3_double(three) == ISO3_111
        and three2 != three
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
        "three": list(three),
        "three2": list(three2),
    }


def killed_end_swaps() -> dict:
    """Ends swap: G(2,0) 001 doubles to G(4,0) 001."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 20
    n2, j2 = 2 * n, 2 * j
    three = iso3_parent(n, j)
    three2 = iso3_even(n2, j2)
    ok = (
        isolated_one(n, j)
        and isolated_one(n2, j2)
        and three == ISO3_001
        and three2 == iso3_double(three) == three
        and three2 != ISO3_100
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
        "three": list(three),
        "three2": list(three2),
    }


def killed_odd_stays_111() -> dict:
    """Odd iso stays 111: G(3,3) doubles to G(6,6) 010."""
    k, s, n, j, p, p2 = 2, 17, 3, 3, 18, 12
    n2, j2 = 2 * n, 2 * j
    three = iso3_parent(n, j)
    three2 = iso3_even(n2, j2)
    ok = (
        isolated_one(n, j)
        and n % 2 == 1
        and isolated_one(n2, j2)
        and three == ISO3_111
        and three2 == iso3_double(three) == ISO3_010
        and three2 != three
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
        "three": list(three),
        "three2": list(three2),
    }


def prefixes() -> dict:
    jp = json.loads(JP_JSON.read_text())
    ok = (
        jp["checks"]["all_ok"]
        and jp["verdict"]["iso3_even_dual_rev"] == "LEMMA"
        and jp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso3_double(ISO3_010) == ISO3_111
    assert iso3_double(ISO3_001) == ISO3_001
    assert iso3_even(6, 6) == ISO3_010
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = dbl_table()
    sc = dbl_cover()
    k0 = killed_mid_stays()
    k1 = killed_end_swaps()
    k2 = killed_odd_stays_111()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dbl_table": {k: rt[k] for k in rt if k != "ok"},
        "dbl_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_mid_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_end_swaps": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_stays_111": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "iso3_double": True,
            "iso3_double_col": True,
            "covering_iso3_double": True,
            "mid_stays": False,
            "end_swaps": False,
            "odd_stays_111": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "iso3_double": "LEMMA",
            "iso3_double_col": "LEMMA",
            "covering_iso3_double": "LEMMA",
            "mid_stays": "KILLED",
            "end_swaps": "KILLED",
            "odd_stays_111": "KILLED",
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
    print("dbl_table", dump["dbl_table"])
    cov = dump["dbl_cover"]
    print(
        "dbl_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_dbl",
        cov["n_dbl"],
        "n_stay_001",
        cov["n_stay_001"],
        "n_stay_100",
        cov["n_stay_100"],
        "n_flip_010",
        cov["n_flip_010"],
        "n_flip_111",
        cov["n_flip_111"],
    )
    print("killed_mid_stays", dump["killed_mid_stays"])
    print("killed_end_swaps", dump["killed_end_swaps"])
    print("killed_odd_stays_111", dump["killed_odd_stays_111"])


if __name__ == "__main__":
    main()
