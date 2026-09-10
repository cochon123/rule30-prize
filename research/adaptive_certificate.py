#!/usr/bin/env python3
"""Data-dependent short-circuit certificates for Rule 30 center bits.

Does not overwrite strip_graph.py, strip_extend.py, or experiment.py.
Does not claim a prize result.

C(n) is the minimum number of internal a⊕(b∨c) gates in a short-circuit
certificate for c_n on the single-1 seed. Independently generated rows are
an oracle for the diagnostic ILP only. The executable evaluator receives
only n and the seed.

Run: python3 research/adaptive_certificate.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.setrecursionlimit(10000)

OUT_JSON = Path(__file__).with_name("adaptive_certificate.json")
NS = (32, 64, 128, 256)
KILL_FRAC = 0.1


# ---------------------------------------------------------------------------
# Packed Rule 30. Bit k of the integer at time t is spatial coordinate k-t.
# ---------------------------------------------------------------------------

def packed_rows(n: int) -> list[int]:
    """rows[t] is the packed light-cone of width 2t+1, t=0..n."""
    rows = [0] * (n + 1)
    row = 1
    for t in range(n + 1):
        rows[t] = row
        row = (row << 2) ^ ((row << 1) | row)
    return rows


def cell_value(rows: list[int], t: int, j: int) -> int:
    if t < 0:
        return 0
    k = j + t
    if k < 0:
        return 0
    return (rows[t] >> k) & 1


def is_free(t: int, j: int) -> bool:
    """Seed or vacuum: not an internal gate."""
    return t <= 0 or abs(j) > t


def light_cone_cells(n: int):
    """Internal cells that can feed x(n,0). Count is at most n²."""
    for t in range(1, n + 1):
        lo = max(-t, t - n)
        hi = min(t, n - t)
        for j in range(lo, hi + 1):
            yield t, j


def preds(t: int, j: int):
    return (t - 1, j - 1), (t - 1, j), (t - 1, j + 1)


def or_kind(rows: list[int], t: int, j: int) -> str:
    """How the OR at gate (t,j) can be certified, given oracle values."""
    _a, b, c = preds(t, j)
    bv = cell_value(rows, *b)
    cv = cell_value(rows, *c)
    if bv == 0 and cv == 0:
        return "both0"
    if bv == 1 and cv == 0:
        return "b"
    if bv == 0 and cv == 1:
        return "c"
    return "either"


def verify_rows(rows: list[int], n: int) -> dict:
    """Packed evolution vs the local rule, plus center bits vs a second run."""
    fail = 0
    checked = 0
    for t in range(1, n + 1):
        for j in range(-t, t + 1):
            a, b, c = preds(t, j)
            got = cell_value(rows, t, j)
            want = cell_value(rows, *a) ^ (cell_value(rows, *b) | cell_value(rows, *c))
            checked += 1
            if got != want:
                fail += 1
    row = 1
    center_fail = 0
    for t in range(n + 1):
        if ((row >> t) & 1) != cell_value(rows, t, 0):
            center_fail += 1
        row = (row << 2) ^ ((row << 1) | row)
    cone = sum(1 for _ in light_cone_cells(n))
    return {
        "update_checked": checked,
        "update_failures": fail,
        "center_failures": center_fail,
        "light_cone_internal": cone,
        "full_triangle_internal": n * n,
        "n2": n * n,
    }


# ---------------------------------------------------------------------------
# Forced AND-closure and matching extras: certified lower bound.
# ---------------------------------------------------------------------------

def required_preds(rows: list[int], t: int, j: int) -> list[tuple[int, int]]:
    """Predecessors that every certificate containing (t,j) must include."""
    a, b, c = preds(t, j)
    kind = or_kind(rows, t, j)
    out = [a]
    if kind == "both0":
        out.extend([b, c])
    elif kind == "b":
        out.append(b)
    elif kind == "c":
        out.append(c)
    return out


def optional_or_pair(rows: list[int], t: int, j: int):
    kind = or_kind(rows, t, j)
    if kind != "either":
        return None
    _a, b, c = preds(t, j)
    return b, c


def forced_closure(rows: list[int], roots) -> tuple[set, list]:
    """Internal cells forced by AND-constraints from roots.

    Returns (forced, list of (cell, b, c) 11-choice points inside forced
    whose witnesses are not themselves forced).
    """
    forced: set[tuple[int, int]] = set()
    stack = list(roots)
    while stack:
        t, j = stack.pop()
        if is_free(t, j) or (t, j) in forced:
            continue
        forced.add((t, j))
        for p in required_preds(rows, t, j):
            if not is_free(*p):
                stack.append(p)
    choices = []
    for t, j in forced:
        pair = optional_or_pair(rows, t, j)
        if pair is None:
            continue
        b, c = pair
        if is_free(*b) or is_free(*c):
            continue
        if b in forced or c in forced:
            continue
        choices.append(((t, j), b, c))
    return forced, choices


def matching_extra(choices) -> tuple[int, int]:
    """Lower bound on extra vertices needed to hit every 11-pair.

    Each 11-gate in the forced set needs at least one witness. Witnesses
    that are still free (vacuum/seed) cost 0. The remaining pairs form a
    graph (actually a collection of paths, since a pair is two spatially
    adjacent cells) and a matching is a certified extra.
    """
    edges = []
    for _v, b, c in choices:
        b_ok = not is_free(*b)
        c_ok = not is_free(*c)
        if b_ok and c_ok:
            edges.append((b, c))
        # If exactly one witness is internal, that vertex is forced into
        # every certificate; it is already counted in the matching as a
        # singleton extra. Those are handled by the caller via unique
        # optional preds... but optional_or_pair with one free witness
        # means the internal one is NOT forced (the free 1 already
        # certifies the OR). So no extra internal vertex is required.
    # Maximum matching on a disjoint union of paths (pairs on a grid of
    # cells). Greedy along time then position is optimal for a matching
    # lower bound if we take a maximal matching of vertex-disjoint edges.
    # The graph is bipartite by (t+j) parity: each pair is two adjacent
    # cells on one row. Kuhn matching is exact.
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    left = [u for u in adj if (u[0] + u[1]) % 2 == 0]
    mate_right = {}

    def dfs(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in mate_right or dfs(mate_right[v], seen):
                mate_right[v] = u
                return True
        return False

    for u in left:
        dfs(u, set())
    match_count = len(mate_right)
    used = set()
    greedy = 0
    for u, v in edges:
        if u in used or v in used:
            continue
        used.add(u)
        used.add(v)
        greedy += 1
    return match_count, greedy


def certified_lower_bound(rows: list[int], n: int) -> dict:
    forced, choices = forced_closure(rows, [(n, 0)])
    match, greedy = matching_extra(choices)
    # Every certificate contains `forced`. Each matched 11-pair requires
    # at least one extra internal vertex, and those extras are disjoint,
    # so they cannot share.
    lb = len(forced) + match
    pair_both_internal = 0
    for _v, b, c in choices:
        if not is_free(*b) and not is_free(*c):
            pair_both_internal += 1
    return {
        "forced": len(forced),
        "eleven_in_forced_with_internal_witness": len(choices),
        "eleven_both_witnesses_internal": pair_both_internal,
        "matching_extra": match,
        "greedy_matching_extra": greedy,
        "certified_lb": lb,
    }


# ---------------------------------------------------------------------------
# Exact C(n): branch on 11-witnesses with forced-closure bounding.
# ---------------------------------------------------------------------------

class ExactSolver:
    def __init__(self, rows: list[int], n: int, ub: int, t_limit: float):
        self.rows = rows
        self.n = n
        self.best = ub
        self.t_limit = t_limit
        self.t0 = time.perf_counter()
        self.nodes = 0
        self.timed_out = False
        self.optima_cert = None

    def expired(self) -> bool:
        if time.perf_counter() - self.t0 > self.t_limit:
            self.timed_out = True
            return True
        return False

    def propagate(self, needed: set) -> tuple[set, list] | None:
        """Close under unique predecessors. Return (selected, choice_points)
        or None if selected already exceeds best."""
        selected = set()
        stack = list(needed)
        while stack:
            t, j = stack.pop()
            if is_free(t, j) or (t, j) in selected:
                continue
            selected.add((t, j))
            if len(selected) >= self.best:
                return None
            for p in required_preds(self.rows, t, j):
                if not is_free(*p):
                    stack.append(p)
        choices = []
        for t, j in selected:
            pair = optional_or_pair(self.rows, t, j)
            if pair is None:
                continue
            b, c = pair
            if is_free(*b) or is_free(*c):
                continue
            if b in selected or c in selected:
                continue
            choices.append(((t, j), b, c))
        return selected, choices

    def search(self, needed: set) -> int | None:
        if self.expired():
            return None
        self.nodes += 1
        prop = self.propagate(needed)
        if prop is None:
            return None
        selected, choices = prop
        if not choices:
            self.best = len(selected)
            self.optima_cert = selected
            return self.best
        # Lower bound: selected + matching extras among remaining choices.
        match, _g = matching_extra(choices)
        if len(selected) + match >= self.best:
            return None
        # Branch on a choice whose two options look cheapest (smallest t
        # first = nearer the seed, fewer descendants).
        choices.sort(key=lambda item: (item[1][0] + item[2][0], item[0][0]))
        _v, b, c = choices[0]
        # Prefer the witness closer to the right edge (often a 1-run).
        opts = [b, c]
        opts.sort(key=lambda p: -p[1])
        ans = None
        for w in opts:
            got = self.search(needed | {w})
            if got is not None:
                ans = got
            if self.timed_out:
                break
        return ans


def exact_C(rows: list[int], n: int, ub: int, t_limit: float) -> dict:
    """ub must be the size of some valid circuit certificate (not edge lemmas).

    Search looks for a strictly smaller certificate. If the tree is exhausted,
    solver.best is the exact C(n). On timeout it remains a certified upper bound.
    """
    solver = ExactSolver(rows, n, ub, t_limit)
    solver.search({(n, 0)})
    return {
        "C_n": None if solver.timed_out else solver.best,
        "upper_after_search": solver.best,
        "nodes": solver.nodes,
        "timed_out": solver.timed_out,
        "seconds": round(time.perf_counter() - solver.t0, 4),
        "certificate_size_if_any": None if solver.optima_cert is None else len(solver.optima_cert),
    }


# ---------------------------------------------------------------------------
# Executable memoized short-circuit evaluators (only n and the seed).
# ---------------------------------------------------------------------------

def executable_eval(n: int, prefer: str) -> dict:
    """Short-circuit OR with memoization. No triangle oracle.

    prefer:
      left  — evaluate b then maybe c (standard lazy OR)
      right — evaluate c then maybe b
      rightedge — try the spatially righter input first
      leftedge  — try the spatially lefter input first
    """
    memo: dict[tuple[int, int], int] = {}
    gates = [0]

    def ev(t: int, j: int) -> int:
        if t <= 0:
            return 1 if (t == 0 and j == 0) else 0
        if abs(j) > t:
            return 0
        key = (t, j)
        if key in memo:
            return memo[key]
        gates[0] += 1
        a = ev(t - 1, j - 1)
        bpos = (t - 1, j)
        cpos = (t - 1, j + 1)
        if prefer == "left":
            order = (bpos, cpos)
        elif prefer == "right":
            order = (cpos, bpos)
        elif prefer == "rightedge":
            order = (cpos, bpos) if cpos[1] >= bpos[1] else (bpos, cpos)
        elif prefer == "leftedge":
            order = (bpos, cpos) if bpos[1] <= cpos[1] else (cpos, bpos)
        else:
            raise ValueError(prefer)
        first = ev(*order[0])
        if first == 1:
            val = a ^ 1
        else:
            second = ev(*order[1])
            val = a ^ (0 | second)
        memo[key] = val
        return val

    t0 = time.perf_counter()
    value = ev(n, 0)
    return {
        "prefer": prefer,
        "value": value,
        "gates": gates[0],
        "memo_internal": sum(1 for (t, _j) in memo if t >= 1),
        "seconds": round(time.perf_counter() - t0, 4),
    }


def executable_with_edge_lemmas(n: int) -> dict:
    """Same as left-first, but x(t,±t)=1 is used as a proved base case.

    Still uniform in n: the two-edge identities are inductive from the seed.
    Charged gates are only the non-edge internals actually evaluated.
    """
    memo: dict[tuple[int, int], int] = {}
    gates = [0]

    def ev(t: int, j: int) -> int:
        if t <= 0:
            return 1 if (t == 0 and j == 0) else 0
        if abs(j) > t:
            return 0
        if j == t or j == -t:
            return 1
        key = (t, j)
        if key in memo:
            return memo[key]
        gates[0] += 1
        a = ev(t - 1, j - 1)
        b = ev(t - 1, j)
        if b == 1:
            val = a ^ 1
        else:
            c = ev(t - 1, j + 1)
            val = a ^ (0 | c)
        memo[key] = val
        return val

    t0 = time.perf_counter()
    value = ev(n, 0)
    return {
        "prefer": "left_plus_edge_lemmas",
        "value": value,
        "gates": gates[0],
        "memo_internal": sum(1 for (t, _j) in memo if t >= 1),
        "seconds": round(time.perf_counter() - t0, 4),
    }


# ---------------------------------------------------------------------------
# Oracle-guided certificate (uncharged triangle): one concrete upper bound
# that MAY look at every cell. This is NOT an algorithm for c_n.
# ---------------------------------------------------------------------------

def oracle_greedy_certificate(rows: list[int], n: int, prefer: str) -> dict:
    """Build one certificate using oracle values to pick 11-witnesses.

    This is an upper bound on C(n). It is not executable from n and the seed
    alone: the 11-policy may inspect values (and, for 'overlap', the forced
    cones of both witnesses) that a uniform evaluator is not charged for.
    """
    t0 = time.perf_counter()
    selected: set[tuple[int, int]] = set()
    stack = [(n, 0)]
    oracle_lookups = 0
    while stack:
        t, j = stack.pop()
        if is_free(t, j) or (t, j) in selected:
            continue
        selected.add((t, j))
        a, b, c = preds(t, j)
        stack.append(a)
        kind = or_kind(rows, t, j)
        oracle_lookups += 1
        if kind == "both0":
            stack.extend([b, c])
        elif kind == "b":
            stack.append(b)
        elif kind == "c":
            stack.append(c)
        else:
            if is_free(*b) or b in selected:
                continue
            if is_free(*c) or c in selected:
                continue
            if prefer == "left":
                stack.append(b)
            elif prefer == "right":
                stack.append(c)
            else:
                fb, _ch = forced_closure(rows, [b])
                fc, _ch = forced_closure(rows, [c])
                extra_b = len(fb - selected)
                extra_c = len(fc - selected)
                stack.append(b if extra_b <= extra_c else c)
    return {
        "prefer": prefer,
        "gates": len(selected),
        "value": cell_value(rows, n, 0),
        "seconds": round(time.perf_counter() - t0, 4),
        "oracle_cells_touched": oracle_lookups,
    }


def cone_kind_histogram(rows: list[int], n: int) -> dict:
    hist = defaultdict(int)
    for t, j in light_cone_cells(n):
        hist[or_kind(rows, t, j)] += 1
    return dict(hist)


def run_n(n: int, exact_limit: float) -> dict:
    t0 = time.perf_counter()
    rows = packed_rows(n)
    ver = verify_rows(rows, n)
    hist = cone_kind_histogram(rows, n)
    lb = certified_lower_bound(rows, n)
    circuit_execs = [
        executable_eval(n, "left"),
        executable_eval(n, "right"),
        executable_eval(n, "rightedge"),
        executable_eval(n, "leftedge"),
    ]
    lemma_exec = executable_with_edge_lemmas(n)
    # All executable values must equal the packed center bit.
    center = cell_value(rows, n, 0)
    for e in circuit_execs + [lemma_exec]:
        if e["value"] != center:
            raise RuntimeError(f"evaluator {e['prefer']} disagrees at n={n}")
    exec_best = min(circuit_execs, key=lambda e: e["gates"])
    oracle_ubs = [
        oracle_greedy_certificate(rows, n, "left"),
        oracle_greedy_certificate(rows, n, "right"),
    ]
    if n <= 64:
        oracle_ubs.append(oracle_greedy_certificate(rows, n, "overlap"))
    for o in oracle_ubs:
        if o["value"] != center:
            raise RuntimeError(f"oracle greedy {o['prefer']} disagrees at n={n}")
    oracle_best = min(oracle_ubs, key=lambda o: o["gates"])
    # Circuit C(n) cannot use the edge-lemma evaluator as a certificate:
    # that machine skips x(t,±t) without paying those gates.
    ub = min(exec_best["gates"], oracle_best["gates"])
    exact = exact_C(rows, n, ub, exact_limit)
    if exact["C_n"] is not None:
        ub = exact["C_n"]
    else:
        ub = min(ub, exact["upper_after_search"])
    n2 = n * n
    cone = ver["light_cone_internal"]
    C_star = exact["C_n"]
    return {
        "n": n,
        "n2": n2,
        "light_cone_internal": cone,
        "kill_threshold": KILL_FRAC * n2,
        "center": center,
        "verify": ver,
        "or_kind_in_cone": hist,
        "lower": lb,
        "C_n_exact": C_star,
        "C_n_certified_lb": lb["certified_lb"],
        "C_n_ub": ub,
        "lb_over_n2": lb["certified_lb"] / n2,
        "ub_over_n2": ub / n2,
        "lb_over_cone": lb["certified_lb"] / cone,
        "ub_over_cone": ub / cone,
        "kill_lb_exceeds_0_1_n2": lb["certified_lb"] > KILL_FRAC * n2,
        "executable": circuit_execs,
        "executable_edge_lemmas": lemma_exec,
        "executable_best_gates": exec_best["gates"],
        "executable_best_prefer": exec_best["prefer"],
        "oracle_greedy": oracle_ubs,
        "oracle_best_gates": oracle_best["gates"],
        "gap_oracle_vs_executable": exec_best["gates"] - oracle_best["gates"],
        "gap_lb_vs_oracle": oracle_best["gates"] - lb["certified_lb"],
        "exact_search": exact,
        "seconds": round(time.perf_counter() - t0, 4),
    }


def main():
    t_all = time.perf_counter()
    # Warm-up exactness check at tiny n against brute closure search.
    tiny = []
    for n in (4, 8, 12, 16):
        rows = packed_rows(n)
        center = cell_value(rows, n, 0)
        ev = executable_eval(n, "left")
        og = oracle_greedy_certificate(rows, n, "overlap")
        lb = certified_lower_bound(rows, n)
        ex = exact_C(rows, n, min(ev["gates"], og["gates"]) + 1, t_limit=5.0)
        if ev["value"] != center or og["value"] != center:
            raise RuntimeError("tiny n mismatch")
        if ex["C_n"] is None:
            raise RuntimeError(f"exact timed out at n={n}")
        circuit_ub = min(ev["gates"], og["gates"])
        if not (lb["certified_lb"] <= ex["C_n"] <= circuit_ub):
            raise RuntimeError(
                f"bound failure n={n}: lb={lb['certified_lb']} "
                f"C={ex['C_n']} ub={circuit_ub}"
            )
        tiny.append(
            {
                "n": n,
                "C_n": ex["C_n"],
                "lb": lb["certified_lb"],
                "oracle_overlap": og["gates"],
                "executable_left": ev["gates"],
                "n2": n * n,
            }
        )

    results = []
    # n=32,64 get a longer exact budget; 128/256 only if the gap is tiny.
    budgets = {32: 20.0, 64: 25.0, 128: 30.0, 256: 45.0}
    for n in NS:
        results.append(run_n(n, exact_limit=budgets[n]))

    both_kill = all(
        r["kill_lb_exceeds_0_1_n2"] for r in results if r["n"] in (128, 256)
    )
    # Second kill: apparent oracle savings that an executable evaluator
    # does not realize, or any "subquadratic" look that still needs the
    # uncharged triangle to pick witnesses.
    oracle_only_savings = False
    for r in results:
        if r["n"] < 128:
            continue
        n2 = r["n2"]
        if r["oracle_best_gates"] <= 0.1 * n2 < r["executable_best_gates"]:
            oracle_only_savings = True
        if r["gap_oracle_vs_executable"] > 0.05 * n2:
            oracle_only_savings = True

    exec_below_half_n2 = all(
        r["executable_best_gates"] < 0.5 * r["n2"] for r in results if r["n"] >= 128
    )
    exec_below_half_cone = all(
        r["executable_best_gates"] < 0.5 * r["light_cone_internal"]
        for r in results if r["n"] >= 128
    )

    dump = {
        "model": {
            "gate": "one internal gate per evolved cell a XOR (b OR c)",
            "free": "seed t=0 and vacuum |j|>t",
            "XOR_always_needs_a": True,
            "OR_one_1_suffices": True,
            "OR_0_needs_both": True,
            "sharing": "each selected gate charged once",
            "C_n": "min selected internal gates for a certificate of c_n",
        },
        "kill_criterion": {
            "retire_if_lb_exceeds_0_1_n2_at_128_and_256": True,
            "retire_if_savings_need_uncharged_oracle": True,
            "finite_cutoff_not_a_complexity_lower_bound": True,
        },
        "tiny_exact_checks": tiny,
        "results": results,
        "both_n128_n256_lb_exceed_threshold": both_kill,
        "oracle_only_savings_flag": oracle_only_savings,
        "executable_below_half_n2": exec_below_half_n2,
        "executable_below_half_cone": exec_below_half_cone,
        "retired": both_kill or oracle_only_savings,
        "prize_claim": False,
        "total_seconds": round(time.perf_counter() - t_all, 4),
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    print(json.dumps(dump, indent=2))
    return dump


if __name__ == "__main__":
    main()
