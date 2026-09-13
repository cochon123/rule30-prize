#!/usr/bin/env python3
"""Cycle QQ: covering UNIQUE_EVEN packed AND xor on even n is 1 for k>=6.

For k>=6 freeze AND at UNIQUE_EVEN splits: p=16 even tot is 1 (Cycle
QN n%4==0), p=32 and p=76 are n%4==1, p=88 even slice cancels, p=72
tot is 0. p=52 and p=60 have tot 0 but both n%4 in {1,2} fire, each
slice equal to Green p=14 and p=16 at k-2 (xor 1). Even tot is
p=16 xor p=52 n2 xor p=60 n2 = 1. Odd tot is the same bit, and they
cancel to Cycle QP unique even packed tot 0. Leftover even-n tot is
even-n rest xor this bit, not even-n rest xor unique even packed tot
(k=6: unique even-n=1, unique even packed tot=0, even rest=0). Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qq.py --certify
Dump: research/cycle_qq.json
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
from cycle_pc import want_p14_gxor
from cycle_ph import in_p16_even
from cycle_pk import in_p32_n1, want_p32_pack
from cycle_pv import want_p16_gxor
from cycle_pw import in_p52_n1, in_p52_n2
from cycle_px import in_p60_n1, in_p60_n2
from cycle_py import in_p72_n2, want_p72_pack
from cycle_pz import in_p76_n1, want_p76_pack
from cycle_qa import want_p22_gxor, want_p24_gxor
from cycle_qb import in_p88_n1, in_p88_n2
from cycle_qn import want_p16_n0, want_p16_n2, want_unique_pack_n0
from cycle_qp import want_unique_even_pack

OUT = Path(__file__).resolve().with_suffix(".json")
QP_JSON = Path(__file__).resolve().parent / "cycle_qp.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QN_JSON = Path(__file__).resolve().parent / "cycle_qn.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_ALG = 64


def want_unique_even_n(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on even n, k>=6: 1."""
    return int(k >= 6)


def want_unique_odd_n(k: int) -> int:
    """UNIQUE_EVEN packed AND xor on odd n, k>=6: 1."""
    return int(k >= 6)


def even_n_par(k: int) -> dict:
    """Green freeze UNIQUE_EVEN xor split by n parity / n%4."""
    U = 1 << k
    e = o = n0 = n2 = 0
    p16e = p52e = p60e = p72e = p88e = 0
    p32o = p52o = p60o = p76o = p88o = 0
    for n in range(0, 4 * U):
        acc = 0
        if in_p16_even(n, k):
            acc ^= 1
            if n % 2 == 0:
                p16e ^= 1
        if in_p32_n1(n, k):
            acc ^= 1
            p32o ^= 1
        if in_p52_n1(n, k):
            acc ^= 1
            p52o ^= 1
        if in_p52_n2(n, k):
            acc ^= 1
            p52e ^= 1
        if in_p60_n1(n, k):
            acc ^= 1
            p60o ^= 1
        if in_p60_n2(n, k):
            acc ^= 1
            p60e ^= 1
        if in_p72_n2(n, k):
            acc ^= 1
            p72e ^= 1
        if in_p76_n1(n, k):
            acc ^= 1
            p76o ^= 1
        if in_p88_n1(n, k):
            acc ^= 1
            p88o ^= 1
        if in_p88_n2(n, k):
            acc ^= 1
            p88e ^= 1
        if not acc:
            continue
        if n % 2:
            o ^= acc
        else:
            e ^= acc
            if n % 4 == 0:
                n0 ^= acc
            else:
                n2 ^= acc
    return {
        "e": e,
        "o": o,
        "n0": n0,
        "n2": n2,
        "p16e": p16e,
        "p52e": p52e,
        "p60e": p60e,
        "p72e": p72e,
        "p88e": p88e,
        "p32o": p32o,
        "p52o": p52o,
        "p60o": p60o,
        "p76o": p76o,
        "p88o": p88o,
    }


def even_n_split() -> dict:
    """k=6..K_G: unique even-n tot is 1; n2 tot 0; odd tot 1."""
    n_ok = 0
    rows = {}
    for k in range(6, K_G + 1):
        w = even_n_par(k)
        if w["e"] != 1 or w["o"] != 1 or w["n0"] != 1 or w["n2"] != 0:
            return {"ok": False, "par": True, "k": k, "w": w}
        if w["p16e"] != 1 or w["p52e"] != 1 or w["p60e"] != 1:
            return {"ok": False, "cols": True, "k": k, "w": w}
        if w["p72e"] != 0 or w["p88e"] != 0:
            return {"ok": False, "silent": True, "k": k, "w": w}
        if w["e"] != want_unique_even_n(k) or w["o"] != want_unique_odd_n(k):
            return {"ok": False, "want": True, "k": k}
        if (w["e"] ^ w["o"]) != want_unique_even_pack(k):
            return {"ok": False, "qp": True, "k": k}
        if w["n0"] != want_unique_pack_n0(k) or w["n0"] != want_p16_n0(k):
            return {"ok": False, "n0": True, "k": k}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {
                "e": w["e"],
                "o": w["o"],
                "n0": w["n0"],
                "n2": w["n2"],
                "p16e": w["p16e"],
                "p52e": w["p52e"],
                "p60e": w["p60e"],
            }
    ok = (
        n_ok == K_G - 5
        and rows["6"]["e"] == 1
        and rows["6"]["o"] == 1
        and rows["8"]["n2"] == 0
        and rows["12"]["e"] == 1
        and rows["12"]["p52e"] == 1
        and rows["12"]["p60e"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: even-n tot 1 for k>=6 via p=16 xor p=14 xor p=16 parents."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_unique_even_n(k) != int(k >= 6):
            return {"ok": False, "e": True, "k": k}
        if want_unique_odd_n(k) != int(k >= 6):
            return {"ok": False, "o": True, "k": k}
        if k >= 6:
            even = (
                want_p16_n0(k)
                ^ want_p16_n2(k)
                ^ want_p14_gxor(k - 2)
                ^ want_p16_gxor(k - 2)
                ^ want_p72_pack(k)
            )
            # p=88 even slice is parent p=22 xor p=24, which cancel.
            even ^= want_p22_gxor(k - 2) ^ want_p24_gxor(k - 2)
            if even != 1 or even != want_unique_even_n(k):
                return {"ok": False, "even": True, "k": k, "even": even}
            odd = (
                want_p32_pack(k)
                ^ want_p14_gxor(k - 2)
                ^ want_p16_gxor(k - 2)
                ^ want_p76_pack(k)
                ^ want_p22_gxor(k - 2)
            )
            if odd != 1 or odd != want_unique_odd_n(k):
                return {"ok": False, "odd": True, "k": k, "odd": odd}
            if (even ^ odd) != want_unique_even_pack(k):
                return {"ok": False, "xor": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_unique_even_n(6) == 1
        and want_unique_even_n(5) == 0
        and want_p14_gxor(4) == 1
        and want_p16_gxor(4) == 1
        and want_p16_n0(6) == 1
        and want_p72_pack(6) == 0
        and want_p22_gxor(4) == 1
        and want_p24_gxor(4) == 1
        and want_unique_even_pack(6) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_lo_even_n() -> dict:
    """Leftover even-n tot equals even rest xor unique even packed tot."""
    qo = json.loads(QO_JSON.read_text())
    r6 = qo["rest_n0_walk"]["rows"]["6"]
    even6 = r6["tot"][0] ^ r6["tot"][2]
    ok = (
        even6 == 0
        and want_unique_even_n(6) == 1
        and want_unique_even_pack(6) == 0
        and want_rest_e0(6) == 1
        and want_rest10(6, 10) == 1
        and want_unique_even_n(8) == 1
        and want_unique_even_pack(8) == 0
    )
    return {"ok": ok, "even6": even6, "ue_n6": 1, "ue_pack6": 0}


def prefixes() -> dict:
    qp = json.loads(QP_JSON.read_text())
    qn = json.loads(QN_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    ok = (
        qp["checks"]["all_ok"]
        and qn["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qp["verdict"]["unique_even_pack_iff_k_in_3_4_5"] == "LEMMA"
        and qn["verdict"]["unique_pack_n0_k_ge_6"] == "LEMMA"
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and qp["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qp["verdict"]["prize"] == "unsolved"
        and want_unique_even_pack(3) == 1
        and want_p16_n0(6) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, split, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and split["ok"] and tot["ok"]
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
    split = even_n_split()
    tot = tot_form()
    kl = killed_lo_even_n()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, kl, sc, pref)
    dump = {
        "cycle": "QQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_n_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_n_k_ge_6": True,
            "unique_odd_n_k_ge_6": True,
            "lo_en_eq_erest_xor_ue_pack": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_n_k_ge_6": "LEMMA",
            "unique_odd_n_k_ge_6": "LEMMA",
            "lo_en_eq_erest_xor_ue_pack": "KILLED",
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
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
