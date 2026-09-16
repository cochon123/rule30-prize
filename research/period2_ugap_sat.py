#!/usr/bin/env python3
"""Ugap onset table: Fibonacci last-sat overcounts, R=16 still lives.

Genuine period-2 even-right u lies in the SFT forbidding {11, 00000}
(research/period2_ugap.md). The L_0 onset scan of
research/period2_certificate.py enumerates all Fibonacci strings, so
last-sat words may contain five consecutive zeros. Restricting to ugap
does not kill the worst onset: three of the six T=20 R=16 words are
legal and still last-sat. Isolated ugap maxR is 9 through T=32 and
already 14 at T=33. Q-forced extra is <=8 through T=36. Not a prize
claim.

Run: python3 research/period2_ugap_sat.py --certify
Dump: research/period2_ugap_sat.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_lead import T20_WORDS
from period2_qshift import force_from
from period2_vacuum import F_of_u, fib_strings, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def max_zero_run(u):
    z = mx = 0
    for b in u:
        if b == 0:
            z += 1
            if z > mx:
                mx = z
        else:
            z = 0
    return mx


def ugap_ok(u):
    return max_zero_run(u) <= 4


def ugap_strings(length: int):
    """Fibonacci words with no five consecutive zeros (one-sided ugap)."""
    out = []

    def rec(pos, last, zrun, acc):
        if pos == length:
            out.append(acc)
            return
        if zrun < 4:
            rec(pos + 1, 0, zrun + 1, acc + [0])
        if last == 0:
            rec(pos + 1, 1, 0, acc + [1])

    rec(0, 0, 0, [])
    return out


def wstr(u):
    return "".join(map(str, u))


def is_bump(F, T: int) -> bool:
    return T >= 1 and F[T - 1] == 1


def onset_scan(generator, Tmin: int, Tmax: int, Rmax: int = 20):
    cache = {}
    rows = []
    for T in range(Tmin, Tmax + 1):
        maxR = -1
        nmax = 0
        last = []
        killed = None
        iso_max = -1
        bump_max = -1
        iso_n = 0
        bump_n = 0
        for R in range(0, Rmax + 1):
            top = T + R
            L = max(nvars(top), 1)
            K = top
            if L not in cache or cache[L][0] < K:
                strs = generator(L)
                kneed = max(K, 2 * L + 2)
                cache[L] = (kneed, strs, [F_of_u(u, kneed)[0] for u in strs])
            strs, rowsF = cache[L][1], cache[L][2]
            mods = []
            n_iso = n_bump = 0
            for u, F in zip(strs, rowsF):
                if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
                    mods.append((u, F))
                    if is_bump(F, T):
                        n_bump += 1
                    else:
                        n_iso += 1
            if mods:
                maxR = R
                nmax = len(mods)
                last = mods
                if n_iso:
                    iso_max, iso_n = R, n_iso
                if n_bump:
                    bump_max, bump_n = R, n_bump
            else:
                killed = top
                break
        kinds = Counter("bump" if is_bump(F, T) else "iso" for _, F in last)
        zruns = [max_zero_run(u) for u, _ in last]
        rows.append(
            {
                "T": T,
                "max_sat_R": maxR,
                "n_at_max": nmax,
                "killed_by": killed,
                "kinds": dict(kinds),
                "iso_maxR": iso_max,
                "iso_n_at_iso_max": iso_n,
                "bump_maxR": bump_max,
                "bump_n_at_bump_max": bump_n,
                "max_zero_run": max(zruns) if zruns else None,
                "n_gap_illegal": sum(1 for z in zruns if z > 4),
                "samples": [wstr(u) for u, _ in last[:6]],
            }
        )
        assert killed is not None or maxR == Rmax
    return rows


def t20_gap_split():
    rows = []
    for u in T20_WORDS:
        z = max_zero_run(u)
        rows.append({"u": wstr(u), "max_zero_run": z, "ugap": z <= 4})
    return rows


def last_sat_models(generator, T: int, R: int):
    L = max(nvars(T + R), 1)
    kmax = max(T + R + 8, 2 * L + 4)
    out = []
    for u in generator(L):
        F, _ = F_of_u(u, kmax)
        if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
            out.append(u)
    return out


def qforce_rows(pairs):
    rows = []
    for T, R in pairs:
        mods = last_sat_models(ugap_strings, T, R)
        n0 = nvars(T)
        stops = Counter()
        extras = []
        for u in mods:
            _bits, ev = force_from(u[:n0], T, n_max=n0 + 48)
            stop = ev[-1].get("stop") if ev else "none"
            stops[stop] += 1
            extras.append(ev[-1]["n"] - n0 if ev else None)
        rows.append(
            {
                "T": T,
                "R": R,
                "n_models": len(mods),
                "n0": n0,
                "force_stops": dict(stops),
                "force_extras": extras,
                "samples": [wstr(u) for u in mods[:4]],
            }
        )
    return rows


def compact(rows):
    return [
        {
            "T": r["T"],
            "maxR": r["max_sat_R"],
            "n": r["n_at_max"],
            "killed": r["killed_by"],
            "iso": r["iso_maxR"],
            "bump": r["bump_maxR"],
            "maxz": r["max_zero_run"],
            "illegal": r["n_gap_illegal"],
        }
        for r in rows
    ]


def certify():
    t0 = time.perf_counter()
    checks: dict = {}

    split = t20_gap_split()
    n_legal = sum(1 for r in split if r["ugap"])
    n_illegal = sum(1 for r in split if not r["ugap"])
    assert n_legal == 3 and n_illegal == 3, split
    checks["t20_three_of_six_ugap"] = True
    legal_words = [r["u"] for r in split if r["ugap"]]
    assert legal_words == [
        "001000010010010001",
        "010100010010010001",
        "101000010010010001",
    ]

    for L in range(1, 13):
        U = ugap_strings(L)
        F = fib_strings(L)
        assert all(ugap_ok(u) and not any(u[i] and u[i + 1] for i in range(len(u) - 1)) for u in U)
        assert len(U) <= len(F)
        fib_set = {tuple(u) for u in F}
        assert all(tuple(u) in fib_set for u in U)

    ugap_rows = onset_scan(ugap_strings, 1, 36, 20)
    fib_tail = onset_scan(fib_strings, 23, 32, 20)

    byT = {r["T"]: r for r in ugap_rows}
    assert byT[4]["max_sat_R"] < 0
    assert byT[20]["max_sat_R"] == 16
    assert byT[20]["n_at_max"] == 3
    assert byT[20]["kinds"] == {"bump": 3}
    assert byT[20]["n_gap_illegal"] == 0
    assert byT[22]["max_sat_R"] == 12
    assert byT[26]["max_sat_R"] == 11
    assert byT[32]["max_sat_R"] == 8
    assert byT[33]["iso_maxR"] == 14
    assert byT[33]["max_sat_R"] == 14
    assert byT[35]["iso_maxR"] == 14
    for r in ugap_rows:
        assert r["n_gap_illegal"] == 0
        if r["T"] <= 32 and r["max_sat_R"] >= 12:
            assert r["kinds"].get("iso", 0) == 0, r
    checks["t20_r16_survives_ugap"] = True
    checks["r_ge_12_all_bumps_through_32"] = True
    checks["t33_iso_maxR_14"] = True

    iso_through_32 = max(r["iso_maxR"] for r in ugap_rows if r["T"] <= 32)
    assert iso_through_32 == 9
    iso_attained = [r["T"] for r in ugap_rows if r["T"] <= 32 and r["iso_maxR"] == 9]
    assert iso_attained == [8, 16], iso_attained
    checks["iso_maxR_9_through_32"] = True
    iso_global = max(r["iso_maxR"] for r in ugap_rows)
    assert iso_global == 14

    bump_max = max(r["bump_maxR"] for r in ugap_rows)
    assert bump_max == 16
    assert [r["T"] for r in ugap_rows if r["max_sat_R"] == 16] == [20]
    checks["ugap_global_maxR_16_unique_T20"] = True

    fib_byT = {r["T"]: r for r in fib_tail}
    assert fib_byT[26]["max_sat_R"] == 11
    assert fib_byT[32]["max_sat_R"] == 13
    assert fib_byT[32]["n_gap_illegal"] == fib_byT[32]["n_at_max"]
    assert fib_byT[25]["n_gap_illegal"] == fib_byT[25]["n_at_max"]
    checks["t26_fib_maxR_11_not_5"] = True
    checks["t32_fib_last_sat_all_illegal"] = True

    for r in ugap_rows:
        if r["T"] in fib_byT:
            assert r["max_sat_R"] <= fib_byT[r["T"]]["max_sat_R"]

    long_pairs = [
        (r["T"], r["max_sat_R"])
        for r in ugap_rows
        if r["max_sat_R"] >= 8
    ]
    qrows = qforce_rows(long_pairs)
    q_byT = {r["T"]: r for r in qrows}
    assert q_byT[20]["force_stops"] == {"11": 3}
    assert q_byT[20]["force_extras"] == [8, 8, 8]
    assert q_byT[22]["force_stops"] == {"11": 5}
    assert set(q_byT[22]["force_extras"]) == {6}
    assert q_byT[26]["force_stops"] == {"even_F": 4}
    assert q_byT[33]["force_stops"] == {"even_F": 3}
    assert set(q_byT[33]["force_extras"]) == {7}
    extras = [x for r in qrows for x in r["force_extras"]]
    assert max(extras) == 8
    for r in qrows:
        assert set(r["force_stops"]).issubset({"11", "00000", "even_F"})
        assert r["n_models"] > 0
    checks["t20_ugap_11clip_extra_8"] = True
    checks["qforce_extra_le_8_through_36"] = True

    return {
        "checks": checks,
        "t20_words": split,
        "ugap_onset": ugap_rows,
        "fib_onset_23_32": fib_tail,
        "ugap_compact": compact(ugap_rows),
        "fib_compact_23_32": compact(fib_tail),
        "qforce": qrows,
        "iso_maxR_through_32": iso_through_32,
        "iso_maxR": iso_global,
        "bump_maxR": bump_max,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("iso_maxR_32", report["iso_maxR_through_32"], "iso_maxR", report["iso_maxR"], "bump_maxR", report["bump_maxR"])
    print("t20", report["t20_words"])
    for row in report["ugap_compact"]:
        print(
            f"  ugap T={row['T']:2d} maxR={row['maxR']:3d} n={row['n']:3d} "
            f"iso={row['iso']:2d} bump={row['bump']:2d} killed={row['killed']}"
        )
    for row in report["qforce"]:
        print(f"  Q T={row['T']} R={row['R']} stops={row['force_stops']} extras={row['force_extras']}")
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
