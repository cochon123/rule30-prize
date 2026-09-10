#!/usr/bin/env python3
"""Left-permutivity kills interior coalescence for the Rule 30 centre.

Two seeds that agree on [-W, W] and differ first at -W-1 have identical
centre bits c_0..c_W and opposite c_{W+1}. Coupling-from-the-past /
coalescence inside the light cone therefore never occurs. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/coalescence.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


def f(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def evolve_from_seed(seed: dict[int, int], t_max: int) -> list[int]:
    """Centre bits c_0..c_{t_max} from a finitely supported seed."""
    row = dict(seed)
    out = []
    for t in range(t_max + 1):
        out.append(row.get(0, 0))
        nxt = {}
        lo = min(row) - 1
        hi = max(row) + 1
        for j in range(lo, hi + 1):
            nxt[j] = f(row.get(j - 1, 0), row.get(j, 0), row.get(j + 1, 0))
        row = nxt
    return out


def packed_prize_centre(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def first_disagreement(a: list[int], b: list[int]) -> int | None:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return None


def check_left_flip(w_max: int) -> dict:
    """Flip site -W-1 of the prize seed; centre must first disagree at time W+1."""
    rows = []
    for w in range(0, w_max + 1):
        prize = {0: 1}
        flipped = {0: 1, -w - 1: 1}
        t_max = w + 4
        a = evolve_from_seed(prize, t_max)
        b = evolve_from_seed(flipped, t_max)
        d = first_disagreement(a, b)
        rows.append({
            "W": w,
            "first_disagreement": d,
            "predicted": w + 1,
            "ok": d == w + 1,
            "agree_through_W": a[: w + 1] == b[: w + 1],
        })
    return {
        "w_max": w_max,
        "all_ok": all(r["ok"] and r["agree_through_W"] for r in rows),
        "rows": rows,
    }


def check_right_flip(w_max: int) -> dict:
    """Flip site +W+1. Light cone reaches the centre at time W+1; may or may not flip."""
    rows = []
    n_flip = 0
    for w in range(0, w_max + 1):
        prize = {0: 1}
        flipped = {0: 1, w + 1: 1}
        t_max = w + 4
        a = evolve_from_seed(prize, t_max)
        b = evolve_from_seed(flipped, t_max)
        d = first_disagreement(a, b)
        if d is not None:
            n_flip += 1
        rows.append({
            "W": w,
            "first_disagreement": d,
            "cone_time": w + 1,
            "not_before_cone": d is None or d >= w + 1,
        })
    return {
        "w_max": w_max,
        "never_before_cone": all(r["not_before_cone"] for r in rows),
        "times_centre_flipped": n_flip,
        "rows": rows,
    }


def main() -> None:
    t0 = time.perf_counter()
    prize = packed_prize_centre(64)
    ref = experiment_center_bits(64)
    assert list(prize) == list(ref), "prize centre mismatches experiment.center_bits"
    direct = evolve_from_seed({0: 1}, 63)
    assert direct == list(prize), "direct evolution mismatches packed centre"

    left = check_left_flip(48)
    right = check_right_flip(48)
    elapsed = time.perf_counter() - t0
    kill = (
        "Left-permutivity: a disagreement at -W-1 always flips c_{W+1} and "
        "never any earlier centre bit. Seeds agreeing on [-W,W] are coupled "
        "only up to the cone; they do not coalesce inside it. Route killed."
    )
    payload = {
        "attack": "coalescence / coupling from the past",
        "prize_prefix_ok": True,
        "left_flip": {"w_max": left["w_max"], "all_ok": left["all_ok"],
                      "sample": left["rows"][:5] + left["rows"][-3:]},
        "right_flip": {
            "w_max": right["w_max"],
            "never_before_cone": right["never_before_cone"],
            "times_centre_flipped": right["times_centre_flipped"],
        },
        "kill": True,
        "kill_reason": kill,
        "elapsed_sec": elapsed,
        "not_a_prize_claim": True,
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in
                      ("prize_prefix_ok", "kill", "elapsed_sec")}, indent=2))
    print("left.all_ok", left["all_ok"], "right.never_before_cone",
          right["never_before_cone"])
    if not left["all_ok"]:
        raise SystemExit("left-permutivity check failed")
    if not right["never_before_cone"]:
        raise SystemExit("right perturbation travelled faster than the cone")


if __name__ == "__main__":
    main()
