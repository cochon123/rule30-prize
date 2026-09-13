#!/usr/bin/env python3
"""Cycle OR: unclipped covering-window pal-right S is 1 iff k%4==2.

Prefix xor P(N) of unclipped pal-right S on n<N has P(2^k)=1 iff
k>=4 and k%4==0, from the class split of pal_right_s_pc, the
dyadic xor of r1_pc, and Cycle ON's fold. Covering n runs through
[0,4U), so the unclipped covering-window xor is P(4U)=1 iff k>=2
and k%4==2. The clip window (5U/2,4U) has unclipped xor 0, because
P(5U/2+1)=P(4U). Covering S is that bit xor the clip-removed
pal-right S xor, and still vanishes on even n. Not covering S
itself (k=2,8,10 clip-removed is 1). Not E_k=0 for all k. Do not
catalogue further S/T subregions unless the experiment answers
why E_k=0. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_or.py --certify
Dump: research/cycle_or.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal, want_cover_t
from cycle_ok import pal_right_s
from cycle_oq import pal_right_s_pc, r1_pc, r2_pc

OUT = Path(__file__).resolve().with_suffix(".json")
OQ_JSON = Path(__file__).resolve().parent / "cycle_oq.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"

N_PAL = 64
M_SLOTS = 64
K_P2 = 12
A_HI = 12
K_COVER = 8
B_SHIFT = 8


def want_Q1_pow2(a: int) -> int:
    """xor_{t<2^a} r1_pc(t)."""
    if a <= 0:
        return 0
    if a == 1:
        return 1
    if a % 2:
        return 0
    return 1


def want_P_pow2(k: int) -> int:
    """xor of pal_right_s_pc on n<2^k."""
    return int(k >= 4 and k % 4 == 0)


def want_unclip_cover(k: int) -> int:
    """Unclipped pal-right S xor on covering n<4U=2^{k+2}."""
    return int(k >= 2 and k % 4 == 2)


def want_cover_s_e0(k: int) -> int:
    """Covering S if E=0: rest10 xor T."""
    return want_rest10(k, 10) ^ want_cover_t(k)


def clipped_s(n: int, jmax: int) -> int:
    """Pal-right S-xor of G(j+1) on cells with j<=jmax."""
    xor_s = 0
    hi = min(2 * n, jmax)
    for j in range(n + 1, hi + 1):
        if G(n, j) == 0:
            continue
        if (j - n) % 3 != 1:
            continue
        if G(n, j - 1) != 0:
            continue
        xor_s ^= G(n, j + 1)
    return xor_s


def r1_high_bit() -> dict:
    """j<2^b: r1(2^{b+2}+j)==r1(j) xor 1, except b odd and j=0."""
    n_ok = n_flip = 0
    sample = {}
    for b in range(1, B_SHIFT + 1):
        L = 1 << b
        for j in range(L):
            got = r1_pc((1 << (b + 2)) + j)
            want = r1_pc(j) ^ 1
            if b % 2 and j == 0:
                want = 0
            if got != want:
                return {"ok": False, "b": b, "j": j, "got": got, "want": want}
            n_ok += 1
            n_flip += int(got != r1_pc(j))
        if b <= 4:
            sample[str(b)] = {
                "j0": r1_pc(1 << (b + 2)),
                "flip0": int(not (b % 2)),
            }
    ok = (
        n_ok == sum(1 << b for b in range(1, B_SHIFT + 1))
        and sample["1"]["j0"] == 0
        and sample["2"]["j0"] == 1
        and n_flip > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_flip": n_flip, "sample": sample}


def q1_pow2() -> dict:
    """a<=A_HI: xor_{t<2^a} r1_pc(t)==want_Q1_pow2(a)."""
    n_ok = 0
    sample = {}
    acc = 0
    t = 0
    for a in range(0, A_HI + 1):
        while t < (1 << a):
            acc ^= r1_pc(t)
            t += 1
        if acc != want_Q1_pow2(a):
            return {"ok": False, "a": a, "got": acc, "want": want_Q1_pow2(a)}
        n_ok += 1
        if a <= 6:
            sample[str(a)] = acc
    ok = (
        n_ok == A_HI + 1
        and sample["0"] == 0
        and sample["1"] == 1
        and sample["2"] == 1
        and sample["3"] == 0
        and sample["4"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "a_hi": A_HI, "sample": sample}


def q5_five() -> dict:
    """b<A_HI: xor_{t<5*2^b} r2_pc(2t+1) is 1 iff b<=1."""
    n_ok = 0
    sample = {}
    for b in range(0, min(A_HI, 8)):
        acc = 0
        N = 5 << b
        for t in range(N):
            acc ^= r2_pc(2 * t + 1)
        want = int(b <= 1)
        if acc != want:
            return {"ok": False, "b": b, "got": acc, "want": want}
        n_ok += 1
        if b <= 4:
            sample[str(b)] = acc
    ok = n_ok >= 8 and sample["0"] == 1 and sample["1"] == 1 and sample["2"] == 0
    return {"ok": ok, "n_ok": n_ok, "sample": sample}


def p_pow2() -> dict:
    """k<=K_P2: P(2^k)==want_P_pow2(k)."""
    n_ok = n_one = 0
    sample = {}
    acc = 0
    n = 0
    for k in range(0, K_P2 + 1):
        while n < (1 << k):
            acc ^= pal_right_s_pc(n)
            n += 1
        if acc != want_P_pow2(k):
            return {"ok": False, "k": k, "got": acc, "want": want_P_pow2(k)}
        n_ok += 1
        n_one += acc
        if k <= 8:
            sample[str(k)] = acc
    ok = (
        n_ok == K_P2 + 1
        and sample["3"] == 0
        and sample["4"] == 1
        and sample["5"] == 0
        and sample["8"] == 1
        and n_one == sum(want_P_pow2(k) for k in range(0, K_P2 + 1))
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "sample": sample}


def hi_unclip() -> dict:
    """a<=A_HI: P(5*2^a+1)==P(2^{a+3})==want_P_pow2(a+3)."""
    n_max = 1 << (A_HI + 3)
    acc = 0
    P = [0] * (n_max + 1)
    for n in range(n_max):
        P[n] = acc
        acc ^= pal_right_s_pc(n)
    P[n_max] = acc
    n_ok = 0
    sample = {}
    for a in range(0, A_HI + 1):
        p5 = P[5 * (1 << a) + 1]
        p8 = P[1 << (a + 3)]
        want = want_P_pow2(a + 3)
        if p5 != p8 or p8 != want:
            return {
                "ok": False,
                "a": a,
                "P5": p5,
                "P8": p8,
                "want": want,
            }
        n_ok += 1
        if a <= 5:
            sample[str(a)] = {"P5": p5, "P8": p8}
    ok = (
        n_ok == A_HI + 1
        and sample["0"]["P5"] == 0
        and sample["1"]["P5"] == 1
        and sample["2"]["P5"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "a_hi": A_HI, "sample": sample}


def even_clip() -> dict:
    """Even n covering S still vanishes under q=10 clip j<=5U."""
    n_ok = 0
    for k in range(0, 6):
        U = 1 << k
        jmax = 5 * U
        for n in range(0, 4 * U, 2):
            if clipped_s(n, jmax) != 0 or pal_right_s(n)[0] != 0:
                return {"ok": False, "k": k, "n": n}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def covering_s_clip() -> dict:
    """q=10 k<=K_COVER: covering S = unclip xor rem; rem nonzero at k=2,8."""
    na = json.loads(NA_JSON.read_text())
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        jmax = T // 2
        cut = (5 * U) // 2
        xor_s = xor_even = xor_rem = xor_unclip = 0
        t = 0
        s = t0 + 1
        while s < T:
            n = odd_clock(t, U, Q)
            cs = clipped_s(n, jmax)
            xor_s ^= cs
            xor_unclip ^= pal_right_s_pc(n)
            if n % 2 == 0:
                xor_even ^= cs
            if n > cut:
                xor_rem ^= pal_right_s_pc(n) ^ cs
            t += 1
            s += 2
        unclip = want_unclip_cover(k)
        e0 = want_cover_s_e0(k)
        na_s = na["q10_green_rest"]["rows"][str(k)]["xor_s"]
        if (
            xor_even != 0
            or xor_unclip != unclip
            or xor_s != unclip ^ xor_rem
            or xor_s != e0
            or xor_s != na_s
        ):
            return {
                "ok": False,
                "k": k,
                "xor_s": xor_s,
                "unclip": xor_unclip,
                "rem": xor_rem,
                "even": xor_even,
                "want_unclip": unclip,
                "e0": e0,
                "na_s": na_s,
            }
        rows[str(k)] = {
            "xor_s": xor_s,
            "unclip": xor_unclip,
            "rem": xor_rem,
            "e0": e0,
        }
        n_ok += 1
    ok = (
        n_ok == K_COVER + 1
        and rows["2"]["unclip"] == 1
        and rows["2"]["rem"] == 1
        and rows["2"]["xor_s"] == 0
        and rows["6"]["xor_s"] == 1
        and rows["6"]["rem"] == 0
        and rows["8"]["xor_s"] == 1
        and rows["8"]["unclip"] == 0
        and rows["8"]["rem"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": rows}


def killed_eq_unclip(cover: dict) -> dict:
    r2, r8 = cover["rows"]["2"], cover["rows"]["8"]
    ok = r2["xor_s"] != r2["unclip"] and r8["xor_s"] != r8["unclip"]
    return {"ok": ok, "k2": r2["xor_s"], "u2": r2["unclip"], "k8": r8["xor_s"], "u8": r8["unclip"]}


def killed_mod4(cover: dict) -> dict:
    r2 = cover["rows"]["2"]
    ok = r2["xor_s"] == 0 and want_unclip_cover(2) == 1
    return {"ok": ok, "k": 2, "xor_s": 0, "unclip": 1}


def prefixes() -> dict:
    oq = json.loads(OQ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    ok = (
        oq["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and oq["verdict"]["s_pc"] == "LEMMA"
        and oq["verdict"]["r0_popcount"] == "LEMMA"
        and oq["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oq["verdict"]["covering_S"] == "PREFIX"
        and oq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, shift, q1, q5, p2, hi, ev, cover, ku, km, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and shift["ok"]
        and q1["ok"]
        and q5["ok"]
        and p2["ok"]
        and hi["ok"]
        and ev["ok"]
        and cover["ok"]
        and ku["ok"]
        and km["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    shift = r1_high_bit()
    q1 = q1_pow2()
    q5 = q5_five()
    p2 = p_pow2()
    hi = hi_unclip()
    ev = even_clip()
    cover = covering_s_clip()
    ku = killed_eq_unclip(cover)
    km = killed_mod4(cover)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, pal, slots, shift, q1, q5, p2, hi, ev, cover, ku, km, sc, pref
    )
    dump = {
        "cycle": "OR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "r1_high_bit": {k: shift[k] for k in shift if k != "ok"},
        "q1_pow2": {k: q1[k] for k in q1 if k != "ok"},
        "q5_five": {k: q5[k] for k in q5 if k != "ok"},
        "p_pow2": {k: p2[k] for k in p2 if k != "ok"},
        "hi_unclip": {k: hi[k] for k in hi if k != "ok"},
        "even_clip": {k: ev[k] for k in ev if k != "ok"},
        "covering_s_clip": {k: cover[k] for k in cover if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_unclip": {k: ku[k] for k in ku if k != "ok"},
        "killed_mod4": {k: km[k] for k in km if k != "ok"},
        "lemmas": {
            "P_pow2": True,
            "unclip_cover": True,
            "hi_unclip": True,
            "even_clip": True,
            "s_pc": True,
            "r0_popcount": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "eq_unclip": False,
            "mod4_is_cover": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "P_pow2": "LEMMA",
            "unclip_cover": "LEMMA",
            "hi_unclip": "LEMMA",
            "even_clip": "LEMMA",
            "s_pc": "LEMMA",
            "r0_popcount": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "covering_s_k8": "CERTIFIED",
            "eq_unclip": "KILLED",
            "mod4_is_cover": "KILLED",
            "covering_S": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("p_pow2 n_ok", dump["p_pow2"]["n_ok"], "n_one", dump["p_pow2"]["n_one"])
    print("hi_unclip n_ok", dump["hi_unclip"]["n_ok"])
    print("covering_s_clip", dump["covering_s_clip"]["rows"])
    print("killed_eq_unclip", dump["killed_eq_unclip"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
