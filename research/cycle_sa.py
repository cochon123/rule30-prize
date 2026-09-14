#!/usr/bin/env python3
"""Cycle SA: odd-child G=1 even-j green4 is (g, g xor 1, 1, g).

Cycle RZ odd-child green4 at even j=2r is (G(m,r), G(m,r-1),
G(m,r)^G(m,r-1), G(m,r)). On G=1, G(2m+1,2r)=G(m,r)^G(m,r-1)=1,
so G(m,r-1)=G(m,r)^1 and the 4-tuple equals (g, g^1, 1, g) with
g=G(m,r): (1,0,1,1) if g=1, else (0,1,1,0). Neither is in
AND_ONES, and (1,0,1,1) is Cycle HS DIE 1011. Cycle RY even-child
G=1 green4 is the single tuple (0,1,1,1), not this pair. Palindrome G(n,j)=G(n,2n-j) pairs the two types on every
full row, so unclipped covering counts are equal. Clipped
counts are not equal (k=0 is 2 vs 1). Packed AND at
consecutive-p can still fire (Cycle QV mismatch). Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sa.py --certify
Dump: research/cycle_sa.json
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
from cycle_ry import even_child_green4
from cycle_rz import odd_child_green4

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
RY_JSON = Path(__file__).resolve().parent / "cycle_ry.json"
RZ_JSON = Path(__file__).resolve().parent / "cycle_rz.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8


def odd_g1_green4(m: int, r: int) -> tuple[int, int, int, int]:
    """Odd-child G=1 even-j green4 from parent bit g=G(m,r)."""
    g = G(m, r)
    return (g, g ^ 1, 1, g)


def identity() -> dict:
    """m<M_HI: odd-child G=1 even-j green4 equals (g, g xor 1, 1, g)."""
    n_ok = n_1011 = n_0110 = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(0, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            r = j // 2
            got = green4(n, j)
            want = odd_g1_green4(m, r)
            if got != want or got != odd_child_green4(m, r):
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            if got in AND_ONES or and_from_tuple(*got) or and_clause(*got):
                return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            if got == (1, 0, 1, 1):
                n_1011 += 1
            elif got == (0, 1, 1, 0):
                n_0110 += 1
            else:
                return {"ok": False, "pair": True, "m": m, "j": j, "got": list(got)}
    ok = (
        n_ok == n_1011 + n_0110
        and n_ok == 1664
        and n_1011 == 832
        and n_0110 == 832
        and odd_g1_green4(0, 0) == (1, 0, 1, 1)
        and odd_g1_green4(2, 1) == (0, 1, 1, 0)
        and G(0, 0) == 1
        and G(2, 1) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_1011": n_1011,
        "n_0110": n_0110,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering odd n, even j, G=1 green4 matches odd_g1_green4."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n_1011 = n_0110 = 0
        for n in range(1, 4 * U, 2):
            m = n // 2
            for j in range(0, 2 * n + 1, 2):
                if G(n, j) != 1:
                    continue
                r = j // 2
                got = green4(n, j)
                if got != odd_g1_green4(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                if got in AND_ONES or and_clause(*got):
                    return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if got == (1, 0, 1, 1):
                    n_1011 += 1
                else:
                    n_0110 += 1
        n_ok += 1
        rows[str(k)] = {"n_cell": n_cell, "n_1011": n_1011, "n_0110": n_0110}
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["0"]["n_1011"] == rows["0"]["n_0110"]
        and rows["1"]["n_1011"] == rows["1"]["n_0110"]
        and rows["5"]["n_cell"] == 1664
        and rows["8"]["n_1011"] == rows["8"]["n_0110"]
        and rows["8"]["n_cell"] > 0
        and all(
            rows[str(k)]["n_1011"] == rows[str(k)]["n_0110"]
            for k in range(0, K_COV + 1)
        )
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def tot_form() -> dict:
    """(g, g xor 1, 1, g) is outside AND_ONES; not even-child (0,1,1,1)."""
    t1 = odd_g1_green4(0, 0)
    t0 = odd_g1_green4(2, 1)
    ok = (
        t1 == (1, 0, 1, 1)
        and t0 == (0, 1, 1, 0)
        and t1 not in AND_ONES
        and t0 not in AND_ONES
        and and_from_tuple(*t1) == 0
        and and_from_tuple(*t0) == 0
        and t1 != even_child_green4(0, 0)
        and even_child_green4(0, 0) == (0, 1, 1, 1)
        and t1 != (0, 1, 1, 1)
        and t0 != (0, 1, 1, 1)
        and t1 != t0
    )
    return {"ok": ok}


def pal_pair() -> dict:
    """On G=1 even j, palindrome partner has complementary g."""
    n_ok = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(0, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            jp = 2 * n - j
            if jp % 2 != 0 or G(n, jp) != 1:
                return {"ok": False, "pal": True, "m": m, "j": j}
            r = j // 2
            rp = jp // 2
            g = G(m, r)
            if G(m, rp) != G(m, r - 1) or G(m, rp) != (g ^ 1):
                return {"ok": False, "g": True, "m": m, "j": j}
            if odd_g1_green4(m, r) == odd_g1_green4(m, rp):
                return {"ok": False, "type": True, "m": m, "j": j}
            n_ok += 1
    ok = n_ok == 1664
    return {"ok": ok, "n_ok": n_ok}


def clip_split() -> dict:
    """k=0 clipped j<=5U: 1011 and 0110 counts differ (2 vs 1)."""
    U = 1
    clip = 5 * U
    n_1011 = n_0110 = 0
    for n in range(1, 4 * U, 2):
        m = n // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) != 1:
                continue
            got = green4(n, j)
            if got == (1, 0, 1, 1):
                n_1011 += 1
            elif got == (0, 1, 1, 0):
                n_0110 += 1
    ok = n_1011 == 2 and n_0110 == 1
    return {"ok": ok, "n_1011": n_1011, "n_0110": n_0110}


def killed_eq() -> dict:
    """Identically (0,1,1,1) / (1,0,1,1) / (0,1,1,0); clipped split equal."""
    t1 = odd_g1_green4(0, 0)
    t0 = odd_g1_green4(2, 1)
    clip = clip_split()
    ok = (
        t1 == (1, 0, 1, 1)
        and t0 == (0, 1, 1, 0)
        and t1 != (0, 1, 1, 1)
        and t0 != (0, 1, 1, 1)
        and t1 != t0
        and green4(1, 0) == t1
        and green4(5, 2) == t0
        and G(1, 0) == 1
        and G(5, 2) == 1
        and clip["ok"]
        and clip["n_1011"] != clip["n_0110"]
    )
    return {
        "ok": ok,
        "clip_n_1011": clip["n_1011"],
        "clip_n_0110": clip["n_0110"],
    }


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    ry = json.loads(RY_JSON.read_text())
    rz = json.loads(RZ_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and ry["checks"]["all_ok"]
        and rz["checks"]["all_ok"]
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hs["verdict"]["AND_of_green4_identically_0"] == "LEMMA"
        and ry["verdict"]["even_child_g1_green4_eq_0111"] == "LEMMA"
        and rz["verdict"]["odd_child_green4_eq_G_Gm_xor_G"] == "LEMMA"
        and rz["verdict"]["odd_child_green4_eq_parent_green4"] == "KILLED"
        and rz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rz["verdict"]["prize"] == "unsolved"
        and odd_g1_green4(0, 0) == (1, 0, 1, 1)
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, ident, cov, pair, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert ident["ok"] and cov["ok"] and pair["ok"] and tot["ok"]
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
    pair = pal_pair()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, ident, cov, pair, tot, kl, sc, pref)
    dump = {
        "cycle": "SA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "identity": {k: ident[k] for k in ident if k != "ok"},
        "covering_chk": {k: cov[k] for k in cov if k != "ok"},
        "pal_pair": {k: pair[k] for k in pair if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_g1_evenj_green4_eq_g_g1_1_g": True,
            "odd_g1_evenj_green4_never_AND": True,
            "odd_g1_evenj_pal_pairs_types": True,
            "odd_g1_evenj_unclip_split_eq": True,
            "odd_g1_evenj_green4_eq_0111": False,
            "odd_g1_evenj_green4_eq_1011": False,
            "odd_g1_evenj_green4_eq_0110": False,
            "odd_g1_evenj_clip_split_eq": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_g1_evenj_green4_eq_g_g1_1_g": "LEMMA",
            "odd_g1_evenj_green4_never_AND": "LEMMA",
            "odd_g1_evenj_pal_pairs_types": "LEMMA",
            "odd_g1_evenj_unclip_split_eq": "LEMMA",
            "odd_g1_evenj_green4_eq_0111": "KILLED",
            "odd_g1_evenj_green4_eq_1011": "KILLED",
            "odd_g1_evenj_green4_eq_0110": "KILLED",
            "odd_g1_evenj_clip_split_eq": "KILLED",
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
        "n_1011",
        dump["identity"]["n_1011"],
        "n_0110",
        dump["identity"]["n_0110"],
        "pal n_ok",
        dump["pal_pair"]["n_ok"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
