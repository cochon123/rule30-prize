#!/usr/bin/env python3
"""Cycle LD: covering AND at p=6 on G=1 is always 0100.

On covering J6,J10 for k<=6, packed AND at p=6 with G=1 is only FRESH
0100. Count is 2 at k=0, else want_p4_n(k-1,6) for q=6 and
want_p4_n(k,6) for q=10. XOR is 0 at k=0 and 1 for k>=1. Not 1001
at p=6; not xor 1 at k=0; not q-independent; not equal to p=4 count.
This is packed AND at p=6, not a Green-only formula for J. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ld.py --certify
Dump: research/cycle_ld.json
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
from cycle_hi import FRESH
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lc import want_p4_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LC_JSON = Path(__file__).resolve().parent / "cycle_lc.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

PAT0100 = FRESH[1]


def want_p6_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=6."""
    if k == 0:
        return 2
    return want_p4_n(k - 1, 6) if q == 6 else want_p4_n(k, 6)


def want_p6_xor(k: int) -> int:
    """p=6 0100 XOR: 0 at k=0, else 1."""
    return 0 if k == 0 else 1


def _walk_p6(k: int, q: int) -> dict:
    """Covering AND at p=6 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p6 = xor_p6 = n_other = 0
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
                    if p == 6:
                        n_p6 += 1
                        xor_p6 ^= 1
                        n_pat[four] = n_pat.get(four, 0) + 1
                        if four != PAT0100:
                            n_other += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "n_p6": n_p6,
        "xor_p6": xor_p6,
        "n_0100": n_pat[(0, 1, 0, 0)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p6_cover() -> dict:
    """k<=6: p=6 AND on G=1 is only 0100 with want_p6_n count."""
    n_ok = n_g1 = n_p6 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p6(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p6_n(k, q)
            wantx = want_p6_xor(k)
            if (
                w["n_p6"] != wantn
                or w["n_0100"] != wantn
                or w["n_other"] != 0
                or w["xor_p6"] != wantx
            ):
                return {
                    "ok": False,
                    "p6": True,
                    "k": k,
                    "q": q,
                    "n_p6": w["n_p6"],
                    "want": wantn,
                    "n_other": w["n_other"],
                    "xor_p6": w["xor_p6"],
                    "wantx": wantx,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_p6 += w["n_p6"]
            krow[name] = {
                "n_p6": w["n_p6"],
                "xor_p6": w["xor_p6"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p6 == 46
        and rows["0"]["j6"]["n_p6"] == 2
        and rows["0"]["j6"]["xor_p6"] == 0
        and rows["1"]["j6"]["n_p6"] == 1
        and rows["2"]["j10"]["n_p6"] == 3
        and rows["6"]["j6"]["n_p6"] == 5
        and rows["6"]["j10"]["n_p6"] == 7
        and want_p6_n(5, 6) == 5
        and want_p6_n(5, 10) == 5
        and PAT0100 == (0, 1, 0, 0)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p6": n_p6, "rows": rows}


def killed_other_and() -> dict:
    """p=6 AND can be 1001: k=0 q=6 is only 0100."""
    w = _walk_p6(0, 6)
    ok = (
        w.get("ok")
        and w["n_p6"] == 2
        and w["n_0100"] == 2
        and w["n_other"] == 0
        and w["n_pat"]["1001"] == 0
    )
    return {"ok": ok, "k": 0, "q": 6, "n_pat": w["n_pat"]}


def killed_xor1() -> dict:
    """p=6 0100 xor is 1 at k=0: count 2, xor 0."""
    ok = want_p6_n(0, 6) == 2 and want_p6_xor(0) == 0
    return {"ok": ok, "n": want_p6_n(0, 6), "xor": want_p6_xor(0)}


def killed_indep_q() -> dict:
    """p=6 count is independent of q: k=2 is 1 vs 3."""
    ok = want_p6_n(2, 6) == 1 and want_p6_n(2, 10) == 3
    return {"ok": ok, "q6": want_p6_n(2, 6), "q10": want_p6_n(2, 10)}


def killed_eq_p4() -> dict:
    """p=6 count equals p=4 count: k=0 is 2 vs 1."""
    ok = want_p6_n(0, 6) == 2 and want_p4_n(0, 6) == 1
    return {"ok": ok, "p6": want_p6_n(0, 6), "p4": want_p4_n(0, 6)}


def prefixes() -> dict:
    lc = json.loads(LC_JSON.read_text())
    ok = (
        lc["checks"]["all_ok"]
        and lc["verdict"]["p4_1001"] == "LEMMA"
        and lc["verdict"]["pat1001_rem"] == "LEMMA"
        and lc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0100 in FRESH
    assert want_p6_n(0, 10) == 2
    assert want_p6_n(4, 6) == 3
    assert want_p6_n(4, 10) == 5
    assert want_p6_xor(3) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p6_cover()
    sc = g4_xor_cover()
    k0 = killed_other_and()
    k1 = killed_xor1()
    k2 = killed_indep_q()
    k3 = killed_eq_p4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p6_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_other_and": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_indep_q": {k: k2[k] for k in k2 if k != "ok"},
        "killed_eq_p4": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "other_and": False,
            "xor1": False,
            "indep_q": False,
            "eq_p4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "other_and": "KILLED",
            "xor1": "KILLED",
            "indep_q": "KILLED",
            "eq_p4": "KILLED",
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
    print("p6_cover n_ok", dump["p6_cover"]["n_ok"], "n_p6", dump["p6_cover"]["n_p6"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_other_and", dump["killed_other_and"])
    print("killed_xor1", dump["killed_xor1"])
    print("killed_indep_q", dump["killed_indep_q"])
    print("killed_eq_p4", dump["killed_eq_p4"])


if __name__ == "__main__":
    main()
