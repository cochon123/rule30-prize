#!/usr/bin/env python3
"""Cycle PQ: covering packed AND xor at p=62 is 1 iff k in (3, 4).

Covering even s=10U-2n-2 for k>=3 has s%8 = 0,2,4,6 iff n%4 =
3,2,1,0. Packed p%4==2 has odd j, so even n have G=0. Freeze AND
residues in (2, 6) therefore make packed AND on G=1 empty once t0
exceeds the freeze. Bits 59..62 freeze from t>=88: bit 59 is 1 iff
t%8 in (3, 5, 7); bit 60 is 1 iff t%8 in (1, 3, 5, 6, 7); bit 61
is 1 iff t%8 in (2, 3, 7); bit 62 is 1 iff t%8 in (2, 3, 6). The
left 63 bits are autonomous; the word at t=88 equals t=96, so even
t>=88 has p=62 4-tuple 0000 / 0011 / 0000 / 0101 on t%8 = 0,2,4,6,
AND iff t%8==2. Early even AND-ones are 30,46,48,66,82. Packed xor
is 1 iff k in (3, 4). Not rest=S xor T. Not E_k=0 for all k. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_pq.py --certify
Dump: research/cycle_pq.json
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
from cycle_pd import left_step
from cycle_po import want_b61, want_b62
from cycle_pp import want_b33, want_b34
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PP_JSON = Path(__file__).resolve().parent / "cycle_pp.json"
PO_JSON = Path(__file__).resolve().parent / "cycle_po.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 128
N_LEFT = 128
K_THIN = 8
K_CLOCK = 12
PAT0000 = (0, 0, 0, 0)
PAT0011 = (0, 0, 1, 1)
PAT0101 = (0, 1, 0, 1)
EARLY62 = {30, 46, 48, 66, 82}
# even t%8 whose covering n is even (G=0 at odd j)
VANISH_RES = frozenset({2, 6})
S_TO_NMOD = {0: 3, 2: 2, 4: 1, 6: 0}


def cover_nmod(s: int) -> int:
    """n%4 from covering even s=10U-2n-2 for k>=3."""
    return S_TO_NMOD[s % 8]


def and_res_vanishes(res) -> bool:
    """Freeze AND residues in (2, 6) hit only even n."""
    return set(res) <= VANISH_RES


def want_b59(t: int) -> int:
    """Packed bit 59: 1 iff t%8 in (3, 5, 7) for t>=88."""
    if t < 88:
        return 0
    return int(t % 8 in (3, 5, 7))


def want_b60(t: int) -> int:
    """Packed bit 60: 1 iff t%8 in (1, 3, 5, 6, 7) for t>=88."""
    if t < 88:
        return 0
    return int(t % 8 in (1, 3, 5, 6, 7))


def want_and62_even(t: int) -> int:
    """Even t>=88: AND at p=62 iff t%8==2. Early even AND-ones listed."""
    if t % 2:
        return 0
    if t < 88:
        return int(t in EARLY62)
    return int(t % 8 == 2)


def even62_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=88 p=62 4-tuple."""
    r = t % 8
    if r == 2:
        return PAT0011
    if r == 6:
        return PAT0101
    return PAT0000


def want_p62_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=62, all k."""
    return int(k in (3, 4))


def clock_nmod() -> dict:
    """k=3..K_CLOCK: covering s%8 maps to n%4; p%4==2 has odd j."""
    n_ok = 0
    for k in range(3, K_CLOCK + 1):
        U = 1 << k
        T = 10 * U
        for n in range(0, 4 * U):
            s = T - 2 * n - 2
            if s % 2:
                return {"ok": False, "odd_s": True, "k": k, "n": n}
            if cover_nmod(s) != n % 4:
                return {"ok": False, "nmod": True, "k": k, "n": n, "s": s}
            n_ok += 1
        for p in range(6, 80, 4):
            j = (T - p) // 2
            if j >= 0 and j % 2 == 0:
                return {"ok": False, "jodd": True, "k": k, "p": p, "j": j}
        n_ok += 1
    ok = (
        n_ok > 0
        and cover_nmod(2) == 2
        and cover_nmod(6) == 0
        and cover_nmod(0) == 3
        and cover_nmod(4) == 1
        and and_res_vanishes({2})
        and and_res_vanishes({2, 6})
        and not and_res_vanishes({0})
        and not and_res_vanishes({2, 4})
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CLOCK}


def frozen_b5962() -> dict:
    """t<=N_BIT: bits 59..62 for t>=88; even t>=88 AND iff t%8==2."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 63)]
        if t >= 44 and (b[33] != want_b33(t) or b[34] != want_b34(t)):
            return {"ok": False, "pp": t}
        if t >= 92 and (b[61] != want_b61(t) or b[62] != want_b62(t)):
            return {"ok": False, "po": t}
        if t >= 88:
            got = (b[59], b[60], b[61], b[62])
            want = (
                want_b59(t),
                want_b60(t),
                int(t % 8 in (2, 3, 7)),
                int(t % 8 in (2, 3, 6)),
            )
            if got != want:
                return {"ok": False, "b5962": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[59:63])
            a = and_clause(*four)
            if t >= 88:
                wp = even62_pat(t)
                if four != wp or a != want_and62_even(t):
                    return {"ok": False, "p62": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 63) - 1)
            if left_step(word, 62) != (nxt & ((1 << 63) - 1)):
                return {"ok": False, "auto63": t}
        row = nxt
    if early != sorted(EARLY62):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 86) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early62": early,
        "t_hi": N_BIT,
    }


def left63_period() -> dict:
    """Left 63 bits autonomous; t=88 equals t=96; even t>=88 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 62
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
    if rows[88] != rows[96]:
        return {"ok": False, "seed": True, "t88": rows[88], "t96": rows[96]}
    n_even = 0
    for t in range(88, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(59, 63))
        if b != even62_pat(t) or and_clause(*b) != want_and62_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 86) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t88": rows[88], "t96": rows[96]}


def thin_p62() -> dict:
    """k<=K_THIN: covering p=62 xor = want_p62_pack; k>=5 n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 62, (T - 62) // 2
        if j < 0:
            rows[str(k)] = {
                "xor_a": 0,
                "n_g": 0,
                "n_and": 0,
                "n_sil": 0,
                "j": j,
                "t0": t0,
                "j_odd": 0,
            }
            n_ok += 1
            continue
        if k >= 1 and j % 2 == 0:
            return {"ok": False, "jodd": True, "k": k, "j": j}
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
                        if packed != want_and62_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and n % 4 != 2:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if packed and G(n, j) == 1:
                            return {"ok": False, "g1and": True, "k": k, "n": n}
                        if n % 2 == 0 and G(n, j) == 1:
                            return {"ok": False, "even_g": True, "k": k, "n": n}
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                        else:
                            n_sil += 1
            row = rule30_step(row)
            s += 1
        want = want_p62_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and (n_and != 0 or n_g == 0):
            return {"ok": False, "sil": True, "k": k, "n_and": n_and, "n_g": n_g}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "j": j,
            "t0": t0,
            "j_odd": int(j % 2 == 1),
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 1
        and rows["5"]["n_and"] == 0
        and rows["6"]["n_and"] == 0
        and rows["8"]["n_and"] == 0
        and rows["5"]["n_g"] > 0
        and rows["8"]["n_g"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pp = json.loads(PP_JSON.read_text())
    po = json.loads(PO_JSON.read_text())
    ok = (
        pp["checks"]["all_ok"]
        and po["checks"]["all_ok"]
        and pp["verdict"]["p34_xor_iff_k34"] == "LEMMA"
        and po["verdict"]["p64_xor_iff_k35"] == "LEMMA"
        and pp["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pp["verdict"]["prize"] == "unsolved"
        and want_p62_pack(3) == 1
        and want_p62_pack(4) == 1
        and want_p62_pack(5) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, clock, fr, per, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and clock["ok"] and fr["ok"]
    assert per["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    clock = clock_nmod()
    fr = frozen_b5962()
    per = left63_period()
    thin = thin_p62()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, clock, fr, per, thin, sc, pref)
    dump = {
        "cycle": "PQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "clock_nmod": {k: clock[k] for k in clock if k != "ok"},
        "frozen_b5962": {k: fr[k] for k in fr if k != "ok"},
        "left63_period": {k: per[k] for k in per if k != "ok"},
        "thin_p62": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "cover_s_nmod": True,
            "p2mod4_j_odd": True,
            "bit59_62_mod8": True,
            "and62_even_t_ge_88": True,
            "p62_silent_k_ge_5": True,
            "p62_xor_iff_k34": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p62_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "cover_s_nmod": "LEMMA",
            "p2mod4_j_odd": "LEMMA",
            "bit59_62_mod8": "LEMMA",
            "left63_period8": "LEMMA",
            "and62_even_t_ge_88": "LEMMA",
            "p62_silent_k_ge_5": "LEMMA",
            "p62_xor_iff_k34": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p62_silent_all_k": "KILLED",
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
        "frozen_b5962 n_ok",
        dump["frozen_b5962"]["n_ok"],
        "n_even",
        dump["frozen_b5962"]["n_even"],
        "early62",
        dump["frozen_b5962"]["early62"],
    )
    print(
        "thin_p62 rows",
        {k: dump["thin_p62"]["rows"][k] for k in ("3", "4", "5", "8")},
    )
    print("clock_nmod n_ok", dump["clock_nmod"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()

