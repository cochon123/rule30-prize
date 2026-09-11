#!/usr/bin/env python3
"""Cycle CG: odd 2-copy scar drives have no later ident-0 for |T0| in {4,8}.

Unique continuation after ident-0, T=T0||not T0, ident-1 depends only on T.
Every nonconstant T0 of length 4 (resp. 8) produces no AND-triple and no
later ident-0 in the next 80 (resp. 130) bits; length 2 always hits a
second odd doubling. Both implications with c not 0 still occur. The
prize k=4 and k=8 odd lifts are instances. Not a prize claim: longer
T0 and the Fermat covering remain prefixes.

Run: python3 research/cycle_cg.py --certify
Dump: research/cycle_cg.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct, xorcat
from cycle_ce import implies

OUT = Path(__file__).resolve().with_suffix(".json")


def scar_lift(T0: list[int], n_extra: int) -> dict[int, list[int]] | None:
    n0 = len(T0)
    T = T0 + [x ^ 1 for x in T0]
    L = 2 * n0
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    for cur in range(3, 3 + n_extra):
        a, b = seqs[cur - 2], seqs[cur - 1]
        if all(x == 0 for x in b):
            sm = xorcat(a)
            u = [0] * L
            for t in range(L - 1):
                u[t + 1] = a[t] ^ u[t]
            if sm == 1:
                return None
            seqs[cur] = u
        else:
            u = reconstruct(a, b)
            if u is None:
                return None
            seqs[cur] = u
    return seqs


def count_tail(seqs: dict[int, list[int]]) -> dict:
    n_and = 0
    n_ident0 = 0
    n_both_nz = 0
    for q in range(3, max(seqs) + 1):
        c, a, b = seqs[q - 3], seqs[q - 2], seqs[q - 1]
        if all(x == 0 for x in seqs[q]):
            n_ident0 += 1
        if c == [x & y for x, y in zip(a, b)]:
            n_and += 1
        if implies(c, a) and implies(c, b) and any(c):
            n_both_nz += 1
    return {"n_and": n_and, "n_ident0": n_ident0, "n_both_nz": n_both_nz}


def exhaust(n0: int, n_extra: int) -> dict:
    n_ok = 0
    n_none = 0
    tot_and = 0
    tot_z = 0
    tot_both = 0
    for mask in range(1 << n0):
        T0 = [(mask >> i) & 1 for i in range(n0)]
        if sum(T0) in (0, n0):
            continue
        seqs = scar_lift(T0, n_extra)
        if seqs is None:
            n_none += 1
            continue
        n_ok += 1
        c = count_tail(seqs)
        tot_and += c["n_and"]
        tot_z += c["n_ident0"]
        tot_both += c["n_both_nz"]
    return {
        "n0": n0,
        "n_extra": n_extra,
        "n_ok": n_ok,
        "n_none": n_none,
        "tot_and": tot_and,
        "tot_ident0": tot_z,
        "tot_both_nz": tot_both,
        "clean": n_ok > 0 and tot_and == 0 and tot_z == 0,
    }


def self_checks(c20, e2: dict, e4: dict, e8: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert e2["n_ok"] == 0 and e2["n_none"] == 2
    assert e4["clean"] and e4["n_ok"] == 14
    assert e8["clean"] and e8["n_ok"] == 254
    assert e8["tot_both_nz"] > 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    e2 = exhaust(2, 20)
    e4 = exhaust(4, 80)
    e8 = exhaust(8, 130)
    checks = self_checks(c20, e2, e4, e8)
    dump = {
        "cycle": "CG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "e2": e2,
        "e4": {k: e4[k] for k in ("n0", "n_extra", "n_ok", "n_none", "tot_and", "tot_ident0", "tot_both_nz")},
        "e8": {k: e8[k] for k in ("n0", "n_extra", "n_ok", "n_none", "tot_and", "tot_ident0", "tot_both_nz")},
        "lemmas": {
            "n0_2_always_second_double": True,
            "n0_4_no_later_ident0": True,
            "n0_8_no_later_ident0": True,
            "no_both_nz_after_scar": False,
            "all_T0_2power_no_later_ident0": None,
            "at_most_one_odd_toggle_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n0_2_always_second_double": "LEMMA",
            "n0_4_no_later_ident0": "LEMMA",
            "n0_8_no_later_ident0": "LEMMA",
            "no_both_nz_after_scar": "KILLED",
            "all_T0_2power_no_later_ident0": "PREFIX",
            "at_most_one_odd_toggle_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("e2", e2)
    print("e4", dump["e4"])
    print("e8", dump["e8"])


if __name__ == "__main__":
    main()
