#!/usr/bin/env python3
"""ideas13 item 2 / leftover ideas11–12: local recurrence for period-2 defects.

Cycle K (research/period2_defects.md) showed that the signed discrepancy
D(N) = sum_{t<N} (2 c_t - 1) equals the signed sum of defect bits
d_t = 1_{c_t = c_{t-1}} plus an O(1) alternating-run endpoint, and that
the defect sequence itself has Berlekamp–Massey L(N) ~ N/2.

This script asks whether d nevertheless obeys a *local* recurrence that
would close without evolving the full Rule 30 triangle:

  1. For window widths w = 1..8, is d_{t+1} a Boolean function of
     (d_t, ..., d_{t-w+1}) on the prize seed through t = 4096?
  2. Is d_{t+1} a Boolean of a bounded centre window c_{t-w..t} together
     with leftover neighbour bits (the cells adjacent to the centre that
     are not already in the centre column)?

Kill if every defect window mismatches (d is not itself a low-order CA /
finite-memory shift), or if the only consistent neighbour fits secretly
need the light cone (current-row bits at |j| >= 1, and the triple
(l_t, c_t, r_t) does not close).

Packed evolution matches experiment.center_bits:
    z_0 = 1,  z <- (z << 2) ^ ((z << 1) | z),  x(t,j) = (z >> (j + t)) & 1.
That file is not modified. Stdlib only. Not a prize claim.

Run: python3 research/defect_recurrence.py --certify
Dump: research/defect_recurrence.json, research/defect_recurrence.md
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits
from experiment import linear_complexity as experiment_linear_complexity

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

T_MAX = 4096
W_MAX = 8
PREFIX_CHECK = 256
PRIZE_PREFIX16 = "1101110011000101"
PRIZE_PREFIX20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
# Hand defects on the documented 16-bit prefix (pairs equal at those t).
PREFIX16_DEFECT_TIMES = (1, 4, 5, 7, 9, 11, 12)
IID_SEED = 20260911
BM_N = 4096
KILL_L_RATIO = 0.40


# ---------------------------------------------------------------------------
# Packed Rule 30 (experiment.py convention). Bit k of z_t is spatial k-t.
# Centre c_t = (z >> t) & 1. Left neighbour l_t = x(t,-1), right r_t = x(t,1).
# ---------------------------------------------------------------------------

def rule30_step(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def packed_rows_and_bits(max_t: int):
    """z_t for t=0..max_t and centre bits c_0..c_{max_t+1}."""
    row = 1
    n_bits = max_t + 2
    bits = bytearray(n_bits)
    rows = [0] * (max_t + 1)
    for t in range(n_bits):
        bits[t] = (row >> t) & 1
        if t <= max_t:
            rows[t] = row
        row = rule30_step(row)
    return rows, bits


def x_of(row: int, t: int, j: int) -> int:
    """Spatial bit x(t,j) under experiment packing. Vacuum 0 for index < 0."""
    idx = j + t
    if idx < 0:
        return 0
    return (row >> idx) & 1


def spatial_window(row: int, t: int, radius: int) -> tuple[int, int]:
    """Pack x(t,-k)..x(t,k) with bit 0 = x(t,-k). Returns (word, width)."""
    width = 2 * radius + 1
    v = 0
    for i, j in enumerate(range(-radius, radius + 1)):
        if x_of(row, t, j):
            v |= 1 << i
    return v, width


def next_centre_from_triple(l: int, c: int, r: int) -> int:
    return l ^ (c | r)


def defect_from_triple(c: int, l: int, r: int) -> int:
    """d_{t+1} = 1_{c_{t+1}=c_t} from the radius-1 slice at time t."""
    nxt = next_centre_from_triple(l, c, r)
    return 1 if nxt == c else 0


def defect_from_triple_closed(c: int, l: int, r: int) -> int:
    """Same map without forming c_{t+1}: c=1 => NOT l; c=0 => 1_{l=r}."""
    if c:
        return 1 - l
    return int(l == r)


def next_left(x_m2: int, l: int, c: int) -> int:
    return x_m2 ^ (l | c)


def next_right(c: int, r: int, x_p2: int) -> int:
    return c ^ (r | x_p2)


def defect_indicators(bits) -> bytearray:
    """d_t = 1_{c_t = c_{t-1}} for t = 1..N-1, stored at index t (d[0] unused)."""
    n = len(bits)
    out = bytearray(n)
    for t in range(1, n):
        out[t] = 1 if bits[t] == bits[t - 1] else 0
    return out


def signed_D(bits) -> int:
    return 2 * sum(bits) - len(bits)


def linear_complexity(bits) -> int:
    """Binary Berlekamp–Massey. Copied from experiment.py; that file is not modified."""
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


def naive_trace(t_max: int):
    """Independent live-cell spacetime. Returns c, l, r, and x(t,-2), x(t,2)."""
    cur = {0: 1}
    cs: list[int] = []
    ls: list[int] = []
    rs: list[int] = []
    lm2: list[int] = []
    rp2: list[int] = []
    for _t in range(t_max + 1):
        cs.append(1 if 0 in cur else 0)
        ls.append(1 if -1 in cur else 0)
        rs.append(1 if 1 in cur else 0)
        lm2.append(1 if -2 in cur else 0)
        rp2.append(1 if 2 in cur else 0)
        if not cur:
            cs.extend([0] * (t_max + 1 - len(cs)))
            ls.extend([0] * (t_max + 1 - len(ls)))
            rs.extend([0] * (t_max + 1 - len(rs)))
            lm2.extend([0] * (t_max + 1 - len(lm2)))
            rp2.extend([0] * (t_max + 1 - len(rp2)))
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
    return cs, ls, rs, lm2, rp2


def pack_window(seq, t: int, width: int) -> int:
    """Pack seq[t], seq[t-1], ..., seq[t-width+1] with bit 0 = seq[t]."""
    v = 0
    for i in range(width):
        if seq[t - i]:
            v |= 1 << i
    return v


def pack_forward(seq, t0: int, width: int) -> int:
    """Pack seq[t0], seq[t0+1], ..., seq[t0+width-1] with bit 0 = seq[t0]."""
    v = 0
    for i in range(width):
        if seq[t0 + i]:
            v |= 1 << i
    return v


# ---------------------------------------------------------------------------
# Boolean fit: does the same key ever map to two values?
# Witnessed determination requires reuse. Unique keys are not a function.
# ---------------------------------------------------------------------------

def fit_boolean(samples: list[tuple[int, int, int]]) -> dict:
    """samples: (t, key, value). key and value are non-negative ints."""
    first: dict[int, tuple[int, int]] = {}
    counts: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    n_mismatch = 0
    first_mismatch = None
    n_reuse_events = 0
    reused_keys: set[int] = set()
    n_samples = len(samples)
    for t, key, val in samples:
        val = int(val)
        counts[key][val] += 1
        if key in first:
            n_reuse_events += 1
            reused_keys.add(key)
            if first[key][1] != val:
                n_mismatch += 1
                if first_mismatch is None:
                    first_mismatch = {
                        "t": t,
                        "key": key,
                        "first_t": first[key][0],
                        "first_value": first[key][1],
                        "new_value": val,
                    }
        else:
            first[key] = (t, val)
    n_keys = len(counts)
    n_colliding = 0
    n_maj = 0
    n_ties = 0
    for hist in counts.values():
        freqs = list(hist.values())
        mx = max(freqs)
        n_maj += mx
        if len(hist) > 1:
            n_colliding += 1
            if sum(1 for f in freqs if f == mx) > 1:
                n_ties += 1
    consistent = n_mismatch == 0 and n_colliding == 0
    n_reused = len(reused_keys)
    vacuous = consistent and n_reused == 0
    return {
        "n_samples": n_samples,
        "n_keys": n_keys,
        "n_reused_keys": n_reused,
        "n_reuse_events": n_reuse_events,
        "n_colliding_keys": n_colliding,
        "n_mismatch_events": n_mismatch,
        "n_majority_ties": n_ties,
        "consistent": consistent,
        "vacuous_consistent": vacuous,
        "witnessed_function": bool(consistent and n_reused > 0),
        "majority_accuracy": (n_maj / n_samples) if n_samples else None,
        "first_mismatch": first_mismatch,
        "t_lo": samples[0][0] if samples else None,
        "t_hi": samples[-1][0] if samples else None,
    }


def yn(flag: bool) -> str:
    return "yes" if flag else "no"


def fmt_acc(x) -> str:
    if x is None:
        return "—"
    return f"{x:.4f}"


def fmt_mm(rec: dict) -> str:
    mm = rec.get("first_mismatch")
    if mm is None:
        return "—"
    return f"t={mm['t']}"


def compact_fit(rec: dict) -> dict:
    out = dict(rec)
    return out


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def self_check(rows, bits, d, l, r, lm2, rp2) -> dict:
    checks: dict = {}
    ref256 = experiment_center_bits(PREFIX_CHECK)
    checks["packed_matches_experiment_center_bits_256"] = list(bits[:PREFIX_CHECK]) == list(ref256)
    long_ref = experiment_center_bits(T_MAX + 2)
    checks["packed_matches_experiment_center_bits_through_T_MAX_plus_1"] = list(bits) == list(long_ref)
    checks["known20"] = list(bits[:20]) == PRIZE_PREFIX20
    checks["prefix16"] = "".join(str(b) for b in bits[:16]) == PRIZE_PREFIX16

    pref = bits[:16]
    d16_times = tuple(t for t in range(1, 16) if pref[t] == pref[t - 1])
    checks["prefix16_defect_times"] = list(d16_times)
    checks["prefix16_n_defects"] = len(d16_times)
    checks["prefix16_n_defects_ok"] = d16_times == PREFIX16_DEFECT_TIMES

    n_naive = min(64, T_MAX)
    ncs, nls, nrs, nlm2, nrp2 = naive_trace(n_naive)
    naive_c_ok = list(bits[: n_naive + 1]) == ncs
    naive_l_ok = list(l[: n_naive + 1]) == nls
    naive_r_ok = list(r[: n_naive + 1]) == nrs
    naive_m2_ok = list(lm2[: n_naive + 1]) == nlm2
    naive_p2_ok = list(rp2[: n_naive + 1]) == nrp2
    checks["naive_spacetime_c_64"] = naive_c_ok
    checks["naive_spacetime_l_64"] = naive_l_ok
    checks["naive_spacetime_r_64"] = naive_r_ok
    checks["naive_spacetime_x_m2_64"] = naive_m2_ok
    checks["naive_spacetime_x_p2_64"] = naive_p2_ok

    packing_centre = True
    formula_ok = True
    closed_ok = True
    next_lr_ok = True
    left_edge = True
    for t in range(T_MAX + 1):
        z = rows[t]
        if ((z >> t) & 1) != bits[t]:
            packing_centre = False
            break
        if t >= 1 and x_of(z, t, -t) != 1:
            left_edge = False
            break
        if t >= 1:
            got = next_centre_from_triple(l[t], bits[t], r[t])
            if got != bits[t + 1]:
                formula_ok = False
                break
            if defect_from_triple(bits[t], l[t], r[t]) != d[t + 1]:
                formula_ok = False
                break
            if defect_from_triple_closed(bits[t], l[t], r[t]) != d[t + 1]:
                closed_ok = False
                break
            if t + 1 <= T_MAX:
                if next_left(lm2[t], l[t], bits[t]) != l[t + 1]:
                    next_lr_ok = False
                    break
                if next_right(bits[t], r[t], rp2[t]) != r[t + 1]:
                    next_lr_ok = False
                    break
    checks["packing_centre_bit"] = packing_centre
    checks["triple_matches_next_centre"] = formula_ok
    checks["closed_defect_formula"] = closed_ok
    checks["next_leftover_needs_radius_2"] = next_lr_ok
    checks["prize_left_edge_x_t_minus_t"] = left_edge

    # D = signed sum at defect positions + O(1) endpoint (Cycle K).
    def d_split(cN):
        n = len(cN)
        D = signed_D(cN)
        D_def = 0
        D_alt = 2 * cN[0] - 1
        for t in range(1, n):
            s = 2 * cN[t] - 1
            if cN[t] == cN[t - 1]:
                D_def += s
            else:
                D_alt += s
        D_alt_endpoint = (2 * cN[0] - 1 + 2 * cN[n - 1] - 1) // 2
        return D, D_def, D_alt, D_alt_endpoint

    D4096, Ddef4096, Dalt4096, Dend4096 = d_split(bits[:4096])
    D4097, Ddef4097, Dalt4097, Dend4097 = d_split(bits[:4097])
    checks["D_equals_D_defects_plus_D_alt"] = (
        D4096 == Ddef4096 + Dalt4096 and D4097 == Ddef4097 + Dalt4097
    )
    checks["D_alt_equals_endpoint"] = Dalt4096 == Dend4096 and Dalt4097 == Dend4097
    checks["D_alt_abs_le_1"] = abs(Dalt4096) <= 1 and abs(Dalt4097) <= 1
    checks["D_at_4096"] = D4096
    checks["D_defects_at_4096"] = Ddef4096
    checks["D_alt_at_4096"] = Dalt4096
    checks["D_at_4097"] = D4097
    checks["D_defects_at_4097"] = Ddef4097
    checks["D_alt_at_4097"] = Dalt4097
    # xor_transform.md quotes D(4096)=-40 for this packing.
    checks["D_4096_matches_xor_transform"] = D4096 == -40

    # Synthetic Boolean fits: constant / alternating / period-2 defects.
    alt = bytearray([i & 1 for i in range(64)])
    d_alt = defect_indicators(alt)
    samples_alt = [(t, d_alt[t], d_alt[t + 1]) for t in range(1, 62)]
    fit_alt = fit_boolean(samples_alt)
    checks["synthetic_alt01_all_defects_zero"] = all(d_alt[t] == 0 for t in range(1, 64))
    checks["synthetic_alt01_w1_witnessed"] = fit_alt["witnessed_function"]

    const = bytearray([1] * 64)
    d_const = defect_indicators(const)
    samples_const = [(t, d_const[t], d_const[t + 1]) for t in range(1, 62)]
    fit_const = fit_boolean(samples_const)
    checks["synthetic_const_all_defects_one"] = all(d_const[t] == 1 for t in range(1, 64))
    checks["synthetic_const_w1_witnessed"] = fit_const["witnessed_function"]

    # d_t = t mod 2 is itself a width-1 CA (NOT of the last bit).
    d_flip = bytearray(64)
    for t in range(1, 64):
        d_flip[t] = t & 1
    samples_flip = [(t, d_flip[t], d_flip[t + 1]) for t in range(1, 62)]
    fit_flip = fit_boolean(samples_flip)
    checks["synthetic_period2_defects_w1_witnessed"] = fit_flip["witnessed_function"]
    # Same window must fail for a mixed mapping.
    mixed = [(1, 0, 0), (2, 0, 1)]
    checks["synthetic_collision_detected"] = not fit_boolean(mixed)["consistent"]

    # BM copy agrees with experiment.linear_complexity on a short word.
    sample_c = list(bits[:40])
    L_copy = linear_complexity(sample_c)
    L_exp, _conn = experiment_linear_complexity(sample_c)
    checks["bm_copy_matches_experiment"] = L_copy == L_exp

    required = (
        "packed_matches_experiment_center_bits_256",
        "packed_matches_experiment_center_bits_through_T_MAX_plus_1",
        "known20",
        "prefix16",
        "prefix16_n_defects_ok",
        "naive_spacetime_c_64",
        "naive_spacetime_l_64",
        "naive_spacetime_r_64",
        "naive_spacetime_x_m2_64",
        "naive_spacetime_x_p2_64",
        "packing_centre_bit",
        "triple_matches_next_centre",
        "closed_defect_formula",
        "next_leftover_needs_radius_2",
        "prize_left_edge_x_t_minus_t",
        "D_equals_D_defects_plus_D_alt",
        "D_alt_equals_endpoint",
        "D_alt_abs_le_1",
        "D_4096_matches_xor_transform",
        "synthetic_alt01_all_defects_zero",
        "synthetic_alt01_w1_witnessed",
        "synthetic_const_all_defects_one",
        "synthetic_const_w1_witnessed",
        "synthetic_period2_defects_w1_witnessed",
        "synthetic_collision_detected",
        "bm_copy_matches_experiment",
    )
    checks["all_ok"] = all(checks[k] is True for k in required)
    checks["required_keys"] = list(required)
    return checks


# ---------------------------------------------------------------------------
# Experiment families
# ---------------------------------------------------------------------------

def neighbour_arrays(rows):
    """l_t, r_t, x(t,-2), x(t,2) for t=0..T_MAX. Vacuum 0 off the packed word."""
    n = T_MAX + 1
    l = bytearray(n)
    r = bytearray(n)
    lm2 = bytearray(n)
    rp2 = bytearray(n)
    for t in range(n):
        z = rows[t]
        l[t] = x_of(z, t, -1)
        r[t] = x_of(z, t, 1)
        lm2[t] = x_of(z, t, -2)
        rp2[t] = x_of(z, t, 2)
    return l, r, lm2, rp2


def defect_window_fits(d) -> list[dict]:
    rows_out = []
    for w in range(1, W_MAX + 1):
        samples = []
        # Predict d_{t+1} from (d_t,...,d_{t-w+1}) at t=w..T_MAX.
        for t in range(w, T_MAX + 1):
            key = pack_window(d, t, w)
            samples.append((t, key, d[t + 1]))
        rec = fit_boolean(samples)
        rec["w"] = w
        rec["family"] = "defect_window"
        rec["key_bits"] = w
        rec["key_space"] = 1 << w
        rec["features"] = f"d_t..d_{{t-{w}+1}}"
        rec["all_keys_seen"] = rec["n_keys"] == (1 << w)
        rows_out.append(rec)
    return rows_out


def centre_and_leftover_fits(bits, d, l, r) -> list[dict]:
    """Boolean fits of d_{t+1} from c_{t-w..t} plus leftover neighbour bits."""
    # w is the lookback on the centre column: key uses c_{t-w}..c_t (w+1 bits).
    leftovers = (
        ("none", lambda t: 0, 0, False, False),
        ("l_t", lambda t: l[t], 1, True, False),
        ("r_t", lambda t: r[t], 1, False, True),
        ("l_t,r_t", lambda t: l[t] | (r[t] << 1), 2, True, True),
        ("l_t,r_t,l_{t-1},r_{t-1}", None, 4, True, True),  # special-cased
    )
    out = []
    for w in range(0, W_MAX + 1):
        c_width = w + 1
        t_lo = max(w, 1)
        for name, fn, extra_bits, uses_l, uses_r in leftovers:
            samples = []
            if name == "l_t,r_t,l_{t-1},r_{t-1}":
                for t in range(max(t_lo, 1), T_MAX + 1):
                    key = pack_forward(bits, t - w, c_width)
                    lefts = l[t] | ((l[t - 1] if t >= 1 else 0) << 1)
                    rights = r[t] | ((r[t - 1] if t >= 1 else 0) << 1)
                    key |= lefts << c_width
                    key |= rights << (c_width + 2)
                    samples.append((t, key, d[t + 1]))
                n_extra = 4
            else:
                for t in range(t_lo, T_MAX + 1):
                    key = pack_forward(bits, t - w, c_width)
                    key |= fn(t) << c_width
                    samples.append((t, key, d[t + 1]))
                n_extra = extra_bits
            rec = fit_boolean(samples)
            rec["w"] = w
            rec["family"] = "centre_leftover"
            rec["leftover"] = name
            rec["key_bits"] = c_width + n_extra
            rec["key_space"] = 1 << rec["key_bits"]
            rec["uses_current_left"] = uses_l
            rec["uses_current_right"] = uses_r
            rec["uses_light_cone"] = bool(uses_l or uses_r)
            rec["features"] = f"c_{{t-{w}..t}}+{name}"
            rec["all_keys_seen"] = rec["n_keys"] == rec["key_space"]
            out.append(rec)
    return out


def leftover_only_fits(bits, d, l, r) -> list[dict]:
    """Windows of leftover neighbours, targeting d_{t+1} and (for (l,r)) c_t."""
    out = []
    for w in range(1, W_MAX + 1):
        samples_lr = []
        samples_l = []
        samples_r = []
        samples_c = []
        for t in range(w, T_MAX + 1):
            key_l = pack_window(l, t, w)
            key_r = pack_window(r, t, w)
            key_lr = key_l | (key_r << w)
            samples_l.append((t, key_l, d[t + 1]))
            samples_r.append((t, key_r, d[t + 1]))
            samples_lr.append((t, key_lr, d[t + 1]))
            samples_c.append((t, key_lr, bits[t]))
        for name, samples, uses_l, uses_r, kbits, target in (
            ("l_t..l_{t-w+1}", samples_l, True, False, w, "d_{t+1}"),
            ("r_t..r_{t-w+1}", samples_r, False, True, w, "d_{t+1}"),
            ("(l,r)_t..(l,r)_{t-w+1}", samples_lr, True, True, 2 * w, "d_{t+1}"),
            ("(l,r) window reconstructs c_t", samples_c, True, True, 2 * w, "c_t"),
        ):
            rec = fit_boolean(samples)
            rec["w"] = w
            rec["family"] = "leftover_window"
            rec["leftover"] = name
            rec["target"] = target
            rec["key_bits"] = kbits
            rec["key_space"] = 1 << kbits
            rec["uses_current_left"] = uses_l
            rec["uses_current_right"] = uses_r
            rec["uses_light_cone"] = True
            rec["features"] = name
            rec["all_keys_seen"] = rec["n_keys"] == rec["key_space"]
            out.append(rec)
    return out


def spatial_radius_fits(rows, d, l, r):
    """Radius-k slice at time t versus d_{t+j} and next leftovers."""
    out = []
    for k in range(0, W_MAX + 1):
        for j in range(1, min(k + 3, W_MAX + 1) + 1):
            samples = []
            t_hi = T_MAX + 1 - j
            if t_hi < 8:
                continue
            for t in range(8, t_hi + 1):
                key, _width = spatial_window(rows[t], t, k)
                samples.append((t, key, d[t + j]))
            rec = fit_boolean(samples)
            rec["family"] = "spatial_radius"
            rec["radius"] = k
            rec["horizon"] = j
            rec["key_bits"] = 2 * k + 1
            rec["key_space"] = 1 << rec["key_bits"]
            rec["target"] = f"d_{{t+{j}}}"
            rec["cone_predicts"] = j <= k  # algebra: radius k determines d_{t+1}..d_{t+k}
            rec["uses_light_cone"] = k >= 1
            rec["features"] = f"x(t,{-k}..{k})"
            rec["all_keys_seen"] = rec["n_keys"] == rec["key_space"]
            out.append(rec)

    # Next leftover pair from radius-k slice.
    leftover_rows = []
    for k in range(0, 5):
        samples_l = []
        samples_r = []
        samples_pair = []
        for t in range(8, T_MAX):
            key, _w = spatial_window(rows[t], t, k)
            samples_l.append((t, key, l[t + 1]))
            samples_r.append((t, key, r[t + 1]))
            samples_pair.append((t, key, l[t + 1] | (r[t + 1] << 1)))
        for target, samples in (
            ("l_{t+1}", samples_l),
            ("r_{t+1}", samples_r),
            ("(l_{t+1},r_{t+1})", samples_pair),
        ):
            rec = fit_boolean(samples)
            rec["family"] = "next_leftover"
            rec["radius"] = k
            rec["key_bits"] = 2 * k + 1
            rec["key_space"] = 1 << rec["key_bits"]
            rec["target"] = target
            rec["uses_light_cone"] = k >= 1
            rec["algebra_closes"] = k >= 2
            rec["features"] = f"x(t,{-k}..{k})"
            leftover_rows.append(rec)
    return out, leftover_rows


def triple_history_fits(bits, d, l, r) -> list[dict]:
    """Does a bounded history of (l,c,r) close, i.e. determine the next triple?"""
    out = []
    for w in range(1, W_MAX + 1):
        samples_d = []
        samples_l = []
        samples_r = []
        samples_c = []
        for t in range(max(w - 1, 1), T_MAX):
            key = 0
            for i in range(w):
                ti = t - i
                triple = l[ti] | (bits[ti] << 1) | (r[ti] << 2)
                key |= triple << (3 * i)
            samples_d.append((t, key, d[t + 1]))
            samples_c.append((t, key, bits[t + 1]))
            samples_l.append((t, key, l[t + 1]))
            samples_r.append((t, key, r[t + 1]))
        for target, samples, algebra_ok in (
            ("d_{t+1}", samples_d, True),   # already determined by the last triple
            ("c_{t+1}", samples_c, True),
            ("l_{t+1}", samples_l, False),  # needs x(t,-2)
            ("r_{t+1}", samples_r, False),  # needs x(t,+2)
        ):
            rec = fit_boolean(samples)
            rec["family"] = "triple_history"
            rec["w"] = w
            rec["key_bits"] = 3 * w
            rec["key_space"] = 1 << rec["key_bits"]
            rec["target"] = target
            rec["algebra_closes"] = algebra_ok
            rec["uses_light_cone"] = True
            rec["features"] = f"(l,c,r)_{{t}}..t-{w}+1"
            out.append(rec)
    return out


def iid_defect_window_fits() -> list[dict]:
    rng = random.Random(IID_SEED)
    n = T_MAX + 2
    c = bytearray(rng.randrange(2) for _ in range(n))
    d = defect_indicators(c)
    rows_out = []
    for w in range(1, W_MAX + 1):
        samples = [(t, pack_window(d, t, w), d[t + 1]) for t in range(w, T_MAX + 1)]
        rec = fit_boolean(samples)
        rec["w"] = w
        rec["family"] = "iid_defect_window"
        rec["key_bits"] = w
        rec["key_space"] = 1 << w
        rec["features"] = f"iid d_t..d_{{t-{w}+1}}"
        rec["all_keys_seen"] = rec["n_keys"] == (1 << w)
        rows_out.append(rec)
    return rows_out


# ---------------------------------------------------------------------------
# Kill / markdown
# ---------------------------------------------------------------------------

def decide_kill(defect_rows, leftover_rows, radius_d, next_lr, triple_hist) -> dict:
    all_defect_mismatch = all(not r["consistent"] for r in defect_rows)
    any_defect_witnessed = any(r["witnessed_function"] for r in defect_rows)

    # Neighbour/centre fits that are witnessed functions.
    witnessed = [r for r in leftover_rows if r["witnessed_function"]]
    witnessed_without_cone = [r for r in witnessed if not r.get("uses_light_cone")]
    witnessed_with_cone = [r for r in witnessed if r.get("uses_light_cone")]

    # Radius-1 slice determines d_{t+1}; radius 0 does not.
    rad0_d1 = next(
        (r for r in radius_d if r["radius"] == 0 and r["horizon"] == 1),
        None,
    )
    rad1_d1 = next(
        (r for r in radius_d if r["radius"] == 1 and r["horizon"] == 1),
        None,
    )
    rad1_d2 = next(
        (r for r in radius_d if r["radius"] == 1 and r["horizon"] == 2),
        None,
    )
    rad2_next_lr = [
        r for r in next_lr
        if r["radius"] == 2 and r["target"] == "(l_{t+1},r_{t+1})"
    ]
    rad1_next_lr = [
        r for r in next_lr
        if r["radius"] == 1 and r["target"] == "(l_{t+1},r_{t+1})"
    ]
    triple_next_l = [
        r for r in triple_hist if r["target"] == "l_{t+1}"
    ]
    triple_next_r = [
        r for r in triple_hist if r["target"] == "r_{t+1}"
    ]
    leftover_does_not_close = (
        all(not r["witnessed_function"] for r in triple_next_l)
        and all(not r["witnessed_function"] for r in triple_next_r)
        and rad1_next_lr
        and not rad1_next_lr[0]["witnessed_function"]
        and rad2_next_lr
        and rad2_next_lr[0]["witnessed_function"]
    )
    needs_light_cone = (
        not witnessed_without_cone
        and bool(witnessed_with_cone)
        and rad0_d1 is not None
        and not rad0_d1["witnessed_function"]
        and rad1_d1 is not None
        and rad1_d1["witnessed_function"]
        and leftover_does_not_close
    )
    # Extra: radius 1 fails to determine d_{t+2} (window would have to grow).
    cone_grows = (
        rad1_d1 is not None
        and rad1_d1["witnessed_function"]
        and rad1_d2 is not None
        and not rad1_d2["consistent"]
    )
    kill = all_defect_mismatch or needs_light_cone
    parts = []
    if all_defect_mismatch:
        firsts = ", ".join(
            f"w={r['w']} at t={r['first_mismatch']['t']}"
            if r["first_mismatch"] else f"w={r['w']}"
            for r in defect_rows
        )
        parts.append(
            "every defect window w=1..8 mismatches on the prize seed through "
            f"t=4096 ({firsts}); d is not a width-<=8 CA / finite-memory shift"
        )
    if needs_light_cone:
        parts.append(
            "d_{t+1} is a witnessed Boolean of the radius-1 slice (c_t,l_t,r_t) "
            "but not of any centre-only window; the leftover pair (l,r) does not "
            "close on a bounded history of triples (next leftovers need x(t,±2), "
            "the original light cone)"
        )
    if cone_grows:
        parts.append(
            "radius 1 determines d_{t+1} and fails for d_{t+2}, so any longer "
            "horizon secretly grows the spatial window"
        )
    reason = ". ".join(p[0].upper() + p[1:] if p else p for p in parts)
    reason = reason + ". Not a prize claim."
    return {
        "kill": kill,
        "survive": (not kill) and any_defect_witnessed,
        "all_defect_windows_mismatch": all_defect_mismatch,
        "any_defect_window_witnessed": any_defect_witnessed,
        "needs_light_cone": needs_light_cone,
        "cone_grows": cone_grows,
        "leftover_does_not_close": leftover_does_not_close,
        "n_witnessed_without_cone": len(witnessed_without_cone),
        "n_witnessed_with_cone": len(witnessed_with_cone),
        "reason": reason,
        "text": (
            "Preregistered kill: every window w=1..8 of previous defects has a "
            "mismatch (the defect sequence is not itself a low-order CA / shift "
            "of finite memory), or fitting d_{t+1} from (c_{t-w..t}, leftover "
            "neighbour bits) secretly needs the light cone. "
            + ("Both fired. " if all_defect_mismatch and needs_light_cone else "")
            + reason
        ),
    }


def write_markdown(payload: dict) -> str:
    kill = payload["kill"]
    checks = payload["checks"]
    drows = payload["defect_windows"]
    crows = payload["centre_leftover"]
    lrows = payload["leftover_windows"]
    rad = payload["spatial_radius"]
    next_left_over = payload["next_leftover"]
    th = payload["triple_history"]
    iid = payload["iid_defect_windows"]
    bm = payload["berlekamp_massey"]
    lines = []
    a = lines.append
    a("# Defect recurrence: local Boolean fits")
    a("")
    a(
        "This note is ideas13 item 2 (leftover ideas11 item 5 / ideas12 "
        "item 3; prize Problem 2). It does **not** prove `D(N)=o(N)`, and "
        "it does not claim a prize result."
    )
    a("")
    a("Helper: `research/defect_recurrence.py --certify`. Dump:")
    a("`research/defect_recurrence.json`. Packed evolution is the same")
    a("engine as `experiment.center_bits`; that file is not modified.")
    a("")
    a("## Attack")
    a("")
    a("Cycle K wrote `D(N) = sum_{t<N} (2 c_t - 1)` as the signed sum of")
    a("the centre at **defect** times `t` with `c_t = c_{t-1}`, plus an")
    a("`O(1)` endpoint from the alternating positions:")
    a("")
    a("```")
    a("D_alt(N) = (σ_0 + σ_{N-1}) / 2  ∈  {-1, 0, +1},")
    a("D(N)     = D_defects(N) + D_alt(N).")
    a("```")
    a("")
    a(
        f"On the length-`4096` centre prefix that identity holds with "
        f"`D={checks['D_at_4096']}`, "
        f"`D_defects={checks['D_defects_at_4096']}`, "
        f"`D_alt={checks['D_alt_at_4096']}` "
        "(same `D(4096)=-40` as [xor_transform.md](xor_transform.md)). "
        "The defect sequence still has Berlekamp–Massey "
        f"`L({bm['n_defects']})={bm['L_defects']}` so "
        f"`L/n={bm['L_defects']/bm['n_defects']:.4f} ~ 1/2`, matching "
        f"`L(c)={bm['L_centre']}` on the same length "
        f"(`L/n={bm['L_centre']/bm['n_centre']:.4f}`)."
    )
    a("")
    a("A *local* recurrence for `d_t = 1_{c_t=c_{t-1}}` would still be a")
    a("Problem 2 handle if it closed on a bounded window (a cellular")
    a("automaton or finite-memory shift on `d`, or on `(c,l,r)` without")
    a("growing the spatial slice). Then the signed sum of `d` would be a")
    a("function of a finite state, and one could hope to bound `D(N)`.")
    a("")
    a("**Kill:** every defect window `w=1..8` mismatches on the prize seed")
    a("through `t=4096` (so `d` is not a low-order CA), or the only")
    a("Boolean fits from `c_{t-w..t}` plus leftover neighbour bits secretly")
    a("need the light cone.")
    a("")
    a("## Local algebra")
    a("")
    a("Rule 30 is `x(t+1,j) = x(t,j-1) XOR (x(t,j) OR x(t,j+1))`. Write")
    a("`l_t = x(t,-1)`, `c_t = x(t,0)`, `r_t = x(t,1)`. Then")
    a("")
    a(r"\[")
    a(r"c_{t+1}=l_t\oplus(c_t\lor r_t),\qquad")
    a(r"d_{t+1}=1_{c_{t+1}=c_t}.")
    a(r"\]")
    a("")
    a("The eight triples:")
    a("")
    a("| `c` | `l` | `r` | `c_{t+1}` | `d_{t+1}` |")
    a("|---:|---:|---:|---:|---:|")
    for c in (0, 1):
        for lv in (0, 1):
            for rv in (0, 1):
                c_next = lv ^ (c | rv)
                dd = int(c_next == c)
                a(f"| {c} | {lv} | {rv} | {c_next} | {dd} |")
    a("")
    a("Closed form: if `c_t=1` then `d_{t+1} = NOT l_t` (right neighbour")
    a("drops out); if `c_t=0` then `d_{t+1} = 1_{l_t=r_t}`. So `d_{t+1}`")
    a("**is** a Boolean of the radius-1 slice. The leftover pair does not")
    a("close:")
    a("")
    a(r"\[")
    a(r"l_{t+1}=x(t,-2)\oplus(l_t\lor c_t),\qquad")
    a(r"r_{t+1}=c_t\oplus(r_t\lor x(t,2)).")
    a(r"\]")
    a("")
    a("Next leftovers need `x(t,±2)`. A bounded history of `(l,c,r)` is a")
    a("bounded spacetime diamond; the missing bits sit on the light cone.")
    a("Radius `k` at time `t` determines `d_{t+1},…,d_{t+k}` and fails at")
    a("`d_{t+k+1}` — the original CA window.")
    a("")
    a("## Engine")
    a("")
    a("Packing is `experiment.py`: `z_0=1`, `z=(z<<2)^((z<<1)|z)`,")
    a("`x(t,j)=(z>>(j+t))&1`. The centre is bit `t`; leftovers sit at")
    a("indices `t-1` and `t+1`. Centre bits match `experiment.center_bits`")
    a(f"through `{T_MAX + 1}`, including the known 20-bit word")
    a("`11011100110001011001`. An independent live-cell spacetime agrees")
    a("on `c`, `l`, `r`, `x(t,±2)` for `t=0..64`. The three-bit formula")
    a("matches `c_{t+1}` and `d_{t+1}` for `t=1..4096`. The prefix-16")
    a("defects are the seven times `1,4,5,7,9,11,12` recorded in")
    a("[period2_defects.md](period2_defects.md). Synthetic `01` has a")
    a("width-1 rule `d_{t+1}=0`; constant `1` has `d_{t+1}=1`; a")
    a("period-2 defect stream has `d_{t+1}=NOT d_t`. A forced collision")
    a("is detected. Copied Berlekamp–Massey agrees with")
    a("`experiment.linear_complexity` on a 40-bit sample.")
    a("")
    a("A Boolean fit on a finite prefix is a **witnessed function** only")
    a("if some key is reused and every reuse agrees. Unique keys are not")
    a("evidence (birthday / injective fingerprint of the triangle).")
    a("")
    a("## Defect windows `w=1..8`")
    a("")
    a("Predict `d_{t+1}` from `(d_t,…,d_{t-w+1})` at `t=w..4096` on the")
    a("prize seed. iid fair bits (seed `20260911`) are a noise control.")
    a("")
    a(
        "| w | keys | reused | colliding | consistent | witnessed | "
        "maj acc | first mismatch | iid mismatch |"
    )
    a("|---:|---:|---:|---:|---|---|---:|---|---|")
    iid_by_w = {r["w"]: r for r in iid}
    for rec in drows:
        iw = iid_by_w[rec["w"]]
        a(
            "| {w} | {nk} | {nr} | {nc} | {cons} | {wit} | {acc} | {mm} | {imm} |".format(
                w=rec["w"],
                nk=rec["n_keys"],
                nr=rec["n_reused_keys"],
                nc=rec["n_colliding_keys"],
                cons=yn(rec["consistent"]),
                wit=yn(rec["witnessed_function"]),
                acc=fmt_acc(rec["majority_accuracy"]),
                mm=fmt_mm(rec),
                imm=fmt_mm(iw),
            )
        )
    a("")
    a(
        "Every prize-seed window collides, with reuse (so the collision is "
        "real) and first mismatch at small `t`. Majority-vote accuracy "
        "stays near `1/2`, as on iid defects. Width 8 has `2^8=256` keys "
        "and thousands of samples; it is not an undersampled lookup. The "
        "defect sequence is not a cellular automaton of memory `≤8`."
    )
    a("")
    a("## Centre window plus leftover neighbours")
    a("")
    a("Predict `d_{t+1}` from `c_{t-w..t}` and leftover neighbour bits")
    a("(cells adjacent to the centre, not already in the centre column).")
    a("Every row is listed; witnessed functions are those with reuse and")
    a("no colliding keys.")
    a("")
    a(
        "| w | leftover | key bits | reused | colliding | witnessed | "
        "maj acc | first mismatch | cone |"
    )
    a("|---:|---|---:|---:|---:|---|---:|---|---|")
    for rec in crows:
        a(
            "| {w} | `{lef}` | {kb} | {nr} | {nc} | {wit} | {acc} | {mm} | {cone} |".format(
                w=rec["w"],
                lef=rec["leftover"],
                kb=rec["key_bits"],
                nr=rec["n_reused_keys"],
                nc=rec["n_colliding_keys"],
                wit=yn(rec["witnessed_function"]),
                acc=fmt_acc(rec["majority_accuracy"]),
                mm=fmt_mm(rec),
                cone=yn(rec["uses_light_cone"]),
            )
        )
    a("")
    a("Centre-only windows (`leftover=none`) all mismatch. Adding only")
    a("`l_t` or only `r_t` still mismatches: algebra needs `r` when")
    a("`c=0` and needs `l` when `c=1`. Adding the current pair")
    a("`(l_t, r_t)` is a witnessed function for every `w` — that is the")
    a("radius-1 slice, i.e. the original local rule, not a closed")
    a("recurrence on the centre column. A one-step history of leftovers")
    a("`l_t,r_t,l_{t-1},r_{t-1}` also works, because it contains the")
    a("current pair; it does not remove the cone.")
    a("")
    a("Windows of leftovers without the centre column:")
    a("")
    a(
        "| w | leftover | target | key bits | reused | colliding | "
        "witnessed | maj acc | first mismatch |"
    )
    a("|---:|---|---|---:|---:|---:|---|---:|---|")
    for rec in lrows:
        a(
            "| {w} | `{lef}` | `{tgt}` | {kb} | {nr} | {nc} | {wit} | {acc} | {mm} |".format(
                w=rec["w"],
                lef=rec["leftover"],
                tgt=rec.get("target", "d_{t+1}"),
                kb=rec["key_bits"],
                nr=rec["n_reused_keys"],
                nc=rec["n_colliding_keys"],
                wit=yn(rec["witnessed_function"]),
                acc=fmt_acc(rec["majority_accuracy"]),
                mm=fmt_mm(rec),
            )
        )
    a("")
    lr_d = [
        r for r in lrows
        if r.get("target") == "d_{t+1}" and r["leftover"].startswith("(l,r)")
    ]
    lr_c = [r for r in lrows if r.get("target") == "c_t"]
    last_fail = next((r for r in reversed(lr_d) if not r["consistent"]), None)
    first_ok = next((r for r in lr_d if r["witnessed_function"]), None)
    c_ok = next((r for r in lr_c if r["witnessed_function"]), None)
    bits_txt = []
    bits_txt.append(
        "A single leftover pair `(l_t,r_t)` does not determine `d_{t+1}` "
        "(the truth table already splits on `c`)."
    )
    if last_fail is not None:
        mm = last_fail["first_mismatch"]
        bits_txt.append(
            "Width-`{}` leftover pair histories still collide (first "
            "mismatch `t={}`).".format(last_fail["w"], mm["t"] if mm else "?")
        )
    if first_ok is not None:
        bits_txt.append(
            "Width `{}` of `(l,r)` is consistent on this prefix "
            "(`{}` reused keys): that is `{}` light-cone bits, and the "
            "required memory grew through the smaller widths.".format(
                first_ok["w"],
                first_ok["n_reused_keys"],
                first_ok["key_bits"],
            )
        )
    if c_ok is not None:
        bits_txt.append(
            "The same leftover window reconstructs `c_t` at width "
            "`{}` (witnessed). That is reading the centre back out of "
            "the cone, not a closed defect rule.".format(c_ok["w"])
        )
    else:
        bits_txt.append(
            "The leftover window does not reconstruct `c_t` on any "
            "scanned width; any apparent `d_{t+1}` fit still uses the cone."
        )
    bits_txt.append(
        "Algebra still needs `c_t`; a growing leftover history is the "
        "original triangle."
    )
    a(" ".join(bits_txt))
    a("")
    a("## Light cone and closing of leftovers")
    a("")
    a("Spatial slice `x(t,-k)..x(t,k)` at times `t=8..` versus `d_{t+j}`")
    a("and versus the next leftover pair. Algebra: radius `k` determines")
    a("`d_{t+1}..d_{t+k}` and the next leftovers iff `k≥2`.")
    a("")
    a("| radius | target | key bits | colliding | witnessed | algebra |")
    a("|---:|---|---:|---:|---|---|")
    shown = []
    for rec in rad:
        if rec["horizon"] <= rec["radius"] + 2 and rec["radius"] <= 4:
            shown.append(rec)
    for rec in shown:
        a(
            "| {k} | `{tgt}` | {kb} | {nc} | {wit} | {alg} |".format(
                k=rec["radius"],
                tgt=rec["target"],
                kb=rec["key_bits"],
                nc=rec["n_colliding_keys"],
                wit=yn(rec["witnessed_function"]),
                alg=yn(rec["cone_predicts"]),
            )
        )
    a("")
    a("Next leftovers from a radius-`k` slice:")
    a("")
    a("| radius | target | colliding | witnessed | algebra closes |")
    a("|---:|---|---:|---|---|")
    for rec in next_left_over:
        a(
            "| {k} | `{tgt}` | {nc} | {wit} | {alg} |".format(
                k=rec["radius"],
                tgt=rec["target"],
                nc=rec["n_colliding_keys"],
                wit=yn(rec["witnessed_function"]),
                alg=yn(rec["algebra_closes"]),
            )
        )
    a("")
    a("Bounded history of the triple `(l_t,c_t,r_t)`:")
    a("")
    a("| w | target | key bits | colliding | witnessed | algebra closes |")
    a("|---:|---|---:|---:|---|---|")
    for rec in th:
        a(
            "| {w} | `{tgt}` | {kb} | {nc} | {wit} | {alg} |".format(
                w=rec["w"],
                tgt=rec["target"],
                kb=rec["key_bits"],
                nc=rec["n_colliding_keys"],
                wit=yn(rec["witnessed_function"]),
                alg=yn(rec["algebra_closes"]),
            )
        )
    a("")
    a("Radius 0 (the centre bit) does not determine `d_{t+1}`. Radius 1")
    a("does, and fails for `d_{t+2}`. Radius 1 does not determine")
    a("`(l_{t+1},r_{t+1})`; radius 2 does. A history of `w≤8` triples")
    a("determines `d_{t+1}` and `c_{t+1}` (they sit in the last triple)")
    a("and never determines the next leftovers. The state `(l,c,r)` is")
    a("not closed. Extending the horizon grows the spatial window: that")
    a("is the Rule 30 light cone, not a defect CA.")
    a("")
    a("## Why it died")
    a("")
    a(kill["text"])
    a("")
    a("Cycle K already killed density / linear-complexity shortcuts.")
    a("This freeze kills the remaining local-recurrence hope: `d` is not")
    a("a width-`≤8` Boolean CA, and the only exact local rule for")
    a("`d_{t+1}` is the original three-bit slice, whose leftovers do not")
    a("close. Finite evidence on the prize prefix through `t=4096`. Not")
    a("a prize claim.")
    a("")
    a("## Verdict")
    a("")
    a(
        "`{status}`, wall time {sec:.2f}s.".format(
            status="KILL" if kill["kill"] else "SURVIVE",
            sec=payload["elapsed_sec"],
        )
    )
    a("")
    a(f"- Kill: {yn(kill['kill'])}.")
    a(f"- Survive: {yn(kill['survive'])}.")
    a(f"- Reason: {kill['reason']}")
    a("")
    a("## Files")
    a("")
    a("- `research/defect_recurrence.md` (this note)")
    a("- `research/defect_recurrence.py` (`--certify` runs the checks and the freeze)")
    a("- `research/defect_recurrence.json` (dump)")
    a("")
    a(
        "Self-check: packed centre agrees with `experiment.center_bits` "
        f"on 256 bits and on `0..{T_MAX + 1}`; "
        f"`checks.all_ok={checks['all_ok']}`."
    )
    a("")
    return "\n".join(lines) + "\n"


def jsonable(x):
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    if isinstance(x, tuple):
        return [jsonable(y) for y in x]
    if isinstance(x, list):
        return [jsonable(y) for y in x]
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    return x


def drop_key_space_tables(rows: list[dict]) -> list[dict]:
    """JSON already stores counts, not the 2^w lookup tables."""
    return [compact_fit(r) for r in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--certify", action="store_true", help="run checks and write dump")
    args = parser.parse_args()
    if not args.certify:
        args.certify = True

    t0 = time.time()
    rows, bits = packed_rows_and_bits(T_MAX)
    l, r, lm2, rp2 = neighbour_arrays(rows)
    d = defect_indicators(bits)
    checks = self_check(rows, bits, d, l, r, lm2, rp2)
    if not checks["all_ok"]:
        failed = [
            k for k in checks["required_keys"]
            if checks.get(k) is not True
        ]
        raise AssertionError(f"self-check failed: {failed}")

    defect_rows = defect_window_fits(d)
    centre_rows = centre_and_leftover_fits(bits, d, l, r)
    leftover_rows = leftover_only_fits(bits, d, l, r)
    radius_d, next_lr = spatial_radius_fits(rows, d, l, r)
    triple_hist = triple_history_fits(bits, d, l, r)
    iid_rows = iid_defect_window_fits()

    d_seq = list(d[1: BM_N + 1])
    c_seq = list(bits[:BM_N])
    L_d = linear_complexity(d_seq)
    L_c = linear_complexity(c_seq)
    L_d_exp, _ = experiment_linear_complexity(d_seq)
    L_c_exp, _ = experiment_linear_complexity(c_seq)
    if L_d != L_d_exp or L_c != L_c_exp:
        raise AssertionError("BM mismatch versus experiment.linear_complexity")
    bm = {
        "n_defects": BM_N,
        "n_centre": BM_N,
        "L_defects": L_d,
        "L_centre": L_c,
        "L_defects_over_n": L_d / BM_N,
        "L_centre_over_n": L_c / BM_N,
        "defects_L_near_N_over_2": L_d / BM_N >= KILL_L_RATIO,
        "matches_experiment_linear_complexity": True,
    }

    kill = decide_kill(
        defect_rows,
        centre_rows + leftover_rows,
        radius_d,
        next_lr,
        triple_hist,
    )

    elapsed = time.time() - t0
    payload = {
        "attack": "defect_recurrence",
        "ideas": "ideas13 item 2 / leftover ideas11 item 5 / leftover ideas12 item 3",
        "problem": 2,
        "t_max": T_MAX,
        "w_max": W_MAX,
        "prize_prefix16": PRIZE_PREFIX16,
        "prize_prefix20": PRIZE_PREFIX20,
        "kill": jsonable(kill),
        "checks": jsonable(checks),
        "berlekamp_massey": bm,
        "defect_windows": jsonable(drop_key_space_tables(defect_rows)),
        "centre_leftover": jsonable(drop_key_space_tables(centre_rows)),
        "leftover_windows": jsonable(drop_key_space_tables(leftover_rows)),
        "spatial_radius": jsonable(drop_key_space_tables(radius_d)),
        "next_leftover": jsonable(drop_key_space_tables(next_lr)),
        "triple_history": jsonable(drop_key_space_tables(triple_hist)),
        "iid_defect_windows": jsonable(drop_key_space_tables(iid_rows)),
        "elapsed_sec": elapsed,
        "not_a_prize_claim": True,
    }
    md = write_markdown(payload)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    OUT_MD.write_text(md)
    print(md)
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    if not kill["kill"]:
        raise SystemExit("expected KILL; freeze did not fire")


if __name__ == "__main__":
    main()
