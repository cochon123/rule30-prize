#!/usr/bin/env python3
"""Cycle EY: 11 in S forces consecutive 00 in gap; even-n0 n4 has 00.

If S has 11 at (t-1, t) then back_dist(t)=back_dist(t+1)=1, so
gap(S)_t = gap(S)_{t+1} = 0. Even-n0 O-type always has a 11 (Cycle EV),
so gap(T) and scar n4=rot^{n0-1}(gap(T)) always have a consecutive 00.
The converse is false (100 and 100100 have gap 00 with no 11). Even-n0
n6 can lack a consecutive 00 (124 of 1364 words). Kills: gap has 00 iff
S has 11; n6 always has 00.
Do not claim an 11-bit gap; do not claim n6 type N for odd n0; do not
claim a formula for extra 414990; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_ey.py --certify
Dump: research/cycle_ey.json
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
from cycle_dv import mask_bits, odd_copy
from cycle_er import U32
from cycle_eu import gap_parity
from cycle_ev import has00, has11
from cycle_ew import scar_n3_to_n6

OUT = Path(__file__).resolve().with_suffix(".json")
EX_JSON = Path(__file__).resolve().parent / "cycle_ex.json"
EV_JSON = Path(__file__).resolve().parent / "cycle_ev.json"
EU_JSON = Path(__file__).resolve().parent / "cycle_eu.json"


def eleven_forces_gap_00() -> dict:
    """S has 11 at (t-1,t) => gap[t]=gap[t+1]=0. Nonzero length 2..10."""
    n_11 = 0
    n_words = 0
    for n in range(2, 11):
        for mask in range(1, 1 << n):
            s = [(mask >> t) & 1 for t in range(n)]
            g = gap_parity(s)
            if g is None:
                return {"ok": False, "n": n, "none": True}
            n_words += 1
            for t in range(n):
                if s[(t - 1) % n] == 1 and s[t] == 1:
                    n_11 += 1
                    if g[t] != 0 or g[(t + 1) % n] != 0:
                        return {"ok": False, "n": n, "t": t}
    return {"ok": n_11 > 0, "n_words": n_words, "n_11": n_11}


def converse_fails() -> dict:
    """gap can have 00 with no 11. Witnesses 100 (odd) and 100100 (even)."""
    rows = []
    for s in ([1, 0, 0], [1, 0, 0, 1, 0, 0]):
        g = gap_parity(s)
        if g is None or has11(s) or not has00(g):
            return {"ok": False, "s": s}
        rows.append(
            {
                "s": "".join(str(x) for x in s),
                "gap": "".join(str(x) for x in g),
            }
        )
    return {"ok": True, "witnesses": rows}


def even_n0_gap_has_00() -> dict:
    """Even-n0 O-type has 11 (EV) so gap(T) and n4 have consecutive 00."""
    n_ok = 0
    n_n6_00 = 0
    n_n6_no00 = 0
    for n0 in range(2, 11, 2):
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            if not has11(t):
                return {"ok": False, "n0": n0, "t11": True}
            g = gap_parity(t)
            if g is None or not has00(g):
                return {"ok": False, "n0": n0, "gap": True}
            _n3, n4, _n5, n6 = scar_n3_to_n6(t)
            if not has00(n4):
                return {"ok": False, "n0": n0, "n4": True}
            if has00(n6):
                n_n6_00 += 1
            else:
                n_n6_no00 += 1
            n_ok += 1
    if n_n6_no00 == 0:
        return {"ok": False, "n6_always_00": True}
    return {
        "ok": n_ok == 1364 and n_n6_no00 == 124,
        "n_ok": n_ok,
        "n_n6_00": n_n6_00,
        "n_n6_no00": n_n6_no00,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    g = gap_parity(t)
    _n3, n4, _n5, n6 = scar_n3_to_n6(t)
    ok = (
        has11(t)
        and g is not None
        and has00(g)
        and has00(n4)
        and has00(n6)
    )
    return {
        "ok": ok,
        "n4_has00": has00(n4),
        "n6_has00": has00(n6),
        "wt4": sum(n4),
        "wt6": sum(n6),
    }


def prefixes() -> dict:
    ex = json.loads(EX_JSON.read_text())
    ev = json.loads(EV_JSON.read_text())
    eu = json.loads(EU_JSON.read_text())
    ok = (
        ex["checks"]["all_ok"]
        and ex["verdict"]["even_n0_n6_consecutive_11"] == "LEMMA"
        and ev["verdict"]["otype_00_iff_11"] == "LEMMA"
        and eu["checks"]["all_ok"]
        and ex["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, eleven: dict, conv: dict, even: dict, ts: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert eleven["ok"] and conv["ok"] and even["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    eleven = eleven_forces_gap_00()
    conv = converse_fails()
    even = even_n0_gap_has_00()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, eleven, conv, even, ts, pref)
    dump = {
        "cycle": "EY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "eleven": {k: eleven[k] for k in eleven if k != "ok"},
        "converse": conv["witnesses"],
        "even_n0": {k: even[k] for k in even if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "eleven_forces_gap_00": True,
            "even_n0_gap_has_00": True,
            "even_n0_n4_has_00": True,
            "gap_00_iff_eleven": False,
            "n6_always_has_00": False,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "eleven_forces_gap_00": "LEMMA",
            "even_n0_gap_has_00": "LEMMA",
            "even_n0_n4_has_00": "LEMMA",
            "gap_00_iff_eleven": "KILLED",
            "n6_always_has_00": "KILLED",
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
    print("eleven", dump["eleven"])
    print("even_n0", dump["even_n0"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
