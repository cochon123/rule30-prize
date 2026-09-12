#!/usr/bin/env python3
"""Cycle HG: J10 and J18 are the in-support j-index from time 2U.

Cycle HF put J6 on [2U,6U) with Q=2. The other covering remainders
are the same clock: J10 on [2U,10U) with Q=4, J18 on [2U,18U) with
Q=8, left-clipped for s<T/2-1. mid10 is not J10 (k=2: 0 vs 1);
tail is not J18 (k=2: 1 vs 0). Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_hg.py --certify
Dump: research/cycle_hg.json
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
from cycle_hc import _walk_in
from cycle_hf import J6_WINDOW
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"
FH_JSON = Path(__file__).resolve().parent / "cycle_fh.json"

# Full covering remainders from t0=2U. Q=(q-2)/2.
J10_WINDOW = ("j10", 10, 2, 4)
J18_WINDOW = ("j18", 18, 2, 8)


def covering_Q(q: int) -> int:
    return (q - 2) // 2


def _walk_jq(k: int, q: int, split_muls: tuple[int, ...]) -> dict:
    """GX/GY on [2U,qU)->qU with Q=(q-2)/2; split XOR; left clip."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    splits = [m * U for m in split_muls]
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    xor_odd = xor_even = xor_andT = 0
    parts = [0] * (len(splits) + 1)
    n_clip = n_g0and = 0
    ns_odd = []
    s = t0
    while s < T:
        A = (row << 1) & row
        t = (s - t0) // 2
        n = odd_clock(t, U, Q)
        m = T - s - 1
        lo_raw = 2 * s - T + 2
        lo = max(lo_raw, 0)
        if lo_raw < 0:
            n_clip += 1
        if (A >> T) & 1:
            xor_andT ^= 1
        contrib = 0
        if s % 2:
            ns_odd.append(n)
            for p in range(lo, T + 1):
                rho = T - p
                g = G(m, rho)
                on = (A >> p) & 1
                if rho % 2:
                    if g:
                        return {"ok": False, "oddrho": True, "k": k, "q": q, "s": s, "p": p}
                    continue
                gj = G(n, rho // 2)
                if g != gj:
                    return {
                        "ok": False,
                        "gx": True,
                        "k": k,
                        "q": q,
                        "s": s,
                        "p": p,
                        "g": g,
                        "want": gj,
                    }
                if on and gj:
                    xor_odd ^= 1
                    contrib ^= 1
                if on and not gj:
                    n_g0and += 1
        else:
            for p in range(lo, T + 1):
                rho = T - p
                g = G(m, rho)
                on = (A >> p) & 1
                if rho % 2 == 0:
                    j = rho // 2
                    want = G(n, j) ^ G(n, j - 1)
                else:
                    want = G(n, (rho - 1) // 2)
                if g != want:
                    return {
                        "ok": False,
                        "gy": True,
                        "k": k,
                        "q": q,
                        "s": s,
                        "p": p,
                        "g": g,
                        "want": want,
                    }
                if on and g:
                    xor_even ^= 1
                    contrib ^= 1
        idx = 0
        while idx < len(splits) and s >= splits[idx]:
            idx += 1
        parts[idx] ^= contrib
        row = rule30_step(row)
        s += 1
    want_clip = U * (q // 2 - 2) - 1
    tot = xor_odd ^ xor_even
    return {
        "ok": n_clip == want_clip and sorted(ns_odd) == list(range(U * Q)),
        "tot": tot,
        "xor_odd": xor_odd,
        "xor_even": xor_even,
        "xor_andT": xor_andT,
        "parts": parts,
        "n_clip": n_clip,
        "n_g0and": n_g0and,
        "n_min": min(ns_odd) if ns_odd else None,
        "n_max": max(ns_odd) if ns_odd else None,
    }


def j10_j18_index() -> dict:
    """J10 Q=4 and J18 Q=8 from t0=2U. Packed k<=6."""
    n_ok = 0
    n_g0 = 0
    rows = {}
    fr = json.loads(FR_JSON.read_text())
    fh = json.loads(FH_JSON.read_text())
    for k in range(0, 7):
        w10 = _walk_jq(k, 10, (6,))
        if not w10.get("ok"):
            return w10
        mid = _walk_in(k, 10, 6, 2)
        if not mid.get("ok"):
            return mid
        mid_tot = mid["xor_odd"] ^ mid["xor_even"]
        if w10["parts"][1] != mid_tot:
            return {
                "ok": False,
                "mid": True,
                "k": k,
                "part": w10["parts"][1],
                "mid10": mid_tot,
            }
        if str(k) in fr["split"]["rows"]:
            r = fr["split"]["rows"][str(k)]
            if w10["tot"] != r["J10"] or w10["parts"][0] != r["Jpre10"]:
                return {
                    "ok": False,
                    "J10": True,
                    "k": k,
                    "tot": w10["tot"],
                    "fr": r["J10"],
                }
        w18 = _walk_jq(k, 18, (6, 10))
        if not w18.get("ok"):
            return w18
        tail = _walk_in(k, 18, 10, 4)
        if not tail.get("ok"):
            return tail
        tail_tot = tail["xor_odd"] ^ tail["xor_even"]
        if w18["parts"][2] != tail_tot:
            return {
                "ok": False,
                "tail": True,
                "k": k,
                "part": w18["parts"][2],
                "Jtail": tail_tot,
            }
        if str(k) in fr["split"]["rows"]:
            r = fr["split"]["rows"][str(k)]
            want_mid18 = r["Jmid10"] ^ r["dR"]
            if w18["parts"][1] != want_mid18 or w18["parts"][0] != r["J6"]:
                return {
                    "ok": False,
                    "J18split": True,
                    "k": k,
                    "parts": w18["parts"],
                }
        if str(k) in fh["split"]["rows"]:
            if w18["tot"] != fh["split"]["rows"][str(k)]["J18"]:
                return {
                    "ok": False,
                    "J18": True,
                    "k": k,
                    "tot": w18["tot"],
                    "fh": fh["split"]["rows"][str(k)]["J18"],
                }
        n_ok += 1
        n_g0 += w10["n_g0and"] + w18["n_g0and"]
        rows[str(k)] = {
            "J10": w10["tot"],
            "xor_odd10": w10["xor_odd"],
            "xor_even10": w10["xor_even"],
            "Jpre10": w10["parts"][0],
            "mid10": mid_tot,
            "J18": w18["tot"],
            "xor_odd18": w18["xor_odd"],
            "xor_even18": w18["xor_even"],
            "parts18": w18["parts"],
            "Jtail": tail_tot,
            "n_clip10": w10["n_clip"],
            "n_clip18": w18["n_clip"],
            "xor_andT10": w10["xor_andT"],
            "xor_andT18": w18["xor_andT"],
        }
    return {"ok": n_ok == 7, "n_ok": n_ok, "n_g0and": n_g0, "rows": rows}


def clip_algebra() -> dict:
    """lo_raw<0 iff s<qU/2-1; clip length U(q/2-2)-1. k<=12, q=10,18."""
    n_ok = 0
    for q in (10, 18):
        for k in range(0, 13):
            U = 1 << k
            T, t0 = q * U, 2 * U
            n_clip = 0
            first = T // 2 - 1
            for s in range(t0, T):
                m = T - s - 1
                lo_raw = 2 * s - T + 2
                want_clip = s < first
                if (lo_raw < 0) != want_clip:
                    return {"ok": False, "k": k, "q": q, "s": s, "lo_raw": lo_raw}
                if lo_raw < 0:
                    n_clip += 1
                else:
                    if T - lo_raw != 2 * m:
                        return {"ok": False, "width": True, "k": k, "q": q, "s": s}
            want = U * (q // 2 - 2) - 1
            if n_clip != want:
                return {"ok": False, "n_clip": n_clip, "want": want, "k": k, "q": q}
            if t0 <= first < T:
                m = T - first - 1
                if 2 * first - T + 2 != 0 or T != 2 * m:
                    return {"ok": False, "first": True, "k": k, "q": q}
            n_ok += 1
    return {"ok": n_ok == 26, "n_ok": n_ok}


def n_scan() -> dict:
    """Odd s enumerates n in [0, UQ) for q=10,18. k<=12."""
    n_ok = 0
    for q in (10, 18):
        Q = covering_Q(q)
        for k in range(0, 13):
            U = 1 << k
            T, t0 = q * U, 2 * U
            UQ = U * Q
            if T - t0 != 2 * UQ:
                return {"ok": False, "len": True, "k": k, "q": q}
            seen = []
            for t in range(UQ):
                seen.append(odd_clock(t, U, Q))
                s_odd = t0 + 2 * t + 1
                s_even = t0 + 2 * t
                if not (t0 <= s_even < T) or not (t0 <= s_odd < T):
                    return {"ok": False, "s": True, "k": k, "q": q, "t": t}
            if sorted(seen) != list(range(UQ)):
                return {"ok": False, "k": k, "q": q}
            n_ok += 1
    return {"ok": n_ok == 26, "n_ok": n_ok}


def killed_mid10_eq_J10() -> dict:
    """[6U,10U) in-support XOR is not J10: k=2, 0 vs 1."""
    mid = _walk_in(2, 10, 6, 2)
    fr = json.loads(FR_JSON.read_text())
    j10 = fr["split"]["rows"]["2"]["J10"]
    tot = mid["xor_odd"] ^ mid["xor_even"]
    ok = tot == 0 and j10 == 1
    return {"ok": ok, "k": 2, "mid10": tot, "J10": j10}


def killed_tail_eq_J18() -> dict:
    """[10U,18U) in-support XOR is not J18: k=2, 1 vs 0."""
    tail = _walk_in(2, 18, 10, 4)
    fh = json.loads(FH_JSON.read_text())
    j18 = fh["split"]["rows"]["2"]["J18"]
    tot = tail["xor_odd"] ^ tail["xor_even"]
    ok = tot == 1 and j18 == 0
    return {"ok": ok, "k": 2, "Jtail": tot, "J18": j18}


def killed_unclipped() -> dict:
    """J10 window is not unclipped full Green: k=2, s=t0, 41 != 63."""
    k = 2
    U = 1 << k
    T, t0 = 10 * U, 2 * U
    s = t0
    m = T - s - 1
    lo_raw = 2 * s - T + 2
    w = T + 1
    full = 2 * m + 1
    ok = lo_raw < 0 and w == 41 and full == 63 and w != full
    return {"ok": ok, "k": k, "s": s, "width": w, "full": full, "lo_raw": lo_raw}


def prefixes() -> dict:
    hf = json.loads(HF_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    fh = json.loads(FH_JSON.read_text())
    ok = (
        hf["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and fh["checks"]["all_ok"]
        and hf["verdict"]["J6_eq_in_support_j_index_Q2"] == "LEMMA"
        and fr["verdict"]["Jpost_eq_Jmid10_xor_DeltaR_xor_Jtail"] == "LEMMA"
        and fh["verdict"]["J18_eq_J6_xor_Jpost"] == "LEMMA"
        and hf["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, jx: dict, cl: dict, ns: dict, km: dict, kt: dict, ku: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        jx["ok"]
        and cl["ok"]
        and ns["ok"]
        and km["ok"]
        and kt["ok"]
        and ku["ok"]
        and pref["ok"]
    )
    assert J6_WINDOW == ("j6", 6, 2, 2)
    assert J10_WINDOW == ("j10", 10, 2, 4)
    assert J18_WINDOW == ("j18", 18, 2, 8)
    assert covering_Q(6) == 2 and covering_Q(10) == 4 and covering_Q(18) == 8
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    jx = j10_j18_index()
    cl = clip_algebra()
    ns = n_scan()
    km = killed_mid10_eq_J10()
    kt = killed_tail_eq_J18()
    ku = killed_unclipped()
    pref = prefixes()
    checks = self_checks(c20, jx, cl, ns, km, kt, ku, pref)
    dump = {
        "cycle": "HG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "j10_j18_index": {k: jx[k] for k in jx if k != "ok"},
        "clip_algebra": {k: cl[k] for k in cl if k != "ok"},
        "n_scan": {k: ns[k] for k in ns if k != "ok"},
        "killed_mid10_eq_J10": {k: km[k] for k in km if k != "ok"},
        "killed_tail_eq_J18": {k: kt[k] for k in kt if k != "ok"},
        "killed_unclipped": {k: ku[k] for k in ku if k != "ok"},
        "lemmas": {
            "J10_eq_in_support_j_index_Q4": True,
            "J18_eq_in_support_j_index_Q8": True,
            "J10_left_clip_s_lt_5U_minus_1": True,
            "J18_left_clip_s_lt_9U_minus_1": True,
            "mid10_XOR_eq_J10": False,
            "tail_XOR_eq_J18": False,
            "J10_window_unclipped_full_Green": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "J10_eq_in_support_j_index_Q4": "LEMMA",
            "J18_eq_in_support_j_index_Q8": "LEMMA",
            "J10_left_clip_s_lt_5U_minus_1": "LEMMA",
            "J18_left_clip_s_lt_9U_minus_1": "LEMMA",
            "mid10_XOR_eq_J10": "KILLED",
            "tail_XOR_eq_J18": "KILLED",
            "J10_window_unclipped_full_Green": "KILLED",
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
        "j10_j18_index n_ok",
        dump["j10_j18_index"]["n_ok"],
        "n_g0and",
        dump["j10_j18_index"]["n_g0and"],
    )
    print("clip_algebra n_ok", dump["clip_algebra"]["n_ok"])
    print("n_scan n_ok", dump["n_scan"]["n_ok"])
    print("killed_mid10_eq_J10", dump["killed_mid10_eq_J10"])
    print("killed_tail_eq_J18", dump["killed_tail_eq_J18"])
    print("killed_unclipped", dump["killed_unclipped"])


if __name__ == "__main__":
    main()
