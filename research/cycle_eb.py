#!/usr/bin/env python3
"""Cycle EB: r-fold of n0=2 O-types ident-0 at extra 22; min extra not monotone.

Unique continuation commutes with r-fold: reconstruct(A^r, B^r) =
reconstruct(A, B)^r whenever B is not identically 0. The four length-4
O-types 0011, 0110, 1001, 1100 therefore lift under repetition: odd r
stays O-type of half-length 2r and odd-ident-0s at extra 22; even r is
E-type and even-ident-0s at extra 22. Through n0=2,6,10,14 the only
O-type extra-22 scars are those four r-folds. n0=6 extra-22 is exactly
the 3-fold orbit {001100, 011001, 100110, 110011}; 12 words even-ident-0
at 99; 48 have none in 800 extras. Prize n0=4,8,16 are 2-powers (even
r) and O-type, so they are not this family. Kills: min extra increases
with n0 (n0=4 is 89, n0=6 is 22); extra>22 for all n0>=4. Do not claim
extra>=22 for every even n0; do not claim the family appears on the
prize orbit after k=2. Not a prize claim.

Run: python3 research/cycle_eb.py --certify
Dump: research/cycle_eb.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, reconstruct, xorcat
from cycle_cb import twocopy_type
from cycle_di import mask_bits
from cycle_dk import PRIZE_U16
from cycle_dm import PRIZE8, first_ident0_int
from cycle_dv import EXPECTED_P

OUT = Path(__file__).resolve().with_suffix(".json")
EA_JSON = Path(__file__).resolve().parent / "cycle_ea.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
DI_JSON = Path(__file__).resolve().parent / "cycle_di.json"
PRIZE4 = "0010"
N6_FOLD3 = {"001100", "011001", "100110", "110011"}
ODD_R = (1, 3, 5, 7, 9)
EVEN_R = (2, 4, 6, 8)
EXACT_R = ((1, 2), (3, 6), (5, 10), (7, 14))


def fold(seq: list[int], r: int) -> list[int]:
    return seq * r


def n0_2_otypes() -> list[list[int]]:
    out: list[list[int]] = []
    for mask in range(4):
        t0 = mask_bits(mask, 2)
        out.append(t0 + [x ^ 1 for x in t0])
    return out


def first_ident0_T(T: list[int], max_extra: int) -> tuple[int | None, int | None]:
    """First ident-0 extra after (0, T, 1), T not necessarily O-type."""
    a, b = T, [1] * len(T)
    for cur in range(3, 3 + max_extra):
        if all(x == 0 for x in b):
            return cur, xorcat(a)
        u = reconstruct(a, b)
        if u is None:
            return None, None
        a, b = b, u
    return None, None


def scar_until(T: list[int], max_extra: int) -> tuple[dict[int, list[int]], int | None]:
    L = len(T)
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    a, b = T, seqs[2]
    for cur in range(3, 3 + max_extra):
        if all(x == 0 for x in b):
            return seqs, cur
        u = reconstruct(a, b)
        if u is None:
            return seqs, None
        seqs[cur] = u
        a, b = b, u
    return seqs, None


def reconstruct_commutes() -> dict:
    """reconstruct(A^r, B^r) = reconstruct(A, B)^r for B not 0."""
    n_exh = 0
    for n in range(2, 7):
        for am in range(1 << n):
            for bm in range(1, 1 << n):
                A = mask_bits(am, n)
                B = mask_bits(bm, n)
                U = reconstruct(A, B)
                if U is None:
                    return {"ok": False, "n": n}
                for r in (2, 3, 4, 5):
                    Ur = reconstruct(fold(A, r), fold(B, r))
                    if Ur != fold(U, r):
                        return {"ok": False, "n": n, "r": r}
                    n_exh += 1
    rng = random.Random(11)
    n_rand = 0
    for n in (8, 12, 16):
        for _ in range(40):
            A = [rng.randint(0, 1) for _ in range(n)]
            B = [rng.randint(0, 1) for _ in range(n)]
            if all(x == 0 for x in B):
                continue
            U = reconstruct(A, B)
            for r in (2, 3, 5, 7):
                if reconstruct(fold(A, r), fold(B, r)) != fold(U, r):
                    return {"ok": False, "n": n, "r": r}
                n_rand += 1
    return {"ok": True, "exhaustive": n_exh, "random": n_rand}


def xorcat_fold_ok() -> bool:
    rng = random.Random(13)
    for n in (2, 4, 5, 8):
        for _ in range(30):
            s = [rng.randint(0, 1) for _ in range(n)]
            xs = xorcat(s)
            for r in range(1, 9):
                if xorcat(fold(s, r)) != (r * xs) % 2:
                    return False
    return True


def type_parity() -> dict:
    """Odd r: O-type (2r ≡ 2 mod 4). Even r: E-type (2r ≡ 0 mod 4)."""
    rows: dict[int, str] = {}
    for r in range(1, 12):
        want = "O" if r % 2 else "E"
        for T in n0_2_otypes():
            Tr = fold(T, r)
            if twocopy_type(Tr) != want:
                return {"ok": False, "r": r, "got": twocopy_type(Tr)}
            h = len(Tr) // 2
            for t in range(h):
                if want == "O" and Tr[t] == Tr[t + h]:
                    return {"ok": False, "r": r, "t": t}
                if want == "E" and Tr[t] != Tr[t + h]:
                    return {"ok": False, "r": r, "t": t}
        rows[r] = want
    return {"ok": True, "rows": rows}


def lift_commutes() -> dict:
    """The n0=2 scar through extra 22 r-folds to the scar of T^r."""
    n_ok = 0
    for T in n0_2_otypes():
        seqs, hit = scar_until(T, 40)
        if hit != 22:
            return {"ok": False, "hit": hit}
        for r in (2, 3, 5, 7):
            seqs_r, hit_r = scar_until(fold(T, r), 40)
            if hit_r != 22:
                return {"ok": False, "r": r, "hit": hit_r}
            for i in range(hit):
                if seqs_r[i] != fold(seqs[i], r):
                    return {"ok": False, "r": r, "i": i}
            n_ok += 1
    return {"ok": True, "n": n_ok}


def odd_fold_extra22() -> dict:
    rows: dict[int, list[str]] = {}
    for r in ODD_R:
        keys: list[str] = []
        for T in n0_2_otypes():
            Tr = fold(T, r)
            if twocopy_type(Tr) != "O":
                return {"ok": False, "r": r, "type": twocopy_type(Tr)}
            t0 = Tr[: 2 * r]
            cur, sm = first_ident0_int(t0, 40)
            if cur != 22 or sm != 1:
                return {"ok": False, "r": r, "cur": cur, "sm": sm}
            keys.append("".join(map(str, t0)))
        rows[r] = keys
    return {"ok": True, "rows": rows}


def even_fold_extra22() -> dict:
    rows: dict[int, int] = {}
    for r in EVEN_R:
        n_ok = 0
        for T in n0_2_otypes():
            Tr = fold(T, r)
            if twocopy_type(Tr) != "E":
                return {"ok": False, "r": r, "type": twocopy_type(Tr)}
            cur, sm = first_ident0_T(Tr, 40)
            if cur != 22 or sm != 0:
                return {"ok": False, "r": r, "cur": cur, "sm": sm}
            n_ok += 1
        rows[r] = n_ok
    return {"ok": True, "rows": rows}


def extra22_exactly_odd_folds() -> dict:
    """Through n0=2,6,10,14, extra-22 O-type T0 are exactly the r-folds."""
    rows: dict[int, list[str]] = {}
    otypes = n0_2_otypes()
    for r, n0 in EXACT_R:
        exp = {"".join(map(str, fold(T, r)[:n0])) for T in otypes}
        got: set[str] = set()
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            cur, sm = first_ident0_int(t0, 30)
            if cur == 22:
                if sm != 1:
                    return {"ok": False, "n0": n0, "sm": sm}
                got.add("".join(map(str, t0)))
        if got != exp:
            return {
                "ok": False,
                "n0": n0,
                "got": sorted(got),
                "exp": sorted(exp),
            }
        rows[n0] = sorted(exp)
    return {"ok": True, "rows": rows}


def n0_6_census() -> dict:
    hits: Counter[tuple[int | None, int | None]] = Counter()
    extra22: list[str] = []
    for mask in range(64):
        t0 = mask_bits(mask, 6)
        cur, sm = first_ident0_int(t0, 800)
        hits[(cur, sm)] += 1
        if cur == 22:
            extra22.append("".join(map(str, t0)))
    ok = (
        hits[(22, 1)] == 4
        and hits[(99, 0)] == 12
        and hits[(None, None)] == 48
        and set(extra22) == N6_FOLD3
    )
    return {
        "ok": ok,
        "n22": 4,
        "n99_even": 12,
        "n_none": 48,
        "extra22": sorted(extra22),
    }


def prize_not_odd_fold() -> dict:
    """Prize n0=4,8,16 are 2-powers (even r) and O-type, not n0=2 folds."""
    prize = {4: PRIZE4, 8: PRIZE8, 16: PRIZE_U16}
    otypes = n0_2_otypes()
    rows: dict[int, dict] = {}
    for n0, key in prize.items():
        r = n0 // 2
        if r % 2 != 0 or n0 % 4 != 0:
            return {"ok": False, "n0": n0, "r": r}
        t0 = [int(c) for c in key]
        T = t0 + [x ^ 1 for x in t0]
        if twocopy_type(T) != "O":
            return {"ok": False, "n0": n0, "type": twocopy_type(T)}
        for U in otypes:
            if twocopy_type(fold(U, r)) != "E":
                return {"ok": False, "n0": n0, "fold_type": r}
        cur, sm = first_ident0_int(t0, 40)
        if cur == 22:
            return {"ok": False, "n0": n0, "cur": 22}
        rows[n0] = {"r": r, "T0": key, "type": "O", "extra22": False}
    if EXPECTED_P[4] != 29 or EXPECTED_P[8] != 400 or EXPECTED_P[16] != 87867:
        return {"ok": False, "P": EXPECTED_P}
    return {"ok": True, "rows": rows}


def di_dm_prefix() -> dict:
    di = json.loads(DI_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    ok = (
        di["checks"]["all_ok"]
        and di["len2"]["extra"] == 22
        and di["len4"]["n89"] == 8
        and di["len4"]["n372"] == 8
        and dm["checks"]["all_ok"]
        and dm["n8"]["min_nonconst"] == 6344
        and dm["verdict"]["n0_8_min_ident0_extra_6344"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n0_2": 22,
        "n0_4": (89, 372),
        "n0_8_min": 6344,
    }


def ea_prefix() -> dict:
    ea = json.loads(EA_JSON.read_text())
    ok = (
        ea["checks"]["all_ok"]
        and ea["lemmas"]["post_odd_10bit_gap_even_n0"]
        and ea["verdict"]["post_odd_10bit_gap_even_n0"] == "LEMMA"
        and ea["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok, "prize_gap10": ea["prize_gap10"]}


def self_checks(
    c20,
    rec: dict,
    xfold: bool,
    typ: dict,
    lift: dict,
    odd: dict,
    even: dict,
    exact: dict,
    n6: dict,
    prize: dict,
    didm: dict,
    eap: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rec["ok"] and xfold and typ["ok"] and lift["ok"]
    assert odd["ok"] and even["ok"] and exact["ok"] and n6["ok"]
    assert prize["ok"] and didm["ok"] and eap["ok"]
    assert rec["exhaustive"] == 21328
    assert lift["n"] == 16
    assert set(odd["rows"][3]) == N6_FOLD3
    assert even["rows"][2] == 4
    assert exact["rows"][6] == sorted(N6_FOLD3)
    assert exact["rows"][14] == sorted(odd["rows"][7])
    assert n6["n22"] == 4 and n6["n_none"] == 48
    assert prize["rows"][16]["extra22"] is False
    assert didm["n0_2"] == 22 and didm["n0_8_min"] == 6344
    assert typ["rows"][3] == "O" and typ["rows"][4] == "E"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rec = reconstruct_commutes()
    xfold = xorcat_fold_ok()
    typ = type_parity()
    lift = lift_commutes()
    odd = odd_fold_extra22()
    even = even_fold_extra22()
    exact = extra22_exactly_odd_folds()
    n6 = n0_6_census()
    prize = prize_not_odd_fold()
    didm = di_dm_prefix()
    eap = ea_prefix()
    checks = self_checks(
        c20, rec, xfold, typ, lift, odd, even, exact, n6, prize, didm, eap
    )
    dump = {
        "cycle": "EB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "reconstruct_commutes": {
            "exhaustive": rec["exhaustive"],
            "random": rec["random"],
        },
        "type_parity": typ["rows"],
        "odd_fold_T0": odd["rows"],
        "even_fold_n": even["rows"],
        "extra22_exactly_folds": exact["rows"],
        "n0_6": n6,
        "prize_not_odd_fold": prize["rows"],
        "min_extras": {
            "n0_2": 22,
            "n0_4": [89, 372],
            "n0_6": 22,
            "n0_8": 6344,
        },
        "lemmas": {
            "reconstruct_commutes_with_rfold": True,
            "xorcat_of_rfold": True,
            "odd_r_O_even_r_E": True,
            "lift_commutes_with_rfold": True,
            "odd_rfold_odd_ident0_at_22": True,
            "even_rfold_even_ident0_at_22": True,
            "extra22_exactly_odd_folds_n0_le_14": True,
            "n0_6_extra22_is_3fold": True,
            "prize_n0_4_8_16_not_odd_fold": True,
            "min_extra_increases_with_n0": False,
            "extra_gt_22_for_all_n0_ge_4": False,
            "extra_ge_22_all_even_n0": None,
            "post_odd_11bit_gap_all_n0": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reconstruct_commutes_with_rfold": "LEMMA",
            "xorcat_of_rfold": "LEMMA",
            "odd_r_O_even_r_E": "LEMMA",
            "lift_commutes_with_rfold": "LEMMA",
            "odd_rfold_odd_ident0_at_22": "LEMMA",
            "even_rfold_even_ident0_at_22": "LEMMA",
            "extra22_exactly_odd_folds_n0_le_14": "LEMMA",
            "n0_6_extra22_is_3fold": "LEMMA",
            "prize_n0_4_8_16_not_odd_fold": "LEMMA",
            "min_extra_increases_with_n0": "KILLED",
            "extra_gt_22_for_all_n0_ge_4": "KILLED",
            "extra_ge_22_all_even_n0": "PREFIX",
            "post_odd_11bit_gap_all_n0": "PREFIX",
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
    print("n0_6", dump["n0_6"])
    print("extra22_exactly_folds", dump["extra22_exactly_folds"])


if __name__ == "__main__":
    main()
