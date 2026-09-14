#!/usr/bin/env python3
"""Cycle UB: odd-n even-j unpaired is parent unpaired xor plus clip-edge.

G(2m+1,2r)=G(m,r) xor G(m,r-1) (Cycle TW). pair+g0 children stay
pal-pairs (leftover extra). Clip-edge pal-pair at r>=1 with
G(m,r-1)=0 has child partner past clip; that g0+pair count is
(J_{k+1}-1)/2 for k>=2. The rest is parent unpaired xor plus j=0
unpaired (Cycle UA). Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ub.py --certify
Dump: research/cycle_ub.json
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
from cycle_tw import green_odd_even
from cycle_tz import unp_j_split
from cycle_ua import want_j0_odd_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"
TW_JSON = Path(__file__).resolve().parent / "cycle_tw.json"
TZ_JSON = Path(__file__).resolve().parent / "cycle_tz.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_clip_gp(k: int) -> int:
    """g0+pair unpaired extra: 0 at k<=1, (J_{k+1}-1)/2 for k>=2."""
    if k <= 1:
        return 0
    return (jacobsthal(k + 1) - 1) // 2


def unpaired_xor_split(k: int) -> dict:
    """Odd-n even-j unpaired: parent xor kinds."""
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    extra = n_xor = n_ug = n_gu = n_gp = n_pg = n_neg = n_bad = 0
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "unp":
                continue
            if j >= n:
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
            if km == "unp" and kr == "g0":
                n_ug += 1
            elif km == "g0" and kr == "unp":
                n_gu += 1
            elif km == "g0" and kr == "pair":
                if is_clip_edge(m, r, k_p):
                    n_gp += 1
                else:
                    n_bad += 1
            elif km == "pair" and kr == "g0":
                n_pg += 1
            else:
                n_bad += 1
    return {
        "extra": extra,
        "n_xor": n_xor,
        "n_ug": n_ug,
        "n_gu": n_gu,
        "n_gp": n_gp,
        "n_pg": n_pg,
        "n_neg": n_neg,
        "n_bad": n_bad,
    }


def tot_form() -> dict:
    """k<=64: J odd; clip-gp half; j=0 unpaired; Green xor samples."""
    n_ok = 0
    if want_clip_gp(0) != 0 or want_clip_gp(1) != 0:
        return {"ok": False, "k01": True}
    if want_clip_gp(2) != 1 or want_clip_gp(3) != 2:
        return {"ok": False, "k23": True}
    if want_j0_odd_unp(0) != 1 or want_j0_odd_unp(2) != 3:
        return {"ok": False, "j0": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 1 and jacobsthal(k) % 2 != 1:
            return {"ok": False, "Jodd": True, "k": k}
        if k >= 2:
            if want_clip_gp(k) * 2 + 1 != jacobsthal(k + 1):
                return {"ok": False, "half": True, "k": k}
            if want_edge_n(k - 1) != jacobsthal(k + 1):
                return {"ok": False, "ed": True, "k": k}
            if want_clip_gp(k) != (want_edge_n(k - 1) - 1) // 2:
                return {"ok": False, "edh": True, "k": k}
        if k >= 3 and want_j0_odd_unp(k) != 2 * want_j0_odd_unp(k - 1):
            return {"ok": False, "j0r": True, "k": k}
        if k >= 2:
            m = 5 * (1 << (k - 2))
            if pal_kind(m, 0, k - 1) != "pair" or not is_clip_edge(m, 0, k - 1):
                return {"ok": False, "r0": True, "k": k, "m": m}
            if 2 * m != 5 * (1 << (k - 1)):
                return {"ok": False, "clip0": True, "k": k}
        if k >= 1:
            u_p = 1 << (k - 1)
            clip_p = 5 * u_p
            clip = 5 * u
            samples_m = {0, 1, u_p, 2 * u_p, 3 * u_p, 4 * u_p - 1}
            for m in samples_m:
                if m >= 4 * u_p:
                    continue
                n = 2 * m + 1
                rs = {0, m}
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
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_unp_rec_killed()
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def want_unp_rec_killed() -> bool:
    """pair+g0 empty; extra is not xor-unp alone."""
    return want_clip_gp(2) == 1 and want_clip_gp(1) == 0


def unpaired_xor_fold() -> dict:
    """k<=8: extra = unp xor + clip-gp + j0; pair+g0 empty."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        js = unp_j_split(k)
        extra = js["unp_o"] - js["unp_oj"]
        xs = unpaired_xor_split(k)
        if xs["extra"] != extra:
            return {"ok": False, "ex": True, "k": k, **xs, "extra_js": extra}
        if xs["n_bad"] != 0 or xs["n_xor"] != xs["extra"]:
            return {"ok": False, "xor": True, "k": k, **xs}
        if xs["n_pg"] != 0:
            return {"ok": False, "pg": True, "k": k, **xs}
        if xs["n_gp"] != want_clip_gp(k):
            return {"ok": False, "gp": True, "k": k, **xs}
        if xs["n_neg"] != want_j0_odd_unp(k):
            return {"ok": False, "j0": True, "k": k, "n_neg": xs["n_neg"]}
        parts = xs["n_ug"] + xs["n_gu"] + xs["n_gp"] + xs["n_neg"]
        if parts != xs["extra"]:
            return {"ok": False, "kind": True, "k": k, **xs}
        if k >= 2 and xs["extra"] == xs["n_ug"] + xs["n_gu"]:
            return {"ok": False, "xoronly": True, "k": k}
        if extra == 0:
            return {"ok": False, "empty": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "extra": xs["extra"],
            "n_ug": xs["n_ug"],
            "n_gu": xs["n_gu"],
            "n_gp": xs["n_gp"],
            "n_neg": xs["n_neg"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["extra"] == 1
        and rows["1"]["extra"] == 1
        and rows["2"]["n_gp"] == 1
        and rows["2"]["n_neg"] == 3
        and rows["8"]["extra"] == 10019
        and rows["8"]["n_gp"] == 85
        and rows["8"]["n_neg"] == 192
        and rows["8"]["extra"]
        != rows["8"]["n_ug"] + rows["8"]["n_gu"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired extra xor-only; pair+g0 nonempty; G(2m+1,2r)=G(m,r)."""
    ok = (
        want_clip_gp(2) != 0
        and want_clip_gp(8) == 85
        and green_odd_even(1, 1) != G(1, 1)
        and want_j0_odd_unp(2) == 3
        and unp_j_split(1)["unp_o"] - unp_j_split(1)["unp_oj"] == 1
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
    ua = json.loads(UA_JSON.read_text())
    tw = json.loads(TW_JSON.read_text())
    tz = json.loads(TZ_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        ua["checks"]["all_ok"]
        and tw["checks"]["all_ok"]
        and tz["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and ua["verdict"]["unp_rec_2prev_J_extra_k_ge_1"] == "LEMMA"
        and ua["verdict"]["j0_odd_unp_eq_3_2km2"] == "LEMMA"
        and tw["verdict"]["odd_ej_lo_from_parent_pair_xor"] == "LEMMA"
        and tw["verdict"]["G_odd_even_eq_adj_xor"] == "LEMMA"
        and tz["verdict"]["oddj_unp_eq_parent_unp_plus_J_k1"] == "LEMMA"
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and ua["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ua["verdict"]["prize"] == "unsolved"
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
    cnt = unpaired_xor_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "unpaired_xor_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_ej_unp_from_unp_xor_plus_clip": True,
            "clip_gp_eq_half_J_k1_k_ge_2": True,
            "pair_g0_empty_in_unp_extra": True,
            "unp_extra_eq_xor_unp_alone": False,
            "unp_extra_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_ej_unp_from_unp_xor_plus_clip": "LEMMA",
            "clip_gp_eq_half_J_k1_k_ge_2": "LEMMA",
            "pair_g0_empty_in_unp_extra": "LEMMA",
            "unp_extra_eq_xor_unp_alone": "KILLED",
            "pair_g0_in_unp_extra": "KILLED",
            "unp_extra_empty": "KILLED",
            "unp_eq_2_even_plus_extra": "KILLED",
            "unp_eq_2_parent_unp": "KILLED",
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
        dump["unpaired_xor_fold"]["rows"]["8"]["extra"],
        "gp",
        dump["unpaired_xor_fold"]["rows"]["8"]["n_gp"],
        "j0",
        dump["unpaired_xor_fold"]["rows"]["8"]["n_neg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
