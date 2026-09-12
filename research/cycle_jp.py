#!/usr/bin/env python3
"""Cycle JP: dual of iso3_even is the bit-reverse of the half 3-window.

Palindrome dual j -> 2n-j reverses even-n iso3_even. 001 swaps with
100; 010 and 111 are palindromes. Dual of 001 is not 001; dual of
010 is not 001; dual iso3 is the reverse. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jp.py --certify
Dump: research/cycle_jp.json
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
from cycle_je import dual_iso_start
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111
from cycle_jh import iso3_even
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JO_JSON = Path(__file__).resolve().parent / "cycle_jo.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

ISO3_SWAP = (ISO3_001, ISO3_100)
ISO3_PAL = (ISO3_010, ISO3_111)


def iso3_rev(three):
    """Bit-reverse of an even-n isolated-one 3-window."""
    return three[::-1]


def iso3_rev_table() -> dict:
    """n<64: dual iso3_even is reverse; 001/100 swap, 010/111 palindromes."""
    if iso3_rev(ISO3_001) != ISO3_100 or iso3_rev(ISO3_100) != ISO3_001:
        return {"ok": False, "swap": True}
    if iso3_rev(ISO3_010) != ISO3_010 or iso3_rev(ISO3_111) != ISO3_111:
        return {"ok": False, "pal": True}
    n_iso = n_pal = n_swap = n_001 = n_010 = n_100 = n_111 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if n % 2 or n <= 0 or not isolated_one(n, j):
                continue
            three = iso3_even(n, j)
            j2 = dual_iso_start(n, j)
            three2 = iso3_even(n, j2)
            if three2 != iso3_rev(three) or not isolated_one(n, j2):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "j2": j2,
                }
            n_iso += 1
            if three == three[::-1]:
                n_pal += 1
            else:
                n_swap += 1
            if three == ISO3_001:
                n_001 += 1
            elif three == ISO3_010:
                n_010 += 1
            elif three == ISO3_100:
                n_100 += 1
            else:
                n_111 += 1
    ok = (
        n_iso == 415
        and n_pal == 185
        and n_swap == 230
        and n_001 == 115
        and n_010 == 141
        and n_100 == 115
        and n_111 == 44
        and iso3_even(2, 4) == iso3_rev(iso3_even(2, 0))
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support iso3_even reverse on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_even = n_dual = 0
    n_pal = n_swap = n_001 = n_010 = n_100 = n_111 = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in bits:
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                if n % 2 or n <= 0:
                    continue
                n_even += 1
                three = iso3_even(n, j)
                j2 = dual_iso_start(n, j)
                if j2 not in bits:
                    continue
                three2 = iso3_even(n, j2)
                if three2 != iso3_rev(three):
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if three == three[::-1]:
                    n_pal += 1
                else:
                    n_swap += 1
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
        "n_even": n_even,
        "n_dual": n_dual,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "xor_j": xor_j,
    }


def iso3_rev_cover() -> dict:
    """Dual-in-support reverse on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_even = n_dual = 0
    n_pal = n_swap = n_001 = n_010 = n_100 = n_111 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rev(k, q)
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
            n_even += w["n_even"]
            n_dual += w["n_dual"]
            n_pal += w["n_pal"]
            n_swap += w["n_swap"]
            n_001 += w["n_001"]
            n_010 += w["n_010"]
            n_100 += w["n_100"]
            n_111 += w["n_111"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_even": w["n_even"],
                "n_dual": w["n_dual"],
                "n_pal": w["n_pal"],
                "n_swap": w["n_swap"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_even == 7030
        and n_dual == 5833
        and n_pal == 2537
        and n_swap == 3296
        and n_001 == 1648
        and n_010 == 1935
        and n_100 == 1648
        and n_111 == 602
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_even": n_even,
        "n_dual": n_dual,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_001": n_001,
        "n_010": n_010,
        "n_100": n_100,
        "n_111": n_111,
        "rows": rows,
    }


def killed_001_stays() -> dict:
    """Dual of 001 is 001: G(2,0) 001 dualizes to 100."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    three = iso3_even(n, j)
    three2 = iso3_even(n, j2)
    ok = (
        three == ISO3_001
        and three2 == iso3_rev(three) == ISO3_100
        and three2 != ISO3_001
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def killed_010_is_001() -> dict:
    """Dual of 010 is 001: G(2,2) 010 is a palindrome."""
    k, s, n, j, p, p2 = 1, 15, 2, 2, 16, 16
    j2 = dual_iso_start(n, j)
    three = iso3_even(n, j)
    three2 = iso3_even(n, j2)
    ok = (
        three == ISO3_010
        and three2 == iso3_rev(three) == ISO3_010
        and three2 != ISO3_001
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def killed_dual_not_reverse() -> dict:
    """Dual iso3 is not reverse: G(2,0) dual equals reverse."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    three = iso3_even(n, j)
    three2 = iso3_even(n, j2)
    ok = three2 == iso3_rev(three) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "three": list(three),
        "three2": list(three2),
    }


def prefixes() -> dict:
    jo = json.loads(JO_JSON.read_text())
    ok = (
        jo["checks"]["all_ok"]
        and jo["verdict"]["core_slot_dbl"] == "LEMMA"
        and jo["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert iso3_rev(ISO3_001) == ISO3_100
    assert iso3_rev(ISO3_010) == ISO3_010
    assert iso3_even(2, 4) == iso3_rev(iso3_even(2, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = iso3_rev_table()
    sc = iso3_rev_cover()
    k0 = killed_001_stays()
    k1 = killed_010_is_001()
    k2 = killed_dual_not_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "iso3_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "iso3_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_001_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_010_is_001": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_not_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "iso3_rev": True,
            "iso3_even_dual_rev": True,
            "covering_iso3_rev": True,
            "end_stays": False,
            "pal_is_001": False,
            "dual_not_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "iso3_rev": "LEMMA",
            "iso3_even_dual_rev": "LEMMA",
            "covering_iso3_rev": "LEMMA",
            "end_stays": "KILLED",
            "pal_is_001": "KILLED",
            "dual_not_reverse": "KILLED",
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
    print("iso3_rev_table", dump["iso3_rev_table"])
    cov = dump["iso3_rev_cover"]
    print(
        "iso3_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_even",
        cov["n_even"],
        "n_dual",
        cov["n_dual"],
        "n_pal",
        cov["n_pal"],
        "n_swap",
        cov["n_swap"],
    )
    print("killed_001_stays", dump["killed_001_stays"])
    print("killed_010_is_001", dump["killed_010_is_001"])
    print("killed_dual_not_reverse", dump["killed_dual_not_reverse"])


if __name__ == "__main__":
    main()
