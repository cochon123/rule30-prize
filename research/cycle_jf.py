#!/usr/bin/env python3
"""Cycle JF: iso1_lift5 is the freshman stretch of the half 3-window.

On even n=2m>0 the parent is odd, so the 5-window is the cob-stretch
(a, a XOR b, b, b XOR c, c) of (G(m-1,k-2), G(m-1,k-1), G(m-1,k))
at even j=2k. The four odd-weight 3-tuples map onto LIFT1. On odd n
the parent is even and the 3-window is always 111, stretching to
10101. Even iso is not always cob of 111; even half 3-window is not
always 010; even-n lift is not the even-parent zero-stretch. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jf.py --certify
Dump: research/cycle_jf.json
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
from cycle_jd import LIFT1, LIFT1_ODD, iso1_lift5
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JE_JSON = Path(__file__).resolve().parent / "cycle_je.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

ISO3_001 = (0, 0, 1)
ISO3_010 = (0, 1, 0)
ISO3_100 = (1, 0, 0)
ISO3_111 = (1, 1, 1)
ISO3_ODD = ISO3_111


def iso_half3(n: int, j: int):
    """Half 3-window for an isolated one; None for n=0 or non-iso."""
    if n <= 0 or not isolated_one(n, j):
        return None
    if n % 2 == 0:
        m, k = n // 2, j // 2
        return (G(m - 1, k - 2), G(m - 1, k - 1), G(m - 1, k))
    m = n // 2
    t = (j - 1) // 2
    return (G(m, t - 1), G(m, t), G(m, t + 1))


def freshman_lift5(three, parent_even: bool):
    """Stretch a 3-window onto a parent-parity 5-window."""
    a, b, c = three
    if parent_even:
        return (a, 0, b, 0, c)
    return (a, a ^ b, b, b ^ c, c)


def half5_table() -> dict:
    """n<64: iso1_lift5 equals freshman_lift5 of iso_half3."""
    n_iso = n_seed = n_even = n_odd = n_odd_111 = 0
    n_001 = n_010 = n_100 = n_111 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            three = iso_half3(n, j)
            if n == 0:
                n_seed += 1
                if three is not None:
                    return {"ok": False, "seed": True}
                continue
            pred = freshman_lift5(three, n % 2 == 1)
            five = iso1_lift5(n, j)
            if pred != five or five not in LIFT1:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "three": list(three),
                    "pred": list(pred),
                    "five": list(five),
                }
            if n % 2:
                n_odd += 1
                if three != ISO3_ODD:
                    return {"ok": False, "odd": True, "n": n, "j": j}
                n_odd_111 += 1
            else:
                n_even += 1
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
        and n_odd_111 == 45
        and n_001 == 115
        and n_010 == 141
        and n_100 == 115
        and n_111 == 44
        and freshman_lift5(ISO3_001, False) == (0, 0, 0, 1, 1)
        and freshman_lift5(ISO3_010, False) == (0, 1, 1, 1, 0)
        and freshman_lift5(ISO3_100, False) == (1, 1, 0, 0, 0)
        and freshman_lift5(ISO3_111, False) == LIFT1_ODD
        and freshman_lift5(ISO3_ODD, True) == LIFT1_ODD
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_odd_111": n_odd_111,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
    }


def _walk_half5(k: int, q: int) -> dict:
    """Half 3-window stretch on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_even = n_odd = n_odd_111 = 0
    n_001 = n_010 = n_100 = n_111 = 0
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
                three = iso_half3(n, j)
                if n == 0:
                    n_seed += 1
                    if three is not None:
                        return {"ok": False, "seed": True, "k": k}
                    continue
                pred = freshman_lift5(three, n % 2 == 1)
                five = iso1_lift5(n, j)
                if pred != five:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                if n % 2:
                    n_odd += 1
                    if three != ISO3_ODD:
                        return {"ok": False, "odd": True, "k": k, "n": n, "j": j}
                    n_odd_111 += 1
                else:
                    n_even += 1
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
        "n_even": n_even,
        "n_odd": n_odd,
        "n_odd_111": n_odd_111,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "xor_j": xor_j,
    }


def half5_cover() -> dict:
    """Half 3-window stretch on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_even = n_odd = n_odd_111 = 0
    n_001 = n_010 = n_100 = n_111 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_half5(k, q)
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
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            n_odd_111 += w["n_odd_111"]
            n_001 += w["n_001"]
            n_010 += w["n_010"]
            n_100 += w["n_100"]
            n_111 += w["n_111"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_even": w["n_even"],
                "n_odd": w["n_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_even == 7030
        and n_odd == 741
        and n_odd_111 == 741
        and n_001 == 2011
        and n_010 == 2373
        and n_100 == 1912
        and n_111 == 734
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_odd_111": n_odd_111,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "rows": rows,
    }


def killed_even_all_111() -> dict:
    """Even iso always cob of 111: G(2,0) is cob of 001."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    three = iso_half3(n, j)
    five = freshman_lift5(three, False)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and three == ISO3_001
        and three != ISO3_111
        and five == (0, 0, 0, 1, 1)
        and five != LIFT1_ODD
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "three": list(three),
        "five": list(five),
    }


def killed_half3_always_010() -> dict:
    """Even half 3-window is always 010: G(2,4) is 100."""
    k, s, n, j, p = 1, 7, 2, 4, 4
    three = iso_half3(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and three == ISO3_100
        and three != ISO3_010
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "three": list(three),
    }


def killed_even_is_even5() -> dict:
    """Even-n lift is even-parent zero-stretch: G(2,0) is cob 00011."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    three = iso_half3(n, j)
    even5 = freshman_lift5(three, True)
    cob = freshman_lift5(three, False)
    five = iso1_lift5(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
        and even5 == (0, 0, 0, 0, 1)
        and cob == five == (0, 0, 0, 1, 1)
        and even5 != cob
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "three": list(three),
        "even5": list(even5),
        "cob": list(cob),
    }


def prefixes() -> dict:
    je = json.loads(JE_JSON.read_text())
    ok = (
        je["checks"]["all_ok"]
        and je["verdict"]["dual_lift5_rev"] == "LEMMA"
        and je["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso_half3(0, 0) is None
    assert iso_half3(2, 0) == ISO3_001
    assert iso_half3(2, 4) == ISO3_100
    assert iso_half3(3, 3) == ISO3_ODD
    assert freshman_lift5(ISO3_ODD, True) == LIFT1_ODD
    assert freshman_lift5(iso_half3(2, 0), False) == iso1_lift5(2, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = half5_table()
    sc = half5_cover()
    k0 = killed_even_all_111()
    k1 = killed_half3_always_010()
    k2 = killed_even_is_even5()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "half5_table": {k: rt[k] for k in rt if k != "ok"},
        "half5_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_all_111": {k: k0[k] for k in k0 if k != "ok"},
        "killed_half3_always_010": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_is_even5": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "iso_half3_stretch": True,
            "iso3_to_LIFT1": True,
            "covering_half_lift5": True,
            "even_all_111": False,
            "half3_always_010": False,
            "even_is_even5": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "iso_half3_stretch": "LEMMA",
            "iso3_to_LIFT1": "LEMMA",
            "covering_half_lift5": "LEMMA",
            "even_all_111": "KILLED",
            "half3_always_010": "KILLED",
            "even_is_even5": "KILLED",
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
    print("half5_table", dump["half5_table"])
    cov = dump["half5_cover"]
    print(
        "half5_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_seed",
        cov["n_seed"],
        "n_even",
        cov["n_even"],
        "n_odd",
        cov["n_odd"],
        "n_001",
        cov["n_001"],
        "n_010",
        cov["n_010"],
        "n_100",
        cov["n_100"],
        "n_111",
        cov["n_111"],
    )
    print("killed_even_all_111", dump["killed_even_all_111"])
    print("killed_half3_always_010", dump["killed_half3_always_010"])
    print("killed_even_is_even5", dump["killed_even_is_even5"])


if __name__ == "__main__":
    main()
