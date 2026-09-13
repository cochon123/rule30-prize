#!/usr/bin/env python3
"""Cycle PM: covering packed AND xor at p=30 is 1 iff k==2 on q=10.

Bit 27 is 1 iff t%4 != 0 for t>=32; bit 28 is 0 for t>=32. The
left 31 bits are autonomous; the word at t=40 equals t=48, so even
t>=40 has p=30 4-tuple 0011 / 1001 / 0001 / 1011 on t%8 =
0,2,4,6. AND fires iff t%8 in (0, 2) already from even t>=32.
Covering even s=10U-2n-2 has s%8 in (0, 2) iff n%4 in (3, 2).
j=5U-15 is odd so even n have G=0. For k>=4 (t0=2U>=32) packed
AND fires iff n%4==3 among live G=1. Those n=4t+3 double to
parent p=8 xor p=10 at k-2, each Green xor 1 for k-2>=2, so the
xor is 0. k=3 has n_and=0; k=2 xor=1. Cycle LK's k<=6 0011 xor=0
is this all-k lemma for k>=5. Not rest=S xor T. Not E_k=0 for all
k. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_pm.py --certify
Dump: research/cycle_pm.json
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
from cycle_lk import want_p30_xor
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import in_p6, live_lo, p6_count
from cycle_pd import left_step
from cycle_ph import in_p8
from cycle_pk import want_b29, want_b30
from cycle_pl import want_b23, want_b24, want_b25, want_b26
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"
PK_JSON = Path(__file__).resolve().parent / "cycle_pk.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 56
K_THIN = 8
K_SET = 12
PAT0011 = (0, 0, 1, 1)
PAT1001 = (1, 0, 0, 1)
PAT0001 = (0, 0, 0, 1)
PAT1011 = (1, 0, 1, 1)
EARLY30 = {14, 26}


def want_b27(t: int) -> int:
    """Packed bit 27: 1 iff t%4 != 0 for t>=32."""
    if t < 32:
        return 0
    return int(t % 4 != 0)


def want_b28(t: int) -> int:
    """Packed bit 28 is 0 for t>=32."""
    return 0


def want_and30_even(t: int) -> int:
    """Even t>=32: AND at p=30 iff t%8 in (0, 2)."""
    if t < 32 or t % 2:
        return int(t in EARLY30)
    return int(t % 8 in (0, 2))


def even30_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=40 p=30 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0011
    if r == 2:
        return PAT1001
    if r == 4:
        return PAT0001
    return PAT1011


def want_p30_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=30, all k."""
    return int(k == 2)


def want_p10_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=10, all k."""
    return int(k >= 2)


def in_p10(n: int, k: int) -> bool:
    """G(n, 5*2^k-5)=1 on the covering live window, k>=2."""
    U = 1 << k
    if k < 2 or n < live_lo(k, 5) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    return in_p6((n - 1) // 2, k - 1)


def in_p30_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-15)=1, k>=4, via parent p=8 xor p=10."""
    if k < 4 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 15) or n >= 4 * U:
        return False
    t = (n - 1) // 4
    return bool(in_p8(t, k - 2)) != bool(in_p10(t, k - 2))


def frozen_b2728() -> dict:
    """t<=N_BIT: bits 27,28; even t>=32 AND; even t>=40 4-tuple period 8."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 31)]
        if t >= 30 and (
            b[23] != want_b23(t)
            or b[24] != want_b24(t)
            or b[25] != want_b25(t)
            or b[26] != want_b26(t)
        ):
            return {"ok": False, "pl": t}
        if t >= 36 and (b[29] != want_b29(t) or b[30] != want_b30(t)):
            return {"ok": False, "pk": t}
        if t >= 32:
            if b[27] != want_b27(t) or b[28] != want_b28(t):
                return {"ok": False, "b2728": t, "got": (b[27], b[28])}
        if t % 2 == 0:
            four = tuple(b[27:31])
            a = and_clause(*four)
            if t >= 40:
                wp = even30_pat(t)
                if four != wp or a != want_and30_even(t):
                    return {"ok": False, "p30": t, "four": four}
                n_even += 1
            elif t >= 32:
                if a != want_and30_even(t):
                    return {"ok": False, "and32": t, "four": four}
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 31) - 1)
            if left_step(word, 30) != (nxt & ((1 << 31) - 1)):
                return {"ok": False, "auto31": t}
        row = nxt
    if early != sorted(EARLY30):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 38) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early30": early,
        "t_hi": N_BIT,
    }


def left31_period() -> dict:
    """Left 31 bits autonomous; t=40 equals t=48; even t>=40 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 30
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
    if rows[40] != rows[48]:
        return {"ok": False, "seed": True, "t40": rows[40], "t48": rows[48]}
    n_even = 0
    for t in range(40, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(27, 31))
        if b != even30_pat(t) or and_clause(*b) != want_and30_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 38) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t40": rows[40], "t48": rows[48]}


def green_p10() -> dict:
    """k=2..K_SET: in_p10 matches G; xor=1; count p6(k-1)."""
    n_ok = 0
    rows = {}
    for k in range(2, K_SET + 1):
        U = 1 << k
        j = 5 * U - 5
        ones = []
        for n in range(live_lo(k, 5), 4 * U):
            g = G(n, j)
            if g != int(in_p10(n, k)):
                return {"ok": False, "k": k, "n": n, "g": g}
            if g:
                ones.append(n)
            n_ok += 1
        if len(ones) != p6_count(k - 1) or len(ones) % 2 != 1:
            return {"ok": False, "cnt": True, "k": k, "n": len(ones)}
        if k <= 6:
            rows[str(k)] = {"n": len(ones), "xor": 1}
    ok = n_ok > 0 and rows["2"]["n"] == 1 and rows["5"]["n"] == 5
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=4..K_SET: n%4==3 G=1 at p=30 is in_p30_n3; xor=0."""
    n_ok = 0
    rows = {}
    for k in range(4, K_SET + 1):
        U = 1 << k
        j = 5 * U - 15
        n3 = []
        for n in range(live_lo(k, 15), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                t = (n - 1) // 4
                pred = G(t, 5 * (U // 4) - 4) ^ G(t, 5 * (U // 4) - 5)
                if g != pred or g != int(in_p30_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g, "pred": pred}
                if g:
                    n3.append(n)
            n_ok += 1
        if len(n3) % 2 != 0:
            return {"ok": False, "cnt": True, "k": k, "n": len(n3)}
        if k <= 8:
            rows[str(k)] = {"n3": len(n3), "xor": 0}
    ok = n_ok > 0 and rows["4"]["n3"] == 6 and rows["6"]["n3"] == 10
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p30() -> dict:
    """k<=K_THIN: covering p=30 xor = want_p30_pack; k>=4 n%4==3 only."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 30, (T - 30) // 2
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
                            if k >= 5 and four != PAT0011:
                                return {"ok": False, "form": True, "k": k, "four": four}
                        else:
                            n_sil += 1
                    if k >= 5:
                        s_even = s - 1
                        if packed != want_and30_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
                            return {"ok": False, "parity": True, "k": k, "n": n}
            row = rule30_step(row)
            s += 1
        want = want_p30_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and xor_a != want_p30_xor(k, 10):
            return {"ok": False, "lk": True, "k": k}
        if k >= 4 and (n_and != n3 or xor_a != 0):
            return {"ok": False, "split": True, "k": k, "n_and": n_and, "n3": n3}
        if k >= 5 and t0 < 40:
            return {"ok": False, "t0": True, "k": k}
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
        and rows["0"]["xor_a"] == 0
        and rows["2"]["xor_a"] == 1
        and rows["3"]["xor_a"] == 0
        and rows["4"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pl = json.loads(PL_JSON.read_text())
    pk = json.loads(PK_JSON.read_text())
    ok = (
        pl["checks"]["all_ok"]
        and pk["checks"]["all_ok"]
        and pl["verdict"]["p26_silent_all_k"] == "LEMMA"
        and pl["verdict"]["p28_silent_all_k"] == "LEMMA"
        and pk["verdict"]["p32_xor_k_ge_5"] == "LEMMA"
        and pl["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pl["verdict"]["prize"] == "unsolved"
        and want_p30_pack(2) == 1
        and want_p30_pack(4) == 0
        and want_p30_xor(5, 10) == 0
        and want_p10_gxor(1) == 0
        and want_p10_gxor(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g10, gre, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g10["ok"] and gre["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b2728()
    per = left31_period()
    g10 = green_p10()
    gre = green_n3()
    thin = thin_p30()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g10, gre, thin, sc, pref)
    dump = {
        "cycle": "PM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b2728": {k: fr[k] for k in fr if k != "ok"},
        "left31_period": {k: per[k] for k in per if k != "ok"},
        "green_p10": {k: g10[k] for k in g10 if k != "ok"},
        "green_n3": {k: gre[k] for k in gre if k != "ok"},
        "thin_p30": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit27_28": True,
            "and30_even_t_ge_32": True,
            "p10_gxor_k_ge_2": True,
            "p30_xor_iff_k2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p30_silent_all_k": False,
            "p30_xor_0_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit27_28": "LEMMA",
            "left31_period8": "LEMMA",
            "and30_even_t_ge_32": "LEMMA",
            "p10_gxor_k_ge_2": "LEMMA",
            "p30_xor_iff_k2": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p30_silent_all_k": "KILLED",
            "p30_xor_0_all_k": "KILLED",
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
        "frozen_b2728 n_ok",
        dump["frozen_b2728"]["n_ok"],
        "n_even",
        dump["frozen_b2728"]["n_even"],
        "early30",
        dump["frozen_b2728"]["early30"],
    )
    print("green_p10 rows", dump["green_p10"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("thin_p30 rows", {k: dump["thin_p30"]["rows"][k] for k in ("2", "3", "4", "5", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
