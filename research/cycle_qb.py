#!/usr/bin/env python3
"""Cycle QB: covering packed AND xor at p=88 is 1 iff k==4 or k>=6.

Bits 85..88 freeze from t>=127: bit 85 is 1 iff t%8 in (0, 1, 3, 5, 7);
bit 86 is 1 iff t%8 != 5; bit 87 is 1 iff t%8 in (3, 5, 7);
bit 88 is 1 iff t%8 in (1, 3, 5, 6). The left 89 bits are autonomous;
the word at t=127 equals t=135, so even t>=128 has p=88 4-tuple
1100 / 0100 / 0100 / 0101 on t%8 = 0,2,4,6, AND iff t%8 in (2, 4).
Covering even s=10U-2n-2 has s%8 in (2, 4) iff n%4 in (2, 1).
j=5U-44 is even so even n can fire. For k>=6 (t0>=128>=127) packed
AND on G=1 is 0100 iff n%4 in (1, 2). Those n=4t+1 double twice to
Green p=22 at k-2; n=4t+2 double twice to Green p=22 xor p=24 at
k-2 and cancel. Packed xor is therefore Green p=22 xor at k-2,
which is 1 for k>=6. Early even AND-ones are 66,70,78,88,100,114;
k=4 xor=1, k=5 xor=0. UNIQUE_REST p=88. Cycle LQ's k<=6 0100 odd
count is this all-k lemma for k>=6. Not rest=S xor T. Not
unique-rest xor=0. Not E_k=0 for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qb.py --certify
Dump: research/cycle_qb.json
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
from cycle_qa import in_p22, in_p24, want_b85, want_b86
from cycle_qa import want_p22_gxor, want_p24_gxor, want_p86_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QA_JSON = Path(__file__).resolve().parent / "cycle_qa.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 160
N_LEFT = 160
K_THIN = 8
K_SET = 10
PAT1100 = (1, 1, 0, 0)
PAT0100 = (0, 1, 0, 0)
PAT0101 = (0, 1, 0, 1)
EARLY88 = {66, 70, 78, 88, 100, 114}


def want_b87(t: int) -> int:
    """Packed bit 87: 1 iff t%8 in (3, 5, 7) for t>=127."""
    if t < 127:
        return 0
    return int(t % 8 in (3, 5, 7))


def want_b88(t: int) -> int:
    """Packed bit 88: 1 iff t%8 in (1, 3, 5, 6) for t>=127."""
    if t < 127:
        return 0
    return int(t % 8 in (1, 3, 5, 6))


def want_and88_even(t: int) -> int:
    """Even t>=128: AND at p=88 iff t%8 in (2, 4). Early listed."""
    if t % 2:
        return 0
    if t < 128:
        return int(t in EARLY88)
    return int(t % 8 in (2, 4))


def even88_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=128 p=88 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT1100
    if r == 6:
        return PAT0101
    return PAT0100


def want_p88_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=88, all k."""
    return int(k == 4 or k >= 6)


def in_p88_n1(n: int, k: int) -> bool:
    """n%4==1 and G(n, 5*2^k-44)=1, k>=6, via parent p=22 at k-2."""
    if k < 6 or n % 4 != 1:
        return False
    U = 1 << k
    if n < live_lo(k, 44) or n >= 4 * U:
        return False
    return in_p22((n - 1) // 4, k - 2)


def in_p88_n2(n: int, k: int) -> bool:
    """n%4==2 and G(n, 5*2^k-44)=1, k>=6, via parent p=22 xor p=24."""
    if k < 6 or n % 4 != 2:
        return False
    U = 1 << k
    if n < live_lo(k, 44) or n >= 4 * U:
        return False
    t = (n - 2) // 4
    return bool(in_p22(t, k - 2)) != bool(in_p24(t, k - 2))


def frozen_b8588() -> dict:
    """t<=N_BIT: bits 85..88; even t>=128 AND iff t%8 in (2,4)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 89)]
        if t >= 125 and (b[85] != want_b85(t) or b[86] != want_b86(t)):
            return {"ok": False, "qa": t}
        if t >= 127:
            got = (b[85], b[86], b[87], b[88])
            want = (want_b85(t), want_b86(t), want_b87(t), want_b88(t))
            if got != want:
                return {"ok": False, "b8588": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[85:89])
            a = and_clause(*four)
            if t >= 128:
                wp = even88_pat(t)
                if four != wp or a != want_and88_even(t):
                    return {"ok": False, "p88": t, "four": four}
                if a and cover_nmod(t) not in (1, 2):
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 89) - 1)
            if left_step(word, 88) != (nxt & ((1 << 89) - 1)):
                return {"ok": False, "auto89": t}
        row = nxt
    if early != sorted(EARLY88):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 126) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early88": early,
        "t_hi": N_BIT,
    }


def left89_period() -> dict:
    """Left 89 bits autonomous; t=127 equals t=135; even t>=128 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 88
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
    if rows[127] != rows[135]:
        return {"ok": False, "seed": True, "t127": rows[127], "t135": rows[135]}
    n_even = 0
    for t in range(128, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(85, 89))
        if b != even88_pat(t) or and_clause(*b) != want_and88_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 126) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t127": rows[127],
        "t135": rows[135],
    }


def green_slices() -> dict:
    """k=6..K_SET: n%4 in (1,2) G=1 at p=88 via p=22 / p=22 xor p=24."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 44
        n1 = n2 = 0
        x1 = x2 = 0
        for n in range(live_lo(k, 44), 4 * U):
            g = G(n, j)
            if n % 4 == 1:
                if g != int(in_p88_n1(n, k)):
                    return {"ok": False, "n1": True, "k": k, "n": n, "g": g}
                if g:
                    n1 += 1
                    x1 ^= 1
            elif n % 4 == 2:
                if g != int(in_p88_n2(n, k)):
                    return {"ok": False, "n2": True, "k": k, "n": n, "g": g}
                if g:
                    n2 += 1
                    x2 ^= 1
            n_ok += 1
        want1 = want_p22_gxor(k - 2)
        want2 = want_p22_gxor(k - 2) ^ want_p24_gxor(k - 2)
        if x1 != want1 or x2 != want2:
            return {"ok": False, "xor": True, "k": k, "x1": x1, "x2": x2}
        rows[str(k)] = {"n1": n1, "n2": n2, "x1": x1, "x2": x2, "xor": x1 ^ x2}
    ok = (
        n_ok > 0
        and rows["6"]["x1"] == 1
        and rows["6"]["x2"] == 0
        and rows["6"]["xor"] == 1
        and rows[str(K_SET)]["xor"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p88() -> dict:
    """k<=K_THIN: covering p=88 xor = want_p88_pack; k>=6 form 0100."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 88, (T - 88) // 2
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
                        if packed != want_and88_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 not in (1, 2):
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 in (1, 2)):
                            return {"ok": False, "g1": True, "k": k, "n": n}
                        if packed and G(n, j) == 1 and four != PAT0100:
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
        want = want_p88_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != want_p22_gxor(k - 2):
            return {"ok": False, "p22": True, "k": k, "xor_a": xor_a}
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
        and rows["4"]["xor_a"] == 1
        and rows["5"]["xor_a"] == 0
        and rows["6"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    qa = json.loads(QA_JSON.read_text())
    ok = (
        qa["checks"]["all_ok"]
        and qa["verdict"]["p86_xor_iff_k5"] == "LEMMA"
        and qa["verdict"]["p22_gxor_k_ge_4"] == "LEMMA"
        and qa["verdict"]["p24_gxor_k_ge_4"] == "LEMMA"
        and qa["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qa["verdict"]["prize"] == "unsolved"
        and want_p88_pack(4) == 1
        and want_p88_pack(5) == 0
        and want_p88_pack(6) == 1
        and want_p86_pack(5) == 1
        and want_p22_gxor(4) == 1
        and want_p24_gxor(4) == 1
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
    fr = frozen_b8588()
    per = left89_period()
    gr = green_slices()
    thin = thin_p88()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gr, thin, sc, pref)
    dump = {
        "cycle": "QB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b8588": {k: fr[k] for k in fr if k != "ok"},
        "left89_period": {k: per[k] for k in per if k != "ok"},
        "green_slices": {k: gr[k] for k in gr if k != "ok"},
        "thin_p88": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit85_88_mod8": True,
            "and88_even_t_ge_128": True,
            "p88_n1_via_p22": True,
            "p88_n2_via_p22_p24": True,
            "p88_xor_iff_k4_or_ge6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p88_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit85_88_mod8": "LEMMA",
            "left89_period8": "LEMMA",
            "and88_even_t_ge_128": "LEMMA",
            "p88_n1_via_p22": "LEMMA",
            "p88_n2_via_p22_p24": "LEMMA",
            "p88_xor_iff_k4_or_ge6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p88_silent": "KILLED",
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
        "frozen_b8588 n_ok",
        dump["frozen_b8588"]["n_ok"],
        "n_even",
        dump["frozen_b8588"]["n_even"],
        "early88",
        dump["frozen_b8588"]["early88"],
    )
    print(
        "thin_p88 rows",
        {k: dump["thin_p88"]["rows"][k] for k in ("4", "5", "6", "8")},
    )
    print("green_slices rows", dump["green_slices"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
