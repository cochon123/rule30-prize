#!/usr/bin/env python3
"""Cycle PX: covering packed AND xor at p=60 is 1 iff k==4.

Bits 57..60 freeze from t>=86: bit 57 is 1 iff t%8 not in (2, 4);
bit 58 is 1 iff t%8 not in (5, 6); bit 59 is 1 iff t%8 in (3, 5, 7);
bit 60 is 1 iff t%8 in (1, 3, 5, 6, 7). The left 61 bits are
autonomous; the word at t=86 equals t=94, so even t>=86 has p=60
4-tuple 1100 / 0100 / 0100 / 1001 on t%8 = 0,2,4,6, AND iff t%8
in (2, 4, 6). Covering even s=10U-2n-2 has s%8 in (2, 4, 6) iff
n%4 in (2, 1, 0). j=5U-30 is even so even n can fire, but n%4==0
halves to even first argument at odd second and G=0. For k>=6
(t0>=128>=86) packed AND on G=1 is 0100 iff n%4 in (1, 2). Those
n=4t+1 and n=4t+2 both double twice to Green p=16 at k-2, whose
xor is 1 for k>=3, so the two slices cancel and packed xor is 0
for k>=5. Early even AND-ones are 30,36,42,48,52,80; k=3 xor=0,
k=4 xor=1. UNIQUE_REST p=60. Cycle LL's k<=6 0100 even count is
this all-k lemma for k>=5. Not rest=S xor T. Not unique-rest
xor=0. Not E_k=0 for all k. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_px.py --certify
Dump: research/cycle_px.json
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
from cycle_pq import want_b59 as want_b59_pq
from cycle_pq import want_b60 as want_b60_pq
from cycle_pv import in_p16, want_p16_gxor
from cycle_pv import want_b57 as want_b57_pv
from cycle_pv import want_b58 as want_b58_pv
from cycle_pw import want_p52_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PW_JSON = Path(__file__).resolve().parent / "cycle_pw.json"
PV_JSON = Path(__file__).resolve().parent / "cycle_pv.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 112
N_LEFT = 112
K_THIN = 8
K_SET = 10
PAT1100 = (1, 1, 0, 0)
PAT0100 = (0, 1, 0, 0)
PAT1001 = (1, 0, 0, 1)
EARLY60 = {30, 36, 42, 48, 52, 80}


def want_b57(t: int) -> int:
    """Packed bit 57: 1 iff t%8 not in (2, 4) for t>=86."""
    if t < 86:
        return 0
    return int(t % 8 not in (2, 4))


def want_b58(t: int) -> int:
    """Packed bit 58: 1 iff t%8 not in (5, 6) for t>=86."""
    if t < 86:
        return 0
    return int(t % 8 not in (5, 6))


def want_b59(t: int) -> int:
    """Packed bit 59: 1 iff t%8 in (3, 5, 7) for t>=86."""
    if t < 86:
        return 0
    return int(t % 8 in (3, 5, 7))


def want_b60(t: int) -> int:
    """Packed bit 60: 1 iff t%8 in (1, 3, 5, 6, 7) for t>=86."""
    if t < 86:
        return 0
    return int(t % 8 in (1, 3, 5, 6, 7))


def want_and60_even(t: int) -> int:
    """Even t>=86: AND at p=60 iff t%8 in (2, 4, 6). Early listed."""
    if t % 2:
        return 0
    if t < 86:
        return int(t in EARLY60)
    return int(t % 8 in (2, 4, 6))


def even60_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=86 p=60 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT1100
    if r == 6:
        return PAT1001
    return PAT0100


def want_p60_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=60, all k."""
    return int(k == 4)


def in_p60_n1(n: int, k: int) -> bool:
    """n%4==1 and G(n, 5*2^k-30)=1, k>=5, via parent p=16 at k-2."""
    if k < 5 or n % 4 != 1:
        return False
    U = 1 << k
    if n < live_lo(k, 30) or n >= 4 * U:
        return False
    return in_p16((n - 1) // 4, k - 2)


def in_p60_n2(n: int, k: int) -> bool:
    """n%4==2 and G(n, 5*2^k-30)=1, k>=5, via parent p=16 at k-2."""
    if k < 5 or n % 4 != 2:
        return False
    U = 1 << k
    if n < live_lo(k, 30) or n >= 4 * U:
        return False
    return in_p16((n - 2) // 4, k - 2)


def frozen_b5760() -> dict:
    """t<=N_BIT: bits 57..60 for t>=86; even t>=86 AND iff t%8 in (2,4,6)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 61)]
        if t >= 84 and (b[57] != want_b57_pv(t) or b[58] != want_b58_pv(t)):
            return {"ok": False, "pv": t}
        if t >= 88 and (b[59] != want_b59_pq(t) or b[60] != want_b60_pq(t)):
            return {"ok": False, "pq": t}
        if t >= 86:
            got = (b[57], b[58], b[59], b[60])
            want = (want_b57(t), want_b58(t), want_b59(t), want_b60(t))
            if got != want:
                return {"ok": False, "b5760": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[57:61])
            a = and_clause(*four)
            if t >= 86:
                wp = even60_pat(t)
                if four != wp or a != want_and60_even(t):
                    return {"ok": False, "p60": t, "four": four}
                if a and cover_nmod(t) not in (0, 1, 2):
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 61) - 1)
            if left_step(word, 60) != (nxt & ((1 << 61) - 1)):
                return {"ok": False, "auto61": t}
        row = nxt
    if early != sorted(EARLY60):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 84) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early60": early,
        "t_hi": N_BIT,
    }


def left61_period() -> dict:
    """Left 61 bits autonomous; t=86 equals t=94; even t>=86 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 60
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
    if rows[86] != rows[94]:
        return {"ok": False, "seed": True, "t86": rows[86], "t94": rows[94]}
    n_even = 0
    for t in range(86, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(57, 61))
        if b != even60_pat(t) or and_clause(*b) != want_and60_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 84) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t86": rows[86], "t94": rows[94]}


def green_slices() -> dict:
    """k=5..K_SET: n%4 in (1,2) G=1 at p=60 via p=16; each xor=1."""
    n_ok = 0
    rows = {}
    for k in range(5, K_SET + 1):
        U = 1 << k
        j = 5 * U - 30
        n1 = n2 = 0
        x1 = x2 = 0
        for n in range(live_lo(k, 30), 4 * U):
            g = G(n, j)
            if n % 4 == 1:
                if g != int(in_p60_n1(n, k)):
                    return {"ok": False, "n1": True, "k": k, "n": n, "g": g}
                if g:
                    n1 += 1
                    x1 ^= 1
            elif n % 4 == 2:
                if g != int(in_p60_n2(n, k)):
                    return {"ok": False, "n2": True, "k": k, "n": n, "g": g}
                if g:
                    n2 += 1
                    x2 ^= 1
            n_ok += 1
        if x1 != 1 or x2 != 1 or x1 != want_p16_gxor(k - 2):
            return {"ok": False, "xor": True, "k": k, "x1": x1, "x2": x2}
        rows[str(k)] = {"n1": n1, "n2": n2, "x1": x1, "x2": x2, "xor": x1 ^ x2}
    ok = n_ok > 0 and rows["5"]["xor"] == 0 and rows[str(K_SET)]["xor"] == 0
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p60() -> dict:
    """k<=K_THIN: covering p=60 xor = want_p60_pack; k>=6 form 0100."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 60, (T - 60) // 2
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
                        if packed != want_and60_even(s_even):
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
        want = want_p60_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != (want_p16_gxor(k - 2) ^ want_p16_gxor(k - 2)):
            return {"ok": False, "p16": True, "k": k, "xor_a": xor_a}
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
        and rows["3"]["xor_a"] == 0
        and rows["4"]["xor_a"] == 1
        and rows["5"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pw = json.loads(PW_JSON.read_text())
    pv = json.loads(PV_JSON.read_text())
    ok = (
        pw["checks"]["all_ok"]
        and pv["checks"]["all_ok"]
        and pw["verdict"]["p52_xor_iff_k3"] == "LEMMA"
        and pv["verdict"]["p16_gxor_k_ge_3"] == "LEMMA"
        and pw["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pw["verdict"]["prize"] == "unsolved"
        and want_p60_pack(4) == 1
        and want_p60_pack(5) == 0
        and want_p52_pack(3) == 1
        and want_p16_gxor(3) == 1
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
    fr = frozen_b5760()
    per = left61_period()
    gr = green_slices()
    thin = thin_p60()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gr, thin, sc, pref)
    dump = {
        "cycle": "PX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b5760": {k: fr[k] for k in fr if k != "ok"},
        "left61_period": {k: per[k] for k in per if k != "ok"},
        "green_slices": {k: gr[k] for k in gr if k != "ok"},
        "thin_p60": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit57_60_mod8": True,
            "and60_even_t_ge_86": True,
            "p60_n1_n2_via_p16": True,
            "p60_xor_iff_k4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p60_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit57_60_mod8": "LEMMA",
            "left61_period8": "LEMMA",
            "and60_even_t_ge_86": "LEMMA",
            "p60_n1_n2_via_p16": "LEMMA",
            "p60_xor_iff_k4": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p60_silent": "KILLED",
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
        "frozen_b5760 n_ok",
        dump["frozen_b5760"]["n_ok"],
        "n_even",
        dump["frozen_b5760"]["n_even"],
        "early60",
        dump["frozen_b5760"]["early60"],
    )
    print(
        "thin_p60 rows",
        {k: dump["thin_p60"]["rows"][k] for k in ("3", "4", "5", "8")},
    )
    print("green_slices rows", dump["green_slices"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
