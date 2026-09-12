#!/usr/bin/env python3
"""Cycle JK: 4-stretch preserves isolated-one LIFT1 windows.

iso1_lift5(4n,4j) equals iso1_lift5(n,j) for n>0, because
lift5_double is an involution. Interiors do not change under
4-stretch; ends do not change; odd iso does not become 01110.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jk.py --certify
Dump: research/cycle_jk.json
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
from cycle_jd import iso1_lift5
from cycle_ji import LIFT1_HI, LIFT1_LO, LIFT1_MID_EVEN, LIFT1_MID_ODD
from cycle_jj import lift5_double
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JJ_JSON = Path(__file__).resolve().parent / "cycle_jj.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def quad_table() -> dict:
    """n<64: iso1_lift5(4n,4j) equals parent; lift5_double involution."""
    for five in (LIFT1_LO, LIFT1_HI, LIFT1_MID_ODD, LIFT1_MID_EVEN):
        if lift5_double(lift5_double(five)) != five:
            return {"ok": False, "inv": True, "five": list(five)}
    n_iso = n_seed = n_lo = n_hi = n_mid_odd = n_mid_even = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            five = iso1_lift5(n, j)
            five4 = iso1_lift5(4 * n, 4 * j)
            if (
                not isolated_one(4 * n, 4 * j)
                or five4 != five
                or five4 != lift5_double(lift5_double(five))
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "five": list(five),
                    "five4": list(five4) if five4 else None,
                }
            if five == LIFT1_LO:
                n_lo += 1
            elif five == LIFT1_HI:
                n_hi += 1
            elif five == LIFT1_MID_ODD:
                n_mid_odd += 1
            else:
                n_mid_even += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_lo == 115
        and n_hi == 115
        and n_mid_odd == 141
        and n_mid_even == 89
        and iso1_lift5(8, 8) == iso1_lift5(2, 2) == LIFT1_MID_ODD
        and iso1_lift5(8, 0) == iso1_lift5(2, 0) == LIFT1_LO
        and iso1_lift5(12, 12) == iso1_lift5(3, 3) == LIFT1_MID_EVEN
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
    }


def _walk_quad(k: int, q: int) -> dict:
    """4-stretch identity on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_quad = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
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
                five = iso1_lift5(n, j)
                five4 = iso1_lift5(4 * n, 4 * j)
                if five4 != five:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                    }
                n_quad += 1
                if five == LIFT1_LO:
                    n_lo += 1
                elif five == LIFT1_HI:
                    n_hi += 1
                elif five == LIFT1_MID_ODD:
                    n_mid_odd += 1
                else:
                    n_mid_even += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_quad": n_quad,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "xor_j": xor_j,
    }


def quad_cover() -> dict:
    """4-stretch identity on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_quad = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
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
            n_lo += w["n_lo"]
            n_hi += w["n_hi"]
            n_mid_odd += w["n_mid_odd"]
            n_mid_even += w["n_mid_even"]
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
        and n_lo == 2011
        and n_hi == 1912
        and n_mid_odd == 2373
        and n_mid_even == 1475
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_quad": n_quad,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "rows": rows,
    }


def killed_mid_changes() -> dict:
    """Interiors change under 4-stretch: G(2,2) stays 01110 at G(8,8)."""
    k, s, n, j, p, p4 = 3, 43, 2, 2, 44, 32
    n4, j4 = 4 * n, 4 * j
    five = iso1_lift5(n, j)
    five4 = iso1_lift5(n4, j4)
    ok = (
        isolated_one(n, j)
        and isolated_one(n4, j4)
        and five == LIFT1_MID_ODD
        and five4 == five
        and five4 != LIFT1_MID_EVEN
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
        "five": list(five),
        "five4": list(five4),
    }


def killed_end_changes() -> dict:
    """Ends change under 4-stretch: G(2,0) stays 00011 at G(8,0)."""
    k, s, n, j, p, p4 = 3, 43, 2, 0, 48, 48
    n4, j4 = 4 * n, 4 * j
    five = iso1_lift5(n, j)
    five4 = iso1_lift5(n4, j4)
    ok = (
        isolated_one(n, j)
        and isolated_one(n4, j4)
        and five == LIFT1_LO
        and five4 == five
        and five4 != LIFT1_HI
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
        "five": list(five),
        "five4": list(five4),
    }


def killed_odd_to_01110() -> dict:
    """Odd iso 4-stretch is 01110: G(3,3) stays 10101 at G(12,12)."""
    k, s, n, j, p, p4 = 3, 73, 3, 3, 74, 56
    n4, j4 = 4 * n, 4 * j
    five = iso1_lift5(n, j)
    five4 = iso1_lift5(n4, j4)
    ok = (
        isolated_one(n, j)
        and n % 2 == 1
        and isolated_one(n4, j4)
        and five == LIFT1_MID_EVEN
        and five4 == five
        and five4 != LIFT1_MID_ODD
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
        "five": list(five),
        "five4": list(five4),
    }


def prefixes() -> dict:
    jj = json.loads(JJ_JSON.read_text())
    ok = (
        jj["checks"]["all_ok"]
        and jj["verdict"]["lift5_double"] == "LEMMA"
        and jj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert lift5_double(lift5_double(LIFT1_MID_ODD)) == LIFT1_MID_ODD
    assert iso1_lift5(8, 8) == iso1_lift5(2, 2)
    assert iso1_lift5(12, 12) == iso1_lift5(3, 3)
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
    k2 = killed_odd_to_01110()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "quad_table": {k: rt[k] for k in rt if k != "ok"},
        "quad_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_mid_changes": {k: k0[k] for k in k0 if k != "ok"},
        "killed_end_changes": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_to_01110": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "lift5_double_involution": True,
            "iso1_quad_col": True,
            "covering_lift5_quad": True,
            "mid_changes": False,
            "end_changes": False,
            "odd_to_01110": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "lift5_double_involution": "LEMMA",
            "iso1_quad_col": "LEMMA",
            "covering_lift5_quad": "LEMMA",
            "mid_changes": "KILLED",
            "end_changes": "KILLED",
            "odd_to_01110": "KILLED",
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
        "n_lo",
        cov["n_lo"],
        "n_hi",
        cov["n_hi"],
        "n_mid_odd",
        cov["n_mid_odd"],
        "n_mid_even",
        cov["n_mid_even"],
    )
    print("killed_mid_changes", dump["killed_mid_changes"])
    print("killed_end_changes", dump["killed_end_changes"])
    print("killed_odd_to_01110", dump["killed_odd_to_01110"])


if __name__ == "__main__":
    main()
