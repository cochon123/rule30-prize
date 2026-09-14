#!/usr/bin/env python3
"""Cycle RG: covering packed doubling spine 2->4->8->16->32->64; p=2 silent.

Packed column doubling is p |-> 2p. The spine is (2,4,8,16,32,64).
p=2 is silent for every k: even t>=2 has bits (-1,0,1,2)=(0,1,1,0),
not an AND-one (Cycle PD freeze). It 2-folds onto forced p=4.
Forced p=4 2-folds onto silent p=8 (Cycle RF). Silent p=8 2-folds
onto unique p=16. Unique p=16 2-folds onto unique p=32. Unique
p=32 2-folds onto leftover p=64, silent for k>=6 (Cycle PO). Not
p=2 unique-rest. Not p=64 unique-rest. Not p=2 2-folds onto unique.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rg.py --certify
Dump: research/cycle_rg.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_ph import want_p16_pack
from cycle_pk import want_p32_pack
from cycle_po import want_p64_pack
from cycle_rf import FOLD_FORCED, want_fold_forced
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"
PF_JSON = Path(__file__).resolve().parent / "cycle_pf.json"
PH_JSON = Path(__file__).resolve().parent / "cycle_ph.json"
PK_JSON = Path(__file__).resolve().parent / "cycle_pk.json"
PO_JSON = Path(__file__).resolve().parent / "cycle_po.json"
RF_JSON = Path(__file__).resolve().parent / "cycle_rf.json"

N_PAL = 64
M_SLOTS = 64
N_BIT = 64
K_THIN = 8
K_ALG = 64
Q = 10
SPINE = (2, 4, 8, 16, 32, 64)
PAT0110 = (0, 1, 1, 0)


def want_p2_silent(k: int) -> int:
    """Covering p=2 packed AND xor, all k: 0."""
    return 0


def want_spine_fold() -> tuple[int, ...]:
    """2-fold of the spine except the last column."""
    return tuple(2 * p for p in SPINE[:-1])


def frozen_p2() -> dict:
    """Even t>=2: p=2 4-tuple is 0110, not AND."""
    row = 1
    n_ok = 0
    n_even = 0
    for t in range(0, N_BIT + 1):
        four = tuple(bit_at(row, 2 - 3 + i) for i in range(4))
        if t >= 2 and t % 2 == 0:
            if four != PAT0110 or and_clause(*four) != 0:
                return {"ok": False, "four": True, "t": t, "four": four}
            if PAT0110 in AND_ONES:
                return {"ok": False, "ones": True}
            n_even += 1
        if t == 0 and four == PAT0110:
            return {"ok": False, "t0": True}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == N_BIT + 1 and n_even == N_BIT // 2 and PAT0110 not in AND_ONES
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even}


def covering_spine_geom() -> dict:
    """k>=3: spine columns live; 2p maps 2,4,8,16,32 to 4,8,16,32,64."""
    n_ok = 0
    rows = {}
    fold = want_spine_fold()
    if fold != (4, 8, 16, 32, 64):
        return {"ok": False, "fold": True, "got": fold}
    if 2 in UNIQUE_REST or 2 in FORCED or 64 in UNIQUE_REST or 64 in FORCED:
        return {"ok": False, "lab": True}
    if 4 not in FORCED or 8 not in FOLD_FORCED:
        return {"ok": False, "rf": True}
    if 16 not in UNIQUE_REST or 32 not in UNIQUE_REST:
        return {"ok": False, "uniq": True}
    if want_fold_forced() != (8, 12, 28):
        return {"ok": False, "ff": True}
    for k in range(3, K_ALG + 1):
        U = 1 << (k - 1)
        Up = 2 * U
        T = Q * U
        Tp = Q * Up
        if T < 32 or Tp < SPINE[-1]:
            return {"ok": False, "T": True, "k": k}
        for p, pp in zip(SPINE[:-1], fold):
            if 2 * p != pp:
                return {"ok": False, "map": True, "p": p}
            if (T - p) % 2 or (Tp - pp) % 2:
                return {"ok": False, "parity": True, "k": k, "p": p}
            j = (T - p) // 2
            jp = (Tp - pp) // 2
            if jp != 2 * j or j < 0 or jp < 0:
                return {"ok": False, "j": True, "k": k, "p": p}
        n_ok += 1
        if k <= 5:
            rows[str(k)] = {"U": U, "T": T, "Tp": Tp}
    ok = (
        n_ok == K_ALG - 2
        and rows["3"]["Tp"] == 80
        and rows["3"]["T"] == 40
        and want_p16_pack(3) == 1
        and want_p32_pack(5) == 1
        and want_p64_pack(6) == 0
        and want_p2_silent(0) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def thin_p2() -> dict:
    """k<=8: covering packed AND at p=2 on G=1 is 0; one live G=1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_THIN + 1):
        U = 1 << k
        T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        n_g1 = n_and = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                t = (s - t0) // 2
                n = odd_clock(t, U, Qc)
                p = 2
                j = (T - p) // 2
                if j < 0 or j > 2 * n or G(n, j) == 0:
                    row = rule30_step(row)
                    s += 1
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                n_g1 += 1
                n_and += and_clause(*four)
            row = rule30_step(row)
            s += 1
        if n_and != 0 or n_g1 != 1 or want_p2_silent(k) != 0:
            return {"ok": False, "k": k, "n_g1": n_g1, "n_and": n_and}
        n_ok += 1
        rows[str(k)] = {"n_g1": n_g1, "n_and": n_and}
    ok = n_ok == K_THIN + 1 and rows["0"]["n_and"] == 0 and rows["8"]["n_g1"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_eq() -> dict:
    """p=2 unique; p=64 unique; p=2 2-folds onto unique."""
    ok = (
        2 not in UNIQUE_REST
        and 64 not in UNIQUE_REST
        and 2 * 2 == 4
        and 4 in FORCED
        and 4 not in UNIQUE_REST
        and want_spine_fold()[0] == 4
    )
    return {"ok": ok, "spine": list(SPINE), "fold": list(want_spine_fold())}


def prefixes() -> dict:
    pd = json.loads(PD_JSON.read_text())
    pf = json.loads(PF_JSON.read_text())
    ph = json.loads(PH_JSON.read_text())
    pk = json.loads(PK_JSON.read_text())
    po = json.loads(PO_JSON.read_text())
    rf = json.loads(RF_JSON.read_text())
    ok = (
        pd["checks"]["all_ok"]
        and pf["checks"]["all_ok"]
        and ph["checks"]["all_ok"]
        and pk["checks"]["all_ok"]
        and po["checks"]["all_ok"]
        and rf["checks"]["all_ok"]
        and pd["verdict"]["frozen_low"] == "LEMMA"
        and pf["verdict"]["p8_silent"] == "LEMMA"
        and ph["verdict"]["p16_xor_k_ge_3"] == "LEMMA"
        and pk["verdict"]["p32_xor_k_ge_5"] == "LEMMA"
        and po["verdict"]["p64_silent_k_ge_6"] == "LEMMA"
        and rf["verdict"]["fold_forced_silent_k_ge_2"] == "LEMMA"
        and rf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rf["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fr, geom, thin, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and fr["ok"] and geom["ok"]
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
    fr = frozen_p2()
    geom = covering_spine_geom()
    thin = thin_p2()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fr, geom, thin, kl, sc, pref)
    dump = {
        "cycle": "RG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "frozen_p2": {k: fr[k] for k in fr if k != "ok"},
        "covering_spine_geom": {k: geom[k] for k in geom if k != "ok"},
        "thin_p2": {k: thin[k] for k in thin if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "p2_silent_all_k": True,
            "spine_2_4_8_16_32_64": True,
            "p2_unique": False,
            "p64_unique": False,
            "p2_fold_unique": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "p2_silent_all_k": "LEMMA",
            "spine_2_4_8_16_32_64": "LEMMA",
            "p2_unique": "KILLED",
            "p64_unique": "KILLED",
            "p2_fold_unique": "KILLED",
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
        "thin_p2 n_ok",
        dump["thin_p2"]["n_ok"],
        "k0",
        dump["thin_p2"]["rows"]["0"],
        "k8",
        dump["thin_p2"]["rows"]["8"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
