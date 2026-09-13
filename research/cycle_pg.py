#!/usr/bin/env python3
"""Cycle PG: bit 10 freeze; covering p=12 silent for k>=2.

Bit 10 is 1 iff t%4 in (0, 3) for t>=6. On even t>=8 the p=12
4-tuple is 1100 (t%4==0) or 1011 (t%4==2), never an AND-one, so
AND at p=12 is 0. Covering even s starts at 2U>=8 for k>=2, hence
covering p=12 is silent. Not rest=S xor T. Not E_k=0 for all k.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_pg.py --certify
Dump: research/cycle_pg.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PF_JSON = Path(__file__).resolve().parent / "cycle_pf.json"
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
K_THIN = 8
PAT1100 = (1, 1, 0, 0)
PAT1011 = (1, 0, 1, 1)
PAT0011 = (0, 0, 1, 1)
PAT1110 = (1, 1, 1, 0)


def want_b10(t: int) -> int:
    """Packed bit 10: 1 iff t%4 in (0, 3) for t>=6."""
    if t < 6:
        return int(t == 5)
    return int(t % 4 in (0, 3))


def want_and12_even(t: int) -> int:
    """Even t>=8: AND at p=12 is 0."""
    return 0


def frozen_b10() -> dict:
    """t<=N_BIT: bit 10; even t>=8 p=12 4-tuple is 1100 or 1011."""
    row = 1
    n_ok = 0
    n_even = 0
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 15)]
        if b[7] != want_b7(t) or b[8] != want_b8(t) or b[9] != want_b9(t):
            return {"ok": False, "pf": t}
        if b[10] != want_b10(t):
            return {"ok": False, "b10": t, "got": b[10], "w": want_b10(t)}
        if t >= 8 and t % 2 == 0:
            four = tuple(b[9:13])
            want = PAT1100 if t % 4 == 0 else PAT1011
            if four != want or and_clause(*four) != 0:
                return {"ok": False, "p12": t, "four": four, "want": list(want)}
            if t >= 12:
                b1114 = tuple(b[11:15])
                w1114 = PAT0011 if t % 4 == 0 else PAT1110
                if b1114 != w1114:
                    return {"ok": False, "p1114": t, "got": b1114}
            n_even += 1
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 15) - 1)
            if left_step(word, 14) != (nxt & ((1 << 15) - 1)):
                return {"ok": False, "auto": t}
        row = nxt
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 6) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t_hi": N_BIT}


def thin_p12() -> dict:
    """k<=K_THIN: covering p=12 AND xor=0; k>=2 n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 12, (T - 12) // 2
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
        if k >= 2 and t0 < 8:
            return {"ok": False, "t0": k, "t0v": t0}
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
        and rows["2"]["n_and"] == 0
        and rows["2"]["t0"] == 8
        and rows["8"]["n_and"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pf = json.loads(PF_JSON.read_text())
    pd = json.loads(PD_JSON.read_text())
    ok = (
        pf["checks"]["all_ok"]
        and pd["checks"]["all_ok"]
        and pf["verdict"]["bit7_zero"] == "LEMMA"
        and pf["verdict"]["p8_silent"] == "LEMMA"
        and pf["verdict"]["p10_silent_k_ge_2"] == "LEMMA"
        and pd["verdict"]["p14_period4"] == "LEMMA"
        and pf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pf["verdict"]["prize"] == "unsolved"
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
    fr = frozen_b10()
    thin = thin_p12()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, thin, sc, pref)
    dump = {
        "cycle": "PG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b10": {k: fr[k] for k in fr if k != "ok"},
        "thin_p12": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit10_mod4": True,
            "and12_even_t_ge_8": True,
            "p12_silent_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit10_mod4": "LEMMA",
            "and12_even_t_ge_8": "LEMMA",
            "p12_silent_k_ge_2": "LEMMA",
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
    print("frozen_b10 n_ok", dump["frozen_b10"]["n_ok"], "n_even", dump["frozen_b10"]["n_even"])
    print("thin_p12 rows", {k: dump["thin_p12"]["rows"][k] for k in ("0", "1", "2", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
