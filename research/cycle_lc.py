#!/usr/bin/env python3
"""Cycle LC: covering AND at p=4 on G=1 is always 1001, with odd count.

On covering J6,J10 for k<=6, packed AND at p=4 with G=1 is only FRESH
1001, never 0010/0100/0011. The count is k+1-(k%2) for q=6 and
k+1+(k%2) for q=10, hence odd, so p=4 1001 XOR is 1. Not other
AND_ONES at p=4; not xor 0; not q-independent count; not count k+1.
This is packed AND at the lowest live slot, not a Green-only formula
for J. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_lc.py --certify
Dump: research/cycle_lc.json
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
from cycle_hi import CONT, FRESH
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lb import PAT1001, want_1001_rem
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LB_JSON = Path(__file__).resolve().parent / "cycle_lb.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

OTHER_AND = FRESH[:2] + (CONT,)


def want_p4_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=4."""
    return k + 1 + (k % 2 if q == 10 else -(k % 2))


def _walk_p4(k: int, q: int) -> dict:
    """Covering AND at p=4 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p4 = xor_p4 = n_other = 0
    n_pat = {(0, 0, 1, 0): 0, (0, 1, 0, 0): 0, (1, 0, 0, 1): 0, (0, 0, 1, 1): 0}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                    if p == 4:
                        n_p4 += 1
                        xor_p4 ^= 1
                        n_pat[four] = n_pat.get(four, 0) + 1
                        if four != PAT1001:
                            n_other += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "n_p4": n_p4,
        "xor_p4": xor_p4,
        "n_1001": n_pat[(1, 0, 0, 1)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, k)): n_pat[k] for k in n_pat},
    }


def p4_cover() -> dict:
    """k<=6: p=4 AND on G=1 is only 1001 with want_p4_n count; xor=1."""
    n_ok = n_g1 = n_p4 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p4(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p4_n(k, q)
            if (
                w["n_p4"] != wantn
                or w["n_1001"] != wantn
                or w["n_other"] != 0
                or w["xor_p4"] != 1
                or wantn % 2 == 0
            ):
                return {
                    "ok": False,
                    "p4": True,
                    "k": k,
                    "q": q,
                    "n_p4": w["n_p4"],
                    "want": wantn,
                    "n_other": w["n_other"],
                    "xor_p4": w["xor_p4"],
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_p4 += w["n_p4"]
            krow[name] = {
                "n_p4": w["n_p4"],
                "xor_p4": w["xor_p4"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p4 == 56
        and rows["0"]["j6"]["n_p4"] == 1
        and rows["1"]["j6"]["n_p4"] == 1
        and rows["1"]["j10"]["n_p4"] == 3
        and rows["2"]["j6"]["n_p4"] == 3
        and rows["6"]["j6"]["n_p4"] == 7
        and rows["6"]["j10"]["n_p4"] == 7
        and want_p4_n(5, 6) == 5
        and want_p4_n(5, 10) == 7
        and PAT1001 == (1, 0, 0, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p4": n_p4, "rows": rows}


def killed_other_and() -> dict:
    """p=4 AND can be 0010: k=0 q=6 is only 1001."""
    w = _walk_p4(0, 6)
    ok = (
        w.get("ok")
        and w["n_p4"] == 1
        and w["n_1001"] == 1
        and w["n_other"] == 0
        and w["n_pat"]["0010"] == 0
    )
    return {"ok": ok, "k": 0, "q": 6, "n_pat": w["n_pat"]}


def killed_xor0() -> dict:
    """p=4 1001 xor is 0: k=0 q=6 is 1."""
    ok = want_p4_n(0, 6) == 1 and want_p4_n(0, 6) % 2 == 1
    return {"ok": ok, "n": want_p4_n(0, 6)}


def killed_indep_q() -> dict:
    """p=4 count is independent of q: k=1 is 1 vs 3."""
    ok = want_p4_n(1, 6) == 1 and want_p4_n(1, 10) == 3
    return {"ok": ok, "q6": want_p4_n(1, 6), "q10": want_p4_n(1, 10)}


def killed_k_plus_1() -> dict:
    """p=4 count is k+1: k=1 q=6 is 1 not 2."""
    ok = want_p4_n(1, 6) == 1 and want_p4_n(1, 6) != 2
    return {"ok": ok, "k": 1, "q": 6, "n": want_p4_n(1, 6)}


def prefixes() -> dict:
    lb = json.loads(LB_JSON.read_text())
    ok = (
        lb["checks"]["all_ok"]
        and lb["verdict"]["pat1001_rem"] == "LEMMA"
        and lb["verdict"]["tri_from_mer"] == "LEMMA"
        and lb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT1001 in FRESH
    assert CONT == (0, 0, 1, 1)
    assert OTHER_AND == ((0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 1))
    assert want_p4_n(4, 6) == want_p4_n(4, 10) == 5
    assert want_1001_rem(2, 6) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p4_cover()
    sc = g4_xor_cover()
    k0 = killed_other_and()
    k1 = killed_xor0()
    k2 = killed_indep_q()
    k3 = killed_k_plus_1()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p4_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_other_and": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor0": {k: k1[k] for k in k1 if k != "ok"},
        "killed_indep_q": {k: k2[k] for k in k2 if k != "ok"},
        "killed_k_plus_1": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p4_1001": True,
            "pat1001_rem": True,
            "tri_from_mer": True,
            "other_and": False,
            "xor0": False,
            "indep_q": False,
            "k_plus_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "tri_from_mer": "LEMMA",
            "other_and": "KILLED",
            "xor0": "KILLED",
            "indep_q": "KILLED",
            "k_plus_1": "KILLED",
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
    print("p4_cover n_ok", dump["p4_cover"]["n_ok"], "n_p4", dump["p4_cover"]["n_p4"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_other_and", dump["killed_other_and"])
    print("killed_xor0", dump["killed_xor0"])
    print("killed_indep_q", dump["killed_indep_q"])
    print("killed_k_plus_1", dump["killed_k_plus_1"])


if __name__ == "__main__":
    main()
