#!/usr/bin/env python3
"""Cycle QP: covering UNIQUE_EVEN packed AND xor tot is 1 iff k in {3,4,5}.

Xor of the seven UNIQUE_EVEN packed formulas (p=16,32,52,60,72,76,88)
is 1 iff k in {3,4,5}: five ones at k=3, three at k=4 and k=5, four
for every k>=6. UNIQUE_ODD packed tot equals the same bit, and they
xor to Cycle QF's unique tot 0. The closed form equals Cycle QG's
Green UNIQUE_REST tot, not Cycle QJ's Green unique even tot (k=4:
packed even=1, Green even=0). Leftover even-n tot is even-n rest xor
this bit, so leftover even-n equals even-n rest except at k=3,4,5.
Not rest=S xor T (k=3: unique even packed=1, rest=0). Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qp.py --certify
Dump: research/cycle_qp.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qf import PACK, want_unique_tot
from cycle_qg import want_unique_gxor_tot_closed
from cycle_qj import UNIQUE_EVEN, UNIQUE_ODD, want_unique_even
from cycle_qn import want_unique_pack_n0

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QF_JSON = Path(__file__).resolve().parent / "cycle_qf.json"
QG_JSON = Path(__file__).resolve().parent / "cycle_qg.json"
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_unique_even_pack(k: int) -> int:
    """UNIQUE_EVEN packed AND xor tot, all k: 1 iff k in {3,4,5}."""
    return int(k in (3, 4, 5))


def want_unique_odd_pack(k: int) -> int:
    """UNIQUE_ODD packed AND xor tot, all k: 1 iff k in {3,4,5}."""
    return int(k in (3, 4, 5))


def pack_parity(k: int) -> tuple[int, int]:
    """Xor PACK formulas split by p%4."""
    e = o = 0
    for p, fn in PACK.items():
        bit = fn(k)
        if p % 4 == 0:
            e ^= bit
        else:
            o ^= bit
    return e, o


def tot_form() -> dict:
    """k<=K_ALG: packed unique even/odd tot is 1 iff k in {3,4,5}."""
    n_ok = 0
    rows = {}
    for k in range(0, K_ALG + 1):
        e, o = pack_parity(k)
        if e != want_unique_even_pack(k) or o != want_unique_odd_pack(k):
            return {"ok": False, "k": k, "e": e, "o": o}
        if (e ^ o) != want_unique_tot(k) or e ^ o != 0:
            return {"ok": False, "qf": True, "k": k, "e": e, "o": o}
        if e != want_unique_gxor_tot_closed(k):
            return {"ok": False, "qg": True, "k": k, "e": e}
        if k >= 6 and e != 0:
            return {"ok": False, "ge6": True, "k": k}
        if k >= 6 and want_unique_pack_n0(k) != 1:
            return {"ok": False, "n0": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12, 16):
            rows[str(k)] = {"e": e, "o": o, "g_even": want_unique_even(k)}
    ok = (
        n_ok == K_ALG + 1
        and rows["2"]["e"] == 0
        and rows["3"]["e"] == 1
        and rows["4"]["e"] == 1
        and rows["4"]["g_even"] == 0
        and rows["5"]["e"] == 1
        and rows["6"]["e"] == 0
        and rows["6"]["g_even"] == 1
        and rows["12"]["e"] == 0
        and rows["16"]["e"] == 0
        and set(UNIQUE_EVEN) == {p for p in PACK if p % 4 == 0}
        and set(UNIQUE_ODD) == {p for p in PACK if p % 4 == 2}
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def killed_eq_green_even() -> dict:
    """Packed unique even tot equals Green unique even tot / ST / rest."""
    ok = (
        want_unique_even_pack(4) == 1
        and want_unique_even(4) == 0
        and want_unique_even_pack(6) == 0
        and want_unique_even(6) == 1
        and want_unique_even_pack(3) == 1
        and want_rest_e0(3) == 0
        and want_rest10(3, 10) == 0
        and want_unique_even_pack(5) == 1
        and want_rest_e0(5) == 0
    )
    return {"ok": ok, "k4_pack": 1, "k4_green": 0, "k3_ST": 0}


def prefixes() -> dict:
    qo = json.loads(QO_JSON.read_text())
    qf = json.loads(QF_JSON.read_text())
    qg = json.loads(QG_JSON.read_text())
    qj = json.loads(QJ_JSON.read_text())
    ok = (
        qo["checks"]["all_ok"]
        and qf["checks"]["all_ok"]
        and qg["checks"]["all_ok"]
        and qj["checks"]["all_ok"]
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and qf["verdict"]["unique_tot_0_all_k"] == "LEMMA"
        and qg["verdict"]["unique_gxor_tot_iff_k_in_3_4_5"] == "LEMMA"
        and qj["verdict"]["unique_even_iff_k3_or_ge6"] == "LEMMA"
        and qf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qf["verdict"]["prize"] == "unsolved"
        and want_unique_gxor_tot_closed(4) == 1
        and want_unique_even(4) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"]
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
    kl = killed_eq_green_even()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, kl, sc, pref)
    dump = {
        "cycle": "QP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_pack_iff_k_in_3_4_5": True,
            "unique_odd_pack_iff_k_in_3_4_5": True,
            "unique_even_pack_eq_green_even": False,
            "unique_even_pack_eq_ST": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_pack_iff_k_in_3_4_5": "LEMMA",
            "unique_odd_pack_iff_k_in_3_4_5": "LEMMA",
            "unique_even_pack_eq_green_even": "KILLED",
            "unique_even_pack_eq_ST": "KILLED",
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
        "tot_form n_ok",
        dump["tot_form"]["n_ok"],
        "k3",
        dump["tot_form"]["rows"]["3"]["e"],
        "k4",
        dump["tot_form"]["rows"]["4"]["e"],
        "k6",
        dump["tot_form"]["rows"]["6"]["e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
