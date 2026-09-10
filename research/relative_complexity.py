"""Relative symbolic complexity of the seed pair (left neighbor, center).

R_m = max over left m-words a of the number of distinct center m-words b
such that (a, b) occurs as a consecutive block of (ell, c) on F^t(delta_0).

Does not modify strip_graph.py, strip_extend.py, or experiment.py.
Not a prize claim.

Run: python3 research/relative_complexity.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).with_name("relative_complexity.json")


def f(z: int) -> int:
    """Packed left-edge encoding: bit k is spatial coordinate k-t."""
    return (z << 2) ^ ((z << 1) | z)


def bit_at(row: int, t: int, j: int) -> int:
    k = j + t
    if k < 0:
        return 0
    return (row >> k) & 1


def evolve_pair(steps: int) -> tuple[list[int], list[int], list[int], list[int]]:
    """ell = x(t,-1), c = x(t,0), r = x(t,1), a = x(t,-2)."""
    ell, c, r, a = [], [], [], []
    row = 1
    for t in range(steps):
        ell.append(bit_at(row, t, -1))
        c.append(bit_at(row, t, 0))
        r.append(bit_at(row, t, 1))
        a.append(bit_at(row, t, -2))
        row = f(row)
    return ell, c, r, a


def pack_bits(bits: list[int], start: int, length: int) -> int:
    v = 0
    for i in range(length):
        v = (v << 1) | bits[start + i]
    return v


def compatible_with_left(a_word: list[int], b_word: list[int]) -> bool:
    """b_{i+1} must equal 1 XOR a_i whenever b_i = 1."""
    for i in range(len(a_word) - 1):
        if b_word[i] == 1 and b_word[i + 1] != (1 ^ a_word[i]):
            return False
    return True


def check_branching(ell: list[int], c: list[int], r: list[int]) -> dict:
    """Exact identities: c' = ell XOR (c OR r); 1-phases lock the next center bit."""
    n = len(c) - 1
    fail_update = 0
    fail_lock = 0
    ones = 0
    zeros = 0
    zero_r_values = set()
    for t in range(n):
        pred = ell[t] ^ (c[t] | r[t])
        if pred != c[t + 1]:
            fail_update += 1
        if c[t] == 1:
            ones += 1
            if c[t + 1] != (1 ^ ell[t]):
                fail_lock += 1
        else:
            zeros += 1
            zero_r_values.add(r[t])
    return {
        "n_steps": n,
        "update_failures": fail_update,
        "lock_failures": fail_lock,
        "center_ones": ones,
        "center_zeros": zeros,
        "r_values_at_center_zero": sorted(zero_r_values),
        "ell0_c0": (ell[0], c[0]),
        "ell1_c1": (ell[1], c[1]),
        "ell2_c2": (ell[2], c[2]),
    }


def local_compatible_count(a_word: list[int]) -> int:
    """Number of center words locally compatible with a fixed left word.

    Independent of any orbit: 1-phases lock the next center bit, 0-phases
    branch on the right neighbor. Maximized by a = 1^m (Fibonacci),
    minimized by a = 0^m (exactly m+1).
    """
    m = len(a_word)
    # dp0, dp1 = number of compatible prefixes ending in 0 / 1
    dp0 = dp1 = 1  # length 1, both bits free
    for i in range(m - 1):
        # from 0: next bit free; from 1: next bit forced
        forced = 1 ^ a_word[i]
        n0 = dp0  # 0 -> 0
        n1 = dp0  # 0 -> 1
        if forced == 0:
            n0 += dp1
        else:
            n1 += dp1
        dp0, dp1 = n0, n1
    return dp0 + dp1


def fibonacci_bound(m: int) -> int:
    """max_a C(a) = number of length-m binary words with no 11 = F_{m+2}."""
    a, b = 1, 1
    for _ in range(m + 1):
        a, b = b, a + b
    return a  # F_{m+2} with F_1=1, F_2=1, so F_{m+2} after m+1 steps from (1,1)->(1,2)->...


def fibers_at(ell: list[int], c: list[int], m: int) -> dict[int, set[int]]:
    n = len(ell)
    buckets: dict[int, set[int]] = defaultdict(set)
    if m <= 0 or n < m:
        return buckets
    mask = (1 << m) - 1
    la = lc = 0
    for i in range(m):
        la = ((la << 1) | ell[i]) & mask
        lc = ((lc << 1) | c[i]) & mask
    buckets[la].add(lc)
    for t in range(m, n):
        la = ((la << 1) | ell[t]) & mask
        lc = ((lc << 1) | c[t]) & mask
        buckets[la].add(lc)
    return buckets


def fiber_of_word(ell: list[int], c: list[int], word: list[int]) -> dict:
    """Occurrence times and center companions of one explicit left word."""
    m = len(word)
    n = len(ell)
    times = []
    centers = []
    seen = set()
    for t in range(n - m + 1):
        if ell[t:t + m] == word:
            b = pack_bits(c, t, m)
            times.append(t)
            if b not in seen:
                seen.add(b)
                centers.append((t, format(b, f"0{m}b")))
    return {
        "a": "".join(map(str, word)),
        "n_occ": len(times),
        "fiber": len(seen),
        "local_C": local_compatible_count(word),
        "first_times": times[:12],
        "center_first_hits": centers[:20],
    }


def pair_certificates(ell: list[int], c: list[int], m: int) -> list[dict]:
    """First occurrence time of every observed (a,b) of length m."""
    n = len(ell)
    first: dict[tuple[int, int], int] = {}
    for t in range(n - m + 1):
        a = pack_bits(ell, t, m)
        b = pack_bits(c, t, m)
        if (a, b) not in first:
            first[(a, b)] = t
    by_a: dict[int, list] = defaultdict(list)
    for (a, b), t in first.items():
        by_a[a].append({"b": format(b, f"0{m}b"), "t": t})
    out = []
    for a in sorted(by_a):
        recs = sorted(by_a[a], key=lambda r: r["t"])
        out.append({
            "a": format(a, f"0{m}b"),
            "fiber": len(recs),
            "local_C": local_compatible_count([(a >> (m - 1 - i)) & 1 for i in range(m)]),
            "hits": recs,
        })
    return out


def special_word_fibers(ell: list[int], c: list[int], ms: list[int]) -> list[dict]:
    rows = []
    for m in ms:
        if m >= len(ell):
            break
        zeros = fiber_of_word(ell, c, [0] * m)
        lead1 = fiber_of_word(ell, c, [1] + [0] * (m - 1))
        ones = fiber_of_word(ell, c, [1] * m)
        rows.append({"m": m, "0^m": zeros, "10^{m-1}": lead1, "1^m": ones})
    return rows


def complexity_profile(ell: list[int], c: list[int], ms: list[int]) -> list[dict]:
    rows = []
    n = len(ell)
    for m in ms:
        if m >= n:
            break
        buckets = fibers_at(ell, c, m)
        fiber_sizes = [len(s) for s in buckets.values()]
        r_m = max(fiber_sizes) if fiber_sizes else 0
        p_ell = len(buckets)
        p_pair = sum(fiber_sizes)
        # center language
        c_set = set()
        for t in range(n - m + 1):
            c_set.add(pack_bits(c, t, m))
        p_c = len(c_set)
        # maximizers
        max_words = [a for a, s in buckets.items() if len(s) == r_m]
        max_occ = []
        for a in max_words[:6]:
            occ = []
            for t in range(n - m + 1):
                if pack_bits(ell, t, m) == a:
                    occ.append(t)
                    if len(occ) >= 8:
                        break
            max_occ.append({
                "a": format(a, f"0{m}b"),
                "fiber": r_m,
                "n_occ_prefix": len(occ),
                "first_occ": occ[:8],
                "centers": [format(b, f"0{m}b") for b in sorted(buckets[a])][:12],
            })
        rows.append({
            "m": m,
            "R_m": r_m,
            "p_ell": p_ell,
            "p_c": p_c,
            "p_pair": p_pair,
            "mean_fiber": p_pair / p_ell if p_ell else 0,
            "n_maximizers": len(max_words),
            "max_sample": max_occ,
            "n_blocks": n - m + 1,
        })
    return rows


def R_m_vs_horizon(ell: list[int], c: list[int], ms: list[int], horizons: list[int]) -> list[dict]:
    out = []
    for N in horizons:
        if N > len(ell):
            continue
        for row in complexity_profile(ell[:N], c[:N], ms):
            out.append({"N": N, **row})
    return out


def nested_amplification(ell: list[int], c: list[int], r: list[int], max_m: int) -> dict:
    """Grow a nested left word, splitting only at seed-valid 0-phases with differing r.

    Start from the length-1 left bit that already has fiber 2. At each length,
    consider one-bit right extensions that occur on the seed, and keep a
    lineage whose fiber is maximal. Record whether each increase happens at a
    0-phase with two distinct right-neighbor values (the only locally legal
    split).
    """
    n = len(ell)
    # R_1 witness: left bit 1 occurs with both center bits (t=1 and t=2).
    lineage = []
    current_mask = 1
    current_len = 1
    for m in range(1, max_m + 1):
        buckets: dict[int, dict] = {}
        limit = n - m
        for t in range(limit + 1):
            a = pack_bits(ell, t, m)
            b = pack_bits(c, t, m)
            rec = buckets.get(a)
            if rec is None:
                rec = {"centers": set(), "times": [], "r_at_last_zero": defaultdict(set)}
                buckets[a] = rec
            rec["centers"].add(b)
            rec["times"].append(t)
            # last-step split data: if previous center bit is 0, record r
            if m >= 2 and c[t + m - 2] == 0:
                rec["r_at_last_zero"][pack_bits(c, t, m - 1)].add(r[t + m - 2])
        # among extensions of current_mask (as prefix), pick max fiber
        if m == 1:
            # prefer the known R_1=2 word `1`, else the global max
            best_a = 1 if 1 in buckets and len(buckets[1]["centers"]) >= 2 else max(
                buckets, key=lambda a: len(buckets[a]["centers"])
            )
        else:
            cands = []
            for bit in (0, 1):
                a = (current_mask << 1) | bit
                if a in buckets:
                    cands.append(a)
            if not cands:
                break
            best_a = max(cands, key=lambda a: (len(buckets[a]["centers"]), -a))
        rec = buckets[best_a]
        fiber = len(rec["centers"])
        split_r = {format(k, f"0{m-1}b"): sorted(v) for k, v in rec["r_at_last_zero"].items()} if m >= 2 else {}
        genuine_split = any(len(v) >= 2 for v in rec["r_at_last_zero"].values())
        lineage.append({
            "m": m,
            "a": format(best_a, f"0{m}b"),
            "fiber": fiber,
            "n_occ": len(rec["times"]),
            "first_times": rec["times"][:8],
            "genuine_r_split": genuine_split,
            "r_at_last_zero_sample": {k: v for i, (k, v) in enumerate(split_r.items()) if i < 6},
            "centers_sample": [format(b, f"0{m}b") for b in sorted(rec["centers"])][:12],
        })
        current_mask = best_a
        current_len = m
    return {"lineage_len": current_len, "lineage": lineage}


def all_nested_max_fiber(ell: list[int], c: list[int], max_m: int, top_k: int = 8) -> dict:
    """Keep the top_k left words by fiber at each length, extending each.

    This searches for *some* nested family whose fiber grows, not just one greedy path.
    """
    n = len(ell)
    # length 1
    buckets1 = fibers_at(ell, c, 1)
    frontier = [(a, 1, len(s)) for a, s in buckets1.items()]
    frontier.sort(key=lambda x: -x[2])
    frontier = frontier[:top_k]
    history = [{"m": 1, "frontier": [{"a": format(a, "01b"), "fiber": fib} for a, _, fib in frontier]}]
    best_by_m = {1: max(fib for _, _, fib in frontier)}
    stuck_growth = []
    prev_best = best_by_m[1]
    for m in range(2, max_m + 1):
        nxt = []
        seen = set()
        for a, _, _ in frontier:
            for bit in (0, 1):
                aa = (a << 1) | bit
                if aa in seen:
                    continue
                seen.add(aa)
                centers = set()
                occ = 0
                for t in range(n - m + 1):
                    if pack_bits(ell, t, m) == aa:
                        centers.add(pack_bits(c, t, m))
                        occ += 1
                if occ:
                    nxt.append((aa, occ, len(centers)))
        if not nxt:
            break
        nxt.sort(key=lambda x: (-x[2], -x[1]))
        frontier = nxt[:top_k]
        best = frontier[0][2]
        best_by_m[m] = best
        history.append({
            "m": m,
            "best_fiber": best,
            "frontier": [{"a": format(a, f"0{m}b"), "occ": occ, "fiber": fib} for a, occ, fib in frontier],
        })
        if best > prev_best:
            stuck_growth.append({"m": m, "fiber": best})
        prev_best = best
    return {
        "best_by_m": best_by_m,
        "growth_steps": stuck_growth,
        "history_tail": history[-6:],
        "history_head": history[:8],
    }


def return_word_scan(ell: list[int], c: list[int], r: list[int], m: int, max_examples: int = 5) -> dict:
    """For each left m-word that repeats, record distinct center words and
    whether a 0-phase in the block sees both right-neighbor values.
    """
    n = len(ell)
    occ: dict[int, list[int]] = defaultdict(list)
    for t in range(n - m + 1):
        occ[pack_bits(ell, t, m)].append(t)
    repeats = [(a, times) for a, times in occ.items() if len(times) >= 2]
    repeats.sort(key=lambda kv: -len(kv[1]))
    examples = []
    max_fiber = 0
    n_with_r_split = 0
    for a, times in repeats:
        centers = [pack_bits(c, t, m) for t in times]
        fiber = len(set(centers))
        if fiber > max_fiber:
            max_fiber = fiber
        # any position j in 0..m-2 with c[t+j]=0 and two r values among times
        split = False
        split_pos = None
        for j in range(m - 1):
            rs = set()
            for t in times:
                if c[t + j] == 0:
                    rs.add(r[t + j])
            if len(rs) >= 2:
                split = True
                split_pos = j
                break
        if split:
            n_with_r_split += 1
        if len(examples) < max_examples and fiber >= 2:
            examples.append({
                "a": format(a, f"0{m}b"),
                "n_occ": len(times),
                "fiber": fiber,
                "first_times": times[:10],
                "r_split": split,
                "r_split_pos": split_pos,
            })
    return {
        "m": m,
        "n_repeating_left_words": len(repeats),
        "max_fiber_among_repeats": max_fiber,
        "n_repeats_with_r_split": n_with_r_split,
        "examples": examples,
    }


def splitting_events(ell: list[int], c: list[int], r: list[int], m: int) -> dict:
    """Count seed-valid last-step splits for length-m left words.

    A split is two times t,s with the same left m-word, the same center
    (m-1)-prefix, c[t+m-2]=0, and r[t+m-2] != r[s+m-2].
    """
    n = len(ell)
    # key: (left m-word, center (m-1)-word) -> set of r at the 0-phase
    groups: dict[tuple[int, int], set[int]] = defaultdict(set)
    n_zero_last = 0
    for t in range(n - m + 1):
        if c[t + m - 2] != 0:
            continue
        n_zero_last += 1
        a = pack_bits(ell, t, m)
        bpre = pack_bits(c, t, m - 1)
        groups[(a, bpre)].add(r[t + m - 2])
    n_split_keys = sum(1 for s in groups.values() if len(s) >= 2)
    n_keys = len(groups)
    examples = []
    for (a, bpre), rs in groups.items():
        if len(rs) >= 2:
            examples.append({
                "a": format(a, f"0{m}b"),
                "b_prefix": format(bpre, f"0{m-1}b"),
                "r_values": sorted(rs),
            })
            if len(examples) >= 6:
                break
    return {
        "m": m,
        "n_zero_junction_blocks": n_zero_last,
        "n_groups": n_keys,
        "n_splitting_groups": n_split_keys,
        "examples": examples,
    }


def free_right_overapprox(ell_word: list[int]) -> int:
    """Number of locally compatible center words for a fixed left word,
    allowing an arbitrary right-neighbor sequence. This is the free-boundary
    fiber, not the seed fiber.
    """
    return local_compatible_count(ell_word)


def compare_seed_vs_free(ell: list[int], c: list[int], ms: list[int], samples: int = 40) -> list[dict]:
    n = len(ell)
    out = []
    for m in ms:
        buckets = fibers_at(ell, c, m)
        # take maximizer and a few random occurring words
        items = sorted(buckets.items(), key=lambda kv: -len(kv[1]))
        recs = []
        for a, s in items[:3]:
            word = [(a >> (m - 1 - i)) & 1 for i in range(m)]
            recs.append({
                "a": format(a, f"0{m}b"),
                "seed_fiber": len(s),
                "free_fiber": free_right_overapprox(word),
            })
        # also mean free fiber over first `samples` left words by occurrence order
        seen = []
        seen_set = set()
        for t in range(n - m + 1):
            a = pack_bits(ell, t, m)
            if a not in seen_set:
                seen_set.add(a)
                seen.append(a)
                if len(seen) >= samples:
                    break
        free_sizes = []
        seed_sizes = []
        for a in seen:
            word = [(a >> (m - 1 - i)) & 1 for i in range(m)]
            free_sizes.append(free_right_overapprox(word))
            seed_sizes.append(len(buckets[a]))
        out.append({
            "m": m,
            "maximizers": recs,
            "sample_mean_seed_fiber": sum(seed_sizes) / len(seed_sizes),
            "sample_mean_free_fiber": sum(free_sizes) / len(free_sizes),
            "sample_max_seed": max(seed_sizes),
            "sample_max_free": max(free_sizes),
        })
    return out


def other_seed_R(steps: int, seed: int, ms: list[int]) -> list[dict]:
    """Packed integer seed at t=0 (bit k = cell k from left edge of the *row*,
    width grows as usual). Used only to test the kill criterion that
    amplification must not change the initial seed.
    """
    ell, c = [], []
    row = seed
    # Determine initial width: bit_length
    # Using the same packed convention as experiment.py requires the single 1
    # at the right of a growing left-edge packing. For a general finite seed
    # we evolve spatially.
    lo, hi = 0, max(seed.bit_length() - 1, 0)
    row_map = {j: (seed >> j) & 1 for j in range(0, hi + 1)}
    for t in range(steps):
        ell.append(row_map.get(-1, 0))
        c.append(row_map.get(0, 0))
        lo, hi = min(row_map) - 1, max(row_map) + 1
        row_map = {
            j: row_map.get(j - 1, 0) ^ (row_map.get(j, 0) | row_map.get(j + 1, 0))
            for j in range(lo, hi + 1)
        }
    return complexity_profile(ell, c, ms)


def spatial_reference_pair(steps: int) -> tuple[list[int], list[int], list[int]]:
    row = {0: 1}
    ell, c, r = [], [], []
    for t in range(steps):
        ell.append(row.get(-1, 0))
        c.append(row.get(0, 0))
        r.append(row.get(1, 0))
        lo, hi = -t - 1, t + 1
        row = {
            j: row.get(j - 1, 0) ^ (row.get(j, 0) | row.get(j + 1, 0))
            for j in range(lo - 1, hi + 2)
        }
    return ell, c, r


def main() -> None:
    horizon = 12000
    ell, c, r, a = evolve_pair(horizon)
    ell_ref, c_ref, r_ref = spatial_reference_pair(80)
    assert ell[:80] == ell_ref and c[:80] == c_ref and r[:80] == r_ref

    branching = check_branching(ell, c, r)
    assert branching["update_failures"] == 0
    assert branching["lock_failures"] == 0
    assert branching["ell0_c0"] == (0, 1)
    assert branching["ell1_c1"] == (1, 1)
    assert branching["ell2_c2"] == (1, 0)
    # R_1 = 2 on the seed
    b1 = fibers_at(ell, c, 1)
    R1 = max(len(s) for s in b1.values())
    assert R1 == 2
    assert len(b1[1]) == 2  # left bit 1 with both centers

    ms_full = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48]
    profile = complexity_profile(ell, c, ms_full)
    horizons = [2000, 4000, 8000, 12000]
    vs_N = R_m_vs_horizon(ell, c, [4, 8, 12, 16, 24, 32], horizons)

    nested = nested_amplification(ell, c, r, max_m=24)
    nested_search = all_nested_max_fiber(ell, c, max_m=20, top_k=12)

    returns = [return_word_scan(ell, c, r, m) for m in (4, 8, 12, 16)]
    splits = [splitting_events(ell, c, r, m) for m in (2, 3, 4, 6, 8, 12, 16)]

    free_cmp = compare_seed_vs_free(ell, c, [4, 8, 12, 16], samples=30)

    # Other finite seeds: same R_m measurement, to see if the construction
    # would have to change the seed to grow fibers.
    other = {}
    for seed in (1, 3, 5, 7):
        other[str(seed)] = other_seed_R(4000, seed, [4, 8, 12, 16])

    # Bound check: number of distinct center m-words vs R_m
    # Compatibility: every observed pair satisfies the 1-lock.
    compat_fail = 0
    for t in range(len(ell) - 16):
        aw = ell[t:t + 16]
        bw = c[t:t + 16]
        if not compatible_with_left(aw, bw):
            compat_fail += 1
    assert compat_fail == 0
    assert fibonacci_bound(1) == 2
    assert fibonacci_bound(2) == 3
    assert fibonacci_bound(3) == 5
    assert local_compatible_count([0, 0]) == 3
    assert local_compatible_count([1, 1]) == 3
    assert local_compatible_count([0] * 4) == 5
    assert local_compatible_count([1] * 4) == 8

    certs = {str(m): pair_certificates(ell, c, m) for m in (1, 2, 3)}
    # R_2 equals the local maximum: every left 2-word has fiber 3.
    assert all(rec["fiber"] == 3 and rec["local_C"] == 3 for rec in certs["2"])

    special = special_word_fibers(ell, c, [1, 2, 3, 4, 5, 6, 7, 8, 10, 12])

    # Longer prefix: only rolling-hash R_m, to see whether small-m fibers
    # saturate or keep growing. Evolution is Θ(N²) in the packed encoding.
    long_N = 40000
    ell_L, c_L, r_L, _ = evolve_pair(long_N)
    long_ms = [4, 6, 8, 10, 12, 14, 16]
    long_horizons = [12000, 20000, 30000, 40000]
    long_vs = R_m_vs_horizon(ell_L, c_L, long_ms, long_horizons)
    long_special = special_word_fibers(ell_L, c_L, [6, 8, 10, 12, 14])
    long_profile = complexity_profile(ell_L, c_L, long_ms)

    report = {
        "horizon": horizon,
        "long_horizon": long_N,
        "branching": branching,
        "R_1": R1,
        "fibonacci_local_bounds": {str(m): fibonacci_bound(m) for m in range(1, 17)},
        "certificates_small_m": certs,
        "special_words": special,
        "profile": [
            {k: (round(v, 6) if isinstance(v, float) else v)
             for k, v in row.items() if k != "max_sample"} | {"max_sample": row["max_sample"]}
            for row in profile
        ],
        "R_m_vs_horizon": [
            {k: v for k, v in row.items() if k not in ("max_sample",)}
            for row in vs_N
        ],
        "long_profile": [
            {k: v for k, v in row.items() if k not in ("max_sample",)}
            for row in long_profile
        ],
        "long_R_m_vs_horizon": [
            {k: v for k, v in row.items() if k not in ("max_sample",)}
            for row in long_vs
        ],
        "long_special_words": long_special,
        "nested_greedy": nested,
        "nested_search": nested_search,
        "return_words": returns,
        "splitting_events": splits,
        "seed_vs_free": free_cmp,
        "other_seeds": other,
        "compat_fail_m16": compat_fail,
    }
    OUT.write_text(json.dumps(report, indent=2))

    summary = {
        "horizon": horizon,
        "R_1": R1,
        "R_m": [{"m": row["m"], "R_m": row["R_m"], "p_ell": row["p_ell"], "p_c": row["p_c"],
                 "p_pair": row["p_pair"], "mean_fiber": round(row["mean_fiber"], 4)}
                for row in profile],
        "nested_fibers": [x["fiber"] for x in nested["lineage"]],
        "nested_search_best": nested_search["best_by_m"],
        "splits": [{"m": s["m"], "n_splitting_groups": s["n_splitting_groups"]} for s in splits],
        "long_R_m": [{"N": row["N"], "m": row["m"], "R_m": row["R_m"], "p_ell": row["p_ell"]}
                     for row in long_vs],
        "special_10": [{"m": row["m"], "fiber": row["10^{m-1}"]["fiber"],
                        "occ": row["10^{m-1}"]["n_occ"], "C": row["10^{m-1}"]["local_C"]}
                       for row in special],
        "wrote": str(OUT),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
