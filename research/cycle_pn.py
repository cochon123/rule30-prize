#!/usr/bin/env python3
"""Cycle PN: covering packed AND xor at p=38 is 1 iff k in (2, 3).

Bit 35 is 1 iff t%8 in (5, 6, 7) for t>=48; bit 36 is 1 iff t%8
in (0, 4, 7); bit 37 is 1 iff t%8 not in (0, 6); bit 38 is 1 iff
t%8 not in (0, 5). The left 39 bits are autonomous; the word at
t=48 equals t=56, so even t>=48 has p=38 4-tuple 0100 / 0011 /
0111 / 1001 on t%8 = 0,2,4,6. AND fires iff t%8 in (0, 2, 6).
Covering even s=10U-2n-2 has AND iff n%4 != 1. j=5U-19 is odd so
even n have G=0. For k>=5 (t0=2U>=64>=48) packed AND fires iff
n%4==3 among live G=1. Those n=4t+3 double to parent p=10 xor
p=12 at k-2. Green p=12 xor is parent p=8 xor, hence 1 for k>=3,
and Cycle PM p=10 xor is 1 for k>=2, so the n%4==3 xor is 0 for
k>=5. Packed xor is 1 iff k in (2, 3). Cycle LN's k<=6 0100 xor=0
is this all-k lemma for k>=5. Not rest=S xor T. Not E_k=0 for all
k. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_pn.py --certify
Dump: research/cycle_pn.json
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
from cycle_ln import want_p38_xor
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import in_p6, live_lo
from cycle_pd import left_step
from cycle_ph import in_p8
from cycle_pm import in_p10, want_b27, want_b28, want_p10_gxor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 64
K_THIN = 8
K_SET = 12
PAT0100 = (0, 1, 0, 0)
PAT0011 = (0, 0, 1, 1)
PAT0111 = (0, 1, 1, 1)
PAT1001 = (1, 0, 0, 1)
EARLY38 = {18, 20, 34, 40, 44}


def want_b35(t: int) -> int:
    """Packed bit 35: 1 iff t%8 in (5, 6, 7) for t>=48."""
    if t < 48:
        return 0
    return int(t % 8 in (5, 6, 7))


def want_b36(t: int) -> int:
    """Packed bit 36: 1 iff t%8 in (0, 4, 7) for t>=48."""
    if t < 48:
        return 0
    return int(t % 8 in (0, 4, 7))


def want_b37(t: int) -> int:
    """Packed bit 37: 1 iff t%8 not in (0, 6) for t>=48."""
    if t < 48:
        return 0
    return int(t % 8 not in (0, 6))


def want_b38(t: int) -> int:
    """Packed bit 38: 1 iff t%8 not in (0, 5) for t>=48."""
    if t < 48:
        return 0
    return int(t % 8 not in (0, 5))


def want_and38_even(t: int) -> int:
    """Even t>=48: AND at p=38 iff t%8 in (0, 2, 6)."""
    if t < 48 or t % 2:
        return int(t in EARLY38)
    return int(t % 8 in (0, 2, 6))


def even38_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=48 p=38 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0100
    if r == 2:
        return PAT0011
    if r == 4:
        return PAT0111
    return PAT1001


def want_p38_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=38, all k."""
    return int(k in (2, 3))


def want_p12_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=12, all k."""
    return int(k >= 3)


def in_p12(n: int, k: int) -> bool:
    """G(n, 5*2^k-6)=1 on the covering live window, k>=3."""
    U = 1 << k
    if k < 3 or n < live_lo(k, 6) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return in_p6(n // 2, k - 1)
    m = (n - 1) // 2
    return bool(in_p6(m, k - 1)) != bool(in_p8(m, k - 1))


def in_p38_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-19)=1, k>=5, via parent p=10 xor p=12."""
    if k < 5 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 19) or n >= 4 * U:
        return False
    t = (n - 1) // 4
    return bool(in_p10(t, k - 2)) != bool(in_p12(t, k - 2))


def frozen_b3538() -> dict:
    """t<=N_BIT: bits 35..38 for t>=48; even t>=48 p=38 period 8."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 39)]
        if t >= 32 and (b[27] != want_b27(t) or b[28] != want_b28(t)):
            return {"ok": False, "pm": t}
        if t >= 48:
            got = (b[35], b[36], b[37], b[38])
            want = (want_b35(t), want_b36(t), want_b37(t), want_b38(t))
            if got != want:
                return {"ok": False, "b3538": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[35:39])
            a = and_clause(*four)
            if t >= 48:
                wp = even38_pat(t)
                if four != wp or a != want_and38_even(t):
                    return {"ok": False, "p38": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 39) - 1)
            if left_step(word, 38) != (nxt & ((1 << 39) - 1)):
                return {"ok": False, "auto39": t}
        row = nxt
    if early != sorted(EARLY38):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 46) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early38": early,
        "t_hi": N_BIT,
    }


def left39_period() -> dict:
    """Left 39 bits autonomous; t=48 equals t=56; even t>=48 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 38
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
    if rows[48] != rows[56]:
        return {"ok": False, "seed": True, "t48": rows[48], "t56": rows[56]}
    n_even = 0
    for t in range(48, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(35, 39))
        if b != even38_pat(t) or and_clause(*b) != want_and38_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 46) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t48": rows[48], "t56": rows[56]}


def green_p12() -> dict:
    """k=3..K_SET: in_p12 matches G; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        j = 5 * U - 6
        ones = []
        xor = 0
        for n in range(live_lo(k, 6), 4 * U):
            g = G(n, j)
            if g != int(in_p12(n, k)):
                return {"ok": False, "k": k, "n": n, "g": g}
            if g:
                ones.append(n)
                xor ^= 1
            n_ok += 1
        if xor != 1 or xor != want_p12_gxor(k):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        if k <= 6:
            rows[str(k)] = {"n": len(ones), "xor": xor}
    ok = n_ok > 0 and rows["3"]["n"] == 7 and rows["5"]["n"] == 13
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=5..K_SET: n%4==3 G=1 at p=38 is in_p38_n3; xor=0."""
    n_ok = 0
    rows = {}
    for k in range(5, K_SET + 1):
        U = 1 << k
        j = 5 * U - 19
        n3 = []
        for n in range(live_lo(k, 19), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                t = (n - 1) // 4
                U2 = U // 4
                pred = G(t, 5 * U2 - 5) ^ G(t, 5 * U2 - 6)
                if g != pred or g != int(in_p38_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g, "pred": pred}
                if g:
                    n3.append(n)
            n_ok += 1
        if len(n3) % 2 != 0:
            return {"ok": False, "cnt": True, "k": k, "n": len(n3)}
        if k <= 8:
            rows[str(k)] = {"n3": len(n3), "xor": 0}
    ok = n_ok > 0 and rows["5"]["n3"] == 8 and rows["7"]["n3"] == 12
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p38() -> dict:
    """k<=K_THIN: covering p=38 xor = want_p38_pack; k>=5 n%4==3 only."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 38, (T - 38) // 2
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_a = n_g = n_and = n_sil = n3 = 0
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
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                            if n % 4 == 3:
                                n3 += 1
                            if k >= 5 and four != PAT0100:
                                return {"ok": False, "form": True, "k": k, "four": four}
                        else:
                            n_sil += 1
                    if k >= 5:
                        s_even = s - 1
                        if packed != want_and38_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
                            return {"ok": False, "parity": True, "k": k, "n": n}
            row = rule30_step(row)
            s += 1
        want = want_p38_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and xor_a != want_p38_xor(k, 10):
            return {"ok": False, "ln": True, "k": k}
        if k >= 5 and (n_and != n3 or xor_a != 0 or t0 < 48):
            return {"ok": False, "split": True, "k": k, "n_and": n_and, "n3": n3}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "n3": n3,
            "j": j,
            "t0": t0,
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["2"]["xor_a"] == 1
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 0
        and rows["5"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pm = json.loads(PM_JSON.read_text())
    pl = json.loads(PL_JSON.read_text())
    ok = (
        pm["checks"]["all_ok"]
        and pl["checks"]["all_ok"]
        and pm["verdict"]["p30_xor_iff_k2"] == "LEMMA"
        and pm["verdict"]["p10_gxor_k_ge_2"] == "LEMMA"
        and pl["verdict"]["p26_silent_all_k"] == "LEMMA"
        and pm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pm["verdict"]["prize"] == "unsolved"
        and want_p38_pack(2) == 1
        and want_p38_pack(3) == 1
        and want_p38_pack(4) == 0
        and want_p38_xor(5, 10) == 0
        and want_p12_gxor(2) == 0
        and want_p12_gxor(3) == 1
        and want_p10_gxor(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g12, gre, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g12["ok"] and gre["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b3538()
    per = left39_period()
    g12 = green_p12()
    gre = green_n3()
    thin = thin_p38()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g12, gre, thin, sc, pref)
    dump = {
        "cycle": "PN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b3538": {k: fr[k] for k in fr if k != "ok"},
        "left39_period": {k: per[k] for k in per if k != "ok"},
        "green_p12": {k: g12[k] for k in g12 if k != "ok"},
        "green_n3": {k: gre[k] for k in gre if k != "ok"},
        "thin_p38": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit35_38_mod8": True,
            "and38_even_t_ge_48": True,
            "p12_gxor_k_ge_3": True,
            "p38_xor_iff_k23": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p38_silent_all_k": False,
            "p38_xor_0_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit35_38_mod8": "LEMMA",
            "left39_period8": "LEMMA",
            "and38_even_t_ge_48": "LEMMA",
            "p12_gxor_k_ge_3": "LEMMA",
            "p38_xor_iff_k23": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p38_silent_all_k": "KILLED",
            "p38_xor_0_all_k": "KILLED",
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
        "frozen_b3538 n_ok",
        dump["frozen_b3538"]["n_ok"],
        "n_even",
        dump["frozen_b3538"]["n_even"],
        "early38",
        dump["frozen_b3538"]["early38"],
    )
    print("green_p12 rows", dump["green_p12"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("thin_p38 rows", {k: dump["thin_p38"]["rows"][k] for k in ("2", "3", "4", "5", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
