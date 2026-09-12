#!/usr/bin/env python3
"""Cycle HR: odd-s Green 6-slot; AND of odd_green4 is G(j+1) and not G(j).

On covering (n,j), odd-s Green at packed bits p-5..p is
odd_green6(n,j)=(0, G(n,j+2), 0, G(n,j+1), 0, G(n,j)), overlapping
odd_green4(n,j+1) and odd_green4(n,j). Dual of Cycle HM green6.
AND(odd_green4) fires iff G(n,j+1)=1 and G(n,j)=0 (only 0100).
The 6-tuple is not odd_green6; odd_green6 is not green6; packed AND
is not that Green formula. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_hr.py --certify
Dump: research/cycle_hr.json
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
from cycle_hl import odd_green4
from cycle_hm import green6
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HQ_JSON = Path(__file__).resolve().parent / "cycle_hq.json"
HL_JSON = Path(__file__).resolve().parent / "cycle_hl.json"
HM_JSON = Path(__file__).resolve().parent / "cycle_hm.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def odd_green6(n: int, j: int) -> tuple[int, int, int, int, int, int]:
    """Odd-s Green at p-5..p on covering (n,j)."""
    return (0, G(n, j + 2), 0, G(n, j + 1), 0, G(n, j))


def odd_green6_identity() -> dict:
    """G(2n, 2j..2j+5) equals odd_green6; overlaps odd_green4. n<64."""
    n_ok = 0
    for n in range(0, 64):
        m = 2 * n
        for j in range(0, 2 * n + 1):
            gm = tuple(G(m, 2 * j + 5 - i) for i in range(6))
            og6 = odd_green6(n, j)
            if gm != og6:
                return {"ok": False, "n": n, "j": j, "gm": gm, "og6": list(og6)}
            if og6[2:] != odd_green4(n, j) or og6[:4] != odd_green4(n, j + 1):
                return {"ok": False, "overlap": True, "n": n, "j": j}
            if og6[0] or og6[2] or og6[4]:
                return {"ok": False, "copy": True, "n": n, "j": j}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def and_og4_table() -> dict:
    """AND(odd_green4) iff G(j+1)=1 and G(j)=0. Four vanishing-copy 4-tuples."""
    n_ok = 0
    for a in (0, 1):
        for c in (0, 1):
            og4 = (0, a, 0, c)
            got = and_from_tuple(*og4)
            want = int(a == 1 and c == 0)
            if got != want:
                return {"ok": False, "og4": og4, "got": got, "want": want}
            n_ok += 1
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            og4 = odd_green4(n, j)
            got = and_from_tuple(*og4)
            want = int(G(n, j + 1) == 1 and G(n, j) == 0)
            if got != want:
                return {"ok": False, "n": n, "j": j, "got": got, "want": want}
            n_ok += 1
    return {"ok": n_ok > 4, "n_ok": n_ok}


def _walk_og6(k: int, q: int) -> dict:
    """Odd-s Green 6-slot on covering (n,j); odd-s XOR on G=1."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = xor_all = 0
    s = t0
    while s < T:
        if s % 2 == 1:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            m = T - s - 1
            if m != 2 * n:
                return {"ok": False, "m": True, "k": k, "s": s, "n": n, "m_got": m}
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                gm = tuple(G(m, 2 * j + 5 - i) for i in range(6))
                og6 = odd_green6(n, j)
                if gm != og6:
                    return {
                        "ok": False,
                        "og6": True,
                        "k": k,
                        "s": s,
                        "n": n,
                        "j": j,
                        "gm": gm,
                        "og6v": list(og6),
                    }
                n_ok += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_all": xor_all}


def og6_cover() -> dict:
    """Odd-s Green 6-slot on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_og6(k, q)
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
            krow[name] = {"n_ok": w["n_ok"], "xor_all": w["xor_all"]}
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "rows": rows}


def killed_six_eq_og6() -> dict:
    """Odd-s 6-tuple is not odd_green6: k=0, s=3, n=1, j=0."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    six = tuple(bit_at(row, p - 5 + i) for i in range(6))
    og6 = odd_green6(n, j)
    ok = six == (1, 0, 1, 1, 1, 1) and og6 == (0, 1, 0, 1, 0, 1) and six != og6
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
        "og6": list(og6),
    }


def killed_og6_eq_g6() -> dict:
    """odd_green6 is not even-s green6: k=0, n=1, j=0."""
    n, j = 1, 0
    og6 = odd_green6(n, j)
    g6 = green6(n, j)
    ok = og6 == (0, 1, 0, 1, 0, 1) and g6 == (1, 0, 1, 0, 1, 1) and og6 != g6
    return {"ok": ok, "n": n, "j": j, "og6": list(og6), "g6": list(g6)}


def killed_and_eq_Gjp1_not_Gj() -> dict:
    """Packed AND is not G(j+1) and not G(j): k=0, s=3, n=1, j=0."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    pred = int(G(n, j + 1) == 1 and G(n, j) == 0)
    ok = four == (0, 1, 0, 0) and packed == 1 and pred == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
        "pred": pred,
        "G": [G(n, j), G(n, j + 1)],
    }


def prefixes() -> dict:
    hq = json.loads(HQ_JSON.read_text())
    hl = json.loads(HL_JSON.read_text())
    hm = json.loads(HM_JSON.read_text())
    ok = (
        hq["checks"]["all_ok"]
        and hl["checks"]["all_ok"]
        and hm["checks"]["all_ok"]
        and hq["verdict"]["FRESH_eq_even_factors_of_001w"] == "LEMMA"
        and hl["verdict"]["odd_s_Green_4slot_eq_odd_green4"] == "LEMMA"
        and hm["verdict"]["even_s_Green_6slot_eq_green6"] == "LEMMA"
        and hq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, oid: dict, at: dict, oc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        oid["ok"]
        and at["ok"]
        and oc["ok"]
        and k0["ok"]
        and k1["ok"]
        and k2["ok"]
        and pref["ok"]
    )
    assert odd_green6(1, 0)[2:] == odd_green4(1, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    oid = odd_green6_identity()
    at = and_og4_table()
    oc = og6_cover()
    k0 = killed_six_eq_og6()
    k1 = killed_og6_eq_g6()
    k2 = killed_and_eq_Gjp1_not_Gj()
    pref = prefixes()
    checks = self_checks(c20, oid, at, oc, k0, k1, k2, pref)
    dump = {
        "cycle": "HR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "odd_green6_identity": {k: oid[k] for k in oid if k != "ok"},
        "and_og4_table": {k: at[k] for k in at if k != "ok"},
        "og6_cover": {k: oc[k] for k in oc if k != "ok"},
        "killed_six_eq_og6": {k: k0[k] for k in k0 if k != "ok"},
        "killed_og6_eq_g6": {k: k1[k] for k in k1 if k != "ok"},
        "killed_and_eq_Gjp1_not_Gj": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "odd_s_Green_6slot_eq_odd_green6": True,
            "odd_green6_overlaps_odd_green4": True,
            "AND_of_odd_green4_iff_Gjp1_and_not_Gj": True,
            "6tuple_eq_odd_green6": False,
            "odd_green6_eq_green6": False,
            "AND_eq_Gjp1_and_not_Gj": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_Green_6slot_eq_odd_green6": "LEMMA",
            "odd_green6_overlaps_odd_green4": "LEMMA",
            "AND_of_odd_green4_iff_Gjp1_and_not_Gj": "LEMMA",
            "6tuple_eq_odd_green6": "KILLED",
            "odd_green6_eq_green6": "KILLED",
            "AND_eq_Gjp1_and_not_Gj": "KILLED",
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
    print("odd_green6_identity n_ok", dump["odd_green6_identity"]["n_ok"])
    print("and_og4_table n_ok", dump["and_og4_table"]["n_ok"])
    print("og6_cover n_ok", dump["og6_cover"]["n_ok"])
    print("killed_six_eq_og6", dump["killed_six_eq_og6"])
    print("killed_og6_eq_g6", dump["killed_og6_eq_g6"])
    print("killed_and_eq_Gjp1_not_Gj", dump["killed_and_eq_Gjp1_not_Gj"])


if __name__ == "__main__":
    main()
