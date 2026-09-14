#!/usr/bin/env python3
"""Cycle RI: UNIQUE_REST 2-fold stays unique iff p in {16,30,38}.

Packed column doubling is p |-> 2p. Cycle RG unique-even chain is
16->32 (then 32->64 leftover). Cycle RH UNIQUE_ODD stay is {30,38}
image {60,76}. Union: UNIQUE_REST 2-fold stays in UNIQUE_REST iff
p in {16,30,38}, image {32,60,76} which is UNIQUE_EVEN. Not
UNIQUE_REST 2-fold all stay unique (13 of 16 leave). Not UNIQUE_EVEN
2-fold all stay unique (only p=16). Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ri.py --certify
Dump: research/cycle_ri.json
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
from cycle_md import UNIQUE_REST
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qj import UNIQUE_EVEN
from cycle_rg import want_spine_fold
from cycle_rh import want_uo_fold_img, want_uo_fold_stay

OUT = Path(__file__).resolve().with_suffix(".json")
RH_JSON = Path(__file__).resolve().parent / "cycle_rh.json"
RG_JSON = Path(__file__).resolve().parent / "cycle_rg.json"
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
Q = 10
STAY = (16, 30, 38)
IMG = (32, 60, 76)


def want_u_fold_stay() -> tuple[int, ...]:
    """UNIQUE_REST columns whose 2-fold stays in UNIQUE_REST."""
    return tuple(sorted(p for p in UNIQUE_REST if 2 * p in UNIQUE_REST))


def want_u_fold_img() -> tuple[int, ...]:
    """UNIQUE_REST image of UNIQUE_REST under p |-> 2p."""
    return tuple(sorted(2 * p for p in UNIQUE_REST if 2 * p in UNIQUE_REST))


def want_ue_fold_stay() -> tuple[int, ...]:
    """UNIQUE_EVEN columns whose 2-fold stays in UNIQUE_REST."""
    return tuple(sorted(p for p in UNIQUE_EVEN if 2 * p in UNIQUE_REST))


def tot_form() -> dict:
    """Stay {16,30,38} = {16} union RH {30,38}; image {32,60,76} UNIQUE_EVEN."""
    stay = want_u_fold_stay()
    img = want_u_fold_img()
    ue = want_ue_fold_stay()
    off = sorted(2 * p for p in UNIQUE_REST if 2 * p not in UNIQUE_REST)
    ok = (
        stay == STAY
        and img == IMG
        and ue == (16,)
        and stay == tuple(sorted((16,) + want_uo_fold_stay()))
        and img == tuple(sorted((32,) + want_uo_fold_img()))
        and set(IMG).issubset(UNIQUE_EVEN)
        and len(UNIQUE_REST) == 16
        and len(stay) == 3
        and 2 * 16 == 32
        and 2 * 32 == 64
        and 64 not in UNIQUE_REST
        and 64 in off
        and want_spine_fold()[-1] == 64
        and tuple(off) == (64, 84, 104, 108, 116, 120, 144, 152, 172, 176, 196, 212, 228)
    )
    return {
        "ok": ok,
        "stay": list(stay),
        "img": list(img),
        "ue_stay": list(ue),
        "off": off,
        "n_off": len(off),
    }


def covering_geom() -> dict:
    """k>=3: 2p maps 16,30,38 to 32,60,76 with matching clip."""
    n_ok = 0
    rows = {}
    for k in range(3, K_ALG + 1):
        U = 1 << (k - 1)
        Up = 2 * U
        T = Q * U
        Tp = Q * Up
        if T < 38 or Tp < 76:
            return {"ok": False, "T": True, "k": k}
        for p, pp in zip(STAY, IMG):
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
        if k <= 5:
            rows[str(k)] = {"U": U, "T": T, "Tp": Tp}
    ok = n_ok == K_ALG - 2 and rows["3"]["Tp"] == 80
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def killed_eq() -> dict:
    """All UNIQUE_REST stay unique; UNIQUE_EVEN all stay unique."""
    ok = (
        want_u_fold_stay() != tuple(sorted(UNIQUE_REST))
        and len(want_u_fold_stay()) == 3
        and want_ue_fold_stay() != UNIQUE_EVEN
        and want_ue_fold_stay() == (16,)
        and 32 in IMG
        and 64 not in IMG
    )
    return {"ok": ok, "stay": list(want_u_fold_stay()), "ue": list(want_ue_fold_stay())}


def prefixes() -> dict:
    rh = json.loads(RH_JSON.read_text())
    rg = json.loads(RG_JSON.read_text())
    qj = json.loads(QJ_JSON.read_text())
    ok = (
        rh["checks"]["all_ok"]
        and rg["checks"]["all_ok"]
        and qj["checks"]["all_ok"]
        and rh["verdict"]["uo_fold_stay_30_38"] == "LEMMA"
        and rg["verdict"]["spine_2_4_8_16_32_64"] == "LEMMA"
        and rh["verdict"]["uo_fold_all_unique"] == "KILLED"
        and rg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rh["verdict"]["prize"] == "unsolved"
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
        "cycle": "RI",
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
            "u_fold_stay_16_30_38": True,
            "u_fold_all_unique": False,
            "ue_fold_all_unique": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "u_fold_stay_16_30_38": "LEMMA",
            "u_fold_all_unique": "KILLED",
            "ue_fold_all_unique": "KILLED",
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
        "tot_form stay",
        dump["tot_form"]["stay"],
        "img",
        dump["tot_form"]["img"],
        "n_off",
        dump["tot_form"]["n_off"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
