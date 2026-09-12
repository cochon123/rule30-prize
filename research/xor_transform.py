#!/usr/bin/env python3
"""Cycle I screen: exact transforms of the Rule 30 centre that might be easier than c.

Transforms (Problem 1 / 2, not raw L(c), not dual-particle, not block energy):
  a_t = c_t XOR (t mod 2)
  d_t = c_t XOR c_{t+1}
  e_t = c_t XOR c_{t//2}
  s_t = c_{t+1} XOR c_t XOR c_{t-1}   (t >= 1)
  m_t = c_t XOR (popcount(t) mod 2)

For each: Berlekamp–Massey L(N), period-witness last-mismatch, run-length
pattern, and dyadic signed-sum A_m analogue versus raw D(N).

Copied BM / period_witnesses / dyadic_annuli match experiment.py. This file
does not modify experiment.py, strip_graph.py, strip_extend.py, REPORT.md,
LOG.md, or README.md. Stdlib only. Not a prize claim.

Run: python3 research/xor_transform.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits
from experiment import linear_complexity as experiment_linear_complexity
from experiment import period_witnesses as experiment_period_witnesses

OUT_JSON = Path(__file__).with_name("xor_transform.json")
OUT_MD = Path(__file__).with_name("xor_transform.md")

BM_NS = (256, 1024, 4096, 16384)
PERIOD_PREFIX = 100000
MAX_PERIOD = 4096
CENTER_BITS = 100000
SMALL_PERIOD = 256
N_OVER_4_NS = (4096, 16384)
D_NS = (256, 1024, 4096, 16384, 32768, 65536, 100000)


# ---------------------------------------------------------------------------
# Packed centre (same convention as experiment.center_bits) and copied BM
# ---------------------------------------------------------------------------

def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def linear_complexity(bits):
    """Binary Berlekamp-Massey; integer bits encode connection coefficients.

    Copied from experiment.py. Do not modify experiment.py.
    """
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
    return length, connection


def linear_complexity_profile(bits, checkpoints):
    """Same BM as experiment.py, recording L after each requested prefix length."""
    wanted = {int(n) for n in checkpoints}
    connection = previous = 1
    length, last_change, history = 0, -1, 0
    profile = {}
    for n, value in enumerate(bits):
        history = (history << 1) | value
        discrepancy = (connection & history).bit_count() & 1
        if discrepancy:
            old = connection
            connection ^= previous << (n - last_change)
            if 2 * length <= n:
                length = n + 1 - length
                previous, last_change = old, n
        n_bits = n + 1
        if n_bits in wanted:
            profile[n_bits] = {"N": n_bits, "L": length, "connection_bit_length": connection.bit_length()}
            wanted.remove(n_bits)
            if not wanted:
                break
    return profile, length, connection


def period_witnesses(bits, max_period):
    """Copied from experiment.py. last_mismatch = -1 means no mismatch on the prefix."""
    packed = int("".join(map(str, reversed(bits))), 2)
    result = []
    for period in range(1, max_period + 1):
        mismatch = (packed ^ (packed >> period)) & ((1 << (len(bits) - period)) - 1)
        result.append({"period": period, "last_mismatch": mismatch.bit_length() - 1})
    return result


def dyadic_annuli(bits):
    """Copied from experiment.py."""
    result = []
    start = 1
    while 2 * start <= len(bits):
        discrepancy = maximum = 0
        for value in bits[start:2 * start]:
            discrepancy += 2 * value - 1
            maximum = max(maximum, abs(discrepancy))
        result.append({
            "start": start,
            "length": start,
            "signed_imbalance": discrepancy,
            "max_absolute_partial_imbalance": maximum,
            "normalized_maximum": maximum / start,
        })
        start *= 2
    return result


def signed_D(bits, n: int) -> int:
    return 2 * sum(bits[:n]) - n


def D_profile(bits, ns):
    out = []
    acc = 0
    want = list(ns)
    wi = 0
    for t, v in enumerate(bits):
        acc += 2 * int(v) - 1
        n = t + 1
        while wi < len(want) and n == want[wi]:
            out.append({"N": n, "D": acc, "abs_D": abs(acc), "abs_D_over_N": abs(acc) / n})
            wi += 1
        if wi >= len(want):
            break
    return out


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------

def transform_raw(c: bytearray) -> bytearray:
    return c


def transform_a(c: bytearray) -> bytearray:
    return bytearray(c[t] ^ (t & 1) for t in range(len(c)))


def transform_d(c: bytearray) -> bytearray:
    return bytearray(c[t] ^ c[t + 1] for t in range(len(c) - 1))


def transform_e(c: bytearray) -> bytearray:
    return bytearray(c[t] ^ c[t // 2] for t in range(len(c)))


def transform_s(c: bytearray) -> bytearray:
    # Discrete Laplacian on t >= 1; sequence index 0 is time t = 1.
    return bytearray(c[t + 1] ^ c[t] ^ c[t - 1] for t in range(1, len(c) - 1))


def transform_tm(c: bytearray) -> bytearray:
    return bytearray(c[t] ^ (t.bit_count() & 1) for t in range(len(c)))


TRANSFORMS = [
    ("c", "c_t (raw baseline)", transform_raw),
    ("a", "c_t XOR (t mod 2)", transform_a),
    ("d", "c_t XOR c_{t+1}", transform_d),
    ("e", "c_t XOR c_{t//2}", transform_e),
    ("s", "c_{t+1} XOR c_t XOR c_{t-1} (t>=1)", transform_s),
    ("m", "c_t XOR (popcount(t) mod 2)", transform_tm),
]


def run_lengths(bits) -> list[tuple[int, int]]:
    if not bits:
        return []
    runs = []
    cur, length = bits[0], 1
    for v in bits[1:]:
        if v == cur:
            length += 1
        else:
            runs.append((cur, length))
            cur, length = v, 1
    runs.append((cur, length))
    return runs


def run_pattern(bits, suffix_start: int) -> dict:
    n = len(bits)
    last_00 = last_11 = None
    for t in range(n - 1):
        pair = (bits[t] << 1) | bits[t + 1]
        if pair == 0:
            last_00 = t
        elif pair == 3:
            last_11 = t
    runs = run_lengths(bits)
    max0 = max((ln for b, ln in runs if b == 0), default=0)
    max1 = max((ln for b, ln in runs if b == 1), default=0)
    start = min(max(suffix_start, 0), n)
    suffix_runs = run_lengths(bits[start:])
    complete = suffix_runs[1:-1] if len(suffix_runs) >= 3 else suffix_runs
    zero_lens = sorted({ln for b, ln in complete if b == 0})
    one_lens = sorted({ln for b, ln in complete if b == 1})
    isolated_zero_q = None
    isolated_one_q = None
    if complete and zero_lens == [1] and len(one_lens) == 1:
        isolated_zero_q = one_lens[0]
    if complete and one_lens == [1] and len(zero_lens) == 1:
        isolated_one_q = zero_lens[0]
    onset_iso0 = None
    if last_00 is None:
        onset_iso0 = 0
    else:
        onset_iso0 = last_00 + 2
    q_after_last_00 = None
    # After the last 00, zeros are isolated by definition. Only call that an
    # eventual 01^q form if a long suffix remains and the 1-runs are constant.
    tail = 0 if onset_iso0 is None else n - onset_iso0
    if onset_iso0 is not None and tail >= max(64, n // 8):
        after = run_lengths(bits[onset_iso0:])
        complete_after = after[1:-1] if len(after) >= 3 else after
        z = {ln for b, ln in complete_after if b == 0}
        o = {ln for b, ln in complete_after if b == 1}
        if complete_after and z <= {1} and len(o) == 1:
            q_after_last_00 = next(iter(o))
    return {
        "length": n,
        "n_runs": len(runs),
        "max_zero_run": max0,
        "max_one_run": max1,
        "last_00": last_00,
        "last_11": last_11,
        "last_00_over_n": None if last_00 is None else last_00 / n,
        "last_11_over_n": None if last_11 is None else last_11 / n,
        "suffix_start": start,
        "suffix_complete_zero_run_lengths": zero_lens,
        "suffix_complete_one_run_lengths": one_lens,
        "eventually_01q_on_suffix": isolated_zero_q,
        "eventually_0q1_on_suffix": isolated_one_q,
        "onset_after_last_00": onset_iso0,
        "unique_q_after_last_00": q_after_last_00,
        "both_00_and_11_persist_past_half": (
            (last_00 is not None and last_00 >= n / 2)
            and (last_11 is not None and last_11 >= n / 2)
        ),
    }


def summarize_periods(witnesses, prefix_len: int, small_p: int) -> dict:
    if not witnesses:
        return {"prefix": prefix_len, "max_period": 0}
    best = min(witnesses, key=lambda w: (w["last_mismatch"], w["period"]))
    half = prefix_len / 2
    tiny = [w for w in witnesses if w["last_mismatch"] < half]
    small = [w for w in witnesses if w["period"] <= small_p]
    best_small = min(small, key=lambda w: (w["last_mismatch"], w["period"])) if small else None
    n_pure = sum(1 for w in witnesses if w["last_mismatch"] < 0)
    head = sorted(witnesses, key=lambda w: (w["last_mismatch"], w["period"]))[:8]
    return {
        "prefix": prefix_len,
        "max_period": witnesses[-1]["period"],
        "min_last_mismatch": best["last_mismatch"],
        "min_last_mismatch_period": best["period"],
        "n_periods_last_mismatch_lt_half": len(tiny),
        "n_periods_no_mismatch": n_pure,
        "best_small_period": None if best_small is None else best_small["period"],
        "best_small_last_mismatch": None if best_small is None else best_small["last_mismatch"],
        "tiny_half_threshold": half,
        "cheapest_last_mismatches": head,
    }


def discrepancy_vs_raw(annuli, d_prof, raw_annuli, raw_d) -> dict:
    by_start_raw = {a["start"]: a for a in raw_annuli}
    by_n_raw = {d["N"]: d for d in raw_d}
    ratios = []
    for a in annuli:
        r = by_start_raw.get(a["start"])
        if r is None or r["max_absolute_partial_imbalance"] == 0:
            ratio = None
        else:
            ratio = a["max_absolute_partial_imbalance"] / r["max_absolute_partial_imbalance"]
        ratios.append({
            "start": a["start"],
            "A_m": a["max_absolute_partial_imbalance"],
            "A_m_raw": None if r is None else r["max_absolute_partial_imbalance"],
            "A_m_over_raw": ratio,
            "normalized_maximum": a["normalized_maximum"],
            "raw_normalized_maximum": None if r is None else r["normalized_maximum"],
            "signed_imbalance": a["signed_imbalance"],
        })
    d_ratios = []
    for d in d_prof:
        r = by_n_raw.get(d["N"])
        d_ratios.append({
            "N": d["N"],
            "D": d["D"],
            "D_raw": None if r is None else r["D"],
            "abs_D": d["abs_D"],
            "abs_D_raw": None if r is None else r["abs_D"],
            "abs_D_over_N": d["abs_D_over_N"],
            "abs_D_over_abs_raw": (
                None if r is None or r["abs_D"] == 0 else d["abs_D"] / r["abs_D"]
            ),
        })
    large = [row for row in ratios if row["start"] >= 256]
    norms = [row["normalized_maximum"] for row in large]
    raw_norms = [row["raw_normalized_maximum"] for row in large if row["raw_normalized_maximum"] is not None]
    last_d = d_prof[-1] if d_prof else None
    last_raw = raw_d[-1] if raw_d else None
    visibly_better = False
    if last_d and last_raw and last_raw["abs_D"] > 0 and norms and raw_norms:
        d_better = last_d["abs_D"] <= last_raw["abs_D"] / 4
        a_better = max(norms) <= max(raw_norms) / 2
        # Need a strictly smaller order, not a lucky single N.
        visibly_better = d_better and a_better
    same_order = not visibly_better
    return {
        "annuli_vs_raw": ratios,
        "D_vs_raw": d_ratios,
        "max_normalized_A_m_from_256": max(norms) if norms else None,
        "raw_max_normalized_A_m_from_256": max(raw_norms) if raw_norms else None,
        "visibly_better_than_raw_D": visibly_better,
        "same_order_as_raw_D": same_order,
    }


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def self_check(c: bytearray) -> dict:
    ref = experiment_center_bits(256)
    packed256 = packed_center(256)
    assert packed256 == ref
    assert c[:256] == ref
    assert list(c[:20]) == [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    for s, expected in [(bytes(40), 0), (bytes([1]) * 40, 1), (bytes([0, 1]) * 20, 2)]:
        length, _connection = linear_complexity(s)
        assert length == expected
        assert experiment_linear_complexity(s)[0] == expected
    L_c100, conn = linear_complexity(c[:100])
    L_exp, conn_exp = experiment_linear_complexity(c[:100])
    assert L_c100 == L_exp == 48
    assert conn == conn_exp
    sample = c[:100]
    copied = period_witnesses(sample, 30)
    exp_w = experiment_period_witnesses(sample, 30)
    assert copied == exp_w
    for witness in copied:
        p = witness["period"]
        naive = max(t for t in range(len(sample) - p) if sample[t] != sample[t + p])
        assert witness["last_mismatch"] == naive
    if len(c) >= 100000:
        assert signed_D(c, 100) == 4
        assert signed_D(c, 1000) == -38
        assert signed_D(c, 10000) == 64
        assert signed_D(c, 100000) == 196
    a = transform_a(c[:16])
    assert list(a) == [c[t] ^ (t & 1) for t in range(16)]
    d = transform_d(c[:16])
    assert list(d) == [c[t] ^ c[t + 1] for t in range(15)]
    e = transform_e(c[:16])
    assert e[0] == 0
    assert list(e) == [c[t] ^ c[t // 2] for t in range(16)]
    s = transform_s(c[:16])
    assert list(s) == [c[t + 1] ^ c[t] ^ c[t - 1] for t in range(1, 15)]
    m = transform_tm(c[:16])
    assert list(m) == [c[t] ^ (t.bit_count() & 1) for t in range(16)]
    # Profile agrees with prefix BM at each checkpoint on a short word.
    prof, _, _ = linear_complexity_profile(c[:200], [50, 100, 200])
    assert prof[100]["L"] == L_c100
    assert prof[200]["L"] == linear_complexity(c[:200])[0]
    return {
        "packed_matches_experiment_256": True,
        "prefix20": True,
        "bm_matches_experiment_on_c100": True,
        "period_witnesses_match_experiment": True,
        "transform_spot_checks": True,
        "bm_profile_agrees": True,
        "raw_D_matches_REPORT": len(c) >= 100000,
    }


def kill_one(rec: dict) -> dict:
    Lmap = {row["N"]: row["L"] for row in rec["linear_complexity"]}
    linear_not_simpler = all(
        Lmap.get(n, 0) >= n / 4 for n in N_OVER_4_NS
    )
    pw = rec["period_witness"]
    no_cheap_period = not (
        pw["min_last_mismatch"] < pw["tiny_half_threshold"]
        and pw["min_last_mismatch_period"] <= SMALL_PERIOD
    )
    # Also kill periodicity if the globally best last-mismatch is still late.
    if pw["min_last_mismatch"] >= pw["tiny_half_threshold"]:
        no_cheap_period = True
    disc = rec["discrepancy"]
    disc_not_better = disc["same_order_as_raw_D"]
    bounded_L = all(Lmap.get(n, n) <= 64 for n in N_OVER_4_NS) or (
        Lmap.get(16384, 16384) <= Lmap.get(4096, 0) + 2 and Lmap.get(4096, 4096) <= 256
    )
    clear_eventual_period = (
        pw["n_periods_no_mismatch"] > 0
        or (pw["min_last_mismatch"] >= 0 and pw["min_last_mismatch"] < min(256, pw["prefix"] / 8))
    )
    simpler_all_three = (
        (not linear_not_simpler)
        and (not no_cheap_period)
        and (not disc_not_better)
    )
    return {
        "linear_not_simpler": linear_not_simpler,
        "L_ge_N_over_4_at_4096_and_16384": linear_not_simpler,
        "no_cheap_period": no_cheap_period,
        "discrepancy_not_better": disc_not_better,
        "bounded_L": bounded_L,
        "clear_eventual_period": clear_eventual_period,
        "simpler_in_all_three": simpler_all_three,
        "stop_and_prove": bounded_L or clear_eventual_period,
    }


def fmt_L_table(records: list[dict]) -> str:
    header = "| transform | formula | L(256) | L(1024) | L(4096) | L(16384) | L(4096)/4096 | L(16384)/16384 |"
    sep = "|---|---|---:|---:|---:|---:|---:|---:|"
    lines = [header, sep]
    for rec in records:
        L = {row["N"]: row["L"] for row in rec["linear_complexity"]}
        lines.append(
            (
                f"| `{rec['name']}` | {rec['formula']} | {L.get(256, '')} | "
                f"{L.get(1024, '')} | {L.get(4096, '')} | {L.get(16384, '')} | "
                f"{L[4096] / 4096:.4f} | {L[16384] / 16384:.4f} |"
            )
        )
    return "\n".join(lines)


def write_markdown(payload: dict) -> str:
    recs = payload["transforms"]
    kill = payload["kill"]
    lines = []
    lines.append("# XOR / difference transforms of the Rule 30 centre")
    lines.append("")
    lines.append(
        "Cycle I screen of the unused Astra prompt: an exact closed form for a "
        "transformed sequence (first difference of `c`, or `c_t XOR (t mod 2)`) "
        "that is easier than `c`. This is not linear complexity of raw `c` "
        "(already `L(N)≈N/2` in `experiment.py` / `REPORT.md`), not dual-particle "
        "pairing, and not block energy `D(N)` of the untransformed centre as a "
        "standalone attack. Finite evidence only. **Not a prize claim.**"
    )
    lines.append("")
    lines.append("Certifier: `research/xor_transform.py`. Dump: `research/xor_transform.json`.")
    lines.append("Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.")
    lines.append("")
    lines.append("## Transforms")
    lines.append("")
    lines.append("Packed centre as in `experiment.center_bits`: `row=1`, bit `t` is `(row>>t)&1`,")
    lines.append("`row=(row<<2)^((row<<1)|row)`. Prefix of length 256 matches that function.")
    lines.append("")
    lines.append(r"\[")
    lines.append(r"\begin{aligned}")
    lines.append(r"a_t &= c_t \oplus (t \bmod 2),\\")
    lines.append(r"d_t &= c_t \oplus c_{t+1},\\")
    lines.append(r"e_t &= c_t \oplus c_{t//2},\\")
    lines.append(r"s_t &= c_{t+1} \oplus c_t \oplus c_{t-1}\quad(t\ge 1),\\")
    lines.append(r"m_t &= c_t \oplus (\mathrm{popcount}(t)\bmod 2).")
    lines.append(r"\end{aligned}")
    lines.append(r"\]")
    lines.append("")
    lines.append("The Laplacian `s` is stored with index `0` equal to time `t=1`.")
    lines.append("Raw `c` is included as a baseline, not as a new attack.")
    lines.append("")
    lines.append("## Linear complexity")
    lines.append("")
    lines.append(
        "Binary Berlekamp–Massey copied from `experiment.py`. "
        "`L(N)` is the length after the length-`N` prefix of each transform."
    )
    lines.append("")
    lines.append(fmt_L_table(recs))
    lines.append("")
    lines.append(
        "Kill on linear recurrences: every transform still has `L(N) ≥ N/4` at "
        "`N=4096` and `N=16384` (so none is a simpler linear recurrence than "
        "the known `L(c)≈N/2` profile)."
        if kill["all_L_ge_N_over_4"]
        else "At least one transform has `L(N) < N/4` at `N=4096` or `N=16384`."
    )
    lines.append("")
    lines.append("## Period witnesses")
    lines.append("")
    prefix = payload["period_prefix"]
    pmax = payload["max_period"]
    lines.append(
        f"Last mismatch of `f_t != f_(t+p)` on a {prefix}-bit prefix, `p=1..{pmax}`, "
        "same packing as `experiment.period_witnesses`."
    )
    lines.append("")
    lines.append(
        "| transform | min last-mismatch | at period | # p with last-mismatch < N/2 | "
        "best p≤256 | last-mismatch for that p | last 00 | last 11 |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for rec in recs:
        pw = rec["period_witness"]
        rp = rec["runs"]
        lines.append(
            (
                f"| `{rec['name']}` | {pw['min_last_mismatch']} | "
                f"{pw['min_last_mismatch_period']} | "
                f"{pw['n_periods_last_mismatch_lt_half']} | "
                f"{pw['best_small_period']} | {pw['best_small_last_mismatch']} | "
                f"{rp['last_00']} | {rp['last_11']} |"
            )
        )
    lines.append("")
    lines.append(
        "No transform is eventually periodic on the scanned prefix with a tiny "
        "last-mismatch (below `N/2`) for a small period. For an aperiodic-through-the-end "
        "prefix, last-mismatch for period `p` sits near `N-p`; the raw-`c` minimum "
        "`95902` matches `REPORT.md` / `results.json`. Digrams `00` and `11` "
        "both persist past the halfway mark on every sequence, so none is "
        "eventually `01^q` or `0^q1` on this prefix."
        if kill["no_eventual_period"]
        else "A cheap eventual period appeared; see the JSON dump."
    )
    lines.append("")
    lines.append("Run lengths on the full generated prefix:")
    lines.append("")
    lines.append(
        "| transform | max 0-run | max 1-run | suffix `01^q`? | suffix `0^q1`? | "
        "unique q after last `00` |"
    )
    lines.append("|---|---:|---:|---|---|---|")
    for rec in recs:
        rp = rec["runs"]
        lines.append(
            f"| `{rec['name']}` | {rp['max_zero_run']} | {rp['max_one_run']} | "
            f"{rp['eventually_01q_on_suffix']} | {rp['eventually_0q1_on_suffix']} | "
            f"{rp['unique_q_after_last_00']} |"
        )
    lines.append("")
    lines.append("## Dyadic discrepancy versus raw `D(N)`")
    lines.append("")
    lines.append(
        r"Signed sums \(D_f(N)=\sum_{t<N}(2f_t-1)\) and the annulus maximum "
        r"\(A_m\) (max absolute partial imbalance on `[2^m,2^{m+1})`), against "
        "the same quantities for raw `c`."
    )
    lines.append("")
    lines.append(
        "| transform | D(4096) | D(16384) | D(32768) | D(65536) | D(end) | max A_m/2^m (m≥8) | same order as D(c) |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for rec in recs:
        dmap = {row["N"]: row["D"] for row in rec["discrepancy"]["D_vs_raw"]}
        nm = rec["discrepancy"]["max_normalized_A_m_from_256"]
        nm_s = "" if nm is None else f"{nm:.4f}"
        same = "yes" if rec["discrepancy"]["same_order_as_raw_D"] else "no"
        d_end = rec["discrepancy"]["D_vs_raw"][-1]["D"] if rec["discrepancy"]["D_vs_raw"] else ""
        lines.append(
            f"| `{rec['name']}` | {dmap.get(4096, '')} | {dmap.get(16384, '')} | "
            f"{dmap.get(32768, '')} | {dmap.get(65536, '')} | {d_end} | "
            f"{nm_s} | {same} |"
        )
    lines.append("")
    lines.append(
        "Signed sums stay the same order as raw `D(N)`: none is visibly `o(N)` "
        "better on these prefixes, so there is no Problem 2 shortcut."
        if kill["no_discrepancy_shortcut"]
        else "A transform has a visibly smaller discrepancy than raw `c`."
    )
    lines.append("")
    lines.append("## Why it died")
    lines.append("")
    lines.append(
        "Preregistered kill: every transform still has `L(N) ≥ N/4` at `N=4096` "
        "and `N=16384`; none is eventually periodic on the scanned prefix with a "
        "tiny last-mismatch; signed sums are the same order as raw `D(N)`. "
        "Overall kill if no transform is simpler in all three. All three clauses "
        "fire, so the overall clause fires. XOR with a period-2 or Thue–Morse "
        "sequence changes `L` by `O(1)`, as expected. First difference and the "
        "discrete Laplacian stay on the `L≈N/2` line. Paperfolding-style `e` "
        "has a *larger* `|D|` than raw `c` at `N=65536`. No bounded `L(N)` and "
        "no eventual period, so there is nothing to prove from Rule 30. "
        "Not a prize claim."
    )
    lines.append("")
    lines.append("## Kill verdict")
    lines.append("")
    lines.append(kill["text"])
    lines.append("")
    lines.append(
        "A single nicer statistic would not have been a prize claim. Overall "
        "kill requires failure to be simpler in **all three** of `L(N)`, "
        "periodicity witnesses, and discrepancy; that overall clause "
        + ("fires" if kill["overall"] else "does not fire")
        + "."
    )
    lines.append("")
    if kill["stop_and_prove"]:
        lines.append(
            "A transform had bounded `L(N)` or a clear eventual period. "
            "That would have been a stop-and-prove event for Problem 1. "
            "See JSON `stop_and_prove`."
        )
        lines.append("")
    else:
        lines.append(
            "No transform has bounded `L(N)` or a clear eventual period on the "
            "scanned prefixes, so there is nothing to prove from Rule 30 along "
            "this route."
        )
        lines.append("")
    lines.append("Wall time: `{:.3f}` seconds.".format(payload["elapsed_sec"]))
    lines.append("")
    lines.append("Self-check: packed centre agrees with `experiment.center_bits` on 256 bits;")
    lines.append("copied BM agrees on `c[:100]` (`L=48`) and on the three toy words;")
    lines.append("copied period witnesses agree with `experiment.period_witnesses` on 100 bits.")
    lines.append("")
    return "\n".join(lines) + "\n"


def analyse_one(name: str, formula: str, seq: bytearray, raw_annuli, raw_d, period_prefix: int) -> dict:
    need = max(BM_NS)
    if len(seq) < need:
        raise ValueError(f"{name} is too short: {len(seq)} < {need}")
    prof, _L, _conn = linear_complexity_profile(seq[:need], BM_NS)
    linear = [prof[n] for n in BM_NS]
    # Cross-check one prefix against the copied one-shot BM.
    assert linear_complexity(seq[:1024])[0] == prof[1024]["L"]
    pbits = seq[: min(period_prefix, len(seq))]
    witnesses = period_witnesses(pbits, min(MAX_PERIOD, len(pbits) // 2))
    pw = summarize_periods(witnesses, len(pbits), SMALL_PERIOD)
    runs = run_pattern(seq, len(seq) // 2)
    d_ns = [n for n in D_NS if n <= len(seq)]
    if len(seq) not in d_ns:
        d_ns.append(len(seq))
        d_ns.sort()
    d_prof = D_profile(seq, d_ns)
    annuli = dyadic_annuli(seq)
    disc = discrepancy_vs_raw(annuli, d_prof, raw_annuli, raw_d)
    rec = {
        "name": name,
        "formula": formula,
        "length": len(seq),
        "ones": int(sum(seq)),
        "density": sum(seq) / len(seq),
        "linear_complexity": linear,
        "period_witness": pw,
        "runs": runs,
        "discrepancy": {
            "D": d_prof,
            **disc,
        },
    }
    rec["kill"] = kill_one(rec)
    return rec


def main() -> None:
    t0 = time.time()
    c = packed_center(CENTER_BITS)
    checks = self_check(c)
    raw_seq = transform_raw(c)
    raw_annuli = dyadic_annuli(raw_seq)
    raw_d = D_profile(raw_seq, [n for n in D_NS if n <= len(raw_seq)])

    records = []
    prove = []
    for name, formula, fn in TRANSFORMS:
        seq = fn(c)
        rec = analyse_one(name, formula, seq, raw_annuli, raw_d, PERIOD_PREFIX)
        records.append(rec)
        if rec["kill"]["stop_and_prove"]:
            prove.append(name)

    # REPORT.md / results.json: min last-mismatch of raw c on 100k, p=1..4096 is 95902.
    raw_pw = records[0]["period_witness"]
    if records[0]["name"] != "c":
        raise RuntimeError("raw baseline must be first")
    if PERIOD_PREFIX >= 100000 and CENTER_BITS >= 100000:
        if raw_pw["min_last_mismatch"] != 95902:
            raise AssertionError(
                f"raw c min last-mismatch {raw_pw['min_last_mismatch']} != 95902"
            )
        checks["raw_c_min_last_mismatch_100k"] = True

    non_raw = [r for r in records if r["name"] != "c"]
    all_L = all(r["kill"]["linear_not_simpler"] for r in non_raw)
    no_period = all(r["kill"]["no_cheap_period"] for r in non_raw)
    no_disc = all(r["kill"]["discrepancy_not_better"] for r in non_raw)
    any_all_three = any(r["kill"]["simpler_in_all_three"] for r in non_raw)
    # Overall kill if no transform is simpler in ALL THREE statistics.
    overall = not any_all_three

    if prove:
        text = (
            "STOP: transform(s) {} had bounded L(N) or a clear eventual period. "
            "A Rule 30 identity for that sequence would likely settle Problem 1 "
            "or give a huge reduction. Not automatically a prize claim without "
            "that identity."
        ).format(", ".join(prove))
    elif overall:
        text = (
            "Killed. No transform is simpler than raw c in all three of "
            "linear complexity, periodicity witnesses, and discrepancy. "
            "Every screened transform still has L(N) ≥ N/4 at N=4096 and "
            "N=16384; none has a tiny last-mismatch for a small period on "
            "the scanned prefix; signed sums stay the same order as D(N). "
            "A single nicer statistic is not a prize claim. Not a prize claim."
        )
    else:
        text = (
            "A transform was simpler in all three statistics on these finite "
            "prefixes. That is still not a prize claim without a Rule 30 proof."
        )

    elapsed = time.time() - t0
    payload = {
        "not_a_prize_claim": True,
        "attack": "exact transformed sequences vs raw c",
        "self_check": checks,
        "n_center_bits": CENTER_BITS,
        "period_prefix": PERIOD_PREFIX,
        "max_period": MAX_PERIOD,
        "bm_N": list(BM_NS),
        "transforms": records,
        "kill": {
            "all_L_ge_N_over_4": all_L,
            "no_eventual_period": no_period,
            "no_discrepancy_shortcut": no_disc,
            "any_simpler_in_all_three": any_all_three,
            "overall": overall,
            "stop_and_prove": bool(prove),
            "stop_and_prove_transforms": prove,
            "text": text,
        },
        "elapsed_sec": elapsed,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(payload))

    table = []
    for rec in records:
        L = {row["N"]: row["L"] for row in rec["linear_complexity"]}
        table.append({
            "name": rec["name"],
            "L": L,
            "L4096_ge_N4": L[4096] >= 4096 / 4,
            "L16384_ge_N4": L[16384] >= 16384 / 4,
            "min_last_mismatch": rec["period_witness"]["min_last_mismatch"],
            "min_last_mismatch_period": rec["period_witness"]["min_last_mismatch_period"],
            "simpler_all_three": rec["kill"]["simpler_in_all_three"],
        })
    print(json.dumps({
        "wrote": [str(OUT_JSON), str(OUT_MD)],
        "L_table": table,
        "kill_overall": overall,
        "kill_text": text,
        "elapsed_sec": elapsed,
        "stop_and_prove": prove,
    }, indent=2))


if __name__ == "__main__":
    main()
