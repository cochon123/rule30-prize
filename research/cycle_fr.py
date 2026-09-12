#!/usr/bin/env python3
"""Cycle FR: band lower edge is G(m,2m)=1; J_post = J_mid10 XOR Delta_R XOR J_tail.

On the unified T=2U+W right band, r_lo=2(s-t0+1) is exactly the Green
corner: W-r_lo=2m, so G(m,W-r_lo)=G(m,2m)=1. After the clip s=U+W the
upper edge is r=W and G(m,0)=1. The AND at the lower edge is not always
live. Splitting [6U,18U) and using Cycle FJ's Delta=Delta_R gives
J_post = J_[6U,10U)->10U XOR Delta_R XOR J_[10U,18U)->18U. Kills:
lo-edge AND always live; J_post=Delta_R; J_mid10=0. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fr.py --certify
Dump: research/cycle_fr.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FK_JSON = Path(__file__).resolve().parent / "cycle_fk.json"
FH_JSON = Path(__file__).resolve().parent / "cycle_fh.json"


def lo_is_corner() -> dict:
    """W - r_lo = 2m and G(m,2m)=1 on the unified band."""
    n_ok = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            for s in (t0, t0 + max(U, 1), U + W, T - 1):
                if not (t0 <= s < T):
                    continue
                m = T - s - 1
                r_lo = 2 * (s - t0 + 1)
                if W - r_lo != 2 * m or G(m, W - r_lo) != 1:
                    return {"ok": False, "k": k, "W": W, "s": s, "m": m}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def hi_after_clip() -> dict:
    """After s=U+W, r_hi=W and G(m,0)=1."""
    n_ok = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            clip = U + W
            for s in (clip, clip + max(U, 1), T - 1):
                if not (clip <= s < T):
                    continue
                m = T - s - 1
                r_hi = min(2 * s - T, W)
                if r_hi != W or G(m, 0) != 1 or G(m, W - r_hi) != 1:
                    return {"ok": False, "k": k, "W": W, "s": s}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def packed_split(kmax: int = 5) -> dict:
    """J_post = J_mid10 XOR Delta_R XOR J_tail; J10 = J_pre10 XOR J_mid10."""
    rows = {}
    n_ok = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        T6, T10, T18 = 6 * U, 10 * U, 18 * U
        row = 1
        J6 = Jpre10 = Jmid10 = Jpost = Jtail = dR = 0
        for s in range(T18):
            if s >= 2 * U:
                A = (row << 1) & row
                tmp, p = A, 0
                while tmp:
                    if tmp & 1:
                        if s < T6:
                            J6 ^= G(T6 - s - 1, T6 - p)
                            Jpre10 ^= G(T10 - s - 1, T10 - p)
                        elif s < T10:
                            Jmid10 ^= G(T10 - s - 1, T10 - p)
                            Jpost ^= G(T18 - s - 1, T18 - p)
                            if p > T10:
                                dR ^= G(T18 - s - 1, T18 - p)
                        else:
                            Jtail ^= G(T18 - s - 1, T18 - p)
                            Jpost ^= G(T18 - s - 1, T18 - p)
                    tmp >>= 1
                    p += 1
            row = rule30_step(row)
        # Jpost above includes [6U,18U) only (the s<T6 branch does not add).
        combo = Jmid10 ^ dR ^ Jtail
        if combo != Jpost:
            return {"ok": False, "k": k, "Jpost": Jpost, "combo": combo}
        rows[str(k)] = {
            "J6": J6,
            "Jpre10": Jpre10,
            "Jmid10": Jmid10,
            "dR": dR,
            "Jtail": Jtail,
            "Jpost": Jpost,
            "J10": Jpre10 ^ Jmid10,
        }
        n_ok += 1
    return {"ok": n_ok == kmax - 1, "n_ok": n_ok, "rows": rows}


def killed_lo_and_live() -> dict:
    """Lower-edge AND is not always live: k=2, W=4U, 7 of 8 times dead."""
    k = 2
    U = 1 << k
    W, T = 4 * U, 6 * U
    t0 = T - W // 2
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live = dead = 0
    for s in range(t0, T):
        A = (row << 1) & row
        r_lo = 2 * (s - t0 + 1)
        p_lo = T + r_lo
        if (A >> p_lo) & 1:
            live += 1
        else:
            dead += 1
        row = rule30_step(row)
    ok = dead > 0 and live > 0
    return {"ok": ok, "k": k, "live": live, "dead": dead}


def prefixes() -> dict:
    fq = json.loads(FQ_JSON.read_text())
    fj = json.loads(FJ_JSON.read_text())
    fk = json.loads(FK_JSON.read_text())
    fh = json.loads(FH_JSON.read_text())
    ok = (
        fq["checks"]["all_ok"]
        and fj["checks"]["all_ok"]
        and fk["checks"]["all_ok"]
        and fh["checks"]["all_ok"]
        and fq["verdict"]["unified_T_eq_2U_plus_W_band"] == "LEMMA"
        and fj["verdict"]["Delta_eq_Delta_R"] == "LEMMA"
        and fk["verdict"]["G_n0_eq_G_n2n_eq_1"] == "LEMMA"
        and fh["verdict"]["J18_eq_J6_xor_Jpost"] == "LEMMA"
        and fq["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, lo: dict, hi: dict, split: dict, klo: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert lo["ok"] and hi["ok"] and split["ok"] and klo["ok"] and pref["ok"]
    rows = split["rows"]
    assert rows["5"]["Jpost"] == 1 and rows["5"]["dR"] == 0
    assert rows["4"]["Jmid10"] == 1
    assert rows["2"]["Jpost"] != rows["2"]["dR"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    lo = lo_is_corner()
    hi = hi_after_clip()
    split = packed_split()
    klo = killed_lo_and_live()
    pref = prefixes()
    checks = self_checks(c20, lo, hi, split, klo, pref)
    dump = {
        "cycle": "FR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lo_corner": {k: lo[k] for k in lo if k != "ok"},
        "hi_clip": {k: hi[k] for k in hi if k != "ok"},
        "split": {k: split[k] for k in split if k != "ok"},
        "killed_lo_and": {k: klo[k] for k in klo if k != "ok"},
        "lemmas": {
            "band_lo_edge_eq_G_m_2m": True,
            "band_hi_after_clip_eq_G_m_0": True,
            "Jpost_eq_Jmid10_xor_DeltaR_xor_Jtail": True,
            "lo_edge_AND_always_live": False,
            "Jpost_eq_DeltaR": False,
            "Jmid10_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "band_lo_edge_eq_G_m_2m": "LEMMA",
            "band_hi_after_clip_eq_G_m_0": "LEMMA",
            "Jpost_eq_Jmid10_xor_DeltaR_xor_Jtail": "LEMMA",
            "lo_edge_AND_always_live": "KILLED",
            "Jpost_eq_DeltaR": "KILLED",
            "Jmid10_eq_0": "KILLED",
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
    print("lo_corner", dump["lo_corner"])
    print("split", dump["split"])


if __name__ == "__main__":
    main()
