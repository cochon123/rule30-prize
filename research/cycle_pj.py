#!/usr/bin/env python3
"""Cycle PJ: bits 19..22 freeze; covering p=22 silent for every k.

Bit 19 is 1 iff t%4 in (2, 3) for t>=28; bit 20 is 1 iff t%4 in
(0, 1); bit 21 is 1 iff t%4 != 3; bit 22 is 1 iff t%4 in (0, 3).
The left 23 bits are autonomous; the word at t=26 equals t=30, so
even t>=26 has p=22 4-tuple 1010 (t%4==2) or 0111 (t%4==0), never
an AND-one. Even t with AND at p=22 are only 10,12. Covering k>=3
starts at 2U>=16, so misses them. k=2 has G(13,9)=G(14,9)=0. k=0,1
have j<0. Hence covering p=22 is silent for every k. Not rest=S
xor T. Not E_k=0 for all k. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pj.py --certify
Dump: research/cycle_pj.json
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
from cycle_pf import want_b7, want_b8, want_b9
from cycle_pg import want_b10
from cycle_ph import want_b13, want_b14, want_b15, want_b16
from cycle_pi import want_b17, want_b18
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PI_JSON = Path(__file__).resolve().parent / "cycle_pi.json"
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 48
K_THIN = 8
PAT1010 = (1, 0, 1, 0)
PAT0111 = (0, 1, 1, 1)
EARLY22 = {10, 12}


def want_b19(t: int) -> int:
    """Packed bit 19: 1 iff t%4 in (2, 3) for t>=28."""
    if t < 28:
        return 0
    return int(t % 4 in (2, 3))


def want_b20(t: int) -> int:
    """Packed bit 20: 1 iff t%4 in (0, 1) for t>=28."""
    if t < 28:
        return 0
    return int(t % 4 in (0, 1))


def want_b21(t: int) -> int:
    """Packed bit 21: 1 iff t%4 != 3 for t>=28."""
    if t < 28:
        return 0
    return int(t % 4 != 3)


def want_b22(t: int) -> int:
    """Packed bit 22: 1 iff t%4 in (0, 3) for t>=28."""
    if t < 28:
        return 0
    return int(t % 4 in (0, 3))


def frozen_b1922() -> dict:
    """t<=N_BIT: bits 19..22 for t>=28; even t>=26 p=22 is 1010 or 0111."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 23)]
        if b[7] != want_b7(t) or b[8] != want_b8(t) or b[9] != want_b9(t):
            return {"ok": False, "pf": t}
        if b[10] != want_b10(t):
            return {"ok": False, "pg": t}
        if t >= 16 and (
            b[13] != want_b13(t)
            or b[14] != want_b14(t)
            or b[15] != want_b15(t)
            or b[16] != want_b16(t)
        ):
            return {"ok": False, "ph": t}
        if t >= 20 and (b[17] != want_b17(t) or b[18] != want_b18(t)):
            return {"ok": False, "pi": t}
        if t >= 28:
            got = (b[19], b[20], b[21], b[22])
            want = (want_b19(t), want_b20(t), want_b21(t), want_b22(t))
            if got != want:
                return {"ok": False, "b1922": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[19:23])
            a = and_clause(*four)
            if t >= 26:
                wantf = PAT1010 if t % 4 == 2 else PAT0111
                if four != wantf or a != 0:
                    return {"ok": False, "p22": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 23) - 1)
            if left_step(word, 22) != (nxt & ((1 << 23) - 1)):
                return {"ok": False, "auto23": t}
        row = nxt
    if early != sorted(EARLY22):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 24) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early22": early,
        "t_hi": N_BIT,
    }


def left23_period() -> dict:
    """Left 23 bits autonomous; t=26 equals t=30; even t>=26 period 4."""
    row = 1
    rows = []
    n_ok = 0
    w = 22
    for t in range(0, N_LEFT + 1):
        word = row & ((1 << (w + 1)) - 1)
        nxt = rule30_step(row)
        if t < N_LEFT:
            want = nxt & ((1 << (w + 1)) - 1)
            if left_step(word, w) != want:
                return {"ok": False, "auto": t, "got": left_step(word, w), "want": want}
        rows.append(word)
        row = nxt
        n_ok += 1
    if rows[26] != rows[30]:
        return {"ok": False, "seed": True, "t26": rows[26], "t30": rows[30]}
    b26 = tuple((rows[26] >> p) & 1 for p in range(19, 23))
    b28 = tuple((rows[28] >> p) & 1 for p in range(19, 23))
    if b26 != PAT1010 or b28 != PAT0111:
        return {"ok": False, "pats": True, "b26": b26, "b28": b28}
    if and_clause(*b26) != 0 or and_clause(*b28) != 0:
        return {"ok": False, "and": True}
    n_even = 0
    for t in range(26, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(19, 23))
        want = PAT1010 if t % 4 == 2 else PAT0111
        if b != want:
            return {"ok": False, "per": t, "got": b, "want": list(want)}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 24) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t26": rows[26], "t30": rows[30]}


def early_miss() -> dict:
    """k=2 covering AND-1 n=13,14 have G=0 at j=9; k=0,1 j<0."""
    if G(13, 9) != 0 or G(14, 9) != 0:
        return {"ok": False, "g": (G(13, 9), G(14, 9))}
    j0, j1 = 5 * 1 - 11, 5 * 2 - 11
    if j0 >= 0 or j1 >= 0:
        return {"ok": False, "j": (j0, j1)}
    return {"ok": True, "g13": 0, "g14": 0, "j0": j0, "j1": j1}


def thin_p22() -> dict:
    """k<=K_THIN: covering p=22 AND xor=0 and n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 22, (T - 22) // 2
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
        if xor_a != 0 or n_and != 0:
            return {"ok": False, "k": k, "xor_a": xor_a, "n_and": n_and}
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
        and rows["0"]["n_and"] == 0
        and rows["2"]["n_and"] == 0
        and rows["8"]["n_and"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pi = json.loads(PI_JSON.read_text())
    ph = json.loads(PH_JSON.read_text())
    ok = (
        pi["checks"]["all_ok"]
        and ph["checks"]["all_ok"]
        and pi["verdict"]["p18_silent_k_ge_2"] == "LEMMA"
        and pi["verdict"]["p20_silent_k_ge_4"] == "LEMMA"
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and pi["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pi["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, miss, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert miss["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b1922()
    per = left23_period()
    miss = early_miss()
    thin = thin_p22()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, miss, thin, sc, pref)
    dump = {
        "cycle": "PJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b1922": {k: fr[k] for k in fr if k != "ok"},
        "left23_period": {k: per[k] for k in per if k != "ok"},
        "early_miss": {k: miss[k] for k in miss if k != "ok"},
        "thin_p22": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit19_22_mod4": True,
            "and22_even_t_ge_26": True,
            "p22_silent_all_k": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p24_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit19_22_mod4": "LEMMA",
            "left23_period4": "LEMMA",
            "and22_even_t_ge_26": "LEMMA",
            "p22_silent_all_k": "LEMMA",
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
        "frozen_b1922 n_ok",
        dump["frozen_b1922"]["n_ok"],
        "n_even",
        dump["frozen_b1922"]["n_even"],
        "early22",
        dump["frozen_b1922"]["early22"],
    )
    print("left23_period n_even", dump["left23_period"]["n_even"])
    print("thin_p22 rows", {k: dump["thin_p22"]["rows"][k] for k in ("0", "2", "3", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
