#!/usr/bin/env python3
"""Cycle GQ: hit endpoints are Green ones; k<=3 AND extras are only lo.

mer_one(0)=mer_one(U-1)=1 for every k. Packed AND at cone-hi j=U-1 is
live on all Cycle GG hits (k<=6). For k<=3 the only possible extra
AND among mer_one columns is j=0. AND at lo is not always live; extras
are not only lo at k=4. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_gq.py --certify
Dump: research/cycle_gq.json
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
from cycle_gn import mer_one
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GP_JSON = Path(__file__).resolve().parent / "cycle_gp.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"
GN_JSON = Path(__file__).resolve().parent / "cycle_gn.json"


def endpoints() -> dict:
    """mer_one(0)=mer_one(U-1)=1 for k<=16."""
    n_ok = 0
    for k in range(0, 17):
        U = 1 << k
        if mer_one(0) != 1 or mer_one(U - 1) != 1:
            return {"ok": False, "k": k, "m0": mer_one(0), "mhi": mer_one(U - 1)}
        n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_and() -> dict:
    """AND at j=U-1 live; k<=3 extras subseteq {0}. k<=6."""
    n_ok = 0
    n_um1 = 0
    n_extra0 = 0
    n_only_hi = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            row = 1
            for _ in range(t0):
                row = rule30_step(row)
            s = t0
            for q in range(Q):
                target = t0 + 1 + q * (2 * U)
                while s < target:
                    row = rule30_step(row)
                    s += 1
                A = (row << 1) & row
                lo = 2 * (s - t0 + 1)
                extras = []
                on_hi = False
                for j in range(U):
                    if not mer_one(j):
                        continue
                    r = lo + 2 * j
                    if ((A >> (T + r)) & 1) == 0:
                        continue
                    if j == U - 1:
                        on_hi = True
                    else:
                        extras.append(j)
                if not on_hi:
                    return {"ok": False, "k": k, "q": q, "hi_dead": True}
                if k <= 3 and any(j != 0 for j in extras):
                    return {"ok": False, "k": k, "extras": extras}
                n_ok += 1
                n_um1 += 1
                n_extra0 += int(extras == [0])
                n_only_hi += int(not extras)
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_um1": n_um1,
        "n_extra0": n_extra0,
        "n_only_hi": n_only_hi,
    }


def killed_mer0() -> dict:
    """mer_one(0) is 1, not 0."""
    return {"ok": mer_one(0) == 1, "mer0": mer_one(0)}


def killed_lo_always() -> dict:
    """AND at j=0 is not always live: k=1, W=4U."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    A = (row << 1) & row
    lo = 2 * (s - t0 + 1)
    on = ((A >> (T + lo)) & 1) == 1
    ok = mer_one(0) == 1 and not on
    return {"ok": ok, "k": k, "AND_lo": int(on)}


def killed_extras_only_lo_k4() -> dict:
    """Extras are not only lo at k=4, W=8U, q=0: {6,7}."""
    k = 4
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    A = (row << 1) & row
    lo = 2 * (s - t0 + 1)
    extras = []
    for j in range(U):
        if j == U - 1 or not mer_one(j):
            continue
        r = lo + 2 * j
        if ((A >> (T + r)) & 1):
            extras.append(j)
    ok = extras == [6, 7]
    return {"ok": ok, "k": k, "extras": extras}


def prefixes() -> dict:
    gp = json.loads(GP_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    gn = json.loads(GN_JSON.read_text())
    ok = (
        gp["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and gn["checks"]["all_ok"]
        and gp["verdict"]["jth_even_r_has_palindrome_index_j"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U"]
        == "LEMMA"
        and gn["verdict"]["G_2k_minus_1_f_eq_1_iff_f_ne_2_mod_3_on_0_U"]
        == "LEMMA"
        and gp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ep: dict, pk: dict, km: dict, kl: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ep["ok"] and pk["ok"]
    assert km["ok"] and kl["ok"] and ke["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ep = endpoints()
    pk = packed_and()
    km = killed_mer0()
    kl = killed_lo_always()
    ke = killed_extras_only_lo_k4()
    pref = prefixes()
    checks = self_checks(c20, ep, pk, km, kl, ke, pref)
    dump = {
        "cycle": "GQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "endpoints": {k: ep[k] for k in ep if k != "ok"},
        "packed_and": {k: pk[k] for k in pk if k != "ok"},
        "killed_mer0": {k: km[k] for k in km if k != "ok"},
        "killed_lo_always": {k: kl[k] for k in kl if k != "ok"},
        "killed_extras_only_lo_k4": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "mer_one_0_and_U_minus_1_eq_1": True,
            "AND_at_j_U_minus_1_live_on_hits": True,
            "k_le_3_AND_extras_subseteq_0": True,
            "mer_one_0_eq_0": False,
            "AND_at_lo_always_live": False,
            "extras_only_lo_at_k_4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mer_one_0_and_U_minus_1_eq_1": "LEMMA",
            "AND_at_j_U_minus_1_live_on_hits": "LEMMA",
            "k_le_3_AND_extras_subseteq_0": "LEMMA",
            "mer_one_0_eq_0": "KILLED",
            "AND_at_lo_always_live": "KILLED",
            "extras_only_lo_at_k_4": "KILLED",
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
    print("packed_and", dump["packed_and"])


if __name__ == "__main__":
    main()
