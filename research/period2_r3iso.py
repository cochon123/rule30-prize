#!/usr/bin/env python3
"""R=3 even fire: S sends the onset to an isolated 1 at T+1.

On a phase-01 period-2 centre, if F_T=1, F_{T+1}=F_{T+2}=F_{T+3}=0
and F_{T+4}=1, spatial reconstruction gives G_T=G_{T+1}=1, G_{T+2}=0,
G_{T+3}=1. Fold then yields F_T(Su)=0, F_{T+1}(Su)=1, F_{T+2}(Su)=0:
Su is isolated at T+1. Even-T even-F extra=2 is exactly this pattern
(R=3, clip at T+4). It is the R=3 companion of the R>=4 germ in
period2_germ / period2_b0, which produced a bump rather than an
isolated 1. Extra of the image is not a rank. Not a prize claim.

Run: python3 research/period2_r3iso.py --certify
Dump: research/period2_r3iso.json
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
from period2_qextra import sound_R
from period2_qshift import shift_u
from period2_ugap_sat import ugap_strings
from period2_vacuum import F_of_u, fib_strings, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def pattern_ok(F, T):
    if T + 4 >= len(F) or T < 1:
        return False
    return (
        F[T] == 1
        and F[T + 1] == 0
        and F[T + 2] == 0
        and F[T + 3] == 0
        and F[T + 4] == 1
    )


def certify_arithmetic():
    rows = []
    for T in range(8, 81, 2):
        n0 = nvars(T)
        e = 2
        n_clip = n0 + e
        R = sound_R(T, n_clip, "even_F")
        assert n0 == T // 2
        assert R == 3
        assert 2 * n_clip == T + 4
        rows.append({"T": T, "n0": n0, "n_clip": n_clip, "R": R})
    return {"n_T": len(rows), "ok": True}


def certify_fib(nlen=12, Tmin=5, Tmax=16):
    n_pat = 0
    n_ok = 0
    for u in fib_strings(nlen):
        kneed = Tmax + 6
        Fu, Gu = F_of_u(u, kneed)
        Su = shift_u(u)
        Fs, _ = F_of_u(Su, kneed)
        for T in range(Tmin, Tmax + 1):
            if not pattern_ok(Fu, T):
                continue
            n_pat += 1
            assert Gu[T] == 1
            assert Gu[T + 1] == 1
            assert Gu[T + 2] == 0
            assert Gu[T + 3] == 1
            assert Fs[T] == 0
            assert Fs[T + 1] == 1
            assert Fs[T + 2] == 0
            n_ok += 1
    assert n_pat > 0
    assert n_ok == n_pat
    return {
        "nlen": nlen,
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_pattern": n_pat,
        "n_germ": n_ok,
        "ok": True,
    }


def certify_ugap(Tmin=8, Tmax=32):
    n = 0
    n_germ = 0
    kinds = Counter()
    extra_S = Counter()
    for T in range(Tmin, Tmax + 1, 2):
        n0 = nvars(T)
        for u in ugap_strings(n0):
            rec = force(u, T)
            if rec is None or rec["stop"] != "even_F" or rec["extra"] != 2:
                continue
            n += 1
            kinds[rec["kind"]] += 1
            bits = rec["bits"]
            Fu, Gu = F_of_u(bits, T + 6)
            assert pattern_ok(Fu, T)
            assert rec["R"] == 3
            Su = shift_u(bits)
            Fs, _ = F_of_u(Su, T + 6)
            assert Fs[T] == 0
            assert Fs[T + 1] == 1
            assert Fs[T + 2] == 0
            n_germ += 1
            n0p = nvars(T + 1)
            pref = list(Su[:n0p]) if len(Su) >= n0p else list(Su) + [0] * (n0p - len(Su))
            rec2 = force(pref, T + 1)
            if rec2 is not None:
                extra_S[rec2["extra"]] += 1
    assert n > 0
    assert n_germ == n
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "n_evenF_e2": n,
        "n_isolated_at_Tplus1": n_germ,
        "src_kind": dict(kinds),
        "image_extra_when_onset": {str(k): v for k, v in sorted(extra_S.items())},
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    ar = certify_arithmetic()
    checks["even_T_e2_evenF_R_is_3"] = True
    fib = certify_fib()
    checks["fib_germ_isolated_at_Tplus1"] = True
    ug = certify_ugap(8, 32)
    checks["ugap_evenF_e2_all_isolated_at_Tplus1"] = True
    return {
        "checks": checks,
        "arithmetic": ar,
        "fib": fib,
        "ugap": ug,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("fib", report["fib"])
    print("ugap", {k: report["ugap"][k] for k in report["ugap"] if k != "ok"})
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
