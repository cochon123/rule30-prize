#!/usr/bin/env python3
"""Cycle DS: even-spine covering-failure empty through k=18 (no Fermat table).

Cycle BO: covering at k+1 fails iff phi^{(6)}_k = phi^{(10)}_k = phi^{(18)}_k
= I_{k+1}, with I_{k+1}=phi^{(2)}_k. That dangerous set is empty for
2<=k<=12. Packed even-spine sampling extends emptiness through k=18, so
the Fermat covering does not fail through k=19. Candidates (6 and 10 match
I, 18 does not) sit at k=5,8,11,15,18. I_k through k=21 still takes both
values. Do not compute phi^{(3,5,9)} at k=16. Not a prize claim: emptiness
and the period-H seed remain prefixes.

Run: python3 research/cycle_ds.py --certify
Dump: research/cycle_ds.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
BO_JSON = Path(__file__).resolve().parent / "cycle_bo.json"
BE_JSON = Path(__file__).resolve().parent / "cycle_be.json"

KMAX = 18
BO_KMAX = 13
EVEN_Q = (2, 6, 10, 18)


class PackedCentre:
    """Packed Rule 30 row; centre bit at time t is (row >> t) & 1."""

    def __init__(self) -> None:
        self.row = 1
        self.t = 0

    def sample_until(self, times: set[int], t_end: int) -> dict[int, int]:
        """Evolve through t_end inclusive; return requested bits in range."""
        row = self.row
        t = self.t
        order = [x for x in sorted(times) if t <= x <= t_end]
        j = 0
        n = len(order)
        nxt = order[0] if order else -1
        out: dict[int, int] = {}
        while t <= t_end:
            if t == nxt:
                out[t] = (row >> t) & 1
                j += 1
                nxt = order[j] if j < n else -1
            row = (row << 2) ^ ((row << 1) | row)
            t += 1
        self.row = row
        self.t = t
        return out


def wanted_pass1(kmax: int) -> tuple[set[int], int]:
    """Times for I_k, phi2/6/10 through kmax, and phi18 through min(kmax,17)."""
    want: set[int] = set()
    for k in range(2, kmax + 1):
        u = 1 << k
        want.add(u)
        want.add(2 * u)
        want.add(6 * u)
        want.add(10 * u)
    for k in range(2, min(kmax, 17) + 1):
        want.add(18 * (1 << k))
    t1 = max(want)
    k_pow = 0
    while (1 << k_pow) <= t1:
        want.add(1 << k_pow)
        k_pow += 1
    return want, t1


def phi_at(centre: dict[int, int], q: int, k: int) -> int:
    u = 1 << k
    return centre[q * u] ^ centre[u]


def spines_from(centre: dict[int, int], kmax: int) -> dict:
    ks = list(range(2, kmax + 1))
    i_max = max(k for k in range(1, 40) if (1 << k) in centre)
    i_vals = []
    for k in range(1, i_max + 1):
        i_vals.append(centre[1 << k] ^ centre[1 << (k - 1)])
    p2, p6, p10, p18 = [], [], [], []
    p18_known = []
    for k in ks:
        p2.append(phi_at(centre, 2, k))
        p6.append(phi_at(centre, 6, k))
        p10.append(phi_at(centre, 10, k))
        t18 = 18 * (1 << k)
        if t18 in centre and (1 << k) in centre:
            p18.append(phi_at(centre, 18, k))
            p18_known.append(True)
        else:
            p18.append(None)
            p18_known.append(False)
    return {
        "k": ks,
        "I": i_vals,
        "I_kmax": i_max,
        "phi2": p2,
        "phi6": p6,
        "phi10": p10,
        "phi18": p18,
        "phi18_known": p18_known,
    }


def candidates_and_dangerous(sp: dict) -> tuple[list[int], list[int], list[int]]:
    """candidate: phi6=phi10=I; dangerous: those with phi18=I too."""
    cand = []
    dang = []
    inferred_fail = []
    for i, k in enumerate(sp["k"]):
        i_next = sp["phi2"][i]
        six = sp["phi6"][i]
        ten = sp["phi10"][i]
        is_cand = six == i_next and ten == i_next
        if is_cand:
            cand.append(k)
        eighteen = sp["phi18"][i]
        if eighteen is None:
            if is_cand:
                continue
            aligned = False
        else:
            aligned = is_cand and eighteen == i_next
        if aligned:
            dang.append(k)
            inferred_fail.append(k + 1)
    return cand, dang, inferred_fail


def bo_prefix() -> dict:
    bo = json.loads(BO_JSON.read_text())
    be = json.loads(BE_JSON.read_text())
    be_i = {rec["k"]: rec["I"] for rec in be["annulus"] if rec["k"] >= 1}
    return {
        "ok": bo["checks"]["all_ok"] and bo["dangerous_k"] == [],
        "k": bo["prefix"]["k"],
        "phi2": bo["prefix"]["phi2"],
        "phi6": bo["prefix"]["phi6"],
        "phi10": bo["prefix"]["phi10"],
        "phi18": bo["prefix"]["phi18"],
        "be_I": be_i,
    }


def self_checks(c20, bo: dict, sp: dict, cand: list[int], dang: list[int]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert bo["ok"]
    assert bo["k"] == list(range(2, BO_KMAX + 1))
    nbo = len(bo["k"])
    assert sp["phi2"][:nbo] == bo["phi2"]
    assert sp["phi6"][:nbo] == bo["phi6"]
    assert sp["phi10"][:nbo] == bo["phi10"]
    assert sp["phi18"][:nbo] == bo["phi18"]
    assert all(sp["phi18_known"][:nbo])
    for k, i_val in bo["be_I"].items():
        assert 1 <= k <= sp["I_kmax"]
        assert sp["I"][k - 1] == i_val
    for i, k in enumerate(sp["k"]):
        # I_{k+1} = c[2^{k+1}] xor c[2^k] = phi^{(2)}_k
        if k + 1 <= sp["I_kmax"]:
            assert sp["phi2"][i] == sp["I"][k]
    assert dang == [k for k in dang if k >= 2]
    assert all(k not in dang for k in range(2, 13))
    assert all(k in cand for k in dang)
    # phi18 is known through k=17 from pass 1, so dangerous through 17 is decided
    for i, k in enumerate(sp["k"]):
        if k <= 17:
            assert sp["phi18_known"][i]
    if 18 in sp["k"] and all(sp["phi18_known"]):
        assert cand == [5, 8, 11, 15, 18]
        assert dang == []
        assert sp["I"] == [
            1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1
        ]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--kmax", type=int, default=KMAX)
    args = parser.parse_args()
    kmax = args.kmax
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    bo = bo_prefix()
    want, t1 = wanted_pass1(kmax)
    packed = PackedCentre()
    centre = packed.sample_until(want, t1)
    # k=18 phi18 sits at 18*2^18 > t1; continue only if 6 and 10 already match I
    if kmax >= 18:
        u18 = 1 << 18
        if (6 * u18 in centre and 10 * u18 in centre and u18 in centre
                and (1 << 19) in centre):
            i19 = centre[1 << 19] ^ centre[u18]
            p6 = centre[6 * u18] ^ centre[u18]
            p10 = centre[10 * u18] ^ centre[u18]
            if p6 == i19 and p10 == i19:
                t18 = 18 * u18
                centre.update(packed.sample_until({t18}, t18))
    sp = spines_from(centre, kmax)
    cand, dang, inferred_fail = candidates_and_dangerous(sp)
    checks = self_checks(c20, bo, sp, cand, dang)
    empty_upto = 1
    for i, k in enumerate(sp["k"]):
        decided = k not in cand or sp["phi18_known"][i]
        if not decided:
            break
        if k in dang:
            break
        empty_upto = k

    def empty_through(upto: int):
        if any(2 <= d <= upto for d in dang):
            return False
        if empty_upto >= upto:
            return True
        return None

    empty_17 = empty_through(17)
    empty_18 = empty_through(18)
    cover_killed = dang != []

    def v_empty(flag):
        if flag is True:
            return "PREFIX"
        if flag is False:
            return "KILLED"
        return "OPEN"

    dump = {
        "cycle": "DS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "kmax": kmax,
        "t1": t1,
        "t_final": packed.t - 1,
        "I": sp["I"],
        "I_kmax": sp["I_kmax"],
        "prefix": {
            "k": sp["k"],
            "phi2": sp["phi2"],
            "phi6": sp["phi6"],
            "phi10": sp["phi10"],
            "phi18": sp["phi18"],
            "phi18_known": sp["phi18_known"],
        },
        "candidate_k": cand,
        "dangerous_k": dang,
        "inferred_cover_fail_at": inferred_fail,
        "empty_upto": empty_upto,
        "lemmas": {
            "cover_fails_iff_even_spines_eq_I": True,
            "dangerous_set_k_2_to_12_empty": True,
            "dangerous_set_k_2_to_17_empty": empty_17,
            "dangerous_set_k_2_to_18_empty": empty_18,
            "fermat_cover_359_all_k": None if not cover_killed else False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "cover_fails_iff_even_spines_eq_I": "LEMMA",
            "dangerous_set_k_2_to_12_empty": "PREFIX",
            "dangerous_set_k_2_to_17_empty": v_empty(empty_17),
            "dangerous_set_k_2_to_18_empty": v_empty(empty_18),
            "fermat_cover_359_all_k": "KILLED" if cover_killed else "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "period_H_seed_all_k": "PREFIX",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("I_kmax", sp["I_kmax"], "I", sp["I"])
    print("candidate_k", cand)
    print("dangerous_k", dang)
    print("inferred_cover_fail_at", inferred_fail)
    print("phi6", sp["phi6"])
    print("phi10", sp["phi10"])
    print("phi18", sp["phi18"])


if __name__ == "__main__":
    main()
