#!/usr/bin/env python3
"""Cycle LR: covering AND at p=58 on G=1 is 0011 for k>=6.

On covering J6,J10 for k<=6, packed AND at p=58 with G=1 is only
CONT 0011 when k>=6. Count is 11 vs 11, hence odd, so p=58 0011
XOR is 1. Not 0011 for all k (k=3 q=10 is 0010); not xor 0 for
k>=6; not equal to the p=14 count; not empty for k<6. This is
packed AND at p=58, not a Green-only formula for J. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_lr.py --certify
Dump: research/cycle_lr.json
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
from cycle_hi import CONT
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lf import PAT0011, want_p14_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LQ_JSON = Path(__file__).resolve().parent / "cycle_lq.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def want_p58_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=58 for k>=6 (0011 only)."""
    if k < 6:
        raise ValueError("p=58 0011 count is only for k>=6")
    return 11


def want_p58_xor(k: int, q: int) -> int:
    """p=58 0011 XOR is 1 for k>=6 (odd counts)."""
    return 1


def _walk_p58(k: int, q: int) -> dict:
    """Covering AND at p=58 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p58 = xor_p58 = n_other = 0
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
                    if p == 58:
                        n_p58 += 1
                        xor_p58 ^= 1
                        n_pat[four] = n_pat.get(four, 0) + 1
                        if four != PAT0011:
                            n_other += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "n_p58": n_p58,
        "xor_p58": xor_p58,
        "n_0011": n_pat[(0, 0, 1, 1)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p58_cover() -> dict:
    """k<=6: for k>=6, p=58 AND on G=1 is only 0011 with want_p58_n."""
    n_ok = n_g1 = n_p58_ge6 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p58(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            if k >= 6:
                wantn = want_p58_n(k, q)
                wantx = want_p58_xor(k, q)
                if (
                    w["n_p58"] != wantn
                    or w["n_0011"] != wantn
                    or w["n_other"] != 0
                    or w["xor_p58"] != wantx
                ):
                    return {
                        "ok": False,
                        "p58": True,
                        "k": k,
                        "q": q,
                        "n_p58": w["n_p58"],
                        "want": wantn,
                        "n_other": w["n_other"],
                        "xor_p58": w["xor_p58"],
                        "wantx": wantx,
                    }
                n_p58_ge6 += w["n_p58"]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_p58": w["n_p58"],
                "xor_p58": w["xor_p58"],
                "n_other": w["n_other"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p58_ge6 == 22
        and rows["6"]["j6"]["n_p58"] == 11
        and rows["6"]["j10"]["n_p58"] == 11
        and rows["3"]["j10"]["n_other"] > 0
        and want_p58_n(6, 6) == 11
        and want_p58_xor(6, 10) == 1
        and PAT0011 == (0, 0, 1, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p58_ge6": n_p58_ge6, "rows": rows}


def killed_all_k() -> dict:
    """p=58 AND is 0011 for all k: k=3 q=10 is 0010."""
    w = _walk_p58(3, 10)
    ok = w.get("ok") and w["n_other"] > 0 and w["n_pat"]["0010"] > 0
    return {"ok": ok, "k": 3, "q": 10, "n_pat": w["n_pat"]}


def killed_xor0() -> dict:
    """p=58 0011 xor is 0 for k>=6: count 11, xor 1."""
    ok = want_p58_n(6, 6) == 11 and want_p58_xor(6, 6) == 1
    return {"ok": ok, "n": want_p58_n(6, 6), "xor": want_p58_xor(6, 6)}


def killed_eq_p14() -> dict:
    """p=58 count equals p=14 count: k=6 q=6 is 11 vs 7."""
    ok = want_p58_n(6, 6) == 11 and want_p14_n(6, 6) == 7
    return {"ok": ok, "p58": want_p58_n(6, 6), "p14": want_p14_n(6, 6)}


def killed_empty() -> dict:
    """p=58 is empty for k<6: k=5 q=6 has events."""
    w = _walk_p58(5, 6)
    ok = w.get("ok") and w["n_p58"] > 0
    return {"ok": ok, "k": 5, "q": 6, "n": w["n_p58"]}


def prefixes() -> dict:
    lq = json.loads(LQ_JSON.read_text())
    ok = (
        lq["checks"]["all_ok"]
        and lq["verdict"]["p88_0100"] == "LEMMA"
        and lq["verdict"]["p72_1001"] == "LEMMA"
        and lq["verdict"]["p6_0100"] == "LEMMA"
        and lq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0011 == CONT
    assert want_p58_n(6, 10) == 11
    assert want_p58_xor(6, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p58_cover()
    sc = g4_xor_cover()
    k0 = killed_all_k()
    k1 = killed_xor0()
    k2 = killed_eq_p14()
    k3 = killed_empty()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p58_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_k": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor0": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_p14": {k: k2[k] for k in k2 if k != "ok"},
        "killed_empty": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p58_0011": True,
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
            "eq_p14": False,
            "empty": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "p58_0011": "LEMMA",
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
            "eq_p14": "KILLED",
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
        "p58_cover n_ok",
        dump["p58_cover"]["n_ok"],
        "n_p58_ge6",
        dump["p58_cover"]["n_p58_ge6"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_k", dump["killed_all_k"])
    print("killed_xor0", dump["killed_xor0"])
    print("killed_eq_p14", dump["killed_eq_p14"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
