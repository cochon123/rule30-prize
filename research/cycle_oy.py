#!/usr/bin/env python3
"""Cycle OY: covering n3 rem of 4s folds by two; n3 xor is 1 iff k>=2 even.

Even-halve twice sends pal-right of 4s to pal-right of s at offsets
d%4==0, and covering thresholds scale by 4, so n3_cover_rem(4s,k)
equals n3_cover_rem(s,k-2) for k>=5. Clip-active t at k>=6 is the
4-groups of clip-active s at k-2, hence the r=0 covering xor is
n3(k-2). The r=1,2,3 rem xor of each group equals G(s,Lp-1) xor
G(s,Lp) with Lp=5*2^{k-5}. That column xor on the covering parent
window is P_pop(5)=1 on each of Lp-1 and Lp (Cycle AL prefix plus
one even-halve), so they cancel. Therefore covering n3 xor at k
equals n3 xor at k-2 for k>=6, and with bases n3(2)=1, n3(3)=0 it
is 1 iff k>=2 even, all k. Not the pointwise 4-to-1 fold (k=6,s=6).
Not one-step even-halve. Not covering S for all k (ep remains).
Not E_k=0 for all k. Do not catalogue further S/T subregions
unless the experiment answers why E_k=0. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_oy.py --certify
Dump: research/cycle_oy.json
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
from cycle_al import G, P_pop, xor_G_prefix
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_ou import n3_rem
from cycle_ow import want_n3_cover
from cycle_ox import n3_cover_rem

OUT = Path(__file__).resolve().with_suffix(".json")
OX_JSON = Path(__file__).resolve().parent / "cycle_ox.json"
OW_JSON = Path(__file__).resolve().parent / "cycle_ow.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
S_TAB = 32
K_FOLD = 8
K_ID = 10
K_COL = 12
K_COVER = 10


def n3_r123(s: int, k: int) -> int:
    """Xor of covering n3 rem on 4s+1, 4s+2, 4s+3 at scale k."""
    return (
        n3_cover_rem(4 * s + 1, k)
        ^ n3_cover_rem(4 * s + 2, k)
        ^ n3_cover_rem(4 * s + 3, k)
    )


def n3_r123_green(s: int, k: int) -> int:
    """G(s, Lp-1) xor G(s, Lp), Lp=5*2^{k-5}."""
    Lp = 5 << (k - 5)
    return G(s, Lp - 1) ^ G(s, Lp)


def pal_t1(s: int, d: int) -> int:
    """Pal-right of 4s+1 from G(s)."""
    f = d // 4
    r = d % 4
    if r == 0 or r == 1:
        return G(s, s + f)
    if r == 2:
        return 0
    return G(s, s + f + 1)


def pal_t2(s: int, d: int) -> int:
    """Pal-right of 4s+2 from G(s)."""
    if d % 2:
        return 0
    f = d // 4
    if d % 4 == 0:
        return G(s, s + f)
    return G(s, s + f) ^ G(s, s + f + 1)


def pal_t3(s: int, d: int) -> int:
    """Pal-right of 4s+3 from G(s)."""
    f = d // 4
    r = d % 4
    if r == 0 or r == 3:
        return G(s, s + f)
    if r == 1:
        return G(s, s + f + 1)
    return G(s, s + f) ^ G(s, s + f + 1)


def doubling_tables() -> dict:
    """s<=S_TAB: pal-right of 4s+r matches the G(s) tables."""
    n_ok = 0
    for s in range(0, S_TAB + 1):
        t0 = 4 * s
        for d in range(0, t0 + 1):
            want = G(s, s + d // 4) if d % 4 == 0 else 0
            if G(t0, t0 + d) != want:
                return {"ok": False, "r": 0, "s": s, "d": d}
            n_ok += 1
        t1 = 4 * s + 1
        for d in range(0, t1 + 1):
            if G(t1, t1 + d) != pal_t1(s, d):
                return {"ok": False, "r": 1, "s": s, "d": d}
            n_ok += 1
        t2 = 4 * s + 2
        for d in range(0, t2 + 1):
            if G(t2, t2 + d) != pal_t2(s, d):
                return {"ok": False, "r": 2, "s": s, "d": d}
            n_ok += 1
        t3 = 4 * s + 3
        for d in range(0, t3 + 1):
            if G(t3, t3 + d) != pal_t3(s, d):
                return {"ok": False, "r": 3, "s": s, "d": d}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "s_hi": S_TAB}


def r0_fold() -> dict:
    """k=5..K_FOLD, s<2^{k-2}: n3_cover_rem(4s,k)=n3_cover_rem(s,k-2)."""
    n_ok = 0
    sample = {}
    for k in range(5, K_FOLD + 1):
        n_k = 0
        for s in range(0, 1 << (k - 2)):
            got = n3_cover_rem(4 * s, k)
            want = n3_cover_rem(s, k - 2)
            if got != want:
                return {"ok": False, "k": k, "s": s, "got": got, "want": want}
            n_ok += 1
            n_k += 1
        if k <= 6:
            sample[str(k)] = {"n": n_k}
    ok = n_ok > 0 and sample["5"]["n"] == 8 and sample["6"]["n"] == 16
    return {"ok": ok, "n_ok": n_ok, "k_lo": 5, "k_hi": K_FOLD, "sample": sample}


def r123_id() -> dict:
    """k=6..K_ID: clip-active r123 rem xor equals G(s,Lp-1) xor G(s,Lp)."""
    n_ok = 0
    sample = {}
    for k in range(6, K_ID + 1):
        smin = 5 << (k - 6)
        shi = (1 << (k - 3)) - 1
        xor_r123 = xor_col = 0
        n_s = 0
        tmin = 5 << (k - 4)
        thi = (1 << (k - 1)) - 1
        groups = {4 * s + r for s in range(smin, shi + 1) for r in range(4)}
        child = set(range(tmin, thi + 1))
        if groups != child:
            return {"ok": False, "part": k, "smin": smin, "shi": shi}
        for s in range(smin, shi + 1):
            got = n3_r123(s, k)
            want = n3_r123_green(s, k)
            if got != want:
                return {"ok": False, "id": k, "s": s, "got": got, "want": want}
            if n3_cover_rem(4 * s, k) != n3_cover_rem(s, k - 2):
                return {"ok": False, "r0": k, "s": s}
            xor_r123 ^= got
            xor_col ^= want
            n_ok += 1
            n_s += 1
        if xor_r123 != 0 or xor_col != 0:
            return {"ok": False, "xor": k, "r123": xor_r123, "col": xor_col}
        if k <= 8:
            sample[str(k)] = {
                "n_s": n_s,
                "smin": smin,
                "shi": shi,
                "xor_r123": xor_r123,
            }
    ok = (
        n_ok > 0
        and sample["6"]["n_s"] == 3
        and sample["8"]["n_s"] == 12
        and sample["6"]["xor_r123"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_lo": 6,
        "k_hi": K_ID,
        "sample": sample,
    }


def column_xor() -> dict:
    """a=1..K_COL-5: covering window column xor of G(s,Lp) and G(s,Lp-1) is 1."""
    if P_pop(5) != 1:
        return {"ok": False, "P5": P_pop(5)}
    n_ok = 0
    sample = {}
    for a in range(1, K_COL - 4):
        U = 1 << a
        Lp = 5 * U
        smin = Lp // 2
        shi = 1 << (a + 2)
        if xor_G_prefix(shi, Lp - 1) != 1:
            return {"ok": False, "al": a, "d": Lp - 1}
        if xor_G_prefix(4 * U, 5 * U - 1) != P_pop(5):
            return {"ok": False, "al5": a}
        # Even N=4U: xor_s<N G(s,5U) = xor_p<2U G(p, 5U/2-1), which is AL at U/2.
        if xor_G_prefix(shi, Lp) != 1:
            return {"ok": False, "even": a, "d": Lp}
        for s in range(0, smin):
            if G(s, Lp) or G(s, Lp - 1):
                return {"ok": False, "below": a, "s": s}
        x1 = xor_G_prefix(shi, Lp - 1) ^ xor_G_prefix(smin, Lp - 1)
        x2 = xor_G_prefix(shi, Lp) ^ xor_G_prefix(smin, Lp)
        if x1 != 1 or x2 != 1:
            return {"ok": False, "win": a, "x1": x1, "x2": x2}
        n_ok += 1
        if a <= 3:
            sample[str(a)] = {"Lp": Lp, "smin": smin, "shi": shi, "x1": x1, "x2": x2}
    ok = n_ok == K_COL - 5 and sample["1"]["x1"] == 1 and sample["1"]["x2"] == 1
    return {"ok": ok, "n_ok": n_ok, "a_hi": K_COL - 5, "sample": sample}


def n3_rec() -> dict:
    """k<=K_COVER: covering n3 xor equals want_n3_cover; k>=6 equals n3(k-2)."""
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        U = 1 << k
        xor_rem = n_clip = 0
        for t in range(U >> 1):
            n = 8 * t + 3
            if 2 * n <= 5 * U:
                continue
            xor_rem ^= n3_rem(t, 5 * U)
            n_clip += 1
        want = want_n3_cover(k)
        rows[str(k)] = {"xor_rem": xor_rem, "n_clip": n_clip, "want": want}
        if xor_rem != want:
            return {"ok": False, "k": k, "got": xor_rem, "want": want}
        if k >= 6 and xor_rem != rows[str(k - 2)]["xor_rem"]:
            return {"ok": False, "rec": k, "got": xor_rem, "prev": rows[str(k - 2)]["xor_rem"]}
        n_ok += 1
    ok = (
        n_ok == K_COVER + 1
        and rows["2"]["xor_rem"] == 1
        and rows["3"]["xor_rem"] == 0
        and rows["10"]["xor_rem"] == 1
        and rows["9"]["xor_rem"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": rows}


def killed_pointwise() -> dict:
    """k=6,s=6: xor of four children is 0, parent rem is 1."""
    k, s = 6, 6
    kids = [n3_cover_rem(4 * s + r, k) for r in range(4)]
    got = 0
    for v in kids:
        got ^= v
    want = n3_cover_rem(s, k - 2)
    ok = kids[0] == want and got != want and got == 0 and want == 1
    return {"ok": ok, "k": k, "s": s, "kids": kids, "got": got, "want": want}


def killed_one_step() -> dict:
    """k=5, clip-active even t=10: n3_cover_rem(10,5)=1 != n3_cover_rem(5,4)=0."""
    got = n3_cover_rem(10, 5)
    want = n3_cover_rem(5, 4)
    ok = got == 1 and want == 0
    return {"ok": ok, "t": 10, "got": got, "want": want}


def prefixes() -> dict:
    ox = json.loads(OX_JSON.read_text())
    ow = json.loads(OW_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        ox["checks"]["all_ok"]
        and ow["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and ox["verdict"]["n3_shape"] == "LEMMA"
        and ox["verdict"]["n3_xor"] == "CERTIFIED"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and ox["verdict"]["covering_S"] == "PREFIX"
        and ox["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tab, fold, ident, col, rec, k4, k1, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and tab["ok"]
        and fold["ok"]
        and ident["ok"]
        and col["ok"]
        and rec["ok"]
        and k4["ok"]
        and k1["ok"]
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
    tab = doubling_tables()
    fold = r0_fold()
    ident = r123_id()
    col = column_xor()
    rec = n3_rec()
    k4 = killed_pointwise()
    k1 = killed_one_step()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tab, fold, ident, col, rec, k4, k1, sc, pref)
    dump = {
        "cycle": "OY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "doubling_tables": {k: tab[k] for k in tab if k != "ok"},
        "r0_fold": {k: fold[k] for k in fold if k != "ok"},
        "r123_id": {k: ident[k] for k in ident if k != "ok"},
        "column_xor": {k: col[k] for k in col if k != "ok"},
        "n3_rec": {k: rec[k] for k in rec if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_pointwise": {k: k4[k] for k in k4 if k != "ok"},
        "killed_one_step": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "r0_fold": True,
            "r123_green": True,
            "column_xor": True,
            "n3_xor_all_k": True,
            "ep_xor_all_k": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "r0_fold": "LEMMA",
            "r123_green": "LEMMA",
            "column_xor": "LEMMA",
            "n3_xor_all_k": "LEMMA",
            "n3_shape": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "pointwise_4to1": "KILLED",
            "one_step_even_halve": "KILLED",
            "ep_xor_all_k": "PREFIX",
            "covering_S": "PREFIX",
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
    print("r0_fold n_ok", dump["r0_fold"]["n_ok"])
    print("r123_id n_ok", dump["r123_id"]["n_ok"])
    print("column_xor n_ok", dump["column_xor"]["n_ok"])
    print("n3_rec", dump["n3_rec"]["rows"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
