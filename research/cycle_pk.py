#!/usr/bin/env python3
"""Cycle PK: covering packed AND xor at p=32 is 1 for k>=5 on q=10.

The left 33 bits are autonomous; the word at t=36 equals t=44, so
even t>=36 has p=32 4-tuple 0100 iff t%8==4, else 0101 / 1110 /
1111, and AND fires iff t%8==4. Covering even s=10U-2n-2 has
s%8==4 iff n%4==1, so for k>=5 (t0=2U>=64>=36) packed AND fires
iff n%4==1 among live G=1. Those n=4t+1 have
G(n, 5U-16)=G(2t, 5*2^{k-1}-8), i.e. Cycle PH's even-n p=16 at
k-1, whose xor is 1. Cycle LG's k<=6 0100 count is this all-k
lemma for k>=5; k=4 xor is 0. Not rest=S xor T. Not E_k=0 for all
k. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_pk.py --certify
Dump: research/cycle_pk.json
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
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lg import want_p32_xor
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import live_lo, p4_count
from cycle_pd import left_step
from cycle_ph import in_p16_even, want_b13, want_b14, want_b15, want_b16
from cycle_pi import want_b17, want_b18
from cycle_pj import want_b19, want_b20, want_b21, want_b22
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PJ_JSON = Path(__file__).resolve().parent / "cycle_pj.json"
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 56
K_THIN = 8
K_SET = 12
PAT0100 = (0, 1, 0, 0)
PAT0101 = (0, 1, 0, 1)
PAT1110 = (1, 1, 1, 0)
PAT1111 = (1, 1, 1, 1)


def want_b29(t: int) -> int:
    """Packed bit 29: 1 iff t%8 in (0, 1, 3, 6) for t>=36."""
    if t < 36:
        return 0
    return int(t % 8 in (0, 1, 3, 6))


def want_b30(t: int) -> int:
    """Packed bit 30 is 1 for t>=36."""
    return int(t >= 36)


def want_b31(t: int) -> int:
    """Packed bit 31: 1 iff t%8 in (0, 3, 5, 6) for t>=36."""
    if t < 36:
        return 0
    return int(t % 8 in (0, 3, 5, 6))


def want_b32(t: int) -> int:
    """Packed bit 32: 1 iff t%8 in (0, 2, 5) for t>=36."""
    if t < 36:
        return 0
    return int(t % 8 in (0, 2, 5))


def want_and32_even(t: int) -> int:
    """Even t>=36: AND at p=32 iff t%8==4."""
    if t < 36 or t % 2:
        return 0
    return int(t % 8 == 4)


def even32_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=36 p=32 4-tuple."""
    r = t % 8
    if r == 4:
        return PAT0100
    if r == 6:
        return PAT1110
    if r == 0:
        return PAT1111
    return PAT0101


def want_p32_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=32, all k."""
    if k <= 2 or k == 4:
        return 0
    return int(k >= 3)


def in_p32_n1(n: int, k: int) -> bool:
    """n%4==1 and G(n, 5*2^k-16)=1, k>=4, via parent even p=16."""
    if k < 4 or n % 4 != 1:
        return False
    U = 1 << k
    if n < live_lo(k, 16) or n >= 4 * U:
        return False
    return in_p16_even((n - 1) // 2, k - 1)


def frozen_b2932() -> dict:
    """t<=N_BIT: bits 29..32 for t>=36; even t>=36 p=32 period 8."""
    row = 1
    n_ok = 0
    n_even = 0
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 33)]
        if t >= 16 and (
            b[13] != want_b13(t)
            or b[14] != want_b14(t)
            or b[15] != want_b15(t)
            or b[16] != want_b16(t)
        ):
            return {"ok": False, "ph": t}
        if t >= 20 and (b[17] != want_b17(t) or b[18] != want_b18(t)):
            return {"ok": False, "pi": t}
        if t >= 28 and (
            b[19] != want_b19(t)
            or b[20] != want_b20(t)
            or b[21] != want_b21(t)
            or b[22] != want_b22(t)
        ):
            return {"ok": False, "pj": t}
        if t >= 36:
            got = (b[29], b[30], b[31], b[32])
            want = (want_b29(t), want_b30(t), want_b31(t), want_b32(t))
            if got != want:
                return {"ok": False, "b2932": t, "got": got, "want": want}
            if t % 2 == 0:
                four = tuple(b[29:33])
                wp = even32_pat(t)
                if four != wp or and_clause(*four) != want_and32_even(t):
                    return {"ok": False, "p32": t, "four": four}
                n_even += 1
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 33) - 1)
            if left_step(word, 32) != (nxt & ((1 << 33) - 1)):
                return {"ok": False, "auto33": t}
        row = nxt
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 34) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t_hi": N_BIT}


def left33_period() -> dict:
    """Left 33 bits autonomous; t=36 equals t=44; even t>=36 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 32
    for t in range(0, N_LEFT + 1):
        word = row & ((1 << (w + 1)) - 1)
        nxt = rule30_step(row)
        if t < N_LEFT:
            want = nxt & ((1 << (w + 1)) - 1)
            if left_step(word, w) != want:
                return {"ok": False, "auto": t}
        rows.append(word)
        row = nxt
        n_ok += 1
    if rows[36] != rows[44]:
        return {"ok": False, "seed": True, "t36": rows[36], "t44": rows[44]}
    n_even = 0
    for t in range(36, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(29, 33))
        if b != even32_pat(t) or and_clause(*b) != want_and32_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 34) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t36": rows[36], "t44": rows[44]}


def green_n1() -> dict:
    """k=4..K_SET: n%4==1 G=1 at p=32 is in_p32_n1; count p4(k-1)."""
    n_ok = 0
    rows = {}
    for k in range(4, K_SET + 1):
        U = 1 << k
        j = 5 * U - 16
        n1 = []
        for n in range(live_lo(k, 16), 4 * U):
            g = G(n, j)
            if n % 4 == 1:
                m = (n - 1) // 2
                pred = G(m, 5 * (U // 2) - 8)
                if g != pred or g != int(in_p32_n1(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g, "pred": pred}
                if g:
                    n1.append(n)
            n_ok += 1
        if len(n1) != p4_count(k - 1) or len(n1) % 2 != 1:
            return {"ok": False, "cnt": True, "k": k, "n": len(n1)}
        if k <= 6:
            rows[str(k)] = {"n1": len(n1), "sample": n1[:4]}
    ok = n_ok > 0 and rows["5"]["n1"] == 5 and rows["6"]["n1"] == 7
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p32() -> dict:
    """k<=K_THIN: covering p=32 xor = want_p32_pack; k>=5 n%4==1 only."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 32, (T - 32) // 2
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_a = n_g = n_and = n_sil = n1 = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                t = (s - t0) // 2
                n = odd_clock(t, U, Q)
                if 0 <= j <= 2 * n:
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                            if n % 4 == 1:
                                n1 += 1
                            if k >= 5 and four != PAT0100:
                                return {"ok": False, "form": True, "k": k, "four": four}
                        else:
                            n_sil += 1
                    if k >= 5:
                        s_even = s - 1
                        if packed != want_and32_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if G(n, j) == 1 and packed != int(n % 4 == 1):
                            return {"ok": False, "parity": True, "k": k, "n": n}
            row = rule30_step(row)
            s += 1
        want = want_p32_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 4 and xor_a != want_p32_xor(k, 10):
            return {"ok": False, "lg": True, "k": k}
        if k >= 5 and (n_and != n1 or n_and != p4_count(k - 1) or t0 < 36):
            return {"ok": False, "split": True, "k": k, "n_and": n_and, "n1": n1}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "n1": n1,
            "j": j,
            "t0": t0,
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["2"]["xor_a"] == 0
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 0
        and rows["5"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pj = json.loads(PJ_JSON.read_text())
    ph = json.loads(PH_JSON.read_text())
    ok = (
        pj["checks"]["all_ok"]
        and ph["checks"]["all_ok"]
        and pj["verdict"]["p22_silent_all_k"] == "LEMMA"
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and pj["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pj["verdict"]["prize"] == "unsolved"
        and want_p32_pack(4) == 0
        and want_p32_pack(5) == 1
        and want_p32_xor(8, 10) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, gre, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert gre["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b2932()
    per = left33_period()
    gre = green_n1()
    thin = thin_p32()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gre, thin, sc, pref)
    dump = {
        "cycle": "PK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b2932": {k: fr[k] for k in fr if k != "ok"},
        "left33_period": {k: per[k] for k in per if k != "ok"},
        "green_n1": {k: gre[k] for k in gre if k != "ok"},
        "thin_p32": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit29_32_mod8": True,
            "and32_even_t_ge_36": True,
            "p32_xor_k_ge_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p32_xor_k_ge_4": False,
            "prize": False,
        },
        "verdict": {
            "bit29_32_mod8": "LEMMA",
            "left33_period8": "LEMMA",
            "and32_even_t_ge_36": "LEMMA",
            "p32_xor_k_ge_5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p32_xor_k_ge_4": "KILLED",
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
    print("frozen_b2932 n_ok", dump["frozen_b2932"]["n_ok"], "n_even", dump["frozen_b2932"]["n_even"])
    print("left33_period n_even", dump["left33_period"]["n_even"])
    print("green_n1 rows", dump["green_n1"]["rows"])
    print("thin_p32 rows", {k: dump["thin_p32"]["rows"][k] for k in ("2", "3", "4", "5", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
