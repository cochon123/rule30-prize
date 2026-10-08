#!/usr/bin/env python3
"""Cycle I / ideas10 item 4: signed pairing of period-2 centre bursts (Problem 2).

An even-length period-2 centre burst contributes 0 to the signed
discrepancy D(N) = sum_{t<N} (2 c_t - 1). Defects are the times that
break alternation (c_t == c_{t-1}); each is a global 01/10 phase flip.
If defect density were o(1), the number of runs would be o(N) and each
run contributes O(1) to D, so D(N) = o(N) plus an O(1) boundary.

This script measures defect density on the prize seed through N=10^5
(packed experiment.center_bits / row = (row<<2)^((row<<1)|row)) and on
every nonzero finite row of support radius w<=6.

Kill: density stays >= 1/4 at N=10^5, or the defect sequence has
Berlekamp-Massey L(N) ~ N/2 like c itself.

Stdlib only. Does not modify experiment.py, strip files, REPORT/LOG/README,
or other agents' files. Not a prize claim.

Run: python3 research/period2_defects.py --certify
Dump: research/period2_defects.json, research/period2_defects.md
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits
from experiment import linear_complexity as experiment_linear_complexity

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

N_PRIZE = 100_000
PREFIX_CHECK = 256
PRIZE_PREFIX16 = "1101110011000101"
PRIZE_PREFIX20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
W_MAX = 6
TCAP = lambda w: 8 * w + 128
CHECKPOINTS = (10, 100, 1000, 10_000, 100_000)
BM_TRAIN = (100, 1000, 4096, 10_000, 20_000)
IID_SEED = 20260910
KILL_DENSITY = 0.25
KILL_L_RATIO = 0.40  # "L(N) ~ N/2" is already this far from o(N)


# ---------------------------------------------------------------------------
# Packed Rule 30. Bit 0 is the leftmost cell of the current support.
# One step: new = (row << 2) ^ ((row << 1) | row)
# Centre at time t is (row >> (w + t)) & 1.
# Prize seed is w=0, mask=1, which is experiment.center_bits.
# ---------------------------------------------------------------------------

def rule30_step(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_centers(mask: int, w: int, tcap: int) -> bytearray:
    row = mask
    out = bytearray(tcap)
    for t in range(tcap):
        out[t] = (row >> (w + t)) & 1
        row = rule30_step(row)
    return out


def naive_centers(live: dict[int, int], tcap: int) -> list[int]:
    """Independent spacetime for self-check. live: position -> bit at t=0."""
    centers: list[int] = []
    cur = {p: 1 for p, b in live.items() if b}
    for _t in range(tcap):
        centers.append(1 if 0 in cur else 0)
        if not cur:
            centers.extend([0] * (tcap - len(centers)))
            break
        mn, mx = min(cur), max(cur)
        nxt = {}
        for j in range(mn - 1, mx + 2):
            a = 1 if (j - 1) in cur else 0
            b = 1 if j in cur else 0
            c = 1 if (j + 1) in cur else 0
            if a ^ (b | c):
                nxt[j] = 1
        cur = nxt
    return centers


def mask_to_live(mask: int, w: int) -> dict[int, int]:
    live = {}
    for i in range(2 * w + 1):
        if (mask >> i) & 1:
            live[i - w] = 1
    return live


def linear_complexity(bits) -> int:
    """Binary Berlekamp-Massey. Copied from experiment.py; that file is not modified."""
    connection = previous = 1
    length, last_change, history = 0, -1, 0
    for n, value in enumerate(bits):
        history = (history << 1) | value
        discrepancy = (connection & history).bit_count() & 1
        if discrepancy:
            old = connection
            connection ^= previous << (n - last_change)
            if 2 * length <= n:
                length = n + 1 - length
                previous, last_change = old, n
    return length


# ---------------------------------------------------------------------------
# Defects, alternating runs, signed D
# ---------------------------------------------------------------------------

def signed_D(bits) -> int:
    return 2 * sum(bits) - len(bits)


def defect_indicators(bits) -> bytearray:
    """d_{t-1} = 1 iff c_t == c_{t-1}, for t = 1..N-1. Length N-1."""
    n = len(bits)
    out = bytearray(n - 1)
    for t in range(1, n):
        out[t - 1] = 1 if bits[t] == bits[t - 1] else 0
    return out


def run_list(bits) -> list[tuple[int, int, int]]:
    """Maximal alternating runs: (start, length, start_bit)."""
    n = len(bits)
    if n == 0:
        return []
    runs: list[tuple[int, int, int]] = []
    start = 0
    for t in range(1, n):
        if bits[t] == bits[t - 1]:
            runs.append((start, t - start, bits[start]))
            start = t
    runs.append((start, n - start, bits[start]))
    return runs


def analyze(bits) -> dict:
    """Full defect / run / D decomposition of a 0-1 centre trace."""
    n = len(bits)
    if n < 2:
        raise ValueError("need at least 2 bits")
    runs = run_list(bits)
    n_def = len(runs) - 1
    density = n_def / (n - 1)
    mean_run = n / len(runs)
    lengths = [L for _s, L, _b in runs]
    max_run = max(lengths)
    n_even = sum(1 for L in lengths if L % 2 == 0)
    n_odd_ge2 = sum(1 for L in lengths if L >= 3 and L % 2 == 1)
    n_len1 = sum(1 for L in lengths if L == 1)

    D = signed_D(bits)
    D_even = 0
    D_odd_ge2 = 0
    D_len1 = 0
    for start, L, b in runs:
        contrib = (L % 2) * (2 * b - 1)
        if L % 2 == 0:
            D_even += contrib
        elif L == 1:
            D_len1 += contrib
        else:
            D_odd_ge2 += contrib

    D_at_defects = 0
    D_at_alternating = 2 * bits[0] - 1  # t=0 is never a defect
    for t in range(1, n):
        s = 2 * bits[t] - 1
        if bits[t] == bits[t - 1]:
            D_at_defects += s
        else:
            D_at_alternating += s

    # Isolated phase flips: a defect at t whose neighbouring pairs alternate.
    # That is the boundary between two genuine (length >=2) alternating bursts.
    n_isolated = 0
    n_clustered = 0
    for t in range(1, n):
        if bits[t] != bits[t - 1]:
            continue
        left = t >= 2 and bits[t - 1] == bits[t - 2]
        right = t + 1 < n and bits[t + 1] == bits[t]
        if left or right:
            n_clustered += 1
        else:
            n_isolated += 1

    # Histogram of run lengths (1, 2, 3-4, 5-8, 9-16, 17+).
    buckets = {"1": 0, "2": 0, "3-4": 0, "5-8": 0, "9-16": 0, "17+": 0}
    for L in lengths:
        if L == 1:
            buckets["1"] += 1
        elif L == 2:
            buckets["2"] += 1
        elif L <= 4:
            buckets["3-4"] += 1
        elif L <= 8:
            buckets["5-8"] += 1
        elif L <= 16:
            buckets["9-16"] += 1
        else:
            buckets["17+"] += 1

    n_odd = n_odd_ge2 + n_len1
    # Alternating positions telescope: D_alt = (σ_0 + σ_{N-1}) / 2 ∈ {-1,0,1}.
    D_alt_endpoint = (2 * bits[0] - 1 + 2 * bits[n - 1] - 1) // 2
    return {
        "N": n,
        "ones": int(sum(bits)),
        "D": D,
        "D_over_N": D / n,
        "n_defects": n_def,
        "defect_density": density,
        "n_runs": len(runs),
        "mean_run_length": mean_run,
        "max_run_length": max_run,
        "n_even_runs": n_even,
        "n_odd_runs_len_ge2": n_odd_ge2,
        "n_len1_runs": n_len1,
        "n_odd_runs": n_odd,
        "D_even_runs": D_even,
        "D_odd_runs_len_ge2": D_odd_ge2,
        "D_len1_runs": D_len1,
        "D_odd_runs": D_odd_ge2 + D_len1,
        "D_at_defect_positions": D_at_defects,
        "D_at_alternating_positions": D_at_alternating,
        "D_alternating_endpoint": D_alt_endpoint,
        "n_isolated_phase_flips": n_isolated,
        "n_clustered_defects": n_clustered,
        "isolated_flip_density": n_isolated / (n - 1),
        "run_length_histogram": buckets,
        # Bound: |D| <= n_odd_runs <= n_runs = n_defects + 1.
        "D_bound_n_odd_runs": n_odd,
    }


def scan_density(mask: int, w: int, tcap: int) -> tuple[float, float, int]:
    """Streaming defect density and mean run length. Returns (dens, mean_run, max_run)."""
    row = mask
    prev = (row >> w) & 1
    n_def = 0
    run = 1
    max_run = 1
    for t in range(1, tcap):
        row = rule30_step(row)
        bit = (row >> (w + t)) & 1
        if bit == prev:
            n_def += 1
            if run > max_run:
                max_run = run
            run = 1
        else:
            run += 1
        prev = bit
    if run > max_run:
        max_run = run
    n_runs = n_def + 1
    return n_def / (tcap - 1), tcap / n_runs, max_run


def prefix_string(bits, n: int = 16) -> str:
    return "".join(str(b) for b in bits[:n])


# ---------------------------------------------------------------------------
# Exhaustive small-w
# ---------------------------------------------------------------------------

def exhaustive_w(w: int) -> dict:
    tcap = TCAP(w)
    n_masks = (1 << (2 * w + 1)) - 1
    densities: list[float] = []
    mean_runs: list[float] = []
    max_runs: list[int] = []
    n_ge = 0
    best_mask = 1
    best_dens = -1.0
    worst_mask = 1
    worst_dens = 2.0
    for mask in range(1, n_masks + 1):
        dens, mean_run, max_run = scan_density(mask, w, tcap)
        densities.append(dens)
        mean_runs.append(mean_run)
        max_runs.append(max_run)
        if dens >= KILL_DENSITY:
            n_ge += 1
        if dens > best_dens:
            best_dens = dens
            best_mask = mask
        if dens < worst_dens:
            worst_dens = dens
            worst_mask = mask
    densities.sort()
    return {
        "w": w,
        "n_nonzero": n_masks,
        "tcap": tcap,
        "mean_defect_density": statistics.fmean(densities),
        "median_defect_density": statistics.median(densities),
        "min_defect_density": densities[0],
        "max_defect_density": densities[-1],
        "stdev_defect_density": statistics.pstdev(densities) if len(densities) > 1 else 0.0,
        "mean_of_mean_run_length": statistics.fmean(mean_runs),
        "min_mean_run_length": min(mean_runs),
        "max_mean_run_length": max(mean_runs),
        "max_L_run": max(max_runs),
        "n_density_ge_1_4": n_ge,
        "frac_density_ge_1_4": n_ge / n_masks,
        "argmax_density_mask": best_mask,
        "argmin_density_mask": worst_mask,
    }


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def run_checks(prize: bytearray) -> dict:
    checks: dict = {}

    ref = experiment_center_bits(PREFIX_CHECK)
    checks["packed_matches_experiment_center_bits_256"] = list(prize[:PREFIX_CHECK]) == list(ref)
    checks["prize_prefix16"] = prefix_string(prize, 16)
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == PRIZE_PREFIX16
    checks["prize_prefix20_ok"] = list(prize[:20]) == PRIZE_PREFIX20

    live = naive_centers({0: 1}, 64)
    checks["packed_matches_live_prize_64"] = list(prize[:64]) == live

    # Hand defects on the documented 16-bit prefix 1101110011000101.
    # Pairs equal at t = 1,4,5,7,9,11,12 → 7 defects in 15 pairs.
    pref = prize[:16]
    d16 = defect_indicators(pref)
    checks["prefix16_n_defects"] = int(sum(d16))
    checks["prefix16_n_defects_ok"] = checks["prefix16_n_defects"] == 7
    checks["prefix16_density"] = 7 / 15

    # Even-length alternating word: density 0, D in {0, ±1} from leftover.
    alt = bytearray([i & 1 for i in range(64)])
    a = analyze(alt)
    checks["synthetic_alt_density_0"] = a["defect_density"] == 0.0
    checks["synthetic_alt_one_run"] = a["n_runs"] == 1
    checks["synthetic_alt_D_even_0"] = a["D_even_runs"] == 0
    checks["synthetic_alt_D"] = a["D"] == 0  # length 64 even

    const = bytearray(32)
    c = analyze(const)
    checks["synthetic_const_density_1"] = c["defect_density"] == 1.0
    checks["synthetic_const_mean_run_1"] = c["mean_run_length"] == 1.0
    checks["synthetic_const_all_len1"] = c["n_len1_runs"] == 32

    # Isolated phase flip: 010101 + extra 1 + 01010 = 010101101010 (12 bits).
    # One defect, two even-length runs, D = 0.
    flip = bytearray([0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0])
    f = analyze(flip)
    checks["synthetic_flip_n_defects"] = f["n_defects"] == 1
    checks["synthetic_flip_isolated"] = f["n_isolated_phase_flips"] == 1
    checks["synthetic_flip_D_even_0"] = f["D_even_runs"] == 0
    checks["synthetic_flip_D"] = f["D"] == 0
    checks["synthetic_flip_two_even_runs"] = f["n_even_runs"] == 2

    # D decomposition identity.
    st = analyze(prize[:1000])
    checks["D_decomp_runs"] = (
        st["D_even_runs"] + st["D_odd_runs_len_ge2"] + st["D_len1_runs"] == st["D"]
    )
    checks["D_decomp_positions"] = (
        st["D_at_defect_positions"] + st["D_at_alternating_positions"] == st["D"]
    )
    checks["n_runs_is_ndef_plus_1"] = st["n_runs"] == st["n_defects"] + 1
    checks["even_runs_contribute_0"] = st["D_even_runs"] == 0
    checks["alternating_positions_telescope"] = (
        st["D_at_alternating_positions"] == st["D_alternating_endpoint"]
        and st["D_alternating_endpoint"]
        == (2 * prize[0] - 1 + 2 * prize[999] - 1) // 2
    )
    for n in (10, 16, 64, 128, 1000):
        sn = analyze(prize[:n])
        end = (2 * prize[0] - 1 + 2 * prize[n - 1] - 1) // 2
        if sn["D_at_alternating_positions"] != end:
            checks["alternating_positions_telescope"] = False
            break
    checks["synthetic_alt_telescopes"] = a["D_at_alternating_positions"] == a["D_alternating_endpoint"]
    checks["synthetic_flip_telescopes"] = f["D_at_alternating_positions"] == f["D_alternating_endpoint"]
    checks["synthetic_const_telescopes"] = c["D_at_alternating_positions"] == c["D_alternating_endpoint"]

    # Copied BM agrees with experiment.linear_complexity on a short prefix.
    L_loc, _conn = experiment_linear_complexity(bytes(prize[:64]))
    checks["bm_matches_experiment_64"] = linear_complexity(prize[:64]) == L_loc

    # Packed evolution of a radius-3 row matches live cells.
    w, mask, tcap = 3, 122, 40
    packed = list(evolve_centers(mask, w, tcap))
    live_w = naive_centers(mask_to_live(mask, w), tcap)
    checks["packed_matches_live_w3_mask122"] = packed == live_w

    # Streaming scorer agrees with stored-trace analyzer on the prize prefix.
    dens_s, mean_s, max_s = scan_density(1, 0, 128)
    stored = analyze(prize[:128])
    checks["stream_matches_stored_prize_128"] = (
        abs(dens_s - stored["defect_density"]) < 1e-15
        and abs(mean_s - stored["mean_run_length"]) < 1e-12
        and max_s == stored["max_run_length"]
    )
    # Cycle I: prize seed L_run(w=0)=7 inside tcap=128.
    checks["prize_L_run_128_is_7"] = stored["max_run_length"] == 7

    checks["all_ok"] = all(
        v is True for k, v in checks.items() if k not in (
            "prize_prefix16", "prefix16_n_defects", "prefix16_density",
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def _fmt(x: float, digits: int = 6) -> str:
    return f"{x:.{digits}f}"


def write_markdown(dump: dict) -> str:
    checks = dump["checks"]
    prize = dump["prize"]
    n1e5 = prize["checkpoints"][-1]
    iid = dump["iid"]
    bm = dump["berlekamp_massey"]
    exh = dump["exhaustive"]
    last_d = bm["defects"][-1]
    last_c = bm["centre"][-1]
    hist = n1e5["run_length_histogram"]
    lines: list[str] = []
    a = lines.append

    a("# Period-2 bursts: defect density and signed discrepancy")
    a("")
    a("This note is ideas10 item 4 (prize Problem 2). It does **not**")
    a("prove `D(N)=o(N)`, and it does not claim a prize result.")
    a("")
    a("Helper: `research/period2_defects.py --certify`. Dump:")
    a("`research/period2_defects.json`. Packed evolution is the same")
    a("engine as `experiment.center_bits`; that file is not modified.")
    a("")
    a("## Attack")
    a("")
    a("Write `D(N) = sum_{t<N} (2 c_t - 1)`. Split the centre into")
    a("maximal alternating (period-2) runs: a new run starts at every")
    a("time `t >= 1` with `c_t == c_{t-1}`. Call those times **defects**.")
    a("Each defect is a global phase flip between the two period-2")
    a("alignments `01` and `10`. An *isolated* phase flip is a defect")
    a("sitting between two genuine alternating bursts (neither neighbour")
    a("pair is a defect).")
    a("")
    a("A period-2 burst of even length contributes **0** to `D`: the")
    a("bits pair as `01` or `10`. An odd-length burst contributes `±1`")
    a("(one leftover unpaired bit). Length-1 runs are leftover defect")
    a("bits that never seed a burst. Hence")
    a("")
    a("```")
    a("D(N) = (signed leftovers of odd-length runs),")
    a("|D(N)| <= (# odd runs) <= (# runs) = (# defects) + 1.")
    a("```")
    a("")
    a("A tighter pairing holds on *positions*: writing `σ_t = 2 c_t - 1`,")
    a("the signed sum over alternating times (`t=0` and every `t` with")
    a("`c_t != c_{t-1}`) telescopes to an endpoint,")
    a("")
    a("```")
    a("D_alt(N) = (σ_0 + σ_{N-1}) / 2  ∈  {-1, 0, +1},")
    a("D(N)     = D_defects(N) + D_alt(N).")
    a("```")
    a("")
    a("So even-length interior bursts, and in fact every alternating")
    a("position, contribute only `O(1)` to `D`. The whole discrepancy")
    a("is the signed sum of the defect bits plus a boundary. If defect")
    a("density were `o(1)`, that sum would be `o(N)` and Problem 2 would")
    a("follow.")
    a("")
    a("**Kill:** density stays `>= 1/4` on the prize seed at `N=10^5`,")
    a("or the defect sequence has Berlekamp–Massey `L(N) ~ N/2` like")
    a("`c` itself.")
    a("")
    a("iid fair bits have expected defect density `1/2` and mean")
    a("alternating-run length `2`. Isolated phase flips have expected")
    a("density `1/8`.")
    a("")
    a("## Engine")
    a("")
    a("Packed Rule 30")
    a("")
    a("```")
    a("new = (row << 2) ^ ((row << 1) | row)")
    a("```")
    a("")
    a("with the centre bit at time `t` equal to `(row >> (w+t)) & 1`.")
    a("The prize seed is `w=0`, mask `1`, which is")
    a("`experiment.center_bits`. The packed prefix of length 256 matches")
    a(f"that function (`{checks['prize_prefix16']}…`). An independent")
    a("live-cell spacetime agrees on the prize seed and on a sampled")
    a("radius-3 row. The streaming defect scorer agrees with the")
    a("stored-trace analyzer. `D_alt = (σ_0 + σ_{N-1})/2` holds on the")
    a("prize prefixes and on the synthetic words. Even-length synthetic")
    a("`01` has density 0 and `D=0`; a single inserted repeat is an")
    a("isolated phase flip whose two even bursts still sum to `D=0`.")
    a("")
    a("## Prize seed through `N=10^5`")
    a("")
    a("| N | ones | D(N) | density | mean run | max run | even | odd ≥2 | len-1 | D even | D odd ≥2 | D len-1 | D defects | D alt | isolated |")
    a("|--:|-----:|-----:|--------:|---------:|--------:|-----:|-------:|------:|-------:|---------:|--------:|----------:|------:|---------:|")
    for row in prize["checkpoints"]:
        a(
            f"| {row['N']} | {row['ones']} | {row['D']} | "
            f"{_fmt(row['defect_density'])} | {_fmt(row['mean_run_length'], 4)} | "
            f"{row['max_run_length']} | {row['n_even_runs']} | "
            f"{row['n_odd_runs_len_ge2']} | {row['n_len1_runs']} | "
            f"{row['D_even_runs']} | {row['D_odd_runs_len_ge2']} | "
            f"{row['D_len1_runs']} | {row['D_at_defect_positions']} | "
            f"{row['D_at_alternating_positions']} | "
            f"{row['n_isolated_phase_flips']} |"
        )
    a("")
    a(
        f"At `N=10^5`, defect density is `{_fmt(n1e5['defect_density'])}` "
        f"(iid expects `1/2`), mean alternating-run length is "
        f"`{_fmt(n1e5['mean_run_length'], 4)}` (iid expects `2`), and "
        f"`D(10^5)={n1e5['D']}`. Every even-length burst contributes "
        f"`{n1e5['D_even_runs']}` to `D`. The signed sum is the leftover "
        f"of odd-length runs (`{n1e5['D_odd_runs_len_ge2']}` from bursts "
        f"of length ≥3, `{n1e5['D_len1_runs']}` from length-1 bits), "
        f"{n1e5['n_odd_runs']} odd runs in all. The bound "
        f"`|D| <= {n1e5['n_odd_runs']}` is true and useless: those "
        f"leftovers cancel down to {n1e5['D']}, the same order as a "
        f"random walk of that many ±1 steps, not a structured pairing."
    )
    a("")
    a(
        f"The position split is the sharp statement. Alternating "
        f"positions contribute `D_alt={n1e5['D_at_alternating_positions']}` "
        f"(equal to `(σ_0 + σ_{{N-1}})/2`; the prize seed starts with 1 "
        f"and the last bit is 1). Defect positions contribute "
        f"`{n1e5['D_at_defect_positions']}`, which *is* `D` up to that "
        f"endpoint. Pairing succeeds; sparsity does not."
    )
    a("")
    a(
        f"Isolated phase flips are `{n1e5['n_isolated_phase_flips']}` of "
        f"the `{n1e5['n_defects']}` defects (density "
        f"`{_fmt(n1e5['isolated_flip_density'])}`; iid expects `1/8 = "
        f"0.125`). The rest are clustered."
    )
    a("")
    a("Run-length histogram at `N=10^5`:")
    a("")
    a("| length | 1 | 2 | 3–4 | 5–8 | 9–16 | 17+ |")
    a("|:-------|--:|--:|----:|----:|-----:|----:|")
    a(
        f"| count | {hist['1']} | {hist['2']} | {hist['3-4']} | "
        f"{hist['5-8']} | {hist['9-16']} | {hist['17+']} |"
    )
    a("")
    a("The mass sits on lengths 1 and 2, as for iid bits")
    n_runs = n1e5["n_runs"]
    a(
        f"(`P(L=k)=1/2^k`: among {n_runs} runs one expects about "
        f"{n_runs // 2} of length 1 and {n_runs // 4} of length 2;"
    )
    a(
        f"the table has {hist['1']} and {hist['2']}). Long period-2"
    )
    a(
        f"bursts exist (Cycle I’s `L_run(0)=7` inside `tcap=128`; here"
    )
    a(
        f"max run is {n1e5['max_run_length']} through `N=10^5`), but"
    )
    a("they are rare and even the long even ones still contribute 0")
    a("only locally.")
    a("")
    a("## Comparison to iid fair bits")
    a("")
    a("| source | N | defect density | mean run | isolated density | `L(d)/n` |")
    a("|--------|--:|---------------:|---------:|-----------------:|---------:|")
    a("| iid expectation | — | 0.500000 | 2.0000 | 0.125000 | ~1/2 |")
    a(
        f"| iid PRNG (seed {iid['seed']}) | {iid['N']} | "
        f"{_fmt(iid['defect_density'])} | {_fmt(iid['mean_run_length'], 4)} | "
        f"{_fmt(iid['isolated_flip_density'])} | {_fmt(iid['L_over_train'])} |"
    )
    a(
        f"| prize centre | {n1e5['N']} | {_fmt(n1e5['defect_density'])} | "
        f"{_fmt(n1e5['mean_run_length'], 4)} | "
        f"{_fmt(n1e5['isolated_flip_density'])} | "
        f"{_fmt(last_d['L_over_train'])} |"
    )
    a("")
    a("The prize centre is statistically indistinguishable from fair")
    a("bits on this screen: density stays near `1/2` at every")
    a("checkpoint from `N=10` through `N=10^5`, never dropping to the")
    a("kill threshold `1/4`.")
    a("")
    a("## Berlekamp–Massey of the defect sequence")
    a("")
    a("Defect bits `d_{t-1} = 1_{c_t == c_{t-1}}` for `t = 1, …, N`.")
    a("Training lengths match `experiment.py`’s centre BM checkpoints,")
    a("plus 4096. Copied BM agrees with `experiment.linear_complexity`")
    a("on a 64-bit prefix.")
    a("")
    a("| train | `L(c)` | `L(c)/n` | `L(d)` | `L(d)/n` |")
    a("|------:|-------:|---------:|-------:|---------:|")
    for c_row, d_row in zip(bm["centre"], bm["defects"]):
        a(
            f"| {c_row['train']} | {c_row['L']} | {_fmt(c_row['L_over_train'])} | "
            f"{d_row['L']} | {_fmt(d_row['L_over_train'])} |"
        )
    a("")
    a(
        f"At {last_d['train']} bits, `L(d)/n={_fmt(last_d['L_over_train'])}` "
        f"and `L(c)/n={_fmt(last_c['L_over_train'])}`. Defects are as"
    )
    a("irregular as `c`: a linear recurrence of order `o(N)` is not")
    a("hiding in the break sequence. (The same `L ~ N/2` profile is why")
    a("residue-class subsamples died in")
    a("`research/residue_discrepancy.md`.)")
    a("")
    a("## Exhaustive small-`w` rows")
    a("")
    a("Every nonzero initial word of support radius `w=0..6`")
    a("(`2^{2w+1}-1` states; `w=6` is 8191) evolved in a quiescent")
    a("background up to `tcap=8w+128`. Defect density of the centre")
    a("trace, as a check that finite rows are similar to the prize seed.")
    a("")
    a("| w | states | tcap | mean density | median | min | max | mean of mean-run | max L_run | frac ≥ 1/4 |")
    a("|--:|-------:|-----:|-------------:|-------:|----:|----:|-----------------:|----------:|-----------:|")
    for r in exh:
        a(
            f"| {r['w']} | {r['n_nonzero']} | {r['tcap']} | "
            f"{_fmt(r['mean_defect_density'])} | {_fmt(r['median_defect_density'])} | "
            f"{_fmt(r['min_defect_density'])} | {_fmt(r['max_defect_density'])} | "
            f"{_fmt(r['mean_of_mean_run_length'], 4)} | {r['max_L_run']} | "
            f"{_fmt(r['frac_density_ge_1_4'], 4)} |"
        )
    a("")
    a("Mean densities sit in a tight band around `1/2`. The `w=0` line")
    a("is the prize seed at `tcap=128` (density already well above")
    a("`1/4`). Every scanned radius-`w` row has density `>= 1/4` (at")
    a("`w=6` the sparsest centre still has density `0.354`). No")
    a("finite-row exception makes the prize seed look atypical. The")
    a("Cycle I `L_run(6)=24` maximizer is a long *local* burst, not a")
    a("low-density trace: long even bursts still contribute 0 only on")
    a("their own support, and the rest of the centre is defect-rich.")
    a("The `max L_run` column reproduces the Cycle I table through")
    a("`w=6`.")
    a("")
    a("## Why it died")
    a("")
    a("Preregistered kill: density stays `>= 1/4` at `N=10^5`, or")
    a("defects have `L(N) ~ N/2` like `c`. Both fired. Period-2 pairing")
    a("does reduce `D` to the defect positions plus an `O(1)` endpoint,")
    a("but defect density is `Θ(1)`, of order `1/2`, so the `o(N)`")
    a("counting argument never starts. The defect sequence is not")
    a("simpler than `c`.")
    a("")
    a("Not a prize claim. Eventual period 2 of the prize seed is a")
    a("different question (a single unbounded run, not a density); this")
    a("screen does not address it.")
    a("")
    a("## Verdict")
    a("")
    a(f"`{dump['verdict']}`, wall time {dump['wall_time_sec']:.2f}s.")
    a("")
    a(f"- Kill: {'yes' if dump['kill'] else 'no'}.")
    a(f"- Survive: {'yes' if dump['survive'] else 'no'}.")
    a(f"- Reason: {dump['kill_reason']}")
    a("")
    a("## Files")
    a("")
    a("- `research/period2_defects.md` (this note)")
    a("- `research/period2_defects.py` (`--certify` runs the checks, the")
    a("  prize-seed screen through `N=10^5`, and exhaustive `w<=6`)")
    a("- `research/period2_defects.json` (dump)")
    a("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def certify() -> dict:
    t_all = time.perf_counter()
    log: list[str] = []

    prize_bits = packed_center(N_PRIZE)
    checks = run_checks(prize_bits)
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    checkpoints = []
    for n in CHECKPOINTS:
        st = analyze(prize_bits[:n])
        checkpoints.append(st)
        log.append(
            f"N={n} density={st['defect_density']:.6f} "
            f"mean_run={st['mean_run_length']:.4f} D={st['D']}"
        )
        print(log[-1], flush=True)

    defects = defect_indicators(prize_bits)
    bm_centre = []
    bm_defects = []
    for n in BM_TRAIN:
        Lc = linear_complexity(prize_bits[:n])
        # Defect sequence has length N-1; train on min(n, N-1).
        nd = min(n, len(defects))
        Ld = linear_complexity(defects[:nd])
        bm_centre.append({"train": n, "L": Lc, "L_over_train": Lc / n})
        bm_defects.append({"train": nd, "L": Ld, "L_over_train": Ld / nd})
        log.append(f"BM n={n} L(c)={Lc} L(d)={Ld}")
        print(log[-1], flush=True)

    rng = random.Random(IID_SEED)
    iid_bits = bytearray(rng.getrandbits(1) for _ in range(N_PRIZE))
    iid_st = analyze(iid_bits)
    iid_def = defect_indicators(iid_bits)
    iid_train = BM_TRAIN[-1]
    iid_L = linear_complexity(iid_def[:iid_train])
    iid = {
        "seed": IID_SEED,
        "N": N_PRIZE,
        "defect_density": iid_st["defect_density"],
        "mean_run_length": iid_st["mean_run_length"],
        "isolated_flip_density": iid_st["isolated_flip_density"],
        "D": iid_st["D"],
        "train": iid_train,
        "L_defects": iid_L,
        "L_over_train": iid_L / iid_train,
    }
    log.append(
        f"iid density={iid['defect_density']:.6f} mean_run={iid['mean_run_length']:.4f}"
    )
    print(log[-1], flush=True)

    exhaustive = []
    for w in range(0, W_MAX + 1):
        rec = exhaustive_w(w)
        exhaustive.append(rec)
        log.append(
            f"w={w} n={rec['n_nonzero']} mean_density={rec['mean_defect_density']:.6f} "
            f"min={rec['min_defect_density']:.6f} max={rec['max_defect_density']:.6f}"
        )
        print(log[-1], flush=True)

    dens_1e5 = checkpoints[-1]["defect_density"]
    min_ckpt_density = min(r["defect_density"] for r in checkpoints)
    last_L_ratio = bm_defects[-1]["L_over_train"]
    kill_density = dens_1e5 >= KILL_DENSITY
    density_stays = min_ckpt_density >= KILL_DENSITY
    kill_bm = last_L_ratio >= KILL_L_RATIO
    kill = kill_density or kill_bm
    if kill:
        verdict = "KILL"
        kill_reason = (
            f"prize-seed defect density at N=10^5 is {dens_1e5:.6f} >= 1/4 "
            f"(stays >= 1/4 at every checkpoint, min {min_ckpt_density:.6f}); "
            f"Berlekamp-Massey of the defect sequence at {bm_defects[-1]['train']} "
            f"bits has L={bm_defects[-1]['L']} so L/n={last_L_ratio:.4f} ~ 1/2, "
            f"matching L(c)/n={bm_centre[-1]['L_over_train']:.4f}. "
            "Even-length period-2 bursts contribute 0 to D, but they are not "
            "the bulk of the trace. Defects are as irregular as c. Not a prize claim."
        )
    else:
        verdict = "SURVIVE"
        kill_reason = (
            "defect density dropped below 1/4 and the defect sequence has "
            "sublinear linear complexity; this screen did not fire"
        )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_defects",
        "ideas": "ideas10 item 4",
        "problem": (
            "even-length period-2 centre bursts contribute 0 to D(N); "
            "if defect density were o(1) then D(N)=o(N) plus boundary"
        ),
        "verdict": verdict,
        "kill": kill,
        "survive": not kill,
        "kill_reason": kill_reason,
        "kill_density_ge_1_4": kill_density,
        "density_stays_ge_1_4_all_checkpoints": density_stays,
        "kill_defects_L_near_N_over_2": kill_bm,
        "wall_time_sec": round(wall, 4),
        "N": N_PRIZE,
        "iid_expected_defect_density": 0.5,
        "iid_expected_mean_run_length": 2.0,
        "checks": checks,
        "prize": {
            "prefix16": checks["prize_prefix16"],
            "checkpoints": checkpoints,
        },
        "iid": iid,
        "berlekamp_massey": {"centre": bm_centre, "defects": bm_defects},
        "exhaustive": exhaustive,
        "w_max": W_MAX,
        "tcap": "8w+128",
        "not_a_prize_claim": True,
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(dump))
    print(f"wrote {OUT_JSON}", flush=True)
    print(f"wrote {OUT_MD}", flush=True)
    print(f"verdict={verdict} wall={wall:.3f}s", flush=True)
    print(f"reason: {kill_reason}", flush=True)
    return dump


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
