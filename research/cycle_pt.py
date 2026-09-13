#!/usr/bin/env python3
"""Cycle PT: covering packed AND xor at p=70 is 1 for k>=6.

Bits 67..70 freeze from t>=100: bit 67 is 1 iff t%8 in (0, 1, 3, 6);
bit 68 is 1 iff t%8 in (0, 2, 3, 4, 7); bit 69 is 1 iff t%8 in
(0, 2, 3, 5, 6); bit 70 is 1 iff t%8 in (5, 6, 7). The left 71
bits are autonomous; the word at t=100 equals t=108, so even
t>=100 has p=70 4-tuple 1110 / 0110 / 0100 / 1011 on t%8 =
0,2,4,6, AND iff t%8==4. Covering even s=10U-2n-2 has s%8==4 iff
n%4==1. For k>=6 (t0>=128>=100) packed AND on G=1 is 0100 iff
n%4==1. Those n=4t+1 double twice to Green p=18 at k-2, whose xor
is 1 for k>=3 (odd n doubles to parent p=10), so packed xor is 1
for k>=6. Early even AND-ones are 34,36,50,52,62,64,84; k<=5 xor=0.
Packed p=18 is silent for k>=2 (Cycle PI) while Green p=18 fires.
Leftover, not UNIQUE_REST. Not rest=S xor T. Not E_k=0 for all k.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_pt.py --certify
Dump: research/cycle_pt.json
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
from cycle_pm import in_p10, want_p10_gxor
from cycle_po import want_b61, want_b62, want_b63, want_b64
from cycle_pq import cover_nmod
from cycle_ps import want_b51, want_b52, want_b53, want_b54
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PS_JSON = Path(__file__).resolve().parent / "cycle_ps.json"
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"
PI_JSON = Path(__file__).resolve().parent / "cycle_pi.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 128
N_LEFT = 128
K_THIN = 8
K_SET = 10
PAT1110 = (1, 1, 1, 0)
PAT0110 = (0, 1, 1, 0)
PAT0100 = (0, 1, 0, 0)
PAT1011 = (1, 0, 1, 1)
EARLY70 = {34, 36, 50, 52, 62, 64, 84}


def want_b67(t: int) -> int:
    """Packed bit 67: 1 iff t%8 in (0, 1, 3, 6) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 in (0, 1, 3, 6))


def want_b68(t: int) -> int:
    """Packed bit 68: 1 iff t%8 in (0, 2, 3, 4, 7) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 in (0, 2, 3, 4, 7))


def want_b69(t: int) -> int:
    """Packed bit 69: 1 iff t%8 in (0, 2, 3, 5, 6) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 in (0, 2, 3, 5, 6))


def want_b70(t: int) -> int:
    """Packed bit 70: 1 iff t%8 in (5, 6, 7) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 in (5, 6, 7))


def want_and70_even(t: int) -> int:
    """Even t>=100: AND at p=70 iff t%8==4. Early even AND-ones listed."""
    if t % 2:
        return 0
    if t < 100:
        return int(t in EARLY70)
    return int(t % 8 == 4)


def even70_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=100 p=70 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT1110
    if r == 2:
        return PAT0110
    if r == 4:
        return PAT0100
    return PAT1011


def want_p70_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=70, all k."""
    return int(k >= 6)


def want_p18_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=18, all k."""
    return int(k >= 3)


def in_p18(n: int, k: int) -> bool:
    """G(n, 5*2^k-9)=1 on the covering live window, k>=3."""
    U = 1 << k
    if k < 3 or n < live_lo(k, 9) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    return in_p10((n - 1) // 2, k - 1)


def in_p70_n1(n: int, k: int) -> bool:
    """n%4==1 and G(n, 5*2^k-35)=1, k>=5, via parent p=18 at k-2."""
    if k < 5 or n % 4 != 1:
        return False
    U = 1 << k
    if n < live_lo(k, 35) or n >= 4 * U:
        return False
    return in_p18((n - 1) // 4, k - 2)


def frozen_b6770() -> dict:
    """t<=N_BIT: bits 67..70 for t>=100; even t>=100 AND iff t%8==4."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 71)]
        if t >= 78 and (
            b[51] != want_b51(t)
            or b[52] != want_b52(t)
            or b[53] != want_b53(t)
            or b[54] != want_b54(t)
        ):
            return {"ok": False, "ps": t}
        if t >= 92 and (
            b[61] != want_b61(t)
            or b[62] != want_b62(t)
            or b[63] != want_b63(t)
            or b[64] != want_b64(t)
        ):
            return {"ok": False, "po": t}
        if t >= 100:
            got = (b[67], b[68], b[69], b[70])
            want = (want_b67(t), want_b68(t), want_b69(t), want_b70(t))
            if got != want:
                return {"ok": False, "b6770": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[67:71])
            a = and_clause(*four)
            if t >= 100:
                wp = even70_pat(t)
                if four != wp or a != want_and70_even(t):
                    return {"ok": False, "p70": t, "four": four}
                if a and cover_nmod(t) != 1:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 71) - 1)
            if left_step(word, 70) != (nxt & ((1 << 71) - 1)):
                return {"ok": False, "auto71": t}
        row = nxt
    if early != sorted(EARLY70):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 98) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early70": early,
        "t_hi": N_BIT,
    }


def left71_period() -> dict:
    """Left 71 bits autonomous; t=100 equals t=108; even t>=100 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 70
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
    if rows[100] != rows[108]:
        return {"ok": False, "seed": True, "t100": rows[100], "t108": rows[108]}
    n_even = 0
    for t in range(100, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(67, 71))
        if b != even70_pat(t) or and_clause(*b) != want_and70_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 98) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t100": rows[100], "t108": rows[108]}


def green_p18() -> dict:
    """k=3..K_SET: in_p18 matches G; xor=want_p18_gxor=want_p10_gxor(k-1)."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        j = 5 * U - 9
        n1 = 0
        xor = 0
        for n in range(live_lo(k, 9), 4 * U):
            g = G(n, j)
            if g != int(in_p18(n, k)):
                return {"ok": False, "k": k, "n": n, "g": g}
            if g:
                n1 += 1
                xor ^= 1
            n_ok += 1
        if xor != want_p18_gxor(k) or xor != want_p10_gxor(k - 1):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": n1, "xor": xor}
    ok = n_ok > 0 and rows["3"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n1() -> dict:
    """k=5..K_SET: n%4==1 G=1 at p=70 is in_p70_n1; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(5, K_SET + 1):
        U = 1 << k
        j = 5 * U - 35
        n1 = []
        xor = 0
        for n in range(live_lo(k, 35), 4 * U):
            g = G(n, j)
            if n % 4 == 1:
                if g != int(in_p70_n1(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n1.append(n)
                    xor ^= 1
            n_ok += 1
        if xor != 1 or xor != want_p18_gxor(k - 2):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": len(n1), "xor": xor}
    ok = n_ok > 0 and rows["5"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p70() -> dict:
    """k<=K_THIN: covering p=70 xor = want_p70_pack; k>=6 form 0100."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 70, (T - 70) // 2
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
                        if packed != want_and70_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and n % 4 != 1:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 1):
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
        want = want_p70_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != want_p18_gxor(k - 2):
            return {"ok": False, "p18": True, "k": k, "xor_a": xor_a}
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
        and rows["5"]["xor_a"] == 0
        and rows["6"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    ps = json.loads(PS_JSON.read_text())
    pm = json.loads(PM_JSON.read_text())
    pi = json.loads(PI_JSON.read_text())
    ok = (
        ps["checks"]["all_ok"]
        and pm["checks"]["all_ok"]
        and pi["checks"]["all_ok"]
        and ps["verdict"]["p54_xor_k_ge_4"] == "LEMMA"
        and pm["verdict"]["p10_gxor_k_ge_2"] == "LEMMA"
        and pi["verdict"]["p18_silent_k_ge_2"] == "LEMMA"
        and ps["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ps["verdict"]["prize"] == "unsolved"
        and want_p70_pack(5) == 0
        and want_p70_pack(6) == 1
        and want_p18_gxor(2) == 0
        and want_p18_gxor(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g18, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g18["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b6770()
    per = left71_period()
    g18 = green_p18()
    gr = green_n1()
    thin = thin_p70()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g18, gr, thin, sc, pref)
    dump = {
        "cycle": "PT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b6770": {k: fr[k] for k in fr if k != "ok"},
        "left71_period": {k: per[k] for k in per if k != "ok"},
        "green_p18": {k: g18[k] for k in g18 if k != "ok"},
        "green_n1": {k: gr[k] for k in gr if k != "ok"},
        "thin_p70": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit67_70_mod8": True,
            "and70_even_t_ge_100": True,
            "p18_gxor_k_ge_3": True,
            "p70_n1_via_p18": True,
            "p70_xor_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p70_silent": False,
            "prize": False,
        },
        "verdict": {
            "bit67_70_mod8": "LEMMA",
            "left71_period8": "LEMMA",
            "and70_even_t_ge_100": "LEMMA",
            "p18_gxor_k_ge_3": "LEMMA",
            "p70_n1_via_p18": "LEMMA",
            "p70_xor_k_ge_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p70_silent": "KILLED",
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
        "frozen_b6770 n_ok",
        dump["frozen_b6770"]["n_ok"],
        "n_even",
        dump["frozen_b6770"]["n_even"],
        "early70",
        dump["frozen_b6770"]["early70"],
    )
    print(
        "thin_p70 rows",
        {k: dump["thin_p70"]["rows"][k] for k in ("5", "6", "8")},
    )
    print("green_p18 rows", dump["green_p18"]["rows"])
    print("green_n1 rows", dump["green_n1"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
