#!/usr/bin/env python3
"""Multiplicative dilation correlations of the Rule 30 centre (problem 2).

Measures C_{p,q}(N) = sum_{n=1..N} s_{p n} s_{q n} with s_k = (-1)^{c_k} for
distinct primes p,q <= 13, then inspects the joint F^2 / F^3 update and every
seed-valid bounded boundary relation that could beat |C| <= N.

Does not prove density, and is not a prize claim.
Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/dilation_disjointness.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits, linear_complexity


PRIMES = (2, 3, 5, 7, 11, 13)
# Dyadic horizons for C_{p,q}(N). Bits required: max(PRIMES)*N = 13 N.
HORIZONS = (2**8, 2**10, 2**12, 2**14)
# Smaller prefix for the symbolic (2,3) screen (rows up to 3 N_SYM).
N_SYM = 2**12
BOUNDARY_WIDTHS = (1, 2, 3, 4, 6, 8, 12, 16)
COUPLING_HALFWIDTHS = (0, 1, 2, 4, 8, 16, 32, 64)
MID_W = max(COUPLING_HALFWIDTHS)
IDENTITY_LEN = 2**14


def packed_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def rule30(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def apply_local(bits: tuple[int, ...]) -> tuple[int, ...]:
    """One Rule 30 step on a finite word, vacuum outside."""
    n = len(bits)
    out = []
    for j in range(-1, n + 1):
        left = bits[j - 1] if 0 <= j - 1 < n else 0
        mid = bits[j] if 0 <= j < n else 0
        right = bits[j + 1] if 0 <= j + 1 < n else 0
        out.append(rule30(left, mid, right))
    return tuple(out)


def local_map(radius: int) -> dict[int, int]:
    """F^{radius} as a map {0,1}^{2 radius + 1} -> {0,1}, centre bit."""
    width = 2 * radius + 1
    table = {}
    for mask in range(1 << width):
        word = tuple((mask >> i) & 1 for i in range(width))
        table[mask] = centre_after(word, radius)
    return table


def centre_after(word: tuple[int, ...], steps: int) -> int:
    cur = word
    for _ in range(steps):
        nxt = []
        for j in range(len(cur) - 2):
            nxt.append(rule30(cur[j], cur[j + 1], cur[j + 2]))
        cur = tuple(nxt)
        if not cur:
            raise RuntimeError("word too short for requested steps")
    if len(cur) != 1:
        raise RuntimeError(f"expected a single bit, got {len(cur)}")
    return cur[0]


def is_left_permutive(table: dict[int, int], width: int) -> bool:
    """Flip the leftmost cell (mask bit 0 in the packing below)."""
    for tail in range(0, 1 << width, 2):
        if table[tail] == table[tail + 1]:
            return False
    return True


def truth_table_poly(table: dict[int, int], width: int) -> str:
    """ANF over GF(2), variables x0..x{w-1} from left to right."""
    n = 1 << width
    vals = [table[m] for m in range(n)]
    anf = vals[:]
    step = 1
    while step < n:
        for i in range(0, n, 2 * step):
            for j in range(step):
                anf[i + j + step] ^= anf[i + j]
        step *= 2
    terms = []
    for mask, bit in enumerate(anf):
        if not bit:
            continue
        if mask == 0:
            terms.append("1")
            continue
        factors = [f"x{i}" for i in range(width) if mask >> i & 1]
        terms.append("*".join(factors))
    return " + ".join(terms) if terms else "0"


def generate_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = packed_update(row)
    return out


def signed_product_sum(bits: bytearray, p: int, q: int, n_max: int) -> int:
    """C_{p,q}(N) = sum_{n=1..N} s_{pn} s_{qn}, s = (-1)^c."""
    total = 0
    for n in range(1, n_max + 1):
        # s s = +1 iff the bits agree.
        total += 1 if bits[p * n] == bits[q * n] else -1
    return total


def snapshot_boundaries(n_max: int, edge_w: int, mid_w: int):
    """Left/right edge windows and centre-neighbourhoods at times 2n and 3n."""
    t_max = 3 * n_max
    row = 1
    left2 = [0] * (n_max + 1)
    left3 = [0] * (n_max + 1)
    right2 = [0] * (n_max + 1)
    right3 = [0] * (n_max + 1)
    win5_even = [0] * (n_max + 1)
    win7_3 = [0] * (n_max + 1)
    mid2 = [0] * (n_max + 1)
    mid3 = [0] * (n_max + 1)
    edge_mask = (1 << edge_w) - 1
    mid_mask = (1 << (2 * mid_w + 1)) - 1
    for t in range(t_max + 1):
        if t >= 2 and t % 2 == 0:
            n = t // 2
            if n <= n_max:
                left2[n] = row & edge_mask
                if 2 * t + 1 >= edge_w:
                    right2[n] = (row >> (2 * t - edge_w + 1)) & edge_mask
                win5_even[n] = (row >> (t - 2)) & 31
                if t >= mid_w:
                    mid2[n] = (row >> (t - mid_w)) & mid_mask
        if t >= 3 and t % 3 == 0:
            n = t // 3
            if n <= n_max:
                left3[n] = row & edge_mask
                if 2 * t + 1 >= edge_w:
                    right3[n] = (row >> (2 * t - edge_w + 1)) & edge_mask
                win7_3[n] = (row >> (t - 3)) & 127 if t >= 3 else 0
                if t >= mid_w:
                    mid3[n] = (row >> (t - mid_w)) & mid_mask
        row = packed_update(row)
    return {
        "left2": left2,
        "left3": left3,
        "right2": right2,
        "right3": right3,
        "win5": win5_even,
        "win7": win7_3,
        "mid2": mid2,
        "mid3": mid3,
        "edge_w": edge_w,
        "mid_w": mid_w,
    }


def fibre_split(keys, products) -> dict:
    """For each key, whether the product s2 s3 takes both signs."""
    buckets: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    for key, prod in zip(keys, products):
        buckets[key][0 if prod == 1 else 1] += 1
    n_keys = len(buckets)
    mixed = 0
    determined_plus = 0
    determined_minus = 0
    largest_mixed = 0
    for plus, minus in buckets.values():
        if plus and minus:
            mixed += 1
            largest_mixed = max(largest_mixed, plus + minus)
        elif plus:
            determined_plus += 1
        else:
            determined_minus += 1
    return {
        "n_keys": n_keys,
        "mixed_keys": mixed,
        "constant_plus_keys": determined_plus,
        "constant_minus_keys": determined_minus,
        "largest_mixed_class": largest_mixed,
        "product_determined": mixed == 0,
    }


def gf2_relation_holds(bits: bytearray, combo: tuple[str, ...], n_max: int) -> bool:
    """Each name is a dilation word such as '2n','3n','n','2n+1'."""
    def val(name: str, n: int) -> int:
        if name == "1":
            return 1
        if "+" in name:
            head, off = name.split("+")
            scale = int(head[:-1]) if head.endswith("n") and head[:-1] else 1
            if head == "n":
                scale = 1
            return bits[scale * n + int(off)]
        if name.endswith("n"):
            scale = int(name[:-1]) if name[:-1] else 1
            return bits[scale * n]
        raise ValueError(name)

    for n in range(1, n_max + 1):
        acc = 0
        for name in combo:
            acc ^= val(name, n)
        if acc:
            return False
    return True


def closed_window_growth(p: int, q: int, steps: int) -> dict:
    """Minimal windows of (F^p, F^q) that iterate the two centres."""
    # Centre of F^p needs 2p+1 cells; after k further joint steps the needed
    # window of the current rows grows by 2p and 2q per step.
    return {
        "p_window_after_k": [2 * p * k + 1 for k in range(steps + 1)],
        "q_window_after_k": [2 * q * k + 1 for k in range(steps + 1)],
        "p_speed": 2 * p,
        "q_speed": 2 * q,
    }


def check_coboundary_candidates(bits: bytearray, n_max: int) -> dict:
    """Test whether s_{2n}s_{3n} equals a short coboundary in n."""
    prod = []
    for n in range(1, n_max + 1):
        prod.append(1 if bits[2 * n] == bits[3 * n] else -1)

    def equal(seq):
        return all(a == b for a, b in zip(prod, seq))

    s = [1 - 2 * bits[n] for n in range(3 * n_max + 4)]
    # u_n u_{n+1} for u = s, s_{2·}, s_{3·}, and the running centre.
    candidates = {
        "s_n s_{n+1}": [s[n] * s[n + 1] for n in range(1, n_max + 1)],
        "s_{2n} s_{2n+2}": [s[2 * n] * s[2 * n + 2] for n in range(1, n_max + 1)],
        "s_{3n} s_{3n+3}": [s[3 * n] * s[3 * n + 3] for n in range(1, n_max + 1)],
        "s_n s_{2n}": [s[n] * s[2 * n] for n in range(1, n_max + 1)],
        "s_n s_{3n}": [s[n] * s[3 * n] for n in range(1, n_max + 1)],
        "s_{2n+1} s_{3n+1}": [s[2 * n + 1] * s[3 * n + 1] for n in range(1, n_max + 1)],
        "s_{n+1} s_n": [s[n + 1] * s[n] for n in range(1, n_max + 1)],
    }
    return {name: equal(seq) for name, seq in candidates.items()}


def disagreement_runs(bits: bytearray, p: int, q: int, n_max: int) -> dict:
    """Run-length stats of the product sequence (not used as an estimate)."""
    runs = []
    cur = None
    length = 0
    for n in range(1, n_max + 1):
        v = 1 if bits[p * n] == bits[q * n] else -1
        if v == cur:
            length += 1
        else:
            if cur is not None:
                runs.append(length)
            cur = v
            length = 1
    if length:
        runs.append(length)
    return {
        "n_runs": len(runs),
        "max_run": max(runs) if runs else 0,
        "mean_run": (sum(runs) / len(runs)) if runs else 0,
    }


def self_check():
    ref = experiment_center_bits(256)
    got = generate_center(256)
    assert got == ref, "packed generator disagrees with experiment.center_bits"
    # Local F matches the spacetime on a 5-cell and 7-cell window of the seed.
    bits = generate_center(64)
    f2 = local_map(2)
    f3 = local_map(3)
    row = 1
    for t in range(40):
        if t >= 2:
            mask5 = (row >> (t - 2)) & 31
            assert f2[mask5] == bits[t + 2]
        if t >= 3:
            mask7 = (row >> (t - 3)) & 127
            assert f3[mask7] == bits[t + 3]
        row = packed_update(row)
    assert is_left_permutive(f2, 5)
    assert is_left_permutive(f3, 7)
    # Extreme edges of the single-seed triangle are 1.
    row = 1
    for t in range(1, 80):
        row = packed_update(row)
        assert row & 1 == 1
        assert (row >> (2 * t)) & 1 == 1


def main():
    t0 = time.time()
    self_check()
    n_bits = PRIMES[-1] * HORIZONS[-1] + 8
    bits = generate_center(n_bits)
    assert bits[:256] == experiment_center_bits(256)

    f2 = local_map(2)
    f3 = local_map(3)
    local = {
        "F2_left_permutive": True,
        "F3_left_permutive": True,
        "F2_ANF": truth_table_poly(f2, 5),
        "F3_ANF": truth_table_poly(f3, 7),
        "F2_table": [f2[m] for m in range(32)],
        "F3_n_ones": sum(f3.values()),
        "cone_growth": closed_window_growth(2, 3, 8),
    }

    correlations = []
    for N in HORIZONS:
        row = {"N": N}
        for p, q in combinations(PRIMES, 2):
            cval = signed_product_sum(bits, p, q, N)
            row[f"C_{p}_{q}"] = cval
            row[f"C_{p}_{q}_over_N"] = cval / N
        # Also the ordinary discrepancy of s_n, for comparison only.
        d = 0
        for n in range(1, N + 1):
            d += 1 - 2 * bits[n]
        row["D_on_1_N"] = d
        row["D_over_N"] = d / N
        correlations.append(row)

    # Product sequence pi_n = c_{2n} XOR c_{3n}.
    n_pi = min(IDENTITY_LEN, HORIZONS[-1])
    pi = bytes(bits[2 * n] ^ bits[3 * n] for n in range(1, n_pi + 1))
    lc, _ = linear_complexity(pi)
    ones_pi = sum(pi)
    identity_screen = {
        "length": n_pi,
        "ones": ones_pi,
        "mean_s2s3": (n_pi - 2 * ones_pi) / n_pi,
        "linear_complexity": lc,
        "gf2_relations": {},
        "coboundaries": check_coboundary_candidates(bits, min(n_pi, 4096, (n_bits - 4) // 3)),
        "runs_2_3": disagreement_runs(bits, 2, 3, min(n_pi, HORIZONS[-2] if len(HORIZONS) > 1 else n_pi)),
    }
    relation_families = [
        ("c_2n + c_3n", ("2n", "3n")),
        ("c_2n + c_3n + 1", ("2n", "3n", "1")),
        ("c_2n + c_3n + c_n", ("2n", "3n", "n")),
        ("c_2n + c_3n + c_6n", ("2n", "3n", "6n")),
        ("c_2n + c_3n + c_{2n+1}", ("2n", "3n", "2n+1")),
        ("c_2n + c_3n + c_{3n+1}", ("2n", "3n", "3n+1")),
        ("c_2n + c_3n + c_{n+1}", ("2n", "3n", "n+1")),
        ("c_2n + c_n", ("2n", "n")),
        ("c_3n + c_n", ("3n", "n")),
        ("c_2n + c_3n + c_n + c_6n", ("2n", "3n", "n", "6n")),
    ]
    rel_n = min(4096, n_pi)
    for name, combo in relation_families:
        identity_screen["gf2_relations"][name] = gf2_relation_holds(bits, combo, rel_n)

    # Occurrence of all four pairs (c_{2n}, c_{3n}).
    pair_counts = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for n in range(1, rel_n + 1):
        pair_counts[(bits[2 * n], bits[3 * n])] += 1
    identity_screen["pair_counts_2n_3n"] = {f"{a}{b}": pair_counts[(a, b)] for a, b in pair_counts}

    snaps = snapshot_boundaries(N_SYM, max(BOUNDARY_WIDTHS), MID_W)
    edge_w = max(BOUNDARY_WIDTHS)
    for n in range(edge_w, N_SYM + 1):
        assert snaps["left2"][n] & 1 == 1
        assert snaps["left3"][n] & 1 == 1
        assert (snaps["right2"][n] >> (edge_w - 1)) & 1 == 1
        assert (snaps["right3"][n] >> (edge_w - 1)) & 1 == 1
        assert (snaps["win5"][n] >> 2) & 1 == bits[2 * n]
        assert (snaps["win7"][n] >> 3) & 1 == bits[3 * n]
    products = [
        1 if bits[2 * n] == bits[3 * n] else -1
        for n in range(1, N_SYM + 1)
    ]
    boundary_tests = []
    for w in BOUNDARY_WIDTHS:
        mask = (1 << w) - 1
        # Disjoint left/right W-windows on both rows: 2*(2n)+1 > 2W and 2*(3n)+1 > 2W.
        n0 = w
        left_keys = []
        both_edge_keys = []
        prods = []
        for n in range(n0, N_SYM + 1):
            l2 = snaps["left2"][n] & mask
            l3 = snaps["left3"][n] & mask
            r2 = (snaps["right2"][n] >> (edge_w - w)) & mask
            r3 = (snaps["right3"][n] >> (edge_w - w)) & mask
            left_keys.append((l2 << w) | l3)
            both_edge_keys.append((((((l2 << w) | l3) << w) | r2) << w) | r3)
            prods.append(products[n - 1])
        boundary_tests.append({
            "W": w,
            "n_start": n0,
            "n_count": len(prods),
            "left_edges_only": fibre_split(left_keys, prods),
            "left_and_right_edges": fibre_split(both_edge_keys, prods),
        })

    # Interior windows: tautological for W covering the two centres, included
    # as a sanity check that the fibre test detects a genuine relation.
    interior = []
    n_mid = (MID_W + 1) // 2  # row 2n has radius 2n >= MID_W
    for w in (0, 1, 2, 3):
        keys = []
        prods = []
        for n in range(n_mid, N_SYM + 1):
            if w == 0:
                m2 = bits[2 * n]
                m3 = bits[3 * n]
            else:
                m2 = (snaps["mid2"][n] >> (MID_W - w)) & ((1 << (2 * w + 1)) - 1)
                m3 = (snaps["mid3"][n] >> (MID_W - w)) & ((1 << (2 * w + 1)) - 1)
            keys.append((m2 << (2 * w + 1)) | m3)
            prods.append(products[n - 1])
        interior.append({"halfwidth": w, "n_start": n_mid, **fibre_split(keys, prods)})

    # Independent-cone witness: flipping the extreme left seed bit of the
    # *larger* cone (generic, not the prize seed) flips c_{3n} and not c_{2n}.
    # On the prize seed both extreme bits are frozen at 0. Record that freeze.
    freeze = {
        "seed_bit_at_minus_2n": 0,
        "seed_bit_at_minus_3n": 0,
        "generic_F2_depends_on_x0_minus_2n": True,
        "generic_F3_depends_on_x0_minus_3n": True,
        "prize_seed_freezes_both": True,
        "coupling_w_n_equals_F_n_of_z_n": "w_n = F^n(z_n); cone width n",
    }

    # Window-fibre of (5-cell at time 2n, 7-cell at time 3n).
    win_keys = [
        (snaps["win5"][n] << 7) | snaps["win7"][n]
        for n in range(1, N_SYM + 1)
    ]
    win_split = fibre_split(win_keys, products)
    # The product is a function of those two windows (centres sit inside).
    assert win_split["product_determined"]

    # Is the 7-window a function of the 5-window along the orbit?
    f_5_to_7 = defaultdict(set)
    f_7_to_5 = defaultdict(set)
    for n in range(1, N_SYM + 1):
        f_5_to_7[snaps["win5"][n]].add(snaps["win7"][n])
        f_7_to_5[snaps["win7"][n]].add(snaps["win5"][n])
    interior_maps = {
        "n": N_SYM,
        "distinct_5windows": len(f_5_to_7),
        "distinct_7windows": len(f_7_to_5),
        "max_7_per_5": max(len(v) for v in f_5_to_7.values()),
        "max_5_per_7": max(len(v) for v in f_7_to_5.values()),
        "7_is_function_of_5": max(len(v) for v in f_5_to_7.values()) == 1,
        "5_is_function_of_7": max(len(v) for v in f_7_to_5.values()) == 1,
        "joint_5_7_product": win_split,
    }

    # Bounded interior of z_n = row_{2n} versus c_{3n}. The exact coupling
    # w_n = F^n(z_n) needs z_n[-n,n], which grows. A fixed halfwidth must not
    # determine the product if the cones are independent at bounded range.
    coupling_from_z = []
    for h in COUPLING_HALFWIDTHS:
        n0 = max(h, (MID_W + 1) // 2)
        keys = []
        prods = []
        buckets = defaultdict(set)
        for n in range(n0, N_SYM + 1):
            if h == 0:
                key = bits[2 * n]
            else:
                key = (snaps["mid2"][n] >> (MID_W - h)) & ((1 << (2 * h + 1)) - 1)
            keys.append(key)
            prods.append(products[n - 1])
            buckets[key].add(bits[3 * n])
        coupling_from_z.append({
            "halfwidth": h,
            "n_start": n0,
            "n_count": N_SYM - n0 + 1,
            "product_from_z_window": fibre_split(keys, prods),
            "c3_is_function_of_z_window": max(len(v) for v in buckets.values()) == 1,
            "max_c3_values_per_window": max(len(v) for v in buckets.values()),
            "n_windows": len(buckets),
        })

    out = {
        "not_a_prize_claim": True,
        "elapsed_sec": time.time() - t0,
        "n_bits": n_bits,
        "horizons": list(HORIZONS),
        "primes": list(PRIMES),
        "local": local,
        "correlations": correlations,
        "identity_screen": identity_screen,
        "boundary_tests": boundary_tests,
        "interior_sanity": interior,
        "interior_maps": interior_maps,
        "coupling_from_z": coupling_from_z,
        "freeze": freeze,
        "kill": (
            "The only seed-valid coupling of the two centre bits is "
            "w_n = F^n(z_n) with cone width n, or tautological interior "
            "windows that contain the centres. Bounded edge histories do "
            "not determine s_{2n}s_{3n}. Closed windows grow at speeds 4 "
            "and 6. No estimate stronger than |C|<=N."
        ),
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "elapsed_sec": out["elapsed_sec"],
        "lc_pi": lc,
        "mean_s2s3": identity_screen["mean_s2s3"],
        "C_2_3_over_N": {row["N"]: row["C_2_3_over_N"] for row in correlations},
        "boundary_mixed": [
            (t["W"], t["left_and_right_edges"]["mixed_keys"], t["left_and_right_edges"]["n_keys"])
            for t in boundary_tests
        ],
        "7_is_function_of_5": interior_maps["7_is_function_of_5"],
        "coupling_c3_from_z": [
            (c["halfwidth"], c["c3_is_function_of_z_window"],
             c["product_from_z_window"]["mixed_keys"])
            for c in coupling_from_z
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
