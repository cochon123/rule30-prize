#!/usr/bin/env python3
"""Cycle PH: covering packed AND xor at p=16 is 1 for k>=3 on q=10.

The left 17 bits are autonomous; the word at t=16 equals t=20, so
even t>=16 has bits 13..16 equal to 1001 iff t%4==2 else 1111.
AND at p=16 therefore fires iff t%4==2. Covering even s=10U-2n-2
has s%4==2 iff n is even, so for k>=3 (t0=2U>=16) packed AND
fires iff n is even among live G=1. Odd G=1 are all silent.
Even-n Green G(n, 5U-8)=1 iff the parent covering p=8 cell fires.
For k>=2, odd Green at p=8 is {3U-3, 3U-1} (in_p4 xor in_p6 of
the parent), even Green is {2s: in_p4(s, k-1)}, so parent xor is
1 and packed p=16 xor is 1. Cycle LE's k<=6 count is the all-k
lemma. Not rest=S xor T. Not E_k=0 for all k. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ph.py --certify
Dump: research/cycle_ph.json
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
from cycle_le import want_p16_xor
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import in_p4, in_p6, live_lo, p4_count
from cycle_pd import left_step
from cycle_pf import want_b7, want_b8, want_b9
from cycle_pg import want_b10
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PG_JSON = Path(__file__).resolve().parent / "cycle_pg.json"
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 48
K_THIN = 8
K_SET = 12
PAT1001 = (1, 0, 0, 1)
PAT1111 = (1, 1, 1, 1)
PAT0011 = (0, 0, 1, 1)
PAT1110 = (1, 1, 1, 0)


def want_b13(t: int) -> int:
    """Packed bit 13: 1 iff t%4 != 3 for t>=16."""
    if t < 16:
        return 0
    return int(t % 4 != 3)


def want_b14(t: int) -> int:
    """Packed bit 14: 1 iff t%4 in (0, 1) for t>=16."""
    if t < 16:
        return 0
    return int(t % 4 in (0, 1))


def want_b15(t: int) -> int:
    """Packed bit 15: 1 iff t%4 in (0, 3) for t>=16."""
    if t < 16:
        return 0
    return int(t % 4 in (0, 3))


def want_b16(t: int) -> int:
    """Packed bit 16: 1 iff t%4 != 1 for t>=16."""
    if t < 16:
        return 0
    return int(t % 4 != 1)


def want_and16_even(t: int) -> int:
    """Even t>=16: AND at p=16 iff t%4==2."""
    if t < 16 or t % 2:
        return 0
    return int(t % 4 == 2)


def want_p16_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=16, all k."""
    return int(k >= 3)


def in_p8(n: int, k: int) -> bool:
    """G(n, 5*2^k-4)=1 on the covering live window, k>=2."""
    U = 1 << k
    if k < 2 or n < live_lo(k, 4) or n >= 4 * U:
        return False
    if n % 2 == 1:
        return n in (3 * U - 3, 3 * U - 1)
    return in_p4(n // 2, k - 1)


def in_p16_even(n: int, k: int) -> bool:
    """Even n with G(n, 5*2^k-8)=1, k>=3."""
    if k < 3 or n % 2 == 1:
        return False
    U = 1 << k
    if n < live_lo(k, 8) or n >= 4 * U:
        return False
    return in_p8(n // 2, k - 1)


def frozen_b1316() -> dict:
    """t<=N_BIT: bits 13..16 for t>=16; even t>=16 p=16 is 1001 or 1111."""
    row = 1
    n_ok = 0
    n_even = 0
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 17)]
        if b[7] != want_b7(t) or b[8] != want_b8(t) or b[9] != want_b9(t):
            return {"ok": False, "pf": t}
        if b[10] != want_b10(t):
            return {"ok": False, "pg": t, "got": b[10]}
        if t >= 12 and t % 2 == 0:
            b1114 = tuple(b[11:15])
            w1114 = PAT0011 if t % 4 == 0 else PAT1110
            if b1114 != w1114:
                return {"ok": False, "p1114": t, "got": b1114}
        if t >= 16:
            if (
                b[13] != want_b13(t)
                or b[14] != want_b14(t)
                or b[15] != want_b15(t)
                or b[16] != want_b16(t)
            ):
                return {"ok": False, "b1316": t, "got": b[13:17]}
            if t % 2 == 0:
                four = tuple(b[13:17])
                want = PAT1001 if t % 4 == 2 else PAT1111
                if four != want or and_clause(*four) != want_and16_even(t):
                    return {"ok": False, "p16": t, "four": four, "want": list(want)}
                n_even += 1
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 17) - 1)
            if left_step(word, 16) != (nxt & ((1 << 17) - 1)):
                return {"ok": False, "auto": t}
        row = nxt
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 14) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t_hi": N_BIT}


def left17_period() -> dict:
    """Left 17 bits autonomous; t=16 equals t=20; even t>=16 period 4."""
    row = 1
    rows = []
    n_ok = 0
    w = 16
    for t in range(0, N_LEFT + 1):
        word = row & ((1 << (w + 1)) - 1)
        nxt = rule30_step(row)
        if t < N_LEFT:
            want = nxt & ((1 << (w + 1)) - 1)
            if left_step(word, w) != want:
                return {"ok": False, "auto": t, "got": left_step(word, w), "want": want}
        rows.append(word)
        row = nxt
        n_ok += 1
    if rows[16] != rows[20]:
        return {"ok": False, "seed": True, "t16": rows[16], "t20": rows[20]}
    b16 = tuple((rows[16] >> p) & 1 for p in range(13, 17))
    b18 = tuple((rows[18] >> p) & 1 for p in range(13, 17))
    if b16 != PAT1111 or b18 != PAT1001:
        return {"ok": False, "pats": True, "b16": b16, "b18": b18}
    if and_clause(*b16) != 0 or and_clause(*b18) != 1:
        return {"ok": False, "and": True}
    n_even = 0
    for t in range(16, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(13, 17))
        want = PAT1001 if t % 4 == 2 else PAT1111
        if b != want:
            return {"ok": False, "per": t, "got": b, "want": list(want)}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 14) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t16": rows[16], "t20": rows[20]}


def green_p8_p16() -> dict:
    """k<=K_SET: p=8 set; even-n p=16 set; doubling matches G."""
    n_ok = 0
    rows = {}
    for k in range(2, K_SET + 1):
        U = 1 << k
        j8 = 5 * U - 4
        even8 = []
        odd8 = []
        for n in range(live_lo(k, 4), 4 * U):
            g = G(n, j8)
            m = n // 2
            if n % 2 == 0:
                pred = G(m, 5 * (U // 2) - 2)
            else:
                pred = G(m, 5 * (U // 2) - 2) ^ G(m, 5 * (U // 2) - 3)
                if pred != (in_p4(m, k - 1) ^ in_p6(m, k - 1)):
                    return {"ok": False, "xor46": True, "k": k, "n": n}
            if g != pred:
                return {"ok": False, "double8": True, "k": k, "n": n}
            if g != int(in_p8(n, k)):
                return {"ok": False, "in8": True, "k": k, "n": n, "g": g}
            if g:
                (even8 if n % 2 == 0 else odd8).append(n)
            n_ok += 1
        if odd8 != [3 * U - 3, 3 * U - 1]:
            return {"ok": False, "odd8": True, "k": k, "odd": odd8}
        if len(even8) != p4_count(k - 1) or (len(even8) + 2) % 2 != 1:
            return {"ok": False, "even8": True, "k": k, "n": len(even8)}
        if k >= 3:
            j16 = 5 * U - 8
            even16 = []
            n_odd_g = 0
            for n in range(live_lo(k, 8), 4 * U):
                g = G(n, j16)
                if n % 2 == 0:
                    pred = G(n // 2, 5 * (U // 2) - 4)
                    if g != pred or g != int(in_p16_even(n, k)):
                        return {"ok": False, "p16e": True, "k": k, "n": n}
                    if g:
                        even16.append(n)
                elif g:
                    n_odd_g += 1
                n_ok += 1
            if len(even16) != p4_count(k) or len(even16) % 2 != 1:
                return {"ok": False, "n16": True, "k": k, "n": len(even16)}
            if k <= 5:
                rows[str(k)] = {
                    "odd8": odd8,
                    "n_even8": len(even8),
                    "n_even16": len(even16),
                    "n_odd16": n_odd_g,
                }
        elif k <= 5:
            rows[str(k)] = {"odd8": odd8, "n_even8": len(even8)}
    ok = (
        n_ok > 0
        and rows["2"]["odd8"] == [9, 11]
        and rows["3"]["n_even16"] == 5
        and rows["3"]["n_odd16"] >= 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p16() -> dict:
    """k<=K_THIN: covering p=16 AND xor = want_p16_pack; k>=3 even-n only."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 16, (T - 16) // 2
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_a = n_g = n_and = n_sil = n_even_g = n_odd_g = 0
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
                        if n % 2 == 0:
                            n_even_g += 1
                        else:
                            n_odd_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                            if four != PAT1001:
                                return {"ok": False, "form": True, "k": k, "four": four}
                        else:
                            n_sil += 1
                    if k >= 3:
                        if packed != want_and16_even(s):
                            return {"ok": False, "and": True, "k": k, "s": s}
                        if G(n, j) == 1 and packed != int(n % 2 == 0):
                            return {"ok": False, "parity": True, "k": k, "n": n}
            row = rule30_step(row)
            s += 1
        if xor_a != want_p16_pack(k) or xor_a != want_p16_xor(k, 10):
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a}
        if k >= 3 and (n_and != n_even_g or n_sil != n_odd_g or n_and != p4_count(k)):
            return {
                "ok": False,
                "split": True,
                "k": k,
                "n_and": n_and,
                "n_even_g": n_even_g,
                "n_sil": n_sil,
            }
        if k >= 3 and t0 < 16:
            return {"ok": False, "t0": k, "t0v": t0}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "n_even_g": n_even_g,
            "n_odd_g": n_odd_g,
            "j": j,
            "t0": t0,
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["xor_a"] == 0
        and rows["2"]["xor_a"] == 0
        and rows["2"]["n_and"] == 2
        and rows["3"]["xor_a"] == 1
        and rows["3"]["n_and"] == 5
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pg = json.loads(PG_JSON.read_text())
    pd = json.loads(PD_JSON.read_text())
    ok = (
        pg["checks"]["all_ok"]
        and pd["checks"]["all_ok"]
        and pg["verdict"]["p12_silent_k_ge_2"] == "LEMMA"
        and pg["verdict"]["bit10_mod4"] == "LEMMA"
        and pd["verdict"]["p14_period4"] == "LEMMA"
        and pg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pg["verdict"]["prize"] == "unsolved"
        and want_p16_pack(2) == 0
        and want_p16_pack(3) == 1
        and want_p16_xor(8, 10) == 1
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
    fr = frozen_b1316()
    per = left17_period()
    gre = green_p8_p16()
    thin = thin_p16()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gre, thin, sc, pref)
    dump = {
        "cycle": "PH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b1316": {k: fr[k] for k in fr if k != "ok"},
        "left17_period": {k: per[k] for k in per if k != "ok"},
        "green_p8_p16": {k: gre[k] for k in gre if k != "ok"},
        "thin_p16": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit13_16_mod4": True,
            "and16_even_t_ge_16": True,
            "p8_odd_two": True,
            "p16_xor_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p16_silent": False,
            "prize": False,
        },
        "verdict": {
            "bit13_16_mod4": "LEMMA",
            "left17_period4": "LEMMA",
            "and16_even_t_ge_16": "LEMMA",
            "p8_odd_two_k_ge_2": "LEMMA",
            "p16_xor_k_ge_3": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p16_silent": "KILLED",
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
    print("frozen_b1316 n_ok", dump["frozen_b1316"]["n_ok"], "n_even", dump["frozen_b1316"]["n_even"])
    print("left17_period n_even", dump["left17_period"]["n_even"])
    print("green_p8_p16 rows", dump["green_p8_p16"]["rows"])
    print("thin_p16 rows", {k: dump["thin_p16"]["rows"][k] for k in ("0", "2", "3", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
