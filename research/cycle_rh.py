#!/usr/bin/env python3
"""Cycle RH: UNIQUE_ODD 2-fold stays unique iff p in {30,38}.

Packed column doubling is p |-> 2p. UNIQUE_ODD is p%4==2 in
UNIQUE_REST. Those nine columns all 2-fold to even packed p
(p%4==0). The image meets UNIQUE_REST iff p in {30,38}, landing on
{60,76} which are UNIQUE_EVEN. The other seven land off unique
(42->84, 54->108, 58->116, 86->172, 98->196, 106->212, 114->228).
Not UNIQUE_ODD 2-fold all stay unique. Not the image is UNIQUE_ODD
(it is even-p). Not packed AND xor at p=30 at k-1 equals p=60 at k
(k=4: 0 vs 1). Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_rh.py --certify
Dump: research/cycle_rh.json
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
from cycle_pm import want_p30_pack
from cycle_pn import want_p38_pack
from cycle_px import want_p60_pack
from cycle_pz import want_p76_pack
from cycle_qj import UNIQUE_EVEN, UNIQUE_ODD
from cycle_rg import SPINE, want_p2_silent, want_spine_fold

OUT = Path(__file__).resolve().with_suffix(".json")
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"
RG_JSON = Path(__file__).resolve().parent / "cycle_rg.json"
PM_JSON = Path(__file__).resolve().parent / "cycle_pm.json"
PN_JSON = Path(__file__).resolve().parent / "cycle_pn.json"
PX_JSON = Path(__file__).resolve().parent / "cycle_px.json"
PZ_JSON = Path(__file__).resolve().parent / "cycle_pz.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
Q = 10
STAY = (30, 38)
IMG = (60, 76)


def want_uo_fold_stay() -> tuple[int, ...]:
    """UNIQUE_ODD columns whose 2-fold stays in UNIQUE_REST."""
    return tuple(sorted(p for p in UNIQUE_ODD if 2 * p in UNIQUE_REST))


def want_uo_fold_img() -> tuple[int, ...]:
    """UNIQUE_REST image of UNIQUE_ODD under p |-> 2p."""
    return tuple(sorted(2 * p for p in UNIQUE_ODD if 2 * p in UNIQUE_REST))


def tot_form() -> dict:
    """Set identity: stay {30,38}, image {60,76} UNIQUE_EVEN; all 2p even."""
    stay = want_uo_fold_stay()
    img = want_uo_fold_img()
    n_even = 0
    off = []
    for p in UNIQUE_ODD:
        pp = 2 * p
        if pp % 4 != 0:
            return {"ok": False, "mod": True, "p": p, "pp": pp}
        n_even += 1
        if p not in STAY:
            if pp in UNIQUE_REST:
                return {"ok": False, "off": True, "p": p, "pp": pp}
            off.append(pp)
    ok = (
        stay == STAY
        and img == IMG
        and n_even == 9
        and len(UNIQUE_ODD) == 9
        and set(IMG).issubset(UNIQUE_EVEN)
        and set(IMG).issubset(UNIQUE_REST)
        and UNIQUE_EVEN == (16, 32, 52, 60, 72, 76, 88)
        and tuple(sorted(off)) == (84, 108, 116, 172, 196, 212, 228)
        and want_spine_fold() == (4, 8, 16, 32, 64)
        and 16 in UNIQUE_EVEN
        and 32 in UNIQUE_EVEN
        and 64 not in UNIQUE_REST
        and want_p2_silent(0) == 0
    )
    return {"ok": ok, "stay": list(stay), "img": list(img), "off": off, "n_even": n_even}


def covering_geom() -> dict:
    """k>=3: 2p maps 30,38 to 60,76 with matching clip."""
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
    ok = n_ok == K_ALG - 2 and rows["3"]["Tp"] == 80 and rows["3"]["T"] == 40
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def killed_eq() -> dict:
    """All UNIQUE_ODD stay unique; image is UNIQUE_ODD; p30(k-1)=p60(k)."""
    ue_stay = tuple(p for p in UNIQUE_EVEN if 2 * p in UNIQUE_REST)
    ok = (
        want_uo_fold_stay() != UNIQUE_ODD
        and len(want_uo_fold_stay()) == 2
        and set(IMG).isdisjoint(UNIQUE_ODD)
        and want_p30_pack(3) == 0
        and want_p60_pack(4) == 1
        and want_p30_pack(3) != want_p60_pack(4)
        and want_p38_pack(3) == 1
        and want_p76_pack(4) == 0
        and want_p38_pack(3) != want_p76_pack(4)
        and ue_stay == (16,)
        and 2 * 16 == 32
        and 2 * 32 == 64
        and 64 not in UNIQUE_REST
    )
    return {
        "ok": ok,
        "stay": list(want_uo_fold_stay()),
        "ue_stay": list(ue_stay),
        "p30_3": want_p30_pack(3),
        "p60_4": want_p60_pack(4),
    }


def prefixes() -> dict:
    qj = json.loads(QJ_JSON.read_text())
    rg = json.loads(RG_JSON.read_text())
    pm = json.loads(PM_JSON.read_text())
    pn = json.loads(PN_JSON.read_text())
    px = json.loads(PX_JSON.read_text())
    pz = json.loads(PZ_JSON.read_text())
    ok = (
        qj["checks"]["all_ok"]
        and rg["checks"]["all_ok"]
        and pm["checks"]["all_ok"]
        and pn["checks"]["all_ok"]
        and px["checks"]["all_ok"]
        and pz["checks"]["all_ok"]
        and rg["verdict"]["spine_2_4_8_16_32_64"] == "LEMMA"
        and rg["verdict"]["p2_silent_all_k"] == "LEMMA"
        and qj["verdict"]["prize"] == "unsolved"
        and rg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and want_p30_pack(2) == 1
        and want_p38_pack(2) == 1
        and want_p60_pack(4) == 1
        and want_p76_pack(3) == 1
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
        "cycle": "RH",
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
            "uo_fold_stay_30_38": True,
            "uo_fold_all_unique": False,
            "uo_fold_img_odd": False,
            "p30_xor_eq_p60_child": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "uo_fold_stay_30_38": "LEMMA",
            "uo_fold_all_unique": "KILLED",
            "uo_fold_img_odd": "KILLED",
            "p30_xor_eq_p60_child": "KILLED",
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
        "off",
        dump["tot_form"]["off"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
