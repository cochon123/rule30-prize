#!/usr/bin/env python3
"""Cycle RF: covering 2-fold of forced columns is silent {8,12,28}.

Forced packed columns are {4,6,14}. Doubling the packed index sends
them to {8,12,28}. Cycle PF covering p=8 is silent for every k,
Cycle PG covering p=12 is silent for k>=2, and Cycle PL covering
p=28 is silent for every k. For child k>=2 the 2-fold image of
forced G=1 therefore has packed AND 0, so parent forced AND does
not leak into child rest. Not the 2-fold of forced is forced
({8,12,28} is disjoint from {4,6,14}). Not cellwise 2-fold packed
AND. Not even-n rest equals parent rest tot. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rf.py --certify
Dump: research/cycle_rf.json
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
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PF_JSON = Path(__file__).resolve().parent / "cycle_pf.json"
PG_JSON = Path(__file__).resolve().parent / "cycle_pg.json"
PL_JSON = Path(__file__).resolve().parent / "cycle_pl.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
RE_JSON = Path(__file__).resolve().parent / "cycle_re.json"

N_PAL = 64
M_SLOTS = 64
K_THIN = 6
K_ALG = 64
Q = 10
FOLD_FORCED = (8, 12, 28)


def want_fold_forced() -> tuple[int, ...]:
    """2-fold of FORCED packed columns."""
    return tuple(sorted(2 * p for p in FORCED))


def covering_fold_geom() -> dict:
    """k>=2: 2p maps FORCED to {8,12,28}, disjoint from FORCED; clip matches."""
    n_ok = 0
    rows = {}
    # Child k>=2: parent T=10*2^{k-1} >=20 > p=14, so all forced columns live.
    for k in range(2, K_ALG + 1):
        U = 1 << (k - 1)
        Up = 2 * U
        T = Q * U
        Tp = Q * Up
        if Tp != 2 * T:
            return {"ok": False, "scale": True, "k": k}
        got = []
        for p in sorted(FORCED):
            pp = 2 * p
            if (T - p) % 2 or (Tp - pp) % 2:
                return {"ok": False, "parity": True, "k": k, "p": p}
            j = (T - p) // 2
            jp = (Tp - pp) // 2
            if jp != 2 * j:
                return {"ok": False, "j": True, "k": k, "p": p, "j": j, "jp": jp}
            if not (0 <= j <= 5 * U) or not (0 <= jp <= 5 * Up):
                return {"ok": False, "clip": True, "k": k, "p": p}
            got.append(pp)
        if tuple(got) != FOLD_FORCED:
            return {"ok": False, "img": True, "k": k, "got": got}
        if set(got) & set(FORCED):
            return {"ok": False, "disjoint": True, "k": k}
        n_ok += 1
        if k <= 4:
            rows[str(k)] = {"U": U, "T": T, "got": got}
    ok = (
        n_ok == K_ALG - 1
        and want_fold_forced() == FOLD_FORCED
        and set(FOLD_FORCED).isdisjoint(FORCED)
        and rows["2"]["got"] == [8, 12, 28]
        and rows["2"]["T"] == 20
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def _walk_forced(k: int) -> dict:
    """Covering G=1 cells on forced packed columns, with AND and 4-tuple."""
    U = 1 << k
    T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    cells = {}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Qc)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0 or p not in FORCED:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                cells[(n, j)] = {
                    "and": and_clause(*four),
                    "p": p,
                }
        row = rule30_step(row)
        s += 1
    return cells


def _walk_img(k: int) -> dict:
    """Covering AND on the 2-fold image columns {8,12,28}."""
    U = 1 << k
    T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    cells = {}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Qc)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0 or p not in FOLD_FORCED:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                cells[(n, j)] = {
                    "and": and_clause(*four),
                    "p": p,
                }
        row = rule30_step(row)
        s += 1
    return cells


def thin_img_and() -> dict:
    """k=2..6: 2-fold of forced G=1 has packed AND 0 at child."""
    n_ok = 0
    rows = {}
    for k in range(2, K_THIN + 1):
        parent = _walk_forced(k - 1)
        child = _walk_img(k)
        n_f = n_and = 0
        for (m, r), rec in parent.items():
            n_f += 1
            n, j = 2 * m, 2 * r
            cc = child.get((n, j))
            if cc is None:
                return {"ok": False, "missing": True, "k": k, "m": m, "r": r}
            if cc["p"] != 2 * rec["p"]:
                return {"ok": False, "p": True, "k": k, "m": m, "r": r}
            n_and += cc["and"]
        if n_and != 0:
            return {"ok": False, "and": True, "k": k, "n_and": n_and}
        n_ok += 1
        rows[str(k)] = {"n_forced": n_f, "n_and": n_and}
    ok = (
        n_ok == K_THIN - 1
        and rows["2"]["n_and"] == 0
        and rows["6"]["n_and"] == 0
        and rows["2"]["n_forced"] >= 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_THIN, "rows": rows}


def killed_eq() -> dict:
    """2-fold of forced is forced; cellwise 2-fold packed AND."""
    qv = json.loads(QV_JSON.read_text())
    ok = (
        set(FOLD_FORCED).isdisjoint(FORCED)
        and want_fold_forced() == FOLD_FORCED
        and qv["cellwise_fold"]["n_mis"] == 31
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
    )
    return {"ok": ok, "fold": list(FOLD_FORCED), "forced": sorted(FORCED)}


def prefixes() -> dict:
    pf = json.loads(PF_JSON.read_text())
    pg = json.loads(PG_JSON.read_text())
    pl = json.loads(PL_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    re = json.loads(RE_JSON.read_text())
    ok = (
        pf["checks"]["all_ok"]
        and pg["checks"]["all_ok"]
        and pl["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and re["checks"]["all_ok"]
        and pf["verdict"]["p8_silent"] == "LEMMA"
        and pg["verdict"]["p12_silent_k_ge_2"] == "LEMMA"
        and pl["verdict"]["p28_silent_all_k"] == "LEMMA"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and re["verdict"]["sil_xor_lo_1110_k_ge_6"] == "LEMMA"
        and re["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and re["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, geom, thin, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and geom["ok"] and thin["ok"]
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
    geom = covering_fold_geom()
    thin = thin_img_and()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, geom, thin, kl, sc, pref)
    dump = {
        "cycle": "RF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "covering_fold_geom": {k: geom[k] for k in geom if k != "ok"},
        "thin_img_and": {k: thin[k] for k in thin if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "fold_forced_silent_k_ge_2": True,
            "fold_forced_is_forced": False,
            "cellwise_2fold_and": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "fold_forced_silent_k_ge_2": "LEMMA",
            "fold_forced_is_forced": "KILLED",
            "cellwise_2fold_and": "KILLED",
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
        "thin_img_and n_ok",
        dump["thin_img_and"]["n_ok"],
        "k2",
        dump["thin_img_and"]["rows"]["2"],
        "k6",
        dump["thin_img_and"]["rows"]["6"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
