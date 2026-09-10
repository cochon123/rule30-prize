#!/usr/bin/env python3
"""Vanishing-noise susceptibility of the Rule 30 centre (Astra ideas7 item 1).

Exact first derivative B_N'(0) by single flipped updates, plus a noisy
relaxation screen. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/noise_susceptibility.py
"""
from __future__ import annotations

import json
import math
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


def packed_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def discrepancy(bits, N: int) -> int:
    d = 0
    for t in range(N):
        d += 1 if bits[t] else -1
    return d


def generate_triangle_rows(N: int) -> list[int]:
    """rows[t] is the packed left-aligned word of length 2t+1, bit 0 = x(t,-t)."""
    rows = [1]
    row = 1
    for t in range(N - 1):
        row = packed_update(row)
        rows.append(row)
    return rows


def center_from_row(row: int, t: int) -> int:
    return (row >> t) & 1


def D_after_flip(N: int, t_flip: int, j_local: int, rows: list[int]) -> int:
    """Flip bit j_local of row t_flip (j_local=0 is left edge x(t,-t)) and
    evolve packed from there. Return D_N of the new centre sequence.
    """
    d = 0
    for t in range(t_flip):
        d += 1 if center_from_row(rows[t], t) else -1
    row = rows[t_flip] ^ (1 << j_local)
    d += 1 if center_from_row(row, t_flip) else -1
    for t in range(t_flip, N - 1):
        row = packed_update(row)
        d += 1 if center_from_row(row, t + 1) else -1
    return d


def exact_derivative(N: int) -> dict:
    rows = generate_triangle_rows(N)
    bits = [center_from_row(rows[t], t) for t in range(N)]
    D0 = discrepancy(bits, N)
    total = 0
    n_sites = 0
    max_abs = 0
    # Update sites: every produced cell with t>=1, plus optionally the seed
    # as a non-update. Astra: "v ranges over update sites in the relevant cone".
    for t in range(1, N):
        width = 2 * t + 1
        for j in range(width):
            Dv = D_after_flip(N, t, j, rows)
            delta = Dv - D0
            total += delta
            n_sites += 1
            if abs(delta) > max_abs:
                max_abs = abs(delta)
    Bp = total / N
    thresh = 8 * (N ** 1.5)
    return {
        "N": N,
        "D_N": D0,
        "n_sites": n_sites,
        "sum_delta": total,
        "B_prime_0": Bp,
        "abs_B_prime": abs(Bp),
        "threshold_8_N_3_2": thresh,
        "exceeds": abs(Bp) > thresh,
        "max_abs_delta": max_abs,
        "mean_abs_delta_times_sites_over_N": abs(total) / N,
    }


def noisy_trajectory(N: int, eps: float, rng: random.Random) -> list[int]:
    """Single-cell seed, flip each produced cell independently with prob eps.

    Geometric skipping samples the same independent Bernoulli(eps) law
    with O(eps * width) RNG calls per row instead of width.
    """
    row = 1
    centres = [1]
    log1p = math.log(1.0 - eps) if 0 < eps < 1 else None
    for t in range(N - 1):
        row = packed_update(row)
        width = 2 * (t + 1) + 1
        if eps <= 0:
            centres.append((row >> (t + 1)) & 1)
            continue
        j = 0
        while j < width:
            u = rng.random()
            if u <= 0:
                u = 1e-16
            skip = int(math.floor(math.log(u) / log1p))
            j += skip
            if j >= width:
                break
            row ^= 1 << j
            j += 1
        centres.append((row >> (t + 1)) & 1)
    return centres


def noisy_screen(N: int, eps: float, n_traj: int, seed: int) -> dict:
    rng = random.Random(seed)
    mean = [0.0] * N
    for i in range(n_traj):
        c = noisy_trajectory(N, eps, rng)
        for t, b in enumerate(c):
            mean[t] += 1.0 if b else -1.0
        if (i + 1) % 2048 == 0:
            print(f"  eps={eps} traj {i+1}/{n_traj}", flush=True)
    for t in range(N):
        mean[t] /= n_traj
    # Envelope 2 exp(-t sqrt(eps)/4)
    se = math.sqrt(eps)
    violations = []
    for t in range(N):
        env = 2.0 * math.exp(-t * se / 4.0)
        if abs(mean[t]) > env + 4.0 / math.sqrt(n_traj):  # 4σ slack for Monte Carlo
            violations.append({"t": t, "mean": mean[t], "envelope": env})
            if len(violations) > 12:
                break
    late = mean[N // 2 :]
    return {
        "eps": eps,
        "N": N,
        "n_traj": n_traj,
        "late_mean_abs": sum(abs(x) for x in late) / len(late),
        "n_envelope_violations_listed": len(violations),
        "violations_head": violations[:8],
        "contradicts_envelope": len(violations) > 0,
        "mean_abs_t_64": abs(mean[min(63, N - 1)]),
        "mean_abs_t_256": abs(mean[min(255, N - 1)]),
        "mean_abs_last": abs(mean[-1]),
    }


def main():
    t0 = time.time()
    bits = experiment_center_bits(257)
    rows = generate_triangle_rows(257)
    assert [center_from_row(rows[t], t) for t in range(257)] == list(bits)

    derivs = []
    for N in (64, 128, 256):
        rec = exact_derivative(N)
        derivs.append(rec)
        print(
            f"N={N} B'={rec['B_prime_0']:.4f} thresh={rec['threshold_8_N_3_2']:.1f} "
            f"exceeds={rec['exceeds']} sites={rec['n_sites']}",
            flush=True,
        )

    kill_deriv = any(r["exceeds"] for r in derivs)
    # Unsigned O(eps N^2) for |B(eps)-B(0)| would mean |B'| = O(N^2).
    # Compare |B'| to N^2 / 4 as a witness of that coarser bound.
    recovers_unsigned = all(abs(r["B_prime_0"]) > (r["N"] ** 2) / 32 for r in derivs)

    noisy = []
    for eps in (2 ** -6, 2 ** -8, 2 ** -10):
        rec = noisy_screen(512, eps, 8192, seed=int(1 / eps))
        noisy.append(rec)
        print(
            f"eps={eps} late_mean_abs={rec['late_mean_abs']:.4f} "
            f"viol={rec['contradicts_envelope']}",
            flush=True,
        )
    kill_relax = any(r["contradicts_envelope"] for r in noisy)

    payload = {
        "not_a_prize_claim": True,
        "self_check_centres": True,
        "derivatives": derivs,
        "noisy": noisy,
        "kill": {
            "derivative_exceeds_8_N_3_2": kill_deriv,
            "relaxation_contradicts_envelope": kill_relax,
            "unsigned_quadratic_fault_scale": recovers_unsigned,
            "fired": kill_deriv or kill_relax or recovers_unsigned,
            "text": "",
        },
        "elapsed_sec": time.time() - t0,
    }
    reasons = []
    if kill_deriv:
        reasons.append("|B_N'(0)| > 8 N^{3/2} at a tested N")
    if kill_relax:
        reasons.append("noisy means violate 2 exp(-t sqrt(eps)/4) beyond MC slack")
    if recovers_unsigned:
        reasons.append("first derivative is on the unsigned O(N^2) fault scale")
    if not reasons:
        reasons.append("screen did not fire; higher-order faults still required")
    payload["kill"]["text"] = "; ".join(reasons) + ". Not a prize claim."
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "B_prime": {r["N"]: r["B_prime_0"] for r in derivs},
        "kill": payload["kill"]["fired"],
        "text": payload["kill"]["text"],
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
