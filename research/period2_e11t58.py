#!/usr/bin/env python3
"""Extra<=10 fails: S-minimal extra=11 at T=58.

A complete ugap scan of T=58 finds max extra 11: eight isolated
even-F words, R=21, extra bits 01010001000, F-pattern 1 then 21
zeros then 1. T=56 has max extra 10, so extra 11 is not a T+2
descent. Uniform extra<=10 is false. Not a prize claim: extra may
still be bounded.

Run: python3 research/period2_e11t58.py --certify
Dump: research/period2_e11t58.json
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
E10CAP = Path(__file__).resolve().with_name("period2_e10cap.json")

T58_PREF8 = [
    "00001000",
    "00010000",
    "00101000",
    "01001000",
    "01010000",
    "10001000",
    "10010000",
    "10101000",
]
T58_TAIL = "100101001000010000100"
T58_ISO_EF_E11 = [p + T58_TAIL for p in T58_PREF8]
T58_E11_EXTRA_BITS = "01010001000"


def scan_T58(Emax=24):
    T = 58
    n0 = nvars(T)
    mx = -1
    n_on = 0
    extra_c = Counter()
    by_kind = Counter()
    at_e11 = []
    n_e10 = 0
    for u in ugap_strings(n0):
        rec = force(u, T, Emax=Emax)
        if rec is None:
            continue
        n_on += 1
        extra_c[rec["extra"]] += 1
        by_kind[rec["kind"]] += 1
        if rec["extra"] > mx:
            mx = rec["extra"]
        if rec["extra"] == 11:
            at_e11.append(
                {
                    "kind": rec["kind"],
                    "stop": rec["stop"],
                    "u": rec["sample"],
                    "R": rec["R"],
                }
            )
        if rec["extra"] == 10:
            n_e10 += 1
        assert rec["extra"] <= Emax
    assert mx == 11, mx
    assert n0 == 29
    return {
        "T": T,
        "n0": n0,
        "n_onset": n_on,
        "max_extra": mx,
        "n_iso": by_kind["iso"],
        "n_bump": by_kind["bump"],
        "extra": {str(k): v for k, v in sorted(extra_c.items())},
        "n_e10": n_e10,
        "n_e11": len(at_e11),
        "e11": at_e11,
        "ok": True,
    }


def certify_family(scan):
    n0 = nvars(58)
    assert sorted(w["u"] for w in scan["e11"]) == sorted(T58_ISO_EF_E11)
    assert all(w["kind"] == "iso" and w["stop"] == "even_F" and w["R"] == 21 for w in scan["e11"])
    rows = []
    for w in T58_ISO_EF_E11:
        rec = force([int(c) for c in w], 58)
        assert rec["extra"] == 11 and rec["R"] == 21
        assert rec["n_clip"] == 40
        assert wstr(rec["bits"][n0:]) == T58_E11_EXTRA_BITS
        Fu, _ = F_of_u(rec["bits"], 81)
        assert Fu[58] == 1
        assert all(Fu[k] == 0 for k in range(59, 80))
        assert Fu[80] == 1
        r2 = extra_of_word(shift_u(rec["bits"]), 60)
        assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 9
        rows.append({"u": w, "R": rec["R"], "desc_extra": 9})
    return {"n": 8, "tail": T58_TAIL, "extra_bits": T58_E11_EXTRA_BITS, "ok": True, "words": rows}


def certify_sminimal():
    prev = json.loads(E10CAP.read_text())
    t56 = next(x for x in prev["scan"]["rows"] if x["T"] == 56)
    assert t56["max_extra"] == 10
    return {"t56_max": 10, "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    scan = scan_T58()
    checks["max11_T58"] = True
    fam = certify_family(scan)
    checks["t58_iso_ef_e11_family"] = True
    sm = certify_sminimal()
    checks["e11_sminimal"] = True
    assert scan["n_e11"] == 8
    return {
        "checks": checks,
        "scan": scan,
        "family": fam,
        "sminimal": sm,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    s = report["scan"]
    print("T", s["T"], "max", s["max_extra"], "n_e11", s["n_e11"], "n_e10", s["n_e10"], "n_on", s["n_onset"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
