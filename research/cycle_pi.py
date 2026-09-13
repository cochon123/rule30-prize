#!/usr/bin/env python3
"""Cycle PI: bits 17,18 freeze; covering p=18 silent for k>=2.

Bit 17 is 1 iff t%4==3 for t>=20; bit 18 is 1 iff t%4 in (1, 2)
for t>=20. The left 19 bits are autonomous; the word at t=20
equals t=24, so even t>=20 has p=18 4-tuple 1100 (t%4==0) or
0101 (t%4==2), never an AND-one. Even t with AND at p=18 are
only 8,12,14,18. Covering k>=4 starts at 2U>=32, so misses them.
k=3 has only s=18, even n, odd column, G=0. k=2 has G(13,11)=
G(15,11)=0. Hence covering p=18 is silent for k>=2. Even t>=24
has p=20 4-tuple 0001 or 0110, so covering p=20 is silent for
k>=4. Not rest=S xor T. Not E_k=0 for all k. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pi.py --certify
Dump: research/cycle_pi.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"
PG_JSON = Path(__file__).resolve().parent / "cycle_pg.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 48
K_THIN = 8
PAT1100 = (1, 1, 0, 0)
PAT0101 = (0, 1, 0, 1)
PAT0001 = (0, 0, 0, 1)
PAT0110 = (0, 1, 1, 0)
EARLY18 = {8, 12, 14, 18}


def want_b17(t: int) -> int:
    """Packed bit 17: 1 iff t%4==3 for t>=20."""
    if t < 20:
        return 0
    return int(t % 4 == 3)


def want_b18(t: int) -> int:
    """Packed bit 18: 1 iff t%4 in (1, 2) for t>=20."""
    if t < 20:
        return 0
    return int(t % 4 in (1, 2))


def want_and18_even(t: int) -> int:
    """Even t>=20: AND at p=18 is 0. Early fires: 8,12,14,18."""
    if t < 20 or t % 2:
        return int(t in EARLY18)
    return 0


def want_and20_even(t: int) -> int:
    """Even t>=24: AND at p=20 is 0."""
    if t < 24 or t % 2:
        return 0
    return 0


def frozen_b1718() -> dict:
    """t<=N_BIT: bits 17,18 for t>=20; even t>=20 p=18 is 1100 or 0101."""
    row = 1
    n_ok = 0
    n_even18 = 0
    n_even20 = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 21)]
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
            return {"ok": False, "ph": t, "got": b[13:17]}
        if t >= 20:
            if b[17] != want_b17(t) or b[18] != want_b18(t):
                return {"ok": False, "b1718": t, "got": (b[17], b[18])}
        if t % 2 == 0:
            four18 = tuple(b[15:19])
            a18 = and_clause(*four18)
            if t >= 20:
                want = PAT1100 if t % 4 == 0 else PAT0101
                if four18 != want or a18 != 0:
                    return {"ok": False, "p18": t, "four": four18}
                n_even18 += 1
            elif a18:
                early.append(t)
            if t >= 24:
                four20 = tuple(b[17:21])
                want20 = PAT0001 if t % 4 == 0 else PAT0110
                a20 = and_clause(*four20)
                if four20 != want20 or a20 != 0:
                    return {"ok": False, "p20": t, "four": four20}
                n_even20 += 1
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 19) - 1)
            if left_step(word, 18) != (nxt & ((1 << 19) - 1)):
                return {"ok": False, "auto19": t}
            word21 = row & ((1 << 21) - 1)
            if left_step(word21, 20) != (nxt & ((1 << 21) - 1)):
                return {"ok": False, "auto21": t}
        row = nxt
    if early != sorted(EARLY18):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even18 == (N_BIT - 18) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even18": n_even18,
        "n_even20": n_even20,
        "early18": early,
        "t_hi": N_BIT,
    }


def left19_period() -> dict:
    """Left 19 bits autonomous; t=20 equals t=24; even t>=20 period 4."""
    row = 1
    rows = []
    n_ok = 0
    w = 18
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
    if rows[20] != rows[24]:
        return {"ok": False, "seed": True, "t20": rows[20], "t24": rows[24]}
    b20 = tuple((rows[20] >> p) & 1 for p in range(15, 19))
    b22 = tuple((rows[22] >> p) & 1 for p in range(15, 19))
    if b20 != PAT1100 or b22 != PAT0101:
        return {"ok": False, "pats": True, "b20": b20, "b22": b22}
    if and_clause(*b20) != 0 or and_clause(*b22) != 0:
        return {"ok": False, "and": True}
    n_even = 0
    for t in range(20, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(15, 19))
        want = PAT1100 if t % 4 == 0 else PAT0101
        if b != want:
            return {"ok": False, "per": t, "got": b, "want": list(want)}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 18) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t20": rows[20], "t24": rows[24]}


def early_miss() -> dict:
    """k=2 covering AND-1 n=13,15 have G=0 at j=11; even n vanish."""
    if G(13, 11) != 0 or G(15, 11) != 0:
        return {"ok": False, "g": (G(13, 11), G(15, 11))}
    if G(10, 11) != 0 or G(12, 11) != 0:
        return {"ok": False, "even": True}
    if G(30, 31) != 0:
        return {"ok": False, "k3": True, "g": G(30, 31)}
    return {"ok": True, "g13": 0, "g15": 0, "g30": 0}


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
            return {"ok": False, "k": k, "n_and": n_and, "xor_a": xor_a}
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
    ph = json.loads(PH_JSON.read_text())
    pg = json.loads(PG_JSON.read_text())
    ok = (
        ph["checks"]["all_ok"]
        and pg["checks"]["all_ok"]
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and ph["verdict"]["p16_silent"] == "KILLED"
        and pg["verdict"]["p12_silent_k_ge_2"] == "LEMMA"
        and ph["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ph["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, per, miss, t18, t20, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and per["ok"]
    assert miss["ok"] and t18["ok"] and t20["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_b1718()
    per = left19_period()
    miss = early_miss()
    t18 = thin_p(18, 2)
    t20 = thin_p(20, 4)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, miss, t18, t20, sc, pref)
    dump = {
        "cycle": "PI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b1718": {k: fr[k] for k in fr if k != "ok"},
        "left19_period": {k: per[k] for k in per if k != "ok"},
        "early_miss": {k: miss[k] for k in miss if k != "ok"},
        "thin_p18": {k: t18[k] for k in t18 if k != "ok"},
        "thin_p20": {k: t20[k] for k in t20 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit17_18_mod4": True,
            "and18_even_t_ge_20": True,
            "p18_silent_k_ge_2": True,
            "p20_silent_k_ge_4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p18_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit17_18_mod4": "LEMMA",
            "left19_period4": "LEMMA",
            "and18_even_t_ge_20": "LEMMA",
            "p18_silent_k_ge_2": "LEMMA",
            "p20_silent_k_ge_4": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p18_silent_all_k": "KILLED",
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
        "frozen_b1718 n_ok",
        dump["frozen_b1718"]["n_ok"],
        "n_even18",
        dump["frozen_b1718"]["n_even18"],
        "early18",
        dump["frozen_b1718"]["early18"],
    )
    print("left19_period n_even", dump["left19_period"]["n_even"])
    print("thin_p18 rows", {k: dump["thin_p18"]["rows"][k] for k in ("0", "1", "2", "8")})
    print("thin_p20 rows", {k: dump["thin_p20"]["rows"][k] for k in ("2", "3", "4", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
