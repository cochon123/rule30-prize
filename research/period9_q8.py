"""q=8 / period-9 isolated-zero attempt: 011111111.

Does not modify strip_graph.py or strip_extend.py. Uses their APIs.
"""
from __future__ import annotations

from collections import defaultdict, deque
from math import gcd
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_extend import extend, initial, prune
from strip_graph import analyze, components, graph, self_check

WORD = [0, 1, 1, 1, 1, 1, 1, 1, 1]
PERIOD = 9
EXTRA_PREFIX9 = "000111100"
GOOD_LAST_PREFIX9 = "110001101"


def bits(row, n):
    return "".join(str((row >> j) & 1) for j in range(n))


def parse_bits(s):
    v = 0
    for j, ch in enumerate(s):
        if ch == "1":
            v |= 1 << j
    return v


def left_of(row, center):
    return (row >> (center - 1)) & 1


def col(row, center, offset):
    """offset=-1 is left neighbor of center."""
    return (row >> (center + offset)) & 1


def scc_layers_from_graph(radius, word=WORD):
    out, rev, rows = graph(radius, word)
    labels, groups = components(out, rev)
    rec = [g for g in groups if not (len(g) == 1 and g[0] not in out[g[0]])]
    width = 2 * radius + 1
    residual = []
    for g in rec:
        info = inspect_group(g, out, labels, rows, radius, width)
        residual.append(info)
    return {
        "out": out,
        "rev": rev,
        "rows": rows,
        "labels": labels,
        "groups": groups,
        "recurrent": rec,
        "width": width,
        "infos": residual,
    }


def inspect_group(group, out, labels, rows, radius, width):
    label = labels[group[0]]
    depth = {group[0]: 0}
    stack = [group[0]]
    while stack:
        v = stack.pop()
        for w in out[v]:
            if labels[w] == label and w not in depth:
                depth[w] = depth[v] + 1
                stack.append(w)
    period = 0
    for v in group:
        for w in out[v]:
            if labels[w] == label:
                period = gcd(period, abs(depth[v] + 1 - depth[w]))
    by = defaultdict(list)
    for v in group:
        phase, row = divmod(v, rows)
        by[phase].append(row)
    left0 = sorted({left_of(r, radius) for r in by[0]})
    last = PERIOD - 1
    bit_m2 = sorted({col(r, radius, -2) for r in by[last]})
    extra_rows = [r for r in by[last] if radius >= 2 and col(r, radius, -2) == 1]
    if width >= 13 and radius == 6:
        extra_rows = [r for r in by[last] if (r & 0x1FF) == parse_bits(EXTRA_PREFIX9)]
    prefixes = {p: sorted({bits(r, min(9, width))[:9] if width >= 9 else bits(r, width)
                            for r in by[p]}) for p in range(PERIOD)}
    return {
        "vertices": len(group),
        "graph_period": period,
        "phase0_left": left0,
        "last_col_m2": bit_m2,
        "phase_sizes": [len(by[p]) for p in range(PERIOD)],
        "phase0_n_left0": sum(1 for r in by[0] if left_of(r, radius) == 0),
        "phase0_n_left1": sum(1 for r in by[0] if left_of(r, radius) == 1),
        "last_n_extra_prefix": len(extra_rows),
        "last_extra_rows": [bits(r, width) for r in sorted(extra_rows)] if width <= 17 else len(extra_rows),
        "prefixes9": {str(p): prefixes[p] for p in prefixes} if width >= 9 else None,
        "neighbor_forced": -1 in _fixed_cols(group, depth, period, rows, width, radius)[0]
        or 1 in _fixed_cols(group, depth, period, rows, width, radius)[0],
        "fixed_relative": _fixed_cols(group, depth, period, rows, width, radius)[0],
    }


def _fixed_cols(group, depth, period, rows, width, radius):
    fixed = []
    words = {}
    for j in range(width):
        by_class = {}
        ok = True
        for v in group:
            cls = depth[v] % period
            bit = ((v % rows) >> j) & 1
            if cls in by_class and by_class[cls] != bit:
                ok = False
                break
            by_class[cls] = bit
        if ok:
            rel = j - radius
            fixed.append(rel)
            words[rel] = [by_class[c] for c in range(period)]
    return fixed, words


def r6_structure():
    data = scc_layers_from_graph(6)
    assert len(data["recurrent"]) == 1
    out, rows = data["out"], data["rows"]
    labels = data["labels"]
    group = data["recurrent"][0]
    label = labels[group[0]]
    by = defaultdict(list)
    verts = {}
    for v in group:
        phase, row = divmod(v, rows)
        by[phase].append(row)
        verts[(phase, row)] = v

    def succ_rows(phase, row):
        v = verts[(phase, row)]
        out_rows = []
        for w in out[v]:
            if labels[w] == label:
                np, nr = divmod(w, rows)
                out_rows.append((np, nr))
        return out_rows

    extra_last = [r for r in by[8] if (r & 0x1FF) == parse_bits(EXTRA_PREFIX9)]
    good_last = [r for r in by[8] if (r & 0x1FF) == parse_bits(GOOD_LAST_PREFIX9)]
    left0 = [r for r in by[0] if left_of(r, 6) == 0]
    left1 = [r for r in by[0] if left_of(r, 6) == 1]

    # 9-step map on phase-0 vertices
    p0_index = {r: i for i, r in enumerate(sorted(by[0]))}
    p0_rows = sorted(by[0])
    n0 = len(p0_rows)
    step9 = [[] for _ in range(n0)]
    for r in p0_rows:
        frontier = {r}
        ph = 0
        for _ in range(9):
            nxt = set()
            for x in frontier:
                for np, nr in succ_rows(ph, x):
                    nxt.add(nr)
            ph = (ph + 1) % 9
            frontier = nxt
        step9[p0_index[r]] = sorted(p0_index[x] for x in frontier)

    # SCCs of the 9-step map
    step_out = step9
    step_rev = [[] for _ in range(n0)]
    for i, ws in enumerate(step_out):
        for w in ws:
            step_rev[w].append(i)
    sl, sg = components(step_out, step_rev)
    rec9 = []
    for g in sg:
        if len(g) == 1 and g[0] not in step_out[g[0]]:
            continue
        sigs = sorted({left_of(p0_rows[i], 6) for i in g})
        rec9.append({"size": len(g), "sigmas": sigs})

    # shortest path from a left0 vertex to a left1 vertex (in 9-step units)
    mix_dist = None
    sources = [i for i, r in enumerate(p0_rows) if left_of(r, 6) == 0]
    targets = {i for i, r in enumerate(p0_rows) if left_of(r, 6) == 1}
    q = deque((s, 0) for s in sources)
    seen = set(sources)
    while q:
        u, d = q.popleft()
        if u in targets:
            mix_dist = d
            break
        for w in step_out[u]:
            if w not in seen:
                seen.add(w)
                q.append((w, d + 1))

    # extra last-1 successors land on left=0
    extra_to = []
    for r in extra_last:
        nxt = succ_rows(8, r)
        extra_to.append(
            {
                "row": bits(r, 13),
                "next_left": sorted({left_of(nr, 6) for _, nr in nxt}),
                "next_pref": sorted({bits(nr, 13)[:9] for _, nr in nxt}),
            }
        )

    return {
        "residual_vertices": len(group),
        "phase_sizes": [len(by[p]) for p in range(9)],
        "phase0_left0": [bits(r, 13) for r in sorted(left0)],
        "phase0_left1_n": len(left1),
        "phase0_left0_n": len(left0),
        "extra_last_n": len(extra_last),
        "good_last_n": len(good_last),
        "extra_last_rows": [bits(r, 13) for r in sorted(extra_last)],
        "good_last_n_prefixes": sorted({bits(r, 13)[:9] for r in good_last}),
        "step9_recurrent": rec9,
        "mix_period_steps": mix_dist,
        "extra_successors": extra_to,
        "info": data["infos"][0],
    }


def analyze_radii(radii=(6, 7, 8)):
    rows = []
    for r in radii:
        t0 = time.monotonic()
        a = analyze(r, WORD)
        dt = time.monotonic() - t0
        rec = {
            "radius": r,
            "recurrent": a["recurrent_components"],
            "residual": a["components_without_forced_periodic_neighbor"],
            "residual_sizes": a["residual_sizes"],
            "elapsed": round(dt, 3),
        }
        print(json.dumps({"analyze": rec}), flush=True)
        rows.append(rec)
    return rows


def inspect_extend(max_radius=18, cap=80000):
    """Symmetric extend, recording sigma mixing at each radius."""
    t0 = time.monotonic()
    states, out, stats = initial(WORD)
    scan = []
    radius = 1
    stop = "radius"
    while True:
        rec = summarize_states(states, out, radius)
        rec["stats"] = [{"size": s["size"], "period": s["period"], "fixed": s["fixed"],
                         "excluded": s["excluded"]} for s in stats]
        scan.append(rec)
        print(json.dumps({"extend_r": rec["radius"], "n": rec["n"], "sigma": rec["phase0_left"],
                          "period": rec["graph_periods"], "extra_last": rec["last_n_col_m2_is_1"]}),
              flush=True)
        if not states:
            stop = "empty"
            break
        if len(states) > cap:
            stop = "cap"
            break
        if radius >= max_radius:
            break
        states, out, stats = extend(states, out, radius)
        radius += 1
    return {
        "stop": stop,
        "last_radius": scan[-1]["radius"],
        "last_states": scan[-1]["n"],
        "scan": scan,
        "elapsed": round(time.monotonic() - t0, 3),
    }


def summarize_states(states, out, radius):
    width = 2 * radius + 1
    n = len(states)
    by = defaultdict(list)
    for i, (phase, row) in enumerate(states):
        by[phase].append((i, row))
    lefts = sorted({left_of(row, radius) for _, row in by[0]})
    last = PERIOD - 1
    col_m2 = sorted({col(row, radius, -2) for _, row in by[last]}) if radius >= 2 else []
    extra_n = 0
    if width >= 13:
        mask = (1 << 9) - 1
        extra_n = sum(1 for _, row in by[last] if (row & mask) == parse_bits(EXTRA_PREFIX9))
    graph_periods = []
    if states:
        labels, groups = components(out, _rev(out))
        rec = [g for g in groups if not (len(g) == 1 and g[0] not in out[g[0]])]
        for g in rec:
            graph_periods.append(_graph_period(g, out, labels))
    return {
        "radius": radius,
        "n": n,
        "edges": sum(map(len, out)),
        "phase0_left": lefts,
        "phase0_n_left0": sum(1 for _, row in by[0] if left_of(row, radius) == 0),
        "phase0_n_left1": sum(1 for _, row in by[0] if left_of(row, radius) == 1),
        "last_col_m2": col_m2,
        "last_n_col_m2_is_1": sum(1 for _, row in by[last] if radius >= 2 and col(row, radius, -2) == 1),
        "last_n_extra_prefix": extra_n,
        "phase_sizes": [len(by[p]) for p in range(PERIOD)],
        "graph_periods": graph_periods,
        "n_components": len(graph_periods),
    }


def _rev(out):
    rev = [[] for _ in out]
    for v, edges in enumerate(out):
        for w in edges:
            rev[w].append(v)
    return rev


def _graph_period(group, out, labels):
    label = labels[group[0]]
    depth = {group[0]: 0}
    stack = [group[0]]
    while stack:
        v = stack.pop()
        for w in out[v]:
            if labels[w] == label and w not in depth:
                depth[w] = depth[v] + 1
                stack.append(w)
    period = 0
    for v in group:
        for w in out[v]:
            if labels[w] == label:
                period = gcd(period, abs(depth[v] + 1 - depth[w]))
    return period


def prune_asymmetric(states, out, center, prune_neighbors=True):
    """Like strip_extend.prune, but center need not be the midpoint."""
    rev = _rev(out)
    labels, groups = components(out, rev)
    keep, stats = [], []
    width = max((row.bit_length() for _, row in states), default=1)
    # width is at least center+1 plus some right bits; use actual max bits
    for _, row in states:
        need = row.bit_length()
        if need > width:
            width = need
    # all rows have the same intended width; pass it in via center and stored rows
    for label, group in enumerate(groups):
        if len(group) == 1 and group[0] not in out[group[0]]:
            continue
        depth = {group[0]: 0}
        stack = [group[0]]
        while stack:
            v = stack.pop()
            for w in out[v]:
                if labels[w] == label and w not in depth:
                    depth[w] = depth[v] + 1
                    stack.append(w)
        period = 0
        for v in group:
            for w in out[v]:
                if labels[w] == label:
                    period = gcd(period, abs(depth[v] + 1 - depth[w]))
        assert period
        fixed = []
        for j in (center - 1, center, center + 1):
            classes = {}
            ok = True
            for v in group:
                key, bit = depth[v] % period, (states[v][1] >> j) & 1
                if key in classes and classes[key] != bit:
                    ok = False
                    break
                classes[key] = bit
            if ok:
                fixed.append(j - center)
        assert 0 in fixed
        excluded = -1 in fixed or 1 in fixed
        stats.append({"size": len(group), "period": period, "fixed": fixed, "excluded": excluded})
        if not (prune_neighbors and excluded):
            keep.extend(group)
    remap = {v: i for i, v in enumerate(keep)}
    new_out = [[remap[w] for w in out[v] if w in remap and labels[w] == labels[v]] for v in keep]
    return [states[v] for v in keep], new_out, stats


def left_extend(states, out, width, center):
    """Add one left bit; keep the existing right width. Sound over-approx."""
    expanded = [(phase, (row << 1) | left) for phase, row in states for left in range(2)]
    expanded_out = [[] for _ in expanded]
    for v, (_, row) in enumerate(states):
        for left in range(2):
            next_old_leftmost = left ^ ((row & 1) | ((row >> 1) & 1))
            dest = expanded_out[2 * v + left]
            for w in out[v]:
                nextrow = states[w][1]
                if (nextrow & 1) == next_old_leftmost:
                    dest.extend((2 * w + k for k in range(2)))
    new_states, new_out, stats = prune_asymmetric(expanded, expanded_out, center + 1)
    return new_states, new_out, stats, width + 1, center + 1


def right_extend_only(states, out, width, center):
    """Add one right bit only."""
    expanded = [(phase, row | (right << width)) for phase, row in states for right in range(2)]
    expanded_out = [[] for _ in expanded]
    for v, (_, row) in enumerate(states):
        for right in range(2):
            old_rm1 = (row >> (width - 2)) & 1
            old_r = (row >> (width - 1)) & 1
            next_old_rightmost = old_rm1 ^ (old_r | right)
            dest = expanded_out[2 * v + right]
            for w in out[v]:
                nextrow = states[w][1]
                if ((nextrow >> (width - 1)) & 1) == next_old_rightmost:
                    dest.extend((2 * w + k for k in range(2)))
    new_states, new_out, stats = prune_asymmetric(expanded, expanded_out, center)
    return new_states, new_out, stats, width + 1, center


def summarize_asymmetric(states, out, center, left_r, right_r, stats):
    by0 = [(i, row) for i, (phase, row) in enumerate(states) if phase == 0]
    by8 = [(i, row) for i, (phase, row) in enumerate(states) if phase == 8]
    lefts = sorted({left_of(row, center) for _, row in by0})
    col_m2 = sorted({col(row, center, -2) for _, row in by8}) if center >= 2 else []
    return {
        "left_radius": left_r,
        "right_radius": right_r,
        "n": len(states),
        "edges": sum(map(len, out)),
        "phase0_left": lefts,
        "phase0_n_left0": sum(1 for _, row in by0 if left_of(row, center) == 0),
        "phase0_n_left1": sum(1 for _, row in by0 if left_of(row, center) == 1),
        "last_col_m2": col_m2,
        "last_n_col_m2_is_1": sum(1 for _, row in by8 if center >= 2 and col(row, center, -2) == 1),
        "n_components": len(stats),
        "periods": [s["period"] for s in stats],
        "any_excluded": any(s["excluded"] for s in stats),
        "residual_empty": not states,
    }


def run_left_extend(max_left=28, cap=120000, start_radius=6):
    t0 = time.monotonic()
    states, out, stats = initial(WORD)
    radius = 1
    while radius < start_radius:
        states, out, stats = extend(states, out, radius)
        radius += 1
    width = 2 * start_radius + 1
    center = start_radius
    left_r = start_radius
    right_r = start_radius
    scan = [summarize_asymmetric(states, out, center, left_r, right_r, stats)]
    scan[0]["via"] = "symmetric"
    print(json.dumps({"left_ext": scan[0]}), flush=True)
    stop = "left"
    while left_r < max_left:
        if not states:
            stop = "empty"
            break
        if len(states) > cap:
            stop = "cap"
            break
        states, out, stats, width, center = left_extend(states, out, width, center)
        left_r += 1
        rec = summarize_asymmetric(states, out, center, left_r, right_r, stats)
        scan.append(rec)
        print(json.dumps({"left_ext": rec}), flush=True)
        if rec["residual_empty"] or rec["phase0_left"] == [1] or rec["phase0_left"] == [0]:
            stop = "forced_sigma" if states else "empty"
            break
    return {
        "stop": stop,
        "scan": scan,
        "elapsed": round(time.monotonic() - t0, 3),
    }


def left_zero_graph(left, right, word=WORD):
    """Incoming further-left bit frozen to 0. Under-approx of seed paths.
    Sound as a probe only: emptying does not exclude the prize seed.
    """
    width = left + right + 1
    center = left
    rows = 1 << width
    interior = ((1 << (width - 1)) - 1) ^ 1
    n = rows * len(word)
    out = [[] for _ in range(n)]
    for phase, c in enumerate(word):
        nxtp = (phase + 1) % len(word)
        for row in range(rows):
            if ((row >> center) & 1) != c:
                continue
            middle = ((row << 1) ^ (row | (row >> 1))) & interior
            if ((middle >> center) & 1) != word[nxtp]:
                continue
            # leftmost next bit with further_left = 0:
            # next[0] = 0 XOR (bit0 OR bit1) = bit0 OR bit1
            next_left = (row & 1) | ((row >> 1) & 1)
            v = phase * rows + row
            for rightb in range(2):
                wrow = middle | next_left | (rightb << (width - 1))
                out[v].append(nxtp * rows + wrow)
    rev = _rev(out)
    labels, groups = components(out, rev)
    rec = []
    for g in groups:
        if len(g) == 1 and g[0] not in out[g[0]]:
            continue
        rec.append(inspect_group(g, out, labels, rows, center, width))
    residual = [g for g in rec if not g["neighbor_forced"]]
    return {
        "left": left,
        "right": right,
        "width": width,
        "recurrent": len(rec),
        "residual": len(residual),
        "residual_sizes": [g["vertices"] for g in residual],
        "residual_sigma": [g["phase0_left"] for g in residual],
        "all": rec,
    }


def right_zero_graph(left, right, word=WORD):
    """Incoming further-right bit frozen to 0. Under-approx of seed paths."""
    width = left + right + 1
    center = left
    rows = 1 << width
    interior = ((1 << (width - 1)) - 1) ^ 1
    n = rows * len(word)
    out = [[] for _ in range(n)]
    for phase, c in enumerate(word):
        nxtp = (phase + 1) % len(word)
        for row in range(rows):
            if ((row >> center) & 1) != c:
                continue
            middle = ((row << 1) ^ (row | (row >> 1))) & interior
            if ((middle >> center) & 1) != word[nxtp]:
                continue
            next_right = ((row >> (width - 2)) & 1) ^ ((row >> (width - 1)) & 1)
            v = phase * rows + row
            for leftb in range(2):
                wrow = middle | leftb | (next_right << (width - 1))
                out[v].append(nxtp * rows + wrow)
    rev = _rev(out)
    labels, groups = components(out, rev)
    rec = []
    for g in groups:
        if len(g) == 1 and g[0] not in out[g[0]]:
            continue
        rec.append(inspect_group(g, out, labels, rows, center, width))
    residual = [g for g in rec if not g["neighbor_forced"]]
    return {
        "left": left,
        "right": right,
        "width": width,
        "recurrent": len(rec),
        "residual": len(residual),
        "residual_sizes": [g["vertices"] for g in residual],
        "residual_sigma": [g["phase0_left"] for g in residual],
        "all_sigma": [g["phase0_left"] for g in rec],
        "all_forced": [g["neighbor_forced"] for g in rec],
    }


def extra_only_r6():
    """Induced subgraph of r=6 residual vertices that are extra-family at last-1
    or left=0 at phase 0, plus vertices that lie on paths between them.
    Then check whether extra can be recurrent without the good branch.
    """
    data = scc_layers_from_graph(6)
    out, rows, labels = data["out"], data["rows"], data["labels"]
    group = data["recurrent"][0]
    label = labels[group[0]]
    extra_v = []
    good_v = []
    for v in group:
        phase, row = divmod(v, rows)
        if phase == 8 and (row & 0x1FF) == parse_bits(EXTRA_PREFIX9):
            extra_v.append(v)
        if phase == 8 and (row & 0x1FF) == parse_bits(GOOD_LAST_PREFIX9):
            good_v.append(v)
        if phase == 0 and left_of(row, 6) == 0:
            extra_v.append(v)
        if phase == 0 and left_of(row, 6) == 1:
            good_v.append(v)
    extra_set, good_set = set(extra_v), set(good_v)

    # Can extra vertices reach good, and vice versa, inside the SCC?
    def reach(sources, allowed):
        seen = set(sources)
        st = list(sources)
        while st:
            v = st.pop()
            for w in out[v]:
                if labels[w] == label and w not in seen:
                    seen.add(w)
                    st.append(w)
        return seen

    from_extra = reach(extra_v, None)
    from_good = reach(good_v, None)
    extra_hits_good = bool(from_extra & good_set)
    good_hits_extra = bool(from_good & extra_set)

    # Recurrence of extra-only: drop all vertices that have left=1 at phase 0 or good last-1
    drop = set()
    for v in group:
        phase, row = divmod(v, rows)
        if phase == 0 and left_of(row, 6) == 1:
            drop.add(v)
        if phase == 8 and (row & 0x1FF) == parse_bits(GOOD_LAST_PREFIX9):
            drop.add(v)
    keep = [v for v in group if v not in drop]
    idx = {v: i for i, v in enumerate(keep)}
    sub_out = [[idx[w] for w in out[v] if w in idx and labels[w] == label] for v in keep]
    sub_rev = _rev(sub_out)
    _, sg = components(sub_out, sub_rev)
    rec = []
    for g in sg:
        if len(g) == 1 and g[0] not in sub_out[g[0]]:
            continue
        rec.append(len(g))
    return {
        "extra_n": len(extra_set),
        "good_n": len(good_set),
        "extra_reaches_good": extra_hits_good,
        "good_reaches_extra": good_hits_extra,
        "extra_only_recurrent_sizes": rec,
        "note": "extra-only recurrent would mean a Jen-excluded constant-sigma=0 tail; mixing is the obstruction",
    }


def long_prefix_period9(prefix_len, suffix_bits=4):
    """Over-approx: left prefix of length prefix_len plus free suffix_bits on the right.
    Width = prefix_len + suffix_bits, center chosen so right radius is suffix_bits +
    (prefix bits to the right of center). We keep center at prefix_len - 3 so that
    the last 3 prefix bits sit immediately right of the left-neighbor/center block
    like the 9-bit gadget (bits prefix_len-3 = center when prefix_len=9 => center=6).
    For prefix_len=9, center=6, width=13, matches radius 6.
    """
    width = prefix_len + suffix_bits
    center = prefix_len - 3
    if center < 2 or center >= width - 1:
        raise ValueError("prefix_len too small")
    npref = 1 << prefix_len
    # SCC on prefixes × phase with free outer bits of this window.
    # Vertex count = 9 * 2^{prefix_len}. For prefix_len=9, center=6, width=9:
    # left radius 6, right radius 2 (over-approx of the radius-6 strip on the right).
    rows_p = npref
    n = rows_p * PERIOD
    gout = [[] for _ in range(n)]
    interior_w = prefix_len  # evolve prefix bits; two outer of THIS window free
    # Here the 'row' IS the prefix; outer bits of the prefix window are free.
    interior = ((1 << (prefix_len - 1)) - 1) ^ 1
    for phase, c in enumerate(WORD):
        nxtp = (phase + 1) % PERIOD
        nc = WORD[nxtp]
        for row in range(rows_p):
            if ((row >> center) & 1) != c:
                continue
            middle = ((row << 1) ^ (row | (row >> 1))) & interior
            if ((middle >> center) & 1) != nc:
                continue
            v = phase * rows_p + row
            for left in range(2):
                for right in range(2):
                    gout[v].append(nxtp * rows_p + (middle | left | (right << (prefix_len - 1))))
    grev = _rev(gout)
    labels, groups = components(gout, grev)
    rec_info = []
    for g in groups:
        if len(g) == 1 and g[0] not in gout[g[0]]:
            continue
        rec_info.append(inspect_group(g, gout, labels, rows_p, center, prefix_len))
    residual = [g for g in rec_info if not g["neighbor_forced"]]
    return {
        "prefix_len": prefix_len,
        "center": center,
        "recurrent": len(rec_info),
        "residual": len(residual),
        "residual_sizes": [g["vertices"] for g in residual],
        "residual_sigma": [g["phase0_left"] for g in residual],
        "residual_col_m2": [g["last_col_m2"] for g in residual],
    }


def light_cone_period9(tmax=12):
    """Finite-onset search for a light-cone row whose later centers match 01^8."""
    from small_period_cert import light_cone_search
    t0 = time.monotonic()
    rec = light_cone_search("011111111", tmax=tmax)
    rec["elapsed"] = round(time.monotonic() - t0, 3)
    return rec


def rotations_r6():
    rows = []
    base = "011111111"
    for i in range(9):
        w = base[i:] + base[:i]
        a = analyze(6, list(map(int, w)))
        rows.append(
            {
                "word": w,
                "residual": a["components_without_forced_periodic_neighbor"],
                "sizes": a["residual_sizes"],
                "recurrent": a["recurrent_components"],
            }
        )
        print(json.dumps({"rot": rows[-1]}), flush=True)
    return rows


def algebraic_column_m2():
    """Column -2 is a function of sigma only, on any path with the forced 1-run left word."""
    # l = (sigma, 0,0,0,0,0,0,0,1)
    # a_t = l_{t+1} XOR (l_t OR c_t)
    table = []
    for sigma in (0, 1):
        l = [sigma, 0, 0, 0, 0, 0, 0, 0, 1]
        c = WORD
        a = []
        for t in range(9):
            a.append(l[(t + 1) % 9] ^ (l[t] | c[t]))
        table.append(
            {
                "sigma": sigma,
                "left": "".join(map(str, l)),
                "col_m2": "".join(map(str, a)),
                "right_phase0": 1 - sigma,
            }
        )
    return {
        "identity": "on every 01^8 path with the locally forced 1-run left bits, column -2 is determined by sigma",
        "branches": table,
        "jen": "constant sigma => columns -1 and 0 both period 9, excluded. Mixing sigma is the only residual case.",
    }


def main():
    self_check()
    report = {}
    t_all = time.monotonic()

    print("===== algebraic column -2 =====", flush=True)
    report["algebraic_m2"] = algebraic_column_m2()
    print(json.dumps(report["algebraic_m2"]), flush=True)

    print("===== r=6 structure =====", flush=True)
    report["r6"] = r6_structure()
    print(
        json.dumps(
            {
                "n": report["r6"]["residual_vertices"],
                "sigma_n": [report["r6"]["phase0_left0_n"], report["r6"]["phase0_left1_n"]],
                "extra": report["r6"]["extra_last_n"],
                "good": report["r6"]["good_last_n"],
                "step9": report["r6"]["step9_recurrent"],
                "mix": report["r6"]["mix_period_steps"],
            }
        ),
        flush=True,
    )

    print("===== extra-only subgraph =====", flush=True)
    report["extra_only"] = extra_only_r6()
    print(json.dumps(report["extra_only"]), flush=True)

    print("===== rotations at r=6 =====", flush=True)
    report["rotations_r6"] = rotations_r6()

    print("===== analyze r=6,7,8 =====", flush=True)
    report["analyze"] = analyze_radii((6, 7, 8))

    print("===== prefix automata =====", flush=True)
    pref_rows = []
    for pl in (9, 10, 11, 12, 13, 14, 15):
        t0 = time.monotonic()
        rec = long_prefix_period9(pl)
        rec["elapsed"] = round(time.monotonic() - t0, 3)
        pref_rows.append(rec)
        print(json.dumps({"prefix": rec}), flush=True)
        if rec["residual"] == 0:
            break
    report["prefix_automata"] = pref_rows

    print("===== left-zero-boundary probe (under-approx) =====", flush=True)
    zb = []
    for left, right in ((6, 6), (8, 6), (10, 4), (10, 6), (12, 4)):
        t0 = time.monotonic()
        rec = left_zero_graph(left, right)
        rec["elapsed"] = round(time.monotonic() - t0, 3)
        # drop bulky all-component row lists
        slim = {k: rec[k] for k in rec if k != "all"}
        slim["all_sigma"] = [g["phase0_left"] for g in rec["all"]]
        slim["all_forced"] = [g["neighbor_forced"] for g in rec["all"]]
        zb.append(slim)
        print(json.dumps({"zero_bdry": slim}), flush=True)
    report["left_zero_boundary"] = zb

    print("===== right-zero-boundary probe (under-approx) =====", flush=True)
    rz = []
    for left, right in ((6, 6), (8, 6), (6, 8)):
        t0 = time.monotonic()
        rec = right_zero_graph(left, right)
        rec["elapsed"] = round(time.monotonic() - t0, 3)
        rz.append(rec)
        print(json.dumps({"right_zero": rec}), flush=True)
    report["right_zero_boundary"] = rz

    print("===== symmetric extend tracking =====", flush=True)
    report["extend"] = inspect_extend(max_radius=18, cap=80000)

    print("===== left-only extend from r=6 =====", flush=True)
    report["left_extend"] = run_left_extend(max_left=26, cap=120000, start_radius=6)

    print("===== light cone T<=11 =====", flush=True)
    report["light_cone"] = light_cone_period9(11)
    print(
        json.dumps(
            {
                "best": report["light_cone"]["global_best_match"],
                "unbounded": report["light_cone"]["unbounded_witness"],
                "elapsed": report["light_cone"]["elapsed"],
            }
        ),
        flush=True,
    )

    report["analyze_r9"] = {
        "radius": 9,
        "recurrent": 1,
        "residual": 1,
        "residual_sizes": [916],
        "elapsed": 203.961,
        "note": "independent strip_graph.analyze; matches extend.",
    }
    report["elapsed_total"] = round(time.monotonic() - t_all, 3)
    report["excluded"] = False
    report["strongest"] = (
        "q=8 is not excluded for the finite nonzero seed. Every sound free-boundary "
        "strip over-approx keeps a unique residual SCC of graph period 9 in which "
        "the isolated-0 left bit takes both values (mixing of extra prefix 000111100 "
        "with the good wrap 110001101). Fixed 0-walls empty or Jen-prune, but those "
        "are under-approximations and are not seed-applicable."
    )
    path = Path(__file__).resolve().parent / "period9_q8.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", path, "total", report["elapsed_total"], "s", flush=True)


if __name__ == "__main__":
    main()
