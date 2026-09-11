#!/usr/bin/env python3
"""Cycle DW: pair invariants imply ham(n3,n4)=n0 for every odd 2-copy.

reconstruct(1,s) has isolated 1s for any nonzero s (NOR). If s is O-type of
half-length n0 then n3_t=1 forces s_{t-1}=0, hence n3_{t+n0}=0
(complementary support). The Hamming difference d=n3 xor n4 obeys
d_{t+1}=not s_t if n3_t else not d_t. On O-type pair slots:
  both n3=0 => both d=1;
  exactly one n3=1 => d on the zero side is 0.
Those pair invariants, certified for 1<=n0<=16, make
phi(i)=(i-1) mod n0 a bijection from {n3=1, d=0} onto the empty slots,
so ham(n3,n4)=n0 for every such n0 (and the bijection argument has no
further n0 bound). Pair invariants fail for generic s and for E-type
length 16. Do not claim the pair invariants for all n0. Do not compute
phi^{(3,5,9)} at k=16. Not a prize claim: Hamming n0 still does not fill
an annulus.

Run: python3 research/cycle_dw.py --certify
Dump: research/cycle_dw.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_ch import ham
from cycle_dv import mask_bits, odd_copy, n3n4_of

OUT = Path(__file__).resolve().with_suffix(".json")
DV_JSON = Path(__file__).resolve().parent / "cycle_dv.json"
N0_MAX = 16


def xorv(a: list[int], b: list[int]) -> list[int]:
    return [x ^ y for x, y in zip(a, b)]


def isolated_ones() -> bool:
    """n3_t=1 implies n3_{t+1}=0, for every nonzero s of length 2..8."""
    for n in range(2, 9):
        ones = [1] * n
        for mask in range(1, 1 << n):
            s = mask_bits(mask, n)
            u = reconstruct(ones, s)
            if u is None:
                return False
            for t in range(n):
                if u[t] == 1 and u[(t + 1) % n] != 0:
                    return False
                if u[(t + 1) % n] != (1 ^ (s[t] | u[t])):
                    return False
    return True


def complementary_support() -> bool:
    """O-type: n3_t=1 => s_{t-1}=0 => n3_{t+n0}=0."""
    for n0 in range(1, 13):
        L = 2 * n0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            n3 = reconstruct([1] * L, s)
            if n3 is None:
                return False
            for t in range(L):
                if n3[t] != 1:
                    continue
                if s[(t - 1) % L] != 0:
                    return False
                if n3[(t + n0) % L] != 0:
                    return False
    return True


def d_recurrence() -> bool:
    """d_{t+1}=not s_t if n3_t else not d_t, any nonzero s length 2..8."""
    for n in range(2, 9):
        for mask in range(1, 1 << n):
            s = mask_bits(mask, n)
            pair = n3n4_of(s)
            if pair is None:
                continue
            n3, n4 = pair
            d = xorv(n3, n4)
            for t in range(n):
                want = (s[t] ^ 1) if n3[t] else (d[t] ^ 1)
                if d[(t + 1) % n] != want:
                    return False
    return True


def pair_invariants_on(s: list[int]) -> bool:
    """Both n3=0 => both d=1; exactly one n3=1 => d on the zero side is 0."""
    n0 = len(s) // 2
    pair = n3n4_of(s)
    if pair is None:
        return False
    n3, n4 = pair
    d = xorv(n3, n4)
    for t in range(n0):
        a, b = n3[t], n3[t + n0]
        x, y = d[t], d[t + n0]
        if a and b:
            return False
        if a == 0 and b == 0 and not (x == 1 and y == 1):
            return False
        if a == 1 and y != 0:
            return False
        if b == 1 and x != 0:
            return False
    return True


def pair_invariants() -> dict:
    """O-type pair invariants for every 1<=n0<=16."""
    rows: dict[int, int] = {}
    for n0 in range(1, N0_MAX + 1):
        n = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            if not pair_invariants_on(s):
                return {"ok": False, "n0": n0, "mask": mask}
            n += 1
        rows[n0] = n
    return {"ok": True, "rows": rows}


def bijection_from_invariants() -> dict:
    """psi(empty t)=t+1 if s_t=0 else t+n0+1 hits agree1; phi inverse."""
    rows: dict[int, dict] = {}
    for n0 in range(1, N0_MAX + 1):
        L = 2 * n0
        n_ok = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(s)
            if pair is None:
                return {"ok": False, "n0": n0}
            n3, n4 = pair
            d = xorv(n3, n4)
            empty = [t for t in range(n0) if n3[t] == 0 and n3[t + n0] == 0]
            agree1 = [i for i in range(L) if n3[i] == 1 and d[i] == 0]
            psi: list[int] = []
            for t in empty:
                if s[t] == 0:
                    i = (t + 1) % L
                else:
                    i = (t + n0 + 1) % L
                if n3[i] != 1 or d[i] != 0:
                    return {"ok": False, "n0": n0, "why": "psi", "t": t}
                if (i - 1) % n0 != t:
                    return {"ok": False, "n0": n0, "why": "phi_psi", "t": t}
                psi.append(i)
            if sorted(psi) != sorted(agree1):
                return {"ok": False, "n0": n0, "why": "surj"}
            mapped = sorted((i - 1) % n0 for i in agree1)
            if mapped != sorted(empty):
                return {"ok": False, "n0": n0, "why": "inj"}
            z = len(empty)
            a = sum(n3)
            ov = len(agree1)
            h = ham(n3, n4)
            if ov != z or h != n0 or h != 2 * z + a - ov:
                return {"ok": False, "n0": n0, "h": h, "z": z, "ov": ov}
            n_ok += 1
        rows[n0] = {"n": n_ok, "ham": n0}
    return {"ok": True, "rows": rows}


def pair_invariants_fail_generic() -> bool:
    """Length-8 non-O-type s can violate complementary support."""
    n_both = 0
    for mask in range(1, 1 << 8):
        s = mask_bits(mask, 8)
        if twocopy_type(s) == "O":
            continue
        n3 = reconstruct([1] * 8, s)
        if n3 is None:
            continue
        for t in range(4):
            if n3[t] and n3[t + 4]:
                n_both += 1
                break
    return n_both > 0


def pair_invariants_fail_E() -> bool:
    """E-type length 16 is not always ham(n3,n4)=8."""
    hamset: set[int] = set()
    for mask in range(1, 1 << 8):
        half = mask_bits(mask, 8)
        s = half + half
        pair = n3n4_of(s)
        if pair is None:
            continue
        hamset.add(ham(pair[0], pair[1]))
    return hamset != {8} and 8 in hamset


def dv_prefix() -> dict:
    dv = json.loads(DV_JSON.read_text())
    prize = dv["prize_ham"]
    ok = (
        dv["checks"]["all_ok"]
        and dv["lemmas"]["ham_n3_n4_equals_n0_O_type"]
        and prize["4"]["ham_n3_n4"] == 4
        and prize["8"]["ham_n3_n4"] == 8
        and prize["16"]["ham_n3_n4"] == 16
        and dv["dual_antecedent_k"] == [15]
    )
    return {"ok": ok, "prize": prize, "dual_k": dv["dual_antecedent_k"]}


def self_checks(
    c20,
    iso: bool,
    comp: bool,
    drec: bool,
    inv: dict,
    bij: dict,
    gen: bool,
    etype: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert iso and comp and drec and inv["ok"] and bij["ok"] and gen and etype
    assert pref["ok"]
    assert inv["rows"][16] == 1 << 16
    assert bij["rows"][16]["ham"] == 16
    assert bij["rows"][1]["ham"] == 1
    assert pref["prize"]["16"]["ham_n3_n4"] == 16
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    iso = isolated_ones()
    comp = complementary_support()
    drec = d_recurrence()
    inv = pair_invariants()
    bij = bijection_from_invariants()
    gen = pair_invariants_fail_generic()
    etype = pair_invariants_fail_E()
    pref = dv_prefix()
    checks = self_checks(c20, iso, comp, drec, inv, bij, gen, etype, pref)
    dump = {
        "cycle": "DW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n0_max": N0_MAX,
        "pair_n": inv["rows"],
        "prize_ham": pref["prize"],
        "lemmas": {
            "n3_ones_isolated": True,
            "O_type_complementary_support": True,
            "d_recurrence": True,
            "pair_invariants_n0_1_to_16": True,
            "pair_invariants_imply_ham_n0": True,
            "pair_invariants_all_n0": None,
            "pair_invariants_generic_s": False,
            "pair_invariants_E_type": False,
            "ham_n3_n4_equals_n0_generic_s": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n3_ones_isolated": "LEMMA",
            "O_type_complementary_support": "LEMMA",
            "d_recurrence": "LEMMA",
            "pair_invariants_n0_1_to_16": "LEMMA",
            "pair_invariants_imply_ham_n0": "LEMMA",
            "pair_invariants_all_n0": "PREFIX",
            "pair_invariants_generic_s": "KILLED",
            "pair_invariants_E_type": "KILLED",
            "ham_n3_n4_equals_n0_generic_s": "KILLED",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("n0_max", N0_MAX)
    print("prize_ham", dump["prize_ham"])


if __name__ == "__main__":
    main()
