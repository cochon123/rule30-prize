#!/usr/bin/env python3
"""Cycle EW: scar n3..n6 are rot^{n0-1} of T-functions; even-n0 n6 type N.

gap-parity is rotation-equivariant. Cycle DV's (n3,n4) is exactly
(gap(T), reconstruct(T, gap(T))). Combined with Cycle EU n3=rot^{n0-1}(T)
and Cycle ES reconstruct-rotation, the scar after (0,T,1) is
  n3 = rot^{n0-1}(T)
  n4 = rot^{n0-1}(gap(T))
  n5 = rot^{n0-1}(reconstruct(T, gap(T)))
  n6 = rot^{n0-1}(reconstruct(gap(T), reconstruct(T, gap(T))))
For even n0, n6 is type N and is not 0 or n5. ham(n5,n6) is not n0
(n0=4 has Hamming 3). Kills: gap not rotation-equivariant; DV pair is
not (gap, reconstruct(T,gap)); ham(n5,n6)=n0; n6 not type N for even n0.
Do not claim n6 type N for odd n0; do not claim an 11-bit gap; do not
claim a formula for extra 414990; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_ew.py --certify
Dump: research/cycle_ew.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_ch import ham
from cycle_dv import mask_bits, n3n4_of, odd_copy
from cycle_er import U32
from cycle_es import rot
from cycle_eu import gap_parity

OUT = Path(__file__).resolve().with_suffix(".json")
EU_JSON = Path(__file__).resolve().parent / "cycle_eu.json"
EV_JSON = Path(__file__).resolve().parent / "cycle_ev.json"
ES_JSON = Path(__file__).resolve().parent / "cycle_es.json"
DX_JSON = Path(__file__).resolve().parent / "cycle_dx.json"


def scar_n3_to_n6(t: list[int]) -> tuple:
    n = len(t)
    ones = [1] * n
    n3 = reconstruct(t, ones)
    n4 = gap_parity(n3)
    n5 = reconstruct(n3, n4) if n4 is not None and any(n4) else [0] * n
    n6 = reconstruct(n4, n5) if n4 is not None and any(n5) else None
    return n3, n4, n5, n6


def gap_rot_equiv() -> dict:
    """gap(rot^k S) = rot^k gap(S) for every nonzero S, n=2..8."""
    n_exh = 0
    for n in range(2, 9):
        for mask in range(1, 1 << n):
            s = [(mask >> i) & 1 for i in range(n)]
            g = gap_parity(s)
            if g is None:
                return {"ok": False, "n": n}
            for k in range(n):
                if gap_parity(rot(s, k)) != rot(g, k):
                    return {"ok": False, "n": n, "k": k}
                n_exh += 1
    rng = random.Random(17)
    n_rand = 0
    for n in (12, 16, 32):
        for _ in range(40):
            s = [rng.randint(0, 1) for _ in range(n)]
            if not any(s):
                s[0] = 1
            g = gap_parity(s)
            k = 1 + rng.randrange(n - 1)
            if gap_parity(rot(s, k)) != rot(g, k):
                return {"ok": False, "n": n, "trial": True}
            n_rand += 1
    return {"ok": True, "n_exh": n_exh, "n_rand": n_rand}


def dv_is_gap_pair() -> dict:
    """DV (n3,n4) = (gap(T), reconstruct(T, gap(T))) for every O-type."""
    n_ok = 0
    for n0 in range(1, 9):
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(t)
            g = gap_parity(t)
            if pair is None:
                if g is not None and any(g):
                    return {"ok": False, "n0": n0, "none": True}
                n_ok += 1
                continue
            dn3, dn4 = pair
            if dn3 != g:
                return {"ok": False, "n0": n0, "gap": True}
            u = reconstruct(t, g) if any(g) else [0] * len(t)
            if dn4 != u:
                return {"ok": False, "n0": n0, "u": True}
            n_ok += 1
    return {"ok": True, "n": n_ok}


def scar_rotates() -> dict:
    """n3..n6 = rot^{n0-1} of (T, gap(T), recon(T,gap), recon(gap, recon))."""
    n_ok = 0
    for n0 in range(1, 9):
        r = n0 - 1
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            n3, n4, n5, n6 = scar_n3_to_n6(t)
            g = gap_parity(t)
            if n3 != rot(t, r) or n4 != rot(g, r):
                return {"ok": False, "n0": n0, "n34": True}
            u = reconstruct(t, g) if g is not None and any(g) else [0] * L
            if n5 != rot(u, r):
                return {"ok": False, "n0": n0, "n5": True}
            if n0 % 2 == 0:
                v = reconstruct(g, u)
                if n6 != rot(v, r):
                    return {"ok": False, "n0": n0, "n6": True}
            n_ok += 1
    return {"ok": True, "n": n_ok}


def even_n6_type_n() -> dict:
    """Even n0: n6 type N, not 0, not n5; ham(n5,n6) is not always n0."""
    rows: dict[int, dict] = {}
    ham_n0 = 0
    ham_other = 0
    cex: dict | None = None
    for n0 in range(2, 11, 2):
        n_n = 0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            n3, n4, n5, n6 = scar_n3_to_n6(t)
            if n6 is None or twocopy_type(n6) != "N" or not any(n6) or n6 == n5:
                return {"ok": False, "n0": n0, "mask": mask}
            h = ham(n5, n6)
            if h == n0:
                ham_n0 += 1
            else:
                ham_other += 1
                if cex is None:
                    cex = {
                        "n0": n0,
                        "T0": "".join(str(x) for x in t[:n0]),
                        "ham": h,
                    }
            n_n += 1
        rows[n0] = {"n": n_n}
    ok = (
        rows[2]["n"] == 4
        and rows[10]["n"] == 1024
        and ham_other > 0
        and cex is not None
        and cex["n0"] == 4
        and cex["ham"] == 3
    )
    return {
        "ok": ok,
        "rows": {str(k): v for k, v in rows.items()},
        "ham_eq_n0": ham_n0,
        "ham_ne_n0": ham_other,
        "cex": cex,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    n3, n4, n5, n6 = scar_n3_to_n6(t)
    r = 15
    g = gap_parity(t)
    u = reconstruct(t, g)
    v = reconstruct(g, u)
    ok = (
        n3 == rot(t, r)
        and n4 == rot(g, r)
        and n5 == rot(u, r)
        and n6 == rot(v, r)
        and twocopy_type(n6) == "N"
        and ham(n5, n6) != 16
    )
    return {
        "ok": ok,
        "type6": twocopy_type(n6),
        "wt6": sum(n6),
        "ham56": ham(n5, n6),
    }


def prefixes() -> dict:
    eu = json.loads(EU_JSON.read_text())
    ev = json.loads(EV_JSON.read_text())
    es = json.loads(ES_JSON.read_text())
    dx = json.loads(DX_JSON.read_text())
    ok = (
        eu["checks"]["all_ok"]
        and eu["verdict"]["otype_n3_is_rot_n0_minus_1"] == "LEMMA"
        and ev["checks"]["all_ok"]
        and ev["verdict"]["scar_ham_n4_n5_equals_n0"] == "LEMMA"
        and es["checks"]["all_ok"]
        and dx["lemmas"]["ham_n3_n4_equals_n0_all_O_type"] is True
        and eu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gap: dict, dv: dict, sc: dict, n6: dict, ts: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gap["ok"] and dv["ok"] and sc["ok"] and n6["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gap = gap_rot_equiv()
    dv = dv_is_gap_pair()
    sc = scar_rotates()
    n6 = even_n6_type_n()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, gap, dv, sc, n6, ts, pref)
    dump = {
        "cycle": "EW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "gap_rot": {k: gap[k] for k in gap if k != "ok"},
        "dv_pair": {k: dv[k] for k in dv if k != "ok"},
        "scar_rot": {k: sc[k] for k in sc if k != "ok"},
        "n6": {k: n6[k] for k in n6 if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "gap_rotation_equivariant": True,
            "DV_pair_is_gap_and_reconstruct_T_gap": True,
            "scar_n3_n6_are_rot_n0_minus_1": True,
            "even_n0_n6_type_N": True,
            "ham_n5_n6_equals_n0": False,
            "gap_not_rotation_equivariant": False,
            "n6_type_N_odd_n0": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "gap_rotation_equivariant": "LEMMA",
            "DV_pair_is_gap_and_reconstruct_T_gap": "LEMMA",
            "scar_n3_n6_are_rot_n0_minus_1": "LEMMA",
            "even_n0_n6_type_N": "LEMMA",
            "ham_n5_n6_equals_n0": "KILLED",
            "gap_not_rotation_equivariant": "KILLED",
            "n6_type_N_odd_n0": "PREFIX",
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
    print("n6", dump["n6"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
