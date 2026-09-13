#!/usr/bin/env python3
"""Cycle PL: bits 23..26 freeze; covering p=26 silent for every k.

Bit 23 is 1 iff t is even for t>=30; bit 24 is 1 iff t%4==3; bit
25 is 1 iff t%4 in (0, 3); bit 26 is 1 iff t%4 != 0. The left 27
bits are autonomous; the word at t=30 equals t=34, so even t>=30
has p=26 4-tuple 1001 iff t%4==2 else 1010. AND fires iff t%4==2,
hence covering even s has p=26 AND iff n is even, but j=5U-13 is
odd so even n have G=0. Early even AND-ones are only 12,14, and
G(13,7)=G(12,7)=0. Hence covering p=26 is silent for every k.
Even t>=28 has p=24 4-tuple 1110 or 1010, so covering p=24 is
silent for k>=4. Even t>=32 has p=28 4-tuple 1000 or 0110, so
covering p=28 is silent for every k. Not rest=S xor T. Not E_k=0
for all k. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_pl.py --certify
Dump: research/cycle_pl.json
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
from cycle_pj import want_b19, want_b20, want_b21, want_b22
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PK_JSON = Path(__file__).resolve().parent / "cycle_pk.json"
PJ_JSON = Path(__file__).resolve().parent / "cycle_pj.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 48
K_THIN = 8
PAT1001 = (1, 0, 0, 1)
PAT1010 = (1, 0, 1, 0)
PAT1110 = (1, 1, 1, 0)
PAT1000 = (1, 0, 0, 0)
PAT0110 = (0, 1, 1, 0)
EARLY26 = {12, 14}
EARLY24 = {16}
EARLY28 = {14, 22}


def want_b23(t: int) -> int:
    """Packed bit 23: 1 iff t even for t>=30."""
    if t < 30:
        return 0
    return int(t % 2 == 0)


def want_b24(t: int) -> int:
    """Packed bit 24: 1 iff t%4==3 for t>=30."""
    if t < 30:
        return 0
    return int(t % 4 == 3)


def want_b25(t: int) -> int:
    """Packed bit 25: 1 iff t%4 in (0, 3) for t>=30."""
    if t < 30:
        return 0
    return int(t % 4 in (0, 3))


def want_b26(t: int) -> int:
    """Packed bit 26: 1 iff t%4 != 0 for t>=30."""
    if t < 30:
        return 0
    return int(t % 4 != 0)


def want_and26_even(t: int) -> int:
    """Even t>=30: AND at p=26 iff t%4==2."""
    if t < 30 or t % 2:
        return int(t in EARLY26)
    return int(t % 4 == 2)


def frozen_b2326() -> dict:
    """t<=N_BIT: bits 23..26 for t>=30; even p=24/26/28 4-tuples."""
    row = 1
    n_ok = 0
    n_even26 = 0
    n_even24 = 0
    n_even28 = 0
    early26, early24, early28 = [], [], []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 29)]
        if t >= 28 and (
            b[19] != want_b19(t)
            or b[20] != want_b20(t)
            or b[21] != want_b21(t)
            or b[22] != want_b22(t)
        ):
            return {"ok": False, "pj": t}
        if t >= 30:
            got = (b[23], b[24], b[25], b[26])
            want = (want_b23(t), want_b24(t), want_b25(t), want_b26(t))
            if got != want:
                return {"ok": False, "b2326": t, "got": got, "want": want}
        if t % 2 == 0:
            four26 = tuple(b[23:27])
            a26 = and_clause(*four26)
            if t >= 30:
                want26 = PAT1001 if t % 4 == 2 else PAT1010
                if four26 != want26 or a26 != want_and26_even(t):
                    return {"ok": False, "p26": t, "four": four26}
                n_even26 += 1
            elif a26:
                early26.append(t)
            four24 = tuple(b[21:25])
            a24 = and_clause(*four24)
            if t >= 28:
                want24 = PAT1110 if t % 4 == 0 else PAT1010
                if four24 != want24 or a24 != 0:
                    return {"ok": False, "p24": t, "four": four24}
                n_even24 += 1
            elif a24:
                early24.append(t)
            four28 = tuple(b[25:29])
            a28 = and_clause(*four28)
            if t >= 32:
                want28 = PAT1000 if t % 4 == 0 else PAT0110
                if four28 != want28 or a28 != 0:
                    return {"ok": False, "p28": t, "four": four28}
                n_even28 += 1
            elif a28:
                early28.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 27) - 1)
            if left_step(word, 26) != (nxt & ((1 << 27) - 1)):
                return {"ok": False, "auto27": t}
        row = nxt
    if early26 != sorted(EARLY26) or early24 != sorted(EARLY24) or early28 != sorted(EARLY28):
        return {"ok": False, "early": (early24, early26, early28)}
    ok = n_ok == N_BIT + 1 and n_even26 == (N_BIT - 28) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even26": n_even26,
        "n_even24": n_even24,
        "n_even28": n_even28,
        "early26": early26,
        "early24": early24,
        "early28": early28,
        "t_hi": N_BIT,
    }


def left27_period() -> dict:
    """Left 27 bits autonomous; t=30 equals t=34; even t>=30 period 4."""
    row = 1
    rows = []
    n_ok = 0
    w = 26
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
    if rows[30] != rows[34]:
        return {"ok": False, "seed": True, "t30": rows[30], "t34": rows[34]}
    n_even = 0
    for t in range(30, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(23, 27))
        want = PAT1001 if t % 4 == 2 else PAT1010
        if b != want:
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 28) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t30": rows[30], "t34": rows[34]}


def early_miss() -> dict:
    """Early AND-1 covering n miss G=1 at p=26 and p=28."""
    if G(13, 7) != 0 or G(12, 7) != 0:
        return {"ok": False, "p26k2": True}
    if G(12, 6) != 0 or G(8, 6) != 0 or G(28, 26) != 0:
        return {"ok": False, "p28": True}
    return {"ok": True, "g13_7": 0, "g12_7": 0, "g12_6": 0, "g8_6": 0, "g28_26": 0}


def thin_p(p: int, silent_from: int) -> dict:
    """Covering AND xor at packed p; n_and=0 for k>=silent_from."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        j = (T - p) // 2
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
                t = (s - t0) // 2
                n = odd_clock(t, U, Q)
                if 0 <= j <= 2 * n:
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                        else:
                            n_sil += 1
            row = rule30_step(row)
            s += 1
        if k >= silent_from and n_and != 0:
            return {"ok": False, "k": k, "p": p, "n_and": n_and}
        rows[str(k)] = {
            "xor_a": xor_a,
            "n_g": n_g,
            "n_and": n_and,
            "n_sil": n_sil,
            "j": j,
            "t0": t0,
        }
        n_ok += 1
    ok = n_ok == K_THIN + 1 and rows[str(silent_from)]["n_and"] == 0
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "silent_from": silent_from, "rows": rows}


def prefixes() -> dict:
    pk = json.loads(PK_JSON.read_text())
    pj = json.loads(PJ_JSON.read_text())
    ok = (
        pk["checks"]["all_ok"]
        and pj["checks"]["all_ok"]
        and pk["verdict"]["p32_xor_k_ge_5"] == "LEMMA"
        and pj["verdict"]["p22_silent_all_k"] == "LEMMA"
        and pk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, miss, t26, t24, t28, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert miss["ok"] and t26["ok"] and t24["ok"] and t28["ok"]
    assert sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b2326()
    per = left27_period()
    miss = early_miss()
    t26 = thin_p(26, 0)
    t24 = thin_p(24, 4)
    t28 = thin_p(28, 0)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, miss, t26, t24, t28, sc, pref)
    dump = {
        "cycle": "PL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b2326": {k: fr[k] for k in fr if k != "ok"},
        "left27_period": {k: per[k] for k in per if k != "ok"},
        "early_miss": {k: miss[k] for k in miss if k != "ok"},
        "thin_p26": {k: t26[k] for k in t26 if k != "ok"},
        "thin_p24": {k: t24[k] for k in t24 if k != "ok"},
        "thin_p28": {k: t28[k] for k in t28 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit23_26_mod4": True,
            "and26_even_t_ge_30": True,
            "p26_silent_all_k": True,
            "p24_silent_k_ge_4": True,
            "p28_silent_all_k": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p24_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit23_26_mod4": "LEMMA",
            "left27_period4": "LEMMA",
            "and26_even_t_ge_30": "LEMMA",
            "p26_silent_all_k": "LEMMA",
            "p24_silent_k_ge_4": "LEMMA",
            "p28_silent_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p24_silent_all_k": "KILLED",
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
        "frozen n_ok",
        dump["frozen_b2326"]["n_ok"],
        "early26",
        dump["frozen_b2326"]["early26"],
        "early24",
        dump["frozen_b2326"]["early24"],
        "early28",
        dump["frozen_b2326"]["early28"],
    )
    print("thin_p26 k0/2/8", {k: dump["thin_p26"]["rows"][k] for k in ("0", "2", "8")})
    print("thin_p24 k2/4/8", {k: dump["thin_p24"]["rows"][k] for k in ("2", "4", "8")})
    print("thin_p28 k2/8", {k: dump["thin_p28"]["rows"][k] for k in ("2", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
