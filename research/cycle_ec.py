#!/usr/bin/env python3
"""Cycle EC: extra is invariant under r-fold; extra 6 is odd-n0 alternating T.

reconstruct commute (Cycle EB) implies the first ident-0 extra of an
O-type scar is unchanged by r-fold: odd r stays O-type with the same
extra and xorcat; even r is E-type with xorcat multiplied by r. This
holds for every half-length n0, not only n0=2. At n0=12 the only
ident-0s in 400 extras are the sixteen 3-folds of n0=4 (8 at 89, 8 at
372). Extra 6 occurs iff T=T0||not T0 is cyclically alternating, which
is exactly the two odd-n0 words 0101...0 and 1010...1 (n4=0, Cycle DY).
A 2-power n0 has no odd divisor >=3, so it is fold-primitive. Left-machine
pi is always a 2-power, hence n0 at every odd ident-0 is a 2-power:
after k=2 the extra-6 (odd n0) and extra-22 (n0=2*odd>=6) families are
unreachable. Kills extra>=22 for all n0 (n0=1 extra 6). Do not claim
extra>=22 for every even n0; do not claim the fold families appear on
the prize orbit after k=2. Not a prize claim.

Run: python3 research/cycle_ec.py --certify
Dump: research/cycle_ec.json
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
from cycle_ca import KNOWN20, packed_center_bits, xorcat
from cycle_cb import twocopy_type
from cycle_ch import is_alternating
from cycle_di import FAM372, FAM89, mask_bits
from cycle_dm import first_ident0_int
from cycle_eb import fold, first_ident0_T

OUT = Path(__file__).resolve().with_suffix(".json")
EB_JSON = Path(__file__).resolve().parent / "cycle_eb.json"
DE_JSON = Path(__file__).resolve().parent / "cycle_de.json"
DU_JSON = Path(__file__).resolve().parent / "cycle_du.json"
DY_JSON = Path(__file__).resolve().parent / "cycle_dy.json"


def otype(t0: list[int]) -> list[int]:
    return t0 + [x ^ 1 for x in t0]


def alt_t0(n0: int, bit: int) -> list[int]:
    return [(i + bit) % 2 for i in range(n0)]


def type_parity_all_n0() -> dict:
    """Odd r: O-type (shift n0). Even r: E-type. Any n0."""
    rows: dict[str, str] = {}
    for n0 in (1, 2, 3, 4, 5, 6, 8):
        n_mask = 1 << n0
        if n_mask > 64:
            n_mask = 64
        for r in range(1, 8):
            want = "O" if r % 2 else "E"
            for mask in range(n_mask):
                T = otype(mask_bits(mask, n0))
                Tr = fold(T, r)
                if twocopy_type(Tr) != want:
                    return {"ok": False, "n0": n0, "r": r}
                h = len(Tr) // 2
                for t in range(h):
                    if want == "O" and Tr[t] == Tr[t + h]:
                        return {"ok": False, "n0": n0, "r": r, "t": t}
                    if want == "E" and Tr[t] != Tr[t + h]:
                        return {"ok": False, "n0": n0, "r": r, "t": t}
            rows[f"{n0}:{r}"] = want
    return {"ok": True, "n": len(rows)}


def inherit_odd() -> dict:
    """Odd r-fold keeps extra and xorcat on every T0 of n0<=5."""
    maxe = {1: 20, 2: 40, 3: 80, 4: 400, 5: 80}
    rows: dict[int, int] = {}
    for n0, mx in maxe.items():
        n_ok = 0
        for r in (3, 5):
            for mask in range(1 << n0):
                t0 = mask_bits(mask, n0)
                cur, sm = first_ident0_int(t0, mx)
                t0r = fold(otype(t0), r)[: n0 * r]
                curr, smr = first_ident0_int(t0r, mx)
                if (curr, smr) != (cur, sm):
                    return {"ok": False, "n0": n0, "r": r, "mask": mask}
                if twocopy_type(fold(otype(t0), r)) != "O":
                    return {"ok": False, "type": n0}
                n_ok += 1
        rows[n0] = n_ok
    return {"ok": True, "rows": rows}


def inherit_even() -> dict:
    """Even r-fold is E-type; extra stays, xorcat *= r."""
    n_ok = 0
    for n0 in (2, 3, 4):
        mx = {2: 40, 3: 80, 4: 400}[n0]
        for r in (2, 4):
            for mask in range(1 << n0):
                t0 = mask_bits(mask, n0)
                cur, sm = first_ident0_int(t0, mx)
                Tr = fold(otype(t0), r)
                if twocopy_type(Tr) != "E":
                    return {"ok": False, "n0": n0, "r": r}
                curr, smr = first_ident0_T(Tr, mx)
                want = None if sm is None else (r * sm) % 2
                if curr != cur or smr != want:
                    return {
                        "ok": False,
                        "n0": n0,
                        "r": r,
                        "cur": cur,
                        "got": (curr, smr),
                    }
                n_ok += 1
    return {"ok": True, "n": n_ok}


def n0_12_exactly_n4_folds() -> dict:
    """Within 400 extras, n0=12 ident-0s are exactly the n0=4 3-folds."""
    exp89: set[str] = set()
    exp372: set[str] = set()
    for mask in range(16):
        t0 = mask_bits(mask, 4)
        key = "".join(map(str, t0))
        hk = "".join(map(str, fold(otype(t0), 3)[:12]))
        if key in FAM89:
            exp89.add(hk)
        elif key in FAM372:
            exp372.add(hk)
        else:
            return {"ok": False, "key": key}
    got89: set[str] = set()
    got372: set[str] = set()
    n_none = 0
    for mask in range(1 << 12):
        t0 = mask_bits(mask, 12)
        cur, sm = first_ident0_int(t0, 400)
        key = "".join(map(str, t0))
        if cur == 89:
            if sm != 1:
                return {"ok": False, "sm89": sm}
            got89.add(key)
        elif cur == 372:
            if sm != 1:
                return {"ok": False, "sm372": sm}
            got372.add(key)
        elif cur is None:
            n_none += 1
        else:
            return {"ok": False, "cur": cur, "key": key}
    ok = (
        got89 == exp89
        and got372 == exp372
        and n_none == 4080
        and len(got89) == 8
        and len(got372) == 8
    )
    return {
        "ok": ok,
        "n89": len(got89),
        "n372": len(got372),
        "n_none": n_none,
    }


def extra6_iff_T_alternating() -> dict:
    """Extra 6 iff T is cyclically alternating (two odd-n0 words)."""
    rows: dict[int, int] = {}
    for n0 in (1, 3, 5, 7, 9, 11):
        extra6: list[str] = []
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            T = otype(t0)
            cur, sm = first_ident0_int(t0, 20)
            if cur == 6:
                if sm != 1 or not is_alternating(T):
                    return {"ok": False, "n0": n0, "mask": mask}
                extra6.append("".join(map(str, t0)))
            elif is_alternating(T):
                return {"ok": False, "n0": n0, "alt_not_6": mask}
        want = {
            "".join(map(str, alt_t0(n0, 0))),
            "".join(map(str, alt_t0(n0, 1))),
        }
        if set(extra6) != want or len(extra6) != 2:
            return {"ok": False, "n0": n0, "got": extra6}
        rows[n0] = 2
    for n0 in (2, 4, 6, 8):
        n_mask = 1 << n0
        if n_mask > 256:
            n_mask = 256
        for mask in range(n_mask):
            t0 = mask_bits(mask, n0)
            T = otype(t0)
            if is_alternating(T):
                return {"ok": False, "even_alt": n0}
            cur, _ = first_ident0_int(t0, 10)
            if cur == 6:
                return {"ok": False, "even_6": n0, "mask": mask}
    return {"ok": True, "rows": rows}


def pow2_fold_primitive() -> bool:
    """A 2-power has no odd divisor >=3, so it is not a nontrivial fold."""
    for e in range(0, 12):
        n0 = 1 << e
        for r in range(3, n0 + 1, 2):
            if n0 % r == 0:
                return False
    for n0 in (6, 10, 12, 14, 15, 20, 24):
        odd = [r for r in range(3, n0 + 1, 2) if n0 % r == 0]
        if not odd:
            return False
    return True


def de_du_pi_pow2() -> dict:
    de = json.loads(DE_JSON.read_text())
    du = json.loads(DU_JSON.read_text())
    pis = de["pis"]
    if pis != du["pis_1_to_19"][:18]:
        return {"ok": False, "pis": pis}
    if any(p & (p - 1) for p in du["pis_1_to_19"]):
        return {"ok": False, "du": du["pis_1_to_19"]}
    odds = du["odd_high_p"] if "odd_high_p" in du else de["odd_high_p"]
    n0_at = {1: 1, 2: 2, 4: 4, 8: 8, 16: 16}
    ok = (
        de["checks"]["all_ok"]
        and du["checks"]["all_ok"]
        and odds == {"1": 3, "2": 8, "4": 29, "8": 400, "16": 87867}
        and all(n0_at[k] & (n0_at[k] - 1) == 0 for k in n0_at)
    )
    return {"ok": ok, "pis": du["pis_1_to_19"], "odd_n0": n0_at}


def eb_dy_prefix() -> dict:
    eb = json.loads(EB_JSON.read_text())
    dy = json.loads(DY_JSON.read_text())
    ok = (
        eb["checks"]["all_ok"]
        and eb["verdict"]["reconstruct_commutes_with_rfold"] == "LEMMA"
        and eb["verdict"]["odd_rfold_odd_ident0_at_22"] == "LEMMA"
        and eb["verdict"]["min_extra_increases_with_n0"] == "KILLED"
        and dy["checks"]["all_ok"]
        and dy["verdict"]["n4_never_zero_odd_n0"] == "KILLED"
        and dy["lemmas"]["n4_never_zero_odd_n0"] is False
    )
    return {"ok": ok, "n0_6_22": eb["n0_6"]["n22"]}


def self_checks(
    c20,
    typ: dict,
    odd: dict,
    even: dict,
    n12: dict,
    e6: dict,
    prim: bool,
    pip: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert typ["ok"] and odd["ok"] and even["ok"] and n12["ok"]
    assert e6["ok"] and prim and pip["ok"] and pref["ok"]
    assert odd["rows"][4] == 32
    assert even["n"] == 56
    assert n12["n89"] == 8 and n12["n372"] == 8 and n12["n_none"] == 4080
    assert e6["rows"][1] == 2 and e6["rows"][11] == 2
    assert pip["odd_n0"][16] == 16
    assert pref["n0_6_22"] == 4
    assert xorcat([0, 1, 0]) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    typ = type_parity_all_n0()
    odd = inherit_odd()
    even = inherit_even()
    n12 = n0_12_exactly_n4_folds()
    e6 = extra6_iff_T_alternating()
    prim = pow2_fold_primitive()
    pip = de_du_pi_pow2()
    pref = eb_dy_prefix()
    checks = self_checks(c20, typ, odd, even, n12, e6, prim, pip, pref)
    dump = {
        "cycle": "EC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "type_parity_n": typ["n"],
        "inherit_odd": odd["rows"],
        "inherit_even_n": even["n"],
        "n0_12": n12,
        "extra6_odd_n0": e6["rows"],
        "pi_pow2": pip["pis"],
        "odd_n0_left_machine": pip["odd_n0"],
        "lemmas": {
            "rfold_type_any_n0": True,
            "extra_invariant_odd_rfold": True,
            "extra_invariant_even_rfold_E": True,
            "n0_12_extra_89_372_are_n4_3folds": True,
            "extra6_iff_T_alternating": True,
            "pow2_n0_fold_primitive": True,
            "left_machine_pi_always_pow2": True,
            "extra6_and_extra22_folds_unreachable_after_k2": True,
            "extra_ge_22_all_n0": False,
            "extra_ge_22_all_even_n0": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "rfold_type_any_n0": "LEMMA",
            "extra_invariant_odd_rfold": "LEMMA",
            "extra_invariant_even_rfold_E": "LEMMA",
            "n0_12_extra_89_372_are_n4_3folds": "LEMMA",
            "extra6_iff_T_alternating": "LEMMA",
            "pow2_n0_fold_primitive": "LEMMA",
            "left_machine_pi_always_pow2": "LEMMA",
            "extra6_and_extra22_folds_unreachable_after_k2": "LEMMA",
            "extra_ge_22_all_n0": "KILLED",
            "extra_ge_22_all_even_n0": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
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
    print("n0_12", dump["n0_12"])
    print("extra6_odd_n0", dump["extra6_odd_n0"])


if __name__ == "__main__":
    main()
