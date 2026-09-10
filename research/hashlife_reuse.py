#!/usr/bin/env python3
"""One-dimensional Hashlife-style evaluator for Rule 30 (prize problem 3).

Interned binary trees of spatial words, leaf width eight, overlapping
decomposition of the centre, empty cache, blocks built from the single-cell
seed. Not a prize claim. Does not contact anyone. Does not modify
experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/hashlife_reuse.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

OUT_JSON = Path(__file__).with_name("hashlife_reuse.json")
LEAF = 8
# 2^15 was attempted: after 40+ minutes the process was in disk sleep at
# ~1.5 GiB RSS and produced no c_{32768} line. The freeze is kept; that
# last doubling is recorded as incomplete rather than rerun.
TARGETS = tuple(2 ** k for k in range(10, 15))
TARGET_INCOMPLETE = 2 ** 15
VERIFY_FULL_RESULT_THROUGH = 2 ** 8
EXPERIMENT_CHECK_THROUGH = 2 ** 12
KILL_RATIO = 3.8

# ---------------------------------------------------------------------------
# Frozen unit-cost model (fixed before any TARGETS measurement).
# ---------------------------------------------------------------------------
# Every intern table probe, every newly constructed interned node, every
# result-cache probe, every cache fill, and every Rule-30 update of one
# 8-cell leaf by one time step costs 1. A key comparison is the intern
# probe itself and is not charged a second time. Bit extraction after the
# jump is uncharged (O(log n) child follows).
#
# W(n) = intern_lookups + node_constructions + cache_lookups
#        + cache_fills + leaf_updates
COST_INTERN_LOOKUP = 1
COST_NODE_CONSTRUCTION = 1
COST_CACHE_LOOKUP = 1
COST_CACHE_FILL = 1
COST_LEAF_UPDATE = 1


class Node:
    __slots__ = (
        "id", "level", "width", "left", "right", "bits",
        "is_zero", "popcount", "l1", "r1",
    )

    def __init__(self, nid, level, width, left, right, bits,
                 is_zero, popcount, l1, r1):
        self.id = nid
        self.level = level
        self.width = width
        self.left = left
        self.right = right
        self.bits = bits
        self.is_zero = is_zero
        self.popcount = popcount
        self.l1 = l1
        self.r1 = r1


def packed_window_step(row: int, width: int | None = None) -> int:
    """One radius-1 step; bit 0 is leftmost. Vacuum enters from both sides."""
    if width is not None:
        row &= (1 << width) - 1
    out = (row << 1) ^ (row | (row >> 1))
    if width is not None:
        out &= (1 << width) - 1
    return out


def independent_center_bit(n: int) -> int:
    """Packed light-cone engine, independent of the Hashlife intern tables."""
    row = 1
    for _ in range(n):
        row = (row << 2) ^ ((row << 1) | row)
    return (row >> n) & 1


def independent_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def local_step_bits(bits: int, width: int) -> int:
    out = 0
    for j in range(width):
        a = (bits >> (j - 1)) & 1 if j >= 1 else 0
        b = (bits >> j) & 1
        c = (bits >> (j + 1)) & 1 if j + 1 < width else 0
        out |= (a ^ (b | c)) << j
    return out


def naive_centre_word(row: int, width: int, steps: int) -> int:
    cur = row
    for _ in range(steps):
        cur = packed_window_step(cur, width)
    return (cur >> steps) & ((1 << (width - 2 * steps)) - 1)


def classify(node: Node, t: int, j0: int) -> str:
    """vacuum / edge / central from the node's support at time t.

    Vacuum: all zeros. Edge: every 1 sits on a light-cone boundary cell
    x(t, ±t), which is identically 1 for this seed. Central: any 1 strictly
    inside the cone, including the t=0 seed.
    """
    if node.is_zero:
        return "vacuum"
    if t == 0:
        return "central"
    lo = j0 + node.l1
    hi = j0 + node.r1
    if lo == hi and abs(lo) == t:
        return "edge"
    if lo == -t and hi == t and node.popcount == 2:
        return "edge"
    return "central"


def charged_work(s: dict) -> int:
    return (
        COST_INTERN_LOOKUP * s["intern_lookups"]
        + COST_NODE_CONSTRUCTION * s["node_constructions"]
        + COST_CACHE_LOOKUP * s["cache_lookups"]
        + COST_CACHE_FILL * s["cache_fills"]
        + COST_LEAF_UPDATE * s["leaf_updates"]
    )


class Engine:
    """Hashlife from an empty intern table and an empty result cache."""

    def __init__(self):
        self.next_id = 0
        self.leaf_table: dict[int, Node] = {}
        self.pair_table: dict[tuple[int, int], Node] = {}
        self.result_cache: dict[int, Node] = {}
        self.intern_lookups = 0
        self.intern_hits = 0
        self.node_constructions = 0
        self.comparisons = 0
        self.cache_lookups = 0
        self.cache_hits = 0
        self.cache_fills = 0
        self.leaf_updates = 0
        self.by_class = {
            cls: {
                "intern_lookups": 0,
                "intern_hits": 0,
                "node_constructions": 0,
                "cache_lookups": 0,
                "cache_hits": 0,
                "cache_fills": 0,
                "evo_requests": 0,
                "evo_ids": set(),
            }
            for cls in ("vacuum", "edge", "central")
        }
        self.level_stats = defaultdict(lambda: {
            "intern_lookups": 0,
            "intern_hits": 0,
            "node_constructions": 0,
            "cache_lookups": 0,
            "cache_hits": 0,
            "cache_fills": 0,
            "evo_requests": 0,
            "evo_ids": set(),
            "leaf_updates": 0,
            "by_class": {
                cls: {"requests": 0, "hits": 0, "fills": 0, "ids": set()}
                for cls in ("vacuum", "edge", "central")
            },
        })

    def _new_leaf(self, bits: int) -> Node:
        bits &= 255
        width = LEAF
        pop = bits.bit_count()
        if pop == 0:
            l1, r1 = width, -1
        else:
            l1 = (bits & -bits).bit_length() - 1
            r1 = bits.bit_length() - 1
        node = Node(
            self.next_id, 0, width, None, None, bits,
            pop == 0, pop, l1, r1,
        )
        self.next_id += 1
        return node

    def _new_pair(self, left: Node, right: Node) -> Node:
        width = left.width + right.width
        pop = left.popcount + right.popcount
        is_zero = pop == 0
        if left.popcount:
            l1 = left.l1
        else:
            l1 = left.width + right.l1
        if right.popcount:
            r1 = left.width + right.r1
        else:
            r1 = left.r1
        node = Node(
            self.next_id, left.level + 1, width, left, right, 0,
            is_zero, pop, l1, r1,
        )
        self.next_id += 1
        return node

    def intern_leaf(self, bits: int, t: int, j0: int) -> Node:
        bits &= 255
        self.intern_lookups += 1
        self.comparisons += 1
        st = self.level_stats[0]
        st["intern_lookups"] += 1
        node = self.leaf_table.get(bits)
        if node is None:
            node = self._new_leaf(bits)
            self.leaf_table[bits] = node
            self.node_constructions += 1
            st["node_constructions"] += 1
            cls = classify(node, t, j0)
            self.by_class[cls]["node_constructions"] += 1
            self.by_class[cls]["intern_lookups"] += 1
            return node
        cls = classify(node, t, j0)
        self.intern_hits += 1
        st["intern_hits"] += 1
        self.by_class[cls]["intern_lookups"] += 1
        self.by_class[cls]["intern_hits"] += 1
        return node

    def intern_pair(self, left: Node, right: Node, t: int, j0: int) -> Node:
        key = (left.id, right.id)
        level = left.level + 1
        self.intern_lookups += 1
        self.comparisons += 1
        st = self.level_stats[level]
        st["intern_lookups"] += 1
        node = self.pair_table.get(key)
        if node is None:
            node = self._new_pair(left, right)
            self.pair_table[key] = node
            self.node_constructions += 1
            st["node_constructions"] += 1
            cls = classify(node, t, j0)
            self.by_class[cls]["node_constructions"] += 1
            self.by_class[cls]["intern_lookups"] += 1
            return node
        cls = classify(node, t, j0)
        self.intern_hits += 1
        st["intern_hits"] += 1
        self.by_class[cls]["intern_lookups"] += 1
        self.by_class[cls]["intern_hits"] += 1
        return node

    def make_vacuum(self, level: int, t: int, j0: int) -> Node:
        if level == 0:
            return self.intern_leaf(0, t, j0)
        half = LEAF << (level - 1)
        z_left = self.make_vacuum(level - 1, t, j0)
        z_right = self.make_vacuum(level - 1, t, j0 + half)
        return self.intern_pair(z_left, z_right, t, j0)

    def plant(self, level: int, t: int, j0: int, seed_j: int = 0) -> Node:
        width = LEAF << level
        if seed_j < j0 or seed_j >= j0 + width:
            return self.make_vacuum(level, t, j0)
        if level == 0:
            return self.intern_leaf(1 << (seed_j - j0), t, j0)
        half = width >> 1
        left = self.plant(level - 1, t, j0, seed_j)
        right = self.plant(level - 1, t, j0 + half, seed_j)
        return self.intern_pair(left, right, t, j0)

    def result(self, node: Node, t: int, j0: int) -> Node:
        """Centre half of `node` after width/4 steps, interned at the next level down."""
        cls = classify(node, t, j0)
        level = node.level
        st = self.level_stats[level]
        st["evo_requests"] += 1
        st["evo_ids"].add(node.id)
        bc = st["by_class"][cls]
        bc["requests"] += 1
        bc["ids"].add(node.id)
        self.by_class[cls]["evo_requests"] += 1
        self.by_class[cls]["evo_ids"].add(node.id)

        self.cache_lookups += 1
        st["cache_lookups"] += 1
        self.by_class[cls]["cache_lookups"] += 1
        cached = self.result_cache.get(node.id)
        if cached is not None:
            self.cache_hits += 1
            st["cache_hits"] += 1
            bc["hits"] += 1
            self.by_class[cls]["cache_hits"] += 1
            return cached

        width = node.width
        dt = width >> 2
        if level == 1:
            row = node.left.bits | (node.right.bits << LEAF)
            cur = row
            for _ in range(dt):
                cur = packed_window_step(cur, 16)
                self.leaf_updates += 2
                st["leaf_updates"] += 2
            centre = (cur >> dt) & 255
            out = self.intern_leaf(centre, t + dt, j0 + dt)
        elif level >= 2:
            a = node.left.left
            b = node.left.right
            c = node.right.left
            d = node.right.right
            w = width
            # Overlapping children: left, middle, right at time t.
            left = node.left
            mid = self.intern_pair(b, c, t, j0 + (w >> 2))
            right = node.right
            dt1 = w >> 3
            l1 = self.result(left, t, j0)
            m1 = self.result(mid, t, j0 + (w >> 2))
            r1 = self.result(right, t, j0 + (w >> 1))
            t2 = t + dt1
            l2n = self.intern_pair(l1, m1, t2, j0 + dt1)
            r2n = self.intern_pair(m1, r1, t2, j0 + 3 * dt1)
            l2 = self.result(l2n, t2, j0 + dt1)
            r2 = self.result(r2n, t2, j0 + 3 * dt1)
            out = self.intern_pair(l2, r2, t + dt, j0 + (w >> 2))
        else:
            raise RuntimeError("result() is not defined on a leaf")

        self.result_cache[node.id] = out
        self.cache_fills += 1
        st["cache_fills"] += 1
        bc["fills"] += 1
        self.by_class[cls]["cache_fills"] += 1
        return out

    def bits_of(self, node: Node) -> int:
        if node.level == 0:
            return node.bits
        return self.bits_of(node.left) | (self.bits_of(node.right) << node.left.width)

    def getbit(self, node: Node, index: int) -> int:
        while node.level:
            half = node.width >> 1
            if index < half:
                node = node.left
            else:
                node = node.right
                index -= half
        return (node.bits >> index) & 1

    def snapshot(self) -> dict:
        by_class = {}
        for cls, d in self.by_class.items():
            by_class[cls] = {
                "intern_lookups": d["intern_lookups"],
                "intern_hits": d["intern_hits"],
                "node_constructions": d["node_constructions"],
                "cache_lookups": d["cache_lookups"],
                "cache_hits": d["cache_hits"],
                "cache_fills": d["cache_fills"],
                "evo_requests": d["evo_requests"],
                "evo_distinct": len(d["evo_ids"]),
            }
        levels = []
        for level in sorted(self.level_stats):
            st = self.level_stats[level]
            entry = {
                "level": level,
                "width": LEAF << level,
                "dt": (LEAF << level) >> 2 if level >= 1 else 0,
                "intern_lookups": st["intern_lookups"],
                "intern_hits": st["intern_hits"],
                "node_constructions": st["node_constructions"],
                "cache_lookups": st["cache_lookups"],
                "cache_hits": st["cache_hits"],
                "cache_fills": st["cache_fills"],
                "evo_requests": st["evo_requests"],
                "evo_distinct": len(st["evo_ids"]),
                "leaf_updates": st["leaf_updates"],
                "by_class": {
                    cls: {
                        "requests": bc["requests"],
                        "hits": bc["hits"],
                        "fills": bc["fills"],
                        "distinct": len(bc["ids"]),
                    }
                    for cls, bc in st["by_class"].items()
                },
            }
            levels.append(entry)
        counts = {
            "intern_lookups": self.intern_lookups,
            "intern_hits": self.intern_hits,
            "node_constructions": self.node_constructions,
            "comparisons": self.comparisons,
            "cache_lookups": self.cache_lookups,
            "cache_hits": self.cache_hits,
            "cache_fills": self.cache_fills,
            "leaf_updates": self.leaf_updates,
            "interned_leaves": len(self.leaf_table),
            "interned_pairs": len(self.pair_table),
            "cached_results": len(self.result_cache),
        }
        return {
            "counts": counts,
            "W": charged_work(counts),
            "by_class": by_class,
            "levels": levels,
        }


def compute_cn(n: int) -> tuple[int, dict, Engine, Node]:
    """Restart from empty tables and return c_n plus charged statistics."""
    if n < 1 or (n & (n - 1)):
        raise ValueError("n must be a positive power of two")
    width = 4 * n
    level = (width // LEAF).bit_length() - 1
    if LEAF << level != width:
        raise RuntimeError(f"width {width} is not 8*2^L")
    eng = Engine()
    j0 = -2 * n
    root = eng.plant(level, 0, j0, 0)
    evolved = eng.result(root, 0, j0)
    bit = eng.getbit(evolved, n)
    return bit, eng.snapshot(), eng, evolved


def self_check() -> dict:
    failures = []
    # Packed window step matches the local rule on 8- and 16-cell words.
    for width in (8, 16):
        for mask in range(1 << min(width, 12)):
            packed = packed_window_step(mask, width)
            local = local_step_bits(mask, width)
            if packed != local:
                failures.append(f"window step width={width} mask={mask}")
                break
        else:
            continue
        break
    for mask in range(1 << 16):
        if packed_window_step(mask, 16) != local_step_bits(mask, 16):
            failures.append(f"16-cell step mask={mask}")
            break

    # Independent packed engine matches experiment.py on a prefix.
    exp = experiment_center_bits(257)
    ind = independent_center_bits(257)
    if exp != ind:
        failures.append("independent packed bits != experiment.center_bits")
    if list(ind[:20]) != [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]:
        failures.append("independent prefix != known c_0..c_19")

    full_result_checked = []
    bit_checked = []
    # n=2 has initial width 8, a single leaf; result() starts at level 1.
    for n in (4, 8, 16, 32, 64, 128, 256):
        bit, snap, _eng, evolved = compute_cn(n)
        want = independent_center_bit(n)
        if bit != want:
            failures.append(f"c_{n} hashlife={bit} packed={want}")
        if n <= EXPERIMENT_CHECK_THROUGH:
            exp_bit = experiment_center_bits(n + 1)[n]
            if bit != exp_bit:
                failures.append(f"c_{n} hashlife={bit} experiment={exp_bit}")
        bit_checked.append({"n": n, "c_n": bit, "W": snap["W"]})
        if n <= VERIFY_FULL_RESULT_THROUGH:
            width = 4 * n
            seed_row = 1 << (width >> 1)
            naive = naive_centre_word(seed_row, width, n)
            got = _eng.bits_of(evolved)
            if got != naive:
                failures.append(
                    f"full result n={n} hashlife={got:x} naive={naive:x}"
                )
            full_result_checked.append(n)

    return {
        "failures": failures,
        "window_step_checked": True,
        "experiment_prefix": 257,
        "bit_checked": bit_checked,
        "full_result_checked_n": full_result_checked,
        "ok": not failures,
    }


def class_report(by_class: dict) -> dict:
    vac = by_class["vacuum"]
    edge = by_class["edge"]
    cen = by_class["central"]
    cache_hits_ve = vac["cache_hits"] + edge["cache_hits"]
    cache_hits_c = cen["cache_hits"]
    intern_hits_ve = vac["intern_hits"] + edge["intern_hits"]
    intern_hits_c = cen["intern_hits"]
    evo_c = cen["evo_requests"]
    dist_c = max(1, cen["evo_distinct"])
    central_evo_reuse = evo_c / dist_c
    evo_savings_central = cache_hits_c
    evo_savings_vacuum_edge = cache_hits_ve
    intern_savings_central = intern_hits_c
    intern_savings_vacuum_edge = intern_hits_ve
    total_savings = (
        intern_hits_c + intern_hits_ve + cache_hits_c + cache_hits_ve
    )
    central_savings = intern_hits_c + cache_hits_c
    central_share = central_savings / total_savings if total_savings else 0.0
    # Confined to vacuum/edge iff those classes supply at least half of all
    # intern-hits plus cache-hits. Central dominates otherwise.
    savings_confined_to_vacuum_or_edge = central_share <= 0.5
    central_reuse_dominates = not savings_confined_to_vacuum_or_edge
    return {
        "cache_hits_central": cache_hits_c,
        "cache_hits_vacuum": vac["cache_hits"],
        "cache_hits_edge": edge["cache_hits"],
        "intern_hits_central": intern_hits_c,
        "intern_hits_vacuum": vac["intern_hits"],
        "intern_hits_edge": edge["intern_hits"],
        "evo_requests_central": evo_c,
        "evo_distinct_central": cen["evo_distinct"],
        "central_evo_reuse_ratio": central_evo_reuse,
        "evo_requests_vacuum": vac["evo_requests"],
        "evo_distinct_vacuum": vac["evo_distinct"],
        "evo_requests_edge": edge["evo_requests"],
        "evo_distinct_edge": edge["evo_distinct"],
        "central_savings_share": central_share,
        "central_cache_dominates": cache_hits_c > cache_hits_ve,
        "central_reuse_dominates": central_reuse_dominates,
        "savings_confined_to_vacuum_or_edge": savings_confined_to_vacuum_or_edge,
        "evo_savings_central": evo_savings_central,
        "evo_savings_vacuum_edge": evo_savings_vacuum_edge,
        "intern_savings_central": intern_savings_central,
        "intern_savings_vacuum_edge": intern_savings_vacuum_edge,
    }


def main() -> None:
    t0 = time.perf_counter()
    check = self_check()
    if not check["ok"]:
        raise SystemExit("self-check failed: " + "; ".join(check["failures"]))

    results = []
    for n in TARGETS:
        t1 = time.perf_counter()
        bit, snap, _eng, _evolved = compute_cn(n)
        packed = independent_center_bit(n)
        exp_bit = None
        if n <= EXPERIMENT_CHECK_THROUGH:
            exp_bit = int(experiment_center_bits(n + 1)[n])
            if bit != exp_bit:
                raise SystemExit(f"c_{n} mismatch experiment")
        if bit != packed:
            raise SystemExit(f"c_{n} mismatch independent packed generator")
        reuse = class_report(snap["by_class"])
        rec = {
            "n": n,
            "c_n": bit,
            "W": snap["W"],
            "n2": n * n,
            "W_over_n2": snap["W"] / (n * n),
            "seconds": time.perf_counter() - t1,
            "verify": {
                "independent_packed": packed,
                "experiment_center_bits": exp_bit,
                "match": True,
            },
            "counts": snap["counts"],
            "by_class": snap["by_class"],
            "reuse": reuse,
            "levels": snap["levels"],
        }
        results.append(rec)
        print(
            f"n={n:6d} c_n={bit} W={snap['W']:10d} "
            f"leaf_upd={snap['counts']['leaf_updates']:8d} "
            f"cache_fill={snap['counts']['cache_fills']:8d} "
            f"central_hits={reuse['cache_hits_central']:8d} "
            f"vac_hits={reuse['cache_hits_vacuum']:8d} "
            f"edge_hits={reuse['cache_hits_edge']:6d} "
            f"t={rec['seconds']:.3f}s",
            flush=True,
        )

    ratios = []
    for a, b in zip(results, results[1:]):
        ratios.append({
            "from": a["n"],
            "to": b["n"],
            "W_ratio": b["W"] / a["W"] if a["W"] else None,
        })
    r14 = next(r for r in ratios if r["from"] == 2 ** 13 and r["to"] == 2 ** 14)
    r15 = next((r for r in ratios if r["from"] == 2 ** 14 and r["to"] == 2 ** 15), None)
    ratio_kill = bool(
        r15 is not None
        and r14["W_ratio"] >= KILL_RATIO
        and r15["W_ratio"] >= KILL_RATIO
    )
    last = results[-1]["reuse"]
    confined = all(r["reuse"]["savings_confined_to_vacuum_or_edge"] for r in results)
    confined_last_two = all(
        r["reuse"]["savings_confined_to_vacuum_or_edge"]
        for r in results if r["n"] in (2 ** 14, 2 ** 15)
    )
    incomplete_last = r15 is None
    # No closed recurrence bounding distinct blocks, and W remains superlinear
    # on every completed doubling. That fails the continuation requirement
    # even when the numerical 3.8-and-confined conjunction is not met.
    no_recurrence = True
    kill_work_and_confined = bool(ratio_kill and confined_last_two)
    precomputed_dictionary = False

    payload = {
        "model": {
            "rule": "x(t+1,j) = x(t,j-1) XOR (x(t,j) OR x(t,j+1))",
            "seed": "x(0,0)=1, else 0",
            "leaf_width": LEAF,
            "children": (
                "Stored children are adjacent halves. Evolution uses the "
                "overlapping triple (left, middle, right) so the next-level "
                "centre of width W/2 after W/4 steps is determined."
            ),
            "result": "centre W/2 cells after W/4 steps, cached on the interned node",
            "cache": "empty at the start of each n; no precomputed spacetime dictionary",
            "construction": "from the single-cell seed only",
            "padding": "initial word width 4n so one result() jump is exactly n steps",
        },
        "cost_model": {
            "intern_lookup": COST_INTERN_LOOKUP,
            "node_construction": COST_NODE_CONSTRUCTION,
            "cache_lookup": COST_CACHE_LOOKUP,
            "cache_fill": COST_CACHE_FILL,
            "leaf_update_8_cells_1_step": COST_LEAF_UPDATE,
            "comparisons": (
                "one key comparison per intern lookup, included in intern_lookup, "
                "reported separately and not added again"
            ),
            "W": (
                "intern_lookups + node_constructions + cache_lookups "
                "+ cache_fills + leaf_updates"
            ),
            "frozen_before_measurement": True,
        },
        "kill_criterion": {
            "ratio_threshold": KILL_RATIO,
            "retire_if_both_final_doublings_at_least_threshold": True,
            "and_savings_confined_to_vacuum_or_edge": True,
            "also_kill_precomputed_spacetime_dictionary": True,
            "finite_cutoff_not_a_complexity_lower_bound": True,
        },
        "self_check": check,
        "results": results,
        "doubling_ratios": ratios,
        "verdict": {
            "W_2_14_over_W_2_13": r14["W_ratio"],
            "W_2_15_over_W_2_14": None if r15 is None else r15["W_ratio"],
            "n_32768_incomplete": incomplete_last,
            "n_32768_note": (
                "Prior attempt at n=2^15 ran >40 min, entered disk sleep at "
                "~1.5 GiB RSS, and never printed a result. Not rerun."
            ),
            "ratio_kill_fires": ratio_kill,
            "savings_confined_to_vacuum_or_edge_last_two": confined_last_two,
            "savings_confined_all_n": confined,
            "central_reuse_dominates_at_last_n": last["central_reuse_dominates"],
            "used_precomputed_spacetime_dictionary": precomputed_dictionary,
            "no_closed_recurrence": no_recurrence,
            "kill": (
                kill_work_and_confined
                or precomputed_dictionary
                or incomplete_last
                or no_recurrence
            ),
            "which_kills": {
                "work_ratio_and_confined_savings": kill_work_and_confined,
                "precomputed_dictionary": precomputed_dictionary,
                "incomplete_2_15": incomplete_last,
                "no_closed_recurrence_superlinear_W": no_recurrence,
            },
        },
        "seconds_total": time.perf_counter() - t0,
        "prize_claim": False,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUT_JSON} in {payload['seconds_total']:.3f}s")
    print("verdict:", json.dumps(payload["verdict"], indent=2))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
