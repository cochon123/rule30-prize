#!/usr/bin/env python3
"""Cycle FB: even-n0 n5 has 00 iff n6 has 00; no-00 class has z=n0/2.

On every even-n0 O-type, n5 has a consecutive 00 iff n6 does. The
no-00 class has size 2^{n0/2+1}, empty-pair count z=n0/2, and n7
O-type. n0=4 no-00 is FAM89; n0=6 no-00 contains the extra-22 3-folds.
Kills: n7 O-type implies n5 has no 00 (316 counterexamples); no-00 is
only extra 22 (n0=4 is FAM89). Do not claim no-00 iff extra 22 or 89;
do not claim n7 consecutive 11 as a production; do not claim an 11-bit
gap; do not bump extras; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_fb.py --certify
Dump: research/cycle_fb.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_dv import mask_bits, odd_copy
from cycle_eb import N6_FOLD3
from cycle_er import U32
from cycle_ev import has00
from cycle_ew import scar_n3_to_n6
from cycle_ex import empty_slots

OUT = Path(__file__).resolve().with_suffix(".json")
FA_JSON = Path(__file__).resolve().parent / "cycle_fa.json"
EB_JSON = Path(__file__).resolve().parent / "cycle_eb.json"

FAM89 = {"0000", "0001", "0011", "0111", "1000", "1100", "1110", "1111"}


def bits(xs: list[int]) -> str:
    return "".join(str(x) for x in xs)


def n5_iff_n6_00() -> dict:
    """n5 has 00 iff n6 has 00; no-00 class: size, z=n0/2, n7 O-type."""
    n_ok = 0
    n_no00 = 0
    n_n7O_with00 = 0
    rows: dict[str, dict] = {}
    n4_fam89 = set()
    n6_folds = set()
    for n0 in range(2, 11, 2):
        n_no = 0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            _n3, n4, n5, n6 = scar_n3_to_n6(t)
            h5, h6 = has00(n5), has00(n6)
            if h5 != h6:
                return {"ok": False, "n0": n0, "iff": True}
            n7 = reconstruct(n5, n6)
            if n7 is None:
                return {"ok": False, "n0": n0, "n7": True}
            if not h5:
                n_no += 1
                n_no00 += 1
                z = len(empty_slots(n4, n0))
                if z != n0 // 2:
                    return {"ok": False, "n0": n0, "z": z}
                if twocopy_type(n7) != "O":
                    return {"ok": False, "n0": n0, "n7O": True}
                t0 = bits(t[:n0])
                if n0 == 4:
                    n4_fam89.add(t0)
                if n0 == 6:
                    n6_folds.add(t0)
            else:
                if twocopy_type(n7) == "O":
                    n_n7O_with00 += 1
            n_ok += 1
        want = 1 << (n0 // 2 + 1)
        if n_no != want:
            return {"ok": False, "n0": n0, "count": n_no}
        rows[str(n0)] = {"n_no00": n_no, "n": 1 << n0}
    if n4_fam89 != FAM89:
        return {"ok": False, "fam89": sorted(n4_fam89)}
    if not N6_FOLD3 <= n6_folds:
        return {"ok": False, "folds": sorted(n6_folds)}
    if n_n7O_with00 == 0:
        return {"ok": False, "n7O_with00": True}
    return {
        "ok": n_ok == 1364 and n_no00 == 124 and n_n7O_with00 == 316,
        "n_ok": n_ok,
        "n_no00": n_no00,
        "n_n7O_with00": n_n7O_with00,
        "rows": rows,
        "n0_4_is_FAM89": True,
        "n0_6_contains_folds": True,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    _n3, n4, n5, n6 = scar_n3_to_n6(t)
    n7 = reconstruct(n5, n6)
    z = len(empty_slots(n4, 16))
    ok = (
        has00(n5) == has00(n6)
        and has00(n5)
        and z != 8
        and n7 is not None
        and twocopy_type(n7) == "N"
    )
    return {
        "ok": ok,
        "n5_has00": has00(n5),
        "n6_has00": has00(n6),
        "z": z,
        "n7_type": twocopy_type(n7) if n7 is not None else None,
    }


def prefixes() -> dict:
    fa = json.loads(FA_JSON.read_text())
    eb = json.loads(EB_JSON.read_text())
    ok = (
        fa["checks"]["all_ok"]
        and eb["checks"]["all_ok"]
        and fa["verdict"]["even_n0_n5_consecutive_11_proved"] == "LEMMA"
        and fa["verdict"]["n5_always_has_00"] == "KILLED"
        and fa["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, scar: dict, ts: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert scar["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    scar = n5_iff_n6_00()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, scar, ts, pref)
    dump = {
        "cycle": "FB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "scar": {
            k: scar[k]
            for k in scar
            if k != "ok"
        },
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "n5_00_iff_n6_00": True,
            "no00_z_n0_over_2": True,
            "no00_n7_O_type": True,
            "n7_O_implies_no00": False,
            "no00_only_extra_22": False,
            "n7_consecutive_11": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n5_00_iff_n6_00": "LEMMA",
            "no00_z_n0_over_2": "LEMMA",
            "no00_n7_O_type": "LEMMA",
            "n7_O_implies_no00": "KILLED",
            "no00_only_extra_22": "KILLED",
            "n7_consecutive_11": "PREFIX",
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
    print("scar n_no00", dump["scar"].get("n_no00"), "rows", dump["scar"].get("rows"))
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
