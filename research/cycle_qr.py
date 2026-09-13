#!/usr/bin/env python3
"""Cycle QR: covering UNIQUE_ODD packed AND xor on even n is 0 for every k.

All nine UNIQUE_ODD freeze helpers require n%4 in {1,3}, so even tot
is 0 for k>=7. At k>=6 the n%4==1 slice is p=54 (xor 1) and the
n%4==3 slice is p=42 xor p=58 xor p=98 xor p=106 xor p=114 (xor 1);
they cancel to Cycle QP unique odd packed tot 0. Packed covering
k<=8 has even tot 0, including k=6 where p=106 and p=114 are not
yet frozen. Leftover even-n tot is therefore even rest xor
UNIQUE_EVEN even-n tot, not ST (k=8: leftover even-n=0, ST=1) and
not leftover tot at k-1 (k=6: leftover even-n=1, ST(5)=0). Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qr.py --certify
Dump: research/cycle_qr.json
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
from cycle_pm import in_p30_n3, want_p30_pack
from cycle_pn import in_p38_n3, want_p38_pack
from cycle_pr import in_p42_n3, want_p42_pack
from cycle_ps import in_p54_n1, want_p54_pack
from cycle_pv import in_p58_n3, want_p58_pack
from cycle_qa import in_p86_n3, want_p86_pack
from cycle_qc import in_p98_n3, want_p98_pack
from cycle_qd import in_p106_n3, want_p106_pack
from cycle_qe import in_p114_n3, want_p114_pack
from cycle_qj import UNIQUE_ODD
from cycle_qp import want_unique_odd_pack
from cycle_qq import want_unique_even_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QQ_JSON = Path(__file__).resolve().parent / "cycle_qq.json"
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QP_JSON = Path(__file__).resolve().parent / "cycle_qp.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 8
K_G = 12
K_ALG = 64

def want_uo_even(k: int) -> int:
    """UNIQUE_ODD packed AND xor on even n, all k: 0."""
    return 0


def want_uo_odd(k: int) -> int:
    """UNIQUE_ODD packed AND xor on odd n, all k: 1 iff k in {3,4,5}."""
    return want_unique_odd_pack(k)


def odd_n_par(k: int) -> dict:
    """Green freeze UNIQUE_ODD xor split by n parity / n%4."""
    U = 1 << k
    e = o = n1 = n3 = 0
    p54o = p42o = p58o = p98o = p106o = p114o = 0
    for n in range(0, 4 * U):
        acc = 0
        if in_p30_n3(n, k):
            acc ^= 1
        if in_p38_n3(n, k):
            acc ^= 1
        if in_p86_n3(n, k):
            acc ^= 1
        if in_p42_n3(n, k):
            acc ^= 1
            p42o ^= 1
        if in_p54_n1(n, k):
            acc ^= 1
            p54o ^= 1
        if in_p58_n3(n, k):
            acc ^= 1
            p58o ^= 1
        if in_p98_n3(n, k):
            acc ^= 1
            p98o ^= 1
        if in_p106_n3(n, k):
            acc ^= 1
            p106o ^= 1
        if in_p114_n3(n, k):
            acc ^= 1
            p114o ^= 1
        if not acc:
            continue
        if n % 2:
            o ^= acc
            if n % 4 == 1:
                n1 ^= acc
            else:
                n3 ^= acc
        else:
            e ^= acc
    return {
        "e": e,
        "o": o,
        "n1": n1,
        "n3": n3,
        "p54o": p54o,
        "p42o": p42o,
        "p58o": p58o,
        "p98o": p98o,
        "p106o": p106o,
        "p114o": p114o,
    }


def odd_n_split() -> dict:
    """k=6..K_G: UNIQUE_ODD even tot 0; n1 and n3 each 1; odd tot 0."""
    n_ok = 0
    rows = {}
    for k in range(6, K_G + 1):
        w = odd_n_par(k)
        if w["e"] != 0 or w["o"] != 0 or w["n1"] != 1 or w["n3"] != 1:
            return {"ok": False, "par": True, "k": k, "w": w}
        if w["e"] != want_uo_even(k) or w["o"] != want_uo_odd(k):
            return {"ok": False, "want": True, "k": k}
        if w["p54o"] != 1:
            return {"ok": False, "n1": True, "k": k, "w": w}
        if k == 6:
            if w["p42o"] != 1 or w["p58o"] != 1 or w["p98o"] != 1:
                return {"ok": False, "k6": True, "k": k, "w": w}
            if w["p106o"] != 0 or w["p114o"] != 0:
                return {"ok": False, "k6late": True, "k": k, "w": w}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {
                "e": w["e"],
                "o": w["o"],
                "n1": w["n1"],
                "n3": w["n3"],
                "p54o": w["p54o"],
                "p42o": w["p42o"],
                "p58o": w["p58o"],
                "p98o": w["p98o"],
            }
    ok = (
        n_ok == K_G - 5
        and rows["6"]["e"] == 0
        and rows["6"]["n1"] == 1
        and rows["6"]["n3"] == 1
        and rows["12"]["e"] == 0
        and rows["12"]["n1"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: even tot 0; odd tot 1 iff k in {3,4,5}; n1 xor n3 at k>=6."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_uo_even(k) != 0:
            return {"ok": False, "e": True, "k": k}
        if want_uo_odd(k) != want_unique_odd_pack(k):
            return {"ok": False, "o": True, "k": k}
        if want_uo_odd(k) != int(k in (3, 4, 5)):
            return {"ok": False, "pack": True, "k": k}
        silent = want_p30_pack(k) ^ want_p38_pack(k) ^ want_p86_pack(k)
        if k >= 6 and silent != 0:
            return {"ok": False, "silent": True, "k": k, "silent": silent}
        if k >= 6:
            n1 = want_p54_pack(k)
            n3 = (
                want_p42_pack(k)
                ^ want_p58_pack(k)
                ^ want_p98_pack(k)
                ^ want_p106_pack(k)
                ^ want_p114_pack(k)
            )
            if n1 != 1 or n3 != 1:
                return {"ok": False, "slices": True, "k": k, "n1": n1, "n3": n3}
            if (n1 ^ n3) != want_uo_odd(k) or (n1 ^ n3) != 0:
                return {"ok": False, "xor": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_uo_even(6) == 0
        and want_uo_odd(3) == 1
        and want_uo_odd(6) == 0
        and want_p54_pack(6) == 1
        and want_p42_pack(6) == 1
        and want_p106_pack(6) == 0
        and want_p114_pack(6) == 0
        and want_unique_odd_pack(4) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _thin_uo(k: int) -> dict:
    """Covering packed UNIQUE_ODD AND xor split by n parity."""
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
            for p in UNIQUE_ODD:
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
    """k<=K_THIN: packed UNIQUE_ODD even tot 0; odd tot equals pack tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        w = _thin_uo(k)
        if w["e"] != 0 or w["e"] != want_uo_even(k):
            return {"ok": False, "e": True, "k": k, "w": w}
        if w["o"] != want_uo_odd(k) or w["o"] != want_unique_odd_pack(k):
            return {"ok": False, "o": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {"e": w["e"], "o": w["o"]}
    ok = (
        n_ok == K_THIN + 1
        and rows["0"]["e"] == 0
        and rows["3"]["o"] == 1
        and rows["4"]["o"] == 1
        and rows["5"]["o"] == 1
        and rows["6"]["e"] == 0
        and rows["6"]["o"] == 0
        and rows["8"]["e"] == 0
        and len(UNIQUE_ODD) == 9
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_lo_even_n() -> dict:
    """Leftover even-n tot equals ST, and equals leftover tot at k-1."""
    qo = json.loads(QO_JSON.read_text())
    r6 = qo["rest_n0_walk"]["rows"]["6"]
    r8 = qo["rest_n0_walk"]["rows"]["8"]
    even6 = r6["tot"][0] ^ r6["tot"][2]
    even8 = r8["tot"][0] ^ r8["tot"][2]
    lo6 = even6 ^ want_unique_even_n(6) ^ want_uo_even(6)
    lo8 = even8 ^ want_unique_even_n(8) ^ want_uo_even(8)
    ok = (
        even6 == 0
        and lo6 == 1
        and want_rest_e0(6) == 1
        and lo6 != want_rest_e0(5)
        and even8 == 1
        and lo8 == 0
        and want_rest_e0(8) == 1
        and lo8 != want_rest_e0(8)
        and want_unique_even_n(8) == 1
        and want_uo_even(8) == 0
    )
    return {"ok": ok, "lo6": lo6, "lo8": lo8, "st8": 1, "st5": 0}


def prefixes() -> dict:
    qq = json.loads(QQ_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    qp = json.loads(QP_JSON.read_text())
    ok = (
        qq["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qp["checks"]["all_ok"]
        and qq["verdict"]["unique_even_n_k_ge_6"] == "LEMMA"
        and qp["verdict"]["unique_even_pack_iff_k_in_3_4_5"] == "LEMMA"
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and qq["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qq["verdict"]["prize"] == "unsolved"
        and want_unique_odd_pack(3) == 1
        and want_unique_even_n(6) == 1
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
    kl = killed_lo_even_n()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, split, tot, thin, kl, sc, pref)
    dump = {
        "cycle": "QR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "odd_n_split": {k: split[k] for k in split if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "thin_pack": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_odd_even_n_0": True,
            "unique_odd_odd_n_iff_k_in_3_4_5": True,
            "lo_en_eq_ST": False,
            "lo_en_eq_ST_k_minus_1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_odd_even_n_0": "LEMMA",
            "unique_odd_odd_n_iff_k_in_3_4_5": "LEMMA",
            "lo_en_eq_ST": "KILLED",
            "lo_en_eq_ST_k_minus_1": "KILLED",
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
        "odd_n_split n_ok",
        dump["odd_n_split"]["n_ok"],
        "k6_e",
        dump["odd_n_split"]["rows"]["6"]["e"],
        "k12_n1",
        dump["odd_n_split"]["rows"]["12"]["n1"],
    )
    print(
        "thin_pack n_ok",
        dump["thin_pack"]["n_ok"],
        "k3_o",
        dump["thin_pack"]["rows"]["3"]["o"],
        "k6_e",
        dump["thin_pack"]["rows"]["6"]["e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
