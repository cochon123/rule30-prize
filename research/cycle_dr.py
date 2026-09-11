#!/usr/bin/env python3
"""Cycle DR: n0=16 scars are ident-0-free in 262144 extras; k=17 skipped.

Bit-sliced unique continuation shows all 65536 length-16 T0 have no ident-0
in the next 2^18 extras after (0, T0||not T0, 1). An odd doubling at any
k=9..16 (period 16) therefore cannot produce a second ident-0 before packed
bit 2^18, i.e. through the end of the k=17 high half. Do not claim a closed
form for a later extra, and do not claim the k=18 high half is covered.
Not a prize claim.

Run: python3 research/cycle_dr.py --certify
Dump: research/cycle_dr.json
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
from cycle_dk import PRIZE_U16
from cycle_dn import N_WORDS, census, prize_mask
from cycle_dq import W16

OUT = Path(__file__).resolve().with_suffix(".json")
DQ_JSON = Path(__file__).resolve().parent / "cycle_dq.json"
N_EXTRA = 1 << 18  # 262144
K17_END = 1 << 18


def dq_prefix() -> bool:
    dq = json.loads(DQ_JSON.read_text())
    return (
        dq["checks"]["all_ok"]
        and dq["n16"]["n_extra"] == W16
        and dq["n16"]["n_hit"] == 0
        and dq["verdict"]["at_most_one_ident0_after_odd_k_2_to_16"] == "LEMMA"
    )


def skip_k17(e: int) -> dict:
    """After an n0=16 odd at k=9..16, extras to packed 2^18 stay < e."""
    rows = {}
    ok = True
    for k in range(9, 17):
        pmin = (1 << k) + 1
        need = K17_END - pmin
        fits = need >= e
        rows[k] = {"pmin": pmin, "need": need, "second_fits": fits}
        if fits:
            ok = False
    return {"ok": ok, "rows": rows, "E": e}


def self_checks(c20, dq_ok: bool, n16: dict, skip: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dq_ok and n16["n_hit"] == 0 and n16["n_none"] == N_WORDS
    assert skip["ok"] and skip["E"] == N_EXTRA + 1
    assert not skip["rows"][9]["second_fits"] and not skip["rows"][16]["second_fits"]
    pz = prize_mask(PRIZE_U16)
    assert 0 <= pz < N_WORDS and pz not in n16["first"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    dq_ok = dq_prefix()
    n16 = census(16, N_EXTRA)
    e16 = N_EXTRA + 1 if n16["n_hit"] == 0 else n16["min_extra"]
    skip = skip_k17(e16)
    checks = self_checks(c20, dq_ok, n16, skip)
    dump = {
        "cycle": "DR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n16": {
            "n_extra": N_EXTRA,
            "n_hit": n16["n_hit"],
            "n_none": n16["n_none"],
            "prize_u16": PRIZE_U16,
            "E16": e16,
        },
        "skip_k17": {
            "k9_need": skip["rows"][9]["need"],
            "k16_need": skip["rows"][16]["need"],
            "E": skip["E"],
        },
        "lemmas": {
            "n0_16_no_ident0_in_262144": True,
            "n0_16_odd_at_k_9_to_16_skips_k17": True,
            "n0_16_odd_covers_k18_high_half": False,
            "n0_16_extras_closed_form": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n0_16_no_ident0_in_262144": "LEMMA",
            "n0_16_odd_at_k_9_to_16_skips_k17": "LEMMA",
            "n0_16_odd_covers_k18_high_half": "KILLED",
            "n0_16_extras_closed_form": "KILLED",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("n16", dump["n16"])
    print("skip_k17", dump["skip_k17"])


if __name__ == "__main__":
    main()
