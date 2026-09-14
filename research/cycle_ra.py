#!/usr/bin/env python3
"""Cycle RA: covering UNIQUE_EVEN packed AND xor on n%4==2 is 0 for every k.

Cycle QQ freeze for k>=6 has n%4==0 tot 1 and n%4==2 tot 0, so even
tot equals n0 tot. Packed covering k<=8 has n2 tot 0 at every k,
including k=3,5 where even tot is 1. Hence n0 tot equals Cycle QS
even tot (1 iff k==3 or k>=5). Odd freeze helpers all require
n%4==1, so for k>=6 n1 tot is 1 and n3 tot is 0. Packed k<=8 matches
n1 tot 1 iff k>=2 and n3 tot 1 iff k in {2,3,5}. They xor to Cycle
QS odd tot. Not n3 tot equals odd tot (k=2: 1 vs 0). Not n2 tot
equals even tot (k=3: 0 vs 1). Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ra.py --certify
Dump: research/cycle_ra.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_ph import in_p16_even
from cycle_pk import in_p32_n1
from cycle_pw import in_p52_n1, in_p52_n2
from cycle_px import in_p60_n1, in_p60_n2
from cycle_py import in_p72_n2
from cycle_pz import in_p76_n1
from cycle_qb import in_p88_n1, in_p88_n2
from cycle_qj import UNIQUE_EVEN
from cycle_qp import want_unique_even_pack
from cycle_qs import want_ue_even, want_ue_odd
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QS_JSON = Path(__file__).resolve().parent / "cycle_qs.json"
QQ_JSON = Path(__file__).resolve().parent / "cycle_qq.json"
QZ_JSON = Path(__file__).resolve().parent / "cycle_qz.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_G = 12
K_ALG = 64


def want_ue_n0(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on n%4==0, all k: 1 iff k==3 or k>=5."""
    return want_ue_even(k)


def want_ue_n2(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on n%4==2, all k: 0."""
    return 0


def want_ue_n1(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on n%4==1, all k: 1 iff k>=2."""
    return int(k >= 2)


def want_ue_n3(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on n%4==3, all k: 1 iff k in {2,3,5}."""
    return int(k in (2, 3, 5))


def even_nmod(k: int) -> dict:
    """Green freeze UNIQUE_EVEN xor split by n%4."""
    U = 1 << k
    tot = [0, 0, 0, 0]
    for n in range(0, 4 * U):
        acc = 0
        if in_p16_even(n, k):
            acc ^= 1
        if in_p32_n1(n, k):
            acc ^= 1
        if in_p52_n1(n, k):
            acc ^= 1
        if in_p52_n2(n, k):
            acc ^= 1
        if in_p60_n1(n, k):
            acc ^= 1
        if in_p60_n2(n, k):
            acc ^= 1
        if in_p72_n2(n, k):
            acc ^= 1
        if in_p76_n1(n, k):
            acc ^= 1
        if in_p88_n1(n, k):
            acc ^= 1
        if in_p88_n2(n, k):
            acc ^= 1
        if acc:
            tot[n % 4] ^= acc
    return {"tot": tot}


def even_n_split() -> dict:
    """k=6..K_G: freeze n%4 is (1,1,0,0)."""
    n_ok = 0
    rows = {}
    for k in range(6, K_G + 1):
        tot = even_nmod(k)["tot"]
        if tot != [1, 1, 0, 0]:
            return {"ok": False, "par": True, "k": k, "tot": tot}
        if tot[0] != want_ue_n0(k) or tot[2] != want_ue_n2(k):
            return {"ok": False, "even": True, "k": k}
        if tot[1] != want_ue_n1(k) or tot[3] != want_ue_n3(k):
            return {"ok": False, "odd": True, "k": k}
        if (tot[0] ^ tot[2]) != want_ue_even(k):
            return {"ok": False, "uee": True, "k": k}
        if (tot[1] ^ tot[3]) != want_ue_odd(k):
            return {"ok": False, "ueo": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"tot": tot}
    ok = (
        n_ok == K_G - 5
        and rows["6"]["tot"] == [1, 1, 0, 0]
        and rows["12"]["tot"] == [1, 1, 0, 0]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: n2=0; n0 iff k==3 or k>=5; n1 iff k>=2; n3 iff k in {2,3,5}."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_ue_n2(k) != 0:
            return {"ok": False, "n2": True, "k": k}
        if want_ue_n0(k) != want_ue_even(k):
            return {"ok": False, "n0": True, "k": k}
        if want_ue_n1(k) != int(k >= 2):
            return {"ok": False, "n1": True, "k": k}
        if want_ue_n3(k) != int(k in (2, 3, 5)):
            return {"ok": False, "n3": True, "k": k}
        if (want_ue_n0(k) ^ want_ue_n2(k)) != want_ue_even(k):
            return {"ok": False, "ee": True, "k": k}
        if (want_ue_n1(k) ^ want_ue_n3(k)) != want_ue_odd(k):
            return {"ok": False, "oo": True, "k": k}
        if (want_ue_even(k) ^ want_ue_odd(k)) != want_unique_even_pack(k):
            return {"ok": False, "qp": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ue_n0(3) == 1
        and want_ue_n0(4) == 0
        and want_ue_n0(5) == 1
        and want_ue_n2(3) == 0
        and want_ue_n1(2) == 1
        and want_ue_n1(1) == 0
        and want_ue_n3(2) == 1
        and want_ue_n3(4) == 0
        and want_ue_n3(5) == 1
        and want_ue_n3(6) == 0
        and want_ue_odd(4) == 1
        and want_ue_odd(5) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _thin_ue(k: int) -> dict:
    """Covering packed UNIQUE_EVEN AND xor split by n%4."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    tot = [0, 0, 0, 0]
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for p in UNIQUE_EVEN:
                j = (T - p) // 2
                if j < 0 or j > 2 * n:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                if not and_clause(*four):
                    continue
                tot[n % 4] ^= 1
        row = rule30_step(row)
        s += 1
    return {"tot": tot}


def thin_pack() -> dict:
    """k<=K_THIN: packed UNIQUE_EVEN n2 tot 0; n0/n1/n3 match closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        tot = _thin_ue(k)["tot"]
        if tot[2] != 0 or tot[2] != want_ue_n2(k):
            return {"ok": False, "n2": True, "k": k, "tot": tot}
        if tot[0] != want_ue_n0(k):
            return {"ok": False, "n0": True, "k": k, "tot": tot}
        if tot[1] != want_ue_n1(k) or tot[3] != want_ue_n3(k):
            return {"ok": False, "odd": True, "k": k, "tot": tot}
        if (tot[1] ^ tot[3]) != want_ue_odd(k):
            return {"ok": False, "xor": True, "k": k, "tot": tot}
        n_ok += 1
        rows[str(k)] = {"tot": tot}
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["tot"] == [0, 0, 0, 0]
        and rows["2"]["tot"] == [0, 1, 0, 1]
        and rows["3"]["tot"] == [1, 1, 0, 1]
        and rows["4"]["tot"] == [0, 1, 0, 0]
        and rows["5"]["tot"] == [1, 1, 0, 1]
        and rows["6"]["tot"] == [1, 1, 0, 0]
        and rows["8"]["tot"] == [1, 1, 0, 0]
        and len(UNIQUE_EVEN) == 7
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_eq() -> dict:
    """UNIQUE_EVEN n3 tot equals odd tot; n2 tot equals even tot."""
    ok = (
        want_ue_n3(2) == 1
        and want_ue_odd(2) == 0
        and want_ue_n3(6) == 0
        and want_ue_odd(6) == 1
        and want_ue_n2(3) == 0
        and want_ue_even(3) == 1
        and want_ue_n0(3) == 1
    )
    return {"ok": ok, "n3_2": 1, "o2": 0, "n3_6": 0, "o6": 1, "n2_3": 0, "e3": 1}


def prefixes() -> dict:
    qs = json.loads(QS_JSON.read_text())
    qq = json.loads(QQ_JSON.read_text())
    qz = json.loads(QZ_JSON.read_text())
    ok = (
        qs["checks"]["all_ok"]
        and qq["checks"]["all_ok"]
        and qz["checks"]["all_ok"]
        and qs["verdict"]["unique_even_n_iff_k_eq_3_or_ge_5"] == "LEMMA"
        and qs["verdict"]["unique_even_odd_n_iff_k_eq_4_or_ge_6"] == "LEMMA"
        and qz["verdict"]["unique_odd_n3_iff_k_ge_2"] == "LEMMA"
        and qq["verdict"]["unique_even_n_k_ge_6"] == "LEMMA"
        and qs["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qs["verdict"]["prize"] == "unsolved"
        and want_ue_n2(6) == 0
        and want_ue_n1(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, split, tot, thin, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and split["ok"] and tot["ok"]
    assert thin["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    split = even_n_split()
    tot = tot_form()
    thin = thin_pack()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, thin, kl, sc, pref)
    dump = {
        "cycle": "RA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_n_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "thin_pack": {k: thin[k] for k in thin if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_n2_0": True,
            "unique_even_n0_iff_k_eq_3_or_ge_5": True,
            "unique_even_n1_iff_k_ge_2": True,
            "unique_even_n3_iff_k_in_2_3_5": True,
            "unique_even_n3_eq_ue_odd": False,
            "unique_even_n2_eq_ue_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_n2_0": "LEMMA",
            "unique_even_n0_iff_k_eq_3_or_ge_5": "LEMMA",
            "unique_even_n1_iff_k_ge_2": "LEMMA",
            "unique_even_n3_iff_k_in_2_3_5": "LEMMA",
            "unique_even_n3_eq_ue_odd": "KILLED",
            "unique_even_n2_eq_ue_even": "KILLED",
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
        "even_n_split n_ok",
        dump["even_n_split"]["n_ok"],
        "k6",
        dump["even_n_split"]["rows"]["6"]["tot"],
        "k12",
        dump["even_n_split"]["rows"]["12"]["tot"],
    )
    print(
        "thin_pack n_ok",
        dump["thin_pack"]["n_ok"],
        "k3",
        dump["thin_pack"]["rows"]["3"]["tot"],
        "k5",
        dump["thin_pack"]["rows"]["5"]["tot"],
        "k8",
        dump["thin_pack"]["rows"]["8"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
