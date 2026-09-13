#!/usr/bin/env python3
"""Cycle LJ: covering AND at p=98 on G=1 is always 0010.

On covering J6,J10 for k<=6, packed AND at p=98 with G=1 is only
FRESH 0010. Empty for k<=4; 0 vs 2 at k=5; 2 vs 5 at k=6. Not
1001 at p=98; not xor 1 at k=5 q=10; not equal to the p=4 count;
not empty for k<6. This is packed AND at p=98, not a Green-only
formula for J. Do not claim J6=J10=0 implies J18=1 for all k; do
not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_lj.py --certify
Dump: research/cycle_lj.json
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
LI_JSON = Path(__file__).resolve().parent / "cycle_li.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

PAT0010 = FRESH[0]


def want_p98_n(k: int, q: int) -> int:
    """Covering G=1 AND count at p=98."""
    if k <= 4:
        return 0
    if k == 5:
        return 0 if q == 6 else 2
    return 2 if q == 6 else 5


def want_p98_xor(k: int, q: int) -> int:
    """p=98 0010 XOR equals the count mod 2."""
    return want_p98_n(k, q) % 2


def _walk_p98(k: int, q: int) -> dict:
    """Covering AND at p=98 on G=1, plus J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = n_p98 = xor_p98 = n_other = 0
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
                    if p == 98:
                        n_p98 += 1
                        xor_p98 ^= 1
                        n_pat[four] = n_pat.get(four, 0) + 1
                        if four != PAT0010:
                            n_other += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "n_p98": n_p98,
        "xor_p98": xor_p98,
        "n_0010": n_pat[(0, 0, 1, 0)],
        "n_other": n_other,
        "n_pat": {"".join(map(str, key)): n_pat[key] for key in n_pat},
    }


def p98_cover() -> dict:
    """k<=6: p=98 AND on G=1 is only 0010 with want_p98_n count."""
    n_ok = n_g1 = n_p98 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_p98(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            wantn = want_p98_n(k, q)
            wantx = want_p98_xor(k, q)
            if (
                w["n_p98"] != wantn
                or w["n_0010"] != wantn
                or w["n_other"] != 0
                or w["xor_p98"] != wantx
            ):
                return {
                    "ok": False,
                    "p98": True,
                    "k": k,
                    "q": q,
                    "n_p98": w["n_p98"],
                    "want": wantn,
                    "n_other": w["n_other"],
                    "xor_p98": w["xor_p98"],
                    "wantx": wantx,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_p98 += w["n_p98"]
            krow[name] = {
                "n_p98": w["n_p98"],
                "xor_p98": w["xor_p98"],
                "xor_j": w["xor_j"],
                "n_pat": w["n_pat"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_p98 == 9
        and rows["4"]["j6"]["n_p98"] == 0
        and rows["4"]["j10"]["n_p98"] == 0
        and rows["5"]["j6"]["n_p98"] == 0
        and rows["5"]["j10"]["n_p98"] == 2
        and rows["6"]["j6"]["n_p98"] == 2
        and rows["6"]["j10"]["n_p98"] == 5
        and PAT0010 == (0, 0, 1, 0)
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_p98": n_p98, "rows": rows}


def killed_other_and() -> dict:
    """p=98 AND can be 1001: k=5 q=10 is only 0010."""
    w = _walk_p98(5, 10)
    ok = (
        w.get("ok")
        and w["n_p98"] == 2
        and w["n_0010"] == 2
        and w["n_other"] == 0
        and w["n_pat"]["1001"] == 0
    )
    return {"ok": ok, "k": 5, "q": 10, "n_pat": w["n_pat"]}


def killed_xor1() -> dict:
    """p=98 0010 xor is 1 at k=5 q=10: count 2, xor 0."""
    ok = want_p98_n(5, 10) == 2 and want_p98_xor(5, 10) == 0
    return {"ok": ok, "n": want_p98_n(5, 10), "xor": want_p98_xor(5, 10)}


def killed_eq_p4() -> dict:
    """p=98 count equals p=4 count: k=6 q=6 is 2 vs 7."""
    ok = want_p98_n(6, 6) == 2 and want_p4_n(6, 6) == 7
    return {"ok": ok, "p98": want_p98_n(6, 6), "p4": want_p4_n(6, 6)}


def killed_empty() -> dict:
    """p=98 is empty for k<6: k=5 q=10 has 2."""
    ok = want_p98_n(5, 10) == 2
    return {"ok": ok, "n": want_p98_n(5, 10)}


def prefixes() -> dict:
    li = json.loads(LI_JSON.read_text())
    ok = (
        li["checks"]["all_ok"]
        and li["verdict"]["p106_1001"] == "LEMMA"
        and li["verdict"]["p54_0100"] == "LEMMA"
        and li["verdict"]["p16_1001"] == "LEMMA"
        and li["verdict"]["p4_1001"] == "LEMMA"
        and li["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT0010 in FRESH
    assert want_p98_n(0, 6) == 0
    assert want_p98_n(5, 6) == 0
    assert want_p98_xor(6, 6) == 0
    assert want_p98_xor(6, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = p98_cover()
    sc = g4_xor_cover()
    k0 = killed_other_and()
    k1 = killed_xor1()
    k2 = killed_eq_p4()
    k3 = killed_empty()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "p98_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_other_and": {k: k0[k] for k in k0 if k != "ok"},
        "killed_xor1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_p4": {k: k2[k] for k in k2 if k != "ok"},
        "killed_empty": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "p98_0010": True,
            "p106_1001": True,
            "p54_0100": True,
            "p16_1001": True,
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "other_and": False,
            "xor1": False,
            "eq_p4": False,
            "empty": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "p98_0010": "LEMMA",
            "p106_1001": "LEMMA",
            "p54_0100": "LEMMA",
            "p16_1001": "LEMMA",
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "other_and": "KILLED",
            "xor1": "KILLED",
            "eq_p4": "KILLED",
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
    print("p98_cover n_ok", dump["p98_cover"]["n_ok"], "n_p98", dump["p98_cover"]["n_p98"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_other_and", dump["killed_other_and"])
    print("killed_xor1", dump["killed_xor1"])
    print("killed_eq_p4", dump["killed_eq_p4"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
