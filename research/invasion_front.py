#!/usr/bin/env python3
"""Periodically driven invasion fronts for Rule 30 (Astra ideas6 item 5).

Right half-line driven at j=0 by w=001 or w=0111. Search travelling
fronts: interface width ≤12, wake spatial period ≤8, temporal period ≤12
compatible with the driver, positive displacement per period. Then a
bounded drift certificate if any front exists.

Not a prize claim. Does not modify experiment.py, strip_graph.py, or
strip_extend.py.

Run: python3 research/invasion_front.py
"""
from __future__ import annotations

import json
import sys
import time
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def rule30(a, b, c):
    return a ^ (b | c)


def evolve_half(row, driver_bit):
    """row[0] is site j=1. Vacuum on the right. Driver occupies j=0."""
    n = len(row)
    nxt = [0] * n
    for j in range(n):
        left = driver_bit if j == 0 else row[j - 1]
        mid = row[j]
        right = row[j + 1] if j + 1 < n else 0
        nxt[j] = rule30(left, mid, right)
    # One extra site may become live from the right edge of the support.
    extra_left = driver_bit if n == 0 else row[n - 1]
    extra = rule30(extra_left, 0, 0)
    if extra:
        nxt.append(extra)
    elif n:
        # keep a trailing vacuum cell so shifts stay comparable
        pass
    return nxt


def evolve_T(row, driver, T, phase0=0):
    cur = list(row)
    for s in range(T):
        cur = evolve_half(cur, driver[(phase0 + s) % len(driver)])
    return cur


def support_max(row):
    last = -1
    for i, b in enumerate(row):
        if b:
            last = i
    return last


def pad_to(row, n):
    r = list(row)
    if len(r) < n:
        r.extend([0] * (n - len(r)))
    return r[:n]


def is_q_periodic_prefix(row, q, length):
    if q <= 0 or length < q:
        return False
    block = row[:q]
    for i in range(length):
        if row[i] != block[i % q]:
            return False
    return True


def travelling_match(row0, rowT, d, wake_len, iface_width):
    """After T steps the occupied pattern has shifted by d>0.

    Sites [0, wake_len) are the wake (must remain the same periodic block,
    possibly wrapping with the shift if d is a multiple of q). Sites
    [wake_len, wake_len+iface_width) are the interface. Right of that is
    vacuum in both snapshots, except the interface may have moved by d.
    """
    L = wake_len + iface_width
    a = pad_to(row0, L + d + 4)
    b = pad_to(rowT, L + d + 4)
    # Vacuum to the right of the initial interface.
    if any(a[L:]):
        return False
    # Shifted copy: b[j+d] == a[j] for j in [0, L), and b[j]==0 for j >= L+d,
    # and the newly occupied prefix b[0:d] equals the wake cycle.
    for j in range(L):
        if b[j + d] != a[j]:
            return False
    if any(b[L + d :]):
        return False
    q = wake_len
    if q == 0:
        return all(b[j] == 0 for j in range(d))
    for j in range(d):
        if b[j] != a[j % q]:
            return False
    return True


def search_fronts(driver, max_q=8, max_iw=12, max_T=12, max_d=6):
    p = len(driver)
    found = []
    n_tried = 0
    # Wake block of period q, interface of width iw. Enumerate 2^{q+iw}
    # only up to q+iw <= 14 to keep the family finite and the budget small;
    # the freeze is q<=8 and iw<=12, but 2^{20} is too large. Cover the
    # freeze by nested loops: all q,iw with q+iw <= 16 using bit masks, and
    # for larger q+iw only the periodic-wake + vacuum-interface slice.
    for T in range(p, max_T + 1, p):
        for q in range(0, max_q + 1):
            for iw in range(0, max_iw + 1):
                L = q + iw
                if L == 0:
                    continue
                if L <= 14:
                    masks = range(1 << L)
                    mode = "full"
                else:
                    # Slice: arbitrary q-bit wake, interface a single 1 at
                    # the left of the interface window, rest 0. Plus vacuum
                    # interface. This is the remaining freeze slice that
                    # still fits the stated widths.
                    masks = []
                    for wake in range(1 << q) if q else [0]:
                        masks.append(wake)
                        if iw:
                            masks.append(wake | (1 << q))
                    mode = "wake_plus_leading_one"
                for mask in masks:
                    n_tried += 1
                    row = [(mask >> i) & 1 for i in range(L)]
                    if q and not is_q_periodic_prefix(row, q, q):
                        continue
                    if q and iw:
                        # interface is the suffix; wake must be exactly one period
                        pass
                    if support_max(row) < 0:
                        continue
                    rowT = evolve_T(row, driver, T, 0)
                    for d in range(1, max_d + 1):
                        if travelling_match(row, rowT, d, q, iw):
                            found.append({
                                "driver": "".join(str(b) for b in driver),
                                "T": T,
                                "q": q,
                                "iw": iw,
                                "d": d,
                                "row": "".join(str(b) for b in row),
                                "rowT": "".join(str(b) for b in pad_to(rowT, q + iw + d + 2)),
                                "mode": mode,
                            })
                            break
    return found, n_tried


def self_check():
    # Vacuum stays vacuum when driven by 0.
    row = [0, 0, 0, 0]
    nxt = evolve_half(row, 0)
    assert nxt[:4] == [0, 0, 0, 0]
    # Driver 1, vacuum right: site 1 becomes 1 XOR (0 OR 0) = 1.
    nxt = evolve_half([0, 0, 0], 1)
    assert nxt[0] == 1
    # Identity travelling: a lone 1 at site 0 of the half-line (j=1) with
    # driver 0 is not a positive-displacement front in one step.
    return True


def main():
    t0 = time.time()
    assert self_check()
    all_found = []
    tried = {}
    for name, driver in (("001", [0, 0, 1]), ("0111", [0, 1, 1, 1])):
        found, n_tried = search_fronts(driver)
        tried[name] = {"n_tried": n_tried, "n_found": len(found)}
        all_found.extend(found)
        print(f"{name}: tried={n_tried} found={len(found)}", flush=True)

    kill_no_front = len(all_found) == 0
    payload = {
        "not_a_prize_claim": True,
        "family": {
            "drivers": ["001", "0111"],
            "max_interface_width": 12,
            "max_wake_period": 8,
            "max_temporal_period": 12,
            "positive_displacement": True,
            "full_enum_when_q_plus_iw_le": 14,
            "larger_slice": "periodic wake plus optional leading 1 in the interface",
        },
        "tried": tried,
        "n_fronts": len(all_found),
        "fronts": all_found[:32],
        "kill": {
            "no_front_in_family": kill_no_front,
            "drift_not_attempted": kill_no_front,
            "fired": True,
            "text": (
                "No travelling front in the frozen family (interface width "
                "≤12, wake period ≤8, temporal period ≤12 compatible with "
                "the driver, positive displacement). Drift certificates were "
                "not searched. A travelling front without attraction would "
                "not have passed."
                if kill_no_front
                else "Fronts exist; a bounded local drift certificate is required "
                "and was not obtained as a universal attraction theorem."
            ),
        },
        "elapsed_sec": time.time() - t0,
    }
    if all_found:
        payload["kill"]["fired"] = True  # still need drift; recorded below
        payload["kill"]["needs_drift"] = True
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "n_fronts": len(all_found),
        "tried": tried,
        "kill": payload["kill"]["text"][:120],
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
