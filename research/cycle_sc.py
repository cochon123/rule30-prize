#!/usr/bin/env python3
"""Cycle SC: odd-child G=1 even-j consecutive Green is (g1, g1 xor g, g, 1).

Cycle HJ odd-child consecutive Green equals parent green4:
cons_g4(2m+1, 2r) = green4(m,r). On G=1, G(2m+1,2r)=1 so the last
bit is 1 and the 4-tuple equals (g1, g1^g, g, 1) with g=G(m,r) and
g1=G(m,r+1): one of (0,1,1,1), (1,1,0,1), (0,0,0,1), (1,0,1,1).
None is in AND_ONES (last-bit-1 members 0011 and 1001 contradict
g1^g vs g). Cycle RX even-child G=1 consecutive is (0,x,0,1), not
this 4-tuple. Cycle SA even-j green4 is not this 4-tuple. Type
counts are not equal. Palindrome of consecutive 4-tuples is not
reverse. Packed AND at consecutive-p can still fire (Cycle QV
mismatch). Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_sc.py --certify
Dump: research/cycle_sc.json
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
from cycle_rx import cons_g4, even_child_g4
from cycle_sa import odd_g1_green4

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
RX_JSON = Path(__file__).resolve().parent / "cycle_rx.json"
SA_JSON = Path(__file__).resolve().parent / "cycle_sa.json"
SB_JSON = Path(__file__).resolve().parent / "cycle_sb.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8

T0111 = (0, 1, 1, 1)
T1101 = (1, 1, 0, 1)
T0001 = (0, 0, 0, 1)
T1011 = (1, 0, 1, 1)


def odd_g1_evenj_cons(m: int, r: int) -> tuple[int, int, int, int]:
    """Odd-child G=1 even-j consecutive Green from parent bits G(m,r+1), G(m,r)."""
    g = G(m, r)
    g1 = G(m, r + 1)
    return (g1, g1 ^ g, g, 1)


def identity() -> dict:
    """m<M_HI: odd-child G=1 even-j cons Green equals (g1, g1 xor g, g, 1)."""
    n_ok = n0111 = n1101 = n0001 = n1011 = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(0, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            r = j // 2
            got = cons_g4(n, j)
            want = odd_g1_evenj_cons(m, r)
            if got != want or got != green4(m, r):
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            if got[-1] != 1:
                return {"ok": False, "last": True, "m": m, "j": j, "got": list(got)}
            if got in AND_ONES or and_from_tuple(*got) or and_clause(*got):
                return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            if got == T0111:
                n0111 += 1
            elif got == T1101:
                n1101 += 1
            elif got == T0001:
                n0001 += 1
            elif got == T1011:
                n1011 += 1
            else:
                return {"ok": False, "pair": True, "m": m, "j": j, "got": list(got)}
    ok = (
        n_ok == n0111 + n1101 + n0001 + n1011
        and n_ok == 1664
        and n0111 == 461
        and n1101 == 460
        and n0001 == 372
        and n1011 == 371
        and odd_g1_evenj_cons(0, 0) == T0111
        and odd_g1_evenj_cons(2, 1) == T1101
        and odd_g1_evenj_cons(0, 1) == T0001
        and odd_g1_evenj_cons(1, 0) == T1011
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n0111": n0111,
        "n1101": n1101,
        "n0001": n0001,
        "n1011": n1011,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering odd n, even j, G=1 cons Green matches odd_g1_evenj_cons."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n0111 = n1101 = n0001 = n1011 = 0
        for n in range(1, 4 * U, 2):
            m = n // 2
            for j in range(0, 2 * n + 1, 2):
                if G(n, j) != 1:
                    continue
                r = j // 2
                got = cons_g4(n, j)
                if got != odd_g1_evenj_cons(m, r) or got != green4(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                if got in AND_ONES or and_clause(*got):
                    return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if got == T0111:
                    n0111 += 1
                elif got == T1101:
                    n1101 += 1
                elif got == T0001:
                    n0001 += 1
                elif got == T1011:
                    n1011 += 1
                else:
                    return {"ok": False, "pair": True, "k": k, "n": n, "j": j}
        n_ok += 1
        rows[str(k)] = {
            "n_cell": n_cell,
            "n0111": n0111,
            "n1101": n1101,
            "n0001": n0001,
            "n1011": n1011,
        }
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["0"]["n1101"] == 0
        and rows["5"]["n_cell"] == 1664
        and rows["5"]["n0111"] == 461
        and rows["8"]["n_cell"] > 0
        and rows["8"]["n0111"] != rows["8"]["n1101"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """Four even-j G=1 cons tuples sit outside AND_ONES; not RX or SA."""
    t0111 = odd_g1_evenj_cons(0, 0)
    t1101 = odd_g1_evenj_cons(2, 1)
    t0001 = odd_g1_evenj_cons(0, 1)
    t1011 = odd_g1_evenj_cons(1, 0)
    last1 = ((0, 0, 1, 1), (1, 0, 0, 1))
    ok = (
        t0111 == T0111
        and t1101 == T1101
        and t0001 == T0001
        and t1011 == T1011
        and all(t not in AND_ONES for t in (T0111, T1101, T0001, T1011))
        and all(and_from_tuple(*t) == 0 for t in (T0111, T1101, T0001, T1011))
        and all(u in AND_ONES for u in last1)
        and T0111 != even_child_g4(0, 0)
        and even_child_g4(0, 0) == T0001
        and t0111 != odd_g1_green4(0, 0)
        and odd_g1_green4(0, 0) == T1011
        and t0111 != T1101
        and cons_g4(1, 0) == T0111
        and green4(0, 0) == T0111
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Identically (0,1,1,1); equals RX cons; equals SA green4; type counts equal."""
    ident = identity()
    ok = (
        T0111 != T1101
        and T0111 != T0001
        and T0111 != T1011
        and T0111 != even_child_g4(0, 0)
        and cons_g4(1, 0) != odd_g1_green4(0, 0)
        and even_child_g4(0, 0) == (0, 0, 0, 1)
        and ident["ok"]
        and ident["n0111"] != ident["n1101"]
        and ident["n0001"] != ident["n1011"]
        and green4(1, 0) == T1011
        and cons_g4(1, 0) == T0111
    )
    return {
        "ok": ok,
        "n0111": ident["n0111"],
        "n1101": ident["n1101"],
        "n0001": ident["n0001"],
        "n1011": ident["n1011"],
    }


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    rx = json.loads(RX_JSON.read_text())
    sa = json.loads(SA_JSON.read_text())
    sb = json.loads(SB_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and rx["checks"]["all_ok"]
        and sa["checks"]["all_ok"]
        and sb["checks"]["all_ok"]
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hs["verdict"]["AND_of_green4_identically_0"] == "LEMMA"
        and rx["verdict"]["even_child_cons_g4_eq_0_Gmrp1_0_Gmr"] == "LEMMA"
        and sa["verdict"]["odd_g1_evenj_green4_eq_g_g1_1_g"] == "LEMMA"
        and sb["verdict"]["odd_g1_oddj_green4_eq_g1x_g1_1_gm"] == "LEMMA"
        and rx["verdict"]["even_child_cons_g4_eq_parent_green4"] == "KILLED"
        and sa["verdict"]["odd_g1_evenj_clip_split_eq"] == "KILLED"
        and sb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sb["verdict"]["prize"] == "unsolved"
        and odd_g1_evenj_cons(0, 0) == T0111
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
        "cycle": "SC",
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
            "odd_g1_evenj_cons_eq_g1_g1xg_g_1": True,
            "odd_g1_evenj_cons_never_AND": True,
            "odd_g1_evenj_cons_eq_parent_green4": True,
            "odd_g1_evenj_cons_eq_0111": False,
            "odd_g1_evenj_cons_eq_RX": False,
            "odd_g1_evenj_cons_eq_SA": False,
            "odd_g1_evenj_cons_type_counts_eq": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_g1_evenj_cons_eq_g1_g1xg_g_1": "LEMMA",
            "odd_g1_evenj_cons_never_AND": "LEMMA",
            "odd_g1_evenj_cons_eq_parent_green4": "LEMMA",
            "odd_g1_evenj_cons_eq_0111": "KILLED",
            "odd_g1_evenj_cons_eq_RX": "KILLED",
            "odd_g1_evenj_cons_eq_SA": "KILLED",
            "odd_g1_evenj_cons_type_counts_eq": "KILLED",
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
        "n0111",
        dump["identity"]["n0111"],
        "n1101",
        dump["identity"]["n1101"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
