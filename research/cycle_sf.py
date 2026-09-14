#!/usr/bin/env python3
"""Cycle SF: odd-child odd-j consecutive Green is (g2 xor g1, g1, g1 xor g, g).

On n=2m+1, odd j=2r+1, doubling gives consecutive Green
(G(n,j+3), G(n,j+2), G(n,j+1), G(n,j)) equal to
(g2^g1, g1, g1^g, g) with g=G(m,r), g1=G(m,r+1), g2=G(m,r+2).
On G=1 this is Cycle SD. AND fires iff the 4-tuple is (0,0,1,1),
which requires g=1; off G=1 the form is AND-dead. Cycle SE
even-child odd-j form is (g2, 0, g1, 0), not this 4-tuple.
Packed AND at consecutive-p can still fire (Cycle QV mismatch).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sf.py --certify
Dump: research/cycle_sf.json
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
from cycle_hh import AND_ONES, and_from_tuple
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_rx import cons_g4
from cycle_sd import odd_g1_oddj_cons
from cycle_se import even_child_oddj_cons

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
SD_JSON = Path(__file__).resolve().parent / "cycle_sd.json"
SE_JSON = Path(__file__).resolve().parent / "cycle_se.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8

T0011 = (0, 0, 1, 1)
T0000 = (0, 0, 0, 0)
T1110 = (1, 1, 1, 0)


def odd_child_oddj_cons(m: int, r: int) -> tuple[int, int, int, int]:
    """Odd-child odd-j consecutive Green from parent bits G(m,r), G(m,r+1), G(m,r+2)."""
    g = G(m, r)
    g1 = G(m, r + 1)
    g2 = G(m, r + 2)
    return (g2 ^ g1, g1, g1 ^ g, g)


def identity() -> dict:
    """m<M_HI: odd-child odd-j cons Green equals (g2 xor g1, g1, g1 xor g, g)."""
    n_ok = n_g1 = n_and = n_eq_sd = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(1, 2 * n + 1, 2):
            r = j // 2
            got = cons_g4(n, j)
            want = odd_child_oddj_cons(m, r)
            if got != want:
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            if G(n, j) == 1:
                n_g1 += 1
                if got != odd_g1_oddj_cons(m, r) or got[-1] != 1:
                    return {"ok": False, "sd": True, "m": m, "j": j, "got": list(got)}
                n_eq_sd += 1
            fires = got in AND_ONES or and_from_tuple(*got) or and_clause(*got)
            if fires:
                if got != T0011 or G(n, j) != 1:
                    return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
                n_and += 1
    ok = (
        n_ok == 4096
        and n_g1 == 1344
        and n_eq_sd == n_g1
        and n_and == 372
        and odd_child_oddj_cons(0, 0) == T0011
        and odd_child_oddj_cons(2, 1) == T1110
        and odd_child_oddj_cons(0, 0) == odd_g1_oddj_cons(0, 0)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_eq_sd": n_eq_sd,
        "n_and": n_and,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering odd n, odd j, cons Green matches odd_child_oddj_cons."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n_g1 = n_and = 0
        for n in range(1, 4 * U, 2):
            m = n // 2
            for j in range(1, 2 * n + 1, 2):
                r = j // 2
                got = cons_g4(n, j)
                if got != odd_child_oddj_cons(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if G(n, j) == 1:
                    n_g1 += 1
                    if got != odd_g1_oddj_cons(m, r):
                        return {"ok": False, "sd": True, "k": k, "n": n, "j": j}
                if got in AND_ONES or and_clause(*got):
                    if got != T0011 or G(n, j) != 1:
                        return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                    n_and += 1
        n_ok += 1
        rows[str(k)] = {"n_cell": n_cell, "n_g1": n_g1, "n_and": n_and}
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["0"]["n_g1"] == 4
        and rows["0"]["n_and"] == 2
        and rows["5"]["n_cell"] == 4096
        and rows["5"]["n_g1"] == 1344
        and rows["5"]["n_and"] == 372
        and rows["8"]["n_cell"] > 0
        and all(
            rows[str(k)]["n_g1"] >= rows[str(k)]["n_and"]
            for k in range(0, K_COV + 1)
        )
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """AND iff 0011; G=1 equals SD; off G=1 not SE."""
    t0011 = odd_child_oddj_cons(0, 0)
    t1110 = odd_child_oddj_cons(2, 1)
    ok = (
        t0011 == T0011
        and t1110 == T1110
        and T0011 in AND_ONES
        and and_from_tuple(*T0011) == 1
        and t1110 not in AND_ONES
        and and_from_tuple(*t1110) == 0
        and t0011 == odd_g1_oddj_cons(0, 0)
        and t1110 != odd_g1_oddj_cons(2, 1)
        and t1110 != even_child_oddj_cons(2, 1)
        and cons_g4(1, 1) == T0011
        and cons_g4(5, 3) == T1110
        and G(5, 3) == 0
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Never AND; identically SD; equals SE; identically 0000."""
    ok = (
        T0011 in AND_ONES
        and odd_child_oddj_cons(0, 0) == T0011
        and odd_child_oddj_cons(2, 1) == T1110
        and odd_child_oddj_cons(2, 1) != odd_g1_oddj_cons(2, 1)
        and odd_child_oddj_cons(2, 1) != even_child_oddj_cons(2, 1)
        and odd_child_oddj_cons(2, 1) != T0000
        and T1110 not in AND_ONES
        and G(2, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    sd = json.loads(SD_JSON.read_text())
    se = json.loads(SE_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and sd["checks"]["all_ok"]
        and se["checks"]["all_ok"]
        and sd["verdict"]["odd_g1_oddj_cons_eq_g2xg1_g1_g1x_1"] == "LEMMA"
        and sd["verdict"]["odd_g1_oddj_cons_meets_AND_ONES"] == "LEMMA"
        and se["verdict"]["even_child_oddj_cons_eq_Gmr2_0_Gmr1_0"] == "LEMMA"
        and se["verdict"]["even_child_oddj_cons_AND_iff_0010"] == "LEMMA"
        and se["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and se["verdict"]["prize"] == "unsolved"
        and odd_child_oddj_cons(0, 0) == T0011
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, ident, cov, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert ident["ok"] and cov["ok"] and tot["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
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
    ident = identity()
    cov = covering_chk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, ident, cov, tot, kl, sc, pref)
    dump = {
        "cycle": "SF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "identity": {k: ident[k] for k in ident if k != "ok"},
        "covering_chk": {k: cov[k] for k in cov if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_child_oddj_cons_eq_g2xg1_g1_g1xg_g": True,
            "odd_child_oddj_cons_G1_eq_SD": True,
            "odd_child_oddj_cons_AND_iff_0011": True,
            "odd_child_oddj_cons_never_AND": False,
            "odd_child_oddj_cons_eq_SD": False,
            "odd_child_oddj_cons_eq_SE": False,
            "odd_child_oddj_cons_eq_0000": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_child_oddj_cons_eq_g2xg1_g1_g1xg_g": "LEMMA",
            "odd_child_oddj_cons_G1_eq_SD": "LEMMA",
            "odd_child_oddj_cons_AND_iff_0011": "LEMMA",
            "odd_child_oddj_cons_never_AND": "KILLED",
            "odd_child_oddj_cons_eq_SD": "KILLED",
            "odd_child_oddj_cons_eq_SE": "KILLED",
            "odd_child_oddj_cons_eq_0000": "KILLED",
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
        "identity n_ok",
        dump["identity"]["n_ok"],
        "n_g1",
        dump["identity"]["n_g1"],
        "n_and",
        dump["identity"]["n_and"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
