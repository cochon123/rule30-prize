#!/usr/bin/env python3
"""Cycle FG: J_{[4U,6U)->6U} = J_{[4U,6U)->18U} by Green translation.

On s in [4U,6U) a light-cone AND at packed p (0<=p<=2s) has Green
degree m=6U-s-1 and d=6U-p. Freshman expands G(m+12U, d+12U) as five
terms G(m, d+12U), G(m, d+8U), G(m,d), G(m, d-8U), G(m, d-12U). Cone
bounds force the four extras off [0,2m], so G(m+12U, d+12U)=G(m,d).
Hence the [4U,6U) remainder to 6U equals the remainder to 18U. Kills:
the same equality to target 10U (shift 4U is too small for the extras
to leave the support). Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_fg.py --certify
Dump: research/cycle_fg.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FE_JSON = Path(__file__).resolve().parent / "cycle_fe.json"
AL_JSON = Path(__file__).resolve().parent / "cycle_al.json"


def cone_bounds() -> dict:
    """Four Freshman extras leave [0,2m] for every light-cone AND on [4U,6U)."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 4 * U, 6 * U
        samples = [t0, t0 + max(U // 2, 1), t1 - 1] if t1 > t0 else []
        for s in samples:
            if not (t0 <= s < t1):
                continue
            m = 6 * U - s - 1
            if m < 0:
                return {"ok": False, "k": k, "m": m}
            two_m = 2 * m
            for p in (0, s, 2 * s):
                d = 6 * U - p
                extras = (d + 12 * U, d + 8 * U, d - 8 * U, d - 12 * U)
                for e in extras:
                    if 0 <= e <= two_m:
                        return {"ok": False, "k": k, "s": s, "p": p, "e": e}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_piece(kmax: int = 7) -> dict:
    """Packed AND remainder on [4U,6U): J6==J18, not always J6==J10."""
    rows = {}
    n_eq18 = 0
    n_neq10 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 4 * U, 6 * U
        T6, T10, T18 = 6 * U, 10 * U, 18 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        j6 = j10 = j18 = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            m6 = T6 - s - 1
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    d6 = T6 - p
                    g6 = G(m6, d6)
                    g18 = G(T18 - s - 1, T18 - p)
                    if g18 != g6:
                        return {"ok": False, "k": k, "s": s, "p": p}
                    j6 ^= g6
                    j10 ^= G(T10 - s - 1, T10 - p)
                    j18 ^= g18
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if j6 != j18:
            return {"ok": False, "k": k, "J": (j6, j18)}
        n_eq18 += 1
        if j6 != j10:
            n_neq10 += 1
        rows[str(k)] = {"J6": j6, "J10": j10, "J18": j18}
    return {
        "ok": n_eq18 == kmax - 1 and n_neq10 > 0,
        "n_eq18": n_eq18,
        "n_neq10": n_neq10,
        "rows": rows,
    }


def prefixes() -> dict:
    ff = json.loads(FF_JSON.read_text())
    fe = json.loads(FE_JSON.read_text())
    al = json.loads(AL_JSON.read_text())
    ok = (
        ff["checks"]["all_ok"]
        and fe["checks"]["all_ok"]
        and al["checks"]["all_ok"]
        and ff["verdict"]["G_shift_q_2a_n_lt_2a_minus_1"] == "LEMMA"
        and fe["verdict"]["cover_fails_iff_J6_J10_J18_vanish"] == "LEMMA"
        and al["verdict"]["all_q_identity"] == "LEMMA"
        and ff["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, cone: dict, piece: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cone["ok"] and piece["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cone = cone_bounds()
    piece = packed_piece()
    pref = prefixes()
    checks = self_checks(c20, cone, piece, pref)
    dump = {
        "cycle": "FG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cone": {k: cone[k] for k in cone if k != "ok"},
        "piece": {k: piece[k] for k in piece if k != "ok"},
        "lemmas": {
            "cone_kills_freshman_extras": True,
            "J_4U_6U_to_6U_eq_to_18U": True,
            "J_4U_6U_to_6U_eq_to_10U": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cone_kills_freshman_extras": "LEMMA",
            "J_4U_6U_to_6U_eq_to_18U": "LEMMA",
            "J_4U_6U_to_6U_eq_to_10U": "KILLED",
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
    print("cone", dump["cone"])
    print("piece", dump["piece"])


if __name__ == "__main__":
    main()
