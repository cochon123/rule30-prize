"""Exact finite ancestry through the inverse Rule 30 row transducer.

Does not overwrite strip_graph.py, strip_extend.py, or experiment.py.
Does not claim a prize result.

The integer row map and unique 2-adic inverse are

    f(y) = y XOR ((y<<1) OR (y<<2))
    y_k  = z_k XOR (y_{k-1} OR y_{k-2}),   y_{-1}=y_{-2}=0.

The inverse is a 4-state transducer. A finite input has a finite
predecessor iff the transducer ends in state 00; every other tail
state produces an infinite 1-tail.

Run: python3 research/ancestry_transducer.py
"""
from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from pathlib import Path


# ---------------------------------------------------------------------------
# Integer map and 4-state inverse transducer
# ---------------------------------------------------------------------------

# State is (y_{k-1}, y_{k-2}), packed as y_{k-1} | (y_{k-2} << 1).
# 0=00, 1=10, 2=01, 3=11.
STATE_00, STATE_10, STATE_01, STATE_11 = 0, 1, 2, 3
STATE_NAMES = ("00", "10", "01", "11")


def f(y: int) -> int:
    return y ^ ((y << 1) | (y << 2))


def trans_step(state: int, z_bit: int) -> tuple[int, int]:
    """One inverse bit. Returns (new_state, y_bit)."""
    y_prev = state & 1
    y_prev2 = (state >> 1) & 1
    y_bit = z_bit ^ (y_prev | y_prev2)
    new_state = y_bit | (y_prev << 1)
    return new_state, y_bit


def inv_finite(z: int) -> tuple[int, bool, int]:
    """Return (y, finite, final_state) for a nonnegative integer z."""
    y = 0
    state = STATE_00
    n = max(z.bit_length(), 1)
    for k in range(n):
        state, y_bit = trans_step(state, (z >> k) & 1)
        if y_bit:
            y |= 1 << k
    return y, state == STATE_00, state


def inv_d(z: int, d: int) -> tuple[int, bool]:
    cur = z
    for _ in range(d):
        cur, finite, _ = inv_finite(cur)
        if not finite:
            return cur, False
    return cur, True


def exact_depth(z: int, max_d: int = 64) -> int:
    """Largest d with d successive finite predecessors."""
    d = 0
    cur = z
    while d < max_d:
        cur, finite, _ = inv_finite(cur)
        if not finite:
            return d
        d += 1
    return d


def zero_tail_class(state: int) -> str:
    """Orbit of a tail state under input 0 (end of a finite word)."""
    seen = []
    s = state
    for _ in range(8):
        if s in seen:
            break
        seen.append(s)
        s, _ = trans_step(s, 0)
    if state == STATE_00:
        return "finite-00"
    return "infinite-ones:" + "->".join(STATE_NAMES[x] for x in seen)


# ---------------------------------------------------------------------------
# d-fold cascade DFA
# ---------------------------------------------------------------------------

def pack_cascade(states: tuple[int, ...]) -> int:
    acc = 0
    for i, s in enumerate(states):
        acc |= s << (2 * i)
    return acc


def unpack_cascade(code: int, d: int) -> tuple[int, ...]:
    return tuple((code >> (2 * i)) & 3 for i in range(d))


def cascade_step(states: tuple[int, ...], z_bit: int) -> tuple[tuple[int, ...], int]:
    """Feed z_bit into layer 1; each layer's output feeds the next."""
    out_states = []
    bit = z_bit
    for s in states:
        ns, bit = trans_step(s, bit)
        out_states.append(ns)
    return tuple(out_states), bit


def cascade_delta(d: int) -> list[list[int]]:
    """delta[code][bit] = next code, 4^d states."""
    n = 4 ** d
    delta = [[0, 0] for _ in range(n)]
    for code in range(n):
        states = unpack_cascade(code, d)
        for bit in (0, 1):
            ns, _ = cascade_step(states, bit)
            delta[code][bit] = pack_cascade(ns)
    return delta


def live_states(delta: list[list[int]], accept: int) -> tuple[set[int], set[int], set[int]]:
    """Reachable from 0, co-reachable to accept, and live = both."""
    n = len(delta)
    reach = set()
    q = deque([0])
    reach.add(0)
    while q:
        v = q.popleft()
        for b in (0, 1):
            w = delta[v][b]
            if w not in reach:
                reach.add(w)
                q.append(w)
    rev = [[] for _ in range(n)]
    for v in range(n):
        for b in (0, 1):
            rev[delta[v][b]].append(v)
    coreach = set()
    q = deque([accept])
    coreach.add(accept)
    while q:
        v = q.popleft()
        for w in rev[v]:
            if w not in coreach:
                coreach.add(w)
                q.append(w)
    live = reach & coreach
    return reach, coreach, live


def minimize_dfa(delta: list[list[int]], accept: set[int], restrict: set[int] | None = None):
    """Partition refinement on a (possibly incomplete) live subset."""
    n = len(delta)
    if restrict is None:
        restrict = set(range(n))
    # Dead states collapse to one sink if they appear as images.
    blocks = []
    acc_block = sorted(s for s in restrict if s in accept)
    rej_block = sorted(s for s in restrict if s not in accept)
    if acc_block:
        blocks.append(acc_block)
    if rej_block:
        blocks.append(rej_block)
    belong = [-1] * n
    for i, block in enumerate(blocks):
        for s in block:
            belong[s] = i
    changed = True
    while changed:
        changed = False
        new_blocks = []
        for block in blocks:
            buckets = defaultdict(list)
            for s in block:
                sig = []
                for b in (0, 1):
                    t = delta[s][b]
                    sig.append(belong[t] if t in restrict else -1)
                buckets[tuple(sig)].append(s)
            parts = list(buckets.values())
            if len(parts) > 1:
                changed = True
            new_blocks.extend(parts)
        blocks = new_blocks
        belong = [-1] * n
        for i, block in enumerate(blocks):
            for s in block:
                belong[s] = i
    return len(blocks), blocks


def prefix_language_full(delta: list[list[int]], live: set[int]) -> bool:
    """Every binary string is a prefix of an accepting word iff start is
    live and every live state has a live 0-successor and live 1-successor.
    """
    if 0 not in live:
        return False
    for s in live:
        for b in (0, 1):
            if delta[s][b] not in live:
                return False
    return True


def factor_count(delta: list[list[int]], live: set[int], width: int) -> int:
    """Number of length-`width` factors of the live language."""
    if prefix_language_full(delta, live):
        return 1 << width
    cur = {(s, 0) for s in live}
    for _ in range(width):
        nxt = set()
        for s, w in cur:
            for b in (0, 1):
                t = delta[s][b]
                if t in live:
                    nxt.add((t, (w << 1) | b))
        cur = nxt
        if not cur:
            return 0
    return len({w for _, w in cur})


def shortest_resets(delta: list[list[int]], live: set[int], accept: int = 0):
    """Length of a shortest word from each live state to accept."""
    n = len(delta)
    dist = [-1] * n
    dist[accept] = 0
    q = deque([accept])
    rev = [[] for _ in range(n)]
    for v in live:
        for b in (0, 1):
            rev[delta[v][b]].append(v)
    while q:
        v = q.popleft()
        for w in rev[v]:
            if w in live and dist[w] < 0:
                dist[w] = dist[v] + 1
                q.append(w)
    vals = [dist[s] for s in live]
    missing = sum(1 for x in vals if x < 0)
    present = [x for x in vals if x >= 0]
    return {
        "max": max(present) if present else None,
        "missing": missing,
        "histogram": {str(k): present.count(k) for k in sorted(set(present))},
    }


# Folded 3-state layer: 00, 01, 1* (10 and 11 are equivalent).
FOLD_A, FOLD_B, FOLD_C = 0, 1, 2  # 00, 01, 1*
FOLD_NAMES = ("00", "01", "1*")


def fold_state(s: int) -> int:
    y_prev = s & 1
    y_prev2 = (s >> 1) & 1
    if y_prev == 1:
        return FOLD_C
    if y_prev2 == 1:
        return FOLD_B
    return FOLD_A


def fold_step(fs: int, z_bit: int) -> tuple[int, int]:
    """Folded inverse step. Output y_bit, next folded state."""
    if fs == FOLD_A:  # OR = 0
        y = z_bit
        return (FOLD_A if y == 0 else FOLD_C), y
    # OR = 1
    y = z_bit ^ 1
    if fs == FOLD_B:  # was 01, next y_prev2 = 0
        return (FOLD_A if y == 0 else FOLD_C), y
    # fs == FOLD_C: was 1*, next y_prev2 = 1
    return (FOLD_B if y == 0 else FOLD_C), y


# ---------------------------------------------------------------------------
# Center column of a finite seed (right-edge-relative origin)
# ---------------------------------------------------------------------------

def centers(y: int, n: int) -> list[int]:
    z = y
    out = []
    for t in range(n):
        out.append((z >> t) & 1)
        z = f(z)
    return out


def last_mismatch(seq: list[int], p: int) -> int:
    """Largest t with seq[t] != seq[t+p], or -1 if none (pure prefix period)."""
    last = -1
    for t in range(len(seq) - p):
        if seq[t] != seq[t + p]:
            last = t
    return last


def kernel_bit_set(max_bits: int) -> list[int]:
    """Odd integers < 2^max_bits with no finite predecessor."""
    out = []
    for y in range(1, 1 << max_bits, 2):
        _, finite, _ = inv_finite(y)
        if not finite:
            out.append(y)
    return out


def all_odd(max_bits: int) -> list[int]:
    return list(range(1, 1 << max_bits, 2))


# ---------------------------------------------------------------------------
# Windows around bit t of f^t(y)
# ---------------------------------------------------------------------------

def iterate_row(y: int, t: int) -> int:
    z = y
    for _ in range(t):
        z = f(z)
    return z


def center_window(row: int, t: int, radius: int) -> int | None:
    """Bits [t-radius, t+radius] of row, packed LSB = bit t-radius.
    None if t-radius < 0."""
    if t < radius:
        return None
    w = 0
    for i in range(2 * radius + 1):
        w |= ((row >> (t - radius + i)) & 1) << i
    return w


def transducer_state_at(z: int, pos: int) -> int:
    """State AFTER reading bits 0..pos-1 (about to read bit pos)."""
    state = STATE_00
    for k in range(pos):
        state, _ = trans_step(state, (z >> k) & 1)
    return state


def cascade_state_at(z: int, d: int, pos: int) -> tuple[int, ...]:
    states = (STATE_00,) * d
    for k in range(pos):
        states, _ = cascade_step(states, (z >> k) & 1)
    return states


# ---------------------------------------------------------------------------
# Period-monitor product on the live cascade (unmarked: any bit may be
# treated as a sampled center of one inverse layer). This is the *wrong*
# geometry for the prize column, and is recorded as such. The correct
# geometry samples layer j at bit (c-j).
# ---------------------------------------------------------------------------

def diagonal_center_bits(z: int, d: int, c: int) -> list[int] | None:
    """Center-column readout of d+1 generations ending at row z, with
    current center at bit c: bit c of z, bit c-1 of inv(z), ... .
    Returns None if some inverse is infinite or c < d."""
    if c < d:
        return None
    bits = []
    cur = z
    for j in range(d + 1):
        pos = c - j
        if pos < 0:
            return None
        bits.append((cur >> pos) & 1)
        if j == d:
            break
        cur, finite, _ = inv_finite(cur)
        if not finite:
            return None
    return bits


def period_stretch_ok(bits: list[int], word: tuple[int, ...]) -> bool:
    p = len(word)
    return all(b == word[i % p] for i, b in enumerate(bits))


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def self_check():
    # Published row sequence 1, 7, 25, 111 and OEIS A269160 formula.
    rows = [1]
    for _ in range(8):
        rows.append(f(rows[-1]))
    assert rows[:4] == [1, 7, 25, 111]
    for n in range(1, 40):
        assert f(n) == n ^ ((n << 1) | (n << 2))
        y, finite, _ = inv_finite(f(n))
        assert finite and y == n, (n, y, finite)

    # 1 has no finite predecessor; its orbit has exact depth t.
    _, finite1, st1 = inv_finite(1)
    assert not finite1
    assert st1 == STATE_10
    z = 1
    for t in range(0, 12):
        assert exact_depth(z) == t
        z = f(z)

    # Tail classification.
    assert zero_tail_class(STATE_00) == "finite-00"
    for s in (STATE_10, STATE_01, STATE_11):
        assert zero_tail_class(s).startswith("infinite-ones")

    # From 01 --0--> 10 --0--> 11 --0--> 11. From 10 --0--> 11.
    s, y = trans_step(STATE_01, 0)
    assert (s, y) == (STATE_10, 1)
    s, y = trans_step(STATE_10, 0)
    assert (s, y) == (STATE_11, 1)
    s, y = trans_step(STATE_11, 0)
    assert (s, y) == (STATE_11, 1)

    # 10 and 11 are equivalent (OR already 1 and y_{k-1}=1); 3-state fold.
    for s in range(4):
        for b in (0, 1):
            ns, y = trans_step(s, b)
            fns, fy = fold_step(fold_state(s), b)
            assert y == fy and fold_state(ns) == fns

    # Parity invariant, bitlength +2 for positive integers.
    for n in range(1, 50):
        fn = f(n)
        assert (fn & 1) == (n & 1)
        assert fn.bit_length() == n.bit_length() + 2

    # Prize center extraction on the seed: first bits 1,1,0,1.
    seq = centers(1, 8)
    assert seq[:4] == [1, 1, 0, 1]

    # Diagonal readout recovers the seed center history.
    z = 1
    for t in range(8):
        z = f(z) if t else 1
    # rebuild f^7(1)
    z = 1
    for _ in range(7):
        z = f(z)
    bits = diagonal_center_bits(z, 7, 7)
    assert bits == centers(1, 8)[::-1], (bits, centers(1, 8))

    # Unique predecessor: two finite y cannot share f(y).
    seen = {}
    for n in range(0, 200):
        fn = f(n)
        y, finite, _ = inv_finite(fn)
        assert finite and y == n
        assert fn not in seen
        seen[fn] = n


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def analyze_cascade(depths):
    out = []
    for d in depths:
        delta = cascade_delta(d)
        accept = 0  # all layers 00
        reach, coreach, live = live_states(delta, accept)
        nmin, _ = minimize_dfa(delta, {accept}, restrict=live)
        full_pref = prefix_language_full(delta, live)
        factors = {}
        for w in (1, 2, 3, 4, 5, 6, 8):
            if full_pref:
                factors[str(w)] = 1 << w
            else:
                factors[str(w)] = factor_count(delta, live, w)
        resets = shortest_resets(delta, live, accept)
        out.append({
            "d": d,
            "raw_states": 4 ** d,
            "reachable": len(reach),
            "coreachable": len(coreach),
            "live": len(live),
            "minimized_live": nmin,
            "all_states_live": live == set(range(4 ** d)),
            "all_coreachable": len(coreach) == 4 ** d,
            "prefix_language_full_binary": full_pref,
            "factor_counts": factors,
            "shortest_reset": resets,
        })
    return out


def seed_state_trace(n: int):
    """Transducer state at the prize center along the actual orbit."""
    z = 1
    rows = []
    for t in range(n):
        # state after reading bits 0..t-1 of the current row f^t(1)
        st = transducer_state_at(z, t)
        center = (z >> t) & 1
        left = (z >> (2 * t)) & 1 if t > 0 or z else 1
        right = z & 1
        rows.append({
            "t": t,
            "center": center,
            "right_endpoint": right,
            "left_endpoint": left,
            "bitlength": z.bit_length() if z else 1,
            "state_before_center": STATE_NAMES[st],
            "state_before_center_code": st,
        })
        z = f(z)
    return rows


def window_survey(depths, extra_kernel_bits, radius):
    """Center windows of f^d(y) at bit d, y odd of bitlength <= extra+? 

    For time t=d+e with kernel bitlength 2e+1, the prize column is still
    bit t. Here we fix time t=d (exact depth d, kernel bitlength 1, so
    only y=1) and also t=d with larger kernels (then bitlength(y)+2d
    vs center index d: the geometric middle is not the prize column).

    Two surveys:
      exact_depth: y kernel, time = d, window at bit d of f^d(y)
      extra_time:  y kernel of max_bits, time = d + extra
    """
    results = []
    kernels = kernel_bit_set(extra_kernel_bits)
    odds = all_odd(extra_kernel_bits)
    for d in depths:
        exact = set()
        for y in kernels:
            row = iterate_row(y, d)
            w = center_window(row, d, radius)
            if w is not None:
                exact.add(w)
        # also all odd finite seeds, not only kernels
        all_odd_windows = set()
        for y in odds:
            row = iterate_row(y, d)
            w = center_window(row, d, radius)
            if w is not None:
                all_odd_windows.add(w)
        results.append({
            "d": d,
            "radius": radius,
            "window_length": 2 * radius + 1,
            "max_possible": 1 << (2 * radius + 1),
            "kernels_scanned": len(kernels),
            "kernel_windows_at_bit_d": len(exact),
            "odd_windows_at_bit_d": len(all_odd_windows),
        })
    return results


def center_factor_survey(max_kernel_bits, n_steps, factor_len):
    """Union of length-m factors of c_t(y) over odd y < 2^bits."""
    all_factors = set()
    kernel_factors = set()
    seed_factors = set()
    kernels = set(kernel_bit_set(max_kernel_bits))
    # Restrict to starting at various T, including large T.
    by_onset = defaultdict(set)
    long_periodic = []  # (y, p, T, run_len)
    period_hits = []

    ys = all_odd(max_kernel_bits)
    for y in ys:
        seq = centers(y, n_steps)
        is_kernel = y in kernels
        for i in range(len(seq) - factor_len + 1):
            word = tuple(seq[i:i + factor_len])
            all_factors.add(word)
            if is_kernel:
                kernel_factors.add(word)
            if y == 1:
                seed_factors.add(word)
            by_onset[i].add(word)
        # longest periodic run for small p
        for p in range(1, 9):
            best = 0
            best_T = 0
            run = 0
            T0 = 0
            for t in range(p, n_steps):
                if seq[t] == seq[t - p]:
                    if run == 0:
                        T0 = t - p
                    run += 1
                    if run > best:
                        best = run
                        best_T = T0
                else:
                    run = 0
            if best >= 4 * p:
                long_periodic.append({
                    "y": y, "p": p, "T": best_T,
                    "agreements": best, "n_steps": n_steps,
                    "is_kernel": is_kernel, "is_seed": y == 1,
                })
        for p in range(1, 9):
            lm = last_mismatch(seq, p)
            # If last mismatch is small, the observed prefix looks periodic
            # after lm+1. Record if the tail is at least 3 periods.
            if lm >= 0 and (n_steps - (lm + 1) - p) >= 3 * p:
                period_hits.append({
                    "y": y, "p": p, "last_mismatch": lm,
                    "tail": n_steps - lm - 1, "is_kernel": is_kernel,
                    "is_seed": y == 1,
                    "tail_word": "".join(map(str, seq[lm + 1:lm + 1 + p])),
                })
            if lm < 0 and n_steps >= 3 * p:
                period_hits.append({
                    "y": y, "p": p, "last_mismatch": -1,
                    "tail": n_steps, "is_kernel": is_kernel,
                    "is_seed": y == 1,
                    "tail_word": "".join(map(str, seq[:p])),
                })

    # growth of factor set as onset T increases (using all y)
    onset_counts = {str(T): len(by_onset[T]) for T in sorted(by_onset)
                    if T <= n_steps - factor_len}

    return {
        "max_kernel_bits": max_kernel_bits,
        "n_steps": n_steps,
        "factor_len": factor_len,
        "max_possible": 1 << factor_len,
        "all_odd_factors": len(all_factors),
        "kernel_factors": len(kernel_factors),
        "seed_factors": len(seed_factors),
        "full_shift": len(all_factors) == (1 << factor_len),
        "factors_starting_with_1": sum(1 for w in all_factors if w[0] == 1),
        "onset_factor_counts_head": {str(T): onset_counts[str(T)]
                                     for T in range(0, min(8, n_steps - factor_len + 1))},
        "onset_full_from_T1": all(onset_counts[str(T)] == (1 << factor_len)
                                  for T in range(1, min(8, n_steps - factor_len + 1))),
        "min_onset_count_T1_to_32": min(
            onset_counts[str(T)]
            for T in range(1, min(33, n_steps - factor_len + 1))
            if str(T) in onset_counts
        ),
        "n_long_periodic_runs": len(long_periodic),
        "n_period_tail_hits": len(period_hits),
    }


def period_monitor_exists(depths, words):
    """For each d and each period word, does some z in L_d with a marked
    center c=d (so hypothesized time d) have a diagonal center readout
    equal to a cyclic shift of the word, of length d+1?

    At time d the unique kernel of bitlength 1 is y=1, so c=d, z=f^d(1)
    is the only length-2d+1 odd row of exact depth d. That readout is
    exactly the seed center history, reversed. This is recorded to make
    the uniqueness obstruction explicit.

    Also search extra: z = f^d(y) for kernels y, mark at bit d, readout
    length min(d, 8)+1.
    """
    out = []
    for d in depths:
        z_seed = 1
        for _ in range(d):
            z_seed = f(z_seed)
        seed_read = diagonal_center_bits(z_seed, d, d)
        row = {"d": d, "seed_readout": seed_read,
               "seed_readout_str": "".join(map(str, seed_read)) if seed_read else None,
               "words": []}
        for word in words:
            w = tuple(word)
            # unique exact-depth-d middle geometry
            ok_seed = False
            if seed_read is not None and len(seed_read) >= len(w):
                # some phase: seed_read[i] = w[(phi+i) % p] along the readout
                p = len(w)
                chunk = seed_read[:len(seed_read) - (len(seed_read) % p)] if False else seed_read
                # check whether the whole readout is eventually the period
                # (it is the true sequence reversed). Just: does the word
                # equal the actual reversed seed prefix of that length?
                ok_seed = tuple(seed_read[:p]) == w or any(
                    all(seed_read[i] == w[(i + phi) % p] for i in range(len(seed_read)))
                    for phi in range(p)
                )
            # other kernels, mark still at bit d
            other = []
            for y in kernel_bit_set(min(8, max(2, d))):
                z = iterate_row(y, d)
                bits = diagonal_center_bits(z, min(d, 12), d)
                if bits is None:
                    continue
                p = len(w)
                if any(all(bits[i] == w[(i + phi) % p] for i in range(len(bits)))
                       for phi in range(p)):
                    other.append(y)
                    if len(other) >= 5:
                        break
            row["words"].append({
                "word": "".join(map(str, w)),
                "matches_seed_readout_some_phase": ok_seed,
                "other_kernel_examples": other,
            })
        out.append(row)
    return out


def ranking_attempt(n: int):
    """Look for a well-founded rank on (state_before_center, t mod p)
    along the seed, and along other kernels. A rank that decreases on
    every periodic-center step would exclude infinite continuation.
    """
    # Candidate ranks: Hamming of cascade at center, 2-adic state id,
    # distance to 00 under 0-input (infinite for non-00).
    seed = seed_state_trace(n)
    states = [row["state_before_center_code"] for row in seed]
    centers_seq = [row["center"] for row in seed]
    # For each p=2..8, restrict to times where the last p centers match
    # a fixed word, and see if the 4-state coordinate is eventually
    # constant / cycling independently of the word, or has a monotone rank.
    period_ranks = []
    for p in range(2, 9):
        # hypothetical: from some T, centers are periodic with the *actual*
        # length-p prefix starting at T. That's only possible if the real
        # sequence is periodic from T, which it is not. Instead: look at
        # the map (state, phase) whenever center == a chosen bit.
        pairs = [(states[t], t % p, centers_seq[t]) for t in range(n)]
        # Does the same (state, phase) occur with two different next
        # centers? That kills a functional ranking on this projection.
        nxt = defaultdict(set)
        for t in range(n - 1):
            key = (states[t], t % p, centers_seq[t])
            nxt[key].add((states[t + 1], (t + 1) % p, centers_seq[t + 1]))
        ambiguous = {str(k): [list(x) for x in vs]
                     for k, vs in nxt.items() if len(vs) > 1}
        period_ranks.append({
            "p": p,
            "observed_keys": len(nxt),
            "ambiguous_keys": len(ambiguous),
            "ambiguous_sample": dict(list(ambiguous.items())[:6]),
        })
    # Cross-kernel: union of (state_before_center, center) at time t
    # over many y, for several t. If both centers occur for the same
    # 4-state at the same t, the 4-state is not a ranking for the bit.
    cross = []
    for t in (4, 8, 12, 16):
        bucket = defaultdict(set)
        for y in all_odd(8):
            row = iterate_row(y, t)
            st = transducer_state_at(row, t)
            bucket[st].add((row >> t) & 1)
        cross.append({
            "t": t,
            "states_with_both_centers": sorted(
                s for s, bits in bucket.items() if bits == {0, 1}
            ),
            "state_to_centers": {STATE_NAMES[s]: sorted(bits)
                                 for s, bits in sorted(bucket.items())},
        })
    return {"seed_period_projection": period_ranks, "cross_kernel_at_t": cross}


def left_reset_survey(depths, extra_bits):
    """From the cascade state at the center, the left half of a finite
    row is a reset word to all-00. Count distinct center-states that
    admit a reset of exact length t (the seed geometry).
    """
    out = []
    for d in depths:
        delta = cascade_delta(d)
        accept = 0
        _, _, live = live_states(delta, accept)
        # For length t = d (kernel bitlength 1): unique accepting word of
        # bitlength 2d+1 with exact depth d among images of kernels of
        # bitlength 1. Count, for general t, how many live states appear
        # as the state AFTER t bits of some accepting word of length 2t+1.
        for t in (d, d + 1, d + 2):
            # BFS: after t symbols from start, live states; then from
            # those, some continuation of length t (left half, remaining
            # after center: bits t..2t) reaching accept. Center is bit t,
            # so after t+1 bits we have passed the center. "At center"
            # means after t bits (about to read / just before center),
            # or after t+1 (just after). We take after t bits.
            at = {0}
            for _ in range(t):
                nxt = set()
                for s in at:
                    for b in (0, 1):
                        u = delta[s][b]
                        if u in live:
                            nxt.add(u)
                at = nxt
            can_reset = set()
            # From each such state, does some word of length t+1 (center
            # plus t left bits, indices t..2t) reach accept?
            for s0 in at:
                cur = {s0}
                for _ in range(t + 1):
                    nxt = set()
                    for s in cur:
                        for b in (0, 1):
                            nxt.add(delta[s][b])
                    cur = nxt
                if 0 in cur:
                    can_reset.add(s0)
            out.append({
                "d": d, "t": t, "states_after_right_half": len(at),
                "states_resettable_by_left_half": len(can_reset),
                "raw": 4 ** d,
            })
    return out


def main():
    t0 = time.time()
    self_check()

    depths = (1, 2, 3, 4, 5, 6)
    cascade = analyze_cascade(depths)
    seed_trace = seed_state_trace(48)
    windows = window_survey(depths, extra_kernel_bits=8, radius=3)
    factors = center_factor_survey(max_kernel_bits=10, n_steps=64, factor_len=6)
    factors8 = center_factor_survey(max_kernel_bits=8, n_steps=96, factor_len=8)
    words = [
        (0,), (1,),
        (0, 1), (1, 0), (0, 0), (1, 1),
        (0, 0, 1), (0, 1, 1), (0, 1, 1, 1),
        (0, 1, 1, 1, 1, 1, 1, 1, 1),
    ]
    monitor = period_monitor_exists((1, 2, 4, 8), words)
    ranks = ranking_attempt(64)
    resets = left_reset_survey((1, 2, 3, 4), extra_bits=4)

    # Strongest numerical claims to re-check as assertions in the note.
    assert cascade[0]["raw_states"] == 4
    assert cascade[0]["minimized_live"] == 3
    mins = [row["minimized_live"] for row in cascade]
    assert mins == [3, 7, 16, 35, 71, 141]
    assert mins == sorted(set(mins))  # strictly increasing
    for row in cascade:
        assert row["prefix_language_full_binary"] is True
        assert row["all_coreachable"] is True
        assert row["factor_counts"]["8"] == 256
        assert row["shortest_reset"]["max"] == 2 * row["d"]

    # Seed 1 is a kernel; no other bitlength-1 odd kernel.
    assert kernel_bit_set(1) == [1]

    assert factors["full_shift"] is True
    assert factors["all_odd_factors"] == 64
    assert factors["kernel_factors"] == 64
    assert factors["min_onset_count_T1_to_32"] >= 63
    assert factors8["full_shift"] is True

    for item in ranks["cross_kernel_at_t"]:
        if item["t"] >= 8:
            assert item["states_with_both_centers"] == [0, 1, 2, 3]

    # Seed 1 is a kernel; no other bitlength-1 odd kernel.
    assert kernel_bit_set(1) == [1]

    # Factor language of finite-seed centers is not the full shift at
    # the start (c_0=1 for odd y) but saturates later: recorded, not
    # asserted beyond c_0.

    result = {
        "seconds": round(time.time() - t0, 3),
        "cascade": cascade,
        "seed_state_trace_head": seed_trace[:16],
        "seed_state_trace_codes": [r["state_before_center_code"] for r in seed_trace],
        "seed_centers": [r["center"] for r in seed_trace],
        "windows": windows,
        "center_factors_len6": factors,
        "center_factors_len8": factors8,
        "period_monitor": monitor,
        "ranking": ranks,
        "left_reset": resets,
    }
    out_path = Path(__file__).with_suffix(".json")
    out_path.write_text(json.dumps(result, indent=2))
    print(json.dumps({
        "ok": True,
        "seconds": result["seconds"],
        "cascade_min_states": [r["minimized_live"] for r in cascade],
        "prefix_full": [r["prefix_language_full_binary"] for r in cascade],
        "seed_factors_6": factors["seed_factors"],
        "all_odd_factors_6": factors["all_odd_factors"],
        "n_period_tail_hits_6": factors["n_period_tail_hits"],
        "n_long_periodic_6": factors["n_long_periodic_runs"],
        "json": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
