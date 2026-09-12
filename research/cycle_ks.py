#!/usr/bin/env python3
"""Cycle KS: family clip counts are Jacobsthal J_{k+1}-1 and 2^{k+1}-1.

Covering k<=6: q=6 max-Mersenne clip and q=10 3*2^k-1 clip equal
jacobsthal(k+1)-1 (zero if k<2); q=10 max-Mersenne clip is 2^{k+1}-1.
Not Jacobsthal without the -1; not q=6 max = q=10 max; not q=10 tri =
q=10 mer; not q=6 max = 2^{k+1}-1. This is covering geometry, not
packed AND XOR J. Do not claim J6=J10=0 implies J18=1 for all k; do
not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_ks.py --certify
Dump: research/cycle_ks.json
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
from cycle_at import jacobsthal
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_kr import family_clippers

OUT = Path(__file__).resolve().with_suffix(".json")
KR_JSON = Path(__file__).resolve().parent / "cycle_kr.json"


def clip_counts(k: int, q: int) -> tuple[int, ...]:
    """Ones clipped on family clippers, order matching want_clippers."""
    if q == 6:
        if k < 2:
            return ()
        return (jacobsthal(k + 1) - 1,)
    mer = (1 << (k + 1)) - 1
    if k < 2:
        return (mer,)
    return (jacobsthal(k + 1) - 1, mer)


def clip_count_table() -> dict:
    """Covering k<=6: family_clippers clip lists match clip_counts."""
    rows = {}
    n_ok = 0
    for k in range(0, 7):
        krow = {}
        for q in (6, 10):
            rec = family_clippers(k, q)
            if not rec.get("ok"):
                return rec
            got = tuple(rec["clip"])
            want = clip_counts(k, q)
            if got != want:
                return {
                    "ok": False,
                    "set": True,
                    "k": k,
                    "q": q,
                    "got": list(got),
                    "want": list(want),
                }
            if q == 6 and k >= 2:
                alt = g_wt((1 << (k - 1)) - 1) - 1
                if alt != want[0]:
                    return {"ok": False, "wt": True, "k": k, "alt": alt, "want": want[0]}
            krow[f"q{q}"] = {"n": rec["n"], "clip": rec["clip"], "want": list(want)}
            n_ok += 1
        rows[str(k)] = krow
    ok = (
        n_ok == 14
        and rows["0"]["q6"]["clip"] == []
        and rows["0"]["q10"]["clip"] == [1]
        and rows["1"]["q10"]["clip"] == [3]
        and rows["2"]["q6"]["clip"] == [2]
        and rows["2"]["q10"]["clip"] == [2, 7]
        and rows["6"]["q6"]["clip"] == [42]
        and rows["6"]["q10"]["clip"] == [42, 127]
        and clip_counts(4, 6) == (10,)
        and clip_counts(4, 10) == (10, 31)
        and clip_counts(5, 10) == (20, 63)
        and jacobsthal(3) - 1 == 2
        and g_wt(1) - 1 == 2
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_no_minus1() -> dict:
    """Clip is jacobsthal(k+1) without -1: k=2 q=6 is 2 vs 3."""
    k, q = 2, 6
    rec = family_clippers(k, q)
    jac = jacobsthal(k + 1)
    got = rec["clip"][0]
    ok = rec.get("ok") and got == 2 and jac == 3 and got == jac - 1 and got != jac
    return {"ok": ok, "k": k, "q": q, "clip": got, "jac": jac}


def killed_q6_eq_q10_mer() -> dict:
    """q=6 max clip equals q=10 max Mersenne clip: k=2 is 2 vs 7."""
    a = clip_counts(2, 6)
    b = clip_counts(2, 10)
    ok = a == (2,) and b == (2, 7) and a[0] != b[1]
    return {"ok": ok, "k": 2, "q6": list(a), "q10": list(b)}


def killed_q10_tri_eq_mer() -> dict:
    """q=10 tri clip equals q=10 mer clip: k=2 is 2 vs 7."""
    got = clip_counts(2, 10)
    ok = got == (2, 7) and got[0] != got[1]
    return {"ok": ok, "k": 2, "q": 10, "clip": list(got)}


def killed_q6_pow2() -> dict:
    """q=6 max clip is 2^{k+1}-1: k=2 is 2 vs 7."""
    k = 2
    got = clip_counts(k, 6)[0]
    pow2 = (1 << (k + 1)) - 1
    ok = got == 2 and pow2 == 7 and got != pow2
    return {"ok": ok, "k": k, "clip": got, "pow2": pow2}


def prefixes() -> dict:
    kr = json.loads(KR_JSON.read_text())
    ok = (
        kr["checks"]["all_ok"]
        and kr["verdict"]["family_clippers"] == "LEMMA"
        and kr["verdict"]["family_wt_odd"] == "LEMMA"
        and kr["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert clip_counts(0, 6) == ()
    assert clip_counts(0, 10) == (1,)
    assert clip_counts(1, 6) == ()
    assert clip_counts(6, 6) == (42,)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_count_table()
    sc = g4_xor_cover()
    k0 = killed_no_minus1()
    k1 = killed_q6_eq_q10_mer()
    k2 = killed_q10_tri_eq_mer()
    k3 = killed_q6_pow2()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_count_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_no_minus1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_q6_eq_q10_mer": {k: k1[k] for k in k1 if k != "ok"},
        "killed_q10_tri_eq_mer": {k: k2[k] for k in k2 if k != "ok"},
        "killed_q6_pow2": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clip_counts": True,
            "family_clippers": True,
            "family_wt_odd": True,
            "fam_cover_parity_q": True,
            "clip_no_minus1": False,
            "q6_eq_q10_mer": False,
            "q10_tri_eq_mer": False,
            "q6_pow2": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clip_counts": "LEMMA",
            "family_clippers": "LEMMA",
            "family_wt_odd": "LEMMA",
            "fam_cover_parity_q": "LEMMA",
            "clip_no_minus1": "KILLED",
            "q6_eq_q10_mer": "KILLED",
            "q10_tri_eq_mer": "KILLED",
            "q6_pow2": "KILLED",
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
    print("clip_count_table n_ok", dump["clip_count_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_no_minus1", dump["killed_no_minus1"])
    print("killed_q6_eq_q10_mer", dump["killed_q6_eq_q10_mer"])
    print("killed_q10_tri_eq_mer", dump["killed_q10_tri_eq_mer"])
    print("killed_q6_pow2", dump["killed_q6_pow2"])


if __name__ == "__main__":
    main()
