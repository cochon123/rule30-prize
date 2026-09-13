#!/usr/bin/env python3
"""Cycle OQ: pal-right residue-0 xor is 1 iff popcount is even.

For t>=1, R0(t) (xor of G(t,t+d) over d%3==0) equals 1 iff
t.bit_count() is even. Even t halves. Odd t=2u+1 doubles to
R0(u) xor A(u), and A(u)=1 for u>=1. Then R1 on odd t>=3 is
R0((t-1)/2), and even t swaps residues, so pal-right S on every
n is a popcount / v2 evaluation. Not covering S (clip remains).
Not E_k=0 for all k. Do not catalogue further S/T subregions
unless the experiment answers why E_k=0. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_oq.py --certify
Dump: research/cycle_oq.json
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
from cycle_ok import pal_right_s
from cycle_on import doubled
from cycle_op import pal_right_R

OUT = Path(__file__).resolve().with_suffix(".json")
OP_JSON = Path(__file__).resolve().parent / "cycle_op.json"
OO_JSON = Path(__file__).resolve().parent / "cycle_oo.json"
ON_JSON = Path(__file__).resolve().parent / "cycle_on.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

T_HI = 128
N_S = 128
U_BOOL = 10
N_PAL = 64
M_SLOTS = 64


def r0_pc(t: int) -> int:
    """R0(t) is 1 iff popcount even, for t>=1; 0 at t=0."""
    if t <= 0:
        return 0
    return int(t.bit_count() % 2 == 0)


def r1_pc(t: int) -> int:
    """R1(t) from v2 unwind and odd R0."""
    if t <= 0:
        return 0
    k = (t & -t).bit_length() - 1
    s = t >> k
    if s == 1:
        base = 1
    else:
        base = r0_pc((s - 1) // 2)
    if k % 2:
        return base ^ 1
    return base


def r2_pc(t: int) -> int:
    """R2(t)=1 xor R1(t) for t>=1."""
    if t <= 0:
        return 0
    return 1 ^ r1_pc(t)


def pal_right_s_pc(n: int) -> int:
    """Unclipped pal-right S from popcount / v2."""
    if n % 2 == 0:
        return 0
    rem = n % 8
    if rem == 3:
        return int(n > 3)
    if rem == 7:
        return pal_right_s_pc((n - 3) // 4)
    if rem == 1:
        return r1_pc((n - 1) // 8)
    return r2_pc(2 * ((n - 5) // 8) + 1)


def child_R(b: list[int]) -> list[int]:
    r = [0, 0, 0]
    for i in range(1, len(b)):
        r[i % 3] ^= b[i]
    return r


def parent_R(c: list[int]) -> list[int]:
    r = [0, 0, 0]
    u = len(c) - 1
    for p in range(1, u + 1):
        r[p % 3] ^= c[p]
    return r


def r0_even_half() -> dict:
    """m<T_HI: R0(2m)==R0(m)."""
    n_ok = 0
    sample = {}
    for m in range(0, T_HI):
        if pal_right_R(2 * m)[0] != pal_right_R(m)[0]:
            return {"ok": False, "m": m}
        n_ok += 1
        if m <= 4:
            sample[str(m)] = {
                "R0_2m": pal_right_R(2 * m)[0],
                "R0_m": pal_right_R(m)[0],
            }
    ok = n_ok == T_HI and sample["0"]["R0_2m"] == 0 and sample["1"]["R0_m"] == 0
    return {"ok": ok, "n_ok": n_ok, "sample": sample}


def r0_odd_fold() -> dict:
    """u<T_HI: R0(2u+1)==R0(u) xor A(u)."""
    n_ok = 0
    sample = {}
    for u in range(0, T_HI):
        t = 2 * u + 1
        r0t = pal_right_R(t)[0]
        ru = pal_right_R(u)
        au = (ru[1] ^ ru[2]) if u else 0
        if r0t != (ru[0] ^ au):
            return {"ok": False, "u": u, "got": r0t, "want": ru[0] ^ au}
        n_ok += 1
        if u <= 4:
            sample[str(u)] = {"t": t, "R0": r0t, "A_u": au, "R0_u": ru[0]}
    ok = (
        n_ok == T_HI
        and sample["0"]["R0"] == 0
        and sample["1"]["R0"] == 1
        and sample["1"]["A_u"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "sample": sample}


def boolean_r0_fold() -> dict:
    """Any endpoint-1 parent: child R0 == parent R0 xor A."""
    n_ok = 0
    for u in range(0, U_BOOL + 1):
        n_free = max(u - 1, 0)
        for mask in range(1 << n_free):
            c = [1]
            for i in range(n_free):
                c.append((mask >> i) & 1)
            if u > 0:
                c.append(1)
            rc = parent_R(c)
            au = (rc[1] ^ rc[2]) if u else 0
            rb = child_R(doubled(c))
            if rb[0] != (rc[0] ^ au):
                return {"ok": False, "u": u, "mask": mask}
            n_ok += 1
    ok = n_ok == 1 + sum(1 << max(u - 1, 0) for u in range(1, U_BOOL + 1))
    return {"ok": ok, "n_ok": n_ok, "u_hi": U_BOOL}


def r0_popcount() -> dict:
    """1<=t<2*T_HI: R0(t)==r0_pc(t); R1/R2 match r1_pc/r2_pc."""
    n_ok = n_one = 0
    sample = {}
    for t in range(0, 2 * T_HI):
        r = pal_right_R(t)
        if r[0] != r0_pc(t) or r[1] != r1_pc(t) or (t >= 1 and r[2] != r2_pc(t)):
            return {
                "ok": False,
                "t": t,
                "R": r,
                "want": [r0_pc(t), r1_pc(t), r2_pc(t)],
            }
        n_ok += 1
        n_one += r[0]
        if t <= 8:
            sample[str(t)] = {"R": r, "pc": t.bit_count() if t else 0}
    ok = (
        n_ok == 2 * T_HI
        and sample["0"]["R"][0] == 0
        and sample["1"]["R"][0] == 0
        and sample["3"]["R"][0] == 1
        and sample["6"]["R"][0] == 1
        and sample["7"]["R"][0] == 0
        and r0_pc(1) == 0
        and r0_pc(3) == 1
        and r1_pc(1) == 1
        and r1_pc(2) == 0
        and n_one > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "sample": sample}


def s_pc() -> dict:
    """n<N_S: pal_right_s(n)==pal_right_s_pc(n)."""
    n_ok = n_one = 0
    sample = {}
    for n in range(0, N_S):
        got = pal_right_s(n)[0]
        want = pal_right_s_pc(n)
        if got != want:
            return {"ok": False, "n": n, "got": got, "want": want}
        n_ok += 1
        n_one += got
        if n <= 11 or n in (15, 17, 23, 39):
            sample[str(n)] = {"S": got}
    ok = (
        n_ok == N_S
        and sample["0"]["S"] == 0
        and sample["1"]["S"] == 0
        and sample["3"]["S"] == 0
        and sample["9"]["S"] == 1
        and sample["11"]["S"] == 1
        and sample["39"]["S"] == 1
        and n_one > 0
        and n_one < n_ok
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "n_hi": N_S, "sample": sample}


def killed_r0_t0(pop: dict) -> dict:
    ok = pop["sample"]["0"]["R"][0] == 0
    return {"ok": ok, "t": 0, "R0": 0}


def killed_r0_odd_pc(pop: dict) -> dict:
    ok = pop["sample"]["1"]["R"][0] == 0 and pop["sample"]["3"]["R"][0] == 1
    return {"ok": ok, "t1": 0, "t3": 1}


def prefixes() -> dict:
    op = json.loads(OP_JSON.read_text())
    oo = json.loads(OO_JSON.read_text())
    on = json.loads(ON_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        op["checks"]["all_ok"]
        and oo["checks"]["all_ok"]
        and on["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and op["verdict"]["b_eq_r2"] == "LEMMA"
        and op["verdict"]["s81_R1"] == "LEMMA"
        and oo["verdict"]["n3_one_all_t"] == "LEMMA"
        and on["verdict"]["s4_fold"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and op["verdict"]["odd_s_closed"] == "PREFIX"
        and op["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, half, fold, parent, pop, spc, k0, kpc, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and half["ok"]
        and fold["ok"]
        and parent["ok"]
        and pop["ok"]
        and spc["ok"]
        and k0["ok"]
        and kpc["ok"]
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
    half = r0_even_half()
    fold = r0_odd_fold()
    parent = boolean_r0_fold()
    pop = r0_popcount()
    spc = s_pc()
    k0 = killed_r0_t0(pop)
    kpc = killed_r0_odd_pc(pop)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, pal, slots, half, fold, parent, pop, spc, k0, kpc, sc, pref
    )
    dump = {
        "cycle": "OQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "r0_even_half": {k: half[k] for k in half if k != "ok"},
        "r0_odd_fold": {k: fold[k] for k in fold if k != "ok"},
        "boolean_r0_fold": {k: parent[k] for k in parent if k != "ok"},
        "r0_popcount": {k: pop[k] for k in pop if k != "ok"},
        "s_pc": {k: spc[k] for k in spc if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_r0_t0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_r0_odd_pc": {k: kpc[k] for k in kpc if k != "ok"},
        "lemmas": {
            "r0_popcount": True,
            "r0_even_half": True,
            "r0_odd_fold": True,
            "s_pc": True,
            "odd_s_closed": True,
            "b_eq_r2": True,
            "n3_one_all_t": True,
            "s4_fold": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "r0_t0": False,
            "r0_odd_pc": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "r0_popcount": "LEMMA",
            "r0_even_half": "LEMMA",
            "r0_odd_fold": "LEMMA",
            "s_pc": "LEMMA",
            "odd_s_closed": "LEMMA",
            "b_eq_r2": "LEMMA",
            "n3_one_all_t": "LEMMA",
            "s4_fold": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "r0_t0": "KILLED",
            "r0_odd_pc": "KILLED",
            "covering_S": "PREFIX",
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
    print("r0_popcount n_ok", dump["r0_popcount"]["n_ok"], "n_one", dump["r0_popcount"]["n_one"])
    print("s_pc n_ok", dump["s_pc"]["n_ok"], "n_one", dump["s_pc"]["n_one"])
    print("boolean_r0_fold", dump["boolean_r0_fold"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_r0_t0", dump["killed_r0_t0"])
    print("killed_r0_odd_pc", dump["killed_r0_odd_pc"])


if __name__ == "__main__":
    main()
