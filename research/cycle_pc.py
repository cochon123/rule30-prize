#!/usr/bin/env python3
"""Cycle PC: Green G=1 sets on covering forced columns p=4,6,14.

On covering q=10, the live n with G(n, 5*2^k-2)=1 (p=4) are
{4U-1} union {3U-1-2^i : i=0..k-1} union {3U-1} iff k odd, for
k>=1 (k=0: {3}). Even n is the unique 3U-2 from Cycle PA's column
G(t, 5*2^{k-1}-1). Odd n doubles the parent p=4 set xor {3U-1}.
p=6 is odd-only: G(2p+1, 5U-3)=G(p, 5*2^{k-1}-2), so the set is
{2s+1 : s in p=4 at k-1}. p=14 for k>=3 is {4U-3, 3U-1} union
{3U-3-2^i : i=1..k-1} union {3U-3} iff k odd. Counts match Cycle
LC/LD/LF want_* on q=10 as Green G=1 counts, not packed AND.
Green xor is 1 at p=4 for all k; p=6 iff k>=1; p=14 iff k>=3.
Green tot=0 at k=1,2 while packed forced xor is 1, so Green G=1
xor is not packed forced. Not rest=S xor T. Not E_k=0 for all k.
Not silent-free / slot forms for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pc.py --certify
Dump: research/cycle_pc.json
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
from cycle_lc import want_p4_n
from cycle_ld import want_p6_n, want_p6_xor
from cycle_lf import want_p14_n, want_p14_xor
from cycle_oj import doubling_slots, green_center_corner_pal

OUT = Path(__file__).resolve().with_suffix(".json")
PA_JSON = Path(__file__).resolve().parent / "cycle_pa.json"
PB_JSON = Path(__file__).resolve().parent / "cycle_pb.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
A_EDGE = 8
K_SET = 12
K_FORM = 24


def is_pow2(d: int) -> bool:
    return d > 0 and (d & (d - 1)) == 0


def live_lo(k: int, delta: int) -> int:
    """Smallest n with 2n >= 5*2^k - delta."""
    j = (5 << k) - delta
    if j < 0:
        return 0
    return (j + 1) // 2


def in_p4(n: int, k: int) -> bool:
    """G(n, 5*2^k-2)=1 on the covering live window, k>=0."""
    U = 1 << k
    if n < live_lo(k, 2) or n >= 4 * U:
        return False
    if k == 0:
        return n == 3
    if n == 4 * U - 1:
        return True
    if n == 3 * U - 1:
        return k % 2 == 1
    return is_pow2((3 * U - 1) - n) and ((3 * U - 1) - n) <= (1 << (k - 1))


def in_p6(n: int, k: int) -> bool:
    """G(n, 5*2^k-3)=1 on the covering live window, k>=0."""
    U = 1 << k
    if n < live_lo(k, 3) or n >= 4 * U:
        return False
    if k == 0:
        return n in (1, 2)
    if n % 2 == 0:
        return False
    if n == 4 * U - 1:
        return True
    if n == 3 * U - 1:
        return k % 2 == 0
    d = (3 * U - 1) - n
    return is_pow2(d) and 2 <= d <= (1 << (k - 1))


def in_p14(n: int, k: int) -> bool:
    """G(n, 5*2^k-7)=1 on the covering live window, k>=3."""
    U = 1 << k
    if k < 3 or n < live_lo(k, 7) or n >= 4 * U:
        return False
    if n % 2 == 0:
        return False
    if n in (4 * U - 3, 3 * U - 1):
        return True
    if n == 3 * U - 3:
        return k % 2 == 1
    d = (3 * U - 3) - n
    return is_pow2(d) and 2 <= d <= (1 << (k - 1))


def p4_count(k: int) -> int:
    return 1 if k == 0 else k + 1 + (k % 2)


def p6_count(k: int) -> int:
    return 2 if k == 0 else k + 1 - (k % 2)


def p14_count(k: int) -> int:
    """Green G=1 count at p=14. Differs from packed AND at k=1,2."""
    if k >= 3:
        return k + 1 + (k % 2)
    if k == 0:
        return 0
    return 2 * k


def want_p4_xor(k: int) -> int:
    """p=4 Green G=1 xor, all k."""
    return 1


def want_p6_gxor(k: int) -> int:
    """p=6 Green G=1 xor, all k."""
    return 0 if k == 0 else 1


def want_p14_gxor(k: int) -> int:
    """p=14 Green G=1 xor, all k."""
    return int(k >= 3)


def want_green_forced(k: int) -> int:
    """Xor of the three Green G=1 columns."""
    return want_p4_xor(k) ^ want_p6_gxor(k) ^ want_p14_gxor(k)


def ones_at(k: int, delta: int) -> list[int]:
    U = 1 << k
    j = (5 << k) - delta
    lo = live_lo(k, delta)
    return [n for n in range(lo, 4 * U) if 0 <= j <= 2 * n and G(n, j)]


def edge_unique() -> dict:
    """G(5*2^{a-1}-1, 5*2^a-1)=0; unique col still only t=3*2^a-1."""
    n_ok = 0
    sample = {}
    for a in range(1, A_EDGE + 1):
        edge = (5 << (a - 1)) - 1
        c5 = (5 << a) - 1
        if G(edge, c5) != 0:
            return {"ok": False, "edge": a, "t": edge, "got": G(edge, c5)}
        lo = (5 << (a - 1)) - 1
        hi = 1 << (a + 2)
        c3 = (3 << a) - 1
        ones = [t for t in range(lo, hi) if G(t, c5)]
        if ones != [c3]:
            return {"ok": False, "a": a, "ones": ones, "want": c3}
        n_ok += hi - lo
        if a <= 3:
            sample[str(a)] = {"edge": edge, "c3": c3, "n": hi - lo}
    ok = n_ok > 0 and sample["1"]["c3"] == 5 and sample["2"]["c3"] == 11
    return {"ok": ok, "n_ok": n_ok, "a_hi": A_EDGE, "sample": sample}


def doubling_p4() -> dict:
    """k>=2: even n is unique 3U-2; odd n doubles parent xor 3U-1."""
    n_ok = 0
    rows = {}
    for k in range(2, K_SET + 1):
        U = 1 << k
        j = 5 * U - 2
        even = []
        odd = []
        for n in range(live_lo(k, 2), 4 * U):
            g = G(n, j)
            p = n // 2
            if n % 2 == 0:
                pred = G(p, 5 * (U // 2) - 1)
                if g != pred:
                    return {"ok": False, "even": True, "k": k, "n": n}
                if g:
                    even.append(n)
            else:
                pred = G(p, 5 * (U // 2) - 1) ^ G(p, 5 * (U // 2) - 2)
                if g != pred:
                    return {"ok": False, "odd": True, "k": k, "n": n}
                if g:
                    odd.append(n)
            n_ok += 1
        want_even = [3 * U - 2]
        parent = ones_at(k - 1, 2)
        want_odd = sorted({2 * s + 1 for s in parent} ^ {3 * U - 1})
        if even != want_even or odd != want_odd:
            return {
                "ok": False,
                "set": True,
                "k": k,
                "even": even,
                "odd": odd,
                "want_odd": want_odd,
            }
        if k <= 4:
            rows[str(k)] = {"even": even, "n_odd": len(odd)}
    ok = (
        n_ok > 0
        and rows["2"]["even"] == [10]
        and rows["3"]["even"] == [22]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def doubling_p6() -> dict:
    """k>=1: G(2p+1, 5U-3)=G(p, j4 of k-1); even n vanish."""
    n_ok = 0
    for k in range(1, K_SET + 1):
        U = 1 << k
        j = 5 * U - 3
        parent = set(ones_at(k - 1, 2))
        got = []
        for n in range(live_lo(k, 3), 4 * U):
            g = G(n, j) if 0 <= j <= 2 * n else 0
            if n % 2 == 0:
                if g:
                    return {"ok": False, "even": True, "k": k, "n": n}
            else:
                p = n // 2
                pred = G(p, 5 * (U // 2) - 2)
                if g != pred:
                    return {"ok": False, "odd": True, "k": k, "n": n}
                if g != int(p in parent):
                    return {"ok": False, "parent": True, "k": k, "n": n, "p": p}
                if g:
                    got.append(n)
            n_ok += 1
        want = sorted(2 * s + 1 for s in parent if live_lo(k, 3) <= 2 * s + 1 < 4 * U)
        if got != want:
            return {"ok": False, "set": True, "k": k, "got": got, "want": want}
    return {"ok": n_ok > 0, "n_ok": n_ok, "k_hi": K_SET}


def set_forms() -> dict:
    """k<=K_SET: closed sets match G=1; counts match LC/LD/LF q=10."""
    n_ok = 0
    rows = {}
    for k in range(0, K_SET + 1):
        g4 = ones_at(k, 2)
        g6 = ones_at(k, 3)
        g14 = ones_at(k, 7)
        w4 = [n for n in range(live_lo(k, 2), 4 << k) if in_p4(n, k)]
        w6 = [n for n in range(live_lo(k, 3), 4 << k) if in_p6(n, k)]
        if g4 != w4 or g6 != w6:
            return {"ok": False, "p4p6": k, "g4": g4, "w4": w4, "g6": g6, "w6": w6}
        if k >= 3:
            w14 = [n for n in range(live_lo(k, 7), 4 << k) if in_p14(n, k)]
            if g14 != w14:
                return {"ok": False, "p14": k, "g14": g14, "w14": w14}
        if len(g4) != want_p4_n(k, 10) or len(g4) != p4_count(k):
            return {"ok": False, "c4": k, "got": len(g4)}
        if len(g6) != want_p6_n(k, 10) or len(g6) != p6_count(k):
            return {"ok": False, "c6": k, "got": len(g6)}
        if len(g14) != p14_count(k):
            return {"ok": False, "c14": k, "got": len(g14)}
        if k >= 3 and len(g14) != want_p14_n(k, 10):
            return {"ok": False, "lf14": k, "got": len(g14)}
        xor4 = len(g4) % 2
        xor6 = len(g6) % 2
        xor14 = len(g14) % 2
        if xor4 != want_p4_xor(k) or xor6 != want_p6_gxor(k) or xor14 != want_p14_gxor(k):
            return {"ok": False, "xor": k}
        if xor6 != want_p6_xor(k):
            return {"ok": False, "ld": k}
        if k >= 3 and xor14 != want_p14_xor(k, 10):
            return {"ok": False, "lf": k}
        tot = xor4 ^ xor6 ^ xor14
        if tot != want_green_forced(k):
            return {"ok": False, "tot": k, "got": tot}
        if k <= 4:
            rows[str(k)] = {
                "n4": len(g4),
                "n6": len(g6),
                "n14": len(g14),
                "tot": tot,
            }
        n_ok += 1
    ok = (
        n_ok == K_SET + 1
        and rows["0"]["tot"] == 1
        and rows["1"]["tot"] == 0
        and rows["2"]["tot"] == 0
        and rows["3"]["tot"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_SET, "rows": rows}


def count_forms() -> dict:
    """k<=K_FORM: closed counts and xors; LC/LD/LF q=10."""
    n_ok = 0
    for k in range(0, K_FORM + 1):
        if p4_count(k) != want_p4_n(k, 10) or p4_count(k) % 2 != want_p4_xor(k):
            return {"ok": False, "p4": k}
        if p6_count(k) != want_p6_n(k, 10) or p6_count(k) % 2 != want_p6_gxor(k):
            return {"ok": False, "p6": k}
        if p14_count(k) % 2 != want_p14_gxor(k):
            return {"ok": False, "p14": k}
        if k >= 3 and p14_count(k) != want_p14_n(k, 10):
            return {"ok": False, "lf14": k}
        if want_green_forced(k) != (
            want_p4_xor(k) ^ want_p6_gxor(k) ^ want_p14_gxor(k)
        ):
            return {"ok": False, "tot": k}
        n_ok += 1
    ok = (
        n_ok == K_FORM + 1
        and want_green_forced(0) == 1
        and want_green_forced(1) == 0
        and want_green_forced(2) == 0
        and want_green_forced(8) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FORM}


def killed_green_eq_packed() -> dict:
    """k=1: Green tot=0, packed forced xor=1 (OG j_odd xor rest)."""
    og = json.loads(OG_JSON.read_text())
    row = og["q10_E_10"]["rows"]["1"]
    packed_f = row["xor_j_odd"] ^ row["xor_r"]
    ok = want_green_forced(1) == 0 and packed_f == 1
    return {
        "ok": ok,
        "k": 1,
        "green_tot": want_green_forced(1),
        "packed_f": packed_f,
        "xor_j_odd": row["xor_j_odd"],
        "xor_r": row["xor_r"],
    }


def killed_p14_k2() -> dict:
    """k=2 p=14 ones include 15, not in the k>=3 closed set."""
    k = 2
    got = ones_at(k, 7)
    closed = [n for n in range(live_lo(k, 7), 4 << k) if in_p14(n, k)]
    ok = 15 in got and 15 not in closed and got == [7, 11, 13, 15]
    return {"ok": ok, "k": k, "got": got, "closed": closed}


def prefixes() -> dict:
    pa = json.loads(PA_JSON.read_text())
    pb = json.loads(PB_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        pa["checks"]["all_ok"]
        and pb["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and pa["verdict"]["unique_col"] == "LEMMA"
        and pa["verdict"]["covering_S"] == "LEMMA"
        and pb["verdict"]["ST_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and pb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pa["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, edge, d4, d6, sets, counts, kpack, k14, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and edge["ok"]
        and d4["ok"]
        and d6["ok"]
        and sets["ok"]
        and counts["ok"]
        and kpack["ok"]
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
    edge = edge_unique()
    d4 = doubling_p4()
    d6 = doubling_p6()
    sets = set_forms()
    counts = count_forms()
    kpack = killed_green_eq_packed()
    k14 = killed_p14_k2()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, pal, slots, edge, d4, d6, sets, counts, kpack, k14, sc, pref
    )
    dump = {
        "cycle": "PC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "edge_unique": {k: edge[k] for k in edge if k != "ok"},
        "doubling_p4": {k: d4[k] for k in d4 if k != "ok"},
        "doubling_p6": {k: d6[k] for k in d6 if k != "ok"},
        "set_forms": {k: sets[k] for k in sets if k != "ok"},
        "count_forms": {k: counts[k] for k in counts if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_green_eq_packed": {k: kpack[k] for k in kpack if k != "ok"},
        "killed_p14_k2": {k: k14[k] for k in k14 if k != "ok"},
        "lemmas": {
            "p4_set": True,
            "p6_set": True,
            "p14_set_k_ge_3": True,
            "green_forced_xor": True,
            "packed_forced_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "p4_set": "LEMMA",
            "p6_set": "LEMMA",
            "p14_set_k_ge_3": "LEMMA",
            "green_forced_xor": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "green_eq_packed_forced": "KILLED",
            "p14_set_k2": "KILLED",
            "packed_forced_all_k": "PREFIX",
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
    print("edge_unique n_ok", dump["edge_unique"]["n_ok"])
    print("set_forms", dump["set_forms"]["rows"])
    print("killed_green_eq_packed", dump["killed_green_eq_packed"])
    print("killed_p14_k2", dump["killed_p14_k2"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
