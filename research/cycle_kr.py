#!/usr/bin/env python3
"""Cycle KR: covering family clip is only the largest Mersenne (and 3*2^k-1 on q=10).

For k<=6, no-00 family clocks with clipped G=1 are: q=6 none if k<2 else
n=2^{k+1}-1; q=10 n=2^{k+2}-1, and also n=3*2^k-1 when k>=2. Not 2^k-1
on q=6; not only the max Mersenne on q=10; not q=6 k=0; not 3U-1 on
q=6. This is covering geometry, not packed AND XOR J. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kr.py --certify
Dump: research/cycle_kr.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_kj import g_wt
from cycle_km import is_no00_family
from cycle_kq import in_support_g1

OUT = Path(__file__).resolve().with_suffix(".json")
KQ_JSON = Path(__file__).resolve().parent / "cycle_kq.json"


def want_clippers(k: int, q: int) -> tuple[int, ...]:
    """Family n with clipped G=1 on covering (k,q)."""
    if q == 6:
        if k < 2:
            return ()
        return ((1 << (k + 1)) - 1,)
    if k < 2:
        return ((1 << (k + 2)) - 1,)
    return (3 * (1 << k) - 1, (1 << (k + 2)) - 1)


def family_clippers(k: int, q: int) -> dict:
    """Family clocks whose in-support G=1 is strictly less than g_wt."""
    U = 1 << k
    T, Q = q * U, covering_Q(q)
    N = U * Q
    got = []
    clips = []
    for n in range(0, N):
        if not is_no00_family(n):
            continue
        w = in_support_g1(n, T)
        c = g_wt(n) - w
        if c < 0:
            return {"ok": False, "neg": True, "n": n, "c": c}
        if c:
            got.append(n)
            clips.append(c)
    want = want_clippers(k, q)
    if tuple(got) != want:
        return {
            "ok": False,
            "set": True,
            "k": k,
            "q": q,
            "got": got,
            "want": list(want),
        }
    return {"ok": True, "n": got, "clip": clips, "T": T, "N": N}


def clip_table() -> dict:
    """Covering k<=6: family clippers match want_clippers."""
    rows = {}
    n_ok = 0
    for k in range(0, 7):
        krow = {}
        for q in (6, 10):
            rec = family_clippers(k, q)
            if not rec.get("ok"):
                return rec
            krow[f"q{q}"] = {key: rec[key] for key in rec if key != "ok"}
            n_ok += 1
        rows[str(k)] = krow
    ok = (
        n_ok == 14
        and rows["0"]["q6"]["n"] == []
        and rows["0"]["q10"]["n"] == [3]
        and rows["1"]["q6"]["n"] == []
        and rows["1"]["q10"]["n"] == [7]
        and rows["2"]["q6"]["n"] == [7]
        and rows["2"]["q10"]["n"] == [11, 15]
        and rows["6"]["q6"]["n"] == [127]
        and rows["6"]["q10"]["n"] == [191, 255]
        and want_clippers(4, 6) == (31,)
        and want_clippers(4, 10) == (47, 63)
    )
    return {"ok": ok, "n_ok": n_ok, "rows": rows}


def killed_q6_half_mer() -> dict:
    """q=6 clips Mersenne 2^k-1: k=2 n=3 has 2n=6 < T/2=12."""
    rec = family_clippers(2, 6)
    n = (1 << 2) - 1
    ok = rec.get("ok") and n == 3 and n not in rec["n"] and rec["n"] == [7]
    return {"ok": ok, "k": 2, "q": 6, "n": n, "clippers": rec.get("n")}


def killed_q10_only_max() -> dict:
    """q=10 clips only the max Mersenne: k=2 also clips n=11=3*4-1."""
    rec = family_clippers(2, 10)
    ok = rec.get("ok") and rec["n"] == [11, 15] and 11 == 3 * 4 - 1
    return {"ok": ok, "k": 2, "q": 10, "clippers": rec.get("n")}


def killed_q6_k0() -> dict:
    """q=6 k=0 max Mersenne clips: n=1 is fully in support."""
    rec = family_clippers(0, 6)
    ok = rec.get("ok") and rec["n"] == [] and rec["N"] == 2
    return {"ok": ok, "k": 0, "q": 6, "clippers": rec.get("n")}


def killed_q6_tri() -> dict:
    """q=6 clips 3*2^k-1: k=2 n=11 is not a covering clock (N=8)."""
    rec = family_clippers(2, 6)
    n = 3 * (1 << 2) - 1
    ok = rec.get("ok") and n == 11 and n >= rec["N"] and 11 not in rec["n"]
    return {"ok": ok, "k": 2, "q": 6, "n": n, "N": rec.get("N")}


def prefixes() -> dict:
    kq = json.loads(KQ_JSON.read_text())
    ok = (
        kq["checks"]["all_ok"]
        and kq["verdict"]["family_wt_odd"] == "LEMMA"
        and kq["verdict"]["fam_cover_parity_q"] == "LEMMA"
        and kq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert want_clippers(0, 6) == ()
    assert want_clippers(5, 10) == (95, 127)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = clip_table()
    sc = g4_xor_cover()
    k0 = killed_q6_half_mer()
    k1 = killed_q10_only_max()
    k2 = killed_q6_k0()
    k3 = killed_q6_tri()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "clip_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_q6_half_mer": {k: k0[k] for k in k0 if k != "ok"},
        "killed_q10_only_max": {k: k1[k] for k in k1 if k != "ok"},
        "killed_q6_k0": {k: k2[k] for k in k2 if k != "ok"},
        "killed_q6_tri": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "family_clippers": True,
            "family_wt_odd": True,
            "fam_cover_parity_q": True,
            "q6_clips_half_mer": False,
            "q10_only_max": False,
            "q6_k0_clips": False,
            "q6_clips_tri": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "family_clippers": "LEMMA",
            "family_wt_odd": "LEMMA",
            "fam_cover_parity_q": "LEMMA",
            "q6_clips_half_mer": "KILLED",
            "q10_only_max": "KILLED",
            "q6_k0_clips": "KILLED",
            "q6_clips_tri": "KILLED",
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
    print("clip_table n_ok", dump["clip_table"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_q6_half_mer", dump["killed_q6_half_mer"])
    print("killed_q10_only_max", dump["killed_q10_only_max"])
    print("killed_q6_k0", dump["killed_q6_k0"])
    print("killed_q6_tri", dump["killed_q6_tri"])


if __name__ == "__main__":
    main()
