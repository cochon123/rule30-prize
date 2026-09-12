#!/usr/bin/env python3
"""Cycle HO: triple-AND 8-tuples are the BOTH_AND overlap chains.

Three consecutive odd-s AND iff the even-s 8-tuple is one of
00100100, 01001001, 10010010, 10010011. Those are the overlapping
pairs of Cycle HN's four both-AND 6-tuples. Triple-AND is not
absent; not only 10010011; not only when all three G=1. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ho.py --certify
Dump: research/cycle_ho.json
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
from cycle_hn import BOTH_AND
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HN_JSON = Path(__file__).resolve().parent / "cycle_hn.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

TRIPLE_AND = (
    (0, 0, 1, 0, 0, 1, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 1, 1),
)


def triple_and_table() -> dict:
    """256-row: triple AND iff 8-tuple in TRIPLE_AND; overlap of BOTH_AND."""
    got = []
    n_ok = 0
    for bits in range(256):
        eight = tuple((bits >> i) & 1 for i in range(7, -1, -1))
        trip = (
            and_from_tuple(*eight[0:4])
            and and_from_tuple(*eight[2:6])
            and and_from_tuple(*eight[4:8])
        )
        if trip:
            got.append(eight)
            if eight[:6] not in BOTH_AND or eight[2:] not in BOTH_AND:
                return {"ok": False, "overlap": True, "eight": eight}
        n_ok += 1
    ok = tuple(got) == TRIPLE_AND and n_ok == 256
    return {"ok": ok, "n_ok": n_ok, "n_trip": len(got)}


def _walk_trip(k: int, q: int) -> dict:
    """Triple-AND 8-tuples on covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_trip = xor_all = 0
    fire = {t: 0 for t in TRIPLE_AND}
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
                eight = tuple(bit_at(prev, p - 7 + i) for i in range(8))
                trip = (
                    and_from_tuple(*eight[0:4])
                    and and_from_tuple(*eight[2:6])
                    and and_from_tuple(*eight[4:8])
                )
                if trip != (eight in TRIPLE_AND):
                    return {"ok": False, "trip": True, "k": k, "eight": eight}
                n_ok += 1
                if trip:
                    n_trip += 1
                    fire[eight] += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_trip": n_trip,
        "xor_all": xor_all,
        "fire": {str(t): fire[t] for t in TRIPLE_AND},
    }


def trip_cover() -> dict:
    """Triple-AND on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_trip = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_trip(k, q)
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
            n_trip += w["n_trip"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_trip": w["n_trip"],
                "xor_all": w["xor_all"],
                "fire": w["fire"],
            }
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "n_trip": n_trip, "rows": rows}


def killed_no_triple() -> dict:
    """Triple-AND is not absent: k=2, s=19, eight=10010011."""
    k, s, n, j, p = 2, 19, 2, 2, 20
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    eight = tuple(bit_at(prev, p - 7 + i) for i in range(8))
    trip = (
        and_from_tuple(*eight[0:4])
        and and_from_tuple(*eight[2:6])
        and and_from_tuple(*eight[4:8])
    )
    ok = eight == (1, 0, 0, 1, 0, 0, 1, 1) and trip
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "eight": list(eight)}


def killed_triple_only_10010011() -> dict:
    """Triple-AND is not only 10010011: k=4, s=37, eight=00100100."""
    k, s, n, j, p = 4, 37, 29, 25, 46
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    eight = tuple(bit_at(prev, p - 7 + i) for i in range(8))
    trip = (
        and_from_tuple(*eight[0:4])
        and and_from_tuple(*eight[2:6])
        and and_from_tuple(*eight[4:8])
    )
    ok = eight == (0, 0, 1, 0, 0, 1, 0, 0) and trip
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "eight": list(eight)}


def killed_triple_only_all_g1() -> dict:
    """Triple-AND is not only when all three G=1: k=2, s=19, G=(1,0,1)."""
    k, s, n, j = 2, 19, 2, 2
    gs = (G(n, j), G(n, j + 1), G(n, j + 2))
    w = killed_no_triple()
    ok = w["ok"] and gs == (1, 0, 1)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "G": list(gs)}


def prefixes() -> dict:
    hn = json.loads(HN_JSON.read_text())
    ok = (
        hn["checks"]["all_ok"]
        and hn["verdict"]["both_AND_iff_4_six_tuples"] == "LEMMA"
        and hn["verdict"]["odd_AND_forbids_even_AND_at_p_minus_2"] == "LEMMA"
        and hn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, tt: dict, tc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert tt["ok"] and tc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert (1, 0, 0, 1, 0, 0, 1, 1) in TRIPLE_AND
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    tt = triple_and_table()
    tc = trip_cover()
    k0 = killed_no_triple()
    k1 = killed_triple_only_10010011()
    k2 = killed_triple_only_all_g1()
    pref = prefixes()
    checks = self_checks(c20, tt, tc, k0, k1, k2, pref)
    dump = {
        "cycle": "HO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "triple_and_table": {k: tt[k] for k in tt if k != "ok"},
        "trip_cover": {k: tc[k] for k in tc if k != "ok"},
        "killed_no_triple": {k: k0[k] for k in k0 if k != "ok"},
        "killed_triple_only_10010011": {k: k1[k] for k in k1 if k != "ok"},
        "killed_triple_only_all_g1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "triple_AND_iff_4_eight_tuples": True,
            "triple_AND_eq_BOTH_AND_overlap": True,
            "no_covering_triple_AND": False,
            "triple_AND_only_10010011": False,
            "triple_AND_only_when_all_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "triple_AND_iff_4_eight_tuples": "LEMMA",
            "triple_AND_eq_BOTH_AND_overlap": "LEMMA",
            "no_covering_triple_AND": "KILLED",
            "triple_AND_only_10010011": "KILLED",
            "triple_AND_only_when_all_G_eq_1": "KILLED",
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
    print("triple_and_table n_trip", dump["triple_and_table"]["n_trip"])
    print("trip_cover n_ok", dump["trip_cover"]["n_ok"], "n_trip", dump["trip_cover"]["n_trip"])
    print("killed_no_triple", dump["killed_no_triple"])
    print("killed_triple_only_10010011", dump["killed_triple_only_10010011"])
    print("killed_triple_only_all_g1", dump["killed_triple_only_all_g1"])


if __name__ == "__main__":
    main()
