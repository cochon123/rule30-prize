#!/usr/bin/env python3
"""Cycle LO: covering AND at p=42 on G=1 is 0011 for k>=4.

On covering J6,J10 for k<=6, packed AND at p=42 with G=1 is only
CONT 0011 when k>=4. Count is 1 vs 2 at k=4, 3 vs 7 at k=5, and
7 vs 9 at k=6. XOR is the count mod 2 (0 only at k=4 q=10). Not
0011 for all k (k=3 q=6 is 1001); not xor 1 for all k>=4; not
equal to the p=14 count; not empty for k<5. This is packed AND at
p=42, not a Green-only formula for J. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_lo.py --certify
Dump: research/cycle_lo.json
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
LN_JSON = Path(__file__).resolve().parent / "cycle_ln.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def want_p42_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=42 for k>=4 (0011 only)."""
    if k < 4:
        raise ValueError("p=42 0011 count is only for k>=4")
    if k == 4:
        return 1 if q == 6 else 2
    if k == 5:
        return 3 if q == 6 else 7
    return 7 if q == 6 else 9


def want_p42_xor(k: int, q: int) -> int:
    """p=42 0011 XOR equals the count mod 2 for k>=4."""
    return want_p42_n(k, q) % 2


def _walk_p42(k: int, q: int) -> dict:
    """Covering AND at p=42 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p42 = xor_p42 = n_other = 0
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
                    if p == 42:
                        n_p42 += 1
                        xor_p42 ^= 1
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
        "n_p42": n_p42,
        "xor_p42": xor_p42,
        "n_0011": n_pat[(0, 0, 1, 1)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p42_cover() -> dict:
    """k<=6: for k>=4, p=42 AND on G=1 is only 0011 with want_p42_n."""
    n_ok = n_g1 = n_p42_ge4 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p42(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            if k >= 4:
                wantn = want_p42_n(k, q)
                wantx = want_p42_xor(k, q)
                if (
                    w["n_p42"] != wantn
                    or w["n_0011"] != wantn
                    or w["n_other"] != 0
                    or w["xor_p42"] != wantx
                ):
                    return {
                        "ok": False,
                        "p42": True,
                        "k": k,
                        "q": q,
                        "n_p42": w["n_p42"],
                        "want": wantn,
                        "n_other": w["n_other"],
                        "xor_p42": w["xor_p42"],
                        "wantx": wantx,
                    }
                n_p42_ge4 += w["n_p42"]
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_p42": w["n_p42"],
                "xor_p42": w["xor_p42"],
                "n_other": w["n_other"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p42_ge4 == 29
        and rows["4"]["j6"]["n_p42"] == 1
        and rows["4"]["j10"]["n_p42"] == 2
        and rows["5"]["j6"]["n_p42"] == 3
        and rows["5"]["j10"]["n_p42"] == 7
        and rows["6"]["j6"]["n_p42"] == 7
        and rows["6"]["j10"]["n_p42"] == 9
        and rows["3"]["j6"]["n_other"] > 0
        and want_p42_n(4, 6) == 1
        and want_p42_xor(4, 10) == 0
        and want_p42_xor(5, 6) == 1
        and PAT0011 == (0, 0, 1, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p42_ge4": n_p42_ge4, "rows": rows}


def killed_all_k() -> dict:
    """p=42 AND is 0011 for all k: k=3 q=6 is 1001."""
    w = _walk_p42(3, 6)
    ok = w.get("ok") and w["n_other"] > 0 and w["n_pat"]["1001"] > 0
    return {"ok": ok, "k": 3, "q": 6, "n_pat": w["n_pat"]}


def killed_xor1() -> dict:
    """p=42 0011 xor is 1 for all k>=4: k=4 q=10 count 2, xor 0."""
    ok = want_p42_n(4, 10) == 2 and want_p42_xor(4, 10) == 0
    return {"ok": ok, "n": want_p42_n(4, 10), "xor": want_p42_xor(4, 10)}


def killed_eq_p14() -> dict:
    """p=42 count equals p=14 count: k=4 q=6 is 1 vs 5."""
    ok = want_p42_n(4, 6) == 1 and want_p14_n(4, 6) == 5
    return {"ok": ok, "p42": want_p42_n(4, 6), "p14": want_p14_n(4, 6)}


def killed_empty() -> dict:
    """p=42 is empty for k<5: k=4 q=6 has 1."""
    ok = want_p42_n(4, 6) == 1
    return {"ok": ok, "n": want_p42_n(4, 6)}


def prefixes() -> dict:
    ln = json.loads(LN_JSON.read_text())
    ok = (
        ln["checks"]["all_ok"]
        and ln["verdict"]["p38_0100"] == "LEMMA"
        and ln["verdict"]["p52_1001"] == "LEMMA"
        and ln["verdict"]["p6_0100"] == "LEMMA"
        and ln["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0011 == CONT
    assert want_p42_n(5, 10) == 7
    assert want_p42_n(6, 6) == 7
    assert want_p42_n(6, 10) == 9
    assert want_p42_xor(6, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p42_cover()
    sc = g4_xor_cover()
    k0 = killed_all_k()
    k1 = killed_xor1()
    k2 = killed_eq_p14()
    k3 = killed_empty()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p42_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_k": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_p14": {k: k2[k] for k in k2 if k != "ok"},
        "killed_empty": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
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
            "xor1": False,
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
            "xor1": "KILLED",
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
        "p42_cover n_ok",
        dump["p42_cover"]["n_ok"],
        "n_p42_ge4",
        dump["p42_cover"]["n_p42_ge4"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_k", dump["killed_all_k"])
    print("killed_xor1", dump["killed_xor1"])
    print("killed_eq_p14", dump["killed_eq_p14"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
