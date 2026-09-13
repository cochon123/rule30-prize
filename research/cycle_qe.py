#!/usr/bin/env python3
"""Cycle QE: covering packed AND xor at p=114 is 1 iff k>=4 and k!=6.

Bits 111..114 freeze from t>=158: bit 111 is 1 iff t%8 in (2, 3, 4, 5);
bit 112 is 1 iff t%8 in (0, 5); bit 113 is 1 iff t%8 in (1, 2, 4);
bit 114 is 1 iff t%8 in (1, 2, 3, 4, 5). The left 115 bits are
autonomous; the word at t=158 equals t=166, so even t>=158 has p=114
4-tuple 0100 / 1011 / 1011 / 0000 on t%8 = 0,2,4,6, AND iff t%8==0.
Covering even s=10U-2n-2 has s%8==0 iff n%4==3. j=5U-57 is odd so
even n have G=0. For k>=7 (t0>=256>=158) packed AND on G=1 is 0100
iff n%4==3. Those n=4t+3 double twice to Green p=30 at k-2. Green
p=30 xor is 1 for k>=4 (odd n via parent p=16 at k-1). Packed p=30
xor is 1 iff k==2 (Cycle PM) while Green p=30 fires for k>=4. Early
even AND-ones are 56,62,78,96,106,112,122,130,150; k=4 and k=5 xor=1,
k=6 xor=0. UNIQUE_REST p=114. Cycle LU's k<=6 0100 even count is this
all-k lemma for k>=7. Not rest=S xor T. Not unique-rest xor=0. Not
E_k=0 for all k. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qe.py --certify
Dump: research/cycle_qe.json
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
from cycle_pv import in_p16, want_p16_gxor
from cycle_qd import want_b103, want_b104, want_b105, want_b106, want_p106_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QD_JSON = Path(__file__).resolve().parent / "cycle_qd.json"
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"
PV_JSON = Path(__file__).resolve().parent / "cycle_pv.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 220
N_LEFT = 220
K_THIN = 8
K_SET = 10
PAT0100 = (0, 1, 0, 0)
PAT1011 = (1, 0, 1, 1)
PAT0000 = (0, 0, 0, 0)
EARLY114 = {56, 62, 78, 96, 106, 112, 122, 130, 150}


def want_b111(t: int) -> int:
    """Packed bit 111: 1 iff t%8 in (2, 3, 4, 5) for t>=158."""
    if t < 158:
        return 0
    return int(t % 8 in (2, 3, 4, 5))


def want_b112(t: int) -> int:
    """Packed bit 112: 1 iff t%8 in (0, 5) for t>=158."""
    if t < 158:
        return 0
    return int(t % 8 in (0, 5))


def want_b113(t: int) -> int:
    """Packed bit 113: 1 iff t%8 in (1, 2, 4) for t>=158."""
    if t < 158:
        return 0
    return int(t % 8 in (1, 2, 4))


def want_b114(t: int) -> int:
    """Packed bit 114: 1 iff t%8 in (1, 2, 3, 4, 5) for t>=158."""
    if t < 158:
        return 0
    return int(t % 8 in (1, 2, 3, 4, 5))


def want_and114_even(t: int) -> int:
    """Even t>=158: AND at p=114 iff t%8==0. Early listed."""
    if t % 2:
        return 0
    if t < 158:
        return int(t in EARLY114)
    return int(t % 8 == 0)


def even114_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=158 p=114 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0100
    if r == 6:
        return PAT0000
    return PAT1011


def want_p114_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=114, all k."""
    return int(k >= 4 and k != 6)


def want_p30_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=30, all k."""
    return int(k >= 4)


def in_p30(n: int, k: int) -> bool:
    """G(n, 5*2^k-15)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 15) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    return in_p16((n - 1) // 2, k - 1)


def in_p114_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-57)=1, k>=7, via parent p=30 at k-2."""
    if k < 7 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 57) or n >= 4 * U:
        return False
    return in_p30((n - 3) // 4, k - 2)


def frozen_b111114() -> dict:
    """t<=N_BIT: bits 111..114; even t>=158 AND iff t%8==0."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 115)]
        if t >= 147 and (
            b[103] != want_b103(t)
            or b[104] != want_b104(t)
            or b[105] != want_b105(t)
            or b[106] != want_b106(t)
        ):
            return {"ok": False, "qd": t}
        if t >= 158:
            got = (b[111], b[112], b[113], b[114])
            want = (want_b111(t), want_b112(t), want_b113(t), want_b114(t))
            if got != want:
                return {"ok": False, "b111114": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[111:115])
            a = and_clause(*four)
            if t >= 158:
                wp = even114_pat(t)
                if four != wp or a != want_and114_even(t):
                    return {"ok": False, "p114": t, "four": four}
                if a and cover_nmod(t) != 3:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 115) - 1)
            if left_step(word, 114) != (nxt & ((1 << 115) - 1)):
                return {"ok": False, "auto115": t}
        row = nxt
    if early != sorted(EARLY114):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 156) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early114": early,
        "t_hi": N_BIT,
    }


def left115_period() -> dict:
    """Left 115 bits autonomous; t=158 equals t=166; even t>=158 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 114
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
    if rows[158] != rows[166]:
        return {"ok": False, "seed": True, "t158": rows[158], "t166": rows[166]}
    n_even = 0
    for t in range(158, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(111, 115))
        if b != even114_pat(t) or and_clause(*b) != want_and114_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 156) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t158": rows[158],
        "t166": rows[166],
    }


def green_p30() -> dict:
    """k=3..K_SET: xor=want; k>=4 in_p30 match G."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        n30 = x30 = 0
        j30 = 5 * U - 15
        for n in range(live_lo(k, 15), 4 * U):
            g = G(n, j30)
            if k >= 4 and g != int(in_p30(n, k)):
                return {"ok": False, "p30": True, "k": k, "n": n, "g": g}
            if g:
                n30 += 1
                x30 ^= 1
            n_ok += 1
        if x30 != want_p30_gxor(k):
            return {"ok": False, "xor": True, "k": k, "x30": x30}
        rows[str(k)] = {"n30": n30, "x30": x30}
    ok = (
        n_ok > 0
        and rows["3"]["x30"] == 0
        and rows["4"]["x30"] == 1
        and rows[str(K_SET)]["x30"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=7..K_SET: n%4==3 G=1 at p=114 is in_p114_n3; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(7, K_SET + 1):
        U = 1 << k
        j = 5 * U - 57
        n3 = 0
        xor = 0
        for n in range(live_lo(k, 57), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p114_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n3 += 1
                    xor ^= 1
            n_ok += 1
        want = want_p30_gxor(k - 2)
        if xor != 1 or xor != want:
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n3": n3, "xor": xor}
    ok = n_ok > 0 and rows["7"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p114() -> dict:
    """k<=K_THIN: covering p=114 xor = want_p114_pack; k>=7 form 0100."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 114, (T - 114) // 2
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
                    if k >= 7:
                        s_even = s - 1
                        if packed != want_and114_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 3:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
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
        want = want_p114_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 7 and xor_a != want_p30_gxor(k - 2):
            return {"ok": False, "p30": True, "k": k, "xor_a": xor_a}
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
        and rows["5"]["xor_a"] == 1
        and rows["6"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    qd = json.loads(QD_JSON.read_text())
    pm = json.loads(PM_JSON.read_text())
    pv = json.loads(PV_JSON.read_text())
    ok = (
        qd["checks"]["all_ok"]
        and pm["checks"]["all_ok"]
        and pv["checks"]["all_ok"]
        and qd["verdict"]["p106_xor_iff_k5_or_ge7"] == "LEMMA"
        and pm["verdict"]["p30_xor_iff_k2"] == "LEMMA"
        and pv["verdict"]["p16_gxor_k_ge_3"] == "LEMMA"
        and qd["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qd["verdict"]["prize"] == "unsolved"
        and want_p114_pack(4) == 1
        and want_p114_pack(6) == 0
        and want_p114_pack(7) == 1
        and want_p106_pack(5) == 1
        and want_p30_gxor(3) == 0
        and want_p30_gxor(4) == 1
        and want_p16_gxor(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g30, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g30["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b111114()
    per = left115_period()
    g30 = green_p30()
    gr = green_n3()
    thin = thin_p114()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g30, gr, thin, sc, pref)
    dump = {
        "cycle": "QE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b111114": {k: fr[k] for k in fr if k != "ok"},
        "left115_period": {k: per[k] for k in per if k != "ok"},
        "green_p30": {k: g30[k] for k in g30 if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p114": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit111_114_mod8": True,
            "and114_even_t_ge_158": True,
            "p30_gxor_k_ge_4": True,
            "p114_n3_via_p30": True,
            "p114_xor_iff_k_ge_4_ne_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p114_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit111_114_mod8": "LEMMA",
            "left115_period8": "LEMMA",
            "and114_even_t_ge_158": "LEMMA",
            "p30_gxor_k_ge_4": "LEMMA",
            "p114_n3_via_p30": "LEMMA",
            "p114_xor_iff_k_ge_4_ne_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p114_silent": "KILLED",
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
        "frozen_b111114 n_ok",
        dump["frozen_b111114"]["n_ok"],
        "n_even",
        dump["frozen_b111114"]["n_even"],
        "early114",
        dump["frozen_b111114"]["early114"],
    )
    print(
        "thin_p114 rows",
        {k: dump["thin_p114"]["rows"][k] for k in ("4", "5", "6", "8")},
    )
    print("green_p30 rows", dump["green_p30"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
