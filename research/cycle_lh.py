#!/usr/bin/env python3
"""Cycle LH: covering AND at p=54 on G=1 is always 0100.

On covering J6,J10 for k<=6, packed AND at p=54 with G=1 is only
FRESH 0100. Empty for k<=3; 0 vs 1 at k=4; 2 vs 5 at k=5; 5 vs 5
at k=6. Not 1001 at p=54; not xor 1 at k=5 q=6; not equal to the
p=6 count; not empty for k<5. This is packed AND at p=54, not a
Green-only formula for J. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_lh.py --certify
Dump: research/cycle_lh.json
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
LG_JSON = Path(__file__).resolve().parent / "cycle_lg.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def want_p54_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=54."""
    if k <= 3:
        return 0
    if k == 4:
        return 0 if q == 6 else 1
    if k == 5:
        return 2 if q == 6 else 5
    return 5


def want_p54_xor(k: int, q: int) -> int:
    """p=54 0100 XOR equals the count mod 2."""
    return want_p54_n(k, q) % 2


def _walk_p54(k: int, q: int) -> dict:
    """Covering AND at p=54 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p54 = xor_p54 = n_other = 0
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
                    if p == 54:
                        n_p54 += 1
                        xor_p54 ^= 1
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
        "n_p54": n_p54,
        "xor_p54": xor_p54,
        "n_0100": n_pat[(0, 1, 0, 0)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p54_cover() -> dict:
    """k<=6: p=54 AND on G=1 is only 0100 with want_p54_n count."""
    n_ok = n_g1 = n_p54 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p54(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p54_n(k, q)
            wantx = want_p54_xor(k, q)
            if (
                w["n_p54"] != wantn
                or w["n_0100"] != wantn
                or w["n_other"] != 0
                or w["xor_p54"] != wantx
            ):
                return {
                    "ok": False,
                    "p54": True,
                    "k": k,
                    "q": q,
                    "n_p54": w["n_p54"],
                    "want": wantn,
                    "n_other": w["n_other"],
                    "xor_p54": w["xor_p54"],
                    "wantx": wantx,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_p54 += w["n_p54"]
            krow[name] = {
                "n_p54": w["n_p54"],
                "xor_p54": w["xor_p54"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p54 == 18
        and rows["3"]["j6"]["n_p54"] == 0
        and rows["3"]["j10"]["n_p54"] == 0
        and rows["4"]["j6"]["n_p54"] == 0
        and rows["4"]["j10"]["n_p54"] == 1
        and rows["5"]["j6"]["n_p54"] == 2
        and rows["5"]["j10"]["n_p54"] == 5
        and rows["6"]["j6"]["n_p54"] == 5
        and rows["6"]["j10"]["n_p54"] == 5
        and PAT0100 == (0, 1, 0, 0)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p54": n_p54, "rows": rows}


def killed_other_and() -> dict:
    """p=54 AND can be 1001: k=5 q=10 is only 0100."""
    w = _walk_p54(5, 10)
    ok = (
        w.get("ok")
        and w["n_p54"] == 5
        and w["n_0100"] == 5
        and w["n_other"] == 0
        and w["n_pat"]["1001"] == 0
    )
    return {"ok": ok, "k": 5, "q": 10, "n_pat": w["n_pat"]}


def killed_xor1() -> dict:
    """p=54 0100 xor is 1 at k=5 q=6: count 2, xor 0."""
    ok = want_p54_n(5, 6) == 2 and want_p54_xor(5, 6) == 0
    return {"ok": ok, "n": want_p54_n(5, 6), "xor": want_p54_xor(5, 6)}


def killed_eq_p6() -> dict:
    """p=54 count equals p=6 count: k=5 q=6 is 2 vs 5."""
    ok = want_p54_n(5, 6) == 2 and want_p6_n(5, 6) == 5
    return {"ok": ok, "p54": want_p54_n(5, 6), "p6": want_p6_n(5, 6)}


def killed_empty() -> dict:
    """p=54 is empty for k<5: k=4 q=10 has 1."""
    ok = want_p54_n(4, 10) == 1
    return {"ok": ok, "n": want_p54_n(4, 10)}


def prefixes() -> dict:
    lg = json.loads(LG_JSON.read_text())
    ok = (
        lg["checks"]["all_ok"]
        and lg["verdict"]["p32_0100"] == "LEMMA"
        and lg["verdict"]["p14_0011"] == "LEMMA"
        and lg["verdict"]["p16_1001"] == "LEMMA"
        and lg["verdict"]["p6_0100"] == "LEMMA"
        and lg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0100 in FRESH
    assert want_p54_n(0, 6) == 0
    assert want_p54_n(4, 6) == 0
    assert want_p54_xor(4, 10) == 1
    assert want_p54_xor(6, 6) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p54_cover()
    sc = g4_xor_cover()
    k0 = killed_other_and()
    k1 = killed_xor1()
    k2 = killed_eq_p6()
    k3 = killed_empty()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p54_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_other_and": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_p6": {k: k2[k] for k in k2 if k != "ok"},
        "killed_empty": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p54_0100": True,
            "p32_0100": True,
            "p14_0011": True,
            "p16_1001": True,
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "other_and": False,
            "xor1": False,
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
            "p54_0100": "LEMMA",
            "p32_0100": "LEMMA",
            "p14_0011": "LEMMA",
            "p16_1001": "LEMMA",
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "other_and": "KILLED",
            "xor1": "KILLED",
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
    print("p54_cover n_ok", dump["p54_cover"]["n_ok"], "n_p54", dump["p54_cover"]["n_p54"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_other_and", dump["killed_other_and"])
    print("killed_xor1", dump["killed_xor1"])
    print("killed_eq_p6", dump["killed_eq_p6"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
