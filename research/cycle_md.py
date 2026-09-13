#!/usr/bin/env python3
"""Cycle MD: covering rest through k<=10 is 1 iff q==10 and k in {2,6,8}.

On covering J6,J10 for k<=10, packed AND xor off {4,6,14} is 1
exactly at (k,q)=(2,10),(6,10),(8,10). Prefix LZ/MA/MB/MC dumps;
no k=10 re-walk. Unique-rest XOR is not always 0 (k=2 q=6 is 1);
leftover XOR is not rest (same cell leftover=1, rest=0). Not
rest10 for all k; not k%4==2 on k<=10; not unique-rest xor vs J.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_md.py --certify
Dump: research/cycle_md.json
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
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED, want_rest
from cycle_mb import want_rest8
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
LZ_JSON = Path(__file__).resolve().parent / "cycle_lz.json"
MA_JSON = Path(__file__).resolve().parent / "cycle_ma.json"
MB_JSON = Path(__file__).resolve().parent / "cycle_mb.json"
MC_JSON = Path(__file__).resolve().parent / "cycle_mc.json"

REST1 = frozenset({(2, 10), (6, 10), (8, 10)})
# Certified unique packed AND slots off {4,6,14} on k<=6 (LC-LU).
UNIQUE_REST = frozenset(
    {16, 30, 32, 38, 42, 52, 54, 58, 60, 72, 76, 86, 88, 98, 106, 114}
)


def want_rest10(k: int, q: int) -> int:
    """AND xor off {4,6,14} on k<=10: 1 iff (k,q) in REST1."""
    return int((k, q) in REST1)


def _walk_split(k: int, q: int) -> dict:
    """Covering rest XOR split into unique-p vs leftover."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = xor_f = xor_rest = xor_u = xor_lo = 0
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
                    if p in FORCED:
                        xor_f ^= 1
                    else:
                        xor_rest ^= 1
                        if p in UNIQUE_REST:
                            xor_u ^= 1
                        else:
                            xor_lo ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "xor_f": xor_f,
        "xor_rest": xor_rest,
        "xor_u": xor_u,
        "xor_lo": xor_lo,
    }


def rest10_prefix() -> dict:
    """k<=10 dumped rest XOR equals want_rest10 (no k=8/10 re-walk)."""
    lz = json.loads(LZ_JSON.read_text())
    ma = json.loads(MA_JSON.read_text())
    mb = json.loads(MB_JSON.read_text())
    mc = json.loads(MC_JSON.read_text())
    rows = {}
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            got = lz["j_form"]["rows"][str(k)][name]["xor_rest"]
            w = want_rest10(k, q)
            if got != w:
                return {"ok": False, "k": k, "q": q, "got": got, "w": w}
            krow[name] = {"xor_rest": got}
        rows[str(k)] = krow
    for k, key in ((7, "k7_holds"), (8, "k8_kill")):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            got = ma[key]["rows"][name]["xor_rest"]
            w = want_rest10(k, q)
            if got != w:
                return {"ok": False, "k": k, "q": q, "got": got, "w": w}
            krow[name] = {"xor_rest": got}
        rows[str(k)] = krow
    for k, blob in ((9, mb["k9_holds"]), (10, mc["k10_kill"])):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            got = blob["rows"][name]["xor_rest"]
            w = want_rest10(k, q)
            if got != w:
                return {"ok": False, "k": k, "q": q, "got": got, "w": w}
            krow[name] = {"xor_rest": got}
        rows[str(k)] = krow
    ok = (
        want_rest10(2, 10) == 1
        and want_rest10(6, 10) == 1
        and want_rest10(8, 10) == 1
        and want_rest10(10, 10) == 0
        and want_rest10(8, 6) == 0
        and want_rest8(8, 10) == 1
        and want_rest8(10, 10) == 1
        and want_rest(10, 10) == 1
        and want_rest(8, 10) == 0
        and rows["8"]["j10"]["xor_rest"] == 1
        and rows["10"]["j10"]["xor_rest"] == 0
    )
    return {"ok": ok, "rows": rows}


def killed_mod4(pref: dict) -> dict:
    """rest=1 iff q==10 and k%4==2 on k<=10: k=8 extra, k=10 missing."""
    ok = (
        pref["rows"]["8"]["j10"]["xor_rest"] == 1
        and want_rest(8, 10) == 0
        and pref["rows"]["10"]["j10"]["xor_rest"] == 0
        and want_rest(10, 10) == 1
    )
    return {
        "ok": ok,
        "k8_rest": pref["rows"]["8"]["j10"]["xor_rest"],
        "k10_rest": pref["rows"]["10"]["j10"]["xor_rest"],
    }


def killed_q10_empty(pref: dict) -> dict:
    """q=10 rest empty through k<=10: (2,10) is 1."""
    ok = pref["rows"]["2"]["j10"]["xor_rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "rest": 1}


def unique_kills() -> dict:
    """k=2 q=6: unique-rest xor is 1, leftover xor is 1, rest is 0."""
    w = _walk_split(2, 6)
    ok = (
        w.get("ok")
        and w["xor_rest"] == 0
        and w["xor_u"] == 1
        and w["xor_lo"] == 1
        and w["xor_rest"] == w["xor_u"] ^ w["xor_lo"]
    )
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor_rest": w.get("xor_rest"),
        "xor_u": w.get("xor_u"),
        "xor_lo": w.get("xor_lo"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def killed_unique0(uk: dict) -> dict:
    """unique-rest XOR always 0: k=2 q=6 is 1."""
    ok = uk["xor_u"] == 1
    return {"ok": ok, "k": 2, "q": 6, "xor_u": uk["xor_u"]}


def killed_left_eq(uk: dict) -> dict:
    """leftover XOR equals rest: k=2 q=6 leftover=1, rest=0."""
    ok = uk["xor_lo"] == 1 and uk["xor_rest"] == 0
    return {"ok": ok, "k": 2, "q": 6, "xor_lo": uk["xor_lo"], "xor_rest": uk["xor_rest"]}


def prefixes() -> dict:
    mc = json.loads(MC_JSON.read_text())
    mb = json.loads(MB_JSON.read_text())
    ok = (
        mc["checks"]["all_ok"]
        and mc["verdict"]["rest8_all"] == "KILLED"
        and mc["verdict"]["k10_kill"] == "KILLED"
        and mb["verdict"]["rest8"] == "LEMMA"
        and mc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    pref10: dict,
    kmod: dict,
    kempty: dict,
    uk: dict,
    ku0: dict,
    kle: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pref10["ok"]
        and kmod["ok"]
        and kempty["ok"]
        and uk["ok"]
        and ku0["ok"]
        and kle["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_rest10(2, 10) == 1 and want_rest10(10, 10) == 0
    assert want_rest10(8, 6) == 0 and want_rest8(8, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pref10 = rest10_prefix()
    kmod = killed_mod4(pref10)
    kempty = killed_q10_empty(pref10)
    uk = unique_kills()
    ku0 = killed_unique0(uk)
    kle = killed_left_eq(uk)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pref10, kmod, kempty, uk, ku0, kle, sc, pref)
    dump = {
        "cycle": "MD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "rest10_prefix": {k: pref10[k] for k in pref10 if k != "ok"},
        "unique_kills": {k: uk[k] for k in uk if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_mod4": {k: kmod[k] for k in kmod if k != "ok"},
        "killed_q10_empty": {k: kempty[k] for k in kempty if k != "ok"},
        "killed_unique0": {k: ku0[k] for k in ku0 if k != "ok"},
        "killed_left_eq": {k: kle[k] for k in kle if k != "ok"},
        "lemmas": {
            "rest10": True,
            "k10_kill": True,
            "forced10": True,
            "q6_rest0": True,
            "rest8": True,
            "k9_holds": True,
            "forced9": True,
            "k7_holds": True,
            "forced8": True,
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "mod4": False,
            "q10_empty": False,
            "unique0": False,
            "left_eq": False,
            "rest8_all": False,
            "j8_all": False,
            "all_k": False,
            "rest_all_k": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "rest10": "LEMMA",
            "k10_kill": "KILLED",
            "forced10": "LEMMA",
            "q6_rest0": "LEMMA",
            "rest8": "LEMMA",
            "k9_holds": "LEMMA",
            "forced9": "LEMMA",
            "k7_holds": "LEMMA",
            "forced8": "LEMMA",
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "mod4": "KILLED",
            "q10_empty": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
            "rest8_all": "KILLED",
            "j8_all": "KILLED",
            "all_k": "KILLED",
            "rest_all_k": "KILLED",
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
    print("unique_kills", dump["unique_kills"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_mod4", dump["killed_mod4"])
    print("killed_q10_empty", dump["killed_q10_empty"])
    print("killed_unique0", dump["killed_unique0"])
    print("killed_left_eq", dump["killed_left_eq"])


if __name__ == "__main__":
    main()
