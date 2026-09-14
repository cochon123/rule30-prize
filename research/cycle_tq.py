#!/usr/bin/env python3
"""Cycle TQ: d=2 pal-pair rest tot equals raw tot for all k.

Even d=2 pal-pairs never meet a forced column. Odd d=2 meets
forced pal-right only at k=2: n=11 at p=14, and n=15 at p=6
and p=14. Those ANDs xor to 0, so d=2 rest tot equals raw tot
for all k. Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk leftover d catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tq.py --certify
Dump: research/cycle_tq.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import packed_p
from cycle_sv import forced_right_j, pal_left_never_forced, unique_even_n
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_te import want_d2_n, want_d2_parity_n
from cycle_tl import d2_v2
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TP_JSON = Path(__file__).resolve().parent / "cycle_tp.json"
TO_JSON = Path(__file__).resolve().parent / "cycle_to.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
T_FREEZE = 18
PAT0011 = (0, 0, 1, 1)


def want_odd_d2_forced(k: int) -> list[tuple[int, int]]:
    """Odd covering d=2 cells with a forced side: (n, p), sorted."""
    if k == 2:
        return [(11, 14), (15, 6), (15, 14)]
    return []


def want_even_d2_forced(k: int) -> list[tuple[int, int]]:
    """Even covering d=2 cells with a forced side: empty."""
    return []


def d2_forced_hits(k: int, parity: int) -> list[tuple[int, int]]:
    """Covering n of given parity with d=2 and a side j forced."""
    u = 1 << k
    cap = 4 * u
    hits: list[tuple[int, int]] = []
    for p in (4, 6, 14):
        j = forced_right_j(p, k)
        for n in (j - 2, j + 2):
            if n < 2 or n >= cap or n % 2 != parity:
                continue
            if d2_v2(n):
                hits.append((n, p))
    hits.sort()
    return hits


def tot_form() -> dict:
    """k<=64: even d=2 empty forced; odd only k=2; unique even d=2U."""
    n_ok = 0
    if want_odd_d2_forced(2) != [(11, 14), (15, 6), (15, 14)]:
        return {"ok": False, "base": True}
    if covering_t(2, 11) != 17 or covering_t(2, 15) != 9:
        return {"ok": False, "t": True}
    if packed_p(13, 2) != 14 or packed_p(17, 2) != 6:
        return {"ok": False, "p": True}
    if d2_v2(11) != 1 or d2_v2(15) != 1 or d2_v2(6) != 0:
        return {"ok": False, "v2": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        got_e = d2_forced_hits(k, 0)
        got_o = d2_forced_hits(k, 1)
        if got_e != want_even_d2_forced(k):
            return {"ok": False, "even": True, "k": k, "got": got_e}
        if got_o != want_odd_d2_forced(k):
            return {"ok": False, "odd": True, "k": k, "got": got_o}
        if k >= 1:
            n_u = unique_even_n(k)
            j_u = forced_right_j(4, k)
            if n_u - j_u != -2 * u and j_u - n_u != 2 * u:
                return {"ok": False, "ud": True, "k": k}
            if abs(n_u - j_u) == 2:
                return {"ok": False, "ud2": True, "k": k}
        for n, p in got_o:
            if pal_kind(n, n - 2, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            if packed_p(n - 2, k) != p and packed_p(n + 2, k) != p:
                return {"ok": False, "side": True, "k": k, "n": n, "p": p}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d2_parity_n(2) == 3
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and 4 in FORCED
        and 6 in FORCED
        and 14 in FORCED
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def freeze_and() -> dict:
    """k=2 odd d=2 times: AND(9,6)=1, AND(9,14)=0, AND(17,14)=1."""
    row = 1
    got: dict[int, dict[str, int]] = {}
    for t in range(0, T_FREEZE):
        if t in (9, 17):
            got[t] = {
                "and6": bit_at(row, 5) & bit_at(row, 6),
                "and14": bit_at(row, 13) & bit_at(row, 14),
            }
        row = rule30_step(row)
    corr = got[9]["and6"] ^ got[9]["and14"] ^ got[17]["and14"]
    ok = (
        got[9]["and6"] == 1
        and got[9]["and14"] == 0
        and got[17]["and14"] == 1
        and corr == 0
        and covering_t(2, 15) == 9
        and covering_t(2, 11) == 17
        and and_clause(0, 0, 0, 1) == 0
    )
    return {
        "ok": ok,
        "t9_and6": got[9]["and6"],
        "t9_and14": got[9]["and14"],
        "t17_and14": got[17]["and14"],
        "corr": corr,
    }


def d2_forced_count() -> dict:
    """k<=12: even d=2 empty forced; odd only the k=2 triple."""
    n_ok = 0
    n_hit_e = 0
    n_hit_o = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        hits_e: list[tuple[int, int]] = []
        hits_o: list[tuple[int, int]] = []
        n_e = n_o = 0
        for n in range(0, 4 * u):
            if n < 2 or not d2_v2(n):
                continue
            if pal_kind(n, n - 2, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            if n % 2 == 0:
                n_e += 1
            else:
                n_o += 1
            for j in (n - 2, n + 2):
                if j < 0:
                    continue
                p = packed_p(j, k)
                if p in FORCED:
                    rec = (n, p)
                    if n % 2 == 0:
                        if rec not in hits_e:
                            hits_e.append(rec)
                    elif rec not in hits_o:
                        hits_o.append(rec)
        hits_e.sort()
        hits_o.sort()
        if n_e != want_d2_parity_n(k) or n_o != want_d2_parity_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_e": n_e,
                "n_o": n_o,
                "want": want_d2_parity_n(k),
            }
        if hits_e != want_even_d2_forced(k) or hits_e != d2_forced_hits(k, 0):
            return {"ok": False, "even": True, "k": k, "hits": hits_e}
        if hits_o != want_odd_d2_forced(k) or hits_o != d2_forced_hits(k, 1):
            return {"ok": False, "odd": True, "k": k, "hits": hits_o}
        n_hit_e += len(hits_e)
        n_hit_o += len(hits_o)
        n_ok += 1
        rows[str(k)] = {"n_e": n_e, "n_o": n_o, "n_fr_e": len(hits_e), "n_fr_o": len(hits_o)}
    ok = (
        n_ok == K_COUNT + 1
        and n_hit_e == 0
        and n_hit_o == 3
        and rows["2"]["n_fr_o"] == 3
        and rows["12"]["n_e"] == 2731
        and rows["12"]["n_fr_e"] == 0
        and rows["12"]["n_fr_o"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_hit_e": n_hit_e,
        "n_hit_o": n_hit_o,
        "k_hi": K_COUNT,
        "rows": rows,
    }


def killed_eq() -> dict:
    """odd d=2 never forced all k; d=2 rest equals raw cellwise."""
    ok = (
        want_odd_d2_forced(2) == [(11, 14), (15, 6), (15, 14)]
        and not want_odd_d2_forced(3)
        and not want_even_d2_forced(2)
        and d2_v2(11) == 1
        and d2_v2(15) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tp = json.loads(TP_JSON.read_text())
    to = json.loads(TO_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    ok = (
        tp["checks"]["all_ok"]
        and to["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and tp["verdict"]["d1_forced_two_cells"] == "LEMMA"
        and tp["verdict"]["d1_rest_eq_raw_xor_k_le_1"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and tp["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tp["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d2_n(0) == 2
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, frz, cnt, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and frz["ok"] and cnt["ok"] and kl["ok"]
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
    frz = freeze_and()
    cnt = d2_forced_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, frz, cnt, kl, sc, pref)
    dump = {
        "cycle": "TQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "freeze_and": {k: frz[k] for k in frz if k != "ok"},
        "d2_forced_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_d2_never_forced": True,
            "odd_d2_forced_only_k2": True,
            "odd_d2_forced_corr_0": True,
            "d2_rest_eq_raw_tot_all_k": True,
            "odd_d2_never_forced_all_k": False,
            "d2_rest_eq_raw_cellwise": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_d2_never_forced": "LEMMA",
            "odd_d2_forced_only_k2": "LEMMA",
            "odd_d2_forced_corr_0": "LEMMA",
            "d2_rest_eq_raw_tot_all_k": "LEMMA",
            "odd_d2_never_forced_all_k": "KILLED",
            "d2_rest_eq_raw_cellwise": "KILLED",
            "d1_never_forced_all_k": "KILLED",
            "d1_rest_eq_raw_all_k": "KILLED",
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
        "n_hit_o",
        dump["d2_forced_count"]["n_hit_o"],
        "k12_e",
        dump["d2_forced_count"]["rows"]["12"]["n_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
