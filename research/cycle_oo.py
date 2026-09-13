#!/usr/bin/env python3
"""Cycle OO: pal-right off-residue-0 xor is 1 for every t>=1.

A(t) is the xor of G(t,j) on pal-right j with (j-t)%3 != 0.
Even t=2m: odd offsets vanish, so A(2m)=A(m). Odd t=2u+1: Green
doubling writes A(t)=A(u) xor (1 xor A(u))=1. Hence A(t)=1 for
every t>=1, and S(8t+3)=1 for every t>=1. Empty at t=0 so S(3)=0.
Not a 0-1 closed S for every odd n (even-parent residue xor
remains). Not covering S (clip remains). Not E_k=0 for all k.
Do not catalogue further S/T subregions unless the experiment
answers why E_k=0. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_oo.py --certify
Dump: research/cycle_oo.json
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
from cycle_ol import pal_right_off0
from cycle_on import doubled

OUT = Path(__file__).resolve().with_suffix(".json")
ON_JSON = Path(__file__).resolve().parent / "cycle_on.json"
OL_JSON = Path(__file__).resolve().parent / "cycle_ol.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

T_HI = 128
U_BOOL = 10
N_PAL = 64
M_SLOTS = 64


def A(t: int) -> int:
    """Pal-right G xor off residue 0."""
    return pal_right_off0(t)


def child_A(b: list[int]) -> int:
    """Xor of b[i] for i=1..len-1 with i%3 != 0."""
    acc = 0
    for i in range(1, len(b)):
        if i % 3:
            acc ^= b[i]
    return acc


def even_half() -> dict:
    """Even t=2m<2*T_HI: odd offsets silent and A(2m)==A(m)."""
    n_ok = n_odd_d = 0
    sample = {}
    for m in range(0, T_HI):
        t = 2 * m
        for d in range(1, t + 1, 2):
            if G(t, t + d) != 0:
                return {"ok": False, "odd_d": t, "d": d}
            n_odd_d += 1
        got = A(t)
        want = A(m)
        if got != want:
            return {"ok": False, "t": t, "got": got, "want": want}
        n_ok += 1
        if m <= 8:
            sample[str(t)] = {"A": got, "A_m": want, "m": m}
    ok = (
        n_ok == T_HI
        and sample["0"]["A"] == 0
        and sample["2"]["A"] == 1
        and sample["4"]["A"] == 1
        and A(1) == 1
        and n_odd_d > 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_odd_d": n_odd_d,
        "t_hi": 2 * T_HI,
        "sample": sample,
    }


def odd_one() -> dict:
    """Odd t<2*T_HI: A(t)==1==A(u) xor (1 xor A(u))."""
    n_ok = 0
    sample = {}
    for t in range(1, 2 * T_HI, 2):
        u = t // 2
        got = A(t)
        au = A(u)
        want = au ^ (1 ^ au)
        b = [G(t, t + i) for i in range(t + 1)]
        if got != 1 or want != 1 or child_A(b) != 1:
            return {
                "ok": False,
                "t": t,
                "got": got,
                "want": want,
                "child": child_A(b),
            }
        n_ok += 1
        if t <= 15:
            sample[str(t)] = {"A": got, "A_u": au, "u": u}
    ok = (
        n_ok == T_HI
        and sample["1"]["A"] == 1
        and sample["1"]["A_u"] == 0
        and sample["3"]["A"] == 1
        and sample["9"]["A"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "t_hi": 2 * T_HI, "sample": sample}


def boolean_odd_A() -> dict:
    """Any endpoint-1 parent: child_A(doubled(c))==1."""
    n_ok = 0
    for u in range(0, U_BOOL + 1):
        n_free = max(u - 1, 0)
        for mask in range(1 << n_free):
            c = [1]
            for i in range(n_free):
                c.append((mask >> i) & 1)
            if u > 0:
                c.append(1)
            b = doubled(c)
            if child_A(b) != 1:
                return {"ok": False, "u": u, "mask": mask}
            n_ok += 1
    ok = n_ok == 1 + sum(1 << max(u - 1, 0) for u in range(1, U_BOOL + 1))
    return {"ok": ok, "n_ok": n_ok, "u_hi": U_BOOL}


def n3_one() -> dict:
    """t<T_HI: pal_right_s(8t+3)==A(t)==int(t>0)."""
    n_ok = 0
    sample = {}
    for t in range(0, T_HI):
        xor_s = pal_right_s(8 * t + 3)[0]
        a = A(t)
        want = int(t > 0)
        if xor_s != a or a != want:
            return {"ok": False, "t": t, "xor": xor_s, "A": a, "want": want}
        n_ok += 1
        if t <= 4 or t == 127:
            sample[str(t)] = {"n": 8 * t + 3, "xor": xor_s, "A": a}
    ok = (
        n_ok == T_HI
        and sample["0"]["xor"] == 0
        and sample["1"]["xor"] == 1
        and sample["127"]["xor"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_HI, "sample": sample}


def killed_t0(n3: dict) -> dict:
    ok = n3["sample"]["0"]["xor"] == 0
    return {"ok": ok, "t": 0, "n": 3, "xor": 0}


def killed_odd_closed() -> dict:
    """n=1 is 0 while n=9 is 1: even-parent residue is not a single bit."""
    s1 = pal_right_s(1)[0]
    s9 = pal_right_s(9)[0]
    ok = s1 == 0 and s9 == 1
    return {"ok": ok, "n1": s1, "n9": s9}


def prefixes() -> dict:
    on = json.loads(ON_JSON.read_text())
    ol = json.loads(OL_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        on["checks"]["all_ok"]
        and ol["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and on["verdict"]["s4_fold"] == "LEMMA"
        and on["verdict"]["n3_one_all_t"] == "PREFIX"
        and ol["verdict"]["n3_off0"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and on["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, half, odd, parent, n3, k0, kc, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and half["ok"]
        and odd["ok"]
        and parent["ok"]
        and n3["ok"]
        and k0["ok"]
        and kc["ok"]
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
    half = even_half()
    odd = odd_one()
    parent = boolean_odd_A()
    n3 = n3_one()
    k0 = killed_t0(n3)
    kc = killed_odd_closed()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, half, odd, parent, n3, k0, kc, sc, pref)
    dump = {
        "cycle": "OO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_half": {k: half[k] for k in half if k != "ok"},
        "odd_one": {k: odd[k] for k in odd if k != "ok"},
        "boolean_odd_A": {k: parent[k] for k in parent if k != "ok"},
        "n3_one": {k: n3[k] for k in n3 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_t0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_odd_closed": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "n3_one_all_t": True,
            "even_half": True,
            "odd_A_one": True,
            "n3_off0": True,
            "s4_fold": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "n3_t0": False,
            "odd_s_closed": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n3_one_all_t": "LEMMA",
            "even_half": "LEMMA",
            "odd_A_one": "LEMMA",
            "n3_off0": "LEMMA",
            "s4_fold": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "n3_t0": "KILLED",
            "odd_s_closed": "PREFIX",
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
    print("even_half n_ok", dump["even_half"]["n_ok"])
    print("odd_one n_ok", dump["odd_one"]["n_ok"])
    print("boolean_odd_A", dump["boolean_odd_A"])
    print("n3_one n_ok", dump["n3_one"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_t0", dump["killed_t0"])
    print("killed_odd_closed", dump["killed_odd_closed"])


if __name__ == "__main__":
    main()
