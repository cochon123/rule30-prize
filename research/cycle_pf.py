#!/usr/bin/env python3
"""Cycle PF: packed bits 7,8,9 freeze; covering p=8 and p=10 silent.

Bit 7 is 0 for every t. Bit 8 is 1 iff t%4 in (0, 1) for t>=4.
Bit 9 is 1 for every t>=5. Hence the p=8 4-tuple is never an
AND-one, so AND at p=8 is 0 for every t and covering p=8 is
silent for every k. For t>=5 the p=10 4-tuple is an AND-one iff
t%4 in (2, 3). Covering even s>=8 therefore has p=10 AND iff n
is even, but j=5U-5 is odd so even n have G=0. Covering p=10 is
silent for k>=2. Not rest=S xor T. Not E_k=0 for all k. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_pf.py --certify
Dump: research/cycle_pf.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PE_JSON = Path(__file__).resolve().parent / "cycle_pe.json"
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
K_THIN = 8
PAT0100 = (0, 1, 0, 0)


def want_b7(t: int) -> int:
    """Packed bit 7, all t."""
    return 0


def want_b8(t: int) -> int:
    """Packed bit 8: 1 iff t%4 in (0, 1) for t>=4."""
    if t < 4:
        return 0
    return int(t % 4 in (0, 1))


def want_b9(t: int) -> int:
    """Packed bit 9: 1 for t>=5."""
    return int(t >= 5)


def want_and8(t: int) -> int:
    """AND at p=8 is 0 for every t."""
    return 0


def want_and10(t: int) -> int:
    """AND at p=10 for t>=5: 1 iff t%4 in (2, 3). t=4 is 0100."""
    if t < 5:
        return int(t == 4)
    return int(t % 4 in (2, 3))


def frozen_789() -> dict:
    """t<=N_BIT: bits 7,8,9 and AND at p=8, p=10 match the freeze."""
    row = 1
    n_ok = 0
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 11)]
        if b[7] != want_b7(t):
            return {"ok": False, "b7": t, "got": b[7]}
        if b[8] != want_b8(t):
            return {"ok": False, "b8": t, "got": b[8], "w": want_b8(t)}
        if b[9] != want_b9(t):
            return {"ok": False, "b9": t, "got": b[9]}
        four8 = tuple(b[5:9])
        four10 = tuple(b[7:11])
        a8 = and_clause(*four8)
        a10 = and_clause(*four10)
        if a8 != want_and8(t):
            return {"ok": False, "a8": t, "got": a8, "four": four8}
        if t >= 4 and a10 != want_and10(t):
            return {"ok": False, "a10": t, "got": a10, "four": four10}
        if t == 4 and four10 != PAT0100:
            return {"ok": False, "t4": four10}
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 11) - 1)
            if left_step(word, 10) != (nxt & ((1 << 11) - 1)):
                return {"ok": False, "auto": t}
        row = nxt
    ok = n_ok == N_BIT + 1
    return {"ok": ok, "n_ok": n_ok, "t_hi": N_BIT}


def thin_silent() -> dict:
    """k<=K_THIN: covering p=8 AND xor=0; p=10 AND xor=0 for k>=1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        start = 1
        for _ in range(t0):
            start = rule30_step(start)
        rec = {}
        for p in (8, 10):
            j = (T - p) // 2
            xor_g = xor_a = n_g = n_and = n_sil = 0
            s = t0
            prev = None
            pos = start
            while s < T:
                if s % 2 == 0:
                    prev = pos
                else:
                    t = (s - t0) // 2
                    n = odd_clock(t, U, Q)
                    if 0 <= j <= 2 * n:
                        four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                        packed = and_clause(*four)
                        if G(n, j) == 1:
                            n_g += 1
                            xor_g ^= 1
                            if packed:
                                xor_a ^= 1
                                n_and += 1
                            else:
                                n_sil += 1
                pos = rule30_step(pos)
                s += 1
            rec[p] = {
                "xor_g": xor_g,
                "xor_a": xor_a,
                "n_g": n_g,
                "n_and": n_and,
                "n_sil": n_sil,
                "j": j,
            }
        if rec[8]["xor_a"] != 0 or rec[8]["n_and"] != 0:
            return {"ok": False, "p8": k, "row": rec[8]}
        if k >= 1 and (rec[10]["xor_a"] != 0 or rec[10]["n_and"] != 0):
            return {"ok": False, "p10": k, "row": rec[10]}
        if k == 0 and rec[10]["n_and"] == 0:
            return {"ok": False, "p10k0": rec[10]}
        rows[str(k)] = rec
        n_ok += 1
    ok = (
        n_ok == K_THIN + 1
        and rows["0"][8]["n_and"] == 0
        and rows["2"][10]["n_and"] == 0
        and rows["8"][8]["n_and"] == 0
    )
    out_rows = {k: {str(p): rows[k][p] for p in rows[k]} for k in rows}
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": out_rows}


def prefixes() -> dict:
    pe = json.loads(PE_JSON.read_text())
    pd = json.loads(PD_JSON.read_text())
    ok = (
        pe["checks"]["all_ok"]
        and pd["checks"]["all_ok"]
        and pe["verdict"]["edge_e0_e5"] == "LEMMA"
        and pe["verdict"]["dual_p4_and"] == "LEMMA"
        and pd["verdict"]["packed_forced_all_k"] == "LEMMA"
        and pe["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pe["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, thin, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and thin["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    fr = frozen_789()
    thin = thin_silent()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, thin, sc, pref)
    dump = {
        "cycle": "PF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_789": {k: fr[k] for k in fr if k != "ok"},
        "thin_silent": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit7_zero": True,
            "bit8_mod4": True,
            "bit9_ones": True,
            "and8_zero": True,
            "p8_silent": True,
            "p10_silent_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit7_zero": "LEMMA",
            "bit8_mod4": "LEMMA",
            "bit9_ones": "LEMMA",
            "and8_zero": "LEMMA",
            "p8_silent": "LEMMA",
            "p10_silent_k_ge_2": "LEMMA",
            "E_q10_10": "CERTIFIED",
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
    print("frozen_789 n_ok", dump["frozen_789"]["n_ok"])
    print("thin_silent k_hi", dump["thin_silent"]["k_hi"])
    print("thin rows", {k: dump["thin_silent"]["rows"][k] for k in ("0", "1", "2", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
