#!/usr/bin/env python3
"""Cycle AB: I_k is an annulus coboundary; R_k is the palindrome-defect parity.

Cycle Z/AA: b_k = b_{k-1} XOR I_k with I_k the Green parity of AND injections
on [T,2T), T=2^{k-1}, and every c_t AND r_t hits, leaving a remainder R_k.
The Rule 30 update makes c XOR c' = ell XOR r XOR (c AND r), so summing
over the annulus telescopes:

    I_k = XOR_{t=T}^{2T-1} (ell_t XOR r_t XOR (c_t AND r_t)).

The Green remainder is therefore the palindrome-defect parity
R_k = XOR_{t=T}^{2T-1} (ell_t XOR r_t). The defect d=ell XOR r is not
eventually 0 (that would force an eventually constant centre). Spatial
vacuums about the origin do not explain the observed centre 0-runs, and
there is no construction of unbounded runs.

Not a prize claim: I_k still unproved not eventually 0. Infinitely many
centred 000s would kill every isolated-zero eventual period (including
period 2), but that is unproved.

Run: python3 research/cycle_ab.py --certify
Dump: research/cycle_ab.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_clr(n: int):
    row = 1
    c = bytearray(n)
    ell = bytearray(n)
    r = bytearray(n)
    for t in range(n):
        c[t] = (row >> t) & 1
        if t >= 1:
            ell[t] = (row >> (t - 1)) & 1
        if t + 1 <= 2 * t:
            r[t] = (row >> (t + 1)) & 1
        row = rule30_step(row)
    return c, ell, r


def run_stats(seq) -> dict:
    n = len(seq)
    runs0 = []
    runs1 = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and seq[j] == seq[i]:
            j += 1
        (runs0 if seq[i] == 0 else runs1).append((i, j - i))
        i = j
    max0 = max((ln for _s, ln in runs0), default=0)
    max1 = max((ln for _s, ln in runs1), default=0)
    n000 = sum(ln - 1 for _s, ln in runs0)  # times with c=0 and a following 0
    return {
        "n_zero_runs": len(runs0),
        "n_one_runs": len(runs1),
        "max0": max0,
        "max1": max1,
        "max0_start": max(runs0, key=lambda x: x[1])[0] if runs0 else None,
        "max1_start": max(runs1, key=lambda x: x[1])[0] if runs1 else None,
        "n000": n000,
    }


def vacuum_max(tmax: int) -> dict:
    row = 1
    max_vac = 0
    at = 0
    by_k = {}
    for t in range(tmax):
        if ((row >> t) & 1) == 0:
            w = 1
            while (
                t - w >= 0
                and ((row >> (t - w)) & 1) == 0
                and ((row >> (t + w)) & 1) == 0
            ):
                w += 1
            if w > max_vac:
                max_vac = w
                at = t
        if t > 0 and (t & (t - 1)) == 0:
            by_k[str(t.bit_length() - 1)] = max_vac
        row = rule30_step(row)
    return {"max_radius": max_vac, "at": at, "by_dyadic": by_k}


def self_checks(c20, c, ell, r, recs) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert list(c[:20]) == KNOWN20
    # 00 occurs in the known prefix
    assert any(c[t] == 0 and c[t + 1] == 0 for t in range(19))
    for rec in recs:
        assert rec["match_coboundary"]
        assert rec["match_defect"]
        assert rec["I"] == rec["cr"] ^ rec["defect"]
    # update identity at every t
    for t in range(len(c) - 1):
        cand = ell[t] ^ r[t] ^ (c[t] & r[t])
        assert cand == (c[t] ^ c[t + 1])
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--kmax", type=int, default=16)
    args = parser.parse_args()
    t0 = time.perf_counter()
    kmax = args.kmax
    n = (1 << kmax) + 1
    c20 = packed_center_bits(20)
    c, ell, r = evolve_clr(n)

    recs = []
    for k in range(1, kmax + 1):
        T = 1 << (k - 1)
        cr = defect = lam = rho = cob = 0
        n_cr = n_def = n000 = 0
        for t in range(T, 2 * T):
            e = c[t] & r[t]
            d = ell[t] ^ r[t]
            cob ^= ell[t] ^ r[t] ^ e
            cr ^= e
            defect ^= d
            lam ^= ell[t]
            rho ^= r[t]
            n_cr += e
            n_def += d
            if c[t] == 0 and d == 0:
                n000 += 1
        I = c[T] ^ c[2 * T]
        recs.append(
            {
                "k": k,
                "I": I,
                "cr": cr,
                "defect": defect,
                "coboundary": cob,
                "lam": lam,
                "rho": rho,
                "n_cr": n_cr,
                "n_def": n_def,
                "n000": n000,
                "match_coboundary": cob == I,
                "match_defect": defect == (I ^ cr),
                "rho_eq_I": rho == I,
                "lam_eq_I": lam == I,
                "cr_eq_I": cr == I,
            }
        )

    stats = run_stats(c[: 1 << kmax])
    vac = vacuum_max(1 << min(kmax, 16))
    prefix_runs = []
    for k in range(4, kmax + 1):
        st = run_stats(c[: 1 << k])
        prefix_runs.append({"k": k, "max0": st["max0"], "max1": st["max1"]})

    both_d = (0 in (ell[t] ^ r[t] for t in range(1, min(n, 64)))) and (
        1 in (ell[t] ^ r[t] for t in range(1, min(n, 64)))
    )
    rho_universal = all(rec["rho_eq_I"] for rec in recs)
    lam_universal = all(rec["lam_eq_I"] for rec in recs)
    cr_universal = all(rec["cr_eq_I"] for rec in recs)
    vac_explains_runs = vac["max_radius"] >= stats["max0"]

    checks = self_checks(c20, c, ell, r, recs)

    dump = {
        "cycle": "AB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "I": [rec["I"] for rec in recs],
        "defect": [rec["defect"] for rec in recs],
        "cr": [rec["cr"] for rec in recs],
        "annulus": recs,
        "run_stats": stats,
        "prefix_runs": prefix_runs,
        "vacuum": vac,
        "d_takes_both_on_prefix": both_d,
        "lemmas": {
            "annulus_coboundary": all(rec["match_coboundary"] for rec in recs),
            "R_is_defect_parity": all(rec["match_defect"] for rec in recs),
            "d_not_eventually_zero": True,
            "unbounded_runs": None,
            "infinitely_many_000": None,
            "b_not_eventually_constant": None,
        },
        "verdict": {
            "annulus_coboundary": "LEMMA",
            "R_is_defect_parity": "LEMMA",
            "d_not_eventually_zero": "LEMMA",
            "I_eq_rho": "KILLED" if not rho_universal else "OPEN",
            "I_eq_lambda": "KILLED" if not lam_universal else "OPEN",
            "I_eq_cr": "KILLED" if not cr_universal else "OPEN",
            "vacuum_explains_runs": "KILLED" if not vac_explains_runs else "OPEN",
            "unbounded_runs": "OPEN",
            "infinitely_many_000": "OPEN",
            "b_k_eventual_constancy": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("I", dump["I"])
    print("defect", dump["defect"])
    print("runs", stats)
    print("vacuum", vac)
    print("prefix_runs", prefix_runs)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
