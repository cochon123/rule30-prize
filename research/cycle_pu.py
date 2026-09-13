#!/usr/bin/env python3
"""Cycle PU: covering packed AND xor at p=40 is 1 iff k in (2, 4).

Bits 39,40 freeze from t>=56: bit 39 is 1 iff t%8 in (6, 7); bit
40 is 1 iff t%8 in (2, 4). Bits 37,38 already freeze from t>=48
(Cycle PN). The left 41 bits are autonomous; the word at t=56
equals t=64, so even t>=56 has p=40 4-tuple 0000 / 1101 / 1101 /
0110 on t%8 = 0,2,4,6, never an AND-one. Early even AND-ones are
28,32,38,42,44,48. Covering k>=5 starts at 2U>=64>48, so p=40 is
silent for k>=5. Packed xor is 1 iff k in (2, 4). At k=2 this
leftover column is the remaining rest bit after classified unique
and leftover. Leftover, not UNIQUE_REST. Not rest=S xor T. Not
E_k=0 for all k. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pu.py --certify
Dump: research/cycle_pu.json
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
from cycle_pn import want_b35, want_b36, want_b37, want_b38
from cycle_pt import want_p70_pack
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PT_JSON = Path(__file__).resolve().parent / "cycle_pt.json"
PN_JSON = Path(__file__).resolve().parent / "cycle_pn.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 80
N_LEFT = 80
K_THIN = 8
PAT0000 = (0, 0, 0, 0)
PAT1101 = (1, 1, 0, 1)
PAT0110 = (0, 1, 1, 0)
EARLY40 = {28, 32, 38, 42, 44, 48}


def want_b39(t: int) -> int:
    """Packed bit 39: 1 iff t%8 in (6, 7) for t>=56."""
    if t < 56:
        return 0
    return int(t % 8 in (6, 7))


def want_b40(t: int) -> int:
    """Packed bit 40: 1 iff t%8 in (2, 4) for t>=56."""
    if t < 56:
        return 0
    return int(t % 8 in (2, 4))


def want_and40_even(t: int) -> int:
    """Even t>=56: AND at p=40 is 0. Early even AND-ones listed."""
    if t < 56 or t % 2:
        return int(t in EARLY40)
    return 0


def even40_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=56 p=40 4-tuple."""
    r = t % 8
    if r == 0:
        return PAT0000
    if r == 6:
        return PAT0110
    return PAT1101


def want_p40_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=40, all k."""
    return int(k in (2, 4))


def frozen_b3940() -> dict:
    """t<=N_BIT: bits 39,40 for t>=56; even t>=56 never AND."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 41)]
        if t >= 48 and (
            b[35] != want_b35(t)
            or b[36] != want_b36(t)
            or b[37] != want_b37(t)
            or b[38] != want_b38(t)
        ):
            return {"ok": False, "pn": t}
        if t >= 56:
            got = (b[39], b[40])
            want = (want_b39(t), want_b40(t))
            if got != want:
                return {"ok": False, "b3940": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[37:41])
            a = and_clause(*four)
            if t >= 56:
                wp = even40_pat(t)
                if four != wp or a != 0:
                    return {"ok": False, "p40": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 41) - 1)
            if left_step(word, 40) != (nxt & ((1 << 41) - 1)):
                return {"ok": False, "auto41": t}
        row = nxt
    if early != sorted(EARLY40):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 54) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early40": early,
        "t_hi": N_BIT,
    }


def left41_period() -> dict:
    """Left 41 bits autonomous; t=56 equals t=64; even t>=56 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 40
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
    if rows[56] != rows[64]:
        return {"ok": False, "seed": True, "t56": rows[56], "t64": rows[64]}
    n_even = 0
    for t in range(56, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(37, 41))
        if b != even40_pat(t) or and_clause(*b) != 0:
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 54) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t56": rows[56], "t64": rows[64]}


def thin_p40() -> dict:
    """k<=K_THIN: covering p=40 xor = want_p40_pack; k>=5 n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 40, (T - 40) // 2
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
                    if G(n, j) == 1:
                        n_g += 1
                        if packed:
                            xor_a ^= 1
                            n_and += 1
                        else:
                            n_sil += 1
                    if k >= 5:
                        s_even = s - 1
                        if packed != want_and40_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
            row = rule30_step(row)
            s += 1
        want = want_p40_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 5 and (n_and != 0 or t0 < 56):
            return {"ok": False, "sil": True, "k": k, "n_and": n_and}
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
        and rows["2"]["xor_a"] == 1
        and rows["3"]["xor_a"] == 0
        and rows["4"]["xor_a"] == 1
        and rows["5"]["n_and"] == 0
        and rows["8"]["n_and"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pt = json.loads(PT_JSON.read_text())
    pn = json.loads(PN_JSON.read_text())
    ok = (
        pt["checks"]["all_ok"]
        and pn["checks"]["all_ok"]
        and pt["verdict"]["p70_xor_k_ge_6"] == "LEMMA"
        and pn["verdict"]["p38_xor_iff_k23"] == "LEMMA"
        and pt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pt["verdict"]["prize"] == "unsolved"
        and want_p40_pack(2) == 1
        and want_p40_pack(3) == 0
        and want_p40_pack(4) == 1
        and want_p40_pack(5) == 0
        and want_p70_pack(6) == 1
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
    fr = frozen_b3940()
    per = left41_period()
    thin = thin_p40()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, thin, sc, pref)
    dump = {
        "cycle": "PU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b3940": {k: fr[k] for k in fr if k != "ok"},
        "left41_period": {k: per[k] for k in per if k != "ok"},
        "thin_p40": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit39_40_mod8": True,
            "and40_even_t_ge_56": True,
            "p40_silent_k_ge_5": True,
            "p40_xor_iff_k24": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p40_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit39_40_mod8": "LEMMA",
            "left41_period8": "LEMMA",
            "and40_even_t_ge_56": "LEMMA",
            "p40_silent_k_ge_5": "LEMMA",
            "p40_xor_iff_k24": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p40_silent_all_k": "KILLED",
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
        "frozen_b3940 n_ok",
        dump["frozen_b3940"]["n_ok"],
        "n_even",
        dump["frozen_b3940"]["n_even"],
        "early40",
        dump["frozen_b3940"]["early40"],
    )
    print(
        "thin_p40 rows",
        {k: dump["thin_p40"]["rows"][k] for k in ("2", "3", "4", "5", "8")},
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
