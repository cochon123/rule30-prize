#!/usr/bin/env python3
"""Cycle QH: covering clipped G=1 xor vanishes for k>=1; Green leftover is 1 iff k>=6.

Unclipped Green row xor of G=1 is 1 (palindrome plus G(n,n)=1). Clip
j<=5U. Even covering n=2m maps onto the parent clip window, so even
contrib is A(k-1). Odd n=2m+1 has clipped xor equal to parent clip
xor of m, by Green doubling: the even/odd 4-tuple telescopes to
xor_{l<=5U'} G(m,l), including the 2m=5U' off-by-one. Hence both
parities equal A(k-1) and A(k)=0 for k>=1. Green forced xor is 1
iff k=0 or k>=3 (Cycle PC), so Green rest off {4,6,14} is 1 iff
k>=3. Green UNIQUE_REST tot is 1 iff k in {3,4,5} (Cycle QG), so
Green leftover xor is 1 iff k>=6. Not packed leftover tot (rest is
not 1 for every k>=6). Not rest=S xor T. Not E_k=0 for all k. Do
not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qh.py --certify
Dump: research/cycle_qh.json
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
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import want_green_forced
from cycle_qg import want_unique_gxor_tot

OUT = Path(__file__).resolve().with_suffix(".json")
QG_JSON = Path(__file__).resolve().parent / "cycle_qg.json"
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64


def want_clip_g1(k: int) -> int:
    """Covering clipped G=1 xor A(k): 1 iff k==0."""
    return int(k == 0)


def want_green_rest(k: int) -> int:
    """Covering Green G=1 xor off {4,6,14}, all k."""
    return int(k >= 3)


def want_green_lo(k: int) -> int:
    """Covering Green leftover xor (off unique and forced), all k."""
    return int(k >= 6)


def clip_bit(n: int, k: int) -> int:
    """Xor of G(n,j) for 0<=j<=min(2n, 5*2^k). Unclipped row xor is 1."""
    clip = 5 << k
    if 2 * n <= clip:
        return 1
    rem = 0
    for j in range(clip + 1, 2 * n + 1):
        rem ^= G(n, j)
    return 1 ^ rem


def A_of(k: int) -> dict:
    """Walk covering n=0..4U-1 clipped G=1 xor, split even/odd n."""
    n_hi = 4 << k
    acc = even = odd = 0
    for n in range(0, n_hi):
        bit = clip_bit(n, k)
        acc ^= bit
        if n % 2 == 0:
            even ^= bit
        else:
            odd ^= bit
    return {"A": acc, "even": even, "odd": odd, "n_hi": n_hi}


def unclipped_row() -> dict:
    """n<N_PAL: xor of G(n,0..2n) is 1."""
    n_ok = 0
    for n in range(0, N_PAL):
        acc = 0
        for j in range(0, 2 * n + 1):
            acc ^= G(n, j)
        if acc != 1:
            return {"ok": False, "n": n, "got": acc}
        n_ok += 1
    return {"ok": n_ok == N_PAL, "n_ok": n_ok, "n_hi": N_PAL}


def clip_recurrence() -> dict:
    """k<=K_CHK: even and odd contrib equal A(k-1); A(k)=want_clip_g1."""
    n_ok = 0
    rows = {}
    prev = None
    for k in range(0, K_CHK + 1):
        w = A_of(k)
        if w["A"] != want_clip_g1(k):
            return {"ok": False, "A": True, "k": k, "got": w["A"]}
        if k >= 1:
            if prev is None or w["even"] != prev or w["odd"] != prev:
                return {
                    "ok": False,
                    "rec": True,
                    "k": k,
                    "even": w["even"],
                    "odd": w["odd"],
                    "prev": prev,
                }
            # odd n=2m+1 clip equals parent clip of m
            m_hi = 4 << (k - 1)
            for m in range(0, m_hi):
                if clip_bit(2 * m + 1, k) != clip_bit(m, k - 1):
                    return {"ok": False, "odd_n": True, "k": k, "m": m}
                n_ok += 1
        rest = w["A"] ^ want_green_forced(k)
        lo = rest ^ want_unique_gxor_tot(k)
        if rest != want_green_rest(k) or lo != want_green_lo(k):
            return {"ok": False, "split": True, "k": k, "rest": rest, "lo": lo}
        rows[str(k)] = {
            "A": w["A"],
            "even": w["even"],
            "odd": w["odd"],
            "forced": want_green_forced(k),
            "unique": want_unique_gxor_tot(k),
            "rest": rest,
            "lo": lo,
        }
        prev = w["A"]
    ok = (
        rows["0"]["A"] == 1
        and rows["1"]["A"] == 0
        and rows["3"]["rest"] == 1
        and rows["5"]["lo"] == 0
        and rows["6"]["lo"] == 1
        and rows["8"]["A"] == 0
        and rows["8"]["lo"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: A, rest, leftover closed forms vs forced and unique tot."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        a = want_clip_g1(k)
        rest = a ^ want_green_forced(k)
        lo = rest ^ want_unique_gxor_tot(k)
        if (
            rest != want_green_rest(k)
            or lo != want_green_lo(k)
            or (k >= 1 and a != 0)
            or (k == 0 and a != 1)
        ):
            return {"ok": False, "k": k, "A": a, "rest": rest, "lo": lo}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_green_lo(6) == 1
        and want_green_lo(5) == 0
        and want_green_rest(2) == 0
        and want_green_rest(3) == 1
        and want_rest_e0(7) == 0
        and want_green_lo(7) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_lo_eq_st() -> dict:
    """Green leftover tot equals S xor T / packed rest: k=7 is 1 vs 0."""
    ok = (
        want_green_lo(7) == 1
        and want_rest_e0(7) == 0
        and want_rest10(7, 10) == 0
    )
    return {"ok": ok, "k": 7, "lo": 1, "ST": 0, "rest10": 0}


def prefixes() -> dict:
    qg = json.loads(QG_JSON.read_text())
    pc = json.loads(PC_JSON.read_text())
    ok = (
        qg["checks"]["all_ok"]
        and pc["checks"]["all_ok"]
        and qg["verdict"]["unique_gxor_tot_iff_k_in_3_4_5"] == "LEMMA"
        and pc["verdict"]["prize"] == "unsolved"
        and qg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qg["verdict"]["prize"] == "unsolved"
        and want_unique_gxor_tot(5) == 1
        and want_unique_gxor_tot(6) == 0
        and want_green_forced(0) == 1
        and want_green_forced(3) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, row, rec, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and row["ok"] and rec["ok"]
    assert tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    row = unclipped_row()
    rec = clip_recurrence()
    tot = tot_form()
    kl = killed_lo_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, row, rec, tot, kl, sc, pref)
    dump = {
        "cycle": "QH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "unclipped_row": {k: row[k] for k in row if k != "ok"},
        "clip_recurrence": {k: rec[k] for k in rec if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unclipped_g1_xor_1": True,
            "clip_g1_0_k_ge_1": True,
            "green_rest_iff_k_ge_3": True,
            "green_lo_iff_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "lo_eq_ST": False,
            "prize": False,
        },
        "verdict": {
            "unclipped_g1_xor_1": "LEMMA",
            "clip_g1_0_k_ge_1": "LEMMA",
            "green_rest_iff_k_ge_3": "LEMMA",
            "green_lo_iff_k_ge_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "lo_eq_ST": "KILLED",
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
        "clip_recurrence n_ok",
        dump["clip_recurrence"]["n_ok"],
        "k_hi",
        dump["clip_recurrence"]["k_hi"],
        "A8",
        dump["clip_recurrence"]["rows"]["8"]["A"],
        "lo8",
        dump["clip_recurrence"]["rows"]["8"]["lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
