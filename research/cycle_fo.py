#!/usr/bin/env python3
"""Cycle FO: G(2^n-1, 2^m-1)=1 for n>=m; 16U left Delta on [10U,18U) is 0.

Odd peeling: G(2^n-1, 2^m-1)=G(2^{n-1}-1, 2^{m-1}-1) down to G(2^{n-m}-1,0)=1.
This is the start-bit Green on every 2^a-shift left strip (p=1 at window
start): G(W/2-1, 2U-1) with W=2^a, T=2U+W. On [10U,18U) the 16U-shift
comparing 18U to 34U has m<8U so FF matches in-support; the left strip
start contributes 1 and the rest cancels, so Delta16_L=0 (FJ-like, not
the 4U FM pattern). Kills: G(2^n-1,2^m-1)=1 for n<m; Delta16_L=1.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fo.py --certify
Dump: research/cycle_fo.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FN_JSON = Path(__file__).resolve().parent / "cycle_fn.json"
FM_JSON = Path(__file__).resolve().parent / "cycle_fm.json"
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FK_JSON = Path(__file__).resolve().parent / "cycle_fk.json"


def mersenne_ones(nmax: int = 12) -> dict:
    """G(2^n-1, 2^m-1)=1 for 0<=m<=n<=nmax."""
    n_ok = 0
    for n in range(0, nmax + 1):
        for m in range(0, n + 1):
            if G((1 << n) - 1, (1 << m) - 1) != 1:
                return {"ok": False, "n": n, "m": m}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "nmax": nmax}


def killed_n_lt_m() -> dict:
    """n<m is false: G(1,3)=0 (off support)."""
    g = G((1 << 1) - 1, (1 << 2) - 1)
    ok = g == 0
    return {"ok": ok, "n": 1, "m": 2, "G": g}


def m_lt_8U() -> dict:
    """m=18U-s-1 < 8U on s in [10U,18U)."""
    n_ok = 0
    for k in range(0, 17):
        U = 1 << k
        for s in (10 * U, 14 * U, 18 * U - 1):
            m = 18 * U - s - 1
            if not (0 <= m < 8 * U):
                return {"ok": False, "k": k, "s": s, "m": m}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def packed_left(kmax: int = 5) -> dict:
    """16U left Delta is 0: start=1, rest=1; in-support 18U matches 34U."""
    rows = {}
    n_ok = 0
    n_dl0 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 10 * U, 18 * U
        T18, T34 = 18 * U, 34 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        dL = start = rest = d_in = 0
        n_p1 = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            m = T18 - s - 1
            lo = 2 * s - 18 * U + 2
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    g18 = G(T18 - s - 1, T18 - p)
                    g34 = G(T34 - s - 1, T34 - p)
                    if p > 18 * U:
                        if g18:
                            return {"ok": False, "k": k, "right18": True}
                    elif p < lo:
                        red = G(m, 2 * U - p)
                        if g34 != red:
                            return {"ok": False, "k": k, "s": s, "p": p}
                        dL ^= g34
                        if s == t0 and p == 1:
                            start ^= g34
                            n_p1 += 1
                        else:
                            rest ^= g34
                    elif g18 != g34:
                        return {"ok": False, "k": k, "ins": True}
                    else:
                        d_in ^= g18
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if n_p1 != 1 or start != 1 or rest != 1 or dL != 0:
            return {
                "ok": False,
                "k": k,
                "start": start,
                "rest": rest,
                "dL": dL,
                "n_p1": n_p1,
            }
        n_ok += 1
        n_dl0 += 1
        rows[str(k)] = {"dL": dL, "start": start, "rest": rest, "d_in": d_in}
    return {
        "ok": n_ok == kmax - 1 and n_dl0 == n_ok,
        "n_ok": n_ok,
        "n_dl0": n_dl0,
        "rows": rows,
    }


def prefixes() -> dict:
    fn = json.loads(FN_JSON.read_text())
    fm = json.loads(FM_JSON.read_text())
    fj = json.loads(FJ_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fk = json.loads(FK_JSON.read_text())
    ok = (
        fn["checks"]["all_ok"]
        and fm["checks"]["all_ok"]
        and fj["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fk["checks"]["all_ok"]
        and fm["verdict"]["Delta4_L_eq_1"] == "LEMMA"
        and fj["verdict"]["Delta_L_eq_0"] == "LEMMA"
        and fk["verdict"]["G_n0_eq_G_n2n_eq_1"] == "LEMMA"
        and fn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, mer: dict, killed: dict, mlt: dict, pack: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mer["ok"] and killed["ok"] and mlt["ok"] and pack["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mer = mersenne_ones()
    killed = killed_n_lt_m()
    mlt = m_lt_8U()
    pack = packed_left()
    pref = prefixes()
    checks = self_checks(c20, mer, killed, mlt, pack, pref)
    dump = {
        "cycle": "FO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mersenne": {k: mer[k] for k in mer if k != "ok"},
        "killed_nltm": {k: killed[k] for k in killed if k != "ok"},
        "m_lt_8U": {k: mlt[k] for k in mlt if k != "ok"},
        "packed": {k: pack[k] for k in pack if k != "ok"},
        "lemmas": {
            "G_2n_minus_1_2m_minus_1_eq_1_n_ge_m": True,
            "m_lt_8U_on_10U_18U": True,
            "Delta16_L_eq_0": True,
            "Delta16_L_start_1_rest_1": True,
            "G_2n_minus_1_2m_minus_1_n_lt_m": False,
            "Delta16_L_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_2n_minus_1_2m_minus_1_eq_1_n_ge_m": "LEMMA",
            "m_lt_8U_on_10U_18U": "LEMMA",
            "Delta16_L_eq_0": "LEMMA",
            "Delta16_L_start_1_rest_1": "LEMMA",
            "G_2n_minus_1_2m_minus_1_n_lt_m": "KILLED",
            "Delta16_L_eq_1": "KILLED",
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
    print("mersenne", dump["mersenne"])
    print("packed", dump["packed"])


if __name__ == "__main__":
    main()
