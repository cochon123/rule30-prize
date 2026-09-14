#!/usr/bin/env python3
"""Cycle RJ: UNIQUE_REST 2-fold off-unique image is 13 even leftover columns.

Packed column doubling is p |-> 2p. Cycle RI stay is {16,30,38}.
The other 13 UNIQUE_REST columns 2-fold off unique to even packed p
(p%4==0), disjoint from FORCED {4,6,14} and from Cycle RF silent
{8,12,28}. The image is (64,84,104,108,116,120,144,152,172,176,
196,212,228), with p=64 leftover silent for k>=6 (Cycle PO). Not
that image meets unique or forced. Not leftover p AND xor catalogue.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rj.py --certify
Dump: research/cycle_rj.json
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
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_po import want_p64_pack
from cycle_rf import FOLD_FORCED
from cycle_ri import IMG, STAY, want_u_fold_img, want_u_fold_stay

OUT = Path(__file__).resolve().with_suffix(".json")
RI_JSON = Path(__file__).resolve().parent / "cycle_ri.json"
RF_JSON = Path(__file__).resolve().parent / "cycle_rf.json"
PO_JSON = Path(__file__).resolve().parent / "cycle_po.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
Q = 10
OFF = (64, 84, 104, 108, 116, 120, 144, 152, 172, 176, 196, 212, 228)


def want_u_fold_off() -> tuple[int, ...]:
    """UNIQUE_REST 2-fold image that leaves UNIQUE_REST."""
    return tuple(sorted(2 * p for p in UNIQUE_REST if 2 * p not in UNIQUE_REST))


def tot_form() -> dict:
    """Off image 13 even leftover columns, disjoint from unique/forced/foldf."""
    off = want_u_fold_off()
    n_even = 0
    for pp in off:
        if pp % 4 != 0:
            return {"ok": False, "mod": True, "pp": pp}
        n_even += 1
        if pp in UNIQUE_REST or pp in FORCED or pp in FOLD_FORCED:
            return {"ok": False, "hit": True, "pp": pp}
    ok = (
        off == OFF
        and n_even == 13
        and len(UNIQUE_REST) == 16
        and len(want_u_fold_stay()) + len(off) == 16
        and want_u_fold_stay() == STAY
        and want_u_fold_img() == IMG
        and set(STAY).isdisjoint(set(p for p in UNIQUE_REST if 2 * p not in UNIQUE_REST))
        and 64 in off
        and want_p64_pack(6) == 0
        and set(OFF).isdisjoint(FORCED)
        and set(OFF).isdisjoint(FOLD_FORCED)
        and set(OFF).isdisjoint(UNIQUE_REST)
    )
    return {"ok": ok, "off": list(off), "n_even": n_even}


def covering_geom() -> dict:
    """k>=5: 2p maps the 13 off-unique columns with matching clip (p=228)."""
    n_ok = 0
    rows = {}
    src = tuple(sorted(p for p in UNIQUE_REST if 2 * p not in UNIQUE_REST))
    if tuple(2 * p for p in src) != OFF:
        return {"ok": False, "src_mismatch": True, "src": list(src)}
    for k in range(5, K_ALG + 1):
        U = 1 << (k - 1)
        Up = 2 * U
        T = Q * U
        Tp = Q * Up
        if T < 114 or Tp < OFF[-1]:
            return {"ok": False, "T": True, "k": k}
        for p, pp in zip(src, OFF):
            if 2 * p != pp:
                return {"ok": False, "map": True, "p": p}
            if (T - p) % 2 or (Tp - pp) % 2:
                return {"ok": False, "parity": True, "k": k, "p": p}
            j = (T - p) // 2
            jp = (Tp - pp) // 2
            if jp != 2 * j or j < 0 or jp < 0:
                return {"ok": False, "j": True, "k": k, "p": p}
            if j > 5 * U or jp > 5 * Up:
                return {"ok": False, "clip": True, "k": k, "p": p}
        n_ok += 1
        if k <= 7:
            rows[str(k)] = {"U": U, "T": T, "Tp": Tp}
    ok = n_ok == K_ALG - 4 and rows["5"]["Tp"] == 320 and rows["5"]["T"] == 160
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows, "src": list(src)}


def killed_eq() -> dict:
    """Off image meets unique or forced; leftover p AND xor catalogue."""
    ok = (
        set(OFF).isdisjoint(UNIQUE_REST)
        and set(OFF).isdisjoint(FORCED)
        and 64 not in UNIQUE_REST
        and 4 not in OFF
        and 8 not in OFF
        and want_u_fold_off() == OFF
    )
    return {"ok": ok, "off": list(OFF)}


def prefixes() -> dict:
    ri = json.loads(RI_JSON.read_text())
    rf = json.loads(RF_JSON.read_text())
    po = json.loads(PO_JSON.read_text())
    ok = (
        ri["checks"]["all_ok"]
        and rf["checks"]["all_ok"]
        and po["checks"]["all_ok"]
        and ri["verdict"]["u_fold_stay_16_30_38"] == "LEMMA"
        and rf["verdict"]["fold_forced_silent_k_ge_2"] == "LEMMA"
        and po["verdict"]["p64_silent_k_ge_6"] == "LEMMA"
        and ri["verdict"]["u_fold_all_unique"] == "KILLED"
        and ri["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ri["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, geom, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and geom["ok"]
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
    geom = covering_geom()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, geom, kl, sc, pref)
    dump = {
        "cycle": "RJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "covering_geom": {k: geom[k] for k in geom if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "u_fold_off_13_even_lo": True,
            "u_fold_off_hits_unique": False,
            "u_fold_off_hits_forced": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "u_fold_off_13_even_lo": "LEMMA",
            "u_fold_off_hits_unique": "KILLED",
            "u_fold_off_hits_forced": "KILLED",
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
    print("tot_form off", dump["tot_form"]["off"], "n_even", dump["tot_form"]["n_even"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
