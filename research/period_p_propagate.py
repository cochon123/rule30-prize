"""Implication system for period-p left-edge phase masks (Astra attack 3).

Two adjacent temporal columns, spatial displacements d=4,8, radius-3 right
consistency. Focus words: 001 and 0111, starting from their depth-4 zeros.

Does not modify strip_graph.py / strip_extend.py.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from period_p_left_edge import (  # noqa: E402
    anf_str,
    band,
    bor,
    cell_anf,
    eval_anf,
    fill_left,
    inject_times,
    isolated_zero_anfs,
    legal_r_strings,
    next_r_choices,
    var_index_map,
)

ONE = 1


# ---------------------------------------------------------------------------
# Radius-3 right automaton
# State: (x1,x2,x3) = columns +1,+2,+3. Far bit x4 free.
# ---------------------------------------------------------------------------

def r3_step(c: int, x1: int, x2: int, x3: int, x4: int) -> tuple[int, int, int]:
    y1 = c ^ (x1 | x2)
    y2 = x1 ^ (x2 | x3)
    y3 = x2 ^ (x3 | x4)
    return (y1, y2, y3)


def r3_successors(c: int, st: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    x1, x2, x3 = st
    seen = []
    for x4 in (0, 1):
        nxt = r3_step(c, x1, x2, x3, x4)
        if nxt not in seen:
            seen.append(nxt)
    return seen


def r3_markov_superset(c: int, r: int) -> tuple[int, ...]:
    """One-step Markov on column +1, for comparison."""
    return next_r_choices(c, r)


def vacuum_implications(word: str) -> dict:
    """Exact one-step images of right-vacuum states, by center phase."""
    p = len(word)
    rows = []
    for a in range(p):
        c = int(word[a])
        for st in product((0, 1), repeat=3):
            zeros_right = st[1] == 0 and st[2] == 0  # columns +2,+3 vacuum
            succs = r3_successors(c, st)
            r1_next = sorted({s[0] for s in succs})
            rows.append(
                {
                    "phase": a,
                    "center": c,
                    "state": "".join(str(b) for b in st),
                    "vacuum_plus23": zeros_right,
                    "full_vacuum": st == (0, 0, 0),
                    "succ": ["".join(str(b) for b in s) for s in succs],
                    "r_next": r1_next,
                    "r_next_forced": r1_next[0] if len(r1_next) == 1 else None,
                }
            )
    full_vac = [r for r in rows if r["full_vacuum"]]
    plus23 = [r for r in rows if r["vacuum_plus23"]]
    return {"full_vacuum": full_vac, "plus23_vacuum": plus23, "all": rows}


def r3_injected_r(word: str, length: int) -> list[int]:
    """Unique r-bitstrings of `length` with 1-phase bits dummy-0, realizable
    as column +1 of some radius-3 path. Injection lemma: left cells ignore
    1-phase r, so these are exactly the R3-legal left reconstructions.
    """
    from collections import deque

    p = len(word)
    seen_pack = set()
    dq = deque()
    visited_layer_cap = 4_000_000
    seen_keys = set()
    for st0 in product((0, 1), repeat=3):
        pack = st0[0] if word[0] == "0" else 0
        key0 = (0, st0, pack)
        if key0 in seen_keys:
            continue
        seen_keys.add(key0)
        dq.append((0, st0, pack))
    while dq:
        t, st, pack = dq.popleft()
        if len(seen_keys) > visited_layer_cap:
            raise RuntimeError(f"r3 BFS overflow at t={t} word={word} L={length}")
        if t == length - 1:
            seen_pack.add(pack)
            continue
        c = int(word[t % p])
        for nxt in r3_successors(c, st):
            npack = pack
            t2 = t + 1
            if word[t2 % p] == "0" and nxt[0]:
                npack = pack | (1 << t2)
            key = (t2, nxt, npack)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            dq.append((t2, nxt, npack))
    return sorted(seen_pack)


def _next_zero_r(word: str, t: int, r: int, t_end: int) -> set[int]:
    """Possible r values at the next 0-phase after time t (r assigned at t)."""
    p = len(word)
    states = {r}
    tau = t
    while tau + 1 < t_end:
        c = int(word[tau % p])
        nxt: set[int] = set()
        for bit in states:
            nxt.update(next_r_choices(c, bit))
        tau += 1
        states = nxt
        if word[tau % p] == "0":
            return states
    return set()


def markov_injected_r(word: str, length: int) -> list[int]:
    """Unique 0-phase r assignments of `length` under one-step Markov.

    1-phase bits are dummy 0. Branches only at 0-phases.
    """
    p = len(word)
    zeros = [t for t in range(length) if word[t % p] == "0"]
    out: set[int] = set()

    def rec(zi: int, acc: int, last_t: int | None, last_r: int | None) -> None:
        if zi == len(zeros):
            out.add(acc)
            return
        t = zeros[zi]
        if last_t is None:
            choices = (0, 1)
        else:
            choices = tuple(_next_zero_r(word, last_t, last_r, length))
            if not choices:
                out.add(acc)
                return
        for bit in choices:
            nacc = acc | ((1 << t) if bit else 0)
            rec(zi + 1, nacc, t, bit)

    rec(0, 0, None, None)
    return sorted(out)


def iter_left_r(word: str, length: int, radius3: bool) -> list[int]:
    if radius3:
        return r3_injected_r(word, length)
    return markov_injected_r(word, length)


def _self_check_inverse(word: str = "001") -> None:
    """iterate_left must match fill_left on a sample string."""
    length = 20
    bits = iter_left_r(word, length, False)[len(iter_left_r(word, length, False)) // 3]
    k, d, w = 4, 4, 14
    x = fill_left(word, bits, k + d, length)
    packed = two_col_window(x, 0, k, w)
    assert packed is not None
    ck, cm = packed
    got = iterate_left(ck, cm, w, d)
    assert got is not None
    ck2, cm2, w2 = got
    for i in range(w2):
        assert ((ck2 >> i) & 1) == x[i][k + d], (i, word)
        assert ((cm2 >> i) & 1) == x[i][k + d - 1], (i, word)


def injected_language(word: str, n_periods: int, radius3: bool) -> dict:
    """Language of injected 0-phase right bits over n_periods, Markov vs R3."""
    p = len(word)
    length = n_periods * p + 1
    zeros = [t for t in range(length) if word[t % p] == "0"]
    strings = iter_left_r(word, length, radius3)
    packed = set()
    for bits in strings:
        acc = 0
        for i, t in enumerate(zeros):
            if (bits >> t) & 1:
                acc |= 1 << i
        packed.add(acc)
    n_inj = len(zeros)
    return {
        "n_injected": n_inj,
        "n_legal": len(packed),
        "n_possible": 1 << n_inj,
        "all_free": len(packed) == (1 << n_inj),
        "samples": sorted(packed)[:32],
        "n_raw_injected": len(strings),
    }


# ---------------------------------------------------------------------------
# Unconditional phase masks at each depth
# ---------------------------------------------------------------------------

def mask_from_values(vals_by_phase: list[set[int]]) -> dict:
    forced0, forced1, mixed = [], [], []
    for a, vs in enumerate(vals_by_phase):
        if vs == {0}:
            forced0.append(a)
        elif vs == {1}:
            forced1.append(a)
        else:
            mixed.append(a)
    return {"forced0": forced0, "forced1": forced1, "mixed": mixed}


def unconditional_masks(word: str, kmax: int, radius3: bool, extra: int = 2) -> dict:
    """For each depth k, the phase mask of identically forced bits."""
    p = len(word)
    length = kmax + p + extra
    strings = iter_left_r(word, length, radius3)
    # first[k][s] = first value or -1 if mixed
    first = [[None] * p for _ in range(kmax + 1)]
    mixed = [[False] * p for _ in range(kmax + 1)]
    for bits in strings:
        x = fill_left(word, bits, kmax, length)
        for k in range(kmax + 1):
            for s in range(p):
                if s + k >= length or mixed[k][s]:
                    continue
                val = x[s][k]
                if first[k][s] is None:
                    first[k][s] = val
                elif first[k][s] != val:
                    mixed[k][s] = True
    by_k = {}
    for k in range(kmax + 1):
        vals = []
        for s in range(p):
            if mixed[k][s] or first[k][s] is None:
                vals.append({0, 1})
            else:
                vals.append({first[k][s]})
        by_k[k] = mask_from_values(vals)
        by_k[k]["values"] = [sorted(v) for v in vals]
    return {
        "word": word,
        "radius3": radius3,
        "n_strings": len(strings),
        "length": length,
        "by_k": {str(k): by_k[k] for k in range(kmax + 1)},
    }


# ---------------------------------------------------------------------------
# Two-column windows and implication maps
# ---------------------------------------------------------------------------

def two_col_window(x, t0: int, k: int, w: int) -> tuple[int, int] | None:
    """Pack (col k, col k-1) over times t0..t0+w-1. col -1 is not in x; k>=1."""
    tmax = len(x)
    if t0 + w > tmax:
        return None
    if t0 + (w - 1) + k >= tmax:
        # fill_left only writes x[t][k] for t < tmax-k
        need = t0 + w - 1
        if need + k >= tmax:
            return None
    ck = 0
    cm = 0
    for i in range(w):
        t = t0 + i
        if t + k >= tmax:
            return None
        ck |= x[t][k] << i
        if k == 0:
            return None
        cm |= x[t][k - 1] << i
    return ck, cm


def collect_two_col(word: str, k: int, w: int, radius3: bool, extra: int = 2,
                    t0_phases: list[int] | None = None):
    """Set of (col_k, col_{k-1}) windows of width w starting at given phases."""
    p = len(word)
    if t0_phases is None:
        t0_phases = list(range(p))
    length = k + w + extra
    strings = iter_left_r(word, length, radius3)
    by_phase = {a: set() for a in t0_phases}
    for bits in strings:
        x = fill_left(word, bits, k, length)
        for a in t0_phases:
            packed = two_col_window(x, a, k, w)
            if packed is not None:
                by_phase[a].add(packed)
    return {
        "word": word,
        "k": k,
        "w": w,
        "radius3": radius3,
        "n_strings": len(strings),
        "n_windows": {str(a): len(by_phase[a]) for a in t0_phases},
        "windows": {str(a): sorted(by_phase[a]) for a in t0_phases},
    }


def extend_pair_left(ck: int, cm: int, w: int) -> int | None:
    """One inverse step: col_{k+1}[0..w-2] from (col_k, col_{k-1}) width w.

    x(t,-(k+1)) = x(t+1,-k) XOR (x(t,-k) OR x(t,-(k-1))).
    Returns packed bits of length w-1, or None if w<2.
    """
    if w < 2:
        return None
    out = 0
    for t in range(w - 1):
        fut = (ck >> (t + 1)) & 1
        a = (ck >> t) & 1
        b = (cm >> t) & 1
        out |= (fut ^ (a | b)) << t
    return out


def iterate_left(ck: int, cm: int, w: int, d: int) -> tuple[int, int, int] | None:
    """Apply inverse d times. Returns (col_{k+d}, col_{k+d-1}, width_left)."""
    width = w
    a, b = ck, cm
    for _ in range(d):
        nxt = extend_pair_left(a, b, width)
        if nxt is None:
            return None
        b, a = a, nxt
        width -= 1
        # col_{k+1} lives on width-1; adjacent older column is previous `a`
        # after assignment: a = new col, b = old col (now adjacent)
        # but b still has the old width, while a has width-1. Trim b.
        b &= (1 << width) - 1
    return a, b, width


def implication_from_mask(word: str, k: int, d: int, w: int, radius3: bool,
                          restrict0: list[int] | None = None,
                          extra: int = 2) -> dict:
    """Windows at depth k, optionally restricted to zeros at given offsets
    of column k (relative to window start). Inverse d steps need no extra r.

    Report forced bits of column k+d on the surviving output window.
    """
    p = len(word)
    rec = collect_two_col(word, k, w, radius3, extra=extra, t0_phases=list(range(p)))
    out_vals = {a: [set() for _ in range(max(0, w - d))] for a in range(p)}
    n_kept = {a: 0 for a in range(p)}
    n_seen = {a: 0 for a in range(p)}
    pair_in = {a: set() for a in range(p)}
    pair_out = {a: set() for a in range(p)}
    for a in range(p):
        for ck, cm in rec["windows"][str(a)]:
            n_seen[a] += 1
            if restrict0:
                ok = True
                for off in restrict0:
                    if (ck >> off) & 1:
                        ok = False
                        break
                if not ok:
                    continue
            n_kept[a] += 1
            pair_in[a].add((ck, cm))
            got = iterate_left(ck, cm, w, d)
            if got is None:
                continue
            ck2, cm2, w2 = got
            pair_out[a].add((ck2, cm2, w2))
            for i in range(w2):
                out_vals[a][i].add((ck2 >> i) & 1)
    forced0, forced1, mixed = {}, {}, {}
    for a in range(p):
        z, o, m = [], [], []
        for i, vs in enumerate(out_vals[a]):
            if vs == {0}:
                z.append(i)
            elif vs == {1}:
                o.append(i)
            else:
                m.append(i)
        forced0[a] = z
        forced1[a] = o
        mixed[a] = m
    return {
        "word": word,
        "k": k,
        "d": d,
        "w": w,
        "radius3": radius3,
        "restrict0_offsets": restrict0,
        "n_strings": rec["n_strings"],
        "n_seen": n_seen,
        "n_kept": n_kept,
        "n_unique_in": {str(a): len(pair_in[a]) for a in range(p)},
        "n_unique_out": {str(a): len(pair_out[a]) for a in range(p)},
        "out_forced0_offsets": {str(a): forced0[a] for a in range(p)},
        "out_forced1_offsets": {str(a): forced1[a] for a in range(p)},
        "out_mixed_offsets": {str(a): mixed[a] for a in range(p)},
        "out_width": w - d,
    }


def mask_implication_table(word: str, k: int, d: int, w: int, radius3: bool,
                           src_forced0_phases: list[int]) -> dict:
    """Restrict windows starting at phase a so that col_k is 0 at each
    time t with (t mod p) in src_forced0_phases (intersected with the window).

    Then read forced zeros of col_{k+d} as absolute phases.
    """
    p = len(word)
    # offsets in a window starting at phase a that land on a src phase
    recs = []
    for a in range(p):
        offs = [i for i in range(w) if (a + i) % p in src_forced0_phases]
        impl = implication_from_mask(
            word, k, d, w, radius3, restrict0=offs if offs else None
        )
        # convert output offsets to absolute phases
        f0_abs = sorted({(a + i) % p for i in impl["out_forced0_offsets"][str(a)]})
        f1_abs = sorted({(a + i) % p for i in impl["out_forced1_offsets"][str(a)]})
        recs.append(
            {
                "t0_phase": a,
                "restrict_offsets": offs,
                "out_forced0_phases": f0_abs,
                "out_forced1_phases": f1_abs,
                "n_kept": impl["n_kept"][a],
                "n_unique_in": impl["n_unique_in"][str(a)],
                "n_unique_out": impl["n_unique_out"][str(a)],
            }
        )
    return {
        "word": word,
        "k": k,
        "d": d,
        "w": w,
        "radius3": radius3,
        "src_forced0_phases": src_forced0_phases,
        "by_t0": recs,
    }


# ---------------------------------------------------------------------------
# ANF relations among injected bits (001 and 0111)
# ---------------------------------------------------------------------------

def column_anfs(word: str, kmax: int, n_periods: int | None = None):
    p = len(word)
    if n_periods is None:
        n_periods = (kmax + p) // p + 4
    tmax = n_periods * p + kmax + 2
    idx = var_index_map(word, tmax)
    vmax = max(idx.values()) + 1 if idx else 0
    memo: dict = {}
    table = []
    for s in range(p):
        row = []
        for k in range(kmax + 1):
            row.append(cell_anf(s, -k, word, vmax, idx, memo))
        table.append(row)
    names = []
    # names by variable index: physical times
    inv = {v: t for t, v in idx.items()}
    for vi in range(vmax):
        t = inv.get(vi, None)
        if t is None:
            names.append(f"v{vi}")
        else:
            names.append(f"r{t}")
    return table, names, idx, vmax


def anf_relations(word: str, kmax: int = 12) -> dict:
    table, names, idx, vmax = column_anfs(word, kmax)
    p = len(word)
    const = []
    simple = []
    for s in range(p):
        for k in range(kmax + 1):
            poly = table[s][k]
            rec = {
                "phase": s,
                "k": k,
                "anf": anf_str(poly, names),
                "const": poly in (0, 1),
            }
            if poly in (0, 1):
                const.append({**rec, "value": poly})
            elif poly.bit_count() <= 4:
                simple.append(rec)
    coinc = []
    zeros = sorted(idx)
    if not zeros:
        return {"const": const, "simple": simple, "shift_coincidences": []}

    def shift_poly2(poly: int, h_periods: int) -> int | None:
        inv = {v: t for t, v in idx.items()}
        res = 0
        m = 0
        pp = poly
        while pp:
            if pp & 1:
                if m == 0:
                    res ^= 1
                else:
                    need = m >> 1
                    new_need = 0
                    b = 0
                    tmp = need
                    while tmp:
                        if tmp & 1:
                            t = inv.get(b)
                            if t is None:
                                return None
                            t2 = t + h_periods * p
                            if t2 not in idx:
                                return None
                            new_need |= 1 << idx[t2]
                        tmp >>= 1
                        b += 1
                    res ^= 1 << (new_need << 1)
            pp >>= 1
            m += 1
        return res

    # Use shift_poly2 only. Search coincidences for modest k.
    for s in range(p):
        for k in range(1, kmax + 1):
            poly = table[s][k]
            if poly in (0, 1):
                continue
            for h in (1, 2):
                sp = shift_poly2(poly, h)
                if sp is None:
                    continue
                for s2 in range(p):
                    for k2 in range(1, kmax + 1):
                        if (s2, k2) == (s, k):
                            continue
                        if table[s2][k2] == sp:
                            coinc.append(
                                {
                                    "src": [s, k],
                                    "dst": [s2, k2],
                                    "h_periods": h,
                                    "anf": anf_str(poly, names),
                                }
                            )
    # d-vs-k equalities without shift
    equal = []
    for s in range(p):
        for k in range(1, kmax + 1):
            for d in (4, 8):
                kd = k + d
                if kd > kmax:
                    continue
                if table[s][kd] == table[s][k] and table[s][k] not in (0, 1):
                    equal.append({"phase": s, "k": k, "k+d": kd, "kind": "same_poly"})
                for h in range(p):
                    s2 = (s + h) % p
                    if table[s2][kd] == table[s][k] and table[s][k] not in (0, 1):
                        equal.append(
                            {
                                "phase": s,
                                "k": k,
                                "phase2": s2,
                                "k+d": kd,
                                "h": h,
                                "kind": "phase_shift_same_poly",
                            }
                        )
    return {
        "word": word,
        "vmax": vmax,
        "const": const,
        "simple": simple[:80],
        "shift_coincidences": coinc[:40],
        "d_equalities": equal[:40],
    }


def enum_shift_relations(word: str, kmax: int, radius3: bool) -> dict:
    """Exact (not ANF) search: is x(s, -(k+d)) equal to x(s+h, -k) after
    shifting injected bits by n periods, on every legal left-r string.
    """
    p = len(word)
    n_per = (kmax + 8) // p + 4
    length = n_per * p
    strings = iter_left_r(word, length, radius3)
    zeros = [t for t in range(length) if word[t % p] == "0"]

    def pack_inj(bits: int) -> int:
        acc = 0
        for i, t in enumerate(zeros):
            if (bits >> t) & 1:
                acc |= 1 << i
        return acc

    cols = {}
    for bits in strings:
        x = fill_left(word, bits, kmax, length)
        inj = pack_inj(bits)
        for s in range(p):
            for k in range(kmax + 1):
                if s + k >= length:
                    continue
                cols.setdefault((s, k), {})[inj] = x[s][k]

    n_inj_per = sum(1 for t in range(p) if word[t] == "0")

    def shift_pack(inj: int, h_periods: int) -> int:
        # drop the first h_periods * n_inj_per bits, keep the rest
        drop = h_periods * n_inj_per
        return inj >> drop

    hits = []
    for d in (4, 8):
        for h_t in range(0, d + 1):  # time delay in steps
            for h_u in range(0, 3):
                for s in range(p):
                    for k in range(0, kmax - d + 1):
                        s2 = (s + h_t) % p
                        kd = k + d
                        src = cols.get((s, k), {})
                        dst = cols.get((s2, kd), {})
                        if not src or not dst:
                            continue
                        # compare dst[inj] vs src[shift_pack(inj)] / 1+src
                        n = 0
                        n_eq = n_plus = n_eq_un = n_plus_un = 0
                        for inj, val_d in dst.items():
                            sh = shift_pack(inj, h_u)
                            if sh not in src and inj not in src:
                                continue
                            n += 1
                            if inj in src:
                                if val_d == src[inj]:
                                    n_eq_un += 1
                                if val_d == (src[inj] ^ 1):
                                    n_plus_un += 1
                            if sh in src:
                                if val_d == src[sh]:
                                    n_eq += 1
                                if val_d == (src[sh] ^ 1):
                                    n_plus += 1
                        if n < 4:
                            continue
                        rel = None
                        if n_eq == n:
                            rel = "equal_shift_u"
                        elif n_plus == n:
                            rel = "one_plus_shift_u"
                        elif n_eq_un == n:
                            rel = "equal_unshifted"
                        elif n_plus_un == n:
                            rel = "one_plus_unshifted"
                        if rel:
                            hits.append(
                                {
                                    "s": s,
                                    "k": k,
                                    "s2": s2,
                                    "k2": kd,
                                    "d": d,
                                    "h_time": h_t,
                                    "h_u": h_u,
                                    "rel": rel,
                                    "n": n,
                                }
                            )
    # Prefer non-constant columns: drop those where src is constant 0/1
    nonconst = []
    for rec in hits:
        src_vals = set(cols[(rec["s"], rec["k"])].values())
        dst_vals = set(cols[(rec["s2"], rec["k2"])].values())
        rec["src_const"] = src_vals in ({0}, {1})
        rec["dst_const"] = dst_vals in ({0}, {1})
        if not rec["src_const"]:
            nonconst.append(rec)
    return {
        "word": word,
        "radius3": radius3,
        "n_strings": len(strings),
        "n_hits": len(hits),
        "n_nonconst": len(nonconst),
        "nonconst": nonconst[:40],
        "const_hits_sample": [h for h in hits if h.get("src_const")][:15],
    }


def fibonacci_u_check(word: str, n_periods: int) -> dict:
    """Does radius-3 forbid consecutive 1s on the 0-phase stream?"""
    p = len(word)
    length = n_periods * p
    zeros = [t for t in range(length) if word[t % p] == "0"]
    rec = {}
    for radius3, name in ((False, "markov"), (True, "r3")):
        strings = iter_left_r(word, length, radius3)
        packs = []
        consec = False
        for bits in strings:
            acc = 0
            prev = 0
            for i, t in enumerate(zeros):
                b = (bits >> t) & 1
                if b and prev:
                    consec = True
                prev = b
                if b:
                    acc |= 1 << i
            packs.append(acc)
        rec[name] = {
            "n": len(strings),
            "n_unique": len(set(packs)),
            "has_consecutive_ones": consec,
            "all_free": len(set(packs)) == (1 << len(zeros)),
        }
    rec["r3_is_fibonacci"] = (
        not rec["r3"]["has_consecutive_ones"] and rec["markov"]["has_consecutive_ones"]
    )
    return rec


# ---------------------------------------------------------------------------
# L_0 local germ transport (do not repeat the period-2 failed descent)
# ---------------------------------------------------------------------------

def l0_germ_transport(word: str, kmax: int, R: int, radius3: bool,
                      extra: int = 2) -> dict:
    """If x(t,-k)=1 and R further zeros, what is the window at (t+h, k+d)?

    Collect image patterns for d in {4,8}, h in 0..d. A successful descent
    would map 1-then-zeros to 1-then-zeros (or all zeros) with h<d. A bump
    (extra 1s near the image edge) is the period-2 failure mode.
    """
    p = len(word)
    length = kmax + R + p + extra + 8
    strings = iter_left_r(word, length, radius3)
    ds = (4, 8)
    hs = list(range(0, 9))
    stats = {
        d: {
            h: {
                "n": 0,
                "image_is_l0": 0,
                "image_forced0": 0,
                "image_bump": 0,
                "edge_bit_1": 0,
                "edge_bit_0": 0,
                "tail_patterns": defaultdict(int),
            }
            for h in hs
        }
        for d in ds
    }
    n_germs = 0
    n_strings_with_germ = 0
    kfill = kmax + 8 + R + 2
    for bits in strings:
        x = fill_left(word, bits, kfill, length)
        found_here = False
        for t in range(p):
            for k in range(1, kmax + 1):
                if t + k + R >= length:
                    continue
                if x[t][k] != 1:
                    continue
                if any(x[t][k + j] != 0 for j in range(1, R + 1)):
                    continue
                n_germs += 1
                found_here = True
                for d in ds:
                    for h in hs:
                        t2 = t + h
                        k2 = k + d
                        if t2 >= length or k2 + R >= kfill:
                            continue
                        if t2 + k2 + R >= length:
                            continue
                        st = stats[d][h]
                        st["n"] += 1
                        edge = x[t2][k2]
                        if edge:
                            st["edge_bit_1"] += 1
                        else:
                            st["edge_bit_0"] += 1
                        tail = tuple(x[t2][k2 + j] for j in range(0, min(R + 1, 6)))
                        pat = "".join(str(b) for b in tail)
                        if len(st["tail_patterns"]) < 40 or pat in st["tail_patterns"]:
                            st["tail_patterns"][pat] += 1
                        ntail = min(R, max(0, length - t2 - k2 - 1))
                        if ntail <= 0:
                            continue
                        zeros_ok = all(x[t2][k2 + j] == 0 for j in range(1, ntail + 1))
                        if edge == 1 and zeros_ok:
                            st["image_is_l0"] += 1
                        elif edge == 0 and zeros_ok:
                            st["image_forced0"] += 1
                        elif not zeros_ok:
                            st["image_bump"] += 1
        if found_here:
            n_strings_with_germ += 1

    def slim(st):
        n = st["n"] or 1
        tops = sorted(st["tail_patterns"].items(), key=lambda kv: -kv[1])[:8]
        return {
            "n": st["n"],
            "frac_l0": round(st["image_is_l0"] / n, 4),
            "frac_forced0": round(st["image_forced0"] / n, 4),
            "frac_bump": round(st["image_bump"] / n, 4),
            "frac_edge1": round(st["edge_bit_1"] / n, 4),
            "top_tails": tops,
            "always_l0": st["n"] > 0 and st["image_is_l0"] == st["n"],
            "always_forced0": st["n"] > 0 and st["image_forced0"] == st["n"],
            "always_bump": st["n"] > 0 and st["image_bump"] == st["n"],
        }

    out_stats = {
        str(d): {str(h): slim(stats[d][h]) for h in hs} for d in ds
    }
    # Closed (d,h) candidates: always_l0 or always_forced0, with h<d
    cands = []
    for d in ds:
        for h in hs:
            s = slim(stats[d][h])
            if s["n"] == 0:
                continue
            if (s["always_l0"] or s["always_forced0"]) and h < d:
                cands.append({"d": d, "h": h, **s})
    return {
        "word": word,
        "kmax": kmax,
        "R": R,
        "radius3": radius3,
        "n_strings": len(strings),
        "n_germs": n_germs,
        "n_strings_with_germ": n_strings_with_germ,
        "stats": out_stats,
        "closed_candidates": cands,
    }


# ---------------------------------------------------------------------------
# Cycle search on unconditional + restricted forced-zero masks
# ---------------------------------------------------------------------------

def forced0_phases_at(masks_by_k: dict, k: int) -> list[int]:
    rec = masks_by_k[str(k)]
    return list(rec["forced0"])


def cycle_search(word: str, masks: dict, d: int, k0: int = 4, steps: int = 3) -> dict:
    """Does the unconditional forced-zero mask at k0 reproduce at k0+m*d
    with a phase shift h, h<d, covering every onset residue vs k=T+s?
    """
    p = len(word)
    by_k = masks["by_k"]
    kmax = max(int(k) for k in by_k)
    z0 = forced0_phases_at(by_k, k0)
    chain = [{"k": k0, "forced0": z0}]
    for m in range(1, steps + 1):
        k = k0 + m * d
        if k > kmax:
            break
        chain.append({"k": k, "forced0": forced0_phases_at(by_k, k)})

    # possible h: z_{m} == (z0 + m*h) mod p, or inclusion
    h_hits = []
    for h in range(0, d):
        ok_eq = True
        ok_inc = True
        for m, rec in enumerate(chain):
            want = sorted({(a + m * h) % p for a in z0})
            got = rec["forced0"]
            if got != want:
                ok_eq = False
            if not set(want) <= set(got):
                # got may be smaller: inclusion the other way
                ok_inc = False
        # also allow got containing a shift even if z0 empty later
        h_hits.append({"h": h, "equal_orbit": ok_eq, "contains_orbit": ok_inc})

    # Edge intersection: for each onset residue ρ=T mod p, exists m,s with
    # T+s = k0+m d and s ≡ α (mod p) for some α in Z(k0+md).
    # For large T this is: ρ ∈ {k0 + m d - α : α ∈ Z(k)} (mod p) for some m.
    coverage = []
    residues_hit = set()
    for m, rec in enumerate(chain):
        k = rec["k"]
        Z = rec["forced0"]
        hit_here = set()
        for alpha in Z:
            # ρ + s = k with s≡α, so ρ ≡ k-α (mod p), taking s=α (one period)
            hit_here.add((k - alpha) % p)
        residues_hit |= hit_here
        coverage.append({"k": k, "T_mod_p_killed": sorted(hit_here), "Z": Z})
    return {
        "word": word,
        "d": d,
        "k0": k0,
        "chain": chain,
        "h_tests": h_hits,
        "any_closed_h": any(
            x["equal_orbit"] and 0 <= x["h"] < d and z0 and len(chain) >= 2
            for x in h_hits
        ),
        "T_residues_killed_by_chain": sorted(residues_hit),
        "all_onset_residues": residues_hit == set(range(p)),
        "coverage": coverage,
        "note": (
            "Unconditional masks only kill those (T mod p) for which some "
            "depth in the chain is a forced zero on the matching edge phase. "
            "Finite depths ⇒ only finite T=k-s."
        ),
    }


def edge_cover_conditional(word: str, k: int, d: int, w: int, radius3: bool,
                           src_phases: list[int]) -> dict:
    """Using restricted implication, which (phase of col k+d) are forced 0
    for every window-start, hence which moving-edge residues could be hit
    at depth k+d independently of t0.
    """
    tab = mask_implication_table(word, k, d, w, radius3, src_phases)
    p = len(word)
    # intersection of out_forced0_phases over all t0
    common = None
    union = set()
    for rec in tab["by_t0"]:
        s = set(rec["out_forced0_phases"])
        union |= s
        common = s if common is None else (common & s)
    common = sorted(common or [])
    # Moving edge at depth K=k+d: phase a ≡ s (mod p), k_edge=T+s=K ⇒ T≡K-a
    killed = sorted({((k + d) - a) % p for a in common})
    killed_union = sorted({((k + d) - a) % p for a in union})
    return {
        **{kk: tab[kk] for kk in ("word", "k", "d", "w", "radius3", "src_forced0_phases")},
        "common_forced0_phases": common,
        "union_forced0_phases": sorted(union),
        "T_residues_if_common": killed,
        "T_residues_if_union": killed_union,
        "by_t0": tab["by_t0"],
        "covers_all_residues_common": set(killed) == set(range(p)),
    }


# ---------------------------------------------------------------------------
# Two-column Boolean relations at k=4 (starting identities)
# ---------------------------------------------------------------------------

def two_col_relations_at_depth(word: str, k: int, radius3: bool) -> dict:
    """Phase-wise values of (col k, col k-1) as ANF / enumerated pairs,
    plus relations among injected bits on those columns.
    """
    p = len(word)
    w = p  # one period
    rec = collect_two_col(word, k, w, radius3, extra=3, t0_phases=list(range(p)))
    # For each phase a (window start), unique pairs; also per-time bits
    rels = []
    for a in range(p):
        pairs = rec["windows"][str(a)]
        # bits at offset 0 of the window are the actual phase-a cells
        ck_bits = {(ck >> 0) & 1 for ck, cm in pairs}
        cm_bits = {(cm >> 0) & 1 for ck, cm in pairs}
        # correlation
        joint = sorted(set(pairs))
        # Does ck determine cm or vice versa?
        by_ck = defaultdict(set)
        by_cm = defaultdict(set)
        for ck, cm in pairs:
            by_ck[ck].add(cm)
            by_cm[cm].add(ck)
        ck_det_cm = all(len(v) == 1 for v in by_ck.values())
        cm_det_ck = all(len(v) == 1 for v in by_cm.values())
        rels.append(
            {
                "t0": a,
                "n_pairs": len(joint),
                "col_k_values_offset0": sorted(ck_bits),
                "col_km1_values_offset0": sorted(cm_bits),
                "ck_determines_cm": ck_det_cm,
                "cm_determines_ck": cm_det_ck,
            }
        )
    return {
        "word": word,
        "k": k,
        "radius3": radius3,
        "n_strings": rec["n_strings"],
        "n_windows": rec["n_windows"],
        "relations": rels,
    }


def injected_relations_001(kmax: int = 8) -> dict:
    """001: two 0-phase streams u_n=r_{3n}, v_n=r_{3n+1}. Relations at k=4,8."""
    word = "001"
    table, names, idx, vmax = column_anfs(word, kmax)
    # Markov constraints on consecutive injected bits via sampling
    length = 3 * 6
    strings = iter_left_r(word, length, False)
    uv_pairs = set()
    uv_triples = set()
    for bits in strings:
        u0 = bits & 1
        v0 = (bits >> 1) & 1
        u1 = (bits >> 3) & 1
        v1 = (bits >> 4) & 1
        uv_pairs.add((u0, v0))
        uv_triples.add((u0, v0, u1, v1))
    r3s = iter_left_r(word, length, True)
    uv_pairs_r3 = set()
    uv_triples_r3 = set()
    for bits in r3s:
        u0 = bits & 1
        v0 = (bits >> 1) & 1
        u1 = (bits >> 3) & 1
        v1 = (bits >> 4) & 1
        uv_pairs_r3.add((u0, v0))
        uv_triples_r3.add((u0, v0, u1, v1))
    # depth-4 ANFs
    d4 = [{"phase": s, "anf": anf_str(table[s][4], names)} for s in range(3)]
    d8 = [{"phase": s, "anf": anf_str(table[s][8], names)} for s in range(3)] if kmax >= 8 else []
    d3 = [{"phase": s, "anf": anf_str(table[s][3], names)} for s in range(3)]
    return {
        "markov_uv_pairs": sorted(uv_pairs),
        "markov_uv_quads": sorted(uv_triples),
        "r3_uv_pairs": sorted(uv_pairs_r3),
        "r3_uv_quads": sorted(uv_triples_r3),
        "r3_strictly_narrower_pairs": uv_pairs_r3 < uv_pairs,
        "r3_strictly_narrower_quads": uv_triples_r3 < uv_triples,
        "col3": d3,
        "col4": d4,
        "col8": d8,
    }


def injected_relations_0111(kmax: int = 12) -> dict:
    word, table, idx = isolated_zero_anfs(3, kmax)
    names = [f"u{i}" for i in range(24)]
    cols = {}
    for k in (1, 2, 3, 4, 5, 6, 7, 8, 12):
        if k > kmax:
            continue
        cols[k] = [{"phase": s, "anf": anf_str(table[s][k], names)} for s in range(4)]
    # consecutive u free?
    length = 4 * 5
    mk = iter_left_r(word, length, False)
    r3 = iter_left_r(word, length, True)
    def pack_u(strings):
        s = set()
        for bits in strings:
            acc = 0
            for n in range(5):
                t = 4 * n
                if (bits >> t) & 1:
                    acc |= 1 << n
            s.add(acc)
        return s
    pu, pr = pack_u(mk), pack_u(r3)
    return {
        "columns": {str(k): cols[k] for k in cols},
        "markov_u_words": sorted(pu),
        "r3_u_words": sorted(pr),
        "r3_strictly_narrower": pr < pu,
        "u_all_free_markov": len(pu) == 32,
        "u_all_free_r3": len(pr) == 32,
    }


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_attack(quick: bool = False) -> dict:
    report: dict = {"words": {}, "cycles": {}, "germs": {}, "implications": {}}
    _self_check_inverse("001")
    _self_check_inverse("0111")
    words = ("001", "0111")
    kmax_mask = 8 if quick else 12
    kmax_germ = 6 if quick else 8
    w001 = 2 * 3 + 8  # 14
    w0111 = 2 * 4 + 8  # 16
    windows = {"001": w001, "0111": w0111}

    report["vacuum"] = {w: vacuum_implications(w) for w in words}
    # compact vacuum
    vac_slim = {}
    for w in words:
        v = report["vacuum"][w]
        vac_slim[w] = {
            "full_vacuum_r_next": [
                {"phase": r["phase"], "center": r["center"], "r_next": r["r_next"]}
                for r in v["full_vacuum"]
            ],
            "plus23_forced_r": [
                {
                    "phase": r["phase"],
                    "state": r["state"],
                    "r_next_forced": r["r_next_forced"],
                }
                for r in v["plus23_vacuum"]
                if r["r_next_forced"] is not None
            ],
        }
    report["vacuum_slim"] = vac_slim

    report["injected"] = {
        "001": injected_relations_001(kmax=8 if quick else 8),
        "0111": injected_relations_0111(kmax=12 if not quick else 8),
        "language_001": {
            "markov": injected_language("001", 3 if quick else 4, False),
            "r3": injected_language("001", 3 if quick else 4, True),
        },
        "language_0111": {
            "markov": injected_language("0111", 3 if quick else 4, False),
            "r3": injected_language("0111", 3 if quick else 4, True),
        },
    }

    for w in words:
        print(f"# masks {w}", flush=True)
        mk = unconditional_masks(w, kmax_mask, radius3=False)
        r3 = unconditional_masks(w, kmax_mask, radius3=True)
        report["words"][w] = {
            "markov_masks": mk,
            "r3_masks": r3,
            "r3_extra_forced0": {},
        }
        extra = {}
        for k in range(kmax_mask + 1):
            a = set(mk["by_k"][str(k)]["forced0"])
            b = set(r3["by_k"][str(k)]["forced0"])
            extra[str(k)] = sorted(b - a)
        report["words"][w]["r3_extra_forced0"] = extra
        report["words"][w]["two_col_k4"] = two_col_relations_at_depth(w, 4, True)
        report["words"][w]["two_col_k8"] = two_col_relations_at_depth(w, 8, True)
        print(f"# enum-shift {w}", flush=True)
        report["words"][w]["enum_shift_r3"] = enum_shift_relations(
            w, kmax=8 if quick else 12, radius3=True
        )
        report["words"][w]["enum_shift_markov"] = enum_shift_relations(
            w, kmax=8 if quick else 12, radius3=False
        )
        report["words"][w]["fib_u"] = fibonacci_u_check(w, 5 if not quick else 4)

    src = {"001": [2], "0111": [0, 2, 3]}  # known depth-4 zeros
    for w in words:
        ww = windows[w]
        for d in (4, 8):
            print(f"# impl {w} d={d}", flush=True)
            # unconditional restriction using known depth-4 zeros, from k=4
            report["implications"][f"{w}:k4:d{d}:r3"] = edge_cover_conditional(
                w, 4, d, ww, True, src[w]
            )
            report["implications"][f"{w}:k4:d{d}:markov"] = edge_cover_conditional(
                w, 4, d, ww, False, src[w]
            )
            # also from k=4 with NO extra restriction (pure identities at k+d)
            report["implications"][f"{w}:k4:d{d}:unrestricted_r3"] = edge_cover_conditional(
                w, 4, d, ww, True, []
            )

    for w in words:
        for d in (4, 8):
            report["cycles"][f"{w}:d{d}:markov"] = cycle_search(
                w, report["words"][w]["markov_masks"], d, k0=4, steps=2
            )
            report["cycles"][f"{w}:d{d}:r3"] = cycle_search(
                w, report["words"][w]["r3_masks"], d, k0=4, steps=2
            )

    for w in words:
        print(f"# germs {w}", flush=True)
        report["germs"][w] = {
            "R2_r3": l0_germ_transport(w, kmax_germ, R=2, radius3=True),
            "R3_r3": l0_germ_transport(w, kmax_germ, R=3, radius3=True),
            "R2_markov": l0_germ_transport(w, kmax_germ, R=2, radius3=False),
        }

    # Verdict helpers
    any_cycle = any(v.get("any_closed_h") for v in report["cycles"].values())
    any_germ_cycle = any(
        bool(g[key]["closed_candidates"])
        for g in report["germs"].values()
        for key in g
    )
    any_cover = any(
        v.get("covers_all_residues_common")
        for v in report["implications"].values()
        if isinstance(v, dict)
    )
    report["verdict"] = {
        "any_period_excluded": False,
        "closed_dh_cycle_unconditional": any_cycle,
        "closed_dh_cycle_l0_germ": any_germ_cycle,
        "restricted_impl_covers_all_T_residues": any_cover,
        "stop_reason": (
            "closed propagation rule"
            if (any_cycle or any_germ_cycle)
            else "only finite identities; no closed (d,h) rule with h<d"
        ),
    }
    return report


def slim_report(report: dict) -> dict:
    """Human-readable extract for the markdown note."""
    slim = {
        "verdict": report["verdict"],
        "vacuum_slim": report["vacuum_slim"],
        "injected": {
            "001_uv": {
                k: report["injected"]["001"][k]
                for k in (
                    "markov_uv_pairs",
                    "r3_uv_pairs",
                    "r3_strictly_narrower_pairs",
                    "col3",
                    "col4",
                    "col8",
                )
            },
            "0111_u": {
                "r3_strictly_narrower": report["injected"]["0111"]["r3_strictly_narrower"],
                "u_all_free_markov": report["injected"]["0111"]["u_all_free_markov"],
                "u_all_free_r3": report["injected"]["0111"]["u_all_free_r3"],
                "columns": {
                    k: report["injected"]["0111"]["columns"][k]
                    for k in report["injected"]["0111"]["columns"]
                    if k in ("1", "3", "4", "8")
                },
            },
            "language_001": report["injected"]["language_001"],
            "language_0111": report["injected"]["language_0111"],
        },
        "masks": {},
        "r3_extra_forced0": {},
        "two_col": {},
        "enum_shift": {},
        "implications": {},
        "cycles": report["cycles"],
        "germs": {},
    }
    for w, rec in report["words"].items():
        slim["masks"][w] = {
            "markov": {k: rec["markov_masks"]["by_k"][k] for k in rec["markov_masks"]["by_k"]},
            "r3": {k: rec["r3_masks"]["by_k"][k] for k in rec["r3_masks"]["by_k"]},
        }
        slim["r3_extra_forced0"][w] = rec["r3_extra_forced0"]
        slim["two_col"][w] = {"k4": rec["two_col_k4"], "k8": rec["two_col_k8"]}
        slim["enum_shift"][w] = {
            "r3": {
                "n_nonconst": rec["enum_shift_r3"]["n_nonconst"],
                "nonconst": rec["enum_shift_r3"]["nonconst"][:25],
            },
            "markov": {
                "n_nonconst": rec["enum_shift_markov"]["n_nonconst"],
                "nonconst": rec["enum_shift_markov"]["nonconst"][:25],
            },
            "fib_u": rec["fib_u"],
        }
    for key, rec in report["implications"].items():
        slim["implications"][key] = {
            "common_forced0_phases": rec.get("common_forced0_phases"),
            "union_forced0_phases": rec.get("union_forced0_phases"),
            "T_residues_if_common": rec.get("T_residues_if_common"),
            "T_residues_if_union": rec.get("T_residues_if_union"),
            "covers_all_residues_common": rec.get("covers_all_residues_common"),
            "src": rec.get("src_forced0_phases"),
            "k": rec.get("k"),
            "d": rec.get("d"),
            "by_t0": rec.get("by_t0"),
        }
    for w, g in report["germs"].items():
        slim["germs"][w] = {}
        for key, rec in g.items():
            slim["germs"][w][key] = {
                "n_germs": rec["n_germs"],
                "closed_candidates": rec["closed_candidates"],
                "stats": {
                    d: {
                        h: v
                        for h, v in rec["stats"][d].items()
                        if int(h) in (0, 1, 2, 3, 4, 8) or v["always_l0"] or v["always_forced0"]
                    }
                    for d in rec["stats"]
                },
            }
    return slim


def certify() -> dict:
    """Fast checks of the lemmas recorded in period_p_propagate.md."""
    _self_check_inverse("001")
    _self_check_inverse("0111")
    out: dict = {}
    m001 = unconditional_masks("001", 12, True)
    out["001_r3_forced0"] = {
        k: m001["by_k"][k]["forced0"] for k in m001["by_k"] if m001["by_k"][k]["forced0"]
    }
    assert out["001_r3_forced0"].get("4") == [2]
    assert all(
        m001["by_k"][str(k)]["forced0"] == []
        for k in range(5, 13)
    )
    m0111m = unconditional_masks("0111", 12, False)
    m0111r = unconditional_masks("0111", 12, True)
    out["0111_markov_forced0"] = {
        k: m0111m["by_k"][k]["forced0"]
        for k in m0111m["by_k"]
        if m0111m["by_k"][k]["forced0"]
    }
    assert m0111m["by_k"]["4"]["forced0"] == [0, 2, 3]
    assert m0111m["by_k"]["8"]["forced0"] == []
    assert m0111m["by_k"]["12"]["forced0"] == []
    assert m0111m["by_k"]["6"]["forced0"] == [2]
    assert m0111m["by_k"]["10"]["forced0"] == [2]
    assert m0111r["by_k"]["11"]["forced0"] == [3]
    assert m0111m["by_k"]["11"]["forced0"] == []
    fib = fibonacci_u_check("0111", 5)
    assert fib["r3_is_fibonacci"]
    assert fib["markov"]["all_free"]
    out["0111_r3_u_fibonacci"] = True
    cyc = cycle_search("001", m001, 4, k0=4, steps=2)
    assert not cyc["any_closed_h"]
    rec = edge_cover_conditional("001", 4, 4, 14, True, [2])
    assert rec["common_forced0_phases"] == []
    rec2 = edge_cover_conditional("0111", 4, 4, 16, True, [0, 2, 3])
    assert rec2["common_forced0_phases"] == []
    g = l0_germ_transport("0111", 6, R=2, radius3=True)
    assert g["closed_candidates"] == []
    out["no_closed_cycle"] = True
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--json-out", type=str, default="")
    parser.add_argument("--slim-out", type=str, default="")
    args = parser.parse_args()
    if args.certify:
        rec = certify()
        print("certify: all assertions passed")
        print(json.dumps(rec, indent=2))
        return
    report = run_attack(quick=args.quick)
    slim = slim_report(report)
    print("VERDICT", json.dumps(report["verdict"], indent=2))
    print("CYCLES")
    for k, v in report["cycles"].items():
        print(
            k,
            "closed_h",
            v["any_closed_h"],
            "residues",
            v["T_residues_killed_by_chain"],
            "all",
            v["all_onset_residues"],
            "chain",
            v["chain"],
        )
    print("GERM CANDIDATES")
    for w, g in report["germs"].items():
        for key, rec in g.items():
            print(w, key, "n_germs", rec["n_germs"], "cands", rec["closed_candidates"])
    print("IMPLICATIONS common forced0")
    for k, v in report["implications"].items():
        print(
            k,
            "common",
            v.get("common_forced0_phases"),
            "Tres",
            v.get("T_residues_if_common"),
            "all",
            v.get("covers_all_residues_common"),
        )
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2, default=str)
            f.write("\n")
    if args.slim_out:
        with open(args.slim_out, "w") as f:
            json.dump(slim, f, indent=2, default=str)
            f.write("\n")


if __name__ == "__main__":
    main()
