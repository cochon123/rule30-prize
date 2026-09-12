#!/usr/bin/env python3
"""Cycle JA: isolated Green pairs lift from the two SAT LIFT2 windows.

LIFT2={101000,011110,000101,110011} are the 6-windows that
trinomial-lift to 0110. Only 101000 (even n, even j) and 000101
(even n, odd j) are freshman-sat. Every iso pair lifts from those
two, predicted by j parity; left lifts from 000100; right from
001000. Iso is not from 011110; iso is not a unique window; left
is not from 011111. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_ja.py --certify
Dump: research/cycle_ja.json
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
from cycle_ik import g6
from cycle_il import freshman_shape
from cycle_in import g_run_kind
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IZ_JSON = Path(__file__).resolve().parent / "cycle_iz.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT2 = (
    (1, 0, 1, 0, 0, 0),
    (0, 1, 1, 1, 1, 0),
    (0, 0, 0, 1, 0, 1),
    (1, 1, 0, 0, 1, 1),
)
LIFT2_SAT = ((1, 0, 1, 0, 0, 0), (0, 0, 0, 1, 0, 1))
LIFT_LEFT = (0, 0, 0, 1, 0, 0)
LIFT_RIGHT = (0, 0, 1, 0, 0, 0)
ISO_EVEN_J = (0, 0, 0, 1, 0, 1)
ISO_ODD_J = (1, 0, 1, 0, 0, 0)


def trinomial4(six) -> tuple[int, int, int, int]:
    """Four-bit trinomial image of a 6-window."""
    return (
        six[0] ^ six[1] ^ six[2],
        six[1] ^ six[2] ^ six[3],
        six[2] ^ six[3] ^ six[4],
        six[3] ^ six[4] ^ six[5],
    )


def pair_lift6(n: int, j: int):
    """Parent 6-window at n-1 starting at j-3."""
    return g6(n - 1, j - 3)


def kind_lift6(n: int, j: int):
    """Predicted parent 6-window from g_run_kind and j parity."""
    kind = g_run_kind(n, j)
    if kind is None:
        return None
    if kind == "left":
        return LIFT_LEFT
    if kind == "right":
        return LIFT_RIGHT
    return ISO_EVEN_J if j % 2 == 0 else ISO_ODD_J


def lift2_sat(six, n_even: bool, j_even: bool) -> bool:
    """Whether a LIFT2 6-window is freshman-sat on this parity."""
    return six in LIFT2 and freshman_shape(n_even, j_even, six)


def lift2_table() -> dict:
    """LIFT2 completeness/SAT; n<64 pair lifts match kind_lift6."""
    n_map = 0
    for x in range(64):
        six = tuple((x >> i) & 1 for i in range(6))
        if trinomial4(six) == (0, 1, 1, 0):
            if six not in LIFT2:
                return {"ok": False, "extra": True, "six": list(six)}
            n_map += 1
    if n_map != 4:
        return {"ok": False, "n_map": n_map}
    n_sat = n_unsat = 0
    sat_ex = []
    for six in LIFT2:
        for n_even in (True, False):
            for j_even in (True, False):
                if lift2_sat(six, n_even, j_even):
                    n_sat += 1
                    sat_ex.append((list(six), n_even, j_even))
                else:
                    n_unsat += 1
    want_sat = [
        ([1, 0, 1, 0, 0, 0], True, True),
        ([0, 0, 0, 1, 0, 1], True, False),
    ]
    if not (n_sat == 2 and n_unsat == 14 and sat_ex == want_sat):
        return {"ok": False, "sat": True, "n_sat": n_sat, "sat_ex": sat_ex}
    n_iso = n_left = n_right = n_iso_even = n_iso_odd = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = kind_lift6(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            got = pair_lift6(n, j)
            if pred != got:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "got": list(got),
                    "pred": list(pred),
                }
            if kind == "iso":
                if got not in LIFT2_SAT:
                    return {"ok": False, "unsat": True, "n": n, "j": j}
                n_iso += 1
                if j % 2 == 0:
                    n_iso_even += 1
                else:
                    n_iso_odd += 1
            elif kind == "left":
                if got != LIFT_LEFT:
                    return {"ok": False, "left": True, "n": n, "j": j}
                n_left += 1
            else:
                if got != LIFT_RIGHT:
                    return {"ok": False, "right": True, "n": n, "j": j}
                n_right += 1
    ok = (
        n_iso == 230
        and n_left == 141
        and n_right == 141
        and n_iso_even == 115
        and n_iso_odd == 115
    )
    return {
        "ok": ok,
        "n_map": n_map,
        "n_sat": n_sat,
        "n_unsat": n_unsat,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
    }


def _walk_lift(k: int, q: int) -> dict:
    """Pair-kind parent 6-windows on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_iso = n_left = n_right = 0
    n_iso_even = n_iso_odd = 0
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
                if pred != got:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                    }
                n_g11 += 1
                if kind == "iso":
                    n_iso += 1
                    if j % 2 == 0:
                        n_iso_even += 1
                    else:
                        n_iso_odd += 1
                elif kind == "left":
                    n_left += 1
                else:
                    n_right += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "xor_j": xor_j,
    }


def lift2_cover() -> dict:
    """Pair-kind lifts on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_iso = n_left = n_right = 0
    n_iso_even = n_iso_odd = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_lift(k, q)
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
            n_iso += w["n_iso"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso_even += w["n_iso_even"]
            n_iso_odd += w["n_iso_odd"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_iso": w["n_iso"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso_even": w["n_iso_even"],
                "n_iso_odd": w["n_iso_odd"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_iso == 3817
        and n_left == 2380
        and n_right == 2380
        and n_iso_even == 1912
        and n_iso_odd == 1905
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso_even": n_iso_even,
        "n_iso_odd": n_iso_odd,
        "rows": rows,
    }


def killed_iso_from_011110() -> dict:
    """Iso lifts from 011110: G(3,0) parent is 000101."""
    k, s, n, j, p = 1, 5, 3, 0, 12
    got = pair_lift6(n, j)
    ok = (
        g_run_kind(n, j) == "iso"
        and got == ISO_EVEN_J
        and got != (0, 1, 1, 1, 1, 0)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "iso",
        "six": list(got),
    }


def killed_iso_unique_window() -> dict:
    """Iso from a unique SAT window: G(3,5) parent is 101000."""
    k, s, n, j, p = 1, 13, 3, 5, 10
    got = pair_lift6(n, j)
    ok = (
        g_run_kind(n, j) == "iso"
        and got == ISO_ODD_J
        and got != ISO_EVEN_J
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "iso",
        "six": list(got),
    }


def killed_left_from_011111() -> dict:
    """Left lifts from 011111: G(1,0) parent is 000100."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    got = pair_lift6(n, j)
    ok = (
        g_run_kind(n, j) == "left"
        and got == LIFT_LEFT
        and got != (0, 1, 1, 1, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "left",
        "six": list(got),
    }


def prefixes() -> dict:
    iz = json.loads(IZ_JSON.read_text())
    ok = (
        iz["checks"]["all_ok"]
        and iz["verdict"]["kind_green4"] == "LEMMA"
        and iz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert kind_lift6(3, 0) == ISO_EVEN_J
    assert kind_lift6(3, 5) == ISO_ODD_J
    assert kind_lift6(1, 0) == LIFT_LEFT
    assert kind_lift6(1, 1) == LIFT_RIGHT
    assert kind_lift6(2, 0) is None
    assert trinomial4(ISO_EVEN_J) == (0, 1, 1, 0)
    assert lift2_sat(ISO_ODD_J, True, True)
    assert not lift2_sat((0, 1, 1, 1, 1, 0), True, True)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift2_table()
    sc = lift2_cover()
    k0 = killed_iso_from_011110()
    k1 = killed_iso_unique_window()
    k2 = killed_left_from_011111()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift2_table": {k: rt[k] for k in rt if k != "ok"},
        "lift2_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_iso_from_011110": {k: k0[k] for k in k0 if k != "ok"},
        "killed_iso_unique_window": {k: k1[k] for k in k1 if k != "ok"},
        "killed_left_from_011111": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "LIFT2_sat": True,
            "iso_from_LIFT2_sat": True,
            "covering_kind_lift6": True,
            "iso_from_011110": False,
            "iso_unique_window": False,
            "left_from_011111": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "LIFT2_sat": "LEMMA",
            "iso_from_LIFT2_sat": "LEMMA",
            "covering_kind_lift6": "LEMMA",
            "iso_from_011110": "KILLED",
            "iso_unique_window": "KILLED",
            "left_from_011111": "KILLED",
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
    print("lift2_table", dump["lift2_table"])
    cov = dump["lift2_cover"]
    print(
        "lift2_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_iso",
        cov["n_iso"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_iso_even",
        cov["n_iso_even"],
        "n_iso_odd",
        cov["n_iso_odd"],
    )
    print("killed_iso_from_011110", dump["killed_iso_from_011110"])
    print("killed_iso_unique_window", dump["killed_iso_unique_window"])
    print("killed_left_from_011111", dump["killed_left_from_011111"])


if __name__ == "__main__":
    main()
