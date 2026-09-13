#!/usr/bin/env python3
"""Cycle OL: pal-right S on n=8t+3 is pal-right G xor off residue 0.

Even m: Green even-n/odd-d kills every odd r and every 11, so
S(2m+1) is the xor of G(m, m+r) over r=4,10,16,... <= m+1.
n=8t+3 has m=4t+1; doubling then leaves only pal-right G(t,j)
with (j-t)%3 != 0. That xor is 0 at t=0 (n=3) and 1 for
1<=t<=127 (n=11..1019); not claimed for all t>=1. Not a closed
S for every odd n (n%8==7 open). Not E_k=0 for all k. Do not
catalogue further S/T subregions unless the experiment answers
why E_k=0. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ol.py --certify
Dump: research/cycle_ol.json
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
from cycle_kh import g4_xor_cover
from cycle_ok import pal_right_s

OUT = Path(__file__).resolve().with_suffix(".json")
OK_JSON = Path(__file__).resolve().parent / "cycle_ok.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

M_EVEN = 128
T_N3 = 128


def even_m_s(m: int) -> int:
    """S(2m+1) for even m: xor G(m, m+4+6i) with 4+6i <= m+1."""
    if m % 2:
        raise ValueError("even m required")
    acc = 0
    r = 4
    while r <= m + 1:
        acc ^= G(m, m + r)
        r += 6
    return acc


def pal_right_off0(t: int) -> int:
    """Xor of G(t,j) on pal-right j with (j-t)%3 != 0."""
    acc = 0
    for j in range(t + 1, 2 * t + 1):
        if (j - t) % 3:
            acc ^= G(t, j)
    return acc


def want_n3(t: int) -> int:
    """Certified: S(8t+3) is 1 iff t>0, through t<128."""
    return int(t > 0)


def even_parent() -> dict:
    """m even, m<128: pal_right_s(2m+1) == even_m_s(m)."""
    n_ok = n_one = 0
    sample = {}
    for m in range(0, M_EVEN, 2):
        n = 2 * m + 1
        xor_s, n_s, n_fire = pal_right_s(n)
        want = even_m_s(m)
        if xor_s != want:
            return {"ok": False, "m": m, "xor": xor_s, "want": want}
        n_ok += 1
        n_one += xor_s
        if n <= 17:
            sample[str(n)] = {"xor": xor_s, "n_s": n_s, "n_fire": n_fire, "want": want}
    ok = (
        n_ok == M_EVEN // 2
        and sample["1"]["xor"] == 0
        and sample["9"]["xor"] == 1
        and n_one > 0
        and n_one < n_ok
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "sample": sample}


def n3_off0() -> dict:
    """t<128: pal_right_s(8t+3) == pal_right_off0(t) == want_n3(t)."""
    n_ok = 0
    sample = {}
    for t in range(0, T_N3):
        n = 8 * t + 3
        xor_s, n_s, n_fire = pal_right_s(n)
        off = pal_right_off0(t)
        want = want_n3(t)
        if xor_s != off or xor_s != want:
            return {
                "ok": False,
                "t": t,
                "n": n,
                "xor": xor_s,
                "off": off,
                "want": want,
            }
        n_ok += 1
        if t <= 4 or t in (127,):
            sample[str(t)] = {
                "n": n,
                "xor": xor_s,
                "off": off,
                "n_s": n_s,
                "n_fire": n_fire,
            }
    ok = (
        n_ok == T_N3
        and sample["0"]["xor"] == 0
        and sample["1"]["xor"] == 1
        and sample["2"]["xor"] == 1
        and sample["127"]["xor"] == 1
        and want_n3(0) == 0
        and want_n3(1) == 1
        and want_n3(127) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_N3, "sample": sample}


def killed_n3_all(n3: dict) -> dict:
    ok = n3["sample"]["0"]["xor"] == 0
    return {"ok": ok, "t": 0, "n": 3, "xor": 0}


def killed_odd_closed(even: dict) -> dict:
    """n=1 (odd, n%8==1) is 0 while n=9 is 1: no single odd-n value."""
    ok = even["sample"]["1"]["xor"] == 0 and even["sample"]["9"]["xor"] == 1
    return {"ok": ok, "n1": 0, "n9": 1}


def prefixes() -> dict:
    okj = json.loads(OK_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        okj["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and okj["verdict"]["even_s_vanish"] == "LEMMA"
        and okj["verdict"]["odd_s_doubling"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and okj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, even, n3, k3, kc, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        even["ok"]
        and n3["ok"]
        and k3["ok"]
        and kc["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    even = even_parent()
    n3 = n3_off0()
    k3 = killed_n3_all(n3)
    kc = killed_odd_closed(even)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, even, n3, k3, kc, sc, pref)
    dump = {
        "cycle": "OL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_parent": {k: even[k] for k in even if k != "ok"},
        "n3_off0": {k: n3[k] for k in n3 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_n3_all": {k: k3[k] for k in k3 if k != "ok"},
        "killed_odd_closed": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "even_m_s": True,
            "n3_off0": True,
            "n3_one": True,
            "even_s_vanish": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "n3_all_one": False,
            "odd_s_closed": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_m_s": "LEMMA",
            "n3_off0": "LEMMA",
            "n3_one": "CERTIFIED",
            "even_s_vanish": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "n3_all_one": "KILLED",
            "odd_s_closed": "PREFIX",
            "n3_one_all_t": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("even_parent", dump["even_parent"]["n_ok"], "n_one", dump["even_parent"]["n_one"])
    print("n3_off0 n_ok", dump["n3_off0"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_n3_all", dump["killed_n3_all"])
    print("killed_odd_closed", dump["killed_odd_closed"])


if __name__ == "__main__":
    main()
