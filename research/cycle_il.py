#!/usr/bin/env python3
"""Cycle IL: LIFT4 is unsat on every freshman 6-window shape of G.

Even n forces every other Green bit to 0; odd n interleaves G(m)
with its coboundary. All 16 LIFT4 x (n parity, j parity) cases
contradict those shapes, so G has no lift-4 window for every n.
Even n does have vanishing odd indices; odd n does not; odd-n
even-index is not G(m,k) without the coboundary XOR. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_il.py --certify
Dump: research/cycle_il.json
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
from cycle_ik import LIFT4, g6
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IK_JSON = Path(__file__).resolve().parent / "cycle_ik.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def freshman_shape(n_even: bool, j_even: bool, six) -> bool:
    """Whether a 6-window can occur for this (n,j) parity."""
    if n_even and j_even:
        return six[1] == 0 and six[3] == 0 and six[5] == 0
    if n_even and not j_even:
        return six[0] == 0 and six[2] == 0 and six[4] == 0
    if (not n_even) and j_even:
        return six[2] == (six[3] ^ six[1]) and six[4] == (six[5] ^ six[3])
    return six[1] == (six[2] ^ six[0]) and six[3] == (six[4] ^ six[2])


def lift4_unsat_table() -> dict:
    """16 LIFT4 x parity cases unsat; n<64 windows match freshman_shape."""
    n_unsat = 0
    for six in LIFT4:
        for n_even in (True, False):
            for j_even in (True, False):
                if freshman_shape(n_even, j_even, six):
                    return {
                        "ok": False,
                        "sat": True,
                        "six": list(six),
                        "n_even": n_even,
                        "j_even": j_even,
                    }
                n_unsat += 1
    n_win = 0
    for n in range(0, 64):
        for j in range(-2, 2 * n - 2):
            six = g6(n, j)
            if not freshman_shape(n % 2 == 0, j % 2 == 0, six):
                return {"ok": False, "shape": True, "n": n, "j": j, "six": list(six)}
            if six in LIFT4:
                return {"ok": False, "lift": True, "n": n, "j": j}
            n_win += 1
    ok = n_unsat == 16 and n_win == 4032
    return {"ok": ok, "n_unsat": n_unsat, "n_win": n_win}


def _walk_unsat(k: int, q: int) -> dict:
    """Freshman shapes on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_win = n_g1 = 0
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
                n_even = n % 2 == 0
                for j in range(-2, 2 * n - 2):
                    six = g6(n, j)
                    if not freshman_shape(n_even, j % 2 == 0, six):
                        return {"ok": False, "shape": True, "k": k, "n": n, "j": j}
                    if six in LIFT4:
                        return {"ok": False, "lift": True, "k": k, "n": n, "j": j}
                    n_win += 1
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
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_win": n_win, "n_g1": n_g1, "xor_j": xor_j}


def unsat_cover() -> dict:
    """Freshman LIFT4-unsat on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_win = n_g1 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_unsat(k, q)
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
            n_win += w["n_win"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_win": w["n_win"],
                "n_g1": w["n_g1"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_ok == 95821 and n_g1 == 22659
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_win": n_win,
        "n_g1": n_g1,
        "rows": rows,
    }


def killed_even_odd_index() -> dict:
    """Even n has no odd-index Green 1: G(2,1)=0."""
    k, s, n, j, p = 0, 5, 2, 1, 8
    ok = (
        n % 2 == 0
        and j % 2 == 1
        and G(n, j) == 0
        and G(n, 0) == 1
        and G(n, 2) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def killed_odd_odd_index_zero() -> dict:
    """Odd n does not vanish on odd indices: G(1,1)=1."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    ok = n % 2 == 1 and j % 2 == 1 and G(n, j) == 1 and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def killed_odd_even_no_cob() -> dict:
    """Odd-n even-index is not G(m,k) without coboundary XOR."""
    k, s, n, j, p = 0, 3, 3, 2, 6
    m = n // 2
    no_cob = G(m, j // 2)
    with_cob = G(m, j // 2) ^ G(m, j // 2 - 1)
    ok = (
        n % 2 == 1
        and j % 2 == 0
        and G(n, j) == 0
        and no_cob == 1
        and with_cob == 0
        and G(n, j) == with_cob
        and G(n, j) != no_cob
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
        "no_cob": no_cob,
        "with_cob": with_cob,
    }


def prefixes() -> dict:
    ik = json.loads(IK_JSON.read_text())
    ok = (
        ik["checks"]["all_ok"]
        and ik["verdict"]["G_no_LIFT4_windows"] == "LEMMA"
        and ik["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert not freshman_shape(True, True, (0, 0, 1, 0, 0, 1))
    assert freshman_shape(True, True, (1, 0, 1, 0, 1, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift4_unsat_table()
    sc = unsat_cover()
    k0 = killed_even_odd_index()
    k1 = killed_odd_odd_index_zero()
    k2 = killed_odd_even_no_cob()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift4_unsat_table": {k: rt[k] for k in rt if k != "ok"},
        "unsat_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_odd_index": {k: k0[k] for k in k0 if k != "ok"},
        "killed_odd_odd_index_zero": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_even_no_cob": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "LIFT4_freshman_unsat": True,
            "G_windows_freshman_shape": True,
            "covering_LIFT4_unsat": True,
            "even_n_odd_index_one": False,
            "odd_n_odd_index_zero": False,
            "odd_n_even_no_cob": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "LIFT4_freshman_unsat": "LEMMA",
            "G_windows_freshman_shape": "LEMMA",
            "covering_LIFT4_unsat": "LEMMA",
            "even_n_odd_index_one": "KILLED",
            "odd_n_odd_index_zero": "KILLED",
            "odd_n_even_no_cob": "KILLED",
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
    print("lift4_unsat_table", dump["lift4_unsat_table"])
    cov = dump["unsat_cover"]
    print(
        "unsat_cover n_ok",
        cov["n_ok"],
        "n_win",
        cov["n_win"],
        "n_g1",
        cov["n_g1"],
    )
    print("killed_even_odd_index", dump["killed_even_odd_index"])
    print("killed_odd_odd_index_zero", dump["killed_odd_odd_index_zero"])
    print("killed_odd_even_no_cob", dump["killed_odd_even_no_cob"])


if __name__ == "__main__":
    main()
