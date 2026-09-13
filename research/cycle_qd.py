#!/usr/bin/env python3
"""Cycle QD: covering packed AND xor at p=106 is 1 iff k==5 or k>=7.

Bits 103..106 freeze from t>=147: bit 103 is 1 iff t%8 in (0, 1, 7);
bit 104 is 1 iff t%8 in (2, 3, 4); bit 105 is 1 iff t%8 not in (0, 2);
bit 106 is 1 iff t%8 in (0, 1, 2, 6, 7). The left 107 bits are
autonomous; the word at t=147 equals t=155, so even t>=148 has p=106
4-tuple 1001 / 0101 / 0110 / 0011 on t%8 = 0,2,4,6, AND iff t%8
in (0, 6). Covering even s=10U-2n-2 has s%8 in (0, 6) iff n%4 in
(3, 0). j=5U-53 is odd so even n have G=0. For k>=7 (t0>=256>=147)
packed AND on G=1 is 1001 iff n%4==3. Those n=4t+3 double twice to
Green p=28 at k-2. Green p=28 xor is 1 for k>=4 (even n via parent
p=14; odd n is p=14 xor p=16 and cancels). Packed p=28 is silent
for every k (Cycle PL) while Green p=28 fires. Early even AND-ones
are 52,54,68,70,74,102,130; k=5 xor=1, k=6 xor=0. UNIQUE_REST p=106.
Cycle LI's k<=6 1001 is this all-k lemma for k>=7. Not rest=S xor T.
Not unique-rest xor=0. Not E_k=0 for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qd.py --certify
Dump: research/cycle_qd.json
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
from cycle_pc import in_p14, live_lo, want_p14_gxor
from cycle_pd import left_step
from cycle_pq import cover_nmod
from cycle_pv import in_p16, want_p16_gxor
from cycle_qc import want_b95, want_b96, want_b97, want_b98, want_p98_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QC_JSON = Path(__file__).resolve().parent / "cycle_qc.json"
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"
PV_JSON = Path(__file__).resolve().parent / "cycle_pv.json"
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 200
N_LEFT = 200
K_THIN = 8
K_SET = 10
PAT1001 = (1, 0, 0, 1)
PAT0101 = (0, 1, 0, 1)
PAT0110 = (0, 1, 1, 0)
PAT0011 = (0, 0, 1, 1)
EARLY106 = {52, 54, 68, 70, 74, 102, 130}


def want_b103(t: int) -> int:
    """Packed bit 103: 1 iff t%8 in (0, 1, 7) for t>=147."""
    if t < 147:
        return 0
    return int(t % 8 in (0, 1, 7))


def want_b104(t: int) -> int:
    """Packed bit 104: 1 iff t%8 in (2, 3, 4) for t>=147."""
    if t < 147:
        return 0
    return int(t % 8 in (2, 3, 4))


def want_b105(t: int) -> int:
    """Packed bit 105: 1 iff t%8 not in (0, 2) for t>=147."""
    if t < 147:
        return 0
    return int(t % 8 not in (0, 2))


def want_b106(t: int) -> int:
    """Packed bit 106: 1 iff t%8 in (0, 1, 2, 6, 7) for t>=147."""
    if t < 147:
        return 0
    return int(t % 8 in (0, 1, 2, 6, 7))


def want_and106_even(t: int) -> int:
    """Even t>=148: AND at p=106 iff t%8 in (0, 6). Early listed."""
    if t % 2:
        return 0
    if t < 148:
        return int(t in EARLY106)
    return int(t % 8 in (0, 6))


def even106_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=148 p=106 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT1001
    if r == 2:
        return PAT0101
    if r == 4:
        return PAT0110
    return PAT0011


def want_p106_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=106, all k."""
    return int(k == 5 or k >= 7)


def want_p28_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=28, all k."""
    return int(k >= 4)


def in_p28(n: int, k: int) -> bool:
    """G(n, 5*2^k-14)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 14) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return in_p14(n // 2, k - 1)
    m = (n - 1) // 2
    return bool(in_p14(m, k - 1)) != bool(in_p16(m, k - 1))


def in_p106_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-53)=1, k>=7, via parent p=28 at k-2."""
    if k < 7 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 53) or n >= 4 * U:
        return False
    return in_p28((n - 3) // 4, k - 2)


def frozen_b103106() -> dict:
    """t<=N_BIT: bits 103..106; even t>=148 AND iff t%8 in (0,6)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 107)]
        if t >= 132 and (
            b[95] != want_b95(t)
            or b[96] != want_b96(t)
            or b[97] != want_b97(t)
            or b[98] != want_b98(t)
        ):
            return {"ok": False, "qc": t}
        if t >= 147:
            got = (b[103], b[104], b[105], b[106])
            want = (want_b103(t), want_b104(t), want_b105(t), want_b106(t))
            if got != want:
                return {"ok": False, "b103106": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[103:107])
            a = and_clause(*four)
            if t >= 148:
                wp = even106_pat(t)
                if four != wp or a != want_and106_even(t):
                    return {"ok": False, "p106": t, "four": four}
                if a and cover_nmod(t) not in (0, 3):
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 107) - 1)
            if left_step(word, 106) != (nxt & ((1 << 107) - 1)):
                return {"ok": False, "auto107": t}
        row = nxt
    if early != sorted(EARLY106):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 146) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early106": early,
        "t_hi": N_BIT,
    }


def left107_period() -> dict:
    """Left 107 bits autonomous; t=147 equals t=155; even t>=148 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 106
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
    if rows[147] != rows[155]:
        return {"ok": False, "seed": True, "t147": rows[147], "t155": rows[155]}
    n_even = 0
    for t in range(148, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(103, 107))
        if b != even106_pat(t) or and_clause(*b) != want_and106_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 146) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t147": rows[147],
        "t155": rows[155],
    }


def green_p28() -> dict:
    """k=3..K_SET: xor=want; k>=4 in_p28 match G."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        n28 = x28 = xe = xo = 0
        j28 = 5 * U - 14
        for n in range(live_lo(k, 14), 4 * U):
            g = G(n, j28)
            if k >= 4 and g != int(in_p28(n, k)):
                return {"ok": False, "p28": True, "k": k, "n": n, "g": g}
            if g:
                n28 += 1
                x28 ^= 1
                if n % 2 == 0:
                    xe ^= 1
                else:
                    xo ^= 1
            n_ok += 1
        if x28 != want_p28_gxor(k):
            return {"ok": False, "xor": True, "k": k, "x28": x28}
        if k >= 4 and (xe != want_p14_gxor(k - 1) or xo != (want_p14_gxor(k - 1) ^ want_p16_gxor(k - 1))):
            return {"ok": False, "slice": True, "k": k, "xe": xe, "xo": xo}
        rows[str(k)] = {"n28": n28, "x28": x28, "xe": xe, "xo": xo}
    ok = (
        n_ok > 0
        and rows["3"]["x28"] == 0
        and rows["4"]["x28"] == 1
        and rows[str(K_SET)]["x28"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=7..K_SET: n%4==3 G=1 at p=106 is in_p106_n3; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(7, K_SET + 1):
        U = 1 << k
        j = 5 * U - 53
        n3 = 0
        xor = 0
        for n in range(live_lo(k, 53), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p106_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n3 += 1
                    xor ^= 1
            n_ok += 1
        want = want_p28_gxor(k - 2)
        if xor != 1 or xor != want:
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n3": n3, "xor": xor}
    ok = n_ok > 0 and rows["7"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p106() -> dict:
    """k<=K_THIN: covering p=106 xor = want_p106_pack; k>=7 form 1001."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 106, (T - 106) // 2
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
                        if packed != want_and106_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 3:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
                            return {"ok": False, "g1": True, "k": k, "n": n}
                        if packed and G(n, j) == 1 and four != PAT1001:
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
        want = want_p106_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 7 and xor_a != want_p28_gxor(k - 2):
            return {"ok": False, "p28": True, "k": k, "xor_a": xor_a}
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
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    qc = json.loads(QC_JSON.read_text())
    pl = json.loads(PL_JSON.read_text())
    pv = json.loads(PV_JSON.read_text())
    pc = json.loads(PC_JSON.read_text())
    ok = (
        qc["checks"]["all_ok"]
        and pl["checks"]["all_ok"]
        and pv["checks"]["all_ok"]
        and pc["checks"]["all_ok"]
        and qc["verdict"]["p98_xor_k_ge_6"] == "LEMMA"
        and pl["verdict"]["p28_silent_all_k"] == "LEMMA"
        and pv["verdict"]["p16_gxor_k_ge_3"] == "LEMMA"
        and pc["verdict"]["p14_set_k_ge_3"] == "LEMMA"
        and qc["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qc["verdict"]["prize"] == "unsolved"
        and want_p106_pack(5) == 1
        and want_p106_pack(6) == 0
        and want_p106_pack(7) == 1
        and want_p98_pack(6) == 1
        and want_p28_gxor(3) == 0
        and want_p28_gxor(4) == 1
        and want_p14_gxor(3) == 1
        and want_p16_gxor(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g28, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g28["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b103106()
    per = left107_period()
    g28 = green_p28()
    gr = green_n3()
    thin = thin_p106()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g28, gr, thin, sc, pref)
    dump = {
        "cycle": "QD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b103106": {k: fr[k] for k in fr if k != "ok"},
        "left107_period": {k: per[k] for k in per if k != "ok"},
        "green_p28": {k: g28[k] for k in g28 if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p106": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit103_106_mod8": True,
            "and106_even_t_ge_148": True,
            "p28_gxor_k_ge_4": True,
            "p106_n3_via_p28": True,
            "p106_xor_iff_k5_or_ge7": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p106_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit103_106_mod8": "LEMMA",
            "left107_period8": "LEMMA",
            "and106_even_t_ge_148": "LEMMA",
            "p28_gxor_k_ge_4": "LEMMA",
            "p106_n3_via_p28": "LEMMA",
            "p106_xor_iff_k5_or_ge7": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p106_silent": "KILLED",
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
        "frozen_b103106 n_ok",
        dump["frozen_b103106"]["n_ok"],
        "n_even",
        dump["frozen_b103106"]["n_even"],
        "early106",
        dump["frozen_b103106"]["early106"],
    )
    print(
        "thin_p106 rows",
        {k: dump["thin_p106"]["rows"][k] for k in ("4", "5", "6", "8")},
    )
    print("green_p28 rows", dump["green_p28"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
