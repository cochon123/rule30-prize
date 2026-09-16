#!/usr/bin/env python3
"""Extra<=8 fails: S-minimal extra=10 at T=51 and T=52.

A complete ugap scan of T=49..52 finds max extra 8 at T=49 and T=50,
then extra 10 at T=51 (four isolated even-F words, R=20, no R=3
preimage) and at T=52 (eight 11-clips, R=20). T=51 also has eleven
S-minimal bump even-F extra-9 onsets. Extra 12 at T=49/50 does not
exist, so none of these high extras is a T+2 descent. Uniform extra
<=8 is false. Not a prize claim: extra may still be bounded.

Run: python3 research/period2_e10t51.py --certify
Dump: research/period2_e10t51.json
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
from period2_r3pull import r3_preimages
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T51_ISO_EF_E10 = [
    "00100100001001010001010100",
    "01000100001001010001010100",
    "10000100001001010001010100",
    "10100100001001010001010100",
]
T51_TAIL_E10 = "00100001001010001010100"
T51_E10_EXTRA_BITS = "0010010001"

T51_E9_A = [
    "00001000100100010101000010",
    "00010000100100010101000010",
    "00101000100100010101000010",
    "01001000100100010101000010",
    "01010000100100010101000010",
    "10001000100100010101000010",
    "10010000100100010101000010",
    "10101000100100010101000010",
]
T51_TAIL_E9_A = "00100100010101000010"

T51_E9_B = [
    "00010101010101010101010001",
    "01010101010101010101010001",
    "10010101010101010101010001",
]
T51_TAIL_E9_B = "01010101010101010001"

T52_E10 = [
    "00001000101001001001000100",
    "00010000101001001001000100",
    "00101000101001001001000100",
    "01001000101001001001000100",
    "01010000101001001001000100",
    "10001000101001001001000100",
    "10010000101001001001000100",
    "10101000101001001001000100",
]
T52_TAIL_E10 = "101001001001000100"


def scan_range(Tmin=49, Tmax=52, Emax=20):
    rows = []
    high = []
    global_max = -1
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        mx = -1
        n_on = 0
        by_kind = Counter()
        extra_c = Counter()
        at_max = []
        at_high = []
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
            if rec["extra"] >= 9:
                at_high.append(
                    {
                        "kind": rec["kind"],
                        "stop": rec["stop"],
                        "u": rec["sample"],
                        "extra": rec["extra"],
                        "R": rec["R"],
                    }
                )
            assert rec["extra"] <= Emax
        if T in (49, 50):
            assert mx == 8, (T, mx)
        if T in (51, 52):
            assert mx == 10, (T, mx)
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
                "n_at_max": len(at_max),
                "n_ge9": len(at_high),
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
        if at_high:
            high.append({"T": T, "n": len(at_high), "words": at_high})
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "global_max_extra": global_max,
        "rows": rows,
        "ge9": high,
        "ok": True,
    }


def words_at(scan, T, extra=None):
    block = next(x for x in scan["ge9"] if x["T"] == T)
    ws = block["words"]
    if extra is None:
        return ws
    return [w for w in ws if w["extra"] == extra]


def certify_t51(scan):
    n0 = nvars(51)
    assert n0 == 26
    e10 = words_at(scan, 51, 10)
    e9 = words_at(scan, 51, 9)
    assert sorted(w["u"] for w in e10) == sorted(T51_ISO_EF_E10)
    assert all(w["kind"] == "iso" and w["stop"] == "even_F" and w["R"] == 20 for w in e10)
    assert all(w["u"].endswith(T51_TAIL_E10) for w in e10)
    assert sorted(w["u"] for w in e9) == sorted(T51_E9_A + T51_E9_B)
    assert all(w["kind"] == "bump" and w["stop"] == "even_F" and w["R"] == 18 for w in e9)
    assert all(w.endswith(T51_TAIL_E9_A) for w in T51_E9_A)
    assert all(w.endswith(T51_TAIL_E9_B) for w in T51_E9_B)
    row = next(x for x in scan["rows"] if x["T"] == 51)
    assert row["extra"].get("8") is None
    assert row["n_ge9"] == 15
    rows = []
    for w in T51_ISO_EF_E10:
        rec = force([int(c) for c in w], 51)
        assert rec["extra"] == 10 and rec["R"] == 20
        assert rec["n_clip"] == 36
        assert wstr(rec["bits"][n0:]) == T51_E10_EXTRA_BITS
        Fu, _ = F_of_u(rec["bits"], 73)
        assert Fu[51] == 1
        assert all(Fu[k] == 0 for k in range(52, 72))
        assert Fu[72] == 1
        assert r3_preimages([int(c) for c in w], 51) == []
        r2 = extra_of_word(shift_u(rec["bits"]), 53)
        assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 8
        rows.append({"u": w, "R": rec["R"], "n_r3": 0, "desc_extra": 8})
    rec_a = force([int(c) for c in T51_E9_A[0]], 51)
    rec_b = force([int(c) for c in T51_E9_B[0]], 51)
    assert rec_a["extra"] == rec_b["extra"] == 9
    da = extra_of_word(shift_u(rec_a["bits"]), 53)
    db = extra_of_word(shift_u(rec_b["bits"]), 53)
    assert da["extra"] == db["extra"] == 7
    return {
        "n_e10": 4,
        "n_e9": 11,
        "tail_e10": T51_TAIL_E10,
        "n_r3": 0,
        "ok": True,
        "e10": rows,
    }


def certify_t52(scan):
    e10 = words_at(scan, 52, 10)
    assert sorted(w["u"] for w in e10) == sorted(T52_E10)
    assert all(w["stop"] == "11" and w["extra"] == 10 and w["R"] == 20 for w in e10)
    assert all(w.endswith(T52_TAIL_E10) for w in T52_E10)
    n_iso = sum(1 for w in e10 if w["kind"] == "iso")
    n_bump = sum(1 for w in e10 if w["kind"] == "bump")
    assert n_iso == 6 and n_bump == 2
    rec0 = force([int(c) for c in T52_E10[0]], 52)
    assert rec0["extra"] == 10 and rec0["n_clip"] == 36
    r2 = extra_of_word(shift_u(rec0["bits"]), 54)
    assert r2["kind"] == "bump" and r2["stop"] == "11" and r2["extra"] == 8
    return {
        "n_e10": 8,
        "n_iso": n_iso,
        "n_bump": n_bump,
        "tail": T52_TAIL_E10,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    scan = scan_range(49, 52)
    checks["max8_T49_T50"] = True
    checks["max10_T51_T52"] = True
    t51 = certify_t51(scan)
    checks["t51_iso_ef_e10_sminimal"] = True
    t52 = certify_t52(scan)
    checks["t52_11_e10_sminimal"] = True
    assert scan["global_max_extra"] == 10
    return {
        "checks": checks,
        "scan": scan,
        "t51": t51,
        "t52": t52,
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
            "n_ge9",
            row["n_ge9"],
            "n_on",
            row["n_onset"],
        )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
