#!/usr/bin/env python3
"""Cycle QI: covering even-j and odd-j clipped G=1 xor via clip-edge p=0.

Cycle QH's covering clipped G=1 xor A(k) splits by j parity. Even n
have G(even, odd)=0, so even-n odd-j tot is 0, and even-n even-j
tot is A(k-1). Odd n=2m+1 telescopes even j=2l to G(m, 5U') on the
parent covering window, which is Green xor at packed p=0 (clip
edge j=5U'). Odd-n odd-j tot is A(k-1) xor that clip-edge xor.
Packed p=0 has even j, so tot equals parent p=2 at k-1 (Cycle QG
even-j doubling). Packed p=2 is Cycle PA's unique column
G(t, 5*2^k-1), which fires only at t=3U-1 on the covering live
window, xor 1 for every k. Hence clip-edge Green p=0 xor is 1 for
every k, even-j tot is 1 except k=1, and odd-j tot is 1 iff k>=2.
Not rest=S xor T (even-j is 1 for every k>=2). Not even-j tot
equals A. Not E_k=0 for all k. Do not walk leftover p catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_qi.py --certify
Dump: research/cycle_qi.json
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
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pa import unique_col
from cycle_pb import want_rest_e0
from cycle_pc import live_lo
from cycle_qg import even_m_range, gxor_p, odd_m_range, parent_p, parent_range
from cycle_qh import want_clip_g1, want_green_lo

OUT = Path(__file__).resolve().with_suffix(".json")
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
PA_JSON = Path(__file__).resolve().parent / "cycle_pa.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_WIN = 64
K_CHK = 8
K_ALG = 64


def want_p0_gxor(k: int) -> int:
    """Covering Green G=1 xor at packed p=0 (clip edge j=5U), all k."""
    return 1


def want_p2_gxor(k: int) -> int:
    """Covering Green G=1 xor at packed p=2, all k."""
    return 1


def want_even_j(k: int) -> int:
    """Covering clipped even-j G=1 xor, all k: 1 except k=1."""
    return int(k != 1)


def want_odd_j(k: int) -> int:
    """Covering clipped odd-j G=1 xor, all k: 1 iff k>=2."""
    return int(k >= 2)


def in_p2(n: int, k: int) -> bool:
    """G(n, 5*2^k-1)=1 on the covering live window, all k."""
    U = 1 << k
    if n < live_lo(k, 1) or n >= 4 * U:
        return False
    return n == 3 * U - 1


def clip_parity(n: int, k: int) -> tuple[int, int]:
    """Xor of G(n,j) on 0<=j<=min(2n, 5*2^k), split even/odd j."""
    clip = 5 << k
    even = odd = 0
    hi = min(2 * n, clip)
    for j in range(0, hi + 1):
        if G(n, j):
            if j % 2 == 0:
                even ^= 1
            else:
                odd ^= 1
    return even, odd


def split_A(k: int) -> dict:
    """Walk covering n=0..4U-1 clipped G=1 xor, split by n and j parity."""
    n_hi = 4 << k
    ee = eo = oe = oo = 0
    for n in range(0, n_hi):
        e, o = clip_parity(n, k)
        if n % 2 == 0:
            ee ^= e
            eo ^= o
        else:
            oe ^= e
            oo ^= o
    return {
        "ee": ee,
        "eo": eo,
        "oe": oe,
        "oo": oo,
        "even_j": ee ^ oe,
        "odd_j": eo ^ oo,
        "A": ee ^ eo ^ oe ^ oo,
        "n_hi": n_hi,
    }


def windows_ok() -> dict:
    """k>=1: p=0 even/odd m-windows match parents p=0 and p=2; p=2 odd matches p=2."""
    n_ok = 0
    for k in range(1, K_WIN + 1):
        if even_m_range(0, k) != parent_range(0, k - 1):
            return {"ok": False, "even0": True, "k": k}
        if odd_m_range(0, k) != parent_range(2, k - 1):
            return {"ok": False, "odd0": True, "k": k}
        if odd_m_range(2, k) != parent_range(2, k - 1):
            return {"ok": False, "odd2": True, "k": k}
        if parent_p(0) != 2 or parent_p(2) != 2:
            return {"ok": False, "parent": True, "k": k}
        n_ok += 1
    return {"ok": n_ok == K_WIN, "n_ok": n_ok, "k_hi": K_WIN}


def green_edge() -> dict:
    """k<=K_G: p=0 and p=2 Green xor are 1; p=2 ones are exactly 3U-1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        got0 = gxor_p(0, k)
        got2 = gxor_p(2, k)
        if got0 != want_p0_gxor(k) or got2 != want_p2_gxor(k):
            return {"ok": False, "xor": True, "k": k, "p0": got0, "p2": got2}
        U = 1 << k
        lo = live_lo(k, 1)
        ones = [n for n in range(lo, 4 * U) if in_p2(n, k)]
        walk = [
            n
            for n in range(lo, 4 * U)
            if 0 <= (5 * U - 1) <= 2 * n and G(n, 5 * U - 1)
        ]
        if ones != [3 * U - 1] or walk != ones:
            return {"ok": False, "set": True, "k": k, "ones": walk, "want": ones}
        if k >= 1 and (got0 != gxor_p(2, k - 1) or got2 != gxor_p(2, k - 1)):
            return {"ok": False, "rec": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"p0": got0, "p2": got2, "one": 3 * U - 1}
    ok = (
        rows["0"]["p0"] == 1
        and rows["0"]["one"] == 2
        and rows["1"]["one"] == 5
        and rows["8"]["one"] == 767
        and rows["12"]["p0"] == 1
        and rows["12"]["p2"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def j_parity() -> dict:
    """k<=K_CHK: even/odd j tot matches want_*; odd-n even-j is p=0 at k-1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = split_A(k)
        if w["A"] != want_clip_g1(k):
            return {"ok": False, "A": True, "k": k, "got": w["A"]}
        if w["even_j"] != want_even_j(k) or w["odd_j"] != want_odd_j(k):
            return {
                "ok": False,
                "form": True,
                "k": k,
                "even_j": w["even_j"],
                "odd_j": w["odd_j"],
            }
        if w["eo"] != 0:
            return {"ok": False, "eo": True, "k": k}
        if k >= 1:
            prev_a = want_clip_g1(k - 1)
            prev0 = want_p0_gxor(k - 1)
            if w["ee"] != prev_a:
                return {"ok": False, "ee": True, "k": k, "got": w["ee"]}
            if w["oe"] != prev0:
                return {"ok": False, "oe": True, "k": k, "got": w["oe"]}
            if w["oo"] != (prev_a ^ prev0):
                return {"ok": False, "oo": True, "k": k, "got": w["oo"]}
            n_ok += 1
        rows[str(k)] = {
            "A": w["A"],
            "even_j": w["even_j"],
            "odd_j": w["odd_j"],
            "ee": w["ee"],
            "eo": w["eo"],
            "oe": w["oe"],
            "oo": w["oo"],
        }
    ok = (
        rows["0"]["even_j"] == 1
        and rows["0"]["odd_j"] == 0
        and rows["1"]["even_j"] == 0
        and rows["1"]["odd_j"] == 0
        and rows["2"]["even_j"] == 1
        and rows["2"]["odd_j"] == 1
        and rows["8"]["even_j"] == 1
        and rows["8"]["A"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: closed forms vs A and p=0/p=2 doubling."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        a = want_clip_g1(k)
        ej = want_even_j(k)
        oj = want_odd_j(k)
        if (ej ^ oj) != a:
            return {"ok": False, "xorA": True, "k": k}
        if want_p0_gxor(k) != 1 or want_p2_gxor(k) != 1:
            return {"ok": False, "edge": True, "k": k}
        if k >= 1 and want_p0_gxor(k) != want_p2_gxor(k - 1):
            return {"ok": False, "rec": True, "k": k}
        if k >= 2:
            if ej != 1 or oj != 1 or a != 0:
                return {"ok": False, "ge2": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_even_j(0) == 1
        and want_even_j(1) == 0
        and want_odd_j(1) == 0
        and want_odd_j(2) == 1
        and want_green_lo(7) == 1
        and want_rest_e0(7) == 0
        and want_even_j(7) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_ej_eq_st() -> dict:
    """Even-j tot equals S xor T / A: k=7 is 1 vs 0; k=2 even-j=1 vs A=0."""
    ok = (
        want_even_j(7) == 1
        and want_rest_e0(7) == 0
        and want_even_j(2) == 1
        and want_clip_g1(2) == 0
        and want_even_j(0) != want_odd_j(0)
    )
    return {"ok": ok, "k": 7, "even_j": 1, "ST": 0, "A2": 0}


def prefixes() -> dict:
    qh = json.loads(QH_JSON.read_text())
    pa = json.loads(PA_JSON.read_text())
    uc = unique_col()
    ok = (
        qh["checks"]["all_ok"]
        and pa["checks"]["all_ok"]
        and uc["ok"]
        and qh["verdict"]["clip_g1_0_k_ge_1"] == "LEMMA"
        and qh["verdict"]["green_lo_iff_k_ge_6"] == "LEMMA"
        and qh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qh["verdict"]["prize"] == "unsolved"
        and pa["verdict"]["prize"] == "unsolved"
        and want_clip_g1(0) == 1
        and want_clip_g1(1) == 0
        and want_green_lo(6) == 1
    )
    return {"ok": ok, "unique_col": {k: uc[k] for k in uc if k != "ok"}}


def self_checks(c20, pal, slots, win, edge, par, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and win["ok"] and edge["ok"]
    assert par["ok"] and tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    win = windows_ok()
    edge = green_edge()
    par = j_parity()
    tot = tot_form()
    kl = killed_ej_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, win, edge, par, tot, kl, sc, pref)
    dump = {
        "cycle": "QI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "windows_ok": {k: win[k] for k in win if k != "ok"},
        "green_edge": {k: edge[k] for k in edge if k != "ok"},
        "j_parity": {k: par[k] for k in par if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "unique_col": pref["unique_col"],
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "p2_gxor_1_all_k": True,
            "p0_gxor_1_all_k": True,
            "even_j_except_k1": True,
            "odd_j_iff_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "ej_eq_ST": False,
            "ej_eq_A": False,
            "prize": False,
        },
        "verdict": {
            "p2_gxor_1_all_k": "LEMMA",
            "p0_gxor_1_all_k": "LEMMA",
            "even_j_except_k1": "LEMMA",
            "odd_j_iff_k_ge_2": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "ej_eq_ST": "KILLED",
            "ej_eq_A": "KILLED",
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
        "j_parity n_ok",
        dump["j_parity"]["n_ok"],
        "k_hi",
        dump["j_parity"]["k_hi"],
        "even_j8",
        dump["j_parity"]["rows"]["8"]["even_j"],
        "odd_j8",
        dump["j_parity"]["rows"]["8"]["odd_j"],
    )
    print("green_edge n_ok", dump["green_edge"]["n_ok"], "k_hi", dump["green_edge"]["k_hi"])
    print("windows n_ok", dump["windows_ok"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
