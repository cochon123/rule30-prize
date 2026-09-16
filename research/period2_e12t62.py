#!/usr/bin/env python3
"""Extra<=11 fails: extra=12 at T=62 on the T=58 prefixes.

The eight length-8 prefixes of the T=58 isolated extra-11 family
each extend to an isolated even-F extra-12 onset at T=62 (R=23,
n_clip=43) and again at T=64 (R=23, n_clip=44). Extra<=11 is
therefore false. This is a forced-word certificate, not a complete
T=62 scan. Not a prize claim: extra may still be bounded.

Run: python3 research/period2_e12t62.py --certify
Dump: research/period2_e12t62.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_e11t58 import T58_PREF8
from period2_exdesc import extra_of_word, force
from period2_qshift import shift_u
from period2_ugap_sat import wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T62_TAIL = "10001001001000100100100"
T62_ISO_EF_E12 = [p + T62_TAIL for p in T58_PREF8]
T62_E12_EXTRA_BITS = "010000101001"

T64_TAIL = "100100100101010001010010"
T64_ISO_EF_E12 = [p + T64_TAIL for p in T58_PREF8]
T64_E12_EXTRA_BITS = "101001010001"


def check_family(words, T, extra, R, extra_bits, n_clip, desc_T, desc_extra):
    n0 = nvars(T)
    assert n0 == len(words[0])
    rows = []
    for w in words:
        rec = force([int(c) for c in w], T)
        assert rec is not None, w
        assert rec["kind"] == "iso" and rec["stop"] == "even_F"
        assert rec["extra"] == extra and rec["R"] == R
        assert rec["n_clip"] == n_clip
        assert wstr(rec["bits"][n0:]) == extra_bits
        Fu, _ = F_of_u(rec["bits"], 2 * n_clip + 1)
        assert Fu[T] == 1
        assert Fu[2 * n_clip] == 1
        r2 = extra_of_word(shift_u(rec["bits"]), desc_T)
        assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == desc_extra
        rows.append({"u": w, "R": rec["R"], "desc_extra": desc_extra})
    return {"n": len(rows), "T": T, "extra": extra, "R": R, "n_clip": n_clip, "ok": True, "words": rows}


def certify():
    t0 = time.perf_counter()
    checks = {}
    assert len(T58_PREF8) == 8
    assert all(len(p) == 8 for p in T58_PREF8)
    t62 = check_family(T62_ISO_EF_E12, 62, 12, 23, T62_E12_EXTRA_BITS, 43, 64, 10)
    checks["t62_iso_ef_e12"] = True
    t64 = check_family(T64_ISO_EF_E12, 64, 12, 23, T64_E12_EXTRA_BITS, 44, 66, 10)
    checks["t64_iso_ef_e12"] = True
    return {
        "checks": checks,
        "t62": t62,
        "t64": t64,
        "prefixes": T58_PREF8,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("t62 n", report["t62"]["n"], "extra", report["t62"]["extra"], "R", report["t62"]["R"])
    print("t64 n", report["t64"]["n"], "extra", report["t64"]["extra"], "R", report["t64"]["R"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
