#!/usr/bin/env python3
"""Cycle QS: covering UNIQUE_EVEN packed AND xor on even n is 1 iff k==3 or k>=5.

Cycle QQ gave even tot 1 for k>=6. Packed covering k<=8 matches 1 iff
k==3 or k>=5 (k=4 even tot 0, odd tot 1). Odd tot is 1 iff k==4 or
k>=6, and they xor to Cycle QP unique even packed tot. Leftover
even-n tot is even rest xor this bit for every k (Cycle QR unique
odd even-n tot is 0), not this bit itself (k=0: leftover even-n=1,
unique even-n=0) and not ST (k=8: leftover even-n=0, ST=1). Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qs.py --certify
Dump: research/cycle_qs.json
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
from cycle_pb import want_rest_e0
from cycle_qj import UNIQUE_EVEN
from cycle_qp import want_unique_even_pack
from cycle_qq import even_n_par, want_unique_even_n
from cycle_qr import want_uo_even
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QR_JSON = Path(__file__).resolve().parent / "cycle_qr.json"
QQ_JSON = Path(__file__).resolve().parent / "cycle_qq.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_G = 12
K_ALG = 64


def want_ue_even(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on even n, all k: 1 iff k==3 or k>=5."""
    return int(k == 3 or k >= 5)


def want_ue_odd(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on odd n, all k: 1 iff k==4 or k>=6."""
    return int(k == 4 or k >= 6)


def even_n_split() -> dict:
    """k=6..K_G: QQ even tot 1 equals want_ue_even; odd tot equals want_ue_odd."""
    n_ok = 0
    rows = {}
    for k in range(6, K_G + 1):
        w = even_n_par(k)
        if w["e"] != 1 or w["o"] != 1:
            return {"ok": False, "par": True, "k": k, "w": w}
        if w["e"] != want_ue_even(k) or w["o"] != want_ue_odd(k):
            return {"ok": False, "want": True, "k": k}
        if w["e"] != want_unique_even_n(k):
            return {"ok": False, "qq": True, "k": k}
        if (w["e"] ^ w["o"]) != want_unique_even_pack(k):
            return {"ok": False, "qp": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"e": w["e"], "o": w["o"], "n0": w["n0"], "n2": w["n2"]}
    ok = (
        n_ok == K_G - 5
        and rows["6"]["e"] == 1
        and rows["12"]["e"] == 1
        and rows["6"]["o"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: even tot 1 iff k==3 or k>=5; odd tot 1 iff k==4 or k>=6."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_ue_even(k) != int(k == 3 or k >= 5):
            return {"ok": False, "e": True, "k": k}
        if want_ue_odd(k) != int(k == 4 or k >= 6):
            return {"ok": False, "o": True, "k": k}
        if (want_ue_even(k) ^ want_ue_odd(k)) != want_unique_even_pack(k):
            return {"ok": False, "xor": True, "k": k}
        if k >= 6 and want_ue_even(k) != want_unique_even_n(k):
            return {"ok": False, "qq": True, "k": k}
        if want_uo_even(k) != 0:
            return {"ok": False, "qr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ue_even(3) == 1
        and want_ue_even(4) == 0
        and want_ue_even(5) == 1
        and want_ue_even(6) == 1
        and want_ue_odd(4) == 1
        and want_ue_odd(5) == 0
        and want_ue_odd(6) == 1
        and want_unique_even_pack(4) == 1
        and want_unique_even_n(4) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _thin_ue(k: int) -> dict:
    """Covering packed UNIQUE_EVEN AND xor split by n parity."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    e = o = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            even = n % 2 == 0
            for p in UNIQUE_EVEN:
                j = (T - p) // 2
                if j < 0 or j > 2 * n:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                if not and_clause(*four):
                    continue
                if even:
                    e ^= 1
                else:
                    o ^= 1
        row = rule30_step(row)
        s += 1
    return {"e": e, "o": o}


def thin_pack() -> dict:
    """k<=K_THIN: packed UNIQUE_EVEN even tot is 1 iff k==3 or k>=5."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        w = _thin_ue(k)
        if w["e"] != want_ue_even(k):
            return {"ok": False, "e": True, "k": k, "w": w}
        if w["o"] != want_ue_odd(k):
            return {"ok": False, "o": True, "k": k, "w": w}
        if (w["e"] ^ w["o"]) != want_unique_even_pack(k):
            return {"ok": False, "xor": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {"e": w["e"], "o": w["o"]}
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["e"] == 0
        and rows["3"]["e"] == 1
        and rows["3"]["o"] == 0
        and rows["4"]["e"] == 0
        and rows["4"]["o"] == 1
        and rows["5"]["e"] == 1
        and rows["5"]["o"] == 0
        and rows["6"]["e"] == 1
        and rows["8"]["e"] == 1
        and len(UNIQUE_EVEN) == 7
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_lo_even_n() -> dict:
    """Leftover even-n tot equals unique even-n tot, and equals ST."""
    qo = json.loads(QO_JSON.read_text())
    r0 = qo["rest_n0_walk"]["rows"]["0"]
    r8 = qo["rest_n0_walk"]["rows"]["8"]
    even0 = r0["tot"][0] ^ r0["tot"][2]
    even8 = r8["tot"][0] ^ r8["tot"][2]
    lo0 = even0 ^ want_ue_even(0) ^ want_uo_even(0)
    lo8 = even8 ^ want_ue_even(8) ^ want_uo_even(8)
    ok = (
        even0 == 1
        and lo0 == 1
        and want_ue_even(0) == 0
        and lo0 != want_ue_even(0)
        and even8 == 1
        and lo8 == 0
        and want_ue_even(8) == 1
        and want_rest_e0(8) == 1
        and lo8 != want_rest_e0(8)
    )
    return {"ok": ok, "lo0": lo0, "lo8": lo8, "ue0": 0, "st8": 1}


def prefixes() -> dict:
    qr = json.loads(QR_JSON.read_text())
    qq = json.loads(QQ_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qr["checks"]["all_ok"]
        and qq["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qr["verdict"]["unique_odd_even_n_0"] == "LEMMA"
        and qq["verdict"]["unique_even_n_k_ge_6"] == "LEMMA"
        and qr["verdict"]["lo_en_eq_ST"] == "KILLED"
        and qr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qr["verdict"]["prize"] == "unsolved"
        and want_ue_even(3) == 1
        and want_unique_even_n(6) == 1
        and want_uo_even(6) == 0
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
    kl = killed_lo_even_n()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, thin, kl, sc, pref)
    dump = {
        "cycle": "QS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_n_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "thin_pack": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_n_iff_k_eq_3_or_ge_5": True,
            "unique_even_odd_n_iff_k_eq_4_or_ge_6": True,
            "lo_en_eq_ue_even": False,
            "lo_en_eq_ST": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_n_iff_k_eq_3_or_ge_5": "LEMMA",
            "unique_even_odd_n_iff_k_eq_4_or_ge_6": "LEMMA",
            "lo_en_eq_ue_even": "KILLED",
            "lo_en_eq_ST": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
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
        "k6_e",
        dump["even_n_split"]["rows"]["6"]["e"],
        "k12_e",
        dump["even_n_split"]["rows"]["12"]["e"],
    )
    print(
        "thin_pack n_ok",
        dump["thin_pack"]["n_ok"],
        "k3_e",
        dump["thin_pack"]["rows"]["3"]["e"],
        "k4_e",
        dump["thin_pack"]["rows"]["4"]["e"],
        "k5_e",
        dump["thin_pack"]["rows"]["5"]["e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
