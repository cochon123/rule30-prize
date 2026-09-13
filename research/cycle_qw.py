#!/usr/bin/env python3
"""Cycle QW: covering Green even-n rest is 1 iff k!=1.

Cycle QV's 2-fold sends even-n clipped G=1 at k to all clipped G=1
at k-1, so even-n G=1 xor equals Cycle QH's clip xor at k-1, which
is 1 iff k==1. For k>=1 forced p=6 and p=14 have odd j, hence vanish
on even n, and Cycle PC's even-n p=4 is the unique cell n=3U-2, xor
1. Green even-n rest off forced is therefore 1 iff k!=1. Green odd-n
rest is 1 iff k in {0,2}; for k>=3 the Green residual lives only on
even n (Cycle QH tot 1 iff k>=3). Packed even-n rest is not this bit
(k=1: packed 1 vs Green 0; k=3: packed 0 vs Green 1). Not rest=S xor
T for all k. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qw.py --certify
Dump: research/cycle_qw.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import in_p4, want_p4_xor, want_p6_gxor, want_p14_gxor
from cycle_qh import want_clip_g1, want_green_rest
from cycle_qv import even_slots

OUT = Path(__file__).resolve().with_suffix(".json")
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"

N_PAL = 64
M_SLOTS = 64
K_GREEN = 8
K_ALG = 64
Q = 10


def want_green_even(k: int) -> int:
    """Green even-n rest off forced: 1 iff k!=1, all k."""
    return int(k != 1)


def want_green_odd(k: int) -> int:
    """Green odd-n rest off forced: 1 iff k in {0,2}, all k."""
    return int(k in (0, 2))


def want_g1_even(k: int) -> int:
    """Even-n clipped G=1 xor: 1 iff k==1."""
    return int(k == 1)


def want_p4_even(k: int) -> int:
    """Even-n Green p=4 xor: 1 iff k>=1."""
    return int(k >= 1)


def green_split(k: int) -> dict:
    """Clipped G=1 xor split by n parity, off forced and raw."""
    U = 1 << k
    clip = 5 * U
    ge = go = g1e = g1o = p4e = 0
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = Q * U - 2 * j
            if n % 2 == 0:
                g1e ^= 1
            else:
                g1o ^= 1
            if p == 4 and n % 2 == 0:
                p4e ^= 1
            if p in FORCED:
                continue
            if n % 2 == 0:
                ge ^= 1
            else:
                go ^= 1
    return {"ge": ge, "go": go, "g1e": g1e, "g1o": g1o, "p4e": p4e}


def p4_even_unique() -> dict:
    """k>=1: even-n G=1 at p=4 is the unique n=3U-2."""
    n_ok = 0
    for k in range(1, K_GREEN + 1):
        U = 1 << k
        j = 5 * U - 2
        n_hit = acc = 0
        hit_n = None
        lo = (j + 1) // 2
        for n in range(0, 4 * U, 2):
            if n < lo:
                continue
            if G(n, j) == 0:
                continue
            acc ^= 1
            n_hit += 1
            hit_n = n
        if (
            n_hit != 1
            or acc != 1
            or hit_n != 3 * U - 2
            or not in_p4(3 * U - 2, k)
            or acc != want_p4_even(k)
        ):
            return {
                "ok": False,
                "k": k,
                "n_hit": n_hit,
                "hit_n": hit_n,
            }
        n_ok += 1
    ok = n_ok == K_GREEN
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN}


def green_walk() -> dict:
    """k<=8: Green even/odd rest match the closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_GREEN + 1):
        w = green_split(k)
        if w["ge"] != want_green_even(k) or w["go"] != want_green_odd(k):
            return {"ok": False, "form": True, "k": k, "w": w}
        if w["ge"] ^ w["go"] != want_green_rest(k):
            return {"ok": False, "qh": True, "k": k, "w": w}
        if w["g1e"] != want_g1_even(k):
            return {"ok": False, "g1e": True, "k": k, "g1e": w["g1e"]}
        if k >= 1 and w["g1e"] != want_clip_g1(k - 1):
            return {"ok": False, "qv": True, "k": k}
        if w["p4e"] != want_p4_even(k):
            return {"ok": False, "p4e": True, "k": k, "p4e": w["p4e"]}
        if k >= 1 and w["ge"] != (w["g1e"] ^ w["p4e"]):
            return {"ok": False, "split": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = w
    ok = (
        n_ok == K_GREEN + 1
        and rows["0"]["ge"] == 1
        and rows["1"]["ge"] == 0
        and rows["2"]["ge"] == 1
        and rows["2"]["go"] == 1
        and rows["3"]["ge"] == 1
        and rows["3"]["go"] == 0
        and rows["8"]["ge"] == 1
        and rows["8"]["go"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def tot_form() -> dict:
    """k<=64: even xor odd Green rest is QH; even is g1e xor p4e for k>=1."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        ge = want_green_even(k)
        go = want_green_odd(k)
        if (ge ^ go) != want_green_rest(k):
            return {"ok": False, "qh": True, "k": k}
        if (ge ^ go) != (
            want_clip_g1(k)
            ^ want_p4_xor(k)
            ^ want_p6_gxor(k)
            ^ want_p14_gxor(k)
        ):
            return {"ok": False, "forced": True, "k": k}
        if k >= 1 and ge != (want_g1_even(k) ^ want_p4_even(k)):
            return {"ok": False, "even": True, "k": k}
        if k >= 1 and want_g1_even(k) != want_clip_g1(k - 1):
            return {"ok": False, "fold": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_green_even(1) == 0
        and want_green_even(2) == 1
        and want_green_odd(2) == 1
        and want_green_odd(3) == 0
        and want_green_rest(3) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def packed_kill() -> dict:
    """Packed even-n rest is not Green even-n rest (k=1 and k=3)."""
    qo = json.loads(QO_JSON.read_text())
    rows = qo["rest_n0_walk"]["rows"]

    def even_of(k: int) -> int:
        tot = rows[str(k)]["tot"]
        return tot[0] ^ tot[2]

    e1, e3 = even_of(1), even_of(3)
    ok = (
        e1 == 1
        and want_green_even(1) == 0
        and e1 != want_green_even(1)
        and e3 == 0
        and want_green_even(3) == 1
        and e3 != want_green_even(3)
        and even_of(2) == 1
        and want_green_even(2) == 1
        and even_of(8) == 1
        and want_green_even(8) == 1
        and even_of(6) == 0
        and want_green_even(6) == 1
    )
    return {
        "ok": ok,
        "k1_pack": e1,
        "k1_green": want_green_even(1),
        "k3_pack": e3,
        "k3_green": want_green_even(3),
        "k6_pack": even_of(6),
    }


def prefixes() -> dict:
    qv = json.loads(QV_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    qu = json.loads(QU_JSON.read_text())
    ok = (
        qv["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qu["checks"]["all_ok"]
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and qv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, p4, walk, tot, kill, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"] and p4["ok"]
    assert walk["ok"] and tot["ok"] and kill["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    p4 = p4_even_unique()
    walk = green_walk()
    tot = tot_form()
    kill = packed_kill()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, p4, walk, tot, kill, sc, pref)
    dump = {
        "cycle": "QW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "p4_even_unique": {k: p4[k] for k in p4 if k != "ok"},
        "green_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "packed_kill": {k: kill[k] for k in kill if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "green_even_rest_iff_k_ne_1": True,
            "green_odd_rest_iff_k_in_0_2": True,
            "green_even_eq_packed_even": False,
            "cellwise_2fold_and": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "green_even_rest_iff_k_ne_1": "LEMMA",
            "green_odd_rest_iff_k_in_0_2": "LEMMA",
            "green_even_eq_packed_even": "KILLED",
            "cellwise_2fold_and": "KILLED",
            "even_rest_eq_parent_odd_k_le_10": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
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
    print(
        "green_walk n_ok",
        dump["green_walk"]["n_ok"],
        "k1_ge",
        dump["green_walk"]["rows"]["1"]["ge"],
        "k8_ge",
        dump["green_walk"]["rows"]["8"]["ge"],
        "k1_pack",
        dump["packed_kill"]["k1_pack"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
