"""Cycle O: germ reduction of period-2 L_0 under the Fibonacci shift S.

L_0 is a 1 at column T followed by R zeros in F_k(u). The Cycle D
certificate already records that S sends a long L_0 germ to a length-2
bump, not to a smaller L_0. This script classifies the bump (B0) and the
next few S-images, looking for a well-founded rank (on R, on Hamming
weight, or on hitting the identically-zero column F_4).

A uniform bound R(T) <= R0 for all T would exclude every L_0 onset and,
with the eventual-vacuum lemma, exclude period 2 for every finite seed.
That is the target. This file does not claim it.

Run: python3 research/period2_germ.py --certify
Dump: research/period2_germ.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_vacuum import F_of_u, fib_strings, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def survivors(T: int, R: int):
    top = T + R
    L = max(nvars(top), 1)
    kmax = max(top + 8, 2 * L + 4)
    out = []
    for u in fib_strings(L):
        F, G = F_of_u(u, kmax)
        if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
            out.append((u, F, G, kmax))
    return out


def window(F, start, length):
    n = len(F)
    bits = []
    for i in range(start, start + length):
        if 0 <= i < n:
            bits.append(str(F[i]))
        else:
            bits.append("?")
    return "".join(bits)


def classify(F, T, length=16):
    """Classify the germ of F at T: L0, B0 (11 then zeros), bump, mixed."""
    w = [F[T + i] if T + i < len(F) else None for i in range(length)]
    if w[0] != 1:
        return "not1", w
    zeros = 0
    for b in w[1:]:
        if b == 0:
            zeros += 1
        else:
            break
    if zeros == length - 1:
        return f"L0_R>={zeros}", w
    if len(w) >= 2 and w[1] == 1:
        z2 = 0
        for b in w[2:]:
            if b == 0:
                z2 += 1
            else:
                break
        return f"B0_Z>={z2}", w
    return f"L0_R={zeros}+tail", w


def shift_u(u):
    if not u:
        return []
    return u[1:] + [0]


def germ_identities(Tmin=5, Tmax=12, R=6):
    """Check proposed identities on every Fibonacci string of exact nvars."""
    checks = {
        "L0_implies_G_T": 0,
        "L0_implies_GT1": 0,
        "L0_implies_FT_Su_0": 0,
        "L0_implies_FT1_Su_1": 0,
        "L0_implies_FT2_Su_1": 0,
        "L0_implies_FT3_Su_0": 0,
        "n_L0": 0,
        "n_fail": 0,
        "fail_examples": [],
    }
    for T in range(Tmin, Tmax + 1):
        if T == 4:
            continue
        L = max(nvars(T + R), 1)
        kmax = max(T + R + 6, 2 * L + 4)
        for u in fib_strings(L):
            F, G = F_of_u(u, kmax)
            if not (F[T] == 1 and all(F[T + d] == 0 for d in range(1, min(R, 4) + 1))):
                continue
            # need at least R>=4 for the full chain; count those with >=4 zeros
            z = 0
            j = T + 1
            while j < len(F) and F[j] == 0:
                z += 1
                j += 1
            if z < 4:
                continue
            checks["n_L0"] += 1
            FS, GS = F_of_u(shift_u(u), kmax)
            ok = (
                G[T] == 1
                and G[T + 1] == 1
                and FS[T] == 0
                and FS[T + 1] == 1
                and FS[T + 2] == 1
                and (z < 5 or FS[T + 3] == 0)
            )
            if ok:
                checks["L0_implies_G_T"] += 1
            else:
                checks["n_fail"] += 1
                if len(checks["fail_examples"]) < 5:
                    checks["fail_examples"].append(
                        {
                            "T": T,
                            "z": z,
                            "u": u[:16],
                            "G": [G[T], G[T + 1]],
                            "FS": window(FS, T, 8),
                        }
                    )
    return checks


def model_shift_table():
    """Last-sat models for the known worst T, and S-images of F."""
    # maxR from period2_certificate through T=32
    worst = [
        (8, 9),
        (16, 9),
        (20, 16),
        (22, 12),
        (12, 6),
        (15, 6),
        (26, 5),
    ]
    rows = []
    for T, R in worst:
        mods = survivors(T, R)
        kinds = Counter()
        images = []
        for u, F, G, kmax in mods[:12]:
            chain = []
            uu = list(u)
            FF = F
            for step in range(0, 6):
                kind, w = classify(FF, T, 12)
                chain.append(
                    {
                        "step": step,
                        "kind": kind,
                        "win": window(FF, max(T - 2, 0), 14),
                        "ones_in_win": window(FF, T, 14).count("1"),
                    }
                )
                kinds[f"s{step}:{kind}"] += 1
                uu = shift_u(uu)
                FF, _ = F_of_u(uu, kmax)
            images.append({"u_head": u[:20], "chain": chain})
        rows.append(
            {
                "T": T,
                "R": R,
                "n_models": len(mods),
                "kind_counts": dict(kinds),
                "sample": images[:3],
            }
        )
    return rows


def rank_candidates():
    """Test whether ones-in-window or last-1 of Su decreases on last-sat models."""
    stats = []
    for T, R in [(8, 9), (16, 9), (20, 16), (22, 12)]:
        mods = survivors(T, R)
        dec_ones = 0
        inc_ones = 0
        dec_last = 0
        inc_last = 0
        n = 0
        for u, F, G, kmax in mods:
            FS, _ = F_of_u(shift_u(u), kmax)
            w0 = F[T : T + R + 1]
            w1 = FS[T : T + R + 1]
            o0 = sum(w0)
            o1 = sum(w1)
            if o1 < o0:
                dec_ones += 1
            elif o1 > o0:
                inc_ones += 1
            def last1(seq, start):
                last = start
                for i, b in enumerate(seq):
                    if b:
                        last = start + i
                return last
            l0 = last1(F, 0)
            l1 = last1(FS, 0)
            if l1 < l0:
                dec_last += 1
            elif l1 > l0:
                inc_last += 1
            n += 1
        stats.append(
            {
                "T": T,
                "R": R,
                "n": n,
                "ones_decrease": dec_ones,
                "ones_increase": inc_ones,
                "last1_decrease": dec_last,
                "last1_increase": inc_last,
            }
        )
    return stats


def periodic_u_zero_runs(periods=None, kmax=240):
    """Max 1-then-zeros run of F on purely periodic Fibonacci u."""
    if periods is None:
        periods = range(1, 13)
    rows = []
    for p in periods:
        for mask in range(1 << p):
            word = [(mask >> i) & 1 for i in range(p)]
            if any(word[i] and word[(i + 1) % p] for i in range(p)):
                continue
            if p > 1 and word == [0] * p:
                continue
            u = (word * ((kmax // 2) // p + 4))[: nvars(kmax) + 2]
            F, _ = F_of_u(u, kmax)
            best = 0
            best_t = None
            run = 0
            run_t = 0
            last_was_one = False
            for i, b in enumerate(F):
                if b == 1:
                    run = 0
                    run_t = i
                    last_was_one = True
                elif last_was_one:
                    run += 1
                    if run > best:
                        best = run
                        best_t = run_t
                else:
                    last_was_one = False
            rows.append(
                {
                    "p": p,
                    "word": "".join(map(str, word)),
                    "maxR": best,
                    "at": best_t,
                    "n1": sum(F),
                }
            )
    rows.sort(key=lambda r: -r["maxR"])
    return rows[:40]


def random_maxR(n_samples=200, ulen=80, kmax=160, seed=0):
    import random

    rng = random.Random(seed)
    best = 0
    witness = None
    hist = Counter()
    for _ in range(n_samples):
        u = []
        last = 0
        for _i in range(ulen):
            if last == 1:
                b = 0
            else:
                b = rng.choice([0, 0, 1])
            u.append(b)
            last = b
        F, _ = F_of_u(u, kmax)
        run = 0
        last_was_one = False
        local = 0
        loc_t = 0
        for i, b in enumerate(F):
            if b == 1:
                run = 0
                last_was_one = True
                t0 = i
            elif last_was_one:
                run += 1
                if run > local:
                    local = run
                    loc_t = t0
            else:
                last_was_one = False
        hist[local] += 1
        if local > best:
            best = local
            witness = {"maxR": local, "at": loc_t, "u_head": u[:24]}
    return {"best": best, "witness": witness, "hist": dict(hist)}


def extend_onset(Tmin, Tmax, Rmax=20):
    """Sound onset table on a T-range; Fibonacci enumeration of exact nvars."""
    rows = []
    cache = {}
    for T in range(Tmin, Tmax + 1):
        maxR = -1
        nmax = 0
        killed = None
        for R in range(0, Rmax + 1):
            top = T + R
            L = max(nvars(top), 1)
            K = top
            if L not in cache or cache[L][0] < K:
                strs = fib_strings(L)
                km = max(K, 2 * L + 2)
                cache[L] = (km, [F_of_u(u, km)[0] for u in strs])
            n = 0
            for F in cache[L][1]:
                if F[T] == 1 and all(F[T + d] == 0 for d in range(1, R + 1)):
                    n += 1
            if n:
                maxR = R
                nmax = n
            else:
                killed = top
                break
        rows.append(
            {"T": T, "max_sat_R": maxR, "n_at_max": nmax, "killed_by": killed}
        )
        if killed is None:
            rows[-1]["cap"] = True
    return rows


def certify():
    ident = germ_identities(5, 14, 6)
    assert ident["n_fail"] == 0, ident["fail_examples"]
    assert ident["n_L0"] > 0
    table = model_shift_table()
    ranks = rank_candidates()
    per = periodic_u_zero_runs()
    rnd = random_maxR()
    # extend T=33..36: nvars(36+16)~27, Fib_27 ~ 317811, may be heavy; do 33-34
    extra = extend_onset(33, 34, 20)
    return {
        "identities": ident,
        "shift_table": table,
        "ranks": ranks,
        "periodic_maxR": per[:15],
        "periodic_global_maxR": per[0]["maxR"] if per else None,
        "random": rnd,
        "onset_33_34": extra,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("identities n_L0", report["identities"]["n_L0"], "fail", report["identities"]["n_fail"])
    print("periodic global maxR", report["periodic_global_maxR"])
    print("random best", report["random"]["best"], report["random"]["hist"])
    print("onset 33-34", report["onset_33_34"])
    print("ranks", report["ranks"])
    for row in report["shift_table"]:
        print(f"T={row['T']} R={row['R']} n={row['n_models']} kinds={row['kind_counts']}")
        if row["sample"]:
            chain = row["sample"][0]["chain"]
            for c in chain:
                print(f"  S^{c['step']} {c['kind']} win={c['win']}")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
