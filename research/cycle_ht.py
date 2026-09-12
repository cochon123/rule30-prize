#!/usr/bin/env python3
"""Cycle HT: coboundary-shaped 4-tuples never fire odd-s AND.

A 4-tuple (z,a,b,c) is coboundary-shaped iff a=z XOR b. Those 8
tuples have AND=0 (Boolean: if b=0 then z^(a|b)=0; if b=1 then the
two AND factors are z and not z). green4 is always cob-shaped, so
this implies Cycle HS. It holds on the packed row, not only Green.
Cob-shaped is not green4; non-cob is not AND. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ht.py --certify
Dump: research/cycle_ht.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def cob_shaped(z: int, a: int, b: int, c: int) -> bool:
    """Even-s Green 4-tuples have a = z XOR b (copy/cob slots)."""
    return a == (z ^ b)


def cob_and_table() -> dict:
    """16-row: cob-shaped iff a=z^b (8 tuples); those have AND=0; AND_ONES not cob."""
    n_cob = n_ok = 0
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        z, a, b, c = four
        cs = cob_shaped(z, a, b, c)
        if cs:
            n_cob += 1
            if and_from_tuple(*four):
                return {"ok": False, "and": True, "four": four}
        if four in AND_ONES and cs:
            return {"ok": False, "ones": True, "four": four}
        n_ok += 1
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            g4 = green4(n, j)
            if not cob_shaped(*g4) or and_from_tuple(*g4):
                return {"ok": False, "g4": True, "n": n, "j": j, "g4": g4}
            n_ok += 1
    ok = n_ok > 16 and n_cob == 8
    return {"ok": ok, "n_ok": n_ok, "n_cob": n_cob}


def _walk_cob(k: int, q: int) -> dict:
    """Packed cob-shaped => odd-s AND=0 on covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_cob = xor_all = 0
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
                cs = cob_shaped(*four)
                if cs and packed:
                    return {"ok": False, "cob_and": True, "k": k, "four": four}
                if cs != (and_from_tuple(*four) == 0 and packed == 0) and cs:
                    return {"ok": False, "pack": True, "k": k, "four": four}
                n_ok += 1
                if cs:
                    n_cob += 1
                if packed and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_cob": n_cob, "xor_all": xor_all}


def cob_cover() -> dict:
    """Cob-shaped AND=0 on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_cob = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_cob(k, q)
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
            n_cob += w["n_cob"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_cob": w["n_cob"],
                "xor_all": w["xor_all"],
            }
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "n_cob": n_cob, "rows": rows}


def killed_cob_eq_green4() -> dict:
    """Cob-shaped is not green4: k=0, s=2, n=3, j=0, four=0000."""
    k, s, n, j, p = 0, 2, 3, 0, 10
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    four = tuple(bit_at(row, p - 3 + i) for i in range(4))
    g4 = green4(n, j)
    ok = (
        four == (0, 0, 0, 0)
        and cob_shaped(*four)
        and g4 == (1, 0, 1, 1)
        and four != g4
    )
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


def killed_noncob_iff_and() -> dict:
    """Non-coboundary is not AND: k=1, s=11, n=4, j=3, four=1111."""
    k, s, n, j, p = 1, 11, 4, 3, 14
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = four == (1, 1, 1, 1) and not cob_shaped(*four) and packed == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "packed": packed,
    }


def killed_cob_only_g0() -> dict:
    """Cob-shaped is not only on G=0: k=0, s=2, n=3, j=0, G(3,0)=1."""
    n, j = 3, 0
    w = killed_cob_eq_green4()
    ok = w["ok"] and G(n, j) == 1
    return {"ok": ok, "n": n, "j": j, "G": G(n, j)}


def prefixes() -> dict:
    hs = json.loads(HS_JSON.read_text())
    ok = (
        hs["checks"]["all_ok"]
        and hs["verdict"]["AND_of_green4_identically_0"] == "LEMMA"
        and hs["verdict"]["even_Green_11_iff_Gj_and_not_Gjm1"] == "LEMMA"
        and hs["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ct: dict, cc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ct["ok"] and cc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert cob_shaped(*green4(1, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ct = cob_and_table()
    cc = cob_cover()
    k0 = killed_cob_eq_green4()
    k1 = killed_noncob_iff_and()
    k2 = killed_cob_only_g0()
    pref = prefixes()
    checks = self_checks(c20, ct, cc, k0, k1, k2, pref)
    dump = {
        "cycle": "HT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cob_and_table": {k: ct[k] for k in ct if k != "ok"},
        "cob_cover": {k: cc[k] for k in cc if k != "ok"},
        "killed_cob_eq_green4": {k: k0[k] for k in k0 if k != "ok"},
        "killed_noncob_iff_and": {k: k1[k] for k in k1 if k != "ok"},
        "killed_cob_only_g0": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "cob_shaped_AND_identically_0": True,
            "green4_is_cob_shaped": True,
            "AND_ONES_not_cob_shaped": True,
            "cob_shaped_eq_green4": False,
            "noncob_iff_AND": False,
            "cob_shaped_only_on_G_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cob_shaped_AND_identically_0": "LEMMA",
            "green4_is_cob_shaped": "LEMMA",
            "AND_ONES_not_cob_shaped": "LEMMA",
            "cob_shaped_eq_green4": "KILLED",
            "noncob_iff_AND": "KILLED",
            "cob_shaped_only_on_G_eq_0": "KILLED",
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
    print("cob_and_table", dump["cob_and_table"])
    print("cob_cover n_ok", dump["cob_cover"]["n_ok"], "n_cob", dump["cob_cover"]["n_cob"])
    print("killed_cob_eq_green4", dump["killed_cob_eq_green4"])
    print("killed_noncob_iff_and", dump["killed_noncob_iff_and"])
    print("killed_cob_only_g0", dump["killed_cob_only_g0"])


if __name__ == "__main__":
    main()
