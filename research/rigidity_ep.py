"""Seed-specific rigidity of time-shifted Rule 30 orbits.

Checks the exact disagreement update of
    e_p(t,j) = x(t+p,j) XOR x(t,j)
on the single-cell seed, the period-7 cyclic counterexample, and a
brute-force census of spatially periodic rows. Does not modify
experiment.py, strip_graph.py, or strip_extend.py. Not a prize claim.

Run: python3 research/rigidity_ep.py
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).with_name("rigidity_ep.json")


def f(z: int) -> int:
    """Packed left-edge encoding of experiment.py: bit k is spatial k-t."""
    return (z << 2) ^ ((z << 1) | z)


def bit_at(row: int, t: int, j: int) -> int:
    """x(t,j) from the packed row whose bit k is cell k-t (LSB = left edge)."""
    k = j + t
    if k < 0:
        return 0
    return (row >> k) & 1


def evolve_packed(steps: int) -> list[int]:
    row = 1
    rows = []
    for _ in range(steps):
        rows.append(row)
        row = f(row)
    return rows


def evolve_columns(steps: int, js: tuple[int, ...] = (-2, -1, 0, 1, 2)):
    """Return dict j -> list of x(t,j) for t < steps, plus lightlike checks."""
    cols = {j: [] for j in js}
    left_edge = []
    right_edge = []
    row = 1
    for t in range(steps):
        for j in js:
            cols[j].append(bit_at(row, t, j))
        left_edge.append(bit_at(row, t, -t))
        right_edge.append(bit_at(row, t, t))
        row = f(row)
    return cols, left_edge, right_edge


def spatial_step(row: dict[int, int]) -> dict[int, int]:
    if not row:
        return {}
    lo, hi = min(row), max(row)
    return {
        j: row.get(j - 1, 0) ^ (row.get(j, 0) | row.get(j + 1, 0))
        for j in range(lo - 1, hi + 2)
    }


def h_from(a0: int, a1: int, b0: int, b1: int) -> int:
    return (a0 | a1) ^ (b0 | b1)


def h_algebra(b0: int, b1: int, e0: int, e1: int) -> int:
    """GF(2) expansion of h, with a = b XOR e."""
    return (e0 ^ e1 ^ (b0 & e1) ^ (b1 & e0) ^ (e0 & e1)) & 1


def verify_update(max_t: int = 80, periods: tuple[int, ...] = (1, 2, 3, 4, 8, 9)) -> dict:
    rows = evolve_packed(max_t + max(periods) + 3)
    mismatches = []
    erasure_checked = 0
    for p in periods:
        for t in range(max_t):
            for j in range(-t - p - 1, t + p + 2):
                e_left = bit_at(rows[t], t, j - 1) ^ bit_at(rows[t + p], t + p, j - 1)
                e0 = bit_at(rows[t], t, j) ^ bit_at(rows[t + p], t + p, j)
                e1 = bit_at(rows[t], t, j + 1) ^ bit_at(rows[t + p], t + p, j + 1)
                b0 = bit_at(rows[t], t, j)
                b1 = bit_at(rows[t], t, j + 1)
                a0 = bit_at(rows[t + p], t + p, j)
                a1 = bit_at(rows[t + p], t + p, j + 1)
                nxt = bit_at(rows[t + 1], t + 1, j) ^ bit_at(rows[t + p + 1], t + p + 1, j)
                h = h_from(a0, a1, b0, b1)
                if h != h_algebra(b0, b1, e0, e1):
                    mismatches.append(("h_algebra", p, t, j))
                if nxt != (e_left ^ h):
                    mismatches.append(("update", p, t, j, nxt, e_left, h))
                if j == 0:
                    # always: e(t+1,0) = e(t,-1) XOR h(t,0)
                    e_m1 = bit_at(rows[t], t, -1) ^ bit_at(rows[t + p], t + p, -1)
                    if nxt != (e_m1 ^ h):
                        mismatches.append(("center_update", p, t, nxt, e_m1, h))
                    if e0 == 0 and nxt == 0:
                        erasure_checked += 1
                        c = bit_at(rows[t], t, 0)
                        e_r = bit_at(rows[t], t, 1) ^ bit_at(rows[t + p], t + p, 1)
                        predicted = ((1 - c) * e_r) & 1
                        if e_m1 != h or e_m1 != predicted:
                            mismatches.append(("erasure", p, t, e_m1, h, predicted, c, e_r))
    return {
        "max_t": max_t,
        "periods": list(periods),
        "mismatches": mismatches[:20],
        "ok": not mismatches,
        "erasure_center_zero_samples": erasure_checked,
    }


def cycle_evolve(word: int, n: int, steps: int) -> list[int]:
    mask = (1 << n) - 1
    row = word & mask
    out = [row]
    for _ in range(steps - 1):
        nxt = 0
        for j in range(n):
            left = (row >> ((j - 1) % n)) & 1
            mid = (row >> j) & 1
            right = (row >> ((j + 1) % n)) & 1
            nxt |= (left ^ (mid | right)) << j
        row = nxt
        out.append(row)
    return out


def period_7_audit() -> dict:
    """Reproduce disagreement.md: spatial period 7, word 0100110, index 0 first 0."""
    n = 7
    # displayed 0100110 with index 0 at first 0: bits [0]=0,1=1,2=0,3=0,4=1,5=1,6=0
    word = 0
    bits = [0, 1, 0, 0, 1, 1, 0]
    for j, b in enumerate(bits):
        word |= b << j
    hist = cycle_evolve(word, n, 8)
    table = []
    for t, row in enumerate(hist):
        f2 = cycle_evolve(row, n, 3)[2]
        e = row ^ f2
        table.append(
            {
                "t": t,
                "b": format(row, f"0{n}b")[::-1],
                "F2": format(f2, f"0{n}b")[::-1],
                "e": format(e, f"0{n}b")[::-1],
                "e0": (e >> 0) & 1,
                "e_m1": (e >> (n - 1)) & 1,
                "center_b": (row >> 0) & 1,
            }
        )
    # temporal period of the orbit of this word
    orbit = []
    seen = {}
    row = word
    while row not in seen:
        seen[row] = len(orbit)
        orbit.append(row)
        row = cycle_evolve(row, n, 2)[1]
    return {
        "word_bits": bits,
        "table": table,
        "orbit_len": len(orbit),
        "e2_center_always_zero": all(item["e0"] == 0 for item in table),
        "e2_col_m1_not_eventually_zero": any(item["e_m1"] == 1 for item in table),
        "e2_col_m1_values": [item["e_m1"] for item in table],
    }


def _cycle_step(row: int, n: int) -> int:
    nxt = 0
    for j in range(n):
        left = (row >> ((j - 1) % n)) & 1
        mid = (row >> j) & 1
        right = (row >> ((j + 1) % n)) & 1
        nxt |= (left ^ (mid | right)) << j
    return nxt


def column_has_period(col: list[int], p: int) -> bool:
    q = len(col)
    return all(col[i] == col[(i + p) % q] for i in range(q))


def cyclic_census(max_n: int = 12, max_steps: int = 512,
                  targets: tuple[int, ...] = (2, 3, 4, 8, 9)) -> dict:
    """Spatially periodic orbits: center period p but column -1 not period p."""
    counts = {p: 0 for p in targets}
    examples = {p: [] for p in targets}
    n_bad_divisibility = 0
    examples_div = []
    for n in range(1, max_n + 1):
        seen = set()
        for word in range(1 << n):
            if word in seen:
                continue
            hist = []
            idx = {}
            row = word
            truncated = False
            while row not in idx:
                idx[row] = len(hist)
                hist.append(row)
                row = _cycle_step(row, n)
                if len(hist) > max_steps:
                    truncated = True
                    break
            for cfg in hist:
                seen.add(cfg)
            if truncated or row not in idx:
                continue
            cycle = hist[idx[row]:]
            q = len(cycle)
            for s in range(n):
                col0 = [(c >> s) & 1 for c in cycle]
                colm1 = [(c >> ((s - 1) % n)) & 1 for c in cycle]
                p0 = min_period(col0)
                pm1 = min_period(colm1)
                rec = {
                    "n": n,
                    "q": q,
                    "origin": s,
                    "p0": p0,
                    "pm1": pm1,
                    "sample": format(cycle[0], f"0{n}b")[::-1],
                }
                if p0 % pm1 != 0:
                    n_bad_divisibility += 1
                    if len(examples_div) < 8:
                        examples_div.append(rec)
                for p in targets:
                    if column_has_period(col0, p) and not column_has_period(colm1, p):
                        counts[p] += 1
                        if len(examples[p]) < 4:
                            examples[p].append(rec)
    return {
        "max_n": max_n,
        "column_pairs_p0_not_multiple_of_pm1": n_bad_divisibility,
        "examples_p0_not_multiple_of_pm1": examples_div,
        "target_hits": {str(p): counts[p] for p in targets},
        "target_examples": {str(p): examples[p] for p in targets},
        "note": (
            "Each cycle is scanned at every spatial origin. A target-p hit "
            "means that column is purely p-periodic while its left neighbour is not."
        ),
    }


def min_period(seq: list[int]) -> int:
    n = len(seq)
    for p in range(1, n + 1):
        if n % p == 0 and all(seq[i] == seq[i % p] for i in range(n)):
            return p
    return n


def last_one(bits: list[int]) -> int | None:
    for i in range(len(bits) - 1, -1, -1):
        if bits[i]:
            return i
    return None


def one_count(bits: list[int]) -> int:
    return sum(bits)


def analyze_runs(e0: list[int], em1: list[int], min_len: int = 8) -> dict:
    best = 0
    best_start = 0
    i = 0
    n = len(e0)
    long_runs = []
    while i < n:
        if e0[i] == 0:
            j = i
            while j < n and e0[j] == 0:
                j += 1
            length = j - i
            if length > best:
                best = length
                best_start = i
            if length >= min_len:
                window_m1 = em1[i:j]
                long_runs.append(
                    {
                        "start": i,
                        "length": length,
                        "col_m1_ones": sum(window_m1),
                        "col_m1_last_one_offset": last_one(window_m1),
                    }
                )
            i = j
        else:
            i += 1
    return {
        "longest_e0_zero_run": best,
        "longest_e0_zero_run_start": best_start,
        "em1_ones_in_longest_e0_zero_run": sum(em1[best_start:best_start + best]) if best else 0,
        "long_runs_ge": min_len,
        "n_long_runs": len(long_runs),
        "long_runs_with_col_m1_ones": sum(1 for r in long_runs if r["col_m1_ones"]),
        "n_long_runs_col_m1_dead": sum(1 for r in long_runs if r["col_m1_ones"] == 0),
        "sample_long_runs": [r for r in long_runs if r["length"] == best][:3],
    }


def seed_scan(times: int = 12000, periods: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)) -> dict:
    horizon = times + max(periods) + 2
    cols, left_edge, right_edge = evolve_columns(horizon, js=(-2, -1, 0, 1, 2))
    edge_ok = all(v == 1 for v in left_edge[:times]) and all(v == 1 for v in right_edge[:times])
    # left front of e_p: e_p(t, -(t+p)) = x(t+p, -(t+p)) = left_edge[t+p]
    out = {"times": times, "left_and_right_lightlike_are_1": edge_ok, "periods": {}}
    for p in periods:
        e0 = [cols[0][t] ^ cols[0][t + p] for t in range(times)]
        em1 = [cols[-1][t] ^ cols[-1][t + p] for t in range(times)]
        em2 = [cols[-2][t] ^ cols[-2][t + p] for t in range(times)]
        e1 = [cols[1][t] ^ cols[1][t + p] for t in range(times)]
        e2 = [cols[2][t] ^ cols[2][t + p] for t in range(times)]
        e_left_front = left_edge[p : p + times]
        erasure_fail = 0
        erasure_ok = 0
        for t in range(times - 1):
            e0n = cols[0][t + 1] ^ cols[0][t + p + 1]
            if e0[t] == 0 and e0n == 0:
                predicted = (1 - cols[0][t]) * e1[t]
                if em1[t] != predicted:
                    erasure_fail += 1
                else:
                    erasure_ok += 1
        rec = {
            "last_e0_one": last_one(e0),
            "last_em1_one": last_one(em1),
            "last_em2_one": last_one(em2),
            "last_e1_one": last_one(e1),
            "last_e2_one": last_one(e2),
            "ones_e0": one_count(e0),
            "ones_em1": one_count(em1),
            "ones_e1": one_count(e1),
            "freq_e0": one_count(e0) / times,
            "freq_em1": one_count(em1) / times,
            "freq_e1": one_count(e1) / times,
            "left_front_always_1": all(e_left_front),
            "erasure_ok": erasure_ok,
            "erasure_fail": erasure_fail,
            "runs": analyze_runs(e0, em1, min_len=6),
        }
        local_agree = local_fail = 0
        for t in range(times - 1):
            e0n = cols[0][t + 1] ^ cols[0][t + p + 1]
            if e0[t] == 0 and e0n == 0:
                local_agree += 1
                if em1[t]:
                    local_fail += 1
        rec["consecutive_center_agreements"] = local_agree
        rec["local_failures_em1_one"] = local_fail
        last0 = rec["last_e0_one"]
        if last0 is None:
            rec["em1_ones_after_last_e0"] = one_count(em1)
            rec["e1_ones_after_last_e0"] = one_count(e1)
        else:
            rec["em1_ones_after_last_e0"] = one_count(em1[last0 + 1 :])
            rec["e1_ones_after_last_e0"] = one_count(e1[last0 + 1 :])
        out["periods"][str(p)] = rec
    return out


def left_diagonal_facts(times: int = 400) -> dict:
    """v(t,k)=x(t,-t+k). Check v(t,0)=1 and v(t,1)=1 for t>=1."""
    rows = evolve_packed(times + 5)
    v0 = [bit_at(rows[t], t, -t) for t in range(times)]
    v1 = [bit_at(rows[t], t, -t + 1) for t in range(1, times)]
    # recurrence v(t+1,k)=v(t,k-2) XOR (v(t,k-1) OR v(t,k))
    rec_fail = 0
    for t in range(times - 1):
        for k in range(0, min(12, 2 * t + 3)):
            def v(tt, kk):
                if kk < 0:
                    return 0
                return bit_at(rows[tt], tt, -tt + kk)
            got = v(t + 1, k)
            pred = v(t, k - 2) ^ (v(t, k - 1) | v(t, k))
            if got != pred:
                rec_fail += 1
    return {
        "v0_all_1": all(v0),
        "v1_all_1_after_t0": all(v1),
        "left_recurrence_failures": rec_fail,
    }


def other_finite_seeds(times: int = 4000, seeds: tuple[int, ...] = (1, 3, 5, 7, 9, 11)) -> dict:
    """Same last-mismatch check for a few other odd finite seeds (packed at t=0)."""
    out = {}
    periods = (2, 3, 4, 8, 9)
    for seed in seeds:
        # packed encoding: bit k is position k from the right edge of THIS seed.
        # For a general odd seed the "center" in prize coordinates is not bit t.
        # Use spatial simulation instead, seed bits as x(0,j) for j>=0, zeros on the left.
        row = {j: (seed >> j) & 1 for j in range(seed.bit_length()) if (seed >> j) & 1}
        hist = []
        cur = dict(row)
        for t in range(times + 12):
            hist.append(dict(cur))
            cur = spatial_step(cur)
        rec = {}
        for p in periods:
            e0 = [hist[t].get(0, 0) ^ hist[t + p].get(0, 0) for t in range(times)]
            em1 = [hist[t].get(-1, 0) ^ hist[t + p].get(-1, 0) for t in range(times)]
            rec[str(p)] = {
                "last_e0_one": last_one(e0),
                "last_em1_one": last_one(em1),
                "ones_e0": one_count(e0),
                "ones_em1": one_count(em1),
            }
        out[str(seed)] = rec
    return out


def packed_matches_spatial(steps: int = 40) -> bool:
    row = {0: 1}
    packed = 1
    for t in range(steps):
        for j in range(-t, t + 1):
            if bit_at(packed, t, j) != row.get(j, 0):
                return False
        packed = f(packed)
        row = spatial_step(row)
    return True


def main() -> None:
    update = verify_update()
    assert update["ok"], update["mismatches"]
    assert packed_matches_spatial()
    period7 = period_7_audit()
    assert period7["e2_center_always_zero"]
    assert period7["e2_col_m1_not_eventually_zero"]
    left_diag = left_diagonal_facts()
    assert left_diag["v0_all_1"]
    assert left_diag["v1_all_1_after_t0"]
    assert left_diag["left_recurrence_failures"] == 0
    seed = seed_scan(times=16000)
    assert seed["left_and_right_lightlike_are_1"]
    for rec in seed["periods"].values():
        assert rec["left_front_always_1"]
        assert rec["erasure_fail"] == 0
    report = {
        "update": update,
        "period7": period7,
        "cyclic_census": cyclic_census(max_n=14),
        "left_diagonal": left_diag,
        "seed": seed,
        "other_seeds": other_finite_seeds(times=2500),
    }
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps({
        "update_ok": report["update"]["ok"],
        "period7_e0": report["period7"]["e2_center_always_zero"],
        "period7_em1": report["period7"]["e2_col_m1_values"][:8],
        "cyclic_target_hits": report["cyclic_census"]["target_hits"],
        "cyclic_target_examples": report["cyclic_census"]["target_examples"],
        "cyclic_p0_not_multiple_of_pm1": report["cyclic_census"]["column_pairs_p0_not_multiple_of_pm1"],
        "seed_last": {
            p: {
                "last_e0": rec["last_e0_one"],
                "last_em1": rec["last_em1_one"],
                "em1_after": rec["em1_ones_after_last_e0"],
                "freq_e0": round(rec["freq_e0"], 4),
                "freq_em1": round(rec["freq_em1"], 4),
                "longest_e0_zero": rec["runs"]["longest_e0_zero_run"],
                "em1_ones_in_longest": rec["runs"]["em1_ones_in_longest_e0_zero_run"],
                "long_runs_m1_alive": rec["runs"]["long_runs_with_col_m1_ones"],
                "n_long_runs": rec["runs"]["n_long_runs"],
                "local_agree": rec["consecutive_center_agreements"],
                "local_fail": rec["local_failures_em1_one"],
            }
            for p, rec in report["seed"]["periods"].items()
        },
        "wrote": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
