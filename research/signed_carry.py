#!/usr/bin/env python3
"""Signed-digit weight of Rule 30's *7 correction stream (Astra ideas6 item 4).

Right-edge packed row Z_t, with bit k equal to x(t, t-k). Ordinary integer
identities are checked, then S(n) = sum_{t<n} w±(Q_t mod 2^n) is measured
at n=128,256,512. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/signed_carry.py
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


def naf_weight(x: int) -> int:
    """Number of nonzero digits in the non-adjacent form of x (digits -1,0,1).

    NAF is a minimum-weight signed-binary representation.
    """
    if x < 0:
        x = -x
    w = 0
    while x:
        if x & 1:
            w += 1
            if x & 2:
                x += 1
            else:
                x -= 1
        x >>= 1
    return w


def min_signed_weight_mod(r: int, n: int) -> int:
    """Min NAF weight of an integer congruent to r modulo 2^n."""
    m = 1 << n
    r %= m
    # Candidates: r, r-2^n (the two n-bit signed interpretations), and
    # NAF may use an extra leading digit, which naf_weight already allows.
    return min(naf_weight(r), naf_weight(r - m), naf_weight(r + m) if r else naf_weight(0))


def right_edge_update(Z: int) -> int:
    """u(t+1,k) = u(t,k) XOR (u(t,k-1) OR u(t,k-2)), bit 0 = right edge."""
    return Z ^ ((Z << 1) | (Z << 2))


def correction_Q(Z: int) -> int:
    U = Z & (Z << 1)
    V = Z & (Z << 2)
    W = Z & (Z << 1) & (Z << 2)
    return 2 * U + V - W


def self_check(max_t: int = 80) -> dict:
    bits = experiment_center_bits(max_t + 1)
    Z = 1
    identity_ok = True
    centre_ok = True
    max_abs_err = 0
    for t in range(max_t):
        # Centre of the right-edge packing is bit t: x(t, 0) = u(t, t).
        if ((Z >> t) & 1) != bits[t]:
            centre_ok = False
            break
        Q = correction_Q(Z)
        Znext = right_edge_update(Z)
        pred = 7 * Z - 2 * Q
        err = abs(pred - Znext)
        if err > max_abs_err:
            max_abs_err = err
        if pred != Znext:
            identity_ok = False
        Z = Znext
    # NAF of 3 is 4 + (-1): weight 2, not 2 via 2+1.
    naf_ok = (
        naf_weight(0) == 0
        and naf_weight(1) == 1
        and naf_weight(2) == 1
        and naf_weight(3) == 2
        and naf_weight(5) == 2
        and naf_weight(6) == 2
        and naf_weight(7) == 2
        and naf_weight(43) == 4
    )
    return {
        "identity_holds_through": max_t if identity_ok else None,
        "identity_ok": identity_ok,
        "centre_matches_experiment": centre_ok,
        "max_abs_err": max_abs_err,
        "naf_ok": naf_ok,
        "Z0": 1,
    }


def measure(n: int) -> dict:
    mask = (1 << n) - 1
    Z = 1
    total = 0
    max_w = 0
    weights = []
    for t in range(n):
        Q = correction_Q(Z)
        w = min_signed_weight_mod(Q, n)
        total += w
        if w > max_w:
            max_w = w
        if t < 16 or t in (n - 1, n // 2):
            weights.append({"t": t, "w": w, "Q_mod": Q & mask})
        Z = right_edge_update(Z)
    n2 = n * n
    return {
        "n": n,
        "S": total,
        "n2": n2,
        "S_over_n2": total / n2,
        "threshold": 0.05 * n2,
        "exceeds_0_05_n2": total > 0.05 * n2,
        "mean_w": total / n,
        "max_w": max_w,
        "sample_weights": weights,
    }


def main() -> None:
    t0 = time.time()
    check = self_check(80)
    if not check["identity_ok"] or not check["centre_matches_experiment"] or not check["naf_ok"]:
        raise SystemExit("self-check failed: " + json.dumps(check))
    ns = (128, 256, 512)
    rows = [measure(n) for n in ns]
    kill_sparse = all(r["exceeds_0_05_n2"] for r in rows if r["n"] in (256, 512))
    # Generating Q_t used the packed row at every t < n.
    kill_generation = True
    payload = {
        "not_a_prize_claim": True,
        "identity": "Z_{t+1} = 7 Z_t - 2 Q_t,  Q_t = 2U + V - W",
        "packing": "right-edge: bit k is x(t, t-k)",
        "weight": "min NAF weight of Q_t, Q_t-2^n, Q_t+2^n",
        "self_check": check,
        "measurements": rows,
        "kill": {
            "S_exceeds_0_05_n2_at_256_and_512": kill_sparse,
            "corrections_require_packed_row_evolution": kill_generation,
            "fired": kill_sparse or kill_generation,
            "text": (
                "S(n) exceeds 0.05 n^2 at n=256 and n=512"
                if kill_sparse
                else "S(n) is sparse enough to continue, but Q_t is still "
                "read from the packed row"
            ),
        },
        "elapsed_sec": time.time() - t0,
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "identity_ok": check["identity_ok"],
        "S_over_n2": {r["n"]: r["S_over_n2"] for r in rows},
        "kill": payload["kill"]["fired"],
        "which": payload["kill"]["text"],
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
