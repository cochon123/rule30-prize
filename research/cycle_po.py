#!/usr/bin/env python3
"""Cycle PO: covering packed AND xor at p=64 is 1 iff k in (3, 5).

Bits 61..64 freeze from t>=92: bit 61 is 1 iff t%8 in (2, 3, 7);
bit 62 is 1 iff t%8 in (2, 3, 6); bit 63 is 1 iff t%8==7; bit 64
is 1 iff t%8 not in (3, 7). The left 65 bits are autonomous; the
word at t=92 equals t=100, so even t>=92 has p=64 4-tuple 0001 /
1101 / 0001 / 0101 on t%8 = 0,2,4,6, never an AND-one. Early even
AND-ones are 38,40,42,48,54,58,60,68,70,72,88. Covering k>=6
starts at 2U>=128>88, so p=64 is silent for k>=6. Packed xor is 1
iff k in (3, 5). Not rest=S xor T. Not E_k=0 for all k. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_po.py --certify
Dump: research/cycle_po.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PN_JSON = Path(__file__).resolve().parent / "cycle_pn.json"
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 128
N_LEFT = 128
K_THIN = 8
PAT0001 = (0, 0, 0, 1)
PAT1101 = (1, 1, 0, 1)
PAT0101 = (0, 1, 0, 1)
EARLY64 = {38, 40, 42, 48, 54, 58, 60, 68, 70, 72, 88}


def want_b61(t: int) -> int:
    """Packed bit 61: 1 iff t%8 in (2, 3, 7) for t>=92."""
    if t < 92:
        return 0
    return int(t % 8 in (2, 3, 7))


def want_b62(t: int) -> int:
    """Packed bit 62: 1 iff t%8 in (2, 3, 6) for t>=92."""
    if t < 92:
        return 0
    return int(t % 8 in (2, 3, 6))


def want_b63(t: int) -> int:
    """Packed bit 63: 1 iff t%8==7 for t>=92."""
    if t < 92:
        return 0
    return int(t % 8 == 7)


def want_b64(t: int) -> int:
    """Packed bit 64: 1 iff t%8 not in (3, 7) for t>=92."""
    if t < 92:
        return 0
    return int(t % 8 not in (3, 7))


def want_and64_even(t: int) -> int:
    """Even t>=92: AND at p=64 is 0. Early even AND-ones listed."""
    if t < 92 or t % 2:
        return int(t in EARLY64)
    return 0


def even64_pat(t: int) -> tuple[int, int, int, int]:
    """Even t>=92 p=64 4-tuple."""
    r = t % 8
    if r == 2:
        return PAT1101
    if r == 6:
        return PAT0101
    return PAT0001


def want_p64_pack(k: int) -> int:
    """Covering q=10 packed AND xor at p=64, all k."""
    return int(k in (3, 5))


def frozen_b6164() -> dict:
    """t<=N_BIT: bits 61..64 for t>=92; even t>=92 never AND."""
    row = 1
    n_ok = 0
    n_even = 0
    early = []
    for t in range(0, N_BIT + 1):
        b = [(row >> p) & 1 for p in range(0, 65)]
        if t >= 48 and (
            b[35] != want_b35(t)
            or b[36] != want_b36(t)
            or b[37] != want_b37(t)
            or b[38] != want_b38(t)
        ):
            return {"ok": False, "pn": t}
        if t >= 92:
            got = (b[61], b[62], b[63], b[64])
            want = (want_b61(t), want_b62(t), want_b63(t), want_b64(t))
            if got != want:
                return {"ok": False, "b6164": t, "got": got, "want": want}
        if t % 2 == 0:
            four = tuple(b[61:65])
            a = and_clause(*four)
            if t >= 92:
                wp = even64_pat(t)
                if four != wp or a != 0:
                    return {"ok": False, "p64": t, "four": four}
                n_even += 1
            elif a:
                early.append(t)
        n_ok += 1
        nxt = rule30_step(row)
        if t < N_BIT:
            word = row & ((1 << 65) - 1)
            if left_step(word, 64) != (nxt & ((1 << 65) - 1)):
                return {"ok": False, "auto65": t}
        row = nxt
    if early != sorted(EARLY64):
        return {"ok": False, "early": early}
    ok = n_ok == N_BIT + 1 and n_even == (N_BIT - 90) // 2
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_even": n_even,
        "early64": early,
        "t_hi": N_BIT,
    }


def left65_period() -> dict:
    """Left 65 bits autonomous; t=92 equals t=100; even t>=92 period 8."""
    row = 1
    rows = []
    n_ok = 0
    w = 64
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
    if rows[92] != rows[100]:
        return {"ok": False, "seed": True, "t92": rows[92], "t100": rows[100]}
    n_even = 0
    for t in range(92, N_LEFT + 1, 2):
        b = tuple((rows[t] >> p) & 1 for p in range(61, 65))
        if b != even64_pat(t) or and_clause(*b) != 0:
            return {"ok": False, "per": t, "got": b}
        n_even += 1
    ok = n_ok == N_LEFT + 1 and n_even == (N_LEFT - 90) // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t92": rows[92], "t100": rows[100]}


def thin_p64() -> dict:
    """k<=K_THIN: covering p=64 xor = want_p64_pack; k>=6 n_and=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        p, j = 64, (T - 64) // 2
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
                    if k >= 6:
                        s_even = s - 1
                        if packed != want_and64_even(s_even):
                            return {"ok": False, "and": True, "k": k, "s": s_even}
            row = rule30_step(row)
            s += 1
        want = want_p64_pack(k)
        if xor_a != want:
            return {"ok": False, "xor": True, "k": k, "xor_a": xor_a, "want": want}
        if k >= 6 and (n_and != 0 or t0 < 92):
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
        and rows["2"]["xor_a"] == 0
        and rows["3"]["xor_a"] == 1
        and rows["4"]["xor_a"] == 0
        and rows["5"]["xor_a"] == 1
        and rows["6"]["n_and"] == 0
        and rows["8"]["n_and"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def prefixes() -> dict:
    pn = json.loads(PN_JSON.read_text())
    pm = json.loads(PM_JSON.read_text())
    ok = (
        pn["checks"]["all_ok"]
        and pm["checks"]["all_ok"]
        and pn["verdict"]["p38_xor_iff_k23"] == "LEMMA"
        and pm["verdict"]["p30_xor_iff_k2"] == "LEMMA"
        and pn["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pn["verdict"]["prize"] == "unsolved"
        and want_p64_pack(3) == 1
        and want_p64_pack(5) == 1
        and want_p64_pack(6) == 0
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
    fr = frozen_b6164()
    per = left65_period()
    thin = thin_p64()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, per, thin, sc, pref)
    dump = {
        "cycle": "PO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_b6164": {k: fr[k] for k in fr if k != "ok"},
        "left65_period": {k: per[k] for k in per if k != "ok"},
        "thin_p64": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "bit61_64_mod8": True,
            "and64_even_t_ge_92": True,
            "p64_silent_k_ge_6": True,
            "p64_xor_iff_k35": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "p64_silent_all_k": False,
            "prize": False,
        },
        "verdict": {
            "bit61_64_mod8": "LEMMA",
            "left65_period8": "LEMMA",
            "and64_even_t_ge_92": "LEMMA",
            "p64_silent_k_ge_6": "LEMMA",
            "p64_xor_iff_k35": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "p64_silent_all_k": "KILLED",
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
        "frozen_b6164 n_ok",
        dump["frozen_b6164"]["n_ok"],
        "n_even",
        dump["frozen_b6164"]["n_even"],
        "early64",
        dump["frozen_b6164"]["early64"],
    )
    print("thin_p64 rows", {k: dump["thin_p64"]["rows"][k] for k in ("2", "3", "5", "6", "8")})
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
