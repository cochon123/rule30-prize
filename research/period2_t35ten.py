#!/usr/bin/env python3
"""T=35 isolated extra-7 is the 10-tail family, S-minimal.

Every T=35 isolated extra-7 ugap onset is one of six words with a
length-12 suffix 101010101010 (alternating 10). They share extra bits
0101000, R=14, and F-pattern 1 then 14 zeros then 1. None is an R=3
image of even-F extra-2 at T=34. They descend at T+2 to bump extra-5.
Isolated extra-8 still lives S-minimally at T=43. Not a prize claim.

Run: python3 research/period2_t35ten.py --certify
Dump: research/period2_t35ten.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import extra_of_word, force
from period2_qshift import shift_u
from period2_r3pull import T35_ISO_EF_E7, r3_preimages
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T35_PREFIXES = [
    "000100",
    "001000",
    "010000",
    "010100",
    "100100",
    "101000",
]
T35_TAIL = "101010101010"
T35_EXTRA_BITS = "0101000"

T43_ISO_EF_E8 = [
    "0000100001001000010010",
    "0001010001001000010010",
    "0010010001001000010010",
    "0010100001001000010010",
    "0100010001001000010010",
    "0100100001001000010010",
    "0101010001001000010010",
    "1000010001001000010010",
    "1000100001001000010010",
    "1001010001001000010010",
    "1010010001001000010010",
    "1010100001001000010010",
]
T43_R3_E8 = [
    "0000100001001000010010",
    "0100100001001000010010",
    "1000100001001000010010",
]
T43_TAIL = "0001001000010010"


def certify_t35_family():
    T = 35
    n0 = nvars(T)
    assert n0 == 18
    assert sorted(p + T35_TAIL for p in T35_PREFIXES) == sorted(T35_ISO_EF_E7)
    rows = []
    for w in T35_ISO_EF_E7:
        u = [int(c) for c in w]
        rec = force(u, T)
        assert rec is not None
        assert rec["kind"] == "iso" and rec["stop"] == "even_F"
        assert rec["extra"] == 7
        assert rec["R"] == 14
        assert rec["n_clip"] == 25
        assert w.endswith(T35_TAIL)
        assert w[:6] in T35_PREFIXES
        assert wstr(rec["bits"][n0:]) == T35_EXTRA_BITS
        Fu, _ = F_of_u(rec["bits"], T + 16)
        assert Fu[T] == 1
        assert all(Fu[T + d] == 0 for d in range(1, 15))
        assert Fu[T + 15] == 1
        assert r3_preimages(u, T) == []
        Su = shift_u(rec["bits"])
        r2 = extra_of_word(Su, T + 2)
        assert r2 is not None
        assert r2["kind"] == "bump" and r2["stop"] == "even_F"
        assert r2["extra"] == 5
        rows.append(
            {
                "u": w,
                "prefix": w[:6],
                "extra_bits": T35_EXTRA_BITS,
                "extra_S": r2["extra"],
                "sample_S": r2["sample"],
            }
        )
    return {"n": len(rows), "words": rows, "ok": True}


def certify_t35_complete():
    T = 35
    n0 = nvars(T)
    found = []
    for u in ugap_strings(n0):
        rec = force(u, T)
        if rec is None or rec["kind"] != "iso" or rec["extra"] != 7:
            continue
        found.append(rec["sample"])
        assert rec["sample"] in T35_ISO_EF_E7
    assert sorted(found) == sorted(T35_ISO_EF_E7)
    return {"n": len(found), "ok": True}


def certify_t43_e8():
    T = 43
    n0 = nvars(T)
    assert n0 == 22
    n_r3 = 0
    n_sm = 0
    rows = []
    for w in T43_ISO_EF_E8:
        u = [int(c) for c in w]
        rec = force(u, T)
        assert rec is not None
        assert rec["kind"] == "iso" and rec["stop"] == "even_F"
        assert rec["extra"] == 8
        assert rec["R"] == 16
        assert w.endswith(T43_TAIL)
        hits = r3_preimages(u, T)
        is_r3 = w in T43_R3_E8
        assert bool(hits) == is_r3, (w, [h["sample"] for h in hits])
        if is_r3:
            n_r3 += 1
            assert all(h["kind"] == "bump" and h["extra"] == 2 for h in hits)
        else:
            n_sm += 1
        rows.append({"u": w, "r3": is_r3, "n_pre": len(hits)})
    assert n_r3 == 3
    assert n_sm == 9
    found = []
    for u in ugap_strings(n0):
        rec = force(u, T)
        if rec is None or rec["kind"] != "iso" or rec["extra"] != 8:
            continue
        found.append(rec["sample"])
        assert rec["sample"] in T43_ISO_EF_E8
    assert sorted(found) == sorted(T43_ISO_EF_E8)
    return {"n": 12, "n_r3": n_r3, "n_sminimal": n_sm, "words": rows, "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    fam = certify_t35_family()
    checks["t35_e7_ten_tail_sminimal"] = True
    comp = certify_t35_complete()
    checks["t35_iso_e7_exactly_six"] = True
    t43 = certify_t43_e8()
    checks["t43_iso_e8_nine_sminimal"] = True
    return {
        "checks": checks,
        "t35_family": fam,
        "t35_complete": comp,
        "t43_e8": t43,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("t35", report["t35_family"]["n"])
    print("t43", report["t43_e8"]["n_r3"], "r3", report["t43_e8"]["n_sminimal"], "sm")
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
