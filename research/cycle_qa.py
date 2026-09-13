#!/usr/bin/env python3
"""Cycle QA: covering packed AND xor at p=86 is 1 iff k==5.

Bits 83..86 freeze from t>=125: bit 83 is 1 iff t%8 in (1, 2, 3, 5, 6);
bit 84 is 1 iff t%8==4; bit 85 is 1 iff t%8 in (0, 1, 3, 5, 7);
bit 86 is 1 iff t%8 != 5. The left 87 bits are autonomous; the word
at t=125 equals t=133, so even t>=126 has p=86 4-tuple 0011 / 1001
/ 0101 / 1001 on t%8 = 0,2,4,6, AND iff t%8 in (0, 2, 6). Covering
even s=10U-2n-2 has s%8 in (0, 2, 6) iff n%4 in (3, 2, 0). j=5U-43
is odd so even n have G=0. For k>=6 (t0>=128>=125) packed AND on
G=1 is 0011 iff n%4==3. Those n=4t+3 double twice to Green p=22 xor
p=24 at k-2. Green p=22 xor and Green p=24 xor are both 1 for k>=4,
so the slices cancel and packed xor is 0 for k>=6. Early even
AND-ones are 42,44,56,58,70,72,76,84,114; k=4 xor=0, k=5 xor=1.
Packed p=22 is silent for every k (Cycle PJ) and packed p=24 is
silent for k>=4 (Cycle PL) while both Green columns fire.
UNIQUE_REST p=86. Cycle LS's k<=6 0011 even count is this all-k
lemma for k>=6. Not rest=S xor T. Not unique-rest xor=0. Not
E_k=0 for all k. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qa.py --certify
Dump: research/cycle_qa.json
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
from cycle_pc import in_p14, live_lo
from cycle_pd import left_step
from cycle_pn import in_p12
from cycle_pq import cover_nmod
from cycle_pz import want_b73, want_b74, want_b75, want_b76, want_p76_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PZ_JSON = Path(__file__).resolve().parent / "cycle_pz.json"
PJ_JSON = Path(__file__).resolve().parent / "cycle_pj.json"
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 160
N_LEFT = 160
K_THIN = 8
K_SET = 10
PAT0011 = (0, 0, 1, 1)
PAT1001 = (1, 0, 0, 1)
PAT0101 = (0, 1, 0, 1)
EARLY86 = {42, 44, 56, 58, 70, 72, 76, 84, 114}


def want_b83(t: int) -> int:
    """Packed bit 83: 1 iff t%8 in (1, 2, 3, 5, 6) for t>=125."""
    if t < 125:
        return 0
    return int(t % 8 in (1, 2, 3, 5, 6))


def want_b84(t: int) -> int:
    """Packed bit 84: 1 iff t%8==4 for t>=125."""
    if t < 125:
        return 0
    return int(t % 8 == 4)


def want_b85(t: int) -> int:
    """Packed bit 85: 1 iff t%8 in (0, 1, 3, 5, 7) for t>=125."""
    if t < 125:
        return 0
    return int(t % 8 in (0, 1, 3, 5, 7))


def want_b86(t: int) -> int:
    """Packed bit 86: 1 iff t%8 != 5 for t>=125."""
    if t < 125:
        return 0
    return int(t % 8 != 5)


def want_and86_even(t: int) -> int:
    """Even t>=126: AND at p=86 iff t%8 in (0, 2, 6). Early listed."""
    if t % 2:
        return 0
    if t < 126:
        return int(t in EARLY86)
    return int(t % 8 in (0, 2, 6))


def even86_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=126 p=86 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0011
    if r == 4:
        return PAT0101
    return PAT1001


def want_p86_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=86, all k."""
    return int(k == 5)


def want_p22_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=22, all k."""
    return int(k >= 4)


def want_p24_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=24, all k."""
    return int(k >= 4)


def in_p22(n: int, k: int) -> bool:
    """G(n, 5*2^k-11)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 11) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    return in_p12((n - 1) // 2, k - 1)


def in_p24(n: int, k: int) -> bool:
    """G(n, 5*2^k-12)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 12) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return in_p12(n // 2, k - 1)
    m = (n - 1) // 2
    return bool(in_p12(m, k - 1)) != bool(in_p14(m, k - 1))


def in_p86_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-43)=1, k>=6, via parent p=22 xor p=24."""
    if k < 6 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 43) or n >= 4 * U:
        return False
    t = (n - 3) // 4
    return bool(in_p22(t, k - 2)) != bool(in_p24(t, k - 2))


def frozen_b8386() -> dict:
    """t<=N_BIT: bits 83..86 for t>=125; even t>=126 AND iff t%8 in (0,2,6)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 87)]
        if t >= 104 and (
            b[73] != want_b73(t)
            or b[74] != want_b74(t)
            or b[75] != want_b75(t)
            or b[76] != want_b76(t)
        ):
            return {"ok": False, "pz": t}
        if t >= 125:
            got = (b[83], b[84], b[85], b[86])
            want = (want_b83(t), want_b84(t), want_b85(t), want_b86(t))
            if got != want:
                return {"ok": False, "b8386": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[83:87])
            a = and_clause(*four)
            if t >= 126:
                wp = even86_pat(t)
                if four != wp or a != want_and86_even(t):
                    return {"ok": False, "p86": t, "four": four}
                if a and cover_nmod(t) not in (0, 2, 3):
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 87) - 1)
            if left_step(word, 86) != (nxt & ((1 << 87) - 1)):
                return {"ok": False, "auto87": t}
        row = nxt
    if early != sorted(EARLY86):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 124) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early86": early,
        "t_hi": N_BIT,
    }


def left87_period() -> dict:
    """Left 87 bits autonomous; t=125 equals t=133; even t>=126 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 86
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
    if rows[125] != rows[133]:
        return {"ok": False, "seed": True, "t125": rows[125], "t133": rows[133]}
    n_even = 0
    for t in range(126, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(83, 87))
        if b != even86_pat(t) or and_clause(*b) != want_and86_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 124) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t125": rows[125],
        "t133": rows[133],
    }


def green_p22_p24() -> dict:
    """k=3..K_SET: xor=want; k>=4 in_p22/in_p24 match G."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        n22 = x22 = n24 = x24 = 0
        j22 = 5 * U - 11
        j24 = 5 * U - 12
        for n in range(min(live_lo(k, 11), live_lo(k, 12)), 4 * U):
            if n >= live_lo(k, 11):
                g = G(n, j22)
                if k >= 4 and g != int(in_p22(n, k)):
                    return {"ok": False, "p22": True, "k": k, "n": n, "g": g}
                if g:
                    n22 += 1
                    x22 ^= 1
            if n >= live_lo(k, 12):
                g = G(n, j24)
                if k >= 4 and g != int(in_p24(n, k)):
                    return {"ok": False, "p24": True, "k": k, "n": n, "g": g}
                if g:
                    n24 += 1
                    x24 ^= 1
            n_ok += 1
        if x22 != want_p22_gxor(k) or x24 != want_p24_gxor(k):
            return {"ok": False, "xor": True, "k": k, "x22": x22, "x24": x24}
        rows[str(k)] = {"n22": n22, "x22": x22, "n24": n24, "x24": x24}
    ok = (
        n_ok > 0
        and rows["3"]["x22"] == 0
        and rows["3"]["x24"] == 0
        and rows["4"]["x22"] == 1
        and rows["4"]["x24"] == 1
        and rows[str(K_SET)]["x22"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=6..K_SET: n%4==3 G=1 at p=86 is in_p86_n3; xor=0."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 43
        n3 = 0
        xor = 0
        for n in range(live_lo(k, 43), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p86_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n3 += 1
                    xor ^= 1
            n_ok += 1
        want = want_p22_gxor(k - 2) ^ want_p24_gxor(k - 2)
        if xor != 0 or xor != want:
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n3": n3, "xor": xor}
    ok = n_ok > 0 and rows["6"]["xor"] == 0 and rows[str(K_SET)]["xor"] == 0
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p86() -> dict:
    """k<=K_THIN: covering p=86 xor = want_p86_pack; k>=6 form 0011."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 86, (T - 86) // 2
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
                        if packed != want_and86_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 3:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
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
        want = want_p86_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != (want_p22_gxor(k - 2) ^ want_p24_gxor(k - 2)):
            return {"ok": False, "p2224": True, "k": k, "xor_a": xor_a}
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
        and rows["4"]["xor_a"] == 0
        and rows["5"]["xor_a"] == 1
        and rows["6"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pz = json.loads(PZ_JSON.read_text())
    pj = json.loads(PJ_JSON.read_text())
    pl = json.loads(PL_JSON.read_text())
    ok = (
        pz["checks"]["all_ok"]
        and pj["checks"]["all_ok"]
        and pl["checks"]["all_ok"]
        and pz["verdict"]["p76_xor_iff_k_ge_3_ne_4"] == "LEMMA"
        and pj["verdict"]["p22_silent_all_k"] == "LEMMA"
        and pl["verdict"]["p24_silent_k_ge_4"] == "LEMMA"
        and pz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pz["verdict"]["prize"] == "unsolved"
        and want_p86_pack(5) == 1
        and want_p86_pack(6) == 0
        and want_p76_pack(5) == 1
        and want_p22_gxor(3) == 0
        and want_p22_gxor(4) == 1
        and want_p24_gxor(4) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g22, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g22["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b8386()
    per = left87_period()
    g22 = green_p22_p24()
    gr = green_n3()
    thin = thin_p86()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g22, gr, thin, sc, pref)
    dump = {
        "cycle": "QA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b8386": {k: fr[k] for k in fr if k != "ok"},
        "left87_period": {k: per[k] for k in per if k != "ok"},
        "green_p22_p24": {k: g22[k] for k in g22 if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p86": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit83_86_mod8": True,
            "and86_even_t_ge_126": True,
            "p22_gxor_k_ge_4": True,
            "p24_gxor_k_ge_4": True,
            "p86_n3_via_p22_p24": True,
            "p86_xor_iff_k5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p86_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit83_86_mod8": "LEMMA",
            "left87_period8": "LEMMA",
            "and86_even_t_ge_126": "LEMMA",
            "p22_gxor_k_ge_4": "LEMMA",
            "p24_gxor_k_ge_4": "LEMMA",
            "p86_n3_via_p22_p24": "LEMMA",
            "p86_xor_iff_k5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p86_silent": "KILLED",
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
        "frozen_b8386 n_ok",
        dump["frozen_b8386"]["n_ok"],
        "n_even",
        dump["frozen_b8386"]["n_even"],
        "early86",
        dump["frozen_b8386"]["early86"],
    )
    print(
        "thin_p86 rows",
        {k: dump["thin_p86"]["rows"][k] for k in ("4", "5", "6", "8")},
    )
    print("green_p22_p24 rows", dump["green_p22_p24"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
