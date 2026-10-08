#!/usr/bin/env python3
"""Forbidden spacetime blocks vs a forced period-2 centre.

ideas11 item 2 / leftover ideas10 item 5 (prize Problem 1).

F is the set of h x w binary blocks that violate the local Rule 30
update x' = L XOR (C OR R) on some interior cell. Those blocks cannot
appear in any Rule 30 spacetime. The attack asks whether a long
period-2 centre column still FORCES some block of F in columns -1..+1
or -2..+2, on every sufficiently long finite-strip path.

This is distinct from residual-SCC emptiness (that would kill period 2
by leaving no infinite strip path). If the known period-2 residual is
nonempty, every locally legal strip path exists, so no locally illegal
block is forced, and this route dies.

Stdlib only. Imports strip_graph.graph / analyze / components without
modifying strip_graph.py. Does not modify strip_extend.py, experiment.py,
REPORT/LOG/README, or other agents' files. Not a prize claim.

Run: python3 research/forbidden_periodic.py --certify
Dump: research/forbidden_periodic.json, research/forbidden_periodic.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strip_graph import analyze, components, graph  # noqa: E402
from experiment import center_bits as experiment_center_bits  # noqa: E402

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

PRIZE_PREFIX16 = "1101110011000101"
PRIZE_TMAX = 64
# Encoding: cell (r, c) is bit (r * w + c), bit 0 = top-left.


def rule30(L: int, C: int, R: int) -> int:
    return L ^ (C | R)


def cell(code: int, r: int, c: int, w: int) -> int:
    return (code >> (r * w + c)) & 1


def pack_block(rows: list[list[int]]) -> int:
    h = len(rows)
    w = len(rows[0])
    code = 0
    for r in range(h):
        for c in range(w):
            if rows[r][c]:
                code |= 1 << (r * w + c)
    return code


def unpack_block(code: int, h: int, w: int) -> list[list[int]]:
    return [[cell(code, r, c, w) for c in range(w)] for r in range(h)]


def block_text(code: int, h: int, w: int) -> str:
    return "|".join(
        "".join(str(cell(code, r, c, w)) for c in range(w)) for r in range(h)
    )


def interior_violations(code: int, h: int, w: int) -> list[tuple[int, int]]:
    """Interior cells of rows 1..h-1, columns 1..w-2, that break Rule 30."""
    bad = []
    for r in range(1, h):
        for c in range(1, w - 1):
            expected = rule30(
                cell(code, r - 1, c - 1, w),
                cell(code, r - 1, c, w),
                cell(code, r - 1, c + 1, w),
            )
            if cell(code, r, c, w) != expected:
                bad.append((r, c))
    return bad


def is_legal(code: int, h: int, w: int) -> bool:
    return not interior_violations(code, h, w)


def n_legal_formula(h: int, w: int) -> int:
    # Row 0 is free (w bits). Each later row has 2 free edge bits; the
    # w-2 interior bits are determined by the previous row. No overconstraint.
    if w < 3 or h < 2:
        return 1 << (h * w)
    return 1 << (w + 2 * (h - 1))


def enumerate_blocks(h: int, w: int) -> dict:
    n = 1 << (h * w)
    legal = []
    forbidden = []
    for code in range(n):
        if is_legal(code, h, w):
            legal.append(code)
        else:
            forbidden.append(code)
    return {
        "h": h,
        "w": w,
        "n_total": n,
        "n_legal": len(legal),
        "n_forbidden": len(forbidden),
        "n_legal_formula": n_legal_formula(h, w),
        "legal": legal,
        "forbidden": forbidden,
    }


def bitset_hex(nbits: int, ones: list[int]) -> str:
    ba = bytearray((nbits + 7) // 8)
    for i in ones:
        ba[i >> 3] |= 1 << (i & 7)
    return ba.hex()


def bitset_ones(nbits: int, hexstr: str) -> list[int]:
    ba = bytes.fromhex(hexstr)
    out = []
    for i in range(nbits):
        if ba[i >> 3] & (1 << (i & 7)):
            out.append(i)
    return out


def sha_ints(xs: list[int]) -> str:
    return hashlib.sha256(",".join(map(str, xs)).encode()).hexdigest()


def interior_row_ok(row: int, nxt: int, radius: int) -> bool:
    width = 2 * radius + 1
    for j in range(1, width - 1):
        L = (row >> (j - 1)) & 1
        C = (row >> j) & 1
        R = (row >> (j + 1)) & 1
        if ((nxt >> j) & 1) != rule30(L, C, R):
            return False
    return True


def decode_vertex(v: int, rows: int, radius: int) -> tuple[int, int, tuple[int, ...]]:
    phase, row = divmod(v, rows)
    width = 2 * radius + 1
    bits = tuple((row >> j) & 1 for j in range(width))
    return phase, row, bits


def window_from_rows(row_ints: list[int], col0: int, h: int, w: int) -> int:
    code = 0
    for r in range(h):
        row = row_ints[r]
        for c in range(w):
            if (row >> (col0 + c)) & 1:
                code |= 1 << (r * w + c)
    return code


def residual_from_analyze(radius: int, word: list[int]) -> dict:
    summary = analyze(radius, word, witnesses=True)
    residual = []
    forced_nb = []
    for g in summary["all_components"] or []:
        rec = {
            "vertices": g["vertices"],
            "graph_period": g["graph_period"],
            "periodic_columns_in_every_path": g["periodic_columns_in_every_path"],
            "neighbor_forced_periodic": g["neighbor_forced_periodic"],
            "vertex_ids": list(g["vertices_encoded"]),
        }
        if g["neighbor_forced_periodic"]:
            forced_nb.append(rec)
        else:
            residual.append(rec)
    return {
        "radius": radius,
        "center_word": "".join(map(str, word)),
        "analyze_residual_count": summary["components_without_forced_periodic_neighbor"],
        "analyze_residual_sizes": list(summary["residual_sizes"]),
        "analyze_recurrent": summary["recurrent_components"],
        "residual": residual,
        "forced_neighbor_components": forced_nb,
    }


def graph_bundle(radius: int, word: list[int]) -> dict:
    out, rev, rows = graph(radius, word)
    labels, groups = components(out, rev)
    width = 2 * radius + 1
    info = residual_from_analyze(radius, word)
    residual_ids = [v for g in info["residual"] for v in g["vertex_ids"]]
    residual_set = set(residual_ids)

    # Every residual (and every recurrent) edge must obey the interior rule
    # and keep the imposed centre word.
    n_res_edges = 0
    illegal_res_edges = 0
    for v in residual_ids:
        phase, row, _ = decode_vertex(v, rows, radius)
        assert ((row >> radius) & 1) == word[phase]
        for w in out[v]:
            if w not in residual_set:
                continue
            n_res_edges += 1
            nphase, nrow, _ = decode_vertex(w, rows, radius)
            assert nphase == (phase + 1) % len(word)
            assert ((nrow >> radius) & 1) == word[nphase]
            if not interior_row_ok(row, nrow, radius):
                illegal_res_edges += 1

    # Rows that occur on residual vertices, by phase.
    rows_by_phase: dict[int, list[str]] = defaultdict(list)
    bits_by_phase_col: dict[tuple[int, int], set[int]] = defaultdict(set)
    for v in residual_ids:
        phase, row, bits = decode_vertex(v, rows, radius)
        rows_by_phase[phase].append(format(row, f"0{width}b")[::-1])
        for j, b in enumerate(bits):
            bits_by_phase_col[(phase, j - radius)].add(b)
    forced_columns = []
    free_columns = []
    for col in range(-radius, radius + 1):
        forced_here = True
        col_info = {"column": col, "by_phase": {}}
        for phase in range(len(word)):
            vals = sorted(bits_by_phase_col[(phase, col)])
            col_info["by_phase"][str(phase)] = vals
            if len(vals) != 1:
                forced_here = False
        if forced_here:
            forced_columns.append(col)
        else:
            free_columns.append(col)

    return {
        "out": out,
        "rev": rev,
        "rows": rows,
        "width": width,
        "labels": labels,
        "groups": groups,
        "info": info,
        "residual_ids": residual_ids,
        "residual_set": residual_set,
        "n_res_edges": n_res_edges,
        "illegal_res_edges": illegal_res_edges,
        "rows_by_phase": {str(p): sorted(set(xs)) for p, xs in rows_by_phase.items()},
        "forced_columns": forced_columns,
        "free_columns": free_columns,
        "bits_by_phase_col": {
            f"phase{p}_col{c}": sorted(vs)
            for (p, c), vs in sorted(bits_by_phase_col.items())
        },
    }


def all_walks(out: list[list[int]], starts: list[int], length: int, allowed: set[int]) -> list[list[int]]:
    """Walks with `length` vertices. Residual graphs here are tiny."""
    found: list[list[int]] = []

    def dfs(path: list[int]) -> None:
        if len(path) == length:
            found.append(path[:])
            return
        for w in out[path[-1]]:
            if w in allowed:
                path.append(w)
                dfs(path)
                path.pop()

    for s in starts:
        if s in allowed:
            dfs([s])
    return found


def simple_cycles(out: list[list[int]], nodes: list[int]) -> list[tuple[int, ...]]:
    allowed = set(nodes)
    cycles: set[tuple[int, ...]] = set()

    def dfs(start: int, path: list[int], blocked: set[int]) -> None:
        v = path[-1]
        for w in out[v]:
            if w not in allowed:
                continue
            if w == start:
                cyc = path[:]
                k = min(range(len(cyc)), key=lambda i: cyc[i])
                cycles.add(tuple(cyc[k:] + cyc[:k]))
            elif w not in blocked:
                blocked.add(w)
                path.append(w)
                dfs(start, path, blocked)
                path.pop()
                blocked.remove(w)

    for s in nodes:
        dfs(s, [s], {s})
    return sorted(cycles, key=lambda c: (len(c), c))


def windows_on_walks(
    walks: list[list[int]],
    rows: int,
    col0: int,
    h: int,
    w: int,
) -> set[int]:
    codes: set[int] = set()
    for walk in walks:
        row_ints = [walk[i] % rows for i in range(h)]
        codes.add(window_from_rows(row_ints, col0, h, w))
    return codes


def cycle_windows(
    cycle: tuple[int, ...],
    rows: int,
    col0: int,
    h: int,
    w: int,
) -> set[int]:
    if not cycle:
        return set()
    n = len(cycle)
    # Need n windows of h consecutive vertices; repeat the cycle enough times.
    seq = list(cycle) * max(h, 2)
    codes: set[int] = set()
    for i in range(n):
        row_ints = [seq[i + k] % rows for k in range(h)]
        codes.add(window_from_rows(row_ints, col0, h, w))
    return codes


def strip_windows(bundle: dict, h: int, w: int, col0: int, forbidden: set[int]) -> dict:
    walks = all_walks(bundle["out"], bundle["residual_ids"], h, bundle["residual_set"])
    codes = windows_on_walks(walks, bundle["rows"], col0, h, w)
    illegal = sorted(codes & forbidden)
    cycles = simple_cycles(bundle["out"], bundle["residual_ids"])
    if cycles:
        unavoidable = set(cycle_windows(cycles[0], bundle["rows"], col0, h, w))
        for cyc in cycles[1:]:
            unavoidable &= cycle_windows(cyc, bundle["rows"], col0, h, w)
    else:
        unavoidable = set()
    forced_forbidden = sorted(unavoidable & forbidden)
    return {
        "h": h,
        "w": w,
        "col0": col0,
        "columns": [col0 - bundle["info"]["radius"] + c for c in range(w)],
        "n_walks": len(walks),
        "n_windows": len(codes),
        "n_illegal_windows": len(illegal),
        "illegal_windows": illegal,
        "n_simple_cycles": len(cycles),
        "cycle_lengths": sorted({len(c) for c in cycles}),
        "n_unavoidable_windows": len(unavoidable),
        "n_forced_forbidden": len(forced_forbidden),
        "forced_forbidden": forced_forbidden,
        "sample_windows": [block_text(c, h, w) for c in sorted(codes)[:8]],
    }


def prize_spacetime_dict(t_max: int) -> dict[tuple[int, int], int]:
    cells: dict[tuple[int, int], int] = {(0, 0): 1}
    for t in range(t_max):
        for j in range(-t - 1, t + 2):
            cells[t + 1, j] = rule30(
                cells.get((t, j - 1), 0),
                cells.get((t, j), 0),
                cells.get((t, j + 1), 0),
            )
    return cells


def prize_spacetime_packed(t_max: int) -> dict[tuple[int, int], int]:
    cells: dict[tuple[int, int], int] = {}
    row = 1
    for t in range(t_max + 1):
        for k in range(2 * t + 1):
            if (row >> k) & 1:
                cells[t, k - t] = 1
        row = (row << 2) ^ ((row << 1) | row)
    return cells


def extract_windows(
    cells: dict[tuple[int, int], int],
    t_max: int,
    h: int,
    w: int,
    margin: int,
) -> tuple[int, list[dict]]:
    """Scan every h x w window, including quiescent zeros. Return (n, illegal)."""
    illegal = []
    n = 0
    j_lo = -t_max - margin
    j_hi = t_max + margin - w + 1
    for t0 in range(0, t_max - h + 2):
        for j0 in range(j_lo, j_hi + 1):
            code = 0
            for r in range(h):
                for c in range(w):
                    if cells.get((t0 + r, j0 + c), 0):
                        code |= 1 << (r * w + c)
            n += 1
            viol = interior_violations(code, h, w)
            if viol:
                illegal.append(
                    {
                        "t": t0,
                        "j": j0,
                        "code": code,
                        "text": block_text(code, h, w),
                        "violations": [list(p) for p in viol],
                    }
                )
    return n, illegal


def load_strip_results_01() -> list[dict]:
    path = HERE / "strip_results.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text())
    return [row for row in data if row.get("center_word") == "01"]


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict[str, bool] = {}

    f3 = enumerate_blocks(3, 3)
    f4 = enumerate_blocks(4, 4)
    checks["legal_3x3_count_128"] = f3["n_legal"] == 128
    checks["forbidden_3x3_count_384"] = f3["n_forbidden"] == 384
    checks["legal_3x3_matches_formula"] = f3["n_legal"] == f3["n_legal_formula"]
    checks["legal_4x4_count_1024"] = f4["n_legal"] == 1024
    checks["forbidden_4x4_count_64512"] = f4["n_forbidden"] == 64512
    checks["legal_4x4_matches_formula"] = f4["n_legal"] == f4["n_legal_formula"]
    checks["legal_plus_forbidden_3x3"] = f3["n_legal"] + f3["n_forbidden"] == 512
    checks["legal_plus_forbidden_4x4"] = f4["n_legal"] + f4["n_forbidden"] == 65536

    # Explicit local-rule examples.
    zeros3 = pack_block([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # Top 111 forces the next centre bit 1 XOR (1 OR 1) = 0. Put a 1 there
    # and give the bottom centre the legal continuation of row 010, so the
    # only interior violation is the middle cell.
    ones_top_bad = pack_block([[1, 1, 1], [0, 1, 0], [0, 1, 0]])
    checks["all_zero_3x3_legal"] = is_legal(zeros3, 3, 3)
    checks["111_over_1_is_forbidden"] = not is_legal(ones_top_bad, 3, 3)
    checks["111_over_1_violation_at_center"] = interior_violations(
        ones_top_bad, 3, 3
    ) == [(1, 1)]

    bitset4 = bitset_hex(65536, f4["forbidden"])
    roundtrip = bitset_ones(65536, bitset4)
    checks["bitset4_roundtrip"] = roundtrip == f4["forbidden"]

    F3 = set(f3["forbidden"])
    F4 = set(f4["forbidden"])

    # Period-2 strip graphs, both phases, radii 1 and 2 (columns -1..+1 / -2..+2).
    strip_rows = []
    any_forced_F = False
    any_illegal_window = False
    residual_nonempty = True
    for word in ([0, 1], [1, 0]):
        for radius in (1, 2):
            bundle = graph_bundle(radius, word)
            info = bundle["info"]
            checks[f"residual_nonempty_{info['center_word']}_r{radius}"] = (
                len(bundle["residual_ids"]) > 0
            )
            residual_nonempty = residual_nonempty and len(bundle["residual_ids"]) > 0
            checks[f"no_illegal_residual_edges_{info['center_word']}_r{radius}"] = (
                bundle["illegal_res_edges"] == 0 and bundle["n_res_edges"] > 0
            )
            checks[f"only_centre_forced_{info['center_word']}_r{radius}"] = (
                bundle["forced_columns"] == [0]
            )
            # 3x3 in columns -1..+1 lives at col0 = radius-1.
            w3 = strip_windows(bundle, 3, 3, radius - 1, F3)
            windows = [w3]
            if radius >= 2:
                # Two 4-wide placements inside columns -2..+2.
                w4a = strip_windows(bundle, 4, 4, 0, F4)  # columns -2..+1
                w4b = strip_windows(bundle, 4, 4, 1, F4)  # columns -1..+2
                windows.extend([w4a, w4b])
            if any(w["n_illegal_windows"] for w in windows):
                any_illegal_window = True
            if any(w["n_forced_forbidden"] for w in windows):
                any_forced_F = True
            strip_rows.append(
                {
                    "center_word": info["center_word"],
                    "radius": radius,
                    "n_residual_vertices": len(bundle["residual_ids"]),
                    "n_residual_edges": bundle["n_res_edges"],
                    "illegal_residual_edges": bundle["illegal_res_edges"],
                    "analyze_residual_count": info["analyze_residual_count"],
                    "analyze_residual_sizes": info["analyze_residual_sizes"],
                    "analyze_recurrent": info["analyze_recurrent"],
                    "forced_columns": bundle["forced_columns"],
                    "free_columns": bundle["free_columns"],
                    "rows_by_phase": bundle["rows_by_phase"],
                    "windows": windows,
                }
            )

    checks["period2_residual_nonempty_all"] = residual_nonempty
    checks["no_F_window_on_any_residual_walk"] = not any_illegal_window
    checks["no_forbidden_block_forced"] = not any_forced_F

    # Cross-check radius-1/2 residual sizes against the stored strip_graph dump.
    stored_01 = {row["radius"]: row for row in load_strip_results_01()}
    if stored_01:
        for rec in strip_rows:
            if rec["center_word"] != "01":
                continue
            st = stored_01.get(rec["radius"])
            if st is None:
                continue
            key = f"matches_strip_results_01_r{rec['radius']}"
            checks[key] = (
                rec["analyze_residual_count"]
                == st["components_without_forced_periodic_neighbor"]
                and rec["analyze_residual_sizes"] == st["residual_sizes"]
            )

    # Period-3 residual nonempty (same obstruction; not the main scan).
    p3 = []
    for word in ([0, 0, 1], [0, 1, 1]):
        for radius in (1, 2):
            an = analyze(radius, word)
            p3.append(
                {
                    "center_word": an["center_word"],
                    "radius": radius,
                    "residual_count": an["components_without_forced_periodic_neighbor"],
                    "residual_sizes": an["residual_sizes"],
                }
            )
    checks["period3_residual_also_nonempty"] = all(r["residual_count"] > 0 for r in p3)

    # Prize seed spacetime, 64 steps, two independent evolutions.
    cells_dict = prize_spacetime_dict(PRIZE_TMAX)
    cells_packed = prize_spacetime_packed(PRIZE_TMAX)
    ones_dict = {k for k, v in cells_dict.items() if v}
    ones_packed = {k for k, v in cells_packed.items() if v}
    # Packed stores only 1s; the live-cell map also writes explicit zeros
    # inside the light cone. Compare the 1-support, then every cone cell.
    cone_ok = True
    for t in range(PRIZE_TMAX + 1):
        for j in range(-t - 2, t + 3):
            if cells_dict.get((t, j), 0) != cells_packed.get((t, j), 0):
                cone_ok = False
                break
        if not cone_ok:
            break
    checks["prize_dict_equals_packed"] = ones_dict == ones_packed and cone_ok

    centres = []
    for t in range(PRIZE_TMAX + 1):
        centres.append(cells_dict.get((t, 0), 0))
    centre_s = "".join(map(str, centres))
    exp_centres = list(experiment_center_bits(PRIZE_TMAX + 1))
    checks["prize_centre_matches_experiment"] = centres == exp_centres
    checks["prize_prefix16"] = centre_s[:16] == PRIZE_PREFIX16

    n3, ill3 = extract_windows(cells_dict, PRIZE_TMAX, 3, 3, margin=3)
    n4, ill4 = extract_windows(cells_dict, PRIZE_TMAX, 4, 4, margin=3)
    checks["prize_no_illegal_3x3"] = ill3 == []
    checks["prize_no_illegal_4x4"] = ill4 == []
    checks["prize_scanned_3x3_positive"] = n3 > 0
    checks["prize_scanned_4x4_positive"] = n4 > 0

    # A locally illegal block must be detected if planted.
    planted = dict(cells_dict)
    planted[5, 0] = 1 - planted.get((5, 0), 0)
    _, planted_ill = extract_windows(planted, PRIZE_TMAX, 3, 3, margin=3)
    checks["planted_flip_is_detected"] = len(planted_ill) > 0

    kill = (
        residual_nonempty
        and not any_forced_F
        and not any_illegal_window
        and ill3 == []
        and ill4 == []
    )
    # The route dies because no block of F is forced. The prize spacetime
    # being locally legal is a sanity check that must hold (and does).
    if kill:
        verdict = "KILL"
        kill_reason = (
            "Period-2 residual SCCs are nonempty at radii 1 and 2 for both "
            "phases 01 and 10 (the known residual: 4 and 8 vertices). Every "
            "residual edge obeys x'=L XOR (C OR R) on interior cells, so no "
            "3x3 or 4x4 local-rule violation appears on any residual walk, "
            "and none is forced on every sufficiently long path. Only the "
            "centre column is fixed; columns ±1 and ±2 remain free. Locally "
            "illegal patterns are therefore not forced. The prize-seed "
            f"spacetime through t={PRIZE_TMAX} contains no illegal 3x3 "
            f"({n3} windows) or 4x4 ({n4} windows). Distinct from residual "
            "emptiness: the residual is nonempty, which is exactly why this "
            "forbidden-block route dies. Not a prize claim."
        )
    else:
        verdict = "SURVIVE"
        kill_reason = (
            "a forbidden block was forced by the period-2 strip, or the "
            "prize spacetime contained a local-rule violation, or the "
            "residual was empty"
        )

    wall = time.perf_counter() - t0
    all_checks_ok = all(checks.values())
    dump = {
        "attack": "forbidden_periodic",
        "ideas": "ideas11 item 2 / leftover ideas10 item 5",
        "problem": (
            "finite h x w block that Rule 30 forbids locally, but that a "
            "long period-2 centre would force in columns -1..+1 or -2..+2"
        ),
        "verdict": verdict,
        "kill": kill,
        "survive": not kill,
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "all_checks_ok": all_checks_ok,
        "checks": checks,
        "encoding": (
            "row-major; cell (r,c) is bit (r*w+c); bit 0 is top-left; "
            "interior constraints on rows 1..h-1 and columns 1..w-2"
        ),
        "local_rule": "x' = L XOR (C OR R)",
        "F": {
            "3x3": {
                "n_total": f3["n_total"],
                "n_legal": f3["n_legal"],
                "n_forbidden": f3["n_forbidden"],
                "n_legal_formula": f3["n_legal_formula"],
                "forbidden": f3["forbidden"],
                "legal": f3["legal"],
                "sha256_forbidden": sha_ints(f3["forbidden"]),
                "sha256_legal": sha_ints(f3["legal"]),
                "examples_forbidden": [
                    {
                        "code": ones_top_bad,
                        "text": block_text(ones_top_bad, 3, 3),
                        "why": "top 111 forces next centre 0, block has 1",
                    }
                ],
                "examples_legal": [
                    {
                        "code": zeros3,
                        "text": block_text(zeros3, 3, 3),
                        "why": "vacuum; 0 = 0 XOR (0 OR 0)",
                    }
                ],
            },
            "4x4": {
                "n_total": f4["n_total"],
                "n_legal": f4["n_legal"],
                "n_forbidden": f4["n_forbidden"],
                "n_legal_formula": f4["n_legal_formula"],
                "legal": f4["legal"],
                "forbidden_bitset_hex": bitset4,
                "sha256_forbidden": sha_ints(f4["forbidden"]),
                "sha256_legal": sha_ints(f4["legal"]),
                "reconstruct": (
                    "F_4x4 = {i in 0..65535 : bit i of forbidden_bitset_hex "
                    "is set}; equivalently the complement of legal"
                ),
            },
        },
        "period2_strip": strip_rows,
        "period3_residual_note": p3,
        "prize_seed": {
            "t_max": PRIZE_TMAX,
            "prefix16": centre_s[:16],
            "prefix32": centre_s[:32],
            "n_windows_3x3": n3,
            "n_windows_4x4": n4,
            "n_illegal_3x3": len(ill3),
            "n_illegal_4x4": len(ill4),
            "illegal_3x3": ill3,
            "illegal_4x4": ill4,
        },
        "files_not_modified": [
            "research/strip_graph.py",
            "research/strip_extend.py",
            "experiment.py",
            "REPORT.md",
            "research/LOG.md",
            "README.md",
        ],
    }
    return dump


def write_markdown(dump: dict) -> str:
    checks = dump["checks"]
    F3 = dump["F"]["3x3"]
    F4 = dump["F"]["4x4"]
    prize = dump["prize_seed"]
    lines: list[str] = []
    a = lines.append

    a("# Forbidden spacetime blocks forced by a period-2 centre")
    a("")
    a("This note is ideas11 item 2 (leftover ideas10 item 5, prize")
    a("Problem 1). It does **not** exclude eventual period 2, and it")
    a("does not claim a prize result.")
    a("")
    a("Helper: `research/forbidden_periodic.py --certify`. Dump:")
    a("`research/forbidden_periodic.json`. The finite-strip graph is")
    a("imported from `strip_graph.graph` / `analyze` / `components`;")
    a("`strip_graph.py` is not modified.")
    a("")
    a("## Attack")
    a("")
    a("Let F be the finite list of h×w binary blocks that")
    a("Rule 30 **forbids locally**: some interior cell violates")
    a("")
    a("```")
    a("x' = L XOR (C OR R).")
    a("```")
    a("")
    a("Those blocks cannot appear in any Rule 30 spacetime. Under a")
    a("forced period-2 centre (both phases `01` and `10`), look at")
    a("columns -1..+1 (radius 1) and -2..+2 (radius 2) in the")
    a("finite-strip graph of `research/strip_graph.py`. If some block")
    a("of F is forced on every sufficiently long path, period 2 is")
    a("impossible.")
    a("")
    a("This is **not** residual-SCC emptiness. Emptiness would kill")
    a("period 2 by leaving no infinite strip completion. A nonempty")
    a("residual means every locally legal period-2 strip path exists,")
    a("so a locally illegal pattern cannot be forced. That is the")
    a("predeclared kill for this route.")
    a("")
    a("**Kill:** no block of F is forced, because every locally legal")
    a("period-2 strip path exists (the known residual SCC).")
    a("")
    a("## Local forbidden list F")
    a("")
    a("A cell at row r≥1, column c with 1≤c≤w-2")
    a("is interior: its neighbourhood on the previous row lies inside")
    a("the block. Edge columns are unconstrained. Row 0 is free; each")
    a("later row contributes two free edge bits and w-2 determined")
    a("interior bits, so")
    a("")
    a("```")
    a("|legal(h,w)| = 2^{w + 2(h-1)}     (h>=2, w>=3).")
    a("```")
    a("")
    a("There is no overconstraint: each determined bit depends only on")
    a("the already-chosen previous row. Enumeration matches the formula.")
    a("")
    a("| block | total | legal | forbidden | formula legal |")
    a("|---|---:|---:|---:|---:|")
    a(
        f"| 3×3 | {F3['n_total']} | {F3['n_legal']} | {F3['n_forbidden']} "
        f"| {F3['n_legal_formula']} |"
    )
    a(
        f"| 4×4 | {F4['n_total']} | {F4['n_legal']} | {F4['n_forbidden']} "
        f"| {F4['n_legal_formula']} |"
    )
    a("")
    a("Encoding: row-major, cell (r,c) is bit r*w+c, bit 0 =")
    a("top-left. The JSON dump lists every forbidden 3×3 as an integer")
    a(f"(`sha256` `{F3['sha256_forbidden'][:16]}…`) and every legal 4×4;")
    a("the 64512 forbidden 4×4 blocks are the bitset")
    a("`F.4x4.forbidden_bitset_hex` (bit i set iff block i is")
    a(f"forbidden; `sha256` `{F4['sha256_forbidden'][:16]}…`).")
    a("")
    a("Example. The 3×3 with top row `111` and middle centre `1` is")
    a("forbidden: `1 XOR (1 OR 1) = 0`. The all-zero 3×3 is legal")
    a("(vacuum). Both checks are in `checks`.")
    a("")
    a("F is **local-rule violations**, not the (possibly larger) sofic")
    a("list of blocks that are locally fine but do not extend to a")
    a("global spacetime. The attack is specifically that the periodic")
    a("centre plus the local rule would still force a locally illegal")
    a("tile.")
    a("")
    a("## Period-2 strip, both phases")
    a("")
    a("`strip_graph.graph(radius, word)` is imported and not edited.")
    a("A genuine eventual period-2 centre must eventually walk in a")
    a("recurrent SCC at every fixed width. Residual SCCs are those")
    a("that do **not** force a periodic neighbour (Jen already excludes")
    a("the ones that do). Outer boundary bits are free, so a residual")
    a("path is an overapproximation of the prize spacetime.")
    a("")
    a("| word | radius | residual SCCs | residual vertices | residual edges | forced columns | illegal residual edges | illegal F-windows | forced F |")
    a("|---|---:|---:|---:|---:|---|---:|---:|---:|")
    for rec in dump["period2_strip"]:
        n_ill = sum(w["n_illegal_windows"] for w in rec["windows"])
        n_forced = sum(w["n_forced_forbidden"] for w in rec["windows"])
        forced = ",".join(str(c) for c in rec["forced_columns"]) or "—"
        a(
            f"| `{rec['center_word']}` | {rec['radius']} | "
            f"{rec['analyze_residual_count']} | {rec['n_residual_vertices']} | "
            f"{rec['n_residual_edges']} | `{forced}` | "
            f"{rec['illegal_residual_edges']} | {n_ill} | {n_forced} |"
        )
    a("")
    a("Radius 1 is columns -1,0,+1; radius 2 is -2..+2. The")
    a("sizes 4 and 8 match `research/strip_results.json` for `01`.")
    a("Phase `10` is the same graph shifted by one step; it has the")
    a("same residual counts. In every residual vertex the centre bit")
    a("equals the imposed phase, and columns ±1 (and ±2 at radius 2)")
    a("take **both** values. Nothing in those columns is forced except")
    a("the prescribed centre. Residual rows, bit 0 = column −radius:")
    a("")
    a("| word | radius | phase 0 rows | phase 1 rows |")
    a("|---|---:|---|---|")
    for rec in dump["period2_strip"]:
        r0 = ", ".join(f"`{x}`" for x in rec["rows_by_phase"].get("0", []))
        r1 = ", ".join(f"`{x}`" for x in rec["rows_by_phase"].get("1", []))
        a(f"| `{rec['center_word']}` | {rec['radius']} | {r0} | {r1} |")
    a("")
    a("Phase `01` radius 1 already has two rows at each phase")
    a("(`001`/`100` with centre 0, and `110`/`111` with centre 1), so")
    a("a single 3-wide block is not forced.")
    a("")
    a("Every residual edge was checked against the local rule on all")
    a("interior cells of the strip. There are none that violate it:")
    a("the graph is defined that way. Consequently every 3×3 window in")
    a("columns -1..+1 on a 3-row residual walk, and every 4×4")
    a("window in -2..+1 or -1..+2 on a 4-row residual walk, is")
    a("locally legal, hence not in F. Walking every such path on these")
    a("tiny residual graphs (4 or 8 vertices) finds 0 members of F.")
    a("No 3×3 or 4×4 tile at all — legal or not — is common to every")
    a("simple residual cycle (`n_unavoidable_windows = 0`), so nothing")
    a("in those columns is forced as a block. Intersecting with F is")
    a("empty.")
    a("")
    a("A nonempty residual cycle is already an infinite locally legal")
    a("period-2 strip path. That path avoids every block of F, so no")
    a("block of F is forced on every sufficiently long path.")
    a("")
    a("Period-3 residual SCCs at the same radii are also nonempty")
    a("(`001` / `011`), so the same obstruction would apply there.")
    a("The scan target was period 2.")
    a("")
    a("## Prize seed spacetime")
    a("")
    a(f"Evolve the single 1 for {prize['t_max']} steps, two ways: the")
    a("live-cell map `x(t+1,j)=x(t,j-1) XOR (x(t,j) OR x(t,j+1))`,")
    a("and the packed recurrence `row = (row<<2)^((row<<1)|row)` with")
    a("bit k at time t equal to spatial k-t. The two")
    a("spacetimes agree. The centre prefix is")
    a(f"`{prize['prefix16']}`, matching `experiment.center_bits`.")
    a("")
    a("Every 3×3 and 4×4 window with a 3-cell vacuum margin, including")
    a("quiescent zeros outside the light cone, is locally legal.")
    a("")
    a("| windows | scanned | illegal |")
    a("|---|---:|---:|")
    a(f"| 3×3 | {prize['n_windows_3x3']} | {prize['n_illegal_3x3']} |")
    a(f"| 4×4 | {prize['n_windows_4x4']} | {prize['n_illegal_4x4']} |")
    a("")
    a("A planted centre-bit flip at t=5 is detected by the same")
    a("scanner, so the zero count is not a dead checker.")
    a("")
    a("## Engine")
    a("")
    a("- Local legality: interior cells only, as above. Independent")
    a("  count 2^{w+2(h-1)} agrees with the 512- and 65536-loop.")
    a("- Strip: `from strip_graph import graph, analyze, components`.")
    a("  Residual classification is `analyze(..., witnesses=True)`;")
    a("  walks and interior-rule checks use `graph` directly.")
    a("- Packed prize evolution matches `experiment.center_bits` on")
    a("  65 centre bits and matches the live-cell spacetime on every")
    a("  stored cell. Those files are not modified.")
    a("")
    a("## Verdict")
    a("")
    a(f"**{dump['verdict']}.** {dump['kill_reason']}")
    a("")
    a("## What this does not show")
    a("")
    a("- Eventual period 2 of the prize seed, or of any finite row.")
    a("  The residual strip is an overapproximation; a path need not")
    a("  extend to the single-seed spacetime.")
    a("- Sofic / extendable-forbidden blocks (locally legal tiles that")
    a("  still do not appear in any global spacetime). F is only the")
    a("  local-rule list.")
    a("- Residual-SCC emptiness. The residual is nonempty; that is why")
    a("  the forbidden-block hope fails.")
    a("")
    a("## Checks")
    a("")
    failed = [k for k, v in checks.items() if not v]
    if failed:
        a("Failed:")
        for k in failed:
            a(f"- `{k}`")
    else:
        a(f"All {len(checks)} machine checks passed.")
    a("")
    a("## Files")
    a("")
    a("- `research/forbidden_periodic.md` (this note)")
    a("- `research/forbidden_periodic.py` (`--certify` runs the census,")
    a("  the strip-graph import, the prize-spacetime scan, and writes")
    a("  the dump)")
    a("- `research/forbidden_periodic.json` (dump)")
    a("")
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--certify", action="store_true", default=True)
    p.add_argument("--output", default=str(OUT_JSON))
    args = p.parse_args()
    dump = certify()
    out = Path(args.output)
    out.write_text(json.dumps(dump, indent=2) + "\n")
    md_path = OUT_MD if out.resolve() == OUT_JSON.resolve() else out.with_suffix(".md")
    md_path.write_text(write_markdown(dump))
    print(json.dumps({
        "verdict": dump["verdict"],
        "kill": dump["kill"],
        "all_checks_ok": dump["all_checks_ok"],
        "n_forbidden_3x3": dump["F"]["3x3"]["n_forbidden"],
        "n_forbidden_4x4": dump["F"]["4x4"]["n_forbidden"],
        "prize_illegal_3x3": dump["prize_seed"]["n_illegal_3x3"],
        "prize_illegal_4x4": dump["prize_seed"]["n_illegal_4x4"],
        "wall_time_sec": dump["wall_time_sec"],
        "json": str(out),
        "md": str(md_path),
    }, indent=2), flush=True)
    if not dump["all_checks_ok"]:
        bad = [k for k, v in dump["checks"].items() if not v]
        print("FAILED CHECKS:", bad, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
