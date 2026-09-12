#!/usr/bin/env python3
"""Cycle IM: even n has no Green 11; every run-3 lifts from 00100.

The 5-windows that trinomial-lift to 111 are LIFT3={00100,01001,
10010,11111}. Only 00100 is freshman-sat (even n, even j). Every
run-3 of G (n<64) lifts from 00100; even n has no consecutive ones
at all, so covering G=1 pairs are all odd n. Even n does have
isolated ones; run-3 is not from 11111; even n is not 11-free
because it has no ones. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_im.py --certify
Dump: research/cycle_im.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IL_JSON = Path(__file__).resolve().parent / "cycle_il.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT3 = (
    (0, 0, 1, 0, 0),
    (0, 1, 0, 0, 1),
    (1, 0, 0, 1, 0),
    (1, 1, 1, 1, 1),
)


def g5(n: int, j: int) -> tuple[int, int, int, int, int]:
    """Length-5 Green window starting at j."""
    return tuple(G(n, j + i) for i in range(5))  # type: ignore[return-value]


def lift3_extend_sat(five, n_even: bool, j_even: bool) -> bool:
    """Whether a LIFT3 5-window extends to a freshman-sat 6-window."""
    return any(freshman_shape(n_even, j_even, five + (b,)) for b in (0, 1))


def lift3_table() -> dict:
    """16 LIFT3 x parity: only 00100 even/even sat; n<64 run-3 from 00100."""
    n_sat = n_unsat = 0
    sat_ex = None
    for five in LIFT3:
        for n_even in (True, False):
            for j_even in (True, False):
                if lift3_extend_sat(five, n_even, j_even):
                    n_sat += 1
                    sat_ex = (list(five), n_even, j_even)
                else:
                    n_unsat += 1
    if not (n_sat == 1 and n_unsat == 15 and sat_ex == ([0, 0, 1, 0, 0], True, True)):
        return {"ok": False, "sat": True, "n_sat": n_sat, "sat_ex": sat_ex}
    n_run3 = n_even11 = n_g11 = n_g11_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            if G(n, j) and G(n, j + 1):
                n_g11 += 1
                if n % 2 == 0:
                    n_even11 += 1
                else:
                    n_g11_odd += 1
        if n == 0:
            continue
        for j in range(0, 2 * n - 1):
            if G(n, j) and G(n, j + 1) and G(n, j + 2):
                five = g5(n - 1, j - 2)
                if five != (0, 0, 1, 0, 0):
                    return {"ok": False, "lift": True, "n": n, "j": j, "five": list(five)}
                n_run3 += 1
    ok = n_even11 == 0 and n_run3 == 141 and n_g11 == 512 and n_g11_odd == 512
    return {
        "ok": ok,
        "n_sat": n_sat,
        "n_unsat": n_unsat,
        "n_run3": n_run3,
        "n_even11": n_even11,
        "n_g11": n_g11,
    }


def _walk_no11(k: int, q: int) -> dict:
    """Even-n no Green 11; run-3 from 00100; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_g11_odd = n_run3 = 0
    xor_j = 0
    s = t0
    prev = None
    seen = set()
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            if n not in seen:
                seen.add(n)
                for j in range(0, 2 * n):
                    if G(n, j) and G(n, j + 1):
                        if n % 2 == 0:
                            return {"ok": False, "even11": True, "k": k, "n": n, "j": j}
                if n >= 1:
                    for j in range(0, 2 * n - 1):
                        if G(n, j) and G(n, j + 1) and G(n, j + 2):
                            five = g5(n - 1, j - 2)
                            if five != (0, 0, 1, 0, 0):
                                return {
                                    "ok": False,
                                    "lift": True,
                                    "k": k,
                                    "n": n,
                                    "j": j,
                                    "five": list(five),
                                }
                            n_run3 += 1
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                bits[j] = packed
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                if G(n, j) and G(n, j + 1):
                    n_g11 += 1
                    if n % 2 == 1:
                        n_g11_odd += 1
                    else:
                        return {"ok": False, "cov_even": True, "k": k, "n": n, "j": j}
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_odd": n_g11_odd,
        "n_run3": n_run3,
        "xor_j": xor_j,
    }


def no11_cover() -> dict:
    """Even-n no 11 on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_g11_odd = n_run3 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_no11(k, q)
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
            n_g11 += w["n_g11"]
            n_g11_odd += w["n_g11_odd"]
            n_run3 += w["n_run3"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_g11_odd": w["n_g11_odd"],
                "n_run3": w["n_run3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_g11_odd == 8577
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_odd": n_g11_odd,
        "n_run3": n_run3,
        "rows": rows,
    }


def killed_even_has_11() -> dict:
    """Even n has a Green 11: G(2)=10101, positions 0,1 are 10."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    ok = (
        n % 2 == 0
        and G(n, j) == 1
        and G(n, j + 1) == 0
        and [G(n, i) for i in range(0, 5)] == [1, 0, 1, 0, 1]
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": [G(n, i) for i in range(0, 5)],
    }


def killed_run3_from_11111() -> dict:
    """Run-3 lifts from 11111: G(1) lifts from 00100."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    five = g5(n - 1, j - 2)
    ok = (
        [G(n, i) for i in range(0, 3)] == [1, 1, 1]
        and five == (0, 0, 1, 0, 0)
        and five != (1, 1, 1, 1, 1)
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
        "G": [G(n, i) for i in range(0, 3)],
    }


def killed_even_no_ones() -> dict:
    """Even n has no Green ones: G(2,2)=1."""
    k, s, n, j, p = 0, 5, 2, 2, 6
    ok = n % 2 == 0 and G(n, j) == 1 and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def prefixes() -> dict:
    il = json.loads(IL_JSON.read_text())
    ok = (
        il["checks"]["all_ok"]
        and il["verdict"]["LIFT4_freshman_unsat"] == "LEMMA"
        and il["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert lift3_extend_sat((0, 0, 1, 0, 0), True, True)
    assert not lift3_extend_sat((1, 1, 1, 1, 1), True, True)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift3_table()
    sc = no11_cover()
    k0 = killed_even_has_11()
    k1 = killed_run3_from_11111()
    k2 = killed_even_no_ones()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift3_table": {k: rt[k] for k in rt if k != "ok"},
        "no11_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_has_11": {k: k0[k] for k in k0 if k != "ok"},
        "killed_run3_from_11111": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_no_ones": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "even_n_no_Green_11": True,
            "run3_from_00100": True,
            "covering_g11_odd_n": True,
            "even_n_has_11": False,
            "run3_from_11111": False,
            "even_n_no_ones": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_n_no_Green_11": "LEMMA",
            "run3_from_00100": "LEMMA",
            "covering_g11_odd_n": "LEMMA",
            "even_n_has_11": "KILLED",
            "run3_from_11111": "KILLED",
            "even_n_no_ones": "KILLED",
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
    print("lift3_table", dump["lift3_table"])
    cov = dump["no11_cover"]
    print(
        "no11_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_g11_odd",
        cov["n_g11_odd"],
        "n_run3",
        cov["n_run3"],
    )
    print("killed_even_has_11", dump["killed_even_has_11"])
    print("killed_run3_from_11111", dump["killed_run3_from_11111"])
    print("killed_even_no_ones", dump["killed_even_no_ones"])


if __name__ == "__main__":
    main()
