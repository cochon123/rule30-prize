#!/usr/bin/env python3
"""Cycle ET: every n0=8 rotation class has a first ident-0 extra.

Cycle ES: 16 classes of 16; nine extras in 53000, seven none. The seven
miss-class representatives first-ident-0 at extras 62792 (odd), 72474
(even), 93359 (even), 114130 (odd), 125210 (odd), 171542 (odd), 214007
(odd). The two even-first classes later odd-double at 322924 and 119349.
So every n0=8 T0 hits ident-0 by extra 214007. First ident-0 extra is
one plus the first time two consecutive unique-continuation bits are
equal (Cycle DH: reconstruct(A,A)=0). Kills: those seven classes never
ident-0; leftover after 53000 empty for them. Do not claim every n0=16
class hits; do not claim a formula for extra 414990; do not bump all
n0=8 past 523777; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_et.py --certify
Dump: research/cycle_et.json
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
from cycle_di import mask_bits
from cycle_dm import N8_HITS, PRIZE8, PRIZE_EXTRA, first_ident0_int, reconstruct_int
from cycle_ee import image_one_annulus
from cycle_eh import ident0_events
from cycle_ep import EXTRA414990
from cycle_er import T_STAR, complement
from cycle_es import N8_NONE_REPS, class_of, otype

OUT = Path(__file__).resolve().with_suffix(".json")
ES_JSON = Path(__file__).resolve().parent / "cycle_es.json"
# first ident-0 extra per miss-class representative
N8_MISS_FIRST = {
    "00001000": (72474, 0),
    "00010010": (114130, 1),
    "00010100": (214007, 1),
    "00011000": (62792, 1),
    "00100100": (125210, 1),
    "00101010": (93359, 0),
    "00101100": (171542, 1),
}
N8_MISS_ODD = {
    "00001000": 322924,
    "00010010": 114130,
    "00010100": 214007,
    "00011000": 62792,
    "00100100": 125210,
    "00101010": 119349,
    "00101100": 171542,
}
MAX_FIRST = 214007


def pack_bits(xs: list[int]) -> int:
    w = 0
    for i, b in enumerate(xs):
        w |= (b & 1) << i
    return w


def first_equal_cur(T0: list[int], max_extra: int) -> tuple[int | None, int | None]:
    """First cur with a==b, and first cur with b==0 (ident-0 extra)."""
    n0 = len(T0)
    L = 2 * n0
    t = T0 + [x ^ 1 for x in T0]
    a, b = pack_bits(t), (1 << L) - 1
    eq_at: int | None = None
    for cur in range(3, 3 + max_extra):
        if b == 0:
            return eq_at, cur
        if a == b and eq_at is None:
            eq_at = cur
        u = reconstruct_int(a, b, L)
        if u is None:
            return eq_at, None
        a, b = b, u
    return eq_at, None


def miss_first() -> dict:
    """Seven ES miss-class reps have the recorded first extras."""
    rows: dict[str, dict] = {}
    for s, (extra, sm) in N8_MISS_FIRST.items():
        if len(class_of(s)) != 16:
            return {"ok": False, "class": s}
        cur, got_sm = first_ident0_int([int(c) for c in s], MAX_FIRST + 1)
        if cur != extra or got_sm != sm:
            return {"ok": False, "T0": s, "cur": cur, "sm": got_sm}
        rows[s] = {"extra": extra, "odd": sm}
    extras = sorted(v["extra"] for v in rows.values())
    dm = set(N8_HITS)
    ok = (
        len(rows) == 7
        and extras == sorted(v[0] for v in N8_MISS_FIRST.values())
        and not (dm & set(extras))
        and len(dm) + 7 == 16
        and max(extras) == MAX_FIRST
    )
    return {"ok": ok, "rows": rows, "extras": extras}


def miss_odds() -> dict:
    """Even-first classes odd-double later; odd-first extra is the first odd."""
    rows: dict[str, dict] = {}
    for s, odd in N8_MISS_ODD.items():
        first, sm = N8_MISS_FIRST[s]
        mx = odd + 1
        ev = ident0_events([int(c) for c in s], mx)
        odds = [e[0] for e in ev if e[1] == "odd"]
        evens = [e[0] for e in ev if e[1] == "even"]
        if not odds or odds[0] != odd:
            return {"ok": False, "T0": s, "odds": odds[:2]}
        if sm == 0:
            if not evens or evens[0] != first:
                return {"ok": False, "T0": s, "even": evens[:1]}
        else:
            if evens or odds[0] != first:
                return {"ok": False, "T0": s, "ev": ev[:2]}
        land = image_one_annulus(8, odd)
        rows[s] = {
            "first": first,
            "first_odd_kind": sm,
            "odd": odd,
            "k8": land["k_lo"] if land["ok"] else None,
        }
    ok = (
        rows["00001000"]["odd"] == 322924
        and rows["00101010"]["odd"] == 119349
        and rows["00011000"]["k8"] == 15
        and rows["00010010"]["k8"] == 16
        and rows["00001000"]["k8"] == 18
    )
    return {"ok": ok, "rows": rows}


def consecutive_equal() -> dict:
    """Ident-0 extra = 1 + first cur with consecutive equal bits."""
    checks: dict[str, dict] = {}
    # n0=2 extra 22
    eq, z = first_equal_cur(mask_bits(0, 2), 40)
    checks["n2"] = {"eq": eq, "zero": z, "ok": z == 22 and eq == 21}
    # prize n0=8 extra 52809
    eq8, z8 = first_equal_cur([int(c) for c in PRIZE8], PRIZE_EXTRA + 2)
    checks["prize8"] = {
        "eq": eq8,
        "zero": z8,
        "ok": z8 == PRIZE_EXTRA and eq8 == PRIZE_EXTRA - 1,
    }
    # T* n0=16 extra 414990
    eq16, z16 = first_equal_cur([int(c) for c in T_STAR], EXTRA414990 + 2)
    checks["Tstar"] = {
        "eq": eq16,
        "zero": z16,
        "ok": z16 == EXTRA414990 and eq16 == EXTRA414990 - 1,
    }
    ok = all(v["ok"] for v in checks.values())
    return {"ok": ok, "rows": checks}


def landings() -> dict:
    """From k=8: 62792 in k=15; several in k=16/17; even 72474 in k=16."""
    k15 = image_one_annulus(8, 62792)
    k16a = image_one_annulus(8, 114130)
    k16e = image_one_annulus(8, 72474)
    k17 = image_one_annulus(8, 171542)
    k18 = image_one_annulus(8, 322924)
    ok = (
        k15["ok"]
        and k15["k_lo"] == 15
        and k16a["ok"]
        and k16a["k_lo"] == 16
        and k16e["ok"]
        and k16e["k_lo"] == 16
        and k17["ok"]
        and k17["k_lo"] == 17
        and k18["ok"]
        and k18["k_lo"] == 18
        and MAX_FIRST < (1 << 18)
    )
    return {
        "ok": ok,
        "odd_62792_k8": {kk: k15[kk] for kk in ("ok", "k_lo", "k_hi")},
        "odd_114130_k8": {kk: k16a[kk] for kk in ("ok", "k_lo", "k_hi")},
        "even_72474_k8": {kk: k16e[kk] for kk in ("ok", "k_lo", "k_hi")},
        "odd_171542_k8": {kk: k17[kk] for kk in ("ok", "k_lo", "k_hi")},
        "odd_322924_k8": {kk: k18[kk] for kk in ("ok", "k_lo", "k_hi")},
    }


def prefixes() -> dict:
    es = json.loads(ES_JSON.read_text())
    ok = (
        es["checks"]["all_ok"]
        and es["verdict"]["n8_sixteen_classes_nine_hit"] == "LEMMA"
        and es["n8"]["n_none_classes"] == 7
        and tuple(es["n8"]["none_reps"]) == N8_NONE_REPS
        and es["verdict"]["every_class_eventually_hits"] == "PREFIX"
    )
    return {"ok": ok}


def self_checks(
    c20, first: dict, odds: dict, eq: dict, land: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert first["ok"] and odds["ok"] and eq["ok"] and land["ok"] and pref["ok"]
    assert otype(PRIZE8)[:8] == PRIZE8
    assert max(first["extras"]) == 214007
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    first = miss_first()
    odds = miss_odds()
    eq = consecutive_equal()
    land = landings()
    pref = prefixes()
    checks = self_checks(c20, first, odds, eq, land, pref)
    dump = {
        "cycle": "ET",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n8_miss_first": first["rows"],
        "n8_miss_odd": {s: v["odd"] for s, v in odds["rows"].items()},
        "n8_miss_k8": {s: v["k8"] for s, v in odds["rows"].items()},
        "consecutive_equal": eq["rows"],
        "land": {k: land[k] for k in land if k != "ok"},
        "lemmas": {
            "every_n8_class_has_ident0": True,
            "seven_miss_extras_recorded": True,
            "ident0_extra_is_1_plus_first_equal": True,
            "seven_n8_classes_never_ident0": False,
            "leftover_after_53000_empty_for_miss": False,
            "every_n16_class_hits": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "every_n8_class_has_ident0": "LEMMA",
            "seven_miss_extras_recorded": "LEMMA",
            "ident0_extra_is_1_plus_first_equal": "LEMMA",
            "seven_n8_classes_never_ident0": "KILLED",
            "leftover_after_53000_empty_for_miss": "KILLED",
            "every_n16_class_hits": "PREFIX",
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
    print("miss_first", {s: v["extra"] for s, v in first["rows"].items()})
    print("miss_odd", dump["n8_miss_odd"])


if __name__ == "__main__":
    main()
