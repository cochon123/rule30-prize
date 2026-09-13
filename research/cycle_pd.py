#!/usr/bin/env python3
"""Cycle PD: covering packed forced xor is 1 for every k on q=10.

Rule 30 on packed bits: bit 0 stays 1; bit 1 is 1 for t>=1; bit 2 is
0 for t>=2. Then bit 3 alternates (0 on even t>=2), bit 4 stays 1,
and bits 5,6 equal t%2 for t>=3. Hence every even t>=2 has bits
1..6 equal to 100100, so the p=4 4-tuple is 1001 and the p=6
4-tuple is 0100. The left 15 bits are autonomous; the word at t=12
equals the word at t=16, so even t>=12 has bits 11..14 equal to
0011 iff t%4==0 else 1110. Covering even s starts at 2U>=16 for
k>=3, so p=14 AND fires iff n is odd. Even n have G=0 at the odd
column 5U-7, and Cycle PC's Green xor at p=14 is 1, so packed AND
xor equals Green xor. With p=4 and p=6 always AND on live n,
packed forced xor is 1 for k>=3, and k=0,1,2 are finite. Rest is
1 xor J_odd. Not rest=S xor T. Not E_k=0 for all k. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pd.py --certify
Dump: research/cycle_pd.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import want_green_forced, want_p14_gxor, want_p4_xor, want_p6_gxor
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"
PB_JSON = Path(__file__).resolve().parent / "cycle_pb.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
N_LEFT = 48
K_THIN = 8
PAT1001 = (1, 0, 0, 1)
PAT0100 = (0, 1, 0, 0)
PAT0011 = (0, 0, 1, 1)
PAT1110 = (1, 1, 1, 0)


def want_forced(k: int) -> int:
    """Covering q=10 packed forced xor, all k."""
    return 1


def want_jodd_e0(k: int) -> int:
    """J_odd if E_k=0: 1 xor S xor T."""
    return 1 ^ want_rest_e0(k)


def low_bits(t: int, row: int, p: int) -> int:
    if p < 0 or p > 2 * t:
        return 0
    return (row >> p) & 1


def left_step(word: int, w: int) -> int:
    """Autonomous step of packed bits 0..w. Negative bits are 0."""
    out = 0
    for p in range(0, w + 1):
        lo = (word >> (p - 2)) & 1 if p >= 2 else 0
        mid = (word >> (p - 1)) & 1 if p >= 1 else 0
        hi = (word >> p) & 1
        if lo ^ (mid | hi):
            out |= 1 << p
    return out


def frozen_low() -> dict:
    """t<=N_BIT: bits 1..6 match the freeze; even t>=2 is 100100."""
    row = 1
    n_ok = 0
    for t in range(0, N_BIT + 1):
        b = [low_bits(t, row, p) for p in range(0, 7)]
        if b[0] != 1:
            return {"ok": False, "b0": t}
        if t >= 1 and b[1] != 1:
            return {"ok": False, "b1": t}
        if t >= 2 and b[2] != 0:
            return {"ok": False, "b2": t}
        if t >= 2 and b[3] != (t % 2):
            return {"ok": False, "b3": t, "got": b[3]}
        if t >= 2 and b[4] != 1:
            return {"ok": False, "b4": t}
        if t >= 3 and (b[5] != (t % 2) or b[6] != (t % 2)):
            return {"ok": False, "b56": t, "got": (b[5], b[6])}
        if t >= 2 and t % 2 == 0:
            four4 = (b[1], b[2], b[3], b[4])
            four6 = (b[3], b[4], b[5], b[6])
            if four4 != PAT1001 or and_clause(*four4) != 1:
                return {"ok": False, "p4": t, "four": four4}
            if t >= 4 and (four6 != PAT0100 or and_clause(*four6) != 1):
                return {"ok": False, "p6": t, "four": four6}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == N_BIT + 1
    return {"ok": ok, "n_ok": n_ok, "t_hi": N_BIT}


def left15_period() -> dict:
    """Left 15 bits autonomous; t=12 equals t=16; even t>=12 period 4."""
    row = 1
    rows = []
    n_ok = 0
    w = 14
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
    if rows[12] != rows[16]:
        return {"ok": False, "seed": True, "t12": rows[12], "t16": rows[16]}
    b12 = tuple((rows[12] >> p) & 1 for p in range(11, 15))
    b14 = tuple((rows[14] >> p) & 1 for p in range(11, 15))
    if b12 != PAT0011 or b14 != PAT1110:
        return {"ok": False, "pats": True, "b12": b12, "b14": b14}
    if and_clause(*b12) != 1 or and_clause(*b14) != 0:
        return {"ok": False, "and": True}
    n_even = 0
    for t in range(12, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(11, 15))
        want = PAT0011 if t % 4 == 0 else PAT1110
        if b != want:
            return {"ok": False, "per": t, "got": b, "want": list(want)}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even >= 18
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "t12": rows[12],
        "t14": rows[14],
        "t16": rows[16],
    }


def thin_forced() -> dict:
    """k<=K_THIN: packed forced xor=1; k>=3 p=14 AND iff n odd."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_f = xor4 = xor6 = xor14 = 0
        n_sil14 = n_odd_and = n_even_and = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                t = (s - t0) // 2
                n = odd_clock(t, U, Q)
                for p in FORCED:
                    if (T - p) % 2:
                        continue
                    j = (T - p) // 2
                    if not (0 <= j <= 2 * n):
                        continue
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    g1 = G(n, j) == 1
                    if p == 4 and four != PAT1001:
                        return {"ok": False, "p4": True, "k": k, "four": four}
                    if p == 6 and four != PAT0100:
                        return {"ok": False, "p6": True, "k": k, "four": four}
                    if k >= 3 and p == 14:
                        want = PAT0011 if n % 2 == 1 else PAT1110
                        if four != want:
                            return {
                                "ok": False,
                                "p14": True,
                                "k": k,
                                "n": n,
                                "four": four,
                            }
                        if n % 2 == 1:
                            n_odd_and += packed
                        else:
                            n_even_and += packed
                    if g1 and packed:
                        xor_f ^= 1
                        if p == 4:
                            xor4 ^= 1
                        elif p == 6:
                            xor6 ^= 1
                        else:
                            xor14 ^= 1
                    if g1 and not packed and p == 14:
                        n_sil14 += 1
            row = rule30_step(row)
            s += 1
        if xor_f != 1:
            return {"ok": False, "xor": k, "got": xor_f}
        if xor4 != want_p4_xor(k) or xor6 != want_p6_gxor(k):
            return {"ok": False, "pc46": k, "x4": xor4, "x6": xor6}
        if k >= 3:
            if n_sil14 != 0 or n_even_and != 0 or xor14 != want_p14_gxor(k):
                return {
                    "ok": False,
                    "p14xor": k,
                    "sil": n_sil14,
                    "even_and": n_even_and,
                    "x14": xor14,
                }
            if xor_f != want_green_forced(k):
                return {"ok": False, "green": k}
        if k <= 2 and n_sil14 == 0 and k != 0:
            return {"ok": False, "expect_sil": k}
        rows[str(k)] = {
            "f": xor_f,
            "x4": xor4,
            "x6": xor6,
            "x14": xor14,
            "sil14": n_sil14,
        }
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["f"] == 1
        and rows["1"]["sil14"] >= 1
        and rows["3"]["sil14"] == 0
        and rows["8"]["f"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def rest_jodd() -> dict:
    """k<=24: rest = 1 xor J_odd if forced=1; E=0 iff J_odd=1 xor ST."""
    n_ok = 0
    rows = {}
    og = json.loads(OG_JSON.read_text())
    for k in range(0, 25):
        rest = want_rest_e0(k)
        jodd = want_jodd_e0(k)
        if (1 ^ rest) != jodd:
            return {"ok": False, "k": k, "rest": rest, "jodd": jodd}
        if k <= 10:
            row = og["q10_E_10"]["rows"][str(k)]
            packed_f = row["xor_j_odd"] ^ row["xor_r"]
            if packed_f != 1 or row["xor_r"] != rest:
                return {"ok": False, "og": k, "f": packed_f, "r": row["xor_r"]}
            if row["xor_j_odd"] != jodd:
                return {"ok": False, "j": k, "got": row["xor_j_odd"], "want": jodd}
        if k <= 12:
            rows[str(k)] = {"rest": rest, "jodd": jodd}
        n_ok += 1
    ok = (
        n_ok == 25
        and rows["2"]["jodd"] == 0
        and rows["6"]["jodd"] == 0
        and rows["0"]["jodd"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": 24, "rows": rows}


def killed_p14_const() -> dict:
    """Even t>=12 bits 11..14 are not constant: t=12 is 0011, t=14 is 1110."""
    row = 1
    got = {}
    for t in range(0, 15):
        if t in (12, 14):
            got[t] = tuple((row >> p) & 1 for p in range(11, 15))
        row = rule30_step(row)
    ok = got[12] == PAT0011 and got[14] == PAT1110
    return {"ok": ok, "t12": list(got[12]), "t14": list(got[14])}


def prefixes() -> dict:
    pc = json.loads(PC_JSON.read_text())
    pb = json.loads(PB_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        pc["checks"]["all_ok"]
        and pb["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and pc["verdict"]["p4_set"] == "LEMMA"
        and pc["verdict"]["green_forced_xor"] == "LEMMA"
        and pb["verdict"]["ST_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and pc["verdict"]["packed_forced_all_k"] == "PREFIX"
        and pc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, low, left, thin, rest, k14, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and low["ok"]
        and left["ok"]
        and thin["ok"]
        and rest["ok"]
        and k14["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    low = frozen_low()
    left = left15_period()
    thin = thin_forced()
    rest = rest_jodd()
    k14 = killed_p14_const()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, low, left, thin, rest, k14, sc, pref)
    dump = {
        "cycle": "PD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_low": {k: low[k] for k in low if k != "ok"},
        "left15_period": {k: left[k] for k in left if k != "ok"},
        "thin_forced": {k: thin[k] for k in thin if k != "ok"},
        "rest_jodd": {k: rest[k] for k in rest if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_p14_const": {k: k14[k] for k in k14 if k != "ok"},
        "lemmas": {
            "frozen_low": True,
            "p14_period4": True,
            "packed_forced_all_k": True,
            "rest_eq_1_xor_jodd": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "frozen_low": "LEMMA",
            "p14_period4": "LEMMA",
            "packed_forced_all_k": "LEMMA",
            "rest_eq_1_xor_jodd": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "p14_four_const": "KILLED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("frozen_low n_ok", dump["frozen_low"]["n_ok"])
    print("left15_period n_even", dump["left15_period"]["n_even"])
    print("thin_forced", dump["thin_forced"]["rows"])
    print("killed_p14_const", dump["killed_p14_const"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
