#!/usr/bin/env python3
"""Cycle PZ: covering packed AND xor at p=76 is 1 iff k>=3 and k!=4.

Bits 73..76 freeze from t>=104: bit 73 is 1 iff t%8 not in (1, 4);
bit 74 is 1 iff t%8 in (1, 5, 7); bit 75 is 1 iff t%8 in
(1, 2, 4, 5, 7); bit 76 is 1 iff t%8 in (3, 4, 5). The left 77
bits are autonomous; the word at t=104 equals t=112, so even
t>=104 has p=76 4-tuple 1000 / 1010 / 0011 / 1000 on t%8 =
0,2,4,6, AND iff t%8==4. Covering even s=10U-2n-2 has s%8==4 iff
n%4==1. j=5U-38 is even; j/2 is odd so n%4==0 has G=0. For k>=6
(t0>=128>=104) packed AND on G=1 is 0011 iff n%4==1. Those
n=4t+1 double twice to Green p=20 at k-2, whose xor is 1 for
k>=4, so packed xor is 1 for k>=6. Early even AND-ones are
38,42,60,76,82,84,90,96,100,102; k=3 xor=1, k=4 xor=0, k=5 xor=1.
UNIQUE_REST p=76. Cycle LT's k<=6 0011 odd count is this all-k
lemma for k>=6. Not rest=S xor T. Not unique-rest xor=0. Not
E_k=0 for all k. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pz.py --certify
Dump: research/cycle_pz.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import live_lo
from cycle_pd import left_step
from cycle_pq import cover_nmod
from cycle_py import in_p20, want_b71, want_b72, want_p20_gxor, want_p72_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PY_JSON = Path(__file__).resolve().parent / "cycle_py.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 128
N_LEFT = 128
K_THIN = 8
K_SET = 10
PAT1000 = (1, 0, 0, 0)
PAT1010 = (1, 0, 1, 0)
PAT0011 = (0, 0, 1, 1)
EARLY76 = {38, 42, 60, 76, 82, 84, 90, 96, 100, 102}


def want_b73(t: int) -> int:
    """Packed bit 73: 1 iff t%8 not in (1, 4) for t>=104."""
    if t < 104:
        return 0
    return int(t % 8 not in (1, 4))


def want_b74(t: int) -> int:
    """Packed bit 74: 1 iff t%8 in (1, 5, 7) for t>=104."""
    if t < 104:
        return 0
    return int(t % 8 in (1, 5, 7))


def want_b75(t: int) -> int:
    """Packed bit 75: 1 iff t%8 in (1, 2, 4, 5, 7) for t>=104."""
    if t < 104:
        return 0
    return int(t % 8 in (1, 2, 4, 5, 7))


def want_b76(t: int) -> int:
    """Packed bit 76: 1 iff t%8 in (3, 4, 5) for t>=104."""
    if t < 104:
        return 0
    return int(t % 8 in (3, 4, 5))


def want_and76_even(t: int) -> int:
    """Even t>=104: AND at p=76 iff t%8==4. Early listed."""
    if t % 2:
        return 0
    if t < 104:
        return int(t in EARLY76)
    return int(t % 8 == 4)


def even76_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=104 p=76 4-tuple."""
    r = t % 8
    if r == 2:
        return PAT1010
    if r == 4:
        return PAT0011
    return PAT1000


def want_p76_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=76, all k."""
    return int(k >= 3 and k != 4)


def in_p76_n1(n: int, k: int) -> bool:
    """n%4==1 and G(n, 5*2^k-38)=1, k>=6, via parent p=20 at k-2."""
    if k < 6 or n % 4 != 1:
        return False
    U = 1 << k
    if n < live_lo(k, 38) or n >= 4 * U:
        return False
    return in_p20((n - 1) // 4, k - 2)


def frozen_b7376() -> dict:
    """t<=N_BIT: bits 73..76 for t>=104; even t>=104 AND iff t%8==4."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 77)]
        if t >= 100 and (b[71] != want_b71(t) or b[72] != want_b72(t)):
            return {"ok": False, "py": t}
        if t >= 104:
            got = (b[73], b[74], b[75], b[76])
            want = (want_b73(t), want_b74(t), want_b75(t), want_b76(t))
            if got != want:
                return {"ok": False, "b7376": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[73:77])
            a = and_clause(*four)
            if t >= 104:
                wp = even76_pat(t)
                if four != wp or a != want_and76_even(t):
                    return {"ok": False, "p76": t, "four": four}
                if a and cover_nmod(t) != 1:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 77) - 1)
            if left_step(word, 76) != (nxt & ((1 << 77) - 1)):
                return {"ok": False, "auto77": t}
        row = nxt
    if early != sorted(EARLY76):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 102) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early76": early,
        "t_hi": N_BIT,
    }


def left77_period() -> dict:
    """Left 77 bits autonomous; t=104 equals t=112; even t>=104 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 76
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
    if rows[104] != rows[112]:
        return {"ok": False, "seed": True, "t104": rows[104], "t112": rows[112]}
    n_even = 0
    for t in range(104, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(73, 77))
        if b != even76_pat(t) or and_clause(*b) != want_and76_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 102) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t104": rows[104],
        "t112": rows[112],
    }


def green_n1() -> dict:
    """k=6..K_SET: n%4==1 G=1 at p=76 is in_p76_n1; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 38
        n1 = 0
        xor = 0
        for n in range(live_lo(k, 38), 4 * U):
            g = G(n, j)
            if n % 4 == 1:
                if g != int(in_p76_n1(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n1 += 1
                    xor ^= 1
            n_ok += 1
        if xor != 1 or xor != want_p20_gxor(k - 2):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": n1, "xor": xor}
    ok = n_ok > 0 and rows["6"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p76() -> dict:
    """k<=K_THIN: covering p=76 xor = want_p76_pack; k>=6 form 0011."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 76, (T - 76) // 2
        if j < 0:
            rows[str(k)] = {
                "xor_a": 0,
                "n_g": 0,
                "n_and": 0,
                "n_sil": 0,
                "j": j,
                "t0": t0,
            }
            n_ok += 1
            continue
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_a = n_g = n_and = n_sil = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                tt = (s - t0) // 2
                n = odd_clock(tt, U, Q)
                if 0 <= j <= 2 * n:
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    if k >= 6:
                        s_even = s - 1
                        if packed != want_and76_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 1:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 1):
                            return {"ok": False, "g1": True, "k": k, "n": n}
                        if packed and G(n, j) == 1 and four != PAT0011:
                            return {"ok": False, "form": True, "k": k, "four": four}
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                        else:
                            n_sil += 1
            row = rule30_step(row)
            s += 1
        want = want_p76_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != want_p20_gxor(k - 2):
            return {"ok": False, "p20": True, "k": k, "xor_a": xor_a}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "j": j,
            "t0": t0,
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 0
        and rows["5"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    py = json.loads(PY_JSON.read_text())
    ok = (
        py["checks"]["all_ok"]
        and py["verdict"]["p72_xor_iff_k3"] == "LEMMA"
        and py["verdict"]["p20_gxor_k_ge_4"] == "LEMMA"
        and py["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and py["verdict"]["prize"] == "unsolved"
        and want_p76_pack(3) == 1
        and want_p76_pack(4) == 0
        and want_p76_pack(5) == 1
        and want_p72_pack(3) == 1
        and want_p20_gxor(4) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b7376()
    per = left77_period()
    gr = green_n1()
    thin = thin_p76()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gr, thin, sc, pref)
    dump = {
        "cycle": "PZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b7376": {k: fr[k] for k in fr if k != "ok"},
        "left77_period": {k: per[k] for k in per if k != "ok"},
        "green_n1": {k: gr[k] for k in gr if k != "ok"},
        "thin_p76": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit73_76_mod8": True,
            "and76_even_t_ge_104": True,
            "p76_n1_via_p20": True,
            "p76_xor_iff_k_ge_3_ne_4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p76_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit73_76_mod8": "LEMMA",
            "left77_period8": "LEMMA",
            "and76_even_t_ge_104": "LEMMA",
            "p76_n1_via_p20": "LEMMA",
            "p76_xor_iff_k_ge_3_ne_4": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p76_silent": "KILLED",
            "unique_rest_xor0": "KILLED",
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
    print(
        "frozen_b7376 n_ok",
        dump["frozen_b7376"]["n_ok"],
        "n_even",
        dump["frozen_b7376"]["n_even"],
        "early76",
        dump["frozen_b7376"]["early76"],
    )
    print(
        "thin_p76 rows",
        {k: dump["thin_p76"]["rows"][k] for k in ("3", "4", "5", "8")},
    )
    print("green_n1 rows", dump["green_n1"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
