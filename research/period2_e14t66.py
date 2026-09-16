#!/usr/bin/env python3
"""Extra=14 recurs S-minimally at T=66.

A complete ugap scan of T=66 has max extra 14: thirty-three bump even-F
words, R=27, extra bits 10101001010101, n_clip=47. T=64 has max extra
12 (probe in period2_e12t62.md), so extra 16 at T=64 does not exist and
extra 14 at T=66 is not a T+2 descent. Extra=14 is therefore a recurring
S-minimal class, not a T=62-only spike. Extra<=14 is not a T-independent
bound. Not a prize claim: extra may still be bounded or unbounded.

Run: python3 research/period2_e14t66.py --certify
Dump: research/period2_e14t66.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import extra_of_word, force
from period2_qshift import shift_u
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T66_E14_PREF9 = [
    "000010010",
    "000010100",
    "000010101",
    "000100010",
    "000100101",
    "000101010",
    "001000010",
    "001000101",
    "001001010",
    "001010010",
    "001010100",
    "001010101",
    "010000101",
    "010001010",
    "010010010",
    "010010100",
    "010010101",
    "010100010",
    "010100101",
    "010101010",
    "100001010",
    "100010010",
    "100010100",
    "100010101",
    "100100010",
    "100100101",
    "100101010",
    "101000010",
    "101000101",
    "101001010",
    "101010010",
    "101010100",
    "101010101",
]
T66_E14_TAIL = "001000101000100001010100"
T66_BUMP_EF_E14 = [p + T66_E14_TAIL for p in T66_E14_PREF9]
T66_E14_EXTRA_BITS = "10101001010101"


def scan_T66(Emax=28):
    T = 66
    n0 = nvars(T)
    mx = -1
    n_on = 0
    extra_c = Counter()
    by_kind = Counter()
    at_e14 = []
    for u in ugap_strings(n0):
        rec = force(u, T, Emax=Emax)
        if rec is None:
            continue
        n_on += 1
        extra_c[rec["extra"]] += 1
        by_kind[rec["kind"]] += 1
        if rec["extra"] > mx:
            mx = rec["extra"]
        if rec["extra"] == 14:
            at_e14.append(
                {
                    "kind": rec["kind"],
                    "stop": rec["stop"],
                    "u": rec["sample"],
                    "R": rec["R"],
                }
            )
        assert rec["extra"] <= Emax
    assert mx == 14, mx
    assert n0 == 33
    return {
        "T": T,
        "n0": n0,
        "n_onset": n_on,
        "max_extra": mx,
        "n_iso": by_kind["iso"],
        "n_bump": by_kind["bump"],
        "extra": {str(k): v for k, v in sorted(extra_c.items())},
        "n_e14": len(at_e14),
        "e14": at_e14,
        "ok": True,
    }


def certify_family():
    n0 = nvars(66)
    assert n0 == 33
    assert len(T66_E14_PREF9) == 33
    rows = []
    for w in T66_BUMP_EF_E14:
        rec = force([int(c) for c in w], 66, Emax=28)
        assert rec is not None
        assert rec["kind"] == "bump" and rec["stop"] == "even_F"
        assert rec["extra"] == 14 and rec["R"] == 27
        assert rec["n_clip"] == 47
        assert wstr(rec["bits"][n0:]) == T66_E14_EXTRA_BITS
        Fu, _ = F_of_u(rec["bits"], 95)
        assert Fu[66] == 1 and Fu[65] == 1 and Fu[64] == 1
        assert Fu[94] == 1
        r2 = extra_of_word(shift_u(rec["bits"]), 68, Emax=28)
        assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 12
        rows.append({"u": w, "R": rec["R"], "desc_extra": 12})
    return {
        "n": 33,
        "tail": T66_E14_TAIL,
        "extra_bits": T66_E14_EXTRA_BITS,
        "ok": True,
        "words": rows,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    fam = certify_family()
    checks["t66_bump_ef_e14_family"] = True
    scan = scan_T66()
    checks["max14_T66"] = True
    assert scan["n_e14"] == 33
    assert sorted(w["u"] for w in scan["e14"]) == sorted(T66_BUMP_EF_E14)
    checks["e14_is_all_max"] = True
    return {
        "checks": checks,
        "scan": scan,
        "family": fam,
        "prefixes": T66_E14_PREF9,
        "wall_time_sec": time.perf_counter() - t0,
        "t64_max_extra_probe": 12,
        "e14_sminimal_via_t64_probe": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    s = report["scan"]
    print("T", s["T"], "max", s["max_extra"], "n_e14", s["n_e14"], "n_on", s["n_onset"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
