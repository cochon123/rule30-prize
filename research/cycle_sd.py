#!/usr/bin/env python3
"""Cycle SD: odd-child G=1 odd-j consecutive Green is (g2 xor g1, g1, g1 xor 1, 1).

On n=2m+1, odd j=2r+1, G=1, doubling gives G(m,r)=1 and consecutive
Green (G(n,j+3), G(n,j+2), G(n,j+1), G(n,j)) equals
(g2^g1, g1, g1^1, 1) with g1=G(m,r+1) and g2=G(m,r+2): one of
(1,0,1,1), (0,0,1,1), (1,1,0,1), (0,1,0,1). The type (0,0,1,1) is
in AND_ONES (g1=g2=0). Cycle SB odd-j green4 is never AND, so
consecutive AND does not imply green4/packed-slot AND. Cycle SC
even-j consecutive is not this 4-tuple. Type counts are not equal.
Packed AND at consecutive-p can still fire (Cycle QV mismatch).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sd.py --certify
Dump: research/cycle_sd.json
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
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_rx import cons_g4
from cycle_sb import odd_g1_oddj_green4
from cycle_sc import odd_g1_evenj_cons

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
SB_JSON = Path(__file__).resolve().parent / "cycle_sb.json"
SC_JSON = Path(__file__).resolve().parent / "cycle_sc.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8

T1011 = (1, 0, 1, 1)
T0011 = (0, 0, 1, 1)
T1101 = (1, 1, 0, 1)
T0101 = (0, 1, 0, 1)


def odd_g1_oddj_cons(m: int, r: int) -> tuple[int, int, int, int]:
    """Odd-child G=1 odd-j consecutive Green from parent bits G(m,r+1), G(m,r+2)."""
    g1 = G(m, r + 1)
    g2 = G(m, r + 2)
    return (g2 ^ g1, g1, g1 ^ 1, 1)


def identity() -> dict:
    """m<M_HI: odd-child G=1 odd-j cons Green equals (g2 xor g1, g1, g1 xor 1, 1)."""
    n_ok = n1011 = n0011 = n1101 = n0101 = n_and = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(1, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            r = j // 2
            if G(m, r) != 1:
                return {"ok": False, "g": True, "m": m, "j": j}
            got = cons_g4(n, j)
            want = odd_g1_oddj_cons(m, r)
            if got != want:
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            fires = got in AND_ONES or and_from_tuple(*got) or and_clause(*got)
            if fires:
                if got != T0011:
                    return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
                n_and += 1
            if got == T1011:
                n1011 += 1
            elif got == T0011:
                n0011 += 1
            elif got == T1101:
                n1101 += 1
            elif got == T0101:
                n0101 += 1
            else:
                return {"ok": False, "pair": True, "m": m, "j": j, "got": list(got)}
    ok = (
        n_ok == n1011 + n0011 + n1101 + n0101
        and n_ok == 1344
        and n1011 == 460
        and n0011 == 372
        and n1101 == 371
        and n0101 == 141
        and n_and == 372
        and n_and == n0011
        and odd_g1_oddj_cons(0, 0) == T0011
        and odd_g1_oddj_cons(2, 0) == T1011
        and odd_g1_oddj_cons(1, 1) == T1101
        and odd_g1_oddj_cons(1, 0) == T0101
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n1011": n1011,
        "n0011": n0011,
        "n1101": n1101,
        "n0101": n0101,
        "n_and": n_and,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering odd n, odd j, G=1 cons Green matches odd_g1_oddj_cons."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n1011 = n0011 = n1101 = n0101 = n_and = 0
        for n in range(1, 4 * U, 2):
            m = n // 2
            for j in range(1, 2 * n + 1, 2):
                if G(n, j) != 1:
                    continue
                r = j // 2
                got = cons_g4(n, j)
                if got != odd_g1_oddj_cons(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if got in AND_ONES or and_clause(*got):
                    if got != T0011:
                        return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                    n_and += 1
                if got == T1011:
                    n1011 += 1
                elif got == T0011:
                    n0011 += 1
                elif got == T1101:
                    n1101 += 1
                elif got == T0101:
                    n0101 += 1
                else:
                    return {"ok": False, "pair": True, "k": k, "n": n, "j": j}
        n_ok += 1
        rows[str(k)] = {
            "n_cell": n_cell,
            "n1011": n1011,
            "n0011": n0011,
            "n1101": n1101,
            "n0101": n0101,
            "n_and": n_and,
        }
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["0"]["n0011"] == 2
        and rows["0"]["n1011"] == 0
        and rows["5"]["n_cell"] == 1344
        and rows["5"]["n0011"] == 372
        and rows["8"]["n_cell"] > 0
        and rows["8"]["n1011"] != rows["8"]["n1101"]
        and rows["8"]["n_and"] == rows["8"]["n0011"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """(0,0,1,1) is AND_ONES; the other three types are not; not SB/SC."""
    t0011 = odd_g1_oddj_cons(0, 0)
    t1011 = odd_g1_oddj_cons(2, 0)
    t1101 = odd_g1_oddj_cons(1, 1)
    t0101 = odd_g1_oddj_cons(1, 0)
    ok = (
        t0011 == T0011
        and t1011 == T1011
        and t1101 == T1101
        and t0101 == T0101
        and T0011 in AND_ONES
        and and_from_tuple(*T0011) == 1
        and and_clause(*T0011) == 1
        and all(t not in AND_ONES for t in (T1011, T1101, T0101))
        and all(and_from_tuple(*t) == 0 for t in (T1011, T1101, T0101))
        and t0011 != odd_g1_oddj_green4(0, 0)
        and odd_g1_oddj_green4(0, 0) == (1, 0, 1, 0)
        and t0011 != odd_g1_evenj_cons(0, 0)
        and green4(1, 1) == (1, 0, 1, 0)
        and cons_g4(1, 1) == T0011
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Never AND; identically one tuple; equals SB/SC; type counts equal."""
    ident = identity()
    g4 = green4(1, 1)
    ok = (
        T0011 in AND_ONES
        and T1011 != T0011
        and T1101 != T0101
        and ident["ok"]
        and ident["n_and"] > 0
        and ident["n1011"] != ident["n1101"]
        and ident["n0011"] != ident["n0101"]
        and cons_g4(1, 1) != odd_g1_oddj_green4(0, 0)
        and cons_g4(1, 1) != odd_g1_evenj_cons(0, 0)
        and g4 not in AND_ONES
        and and_from_tuple(*g4) == 0
    )
    return {
        "ok": ok,
        "n1011": ident["n1011"],
        "n0011": ident["n0011"],
        "n1101": ident["n1101"],
        "n0101": ident["n0101"],
        "n_and": ident["n_and"],
    }


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    sb = json.loads(SB_JSON.read_text())
    sc = json.loads(SC_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and sb["checks"]["all_ok"]
        and sc["checks"]["all_ok"]
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hs["verdict"]["AND_of_green4_identically_0"] == "LEMMA"
        and sb["verdict"]["odd_g1_oddj_green4_eq_g1x_g1_1_gm"] == "LEMMA"
        and sb["verdict"]["odd_g1_oddj_green4_never_AND"] == "LEMMA"
        and sc["verdict"]["odd_g1_evenj_cons_eq_g1_g1xg_g_1"] == "LEMMA"
        and sc["verdict"]["odd_g1_evenj_cons_never_AND"] == "LEMMA"
        and sb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sc["verdict"]["prize"] == "unsolved"
        and odd_g1_oddj_cons(0, 0) == T0011
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
        "cycle": "SD",
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
            "odd_g1_oddj_cons_eq_g2xg1_g1_g1x_1": True,
            "odd_g1_oddj_cons_meets_AND_ONES": True,
            "odd_g1_oddj_cons_AND_iff_0011": True,
            "odd_g1_oddj_cons_never_AND": False,
            "odd_g1_oddj_cons_eq_one_tuple": False,
            "odd_g1_oddj_cons_eq_SB": False,
            "odd_g1_oddj_cons_eq_SC": False,
            "odd_g1_oddj_cons_type_counts_eq": False,
            "odd_g1_oddj_cons_AND_implies_green4_AND": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_g1_oddj_cons_eq_g2xg1_g1_g1x_1": "LEMMA",
            "odd_g1_oddj_cons_meets_AND_ONES": "LEMMA",
            "odd_g1_oddj_cons_AND_iff_0011": "LEMMA",
            "odd_g1_oddj_cons_never_AND": "KILLED",
            "odd_g1_oddj_cons_eq_one_tuple": "KILLED",
            "odd_g1_oddj_cons_eq_SB": "KILLED",
            "odd_g1_oddj_cons_eq_SC": "KILLED",
            "odd_g1_oddj_cons_type_counts_eq": "KILLED",
            "odd_g1_oddj_cons_AND_implies_green4_AND": "KILLED",
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
        "n0011",
        dump["identity"]["n0011"],
        "n_and",
        dump["identity"]["n_and"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
