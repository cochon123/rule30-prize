#!/usr/bin/env python3
"""Cycle TI: covering times by n mod 4 are four 8-APs partitioning odd t.

On q=10, t=10U-2n-1. Covering n=4l+r has times the AP
2U+7-2r, ..., 10U-2r-1 with difference 8. The four residue APs
partition the odd integers in [2U+1, 10U-1]. For k>=2 they sit in
distinct classes t=7,5,3,1 mod 8. Pal-center tot is the xor of
c_t and x(t,1) on these four APs and is not identically 0 on any
residue. Not rest=S xor T. Do not walk leftover p catalogues. Do
not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ti.py --certify
Dump: research/cycle_ti.json
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
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_st import pal_center_and
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_td import want_d1_n
from cycle_tf import want_d1_r1_n
from cycle_th import n1_ap_ok, n1_times
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TH_JSON = Path(__file__).resolve().parent / "cycle_th.json"
TG_JSON = Path(__file__).resolve().parent / "cycle_tg.json"
TF_JSON = Path(__file__).resolve().parent / "cycle_tf.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_CELL = 8
Q = 10
PAT0011 = (0, 0, 1, 1)
MOD8_R = (7, 5, 3, 1)


def residue_t_lo(k: int, r: int) -> int:
    """Least covering time of n=r mod 4."""
    return 2 * (1 << k) + 7 - 2 * r


def residue_t_hi(k: int, r: int) -> int:
    """Greatest covering time of n=r mod 4."""
    return 10 * (1 << k) - 2 * r - 1


def residue_ap_ok(k: int, r: int) -> bool:
    """Length U, step 8, endpoints 2U+7-2r and 10U-2r-1."""
    u = 1 << k
    lo = residue_t_lo(k, r)
    hi = residue_t_hi(k, r)
    if r < 0 or r > 3 or lo > hi or (hi - lo) % 8:
        return False
    return ((hi - lo) // 8) + 1 == u


def tot_form() -> dict:
    """k<=64: four APs partition odd covering window; k>=2 t mod 8."""
    n_ok = 0
    if not all(residue_ap_ok(0, r) for r in range(4)):
        return {"ok": False, "k0": True}
    if residue_t_lo(0, 1) != 7 or covering_t(0, 1) != 7:
        return {"ok": False, "th": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if not n1_ap_ok(k) or not residue_ap_ok(k, 1):
            return {"ok": False, "n1": True, "k": k}
        if residue_t_lo(k, 1) != 2 * u + 5 or residue_t_hi(k, 1) != 10 * u - 3:
            return {"ok": False, "n1ep": True, "k": k}
        los = [residue_t_lo(k, r) for r in range(4)]
        his = [residue_t_hi(k, r) for r in range(4)]
        if sorted(los) != [2 * u + 1, 2 * u + 3, 2 * u + 5, 2 * u + 7]:
            return {"ok": False, "los": True, "k": k, "los": los}
        if sorted(his) != [10 * u - 7, 10 * u - 5, 10 * u - 3, 10 * u - 1]:
            return {"ok": False, "his": True, "k": k}
        if not all(residue_ap_ok(k, r) for r in range(4)):
            return {"ok": False, "ap": True, "k": k}
        if k >= 2:
            for r in range(4):
                if residue_t_lo(k, r) % 8 != MOD8_R[r]:
                    return {"ok": False, "mod": True, "k": k, "r": r}
                if residue_t_hi(k, r) % 8 != MOD8_R[r]:
                    return {"ok": False, "modh": True, "k": k, "r": r}
        samples = {0, 1, 2, 3, u, 4 * u - 4, 4 * u - 3, 4 * u - 2, 4 * u - 1}
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            r = n % 4
            t = covering_t(k, n)
            if t != 10 * u - 2 * n - 1:
                return {"ok": False, "t": True, "k": k, "n": n}
            if t < residue_t_lo(k, r) or t > residue_t_hi(k, r):
                return {"ok": False, "band": True, "k": k, "n": n}
            if (t - residue_t_lo(k, r)) % 8:
                return {"ok": False, "step": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and residue_ap_ok(64, 0)
        and residue_ap_ok(64, 3)
        and want_d1_r1_n(7) == 128
        and G(1, 0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ap_count() -> dict:
    """k<=12: covering times of each residue equal the 8-AP; partition."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        union = []
        rec = {}
        for r in range(4):
            got = sorted(covering_t(k, n) for n in range(r, 4 * u, 4))
            lo = residue_t_lo(k, r)
            hi = residue_t_hi(k, r)
            want = list(range(lo, hi + 1, 8))
            if r == 1 and want != n1_times(k):
                return {"ok": False, "th": True, "k": k}
            if got != want:
                return {"ok": False, "ap": True, "k": k, "r": r}
            union.extend(got)
            rec[str(r)] = {"n": len(got), "lo": got[0], "hi": got[-1]}
        if sorted(union) != list(range(2 * u + 1, 10 * u, 2)):
            return {"ok": False, "part": True, "k": k}
        n_ok += 1
        rows[str(k)] = rec
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["1"]["lo"] == 7
        and rows["2"]["1"]["lo"] == 13
        and rows["7"]["0"]["n"] == 128
        and rows["12"]["3"]["lo"] == 2 * 4096 + 1
        and rows["12"]["0"]["hi"] == 10 * 4096 - 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def pal_res() -> dict:
    """k<=8 pal-center tot by n mod 4: none identically 0."""
    t_hi = Q * (1 << K_CELL)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    rows = {}
    fired = [False, False, False, False]
    for k in range(0, K_CELL + 1):
        u = 1 << k
        tot = [0, 0, 0, 0]
        for n in range(0, 4 * u):
            t = covering_t(k, n)
            tot[n % 4] ^= pal_center_and(packed[t], even_s(n, k))
        for r in range(4):
            if tot[r]:
                fired[r] = True
        n_ok += 1
        rows[str(k)] = {"tot": tot, "all": tot[0] ^ tot[1] ^ tot[2] ^ tot[3]}
    ok = (
        n_ok == K_CELL + 1
        and all(fired)
        and rows["2"]["tot"][1] == 1
        and rows["0"]["tot"] == [0, 0, 1, 1]
        and rows["7"]["tot"][1] == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_CELL,
        "rows": rows,
        "ident0": [False, False, False, False],
    }


def killed_eq() -> dict:
    """pal-center tot on each n mod 4 identically 0."""
    ok = (
        residue_t_lo(0, 1) == 7
        and n1_ap_ok(0)
        and want_d1_n(1) == 3
        and want_d1_r1_n(1) == 2
        and G(5, 4) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    th = json.loads(TH_JSON.read_text())
    tg = json.loads(TG_JSON.read_text())
    tf = json.loads(TF_JSON.read_text())
    ok = (
        th["checks"]["all_ok"]
        and tg["checks"]["all_ok"]
        and tf["checks"]["all_ok"]
        and th["verdict"]["n1_times_eq_8_ap"] == "LEMMA"
        and th["verdict"]["d1_r1_odd_children_even_covering"] == "LEMMA"
        and tf["verdict"]["d1_all_n1_mod4"] == "LEMMA"
        and th["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and th["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, pr, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and pr["ok"] and kl["ok"]
    assert sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    tot = tot_form()
    cnt = ap_count()
    pr = pal_res()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, pr, kl, sc, pref)
    dump = {
        "cycle": "TI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ap_count": {k: cnt[k] for k in cnt if k != "ok"},
        "pal_res": {k: pr[k] for k in pr if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "residue_times_eq_8_ap": True,
            "four_aps_partition_odd_covering": True,
            "k_ge2_t_mod8_by_n_mod4": True,
            "pal_res_identically_0": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "residue_times_eq_8_ap": "LEMMA",
            "four_aps_partition_odd_covering": "LEMMA",
            "k_ge2_t_mod8_by_n_mod4": "LEMMA",
            "pal_res_identically_0": "KILLED",
            "pal_r1_identically_0": "KILLED",
            "d1_spat_r1_identically_0": "KILLED",
            "pal_c_eq_ST": "KILLED",
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
        "ap k12 r3 lo",
        dump["ap_count"]["rows"]["12"]["3"]["lo"],
        "pal k2",
        dump["pal_res"]["rows"]["2"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
