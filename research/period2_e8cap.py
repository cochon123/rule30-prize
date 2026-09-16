#!/usr/bin/env python3
"""Ugap extra is at most 8 through T=48.

A complete ugap onset scan for T=41..48 finds max extra 8, attained
at T=43 (iso even_F, the (00010010)^2 tail), T=44 (iso 11), T=46
(bump even_F), T=47 (iso even_F), and T=48 (bump even_F). Combined
with period2_alldesc through T=40, extra<=8 holds through T=48. This
is a census, not a T-independent bound. Not a prize claim.

Run: python3 research/period2_e8cap.py --certify
Dump: research/period2_e8cap.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import force
from period2_t35ten import T43_ISO_EF_E8, T43_TAIL
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")

# T in 41..48 at which extra 8 occurs, from a prior full scan.
E8_T = (43, 44, 46, 47, 48)
NO_E8_T = (41, 42, 45)


def scan_range(Tmin=41, Tmax=48, Emax=16):
    rows = []
    e8 = []
    global_max = -1
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        mx = -1
        n_on = 0
        by_kind = Counter()
        extra_c = Counter()
        at_max = []
        at_e8 = []
        for u in ugap_strings(n0):
            rec = force(u, T, Emax=Emax)
            if rec is None:
                continue
            n_on += 1
            extra_c[rec["extra"]] += 1
            by_kind[rec["kind"]] += 1
            if rec["extra"] > mx:
                mx = rec["extra"]
                at_max = [(rec["kind"], rec["stop"], rec["sample"], rec["extra"])]
            elif rec["extra"] == mx:
                at_max.append((rec["kind"], rec["stop"], rec["sample"], rec["extra"]))
            if rec["extra"] == 8:
                at_e8.append(
                    {
                        "kind": rec["kind"],
                        "stop": rec["stop"],
                        "u": rec["sample"],
                        "R": rec["R"],
                    }
                )
            assert rec["extra"] <= Emax
        assert mx <= 8, (T, mx)
        global_max = max(global_max, mx)
        if T in E8_T:
            assert mx == 8, T
            assert at_e8
        if T in NO_E8_T:
            assert mx == 7, (T, mx)
        rows.append(
            {
                "T": T,
                "n0": n0,
                "n_onset": n_on,
                "max_extra": mx,
                "n_iso": by_kind["iso"],
                "n_bump": by_kind["bump"],
                "extra": {str(k): v for k, v in sorted(extra_c.items())},
                "n_at_max": len(at_max),
                "n_e8": len(at_e8),
                "sample_max": {
                    "kind": at_max[0][0],
                    "stop": at_max[0][1],
                    "u": at_max[0][2],
                    "extra": at_max[0][3],
                }
                if at_max
                else None,
            }
        )
        if at_e8:
            e8.append({"T": T, "n": len(at_e8), "words": at_e8})
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "global_max_extra": global_max,
        "rows": rows,
        "e8": e8,
        "ok": True,
    }


def certify_t43_p8(scan):
    t43 = next(x for x in scan["e8"] if x["T"] == 43)
    iso = [w for w in t43["words"] if w["kind"] == "iso"]
    assert {w["u"] for w in iso} == set(T43_ISO_EF_E8)
    assert all(w["stop"] == "even_F" and w["u"].endswith(T43_TAIL) for w in iso)
    assert T43_TAIL == "00010010" * 2
    return {"n_iso_e8": len(iso), "tail": T43_TAIL, "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    scan = scan_range(41, 48)
    checks["extra_le_8_T_41_48"] = True
    checks["e8_at_43_44_46_47_48"] = True
    checks["max_7_at_41_42_45"] = True
    p8 = certify_t43_p8(scan)
    checks["t43_e8_is_p8_tail"] = True
    return {
        "checks": checks,
        "scan": scan,
        "t43_p8": p8,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    for row in report["scan"]["rows"]:
        print(
            "T",
            row["T"],
            "max",
            row["max_extra"],
            "n_e8",
            row["n_e8"],
            "n_on",
            row["n_onset"],
        )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
