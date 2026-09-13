#!/usr/bin/env python3
"""Cycle PV: covering packed AND xor at p=58 is 1 iff k>=3 and k!=5.

Bits 55..58 freeze from t>=84: bit 55 is 1 iff t%8 in (1, 2, 3);
bit 56 is 1 iff t%8 in (4, 5); bit 57 is 1 iff t%8 not in (2, 4);
bit 58 is 1 iff t%8 not in (5, 6). The left 59 bits are autonomous;
the word at t=84 equals t=92, so even t>=84 has p=58 4-tuple 0011 /
1001 / 0101 / 0010 on t%8 = 0,2,4,6, AND iff t%8 in (0, 2, 6).
Covering even s=10U-2n-2 has s%8 in (0, 2, 6) iff n%4 in (3, 2, 0).
j=5U-29 is odd so even n have G=0. For k>=6 (t0>=128>=84) packed
AND on G=1 is 0011 iff n%4==3. Those n=4t+3 double twice to Green
p=16 at k-2, whose xor is 1 for k>=3, so packed xor is 1 for
k>=6. Early even AND-ones are 28,30,52,60,62,64; k=3 and k=4
xor=1, k=5 xor=0. UNIQUE_REST p=58. Cycle LR's k<=6 0011 xor=1
is this all-k lemma for k>=6. Not rest=S xor T. Not unique-rest
xor=0. Not E_k=0 for all k. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pv.py --certify
Dump: research/cycle_pv.json
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
from cycle_ph import in_p8, in_p16_even, want_p16_pack
from cycle_pm import in_p10
from cycle_pq import cover_nmod
from cycle_ps import want_b51, want_b52, want_b53, want_b54
from cycle_pu import want_p40_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PU_JSON = Path(__file__).resolve().parent / "cycle_pu.json"
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 112
N_LEFT = 112
K_THIN = 8
K_SET = 10
PAT0011 = (0, 0, 1, 1)
PAT1001 = (1, 0, 0, 1)
PAT0101 = (0, 1, 0, 1)
PAT0010 = (0, 0, 1, 0)
EARLY58 = {28, 30, 52, 60, 62, 64}


def want_b55(t: int) -> int:
    """Packed bit 55: 1 iff t%8 in (1, 2, 3) for t>=84."""
    if t < 84:
        return 0
    return int(t % 8 in (1, 2, 3))


def want_b56(t: int) -> int:
    """Packed bit 56: 1 iff t%8 in (4, 5) for t>=84."""
    if t < 84:
        return 0
    return int(t % 8 in (4, 5))


def want_b57(t: int) -> int:
    """Packed bit 57: 1 iff t%8 not in (2, 4) for t>=84."""
    if t < 84:
        return 0
    return int(t % 8 not in (2, 4))


def want_b58(t: int) -> int:
    """Packed bit 58: 1 iff t%8 not in (5, 6) for t>=84."""
    if t < 84:
        return 0
    return int(t % 8 not in (5, 6))


def want_and58_even(t: int) -> int:
    """Even t>=84: AND at p=58 iff t%8 in (0, 2, 6). Early listed."""
    if t % 2:
        return 0
    if t < 84:
        return int(t in EARLY58)
    return int(t % 8 in (0, 2, 6))


def even58_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=84 p=58 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0011
    if r == 2:
        return PAT1001
    if r == 4:
        return PAT0101
    return PAT0010


def want_p58_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=58, all k."""
    return int(k >= 3 and k != 5)


def want_p16_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=16, all k."""
    return int(k >= 3)


def in_p16(n: int, k: int) -> bool:
    """G(n, 5*2^k-8)=1 on the covering live window, k>=3."""
    U = 1 << k
    if k < 3 or n < live_lo(k, 8) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return in_p16_even(n, k)
    m = (n - 1) // 2
    return bool(in_p8(m, k - 1)) != bool(in_p10(m, k - 1))


def in_p58_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-29)=1, k>=6, via parent p=16 at k-2."""
    if k < 6 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 29) or n >= 4 * U:
        return False
    return in_p16((n - 3) // 4, k - 2)


def frozen_b5558() -> dict:
    """t<=N_BIT: bits 55..58 for t>=84; even t>=84 AND iff t%8 in (0,2,6)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 59)]
        if t >= 78 and (
            b[51] != want_b51(t)
            or b[52] != want_b52(t)
            or b[53] != want_b53(t)
            or b[54] != want_b54(t)
        ):
            return {"ok": False, "ps": t}
        if t >= 84:
            got = (b[55], b[56], b[57], b[58])
            want = (want_b55(t), want_b56(t), want_b57(t), want_b58(t))
            if got != want:
                return {"ok": False, "b5558": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[55:59])
            a = and_clause(*four)
            if t >= 84:
                wp = even58_pat(t)
                if four != wp or a != want_and58_even(t):
                    return {"ok": False, "p58": t, "four": four}
                if a and cover_nmod(t) == 1:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 59) - 1)
            if left_step(word, 58) != (nxt & ((1 << 59) - 1)):
                return {"ok": False, "auto59": t}
        row = nxt
    if early != sorted(EARLY58):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 82) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early58": early,
        "t_hi": N_BIT,
    }


def left59_period() -> dict:
    """Left 59 bits autonomous; t=84 equals t=92; even t>=84 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 58
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
    if rows[84] != rows[92]:
        return {"ok": False, "seed": True, "t84": rows[84], "t92": rows[92]}
    n_even = 0
    for t in range(84, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(55, 59))
        if b != even58_pat(t) or and_clause(*b) != want_and58_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 82) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t84": rows[84], "t92": rows[92]}


def green_p16() -> dict:
    """k=3..K_SET: in_p16 matches G; xor=want_p16_gxor=want_p16_pack."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        j = 5 * U - 8
        n1 = 0
        xor = 0
        for n in range(live_lo(k, 8), 4 * U):
            g = G(n, j)
            if g != int(in_p16(n, k)):
                return {"ok": False, "k": k, "n": n, "g": g}
            if g:
                n1 += 1
                xor ^= 1
            n_ok += 1
        if xor != want_p16_gxor(k) or xor != want_p16_pack(k):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": n1, "xor": xor}
    ok = n_ok > 0 and rows["3"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=6..K_SET: n%4==3 G=1 at p=58 is in_p58_n3; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 29
        n1 = []
        xor = 0
        for n in range(live_lo(k, 29), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p58_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n1.append(n)
                    xor ^= 1
            n_ok += 1
        if xor != 1 or xor != want_p16_gxor(k - 2):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": len(n1), "xor": xor}
    ok = n_ok > 0 and rows["6"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p58() -> dict:
    """k<=K_THIN: covering p=58 xor = want_p58_pack; k>=6 form 0011."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 58, (T - 58) // 2
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
                        if packed != want_and58_even(s_even):
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
        want = want_p58_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != want_p16_gxor(k - 2):
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
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 1
        and rows["5"]["xor_a"] == 0
        and rows["6"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pu = json.loads(PU_JSON.read_text())
    ph = json.loads(PH_JSON.read_text())
    pm = json.loads(PM_JSON.read_text())
    ok = (
        pu["checks"]["all_ok"]
        and ph["checks"]["all_ok"]
        and pm["checks"]["all_ok"]
        and pu["verdict"]["p40_xor_iff_k24"] == "LEMMA"
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and pm["verdict"]["p10_gxor_k_ge_2"] == "LEMMA"
        and pu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pu["verdict"]["prize"] == "unsolved"
        and want_p58_pack(3) == 1
        and want_p58_pack(5) == 0
        and want_p58_pack(6) == 1
        and want_p40_pack(2) == 1
        and want_p16_gxor(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g16, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g16["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b5558()
    per = left59_period()
    g16 = green_p16()
    gr = green_n3()
    thin = thin_p58()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g16, gr, thin, sc, pref)
    dump = {
        "cycle": "PV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b5558": {k: fr[k] for k in fr if k != "ok"},
        "left59_period": {k: per[k] for k in per if k != "ok"},
        "green_p16": {k: g16[k] for k in g16 if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p58": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit55_58_mod8": True,
            "and58_even_t_ge_84": True,
            "p16_gxor_k_ge_3": True,
            "p58_n3_via_p16": True,
            "p58_xor_iff_k_ge_3_ne_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p58_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit55_58_mod8": "LEMMA",
            "left59_period8": "LEMMA",
            "and58_even_t_ge_84": "LEMMA",
            "p16_gxor_k_ge_3": "LEMMA",
            "p58_n3_via_p16": "LEMMA",
            "p58_xor_iff_k_ge_3_ne_5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p58_silent": "KILLED",
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
        "frozen_b5558 n_ok",
        dump["frozen_b5558"]["n_ok"],
        "n_even",
        dump["frozen_b5558"]["n_even"],
        "early58",
        dump["frozen_b5558"]["early58"],
    )
    print(
        "thin_p58 rows",
        {k: dump["thin_p58"]["rows"][k] for k in ("3", "4", "5", "6", "8")},
    )
    print("green_p16 rows", dump["green_p16"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
