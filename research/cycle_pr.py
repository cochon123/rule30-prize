#!/usr/bin/env python3
"""Cycle PR: covering packed AND xor at p=42 is 1 iff k==3 or k>=5.

Bits 39..42 freeze from t>=58: bit 39 is 1 iff t%8 in (6, 7); bit
40 is 1 iff t%8 in (2, 4); bit 41 is 1 iff t%8 != 7; bit 42 is 1
iff t%8 not in (3, 5). The left 43 bits are autonomous; the word
at t=58 equals t=66, so even t>=58 has p=42 4-tuple 0011 / 0111 /
0111 / 1011 on t%8 = 0,2,4,6, AND iff t%8==0. Covering even
s=10U-2n-2 has s%8==0 iff n%4==3. For k>=5 (t0>=64>=58) packed
AND on G=1 is 0011 iff n%4==3. Those n=4t+3 double twice to Green
p=12 at k-2, whose xor is 1 for k>=3, so packed xor is 1 for
k>=5. Early even AND-ones are 20,22,24,36,44,52,56; k=3 xor=1 and
k=4 xor=0. Not rest=S xor T. Not unique-rest xor=0. Not E_k=0 for
all k. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_pr.py --certify
Dump: research/cycle_pr.json
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
from cycle_pn import in_p12, want_b35, want_b36, want_b37, want_b38, want_p12_gxor
from cycle_pq import cover_nmod
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PQ_JSON = Path(__file__).resolve().parent / "cycle_pq.json"
PN_JSON = Path(__file__).resolve().parent / "cycle_pn.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 80
N_LEFT = 80
K_THIN = 8
K_SET = 8
PAT0011 = (0, 0, 1, 1)
PAT0111 = (0, 1, 1, 1)
PAT1011 = (1, 0, 1, 1)
EARLY42 = {20, 22, 24, 36, 44, 52, 56}


def want_b39(t: int) -> int:
    """Packed bit 39: 1 iff t%8 in (6, 7) for t>=58."""
    if t < 58:
        return 0
    return int(t % 8 in (6, 7))


def want_b40(t: int) -> int:
    """Packed bit 40: 1 iff t%8 in (2, 4) for t>=58."""
    if t < 58:
        return 0
    return int(t % 8 in (2, 4))


def want_b41(t: int) -> int:
    """Packed bit 41: 1 iff t%8 != 7 for t>=58."""
    if t < 58:
        return 0
    return int(t % 8 != 7)


def want_b42(t: int) -> int:
    """Packed bit 42: 1 iff t%8 not in (3, 5) for t>=58."""
    if t < 58:
        return 0
    return int(t % 8 not in (3, 5))


def want_and42_even(t: int) -> int:
    """Even t>=58: AND at p=42 iff t%8==0. Early even AND-ones listed."""
    if t % 2:
        return 0
    if t < 58:
        return int(t in EARLY42)
    return int(t % 8 == 0)


def even42_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=58 p=42 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0011
    if r == 6:
        return PAT1011
    return PAT0111


def want_p42_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=42, all k."""
    return int(k == 3 or k >= 5)


def in_p42_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-21)=1, k>=5, via parent p=12 at k-2."""
    if k < 5 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 21) or n >= 4 * U:
        return False
    return in_p12((n - 3) // 4, k - 2)


def frozen_b3942() -> dict:
    """t<=N_BIT: bits 39..42 for t>=58; even t>=58 AND iff t%8==0."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 43)]
        if t >= 48 and (
            b[35] != want_b35(t)
            or b[36] != want_b36(t)
            or b[37] != want_b37(t)
            or b[38] != want_b38(t)
        ):
            return {"ok": False, "pn": t}
        if t >= 58:
            got = (b[39], b[40], b[41], b[42])
            want = (want_b39(t), want_b40(t), want_b41(t), want_b42(t))
            if got != want:
                return {"ok": False, "b3942": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[39:43])
            a = and_clause(*four)
            if t >= 58:
                wp = even42_pat(t)
                if four != wp or a != want_and42_even(t):
                    return {"ok": False, "p42": t, "four": four}
                if a and cover_nmod(t) != 3:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 43) - 1)
            if left_step(word, 42) != (nxt & ((1 << 43) - 1)):
                return {"ok": False, "auto43": t}
        row = nxt
    if early != sorted(EARLY42):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 56) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early42": early,
        "t_hi": N_BIT,
    }


def left43_period() -> dict:
    """Left 43 bits autonomous; t=58 equals t=66; even t>=58 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 42
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
    if rows[58] != rows[66]:
        return {"ok": False, "seed": True, "t58": rows[58], "t66": rows[66]}
    n_even = 0
    for t in range(58, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(39, 43))
        if b != even42_pat(t) or and_clause(*b) != want_and42_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 56) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t58": rows[58], "t66": rows[66]}


def green_n3() -> dict:
    """k=5..K_SET: n%4==3 G=1 at p=42 is in_p42_n3; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(5, K_SET + 1):
        U = 1 << k
        j = 5 * U - 21
        n3 = []
        xor = 0
        for n in range(live_lo(k, 21), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p42_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n3.append(n)
                    xor ^= 1
            elif g and in_p42_n3(n, k):
                return {"ok": False, "even": True, "k": k, "n": n}
            n_ok += 1
        if xor != 1 or xor != want_p12_gxor(k - 2):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        if k <= 8:
            rows[str(k)] = {"n3": len(n3), "xor": xor}
    ok = n_ok > 0 and rows["5"]["xor"] == 1 and rows["8"]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p42() -> dict:
    """k<=K_THIN: covering p=42 xor = want_p42_pack; k>=5 form 0011."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 42, (T - 42) // 2
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
                    if k >= 5:
                        s_even = s - 1
                        if packed != want_and42_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and n % 4 != 3:
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
        want = want_p42_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and xor_a != want_p12_gxor(k - 2):
            return {"ok": False, "p12": True, "k": k, "xor_a": xor_a}
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
    pq = json.loads(PQ_JSON.read_text())
    pn = json.loads(PN_JSON.read_text())
    ok = (
        pq["checks"]["all_ok"]
        and pn["checks"]["all_ok"]
        and pq["verdict"]["p62_xor_iff_k34"] == "LEMMA"
        and pn["verdict"]["p38_xor_iff_k23"] == "LEMMA"
        and pq["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pq["verdict"]["prize"] == "unsolved"
        and want_p42_pack(3) == 1
        and want_p42_pack(4) == 0
        and want_p42_pack(5) == 1
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
    fr = frozen_b3942()
    per = left43_period()
    gr = green_n3()
    thin = thin_p42()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, gr, thin, sc, pref)
    dump = {
        "cycle": "PR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b3942": {k: fr[k] for k in fr if k != "ok"},
        "left43_period": {k: per[k] for k in per if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p42": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit39_42_mod8": True,
            "and42_even_t_ge_58": True,
            "p42_n3_via_p12": True,
            "p42_xor_iff_k3_or_ge5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p42_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit39_42_mod8": "LEMMA",
            "left43_period8": "LEMMA",
            "and42_even_t_ge_58": "LEMMA",
            "p42_n3_via_p12": "LEMMA",
            "p42_xor_iff_k3_or_ge5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p42_silent": "KILLED",
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
        "frozen_b3942 n_ok",
        dump["frozen_b3942"]["n_ok"],
        "n_even",
        dump["frozen_b3942"]["n_even"],
        "early42",
        dump["frozen_b3942"]["early42"],
    )
    print(
        "thin_p42 rows",
        {k: dump["thin_p42"]["rows"][k] for k in ("3", "4", "5", "8")},
    )
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
