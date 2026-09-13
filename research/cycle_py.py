#!/usr/bin/env python3
"""Cycle PY: covering packed AND xor at p=72 is 1 iff k==3.

Bits 69..72 freeze from t>=100: bit 69 is 1 iff t%8 in (0, 2, 3, 5, 6);
bit 70 is 1 iff t%8 in (5, 6, 7); bit 71 is 1 iff t%8 in (0, 3);
bit 72 is 1 iff t%8 not in (0, 6). The left 73 bits are autonomous;
the word at t=100 equals t=108, so even t>=100 has p=72 4-tuple
1010 / 1001 / 0001 / 1100 on t%8 = 0,2,4,6, AND iff t%8==2.
Covering even s=10U-2n-2 has s%8==2 iff n%4==2. j=5U-36 is even
so even n can fire. For k>=6 (t0>=128>=100) packed AND on G=1 is
1001 iff n%4==2. Those n=4t+2 double twice to Green p=18 xor p=20
at k-2. Green p=18 xor is 1 for k>=3 and Green p=20 xor is 1 for
k>=4, so the slices cancel and packed xor is 0 for k>=6. Early
even AND-ones are 58,60,80,84,88,90; k=3 xor=1, k=4 and k=5 xor=0.
Packed p=18 is silent for k>=2 and packed p=20 is silent for k>=4
(Cycle PI) while both Green columns fire. UNIQUE_REST p=72. Cycle
LP's k<=6 1001 form is this all-k lemma for k>=4. Not rest=S xor T.
Not unique-rest xor=0. Not E_k=0 for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_py.py --certify
Dump: research/cycle_py.json
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
from cycle_pc import in_p6, live_lo
from cycle_pd import left_step
from cycle_pm import in_p10
from cycle_pn import in_p12
from cycle_pq import cover_nmod
from cycle_pt import in_p18, want_b67, want_b68, want_b69, want_b70, want_p18_gxor
from cycle_px import want_p60_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PX_JSON = Path(__file__).resolve().parent / "cycle_px.json"
PT_JSON = Path(__file__).resolve().parent / "cycle_pt.json"
PI_JSON = Path(__file__).resolve().parent / "cycle_pi.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 128
N_LEFT = 128
K_THIN = 8
K_SET = 10
PAT1010 = (1, 0, 1, 0)
PAT1001 = (1, 0, 0, 1)
PAT0001 = (0, 0, 0, 1)
PAT1100 = (1, 1, 0, 0)
EARLY72 = {58, 60, 80, 84, 88, 90}


def want_b71(t: int) -> int:
    """Packed bit 71: 1 iff t%8 in (0, 3) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 in (0, 3))


def want_b72(t: int) -> int:
    """Packed bit 72: 1 iff t%8 not in (0, 6) for t>=100."""
    if t < 100:
        return 0
    return int(t % 8 not in (0, 6))


def want_and72_even(t: int) -> int:
    """Even t>=100: AND at p=72 iff t%8==2. Early listed."""
    if t % 2:
        return 0
    if t < 100:
        return int(t in EARLY72)
    return int(t % 8 == 2)


def even72_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=100 p=72 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT1010
    if r == 2:
        return PAT1001
    if r == 4:
        return PAT0001
    return PAT1100


def want_p72_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=72, all k."""
    return int(k == 3)


def want_p20_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=20, all k."""
    return int(k >= 4)


def in_p20(n: int, k: int) -> bool:
    """G(n, 5*2^k-10)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 10) or n >= 4 * U:
        return False
    if n % 2 == 0:
        if n % 4 != 2:
            return False
        return in_p6((n - 2) // 4, k - 2)
    m = (n - 1) // 2
    return bool(in_p10(m, k - 1)) != bool(in_p12(m, k - 1))


def in_p72_n2(n: int, k: int) -> bool:
    """n%4==2 and G(n, 5*2^k-36)=1, k>=6, via parent p=18 xor p=20."""
    if k < 6 or n % 4 != 2:
        return False
    U = 1 << k
    if n < live_lo(k, 36) or n >= 4 * U:
        return False
    t = (n - 2) // 4
    return bool(in_p18(t, k - 2)) != bool(in_p20(t, k - 2))


def frozen_b6972() -> dict:
    """t<=N_BIT: bits 69..72 for t>=100; even t>=100 AND iff t%8==2."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 73)]
        if t >= 100 and (
            b[67] != want_b67(t)
            or b[68] != want_b68(t)
            or b[69] != want_b69(t)
            or b[70] != want_b70(t)
        ):
            return {"ok": False, "pt": t}
        if t >= 100:
            got = (b[69], b[70], b[71], b[72])
            want = (want_b69(t), want_b70(t), want_b71(t), want_b72(t))
            if got != want:
                return {"ok": False, "b6972": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[69:73])
            a = and_clause(*four)
            if t >= 100:
                wp = even72_pat(t)
                if four != wp or a != want_and72_even(t):
                    return {"ok": False, "p72": t, "four": four}
                if a and cover_nmod(t) != 2:
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 73) - 1)
            if left_step(word, 72) != (nxt & ((1 << 73) - 1)):
                return {"ok": False, "auto73": t}
        row = nxt
    if early != sorted(EARLY72):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 98) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early72": early,
        "t_hi": N_BIT,
    }


def left73_period() -> dict:
    """Left 73 bits autonomous; t=100 equals t=108; even t>=100 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 72
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
        b = tuple((rows[t] >> p) & 1 for p in range(69, 73))
        if b != even72_pat(t) or and_clause(*b) != want_and72_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 98) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t100": rows[100],
        "t108": rows[108],
    }


def green_p20() -> dict:
    """k=2..K_SET: xor=want_p20_gxor; k>=4 in_p20 matches G."""
    n_ok = 0
    rows = {}
    for k in range(2, K_SET + 1):
        U = 1 << k
        j = 5 * U - 10
        n1 = 0
        xor = 0
        for n in range(live_lo(k, 10), 4 * U):
            g = G(n, j)
            if k >= 4 and g != int(in_p20(n, k)):
                return {"ok": False, "k": k, "n": n, "g": g}
            if g:
                n1 += 1
                xor ^= 1
            n_ok += 1
        if xor != want_p20_gxor(k):
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n1": n1, "xor": xor}
    ok = (
        n_ok > 0
        and rows["2"]["xor"] == 0
        and rows["3"]["xor"] == 0
        and rows["4"]["xor"] == 1
        and rows[str(K_SET)]["xor"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n2() -> dict:
    """k=6..K_SET: n%4==2 G=1 at p=72 is in_p72_n2; xor=0."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 36
        n2 = 0
        xor = 0
        for n in range(live_lo(k, 36), 4 * U):
            g = G(n, j)
            if n % 4 == 2:
                if g != int(in_p72_n2(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n2 += 1
                    xor ^= 1
            n_ok += 1
        want = want_p18_gxor(k - 2) ^ want_p20_gxor(k - 2)
        if xor != 0 or xor != want:
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n2": n2, "xor": xor}
    ok = n_ok > 0 and rows["6"]["xor"] == 0 and rows[str(K_SET)]["xor"] == 0
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p72() -> dict:
    """k<=K_THIN: covering p=72 xor = want_p72_pack; k>=6 form 1001."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 72, (T - 72) // 2
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
                        if packed != want_and72_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 2:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 2):
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
        want = want_p72_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != (want_p18_gxor(k - 2) ^ want_p20_gxor(k - 2)):
            return {"ok": False, "p1820": True, "k": k, "xor_a": xor_a}
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
        and rows["5"]["xor_a"] == 0
        and rows["8"]["xor_a"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    px = json.loads(PX_JSON.read_text())
    pt = json.loads(PT_JSON.read_text())
    pi = json.loads(PI_JSON.read_text())
    ok = (
        px["checks"]["all_ok"]
        and pt["checks"]["all_ok"]
        and pi["checks"]["all_ok"]
        and px["verdict"]["p60_xor_iff_k4"] == "LEMMA"
        and pt["verdict"]["p18_gxor_k_ge_3"] == "LEMMA"
        and pi["verdict"]["p20_silent_k_ge_4"] == "LEMMA"
        and px["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and px["verdict"]["prize"] == "unsolved"
        and want_p72_pack(3) == 1
        and want_p72_pack(4) == 0
        and want_p60_pack(4) == 1
        and want_p18_gxor(3) == 1
        and want_p20_gxor(3) == 0
        and want_p20_gxor(4) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g20, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g20["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b6972()
    per = left73_period()
    g20 = green_p20()
    gr = green_n2()
    thin = thin_p72()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g20, gr, thin, sc, pref)
    dump = {
        "cycle": "PY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b6972": {k: fr[k] for k in fr if k != "ok"},
        "left73_period": {k: per[k] for k in per if k != "ok"},
        "green_p20": {k: g20[k] for k in g20 if k != "ok"},
        "green_n2": {k: gr[k] for k in gr if k != "ok"},
        "thin_p72": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit69_72_mod8": True,
            "and72_even_t_ge_100": True,
            "p20_gxor_k_ge_4": True,
            "p72_n2_via_p18_p20": True,
            "p72_xor_iff_k3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p72_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit69_72_mod8": "LEMMA",
            "left73_period8": "LEMMA",
            "and72_even_t_ge_100": "LEMMA",
            "p20_gxor_k_ge_4": "LEMMA",
            "p72_n2_via_p18_p20": "LEMMA",
            "p72_xor_iff_k3": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p72_silent": "KILLED",
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
        "frozen_b6972 n_ok",
        dump["frozen_b6972"]["n_ok"],
        "n_even",
        dump["frozen_b6972"]["n_even"],
        "early72",
        dump["frozen_b6972"]["early72"],
    )
    print(
        "thin_p72 rows",
        {k: dump["thin_p72"]["rows"][k] for k in ("3", "4", "5", "8")},
    )
    print("green_p20 rows", dump["green_p20"]["rows"])
    print("green_n2 rows", dump["green_n2"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
