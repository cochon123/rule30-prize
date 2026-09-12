#!/usr/bin/env python3
"""Cycle HF: J6 is the in-support j-index on [2U,6U) with Q=2.

The covering j6slice [4U,6U) is only n in [0,U). Full J6 uses
T=6U, t0=2U, Q=2: GX/GY with n=2U-t-1, left-clipped for s<3U-1,
and tot equals FR J6. The [4U,6U) XOR is not J6 (k=3: 1 vs 0).
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_hf.py --certify
Dump: research/cycle_hf.json
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
from cycle_hc import WINDOWS, _walk_in
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HE_JSON = Path(__file__).resolve().parent / "cycle_he.json"
HC_JSON = Path(__file__).resolve().parent / "cycle_hc.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"

# Full J6 remainder [2U,6U) -> 6U. Not a unified T=2U+W band.
J6_WINDOW = ("j6", 6, 2, 2)


def _walk_j6(k: int) -> dict:
    """GX/GY on [2U,6U)->6U; split at 4U; left clip; AND at p=T."""
    U = 1 << k
    T, t0, Q = 6 * U, 2 * U, 2
    mid = 4 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    xor_odd = xor_even = xor_pre = xor_andT = 0
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
        andT = (A >> T) & 1
        if andT:
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
                        return {"ok": False, "oddrho": True, "k": k, "s": s, "p": p}
                    continue
                j = rho // 2
                gj = G(n, j)
                if g != gj:
                    return {
                        "ok": False,
                        "gx": True,
                        "k": k,
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
                    j = (rho - 1) // 2
                    want = G(n, j)
                if g != want:
                    return {
                        "ok": False,
                        "gy": True,
                        "k": k,
                        "s": s,
                        "p": p,
                        "g": g,
                        "want": want,
                    }
                if on and g:
                    xor_even ^= 1
                    contrib ^= 1
        if s < mid:
            xor_pre ^= contrib
        row = rule30_step(row)
        s += 1
    tot = xor_odd ^ xor_even
    return {
        "ok": n_clip == U - 1 and sorted(ns_odd) == list(range(2 * U)),
        "xor_odd": xor_odd,
        "xor_even": xor_even,
        "tot": tot,
        "xor_pre": xor_pre,
        "xor_andT": xor_andT,
        "n_clip": n_clip,
        "n_g0and": n_g0and,
        "n_min": min(ns_odd) if ns_odd else None,
        "n_max": max(ns_odd) if ns_odd else None,
    }


def j6_j_index() -> dict:
    """GX/GY on full J6; tot = FR J6; pre XOR j6slice = tot. k<=6."""
    n_ok = 0
    n_g0 = 0
    rows = {}
    fr = json.loads(FR_JSON.read_text())
    for k in range(0, 7):
        w = _walk_j6(k)
        if not w.get("ok"):
            return w
        sl = _walk_in(k, 6, 4, 1)
        if not sl.get("ok"):
            return sl
        slice_tot = sl["xor_odd"] ^ sl["xor_even"]
        if w["xor_pre"] ^ slice_tot != w["tot"]:
            return {
                "ok": False,
                "split": True,
                "k": k,
                "pre": w["xor_pre"],
                "slice": slice_tot,
                "tot": w["tot"],
            }
        if str(k) in fr["split"]["rows"]:
            j6 = fr["split"]["rows"][str(k)]["J6"]
            if w["tot"] != j6:
                return {"ok": False, "J6": True, "k": k, "tot": w["tot"], "fr": j6}
        n_ok += 1
        n_g0 += w["n_g0and"]
        rows[str(k)] = {
            "tot": w["tot"],
            "xor_odd": w["xor_odd"],
            "xor_even": w["xor_even"],
            "xor_pre": w["xor_pre"],
            "j6slice": slice_tot,
            "xor_andT": w["xor_andT"],
            "n_clip": w["n_clip"],
            "n_g0and": w["n_g0and"],
        }
    return {"ok": n_ok == 7, "n_ok": n_ok, "n_g0and": n_g0, "rows": rows}


def clip_algebra() -> dict:
    """lo_raw<0 iff s<3U-1; at s=3U-1, lo=0 and T-lo=2m. k<=12."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        T, t0 = 6 * U, 2 * U
        n_clip = 0
        for s in range(t0, T):
            m = T - s - 1
            lo_raw = 2 * s - T + 2
            want_clip = s < 3 * U - 1
            if (lo_raw < 0) != want_clip:
                return {"ok": False, "k": k, "s": s, "lo_raw": lo_raw}
            if lo_raw < 0:
                n_clip += 1
            else:
                lo = lo_raw
                if T - lo != 2 * m:
                    return {"ok": False, "width": True, "k": k, "s": s}
        if n_clip != U - 1:
            return {"ok": False, "n_clip": n_clip, "k": k}
        s0 = 3 * U - 1
        if t0 <= s0 < T:
            m = T - s0 - 1
            if 2 * s0 - T + 2 != 0 or T != 2 * m:
                return {"ok": False, "first": True, "k": k, "s": s0}
        n_ok += 1
    return {"ok": n_ok == 13, "n_ok": n_ok}


def n_scan_j6() -> dict:
    """Odd s enumerates n in [0, 2U); even s shares n. k<=12."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        T, t0, Q = 6 * U, 2 * U, 2
        UQ = U * Q
        if T - t0 != 2 * UQ:
            return {"ok": False, "len": True, "k": k}
        seen = []
        for t in range(UQ):
            n = odd_clock(t, U, Q)
            seen.append(n)
            s_odd = t0 + 2 * t + 1
            s_even = t0 + 2 * t
            if not (t0 <= s_even < T) or not (t0 <= s_odd < T):
                return {"ok": False, "s": True, "k": k, "t": t}
        if sorted(seen) != list(range(UQ)):
            return {"ok": False, "k": k, "seen": seen[:4]}
        n_ok += 1
    return {"ok": n_ok == 13, "n_ok": n_ok}


def killed_j6slice_eq_J6() -> dict:
    """[4U,6U) in-support XOR is not J6: k=3, 1 vs 0."""
    sl = _walk_in(3, 6, 4, 1)
    fr = json.loads(FR_JSON.read_text())
    j6 = fr["split"]["rows"]["3"]["J6"]
    tot = sl["xor_odd"] ^ sl["xor_even"]
    ok = tot == 1 and j6 == 0
    return {"ok": ok, "k": 3, "j6slice": tot, "J6": j6}


def killed_full_width() -> dict:
    """J6 window is not unclipped full Green: k=2, s=t0, 25 != 31."""
    k = 2
    U = 1 << k
    T, t0 = 6 * U, 2 * U
    s = t0
    m = T - s - 1
    lo_raw = 2 * s - T + 2
    w = T - 0 + 1
    full = 2 * m + 1
    ok = lo_raw < 0 and w == 25 and full == 31 and w != full
    return {"ok": ok, "k": k, "s": s, "width": w, "full": full, "lo_raw": lo_raw}


def killed_andT_eq_J6() -> dict:
    """AND at p=T XOR is not J6: k=3, 1 vs 0."""
    w = _walk_j6(3)
    fr = json.loads(FR_JSON.read_text())
    j6 = fr["split"]["rows"]["3"]["J6"]
    ok = w["xor_andT"] == 1 and j6 == 0 and w["tot"] == 0
    return {"ok": ok, "k": 3, "xor_andT": w["xor_andT"], "J6": j6, "tot": w["tot"]}


def prefixes() -> dict:
    he = json.loads(HE_JSON.read_text())
    hc = json.loads(HC_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        he["checks"]["all_ok"]
        and hc["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and he["verdict"]["in_support_eq_full_Green_row"] == "LEMMA"
        and hc["verdict"]["in_support_odd_s_XOR_eq_AND_on_G_n_j_eq_1"] == "LEMMA"
        and fr["verdict"]["Jpost_eq_Jmid10_xor_DeltaR_xor_Jtail"] == "LEMMA"
        and he["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, jx: dict, cl: dict, ns: dict, kj: dict, kw: dict, ka: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        jx["ok"]
        and cl["ok"]
        and ns["ok"]
        and kj["ok"]
        and kw["ok"]
        and ka["ok"]
        and pref["ok"]
    )
    # WINDOWS j6slice is the n<U half, not a unified synonym of J6.
    assert WINDOWS[2] == ("j6slice", 6, 4, 1)
    assert J6_WINDOW == ("j6", 6, 2, 2)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    jx = j6_j_index()
    cl = clip_algebra()
    ns = n_scan_j6()
    kj = killed_j6slice_eq_J6()
    kw = killed_full_width()
    ka = killed_andT_eq_J6()
    pref = prefixes()
    checks = self_checks(c20, jx, cl, ns, kj, kw, ka, pref)
    dump = {
        "cycle": "HF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "j6_j_index": {k: jx[k] for k in jx if k != "ok"},
        "clip_algebra": {k: cl[k] for k in cl if k != "ok"},
        "n_scan_j6": {k: ns[k] for k in ns if k != "ok"},
        "killed_j6slice_eq_J6": {k: kj[k] for k in kj if k != "ok"},
        "killed_full_width": {k: kw[k] for k in kw if k != "ok"},
        "killed_andT_eq_J6": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "J6_eq_in_support_j_index_Q2": True,
            "J6_left_clip_s_lt_3U_minus_1": True,
            "odd_s_enumerates_n_in_0_2U": True,
            "pre_2U_4U_xor_j6slice_eq_J6": True,
            "j6slice_XOR_eq_J6": False,
            "J6_window_unclipped_full_Green": False,
            "AND_at_T_XOR_eq_J6": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "J6_eq_in_support_j_index_Q2": "LEMMA",
            "J6_left_clip_s_lt_3U_minus_1": "LEMMA",
            "odd_s_enumerates_n_in_0_2U": "LEMMA",
            "pre_2U_4U_xor_j6slice_eq_J6": "LEMMA",
            "j6slice_XOR_eq_J6": "KILLED",
            "J6_window_unclipped_full_Green": "KILLED",
            "AND_at_T_XOR_eq_J6": "KILLED",
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
    print("j6_j_index n_ok", dump["j6_j_index"]["n_ok"], "n_g0and", dump["j6_j_index"]["n_g0and"])
    print("clip_algebra n_ok", dump["clip_algebra"]["n_ok"])
    print("n_scan_j6 n_ok", dump["n_scan_j6"]["n_ok"])
    print("killed_j6slice_eq_J6", dump["killed_j6slice_eq_J6"])
    print("killed_full_width", dump["killed_full_width"])
    print("killed_andT_eq_J6", dump["killed_andT_eq_J6"])


if __name__ == "__main__":
    main()
