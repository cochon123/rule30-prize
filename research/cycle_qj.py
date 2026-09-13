#!/usr/bin/env python3
"""Cycle QJ: covering Green leftover even-j / odd-j xor closed forms.

For k>=1, 10U is 0 mod 4, so even j is packed p%4==0. Cycle QI even-j
tot xor Cycle PC p=4 xor Cycle QG UNIQUE_REST even-p tot is leftover
even-j tot. That equals unique even-p tot for k>=2, hence leftover
even-j is 1 iff k<=1 or k==3 or k>=6. Odd-j tot xor p=6 xor p=14 xor
unique odd-p tot is leftover odd-j tot, which is 1 iff k<=1 or k==3.
Xor of the two is Cycle QH leftover tot (1 iff k>=6). Unique even-p
tot is 1 iff k==3 or k>=6; unique odd-p tot is 1 iff k>=4. Not
rest=S xor T (leftover even-j is 1 at k=7). Not leftover even-j tot
equals packed leftover / rest. Not leftover odd-j tot equals unique
odd-p tot. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qj.py --certify
Dump: research/cycle_qj.json
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
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import want_p4_xor, want_p6_gxor, want_p14_gxor
from cycle_qg import PS, want_col_gxor, want_unique_gxor_tot_closed
from cycle_qh import want_clip_g1, want_green_lo
from cycle_qi import want_even_j, want_odd_j

OUT = Path(__file__).resolve().with_suffix(".json")
QI_JSON = Path(__file__).resolve().parent / "cycle_qi.json"
QG_JSON = Path(__file__).resolve().parent / "cycle_qg.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64
UNIQUE_EVEN = tuple(p for p in PS if p % 4 == 0)
UNIQUE_ODD = tuple(p for p in PS if p % 4 == 2)


def want_unique_even(k: int) -> int:
    """UNIQUE_REST Green xor on p%4==0, all k: 1 iff k==3 or k>=6."""
    return int(k == 3 or k >= 6)


def want_unique_odd(k: int) -> int:
    """UNIQUE_REST Green xor on p%4==2, all k: 1 iff k>=4."""
    return int(k >= 4)


def want_lo_even(k: int) -> int:
    """Covering Green leftover even-j xor, all k."""
    return int(k <= 1 or k == 3 or k >= 6)


def want_lo_odd(k: int) -> int:
    """Covering Green leftover odd-j xor, all k."""
    return int(k <= 1 or k == 3)


def unique_parity(k: int) -> tuple[int, int]:
    """Green UNIQUE_REST xor split by packed p%4."""
    e = o = 0
    for p in PS:
        bit = want_col_gxor(p, k)
        if p % 4 == 0:
            e ^= bit
        else:
            o ^= bit
    return e, o


def leftover_walk(k: int) -> dict:
    """Walk covering clipped G=1 xor split leftover / unique / forced by j parity."""
    U = 1 << k
    t_pack = 10 * U
    clip = 5 * U
    le = lo = ue = uo = fe = fo = 0
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = t_pack - 2 * j
            if p < 0:
                continue
            if p in FORCED:
                if j % 2 == 0:
                    fe ^= 1
                else:
                    fo ^= 1
            elif p in UNIQUE_REST:
                if j % 2 == 0:
                    ue ^= 1
                else:
                    uo ^= 1
            else:
                if j % 2 == 0:
                    le ^= 1
                else:
                    lo ^= 1
    return {"lo_e": le, "lo_o": lo, "u_e": ue, "u_o": uo, "f_e": fe, "f_o": fo}


def lo_split() -> dict:
    """k<=K_CHK: leftover even/odd match want_lo_*; partition recovers QI tots."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = leftover_walk(k)
        ue, uo = unique_parity(k)
        if w["lo_e"] != want_lo_even(k) or w["lo_o"] != want_lo_odd(k):
            return {
                "ok": False,
                "lo": True,
                "k": k,
                "lo_e": w["lo_e"],
                "lo_o": w["lo_o"],
            }
        if (w["lo_e"] ^ w["u_e"] ^ w["f_e"]) != want_even_j(k):
            return {"ok": False, "even_j": True, "k": k}
        if (w["lo_o"] ^ w["u_o"] ^ w["f_o"]) != want_odd_j(k):
            return {"ok": False, "odd_j": True, "k": k}
        if (w["lo_e"] ^ w["lo_o"]) != want_green_lo(k):
            return {"ok": False, "qh": True, "k": k}
        if k >= 1 and (w["u_e"] != ue or w["u_o"] != uo):
            return {"ok": False, "uwalk": True, "k": k}
        if k >= 1 and w["f_e"] != want_p4_xor(k):
            return {"ok": False, "p4": True, "k": k}
        if k >= 1 and w["f_o"] != (want_p6_gxor(k) ^ want_p14_gxor(k)):
            return {"ok": False, "p614": True, "k": k}
        if k >= 2 and w["lo_e"] != ue:
            return {"ok": False, "eq_u": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "lo_e": w["lo_e"],
            "lo_o": w["lo_o"],
            "u_e": w["u_e"],
            "u_o": w["u_o"],
            "f_e": w["f_e"],
            "f_o": w["f_o"],
        }
    ok = (
        rows["0"]["lo_e"] == 1
        and rows["0"]["lo_o"] == 1
        and rows["2"]["lo_e"] == 0
        and rows["3"]["lo_e"] == 1
        and rows["3"]["lo_o"] == 1
        and rows["5"]["lo_e"] == 0
        and rows["6"]["lo_e"] == 1
        and rows["6"]["lo_o"] == 0
        and rows["8"]["lo_e"] == 1
        and UNIQUE_EVEN == (16, 32, 52, 60, 72, 76, 88)
        and len(UNIQUE_ODD) == 9
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: unique even/odd and leftover even/odd closed forms."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        ue, uo = unique_parity(k)
        if ue != want_unique_even(k) or uo != want_unique_odd(k):
            return {"ok": False, "unique": True, "k": k, "ue": ue, "uo": uo}
        if (ue ^ uo) != want_unique_gxor_tot_closed(k):
            return {"ok": False, "qg": True, "k": k}
        if (want_lo_even(k) ^ want_lo_odd(k)) != want_green_lo(k):
            return {"ok": False, "qh": True, "k": k}
        if k >= 1:
            lo_e = want_even_j(k) ^ want_unique_even(k) ^ want_p4_xor(k)
            lo_o = (
                want_odd_j(k)
                ^ want_unique_odd(k)
                ^ want_p6_gxor(k)
                ^ want_p14_gxor(k)
            )
            if lo_e != want_lo_even(k) or lo_o != want_lo_odd(k):
                return {"ok": False, "alg": True, "k": k, "lo_e": lo_e, "lo_o": lo_o}
        if k >= 2 and want_lo_even(k) != want_unique_even(k):
            return {"ok": False, "eq": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_unique_even(3) == 1
        and want_unique_even(5) == 0
        and want_unique_odd(3) == 0
        and want_unique_odd(4) == 1
        and want_lo_odd(3) == 1
        and want_lo_odd(4) == 0
        and want_lo_even(7) == 1
        and want_clip_g1(7) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_lo_e_eq_st() -> dict:
    """Leftover even-j tot equals ST / unique odd tot: k=7 is 1 vs 0; k=3 lo_odd=1 unique_odd=0."""
    ok = (
        want_lo_even(7) == 1
        and want_rest_e0(7) == 0
        and want_rest10(7, 10) == 0
        and want_lo_odd(3) == 1
        and want_unique_odd(3) == 0
        and want_lo_odd(4) == 0
        and want_unique_odd(4) == 1
    )
    return {"ok": ok, "k": 7, "lo_e": 1, "ST": 0}


def prefixes() -> dict:
    qi = json.loads(QI_JSON.read_text())
    qg = json.loads(QG_JSON.read_text())
    ok = (
        qi["checks"]["all_ok"]
        and qg["checks"]["all_ok"]
        and qi["verdict"]["even_j_except_k1"] == "LEMMA"
        and qi["verdict"]["p0_gxor_1_all_k"] == "LEMMA"
        and qg["verdict"]["unique_gxor_tot_iff_k_in_3_4_5"] == "LEMMA"
        and qi["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qi["verdict"]["prize"] == "unsolved"
        and want_even_j(2) == 1
        and want_unique_gxor_tot_closed(5) == 1
        and want_green_lo(6) == 1
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
    split = lo_split()
    tot = tot_form()
    kl = killed_lo_e_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, kl, sc, pref)
    dump = {
        "cycle": "QJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "lo_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_iff_k3_or_ge6": True,
            "unique_odd_iff_k_ge_4": True,
            "lo_even_iff_le1_or_k3_or_ge6": True,
            "lo_odd_iff_le1_or_k3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "lo_e_eq_ST": False,
            "lo_o_eq_u_odd": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_iff_k3_or_ge6": "LEMMA",
            "unique_odd_iff_k_ge_4": "LEMMA",
            "lo_even_iff_le1_or_k3_or_ge6": "LEMMA",
            "lo_odd_iff_le1_or_k3": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "lo_e_eq_ST": "KILLED",
            "lo_o_eq_u_odd": "KILLED",
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
        "lo_split n_ok",
        dump["lo_split"]["n_ok"],
        "k_hi",
        dump["lo_split"]["k_hi"],
        "lo_e8",
        dump["lo_split"]["rows"]["8"]["lo_e"],
        "lo_o8",
        dump["lo_split"]["rows"]["8"]["lo_o"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
