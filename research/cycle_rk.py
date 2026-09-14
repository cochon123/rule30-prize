#!/usr/bin/env python3
"""Cycle RK: UNIQUE_ODD Green xor on even n is 0 for every k.

Cycle QK UNIQUE_EVEN odd-n Green tot vanishes. Dual: UNIQUE_ODD has
p%4==2, so for k>=2 covering j is odd and G(even, odd)=0, hence
even-n tot is 0 per column. At k=0,1 every UNIQUE_ODD packed p
exceeds T=10U and is clipped. Unique Green even-n tot is therefore
UNIQUE_EVEN tot, and unique Green odd-n tot is UNIQUE_ODD tot.
Not UNIQUE_ODD Green n%4==(0,0,0,1) for all k (k=5 is n%4==1).
Not unique Green n%4 equals packed unique n%4. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rk.py --certify
Dump: research/cycle_rk.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qg import gxor_p, want_col_gxor
from cycle_qj import UNIQUE_EVEN, UNIQUE_ODD, want_unique_even, want_unique_odd
from cycle_qk import gxor_parity
from cycle_qv import even_slots
from cycle_rb import want_u_nmod

OUT = Path(__file__).resolve().with_suffix(".json")
QK_JSON = Path(__file__).resolve().parent / "cycle_qk.json"
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"
RJ_JSON = Path(__file__).resolve().parent / "cycle_rj.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_ALG = 64
Q = 10


def want_uo_even_n() -> int:
    """UNIQUE_ODD Green xor on even n, all k."""
    return 0


def want_u_even_n(k: int) -> int:
    """UNIQUE_REST Green xor on even n: UNIQUE_EVEN tot."""
    return want_unique_even(k)


def want_u_odd_n(k: int) -> int:
    """UNIQUE_REST Green xor on odd n: UNIQUE_ODD tot."""
    return want_unique_odd(k)


def tot_form() -> dict:
    """Even-n unique Green equals UNIQUE_EVEN tot; odd-n equals UNIQUE_ODD tot."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_uo_even_n() != 0:
            return {"ok": False, "uo": True, "k": k}
        if want_u_even_n(k) != want_unique_even(k):
            return {"ok": False, "even": True, "k": k}
        if want_u_odd_n(k) != want_unique_odd(k):
            return {"ok": False, "odd": True, "k": k}
        if (want_u_even_n(k) ^ want_u_odd_n(k)) != (
            want_unique_even(k) ^ want_unique_odd(k)
        ):
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_u_even_n(3) == 1
        and want_u_even_n(5) == 0
        and want_u_even_n(6) == 1
        and want_u_odd_n(3) == 0
        and want_u_odd_n(4) == 1
        and all(p % 4 == 2 for p in UNIQUE_ODD)
        and all(p % 4 == 0 for p in UNIQUE_EVEN)
        and len(UNIQUE_ODD) == 9
        and len(UNIQUE_EVEN) == 7
    )
    return {"ok": ok, "n_ok": n_ok}


def covering_geom() -> dict:
    """k>=2: UNIQUE_ODD packed p has odd covering j, so even n vanish."""
    n_ok = 0
    rows = {}
    for k in range(2, K_ALG + 1):
        U = 1 << k
        T = Q * U
        if T % 4 != 0:
            return {"ok": False, "T": True, "k": k}
        for p in UNIQUE_ODD:
            if p % 4 != 2:
                return {"ok": False, "p": p}
            if (T - p) % 2:
                return {"ok": False, "parity": True, "k": k, "p": p}
            j = (T - p) // 2
            if j % 2 == 0:
                return {"ok": False, "j": True, "k": k, "p": p}
        n_ok += 1
        if k <= 4:
            U = 1 << k
            rows[str(k)] = {"U": U, "T": T, "j30": (T - 30) // 2}
    ok = n_ok == K_ALG - 1 and rows["2"]["j30"] == 5 and rows["2"]["T"] == 40
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def unique_odd_even() -> dict:
    """k<=K_G: each UNIQUE_ODD column has even-n Green xor 0; odd-n is tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        ee = eo = 0
        per = {}
        for p in UNIQUE_ODD:
            e, o = gxor_parity(p, k)
            want = want_col_gxor(p, k)
            if e != 0 or o != want or (e ^ o) != gxor_p(p, k):
                return {"ok": False, "p": p, "k": k, "e": e, "o": o, "want": want}
            ee ^= e
            eo ^= o
            per[str(p)] = o
            n_ok += 1
        if ee != 0 or eo != want_unique_odd(k):
            return {"ok": False, "tot": True, "k": k, "ee": ee, "eo": eo}
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"ee": ee, "eo": eo, "per": per}
    ok = (
        rows["0"]["ee"] == 0
        and rows["1"]["ee"] == 0
        and rows["4"]["eo"] == 1
        and rows["5"]["eo"] == 1
        and rows["5"]["per"]["30"] == 1
        and rows["5"]["per"]["86"] == 0
        and rows["6"]["per"]["86"] == 1
        and rows["6"]["eo"] == 1
        and rows["12"]["ee"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def unique_npar() -> dict:
    """k<=K_G: unique Green even-n tot is UNIQUE_EVEN tot, odd-n UNIQUE_ODD tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        ue = uo = 0
        for p in UNIQUE_EVEN:
            e, o = gxor_parity(p, k)
            ue ^= e
            uo ^= o
            if o != 0:
                return {"ok": False, "qk": True, "k": k, "p": p}
        for p in UNIQUE_ODD:
            e, o = gxor_parity(p, k)
            ue ^= e
            uo ^= o
            if e != 0:
                return {"ok": False, "uo": True, "k": k, "p": p}
        if ue != want_u_even_n(k) or uo != want_u_odd_n(k):
            return {"ok": False, "form": True, "k": k, "ue": ue, "uo": uo}
        n_ok += 1
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"ue": ue, "uo": uo}
    ok = (
        n_ok == K_G + 1
        and rows["3"]["ue"] == 1
        and rows["3"]["uo"] == 0
        and rows["6"]["ue"] == 1
        and rows["6"]["uo"] == 1
        and rows["12"]["ue"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def killed_eq() -> dict:
    """UNIQUE_ODD n%4==(0,0,0,1) all k; unique Green n%4 equals packed unique."""
    # k=5 UNIQUE_ODD Green tot is 1 but lives on n%4==1, not n%4==3.
    tot5 = [0, 0, 0, 0]
    U = 1 << 5
    clip = 5 * U
    T = Q * U
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            p = T - 2 * j
            if p not in UNIQUE_ODD:
                continue
            if G(n, j):
                tot5[n % 4] ^= 1
    packed6 = want_u_nmod(6)
    ok = (
        tot5 == [0, 1, 0, 0]
        and want_unique_odd(5) == 1
        and tot5 != [0, 0, 0, 1]
        and packed6 == [1, 0, 0, 1]
        and want_u_even_n(6) == 1
        and want_u_odd_n(6) == 1
        and packed6[0] ^ packed6[2] == 1
        and packed6[1] ^ packed6[3] == 1
        and packed6 != [0, 1, 1, 0]
        and want_unique_even(2) == 0
    )
    return {"ok": ok, "tot5": tot5, "packed6": packed6}


def prefixes() -> dict:
    qk = json.loads(QK_JSON.read_text())
    qj = json.loads(QJ_JSON.read_text())
    rj = json.loads(RJ_JSON.read_text())
    ok = (
        qk["checks"]["all_ok"]
        and qj["checks"]["all_ok"]
        and rj["checks"]["all_ok"]
        and qk["verdict"]["unique_even_odd_n_0"] == "LEMMA"
        and qj["verdict"]["unique_even_iff_k3_or_ge6"] == "LEMMA"
        and rj["verdict"]["u_fold_off_13_even_lo"] == "LEMMA"
        and qk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, geom, uo, npar, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and geom["ok"]
    assert uo["ok"] and npar["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    ev = even_slots(M_SLOTS)
    assert ev["ok"]
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
    geom = covering_geom()
    uo = unique_odd_even()
    npar = unique_npar()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, geom, uo, npar, kl, sc, pref)
    dump = {
        "cycle": "RK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "covering_geom": {k: geom[k] for k in geom if k != "ok"},
        "unique_odd_even": {k: uo[k] for k in uo if k != "ok"},
        "unique_npar": {k: npar[k] for k in npar if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "uo_even_n_0": True,
            "u_even_n_eq_unique_even": True,
            "uo_nmod_0011_all_k": False,
            "u_nmod_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "uo_even_n_0": "LEMMA",
            "u_even_n_eq_unique_even": "LEMMA",
            "uo_nmod_0011_all_k": "KILLED",
            "u_nmod_eq_packed": "KILLED",
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
        "unique_odd_even n_ok",
        dump["unique_odd_even"]["n_ok"],
        "eo4",
        dump["unique_odd_even"]["rows"]["4"]["eo"],
        "ee12",
        dump["unique_odd_even"]["rows"]["12"]["ee"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
