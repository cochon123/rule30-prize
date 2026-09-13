#!/usr/bin/env python3
"""Cycle QC: covering packed AND xor at p=98 is 1 for k>=6.

Bits 95..98 freeze from t>=132: bit 95 is 1 iff t%8 in (3, 5);
bit 96 is 1 iff t%8 in (2, 7); bit 97 is 1 iff t%8 not in (4, 5);
bit 98 is 1 iff t%8 not in (0, 3). The left 99 bits are autonomous;
the word at t=132 equals t=140, so even t>=132 has p=98 4-tuple
0010 / 0111 / 0001 / 0011 on t%8 = 0,2,4,6, AND iff t%8 in (0, 6).
Covering even s=10U-2n-2 has s%8 in (0, 6) iff n%4 in (3, 0).
j=5U-49 is odd so even n have G=0. For k>=6 (t0>=128, freeze 132
so t0>=256 at k>=7; k=6 t0=128 is before freeze but thin still
matches) packed AND on G=1 is 0010 iff n%4==3. Those n=4t+3
double twice to Green p=26 at k-2. Green p=26 xor is 1 for k>=4
(odd n via parent p=14 at k-1). Packed p=26 is silent for every k
(Cycle PL) while Green p=26 fires. Early even AND-ones are
48,52,64,66,68,88,90,92,98,114,116,130; k=4 xor=0, k=5 xor=0.
UNIQUE_REST p=98. Cycle LJ's k<=6 0010 is this all-k lemma for
k>=6. Not rest=S xor T. Not unique-rest xor=0. Not E_k=0 for all
k. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_qc.py --certify
Dump: research/cycle_qc.json
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
from cycle_qb import want_b87, want_b88, want_p88_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QB_JSON = Path(__file__).resolve().parent / "cycle_qb.json"
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 180
N_LEFT = 180
K_THIN = 8
K_SET = 10
PAT0010 = (0, 0, 1, 0)
PAT0111 = (0, 1, 1, 1)
PAT0001 = (0, 0, 0, 1)
PAT0011 = (0, 0, 1, 1)
EARLY98 = {48, 52, 64, 66, 68, 88, 90, 92, 98, 114, 116, 130}


def want_b95(t: int) -> int:
    """Packed bit 95: 1 iff t%8 in (3, 5) for t>=132."""
    if t < 132:
        return 0
    return int(t % 8 in (3, 5))


def want_b96(t: int) -> int:
    """Packed bit 96: 1 iff t%8 in (2, 7) for t>=132."""
    if t < 132:
        return 0
    return int(t % 8 in (2, 7))


def want_b97(t: int) -> int:
    """Packed bit 97: 1 iff t%8 not in (4, 5) for t>=132."""
    if t < 132:
        return 0
    return int(t % 8 not in (4, 5))


def want_b98(t: int) -> int:
    """Packed bit 98: 1 iff t%8 not in (0, 3) for t>=132."""
    if t < 132:
        return 0
    return int(t % 8 not in (0, 3))


def want_and98_even(t: int) -> int:
    """Even t>=132: AND at p=98 iff t%8 in (0, 6). Early listed."""
    if t % 2:
        return 0
    if t < 132:
        return int(t in EARLY98)
    return int(t % 8 in (0, 6))


def even98_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=132 p=98 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0010
    if r == 2:
        return PAT0111
    if r == 4:
        return PAT0001
    return PAT0011


def want_p98_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=98, all k."""
    return int(k >= 6)


def want_p26_gxor(k: int) -> int:
    """Covering Green G=1 xor at p=26, all k."""
    return int(k >= 4)


def in_p26(n: int, k: int) -> bool:
    """G(n, 5*2^k-13)=1 on the covering live window, k>=4."""
    U = 1 << k
    if k < 4 or n < live_lo(k, 13) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    return in_p14((n - 1) // 2, k - 1)


def in_p98_n3(n: int, k: int) -> bool:
    """n%4==3 and G(n, 5*2^k-49)=1, k>=6, via parent p=26 at k-2."""
    if k < 6 or n % 4 != 3:
        return False
    U = 1 << k
    if n < live_lo(k, 49) or n >= 4 * U:
        return False
    return in_p26((n - 3) // 4, k - 2)


def frozen_b9598() -> dict:
    """t<=N_BIT: bits 95..98 for t>=132; even t>=132 AND iff t%8 in (0,6)."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 99)]
        if t >= 127 and (b[87] != want_b87(t) or b[88] != want_b88(t)):
            return {"ok": False, "qb": t}
        if t >= 132:
            got = (b[95], b[96], b[97], b[98])
            want = (want_b95(t), want_b96(t), want_b97(t), want_b98(t))
            if got != want:
                return {"ok": False, "b9598": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[95:99])
            a = and_clause(*four)
            if t >= 132:
                wp = even98_pat(t)
                if four != wp or a != want_and98_even(t):
                    return {"ok": False, "p98": t, "four": four}
                if a and cover_nmod(t) not in (0, 3):
                    return {"ok": False, "nmod": t}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 99) - 1)
            if left_step(word, 98) != (nxt & ((1 << 99) - 1)):
                return {"ok": False, "auto99": t}
        row = nxt
    if early != sorted(EARLY98):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 130) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early98": early,
        "t_hi": N_BIT,
    }


def left99_period() -> dict:
    """Left 99 bits autonomous; t=132 equals t=140; even t>=132 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 98
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
    if rows[132] != rows[140]:
        return {"ok": False, "seed": True, "t132": rows[132], "t140": rows[140]}
    n_even = 0
    for t in range(132, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(95, 99))
        if b != even98_pat(t) or and_clause(*b) != want_and98_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 130) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t132": rows[132],
        "t140": rows[140],
    }


def green_p26() -> dict:
    """k=3..K_SET: xor=want; k>=4 in_p26 match G."""
    n_ok = 0
    rows = {}
    for k in range(3, K_SET + 1):
        U = 1 << k
        n26 = x26 = 0
        j26 = 5 * U - 13
        for n in range(live_lo(k, 13), 4 * U):
            g = G(n, j26)
            if k >= 4 and g != int(in_p26(n, k)):
                return {"ok": False, "p26": True, "k": k, "n": n, "g": g}
            if g:
                n26 += 1
                x26 ^= 1
            n_ok += 1
        if x26 != want_p26_gxor(k):
            return {"ok": False, "xor": True, "k": k, "x26": x26}
        rows[str(k)] = {"n26": n26, "x26": x26}
    ok = (
        n_ok > 0
        and rows["3"]["x26"] == 0
        and rows["4"]["x26"] == 1
        and rows[str(K_SET)]["x26"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def green_n3() -> dict:
    """k=6..K_SET: n%4==3 G=1 at p=98 is in_p98_n3; xor=1."""
    n_ok = 0
    rows = {}
    for k in range(6, K_SET + 1):
        U = 1 << k
        j = 5 * U - 49
        n3 = 0
        xor = 0
        for n in range(live_lo(k, 49), 4 * U):
            g = G(n, j)
            if n % 4 == 3:
                if g != int(in_p98_n3(n, k)):
                    return {"ok": False, "k": k, "n": n, "g": g}
                if g:
                    n3 += 1
                    xor ^= 1
            n_ok += 1
        want = want_p26_gxor(k - 2)
        if xor != 1 or xor != want:
            return {"ok": False, "xor": True, "k": k, "xor": xor}
        rows[str(k)] = {"n3": n3, "xor": xor}
    ok = n_ok > 0 and rows["6"]["xor"] == 1 and rows[str(K_SET)]["xor"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def thin_p98() -> dict:
    """k<=K_THIN: covering p=98 xor = want_p98_pack; k>=6 form 0010."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 98, (T - 98) // 2
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
                        if packed != want_and98_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
                        if packed and G(n, j) == 1 and n % 4 != 3:
                            return {"ok": False, "nmod": True, "k": k, "n": n}
                        if G(n, j) == 1 and packed != int(n % 4 == 3):
                            return {"ok": False, "g1": True, "k": k, "n": n}
                        if packed and G(n, j) == 1 and four != PAT0010:
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
        want = want_p98_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and xor_a != want_p26_gxor(k - 2):
            return {"ok": False, "p26": True, "k": k, "xor_a": xor_a}
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
        and rows["5"]["xor_a"] == 0
        and rows["6"]["xor_a"] == 1
        and rows["8"]["xor_a"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    qb = json.loads(QB_JSON.read_text())
    pl = json.loads(PL_JSON.read_text())
    pc = json.loads(PC_JSON.read_text())
    ok = (
        qb["checks"]["all_ok"]
        and pl["checks"]["all_ok"]
        and pc["checks"]["all_ok"]
        and qb["verdict"]["p88_xor_iff_k4_or_ge6"] == "LEMMA"
        and pl["verdict"]["p26_silent_all_k"] == "LEMMA"
        and pc["verdict"]["p14_set_k_ge_3"] == "LEMMA"
        and qb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qb["verdict"]["prize"] == "unsolved"
        and want_p98_pack(5) == 0
        and want_p98_pack(6) == 1
        and want_p88_pack(4) == 1
        and want_p26_gxor(3) == 0
        and want_p26_gxor(4) == 1
        and want_p14_gxor(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, g26, gr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert g26["ok"] and gr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b9598()
    per = left99_period()
    g26 = green_p26()
    gr = green_n3()
    thin = thin_p98()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, g26, gr, thin, sc, pref)
    dump = {
        "cycle": "QC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b9598": {k: fr[k] for k in fr if k != "ok"},
        "left99_period": {k: per[k] for k in per if k != "ok"},
        "green_p26": {k: g26[k] for k in g26 if k != "ok"},
        "green_n3": {k: gr[k] for k in gr if k != "ok"},
        "thin_p98": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit95_98_mod8": True,
            "and98_even_t_ge_132": True,
            "p26_gxor_k_ge_4": True,
            "p98_n3_via_p26": True,
            "p98_xor_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p98_silent": False,
            "unique_rest_xor0": False,
            "prize": False,
        },
        "verdict": {
            "bit95_98_mod8": "LEMMA",
            "left99_period8": "LEMMA",
            "and98_even_t_ge_132": "LEMMA",
            "p26_gxor_k_ge_4": "LEMMA",
            "p98_n3_via_p26": "LEMMA",
            "p98_xor_k_ge_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p98_silent": "KILLED",
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
        "frozen_b9598 n_ok",
        dump["frozen_b9598"]["n_ok"],
        "n_even",
        dump["frozen_b9598"]["n_even"],
        "early98",
        dump["frozen_b9598"]["early98"],
    )
    print(
        "thin_p98 rows",
        {k: dump["thin_p98"]["rows"][k] for k in ("4", "5", "6", "8")},
    )
    print("green_p26 rows", dump["green_p26"]["rows"])
    print("green_n3 rows", dump["green_n3"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
