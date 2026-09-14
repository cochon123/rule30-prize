#!/usr/bin/env python3
"""Cycle RY: even-child green4 is (0, G(m,r), G(m,r), G(m,r)) at even j.

Cycle HJ green4(n,j)=(G(n,j+1), G(n,j+1)^G(n,j), G(n,j),
G(n,j)^G(n,j-1)) is the even-s Green 4-tuple at packed p-3..p.
Cycle QV G(2m,2r)=G(m,r) and G(2m,odd)=0, so at even child n=2m
and even j=2r that 4-tuple equals (0, G(m,r), G(m,r), G(m,r)).
On G=1 it is (0,1,1,1), never in AND_ONES. At odd j=2r+1 it equals
(G(m,r+1), G(m,r+1), 0, G(m,r)), also never in AND_ONES, so Green
AND is dead on every even-child cell. Packed AND at consecutive-p
can still fire (Cycle QV mismatch). Cycle RX consecutive Green is
(0, G(m,r+1), 0, G(m,r)), not this 4-tuple. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ry.py --certify
Dump: research/cycle_ry.json
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
from cycle_rx import even_child_g4

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
RX_JSON = Path(__file__).resolve().parent / "cycle_rx.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8


def even_child_green4(m: int, r: int) -> tuple[int, int, int, int]:
    """green4 at even child n=2m, even j=2r."""
    g = G(m, r)
    return (0, g, g, g)


def even_child_green4_oddj(m: int, r: int) -> tuple[int, int, int, int]:
    """green4 at even child n=2m, odd j=2r+1."""
    gp = G(m, r + 1)
    return (gp, gp, 0, G(m, r))


def identity() -> dict:
    """m<M_HI: even-child green4 matches even_child_green4 / oddj; never AND."""
    n_ok = n_g1 = n_dead = 0
    for m in range(0, M_HI):
        n = 2 * m
        for j in range(0, 2 * n + 1):
            got = green4(n, j)
            r = j // 2
            want = even_child_green4(m, r) if j % 2 == 0 else even_child_green4_oddj(m, r)
            if got != want:
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            if got in AND_ONES or and_from_tuple(*got) or and_clause(*got):
                return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
            n_dead += 1
            if G(n, j) == 1:
                if got != (0, 1, 1, 1) or j % 2 != 0:
                    return {"ok": False, "g1": True, "m": m, "j": j, "got": list(got)}
                n_g1 += 1
    ok = (
        n_ok == n_dead
        and n_ok == 8128
        and n_g1 == 1344
        and even_child_green4(0, 0) == (0, 1, 1, 1)
        and even_child_green4(1, 0) == (0, 1, 1, 1)
        and even_child_green4_oddj(2, 0) == (0, 0, 0, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_dead": n_dead, "m_hi": M_HI}


def covering_chk() -> dict:
    """k<=8: covering even n, green4 matches even_child_green4 / oddj."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n_g1 = 0
        for n in range(0, 4 * U, 2):
            m = n // 2
            for j in range(0, 2 * n + 1):
                got = green4(n, j)
                r = j // 2
                want = (
                    even_child_green4(m, r) if j % 2 == 0 else even_child_green4_oddj(m, r)
                )
                if got != want:
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if G(n, j) == 1:
                    if got != (0, 1, 1, 1) or got in AND_ONES or and_clause(*got):
                        return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                    n_g1 += 1
        n_ok += 1
        rows[str(k)] = {"n_cell": n_cell, "n_g1": n_g1}
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_g1"] >= 1
        and rows["8"]["n_cell"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """(0,1,1,1) and the four odd-j green4 patterns are outside AND_ONES."""
    oddj = (
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (1, 1, 0, 0),
        (1, 1, 0, 1),
    )
    ok = (
        (0, 1, 1, 1) not in AND_ONES
        and and_from_tuple(0, 1, 1, 1) == 0
        and and_clause(0, 1, 1, 1) == 0
        and all(t not in AND_ONES for t in oddj)
        and all(and_from_tuple(*t) == 0 for t in oddj)
        and even_child_green4(0, 0) != even_child_g4(0, 0)
        and even_child_green4(1, 0) != green4(1, 0)
        and even_child_green4(0, 0) == (0, 1, 1, 1)
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Even-child green4 equals parent green4; equals RX consecutive Green."""
    e00 = even_child_green4(0, 0)
    e10 = even_child_green4(1, 0)
    ok = (
        e00 == (0, 1, 1, 1)
        and e00 != even_child_g4(0, 0)
        and even_child_g4(0, 0) == (0, 0, 0, 1)
        and e10 != green4(1, 0)
        and green4(1, 0) == (1, 0, 1, 1)
        and e10 == (0, 1, 1, 1)
        and even_child_green4_oddj(2, 0) == (0, 0, 0, 1)
    )
    return {"ok": ok}


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    rx = json.loads(RX_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and rx["checks"]["all_ok"]
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hs["verdict"]["AND_of_green4_identically_0"] == "LEMMA"
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and rx["verdict"]["even_child_cons_g4_eq_0_Gmrp1_0_Gmr"] == "LEMMA"
        and rx["verdict"]["even_child_cons_g4_eq_parent_green4"] == "KILLED"
        and rx["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rx["verdict"]["prize"] == "unsolved"
        and even_child_green4(0, 0) == (0, 1, 1, 1)
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
        "cycle": "RY",
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
            "even_child_green4_eq_0_G_G_G": True,
            "even_child_green4_never_AND": True,
            "even_child_g1_green4_eq_0111": True,
            "even_child_green4_eq_parent_green4": False,
            "even_child_green4_eq_rx_cons": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_child_green4_eq_0_G_G_G": "LEMMA",
            "even_child_green4_never_AND": "LEMMA",
            "even_child_g1_green4_eq_0111": "LEMMA",
            "even_child_green4_eq_parent_green4": "KILLED",
            "even_child_green4_eq_rx_cons": "KILLED",
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
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
