#!/usr/bin/env python3
"""Cycle JB: dual of pair_lift6 is the bit-reverse of the parent 6-window.

Palindrome dual j -> 2n-j-1 reverses the parent 6-window, swapping
left 000100 with right 001000 and the two iso SAT windows 000101
and 101000. Unsat LIFT2 windows 011110 and 110011 are palindromes.
Dual of left lift is not left; dual of iso SAT is not the same
window; dual lift is the reverse. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jb.py --certify
Dump: research/cycle_jb.json
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
from cycle_iy import dual_kind, dual_pair_start
from cycle_ja import (
    ISO_EVEN_J,
    ISO_ODD_J,
    LIFT2,
    LIFT_LEFT,
    LIFT_RIGHT,
    kind_lift6,
    pair_lift6,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JA_JSON = Path(__file__).resolve().parent / "cycle_ja.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT2_UNSAT = ((0, 1, 1, 1, 1, 0), (1, 1, 0, 0, 1, 1))


def lift6_rev(six):
    """Bit-reverse of a parent 6-window."""
    return six[::-1]


def lift_rev_table() -> dict:
    """n<64: dual pair_lift6 is reverse; LIFT2 SAT swap, unsat palindromes."""
    if lift6_rev(LIFT_LEFT) != LIFT_RIGHT or lift6_rev(LIFT_RIGHT) != LIFT_LEFT:
        return {"ok": False, "lr": True}
    if lift6_rev(ISO_EVEN_J) != ISO_ODD_J or lift6_rev(ISO_ODD_J) != ISO_EVEN_J:
        return {"ok": False, "iso": True}
    for six in LIFT2_UNSAT:
        if lift6_rev(six) != six or six in (ISO_EVEN_J, ISO_ODD_J):
            return {"ok": False, "pal": True, "six": list(six)}
    if set(LIFT2) != set(LIFT2_UNSAT + (ISO_EVEN_J, ISO_ODD_J)):
        return {"ok": False, "fam": True}
    n_g11 = n_left = n_right = n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = kind_lift6(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            j2 = dual_pair_start(n, j)
            six = pair_lift6(n, j)
            six2 = pair_lift6(n, j2)
            if (
                six != pred
                or six2 != lift6_rev(six)
                or kind_lift6(n, j2) != lift6_rev(pred)
                or g_run_kind(n, j2) != dual_kind(kind)
            ):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "j2": j2,
                }
            n_g11 += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
    ok = n_g11 == 512 and n_left == 141 and n_right == 141 and n_iso == 230
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support pair_lift6 reverse on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_dual = n_left = n_right = n_iso = 0
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
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                pred = kind_lift6(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                got = pair_lift6(n, j)
                if got != pred:
                    return {"ok": False, "lift": True, "k": k, "n": n, "j": j}
                n_g11 += 1
                j2 = dual_pair_start(n, j)
                if j2 not in bits or (j2 + 1) not in bits:
                    continue
                six2 = pair_lift6(n, j2)
                if six2 != lift6_rev(got) or kind_lift6(n, j2) != lift6_rev(pred):
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if kind == "left":
                    n_left += 1
                elif kind == "right":
                    n_right += 1
                else:
                    n_iso += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "xor_j": xor_j,
    }


def lift_rev_cover() -> dict:
    """Dual-in-support reverse on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_dual = n_left = n_right = n_iso = 0
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
            n_g11 += w["n_g11"]
            n_dual += w["n_dual"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso += w["n_iso"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_dual": w["n_dual"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso": w["n_iso"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_dual == 6968
        and n_left == 1942
        and n_right == 1942
        and n_iso == 3084
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_dual": n_dual,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "rows": rows,
    }


def killed_left_rev_left() -> dict:
    """Dual of left lift is left: G(1,0) 000100 reverses to 001000."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    six = pair_lift6(n, j)
    six2 = pair_lift6(n, j2)
    ok = (
        g_run_kind(n, j) == "left"
        and six == LIFT_LEFT
        and six2 == lift6_rev(six) == LIFT_RIGHT
        and six2 != LIFT_LEFT
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
        "six": list(six),
        "six2": list(six2),
    }


def killed_iso_same_window() -> dict:
    """Dual of iso SAT is the same window: G(3,0) 000101 vs 101000."""
    k, s, n, j, p, p2 = 1, 13, 3, 0, 20, 10
    j2 = dual_pair_start(n, j)
    six = pair_lift6(n, j)
    six2 = pair_lift6(n, j2)
    ok = (
        g_run_kind(n, j) == "iso"
        and six == ISO_EVEN_J
        and six2 == lift6_rev(six) == ISO_ODD_J
        and six2 != six
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
        "six": list(six),
        "six2": list(six2),
    }


def killed_dual_not_reverse() -> dict:
    """Dual lift is not reverse: G(1,0) dual equals reverse."""
    k, s, n, j, p, p2 = 0, 3, 1, 0, 6, 4
    j2 = dual_pair_start(n, j)
    six = pair_lift6(n, j)
    six2 = pair_lift6(n, j2)
    ok = six2 == lift6_rev(six) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "six": list(six),
        "six2": list(six2),
    }


def prefixes() -> dict:
    ja = json.loads(JA_JSON.read_text())
    ok = (
        ja["checks"]["all_ok"]
        and ja["verdict"]["LIFT2_sat"] == "LEMMA"
        and ja["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert lift6_rev(LIFT_LEFT) == LIFT_RIGHT
    assert lift6_rev(ISO_EVEN_J) == ISO_ODD_J
    assert lift6_rev((0, 1, 1, 1, 1, 0)) == (0, 1, 1, 1, 1, 0)
    assert pair_lift6(1, 1) == lift6_rev(pair_lift6(1, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift_rev_table()
    sc = lift_rev_cover()
    k0 = killed_left_rev_left()
    k1 = killed_iso_same_window()
    k2 = killed_dual_not_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "lift_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_left_rev_left": {k: k0[k] for k in k0 if k != "ok"},
        "killed_iso_same_window": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_not_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_lift6_rev": True,
            "lift6_rev_swap": True,
            "covering_lift6_rev": True,
            "left_rev_left": False,
            "iso_same_window": False,
            "dual_not_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_lift6_rev": "LEMMA",
            "lift6_rev_swap": "LEMMA",
            "covering_lift6_rev": "LEMMA",
            "left_rev_left": "KILLED",
            "iso_same_window": "KILLED",
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
    print("lift_rev_table", dump["lift_rev_table"])
    cov = dump["lift_rev_cover"]
    print(
        "lift_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_dual",
        cov["n_dual"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_iso",
        cov["n_iso"],
    )
    print("killed_left_rev_left", dump["killed_left_rev_left"])
    print("killed_iso_same_window", dump["killed_iso_same_window"])
    print("killed_dual_not_reverse", dump["killed_dual_not_reverse"])


if __name__ == "__main__":
    main()
