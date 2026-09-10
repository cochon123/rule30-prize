"""Certificates for primitive periodic center words (period 3..9).

Does not modify strip_graph.py / strip_extend.py.
"""
from __future__ import annotations

import json
import sys
import time
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_extend import extend, initial
from strip_graph import analyze, components, graph, self_check


def check_algebraic_lemmas():
    """Hand-checkable identities used in research/small_periods.md."""
    # Isolated-one reset: for 0^q 1, r_0=1 forces next-period r_0=0.
    # Local: during the 0-run, r_{t+1}=r_t OR e_t, so r stays 1; at the
    # unique 1, next r = NOT (r OR e) = 0.
    for q in range(2, 9):
        word = "0" * q + "1"
        info = period_map_right_window(word, extra=3)
        assert info["phase0_r_from_1"] == [0], (word, info["phase0_r_from_1"])
        # Possible r-words are exactly the nondecreasing 0^a 1^b.
        p = q + 1
        expected = {("0" * a + "1" * (p - a)) for a in range(p + 1)}
        assert set(info["possible_r_words"]) == expected, (word, info["possible_r_words"])
    # 001 left words and the unstable 101.
    info = period_map_right_window("001", extra=3)
    assert set(info["possible_l_words"]) == {"001", "011", "101"}
    assert info["phase0_r_from_1"] == [0]
    # Isolated-zero 011: only the isolated-0 left bit is free.
    info = period_map_right_window("011", extra=3)
    assert info["l_bits_forced"] == {1: 0, 2: 1}
    assert set(info["possible_l_words"]) == {"001", "101"}
    # 0011 does NOT have the isolated-one reset: extra 1 can restore r_0.
    info = period_map_right_window("0011", extra=3)
    assert set(info["phase0_r_from_1"]) == {0, 1}


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


def forced_left_on_ones(word: str) -> dict:
    p = len(word)
    c = [int(b) for b in word]
    forced = []
    free = []
    for t in range(p):
        nxt = c[(t + 1) % p]
        if c[t] == 1:
            forced.append({"phase": t, "left": 1 - nxt})
        else:
            free.append(t)
            forced.append({"phase": t, "left": None, "formula": f"{nxt} XOR r"})
    # 0-runs, including wrap-around
    runs = []
    start = 0
    while start < p:
        bit = c[start]
        k = 1
        while k < p and c[(start + k) % p] == bit:
            k += 1
        runs.append((start, bit, k))
        start += k
        if start >= p:
            break
    if len(runs) >= 2 and runs[0][1] == runs[-1][1] and runs[0][0] == 0:
        t1, bit, k1 = runs[-1]
        _, _, k0 = runs[0]
        runs[0] = (t1, bit, k0 + k1)
        runs.pop()
    zero_runs = []
    for st, bit, k in runs:
        if bit != 0:
            continue
        length = p if k >= p else k
        if length < 2:
            continue
        zero_runs.append(
            {
                "start_phase": st % p,
                "length": length,
                "equal_nondecreasing_phases": [(st + i) % p for i in range(length - 1)],
            }
        )
    pred = [(1 - c[(t + 1) % p]) if c[t] else None for t in range(p)]
    return {
        "forced_left_on_ones": forced,
        "free_zero_phases": free,
        "zero_runs_k_ge_2": zero_runs,
        "predicted_left_on_ones": pred,
    }


def period_map_right_window(word: str, extra: int = 3) -> dict:
    """Possible left/right neighbor words over one period, free far-right bit.

    Window columns are center (imposed) plus `extra` cells to the right.
    """
    p = len(word)
    c = [int(b) for b in word]
    width = extra
    two_r = []
    two_l = []
    d0_pairs = set()

    def dfs(t, bits, r_seq, l_seq):
        if t == 2 * p:
            two_r.append(tuple(r_seq))
            two_l.append(tuple(l_seq))
            d0_pairs.add((r_seq[0], r_seq[p]))
            return
        r = bits[0]
        l = c[(t + 1) % p] ^ (c[t % p] | r)
        for far in range(2):
            extended = bits + [far]
            nxt = []
            for j in range(width):
                left = c[t % p] if j == 0 else bits[j - 1]
                nxt.append(left ^ (bits[j] | extended[j + 1]))
            dfs(t + 1, nxt, r_seq + [r], l_seq + [l])

    for s0 in range(1 << width):
        bits = [(s0 >> j) & 1 for j in range(width)]
        dfs(0, bits, [], [])

    one_r = {seq[:p] for seq in two_r}
    one_l = {seq[:p] for seq in two_l}
    r_phase = {j: {seq[j] for seq in one_r} for j in range(p)}
    l_phase = {j: {seq[j] for seq in one_l} for j in range(p)}
    r_forced = {j: next(iter(v)) for j, v in r_phase.items() if len(v) == 1}
    l_forced = {j: next(iter(v)) for j, v in l_phase.items() if len(v) == 1}
    d1_next = sorted({b for a, b in d0_pairs if a == 1})
    d0_next = sorted({b for a, b in d0_pairs if a == 0})
    return {
        "extra_width": extra,
        "n_r_words": len(one_r),
        "n_l_words": len(one_l),
        "r_bits_forced": r_forced,
        "l_bits_forced": l_forced,
        "phase0_r_pairs": sorted(d0_pairs),
        "phase0_r_from_1": d1_next,
        "phase0_r_from_0": d0_next,
        "left_forced_periodic": len(one_l) == 1,
        "right_forced_periodic": len(one_r) == 1,
        "possible_l_words": ["".join(map(str, s)) for s in sorted(one_l)],
        "possible_r_words": ["".join(map(str, s)) for s in sorted(one_r)],
    }


def analyze_any_pair(radius: int, word: list[int]) -> dict:
    out, rev, rows = graph(radius, word)
    labels, groups = components(out, rev)
    recurrent = []
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
        assert period > 0
        fixed = []
        width = 2 * radius + 1
        for j in range(width):
            by_class = {}
            for v in group:
                cls = depth[v] % period
                bit = ((v % rows) >> j) & 1
                if cls in by_class and by_class[cls] != bit:
                    break
                by_class[cls] = bit
            else:
                fixed.append(j - radius)
        assert 0 in fixed
        adjacent_pairs = [
            (fixed[i], fixed[i + 1])
            for i in range(len(fixed) - 1)
            if fixed[i + 1] == fixed[i] + 1
        ]
        recurrent.append(
            {
                "vertices": len(group),
                "graph_period": period,
                "periodic_columns": fixed,
                "neighbor_forced_periodic": -1 in fixed or 1 in fixed,
                "any_adjacent_pair_periodic": bool(adjacent_pairs),
                "adjacent_periodic_pairs": adjacent_pairs,
            }
        )
    residual_neighbor = [g for g in recurrent if not g["neighbor_forced_periodic"]]
    residual_any = [g for g in recurrent if not g["any_adjacent_pair_periodic"]]
    return {
        "radius": radius,
        "center_word": "".join(map(str, word)),
        "recurrent_components": len(recurrent),
        "residual_neighbor": len(residual_neighbor),
        "residual_any_adjacent": len(residual_any),
        "residual_neighbor_sizes": sorted(
            [g["vertices"] for g in residual_neighbor], reverse=True
        ),
        "residual_any_sizes": sorted([g["vertices"] for g in residual_any], reverse=True),
        "excluded_neighbor": len(residual_neighbor) == 0,
        "excluded_any_adjacent": len(residual_any) == 0,
        "components": recurrent,
    }


def extend_scan(word: str, max_radius: int = 22, cap: int = 30000) -> dict:
    start = time.monotonic()
    states, out, stats = initial(list(map(int, word)))
    rows = []
    radius = 1
    stop = "radius"
    while True:
        rows.append(
            {
                "radius": radius,
                "states": len(states),
                "edges": sum(map(len, out)),
                "n_components": len(stats),
            }
        )
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
        "word": word,
        "stop": stop,
        "last_radius": rows[-1]["radius"],
        "last_states": rows[-1]["states"],
        "scan": rows,
        "elapsed": round(time.monotonic() - start, 3),
    }


def step_light_cone(row: int, t: int) -> int:
    """row bit k = x(t, k-t). Returns the time-(t+1) row of width 2t+3."""
    # next[k'] = old[k'-2] XOR (old[k'-1] OR old[k'])
    return ((row << 2) ^ ((row << 1) | row)) & ((1 << (2 * t + 3)) - 1)


def light_cone_search(word: str, tmax: int = 11) -> dict:
    p = len(word)
    rotations = [[int(b) for b in (word[i:] + word[:i])] for i in range(p)]
    per_T = []
    global_best = 0
    for T in range(0, tmax + 1):
        width = 2 * T + 1
        n_int = max(width - 2, 0)
        n_rows = 1 << n_int if T > 0 else 1
        max_match = 0
        for interior in range(n_rows):
            row = 1 if T == 0 else (1 | (interior << 1) | (1 << (2 * T)))
            center0 = (row >> T) & 1
            for rot in rotations:
                if center0 != rot[0]:
                    continue
                cur = row
                tcur = T
                steps = 1
                limit = 8 * p + 2 * T + 24
                while True:
                    cur = step_light_cone(cur, tcur)
                    tcur += 1
                    if ((cur >> tcur) & 1) != rot[steps % p]:
                        break
                    steps += 1
                    if steps > limit:
                        steps = 10**9
                        break
                if steps > max_match:
                    max_match = steps
                if steps > global_best:
                    global_best = steps
        per_T.append({"T": T, "max_match": max_match, "width": width})
    return {
        "word": word,
        "tmax": tmax,
        "per_T": per_T,
        "global_best_match": global_best,
        "unbounded_witness": global_best >= 10**9,
    }


def algebraic_notes(word: str) -> dict:
    info = forced_left_on_ones(word)
    maps = period_map_right_window(word, extra=3)
    return {**info, "window3": maps}


def main():
    self_check()
    check_algebraic_lemmas()
    # Cross-check analyze_any_pair against stock analyze on a known exclusion.
    stock = analyze(6, [0] + [1] * 7)
    ours = analyze_any_pair(6, [0] + [1] * 7)
    assert stock["components_without_forced_periodic_neighbor"] == 0
    assert ours["excluded_neighbor"] is True

    out_dir = Path(__file__).resolve().parent
    focus = []
    for n in range(3, 8):
        focus.extend(primitive_necklaces(n))
    focus.append("011111111")

    algebraic = {w: algebraic_notes(w) for w in focus}
    for w, info in algebraic.items():
        w3 = info["window3"]
        print(
            json.dumps(
                {
                    "alg": w,
                    "l_forced": w3["l_bits_forced"],
                    "r_forced": w3["r_bits_forced"],
                    "n_l": w3["n_l_words"],
                    "n_r": w3["n_r_words"],
                    "d_from_1": w3["phase0_r_from_1"],
                    "left_periodic": w3["left_forced_periodic"],
                }
            ),
            flush=True,
        )

    radius_table = []
    for w in focus:
        radii = (6, 7)
        if w == "011111111":
            radii = (6, 7, 8)
        for radius in radii:
            t0 = time.monotonic()
            a = analyze_any_pair(radius, list(map(int, w)))
            a["elapsed"] = round(time.monotonic() - t0, 3)
            # drop bulky component list from json except flags
            slim = {k: a[k] for k in a if k != "components"}
            slim["n_with_adjacent_pair"] = sum(
                1 for g in a["components"] if g["any_adjacent_pair_periodic"]
            )
            radius_table.append(slim)
            print(
                json.dumps(
                    {
                        "word": w,
                        "radius": radius,
                        "excl_nb": slim["excluded_neighbor"],
                        "excl_any": slim["excluded_any_adjacent"],
                        "res_nb": slim["residual_neighbor_sizes"],
                        "res_any": slim["residual_any_sizes"],
                        "sec": slim["elapsed"],
                    }
                ),
                flush=True,
            )

    # Radius 8 for period 3-4 survivors
    need8 = []
    by7 = {r["center_word"]: r for r in radius_table if r["radius"] == 7}
    for w in primitive_necklaces(3) + primitive_necklaces(4) + primitive_necklaces(5):
        row = by7.get(w)
        if row and not row["excluded_any_adjacent"]:
            need8.append(w)
    for w in need8:
        t0 = time.monotonic()
        a = analyze_any_pair(8, list(map(int, w)))
        a["elapsed"] = round(time.monotonic() - t0, 3)
        slim = {k: a[k] for k in a if k != "components"}
        radius_table.append(slim)
        print(
            json.dumps(
                {
                    "word": w,
                    "radius": 8,
                    "excl_nb": slim["excluded_neighbor"],
                    "excl_any": slim["excluded_any_adjacent"],
                    "res_nb": slim["residual_neighbor_sizes"],
                    "sec": slim["elapsed"],
                }
            ),
            flush=True,
        )

    extend_words = ["001", "011", "0001", "0011", "0111", "011111111"]
    extend_words += primitive_necklaces(5)
    extend_results = []
    for w in extend_words:
        rows = [r for r in radius_table if r["center_word"] == w]
        if rows and any(r["excluded_neighbor"] for r in rows):
            continue
        rec = extend_scan(w, max_radius=22, cap=35000)
        extend_results.append(rec)
        print(
            json.dumps(
                {
                    "extend": w,
                    "stop": rec["stop"],
                    "last_r": rec["last_radius"],
                    "states": rec["last_states"],
                    "sec": rec["elapsed"],
                }
            ),
            flush=True,
        )

    cone = []
    for w in ["001", "011", "0001", "0011", "0111"]:
        t0 = time.monotonic()
        rec = light_cone_search(w, tmax=11)
        rec["elapsed"] = round(time.monotonic() - t0, 3)
        cone.append(rec)
        print(
            json.dumps(
                {
                    "cone": w,
                    "best": rec["global_best_match"],
                    "unbounded": rec["unbounded_witness"],
                    "sec": rec["elapsed"],
                }
            ),
            flush=True,
        )

    payload = {
        "algebraic": algebraic,
        "radius_table": radius_table,
        "extend": extend_results,
        "light_cone": cone,
        "period8_known_empty": ["00000001", "00000011", "01111111"],
        "necklaces": {str(n): primitive_necklaces(n) for n in range(3, 10)},
    }
    path = out_dir / "small_period_cert.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main()
