#!/usr/bin/env python3
"""Cycle CB: half-xor intertwines with the cyclic derivative.

Write v(s)_t = s_t xor s_{t+pi} on a length-2pi string. Then v(DB)=D(v(B)),
so A=DB forces v(A)=D(v(B)). Odd 2-copy drivers therefore cannot be
derivatives of even 2-copy bits. Unique continuation does not preserve
2-copy type, and the half-xor obstruction is not absorbing on arbitrary
drives. After the three-pair scar window on the k=8 odd lift, v(A) differs
from D(v(B)) on every remaining pair (prefix). Not a prize claim.

Run: python3 research/cycle_cb.py --certify
Dump: research/cycle_cb.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import (
    KNOWN20,
    deriv,
    packed_center_bits,
    prize_cycle,
    reconstruct,
    xorcat,
)

OUT = Path(__file__).resolve().with_suffix(".json")


def ext(seq: list[int], L: int) -> list[int]:
    return seq if L == len(seq) else seq * (L // len(seq))


def half_xor(seq: list[int]) -> list[int]:
    n = len(seq)
    h = n // 2
    return [seq[t] ^ seq[t + h] for t in range(h)]


def twocopy_type(seq: list[int]) -> str:
    n = len(seq)
    if n % 2:
        return "oddlen"
    h = n // 2
    a, b = seq[:h], seq[h:]
    if a == b:
        return "E"
    if a == [x ^ 1 for x in b]:
        return "O"
    return "N"


def intertwine_ok(trials: int = 200) -> bool:
    """v(DB)=D(v(B)) on random even-length strings."""
    rng = random.Random(3)
    for L in (8, 16, 32):
        for _ in range(trials):
            b = [rng.randint(0, 1) for _ in range(L)]
            if half_xor(deriv(b)) != deriv(half_xor(b)):
                return False
    return True


def d_kills_odd_twocopy() -> bool:
    """D maps even and odd 2-copies into even 2-copies."""
    rng = random.Random(5)
    for n0 in (2, 4, 8, 16):
        for _ in range(40):
            b0 = [rng.randint(0, 1) for _ in range(n0)]
            be = b0 + b0
            bo = b0 + [x ^ 1 for x in b0]
            if twocopy_type(deriv(be)) != "E":
                return False
            if twocopy_type(deriv(bo)) != "E":
                return False
    return True


def twocopy_not_invariant() -> bool:
    """Unique continuation of 2-copy drives is often not a 2-copy."""
    rng = random.Random(7)
    n_not = 0
    n_ok = 0
    for n0 in (4, 8):
        for _ in range(80):
            a0 = [rng.randint(0, 1) for _ in range(n0)]
            b0 = [rng.randint(0, 1) for _ in range(n0)]
            a = a0 + [x ^ 1 for x in a0]
            b = b0 + b0
            u = reconstruct(a, b)
            if u is None:
                continue
            n_ok += 1
            if twocopy_type(u) == "N":
                n_not += 1
    return n_ok > 0 and n_not > n_ok // 2


def obstruction_not_absorbing(trials: int = 400) -> dict:
    """v(A)!=D(v(B)) need not pass to the next pair on a random drive."""
    rng = random.Random(9)
    n_fail = 0
    n_hold = 0
    L = 16
    for _ in range(trials):
        a = [rng.randint(0, 1) for _ in range(L)]
        b = [rng.randint(0, 1) for _ in range(L)]
        if all(x == 0 for x in b):
            continue
        h0 = sum(x ^ y for x, y in zip(half_xor(a), deriv(half_xor(b))))
        if h0 == 0:
            continue
        u = reconstruct(a, b)
        if u is None:
            continue
        h1 = sum(x ^ y for x, y in zip(half_xor(b), deriv(half_xor(u))))
        if h1 == 0:
            n_fail += 1
        else:
            n_hold += 1
    return {"ok": n_fail > 0, "n_fail": n_fail, "n_hold": n_hold}


def odd_lift_syndrome(k: int) -> dict:
    """Half-xor syndrome along the odd lift of the k-machine."""
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
    rows = []
    p = W + 1
    while p <= 2 * W:
        a = ext(seqs[p - 2], cur_pi)
        b = ext(seqs[p - 1], cur_pi)
        if all(x == 0 for x in b):
            sm = xorcat(a)
            u = [0] * cur_pi
            for t in range(cur_pi - 1):
                u[t + 1] = a[t] ^ u[t]
            if sm == 1:
                if odd_p is None:
                    odd_p = p
                u = u + [x ^ 1 for x in u]
                cur_pi *= 2
            seqs[p] = u
        else:
            seqs[p] = reconstruct(a, b)
        if odd_p is not None:
            aa = ext(seqs[p - 2], cur_pi)
            bb = ext(seqs[p - 1], cur_pi)
            va = half_xor(aa)
            vb = half_xor(bb)
            hamv = sum(x ^ y for x, y in zip(va, deriv(vb)))
            tu = twocopy_type(ext(seqs[p], cur_pi))
            rows.append(
                {
                    "p": p,
                    "hamv": hamv,
                    "A": twocopy_type(aa),
                    "B": twocopy_type(bb),
                    "U": tu,
                }
            )
        p += 1
    nec_ps = [r["p"] for r in rows if r["hamv"] == 0]
    after = [r for r in rows if odd_p is not None and r["p"] > odd_p + 3]
    after_min = min((r["hamv"] for r in after), default=None)
    not2 = sum(1 for r in rows if r["U"] == "N")
    return {
        "k": k,
        "odd_p": odd_p,
        "n": len(rows),
        "nec_ps": nec_ps,
        "after_n": len(after),
        "after_min_hamv": after_min,
        "not2": not2,
        "ok": (
            odd_p is not None
            and (after_min is None or after_min > 0)
            and 0 not in (r["hamv"] for r in after)
        ),
    }


def self_checks(
    c20,
    inter: bool,
    kills: bool,
    notinv: bool,
    absorb: dict,
    syn4: dict,
    syn8: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert inter and kills and notinv
    assert absorb["ok"] and absorb["n_fail"] > 0
    assert syn4["odd_p"] == 29 and syn4["ok"]
    assert syn8["odd_p"] == 400 and syn8["ok"]
    assert syn8["after_n"] > 0 and syn8["after_min_hamv"] >= 1
    assert syn8["nec_ps"] == [400, 401, 403]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    inter = intertwine_ok()
    kills = d_kills_odd_twocopy()
    notinv = twocopy_not_invariant()
    absorb = obstruction_not_absorbing()
    syn4 = odd_lift_syndrome(4)
    syn8 = odd_lift_syndrome(8)
    checks = self_checks(c20, inter, kills, notinv, absorb, syn4, syn8)
    dump = {
        "cycle": "CB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "absorb": {k: absorb[k] for k in ("n_fail", "n_hold")},
        "syn4": {k: syn4[k] for k in ("odd_p", "n", "nec_ps", "after_n", "after_min_hamv", "not2")},
        "syn8": {k: syn8[k] for k in ("odd_p", "n", "nec_ps", "after_n", "after_min_hamv", "not2")},
        "lemmas": {
            "half_xor_intertwines_D": True,
            "D_kills_odd_twocopy": True,
            "twocopy_invariant": False,
            "half_xor_obstruction_absorbing": False,
            "post_window_half_xor_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "half_xor_intertwines_D": "LEMMA",
            "D_kills_odd_twocopy": "LEMMA",
            "twocopy_invariant": "KILLED",
            "half_xor_obstruction_absorbing": "KILLED",
            "post_window_half_xor_all_k": "PREFIX",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("syn4", dump["syn4"])
    print("syn8", dump["syn8"])
    print("absorb", dump["absorb"])


if __name__ == "__main__":
    main()
