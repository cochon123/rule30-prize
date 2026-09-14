#!/usr/bin/env python3
"""Cycle QZ: covering UNIQUE_ODD packed AND xor on n%4==3 is 1 for k>=2.

UNIQUE_ODD lives only on odd n (Cycle QR even tot 0). Cycle QR freeze
for k>=6 has n%4==1 equal to p=54 (xor 1) and n%4==3 equal to
p=42 xor p=58 xor p=98 xor p=106 xor p=114 (xor 1); silent
p=30,38,86 tot is 0. Packed covering k<=8 matches n3 tot 1 iff
k>=2 and n1 tot 1 iff k==2 or k>=6, including the k=2..5 gap
where freeze n%4 labels are not yet packed-AND locations. They
xor to Cycle QP unique odd packed tot. Not n3 tot equals unique
odd tot (k=2: 1 vs 0). Not Green n%4==3 rest equals this bit
(k=0: Green 1 vs 0). Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qz.py --certify
Dump: research/cycle_qz.json
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
from cycle_pn import want_p38_pack
from cycle_pm import want_p30_pack
from cycle_pr import want_p42_pack
from cycle_ps import want_p54_pack
from cycle_pv import want_p58_pack
from cycle_qa import want_p86_pack
from cycle_qc import want_p98_pack
from cycle_qd import want_p106_pack
from cycle_qe import want_p114_pack
from cycle_qj import UNIQUE_ODD
from cycle_qp import want_unique_odd_pack
from cycle_qr import odd_n_par, want_uo_even, want_uo_odd
from cycle_qs import want_ue_odd
from cycle_qx import want_g_n3
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QR_JSON = Path(__file__).resolve().parent / "cycle_qr.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_G = 12
K_ALG = 64


def want_uo_n3(k: int) -> int:
    """UNIQUE_ODD packed AND xor on n%4==3, all k: 1 iff k>=2."""
    return int(k >= 2)


def want_uo_n1(k: int) -> int:
    """UNIQUE_ODD packed AND xor on n%4==1, all k: 1 iff k==2 or k>=6."""
    return int(k == 2 or k >= 6)


def n3_freeze_pack(k: int) -> int:
    """Pack-helper xor of UNIQUE_ODD columns that freeze on n%4==3."""
    return (
        want_p42_pack(k)
        ^ want_p58_pack(k)
        ^ want_p98_pack(k)
        ^ want_p106_pack(k)
        ^ want_p114_pack(k)
    )


def silent_odd_pack(k: int) -> int:
    return want_p30_pack(k) ^ want_p38_pack(k) ^ want_p86_pack(k)


def odd_n_split() -> dict:
    """k=6..K_G: Green freeze n1 and n3 each 1; even tot 0."""
    n_ok = 0
    rows = {}
    for k in range(6, K_G + 1):
        w = odd_n_par(k)
        if w["e"] != 0 or w["n1"] != 1 or w["n3"] != 1:
            return {"ok": False, "par": True, "k": k, "w": w}
        if w["n1"] != want_uo_n1(k) or w["n3"] != want_uo_n3(k):
            return {"ok": False, "want": True, "k": k}
        if w["n1"] != want_p54_pack(k) or w["n3"] != n3_freeze_pack(k):
            return {"ok": False, "pack": True, "k": k}
        if (w["n1"] ^ w["n3"]) != want_uo_odd(k):
            return {"ok": False, "xor": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"e": w["e"], "n1": w["n1"], "n3": w["n3"]}
    ok = (
        n_ok == K_G - 5
        and rows["6"]["n3"] == 1
        and rows["6"]["n1"] == 1
        and rows["12"]["n3"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: n3 iff k>=2; n1 iff k==2 or k>=6; freeze pack for k>=6."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_uo_n3(k) != int(k >= 2):
            return {"ok": False, "n3": True, "k": k}
        if want_uo_n1(k) != int(k == 2 or k >= 6):
            return {"ok": False, "n1": True, "k": k}
        if want_uo_even(k) != 0:
            return {"ok": False, "e": True, "k": k}
        if (want_uo_n1(k) ^ want_uo_n3(k)) != want_uo_odd(k):
            return {"ok": False, "xor": True, "k": k}
        if (want_uo_n1(k) ^ want_uo_n3(k)) != want_unique_odd_pack(k):
            return {"ok": False, "qp": True, "k": k}
        if k < 2 and (
            want_p30_pack(k)
            | want_p38_pack(k)
            | want_p86_pack(k)
            | want_p42_pack(k)
            | want_p54_pack(k)
            | want_p58_pack(k)
            | want_p98_pack(k)
            | want_p106_pack(k)
            | want_p114_pack(k)
        ):
            return {"ok": False, "early": True, "k": k}
        if k >= 6:
            if silent_odd_pack(k) != 0:
                return {"ok": False, "silent": True, "k": k}
            if want_p54_pack(k) != 1 or n3_freeze_pack(k) != 1:
                return {"ok": False, "slices": True, "k": k}
            if want_p54_pack(k) != want_uo_n1(k):
                return {"ok": False, "n1pack": True, "k": k}
            if n3_freeze_pack(k) != want_uo_n3(k):
                return {"ok": False, "n3pack": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_uo_n3(0) == 0
        and want_uo_n3(2) == 1
        and want_uo_n1(2) == 1
        and want_uo_n1(3) == 0
        and want_uo_n1(5) == 0
        and want_uo_n1(6) == 1
        and want_uo_odd(3) == 1
        and want_uo_odd(6) == 0
        and n3_freeze_pack(6) == 1
        and want_p106_pack(6) == 0
        and want_p114_pack(6) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _thin_uo(k: int) -> dict:
    """Covering packed UNIQUE_ODD AND xor split by n%4."""
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
            for p in UNIQUE_ODD:
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
    """k<=K_THIN: packed UNIQUE_ODD n3 tot 1 iff k>=2; n1 iff k==2 or k>=6."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        w = _thin_uo(k)
        tot = w["tot"]
        if tot[0] != 0 or tot[2] != 0:
            return {"ok": False, "even": True, "k": k, "tot": tot}
        if tot[1] != want_uo_n1(k) or tot[3] != want_uo_n3(k):
            return {"ok": False, "odd": True, "k": k, "tot": tot}
        if (tot[1] ^ tot[3]) != want_uo_odd(k):
            return {"ok": False, "xor": True, "k": k, "tot": tot}
        n_ok += 1
        rows[str(k)] = {"tot": tot}
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["tot"] == [0, 0, 0, 0]
        and rows["1"]["tot"] == [0, 0, 0, 0]
        and rows["2"]["tot"] == [0, 1, 0, 1]
        and rows["3"]["tot"] == [0, 0, 0, 1]
        and rows["4"]["tot"] == [0, 0, 0, 1]
        and rows["5"]["tot"] == [0, 0, 0, 1]
        and rows["6"]["tot"] == [0, 1, 0, 1]
        and rows["8"]["tot"] == [0, 1, 0, 1]
        and len(UNIQUE_ODD) == 9
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_eq() -> dict:
    """UNIQUE_ODD n3 tot equals unique odd tot, Green n3, leftover odd-n."""
    qo = json.loads(QO_JSON.read_text())
    r0 = qo["rest_n0_walk"]["rows"]["0"]
    r6 = qo["rest_n0_walk"]["rows"]["6"]
    odd0 = r0["tot"][1] ^ r0["tot"][3]
    odd6 = r6["tot"][1] ^ r6["tot"][3]
    lo0 = odd0 ^ want_ue_odd(0) ^ want_uo_odd(0)
    lo6 = odd6 ^ want_ue_odd(6) ^ want_uo_odd(6)
    ok = (
        want_uo_n3(2) == 1
        and want_unique_odd_pack(2) == 0
        and want_uo_n3(6) == 1
        and want_unique_odd_pack(6) == 0
        and want_g_n3(0) == 1
        and want_uo_n3(0) == 0
        and lo0 == 1
        and lo0 != want_uo_n3(0)
        and lo6 == 0
        and lo6 != want_uo_n3(6)
        and want_ue_odd(6) == 1
        and want_uo_odd(6) == 0
    )
    return {
        "ok": ok,
        "n3_2": 1,
        "pack_2": 0,
        "g0": 1,
        "uo0": 0,
        "lo0": lo0,
        "lo6": lo6,
    }


def prefixes() -> dict:
    qr = json.loads(QR_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qr["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qr["verdict"]["unique_odd_even_n_0"] == "LEMMA"
        and qr["verdict"]["unique_odd_odd_n_iff_k_in_3_4_5"] == "LEMMA"
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and qy["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and qr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qr["verdict"]["prize"] == "unsolved"
        and want_uo_n3(2) == 1
        and want_uo_odd(3) == 1
        and want_g_n3(10) == 1
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
    split = odd_n_split()
    tot = tot_form()
    thin = thin_pack()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, thin, kl, sc, pref)
    dump = {
        "cycle": "QZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "odd_n_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "thin_pack": {k: thin[k] for k in thin if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_odd_n3_iff_k_ge_2": True,
            "unique_odd_n1_iff_k_eq_2_or_ge_6": True,
            "unique_odd_n3_eq_pack": False,
            "green_n3_eq_uo_n3": False,
            "lo_on_eq_uo_n3": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_odd_n3_iff_k_ge_2": "LEMMA",
            "unique_odd_n1_iff_k_eq_2_or_ge_6": "LEMMA",
            "unique_odd_n3_eq_pack": "KILLED",
            "green_n3_eq_uo_n3": "KILLED",
            "lo_on_eq_uo_n3": "KILLED",
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
        "odd_n_split n_ok",
        dump["odd_n_split"]["n_ok"],
        "k6_n3",
        dump["odd_n_split"]["rows"]["6"]["n3"],
        "k12_n3",
        dump["odd_n_split"]["rows"]["12"]["n3"],
    )
    print(
        "thin_pack n_ok",
        dump["thin_pack"]["n_ok"],
        "k2",
        dump["thin_pack"]["rows"]["2"]["tot"],
        "k5",
        dump["thin_pack"]["rows"]["5"]["tot"],
        "k8",
        dump["thin_pack"]["rows"]["8"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
