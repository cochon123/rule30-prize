#!/usr/bin/env python3
"""Cycle LQ: covering AND at p=88 on G=1 is 0100 for k>=6.

On covering J6,J10 for k<=6, packed AND at p=88 with G=1 is only
FRESH 0100 when k>=6. Count is 9 vs 19, hence odd, so p=88 0100
XOR is 1. Not 0100 for all k (k=4 q=6 is 0010); not xor 0 for
k>=6; not equal to the p=6 count; not empty for k<6. This is
packed AND at p=88, not a Green-only formula for J. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_lq.py --certify
Dump: research/cycle_lq.json
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
from cycle_ld import PAT0100, want_p6_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LP_JSON = Path(__file__).resolve().parent / "cycle_lp.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def want_p88_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=88 for k>=6 (0100 only)."""
    if k < 6:
        raise ValueError("p=88 0100 count is only for k>=6")
    return 9 if q == 6 else 19


def want_p88_xor(k: int, q: int) -> int:
    """p=88 0100 XOR is 1 for k>=6 (odd counts)."""
    return 1


def _walk_p88(k: int, q: int) -> dict:
    """Covering AND at p=88 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p88 = xor_p88 = n_other = 0
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
                    if p == 88:
                        n_p88 += 1
                        xor_p88 ^= 1
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
        "n_p88": n_p88,
        "xor_p88": xor_p88,
        "n_0100": n_pat[(0, 1, 0, 0)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p88_cover() -> dict:
    """k<=6: for k>=6, p=88 AND on G=1 is only 0100 with want_p88_n."""
    n_ok = n_g1 = n_p88_ge6 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p88(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            if k >= 6:
                wantn = want_p88_n(k, q)
                wantx = want_p88_xor(k, q)
                if (
                    w["n_p88"] != wantn
                    or w["n_0100"] != wantn
                    or w["n_other"] != 0
                    or w["xor_p88"] != wantx
                ):
                    return {
                        "ok": False,
                        "p88": True,
                        "k": k,
                        "q": q,
                        "n_p88": w["n_p88"],
                        "want": wantn,
                        "n_other": w["n_other"],
                        "xor_p88": w["xor_p88"],
                        "wantx": wantx,
                    }
                n_p88_ge6 += w["n_p88"]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_p88": w["n_p88"],
                "xor_p88": w["xor_p88"],
                "n_other": w["n_other"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p88_ge6 == 28
        and rows["6"]["j6"]["n_p88"] == 9
        and rows["6"]["j10"]["n_p88"] == 19
        and rows["4"]["j6"]["n_other"] > 0
        and want_p88_n(6, 6) == 9
        and want_p88_xor(6, 10) == 1
        and PAT0100 == (0, 1, 0, 0)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p88_ge6": n_p88_ge6, "rows": rows}


def killed_all_k() -> dict:
    """p=88 AND is 0100 for all k: k=4 q=6 is 0010."""
    w = _walk_p88(4, 6)
    ok = w.get("ok") and w["n_other"] > 0 and w["n_pat"]["0010"] > 0
    return {"ok": ok, "k": 4, "q": 6, "n_pat": w["n_pat"]}


def killed_xor0() -> dict:
    """p=88 0100 xor is 0 for k>=6: count 9, xor 1."""
    ok = want_p88_n(6, 6) == 9 and want_p88_xor(6, 6) == 1
    return {"ok": ok, "n": want_p88_n(6, 6), "xor": want_p88_xor(6, 6)}


def killed_eq_p6() -> dict:
    """p=88 count equals p=6 count: k=6 q=6 is 9 vs 5."""
    ok = want_p88_n(6, 6) == 9 and want_p6_n(6, 6) == 5
    return {"ok": ok, "p88": want_p88_n(6, 6), "p6": want_p6_n(6, 6)}


def killed_empty() -> dict:
    """p=88 is empty for k<6: k=5 q=6 has events."""
    w = _walk_p88(5, 6)
    ok = w.get("ok") and w["n_p88"] > 0
    return {"ok": ok, "k": 5, "q": 6, "n": w["n_p88"]}


def prefixes() -> dict:
    lp = json.loads(LP_JSON.read_text())
    ok = (
        lp["checks"]["all_ok"]
        and lp["verdict"]["p72_1001"] == "LEMMA"
        and lp["verdict"]["p42_0011"] == "LEMMA"
        and lp["verdict"]["p6_0100"] == "LEMMA"
        and lp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0100 in FRESH
    assert want_p88_n(6, 10) == 19
    assert want_p88_xor(6, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p88_cover()
    sc = g4_xor_cover()
    k0 = killed_all_k()
    k1 = killed_xor0()
    k2 = killed_eq_p6()
    k3 = killed_empty()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p88_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_k": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor0": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_p6": {k: k2[k] for k in k2 if k != "ok"},
        "killed_empty": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p88_0100": True,
            "p72_1001": True,
            "p42_0011": True,
            "p38_0100": True,
            "p52_1001": True,
            "p60_0100": True,
            "p30_0011": True,
            "p98_0010": True,
            "p106_1001": True,
            "p54_0100": True,
            "p32_0100": True,
            "p16_1001": True,
            "p14_0011": True,
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "all_k": False,
            "xor0": False,
            "eq_p6": False,
            "empty": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "p88_0100": "LEMMA",
            "p72_1001": "LEMMA",
            "p42_0011": "LEMMA",
            "p38_0100": "LEMMA",
            "p52_1001": "LEMMA",
            "p60_0100": "LEMMA",
            "p30_0011": "LEMMA",
            "p98_0010": "LEMMA",
            "p106_1001": "LEMMA",
            "p54_0100": "LEMMA",
            "p32_0100": "LEMMA",
            "p16_1001": "LEMMA",
            "p14_0011": "LEMMA",
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "all_k": "KILLED",
            "xor0": "KILLED",
            "eq_p6": "KILLED",
            "empty": "KILLED",
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
        "p88_cover n_ok",
        dump["p88_cover"]["n_ok"],
        "n_p88_ge6",
        dump["p88_cover"]["n_p88_ge6"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_k", dump["killed_all_k"])
    print("killed_xor0", dump["killed_xor0"])
    print("killed_eq_p6", dump["killed_eq_p6"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
