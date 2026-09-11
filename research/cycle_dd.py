#!/usr/bin/env python3
"""Cycle DD: period-H seed through k=17; prize even ident-0; pair 17 not closed.

F^H(L_k(2W))=L_k(2W) holds for every 1<=k<=17, with periods
1,2,4,4,8,8,8,8,16x8,32. In particular pi_17=32 divides H=2^16. The prize
scar T0=00000110 hits an even ident-0 (all-zero bit, even xor a) at extra
52807, so an infinite no-zero-column lemma on |T0|=8 is false. The
seventeenth tail pair is equal on 10 even T0||not T0 (n0 in {2,6,10});
10-or-witness-B does not close that pair. 2-power n0 in {4,8,16} stay
unequal there. Not a prize claim.

Run: python3 research/cycle_dd.py --certify
Dump: research/cycle_dd.json
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
from cycle_ca import KNOWN20, apply_n, left_at_2W, min_period, packed_center_bits, xorcat
from cycle_ch import scar_lift
from cycle_ci import EVEN_N0, reset_toggle_step
from cycle_co import has10, pointwise_10_kills

OUT = Path(__file__).resolve().with_suffix(".json")
EXPECTED_PI = (1, 2, 4, 4, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 16, 16, 32)
PRIZE_T0 = [0, 0, 0, 0, 0, 1, 1, 0]


def seed_through_17() -> dict:
    pis: list[int] = []
    for k in range(1, 18):
        W = 1 << k
        H = W >> 1
        w = left_at_2W(k)
        pi = min_period(w, W)
        if pi != EXPECTED_PI[k - 1]:
            return {"ok": False, "k": k, "pi": pi, "pis": pis}
        if apply_n(w, W, H) != w or H % pi:
            return {"ok": False, "k": k, "pi": pi, "why": "seed", "pis": pis}
        pis.append(pi)
    return {"ok": True, "pis": pis, "pi_17": 32}


def prize_even_ident0() -> dict:
    ok_lift = scar_lift(PRIZE_T0, 52806)
    fail = scar_lift(PRIZE_T0, 52807)
    if ok_lift is None or fail is not None:
        return {"ok": False}
    mx = max(ok_lift)
    a, b = ok_lift[mx - 1], ok_lift[mx]
    even = all(x == 0 for x in b) and xorcat(a) == 0
    return {"ok": even, "max_key": mx, "xor_a": xorcat(a), "extra_fail": 52807}


def pair17_census() -> dict:
    n_ok = 0
    n_eq = 0
    n_10 = 0
    n_imp = 0
    n_imp_B = 0
    n_eq_n0: dict[int, int] = {}
    n_eq_pow = 0
    for n0 in EVEN_N0:
        for mask in range(1 << n0):
            T0 = [(mask >> i) & 1 for i in range(n0)]
            if sum(T0) in (0, n0):
                continue
            seqs = scar_lift(T0, 18)
            if seqs is None or 20 not in seqs or not reset_toggle_step(seqs[1], seqs[4]):
                return {"ok": False, "n_ok": n_ok, "why": "lift"}
            A, B, C, D = seqs[17], seqs[18], seqs[19], seqs[20]
            n_ok += 1
            eq = C == D
            if eq:
                n_eq += 1
                n_eq_n0[n0] = n_eq_n0.get(n0, 0) + 1
                if n0 in (4, 8, 16):
                    n_eq_pow += 1
            A10 = has10(A, B)
            if A10:
                n_10 += 1
                if eq:
                    return {"ok": False, "n_ok": n_ok, "why": "10eq"}
            else:
                n_imp += 1
                L = len(A)
                Bwit = False
                for t in range(L):
                    nxt = (t + 1) % L
                    if B[t] == 1 and B[nxt] == 1 and A[t] == A[nxt]:
                        Bwit = True
                        break
                if Bwit:
                    n_imp_B += 1
                    if eq:
                        return {"ok": False, "n_ok": n_ok, "why": "Beq"}
                elif not eq:
                    return {"ok": False, "n_ok": n_ok, "why": "noB_neq"}
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_eq": n_eq,
        "n_10": n_10,
        "n_imp": n_imp,
        "n_imp_B": n_imp_B,
        "n_eq_n0": n_eq_n0,
        "n_eq_pow": n_eq_pow,
    }


def V11_imp_gives_B() -> bool:
    """Local skip-2 witness still holds pointwise; it is not universal at pair 17."""
    Vt = Vn = 1
    Xn = Vt ^ 1
    return Xn == 0 and Xn != Vn


def self_checks(c20, loc: tuple[bool, bool], seed: dict, even0: dict, p17: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert all(loc)
    assert seed["ok"] and seed["pis"] == list(EXPECTED_PI) and seed["pi_17"] == 32
    assert even0["ok"] and even0["xor_a"] == 0 and even0["extra_fail"] == 52807
    expect = sum((1 << n) - 2 for n in EVEN_N0)
    assert p17["ok"] and p17["n_ok"] == expect
    assert p17["n_eq"] == 10 and p17["n_eq_pow"] == 0
    assert p17["n_eq_n0"] == {2: 2, 6: 4, 10: 4}
    assert p17["n_10"] + p17["n_imp"] == expect
    assert p17["n_imp_B"] + p17["n_eq"] == p17["n_imp"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = (pointwise_10_kills(), V11_imp_gives_B())
    seed = seed_through_17()
    even0 = prize_even_ident0()
    p17 = pair17_census()
    checks = self_checks(c20, loc, seed, even0, p17)
    dump = {
        "cycle": "DD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "seed": {"pis": seed["pis"], "pi_17": seed["pi_17"]},
        "even_ident0": {
            "T0": "00000110",
            "extra_fail": even0["extra_fail"],
            "xor_a": even0["xor_a"],
        },
        "pair17": {
            "n_ok": p17["n_ok"],
            "n_eq": p17["n_eq"],
            "n_10": p17["n_10"],
            "n_imp": p17["n_imp"],
            "n_imp_B": p17["n_imp_B"],
            "n_eq_n0": p17["n_eq_n0"],
            "n_eq_pow": p17["n_eq_pow"],
        },
        "lemmas": {
            "period_H_seed_k_le_17": True,
            "pi_17_is_32": True,
            "prize_n0_8_infinite_no_zero": False,
            "seventeenth_pair_never_equal": False,
            "pair17_eq_only_n0_2_6_10": True,
            "pair17_2power_n0_unequal": True,
            "period_H_seed_all_k": None,
            "at_most_one_odd_toggle_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "period_H_seed_k_le_17": "LEMMA",
            "pi_17_is_32": "LEMMA",
            "prize_n0_8_infinite_no_zero": "KILLED",
            "seventeenth_pair_never_equal": "KILLED",
            "pair17_eq_only_n0_2_6_10": "LEMMA",
            "pair17_2power_n0_unequal": "LEMMA",
            "period_H_seed_all_k": "PREFIX",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("seed", dump["seed"])
    print("even_ident0", dump["even_ident0"])
    print("pair17", dump["pair17"])


if __name__ == "__main__":
    main()
