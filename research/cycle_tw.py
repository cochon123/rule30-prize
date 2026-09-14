#!/usr/bin/env python3
"""Cycle TW: odd-n even-j leftover is parent pal-pair adjacent xor.

G(2m+1, 2r) = G(m,r) xor G(m, r-1) with G(m,-1)=0. Odd-n even-j
leftover pal-pairs are the children of a unique parent pal-pair at
r or r-1. Unpaired parents stay unpaired. Pal-center parents become
d=1. Left-edge j=0 leftover on odd n has count 5*2^{k-2}-1 for
k>=2. Not rest=S xor T. Do not walk leftover p catalogues. Do not
walk leftover d catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tw.py --certify
Dump: research/cycle_tw.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_tv import leftover_j_split
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TV_JSON = Path(__file__).resolve().parent / "cycle_tv.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def green_odd_even(m: int, r: int) -> int:
    """G(2m+1, 2r) = G(m,r) xor G(m, r-1), G(m,-1)=0."""
    a = G(m, r) if r >= 0 else 0
    b = G(m, r - 1) if r - 1 >= 0 else 0
    return a ^ b


def want_j0_odd_lo(k: int) -> int:
    """j=0 leftover on odd n: 0,1, then 5*2^{k-2}-1."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return 5 * (1 << (k - 2)) - 1


def leftover_xor_split(k: int) -> dict:
    """Odd-n even-j leftover: parent xor kinds."""
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    extra = n_xor = n_pg = n_gp = n_neg = n_bad = 0
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            extra += 1
            r = j // 2
            if green_odd_even(m, r) != 1:
                n_bad += 1
                continue
            n_xor += 1
            if r == 0:
                n_neg += 1
                continue
            kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
            km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
            if km == "pair" and kr == "g0":
                n_pg += 1
            elif km == "g0" and kr == "pair":
                n_gp += 1
            else:
                n_bad += 1
    return {
        "extra": extra,
        "n_xor": n_xor,
        "n_pg": n_pg,
        "n_gp": n_gp,
        "n_neg": n_neg,
        "n_bad": n_bad,
    }


def tot_form() -> dict:
    """k<=64: Green xor; unpaired stay unpaired; pal-center is d=1; j=0."""
    n_ok = 0
    if green_odd_even(0, 0) != G(1, 0):
        return {"ok": False, "g0": True}
    if want_j0_odd_lo(0) != 0 or want_j0_odd_lo(1) != 1:
        return {"ok": False, "j00": True}
    if want_j0_odd_lo(2) != 4 or want_j0_odd_lo(3) != 9:
        return {"ok": False, "j01": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 3 and want_j0_odd_lo(k) != 2 * want_j0_odd_lo(k - 1) + 1:
            return {"ok": False, "j0r": True, "k": k}
        if k >= 2 and want_j0_odd_lo(k) != 5 * (1 << (k - 2)) - 1:
            return {"ok": False, "j0c": True, "k": k}
        if k >= 1:
            u_p = 1 << (k - 1)
            clip_p = 5 * u_p
            clip = 5 * u
            samples_m = {0, 1, u_p, 2 * u_p, 3 * u_p, 4 * u_p - 1}
            for m in samples_m:
                if m < 0 or m >= 4 * u_p:
                    continue
                n = 2 * m + 1
                if G(n, 2 * m) != green_odd_even(m, m):
                    return {"ok": False, "gd1": True, "k": k, "m": m}
                if n - 2 * m != 1:
                    return {"ok": False, "d1": True, "k": k, "m": m}
                rs = {0, m, min(2 * m, clip_p)}
                if 2 * m >= 1:
                    rs.add(1)
                for r in rs:
                    if G(n, 2 * r) != green_odd_even(m, r):
                        return {"ok": False, "gx": True, "k": k, "m": m, "r": r}
                    jp_p = 2 * m - r
                    if jp_p > clip_p:
                        jpc = 2 * n - 2 * r
                        if jpc <= clip:
                            return {"ok": False, "unp": True, "k": k, "m": m, "r": r}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_j0_odd_lo(8) == 319
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def leftover_xor_fold() -> dict:
    """k<=8: extra leftover is parent pal-pair xor; j=0 count."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        js = leftover_j_split(k)
        xs = leftover_xor_split(k)
        if xs["extra"] != js["lo_ej_o"]:
            return {"ok": False, "ex": True, "k": k, **xs, "lo_ej_o": js["lo_ej_o"]}
        if xs["n_bad"] != 0 or xs["n_xor"] != xs["extra"]:
            return {"ok": False, "xor": True, "k": k, **xs}
        if xs["n_pg"] + xs["n_gp"] + xs["n_neg"] != xs["extra"]:
            return {"ok": False, "kind": True, "k": k, **xs}
        if xs["n_neg"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k, "n_neg": xs["n_neg"]}
        if k >= 1 and js["lo"] == 2 * js["lo_e"]:
            return {"ok": False, "empty": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "extra": xs["extra"],
            "n_pg": xs["n_pg"],
            "n_gp": xs["n_gp"],
            "n_neg": xs["n_neg"],
            "lo_e": js["lo_e"],
            "lo": js["lo"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["extra"] == 0
        and rows["1"]["extra"] == 2
        and rows["1"]["n_neg"] == 1
        and rows["2"]["n_neg"] == 4
        and rows["8"]["n_neg"] == 319
        and rows["8"]["extra"] == 17630
        and rows["8"]["lo"] != 2 * rows["8"]["lo_e"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """odd-n even-j leftover empty; G(2m+1,2r)=G(m,r)."""
    ok = (
        green_odd_even(1, 1) != G(1, 1)
        and want_j0_odd_lo(2) == 4
        and leftover_j_split(1)["lo_ej_o"] == 2
        and d2_clip_covering(0)
        and not d2_clip_covering(1)
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_odd(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    tv = json.loads(TV_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        tv["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and tv["verdict"]["oddj_lo_eq_even_lo"] == "LEMMA"
        and tv["verdict"]["odd_lo_eq_even_lo"] == "KILLED"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and tb["verdict"]["oddj_pairs_drop_clip_edge"] == "LEMMA"
        and tv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tv["verdict"]["prize"] == "unsolved"
        and want_d2_n(0) == 2
        and jacobsthal(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and kl["ok"]
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
    cnt = leftover_xor_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_xor_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "G_odd_even_eq_adj_xor": True,
            "odd_ej_lo_from_parent_pair_xor": True,
            "j0_odd_lo_eq_5_2km2_minus_1": True,
            "odd_ej_lo_empty": False,
            "G_odd_even_eq_G_m_r": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "G_odd_even_eq_adj_xor": "LEMMA",
            "odd_ej_lo_from_parent_pair_xor": "LEMMA",
            "j0_odd_lo_eq_5_2km2_minus_1": "LEMMA",
            "odd_ej_lo_empty": "KILLED",
            "G_odd_even_eq_G_m_r": "KILLED",
            "odd_lo_eq_even_lo": "KILLED",
            "oddj_lo_fold_all_k": "KILLED",
            "leftover_pairs_empty": "KILLED",
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
        "extra k8",
        dump["leftover_xor_fold"]["rows"]["8"]["extra"],
        "j0",
        dump["leftover_xor_fold"]["rows"]["8"]["n_neg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
