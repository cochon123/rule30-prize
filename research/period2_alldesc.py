#!/usr/bin/env python3
"""Every extra>=3 Q-clip descends by 2 at T+2 onto a bump of the same kind.

A phase-01 ugap onset (isolated or bump) whose Q-forced tail clips
with extra e>=3 — by 11, 00000, or even F_{2n}>T — has Su a bump of
the same clip kind at T+2 with extra e-2. Isolated onsets become
bumps; bumps stay bumps. Extra of every finite clip family is a rank.
Uniform extra<=8 is equivalent to extra<=8 at every S-minimal member,
which is not proved. Infinite B_0 is a fixed point of e|->e-2.
Not a prize claim.

Run: python3 research/period2_alldesc.py --certify
Dump: research/period2_alldesc.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import extra_of_word, force, skip_applies
from period2_qextra import T37_WORDS, sound_R
from period2_qshift import shift_u
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T20_UGAP_E8 = [
    "0010000100",
    "0101000100",
    "1010000100",
]

T33_ISO_EF_E7 = [
    "00100010100100100",
    "01000010100100100",
    "10100010100100100",
]


def r_of(T, extra, stop):
    n0 = nvars(T)
    return sound_R(T, n0 + extra, stop)


def certify_arithmetic():
    rows = []
    for T in range(5, 81):
        n0 = nvars(T)
        n0p = nvars(T + 2)
        assert n0p == n0 + 1
        for e in range(3, 12):
            n_clip = n0 + e
            extra_S = (n_clip - 1) - n0p
            assert extra_S == e - 2
            for stop in ("11", "00000", "even_F"):
                R = r_of(T, e, stop)
                if stop == "even_F":
                    assert R >= 5
                else:
                    assert R >= 6
                assert skip_applies(T, e, e)
                assert skip_applies(T, e, e - 1)
                assert 2 * n_clip - 4 > T  # four-zero even skip window
                assert R >= 4  # B_0 hypothesis of period2_b0
        rows.append({"T": T, "n0": n0, "n0_Tplus2": n0p})
    return {"n_T": len(rows), "ok": True}


def scan_all(Tmin=8, Tmax=40):
    n_ge3 = 0
    n_desc = 0
    n_iso = 0
    n_short = Counter()
    n_class = Counter()
    max_e = -1
    max_iso = -1
    at_max = []
    at_iso_max = []
    for T in range(Tmin, Tmax + 1):
        for u in ugap_strings(nvars(T)):
            rec = force(u, T)
            if rec is None:
                continue
            key = (rec["kind"], rec["stop"])
            n_class[key] += 1
            if rec["extra"] > max_e:
                max_e = rec["extra"]
                at_max = [(T, rec["kind"], rec["stop"], rec["sample"], rec["extra"])]
            elif rec["extra"] == max_e:
                at_max.append((T, rec["kind"], rec["stop"], rec["sample"], rec["extra"]))
            if rec["kind"] == "iso":
                if rec["extra"] > max_iso:
                    max_iso = rec["extra"]
                    at_iso_max = [(T, rec["stop"], rec["sample"], rec["extra"])]
                elif rec["extra"] == max_iso:
                    at_iso_max.append((T, rec["stop"], rec["sample"], rec["extra"]))
            if rec["extra"] < 3:
                n_short[key] += 1
                continue
            n_ge3 += 1
            if rec["kind"] == "iso":
                n_iso += 1
            Su = shift_u(rec["bits"])
            r2 = extra_of_word(Su, T + 2)
            assert r2 is not None, (T, rec["sample"])
            assert r2["kind"] == "bump", (T, rec["kind"], r2["kind"])
            assert r2["stop"] == rec["stop"], (T, rec["stop"], r2["stop"])
            assert r2["extra"] == rec["extra"] - 2, (T, rec["extra"], r2["extra"])
            n_desc += 1
    class_ge3 = {f"{k[0]}/{k[1]}": n_class[k] - n_short[k] for k in n_class}
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_ge3": n_ge3,
        "n_descended": n_desc,
        "n_iso_ge3": n_iso,
        "n_short": {f"{k[0]}/{k[1]}": v for k, v in n_short.items()},
        "n_class": {f"{k[0]}/{k[1]}": v for k, v in n_class.items()},
        "n_class_ge3": class_ge3,
        "max_extra": max_e,
        "max_iso_extra": max_iso,
        "n_at_max": len(at_max),
        "at_max": [
            {"T": t, "kind": k, "stop": s, "u": u, "extra": e} for t, k, s, u, e in at_max
        ],
        "n_at_iso_max": len(at_iso_max),
        "at_iso_max": [
            {"T": t, "stop": s, "u": u, "extra": e} for t, s, u, e in at_iso_max
        ],
    }


def certify_families():
    out = []
    specs = [
        (20, T20_UGAP_E8, 8, "bump", "11"),
        (37, [w[: nvars(37)] for w in T37_WORDS], 8, "bump", "11"),
        (33, T33_ISO_EF_E7, 7, "iso", "even_F"),
    ]
    for T, words, e0, kind, stop in specs:
        recs = []
        for w in words:
            u = [int(c) for c in w]
            rec = force(u, T)
            assert rec is not None
            assert rec["kind"] == kind and rec["stop"] == stop
            assert rec["extra"] == e0
            Su = shift_u(rec["bits"])
            r2 = extra_of_word(Su, T + 2)
            assert r2 is not None
            assert r2["kind"] == "bump" and r2["stop"] == stop
            assert r2["extra"] == e0 - 2
            recs.append(
                {
                    "u": wstr(u),
                    "extra": rec["extra"],
                    "kind": rec["kind"],
                    "extra_S": r2["extra"],
                    "kind_S": r2["kind"],
                    "sample_S": r2["sample"],
                }
            )
        out.append(
            {
                "T": T,
                "n": len(recs),
                "extra": e0,
                "kind": kind,
                "stop": stop,
                "words": recs,
            }
        )
    return out


def certify():
    t0 = time.perf_counter()
    checks = {}
    arith = certify_arithmetic()
    checks["nvars_Tplus2_and_skip_for_e_ge_3"] = arith["ok"]
    scan = scan_all(8, 40)
    assert scan["n_ge3"] == scan["n_descended"]
    assert scan["n_ge3"] == 1761
    assert scan["n_iso_ge3"] == 860
    assert scan["n_class_ge3"]["bump/11"] == 122
    assert scan["n_class_ge3"]["bump/even_F"] == 774
    assert scan["n_class_ge3"]["bump/00000"] == 5
    assert scan["n_class_ge3"]["iso/11"] == 135
    assert scan["n_class_ge3"]["iso/even_F"] == 703
    assert scan["n_class_ge3"]["iso/00000"] == 22
    assert scan["max_extra"] == 8
    assert scan["max_iso_extra"] == 7
    Ts = sorted({r["T"] for r in scan["at_max"]})
    assert Ts == [20, 37]
    checks["all_class_descent_through_40"] = True
    checks["iso_becomes_bump"] = True
    checks["max_extra_8_still_bump_11"] = True
    checks["iso_max_extra_7_through_40"] = True
    fam = certify_families()
    checks["t20_t37_t33_families"] = True
    return {
        "checks": checks,
        "arithmetic": arith,
        "scan": scan,
        "families": fam,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    scan = report["scan"]
    print(
        "scan",
        {
            k: scan[k]
            for k in (
                "n_ge3",
                "n_descended",
                "n_iso_ge3",
                "n_class_ge3",
                "max_extra",
                "max_iso_extra",
            )
        },
    )
    print("families", [(f["T"], f["n"], f["kind"], f["stop"], f["extra"]) for f in report["families"]])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
