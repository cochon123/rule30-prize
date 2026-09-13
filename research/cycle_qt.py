#!/usr/bin/env python3
"""Cycle QT: leftover even-n tot is even rest xor UNIQUE_EVEN even-n tot.

Partition of even-n rest into unique vs leftover, Cycle QR unique odd
even-n tot 0, and Cycle QS UNIQUE_EVEN even-n tot (1 iff k==3 or k>=5)
give leftover even-n tot = even rest xor UNIQUE_EVEN even-n tot for
every k. Equivalently leftover even-n equals even rest except when
k==3 or k>=5, where it flips. Leftover odd-n tot is odd rest xor
UNIQUE_EVEN odd-n xor UNIQUE_ODD odd-n. Not leftover even-n equals
even rest (k=3: leftover=1, even rest=0). Not leftover even-n equals
ST (k=8: leftover=0, ST=1). Not leftover even-n equals unique even-n
(k=0: leftover=1, unique=0). Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qt.py --certify
Dump: research/cycle_qt.json
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
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qr import want_uo_even, want_uo_odd
from cycle_qs import want_ue_even, want_ue_odd
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QS_JSON = Path(__file__).resolve().parent / "cycle_qs.json"
QR_JSON = Path(__file__).resolve().parent / "cycle_qr.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_ALG = 64


def want_lo_en(k: int, even_rest: int) -> int:
    """Leftover even-n tot from even rest and UNIQUE_EVEN even-n tot."""
    return even_rest ^ want_ue_even(k) ^ want_uo_even(k)


def want_lo_on(k: int, odd_rest: int) -> int:
    """Leftover odd-n tot from odd rest and unique odd-n tot."""
    return odd_rest ^ want_ue_odd(k) ^ want_uo_odd(k)


def tot_form() -> dict:
    """k<=K_ALG: unique even-n xor unique odd-n tot is 0; QR even tot 0."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_uo_even(k) != 0:
            return {"ok": False, "qr": True, "k": k}
        u_even = want_ue_even(k) ^ want_uo_even(k)
        u_odd = want_ue_odd(k) ^ want_uo_odd(k)
        if (u_even ^ u_odd) != 0:
            return {"ok": False, "unique": True, "k": k, "u_even": u_even, "u_odd": u_odd}
        if u_even != want_ue_even(k):
            return {"ok": False, "ue": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ue_even(3) == 1
        and want_ue_even(4) == 0
        and want_ue_even(5) == 1
        and want_uo_even(6) == 0
        and want_ue_odd(4) == 1
        and want_uo_odd(3) == 1
        and want_lo_en(3, 0) == 1
        and want_lo_en(4, 0) == 0
        and want_lo_en(8, 1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _walk_par(k: int) -> dict:
    """Covering packed rest/leftover xor split by n parity."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    rest_e = rest_o = lo_e = lo_o = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            even = n % 2 == 0
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                if not and_clause(*four) or p in FORCED:
                    continue
                if even:
                    rest_e ^= 1
                    if p not in UNIQUE_REST:
                        lo_e ^= 1
                else:
                    rest_o ^= 1
                    if p not in UNIQUE_REST:
                        lo_o ^= 1
        row = rule30_step(row)
        s += 1
    return {"rest_e": rest_e, "rest_o": rest_o, "lo_e": lo_e, "lo_o": lo_o}


def thin_pack() -> dict:
    """k<=K_THIN: leftover even-n tot is even rest xor UNIQUE_EVEN even-n tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        w = _walk_par(k)
        if (w["rest_e"] ^ w["rest_o"]) != want_rest10(k, 10):
            return {"ok": False, "rest": True, "k": k, "w": w}
        if (w["rest_e"] ^ w["rest_o"]) != want_rest_e0(k):
            return {"ok": False, "st": True, "k": k, "w": w}
        if w["lo_e"] != want_lo_en(k, w["rest_e"]):
            return {"ok": False, "lo_e": True, "k": k, "w": w}
        if w["lo_o"] != want_lo_on(k, w["rest_o"]):
            return {"ok": False, "lo_o": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {
            "rest_e": w["rest_e"],
            "rest_o": w["rest_o"],
            "lo_e": w["lo_e"],
            "lo_o": w["lo_o"],
        }
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["lo_e"] == 1
        and rows["0"]["rest_e"] == 1
        and rows["3"]["lo_e"] == 1
        and rows["3"]["rest_e"] == 0
        and rows["4"]["lo_e"] == 0
        and rows["5"]["lo_e"] == 1
        and rows["6"]["lo_e"] == 1
        and rows["8"]["lo_e"] == 0
        and rows["8"]["rest_e"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_lo_even_n() -> dict:
    """Leftover even-n tot equals even rest, ST, or unique even-n tot."""
    qo = json.loads(QO_JSON.read_text())
    r0 = qo["rest_n0_walk"]["rows"]["0"]
    r3 = qo["rest_n0_walk"]["rows"]["3"]
    r8 = qo["rest_n0_walk"]["rows"]["8"]
    even0 = r0["tot"][0] ^ r0["tot"][2]
    even3 = r3["tot"][0] ^ r3["tot"][2]
    even8 = r8["tot"][0] ^ r8["tot"][2]
    lo0 = want_lo_en(0, even0)
    lo3 = want_lo_en(3, even3)
    lo8 = want_lo_en(8, even8)
    ok = (
        even0 == 1
        and lo0 == 1
        and want_ue_even(0) == 0
        and lo0 != want_ue_even(0)
        and even3 == 0
        and lo3 == 1
        and lo3 != even3
        and even8 == 1
        and lo8 == 0
        and want_rest_e0(8) == 1
        and lo8 != want_rest_e0(8)
    )
    return {"ok": ok, "lo0": lo0, "lo3": lo3, "lo8": lo8}


def prefixes() -> dict:
    qs = json.loads(QS_JSON.read_text())
    qr = json.loads(QR_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qs["checks"]["all_ok"]
        and qr["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qs["verdict"]["unique_even_n_iff_k_eq_3_or_ge_5"] == "LEMMA"
        and qr["verdict"]["unique_odd_even_n_0"] == "LEMMA"
        and qs["verdict"]["lo_en_eq_ST"] == "KILLED"
        and qs["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qs["verdict"]["prize"] == "unsolved"
        and want_ue_even(3) == 1
        and want_uo_even(6) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, thin, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and thin["ok"]
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
    tot = tot_form()
    thin = thin_pack()
    kl = killed_lo_even_n()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, thin, kl, sc, pref)
    dump = {
        "cycle": "QT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "thin_pack": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_en_eq_erest_xor_ue_even": True,
            "lo_on_eq_orest_xor_unique_odd_n": True,
            "lo_en_eq_erest": False,
            "lo_en_eq_ST": False,
            "lo_en_eq_ue_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_en_eq_erest_xor_ue_even": "LEMMA",
            "lo_on_eq_orest_xor_unique_odd_n": "LEMMA",
            "lo_en_eq_erest": "KILLED",
            "lo_en_eq_ST": "KILLED",
            "lo_en_eq_ue_even": "KILLED",
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
        "thin_pack n_ok",
        dump["thin_pack"]["n_ok"],
        "k3_lo_e",
        dump["thin_pack"]["rows"]["3"]["lo_e"],
        "k8_lo_e",
        dump["thin_pack"]["rows"]["8"]["lo_e"],
        "k8_rest_e",
        dump["thin_pack"]["rows"]["8"]["rest_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
