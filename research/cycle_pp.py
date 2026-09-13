#!/usr/bin/env python3
"""Cycle PP: covering packed AND xor at p=34 is 1 iff k in (3, 4).

Bits 33,34 freeze from t>=44: bit 33 is 1 iff t%8 in (0, 3, 7);
bit 34 is 1 iff t%8 in (0, 3, 4, 5). The left 35 bits are
autonomous; the word at t=44 equals t=52, so even t>=44 has p=34
4-tuple 1111 / 0100 / 0001 / 1000 on t%8 = 0,2,4,6, AND iff
t%8==2. Covering even s=10U-2n-2 has s%8==2 iff n%4==2. Column
j=5U-17 is odd, so even n have G=0. For k>=5 (t0=2U>=64>=44)
packed AND on G=1 is empty. Early even AND-ones are
16,26,30,32,38,42. Packed xor is 1 iff k in (3, 4). Not
rest=S xor T. Not E_k=0 for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pp.py --certify
Dump: research/cycle_pp.json
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
from cycle_pk import want_b29, want_b30, want_b31, want_b32
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PO_JSON = Path(__file__).resolve().parent / "cycle_po.json"
PK_JSON = Path(__file__).resolve().parent / "cycle_pk.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 64
K_THIN = 8
PAT1111 = (1, 1, 1, 1)
PAT0100 = (0, 1, 0, 0)
PAT0001 = (0, 0, 0, 1)
PAT1000 = (1, 0, 0, 0)
EARLY34 = {16, 26, 30, 32, 38, 42}


def want_b33(t: int) -> int:
    """Packed bit 33: 1 iff t%8 in (0, 3, 7) for t>=44."""
    if t < 44:
        return 0
    return int(t % 8 in (0, 3, 7))


def want_b34(t: int) -> int:
    """Packed bit 34: 1 iff t%8 in (0, 3, 4, 5) for t>=44."""
    if t < 44:
        return 0
    return int(t % 8 in (0, 3, 4, 5))


def want_and34_even(t: int) -> int:
    """Even t>=44: AND at p=34 iff t%8==2. Early even AND-ones listed."""
    if t < 44 or t % 2:
        return int(t in EARLY34)
    return int(t % 8 == 2)


def even34_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=44 p=34 4-tuple."""
    r = t % 8
    if r == 2:
        return PAT0100
    if r == 4:
        return PAT0001
    if r == 6:
        return PAT1000
    return PAT1111


def want_p34_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=34, all k."""
    return int(k in (3, 4))


def frozen_b3334() -> dict:
    """t<=N_BIT: bits 33,34 for t>=44; even t>=44 AND iff t%8==2."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 35)]
        if t >= 36 and (
            b[29] != want_b29(t)
            or b[30] != want_b30(t)
            or b[31] != want_b31(t)
            or b[32] != want_b32(t)
        ):
            return {"ok": False, "pk": t}
        if t >= 44:
            got = (b[33], b[34])
            want = (want_b33(t), want_b34(t))
            if got != want:
                return {"ok": False, "b3334": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[31:35])
            a = and_clause(*four)
            if t >= 44:
                wp = even34_pat(t)
                if four != wp or a != want_and34_even(t):
                    return {"ok": False, "p34": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 35) - 1)
            if left_step(word, 34) != (nxt & ((1 << 35) - 1)):
                return {"ok": False, "auto35": t}
        row = nxt
    if early != sorted(EARLY34):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 42) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early34": early,
        "t_hi": N_BIT,
    }


def left35_period() -> dict:
    """Left 35 bits autonomous; t=44 equals t=52; even t>=44 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 34
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
    if rows[44] != rows[52]:
        return {"ok": False, "seed": True, "t44": rows[44], "t52": rows[52]}
    n_even = 0
    for t in range(44, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(31, 35))
        if b != even34_pat(t) or and_clause(*b) != want_and34_even(t):
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 42) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t44": rows[44], "t52": rows[52]}


def thin_p34() -> dict:
    """k<=K_THIN: covering p=34 xor = want_p34_pack; k>=5 n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 34, (T - 34) // 2
        if j < 0:
            rows[str(k)] = {
                "xor_a": 0,
                "n_g": 0,
                "n_and": 0,
                "n_sil": 0,
                "j": j,
                "t0": t0,
                "j_odd": int(j % 2 == 1) if j >= 0 else 0,
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
                        if packed != want_and34_even(s_even):
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
        want = want_p34_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and (n_and != 0 or t0 < 44 or n_g == 0):
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
        and rows["2"]["xor_a"] == 0
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
    po = json.loads(PO_JSON.read_text())
    pk = json.loads(PK_JSON.read_text())
    ok = (
        po["checks"]["all_ok"]
        and pk["checks"]["all_ok"]
        and po["verdict"]["p64_xor_iff_k35"] == "LEMMA"
        and pk["verdict"]["p32_xor_k_ge_5"] == "LEMMA"
        and po["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and po["verdict"]["prize"] == "unsolved"
        and want_p34_pack(3) == 1
        and want_p34_pack(4) == 1
        and want_p34_pack(5) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b3334()
    per = left35_period()
    thin = thin_p34()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, thin, sc, pref)
    dump = {
        "cycle": "PP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b3334": {k: fr[k] for k in fr if k != "ok"},
        "left35_period": {k: per[k] for k in per if k != "ok"},
        "thin_p34": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit33_34_mod8": True,
            "and34_even_t_ge_44": True,
            "p34_silent_k_ge_5": True,
            "p34_xor_iff_k34": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p34_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit33_34_mod8": "LEMMA",
            "left35_period8": "LEMMA",
            "and34_even_t_ge_44": "LEMMA",
            "p34_silent_k_ge_5": "LEMMA",
            "p34_xor_iff_k34": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p34_silent_all_k": "KILLED",
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
        "frozen_b3334 n_ok",
        dump["frozen_b3334"]["n_ok"],
        "n_even",
        dump["frozen_b3334"]["n_even"],
        "early34",
        dump["frozen_b3334"]["early34"],
    )
    print(
        "thin_p34 rows",
        {k: dump["thin_p34"]["rows"][k] for k in ("2", "3", "4", "5", "8")},
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
