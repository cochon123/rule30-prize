#!/usr/bin/env python3
"""Deep-tail shift of Q_n under a three-zero run of F.

On a phase-01 period-2 centre, if F_{2n-1}=F_{2n-2}=F_{2n-3}=0 then
    F_{2n+1}(u) = F_{2n-1}(Su)
and therefore Q_n(u) = Q_{n-1}(Su) in the Fibonacci ring (values).
An L_0 tail of width T forces this for every n with 2n-3 > T, so the
forced bit is u_n = Q_{n-1}(Su). Four consecutive zeros give the even
companion F_{2n}(u)=F_{2n-2}(Su). This is the second step of
tail-forcing. It does not kill L_0: Q_n is not a T-independent sliding
window, and iterating a fixed Q_{n0} along S fails because Su is a
bump, not L_0. Not a prize claim.

Run: python3 research/period2_qshift.py --certify
Dump: research/period2_qshift.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_lead import Q_n, T20_WORDS
from period2_vacuum import F_of_u, fib_strings, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

LAST_SAT = [
    (8, 9),
    (15, 6),
    (16, 9),
    (20, 16),
    (22, 12),
    (26, 5),
]


def shift_u(u):
    if not u:
        return []
    return u[1:] + [0]


def clip_kind(u, q):
    if not u:
        return None
    if q == 1 and u[-1] == 1:
        return "11"
    if q == 0 and len(u) >= 4 and u[-4:] == [0, 0, 0, 0]:
        return "00000"
    return None


def force_from(prefix, T, n_max=64):
    """Append u_n=Q_n until 11-clip, 00000-clip, even F_{2n}>T, or n_max."""
    bits = list(prefix)
    events = []
    for n in range(len(prefix), n_max + 1):
        Ff, _ = F_of_u(bits + [0], 2 * n + 2)
        even_k = 2 * n
        even_fire = even_k > T and even_k < len(Ff) and Ff[even_k] == 1
        q = Q_n(bits, n)
        clip = clip_kind(bits, q)
        rec = {
            "n": n,
            "q": q,
            "even_fire": even_fire,
            "clip": clip,
        }
        events.append(rec)
        if even_fire:
            rec["stop"] = "even_F"
            return bits, events
        if clip:
            rec["stop"] = clip
            return bits, events
        bits.append(q)
    return bits, events


def survivors_u(T: int, R: int):
    top = T + R
    L = max(nvars(top), 1)
    kmax = max(top + 8, 2 * L + 4)
    out = []
    for u in fib_strings(L):
        F, _ = F_of_u(u, kmax)
        if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
            out.append(u)
    return out


def certify_skip_on_fib(L: int = 12) -> dict:
    """Three-zero odd skip and four-zero even skip on every Fibonacci word."""
    n_odd = 0
    n_even = 0
    n_odd_fail = 0
    n_even_fail = 0
    fail_ex = []
    kmax = 2 * L + 6
    for u in fib_strings(L):
        F, _ = F_of_u(u, kmax)
        FS, _ = F_of_u(shift_u(u), kmax)
        n_hi = min(L, (kmax - 1) // 2)
        for n in range(2, n_hi + 1):
            if F[2 * n - 1] == 0 and F[2 * n - 2] == 0 and F[2 * n - 3] == 0:
                n_odd += 1
                ok_f = F[2 * n + 1] == FS[2 * n - 1]
                ok_q = Q_n(u, n) == Q_n(u[1:], n - 1)
                if not (ok_f and ok_q):
                    n_odd_fail += 1
                    if len(fail_ex) < 5:
                        fail_ex.append(
                            {"kind": "odd", "n": n, "u": u, "ok_f": ok_f, "ok_q": ok_q}
                        )
            if (
                n >= 2
                and F[2 * n - 1] == 0
                and F[2 * n - 2] == 0
                and F[2 * n - 3] == 0
                and F[2 * n - 4] == 0
            ):
                n_even += 1
                if F[2 * n] != FS[2 * n - 2]:
                    n_even_fail += 1
                    if len(fail_ex) < 5:
                        fail_ex.append({"kind": "even", "n": n, "u": u})
    return {
        "L": L,
        "n_odd": n_odd,
        "n_odd_fail": n_odd_fail,
        "n_even": n_even,
        "n_even_fail": n_even_fail,
        "fail_ex": fail_ex,
    }


def certify_last_sat() -> dict:
    """Deep-tail Q_n=Q_{n-1}(Su) on last-sat, and Q-forced obstruction."""
    rows = []
    for T, R in LAST_SAT:
        mods = survivors_u(T, R)
        n_deep = 0
        n_deep_fail = 0
        n_iter_fail = 0
        n_iter = 0
        stops = Counter()
        extras = []
        n0 = nvars(T)
        for u in mods:
            F, _ = F_of_u(u, max(T + R + 4, 2 * len(u) + 4))
            n_hi = min(len(u) - 1, (len(F) - 1) // 2)
            for n in range(2, n_hi + 1):
                if 2 * n - 3 <= T:
                    continue
                if not (F[2 * n - 1] == 0 and F[2 * n - 2] == 0 and F[2 * n - 3] == 0):
                    continue
                n_deep += 1
                if Q_n(u, n) != Q_n(u[1:], n - 1):
                    n_deep_fail += 1
                # iterated sliding of a fixed Q_{n0} must be allowed to fail
                n_anchor = (T + 3) // 2 + 1
                if n > n_anchor and n_anchor >= 2 and len(u) >= n:
                    n_iter += 1
                    q_slide = Q_n(u[n - n_anchor :], n_anchor)
                    if q_slide != Q_n(u, n):
                        n_iter_fail += 1
            bits, ev = force_from(u[:n0], T, n_max=n0 + 48)
            stop = ev[-1].get("stop") if ev else "none"
            stops[stop] += 1
            extras.append(ev[-1]["n"] - n0 if ev else None)
        rows.append(
            {
                "T": T,
                "R": R,
                "n_models": len(mods),
                "n_deep": n_deep,
                "n_deep_fail": n_deep_fail,
                "n_iter": n_iter,
                "n_iter_fail": n_iter_fail,
                "force_stops": dict(stops),
                "force_extras": extras,
            }
        )
        assert n_deep_fail == 0, (T, R, n_deep_fail)
        assert all(s in {"11", "00000", "even_F"} for s in stops), stops
    return rows


def certify_t20_clip11() -> dict:
    """T=20 last-sat: forced continuation 11-clips at n=18, not a pad F_37."""
    rows = []
    for i, w in enumerate(T20_WORDS):
        n0 = nvars(20)
        bits, ev = force_from(w[:n0], 20, n_max=40)
        stop = ev[-1].get("stop")
        nstop = ev[-1]["n"]
        # deep-tail on the sat word itself, n=12..17
        deep = []
        for n in range(12, 18):
            deep.append(Q_n(w, n) == Q_n(w[1:], n - 1))
        # sliding Q_11 is not the same as iterating the one-step identity
        slide_fail = []
        for n in range(12, 18):
            if Q_n(w, n) != Q_n(w[n - 11 :], 11):
                slide_fail.append(n)
        rows.append(
            {
                "i": i,
                "stop": stop,
                "nstop": nstop,
                "deep_12_17": all(deep),
                "slide_Q11_fail_n": slide_fail,
                "u17": w[17],
                "Q18": Q_n(w, 18),
            }
        )
        assert stop == "11" and nstop == 18
        assert w[17] == 1 and Q_n(w, 18) == 1
        assert all(deep)
        assert slide_fail  # must fail: Su is a bump
    return rows


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict = {}

    skip = certify_skip_on_fib(12)
    checks["odd_skip_fib12"] = skip["n_odd_fail"] == 0 and skip["n_odd"] > 0
    checks["even_skip_fib12"] = skip["n_even_fail"] == 0 and skip["n_even"] > 0
    assert checks["odd_skip_fib12"] and checks["even_skip_fib12"], skip

    last = certify_last_sat()
    checks["last_sat_deep_Q"] = all(r["n_deep_fail"] == 0 and r["n_deep"] > 0 for r in last)
    checks["last_sat_force_sft_or_even"] = all(
        set(r["force_stops"]).issubset({"11", "00000", "even_F"}) and r["n_models"] > 0
        for r in last
    )
    # iterated fixed-window Q_{n0} is not a lemma
    checks["iter_slide_fails_somewhere"] = any(r["n_iter_fail"] > 0 for r in last)
    assert checks["last_sat_deep_Q"]
    assert checks["last_sat_force_sft_or_even"]
    assert checks["iter_slide_fails_somewhere"]

    t20 = certify_t20_clip11()
    checks["t20_force_clip11_n18"] = True
    checks["t20_slide_Q11_not_identity"] = all(r["slide_Q11_fail_n"] for r in t20)

    checks["all_ok"] = True
    wall = time.perf_counter() - t0
    dump = {
        "attack": "period2_qshift",
        "problem": "deep-tail Q_n = Q_{n-1}(Su) under a three-zero run",
        "verdict": "LEMMA",
        "kill": False,
        "survive": False,
        "prize": False,
        "kill_reason": (
            "Three consecutive F zeros skip two columns under S, so "
            "Q_n(u)=Q_{n-1}(Su) on an L_0 tail; the T=20 forced bit is "
            "an 11-clip at n=18. Q_n is not a T-independent sliding "
            "window and a fixed Q_{n0} does not iterate. Not a uniform R."
        ),
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "skip_fib12": {k: skip[k] for k in ("L", "n_odd", "n_odd_fail", "n_even", "n_even_fail")},
        "last_sat": last,
        "t20_force": t20,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict=LEMMA wall={wall:.3f}s odd={skip['n_odd']} even={skip['n_even']}")
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
