#!/usr/bin/env python3
"""Cycle DV: after odd doubling, ham(n3,n4)=n0; I=0 dual of 11=>0.

Unique continuation of (1, s) is the NOR recurrence u_{t+1}=NOR(s_t, u_t).
If s is an odd 2-copy of half-length n0, then ham(n3, n4)=n0 where
n3=reconstruct(1,s) and n4=reconstruct(s,n3). After an odd ident-0 the
scar is O-type of length 2 pi, so the first type-N pair differs in
exactly pi bits and cannot be equal. That holds for every O-type s, not
only shifted-not of the prize toggle, and on the prize orbit at
k=4,8,16. It fails for a generic (non 2-copy) s. Do not claim ham(s,n3)
equals n0, and do not claim the first odd-weight bit is at offset +3.

Covering never fails iff phi6=phi10=I implies phi18!=I. The I=0 slice is
I=phi6=phi10=0 => phi18=1. On Cycle DS that antecedent occurs only at
k=15, where phi18=1. Together with Cycle DT's 11=>0 (the I=1 slice),
both covering-relevant slices hold through k=18. Do not compute
phi^{(3,5,9)} at k=16. Not a prize claim: ham=n0 does not fill an
annulus, and the dual remains a prefix.

Run: python3 research/cycle_dv.py --certify
Dump: research/cycle_dv.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext, twocopy_type
from cycle_ch import ham, shifted_not
from cycle_df import unfold

OUT = Path(__file__).resolve().with_suffix(".json")
DS_JSON = Path(__file__).resolve().parent / "cycle_ds.json"
DT_JSON = Path(__file__).resolve().parent / "cycle_dt.json"
EXPECTED_P = {4: 29, 8: 400, 16: 87867}
DUAL_K = [15]


def mask_bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def odd_copy(s: list[int]) -> list[int]:
    return s + [x ^ 1 for x in s]


def nor_form() -> bool:
    """reconstruct(1, s)_{t+1} = NOR(s_t, u_t) for every nonzero s."""
    for n in range(2, 9):
        ones = [1] * n
        for mask in range(1 << n):
            s = mask_bits(mask, n)
            if not any(s):
                continue
            u = reconstruct(ones, s)
            if u is None:
                return False
            for t in range(n):
                if u[(t + 1) % n] != (1 ^ (s[t] | u[t])):
                    return False
    return True


def shifted_not_preserves_O() -> bool:
    """s_t = not O_{t-1} and O_{t+n}=not O_t force s_{t+n}=not s_t."""
    for n0 in range(1, 11):
        for mask in range(1 << n0):
            o = odd_copy(mask_bits(mask, n0))
            s = shifted_not(o)
            if twocopy_type(o) != "O" or twocopy_type(s) != "O":
                return False
            n = n0
            for t in range(2 * n):
                if s[(t + n) % (2 * n)] != (s[t] ^ 1):
                    return False
    return True


def otype_weight_ham() -> bool:
    """O-type has weight n0; ham(0,O)=ham(O,1)=ham(1,s)=n0."""
    for n0 in range(1, 9):
        L = 2 * n0
        zeros = [0] * L
        ones = [1] * L
        for mask in range(1 << n0):
            o = odd_copy(mask_bits(mask, n0))
            s = shifted_not(o)
            if xorcat(o) != (n0 % 2):
                return False
            if sum(o) != n0 or ham(zeros, o) != n0:
                return False
            if ham(o, ones) != n0 or ham(ones, s) != n0:
                return False
    return True


def n3n4_of(s: list[int]) -> tuple[list[int], list[int]] | None:
    L = len(s)
    n3 = reconstruct([1] * L, s)
    if n3 is None:
        return None
    n4 = reconstruct(s, n3)
    if n4 is None:
        return None
    return n3, n4


def ham_n3_n4_equals_n0() -> dict:
    """Every odd 2-copy of half-length n0 has ham(n3,n4)=n0."""
    rows: dict[int, dict] = {}
    for n0 in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12):
        n_ok = 0
        hamset: set[int] = set()
        n3_types: set[str] = set()
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(s)
            if pair is None:
                return {"ok": False, "n0": n0, "why": "none"}
            n3, n4 = pair
            h = ham(n3, n4)
            hamset.add(h)
            n3_types.add(twocopy_type(n3))
            if h != n0:
                return {"ok": False, "n0": n0, "h": h}
            n_ok += 1
        if hamset != {n0}:
            return {"ok": False, "n0": n0, "hamset": sorted(hamset)}
        rows[n0] = {"n": n_ok, "ham": n0, "n3_types": sorted(n3_types)}
    rng = random.Random(41)
    n16 = 0
    for _ in range(80):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        pair = n3n4_of(s)
        if pair is None or ham(pair[0], pair[1]) != 16:
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = {"n": n16, "ham": 16, "sampled": True}
    return {"ok": True, "rows": rows}


def ham_fails_generic_s() -> bool:
    """A non 2-copy s of length 8 need not have ham(n3,n4)=4."""
    hamset: set[int] = set()
    for mask in range(1, 1 << 8):
        s = mask_bits(mask, 8)
        if twocopy_type(s) == "O":
            continue
        pair = n3n4_of(s)
        if pair is None:
            continue
        hamset.add(ham(pair[0], pair[1]))
    return 4 in hamset and hamset != {4} and 3 in hamset


def ham_s_n3_not_n0() -> bool:
    """ham(s,n3)=n0 fails already on length-4 odd 2-copies."""
    hamset: set[int] = set()
    for mask in range(16):
        s = odd_copy(mask_bits(mask, 4))
        pair = n3n4_of(s)
        if pair is None:
            return False
        hamset.add(ham(s, pair[0]))
    return hamset != {4} and 3 in hamset


def first_odd_weight_not_always_3() -> bool:
    """First xorcat=1 after (0,O,1) is not always n3 (offset +3)."""
    offs: set[int] = set()
    for mask in range(16):
        t0 = mask_bits(mask, 4)
        o = odd_copy(t0)
        L = 8
        seqs: dict[int, list[int]] = {0: [0] * L, 1: o, 2: [1] * L}
        found = None
        for cur in range(3, 12):
            a, b = seqs[cur - 2], seqs[cur - 1]
            u = reconstruct(a, b)
            if u is None:
                return False
            seqs[cur] = u
            if xorcat(u) == 1:
                found = cur
                break
        if found is None:
            return False
        offs.add(found)
    return offs == {4, 8}


def prize_ham() -> dict:
    """Prize k=4,8,16: after the odd toggle, ham(n3,n4)=pi."""
    rows: dict[int, dict] = {}
    for k, p_odd in EXPECTED_P.items():
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
        cur_pi = pi
        found = None
        p = W + 1
        while p <= 2 * W:
            a = ext(seqs[p - 2], cur_pi)
            b = ext(seqs[p - 1], cur_pi)
            if all(x == 0 for x in b):
                sm = xorcat(a)
                u = unfold(a)
                if sm == 1:
                    found = p
                    seqs[p] = u + [x ^ 1 for x in u]
                    cur_pi *= 2
                    break
                seqs[p] = u
            else:
                seqs[p] = reconstruct(a, b)
            p += 1
        if found != p_odd:
            return {"ok": False, "k": k, "p": found}
        for q in range(found + 1, found + 5):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        o = ext(seqs[found], cur_pi)
        ones = ext(seqs[found + 1], cur_pi)
        s = ext(seqs[found + 2], cur_pi)
        n3 = ext(seqs[found + 3], cur_pi)
        n4 = ext(seqs[found + 4], cur_pi)
        n0 = cur_pi // 2
        if (
            twocopy_type(o) != "O"
            or ones != [1] * cur_pi
            or s != shifted_not(o)
            or twocopy_type(s) != "O"
            or twocopy_type(n3) != "N"
            or ham(n3, n4) != n0
            or n0 != pi
        ):
            return {"ok": False, "k": k, "ham": ham(n3, n4), "n0": n0}
        rows[k] = {"p": found, "pi": pi, "ham_n3_n4": n0, "n3": "N"}
    return {"ok": True, "rows": rows}


def covering_never_fail_iff_matched() -> bool:
    """Covering fails iff a=b=g=I; never-fail iff a=b=I => g!=I."""
    for a, b, g, i in product((0, 1), repeat=4):
        fail = a == b == g == i
        impl = a != i or b != i or g != i
        if (not fail) != impl:
            return False
    return True


def dual_kills_I0_dangerous() -> bool:
    """If I=a=b=0 => g=1, the tuple (0,0,0,0) is forbidden."""
    for a, b, g, i in product((0, 1), repeat=4):
        if i == a == b == 0 and g != 1:
            continue
        if (a, b, g, i) == (0, 0, 0, 0):
            return False
    return True


def ds_dt_dual_prefix() -> dict:
    ds = json.loads(DS_JSON.read_text())
    dt = json.loads(DT_JSON.read_text())
    p = ds["prefix"]
    ks, p2, p6, p10, p18 = p["k"], p["phi2"], p["phi6"], p["phi10"], p["phi18"]
    dual_ant = []
    dual_ok = True
    for i, k in enumerate(ks):
        if p2[i] == p6[i] == p10[i] == 0:
            dual_ant.append(k)
            if p18[i] != 1:
                dual_ok = False
    ok = (
        ds["checks"]["all_ok"]
        and dt["checks"]["all_ok"]
        and ds["empty_upto"] == 18
        and dt["i0_dangerous_k"] == []
        and dt["i1_dangerous_k"] == []
        and dt["match11_k"] == [5, 6, 7, 8, 11, 18]
        and dt["match00_k"] == [13, 14, 15, 17]
        and dual_ant == DUAL_K
        and dual_ok
        and dt["lemmas"]["phi6_phi10_1_implies_phi18_0_k_2_to_18"]
    )
    return {
        "ok": ok,
        "dual_antecedent_k": dual_ant,
        "dual_ok": dual_ok,
        "match00_k": dt["match00_k"],
        "match11_k": dt["match11_k"],
        "i0_empty": dt["i0_dangerous_k"] == [],
        "onesided": dt["lemmas"]["phi6_phi10_1_implies_phi18_0_k_2_to_18"],
    }


def self_checks(
    c20,
    nor: bool,
    sh: bool,
    wt: bool,
    n3n4: dict,
    gen: bool,
    sn3: bool,
    odd3: bool,
    prize: dict,
    taut1: bool,
    taut2: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert nor and sh and wt and n3n4["ok"] and gen and sn3 and odd3
    assert prize["ok"] and taut1 and taut2 and pref["ok"]
    assert n3n4["rows"][8]["ham"] == 8
    assert n3n4["rows"][4]["n3_types"] == ["N"]
    assert prize["rows"][16]["ham_n3_n4"] == 16
    assert pref["dual_antecedent_k"] == DUAL_K and pref["dual_ok"]
    assert pref["i0_empty"] and pref["onesided"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    nor = nor_form()
    sh = shifted_not_preserves_O()
    wt = otype_weight_ham()
    n3n4 = ham_n3_n4_equals_n0()
    gen = ham_fails_generic_s()
    sn3 = ham_s_n3_not_n0()
    odd3 = first_odd_weight_not_always_3()
    prize = prize_ham()
    taut1 = covering_never_fail_iff_matched()
    taut2 = dual_kills_I0_dangerous()
    pref = ds_dt_dual_prefix()
    checks = self_checks(
        c20, nor, sh, wt, n3n4, gen, sn3, odd3, prize, taut1, taut2, pref
    )
    dump = {
        "cycle": "DV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n3n4_n0": sorted(n3n4["rows"]),
        "prize_ham": prize["rows"],
        "dual_antecedent_k": pref["dual_antecedent_k"],
        "lemmas": {
            "reconstruct_ones_is_NOR": True,
            "shifted_not_preserves_O": True,
            "O_type_first_three_ham_n0": True,
            "ham_n3_n4_equals_n0_O_type": True,
            "ham_n3_n4_equals_n0_generic_s": False,
            "ham_s_n3_equals_n0": False,
            "prize_k_4_8_16_ham_n3_n4": True,
            "covering_never_fail_iff_matched_complement": True,
            "dual_I0_kills_allzero_kernel": True,
            "dual_I_phi6_phi10_0_implies_phi18_1_k_2_to_18": True,
            "dual_I_phi6_phi10_0_implies_phi18_1_all_k": None,
            "first_odd_weight_always_offset_3": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reconstruct_ones_is_NOR": "LEMMA",
            "shifted_not_preserves_O": "LEMMA",
            "O_type_first_three_ham_n0": "LEMMA",
            "ham_n3_n4_equals_n0_O_type": "LEMMA",
            "ham_n3_n4_equals_n0_generic_s": "KILLED",
            "ham_s_n3_equals_n0": "KILLED",
            "prize_k_4_8_16_ham_n3_n4": "LEMMA",
            "covering_never_fail_iff_matched_complement": "LEMMA",
            "dual_I0_kills_allzero_kernel": "LEMMA",
            "dual_I_phi6_phi10_0_implies_phi18_1_k_2_to_18": "PREFIX",
            "dual_I_phi6_phi10_0_implies_phi18_1_all_k": "PREFIX",
            "first_odd_weight_always_offset_3": "KILLED",
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
    print("n3n4_n0", dump["n3n4_n0"])
    print("prize_ham", dump["prize_ham"])
    print("dual_antecedent_k", dump["dual_antecedent_k"])


if __name__ == "__main__":
    main()
