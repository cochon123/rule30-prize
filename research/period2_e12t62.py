#!/usr/bin/env python3
"""Extra<=13 fails: S-minimal extra=14 at T=62.

A complete ugap scan of T=62 has max extra 14: ten bump even-F words,
R=27, extra bits 01001010001000, n_clip=45. T=60 has max extra 11, so
extra 16 at T=60 does not exist and extra 14 at T=62 is not a T+2
descent. Uniform extra<=11, <=12, and <=13 are therefore false. The
same T also has fifteen isolated even-F extra-12 onsets (R=23), of
which eight are the T=58 extra-11 prefixes. Not a prize claim: extra
may still be bounded.

Run: python3 research/period2_e12t62.py --certify
Dump: research/period2_e12t62.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_e11t58 import T58_PREF8
from period2_exdesc import extra_of_word, force
from period2_qshift import shift_u
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T62_E14_PREF5 = [
    "00001",
    "00010",
    "00100",
    "00101",
    "01001",
    "01010",
    "10001",
    "10010",
    "10100",
    "10101",
]
T62_E14_TAIL = "00100001000100010001000100"
T62_BUMP_EF_E14 = [p + T62_E14_TAIL for p in T62_E14_PREF5]
T62_E14_EXTRA_BITS = "01001010001000"

T62_TAIL_E12 = "10001001001000100100100"
T62_ISO_EF_E12 = [p + T62_TAIL_E12 for p in T58_PREF8]
T62_E12_EXTRA_BITS = "010000101001"

T64_TAIL_E12 = "100100100101010001010010"
T64_ISO_EF_E12 = [p + T64_TAIL_E12 for p in T58_PREF8]
T64_E12_EXTRA_BITS = "101001010001"


def scan_T(T, Emax=24, high_at=12):
    n0 = nvars(T)
    mx = -1
    n_on = 0
    extra_c = Counter()
    by_kind = Counter()
    high = []
    for u in ugap_strings(n0):
        rec = force(u, T, Emax=Emax)
        if rec is None:
            continue
        n_on += 1
        extra_c[rec["extra"]] += 1
        by_kind[rec["kind"]] += 1
        if rec["extra"] > mx:
            mx = rec["extra"]
        if rec["extra"] >= high_at:
            high.append(
                {
                    "kind": rec["kind"],
                    "stop": rec["stop"],
                    "u": rec["sample"],
                    "R": rec["R"],
                    "extra": rec["extra"],
                }
            )
        assert rec["extra"] <= Emax
    return {
        "T": T,
        "n0": n0,
        "n_onset": n_on,
        "max_extra": mx,
        "n_iso": by_kind["iso"],
        "n_bump": by_kind["bump"],
        "extra": {str(k): v for k, v in sorted(extra_c.items())},
        "n_high": len(high),
        "high": high,
        "ok": True,
    }


def check_family(words, T, extra, R, extra_bits, n_clip, desc_T, desc_extra, kind, stop):
    n0 = nvars(T)
    assert n0 == len(words[0])
    rows = []
    for w in words:
        rec = force([int(c) for c in w], T, Emax=24)
        assert rec is not None, w
        assert rec["kind"] == kind and rec["stop"] == stop
        assert rec["extra"] == extra and rec["R"] == R
        assert rec["n_clip"] == n_clip
        assert wstr(rec["bits"][n0:]) == extra_bits
        Fu, _ = F_of_u(rec["bits"], 2 * n_clip + 1)
        assert Fu[T] == 1
        assert Fu[2 * n_clip] == 1
        r2 = extra_of_word(shift_u(rec["bits"]), desc_T, Emax=24)
        assert r2["kind"] == "bump" and r2["stop"] == stop and r2["extra"] == desc_extra
        rows.append({"u": w, "R": rec["R"], "desc_extra": desc_extra})
    return {
        "n": len(rows),
        "T": T,
        "extra": extra,
        "R": R,
        "n_clip": n_clip,
        "kind": kind,
        "stop": stop,
        "ok": True,
        "words": rows,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    t60 = scan_T(60, high_at=11)
    assert t60["max_extra"] == 11, t60["max_extra"]
    assert t60["n0"] == 30
    checks["max11_T60"] = True
    t62 = scan_T(62, high_at=12)
    assert t62["max_extra"] == 14, t62["max_extra"]
    assert t62["n0"] == 31
    n_e14 = sum(1 for w in t62["high"] if w["extra"] == 14)
    n_e12 = sum(1 for w in t62["high"] if w["extra"] == 12)
    assert n_e14 == 10 and n_e12 == 15
    checks["max14_T62"] = True
    fam14 = check_family(
        T62_BUMP_EF_E14, 62, 14, 27, T62_E14_EXTRA_BITS, 45, 64, 12, "bump", "even_F"
    )
    assert sorted(w["u"] for w in t62["high"] if w["extra"] == 14) == sorted(
        T62_BUMP_EF_E14
    )
    checks["t62_bump_ef_e14_family"] = True
    fam12 = check_family(
        T62_ISO_EF_E12, 62, 12, 23, T62_E12_EXTRA_BITS, 43, 64, 10, "iso", "even_F"
    )
    checks["t62_iso_ef_e12"] = True
    fam64 = check_family(
        T64_ISO_EF_E12, 64, 12, 23, T64_E12_EXTRA_BITS, 44, 66, 10, "iso", "even_F"
    )
    checks["t64_iso_ef_e12"] = True
    checks["e14_sminimal"] = True
    return {
        "checks": checks,
        "t60": {k: t60[k] for k in t60 if k != "high"},
        "t60_e11": t60["high"],
        "t62": {k: t62[k] for k in t62 if k != "high"},
        "t62_high": t62["high"],
        "family14": fam14,
        "family12": fam12,
        "family64": fam64,
        "prefixes14": T62_E14_PREF5,
        "prefixes8": T58_PREF8,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("T60 max", report["t60"]["max_extra"], "n_e11", report["t60"]["n_high"])
    print(
        "T62 max",
        report["t62"]["max_extra"],
        "n_high",
        report["t62"]["n_high"],
        "n_e14",
        report["family14"]["n"],
    )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
