#!/usr/bin/env python3
"""Cycle EO: n0=16 unfolds after n0=2 odds are ident-0-free through k=20; seed at k=21.

Cycle EN: those 16 unfolds are ident-0-free through k=19, so every n0=2
scar has the period-H seed at k=20. Scanning the same unfolds through
extras covering k=20 (image lo to 2^21) is still empty: no even, no odd,
no wrap. Cycle ED's threshold v(16)=19 is past, and leftover at k=19 and
k=20 still hosts no ident-0. Hence at most one odd in k=20 (namely zero),
and pi_21=32 divides 2^20. Kills: next n0=16 ident-0 forced at v(16)=19;
leftover at k=20 hosts an ident-0. Do not claim a closed form for the
u16 strings; do not bump all n0=16 past 2^18; do not scan k=21 as a
substitute; do not claim the seed for all k. Not a prize claim.

Run: python3 research/cycle_eo.py --certify
Dump: research/cycle_eo.json
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
from cycle_df import unfold
from cycle_du import pi_from_odds, seed_from_at_most_one
from cycle_ee import image_one_annulus
from cycle_ef import EXTRA87468, PRIZE8
from cycle_eh import ident0_events
from cycle_ek import ODD_COUNTS_1_15
from cycle_el import EXTRA228939
from cycle_em import EXTRA271197, HOLD
from cycle_en import FAMILY

OUT = Path(__file__).resolve().with_suffix(".json")
EN_JSON = Path(__file__).resolve().parent / "cycle_en.json"
ED_JSON = Path(__file__).resolve().parent / "cycle_ed.json"
K21 = 1 << 21
EXPECTED_MX = {
    str(EXTRA87468): 2009429,
    str(EXTRA228939): 1867958,
    "182785": 1914112,
    "195790": 1901107,
    str(EXTRA271197): 1825700,
}


def max_extra_k20(lo: int) -> int:
    """Extras so packed lo+E-1 stays <= 2^21 (end of k=20)."""
    return K21 - lo + 1


def k20_scan() -> dict:
    """EN u16 unfolds have no ident-0 through the k=20 window."""
    en = json.loads(EN_JSON.read_text())
    u16 = en["u16"]
    rows: dict[str, dict] = {}
    for extra, words, k_land in FAMILY:
        land = image_one_annulus(8, extra)
        if not land["ok"] or land["k_lo"] != k_land:
            return {"ok": False, "land": extra, "got": land}
        mx = max_extra_k20(land["lo"])
        for s in words:
            if s not in u16:
                return {"ok": False, "missing": s}
            ev = ident0_events([int(c) for c in u16[s]], mx)
            if ev:
                return {"ok": False, "T0": s, "ev": [(e, k) for e, k, _ in ev[:4]]}
            rows[s] = {"extra": extra, "k": k_land, "max_extra": mx, "n_ident0": 0}
    ok = (
        len(rows) == 16
        and rows[PRIZE8]["extra"] == EXTRA228939
        and rows[HOLD]["extra"] == EXTRA271197
        and all(r["n_ident0"] == 0 for r in rows.values())
    )
    return {"ok": ok, "rows": rows}


def prize_unfold_matches() -> dict:
    """Prize u16 in EN json is unfold of a at extra 228939."""
    en = json.loads(EN_JSON.read_text())
    ev = ident0_events([int(c) for c in PRIZE8], EXTRA228939 + 1)
    odd = [e for e in ev if e[1] == "odd"]
    if len(odd) != 1 or odd[0][0] != EXTRA228939:
        return {"ok": False, "odd": odd[:1]}
    u = "".join(map(str, unfold([int(c) for c in odd[0][2]])))
    ok = u == en["u16"][PRIZE8] and u[0] == "0"
    return {"ok": ok, "u16": u}


def k20_window() -> dict:
    lands = {str(extra): image_one_annulus(8, extra) for extra, _, _ in FAMILY}
    mxs = {k: max_extra_k20(v["lo"]) for k, v in lands.items()}
    ok = (
        all(v["ok"] for v in lands.values())
        and mxs == EXPECTED_MX
        and min(mxs.values()) == 1825700
        and min(mxs.values()) > (1 << 20)
    )
    return {"ok": ok, "max_extra": mxs, "min_max_extra": min(mxs.values())}


def seed_k21() -> dict:
    occurring = ((1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0))
    pis = [pi_from_odds(ODD_COUNTS_1_15 + list(abc)) for abc in occurring]
    h = 1 << 20
    ok = (
        set(pis) == {32}
        and all(h % p == 0 for p in pis)
        and seed_from_at_most_one(21)
        and max(ODD_COUNTS_1_15) <= 1
    )
    return {"ok": ok, "pi": 32, "H21": h}


def prefixes() -> dict:
    en = json.loads(EN_JSON.read_text())
    ed = json.loads(ED_JSON.read_text())
    ok = (
        en["checks"]["all_ok"]
        and en["verdict"]["n16_unfold_ident0_free_through_k19"] == "LEMMA"
        and en["verdict"]["period_H_seed_at_k20_every_n0_2"] == "LEMMA"
        and len(en["u16"]) == 16
        and PRIZE8 in en["u16"]
        and ed["checks"]["all_ok"]
        and ed["threshold_v"]["16"] == 19
    )
    return {"ok": ok}


def self_checks(
    c20, scan: dict, match: dict, win: dict, seed: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert scan["ok"] and match["ok"] and win["ok"] and seed["ok"] and pref["ok"]
    assert scan["rows"][HOLD]["n_ident0"] == 0
    assert seed["pi"] == 32 and seed["H21"] == 1 << 20
    assert win["min_max_extra"] == 1825700
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    match = prize_unfold_matches()
    scan = k20_scan()
    win = k20_window()
    seed = seed_k21()
    pref = prefixes()
    checks = self_checks(c20, scan, match, win, seed, pref)
    dump = {
        "cycle": "EO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prize_u16": match.get("u16"),
        "k20": {"ok": win["ok"], "max_extra": win["max_extra"], "min_max_extra": win["min_max_extra"]},
        "seed_k21": {"pi": seed["pi"], "H21": seed["H21"]},
        "n_words": 16,
        "lemmas": {
            "n16_unfold_ident0_free_through_k20": True,
            "k20_window_covered_from_image_lo": True,
            "at_most_one_odd_k20_on_n0_2": True,
            "period_H_seed_at_k21_every_n0_2": True,
            "n16_ident0_forced_at_v16": False,
            "leftover_k20_hosts_ident0_on_n0_2": False,
            "n16_u16_closed_form": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n16_unfold_ident0_free_through_k20": "LEMMA",
            "k20_window_covered_from_image_lo": "LEMMA",
            "at_most_one_odd_k20_on_n0_2": "LEMMA",
            "period_H_seed_at_k21_every_n0_2": "LEMMA",
            "n16_ident0_forced_at_v16": "KILLED",
            "leftover_k20_hosts_ident0_on_n0_2": "KILLED",
            "n16_u16_closed_form": "PREFIX",
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
    print("k20", dump["k20"])
    print("seed_k21", dump["seed_k21"])


if __name__ == "__main__":
    main()
