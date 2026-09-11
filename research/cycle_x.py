#!/usr/bin/env python3
"""Cycle X: local coboundaries / currents for D(N), and ideas21.1 corollary.

Problem 2 is D(N)=sum_{t<N}(2c_t-1)=o(N). A finite-window coboundary
    2c_t-1 = φ(next window) - φ(current window)
would give D(N)=O(1) on every orbit, hence density 1/2. A bond flux
    2c_t-1 = Δφ + J_left - J_right
would rewrite D as a telescoping term plus a flux sum. This cycle
enumerates those linear identities on Rule 30 neighbourhoods (all
configurations, then the prize light cone). Not a prize claim unless
an identity holds and the remaining flux is proved o(N).

ideas21.1: infinitely many 0s in column -1 plus infinitely many 1s in
c do not force the spatial triple 010/011 (equivalently (c,l)=(1,0)).

Run: python3 research/cycle_x.py --certify
Dump: research/cycle_x.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def f(l: int, c: int, r: int) -> int:
    return l ^ (c | r)


def bits_of(mask: int, n: int) -> tuple[int, ...]:
    return tuple((mask >> (n - 1 - i)) & 1 for i in range(n))


def pack(bits) -> int:
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return v


def image(bits: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(f(bits[i], bits[i + 1], bits[i + 2]) for i in range(len(bits) - 2))


# ---------------------------------------------------------------------------
# Exact linear algebra over Q
# ---------------------------------------------------------------------------

def gauss(eqs: list[tuple[list[int], int]], nvars: int) -> dict:
    """Row-reduce eqs (coeff list, rhs) over Q. Report consistency and kernel."""
    if not eqs:
        return {
            "n_eq": 0,
            "nvars": nvars,
            "rank": 0,
            "consistent": True,
            "nullity": nvars,
            "particular": [0] * nvars,
        }
    # Dedup
    seen = set()
    rows: list[list[Fraction]] = []
    for coeff, rhs in eqs:
        key = tuple(coeff) + (rhs,)
        if key in seen:
            continue
        seen.add(key)
        rows.append([Fraction(c) for c in coeff] + [Fraction(rhs)])
    m = len(rows)
    w = nvars + 1
    lead_for_col = [-1] * nvars
    row = 0
    for col in range(nvars):
        piv = None
        for i in range(row, m):
            if rows[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[row], rows[piv] = rows[piv], rows[row]
        pivval = rows[row][col]
        for j in range(col, w):
            rows[row][j] /= pivval
        for i in range(m):
            if i == row or rows[i][col] == 0:
                continue
            fac = rows[i][col]
            for j in range(col, w):
                rows[i][j] -= fac * rows[row][j]
        lead_for_col[col] = row
        row += 1
        if row == m:
            break
    rank = row
    for i in range(rank, m):
        if rows[i][nvars] != 0:
            return {
                "n_eq": m,
                "nvars": nvars,
                "rank": rank,
                "consistent": False,
                "nullity": None,
                "particular": None,
                "obstruction_row": [str(rows[i][j]) for j in range(w)],
            }
    particular = [Fraction(0)] * nvars
    free = []
    for col in range(nvars):
        r = lead_for_col[col]
        if r == -1:
            free.append(col)
        else:
            particular[col] = rows[r][nvars]
    # Integer-clear a particular solution for the dump
    dens = [p.denominator for p in particular if p != 0]
    lcm = 1
    for d in dens:
        a, b = lcm, d
        while b:
            a, b = b, a % b
        lcm = lcm // a * d
    part_int = [int(p * lcm) for p in particular]
    return {
        "n_eq": m,
        "nvars": nvars,
        "rank": rank,
        "consistent": True,
        "nullity": nvars - rank,
        "n_free": len(free),
        "particular_int": part_int,
        "particular_scale": lcm,
        "max_abs_particular": max((abs(x) for x in part_int), default=0),
    }


def summarize_gauss(g: dict) -> dict:
    keep = (
        "n_eq",
        "nvars",
        "rank",
        "consistent",
        "nullity",
        "n_free",
        "max_abs_particular",
        "particular_scale",
    )
    out = {k: g.get(k) for k in keep}
    if not g["consistent"]:
        out["killed"] = True
    else:
        out["killed"] = False
    return out


# ---------------------------------------------------------------------------
# Identity families on all neighbourhoods
# ---------------------------------------------------------------------------

def eqs_phi_window(win: int, src: int, target: str, phased: bool = False):
    """φ on a centred `win`-window; source neighbourhood length src = win+2.

    target 's' means 2c-1, '2c' means 2c, 'e' means c + c' - 1 (pair current).
    cur window is the middle win bits of the source; next is image(source).
    """
    n_src = src
    n_phi = 1 << win
    off = (src - win) // 2
    eqs = []
    nvars = 2 * n_phi if phased else n_phi
    for mask in range(1 << n_src):
        bits = bits_of(mask, n_src)
        cur = pack(bits[off : off + win])
        nxt_bits = image(bits)
        assert len(nxt_bits) == win
        nxt = pack(nxt_bits)
        c = bits[src // 2]
        cp = nxt_bits[win // 2]
        if target == "s":
            rhs = 2 * c - 1
        elif target == "2c":
            rhs = 2 * c
        elif target == "e":
            rhs = c + cp - 1
        else:
            raise ValueError(target)
        coeff = [0] * nvars
        if phased:
            # φ_odd(next) - φ_even(cur) and the swapped phase: both must
            # equal rhs because the local rule is time-independent, so the
            # identity is imposed on both phases (vacuum then sums to -2).
            coeff[nxt] += 1
            coeff[cur] -= 1
            eqs.append((coeff, rhs))
            coeff2 = [0] * nvars
            coeff2[n_phi + nxt] += 1
            coeff2[n_phi + cur] -= 1
            eqs.append((coeff2, rhs))
        else:
            coeff[nxt] += 1
            coeff[cur] -= 1
            eqs.append((coeff, rhs))
    return eqs, nvars


def eqs_phi_flux(win: int, jwin: int, src: int, target: str, jmode: str):
    """φ on centred win-window plus bond flux J_left - J_right.

    jmode 'outer': J reads the leftmost / rightmost jwin bits of the source.
    jmode 'inner': J reads the left-justified / right-justified jwin bits
    that include the centre (so the two J-windows overlap on the centre).
    """
    n_phi = 1 << win
    n_j = 1 << jwin
    off = (src - win) // 2
    nvars = n_phi + n_j
    eqs = []
    for mask in range(1 << src):
        bits = bits_of(mask, src)
        cur = pack(bits[off : off + win])
        nxt_bits = image(bits)
        nxt = pack(nxt_bits)
        c = bits[src // 2]
        if target == "s":
            rhs = 2 * c - 1
        elif target == "2c":
            rhs = 2 * c
        elif target == "e":
            rhs = c + nxt_bits[win // 2] - 1
        else:
            raise ValueError(target)
        coeff = [0] * nvars
        coeff[nxt] += 1
        coeff[cur] -= 1
        if jmode == "outer":
            jl = pack(bits[:jwin])
            jr = pack(bits[src - jwin :])
        elif jmode == "inner":
            jl = pack(bits[:jwin])
            jr = pack(bits[src - jwin :])
        elif jmode == "overlap":
            # left jwin ending at centre inclusive; right jwin starting at centre
            mid = src // 2
            jl = pack(bits[mid - jwin + 1 : mid + 1])
            jr = pack(bits[mid : mid + jwin])
        else:
            raise ValueError(jmode)
        coeff[n_phi + jl] += 1
        coeff[n_phi + jr] -= 1
        eqs.append((coeff, rhs))
    return eqs, nvars


def vacuum_rhs_check() -> dict:
    """Direct 00000 evaluation of the three targets."""
    z = (0, 0, 0, 0, 0)
    nxt = image(z)
    c, cp = z[2], nxt[1]
    return {
        "next_is_vacuum": nxt == (0, 0, 0),
        "rhs_s": 2 * c - 1,
        "rhs_2c": 2 * c,
        "rhs_e": c + cp - 1,
        "delta_phi_vacuum": 0,
        "s_obstructed": (2 * c - 1) != 0,
        "e_obstructed": (c + cp - 1) != 0,
        "twoc_ok_on_vacuum": (2 * c) == 0,
    }


# ---------------------------------------------------------------------------
# Prize light cone
# ---------------------------------------------------------------------------

def prize_census(n: int) -> dict:
    """Spatial windows about the origin, D(t) by 3-window, (c,l) co-occurrence."""
    row = 1
    D = 0
    n3 = [0] * 8
    n5 = [0] * 32
    n7 = [0] * 128
    dmin = [10**9] * 8
    dmax = [-(10**9)] * 8
    dfirst = [None] * 8
    vacuum5_times = []
    vacuum3_times = []
    vacuum3_phase = [0, 0]
    lc_counts = [[0, 0], [0, 0]]  # lc_counts[c][l]
    n11_spatial = 0  # (c,l)=(1,0) i.e. 010 or 011
    last_11 = -1
    last_00 = -1
    prev_c = None
    max_spatial_zero_radius = 0
    zero_radius_unbounded_sample = []
    for t in range(n):
        def x(j: int) -> int:
            k = j + t
            if k < 0:
                return 0
            return (row >> k) & 1

        l, c, r = x(-1), x(0), x(1)
        trip = (l << 2) | (c << 1) | r
        n3[trip] += 1
        if dfirst[trip] is None:
            dfirst[trip] = D
        if D < dmin[trip]:
            dmin[trip] = D
        if D > dmax[trip]:
            dmax[trip] = D
        if l == 0 and c == 0 and r == 0:
            vacuum3_times.append(t)
            vacuum3_phase[t & 1] += 1
        quint = pack((x(-2), l, c, r, x(2)))
        n5[quint] += 1
        if quint == 0:
            vacuum5_times.append(t)
        sept = pack((x(-3), x(-2), l, c, r, x(2), x(3)))
        n7[sept] += 1
        lc_counts[c][l] += 1
        if c == 1 and l == 0:
            n11_spatial += 1
            last_11 = t
        if prev_c is not None:
            if prev_c == 1 and c == 1:
                last_11 = last_11  # already
            if prev_c == 0 and c == 0:
                last_00 = t - 1
        prev_c = c
        # largest r with [-r,r] all zeros
        rad = 0
        while rad <= t and x(-rad) == 0 and x(rad) == 0:
            rad += 1
        rad -= 1
        if rad > max_spatial_zero_radius:
            max_spatial_zero_radius = rad
            if len(zero_radius_unbounded_sample) < 8:
                zero_radius_unbounded_sample.append({"t": t, "radius": rad})
        D += 2 * c - 1
        row = rule30_step(row)

    # Consecutive vacuum-5 runs (a self-loop of the 5-window map on the orbit).
    vac5_runs = []
    run_start = None
    run_len = 0
    for t in vacuum5_times + [None]:
        if run_start is None:
            if t is None:
                break
            run_start, run_len = t, 1
            continue
        if t is not None and t == run_start + run_len:
            run_len += 1
            continue
        if run_len >= 2:
            vac5_runs.append({"start": run_start, "length": run_len})
        if t is None:
            break
        run_start, run_len = t, 1
    d_range = []
    for w in range(8):
        if n3[w] == 0:
            d_range.append({"w": format(w, "03b"), "count": 0, "range": None})
        else:
            d_range.append(
                {
                    "w": format(w, "03b"),
                    "count": n3[w],
                    "D_min": dmin[w],
                    "D_max": dmax[w],
                    "D_range": dmax[w] - dmin[w],
                    "D_first": dfirst[w],
                }
            )
    # A 3-window coboundary for 2c-1 forces D constant on each window.
    kill_phi3_by_D = any(row["count"] > 0 and row["D_range"] > 0 for row in d_range)
    appeared3 = sum(1 for v in n3 if v)
    appeared5 = sum(1 for v in n5 if v)
    appeared7 = sum(1 for v in n7 if v)
    return {
        "N": n,
        "D_N": D,
        "triples": {format(i, "03b"): n3[i] for i in range(8)},
        "n_triples": appeared3,
        "n_quints": appeared5,
        "n_septs": appeared7,
        "missing_quints": [format(i, "05b") for i, v in enumerate(n5) if v == 0],
        "n_vacuum3": len(vacuum3_times),
        "vacuum3_head": vacuum3_times[:12],
        "vacuum3_phase": {"even": vacuum3_phase[0], "odd": vacuum3_phase[1]},
        "n_vacuum5": len(vacuum5_times),
        "vacuum5_head": vacuum5_times[:12],
        "vacuum5_runs_len_ge2": vac5_runs[:12],
        "n_vacuum5_runs_len_ge2": len(vac5_runs),
        "longest_vacuum5_run": max((r["length"] for r in vac5_runs), default=0),
        "all_128_septs": appeared7 == 128,
        "max_spatial_zero_radius": max_spatial_zero_radius,
        "zero_radius_growth": zero_radius_unbounded_sample,
        "D_by_triple": d_range,
        "kill_phi3_D_not_window_fn": kill_phi3_by_D,
        "lc_counts": {
            "c0_l0": lc_counts[0][0],
            "c0_l1": lc_counts[0][1],
            "c1_l0": lc_counts[1][0],  # 11 in the centre
            "c1_l1": lc_counts[1][1],
        },
        "n_spatial_11": n11_spatial,
        "last_spatial_11": last_11,
        "last_temporal_00_pair": last_00,
        "all_8_triples": appeared3 == 8,
        "all_32_quints": appeared5 == 32,
    }


def prize_restricted_eqs(n: int, win: int, src: int, target: str, flux: bool, jwin: int = 2):
    """Same linear family, only on 5/7-windows that actually occur."""
    row = 1
    seen = set()
    eqs = []
    n_phi = 1 << win
    n_j = 1 << jwin
    nvars = n_phi + (n_j if flux else 0)
    off = (src - win) // 2
    for t in range(n):
        def x(j: int) -> int:
            k = j + t
            if k < 0:
                return 0
            return (row >> k) & 1

        half = src // 2
        bits = tuple(x(j) for j in range(-half, half + 1))
        key = bits
        if key not in seen:
            seen.add(key)
            cur = pack(bits[off : off + win])
            nxt_bits = image(bits)
            nxt = pack(nxt_bits)
            c = bits[half]
            if target == "s":
                rhs = 2 * c - 1
            elif target == "2c":
                rhs = 2 * c
            else:
                rhs = c + nxt_bits[win // 2] - 1
            coeff = [0] * nvars
            coeff[nxt] += 1
            coeff[cur] -= 1
            if flux:
                jl = pack(bits[:jwin])
                jr = pack(bits[src - jwin :])
                coeff[n_phi + jl] += 1
                coeff[n_phi + jr] -= 1
            eqs.append((coeff, rhs))
        row = rule30_step(row)
    return eqs, nvars, len(seen)


def period2_avoids_spatial_11() -> dict:
    """On phase 01, (c,l)=(1,0) never occurs after onset.

    even t: c=0, l=1-u; odd t: c=1, l=1. The pair (c,l)=(1,0) is empty.
    Compatible with infinitely many 0s in column -1 (even times, when u=1)
    and infinitely many 1s in c (odd times). Certified as a finite table
    of the local assignments, not an orbit claim.
    """
    rows = []
    for u in (0, 1):
        rows.append(
            {
                "phase": "even",
                "u": u,
                "c": 0,
                "l": 1 - u,
                "r": u,
                "triple": f"{1 - u}0{u}",
                "is_spatial_11": False,
            }
        )
    for r in (0, 1):
        rows.append(
            {
                "phase": "odd",
                "u": None,
                "c": 1,
                "l": 1,
                "r": r,
                "triple": f"11{r}",
                "is_spatial_11": False,
            }
        )
    # Contrast: (c,l)=(1,0) is exactly the centre-11 production.
    return {
        "assignments": rows,
        "any_spatial_11": any(r["is_spatial_11"] for r in rows),
        "compatible_with_inf_zeros_of_l": True,
        "compatible_with_inf_ones_of_c": True,
        "ideas21_is_reduction": False,
    }


def self_checks(c20) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    z = image((0, 0, 0, 0, 0))
    assert z == (0, 0, 0)
    # Packed centre at t: bit t of row is x(t,0)
    row = 1
    for t in range(20):
        assert ((row >> t) & 1) == c20[t]
        row = rule30_step(row)
    # Identity image length
    assert len(image((1, 0, 1, 1, 0, 0, 1))) == 5
    vac = vacuum_rhs_check()
    assert vac["s_obstructed"] and vac["e_obstructed"] and vac["twoc_ok_on_vacuum"]
    p2 = period2_avoids_spatial_11()
    assert p2["any_spatial_11"] is False
    # Consecutive vacuum 5-windows on a tiny prefix (t=156..158).
    tiny = prize_census(200)
    assert tiny["n_vacuum5"] >= 3
    assert tiny["longest_vacuum5_run"] >= 3
    return {"all_ok": True}


def run_family(name: str, eqs, nvars, **extra) -> dict:
    g = gauss(eqs, nvars)
    rec = {"name": name, **summarize_gauss(g), **extra}
    rec["verdict"] = "CONSISTENT" if g["consistent"] else "KILLED"
    if g["consistent"] and g.get("particular_int") is not None:
        rec["particular_head"] = g["particular_int"][:16]
    return rec


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 14)
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    checks = self_checks(c20)

    vac = vacuum_rhs_check()
    p2 = period2_avoids_spatial_11()

    families = []
    # Universal coboundaries (all neighbourhoods)
    for target, tag in (("s", "2c-1"), ("2c", "2c"), ("e", "pair")):
        eqs, nv = eqs_phi_window(3, 5, target)
        families.append(run_family(f"phi3_{tag}", eqs, nv, target=tag, win=3))
        eqs, nv = eqs_phi_window(5, 7, target)
        families.append(run_family(f"phi5_{tag}", eqs, nv, target=tag, win=5))
        eqs, nv = eqs_phi_window(3, 5, target, phased=True)
        families.append(run_family(f"phi3_phase2_{tag}", eqs, nv, target=tag, phased=True))

    # Flux families
    for target, tag in (("s", "2c-1"), ("2c", "2c"), ("e", "pair")):
        eqs, nv = eqs_phi_flux(3, 2, 5, target, "outer")
        families.append(run_family(f"phi3_J2outer_{tag}", eqs, nv, target=tag, flux="outer2"))
        eqs, nv = eqs_phi_flux(3, 3, 5, target, "overlap")
        families.append(run_family(f"phi3_J3overlap_{tag}", eqs, nv, target=tag, flux="overlap3"))
        eqs, nv = eqs_phi_flux(5, 3, 7, target, "outer")
        families.append(run_family(f"phi5_J3outer_{tag}", eqs, nv, target=tag, flux="outer3"))
        eqs, nv = eqs_phi_flux(5, 4, 7, target, "outer")
        families.append(run_family(f"phi5_J4outer_{tag}", eqs, nv, target=tag, flux="outer4"))

    census = prize_census(args.bits)

    restricted = []
    for target, tag in (("s", "2c-1"), ("2c", "2c")):
        eqs, nv, nseen = prize_restricted_eqs(args.bits, 3, 5, target, False)
        restricted.append(
            run_family(f"orbit_phi3_{tag}", eqs, nv, target=tag, n_windows=nseen)
        )
        eqs, nv, nseen = prize_restricted_eqs(args.bits, 3, 5, target, True, jwin=2)
        restricted.append(
            run_family(f"orbit_phi3_J2_{tag}", eqs, nv, target=tag, n_windows=nseen)
        )
        eqs, nv, nseen = prize_restricted_eqs(args.bits, 5, 7, target, False)
        restricted.append(
            run_family(f"orbit_phi5_{tag}", eqs, nv, target=tag, n_windows=nseen)
        )
        eqs, nv, nseen = prize_restricted_eqs(args.bits, 5, 7, target, True, jwin=3)
        restricted.append(
            run_family(f"orbit_phi5_J3_{tag}", eqs, nv, target=tag, n_windows=nseen)
        )

    killed_univ = [
        f["name"]
        for f in families
        if f["verdict"] == "KILLED" and "2c-1" in f["name"]
    ]
    consistent_univ = [f["name"] for f in families if f["verdict"] == "CONSISTENT"]
    killed_orbit = [f["name"] for f in restricted if f["verdict"] == "KILLED"]
    consistent_orbit = [f["name"] for f in restricted if f["verdict"] == "CONSISTENT"]

    # Lemma flags
    lemmas = {
        "vacuum_kills_universal_2c_minus_1": vac["s_obstructed"],
        "vacuum_kills_universal_pair_current": vac["e_obstructed"],
        "vacuum_allows_2c": vac["twoc_ok_on_vacuum"],
        "phase2_vacuum_sum": "0=-2 on two vacuum steps for 2c-1",
        "infinitely_many_ones_kill_bounded_2c_coboundary": True,
        "ideas21_1_not_a_reduction": (not p2["ideas21_is_reduction"]),
        "D_not_a_3window_function_on_prefix": census["kill_phi3_D_not_window_fn"],
        "prize_visits_consecutive_vacuum5": census["longest_vacuum5_run"] >= 3,
        "prize_spatial_7_is_full_shift_on_prefix": census.get(
            "all_128_septs", census["n_septs"] == 128
        ),
    }

    dump = {
        "cycle": "X",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "vacuum": vac,
        "period2_avoidance": p2,
        "families": families,
        "census": census,
        "restricted": restricted,
        "lemmas": lemmas,
        "verdict": {
            "universal_2c-1": "KILLED",
            "universal_pair": "KILLED",
            "n_universal_consistent": len(consistent_univ),
            "universal_consistent": consistent_univ,
            "n_universal_killed": sum(1 for f in families if f["verdict"] == "KILLED"),
            "orbit_killed": killed_orbit,
            "orbit_consistent": consistent_orbit,
            "ideas21_1": "KILLED_AS_REDUCTION",
            "consecutive_vacuum5": census["longest_vacuum5_run"],
            "spatial_7_full": census.get("all_128_septs", census["n_septs"] == 128),
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("vacuum", vac)
    print("lemmas", lemmas)
    print("triples", census["triples"], "D_N", census["D_N"])
    print(
        "vacuum3",
        census["n_vacuum3"],
        "vacuum5",
        census["n_vacuum5"],
        "vac5_run",
        census["longest_vacuum5_run"],
        "max_zero_r",
        census["max_spatial_zero_radius"],
        "septs",
        census["n_septs"],
    )
    print("D_by_triple", census["D_by_triple"])
    print("lc", census["lc_counts"], "spatial11", census["n_spatial_11"])
    print("consistent_univ", consistent_univ)
    print("consistent_orbit", consistent_orbit)
    print("killed_orbit", killed_orbit)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
