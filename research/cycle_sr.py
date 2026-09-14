#!/usr/bin/env python3
"""Cycle SR: even-n clip-unpaired G=1 never packed-AND through k<=10.

Palindrome pairs of even-n clipped G=1 cancel, and there are 2^{k+1}
pal-centers (all clipped, each G=1), so even-n clipped G=1 xor equals
the xor of clip-unpaired cells. Those unpaired cells are pal-left
j<2n-5U on even n>5U/2; their pal-partner has negative packed p.
Packed AND vanishes on them through k<=10, so even-n rest tot is
pal-center AND xor pal-pair AND-mismatch. That is the even-n
obstruction to Green-only rest, not rest=S xor T. Do not claim
unpaired silence for all k. Do not walk leftover p catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_sr.py --certify
Dump: research/cycle_sr.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_qw import want_g1_even, want_green_even
from cycle_so import want_even
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
SO_JSON = Path(__file__).resolve().parent / "cycle_so.json"
SQ_JSON = Path(__file__).resolve().parent / "cycle_sq.json"

N_PAL = 64
M_SLOTS = 64
K_GREEN = 8
K_REST = 10
K_ALG = 64
Q = 10


def pal_center_count(k: int) -> int:
    """Even n in the q=10 covering window: 2U = 2^{k+1}."""
    return 1 << (k + 1)


def _green_even_pal(k: int) -> dict:
    """Clipped even-n G=1 split: pal-center, pal-pair, clip-unpaired."""
    U = 1 << k
    clip = 5 * U
    g1 = pal_c = unp = 0
    n_pal = n_unp = n_pair = 0
    for n in range(0, 4 * U, 2):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            g1 ^= 1
            jp = 2 * n - j
            if j == n:
                pal_c ^= 1
                n_pal += 1
            elif jp > clip:
                unp ^= 1
                n_unp += 1
            elif j < jp:
                n_pair += 1
    return {
        "g1": g1,
        "pal_c": pal_c,
        "unp": unp,
        "n_pal": n_pal,
        "n_unp": n_unp,
        "n_pair": n_pair,
    }


def green_split() -> dict:
    """k<=8: pal-centers all clipped, xor 0; g1e equals unpaired tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_GREEN + 1):
        U = 1 << k
        r = _green_even_pal(k)
        if r["n_pal"] != pal_center_count(k):
            return {"ok": False, "count": True, "k": k, "r": r}
        if r["pal_c"] != 0:
            return {"ok": False, "pal_c": True, "k": k, "r": r}
        if r["g1"] != r["unp"] or r["g1"] != want_g1_even(k):
            return {"ok": False, "g1": True, "k": k, "r": r}
        if k == 0 and r["n_unp"] != 0:
            return {"ok": False, "k0_unp": True, "r": r}
        if k == 1 and r["n_unp"] == 0:
            return {"ok": False, "k1_empty": True, "r": r}
        if 4 * U - 2 > 5 * U:
            return {"ok": False, "clip": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "g1": r["g1"],
            "unp": r["unp"],
            "n_pal": r["n_pal"],
            "n_unp": r["n_unp"],
            "n_pair": r["n_pair"],
        }
    ok = (
        n_ok == K_GREEN + 1
        and rows["0"]["g1"] == 0
        and rows["1"]["g1"] == 1
        and rows["2"]["g1"] == 0
        and rows["1"]["n_unp"] == 1
        and pal_center_count(0) == 2
        and pal_center_count(8) == 512
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_GREEN, "rows": rows}


def tot_form() -> dict:
    """k<=64: pal-center count even; all pal-centers clipped; G(m,m)=1."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        U = 1 << k
        cnt = pal_center_count(k)
        if cnt != 2 * U or cnt % 2 != 0:
            return {"ok": False, "count": True, "k": k, "cnt": cnt}
        if 4 * U - 2 > 5 * U:
            return {"ok": False, "clip": True, "k": k}
        n_ok += 1
    for m in range(0, 64):
        if G(m, m) != 1:
            return {"ok": False, "gmm": True, "m": m}
        if m % 2 == 0 and G(m, m) != G(m // 2, m // 2):
            return {"ok": False, "fold": True, "m": m}
    ok = (
        n_ok == K_ALG + 1
        and pal_center_count(0) == 2
        and pal_center_count(10) == 2048
        and want_g1_even(1) == 1
        and want_g1_even(0) == 0
        and want_g1_even(2) == 0
        and want_green_even(1) == 0
        and want_even(1) == 1
        and G(0, 0) == 1
        and G(63, 63) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def _walk_even_pal(k: int) -> dict:
    """Even-n packed rest split: pal-center, pal-pair mismatch, unpaired AND."""
    U = 1 << k
    T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
    clip = 5 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    pal_c = pair_mis = rest = 0
    n_pal = n_unp = n_pair = n_pair_mis = 0
    n_unp_and = n_unp_raw = n_pal_and = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Qc)
            if n % 2 == 0:
                cells = {}
                raw = {}
                hi = min(2 * n, clip)
                for j in range(0, hi + 1, 2):
                    p = T - 2 * j
                    if p < 0:
                        continue
                    if G(n, j) == 0:
                        continue
                    z, a, b, c = (bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(z, a, b, c)
                    raw[j] = packed
                    cells[j] = int(packed and p not in FORCED)
                    rest ^= cells[j]
                if n <= clip and n in cells:
                    pal_c ^= cells[n]
                    n_pal += 1
                    n_pal_and += cells[n]
                seen = set()
                for j, rbit in cells.items():
                    if j in seen or j == n:
                        continue
                    jp = 2 * n - j
                    if jp in cells:
                        seen.add(j)
                        seen.add(jp)
                        n_pair += 1
                        if rbit != cells[jp]:
                            pair_mis ^= 1
                            n_pair_mis += 1
                    else:
                        n_unp += 1
                        n_unp_raw += raw[j]
                        n_unp_and += rbit
        row = rule30_step(row)
        s += 1
    return {
        "rest": rest,
        "pal_c": pal_c,
        "pair_mis": pair_mis,
        "n_pal": n_pal,
        "n_unp": n_unp,
        "n_pair": n_pair,
        "n_pair_mis": n_pair_mis,
        "n_unp_and": n_unp_and,
        "n_unp_raw": n_unp_raw,
        "n_pal_and": n_pal_and,
    }


def _walk_odd_unp(k: int) -> dict:
    """Odd-n clip-unpaired packed AND count (killed identically 0)."""
    U = 1 << k
    T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
    clip = 5 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_unp = n_unp_raw = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Qc)
            if n % 2 == 1:
                hi = min(2 * n, clip)
                for j in range(0, hi + 1):
                    p = T - 2 * j
                    if p < 0:
                        continue
                    if G(n, j) == 0:
                        continue
                    jp = 2 * n - j
                    if j == n or jp <= clip:
                        continue
                    z, a, b, c = (bit_at(prev, p - 3 + i) for i in range(4))
                    n_unp += 1
                    n_unp_raw += and_clause(z, a, b, c)
        row = rule30_step(row)
        s += 1
    return {"n_unp": n_unp, "n_unp_raw": n_unp_raw}


def fold_split() -> dict:
    """k<=10: even-n unpaired packed AND is 0; rest = pal_c xor pair_mis."""
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        r = _walk_even_pal(k)
        if r["n_unp_and"] != 0 or r["n_unp_raw"] != 0:
            return {"ok": False, "unp_and": True, "k": k, "r": r}
        if r["rest"] != (r["pal_c"] ^ r["pair_mis"]):
            return {"ok": False, "sum": True, "k": k, "r": r}
        if r["rest"] != want_even(k):
            return {"ok": False, "even": True, "k": k, "r": r}
        if r["n_pal"] != pal_center_count(k):
            return {"ok": False, "pal_n": True, "k": k, "r": r}
        n_ok += 1
        rows[str(k)] = {
            "rest": r["rest"],
            "pal_c": r["pal_c"],
            "pair_mis": r["pair_mis"],
            "n_unp": r["n_unp"],
            "n_pair_mis": r["n_pair_mis"],
            "n_pal_and": r["n_pal_and"],
        }
    odd = _walk_odd_unp(3)
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["rest"] == 1
        and rows["0"]["pal_c"] == 0
        and rows["0"]["pair_mis"] == 1
        and rows["1"]["n_unp"] > 0
        and rows["6"]["rest"] == 0
        and rows["7"]["rest"] == 1
        and rows["10"]["rest"] == 0
        and rows["3"]["pal_c"] == 1
        and rows["3"]["pair_mis"] == 1
        and odd["n_unp_raw"] > 0
        and odd["n_unp"] > 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_REST,
        "rows": rows,
        "odd_unp_k3": odd,
    }


def killed_eq() -> dict:
    """pal-center tot equals want_even; unpaired empty; pair_mis=0; all-n silent."""
    ok = (
        want_even(0) == 1
        and want_green_even(0) == 1
        and want_even(1) != want_green_even(1)
        and want_even(3) != want_green_even(3)
        and want_g1_even(1) == 1
        and want_rest_e0(2) == 1
        and want_even(2) == want_rest_e0(2)
        and want_even(6) != want_rest_e0(6)
    )
    return {"ok": ok}


def prefixes() -> dict:
    qw = json.loads(QW_JSON.read_text())
    qu = json.loads(QU_JSON.read_text())
    so = json.loads(SO_JSON.read_text())
    sq = json.loads(SQ_JSON.read_text())
    ok = (
        qw["checks"]["all_ok"]
        and qu["checks"]["all_ok"]
        and so["checks"]["all_ok"]
        and sq["checks"]["all_ok"]
        and qw["verdict"]["green_even_rest_iff_k_ne_1"] == "LEMMA"
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and so["verdict"]["odd_eq_want_odd_k_le_10"] == "CERTIFIED"
        and sq["verdict"]["n0_oo_eq_want_n0_oo_k_le_10"] == "CERTIFIED"
        and so["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sq["verdict"]["prize"] == "unsolved"
        and want_even(7) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, green, tot, fold, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert green["ok"] and tot["ok"] and fold["ok"] and kl["ok"]
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
    green = green_split()
    tot = tot_form()
    fold = fold_split()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, green, tot, fold, kl, sc, pref)
    dump = {
        "cycle": "SR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "green_split": {k: green[k] for k in green if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "fold_split": {k: fold[k] for k in fold if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_g1_eq_unpaired_k_le_8": True,
            "pal_center_count_all_k": True,
            "unpaired_packed_and_0_k_le_10": True,
            "unpaired_packed_and_0_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_g1_eq_unpaired": "LEMMA",
            "pal_center_count_all_k": "LEMMA",
            "unpaired_packed_and_0_k_le_10": "CERTIFIED",
            "even_rest_eq_pal_c_xor_pair_mis_k_le_10": "CERTIFIED",
            "unpaired_packed_and_0_all_k": "PREFIX",
            "pal_c_eq_want_even": "KILLED",
            "pair_mis_identically_0": "KILLED",
            "unpaired_empty": "KILLED",
            "odd_unpaired_and_0": "KILLED",
            "green_even_eq_packed_even": "KILLED",
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
        "fold n_ok",
        dump["fold_split"]["n_ok"],
        "k0 pal_c",
        dump["fold_split"]["rows"]["0"]["pal_c"],
        "k7 rest",
        dump["fold_split"]["rows"]["7"]["rest"],
        "odd_unp_k3",
        dump["fold_split"]["odd_unp_k3"]["n_unp_raw"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
