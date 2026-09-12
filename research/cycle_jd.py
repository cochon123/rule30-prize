#!/usr/bin/env python3
"""Cycle JD: isolated Green ones lift from the four LIFT1 5-windows.

LIFT1={11000,01110,10101,00011} are the 5-windows that
trinomial-lift to 010. Five of 16 parity cases are freshman-sat;
only 10101 is sat on even n. Every isolated one with n>0 lifts from
LIFT1; odd-n isolated ones all from 10101. Odd iso is not from
01110; even iso is not all 10101; seed n=0 has no parent window.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jd.py --certify
Dump: research/cycle_jd.json
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
from cycle_il import freshman_shape
from cycle_im import g5
from cycle_ir import isolated_one
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JC_JSON = Path(__file__).resolve().parent / "cycle_jc.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT1 = (
    (1, 1, 0, 0, 0),
    (0, 1, 1, 1, 0),
    (1, 0, 1, 0, 1),
    (0, 0, 0, 1, 1),
)
LIFT1_ODD = (1, 0, 1, 0, 1)


def trinomial3(five) -> tuple[int, int, int]:
    """Three-bit trinomial image of a 5-window."""
    return (
        five[0] ^ five[1] ^ five[2],
        five[1] ^ five[2] ^ five[3],
        five[2] ^ five[3] ^ five[4],
    )


def iso1_lift5(n: int, j: int):
    """Parent 5-window at n-1 starting at j-3; None for n=0."""
    if n <= 0:
        return None
    return g5(n - 1, j - 3)


def lift1_extend_sat(five, n_even: bool, j_even: bool) -> bool:
    """Whether a LIFT1 5-window extends to a freshman-sat 6-window."""
    return five in LIFT1 and any(
        freshman_shape(n_even, j_even, five + (b,)) for b in (0, 1)
    )


def lift1_table() -> dict:
    """LIFT1 completeness/SAT; n<64 isolated ones match LIFT1."""
    n_map = 0
    for x in range(32):
        five = tuple((x >> i) & 1 for i in range(5))
        if trinomial3(five) == (0, 1, 0):
            if five not in LIFT1:
                return {"ok": False, "extra": True, "five": list(five)}
            n_map += 1
    if n_map != 4:
        return {"ok": False, "n_map": n_map}
    n_sat = n_unsat = 0
    sat_ex = []
    for five in LIFT1:
        for n_even in (True, False):
            for j_even in (True, False):
                if lift1_extend_sat(five, n_even, j_even):
                    n_sat += 1
                    sat_ex.append((list(five), n_even, j_even))
                else:
                    n_unsat += 1
    want_sat = [
        ([1, 1, 0, 0, 0], False, False),
        ([0, 1, 1, 1, 0], False, False),
        ([1, 0, 1, 0, 1], True, True),
        ([1, 0, 1, 0, 1], False, False),
        ([0, 0, 0, 1, 1], False, False),
    ]
    if not (n_sat == 5 and n_unsat == 11 and sat_ex == want_sat):
        return {"ok": False, "sat": True, "n_sat": n_sat, "sat_ex": sat_ex}
    n_iso = n_seed = n_odd = n_even = n_odd_10101 = 0
    n_01110 = n_00011 = n_11000 = n_10101 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                if iso1_lift5(n, j) is not None:
                    return {"ok": False, "seed": True}
                continue
            five = iso1_lift5(n, j)
            if five not in LIFT1 or trinomial3(five) != (0, 1, 0):
                return {"ok": False, "lift": True, "n": n, "j": j, "five": list(five)}
            if five == (0, 1, 1, 1, 0):
                n_01110 += 1
            elif five == (0, 0, 0, 1, 1):
                n_00011 += 1
            elif five == (1, 1, 0, 0, 0):
                n_11000 += 1
            else:
                n_10101 += 1
            if n % 2:
                n_odd += 1
                if five != LIFT1_ODD:
                    return {"ok": False, "odd": True, "n": n, "j": j}
                n_odd_10101 += 1
            else:
                n_even += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_odd == 45
        and n_even == 415
        and n_odd_10101 == 45
        and n_01110 == 141
        and n_00011 == 115
        and n_11000 == 115
        and n_10101 == 89
    )
    return {
        "ok": ok,
        "n_map": n_map,
        "n_sat": n_sat,
        "n_unsat": n_unsat,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_odd_10101": n_odd_10101,
        "n_01110": n_01110,
        "n_00011": n_00011,
        "n_11000": n_11000,
        "n_10101": n_10101,
    }


def _walk_lift1(k: int, q: int) -> dict:
    """LIFT1 on covering isolated ones; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = n_odd_10101 = 0
    n_01110 = n_00011 = n_11000 = n_10101 = 0
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
                if five not in LIFT1:
                    return {"ok": False, "lift": True, "k": k, "n": n, "j": j}
                if five == (0, 1, 1, 1, 0):
                    n_01110 += 1
                elif five == (0, 0, 0, 1, 1):
                    n_00011 += 1
                elif five == (1, 1, 0, 0, 0):
                    n_11000 += 1
                else:
                    n_10101 += 1
                if n % 2:
                    n_odd += 1
                    if five != LIFT1_ODD:
                        return {"ok": False, "odd": True, "k": k, "n": n, "j": j}
                    n_odd_10101 += 1
                else:
                    n_even += 1
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
        "n_odd_10101": n_odd_10101,
        "n_01110": n_01110,
        "n_00011": n_00011,
        "n_11000": n_11000,
        "n_10101": n_10101,
        "xor_j": xor_j,
    }


def lift1_cover() -> dict:
    """LIFT1 on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_seed = n_odd = n_even = n_odd_10101 = 0
    n_01110 = n_00011 = n_11000 = n_10101 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_lift1(k, q)
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
            n_odd_10101 += w["n_odd_10101"]
            n_01110 += w["n_01110"]
            n_00011 += w["n_00011"]
            n_11000 += w["n_11000"]
            n_10101 += w["n_10101"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_seed": w["n_seed"],
                "n_odd": w["n_odd"],
                "n_even": w["n_even"],
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
        and n_odd_10101 == 741
        and n_01110 == 2373
        and n_00011 == 2011
        and n_11000 == 1912
        and n_10101 == 1475
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_odd": n_odd,
        "n_even": n_even,
        "n_odd_10101": n_odd_10101,
        "n_01110": n_01110,
        "n_00011": n_00011,
        "n_11000": n_11000,
        "n_10101": n_10101,
        "rows": rows,
    }


def killed_odd_from_01110() -> dict:
    """Odd iso from 01110: G(3,3) parent is 10101."""
    k, s, n, j, p = 0, 3, 3, 3, 4
    five = iso1_lift5(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 1
        and five == LIFT1_ODD
        and five != (0, 1, 1, 1, 0)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "five": list(five),
    }


def killed_even_all_10101() -> dict:
    """Even iso all from 10101: G(2,0) parent is 00011."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    five = iso1_lift5(n, j)
    ok = (
        isolated_one(n, j)
        and n % 2 == 0
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
        "five": list(five),
    }


def killed_seed_is_lift1() -> dict:
    """Seed n=0 is a LIFT1 window: no parent."""
    k, s, n, j, p = 0, 5, 0, 0, 6
    ok = isolated_one(n, j) and iso1_lift5(n, j) is None and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "five": None,
    }


def prefixes() -> dict:
    jc = json.loads(JC_JSON.read_text())
    ok = (
        jc["checks"]["all_ok"]
        and jc["verdict"]["half_neigh3_stretch"] == "LEMMA"
        and jc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert trinomial3(LIFT1_ODD) == (0, 1, 0)
    assert iso1_lift5(3, 3) == LIFT1_ODD
    assert iso1_lift5(2, 0) == (0, 0, 0, 1, 1)
    assert iso1_lift5(0, 0) is None
    assert lift1_extend_sat(LIFT1_ODD, True, True)
    assert not lift1_extend_sat((1, 1, 0, 0, 0), True, True)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift1_table()
    sc = lift1_cover()
    k0 = killed_odd_from_01110()
    k1 = killed_even_all_10101()
    k2 = killed_seed_is_lift1()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift1_table": {k: rt[k] for k in rt if k != "ok"},
        "lift1_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_odd_from_01110": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_all_10101": {k: k1[k] for k in k1 if k != "ok"},
        "killed_seed_is_lift1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "LIFT1_sat": True,
            "iso1_from_LIFT1": True,
            "covering_iso1_LIFT1": True,
            "odd_from_01110": False,
            "even_all_10101": False,
            "seed_is_LIFT1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "LIFT1_sat": "LEMMA",
            "iso1_from_LIFT1": "LEMMA",
            "covering_iso1_LIFT1": "LEMMA",
            "odd_from_01110": "KILLED",
            "even_all_10101": "KILLED",
            "seed_is_LIFT1": "KILLED",
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
    print("lift1_table", dump["lift1_table"])
    cov = dump["lift1_cover"]
    print(
        "lift1_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_seed",
        cov["n_seed"],
        "n_odd",
        cov["n_odd"],
        "n_even",
        cov["n_even"],
        "n_10101",
        cov["n_10101"],
    )
    print("killed_odd_from_01110", dump["killed_odd_from_01110"])
    print("killed_even_all_10101", dump["killed_even_all_10101"])
    print("killed_seed_is_lift1", dump["killed_seed_is_lift1"])


if __name__ == "__main__":
    main()
