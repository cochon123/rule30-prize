#!/usr/bin/env python3
"""Cycle PA: covering r123 xor is 1 iff k even; covering S is Green 0-1.

On the covering window, r123(s,k) equals the pal-right suffix of G(s)
from j=M+1 through 2s, xor G(s,M-1) unless (M-s)%3==2, with
M=5*2^{k-4}. Pal-suffix doubles, so the odd and even folds differ
from the parent r123 by the unique Green columns G(t,3*2^{k-5}-1)
and G(t,5*2^{k-5}-1), which fire at the same unique t. Covering
odd xor even therefore cancels the parent and equals 1 xor (k%2)
for k>=6. With Cycle OZ's r0 xor = ep(k-2), covering ep xor is
1 iff k>=6 and k%4==2, all k. Covering rem and covering S then
close as Green 0-1 in k: S=1 iff k>=6 and k%8 in (0, 6). Not
E_k=0 for all k (packed R=S xor T remains). Not the pal-suffix
formula off the covering window. Not even-s r123 vanishing
pointwise. Do not catalogue further S/T subregions unless the
experiment answers why E_k=0. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_pa.py --certify
Dump: research/cycle_pa.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_or import want_unclip_cover
from cycle_ov import covering_rem_parts
from cycle_ow import want_ep_cover, want_n3_cover, want_rem_cover
from cycle_oz import ep_cover_rem, want_r123_ep

OUT = Path(__file__).resolve().with_suffix(".json")
OZ_JSON = Path(__file__).resolve().parent / "cycle_oz.json"
OY_JSON = Path(__file__).resolve().parent / "cycle_oy.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
A_HI = 8
K_FORM = 8
K_FOLD = 10
K_COVER = 10
K_REM = 8


def r123(s: int, k: int) -> int:
    """Xor of covering ep rem on 4s+1, 4s+2, 4s+3 at scale k."""
    return (
        ep_cover_rem(4 * s + 1, k)
        ^ ep_cover_rem(4 * s + 2, k)
        ^ ep_cover_rem(4 * s + 3, k)
    )


def pal_suffix(s: int, start_j: int) -> int:
    """Xor of G(s,j) for start_j <= j <= 2s."""
    acc = 0
    for j in range(max(start_j, 0), 2 * s + 1):
        acc ^= G(s, j)
    return acc


def r123_suffix(s: int, k: int) -> int:
    """Pal-right suffix from M+1, plus G(s,M-1) unless (M-s)%3==2."""
    M = 5 << (k - 4)
    extra = G(s, M - 1) if (M - s) % 3 != 2 else 0
    return pal_suffix(s, M + 1) ^ extra


def tstar(k: int) -> int:
    """Unique column index 3*2^{k-5}-1."""
    return (3 << (k - 5)) - 1


def want_cover_s(k: int) -> int:
    """Covering pal-right S xor, all k: 1 iff k>=6 and k%8 in (0, 6)."""
    return int(k >= 6 and k % 8 in (0, 6))


def unique_col() -> dict:
    """a=1..A_HI: G(t,3*2^a-1) and G(t,5*2^a-1) fire only at t=3*2^a-1."""
    n_ok = 0
    sample = {}
    for a in range(1, A_HI + 1):
        lo = 5 << (a - 1)
        hi = 1 << (a + 2)
        c3 = (3 << a) - 1
        c5 = (5 << a) - 1
        ones3 = []
        ones5 = []
        for t in range(lo, hi):
            if G(t, c3):
                ones3.append(t)
            if G(t, c5):
                ones5.append(t)
            n_ok += 1
        if ones3 != [c3] or ones5 != [c3]:
            return {
                "ok": False,
                "a": a,
                "ones3": ones3,
                "ones5": ones5,
                "want": c3,
            }
        if a <= 3:
            sample[str(a)] = {"c3": c3, "c5": c5, "n": hi - lo}
    ok = (
        n_ok > 0
        and sample["1"]["c3"] == 5
        and sample["1"]["c5"] == 9
        and sample["2"]["c3"] == 11
    )
    return {"ok": ok, "n_ok": n_ok, "a_hi": A_HI, "sample": sample}


def suffix_id() -> dict:
    """k=6..K_FORM covering s: r123(s,k)=r123_suffix(s,k)."""
    n_ok = 0
    sample = {}
    for k in range(6, K_FORM + 1):
        smin = 5 << (k - 5)
        shi = (1 << (k - 2)) - 1
        n_s = 0
        for s in range(smin, shi + 1):
            if r123(s, k) != r123_suffix(s, k):
                return {"ok": False, "k": k, "s": s}
            n_ok += 1
            n_s += 1
        if k <= 7:
            sample[str(k)] = {"n_s": n_s, "smin": smin, "shi": shi}
    ok = n_ok > 0 and sample["6"]["n_s"] == 6 and sample["7"]["n_s"] == 12
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_lo": 6,
        "k_hi": K_FORM,
        "sample": sample,
    }


def suffix_double() -> dict:
    """k=6..K_FORM: pal_suffix(2h,M+1)=pal_suffix(h,Mp+1) on covering h."""
    n_ok = 0
    for k in range(6, K_FORM + 1):
        M = 5 << (k - 4)
        Mp = 5 << (k - 5)
        tmin = 5 << (k - 6)
        thi = (1 << (k - 3)) - 1
        for h in range(tmin, thi + 1):
            if pal_suffix(2 * h, M + 1) != pal_suffix(h, Mp + 1):
                return {"ok": False, "even": k, "h": h}
            if pal_suffix(2 * h + 1, M + 1) != pal_suffix(h, Mp + 1):
                return {"ok": False, "odd": k, "h": h}
            n_ok += 1
    ok = n_ok > 0
    return {"ok": ok, "n_ok": n_ok, "k_lo": 6, "k_hi": K_FORM}


def folds() -> dict:
    """k=6..K_FOLD covering s: odd/even r123 folds vs parent xor unique col."""
    n_ok = 0
    sample = {}
    for k in range(6, K_FOLD + 1):
        smin = 5 << (k - 5)
        shi = (1 << (k - 2)) - 1
        ts = tstar(k)
        n_k = 0
        for s in range(smin, shi + 1):
            parent = s // 2
            if s % 2:
                want = r123(parent, k - 1) ^ G(parent, ts)
            else:
                want = r123(parent, k - 1) ^ ((k % 2) * G(parent, ts))
            if r123(s, k) != want:
                return {"ok": False, "k": k, "s": s, "got": r123(s, k), "want": want}
            n_ok += 1
            n_k += 1
        if k <= 7:
            sample[str(k)] = {"n": n_k, "tstar": ts}
    ok = n_ok > 0 and sample["6"]["n"] == 6 and sample["7"]["n"] == 12
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_lo": 6,
        "k_hi": K_FOLD,
        "sample": sample,
    }


def covering_xor() -> dict:
    """k=6..K_COVER: covering r123/ep/S match the 0-1 forms."""
    n_ok = 0
    rows = {}
    for k in range(6, K_COVER + 1):
        smin = 5 << (k - 5)
        shi = (1 << (k - 2)) - 1
        odd = even = r0 = 0
        for s in range(smin, shi + 1):
            v = r123(s, k)
            if s % 2:
                odd ^= v
            else:
                even ^= v
            r0 ^= ep_cover_rem(4 * s, k)
        r123x = odd ^ even
        tot = r0 ^ r123x
        if r0 != want_ep_cover(k - 2):
            return {"ok": False, "r0": k, "got": r0}
        if r123x != want_r123_ep(k):
            return {"ok": False, "r123": k, "got": r123x}
        if tot != want_ep_cover(k):
            return {"ok": False, "ep": k, "got": tot}
        if r123x != (1 ^ (k % 2)):
            return {"ok": False, "par": k, "got": r123x}
        cov_s = want_unclip_cover(k) ^ want_rem_cover(k)
        if cov_s != want_cover_s(k):
            return {"ok": False, "S": k, "got": cov_s}
        rows[str(k)] = {
            "odd": odd,
            "even": even,
            "r123": r123x,
            "r0": r0,
            "ep": tot,
            "S": cov_s,
        }
        n_ok += 1
    ok = (
        n_ok == K_COVER - 5
        and rows["6"]["r123"] == 1
        and rows["6"]["S"] == 1
        and rows["8"]["S"] == 1
        and rows["10"]["S"] == 0
        and rows["10"]["ep"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_lo": 6, "k_hi": K_COVER, "rows": rows}


def rem_s_forms() -> dict:
    """Closed rem and S forms match the recurrences; rem walk k<=K_REM."""
    n_ok = 0
    rows = {}
    for k in range(0, 24):
        rem = want_rem_cover(k)
        want_r = int(k >= 2 and k % 8 in (0, 2))
        if rem != want_r:
            return {"ok": False, "rem": k, "got": rem, "want": want_r}
        cov_s = want_unclip_cover(k) ^ rem
        if cov_s != want_cover_s(k):
            return {"ok": False, "S": k, "got": cov_s}
        n3 = want_n3_cover(k)
        ep = want_ep_cover(k)
        if k >= 2 and rem != (n3 ^ want_rem_cover(k - 2) ^ ep):
            return {"ok": False, "rec": k}
        n_ok += 1
    for k in range(0, K_REM + 1):
        parts = covering_rem_parts(k)
        if parts["tot"] != want_rem_cover(k):
            return {"ok": False, "walk": k, "got": parts["tot"]}
        if parts["ep"] != want_ep_cover(k):
            return {"ok": False, "walk_ep": k}
        if parts["n3"] != want_n3_cover(k):
            return {"ok": False, "walk_n3": k}
        got_s = want_unclip_cover(k) ^ parts["tot"]
        if got_s != want_cover_s(k):
            return {"ok": False, "walk_S": k, "got": got_s}
        rows[str(k)] = {
            "rem": parts["tot"],
            "S": got_s,
            "ep": parts["ep"],
            "n3": parts["n3"],
        }
    ok = (
        n_ok == 24
        and rows["2"]["S"] == 0
        and rows["6"]["S"] == 1
        and rows["8"]["S"] == 1
        and rows["0"]["rem"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_walk": K_REM, "rows": rows}


def killed_pointwise() -> dict:
    """k=6,s=12: even-s r123 is 1, not 0."""
    k, s = 6, 12
    got = r123(s, k)
    ok = s % 2 == 0 and got == 1
    return {"ok": ok, "k": k, "s": s, "got": got}


def prefixes() -> dict:
    oz = json.loads(OZ_JSON.read_text())
    oy = json.loads(OY_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oz["checks"]["all_ok"]
        and oy["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oz["verdict"]["r0_fold"] == "LEMMA"
        and oy["verdict"]["n3_xor_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oz["verdict"]["covering_S"] == "PREFIX"
        and oz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, uniq, suf, dbl, fld, cov, forms, k4, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and uniq["ok"]
        and suf["ok"]
        and dbl["ok"]
        and fld["ok"]
        and cov["ok"]
        and forms["ok"]
        and k4["ok"]
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
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    uniq = unique_col()
    suf = suffix_id()
    dbl = suffix_double()
    fld = folds()
    cov = covering_xor()
    forms = rem_s_forms()
    k4 = killed_pointwise()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, pal, slots, uniq, suf, dbl, fld, cov, forms, k4, sc, pref
    )
    dump = {
        "cycle": "PA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "unique_col": {k: uniq[k] for k in uniq if k != "ok"},
        "suffix_id": {k: suf[k] for k in suf if k != "ok"},
        "suffix_double": {k: dbl[k] for k in dbl if k != "ok"},
        "folds": {k: fld[k] for k in fld if k != "ok"},
        "covering_xor": {k: cov[k] for k in cov if k != "ok"},
        "rem_s_forms": {k: forms[k] for k in forms if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_pointwise": {k: k4[k] for k in k4 if k != "ok"},
        "lemmas": {
            "unique_col": True,
            "suffix_id": True,
            "r123_xor_all_k": True,
            "ep_xor_all_k": True,
            "covering_S": True,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_col": "LEMMA",
            "suffix_id": "LEMMA",
            "r123_xor_all_k": "LEMMA",
            "ep_xor_all_k": "LEMMA",
            "covering_S": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "even_s_r123_zero": "KILLED",
            "E_all_k": "PREFIX",
            "packed_R_eq_ST": "PREFIX",
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
    print("unique_col n_ok", dump["unique_col"]["n_ok"])
    print("suffix_id n_ok", dump["suffix_id"]["n_ok"])
    print("folds n_ok", dump["folds"]["n_ok"])
    print("covering_xor", dump["covering_xor"]["rows"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
