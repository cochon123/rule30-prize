#!/usr/bin/env python3
"""Cycle HP: quadruple-AND 10-tuples are the TRIPLE_AND overlap chains.

Four consecutive odd-s AND iff the even-s 10-tuple is one of
0010010010, 0010010011, 0100100100, 1001001001. Those are the
overlapping pairs of Cycle HO's four triple-AND 8-tuples.
Quad-AND is not absent; not only 0010010010; not only when all
four G=1. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_hp.py --certify
Dump: research/cycle_hp.json
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
from cycle_ho import TRIPLE_AND
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HO_JSON = Path(__file__).resolve().parent / "cycle_ho.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

QUAD_AND = (
    (0, 0, 1, 0, 0, 1, 0, 0, 1, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 1, 1),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 0),
    (1, 0, 0, 1, 0, 0, 1, 0, 0, 1),
)


def _quad_from(ten: tuple) -> bool:
    return (
        and_from_tuple(*ten[0:4])
        and and_from_tuple(*ten[2:6])
        and and_from_tuple(*ten[4:8])
        and and_from_tuple(*ten[6:10])
    )


def quad_and_table() -> dict:
    """1024-row: quad AND iff 10-tuple in QUAD_AND; overlap of TRIPLE_AND."""
    got = []
    n_ok = 0
    for bits in range(1024):
        ten = tuple((bits >> i) & 1 for i in range(9, -1, -1))
        if _quad_from(ten):
            got.append(ten)
            if ten[:8] not in TRIPLE_AND or ten[2:] not in TRIPLE_AND:
                return {"ok": False, "overlap": True, "ten": ten}
        n_ok += 1
    ok = tuple(got) == QUAD_AND and n_ok == 1024
    return {"ok": ok, "n_ok": n_ok, "n_quad": len(got)}


def _walk_quad(k: int, q: int) -> dict:
    """Quad-AND 10-tuples on covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_quad = xor_all = 0
    fire = {t: 0 for t in QUAD_AND}
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
                ten = tuple(bit_at(prev, p - 9 + i) for i in range(10))
                quad = _quad_from(ten)
                if quad != (ten in QUAD_AND):
                    return {"ok": False, "quad": True, "k": k, "ten": ten}
                n_ok += 1
                if quad:
                    n_quad += 1
                    fire[ten] += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_quad": n_quad,
        "xor_all": xor_all,
        "fire": {str(t): fire[t] for t in QUAD_AND},
    }


def quad_cover() -> dict:
    """Quad-AND on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_quad = 0
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
            n_quad += w["n_quad"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_quad": w["n_quad"],
                "xor_all": w["xor_all"],
                "fire": w["fire"],
            }
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "n_quad": n_quad, "rows": rows}


def killed_no_quad() -> dict:
    """Quad-AND is not absent: k=3, s=45, ten=0010010010."""
    k, s, n, j, p = 3, 45, 1, 2, 44
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    ten = tuple(bit_at(prev, p - 9 + i) for i in range(10))
    ok = ten == (0, 0, 1, 0, 0, 1, 0, 0, 1, 0) and _quad_from(ten)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "ten": list(ten)}


def killed_quad_only_0010010010() -> dict:
    """Quad-AND is not only 0010010010: k=3, s=31, ten=0100100100."""
    k, s, n, j, p = 3, 31, 24, 9, 62
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    ten = tuple(bit_at(prev, p - 9 + i) for i in range(10))
    ok = ten == (0, 1, 0, 0, 1, 0, 0, 1, 0, 0) and _quad_from(ten)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "ten": list(ten)}


def killed_quad_only_all_g1() -> dict:
    """Quad-AND is not only when all four G=1: k=3, s=45, G=(1,0,0,0)."""
    k, s, n, j = 3, 45, 1, 2
    gs = (G(n, j), G(n, j + 1), G(n, j + 2), G(n, j + 3))
    w = killed_no_quad()
    ok = w["ok"] and gs == (1, 0, 0, 0)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "G": list(gs)}


def prefixes() -> dict:
    ho = json.loads(HO_JSON.read_text())
    ok = (
        ho["checks"]["all_ok"]
        and ho["verdict"]["triple_AND_iff_4_eight_tuples"] == "LEMMA"
        and ho["verdict"]["triple_AND_eq_BOTH_AND_overlap"] == "LEMMA"
        and ho["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, qt: dict, qc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert qt["ok"] and qc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert (0, 0, 1, 0, 0, 1, 0, 0, 1, 0) in QUAD_AND
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    qt = quad_and_table()
    qc = quad_cover()
    k0 = killed_no_quad()
    k1 = killed_quad_only_0010010010()
    k2 = killed_quad_only_all_g1()
    pref = prefixes()
    checks = self_checks(c20, qt, qc, k0, k1, k2, pref)
    dump = {
        "cycle": "HP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "quad_and_table": {k: qt[k] for k in qt if k != "ok"},
        "quad_cover": {k: qc[k] for k in qc if k != "ok"},
        "killed_no_quad": {k: k0[k] for k in k0 if k != "ok"},
        "killed_quad_only_0010010010": {k: k1[k] for k in k1 if k != "ok"},
        "killed_quad_only_all_g1": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "quad_AND_iff_4_ten_tuples": True,
            "quad_AND_eq_TRIPLE_AND_overlap": True,
            "no_covering_quad_AND": False,
            "quad_AND_only_0010010010": False,
            "quad_AND_only_when_all_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "quad_AND_iff_4_ten_tuples": "LEMMA",
            "quad_AND_eq_TRIPLE_AND_overlap": "LEMMA",
            "no_covering_quad_AND": "KILLED",
            "quad_AND_only_0010010010": "KILLED",
            "quad_AND_only_when_all_G_eq_1": "KILLED",
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
    print("quad_and_table n_quad", dump["quad_and_table"]["n_quad"])
    print("quad_cover n_ok", dump["quad_cover"]["n_ok"], "n_quad", dump["quad_cover"]["n_quad"])
    print("killed_no_quad", dump["killed_no_quad"])
    print("killed_quad_only_0010010010", dump["killed_quad_only_0010010010"])
    print("killed_quad_only_all_g1", dump["killed_quad_only_all_g1"])


if __name__ == "__main__":
    main()
