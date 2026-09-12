#!/usr/bin/env python3
"""Cycle FY: unclipped hi-ones count (W/4U)(a + a mod 2); residue walks backward.

On the unified T=2U+W band the unclipped window is s in [t0, clip] with
t0=T-W/2 and clip=U+W. Residue r(s)=(-s-1) mod 2U starts at 2U-1, steps
-1, and ends at U-1; length W/2-U+1. Cycle FW's one-zero residues all
lie in [U-1, 2U-1] and there are N=a+(a mod 2) of them (N even). The
walk is (W/(4U)-1) full periods plus that high half, so the unclipped
hi-ones count is (W/4U)*N and the unclipped hi Green XOR-vanishes. At
clip, m=U-1 and G(m,2U-2)=G(m,0)=G(m,2m)=1. The unclipped formula fails
after clip, and the count depends on W. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fy.py --certify
Dump: research/cycle_fy.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_fw import want_one

OUT = Path(__file__).resolve().with_suffix(".json")
FX_JSON = Path(__file__).resolve().parent / "cycle_fx.json"
FW_JSON = Path(__file__).resolve().parent / "cycle_fw.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"


def n_ones(a: int) -> int:
    """Number of one-zero residues at scale a; always even."""
    return a + (a & 1)


def residue_walk() -> dict:
    """Start 2U-1, step -1, end U-1, length W/2-U+1; count (W/4U)*N."""
    n_ok = 0
    xor_zero = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        N = n_ones(a)
        if N % 2:
            return {"ok": False, "k": k, "N": N}
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            L = clip - t0 + 1
            if L != W // 2 - U + 1:
                return {"ok": False, "k": k, "W": W, "L": L}
            prev = None
            ones = 0
            for i, s in enumerate(range(t0, clip + 1)):
                r = (-s - 1) % (2 * U)
                if i == 0 and r != 2 * U - 1:
                    return {"ok": False, "k": k, "start": r}
                if prev is not None and r != (prev - 1) % (2 * U):
                    return {"ok": False, "k": k, "s": s, "r": r}
                prev = r
                ones += want_one(r, a)
            if prev != U - 1:
                return {"ok": False, "k": k, "end": prev}
            expect = (W // (4 * U)) * N
            if ones != expect:
                return {"ok": False, "k": k, "W": W, "ones": ones, "expect": expect}
            if ones % 2:
                return {"ok": False, "k": k, "W": W, "ones": ones}
            n_ok += 1
            xor_zero += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_zero": xor_zero}


def support_high_half() -> dict:
    """One-zero residues lie in [2^{a-1}-1, 2^a-1]; none in the lower half for a>=2."""
    n_ok = 0
    for a in range(1, 16):
        pa = 1 << a
        lo = (1 << (a - 1)) - 1
        got = []
        for r in range(pa):
            if want_one(r, a):
                if r < lo:
                    return {"ok": False, "a": a, "r": r}
                got.append(r)
        if len(got) != n_ones(a):
            return {"ok": False, "a": a, "n": len(got)}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def clip_corner() -> dict:
    """At s=U+W, m=U-1 and G(m,2U-2)=G(m,0)=G(m,2m)=1."""
    n_ok = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            clip = U + W
            m = T - clip - 1
            if m != U - 1:
                return {"ok": False, "k": k, "m": m}
            g_hi = G(m, 2 * U - 2) if U > 1 else G(m, 0)
            g0 = G(m, 0)
            g2m = G(m, 2 * m)
            if not (g_hi == g0 == g2m == 1):
                return {
                    "ok": False,
                    "k": k,
                    "g_hi": g_hi,
                    "g0": g0,
                    "g2m": g2m,
                }
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def g_matches_walk() -> dict:
    """G(m,2U-2)=want_one(r,k+1) on the full unclipped window, k<=7."""
    n_ok = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, clip + 1):
                m = T - s - 1
                g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                r = (-s - 1) % (2 * U)
                if g != want_one(r, a):
                    return {"ok": False, "k": k, "s": s, "g": g, "r": r}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_after_clip() -> dict:
    """Unclipped G(m,2U-2) fails after clip: k=2, W=8U, s=clip+1."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    clip = U + W
    s = clip + 1
    m = T - s - 1
    g_unclip = G(m, 2 * U - 2)
    g_clip = G(m, 0)
    ok = g_unclip == 0 and g_clip == 1
    return {"ok": ok, "k": k, "s": s, "m": m, "G_unclip": g_unclip, "G_clip": g_clip}


def killed_count_indep_W() -> dict:
    """Ones-count is not independent of W (k=2: 4, 8, 16)."""
    k = 2
    U = 1 << k
    a = k + 1
    counts = {}
    for tag, mul in (("4U", 4), ("8U", 8), ("16U", 16)):
        W = mul * U
        T = 2 * U + W
        t0 = T - W // 2
        clip = U + W
        ones = 0
        for s in range(t0, clip + 1):
            ones += want_one((-s - 1) % (2 * U), a)
        counts[tag] = ones
    ok = counts["4U"] == 4 and counts["8U"] == 8 and counts["16U"] == 16
    return {"ok": ok, **counts}


def killed_whole_window_xor0() -> dict:
    """Whole-window hi Green XOR is not 0: clipped tail has length U-1 (odd for k>=1)."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    a = k + 1
    unclip = 0
    for s in range(t0, clip + 1):
        unclip ^= want_one((-s - 1) % (2 * U), a)
    n_clip = T - clip - 1
    whole = unclip ^ (n_clip & 1)
    ok = unclip == 0 and n_clip == U - 1 and whole == 1
    return {"ok": ok, "k": k, "unclip_xor": unclip, "n_clip": n_clip, "whole_xor": whole}


def prefixes() -> dict:
    fx = json.loads(FX_JSON.read_text())
    fw = json.loads(FW_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ok = (
        fx["checks"]["all_ok"]
        and fw["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and fx["verdict"]["unclipped_hi_eq_want_one_minus_s_minus_1"] == "LEMMA"
        and fw["verdict"]["G_r_2a_minus_2_bit_pattern"] == "LEMMA"
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and fx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    walk: dict,
    supp: dict,
    clip: dict,
    gmatch: dict,
    ka: dict,
    kc: dict,
    kw: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert walk["ok"] and supp["ok"] and clip["ok"] and gmatch["ok"]
    assert ka["ok"] and kc["ok"] and kw["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    walk = residue_walk()
    supp = support_high_half()
    clip = clip_corner()
    gmatch = g_matches_walk()
    ka = killed_after_clip()
    kc = killed_count_indep_W()
    kw = killed_whole_window_xor0()
    pref = prefixes()
    checks = self_checks(c20, walk, supp, clip, gmatch, ka, kc, kw, pref)
    dump = {
        "cycle": "FY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "residue_walk": {k: walk[k] for k in walk if k != "ok"},
        "support_high_half": {k: supp[k] for k in supp if k != "ok"},
        "clip_corner": {k: clip[k] for k in clip if k != "ok"},
        "g_matches_walk": {k: gmatch[k] for k in gmatch if k != "ok"},
        "killed_after_clip": {k: ka[k] for k in ka if k != "ok"},
        "killed_count_indep_W": {k: kc[k] for k in kc if k != "ok"},
        "killed_whole_window_xor0": {k: kw[k] for k in kw if k != "ok"},
        "lemmas": {
            "residue_walk_2U_minus_1_to_U_minus_1": True,
            "unclipped_hi_ones_count": True,
            "unclipped_hi_XOR_vanishes": True,
            "clip_corner_G_eq_1": True,
            "unclipped_formula_after_clip": False,
            "ones_count_independent_of_W": False,
            "whole_window_hi_XOR_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "residue_walk_2U_minus_1_to_U_minus_1": "LEMMA",
            "unclipped_hi_ones_count": "LEMMA",
            "unclipped_hi_XOR_vanishes": "LEMMA",
            "clip_corner_G_eq_1": "LEMMA",
            "unclipped_formula_after_clip": "KILLED",
            "ones_count_independent_of_W": "KILLED",
            "whole_window_hi_XOR_eq_0": "KILLED",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("residue_walk", dump["residue_walk"])


if __name__ == "__main__":
    main()
