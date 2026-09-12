#!/usr/bin/env python3
"""Cycle EN: n0=16 unfolds after n0=2 odds are ident-0-free through k=19; seed at k=20.

Cycle EM: every n0=2 scar has at most one odd in k=18 and the period-H
seed at k=19. After each n0=8 odd (87468 in k=16, 228939/182785/195790
in k=17, 271197 in k=18), unfold(a) is an n0=16 T0. ident0_events on
those 16 unfolds through extras covering k=19 (from each image lo to
2^20) is empty: no even, no odd, no wrap. So k=19 has no odd on any
n0=2 scar, and the nine earlier n0=16 lifts have no odd in k=18 either.
The k=16/17/18 odds are mutually exclusive, so pi_20=32 divides 2^19.
Kills: those n0=16 T0s odd-double in k=18 or k=19; leftover after
271197 hosts an ident-0 before k=20. Do not claim a closed form for
the u16 strings; do not bump all n0=16 past 2^18; do not claim the
seed for all k. Not a prize claim.

Run: python3 research/cycle_en.py --certify
Dump: research/cycle_en.json
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
from cycle_dk import PRIZE_U16
from cycle_du import pi_from_odds, seed_from_at_most_one
from cycle_ee import image_one_annulus
from cycle_ef import EXTRA87468, PRIZE8
from cycle_eh import ident0_events
from cycle_ek import ODD_COUNTS_1_15
from cycle_el import (
    EXTRA182785,
    EXTRA195790,
    EXTRA228939,
    G72177,
    HIT87468_8,
    MISS57888,
)
from cycle_em import EXTRA271197, HOLD

OUT = Path(__file__).resolve().with_suffix(".json")
EM_JSON = Path(__file__).resolve().parent / "cycle_em.json"
EL_JSON = Path(__file__).resolve().parent / "cycle_el.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
K20 = 1 << 20
FAMILY: list[tuple[int, tuple[str, ...], int]] = [
    (EXTRA87468, tuple(sorted(HIT87468_8)), 16),
    (EXTRA228939, tuple(sorted(MISS57888)), 17),
    (EXTRA182785, ("00100000", "10010000"), 17),
    (EXTRA195790, ("01111100",), 17),
    (EXTRA271197, (HOLD,), 18),
]


def max_extra_k19(lo: int) -> int:
    """Extras so packed lo+E-1 stays <= 2^20 (end of k=19)."""
    return K20 - lo + 1


def n16_scan() -> dict:
    """Unfold after each n0=8 odd; no ident-0 through the k=19 window."""
    rows: dict[str, dict] = {}
    for extra, words, k_land in FAMILY:
        land = image_one_annulus(8, extra)
        if not land["ok"] or land["k_lo"] != k_land or land["k_hi"] != k_land:
            return {"ok": False, "land": extra, "got": land}
        mx = max_extra_k19(land["lo"])
        for s in words:
            ev = ident0_events([int(c) for c in s], extra + 1)
            odd = [e for e in ev if e[1] == "odd"]
            if len(odd) != 1 or odd[0][0] != extra:
                return {"ok": False, "T0": s, "odd": odd[:1]}
            a = odd[0][2]
            u = unfold([int(c) for c in a])
            ustr = "".join(map(str, u))
            if len(u) != 16 or u[0] != 0:
                return {"ok": False, "T0": s, "u": ustr}
            ev2 = ident0_events(u, mx)
            if ev2:
                return {"ok": False, "T0": s, "n16": [(e, k) for e, k, _ in ev2[:4]]}
            rows[s] = {
                "extra": extra,
                "k": k_land,
                "u16": ustr,
                "max_extra": mx,
                "n_ident0": 0,
            }
    fam = set(rows)
    want = HIT87468_8 | MISS57888 | G72177
    ok = (
        fam == want
        and len(rows) == 16
        and rows[PRIZE8]["extra"] == EXTRA228939
        and rows[PRIZE8]["u16"] != PRIZE_U16
        and rows[HOLD]["extra"] == EXTRA271197
        and all(r["n_ident0"] == 0 for r in rows.values())
    )
    return {"ok": ok, "rows": rows}


def k19_window() -> dict:
    lands = {str(extra): image_one_annulus(8, extra) for extra, _, _ in FAMILY}
    mxs = {k: max_extra_k19(v["lo"]) for k, v in lands.items()}
    ok = (
        all(v["ok"] for v in lands.values())
        and lands[str(EXTRA87468)]["k_lo"] == 16
        and lands[str(EXTRA228939)]["k_lo"] == 17
        and lands[str(EXTRA271197)]["k_lo"] == 18
        and mxs[str(EXTRA87468)] == 960853
        and mxs[str(EXTRA228939)] == 819382
        and mxs[str(EXTRA182785)] == 865536
        and mxs[str(EXTRA195790)] == 852531
        and mxs[str(EXTRA271197)] == 777124
        and all(mx > 262144 for mx in mxs.values())
    )
    return {
        "ok": ok,
        "land": {
            k: {kk: lands[k][kk] for kk in ("lo", "hi", "k_lo", "k_hi")} for k in lands
        },
        "max_extra": mxs,
    }


def seed_k20() -> dict:
    """k=16,17,18 odds are mutually exclusive on n0=2; k=19 is empty. pi=32."""
    occurring = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0))
    pis = [pi_from_odds(ODD_COUNTS_1_15 + list(abc)) for abc in occurring]
    h = 1 << 19
    ok = (
        set(pis) == {32}
        and all(h % p == 0 for p in pis)
        and seed_from_at_most_one(20)
        and max(ODD_COUNTS_1_15) <= 1
    )
    return {
        "ok": ok,
        "pi_min": min(pis),
        "pi_max": max(pis),
        "H20": h,
        "pis": sorted(set(pis)),
    }


def prefixes() -> dict:
    em = json.loads(EM_JSON.read_text())
    el = json.loads(EL_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    ok = (
        em["checks"]["all_ok"]
        and em["verdict"]["at_most_one_odd_k18_on_n0_2"] == "LEMMA"
        and em["verdict"]["period_H_seed_at_k19_every_n0_2"] == "LEMMA"
        and em["holdout"]["odd"] == EXTRA271197
        and el["checks"]["all_ok"]
        and el["family"]["prize_odd"] == EXTRA228939
        and el["family"]["n87468"] == 6
        and dr["checks"]["all_ok"]
        and dr["n16"]["n_hit"] == 0
    )
    return {"ok": ok}


def self_checks(c20, scan: dict, win: dict, seed: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert scan["ok"] and win["ok"] and seed["ok"] and pref["ok"]
    assert scan["rows"][PRIZE8]["u16"] != PRIZE_U16
    assert scan["rows"][HOLD]["n_ident0"] == 0
    assert seed["pis"] == [32] and seed["H20"] == 1 << 19
    assert win["max_extra"][str(EXTRA271197)] == 777124
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    scan = n16_scan()
    win = k19_window()
    seed = seed_k20()
    pref = prefixes()
    checks = self_checks(c20, scan, win, seed, pref)
    u16 = {s: scan["rows"][s]["u16"] for s in sorted(scan["rows"])} if scan.get("rows") else {}
    dump = {
        "cycle": "EN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "u16": u16,
        "prize_u16_scar": scan["rows"][PRIZE8]["u16"] if scan.get("ok") else None,
        "prize_u16_packed": PRIZE_U16,
        "k19": {
            "ok": win["ok"],
            "land": win["land"],
            "max_extra": win["max_extra"],
        },
        "seed_k20": {
            "pi_min": seed["pi_min"],
            "pi_max": seed["pi_max"],
            "H20": seed["H20"],
            "pis": seed["pis"],
        },
        "lemmas": {
            "n16_unfold_ident0_free_through_k19": True,
            "k19_window_covered_from_image_lo": True,
            "prize_scar_u16_ne_packed_u16": True,
            "at_most_one_odd_k19_on_n0_2": True,
            "period_H_seed_at_k20_every_n0_2": True,
            "n16_odd_in_k18_or_k19_after_n0_8_odd": False,
            "leftover_after_271197_hosts_ident0_before_k20": False,
            "n16_u16_closed_form": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n16_unfold_ident0_free_through_k19": "LEMMA",
            "k19_window_covered_from_image_lo": "LEMMA",
            "prize_scar_u16_ne_packed_u16": "LEMMA",
            "at_most_one_odd_k19_on_n0_2": "LEMMA",
            "period_H_seed_at_k20_every_n0_2": "LEMMA",
            "n16_odd_in_k18_or_k19_after_n0_8_odd": "KILLED",
            "leftover_after_271197_hosts_ident0_before_k20": "KILLED",
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
    print("prize_u16_scar", dump["prize_u16_scar"])
    print("k19_max_extra", win["max_extra"])
    print("seed_k20", dump["seed_k20"])


if __name__ == "__main__":
    main()
