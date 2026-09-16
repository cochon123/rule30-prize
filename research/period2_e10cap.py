#!/usr/bin/env python3
"""Extra<=10 through T=56; S-minimal extra=10 recurs.

A complete ugap scan of T=53..56 finds max extra 9 at T=53 and max
extra 10 at T=54,55,56. The extra-10 onsets are S-minimal (no extra-12
parent at T-2) and fall in two explicit families: T=54 is P_35 with
an 11-clip, T=55 and T=56 are seven isolated even-F words on the
odd-ending P_43 prefixes. Extra does not climb past 10 on this range.
Census, not a T-independent bound. Not a prize claim.

Run: python3 research/period2_e10cap.py --certify
Dump: research/period2_e10cap.json
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
from period2_t35ten import T35_PREFIXES
from period2_ugap_sat import ugap_strings
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")
E10T51 = Path(__file__).resolve().with_name("period2_e10t51.json")

T54_TAIL = "101010000101001001010"
T54_ISO_11_E10 = [p + T54_TAIL for p in T35_PREFIXES]

T55_PREFS = [
    "000101",
    "001001",
    "010001",
    "010101",
    "100001",
    "100101",
    "101001",
]
T55_TAIL = "0010001010000100101001"
T55_ISO_EF_E10 = [p + T55_TAIL for p in T55_PREFS]

T56_TAIL = "0010000100010101000100"
T56_ISO_EF_E10 = [p + T56_TAIL for p in T55_PREFS]


def scan_range(Tmin=53, Tmax=56, Emax=24):
    rows = []
    e10 = []
    global_max = -1
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        mx = -1
        n_on = 0
        extra_c = Counter()
        by_kind = Counter()
        at_e10 = []
        for u in ugap_strings(n0):
            rec = force(u, T, Emax=Emax)
            if rec is None:
                continue
            n_on += 1
            extra_c[rec["extra"]] += 1
            by_kind[rec["kind"]] += 1
            if rec["extra"] > mx:
                mx = rec["extra"]
            if rec["extra"] == 10:
                at_e10.append(
                    {
                        "kind": rec["kind"],
                        "stop": rec["stop"],
                        "u": rec["sample"],
                        "R": rec["R"],
                    }
                )
            assert rec["extra"] <= Emax
        assert mx <= 10, (T, mx)
        if T == 53:
            assert mx == 9, T
            assert not at_e10
        if T in (54, 55, 56):
            assert mx == 10, T
            assert at_e10
        global_max = max(global_max, mx)
        rows.append(
            {
                "T": T,
                "n0": n0,
                "n_onset": n_on,
                "max_extra": mx,
                "n_iso": by_kind["iso"],
                "n_bump": by_kind["bump"],
                "extra": {str(k): v for k, v in sorted(extra_c.items())},
                "n_e10": len(at_e10),
            }
        )
        if at_e10:
            e10.append({"T": T, "n": len(at_e10), "words": at_e10})
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "global_max_extra": global_max,
        "rows": rows,
        "e10": e10,
        "ok": True,
    }


def e10_words(scan, T):
    block = next(x for x in scan["e10"] if x["T"] == T)
    return block["words"]


def certify_families(scan):
    w54 = e10_words(scan, 54)
    assert sorted(w["u"] for w in w54) == sorted(T54_ISO_11_E10)
    assert all(w["kind"] == "iso" and w["stop"] == "11" and w["R"] == 20 for w in w54)
    rec54 = force([int(c) for c in T54_ISO_11_E10[0]], 54)
    r2 = extra_of_word(shift_u(rec54["bits"]), 56)
    assert r2["kind"] == "bump" and r2["stop"] == "11" and r2["extra"] == 8

    w55 = e10_words(scan, 55)
    assert sorted(w["u"] for w in w55) == sorted(T55_ISO_EF_E10)
    assert all(w["kind"] == "iso" and w["stop"] == "even_F" and w["R"] == 20 for w in w55)
    rec55 = force([int(c) for c in T55_ISO_EF_E10[0]], 55)
    r2 = extra_of_word(shift_u(rec55["bits"]), 57)
    assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 8

    w56 = e10_words(scan, 56)
    assert sorted(w["u"] for w in w56) == sorted(T56_ISO_EF_E10)
    assert all(w["kind"] == "iso" and w["stop"] == "even_F" and w["R"] == 19 for w in w56)
    rec56 = force([int(c) for c in T56_ISO_EF_E10[0]], 56)
    r2 = extra_of_word(shift_u(rec56["bits"]), 58)
    assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 8
    return {
        "t54_n": 6,
        "t54_tail": T54_TAIL,
        "t55_n": 7,
        "t55_tail": T55_TAIL,
        "t56_n": 7,
        "t56_tail": T56_TAIL,
        "ok": True,
    }


def certify_sminimal(scan):
    prev = json.loads(E10T51.read_text())
    t52 = next(x for x in prev["scan"]["rows"] if x["T"] == 52)
    assert t52["max_extra"] == 10
    t53 = next(x for x in scan["rows"] if x["T"] == 53)
    t54 = next(x for x in scan["rows"] if x["T"] == 54)
    assert t53["max_extra"] == 9
    assert t54["max_extra"] == 10
    return {"t52_max": 10, "t53_max": 9, "t54_max": 10, "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    scan = scan_range(53, 56)
    checks["extra_le_10_T53_56"] = True
    fam = certify_families(scan)
    checks["e10_families"] = True
    sm = certify_sminimal(scan)
    checks["e10_sminimal"] = True
    assert scan["global_max_extra"] == 10
    return {
        "checks": checks,
        "scan": scan,
        "families": fam,
        "sminimal": sm,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    for row in report["scan"]["rows"]:
        print("T", row["T"], "max", row["max_extra"], "n_e10", row["n_e10"], "n_on", row["n_onset"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
