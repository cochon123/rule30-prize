#!/usr/bin/env python3
"""Cycle HL: odd-s Green 4-slot is (0, G(n,j+1), 0, G(n,j)).

On covering (n,j), odd-s Green at packed bits p-3..p is
odd_green4(n,j)=(0, G(n,j+1), 0, G(n,j)): copy slots vanish and
cob slots copy G(n,j+1) and G(n,j). Dual of Cycle HJ green4.
The odd-s 4-tuple is not that Green 4-tuple; odd_green4 is not
even-s green4; odd-s Green does not vanish on coboundary slots.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_hl.py --certify
Dump: research/cycle_hl.json
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
from cycle_hj import green4
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HK_JSON = Path(__file__).resolve().parent / "cycle_hk.json"
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def odd_green4(n: int, j: int) -> tuple[int, int, int, int]:
    """Odd-s Green at p-3..p on covering (n,j)."""
    return (0, G(n, j + 1), 0, G(n, j))


def odd_green4_identity() -> dict:
    """G(2n, 2j..2j+3) equals odd_green4(n,j). n<64."""
    n_ok = 0
    for n in range(0, 64):
        m = 2 * n
        for j in range(0, 2 * n + 1):
            gm = (
                G(m, 2 * j + 3),
                G(m, 2 * j + 2),
                G(m, 2 * j + 1),
                G(m, 2 * j),
            )
            og4 = odd_green4(n, j)
            if gm != og4:
                return {"ok": False, "n": n, "j": j, "gm": gm, "og4": list(og4)}
            if og4[0] != 0 or og4[2] != 0:
                return {"ok": False, "copy": True, "n": n, "j": j, "og4": list(og4)}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def _walk_og4(k: int, q: int) -> dict:
    """Odd-s Green 4-slot on covering (n,j); odd-s XOR on G=1."""
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
                gm = (
                    G(m, 2 * j + 3),
                    G(m, 2 * j + 2),
                    G(m, 2 * j + 1),
                    G(m, 2 * j),
                )
                og4 = odd_green4(n, j)
                if gm != og4:
                    return {
                        "ok": False,
                        "og4": True,
                        "k": k,
                        "s": s,
                        "n": n,
                        "j": j,
                        "gm": gm,
                        "og4v": list(og4),
                    }
                n_ok += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_all": xor_all}


def og4_cover() -> dict:
    """Odd-s Green 4-slot on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_og4(k, q)
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


def killed_tup_eq_og4() -> dict:
    """Odd-s 4-tuple is not odd_green4: k=0, s=3, n=1, j=0."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    tup = (
        bit_at(row, p - 3),
        bit_at(row, p - 2),
        bit_at(row, p - 1),
        bit_at(row, p),
    )
    og4 = odd_green4(n, j)
    ok = tup == (1, 1, 1, 1) and og4 == (0, 1, 0, 1) and tup != og4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "og4": list(og4),
    }


def killed_og4_eq_green4() -> dict:
    """odd_green4 is not even-s green4: k=0, n=1, j=0."""
    n, j = 1, 0
    og4 = odd_green4(n, j)
    g4 = green4(n, j)
    ok = og4 == (0, 1, 0, 1) and g4 == (1, 0, 1, 1) and og4 != g4
    return {"ok": ok, "n": n, "j": j, "og4": list(og4), "g4": list(g4)}


def killed_odd_s_green_vanishes_cob() -> dict:
    """Odd-s Green does not vanish on coboundary slots: k=0, n=1, j=0."""
    n, j = 1, 0
    og4 = odd_green4(n, j)
    ok = og4[0] == 0 and og4[2] == 0 and og4[1] == 1 and og4[3] == 1
    return {"ok": ok, "n": n, "j": j, "og4": list(og4)}


def prefixes() -> dict:
    hk = json.loads(HK_JSON.read_text())
    hj = json.loads(HJ_JSON.read_text())
    ok = (
        hk["checks"]["all_ok"]
        and hj["checks"]["all_ok"]
        and hk["verdict"]["die_iff_0111_or_1011_or_1111"] == "LEMMA"
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, oid: dict, oc: dict, kt: dict, kg: dict, kc: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert oid["ok"] and oc["ok"] and kt["ok"] and kg["ok"] and kc["ok"] and pref["ok"]
    assert odd_green4(0, 0) == (0, 0, 0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    oid = odd_green4_identity()
    oc = og4_cover()
    kt = killed_tup_eq_og4()
    kg = killed_og4_eq_green4()
    kc = killed_odd_s_green_vanishes_cob()
    pref = prefixes()
    checks = self_checks(c20, oid, oc, kt, kg, kc, pref)
    dump = {
        "cycle": "HL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "odd_green4_identity": {k: oid[k] for k in oid if k != "ok"},
        "og4_cover": {k: oc[k] for k in oc if k != "ok"},
        "killed_tup_eq_og4": {k: kt[k] for k in kt if k != "ok"},
        "killed_og4_eq_green4": {k: kg[k] for k in kg if k != "ok"},
        "killed_odd_s_green_vanishes_cob": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "odd_s_Green_4slot_eq_odd_green4": True,
            "odd_s_copy_slots_vanish": True,
            "odd_s_4tuple_eq_odd_green4": False,
            "odd_green4_eq_even_s_green4": False,
            "odd_s_Green_vanishes_on_cob_slots": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_Green_4slot_eq_odd_green4": "LEMMA",
            "odd_s_copy_slots_vanish": "LEMMA",
            "odd_s_4tuple_eq_odd_green4": "KILLED",
            "odd_green4_eq_even_s_green4": "KILLED",
            "odd_s_Green_vanishes_on_cob_slots": "KILLED",
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
    print("odd_green4_identity n_ok", dump["odd_green4_identity"]["n_ok"])
    print("og4_cover n_ok", dump["og4_cover"]["n_ok"])
    print("killed_tup_eq_og4", dump["killed_tup_eq_og4"])
    print("killed_og4_eq_green4", dump["killed_og4_eq_green4"])
    print("killed_odd_s_green_vanishes_cob", dump["killed_odd_s_green_vanishes_cob"])


if __name__ == "__main__":
    main()
