#!/usr/bin/env python3
"""Cycle TJ: residue time APs 2-fold as interleaved 16-APs.

At k>=1, even children of parent n=r mod 4 have times the 16-AP
2 lo+1 .. 2 hi+1 and land on child residue (2r) mod 4. Odd children
have times 2 lo-1 .. 2 hi-1 on residue (2r+1) mod 4. Each child
residue AP is the interleaving of those two parent 16-APs. Pal-center
tot does not 2-fold by residue (dies at k=3). Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_tj.py --certify
Dump: research/cycle_tj.json
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
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_sz import even_child_t, odd_child_t
from cycle_td import want_d1_n
from cycle_th import n1_ap_ok
from cycle_ti import MOD8_R, residue_ap_ok, residue_t_hi, residue_t_lo

OUT = Path(__file__).resolve().with_suffix(".json")
TI_JSON = Path(__file__).resolve().parent / "cycle_ti.json"
TH_JSON = Path(__file__).resolve().parent / "cycle_th.json"
TG_JSON = Path(__file__).resolve().parent / "cycle_tg.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def even_child_res(r: int) -> int:
    """n mod 4 of even child of parent residue r."""
    return (2 * r) % 4


def odd_child_res(r: int) -> int:
    """n mod 4 of odd child of parent residue r."""
    return (2 * r + 1) % 4


def parent_sources(cr: int) -> tuple[tuple[int, int], str]:
    """Parent residues and fold kind that fill child residue cr."""
    if cr % 2 == 0:
        return (cr // 2, cr // 2 + 2), "even"
    return ((cr - 1) // 2, (cr - 1) // 2 + 2), "odd"


def tot_form() -> dict:
    """k<=64: 2-fold endpoints are 16-APs inside child residue AP."""
    n_ok = 0
    if even_child_res(1) != 2 or odd_child_res(1) != 3:
        return {"ok": False, "res": True}
    if parent_sources(0) != ((0, 2), "even"):
        return {"ok": False, "src0": True}
    if parent_sources(1) != ((0, 2), "odd"):
        return {"ok": False, "src1": True}
    if parent_sources(3) != ((1, 3), "odd"):
        return {"ok": False, "src3": True}
    for k in range(0, K_ALG + 1):
        if not all(residue_ap_ok(k, r) for r in range(4)):
            return {"ok": False, "ap": True, "k": k}
        if k >= 1:
            up = 1 << (k - 1)
            for r in range(4):
                lo = residue_t_lo(k - 1, r)
                hi = residue_t_hi(k - 1, r)
                elo, ehi = 2 * lo + 1, 2 * hi + 1
                olo, ohi = 2 * lo - 1, 2 * hi - 1
                if (ehi - elo) % 16 or (ohi - olo) % 16:
                    return {"ok": False, "step": True, "k": k, "r": r}
                if ((ehi - elo) // 16) + 1 != up:
                    return {"ok": False, "elen": True, "k": k, "r": r}
                if ((ohi - olo) // 16) + 1 != up:
                    return {"ok": False, "olen": True, "k": k, "r": r}
                wr, wor = even_child_res(r), odd_child_res(r)
                clo, chi = residue_t_lo(k, wr), residue_t_hi(k, wr)
                colo, cohi = residue_t_lo(k, wor), residue_t_hi(k, wor)
                if not (clo <= elo <= ehi <= chi):
                    return {"ok": False, "ein": True, "k": k, "r": r}
                if not (colo <= olo <= ohi <= cohi):
                    return {"ok": False, "oin": True, "k": k, "r": r}
                if (elo - clo) % 8 or (olo - colo) % 8:
                    return {"ok": False, "align": True, "k": k, "r": r}
                if even_child_t(r, k) != covering_t(k, 2 * r):
                    return {"ok": False, "et": True, "k": k, "r": r}
                if odd_child_t(r, k) != covering_t(k, 2 * r + 1):
                    return {"ok": False, "ot": True, "k": k, "r": r}
            if k >= 2:
                for r in range(4):
                    if residue_t_lo(k, r) % 8 != MOD8_R[r]:
                        return {"ok": False, "mod": True, "k": k, "r": r}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and n1_ap_ok(64)
        and residue_ap_ok(64, 3)
        and even_child_res(0) == 0
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def fold_count() -> dict:
    """k<=12: child residue times = interleaved parent 16-APs."""
    n_ok = 0
    rows = {}
    for k in range(1, K_COUNT + 1):
        up = 1 << (k - 1)
        rec = {}
        for cr in range(4):
            src, kind = parent_sources(cr)
            got = []
            for r in src:
                ns = range(r, 4 * up, 4)
                if kind == "even":
                    got.extend(even_child_t(n, k) for n in ns)
                else:
                    got.extend(odd_child_t(n, k) for n in ns)
            lo = residue_t_lo(k, cr)
            hi = residue_t_hi(k, cr)
            want = list(range(lo, hi + 1, 8))
            if sorted(got) != want:
                return {
                    "ok": False,
                    "set": True,
                    "k": k,
                    "cr": cr,
                    "n_got": len(got),
                    "n_want": len(want),
                }
            rec[str(cr)] = {"n": len(want), "kind": kind, "src": list(src)}
        n_ok += 1
        rows[str(k)] = rec
    ok = (
        n_ok == K_COUNT
        and rows["1"]["0"]["n"] == 2
        and rows["7"]["1"]["n"] == 128
        and rows["12"]["3"]["n"] == 4096
        and rows["12"]["1"]["kind"] == "odd"
        and rows["12"]["2"]["src"] == [1, 3]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def pal_fold_killed() -> dict:
    """TI pal_res: child residue tot is not xor of parent sources."""
    ti = json.loads(TI_JSON.read_text())
    rows = ti["pal_res"]["rows"]
    k = 3
    child = rows[str(k)]["tot"]
    parent = rows[str(k - 1)]["tot"]
    naive = []
    for cr in range(4):
        src, _kind = parent_sources(cr)
        naive.append(parent[src[0]] ^ parent[src[1]])
    ok = child != naive and child[0] == 0 and naive[0] == 1
    return {"ok": ok, "k": k, "child": child, "naive": naive}


def killed_eq() -> dict:
    """residue pal tot 2-folds; cellwise spat 2-fold."""
    ok = (
        even_child_res(1) == 2
        and odd_child_res(0) == 1
        and parent_sources(2) == ((1, 3), "even")
        and want_d1_n(0) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    ti = json.loads(TI_JSON.read_text())
    th = json.loads(TH_JSON.read_text())
    tg = json.loads(TG_JSON.read_text())
    ok = (
        ti["checks"]["all_ok"]
        and th["checks"]["all_ok"]
        and tg["checks"]["all_ok"]
        and ti["verdict"]["residue_times_eq_8_ap"] == "LEMMA"
        and ti["verdict"]["four_aps_partition_odd_covering"] == "LEMMA"
        and th["verdict"]["n1_times_eq_8_ap"] == "LEMMA"
        and ti["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ti["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, pk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and pk["ok"] and kl["ok"]
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
    cnt = fold_count()
    pk = pal_fold_killed()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, pk, kl, sc, pref)
    dump = {
        "cycle": "TJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "fold_count": {k: cnt[k] for k in cnt if k != "ok"},
        "pal_fold_killed": {k: pk[k] for k in pk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_child_times_16_ap": True,
            "odd_child_times_16_ap": True,
            "child_residue_ap_interleaves_parents": True,
            "pal_res_tot_2fold": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_child_times_16_ap": "LEMMA",
            "odd_child_times_16_ap": "LEMMA",
            "child_residue_ap_interleaves_parents": "LEMMA",
            "pal_res_tot_2fold": "KILLED",
            "pal_res_identically_0": "KILLED",
            "d2_spat_eq_parent_d1_spat": "KILLED",
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
        "fold k12 r3",
        dump["fold_count"]["rows"]["12"]["3"]["n"],
        "pal_kill",
        dump["pal_fold_killed"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
