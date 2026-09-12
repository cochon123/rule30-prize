#!/usr/bin/env python3
"""Cycle ER: FAM414990 T0s are the 16-prefixes of rotations of one O-type word.

Cycle EQ: the 32 predecessors are rots of W, and FAM414990 is
complement-closed. Aligning T0 with the rotation index of W shows the 32
T0s are exactly the length-16 prefixes of the 32 rotations of the O-type
necklace U=01100111001011101001100011010001 (U=T*||not T* with
T*=0110011100101110). Min period of U is 32. The member whose predecessor
is W itself is T*. Complement of T0 is rotation by 16. Kills: no T0 closed
form beyond the predecessor necklace. Do not claim U=W; do not claim a
formula for extra 414990; do not claim U on the n0=2 cascade; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_er.py --certify
Dump: research/cycle_er.json
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
from cycle_ca import KNOWN20, packed_center_bits, xorcat
from cycle_cb import twocopy_type
from cycle_eh import ident0_events
from cycle_ep import EXTRA414990, FAM414990, N_FAM, WITNESSES
from cycle_eq import PRED32, ROTS_PRED32, complement, rotations

OUT = Path(__file__).resolve().with_suffix(".json")
EQ_JSON = Path(__file__).resolve().parent / "cycle_eq.json"
T_STAR = "0110011100101110"
U32 = T_STAR + complement(T_STAR)


def min_period(s: str) -> int:
    n = len(s)
    for p in range(1, n + 1):
        if n % p == 0 and s == s[:p] * (n // p):
            return p
    return n


def prefixes_of_rots(s: str, n0: int = 16) -> frozenset[str]:
    return frozenset((s[k:] + s[:k])[:n0] for k in range(len(s)))


def family_from_U() -> dict:
    """FAM414990 is the 16-prefixes of the 32 rotations of U."""
    got = prefixes_of_rots(U32)
    ok = (
        U32 == T_STAR + complement(T_STAR)
        and T_STAR == WITNESSES[1]
        and len(U32) == 32
        and min_period(U32) == 32
        and twocopy_type([int(c) for c in U32]) == "O"
        and xorcat([int(c) for c in U32]) == 0
        and U32.count("1") == 16
        and got == FAM414990
        and len(got) == N_FAM
        and len(rotations(U32)) == 32
    )
    return {"ok": ok, "U": U32, "T_star": T_STAR, "n": len(got)}


def rot16_is_complement() -> dict:
    """Rotation by 16 of U yields the complementary T0."""
    r16 = (U32[16:] + U32[:16])[:16]
    ok = r16 == complement(T_STAR) and r16 in FAM414990
    pairs = 0
    for k in range(16):
        a = (U32[k:] + U32[:k])[:16]
        b = (U32[k + 16 :] + U32[: k + 16])[:16]
        if b != complement(a) or a not in FAM414990 or b not in FAM414990:
            return {"ok": False, "k": k}
        pairs += 1
    return {"ok": ok and pairs == 16, "n_pairs": pairs, "rot16": r16}


def pred_of_T_star_is_W() -> dict:
    """The T0 whose predecessor is W is T* = U[:16]."""
    ev = ident0_events([int(c) for c in T_STAR], EXTRA414990 + 1)
    ok = (
        len(ev) == 1
        and ev[0][0] == EXTRA414990
        and ev[0][1] == "even"
        and ev[0][2] == PRED32
        and ev[0][2] in ROTS_PRED32
        and T_STAR in FAM414990
    )
    return {"ok": ok, "pred": ev[0][2] if ev else None}


def prefixes() -> dict:
    eq = json.loads(EQ_JSON.read_text())
    ok = (
        eq["checks"]["all_ok"]
        and eq["verdict"]["fam414990_preds_rots_of_W"] == "LEMMA"
        and eq["verdict"]["fam414990_complement_closed"] == "LEMMA"
        and eq["pred32"] == PRED32
        and eq["n_fam"] == N_FAM
        and eq["verdict"]["T0_closed_form_beyond_necklace"] == "PREFIX"
    )
    return {"ok": ok}


def self_checks(c20, fam: dict, r16: dict, pred: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fam["ok"] and r16["ok"] and pred["ok"] and pref["ok"]
    assert U32 != PRED32
    assert T_STAR in WITNESSES
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fam = family_from_U()
    r16 = rot16_is_complement()
    pred = pred_of_T_star_is_W()
    pref = prefixes()
    checks = self_checks(c20, fam, r16, pred, pref)
    dump = {
        "cycle": "ER",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "U32": U32,
        "T_star": T_STAR,
        "pred32": PRED32,
        "n_fam": N_FAM,
        "rot16": r16["rot16"],
        "lemmas": {
            "fam414990_16_prefixes_of_rots_U": True,
            "U32_O_type_min_period_32": True,
            "rot16_prefix_is_complement": True,
            "T_star_pred_is_W": True,
            "no_T0_closed_form_beyond_W": False,
            "U_eq_W": False,
            "U_on_n0_2_cascade": False,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "fam414990_16_prefixes_of_rots_U": "LEMMA",
            "U32_O_type_min_period_32": "LEMMA",
            "rot16_prefix_is_complement": "LEMMA",
            "T_star_pred_is_W": "LEMMA",
            "no_T0_closed_form_beyond_W": "KILLED",
            "U_eq_W": "KILLED",
            "U_on_n0_2_cascade": "KILLED",
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
    print("U32", U32)
    print("T_star", T_STAR)


if __name__ == "__main__":
    main()
