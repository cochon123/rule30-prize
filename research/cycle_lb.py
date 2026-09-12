#!/usr/bin/env python3
"""Cycle LB: covering FRESH 1001 AND xor is J xor 1_{q=6 and k%4==2}.

On covering J6,J10 for k<=6, XOR of packed AND pattern 1001 on G=1
equals J except when q=6 and k%4==2, where it flips. Not equal to J;
not all even k; not all q=6; not only k=2. This is packed AND XOR,
not a Green-only formula for J. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_lb.py --certify
Dump: research/cycle_lb.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LA_JSON = Path(__file__).resolve().parent / "cycle_la.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

PAT1001 = FRESH[2]


def want_1001_rem(k: int, q: int) -> int:
    """1 iff covering 1001 AND xor differs from J."""
    return int(q == 6 and k % 4 == 2)


def _walk_1001(k: int, q: int) -> dict:
    """Covering XOR of packed AND pattern 1001 on G=1, and J."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_1001 = xor_j = xor_1001 = 0
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
                    if four == PAT1001:
                        xor_1001 ^= 1
                        n_1001 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_1001": n_1001,
        "xor_j": xor_j,
        "xor_1001": xor_1001,
        "rem": xor_j ^ xor_1001,
    }


def pat1001_cover() -> dict:
    """k<=6: 1001 AND xor = J xor want_1001_rem; J matches HF/HG."""
    n_ok = n_g1 = n_1001 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_1001(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
            if w["xor_j"] != jwant:
                return {"ok": False, "xor": True, "k": k, "q": q, "got": w["xor_j"], "want": jwant}
            rem = want_1001_rem(k, q)
            if w["rem"] != rem or w["xor_1001"] != (w["xor_j"] ^ rem):
                return {
                    "ok": False,
                    "1001": True,
                    "k": k,
                    "q": q,
                    "xor_1001": w["xor_1001"],
                    "xor_j": w["xor_j"],
                    "rem": w["rem"],
                    "want_rem": rem,
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_1001 += w["n_1001"]
            krow[name] = {
                "n_g1": w["n_g1"],
                "n_1001": w["n_1001"],
                "xor_j": w["xor_j"],
                "xor_1001": w["xor_1001"],
                "rem": w["rem"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and rows["0"]["j6"]["xor_1001"] == 1
        and rows["1"]["j6"]["xor_1001"] == 0
        and rows["2"]["j6"]["rem"] == 1
        and rows["2"]["j6"]["n_1001"] == 5
        and rows["4"]["j6"]["rem"] == 0
        and rows["6"]["j6"]["rem"] == 1
        and rows["6"]["j10"]["rem"] == 0
        and want_1001_rem(2, 6) == 1
        and want_1001_rem(6, 10) == 0
        and PAT1001 == (1, 0, 0, 1)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_1001": n_1001,
        "rows": rows,
    }


def killed_eq_j() -> dict:
    """1001 AND xor equals J: k=2 q=6 is 1 vs J=0."""
    w = _walk_1001(2, 6)
    ok = w.get("ok") and w["xor_j"] == 0 and w["xor_1001"] == 1 and w["n_1001"] == 5
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor_j": w["xor_j"],
        "xor_1001": w["xor_1001"],
        "n_1001": w["n_1001"],
    }


def killed_even_k() -> dict:
    """Remainder is all even k: k=4 q=6 rem=0."""
    ok = want_1001_rem(4, 6) == 0 and want_1001_rem(2, 6) == 1
    return {"ok": ok, "k4": want_1001_rem(4, 6), "k2": want_1001_rem(2, 6)}


def killed_all_q6() -> dict:
    """Remainder is all q=6: k=0 q=6 rem=0."""
    ok = want_1001_rem(0, 6) == 0 and want_1001_rem(2, 6) == 1
    return {"ok": ok, "k0q6": want_1001_rem(0, 6), "k2q6": want_1001_rem(2, 6)}


def killed_k2_only() -> dict:
    """Remainder is only k=2: k=6 q=6 rem=1."""
    ok = want_1001_rem(6, 6) == 1 and want_1001_rem(2, 10) == 0
    return {"ok": ok, "k6q6": want_1001_rem(6, 6), "k2q10": want_1001_rem(2, 10)}


def prefixes() -> dict:
    la = json.loads(LA_JSON.read_text())
    ok = (
        la["checks"]["all_ok"]
        and la["verdict"]["tri_from_mer"] == "LEMMA"
        and la["verdict"]["tri_three_iso"] == "LEMMA"
        and la["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert PAT1001 in FRESH
    assert want_1001_rem(6, 6) == 1
    assert want_1001_rem(7, 6) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = pat1001_cover()
    sc = g4_xor_cover()
    k0 = killed_eq_j()
    k1 = killed_even_k()
    k2 = killed_all_q6()
    k3 = killed_k2_only()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "LB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "pat1001_cover": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_j": {k: k0[k] for k in k0 if k != "ok"},
        "killed_even_k": {k: k1[k] for k in k1 if k != "ok"},
        "killed_all_q6": {k: k2[k] for k in k2 if k != "ok"},
        "killed_k2_only": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "pat1001_rem": True,
            "tri_from_mer": True,
            "tri_three_iso": True,
            "eq_j": False,
            "even_k": False,
            "all_q6": False,
            "k2_only": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "pat1001_rem": "LEMMA",
            "tri_from_mer": "LEMMA",
            "tri_three_iso": "LEMMA",
            "eq_j": "KILLED",
            "even_k": "KILLED",
            "all_q6": "KILLED",
            "k2_only": "KILLED",
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
    print("pat1001_cover n_ok", dump["pat1001_cover"]["n_ok"], "n_1001", dump["pat1001_cover"]["n_1001"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_j", dump["killed_eq_j"])
    print("killed_even_k", dump["killed_even_k"])
    print("killed_all_q6", dump["killed_all_q6"])
    print("killed_k2_only", dump["killed_k2_only"])


if __name__ == "__main__":
    main()
