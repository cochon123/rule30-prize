#!/usr/bin/env python3
"""Cycle TK: d=1/d=2 pal-pairs split by n mod 8.

G(n, n-1) is 0 if n is even, 1 if n=1 mod 4, and G(n//4, n//4-1)
if n=3 mod 4. At k>=1 every covering n=1 or 5 mod 8 is d=1 and
every covering n=2 or 3 mod 8 is d=2. Covering n=7 mod 8 is
partitioned by d=1 and d=2 (J_k and J_{k-1}); n=6 mod 8 carries
the remaining even d=2 (J_{k-1}). Covering times of n=r mod 8
are the 16-AP 2U-2r+15 .. 10U-2r-1. Pal-center tot is not
identically 0 on any residue. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_tk.py --certify
Dump: research/cycle_tk.json
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
from cycle_ta import pal_kind
from cycle_tb import jacobsthal
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tf import want_d1_r1_n, want_d1_r3_n, want_d2_r2_n, want_d2_r3_n
from cycle_ti import residue_ap_ok
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TJ_JSON = Path(__file__).resolve().parent / "cycle_tj.json"
TI_JSON = Path(__file__).resolve().parent / "cycle_ti.json"
TF_JSON = Path(__file__).resolve().parent / "cycle_tf.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_CELL = 8
Q = 10
PAT0011 = (0, 0, 1, 1)
MOD16_R = (15, 13, 11, 9, 7, 5, 3, 1)


def G_nm1(n: int) -> int:
    """G(n, n-1): 0 if even; 1 if n=1 mod 4; G(n//4, n//4-1) if n=3 mod 4."""
    if n < 1:
        return 0
    while n % 4 == 3:
        n //= 4
        if n < 1:
            return 0
    if n % 2 == 0:
        return 0
    return 1


def want_d1_r1_n8(k: int) -> int:
    """d=1 pal-pairs on n=1 mod 8: 2^{max(k-1,0)}."""
    return 1 << max(k - 1, 0)


def want_d1_r5_n8(k: int) -> int:
    """d=1 pal-pairs on n=5 mod 8: 2^{k-1} (k>=1); 0 at k=0."""
    return 0 if k == 0 else 1 << (k - 1)


def want_d1_r7_n8(k: int) -> int:
    """d=1 pal-pairs on n=7 mod 8: J_k."""
    return jacobsthal(k)


def want_d2_r2_n8(k: int) -> int:
    """d=2 pal-pairs on n=2 mod 8: 2^{max(k-1,0)}."""
    return 1 << max(k - 1, 0)


def want_d2_r3_n8(k: int) -> int:
    """d=2 pal-pairs on n=3 mod 8: 2^{max(k-1,0)}."""
    return 1 << max(k - 1, 0)


def want_d2_r6_n8(k: int) -> int:
    """d=2 pal-pairs on n=6 mod 8: J_{k-1} (k>=1); 0 at k=0."""
    return 0 if k == 0 else jacobsthal(k - 1)


def want_d2_r7_n8(k: int) -> int:
    """d=2 pal-pairs on n=7 mod 8: J_{k-1} (k>=1); 0 at k=0."""
    return 0 if k == 0 else jacobsthal(k - 1)


def residue8_t_lo(k: int, r: int) -> int:
    """Least covering time of n=r mod 8."""
    return 2 * (1 << k) - 2 * r + 15


def residue8_t_hi(k: int, r: int) -> int:
    """Greatest covering time of n=r mod 8."""
    return 10 * (1 << k) - 2 * r - 1


def residue8_ap_ok(k: int, r: int) -> bool:
    """k>=1: length 2^{k-1}, step 16, endpoints 2U-2r+15 and 10U-2r-1."""
    if k < 1 or r < 0 or r > 7:
        return False
    lo = residue8_t_lo(k, r)
    hi = residue8_t_hi(k, r)
    if lo > hi or (hi - lo) % 16:
        return False
    return ((hi - lo) // 16) + 1 == (1 << (k - 1))


def tot_form() -> dict:
    """k<=64: G(n,n-1) form; residue counts; 16-AP endpoints."""
    n_ok = 0
    if G_nm1(0) != 0 or G_nm1(1) != 1 or G_nm1(2) != 0:
        return {"ok": False, "g0": True}
    if G_nm1(3) != 0 or G_nm1(7) != 1 or G_nm1(15) != 0:
        return {"ok": False, "g3": True}
    if want_d1_r1_n8(0) != 1 or want_d1_r5_n8(0) != 0:
        return {"ok": False, "base": True}
    if want_d2_r2_n8(0) != 1 or want_d2_r6_n8(0) != 0:
        return {"ok": False, "base2": True}
    for k in range(0, K_ALG + 1):
        if want_d1_r1_n8(k) + want_d1_r5_n8(k) != want_d1_r1_n(k):
            return {"ok": False, "d1r1": True, "k": k}
        if want_d1_r7_n8(k) != want_d1_r3_n(k):
            return {"ok": False, "d1r7": True, "k": k}
        if (
            want_d1_r1_n8(k)
            + want_d1_r5_n8(k)
            + want_d1_r7_n8(k)
            != want_d1_n(k)
        ):
            return {"ok": False, "d1sum": True, "k": k}
        if want_d2_r2_n8(k) + want_d2_r6_n8(k) != want_d2_r2_n(k):
            return {"ok": False, "d2r2": True, "k": k}
        if want_d2_r3_n8(k) + want_d2_r7_n8(k) != want_d2_r3_n(k):
            return {"ok": False, "d2r3": True, "k": k}
        if (
            want_d2_r2_n8(k)
            + want_d2_r3_n8(k)
            + want_d2_r6_n8(k)
            + want_d2_r7_n8(k)
            != want_d2_n(k)
        ):
            return {"ok": False, "d2sum": True, "k": k}
        if k >= 1:
            half = 1 << (k - 1)
            if want_d1_r1_n8(k) != half or want_d1_r5_n8(k) != half:
                return {"ok": False, "half1": True, "k": k}
            if want_d2_r2_n8(k) != half or want_d2_r3_n8(k) != half:
                return {"ok": False, "half2": True, "k": k}
            if want_d1_r7_n8(k) + want_d2_r7_n8(k) != half:
                return {"ok": False, "r7": True, "k": k}
            if want_d2_r6_n8(k) + want_d2_r6_n8(k) != 2 * jacobsthal(k - 1):
                return {"ok": False, "r6": True, "k": k}
            if jacobsthal(k) + jacobsthal(k - 1) != half:
                return {"ok": False, "J": True, "k": k}
            if not all(residue8_ap_ok(k, r) for r in range(8)):
                return {"ok": False, "ap": True, "k": k}
            if not all(residue_ap_ok(k, r) for r in range(4)):
                return {"ok": False, "ti": True, "k": k}
            if k >= 3:
                for r in range(8):
                    if residue8_t_lo(k, r) % 16 != MOD16_R[r]:
                        return {"ok": False, "mod": True, "k": k, "r": r}
                    if residue8_t_hi(k, r) % 16 != MOD16_R[r]:
                        return {"ok": False, "modh": True, "k": k, "r": r}
        u = 1 << k
        samples = {
            0,
            1,
            2,
            3,
            5,
            6,
            7,
            u,
            u + 1,
            3 * u,
            4 * u - 8,
            4 * u - 7,
            4 * u - 6,
            4 * u - 5,
            4 * u - 4,
            4 * u - 3,
            4 * u - 2,
            4 * u - 1,
        }
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            r = n % 8
            g1 = G(n, n - 1) if n >= 1 else 0
            g2 = G(n, n - 2) if n >= 2 else 0
            if g1 != G_nm1(n):
                return {"ok": False, "gnm1": True, "k": k, "n": n}
            if r in (0, 4) and (g1 or g2):
                return {"ok": False, "r04": True, "k": k, "n": n}
            if r in (1, 5):
                if g1 != 1 or g2 != 0:
                    return {"ok": False, "r15": True, "k": k, "n": n}
                if pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "kind15": True, "k": k, "n": n}
            if r in (2, 3) and n >= 2:
                if g1 != 0 or g2 != 1:
                    return {"ok": False, "r23": True, "k": k, "n": n}
                if pal_kind(n, n - 2, k) != "pair":
                    return {"ok": False, "kind23": True, "k": k, "n": n}
            if r == 7 and n >= 2 and g1 ^ g2 != 1:
                return {"ok": False, "r7xor": True, "k": k, "n": n}
            if k >= 1:
                t = covering_t(k, n)
                lo = residue8_t_lo(k, r)
                hi = residue8_t_hi(k, r)
                if t < lo or t > hi or (t - lo) % 16:
                    return {"ok": False, "t": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d1_r1_n8(7) == 64
        and want_d1_r5_n8(7) == 64
        and want_d1_r7_n8(7) == 43
        and want_d2_r2_n8(7) == 64
        and want_d2_r3_n8(7) == 64
        and want_d2_r6_n8(7) == 21
        and want_d2_r7_n8(7) == 21
        and G_nm1(11) == 0
        and G(11, 10) == 0
        and G(11, 9) == 1
        and residue8_ap_ok(64, 7)
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: d=1/d=2 counts by n mod 8; times equal the 16-AP."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        d1 = [0] * 8
        d2 = [0] * 8
        covering = [0] * 8
        for n in range(0, 4 * u):
            covering[n % 8] += 1
            if n >= 1 and G(n, n - 1) == 1:
                if pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "kind1": True, "k": k, "n": n}
                d1[n % 8] += 1
            if n >= 2 and G(n, n - 2) == 1:
                if pal_kind(n, n - 2, k) != "pair":
                    return {"ok": False, "kind2": True, "k": k, "n": n}
                d2[n % 8] += 1
        want_d1 = [
            0,
            want_d1_r1_n8(k),
            0,
            0,
            0,
            want_d1_r5_n8(k),
            0,
            want_d1_r7_n8(k),
        ]
        want_d2 = [
            0,
            0,
            want_d2_r2_n8(k),
            want_d2_r3_n8(k),
            0,
            0,
            want_d2_r6_n8(k),
            want_d2_r7_n8(k),
        ]
        if d1 != want_d1 or d2 != want_d2:
            return {
                "ok": False,
                "count": True,
                "k": k,
                "d1": d1,
                "d2": d2,
                "want_d1": want_d1,
                "want_d2": want_d2,
            }
        rec = {"d1": d1, "d2": d2, "times": {}}
        if k >= 1:
            for r in range(8):
                got = sorted(covering_t(k, n) for n in range(r, 4 * u, 8))
                lo = residue8_t_lo(k, r)
                hi = residue8_t_hi(k, r)
                want = list(range(lo, hi + 1, 16))
                if got != want:
                    return {"ok": False, "ap": True, "k": k, "r": r}
                rec["times"][str(r)] = {
                    "n": len(got),
                    "lo": got[0],
                    "hi": got[-1],
                }
        n_ok += 1
        rows[str(k)] = rec
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["d1"] == [0, 1, 0, 0, 0, 0, 0, 0]
        and rows["0"]["d2"] == [0, 0, 1, 1, 0, 0, 0, 0]
        and rows["1"]["d1"][7] == 1
        and rows["7"]["d1"] == [0, 64, 0, 0, 0, 64, 0, 43]
        and rows["7"]["d2"] == [0, 0, 64, 64, 0, 0, 21, 21]
        and rows["12"]["d1"][1] == 2048
        and rows["12"]["d2"][2] == 2048
        and rows["12"]["d1"][7] == 1365
        and rows["12"]["times"]["3"]["n"] == 2048
        and rows["12"]["times"]["7"]["lo"] == 2 * 4096 + 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def pal_res() -> dict:
    """k<=8 pal-center tot by n mod 8: none identically 0."""
    t_hi = Q * (1 << K_CELL)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    rows = {}
    fired = [False] * 8
    for k in range(0, K_CELL + 1):
        u = 1 << k
        tot = [0] * 8
        for n in range(0, 4 * u):
            t = covering_t(k, n)
            tot[n % 8] ^= pal_center_and(packed[t], even_s(n, k))
        for r in range(8):
            if tot[r]:
                fired[r] = True
        acc = 0
        for b in tot:
            acc ^= b
        n_ok += 1
        rows[str(k)] = {"tot": tot, "all": acc}
    ok = (
        n_ok == K_CELL + 1
        and all(fired)
        and rows["0"]["tot"][:4] == [0, 0, 1, 1]
        and rows["3"]["tot"][6] == 1
        and rows["8"]["tot"][3] == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_CELL,
        "rows": rows,
        "ident0": [False] * 8,
    }


def killed_eq() -> dict:
    """d=1 on all n=7 mod 8; d=2 on all n=6 mod 8; pal tot ident 0."""
    ok = (
        want_d1_r7_n8(2) == 1
        and want_d1_r7_n8(2) != (1 << 1)
        and want_d2_r6_n8(1) == 0
        and want_d2_r3_n8(1) == 1
        and G_nm1(7) == 1
        and G_nm1(15) == 0
        and G(5, 4) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tj = json.loads(TJ_JSON.read_text())
    ti = json.loads(TI_JSON.read_text())
    tf = json.loads(TF_JSON.read_text())
    ok = (
        tj["checks"]["all_ok"]
        and ti["checks"]["all_ok"]
        and tf["checks"]["all_ok"]
        and tj["verdict"]["child_residue_ap_interleaves_parents"] == "LEMMA"
        and ti["verdict"]["residue_times_eq_8_ap"] == "LEMMA"
        and tf["verdict"]["d1_all_n1_mod4"] == "LEMMA"
        and tj["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tj["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
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
    cnt = residue_count()
    pr = pal_res()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, pr, kl, sc, pref)
    dump = {
        "cycle": "TK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "residue_count": {k: cnt[k] for k in cnt if k != "ok"},
        "pal_res": {k: pr[k] for k in pr if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "G_nm1_closed_form": True,
            "d1_all_n1_n5_mod8": True,
            "d2_all_n2_n3_mod8": True,
            "n7_mod8_d1_xor_d2": True,
            "residue8_times_eq_16_ap": True,
            "d1_all_n7_mod8": False,
            "d2_all_n6_mod8": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "G_nm1_closed_form": "LEMMA",
            "d1_all_n1_n5_mod8": "LEMMA",
            "d2_all_n2_n3_mod8": "LEMMA",
            "n7_mod8_d1_xor_d2": "LEMMA",
            "residue8_times_eq_16_ap": "LEMMA",
            "d1_all_n7_mod8": "KILLED",
            "d2_all_n6_mod8": "KILLED",
            "pal_res8_identically_0": "KILLED",
            "d1_all_odd_n": "KILLED",
            "d2_all_even_n": "KILLED",
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
        "d1 r1 k12",
        dump["residue_count"]["rows"]["12"]["d1"][1],
        "d2 r2",
        dump["residue_count"]["rows"]["12"]["d2"][2],
        "d1 r7",
        dump["residue_count"]["rows"]["12"]["d1"][7],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
