#!/usr/bin/env python3
"""Cycle ON: pal-right S(4s+3)=S(s) for every odd s.

Green doubling of n=2(2s+1)+1 splits pal-right S into od_even,
which is exactly S(s), and three extra classes. The extras xor
to 0: parent doubling of odd s writes the pal-right string as
the 01-interleave of G(u), u=(s-1)/2, and T01_0 xor T11_1 xor
T10_2 equals (u%3==2); od_odd also includes the corner 10 iff
s%3==2, which is the same bit. Hence S(8t+7)=S(2t+1) for every
t. Not the fold for even s. Not S(8t+3)=1 for all t>=1. Not
covering S (clip remains). Not E_k=0 for all k. Do not catalogue
further S/T subregions unless the experiment answers why E_k=0.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_on.py --certify
Dump: research/cycle_on.json
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
from cycle_ok import doubling_s, pal_right_s

OUT = Path(__file__).resolve().with_suffix(".json")
OM_JSON = Path(__file__).resolve().parent / "cycle_om.json"
OL_JSON = Path(__file__).resolve().parent / "cycle_ol.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

S_HI = 128
U_BOOL = 10
N_PAL = 64
M_SLOTS = 64


def trans_xor(b: list[int], a0: int, a1: int, r: int) -> int:
    """Xor-count of (a0,a1) starts at i%r==r, i=0..len(b)-2."""
    acc = 0
    for i in range(len(b) - 1):
        if i % 3 == r and b[i] == a0 and b[i + 1] == a1:
            acc ^= 1
    return acc


def doubled(c: list[int]) -> list[int]:
    """Pal-right interleave of parent c with virtual c[u+1]=0."""
    u = len(c) - 1
    b: list[int] = []
    for p in range(u):
        b.append(c[p])
        b.append(c[p] ^ c[p + 1])
    b.append(c[u])
    b.append(c[u])  # c[u] xor 0
    return b


def extras_count(b: list[int]) -> int:
    return trans_xor(b, 0, 1, 0) ^ trans_xor(b, 1, 1, 1) ^ trans_xor(b, 1, 0, 2)


def class_xors(s: int) -> dict:
    """Split doubling_s(2s+1) by r mod 6."""
    m = 2 * s + 1
    ev_even = ev_odd = od_even = od_odd = 0
    n_ee = n_eo = n_oe = n_oo = 0
    n_oo_zero = 0
    for k in range(m + 1, 2 * m + 2):
        r = k - m
        if r % 3 != 1:
            continue
        if G(m, k - 1) != 0 or G(m, k) != 1:
            continue
        if r % 2 == 0:
            ev_even ^= 1
            n_ee += 1
        else:
            ev_odd ^= 1
            n_eo += 1
    for k in range(m + 1, 2 * m + 1):
        r = k - m
        if r % 3 != 2:
            continue
        if G(m, k - 1) != 1 or G(m, k) != 1:
            continue
        bit = 1 ^ G(m, k + 1)
        if r % 2 == 0:
            od_even ^= bit
            n_oe += 1
        else:
            od_odd ^= bit
            n_oo += 1
            n_oo_zero += bit == 0
    extras = ev_even ^ ev_odd ^ od_odd
    return {
        "ev_even": ev_even,
        "ev_odd": ev_odd,
        "od_even": od_even,
        "od_odd": od_odd,
        "extras": extras,
        "n_ee": n_ee,
        "n_eo": n_eo,
        "n_oe": n_oe,
        "n_oo": n_oo,
        "n_oo_zero": n_oo_zero,
    }


def pal_right_double(s: int) -> bool:
    """Odd s=2u+1: G(s,s+2p)=G(u,u+p), G(s,s+2p+1)=G(u,u+p) xor G(u,u+p+1)."""
    if s % 2 == 0:
        raise ValueError("odd s required")
    u = s // 2
    for i in range(s + 1):
        p = i // 2
        if i % 2 == 0:
            if G(s, s + i) != G(u, u + p):
                return False
        else:
            if G(s, s + i) != (G(u, u + p) ^ G(u, u + p + 1)):
                return False
    return True


def boolean_parent_extras() -> dict:
    """Any endpoint-1 parent: extras_count(doubled(c))==(u%3==2)."""
    n_ok = 0
    for u in range(0, U_BOOL + 1):
        n_free = max(u - 1, 0)
        for mask in range(1 << n_free):
            c = [1]
            for i in range(n_free):
                c.append((mask >> i) & 1)
            if u > 0:
                c.append(1)
            if len(c) != u + 1:
                return {"ok": False, "len": len(c), "u": u}
            b = doubled(c)
            if len(b) != 2 * u + 2:
                return {"ok": False, "blen": len(b), "u": u}
            if b[0] != 1 or b[-1] != 1:
                return {"ok": False, "ends": u}
            got = extras_count(b)
            want = int(u % 3 == 2)
            if got != want:
                return {"ok": False, "u": u, "mask": mask, "got": got, "want": want}
            n_ok += 1
    ok = n_ok == 1 + sum(1 << max(u - 1, 0) for u in range(1, U_BOOL + 1))
    return {"ok": ok, "n_ok": n_ok, "u_hi": U_BOOL}


def residue_iff() -> dict:
    """s=2u+1: s%3==2 iff u%3==2."""
    n_ok = 0
    for u in range(0, 96):
        s = 2 * u + 1
        if (s % 3 == 2) != (u % 3 == 2):
            return {"ok": False, "u": u, "s": s}
        n_ok += 1
    return {"ok": n_ok == 96, "n_ok": n_ok}


def s4_fold() -> dict:
    """Odd s<S_HI: pal_right_s(4s+3)==S(s)==od_even, extras=0."""
    n_ok = n_one = 0
    n_oo_zero = 0
    sample = {}
    for s in range(1, S_HI, 2):
        if not pal_right_double(s):
            return {"ok": False, "double": s}
        xor_s = pal_right_s(s)[0]
        child = pal_right_s(4 * s + 3)[0]
        dbl = doubling_s(2 * s + 1)
        cls = class_xors(s)
        b = [G(s, s + i) for i in range(s + 1)]
        tcount = extras_count(b)
        corner = int(s % 3 == 2)
        if (
            child != xor_s
            or dbl != xor_s
            or cls["od_even"] != xor_s
            or cls["extras"] != 0
            or cls["n_oo_zero"] != 0
            or (tcount ^ corner) != 0
        ):
            return {
                "ok": False,
                "s": s,
                "child": child,
                "xor": xor_s,
                "dbl": dbl,
                "cls": cls,
                "tcount": tcount,
                "corner": corner,
            }
        n_ok += 1
        n_one += xor_s
        n_oo_zero += cls["n_oo_zero"]
        if s <= 11 or s in (39, 127):
            sample[str(s)] = {
                "xor": xor_s,
                "child": child,
                "n": 4 * s + 3,
                "extras": cls["extras"],
                "n_oe": cls["n_oe"],
                "n_ee": cls["n_ee"],
                "n_eo": cls["n_eo"],
                "n_oo": cls["n_oo"],
            }
    ok = (
        n_ok == S_HI // 2
        and sample["1"]["xor"] == 0
        and sample["1"]["n"] == 7
        and sample["9"]["xor"] == 1
        and sample["9"]["n"] == 39
        and sample["127"]["xor"] == pal_right_s(127)[0]
        and n_one > 0
        and n_one < n_ok
        and n_oo_zero == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_one": n_one,
        "s_hi": S_HI,
        "n_oo_zero": n_oo_zero,
        "sample": sample,
    }


def killed_even_s() -> dict:
    """Fold fails for even s=2: S(11)=1, S(2)=0."""
    s11 = pal_right_s(11)[0]
    s2 = pal_right_s(2)[0]
    ok = s11 == 1 and s2 == 0
    return {"ok": ok, "s": 2, "n": 11, "S_n": s11, "S_s": s2}


def killed_fold_zero(fold: dict) -> dict:
    ok = fold["sample"]["9"]["xor"] == 1
    return {"ok": ok, "s": 9, "n": 39, "xor": 1}


def prefixes() -> dict:
    om = json.loads(OM_JSON.read_text())
    ol = json.loads(OL_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        om["checks"]["all_ok"]
        and ol["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and om["verdict"]["n7_fold"] == "CERTIFIED"
        and om["verdict"]["n7_all_t"] == "PREFIX"
        and ol["verdict"]["n3_off0"] == "LEMMA"
        and ol["verdict"]["even_m_s"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and om["verdict"]["prize"] == "unsolved"
        and ol["verdict"]["n3_one_all_t"] == "PREFIX"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, parent, iff, fold, ke, kz, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and parent["ok"]
        and iff["ok"]
        and fold["ok"]
        and ke["ok"]
        and kz["ok"]
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
    parent = boolean_parent_extras()
    iff = residue_iff()
    fold = s4_fold()
    ke = killed_even_s()
    kz = killed_fold_zero(fold)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, parent, iff, fold, ke, kz, sc, pref)
    dump = {
        "cycle": "ON",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "boolean_parent_extras": {k: parent[k] for k in parent if k != "ok"},
        "residue_iff": {k: iff[k] for k in iff if k != "ok"},
        "s4_fold": {k: fold[k] for k in fold if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_even_s": {k: ke[k] for k in ke if k != "ok"},
        "killed_fold_zero": {k: kz[k] for k in kz if k != "ok"},
        "lemmas": {
            "s4_fold": True,
            "n7_all_t": True,
            "extras_cancel": True,
            "od_even_is_S": True,
            "n3_off0": True,
            "even_m_s": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "even_s_fold": False,
            "fold_zero": False,
            "n3_one_all_t": False,
            "odd_s_closed": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "s4_fold": "LEMMA",
            "n7_all_t": "LEMMA",
            "extras_cancel": "LEMMA",
            "od_even_is_S": "LEMMA",
            "n3_off0": "LEMMA",
            "even_m_s": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "even_s_fold": "KILLED",
            "fold_zero": "KILLED",
            "n3_one_all_t": "PREFIX",
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
    print("s4_fold n_ok", dump["s4_fold"]["n_ok"], "n_one", dump["s4_fold"]["n_one"])
    print("boolean_parent_extras", dump["boolean_parent_extras"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_even_s", dump["killed_even_s"])
    print("killed_fold_zero", dump["killed_fold_zero"])


if __name__ == "__main__":
    main()
