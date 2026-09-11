#!/usr/bin/env python3
"""Cycle CD: AND-triples stay iff a forced fifth bit; identically AND implies d=Da.

If (c,a,b) is AND-closed, packed update collapses to a'=d xor a and
b'=a xor b, and the next triple stays AND-closed iff
e = a xor (d and not (a or b)). Identically AND therefore forces
d=Da, hence d_t = b_t xor b_{t+2}. A forbidden triple cannot enter
S when (e,d)=(0,1). S is not absorbing. No identically-AND triple
after the scar on the k=4 and k=8 odd lifts (prefix). Not a prize
claim.

Run: python3 research/cycle_cd.py --certify
Dump: research/cycle_cd.json
"""
from __future__ import annotations

import argparse
import json
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
from cycle_cb import ext

OUT = Path(__file__).resolve().with_suffix(".json")

S = {(c, a, b) for c in (0, 1) for a in (0, 1) for b in (0, 1) if c == (a & b)}
F = {(c, a, b) for c in (0, 1) for a in (0, 1) for b in (0, 1) if (c, a, b) not in S}


def forced_e(a: int, b: int, d: int) -> int:
    return a ^ (d & (0 if (a | b) else 1))


def step5(e: int, d: int, c: int, a: int, b: int) -> tuple[int, int, int]:
    bp = c ^ (a | b)
    ap = d ^ (c | a)
    cp = e ^ (d | c)
    return cp, ap, bp


def stay_iff_forced() -> bool:
    for e in (0, 1):
        for d in (0, 1):
            for c, a, b in S:
                nxt = step5(e, d, c, a, b) in S
                if nxt != (e == forced_e(a, b, d)):
                    return False
    return True


def collapse_under_S() -> bool:
    """In S, a' = d xor a and b' = a xor b, independently of e,c."""
    for d in (0, 1):
        for c, a, b in S:
            _cp, ap, bp = step5(0, d, c, a, b)
            if ap != (d ^ a) or bp != (a ^ b):
                return False
            _cp, ap, bp = step5(1, d, c, a, b)
            if ap != (d ^ a) or bp != (a ^ b):
                return False
    return True


def no_enter_ed01() -> bool:
    """Forbidden triples cannot enter S when (e,d)=(0,1)."""
    for c, a, b in F:
        if step5(0, 1, c, a, b) in S:
            return False
    return True


def s_not_absorbing() -> dict:
    n_enter = 0
    n_leave = 0
    for e in (0, 1):
        for d in (0, 1):
            for c, a, b in F:
                if step5(e, d, c, a, b) in S:
                    n_enter += 1
            for c, a, b in S:
                if step5(e, d, c, a, b) not in S:
                    n_leave += 1
    return {"ok": n_enter > 0 and n_leave > 0, "n_enter": n_enter, "n_leave": n_leave}


def known_ident0_Da(kmax: int = 12) -> dict:
    """On settled prize cycles, ident-0 at r>=7 has d=Da on the AND triple."""
    rows = []
    for k in range(3, kmax + 1):
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seq = [[(w >> p) & 1 for w in cyc] for p in range(W + 1)]
        z = [p for p in range(W + 1) if all(x == 0 for x in seq[p])]
        ok = True
        for r in z:
            if r < 5:
                continue
            a = seq[r - 3]
            d = seq[r - 5]
            c = seq[r - 4]
            b = seq[r - 2]
            if c != [x & y for x, y in zip(a, b)]:
                ok = False
            if d != deriv(a):
                ok = False
            if d != [b[t] ^ b[(t + 2) % pi] for t in range(pi)]:
                ok = False
        rows.append({"k": k, "z": z, "ok": ok})
    return {"ok": all(r["ok"] for r in rows), "n": len(rows)}


def odd_lift_and(k: int) -> dict:
    pi, cyc = prize_cycle(k)
    W = 1 << k
    seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
    cur_pi = pi
    odd_p = None
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
        p += 1
    L = cur_pi
    n_and = 0
    n_Da = 0
    min_bad = None
    n = 0
    q = odd_p
    while q <= 2 * W:
        c = ext(seqs[q - 3], L)
        a = ext(seqs[q - 2], L)
        b = ext(seqs[q - 1], L)
        and_eq = c == [x & y for x, y in zip(a, b)]
        if and_eq:
            n_and += 1
        n_bad = sum(1 for t in range(L) if (c[t], a[t], b[t]) not in S)
        if min_bad is None or n_bad < min_bad:
            min_bad = n_bad
        if q - 4 in seqs:
            d = ext(seqs[q - 4], L)
            if d == deriv(a):
                n_Da += 1
        n += 1
        q += 1
    return {
        "k": k,
        "odd_p": odd_p,
        "n": n,
        "n_and": n_and,
        "n_Da": n_Da,
        "min_bad": min_bad,
        "ok": n_and == 0 and min_bad is not None and min_bad > 0,
    }


def self_checks(c20, stay: bool, coll: bool, barrier: bool, absorb: dict, known: dict, ham4: dict, ham8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert stay and coll and barrier and absorb["ok"]
    assert known["ok"]
    assert ham4["ok"] and ham4["odd_p"] == 29
    assert ham8["ok"] and ham8["odd_p"] == 400
    assert ham8["n_Da"] < ham8["n"]  # d=Da is not automatic after the scar
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    stay = stay_iff_forced()
    coll = collapse_under_S()
    barrier = no_enter_ed01()
    absorb = s_not_absorbing()
    known = known_ident0_Da()
    ham4 = odd_lift_and(4)
    ham8 = odd_lift_and(8)
    checks = self_checks(c20, stay, coll, barrier, absorb, known, ham4, ham8)
    dump = {
        "cycle": "CD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "absorb": {k: absorb[k] for k in ("n_enter", "n_leave")},
        "known": known,
        "ham4": {k: ham4[k] for k in ("odd_p", "n", "n_and", "n_Da", "min_bad")},
        "ham8": {k: ham8[k] for k in ("odd_p", "n", "n_and", "n_Da", "min_bad")},
        "lemmas": {
            "stay_iff_forced_e": True,
            "collapse_a_b_under_S": True,
            "ident_AND_implies_d_eq_Da": True,
            "no_enter_S_when_ed_01": True,
            "S_absorbing": False,
            "no_AND_triple_after_scar_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "stay_iff_forced_e": "LEMMA",
            "collapse_a_b_under_S": "LEMMA",
            "ident_AND_implies_d_eq_Da": "LEMMA",
            "no_enter_S_when_ed_01": "LEMMA",
            "S_absorbing": "KILLED",
            "no_AND_triple_after_scar_all_k": "PREFIX",
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
    print("absorb", dump["absorb"])
    print("ham4", dump["ham4"])
    print("ham8", dump["ham8"])


if __name__ == "__main__":
    main()
