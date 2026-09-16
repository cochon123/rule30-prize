#!/usr/bin/env python3
"""Q-forced extra to sound R, and T=37 attaining R=17.

A length-nvars(T) ugap prefix with F_T=1 has a unique attempted L_0
extension u_n=Q_n until a 11-clip, 00000-clip, or even F_{2n}>T.
That clip index n gives a sound extra-zero count
    R = 2n-T     (11 / 00000),
    R = 2n-1-T   (even F),
because F_{2n} does not depend on u_n and a ugap clip means no legal
bit realises F_{2n+1}=0. Hence extra<=E implies R<=2E+1. Through T=40
every ugap onset prefix has extra<=8, so R<=17 there, and T=37 attains
17. Not a prize claim: extra<=8 is a census, not a bound for all T.

Run: python3 research/period2_qextra.py --certify
Dump: research/period2_qextra.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_qshift import force_from
from period2_ugap_sat import ugap_strings, wstr
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T37_WORDS = [
    "000101010101010100100100101",
    "010101010101010100100100101",
    "100101010101010100100100101",
]


def sound_R(T: int, n_clip: int, stop: str) -> int:
    if stop == "even_F":
        return 2 * n_clip - 1 - T
    return 2 * n_clip - T


def r_cap(E: int, T: int) -> int:
    """Max sound R if extra<=E, from n0=nvars(T)."""
    n0 = nvars(T)
    n = n0 + E
    # 11-clip is the larger of the two
    return 2 * n - T


def scan_onsets(Tmin: int, Tmax: int, Emax: int = 32):
    rows = []
    for T in range(Tmin, Tmax + 1):
        if T == 4:
            rows.append(
                {
                    "T": T,
                    "n0": nvars(T),
                    "n_onset": 0,
                    "max_extra": None,
                    "max_sat_R": -1,
                    "n_at_maxR": 0,
                    "stop_at_maxR": None,
                    "kind_at_maxR": None,
                    "n_clip": None,
                    "sample": None,
                    "stops": {},
                    "max_extra_n": 0,
                }
            )
            continue
        n0 = nvars(T)
        strs = ugap_strings(n0)
        kneed = max(T + 2, 2 * n0 + 2)
        best_ex = -1
        n_ex = 0
        best_R = -1
        n_R = 0
        info = None
        stops = Counter()
        n_on = 0
        for u in strs:
            F0, _ = F_of_u(u, kneed)
            if F0[T] != 1:
                continue
            n_on += 1
            _bits, ev = force_from(u, T, n_max=n0 + Emax)
            stop = ev[-1].get("stop") if ev else "none"
            n_clip = ev[-1]["n"]
            ex = n_clip - n0
            R = sound_R(T, n_clip, stop)
            stops[stop] += 1
            kind = "bump" if T >= 1 and F0[T - 1] == 1 else "iso"
            if ex > best_ex:
                best_ex = ex
                n_ex = 1
            elif ex == best_ex:
                n_ex += 1
            if R > best_R:
                best_R = R
                n_R = 1
                info = {
                    "extra": ex,
                    "stop": stop,
                    "kind": kind,
                    "n_clip": n_clip,
                    "sample": wstr(u),
                }
            elif R == best_R:
                n_R += 1
        rec = {
            "T": T,
            "n0": n0,
            "n_onset": n_on,
            "max_extra": best_ex,
            "max_sat_R": best_R,
            "n_at_maxR": n_R,
            "stop_at_maxR": None if info is None else info["stop"],
            "kind_at_maxR": None if info is None else info["kind"],
            "n_clip": None if info is None else info["n_clip"],
            "sample": None if info is None else info["sample"],
            "stops": dict(stops),
            "max_extra_n": n_ex,
        }
        rows.append(rec)
        assert n_on == 0 or best_ex <= Emax
        if n_on:
            assert rec["max_sat_R"] == sound_R(T, rec["n_clip"], rec["stop_at_maxR"])
            assert rec["max_sat_R"] <= r_cap(best_ex, T)
    return rows


def certify_t37():
    T, R = 37, 17
    kmax = 60
    for word in T37_WORDS:
        u = [int(c) for c in word]
        F, _ = F_of_u(u, kmax)
        assert F[T] == 1 and F[T - 1] == 1
        assert all(F[T + d] == 0 for d in range(1, R + 1))
        assert F[T + R + 1] == 1
        n0 = nvars(T)
        _bits, ev = force_from(u[:n0], T, n_max=n0 + 16)
        assert ev[-1].get("stop") == "11"
        assert ev[-1]["n"] - n0 == 8
        assert sound_R(T, ev[-1]["n"], "11") == 17
    return {"n_R17": 3, "words": T37_WORDS}


def certify():
    t0 = time.perf_counter()
    checks: dict = {}

    # Arithmetic cap: extra<=8 => R<=17.
    for T in range(1, 41):
        if T == 4:
            continue
        cap = r_cap(8, T)
        n0 = nvars(T)
        # 11-clip at n0+8
        assert cap == 2 * (n0 + 8) - T
        if T % 2 == 0:
            assert cap == 16
        else:
            assert cap == 17
    checks["extra8_implies_R_le_17"] = True

    rows = scan_onsets(1, 40, 32)
    extras = [r["max_extra"] for r in rows if r["max_extra"] is not None]
    assert max(extras) == 8, max(extras)
    byT = {r["T"]: r for r in rows}
    assert byT[20]["max_sat_R"] == 16
    assert byT[20]["max_extra"] == 8
    assert byT[37]["max_sat_R"] == 17
    assert byT[37]["max_extra"] == 8
    assert byT[37]["stop_at_maxR"] == "11"
    assert byT[37]["kind_at_maxR"] == "bump"
    assert byT[37]["n_at_maxR"] == 3
    assert max(r["max_sat_R"] for r in rows) == 17
    assert [r["T"] for r in rows if r["max_sat_R"] == 17] == [37]
    for r in rows:
        if r["n_onset"]:
            assert r["max_extra"] <= 8
            assert r["max_sat_R"] <= 17
            assert set(r["stops"]).issubset({"11", "00000", "even_F"})
    checks["extra_le_8_through_40"] = True
    checks["t37_unique_maxR_17"] = True
    checks["t20_no_longer_unique_worst"] = True

    t37 = certify_t37()
    checks["t37_three_words_R17_clip11"] = True

    return {
        "checks": checks,
        "onset": rows,
        "t37": t37,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    for r in report["onset"]:
        print(
            f"  T={r['T']:2d} maxR={r['max_sat_R']:3d} extra={r['max_extra']} "
            f"n={r['n_at_maxR']} {r['stop_at_maxR']} {r['kind_at_maxR']} {r['sample']}"
        )
    print("t37 words", report["t37"]["n_R17"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
