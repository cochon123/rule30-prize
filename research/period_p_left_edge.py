"""Left-edge reconstruction for a hypothetical period-p Rule 30 center.

For each primitive necklace of period 3..7, left columns are recovered from
    x(t, j-1) = x(t+1, j) XOR (x(t, j) OR x(t, j+1))
as Boolean functions of the right-neighbor bits r_t = x(t, 1), then reduced
by the local Markov constraints on r coming from a free far-right bit.

The prize seed's left light-cone L_0 is imposed at the onset of the
periodic regime: leftmost 1 at column -T, zeros strictly further left,
and the moving edge x(s, -(T+s))=1 for as long as the regime lasts.

This file is a verifier. It does not modify strip_graph.py / strip_extend.py.
"""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from itertools import product


# ---------------------------------------------------------------------------
# GF(2) ANF helpers (same bit-coding as period2_left_edge.py)
# bit 0 of the integer is the constant 1; bit (i+1) is variable i.
# ---------------------------------------------------------------------------

def band(p: int, q: int) -> int:
    res = 0
    i = 0
    pp = p
    while pp:
        if pp & 1:
            j = 0
            qq = q
            while qq:
                if qq & 1:
                    res ^= 1 << (i | j)
                qq >>= 1
                j += 1
        pp >>= 1
        i += 1
    return res


def bor(p: int, q: int) -> int:
    return p ^ q ^ band(p, q)


def anf_vars(p: int) -> list[int]:
    used = []
    i = 0
    while (1 << (i + 1)) <= p:
        mask = 0
        m = 0
        pp = p
        while pp:
            if (pp & 1) and (m >> (i + 1)) & 1:
                mask = 1
                break
            pp >>= 1
            m += 1
        if mask:
            used.append(i)
        i += 1
    return used


def anf_str(p: int, names: list[str] | None = None) -> str:
    if p == 0:
        return "0"
    if p == 1:
        return "1"
    terms = []
    m = 0
    pp = p
    while pp:
        if pp & 1:
            if m == 0:
                terms.append("1")
            else:
                fac = []
                for i in range(m.bit_length()):
                    if (m >> i) & 1:
                        if names is None:
                            fac.append(f"v{i}")
                        else:
                            fac.append(names[i] if i < len(names) else f"v{i}")
                terms.append("*".join(fac) if fac else "1")
        pp >>= 1
        m += 1
    return " + ".join(terms)


def eval_anf(p: int, bits: int) -> int:
    """bits has variable i in bit i (not shifted by the constant)."""
    acc = 0
    m = 0
    pp = p
    while pp:
        if pp & 1:
            # monomial m: bit 0 is constant, bit i+1 is variable i
            if m == 0:
                acc ^= 1
            else:
                need = m >> 1
                if (bits & need) == need:
                    acc ^= 1
        pp >>= 1
        m += 1
    return acc


ONE = 1


def primitive_necklaces(n: int) -> list[str]:
    out = []
    for x in range(1 << n):
        w = "".join(str((x >> (n - 1 - i)) & 1) for i in range(n))
        if any(n % d == 0 and w == w[:d] * (n // d) for d in range(1, n)):
            continue
        if w != min(w[i:] + w[:i] for i in range(n)):
            continue
        out.append(w)
    return out


def rotations(word: str) -> list[str]:
    p = len(word)
    seen = []
    for i in range(p):
        rot = word[i:] + word[:i]
        if rot not in seen:
            seen.append(rot)
    return seen


# ---------------------------------------------------------------------------
# Local Markov constraints on the right neighbor
# r_{t+1} = c_t XOR (r_t OR e_t) with e_t free in {0,1}.
# ---------------------------------------------------------------------------

def next_r_choices(c: int, r: int) -> tuple[int, ...]:
    if c == 0:
        return (1,) if r == 1 else (0, 1)
    return (0,) if r == 1 else (0, 1)


def legal_r_strings(word: str, length: int, r0: int | None = None) -> list[int]:
    """All Markov-legal r bitstrings of given length (bit 0 = r_0)."""
    c = [int(b) for b in word]
    p = len(c)
    out: list[int] = []

    def rec(t: int, acc: int, last: int) -> None:
        if t == length:
            out.append(acc)
            return
        choices = next_r_choices(c[(t - 1) % p], last) if t else (
            (0, 1) if r0 is None else (r0,)
        )
        for bit in choices:
            rec(t + 1, acc | (bit << t), bit)

    rec(0, 0, 0)
    return out


def inject_times(word: str, tmax: int) -> list[int]:
    """Times in 0..tmax-1 at which the center is 0 (r_t may enter the left)."""
    p = len(word)
    return [t for t in range(tmax) if word[t % p] == "0"]


# ---------------------------------------------------------------------------
# Direct reconstruction from a concrete r-string
# ---------------------------------------------------------------------------

def recon_cell(t: int, j: int, word: str, r_bits: int, memo: dict | None = None):
    """x(t,j) for j<=1, using r_bits bit t = r_t and periodic center `word`."""
    if memo is None:
        memo = {}
    key = (t, j)
    if key in memo:
        return memo[key]
    p = len(word)
    if j == 0:
        r = int(word[t % p])
    elif j == 1:
        r = (r_bits >> t) & 1
    elif j > 1:
        raise ValueError("reconstruction asked for a right column > 1")
    else:
        r = recon_cell(t + 1, j + 1, word, r_bits, memo) ^ (
            recon_cell(t, j + 1, word, r_bits, memo)
            | recon_cell(t, j + 2, word, r_bits, memo)
        )
    memo[key] = r
    return r


def recon_dummy_r(t: int, j: int, word: str, r_bits: int, dummy: int, memo=None):
    """Like recon_cell, but at 1-phases of the center use `dummy` instead of r_t.

    Used to check the injection lemma: left columns must ignore r at 1-phases.
    """
    if memo is None:
        memo = {}
    key = (t, j)
    if key in memo:
        return memo[key]
    p = len(word)
    if j == 0:
        r = int(word[t % p])
    elif j == 1:
        if word[t % p] == "1":
            r = dummy
        else:
            r = (r_bits >> t) & 1
    elif j > 1:
        raise ValueError("right column > 1")
    else:
        r = recon_dummy_r(t + 1, j + 1, word, r_bits, dummy, memo) ^ (
            recon_dummy_r(t, j + 1, word, r_bits, dummy, memo)
            | recon_dummy_r(t, j + 2, word, r_bits, dummy, memo)
        )
    memo[key] = r
    return r


# ---------------------------------------------------------------------------
# ANF reconstruction: variables are r at 0-phases only
# ---------------------------------------------------------------------------

def var_index_map(word: str, tmax: int) -> dict[int, int]:
    """Map physical time t (center 0) -> ANF variable index 0,1,2,..."""
    idx = {}
    k = 0
    p = len(word)
    for t in range(tmax):
        if word[t % p] == "0":
            idx[t] = k
            k += 1
    return idx


def cell_anf(t: int, j: int, word: str, vmax: int, idx: dict[int, int], memo: dict):
    key = (t, j)
    if key in memo:
        return memo[key]
    p = len(word)
    if j == 0:
        val = ONE if word[t % p] == "1" else 0
    elif j == 1:
        if word[t % p] == "1":
            val = 0  # dummy; injection lemma says this never appears on the left
        else:
            vi = idx[t]
            if vi >= vmax:
                # beyond the named window: treat as 0 (only used when depth fits)
                val = 0
            else:
                val = 1 << (vi + 1)
    elif j > 1:
        raise ValueError("right column > 1")
    else:
        fut = cell_anf(t + 1, j + 1, word, vmax, idx, memo)
        a = cell_anf(t, j + 1, word, vmax, idx, memo)
        b = cell_anf(t, j + 2, word, vmax, idx, memo)
        val = fut ^ bor(a, b)
    memo[key] = val
    return val


def reduce_by_legal(p_anf: int, word: str, vmax: int, idx: dict[int, int],
                    n_times: int) -> set[int]:
    """Evaluate an ANF on every legal r-string covering the named variables."""
    # Need r-bits long enough that every named time is assigned.
    if not idx:
        return {eval_anf(p_anf, 0)}
    tmax = max(idx) + 1
    vals = set()
    for bits in legal_r_strings(word, tmax):
        packed = 0
        for t, vi in idx.items():
            if vi < vmax and ((bits >> t) & 1):
                packed |= 1 << vi
        vals.add(eval_anf(p_anf, packed))
        if len(vals) == 2:
            break
    return vals


# ---------------------------------------------------------------------------
# Fast iterative left triangle for one r-string
# ---------------------------------------------------------------------------

def fill_left(word: str, r_bits: int, kmax: int, tmax: int) -> list[list[int]]:
    """x[t][k] = x(t, -k) for t=0..tmax-1, k=0..kmax. Needs r bits up to tmax-1.

    Fill from the right: column 0 is the center, then k=1,2,... using the inverse.
    x(t,-k) needs x(t+1,-(k-1)), so tmax must be > kmax for a full first-period
    triangle (use tmax >= p + kmax).
    """
    p = len(word)
    # x[t][k] for k=0..kmax; also need column +1 = r as x[t][-1] conceptually.
    # Store col1 separately.
    col1 = [(r_bits >> t) & 1 for t in range(tmax)]
    x = [[0] * (kmax + 1) for _ in range(tmax)]
    for t in range(tmax):
        x[t][0] = int(word[t % p])
    for k in range(1, kmax + 1):
        for t in range(tmax - k):
            # x(t,-k) = x(t+1,-(k-1)) XOR (x(t,-(k-1)) OR x(t,-(k-2)))
            right1 = x[t][k - 1]
            if k == 1:
                right2 = col1[t]
            else:
                right2 = x[t][k - 2]
            fut = x[t + 1][k - 1]
            x[t][k] = fut ^ (right1 | right2)
    return x


# ---------------------------------------------------------------------------
# 1-run vacuum triangle (no r-injection)
# ---------------------------------------------------------------------------

def run_ones_starts(word: str) -> list[tuple[int, int]]:
    """List of (start_phase, length) for every 1-run, wrapping at most once."""
    p = len(word)
    c = [int(b) for b in word]
    if all(c):
        return [(0, p)]
    # find a 0 to start
    s0 = c.index(0)
    runs = []
    t = s0
    for _ in range(p):
        if c[t % p] == 1 and c[(t - 1) % p] == 0:
            k = 0
            while c[(t + k) % p] == 1:
                k += 1
            runs.append((t % p, k))
        t += 1
    return runs


def vacuum_interval(word: str, t: int, k: int) -> bool:
    """True if times t..t+k are all 1s, so x(t,-k) ignores r."""
    p = len(word)
    return all(word[(t + i) % p] == "1" for i in range(k + 1))


def determined_triangle(word: str, kmax: int | None = None) -> list[dict]:
    """Phases and depths at which a 1-run makes x(s,-k) a center-only constant.

    Sufficient condition: word[s],...,word[s+k] are all 1. Then evaluate with
    r=0 (any r agrees).
    """
    p = len(word)
    if kmax is None:
        kmax = p
    tmax = p + kmax + 2
    x = fill_left(word, r_bits=0, kmax=kmax, tmax=tmax)
    rows = []
    for s in range(p):
        for k in range(1, kmax + 1):
            if vacuum_interval(word, s, k):
                rows.append(
                    {
                        "phase": s,
                        "k": k,
                        "value": x[s][k],
                        "center": int(word[s]),
                    }
                )
    return rows


# ---------------------------------------------------------------------------
# Column identities
# ---------------------------------------------------------------------------

def column_values(word: str, kmax: int, extra_periods: int = 2) -> list[dict]:
    """For each phase s and depth k, the set of values of x(s,-k) on legal r."""
    p = len(word)
    # x(s,-k) reads times s..s+k, so length p+kmax is enough for every phase.
    length = kmax + p + extra_periods
    # Track value sets; drop mixed slots from the live set.
    live = {(s, k) for s in range(p) for k in range(kmax + 1)}
    first = {}
    mixed = set()
    # Determined vacuum cells: evaluate once.
    for rec in determined_triangle(word, kmax):
        key = (rec["phase"], rec["k"])
        first[key] = rec["value"]
        live.discard(key)
    for s in range(p):
        first[(s, 0)] = int(word[s])
        live.discard((s, 0))

    def rec_r(t: int, acc: int, last: int) -> None:
        if not live:
            return
        if t == length:
            x = fill_left(word, acc, kmax, length)
            done = []
            for s, k in live:
                if s + k >= length:
                    continue
                val = x[s][k]
                if (s, k) not in first:
                    first[(s, k)] = val
                elif first[(s, k)] != val:
                    mixed.add((s, k))
                    done.append((s, k))
            for key in done:
                live.discard(key)
            return
        c = int(word[(t - 1) % p]) if t else None
        choices = next_r_choices(c, last) if t else (0, 1)
        for bit in choices:
            rec_r(t + 1, acc | (bit << t), bit)

    rec_r(0, 0, 0)
    rows = []
    for s in range(p):
        for k in range(kmax + 1):
            key = (s, k)
            if key in mixed:
                ident = "mixed"
                vals = [0, 1]
            elif key in first:
                ident = str(first[key])
                vals = [first[key]]
            else:
                ident = "unknown"
                vals = []
            rows.append(
                {
                    "phase": s,
                    "k": k,
                    "center": int(word[s]),
                    "values": vals,
                    "identically": ident,
                }
            )
    return rows


def vanishing_table(word: str, kmax: int) -> list[dict]:
    return [r for r in column_values(word, kmax) if r["identically"] != "mixed"]


# ---------------------------------------------------------------------------
# Isolated-zero ANFs 01^q, q>=2: one free bit u_n = r_{n p} per period
# ---------------------------------------------------------------------------

def isolated_zero_anfs(q: int, kmax: int, n_periods: int | None = None):
    """ANFs of x(s,-k) in u_0,u_1,... for word 01^q.

    u_n occupies ANF variable n (bit n+1).
    """
    word = "0" + "1" * q
    p = q + 1
    if n_periods is None:
        n_periods = (kmax + p) // p + 3
    tmax = n_periods * p + kmax + 2
    idx = var_index_map(word, tmax)
    vmax = n_periods + 2
    memo: dict = {}
    table = []
    for s in range(p):
        row = []
        for k in range(kmax + 1):
            poly = cell_anf(s, -k, word, vmax, idx, memo)
            row.append(poly)
        table.append(row)
    return word, table, idx


def isolated_zero_identities(q: int, kmax: int) -> list[dict]:
    word, table, _ = isolated_zero_anfs(q, kmax)
    p = q + 1
    names = [f"u{i}" for i in range(24)]
    out = []
    for s in range(p):
        for k in range(kmax + 1):
            poly = table[s][k]
            if poly in (0, 1):
                out.append(
                    {
                        "phase": s,
                        "k": k,
                        "anf": "0" if poly == 0 else "1",
                        "center": int(word[s]),
                    }
                )
            elif poly.bit_count() <= 3:
                out.append(
                    {
                        "phase": s,
                        "k": k,
                        "anf": anf_str(poly, names),
                        "center": int(word[s]),
                    }
                )
    return out


def injection_check(word: str, kmax: int = 8, n_strings: int = 200) -> bool:
    """Left cells ignore r at 1-phases. Compare dummy 0 vs dummy 1."""
    p = len(word)
    length = kmax + 2 * p + 4
    strings = legal_r_strings(word, length)
    if len(strings) > n_strings:
        # spread sample
        step = max(1, len(strings) // n_strings)
        strings = strings[::step][:n_strings]
    for bits in strings:
        for dummy in (0, 1):
            for s in range(min(p, 4)):
                for k in range(1, kmax + 1):
                    a = recon_cell(s, -k, word, bits)
                    b = recon_dummy_r(s, -k, word, bits, dummy)
                    if a != b:
                        return False
    return True


def verify_against_forward(word: str, steps: int = 40) -> bool:
    """On a random-ish right half, inverse recovers the true left."""
    # Build a spacetime with imposed center and free right of column 1,
    # left of center evolved normally. Easier: evolve a finite window with
    # the center overwritten each step? That would not be a valid spacetime.
    # Instead: start from a row with the given center bit, arbitrary other
    # bits, evolve freely, and whenever the center matches the word for a
    # stretch, check inverse on that stretch.
    #
    # Direct check: pick legal r and a dummy right of 1, reconstruct left,
    # then verify the forward rule on columns j<0.
    p = len(word)
    length = steps
    bits = legal_r_strings(word, length + 8)[len(legal_r_strings(word, 3)) % 7]
    # use a mid string
    all_s = legal_r_strings(word, length + 8)
    bits = all_s[len(all_s) // 3]
    memo = {}
    for t in range(steps):
        for k in range(1, min(t + 3, 12)):
            j = -k
            if t + 1 >= length:
                continue
            got = recon_cell(t, j, word, bits, memo)
            fwd = recon_cell(t, j - 1, word, bits, memo) ^ (
                recon_cell(t, j, word, bits, memo)
                | recon_cell(t, j + 1, word, bits, memo)
            )
            want = recon_cell(t + 1, j, word, bits, memo)
            if fwd != want:
                return False
            # inverse roundtrip
            inv = recon_cell(t + 1, j + 1, word, bits, memo) ^ (
                recon_cell(t, j + 1, word, bits, memo)
                | recon_cell(t, j + 2, word, bits, memo)
            )
            if inv != got:
                return False
    return True


# ---------------------------------------------------------------------------
# L_0 onset and moving-edge SAT (on-demand assignment of r)
# ---------------------------------------------------------------------------

class RAssign:
    """Partial r assignment with Markov constraints. Unassigned = -1."""

    __slots__ = ("word", "bits")

    def __init__(self, word: str):
        self.word = word
        self.bits: dict[int, int] = {}

    def get(self, t: int) -> int | None:
        return self.bits.get(t)

    def clone(self) -> "RAssign":
        o = RAssign(self.word)
        o.bits = dict(self.bits)
        return o

    def consistent_set(self, t: int, val: int) -> bool:
        if t in self.bits:
            return self.bits[t] == val
        p = len(self.word)
        # check against previous
        if t - 1 in self.bits:
            prev = self.bits[t - 1]
            c = int(self.word[(t - 1) % p])
            if val not in next_r_choices(c, prev):
                return False
        # check against next
        if t + 1 in self.bits:
            nxt = self.bits[t + 1]
            c = int(self.word[t % p])
            if nxt not in next_r_choices(c, val):
                return False
        self.bits[t] = val
        return True


def recon_sat(t: int, j: int, word: str, asg: RAssign, memo: dict) -> int | None:
    """Return 0/1 if determined, or None if a branch is needed (not used).

    This version assumes all needed r bits are already assigned; missing r
    is treated as a request. Callers must assign first.
    """
    key = (t, j)
    if key in memo:
        return memo[key]
    p = len(word)
    if j == 0:
        r = int(word[t % p])
    elif j == 1:
        got = asg.get(t)
        if got is None:
            raise KeyError(t)
        r = got
    elif j > 1:
        raise ValueError("right > 1")
    else:
        r = recon_sat(t + 1, j + 1, word, asg, memo) ^ (
            recon_sat(t, j + 1, word, asg, memo)
            | recon_sat(t, j + 2, word, asg, memo)
        )
    memo[key] = r
    return r


def needed_r_times(t: int, j: int, word: str) -> list[int]:
    """Times at which r is read to compute x(t,j). Injection: only 0-phases."""
    # Triangle: times t .. t + (-j) if j<0, columns up to 1.
    if j >= 0:
        if j == 1 and word[t % len(word)] == "0":
            return [t]
        return []
    depth = -j
    times = []
    p = len(word)
    for s in range(t, t + depth + 1):
        if word[s % p] == "0":
            times.append(s)
    return times


def eval_with_asg(t: int, j: int, word: str, asg: RAssign) -> int:
    memo = {}
    # ensure all needed r assigned — caller must have done that
    return recon_sat(t, j, word, asg, memo)


def search_onset(word: str, T: int, extra: int = 2, limit: int = 2_000_000):
    """Existential Markov r making L_0 hold at time 0: x(0,-T)=1, zeros left.

    Returns (found, n_nodes, witness_or_none).
    """
    p = len(word)
    nodes = 0
    witness = None

    def need_times():
        s = set()
        for k in range(T, T + extra + 1):
            for tau in needed_r_times(0, -k, word):
                s.add(tau)
        return sorted(s)

    times = need_times()

    def rec(i: int, asg: RAssign) -> bool:
        nonlocal nodes, witness
        nodes += 1
        if nodes > limit:
            return False
        if i == len(times):
            if eval_with_asg(0, -T, word, asg) != 1:
                return False
            for d in range(1, extra + 1):
                if eval_with_asg(0, -T - d, word, asg) != 0:
                    return False
            witness = dict(asg.bits)
            return True
        tau = times[i]
        if asg.get(tau) is not None:
            return rec(i + 1, asg)
        for val in (0, 1):
            nxt = asg.clone()
            if nxt.consistent_set(tau, val) and rec(i + 1, nxt):
                return True
        return False

    found = rec(0, RAssign(word))
    return found, nodes, witness


def search_chain(word: str, T: int, tmax: int, extra: int = 1, limit: int = 3_000_000):
    """Existential r making the moving edge hold for s=0..tmax.

    x(s, -(T+s))=1 and extra zeros to the left.
    Returns max s reached (inclusive) under DFS first-success, and whether
    the full [0,tmax] interval is satisfiable.
    """
    nodes = 0

    def all_times():
        s = set()
        for t in range(tmax + 1):
            edge = T + t
            for k in range(edge, edge + extra + 1):
                for tau in needed_r_times(t, -k, word):
                    s.add(tau)
        return sorted(s)

    times = all_times()

    def ok_prefix(asg: RAssign, tstop: int) -> bool:
        for t in range(tstop + 1):
            edge = T + t
            if eval_with_asg(t, -edge, word, asg) != 1:
                return False
            for d in range(1, extra + 1):
                if eval_with_asg(t, -(edge + d), word, asg) != 0:
                    return False
        return True

    found = False

    def rec(i: int, asg: RAssign) -> bool:
        nonlocal nodes, found
        nodes += 1
        if nodes > limit:
            return False
        if i == len(times):
            if ok_prefix(asg, tmax):
                found = True
                return True
            return False
        tau = times[i]
        if asg.get(tau) is not None:
            return rec(i + 1, asg)
        for val in (0, 1):
            nxt = asg.clone()
            if nxt.consistent_set(tau, val) and rec(i + 1, nxt):
                return True
        return False

    rec(0, RAssign(word))
    return found, nodes, len(times)


def max_chain(word: str, T: int, smax: int, extra: int = 1, limit: int = 2_000_000):
    """Largest s0 such that the chain s=0..s0 is satisfiable, s0<=smax, or -1."""
    best = -1
    for s0 in range(smax + 1):
        found, nodes, _ = search_chain(word, T, s0, extra=extra, limit=limit)
        if not found:
            return best, s0, nodes
        best = s0
    return best, None, 0


def fast_chain(word: str, T: int, extra: int = 1, smax: int = 8, limit: int = 2_000_000):
    """Backtrack injected r (0-phases) in time order; max s with L_0.

    Returns (max_s, nodes). max_s=-1 means even the onset row fails.
    1-phase right bits are omitted (injection lemma); consecutive 0-phase
    bits respect the Markov walk through the intervening 1s.
    """
    p = len(word)
    t_end = T + 2 * smax + extra + 4
    zeros = [t for t in range(t_end) if word[t % p] == "0"]
    nodes = 0
    best = -1
    rlist = [0] * t_end  # 1-phases stay 0; 0-phases get assigned

    def successors(t: int, r: int) -> set[int]:
        """Possible r values at the next 0-time after t."""
        states = {r}
        tau = t
        while True:
            c = int(word[tau % p])
            nxt: set[int] = set()
            for bit in states:
                nxt.update(next_r_choices(c, bit))
            tau += 1
            states = nxt
            if tau >= t_end:
                return states
            if word[tau % p] == "0":
                return states

    def pack() -> int:
        acc = 0
        for i, b in enumerate(rlist):
            if b:
                acc |= 1 << i
        return acc

    def check_s(s: int, assigned_through: int) -> bool | None:
        edge = T + s
        need = edge + extra
        if s + need > assigned_through:
            return None
        bits = pack()
        x = fill_left(word, bits, need, assigned_through + 1)
        if x[s][edge] != 1:
            return False
        for d in range(1, extra + 1):
            if x[s][edge + d] != 0:
                return False
        return True

    def rec(zi: int, last_t: int | None, last_r: int | None, confirmed: int) -> None:
        nonlocal nodes, best
        nodes += 1
        if nodes > limit or best >= smax:
            return
        assigned_through = zeros[zi - 1] if zi else -1
        conf = confirmed
        while True:
            nxt = conf + 1
            if nxt > smax:
                break
            ans = check_s(nxt, assigned_through)
            if ans is None:
                break
            if not ans:
                return
            conf = nxt
            if conf > best:
                best = conf
        if conf >= smax or zi >= len(zeros):
            return
        t = zeros[zi]
        choices = (0, 1)
        if last_t is not None:
            choices = tuple(successors(last_t, last_r))
        for bit in choices:
            rlist[t] = bit
            rec(zi + 1, t, bit, conf)
            rlist[t] = 0
            if best >= smax:
                return

    rec(0, None, None, -1)
    return best, nodes


# ---------------------------------------------------------------------------
# Analytic identities for isolated-zero words 01^q (q>=2)
# ---------------------------------------------------------------------------

def window_10010_phases(word: str) -> list[int]:
    """Phases t where the center reads 10010, hence x(t,-4)=0."""
    ww = word * 3
    return [s for s in range(len(word)) if ww[s : s + 5] == "10010"]


def isolated_zero_column_minus2(q: int) -> dict:
    """Lemma: at phase p-2, x(t,-2)=0 identically, for word 01^q, q>=2."""
    word = "0" + "1" * q
    p = q + 1
    phase = p - 2
    recs = double_one_column_minus2(word)
    hit = next(r for r in recs if r["phase"] == phase)
    return {
        "word": word,
        "phase": phase,
        "k": 2,
        "identically": "0" if hit["ok"] and hit["predicted"] == 0 else hit["observed"],
        "center_at_phase": int(word[phase]),
        "ok": hit["ok"] and hit["predicted"] == 0,
    }


def double_one_column_minus2(word: str) -> list[dict]:
    """At every phase s with c_s=c_{s+1}=1, x(s,-2)=c_{s+2} identically."""
    p = len(word)
    c = [int(b) for b in word]
    predicted = []
    for s in range(p):
        if c[s] == 1 and c[(s + 1) % p] == 1:
            predicted.append(
                {
                    "phase": s,
                    "k": 2,
                    "predicted": c[(s + 2) % p],
                }
            )
    if not predicted:
        return []
    # Algebraic identity: independent of r. Check on two legal strings.
    length = p + 6
    strings = legal_r_strings(word, length)
    samples = [strings[0], strings[len(strings) // 2], strings[-1]]
    out = []
    for pred in predicted:
        vals = {fill_left(word, bits, 2, length)[pred["phase"]][2] for bits in samples}
        ident = str(next(iter(vals))) if len(vals) == 1 else "mixed"
        out.append(
            {
                **pred,
                "observed": ident,
                "ok": vals == {pred["predicted"]},
            }
        )
    return out


def zero_run_column_minus1(word: str) -> list[dict]:
    """On a 0 of the center, x(t,-1)=c_{t+1} XOR r_t; on a 1, x(t,-1)=NOT c_{t+1}."""
    p = len(word)
    c = [int(b) for b in word]
    length = 2 * p + 4
    strings = legal_r_strings(word, length)
    samples = [strings[0], strings[len(strings) // 3], strings[-1]]
    out = []
    for s in range(p):
        if c[s] == 1:
            want = 1 - c[(s + 1) % p]
            vals = {fill_left(word, bits, 1, length)[s][1] for bits in samples}
            out.append(
                {
                    "phase": s,
                    "forced": True,
                    "value": want,
                    "ok": vals == {want},
                }
            )
        else:
            vals = {fill_left(word, bits, 1, length)[s][1] for bits in samples}
            out.append(
                {
                    "phase": s,
                    "forced": False,
                    "values": sorted(vals),
                    "ok": True,
                }
            )
    return out


# ---------------------------------------------------------------------------
# Stronger: look for a column that is a function of the center only
# (hence periodic), which together with the center would give Jen.
# ---------------------------------------------------------------------------

def periodic_left_columns(word: str, kmax: int) -> list[dict]:
    """Columns whose entire p-tuple of phases is identically a fixed word."""
    rows = column_values(word, kmax)
    by_k = {}
    for r in rows:
        by_k.setdefault(r["k"], []).append(r)
    hits = []
    for k, group in by_k.items():
        group = sorted(group, key=lambda r: r["phase"])
        if all(r["identically"] != "mixed" for r in group):
            word_k = "".join(
                "0" if r["identically"] == "0" else "1" for r in group
            )
            hits.append({"k": k, "periodic_word": word_k})
    return hits


# ---------------------------------------------------------------------------
# Onset T that are immediately impossible because x(0,-T) is identically 0
# ---------------------------------------------------------------------------

def immediate_onset_exclusions(word: str, kmax: int) -> list[int]:
    rows = column_values(word, kmax)
    return [r["k"] for r in rows if r["phase"] == 0 and r["identically"] == "0" and r["k"] > 0]


def certify_lemmas() -> dict:
    report: dict = {}
    # Injection lemma on every primitive 3..7
    inj = {}
    for n in range(3, 8):
        for w in primitive_necklaces(n):
            inj[w] = injection_check(w, kmax=6, n_strings=80)
            assert inj[w], w
    report["injection"] = inj

    # Double-1 identity x(s,-2)=c_{s+2}
    d1 = {}
    for n in range(3, 8):
        for w in primitive_necklaces(n):
            recs = double_one_column_minus2(w)
            d1[w] = recs
            for r in recs:
                assert r["ok"], (w, r)
    report["double_one_column_minus2"] = {
        w: recs for w, recs in d1.items() if recs
    }

    # Isolated-zero q>=2: phase p-2, k=2 vanishes
    iz = {}
    for q in range(2, 7):
        rec = isolated_zero_column_minus2(q)
        iz[rec["word"]] = rec
        assert rec["identically"] == "0", rec
    report["isolated_zero_k2"] = iz

    # Vacuum triangle: 1-run of length q determines columns 1..q-1 at the first 1.
    for q in range(2, 7):
        w = "0" + "1" * q
        tri = determined_triangle(w, kmax=q)
        first1 = 1
        depths = {r["k"] for r in tri if r["phase"] == first1}
        assert set(range(1, q)) <= depths, (w, depths)
    report["vacuum_triangle_first_one"] = True

    # 0111: F_4 analog, x(4n,-4)=0 as a polynomial in u.
    w, table, _ = isolated_zero_anfs(3, kmax=4)
    assert table[0][4] == 0
    report["0111_F4"] = True

    # 011 plateau: x(3n,-1)=x(3n,-2)=x(3n,-3)=1+u_n, and B_2=B_4=0.
    w011, tab011, _ = isolated_zero_anfs(2, kmax=4)
    assert tab011[0][1] == tab011[0][2] == tab011[0][3]
    assert tab011[1][2] == 0 and tab011[1][4] == 0
    report["011_plateau_and_B4"] = True

    # 001: F_4 analog at the unique 1, even as an unreduced ANF in the
    # two 0-phase streams (1-phase r never appears).
    idx = var_index_map("001", 16)
    assert cell_anf(2, -4, "001", 20, idx, {}) == 0
    report["001_F4"] = True

    # Uniform 10010 window: x(t,-4)=0 whenever the center reads 10010.
    for n in range(3, 8):
        for w in primitive_necklaces(n):
            ww = w * 3
            for s in range(n):
                if ww[s : s + 5] != "10010":
                    continue
                idx = var_index_map(w, n + 12)
                assert cell_anf(s, -4, w, 30, idx, {}) == 0, (w, s)
    report["window_10010_F4"] = True

    # Isolated-zero ANFs agree with enumeration on constants (small k)
    for q in (2, 3):
        w, table, _ = isolated_zero_anfs(q, kmax=6)
        rows = column_values(w, kmax=6)
        for r in rows:
            poly = table[r["phase"]][r["k"]]
            if r["identically"] == "0":
                assert poly == 0, (w, r, poly)
            elif r["identically"] == "1":
                assert poly == 1, (w, r, poly)
            else:
                assert poly not in (0, 1), (w, r, hex(poly))
    report["anf_matches_enum"] = True

    # Forced left on 1s
    for n in range(3, 8):
        for w in primitive_necklaces(n):
            for rec in zero_run_column_minus1(w):
                assert rec["ok"], (w, rec)

    # Forward inverse roundtrip
    for w in ("001", "011", "0001", "0011", "0111", "00001", "00101"):
        assert verify_against_forward(w, 24), w
    report["forward_recon"] = True

    # Period-2 sanity: word 01 is not in 3..7, but the double-1 identity
    # does not apply (no consecutive 1s). Isolated-one 001 has no consecutive 1s
    # either. Check 011 F-analogue: phase 1, k=2 is 0; also k=4 at phase 1.
    rows = vanishing_table("011", kmax=8)
    report["011_vanishing"] = rows
    assert any(r["phase"] == 1 and r["k"] == 2 and r["identically"] == "0" for r in rows)
    assert any(r["phase"] == 1 and r["k"] == 4 and r["identically"] == "0" for r in rows)

    return report


def scan_all(kmax: int = 10, Tmax: int = 8, smax: int = 4, extra: int = 2) -> dict:
    words = []
    for n in range(3, 8):
        words.extend(primitive_necklaces(n))
    out = {"words": {}}
    for w in words:
        print(f"# {w}", flush=True)
        vanish = vanishing_table(w, kmax)
        periodic = periodic_left_columns(w, kmax)
        imm = immediate_onset_exclusions(w, kmax)
        d1 = double_one_column_minus2(w)
        # onset SAT for each rotation, small T
        onset = []
        for rot in rotations(w):
            for T in range(1, Tmax + 1):
                if T in immediate_onset_exclusions(rot, kmax):
                    onset.append(
                        {
                            "rot": rot,
                            "T": T,
                            "sat": False,
                            "reason": "identically_zero",
                        }
                    )
                    continue
                found, nodes, _ = search_onset(rot, T, extra=extra)
                onset.append(
                    {
                        "rot": rot,
                        "T": T,
                        "sat": found,
                        "nodes": nodes,
                    }
                )
        # chain lifetime for the lexicographic rotation, T with sat onset
        chains = []
        sat_T = sorted(
            {
                rec["T"]
                for rec in onset
                if rec["rot"] == w and rec["sat"]
            }
        )
        for T in sat_T[:6]:
            best, fail_at, nodes = max_chain(w, T, smax, extra=1)
            chains.append(
                {
                    "T": T,
                    "max_s": best,
                    "first_fail": fail_at,
                    "nodes": nodes,
                }
            )
            print(
                f"  chain T={T} max_s={best} fail={fail_at}",
                flush=True,
            )
        rec = {
            "vanishing": vanish,
            "periodic_left_columns": periodic,
            "immediate_T_excluded": imm,
            "double_one": d1,
            "onset": onset,
            "chains": chains,
            "n_vanishing": len(vanish),
            "any_fully_periodic_left_col": bool(periodic),
        }
        out["words"][w] = rec
        print(
            json.dumps(
                {
                    "word": w,
                    "n_vanish": len(vanish),
                    "periodic_left": periodic,
                    "imm_T": imm,
                    "onset_unsat": [
                        (r["rot"], r["T"])
                        for r in onset
                        if not r["sat"]
                    ][:20],
                    "chains": chains,
                }
            ),
            flush=True,
        )
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--kmax", type=int, default=10)
    parser.add_argument("--Tmax", type=int, default=8)
    parser.add_argument("--smax", type=int, default=3)
    parser.add_argument("--json-out", type=str, default="")
    parser.add_argument("--word", type=str, default="")
    parser.add_argument("--identities", action="store_true")
    parser.add_argument("--chains", action="store_true")
    args = parser.parse_args()

    if args.identities:
        for n in range(3, 8):
            for w in primitive_necklaces(n):
                vac = [
                    (r["phase"], r["k"], r["value"])
                    for r in determined_triangle(w, kmax=len(w))
                ]
                extra = []
                if w.count("0") == 1:
                    q = w.count("1")
                    ids = isolated_zero_identities(q, args.kmax)
                    extra = [
                        (r["phase"], r["k"], r["anf"])
                        for r in ids
                        if r["anf"] in ("0", "1") and r["k"] > 0
                        and (r["phase"], r["k"]) not in {(a, b) for a, b, _ in vac}
                    ]
                else:
                    rows = column_values(w, kmax=min(args.kmax, 8), extra_periods=1)
                    vac_set = {(a, b) for a, b, _ in vac}
                    extra = [
                        (r["phase"], r["k"], r["identically"])
                        for r in rows
                        if r["k"] > 0
                        and r["identically"] in ("0", "1")
                        and (r["phase"], r["k"]) not in vac_set
                    ]
                print(
                    json.dumps({"word": w, "vacuum": vac, "extra_const": extra})
                )
        return

    if args.chains:
        focus = []
        if args.word:
            focus = [args.word]
        else:
            for n in range(3, 6):
                focus.extend(primitive_necklaces(n))
        payload = {}
        for w in focus:
            rows = []
            for rot in rotations(w)[: min(len(w), 3)]:
                for T in range(1, args.Tmax + 1):
                    best, nodes = fast_chain(
                        rot, T, extra=1, smax=args.smax, limit=400000
                    )
                    rows.append(
                        {
                            "rot": rot,
                            "T": T,
                            "max_s": best,
                            "nodes": nodes,
                        }
                    )
                    print(
                        f"{rot} T={T} max_s={best} nodes={nodes}",
                        flush=True,
                    )
            payload[w] = rows
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump(payload, f, indent=2)
                f.write("\n")
        return

    if args.certify:
        report = certify_lemmas()
        print("certify: all assertions passed")
        # compact print
        slim = {
            "injection_all": all(report["injection"].values()),
            "forward_recon": report["forward_recon"],
            "001_F4": report.get("001_F4"),
            "0111_F4": report.get("0111_F4"),
            "011_plateau_and_B4": report.get("011_plateau_and_B4"),
            "window_10010_F4": report.get("window_10010_F4"),
            "isolated_zero_k2": {
                w: v["identically"] for w, v in report["isolated_zero_k2"].items()
            },
            "n_words_with_double_one": len(report["double_one_column_minus2"]),
        }
        print(json.dumps(slim, indent=2))
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        return

    if args.word:
        w = args.word
        vanish = vanishing_table(w, args.kmax)
        print("vanishing:", json.dumps(vanish, indent=2))
        print("periodic left:", periodic_left_columns(w, args.kmax))
        print("immediate T:", immediate_onset_exclusions(w, args.kmax))
        for T in range(1, args.Tmax + 1):
            found, nodes, _ = search_onset(w, T, extra=2)
            print(f"onset T={T} sat={found} nodes={nodes}")
            if found:
                best, fail, n2 = max_chain(w, T, args.smax, extra=1)
                print(f"  chain max_s={best} fail={fail} nodes={n2}")
        return

    if args.scan:
        report = {"lemmas": certify_lemmas()}
        report["scan"] = scan_all(
            kmax=args.kmax, Tmax=args.Tmax, smax=args.smax
        )
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        return

    report = certify_lemmas()
    print("certify: all assertions passed")
    print("injection:", all(report["injection"].values()))
    print("011 vanishing columns:", report["011_vanishing"])


if __name__ == "__main__":
    main()
