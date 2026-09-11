#!/usr/bin/env python3
"""Cycle AH: odd-spine half-step; period constraint on (c_{2^k}); one-step Green.

Cycle Z is the q=1 case of a Freshman half-step at times q*2^k. For every
q>=1, (1+x+x^2)^{q 2^k} = Q(x^{2^k}) with Q=(1+x+x^2)^q, the light-cone
edges cancel, and the centre contributes because G(q,q)=1, so

    c_{2 q U} = c_{q U} XOR Delta^{(q)}_k XOR J^{(q)}_k,   U=2^k,

where Delta is the XOR of the extra Q-support samples of the row at time
qU and J is the Green AND parity on [qU, 2qU). Even q reduces to a
smaller odd spine. Neither Delta nor J is identically 0 for q in
{3,5,7,9}, so those spines are not a closed form for a doubling.

If c is eventually period p=2^m * r with r odd, then (c_{2^k})_{k>=k0}
is eventually periodic with period dividing ord_r(2). In particular
r=1 (pure power-of-2 period, including period 2 and isolated-zero q=3)
forces (c_{2^k}) eventually constant, equivalently I_k eventually 0.

The one-step Green identity (AF's m=0 case) has a local remainder
O^{(1)}=1 XOR ell XOR c XOR r on the prize orbit, so it is not a bulk
handle for 00s or for I_k.

Not a prize claim: eventual vanishing of I_k remains open.

Run: python3 research/cycle_ah.py --certify
Dump: research/cycle_ah.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
    if d < 0 or d > 2 * m:
        return 0
    if m == 0:
        return int(d == 0)
    if m % 2 == 0:
        if d % 2:
            return 0
        return G(m // 2, d // 2)
    n = m // 2
    if d % 2 == 0:
        return G(n, d // 2) ^ G(n, d // 2 - 1)
    return G(n, (d - 1) // 2)


def poly_mul_gf2(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def trinom_pow(m: int) -> int:
    result = 1
    base = 0b111
    e = m
    while e:
        if e & 1:
            result = poly_mul_gf2(result, base)
        base = poly_mul_gf2(base, base)
        e >>= 1
    return result


def Q_support(q: int) -> list[int]:
    p = trinom_pow(q)
    return [i for i in range(2 * q + 1) if (p >> i) & 1]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def spatial(row: int, t: int, j: int) -> int:
    bit = j + t
    if bit < 0:
        return 0
    return (row >> bit) & 1


def and_remainder(rows: list[int], t0: int, t1: int, target_t: int) -> int:
    acc = 0
    for s in range(t0, t1):
        A = (rows[s] << 1) & rows[s]
        delta = target_t - s - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(delta, target_t - p):
                acc ^= 1
            tmp >>= 1
            p += 1
    return acc


def mul_order(q: int, a: int = 2) -> int:
    if q == 1:
        return 1
    x = 1
    for n in range(1, q + 8):
        x = (x * a) % q
        if x == 1:
            return n
    raise RuntimeError(f"no multiplicative order for {a} mod {q}")


def freshman_poly_ok(qs: list[int], kmax: int) -> bool:
    for q in qs:
        Q = trinom_pow(q)
        for k in range(0, kmax + 1):
            U = 1 << k
            left = trinom_pow(q * U)
            right = 0
            tmp, i = Q, 0
            while tmp:
                if tmp & 1:
                    right |= 1 << (i * U)
                tmp >>= 1
                i += 1
            if left != right:
                return False
    return True


def spine_half_step(rows: list[int], q: int, kmax: int) -> dict:
    """c_{2qU} = c_{qU} XOR Delta XOR J, and collect kill stats."""
    supp = Q_support(q)
    recs = []
    all_ok = True
    delta_all0 = True
    J_all0 = True
    flip_eq_delta = True
    flip_eq_J = True
    for k in range(0, kmax + 1):
        U = 1 << k
        t0 = q * U
        t1 = 2 * q * U
        if t1 >= len(rows):
            break
        P = rows[t0]
        lin = 0
        extras = 0
        for i in supp:
            bit = (P >> ((2 * q - i) * U)) & 1
            lin ^= bit
            if i not in (0, q, 2 * q):
                extras ^= bit
        J = and_remainder(rows, t0, t1, t1)
        c0 = spatial(P, t0, 0)
        c1 = spatial(rows[t1], t1, 0)
        ok = c1 == (lin ^ J)
        # edges are 1 XOR 1; centre is in the support, so lin = c0 XOR extras
        if lin != (c0 ^ extras):
            ok = False
        if not ok:
            all_ok = False
        if extras:
            delta_all0 = False
        if J:
            J_all0 = False
        flip = c0 ^ c1
        if flip != extras:
            flip_eq_delta = False
        if flip != J:
            flip_eq_J = False
        recs.append({
            "k": k,
            "c0": c0,
            "c1": c1,
            "Delta": extras,
            "J": J,
            "ok": ok,
        })
    return {
        "q": q,
        "support": supp,
        "all_ok": all_ok,
        "n": len(recs),
        "Delta_identically_0": delta_all0,
        "J_identically_0": J_all0,
        "flip_eq_Delta": flip_eq_delta,
        "flip_eq_J": flip_eq_J,
        "empty_extras": Q_support(q) == [0, 1, 2] and q == 1,
        "rows": recs,
    }


def q9_delta_at_k8(rows: list[int]) -> int:
    """Delta^{(9)}_8 from the row at time 9*2^8; no AND remainder needed."""
    q, k = 9, 8
    U = 1 << k
    t0 = q * U
    P = rows[t0]
    extras = 0
    for i in Q_support(q):
        if i not in (0, q, 2 * q):
            extras ^= (P >> ((2 * q - i) * U)) & 1
    return extras


def one_step(rows: list[int], cap: int) -> dict:
    one_fail = 0
    local_fail = 0
    for t in range(cap):
        R = rows[t]
        ell = spatial(R, t, -1)
        c = spatial(R, t, 0)
        r = spatial(R, t, 1)
        cp = spatial(rows[t + 1], t + 1, 0)
        older = and_remainder(rows, 0, t, t + 1)
        if (1 ^ (c & r) ^ older) != cp:
            one_fail += 1
        if older != (1 ^ ell ^ c ^ r):
            local_fail += 1
    return {"one_fail": one_fail, "local_fail": local_fail, "cap": cap}


def annulus_O1_vs_I(rows: list[int], kmax: int) -> dict:
    fails = []
    matches = []
    for k in range(1, kmax + 1):
        T = 1 << (k - 1)
        acc = 0
        for t in range(T, 2 * T):
            R = rows[t]
            acc ^= 1 ^ spatial(R, t, -1) ^ spatial(R, t, 0) ^ spatial(R, t, 1)
        Ik = spatial(rows[2 * T], 2 * T, 0) ^ spatial(rows[T], T, 0)
        if acc == Ik:
            matches.append(k)
        else:
            fails.append(k)
    return {"fails": fails, "matches": matches}


def synthetic_period_constraint() -> dict:
    """Eventual period 2^m * r (r odd) => (c_{2^k}) eventually period | ord_r(2)."""
    T = 5
    recs = []
    all_ok = True
    for m, r in [
        (0, 1), (1, 1), (2, 1), (3, 1),
        (0, 3), (1, 3),
        (0, 5), (2, 5),
        (0, 7),
        (0, 9), (1, 9),
    ]:
        p = (1 << m) * r
        seed = [((i * 3 + 1) % 2) for i in range(p)]
        N = 1 << 14
        c = [0] * N
        for i in range(T, N):
            c[i] = seed[(i - T) % p]
        k_start = m
        while (1 << k_start) < T:
            k_start += 1
        b = [c[1 << k] for k in range(k_start, 14)]
        lam = mul_order(r)
        ok = all(b[i] == b[i + lam] for i in range(len(b) - lam))
        const = len(set(b)) == 1
        if r == 1 and not const:
            ok = False
        if not ok:
            all_ok = False
        recs.append({
            "m": m, "r": r, "p": p, "lam": lam, "k_start": k_start,
            "ok": ok, "const": const,
        })
    orders = {r: mul_order(r) for r in (1, 3, 5, 7, 9)}
    return {"all_ok": all_ok, "orders": orders, "rows": recs}


def self_checks(
    c20,
    poly_ok: bool,
    spines: dict,
    d9k8: int,
    one: dict,
    o1: dict,
    synth: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert poly_ok
    assert G(1, 1) == 1 and G(3, 3) == 1 and G(9, 9) == 1
    for q, sp in spines.items():
        assert sp["all_ok"], q
    assert Q_support(1) == [0, 1, 2]
    assert spines[1]["Delta_identically_0"]
    assert spines[1]["empty_extras"]
    assert spines[1]["flip_eq_J"]
    for q in (3, 5, 7):
        assert not spines[q]["Delta_identically_0"]
        assert not spines[q]["J_identically_0"]
        assert not spines[q]["flip_eq_Delta"]
        assert not spines[q]["flip_eq_J"]
    assert not spines[9]["J_identically_0"]
    assert d9k8 == 1
    assert one["one_fail"] == 0 and one["local_fail"] == 0
    assert o1["fails"], "O^(1) annulus was not killed"
    assert synth["all_ok"]
    assert synth["orders"] == {1: 1, 3: 2, 5: 4, 7: 3, 9: 6}
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)

    poly_ok = freshman_poly_ok([1, 3, 5, 7, 9], 8)
    synth = synthetic_period_constraint()

    # tmax: q=9 k=7 identity uses 18*128=2304; q=9 k=8 Delta uses row 9*256=2304.
    tmax = 9 * (1 << 8)
    rows = evolve_rows(tmax)
    spines = {
        1: spine_half_step(rows, 1, 9),
        3: spine_half_step(rows, 3, 8),
        5: spine_half_step(rows, 5, 7),
        7: spine_half_step(rows, 7, 6),
        9: spine_half_step(rows, 9, 7),
    }
    d9k8 = q9_delta_at_k8(rows)
    if d9k8:
        spines[9]["Delta_identically_0"] = False
        spines[9]["flip_eq_J"] = False
    one = one_step(rows, 40)
    o1 = annulus_O1_vs_I(rows, 10)

    checks = self_checks(c20, poly_ok, spines, d9k8, one, o1, synth)
    dump = {
        "cycle": "AH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "freshman_poly_ok": poly_ok,
        "Q_support": {str(q): Q_support(q) for q in (1, 3, 5, 7, 9)},
        "spines": {
            str(q): {
                "all_ok": sp["all_ok"],
                "n": sp["n"],
                "Delta_identically_0": sp["Delta_identically_0"],
                "J_identically_0": sp["J_identically_0"],
                "flip_eq_Delta": sp["flip_eq_Delta"],
                "flip_eq_J": sp["flip_eq_J"],
                "empty_extras": sp["empty_extras"],
            }
            for q, sp in spines.items()
        },
        "q9_Delta_k8": d9k8,
        "one_step": one,
        "O1_vs_I": o1,
        "period_constraint": {
            "all_ok": synth["all_ok"],
            "orders": synth["orders"],
        },
        "lemmas": {
            "odd_spine_half_step": True,
            "power_of_2_period_forces_b_constant": True,
            "one_step_O1_local": True,
            "I_k_not_eventually_0": None,
            "prize": False,
        },
        "verdict": {
            "odd_spine_half_step": "LEMMA",
            "period_constraint_on_b": "LEMMA",
            "one_step_O1_local": "LEMMA",
            "Delta_or_J_closed_form": "KILLED",
            "O1_as_I_k_or_bulk_00": "KILLED",
            "I_k_eventually_0": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("q9_Delta_k8", d9k8, "O1_fails", o1["fails"])


if __name__ == "__main__":
    main()
