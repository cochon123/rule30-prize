#!/usr/bin/env python3
"""Cycle HV: covering J is the G=1 FRESH XOR CONT slice.

Odd-s covering J XORs and_clause only on Green ones. That slice is
FRESH plus CONT on G=1, not all AND and not all FRESH. G=1 AND does
not force packed copy(j). Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_hv.py --certify
Dump: research/cycle_hv.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hi import CONT, FRESH
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HU_JSON = Path(__file__).resolve().parent / "cycle_hu.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _walk_g1(k: int, q: int) -> dict:
    """G=1 FRESH/CONT slice vs all-AND / all-FRESH XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_and = n_and_g1 = 0
    n_fresh_g1 = n_cont_g1 = n_cob_g1 = n_noncob0_g1 = 0
    xor_j = xor_all = xor_f = xor_fg = xor_cg = 0
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
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                cl = and_clause(*four)
                if packed != cl:
                    return {"ok": False, "pack": True, "k": k, "four": four}
                if packed != int(four in AND_ONES):
                    return {"ok": False, "ones": True, "k": k, "four": four}
                n_ok += 1
                gj = G(n, j)
                if packed:
                    n_and += 1
                    xor_all ^= 1
                if four in FRESH:
                    xor_f ^= 1
                if gj:
                    n_g1 += 1
                    if cob_shaped(*four):
                        n_cob_g1 += 1
                        if packed:
                            return {"ok": False, "cob_and": True, "k": k, "four": four}
                    elif four in FRESH:
                        n_fresh_g1 += 1
                        xor_fg ^= 1
                    elif four == CONT:
                        n_cont_g1 += 1
                        xor_cg ^= 1
                    else:
                        n_noncob0_g1 += 1
                        if packed:
                            return {"ok": False, "noncob0_and": True, "k": k, "four": four}
                    if packed:
                        n_and_g1 += 1
                        xor_j ^= 1
        row = rule30_step(row)
        s += 1
    ok = (
        n_ok > 0
        and xor_j == (xor_fg ^ xor_cg)
        and n_and_g1 == n_fresh_g1 + n_cont_g1
        and n_g1 == n_cob_g1 + n_fresh_g1 + n_cont_g1 + n_noncob0_g1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_and": n_and,
        "n_and_g1": n_and_g1,
        "n_fresh_g1": n_fresh_g1,
        "n_cont_g1": n_cont_g1,
        "n_cob_g1": n_cob_g1,
        "n_noncob0_g1": n_noncob0_g1,
        "xor_j": xor_j,
        "xor_all": xor_all,
        "xor_f": xor_f,
        "xor_fg": xor_fg,
        "xor_cg": xor_cg,
    }


def g1_slice_cover() -> dict:
    """J = G=1 FRESH XOR CONT on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_and = n_and_g1 = 0
    n_fresh_g1 = n_cont_g1 = n_cob_g1 = n_noncob0_g1 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    n_j_ne_all = n_j_ne_f = 0
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g1(k, q)
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
            if w["xor_j"] != w["xor_all"]:
                n_j_ne_all += 1
            if w["xor_j"] != w["xor_f"]:
                n_j_ne_f += 1
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_and += w["n_and"]
            n_and_g1 += w["n_and_g1"]
            n_fresh_g1 += w["n_fresh_g1"]
            n_cont_g1 += w["n_cont_g1"]
            n_cob_g1 += w["n_cob_g1"]
            n_noncob0_g1 += w["n_noncob0_g1"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_and_g1": w["n_and_g1"],
                "n_fresh_g1": w["n_fresh_g1"],
                "n_cont_g1": w["n_cont_g1"],
                "xor_j": w["xor_j"],
                "xor_all": w["xor_all"],
                "xor_f": w["xor_f"],
            }
        rows[str(k)] = krow
    ok = (
        n_and_g1 == n_fresh_g1 + n_cont_g1
        and n_j_ne_all > 0
        and n_j_ne_f > 0
        and n_g1 == 22659
        and n_and_g1 == 4522
        and n_fresh_g1 == 3376
        and n_cont_g1 == 1146
        and n_cob_g1 == 13628
        and n_noncob0_g1 == 4509
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_and": n_and,
        "n_and_g1": n_and_g1,
        "n_fresh_g1": n_fresh_g1,
        "n_cont_g1": n_cont_g1,
        "n_cob_g1": n_cob_g1,
        "n_noncob0_g1": n_noncob0_g1,
        "n_j_ne_all": n_j_ne_all,
        "n_j_ne_f": n_j_ne_f,
        "rows": rows,
    }


def killed_g1_and_implies_copy_j() -> dict:
    """G=1 AND does not force packed copy(j): k=0, s=3, four=0100."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    g4 = green4(n, j)
    ok = (
        four == (0, 1, 0, 0)
        and four in FRESH
        and packed == 1
        and G(n, j) == 1
        and four[2] == 0
        and g4[2] == 1
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
        "G": G(n, j),
        "g4": list(g4),
    }


def killed_j_eq_xor_all_and() -> dict:
    """Covering J is not XOR of all AND: k=1, q=6, four=1001 on G=0."""
    k, s, n, j, p = 1, 5, 3, 4, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    w = _walk_g1(1, 6)
    ok = (
        four == (1, 0, 0, 1)
        and four in FRESH
        and packed == 1
        and G(n, j) == 0
        and w.get("ok")
        and w["xor_j"] != w["xor_all"]
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
        "G": G(n, j),
        "xor_j": w.get("xor_j"),
        "xor_all": w.get("xor_all"),
    }


def killed_j_eq_xor_all_fresh() -> dict:
    """Covering J is not XOR of all FRESH: k=1, q=6."""
    w = _walk_g1(1, 6)
    ok = w.get("ok") and w["xor_j"] != w["xor_f"]
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_j": w.get("xor_j"),
        "xor_f": w.get("xor_f"),
        "xor_all": w.get("xor_all"),
    }


def prefixes() -> dict:
    hu = json.loads(HU_JSON.read_text())
    ok = (
        hu["checks"]["all_ok"]
        and hu["verdict"]["AND_iff_noncob_and_a_xor_bORc"] == "LEMMA"
        and hu["verdict"]["AND_only_on_G1"] == "KILLED"
        and hu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gs: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gs["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert and_clause(0, 1, 0, 0) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gs = g1_slice_cover()
    k0 = killed_g1_and_implies_copy_j()
    k1 = killed_j_eq_xor_all_and()
    k2 = killed_j_eq_xor_all_fresh()
    pref = prefixes()
    checks = self_checks(c20, gs, k0, k1, k2, pref)
    dump = {
        "cycle": "HV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g1_slice_cover": {k: gs[k] for k in gs if k != "ok"},
        "killed_g1_and_implies_copy_j": {k: k0[k] for k in k0 if k != "ok"},
        "killed_j_eq_xor_all_and": {k: k1[k] for k in k1 if k != "ok"},
        "killed_j_eq_xor_all_fresh": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "covering_J_eq_G1_FRESH_XOR_CONT": True,
            "G1_AND_eq_FRESH_or_CONT": True,
            "G1_AND_implies_packed_copy_j": False,
            "J_eq_XOR_all_AND": False,
            "J_eq_XOR_all_FRESH": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "covering_J_eq_G1_FRESH_XOR_CONT": "LEMMA",
            "G1_AND_eq_FRESH_or_CONT": "LEMMA",
            "G1_AND_implies_packed_copy_j": "KILLED",
            "J_eq_XOR_all_AND": "KILLED",
            "J_eq_XOR_all_FRESH": "KILLED",
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
    cov = dump["g1_slice_cover"]
    print(
        "g1_slice n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_and_g1",
        cov["n_and_g1"],
        "n_fresh_g1",
        cov["n_fresh_g1"],
        "n_cont_g1",
        cov["n_cont_g1"],
        "n_cob_g1",
        cov["n_cob_g1"],
        "n_noncob0_g1",
        cov["n_noncob0_g1"],
    )
    print("killed_g1_and_implies_copy_j", dump["killed_g1_and_implies_copy_j"])
    print("killed_j_eq_xor_all_and", dump["killed_j_eq_xor_all_and"])
    print("killed_j_eq_xor_all_fresh", dump["killed_j_eq_xor_all_fresh"])


if __name__ == "__main__":
    main()
