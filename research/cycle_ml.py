#!/usr/bin/env python3
"""Cycle ML: on q=6 and q=10 for k<=8, xor of G(n,j-1) on G=1 at j=n+2 vanishes.

On covering J6,J10 for k<=8, XOR of G(n,j-1) over covering G=1
cells with j=n+2 (p=T-2j>=0; no packed row) is 0. Counts are even
(empty only at k=0 q=6). Not rest; not d=2 empty on q=10; not all
palindrome offsets (d=4 at k=1 q=10 xor=1); not Green-only rest;
not the form for all k. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_ml.py --certify
Dump: research/cycle_ml.json
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
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10

OUT = Path(__file__).resolve().with_suffix(".json")
MK_JSON = Path(__file__).resolve().parent / "cycle_mk.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def _walk_off(k: int, q: int, d: int) -> dict:
    """Covering G=1 xor of G(n,j-1) at palindrome offset j=n+d."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_off = xor_off = 0
    t = 0
    s = t0 + 1
    while s < T:
        n = odd_clock(t, U, Q)
        for j in range(0, 2 * n + 1):
            p = T - 2 * j
            if p < 0:
                continue
            n_ok += 1
            if G(n, j) == 0:
                continue
            n_g1 += 1
            if j - n == d:
                n_off += 1
                xor_off ^= G(n, j - 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_off": n_off,
        "xor_off": xor_off,
    }


def bothq_d2() -> dict:
    """k<=8 both q: j=n+2 xor of G(n,j-1) on G=1 is 0; n_off even."""
    n_ok = n_g1 = n_off = 0
    rows = {}
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_off(k, q, 2)
            mj_n = mj["bothq_jgtn"]["rows"][str(k)][name]["n_ok"]
            mj_g = mj["bothq_jgtn"]["rows"][str(k)][name]["n_g1"]
            if (
                not w.get("ok")
                or w["xor_off"] != 0
                or w["n_off"] % 2 != 0
                or w["n_ok"] != mj_n
                or w["n_g1"] != mj_g
            ):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "xor_off": w.get("xor_off"),
                    "n_off": w.get("n_off"),
                }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_off += w["n_off"]
            krow[name] = {
                "xor_off": w["xor_off"],
                "n_off": w["n_off"],
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
            }
        rows[str(k)] = krow
    ok = (
        all(rows[str(k)][name]["xor_off"] == 0 for k in range(0, 9) for name in ("j6", "j10"))
        and rows["0"]["j10"]["n_off"] == 2
        and rows["0"]["j6"]["n_off"] == 0
        and rows["8"]["j10"]["n_off"] == 342
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_off": n_off, "rows": rows}


def killed_eq_rest(both: dict) -> dict:
    """d=2 xor equals rest: xor is 0, rest is 1 at k=2 q=10."""
    r = both["rows"]["2"]["j10"]
    wr = want_rest10(2, 10)
    ok = r["xor_off"] == 0 and wr == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_off": r["xor_off"], "rest": wr}


def killed_empty(both: dict) -> dict:
    """d=2 G=1 empty on q=10: k=0 has n_off=2."""
    r = both["rows"]["0"]["j10"]
    ok = r["n_off"] == 2 and r["xor_off"] == 0
    return {"ok": ok, "k": 0, "q": 10, "n_off": r["n_off"]}


def killed_all_off() -> dict:
    """all palindrome offsets vanish: d=4 at k=1 q=10 xor=1."""
    w = _walk_off(1, 10, 4)
    ok = w.get("ok") and w["xor_off"] == 1 and w["n_off"] == 3
    return {
        "ok": ok,
        "k": 1,
        "q": 10,
        "d": 4,
        "xor_off": w.get("xor_off"),
        "n_off": w.get("n_off"),
    }


def prefixes() -> dict:
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mk["checks"]["all_ok"]
        and mk["verdict"]["inner0"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    both: dict,
    keq: dict,
    kemp: dict,
    kall: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        both["ok"]
        and keq["ok"]
        and kemp["ok"]
        and kall["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    assert both["n_ok"] == mj["bothq_jgtn"]["n_ok"]
    assert both["n_g1"] == mj["bothq_jgtn"]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    both = bothq_d2()
    keq = killed_eq_rest(both)
    kemp = killed_empty(both)
    kall = killed_all_off()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, both, keq, kemp, kall, sc, pref)
    dump = {
        "cycle": "ML",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "bothq_d2": {k: both[k] for k in both if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_all_off": {k: kall[k] for k in kall if k != "ok"},
        "lemmas": {
            "d2_zero": True,
            "inner0": True,
            "jgtn_even": True,
            "jeqn_one": True,
            "q10_jm1": True,
            "rest10": True,
            "eq_rest": False,
            "d2_empty": False,
            "all_off": False,
            "green_only_rest": False,
            "all_k": False,
            "u_vs_j": False,
            "unique0": False,
            "left_eq": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "d2_zero": "LEMMA",
            "inner0": "LEMMA",
            "jgtn_even": "LEMMA",
            "jeqn_one": "LEMMA",
            "q10_jm1": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "d2_empty": "KILLED",
            "all_off": "KILLED",
            "green_only_rest": "KILLED",
            "all_k": "KILLED",
            "u_vs_j": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
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
    print("bothq_d2 n_ok", dump["bothq_d2"]["n_ok"], "n_g1", dump["bothq_d2"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_all_off", dump["killed_all_off"])


if __name__ == "__main__":
    main()
