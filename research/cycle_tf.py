#!/usr/bin/env python3
"""Cycle TF: d=1/d=2 pal-pairs split by n mod 4.

All covering n=1 mod 4 are d=1 pal-pairs (count 2^k). Covering
n=3 mod 4 is partitioned by d=1 and d=2, counts J_k and J_{k+1}.
Covering n=2 mod 4 carries every even d=2 pal-pair (count J_{k+1}).
Covering n=0 mod 4 has neither d=1 nor d=2. Thus d=1 lives on
n=1,3 mod 4 and d=2 lives on n=2,3 mod 4. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_tf.py --certify
Dump: research/cycle_tf.json
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
from cycle_sv import pal_left_never_forced
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal
from cycle_td import want_d1_n
from cycle_te import want_d2_n, want_d2_parity_n

OUT = Path(__file__).resolve().with_suffix(".json")
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"
TC_JSON = Path(__file__).resolve().parent / "cycle_tc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def want_d1_r1_n(k: int) -> int:
    """d=1 pal-pairs on n=1 mod 4: all 2^k of them."""
    return 1 << k


def want_d1_r3_n(k: int) -> int:
    """d=1 pal-pairs on n=3 mod 4: J_k."""
    return jacobsthal(k)


def want_d2_r2_n(k: int) -> int:
    """d=2 pal-pairs on n=2 mod 4: J_{k+1}."""
    return jacobsthal(k + 1)


def want_d2_r3_n(k: int) -> int:
    """d=2 pal-pairs on n=3 mod 4: J_{k+1}."""
    return jacobsthal(k + 1)


def tot_form() -> dict:
    """k<=64: 2^k+J_k=J_{k+2}; residue G; n=1 mod 4 always d=1."""
    n_ok = 0
    if want_d1_r1_n(0) != 1 or want_d1_r3_n(0) != 0:
        return {"ok": False, "base": True}
    if want_d2_r2_n(0) != 1 or want_d2_r3_n(0) != 1:
        return {"ok": False, "base2": True}
    for k in range(0, K_ALG + 1):
        if want_d1_r1_n(k) + want_d1_r3_n(k) != want_d1_n(k):
            return {"ok": False, "d1sum": True, "k": k}
        if want_d1_r3_n(k) + want_d2_r3_n(k) != (1 << k):
            return {"ok": False, "r3": True, "k": k}
        if want_d2_r2_n(k) + want_d2_r3_n(k) != want_d2_n(k):
            return {"ok": False, "d2sum": True, "k": k}
        if want_d2_r2_n(k) != want_d2_parity_n(k):
            return {"ok": False, "par": True, "k": k}
        u = 1 << k
        samples = {0, 1, 2, 3, u, u + 1, 3 * u, 4 * u - 4, 4 * u - 3, 4 * u - 2, 4 * u - 1}
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            r = n % 4
            g1 = G(n, n - 1) if n >= 1 else 0
            g2 = G(n, n - 2) if n >= 2 else 0
            if r == 0 and (g1 or g2):
                return {"ok": False, "r0": True, "k": k, "n": n}
            if r == 1:
                if g1 != 1 or g2 != 0:
                    return {"ok": False, "r1": True, "k": k, "n": n}
                if pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "kind1": True, "k": k, "n": n}
            if r == 2:
                if g1 != 0:
                    return {"ok": False, "r2d1": True, "k": k, "n": n}
                m = n // 2
                if g2 != G(m, m - 1):
                    return {"ok": False, "r2fold": True, "k": k, "n": n}
                if m % 2 == 0 and g2 != 0:
                    return {"ok": False, "r2evenm": True, "k": k, "n": n}
            if r == 3:
                if g1 ^ g2 != 1:
                    return {"ok": False, "r3xor": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d1_r1_n(7) == 128
        and want_d1_r3_n(7) == 43
        and want_d2_r2_n(7) == 85
        and G(1, 0) == 1
        and G(4, 3) == 0
        and G(4, 2) == 0
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: d=1/d=2 counts by n mod 4 match Jacobsthal/power-of-two."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        d1 = [0, 0, 0, 0]
        d2 = [0, 0, 0, 0]
        covering = [0, 0, 0, 0]
        for n in range(0, 4 * u):
            covering[n % 4] += 1
            if n >= 1 and G(n, n - 1) == 1:
                if pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "kind1": True, "k": k, "n": n}
                d1[n % 4] += 1
            if n >= 2 and G(n, n - 2) == 1:
                if pal_kind(n, n - 2, k) != "pair":
                    return {"ok": False, "kind2": True, "k": k, "n": n}
                d2[n % 4] += 1
        want = {
            "d1": [0, want_d1_r1_n(k), 0, want_d1_r3_n(k)],
            "d2": [0, 0, want_d2_r2_n(k), want_d2_r3_n(k)],
            "cov": [u, u, u, u],
        }
        if d1 != want["d1"] or d2 != want["d2"] or covering != want["cov"]:
            return {
                "ok": False,
                "count": True,
                "k": k,
                "d1": d1,
                "d2": d2,
                "covering": covering,
                "want": want,
            }
        n_ok += 1
        rows[str(k)] = {"d1": d1, "d2": d2}
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["d1"] == [0, 1, 0, 0]
        and rows["0"]["d2"] == [0, 0, 1, 1]
        and rows["7"]["d1"] == [0, 128, 0, 43]
        and rows["12"]["d1"][1] == 4096
        and rows["12"]["d2"][2] == 2731
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """d=1 on all odd n; d=2 on all even n; n=0 mod 4 has d=2."""
    ok = (
        want_d1_r3_n(0) == 0
        and want_d1_r1_n(1) == 2
        and want_d1_n(1) == 3
        and want_d2_r2_n(0) == 1
        and want_d2_n(0) == 2
        and G(5, 4) == 1
        and G(4, 2) == 0
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    te = json.loads(TE_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    tc = json.loads(TC_JSON.read_text())
    ok = (
        te["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and tc["checks"]["all_ok"]
        and te["verdict"]["odd_n_d1_xor_d2"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and te["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and te["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
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
    cnt = residue_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "residue_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d1_all_n1_mod4": True,
            "d1_r3_eq_jacobsthal": True,
            "d2_only_n2_n3_mod4": True,
            "n0_mod4_no_d1_d2": True,
            "n3_mod4_d1_xor_d2": True,
            "d1_all_odd_n": False,
            "d2_all_even_n": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d1_all_n1_mod4": "LEMMA",
            "d1_r3_eq_jacobsthal": "LEMMA",
            "d2_only_n2_n3_mod4": "LEMMA",
            "n0_mod4_no_d1_d2": "LEMMA",
            "n3_mod4_d1_xor_d2": "LEMMA",
            "d1_all_odd_n": "KILLED",
            "d2_all_even_n": "KILLED",
            "d2_and_identically_0": "KILLED",
            "d1_and_identically_0": "KILLED",
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
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
