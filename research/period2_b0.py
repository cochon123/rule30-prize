#!/usr/bin/env python3
"""L_0 to B_0 tail, and S: B_0(S,R) -> B_0(S+2, R-4).

A long L_0 onset is a single 1 then zeros. Under S it becomes a
length-2 bump (germ), and the zeros after the bump last R-4 columns.
That bump B_0 (F_S=F_{S+1}=1, then zeros) has G_S=0, G_{S+1}=G_{S+2}=1,
and S sends it to B_0 at S+2 with four fewer zeros. Finite R therefore
descends under S once it is a bump; infinite L_0 still maps to infinite
B_0 at larger S. Isolated L_0 (F_{T-1}=0) has maxR<=9 through T=22;
every last-sat with R>=12 is a bump. Not a prize claim: no uniform R.

Run: python3 research/period2_b0.py --certify
Dump: research/period2_b0.json
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
from period2_qshift import shift_u
from period2_vacuum import F_of_u, fib_strings, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

LAST_SAT = [
    (8, 9),
    (15, 6),
    (16, 9),
    (20, 16),
    (22, 12),
    (26, 5),
]


def zeros_after(F, start: int) -> int:
    z = 0
    j = start
    while j < len(F) and F[j] == 0:
        z += 1
        j += 1
    return z


def is_b0(F, S: int, R: int) -> bool:
    if S + 1 + R >= len(F):
        return False
    return (
        F[S] == 1
        and F[S + 1] == 1
        and all(F[S + 1 + d] == 0 for d in range(1, R + 1))
    )


def survivors_l0(T: int, R: int):
    top = T + R
    L = max(nvars(top), 1)
    kmax = max(top + 8, 2 * L + 4)
    out = []
    for u in fib_strings(L):
        F, G = F_of_u(u, kmax)
        if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
            out.append((u, F, G, kmax))
    return out


def g_pattern_b0(G, S: int) -> tuple[int, int, int]:
    return G[S], G[S + 1], G[S + 2]


def certify_g_pattern(L: int = 12) -> dict:
    n = 0
    n_fail = 0
    fail_ex = []
    kmax = 2 * L + 6
    for u in fib_strings(L):
        F, G = F_of_u(u, kmax)
        for S in range(1, kmax - 4):
            if F[S] == 1 and F[S + 1] == 1 and F[S + 2] == 0:
                n += 1
                if G[S] != 0:
                    n_fail += 1
                    if len(fail_ex) < 3:
                        fail_ex.append({"S": S, "u": u[:16], "G_S": G[S]})
                if S + 3 < len(F) and F[S + 3] == 0:
                    if G[S + 1] != 1 or G[S + 2] != 1:
                        n_fail += 1
                        if len(fail_ex) < 3:
                            fail_ex.append(
                                {"S": S, "u": u[:16], "G": [G[S], G[S + 1], G[S + 2]]}
                            )
    return {"n": n, "n_fail": n_fail, "fail_ex": fail_ex}


def certify_l0_to_b0() -> dict:
    rows = []
    for T, R in LAST_SAT:
        mods = survivors_l0(T, R)
        n_ok = 0
        n_fail = 0
        prev = Counter()
        for u, F, G, kmax in mods:
            prev[F[T - 1] if T >= 1 else None] += 1
            FS, GS = F_of_u(shift_u(u), kmax)
            bump = FS[T] == 0 and FS[T + 1] == 1 and FS[T + 2] == 1
            z = zeros_after(FS, T + 3)
            want = R - 4
            ok = bump and z >= want
            n_ok += int(ok)
            n_fail += int(not ok)
        rows.append(
            {
                "T": T,
                "R": R,
                "n_models": len(mods),
                "n_ok": n_ok,
                "n_fail": n_fail,
                "want_Rprime": R - 4,
                "F_Tminus1": dict(prev),
            }
        )
        assert n_fail == 0 and n_ok == len(mods) > 0, rows[-1]
    return rows


def certify_b0_to_b0() -> dict:
    """S sends last-sat B_0 (the T=20 / S=19 six words) to B_0 at S+2 with R-4."""
    S, R = 19, 16
    rows = []
    for i, u in enumerate(T20_WORDS):
        F, G = F_of_u(u, S + 1 + R + 8)
        assert is_b0(F, S, R), (i, "not B0")
        assert g_pattern_b0(G, S) == (0, 1, 1)
        FS, GS = F_of_u(shift_u(u), S + 1 + R + 8)
        ok = (
            FS[S + 1] == 0
            and is_b0(FS, S + 2, R - 4)
            and g_pattern_b0(GS, S + 2) == (0, 1, 1)
        )
        z = zeros_after(FS, S + 4)
        rows.append({"i": i, "ok": ok, "z_after_S+4": z, "want": R - 4})
        assert ok and z >= R - 4
    return rows


def certify_iso_bump_split(Tmax: int = 22, Rmax: int = 18) -> dict:
    cache: dict = {}
    rows = []
    worst_iso = -1
    worst_bump = -1
    for T in range(5, Tmax + 1):
        iso_max = -1
        bump_max = -1
        for R in range(0, Rmax + 1):
            top = T + R
            L = max(nvars(top), 1)
            kneed = max(top, 2 * L + 2)
            if L not in cache or cache[L][0] < kneed:
                strs = fib_strings(L)
                cache[L] = (kneed, strs, [F_of_u(u, kneed)[0] for u in strs])
            n_iso = n_bump = 0
            for u, F in zip(cache[L][1], cache[L][2]):
                if T >= len(F) or F[T] != 1:
                    continue
                if any(T + d >= len(F) for d in range(1, R + 1)):
                    continue
                if not all(F[T + d] == 0 for d in range(1, R + 1)):
                    continue
                if T >= 1 and F[T - 1] == 1:
                    n_bump += 1
                else:
                    n_iso += 1
            if n_iso:
                iso_max = R
            if n_bump:
                bump_max = R
            if n_iso == 0 and n_bump == 0:
                break
        worst_iso = max(worst_iso, iso_max)
        worst_bump = max(worst_bump, bump_max)
        rows.append({"T": T, "iso_maxR": iso_max, "bump_maxR": bump_max})
    return {
        "Tmax": Tmax,
        "worst_iso": worst_iso,
        "worst_bump": worst_bump,
        "rows": rows,
    }


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict = {}

    gp = certify_g_pattern(12)
    checks["g_pattern_fib12"] = gp["n_fail"] == 0 and gp["n"] > 0
    assert checks["g_pattern_fib12"], gp

    l0 = certify_l0_to_b0()
    checks["l0_to_b0_last_sat"] = all(r["n_fail"] == 0 for r in l0)
    assert checks["l0_to_b0_last_sat"]

    b0 = certify_b0_to_b0()
    checks["b0_S19_to_S21"] = all(r["ok"] for r in b0)
    assert checks["b0_S19_to_S21"]

    split = certify_iso_bump_split(22, 18)
    checks["iso_maxR_le_9_Tle22"] = split["worst_iso"] <= 9
    checks["bump_is_worst"] = split["worst_bump"] >= 16
    checks["all_R_ge_12_are_bump"] = all(
        r["iso_maxR"] < 12 for r in split["rows"]
    )
    assert checks["iso_maxR_le_9_Tle22"]
    assert checks["bump_is_worst"]
    assert checks["all_R_ge_12_are_bump"]

    checks["all_ok"] = True
    wall = time.perf_counter() - t0
    dump = {
        "attack": "period2_b0",
        "problem": "L_0 to B_0 tail and S-descent of the 11-bump",
        "verdict": "LEMMA",
        "kill": False,
        "survive": False,
        "prize": False,
        "kill_reason": (
            "Long L_0 becomes B_0 under S with R-4 zeros after the bump; "
            "S then sends B_0(S,R) to B_0(S+2,R-4) with G_S=0. Finite R "
            "descends; infinite L_0 still yields infinite B_0 at larger S. "
            "Isolated L_0 has maxR<=9 through T=22. Not a uniform R."
        ),
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "g_pattern": {"n": gp["n"], "n_fail": gp["n_fail"]},
        "l0_to_b0": l0,
        "b0_S19": b0,
        "iso_bump": {
            "Tmax": split["Tmax"],
            "worst_iso": split["worst_iso"],
            "worst_bump": split["worst_bump"],
            "rows": split["rows"],
        },
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(
        f"verdict=LEMMA wall={wall:.3f}s iso={split['worst_iso']} "
        f"bump={split['worst_bump']} g_n={gp['n']}"
    )
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
