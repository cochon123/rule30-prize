#!/usr/bin/env python3
"""Cycle HQ: fresh AND is even factors of (001)^w; CONT is the terminator.

FRESH 4-tuples are the even-offset 4-factors of (001)^w (bit i is 1
iff i%3==2). Period-3 BOTH_AND {001001,010010,100100} are the
6-factors; the unique non-period-3 BOTH_AND is CONT terminator
010011. Triple/quad minus the unique ...11 terminator are the 8/10
factors. Period-3 AND is not absent; not all consecutive AND is
period-3; not only on G=1. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_hq.py --certify
Dump: research/cycle_hq.json
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
from cycle_hh import and_from_tuple, bit_at
from cycle_hi import CONT, FRESH
from cycle_hn import BOTH_AND
from cycle_ho import TRIPLE_AND
from cycle_hp import QUAD_AND
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HP_JSON = Path(__file__).resolve().parent / "cycle_hp.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

CONT_TERM = (0, 1, 0, 0, 1, 1)
TRIPLE_TERM = (1, 0, 0, 1, 0, 0, 1, 1)
QUAD_TERM = (0, 0, 1, 0, 0, 1, 0, 0, 1, 1)


def per3_word(length: int, off: int) -> tuple:
    """Even-offset factor of (001)^w: bit i is 1 iff (i+off)%3==2."""
    return tuple(int((i + off) % 3 == 2) for i in range(length))


def per3_factors(length: int) -> set:
    return {per3_word(length, off) for off in (0, 2, 4)}


def per3_table() -> dict:
    """FRESH/BOTH/TRIPLE/QUAD minus the CONT terminator are period-3 factors."""
    if set(FRESH) != per3_factors(4):
        return {"ok": False, "fresh": True}
    if CONT in per3_factors(4) or CONT_TERM[2:] != CONT:
        return {"ok": False, "cont": True}
    if set(BOTH_AND) - {CONT_TERM} != per3_factors(6):
        return {"ok": False, "both": True}
    if CONT_TERM not in BOTH_AND:
        return {"ok": False, "term": True}
    if set(TRIPLE_AND) - {TRIPLE_TERM} != per3_factors(8):
        return {"ok": False, "triple": True}
    if set(QUAD_AND) - {QUAD_TERM} != per3_factors(10):
        return {"ok": False, "quad": True}
    return {
        "ok": True,
        "n_fresh": len(FRESH),
        "n_per3_both": 3,
        "n_term": 1,
    }


def _walk_per3(k: int, q: int) -> dict:
    """Period-3 vs CONT-terminator both-AND on covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_per3 = n_term = xor_all = 0
    per3_6 = per3_factors(6)
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
                both = and_from_tuple(*six[0:4]) and and_from_tuple(*six[2:6])
                if both != (six in BOTH_AND):
                    return {"ok": False, "both": True, "k": k, "six": six}
                if both and (six in per3_6) == (six == CONT_TERM):
                    return {"ok": False, "split": True, "k": k, "six": six}
                n_ok += 1
                if six in per3_6:
                    n_per3 += 1
                elif six == CONT_TERM:
                    n_term += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_per3": n_per3,
        "n_term": n_term,
        "xor_all": xor_all,
    }


def per3_cover() -> dict:
    """Period-3 / terminator on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_per3 = n_term = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_per3(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_all"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_all"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_all"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_per3 += w["n_per3"]
            n_term += w["n_term"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_per3": w["n_per3"],
                "n_term": w["n_term"],
                "xor_all": w["xor_all"],
            }
        rows[str(k)] = krow
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_per3": n_per3,
        "n_term": n_term,
        "rows": rows,
    }


def killed_no_per3() -> dict:
    """Period-3 AND is not absent: k=0, s=3, six=100100."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    ok = six == (1, 0, 0, 1, 0, 0) and six in per3_factors(6)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "six": list(six)}


def killed_all_and_is_per3() -> dict:
    """Not all consecutive AND is period-3: k=1, s=19, six=010011."""
    k, s, n, j, p = 1, 19, 0, 0, 20
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    ok = six == CONT_TERM and six not in per3_factors(6)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "six": list(six)}


def killed_per3_only_g1() -> dict:
    """Period-3 AND is not only on G=1: k=0, s=3, n=3, j=2, G=0."""
    k, s, n, j, p = 0, 3, 3, 2, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    ok = six in per3_factors(6) and G(n, j) == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
        "G": G(n, j),
    }


def prefixes() -> dict:
    hp = json.loads(HP_JSON.read_text())
    ok = (
        hp["checks"]["all_ok"]
        and hp["verdict"]["quad_AND_iff_4_ten_tuples"] == "LEMMA"
        and hp["verdict"]["quad_AND_eq_TRIPLE_AND_overlap"] == "LEMMA"
        and hp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, pt: dict, pc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pt["ok"] and pc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert (1, 0, 0, 1, 0, 0) in per3_factors(6)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pt = per3_table()
    pc = per3_cover()
    k0 = killed_no_per3()
    k1 = killed_all_and_is_per3()
    k2 = killed_per3_only_g1()
    pref = prefixes()
    checks = self_checks(c20, pt, pc, k0, k1, k2, pref)
    dump = {
        "cycle": "HQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "per3_table": {k: pt[k] for k in pt if k != "ok"},
        "per3_cover": {k: pc[k] for k in pc if k != "ok"},
        "killed_no_per3": {k: k0[k] for k in k0 if k != "ok"},
        "killed_all_and_is_per3": {k: k1[k] for k in k1 if k != "ok"},
        "killed_per3_only_g1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "FRESH_eq_even_factors_of_001w": True,
            "period3_BOTH_AND_eq_6_factors": True,
            "CONT_TERM_unique_non_period3_BOTH_AND": True,
            "no_covering_period3_AND": False,
            "all_consecutive_AND_is_period3": False,
            "period3_AND_only_on_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "FRESH_eq_even_factors_of_001w": "LEMMA",
            "period3_BOTH_AND_eq_6_factors": "LEMMA",
            "CONT_TERM_unique_non_period3_BOTH_AND": "LEMMA",
            "no_covering_period3_AND": "KILLED",
            "all_consecutive_AND_is_period3": "KILLED",
            "period3_AND_only_on_G_eq_1": "KILLED",
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
    print("per3_table", dump["per3_table"])
    print(
        "per3_cover n_ok",
        dump["per3_cover"]["n_ok"],
        "n_per3",
        dump["per3_cover"]["n_per3"],
        "n_term",
        dump["per3_cover"]["n_term"],
    )
    print("killed_no_per3", dump["killed_no_per3"])
    print("killed_all_and_is_per3", dump["killed_all_and_is_per3"])
    print("killed_per3_only_g1", dump["killed_per3_only_g1"])


if __name__ == "__main__":
    main()
