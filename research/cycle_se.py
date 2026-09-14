#!/usr/bin/env python3
"""Cycle SE: even-child odd-j consecutive Green is (G(m,r+2), 0, G(m,r+1), 0).

Cycle QV G(2m,2r)=G(m,r) and G(2m,odd)=0, so at even child n=2m and
odd j=2r+1 the consecutive Green bits (G(n,j+3), G(n,j+2), G(n,j+1),
G(n,j)) equal (G(m,r+2), 0, G(m,r+1), 0). Last bit is 0, so there
are no G=1 cells. The type (0,0,1,0) is in AND_ONES when G(m,r+2)=0
and G(m,r+1)=1; (0,1,0,0) never occurs. Cycle RX even-j form is
(0, G(m,r+1), 0, G(m,r)), not this 4-tuple. Packed AND at
consecutive-p can still fire (Cycle QV mismatch). Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_se.py --certify
Dump: research/cycle_se.json
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
from cycle_rx import cons_g4, even_child_g4
from cycle_sd import odd_g1_oddj_cons

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
RX_JSON = Path(__file__).resolve().parent / "cycle_rx.json"
SD_JSON = Path(__file__).resolve().parent / "cycle_sd.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8

T0000 = (0, 0, 0, 0)
T0010 = (0, 0, 1, 0)
T1000 = (1, 0, 0, 0)
T1010 = (1, 0, 1, 0)
T0100 = (0, 1, 0, 0)


def even_child_oddj_cons(m: int, r: int) -> tuple[int, int, int, int]:
    """Consecutive Green bits at even child n=2m, odd j=2r+1."""
    return (G(m, r + 2), 0, G(m, r + 1), 0)


def identity() -> dict:
    """m<M_HI: even-child odd-j cons Green equals (G(m,r+2), 0, G(m,r+1), 0)."""
    n_ok = n_g1 = n_and = n0000 = n0010 = n1000 = n1010 = 0
    for m in range(0, M_HI):
        n = 2 * m
        for r in range(0, 2 * m + 1):
            j = 2 * r + 1
            got = cons_g4(n, j)
            want = even_child_oddj_cons(m, r)
            if got != want:
                return {"ok": False, "id": True, "m": m, "r": r, "got": list(got)}
            if got[1] != 0 or got[3] != 0:
                return {"ok": False, "z": True, "m": m, "r": r, "got": list(got)}
            n_ok += 1
            if G(n, j) == 1:
                n_g1 += 1
            fires = got in AND_ONES or and_from_tuple(*got) or and_clause(*got)
            if fires:
                if got != T0010:
                    return {"ok": False, "and": True, "m": m, "r": r, "got": list(got)}
                n_and += 1
            if got == T0000:
                n0000 += 1
            elif got == T0010:
                n0010 += 1
            elif got == T1000:
                n1000 += 1
            elif got == T1010:
                n1010 += 1
            else:
                return {"ok": False, "pair": True, "m": m, "r": r, "got": list(got)}
    ok = (
        n_ok == n0000 + n0010 + n1000 + n1010
        and n_ok == 4096
        and n_g1 == 0
        and n_and == 800
        and n0010 == 800
        and n0000 == 2048
        and n1000 == 768
        and n1010 == 480
        and even_child_oddj_cons(0, 0) == T0000
        and even_child_oddj_cons(1, 1) == T0010
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_and": n_and,
        "n0000": n0000,
        "n0010": n0010,
        "n1000": n1000,
        "n1010": n1010,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering even n, odd j, cons Green matches even_child_oddj_cons."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n_g1 = n_and = n0010 = 0
        for n in range(0, 4 * U, 2):
            m = n // 2
            for r in range(0, n + 1):
                j = 2 * r + 1
                got = cons_g4(n, j)
                if got != even_child_oddj_cons(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "r": r}
                n_cell += 1
                if G(n, j) == 1:
                    n_g1 += 1
                if got in AND_ONES or and_clause(*got):
                    if got != T0010:
                        return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                    n_and += 1
                    n0010 += 1
        n_ok += 1
        rows[str(k)] = {
            "n_cell": n_cell,
            "n_g1": n_g1,
            "n_and": n_and,
            "n0010": n0010,
        }
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["0"]["n_g1"] == 0
        and rows["0"]["n_and"] == 1
        and rows["5"]["n_cell"] == 4096
        and rows["5"]["n_and"] == 800
        and rows["8"]["n_cell"] > 0
        and all(rows[str(k)]["n_g1"] == 0 for k in range(0, K_COV + 1))
        and all(rows[str(k)]["n_and"] == rows[str(k)]["n0010"] for k in range(0, K_COV + 1))
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """Form is (x,0,y,0); 0010 is AND_ONES; 0100 never; not RX/SD."""
    t0000 = even_child_oddj_cons(0, 0)
    t0010 = even_child_oddj_cons(1, 1)
    ok = (
        t0000 == T0000
        and t0010 == T0010
        and T0010 in AND_ONES
        and T0100 in AND_ONES
        and and_from_tuple(*T0010) == 1
        and and_clause(*T0010) == 1
        and t0000 not in AND_ONES
        and T1000 not in AND_ONES
        and T1010 not in AND_ONES
        and t0000 != even_child_g4(0, 0)
        and even_child_g4(0, 0) == (0, 0, 0, 1)
        and t0010 != odd_g1_oddj_cons(0, 0)
        and cons_g4(2, 3) == T0010
        and G(2, 3) == 0
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Never AND; equals RX even-j; G=1 nonempty; equals SD."""
    ok = (
        T0010 in AND_ONES
        and even_child_oddj_cons(1, 1) == T0010
        and even_child_oddj_cons(0, 0) == T0000
        and even_child_oddj_cons(0, 0) != even_child_g4(0, 0)
        and cons_g4(2, 3) != odd_g1_oddj_cons(0, 0)
        and G(0, 1) == 0
        and G(2, 1) == 0
        and G(4, 1) == 0
        and T0100 != even_child_oddj_cons(1, 1)
    )
    return {"ok": ok}


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    rx = json.loads(RX_JSON.read_text())
    sd = json.loads(SD_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and rx["checks"]["all_ok"]
        and sd["checks"]["all_ok"]
        and rx["verdict"]["even_child_cons_g4_eq_0_Gmrp1_0_Gmr"] == "LEMMA"
        and rx["verdict"]["even_child_g1_cons_g4_never_AND"] == "LEMMA"
        and rx["verdict"]["even_child_cons_g4_never_AND_ONES"] == "KILLED"
        and sd["verdict"]["odd_g1_oddj_cons_eq_g2xg1_g1_g1x_1"] == "LEMMA"
        and sd["verdict"]["odd_g1_oddj_cons_meets_AND_ONES"] == "LEMMA"
        and sd["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sd["verdict"]["prize"] == "unsolved"
        and even_child_oddj_cons(0, 0) == T0000
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
        "cycle": "SE",
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
            "even_child_oddj_cons_eq_Gmr2_0_Gmr1_0": True,
            "even_child_oddj_cons_never_G1": True,
            "even_child_oddj_cons_AND_iff_0010": True,
            "even_child_oddj_cons_never_AND": False,
            "even_child_oddj_cons_eq_RX": False,
            "even_child_oddj_cons_eq_SD": False,
            "even_child_oddj_cons_eq_0000": False,
            "even_child_oddj_cons_meets_0100": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_child_oddj_cons_eq_Gmr2_0_Gmr1_0": "LEMMA",
            "even_child_oddj_cons_never_G1": "LEMMA",
            "even_child_oddj_cons_AND_iff_0010": "LEMMA",
            "even_child_oddj_cons_never_AND": "KILLED",
            "even_child_oddj_cons_eq_RX": "KILLED",
            "even_child_oddj_cons_eq_SD": "KILLED",
            "even_child_oddj_cons_eq_0000": "KILLED",
            "even_child_oddj_cons_meets_0100": "KILLED",
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
        "n_and",
        dump["identity"]["n_and"],
        "n_g1",
        dump["identity"]["n_g1"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
