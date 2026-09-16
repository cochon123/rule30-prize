#!/usr/bin/env python3
"""11-clip extra of a bump descends by 2 under S at T+2.

A phase-01 ugap bump onset (F_T=F_{T-1}=1) whose Q-forced tail
11-clips with extra e>=3 has 11-clip R=2e or 2e+1 >=6, so the
three-zero skip of period2_qshift applies at n_clip and n_clip-1.
The clip therefore propagates: Su is a bump 11-clip at T+2 with
extra e-2. Extra of a 11-clip bump family is a rank, equal to
e_ker+2m with e_ker in {0,1,2} at the large-T end. A uniform extra
<=8 for this class is equivalent to extra<=8 at every S-minimal
member. Isolated onsets and even_F clips are not this identity.
Not a prize claim: S-minimal extra is not bounded.

Run: python3 research/period2_exdesc.py --certify
Dump: research/period2_exdesc.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_qextra import T37_WORDS, sound_R
from period2_qshift import force_from, shift_u
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T20_UGAP_E8 = [
    "0010000100",
    "0101000100",
    "1010000100",
]


def force(u, T, Emax=16):
    n0 = nvars(T)
    u = list(u[:n0])
    F, _ = F_of_u(u, max(T + 2, 2 * n0 + 2))
    if T >= len(F) or F[T] != 1:
        return None
    bits, ev = force_from(u, T, n_max=n0 + Emax)
    stop = ev[-1].get("stop")
    n_clip = ev[-1]["n"]
    return {
        "extra": n_clip - n0,
        "stop": stop,
        "kind": "bump" if T >= 1 and F[T - 1] == 1 else "iso",
        "bits": bits,
        "n_clip": n_clip,
        "n0": n0,
        "R": sound_R(T, n_clip, stop),
        "sample": wstr(u),
    }


def extra_of_word(bits, T, Emax=16):
    n0 = nvars(T)
    prefix = list(bits[:n0]) if len(bits) >= n0 else list(bits) + [0] * (n0 - len(bits))
    return force(prefix, T, Emax)


def skip_applies(T, extra, n_rel):
    """Three-zero skip at n = n0 + n_rel needs 2n-3 > T."""
    n0 = nvars(T)
    n = n0 + n_rel
    return 2 * n - 3 > T


def certify_arithmetic():
    rows = []
    for T in range(5, 81):
        if T == 4:
            continue
        n0 = nvars(T)
        for e in range(3, 12):
            R11 = 2 * (n0 + e) - T
            assert R11 >= 6
            assert skip_applies(T, e, e)
            assert skip_applies(T, e, e - 1)
            n_clip = n0 + e
            assert 2 * (n_clip - 1) - 3 == 2 * n_clip - 5
            assert 2 * n_clip - 5 >= T + 1
        rows.append({"T": T, "n0": n0, "R11_e3": 2 * (n0 + 3) - T})
    return {"n_T": len(rows), "ok": True}


def scan_bump11(Tmin=8, Tmax=40):
    n_ge3 = 0
    n_short = Counter()
    n_desc = 0
    max_e = -1
    at_max = []
    for T in range(Tmin, Tmax + 1):
        for u in ugap_strings(nvars(T)):
            rec = force(u, T)
            if rec is None or rec["kind"] != "bump" or rec["stop"] != "11":
                continue
            if rec["extra"] > max_e:
                max_e = rec["extra"]
                at_max = [(T, rec["sample"], rec["extra"])]
            elif rec["extra"] == max_e:
                at_max.append((T, rec["sample"], rec["extra"]))
            if rec["extra"] < 3:
                n_short[rec["extra"]] += 1
                continue
            n_ge3 += 1
            Su = shift_u(rec["bits"])
            r2 = extra_of_word(Su, T + 2)
            assert r2 is not None, (T, rec["sample"])
            assert r2["kind"] == "bump" and r2["stop"] == "11"
            assert r2["extra"] == rec["extra"] - 2, (T, rec["extra"], r2["extra"])
            n_desc += 1
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_ge3": n_ge3,
        "n_descended": n_desc,
        "n_short": dict(n_short),
        "max_extra": max_e,
        "n_at_max": len(at_max),
        "at_max": [{"T": t, "u": s, "extra": e} for t, s, e in at_max],
    }


def certify_families():
    out = []
    for T, words, e0 in ((20, T20_UGAP_E8, 8), (37, [w[: nvars(37)] for w in T37_WORDS], 8)):
        recs = []
        for w in words:
            u = [int(c) for c in w]
            rec = force(u, T)
            assert rec is not None
            assert rec["kind"] == "bump" and rec["stop"] == "11"
            assert rec["extra"] == e0
            Su = shift_u(rec["bits"])
            r2 = extra_of_word(Su, T + 2)
            assert r2 is not None and r2["extra"] == e0 - 2
            assert r2["kind"] == "bump" and r2["stop"] == "11"
            recs.append({"u": wstr(u), "extra": rec["extra"], "extra_S": r2["extra"]})
        out.append({"T": T, "n": len(recs), "extra": e0, "words": recs})
    return out


def certify():
    t0 = time.perf_counter()
    checks = {}
    arith = certify_arithmetic()
    checks["skip_at_clip_for_e_ge_3"] = arith["ok"]
    scan = scan_bump11(8, 40)
    assert scan["n_ge3"] == scan["n_descended"]
    assert scan["max_extra"] == 8
    assert scan["n_at_max"] == 6
    Ts = sorted({r["T"] for r in scan["at_max"]})
    assert Ts == [20, 37]
    checks["descent_through_40"] = True
    checks["max_extra_8_at_20_and_37"] = True
    fam = certify_families()
    checks["t20_t37_families"] = True
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
    print("scan", {k: report["scan"][k] for k in ("n_ge3", "n_descended", "n_short", "max_extra", "n_at_max")})
    print("families", [(f["T"], f["n"], f["extra"]) for f in report["families"]])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
