#!/usr/bin/env python3
"""Cycle HS: even-s Green never fires odd-s AND; even Green 11 iff G(j) and not G(j-1).

and_from_tuple(*green4) is identically 0: even-s Green is never in
AND_ONES. Same-row 11 on green4 (DIE 0111/1011) iff G(n,j)=1 and
G(n,j-1)=0. Dual of Cycle HR's AND(odd_green4). Packed odd-s AND is
not identically 0; packed even-s AND is not that Green formula;
green4 is not DIE-free. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_hs.py --certify
Dump: research/cycle_hs.json
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
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_hj import green4
from cycle_hk import DIE
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HR_JSON = Path(__file__).resolve().parent / "cycle_hr.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

GREEN_DIE = ((0, 1, 1, 1), (1, 0, 1, 1))


def green4_and_table() -> dict:
    """8-row: AND(green4)=0; even-11 iff G(j) and not G(j-1) iff DIE 0111/1011."""
    n_ok = 0
    n_die = 0
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                g4 = (a, a ^ b, b, b ^ c)
                if and_from_tuple(*g4) or g4 in AND_ONES:
                    return {"ok": False, "and": True, "g4": g4}
                even11 = int(g4[2] == 1 and g4[3] == 1)
                want = int(b == 1 and c == 0)
                if even11 != want:
                    return {"ok": False, "even11": True, "g4": g4}
                in_die = g4 in DIE
                if even11 != int(in_die) or (in_die and g4 not in GREEN_DIE):
                    return {"ok": False, "die": True, "g4": g4}
                if in_die:
                    n_die += 1
                n_ok += 1
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            g4 = green4(n, j)
            if and_from_tuple(*g4):
                return {"ok": False, "alg": True, "n": n, "j": j, "g4": g4}
            want = int(G(n, j) == 1 and G(n, j - 1) == 0)
            even11 = int(g4[2] == 1 and g4[3] == 1)
            if even11 != want:
                return {"ok": False, "alg11": True, "n": n, "j": j}
            n_ok += 1
    ok = n_ok > 8 and n_die == 2
    return {"ok": ok, "n_ok": n_ok, "n_die": n_die}


def _walk_g4and(k: int, q: int) -> dict:
    """green4 never odd-s AND; covering XOR on packed odd-s AND."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = xor_all = 0
    s = t0
    while s < T:
        if s % 2 == 0:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                g4 = green4(n, j)
                if and_from_tuple(*g4):
                    return {"ok": False, "g4and": True, "k": k, "n": n, "j": j, "g4": g4}
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                n_ok += 1
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_all": xor_all}


def g4and_cover() -> dict:
    """green4 AND=0 on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g4and(k, q)
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


def killed_odd_and_identically_0() -> dict:
    """Packed odd-s AND is not identically 0: k=0, s=3, AND=1."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = packed == 1
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "packed": packed}


def killed_even_and_eq_Gj_not_Gjm1() -> dict:
    """Packed even-s AND is not G(j) and not G(j-1): k=0, s=2."""
    k, s, n, j, p = 0, 2, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    four = tuple(bit_at(row, p - 3 + i) for i in range(4))
    A = (row << 1) & row
    packed = (A >> p) & 1
    pred = int(G(n, j) == 1 and G(n, j - 1) == 0)
    ok = four == (0, 1, 0, 0) and packed == 0 and pred == 1
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
        "G": [G(n, j), G(n, j - 1)],
    }


def killed_green4_die_free() -> dict:
    """green4 is not DIE-free: k=0, s=8, n=0, j=0, g4=0111."""
    k, s, n, j, p = 0, 8, 0, 0, 10
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    four = tuple(bit_at(row, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    ok = four == g4 == (0, 1, 1, 1) and g4 in DIE
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
    }


def prefixes() -> dict:
    hr = json.loads(HR_JSON.read_text())
    ok = (
        hr["checks"]["all_ok"]
        and hr["verdict"]["odd_s_Green_6slot_eq_odd_green6"] == "LEMMA"
        and hr["verdict"]["AND_of_odd_green4_iff_Gjp1_and_not_Gj"] == "LEMMA"
        and hr["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gt: dict, gc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gt["ok"] and gc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert and_from_tuple(*green4(1, 0)) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gt = green4_and_table()
    gc = g4and_cover()
    k0 = killed_odd_and_identically_0()
    k1 = killed_even_and_eq_Gj_not_Gjm1()
    k2 = killed_green4_die_free()
    pref = prefixes()
    checks = self_checks(c20, gt, gc, k0, k1, k2, pref)
    dump = {
        "cycle": "HS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green4_and_table": {k: gt[k] for k in gt if k != "ok"},
        "g4and_cover": {k: gc[k] for k in gc if k != "ok"},
        "killed_odd_and_identically_0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_and_eq_Gj_not_Gjm1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_green4_die_free": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "AND_of_green4_identically_0": True,
            "even_Green_11_iff_Gj_and_not_Gjm1": True,
            "even_Green_11_iff_DIE_0111_or_1011": True,
            "odd_AND_identically_0": False,
            "even_AND_eq_Gj_and_not_Gjm1": False,
            "green4_DIE_free": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "AND_of_green4_identically_0": "LEMMA",
            "even_Green_11_iff_Gj_and_not_Gjm1": "LEMMA",
            "even_Green_11_iff_DIE_0111_or_1011": "LEMMA",
            "odd_AND_identically_0": "KILLED",
            "even_AND_eq_Gj_and_not_Gjm1": "KILLED",
            "green4_DIE_free": "KILLED",
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
    print("green4_and_table", dump["green4_and_table"])
    print("g4and_cover n_ok", dump["g4and_cover"]["n_ok"])
    print("killed_odd_and_identically_0", dump["killed_odd_and_identically_0"])
    print("killed_even_and_eq_Gj_not_Gjm1", dump["killed_even_and_eq_Gj_not_Gjm1"])
    print("killed_green4_die_free", dump["killed_green4_die_free"])


if __name__ == "__main__":
    main()
