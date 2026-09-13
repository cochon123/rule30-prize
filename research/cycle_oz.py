#!/usr/bin/env python3
"""Cycle OZ: covering even-parent rem of 4s folds by two; r0 xor is ep(k-2).

Even-halve twice sends pal-right of p=4s to pal-right of s at offsets
d%4==0, and covering R2 thresholds scale by 4, so ep_cover_rem(4s,k)
equals ep_cover_rem(s,k-2) for k>=4. Clip-active p at k>=5 is the
4-groups of clip-active s at k-2, hence the r=0 covering xor is
ep(k-2). The r=1,2,3 xor is 1 iff k>=6 even on k<=12, so covering
ep xor is 1 iff k>=6 and k%4==2 on that range. Not the pointwise
4-to-1 fold (k=6,s=11). Not ep xor for all k. Not covering S for
all k. Not E_k=0 for all k. Do not catalogue further S/T
subregions unless the experiment answers why E_k=0. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_oz.py --certify
Dump: research/cycle_oz.json
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
from cycle_os import r2_tail
from cycle_ow import want_ep_cover
from cycle_oy import pal_t1, pal_t2, pal_t3

OUT = Path(__file__).resolve().with_suffix(".json")
OY_JSON = Path(__file__).resolve().parent / "cycle_oy.json"
OW_JSON = Path(__file__).resolve().parent / "cycle_ow.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
S_TAB = 32
K_FOLD = 8
K_COVER = 12


def ep_cover_rem(p: int, k: int) -> int:
    """Covering R2 tail of p at k>=2: dmin=5*2^{k-2}-p+1."""
    return r2_tail(p, (5 << (k - 2)) - p + 1)


def want_r123_ep(k: int) -> int:
    """Covering r=1,2,3 ep rem xor on k<=12."""
    if k < 2:
        return want_ep_cover(k)
    return want_ep_cover(k) ^ want_ep_cover(k - 2)


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
    """k=4..K_FOLD, s<2^{k-2}: ep_cover_rem(4s,k)=ep_cover_rem(s,k-2)."""
    n_ok = 0
    sample = {}
    for k in range(4, K_FOLD + 1):
        n_k = 0
        for s in range(0, 1 << (k - 2)):
            got = ep_cover_rem(4 * s, k)
            want = ep_cover_rem(s, k - 2)
            if got != want:
                return {"ok": False, "k": k, "s": s, "got": got, "want": want}
            n_ok += 1
            n_k += 1
        if k <= 6:
            sample[str(k)] = {"n": n_k}
    ok = n_ok > 0 and sample["4"]["n"] == 4 and sample["6"]["n"] == 16
    return {"ok": ok, "n_ok": n_ok, "k_lo": 4, "k_hi": K_FOLD, "sample": sample}


def covering_split() -> dict:
    """k=5..K_COVER: 4-groups partition; r0 xor=ep(k-2); tot=want_ep."""
    n_ok = 0
    rows = {}
    for k in range(5, K_COVER + 1):
        pmin = 5 << (k - 3)
        phi = (1 << k) - 1
        smin = 5 << (k - 5)
        shi = (1 << (k - 2)) - 1
        child = set(range(pmin, phi + 1))
        groups = {4 * s + r for s in range(smin, shi + 1) for r in range(4)}
        if child != groups:
            return {"ok": False, "part": k}
        px = [0, 0, 0, 0]
        n = [0, 0, 0, 0]
        for p in range(pmin, phi + 1):
            px[p % 4] ^= ep_cover_rem(p, k)
            n[p % 4] += 1
        tot = px[0] ^ px[1] ^ px[2] ^ px[3]
        r123 = px[1] ^ px[2] ^ px[3]
        if px[0] != want_ep_cover(k - 2):
            return {"ok": False, "r0": k, "got": px[0], "want": want_ep_cover(k - 2)}
        if r123 != want_r123_ep(k):
            return {"ok": False, "r123": k, "got": r123, "want": want_r123_ep(k)}
        if tot != want_ep_cover(k):
            return {"ok": False, "tot": k, "got": tot, "want": want_ep_cover(k)}
        rows[str(k)] = {
            "n": n,
            "px": px,
            "r0": px[0],
            "r123": r123,
            "tot": tot,
            "want": want_ep_cover(k),
        }
        n_ok += 1
    ok = (
        n_ok == K_COVER - 4
        and rows["6"]["tot"] == 1
        and rows["8"]["tot"] == 0
        and rows["10"]["tot"] == 1
        and rows["12"]["tot"] == 0
        and rows["6"]["r123"] == 1
        and rows["12"]["r0"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_lo": 5, "k_hi": K_COVER, "rows": rows}


def killed_pointwise() -> dict:
    """k=6,s=11: xor of four children is 0, parent rem is 1."""
    k, s = 6, 11
    kids = [ep_cover_rem(4 * s + r, k) for r in range(4)]
    got = 0
    for v in kids:
        got ^= v
    want = ep_cover_rem(s, k - 2)
    ok = kids[0] == want and got != want and got == 0 and want == 1
    return {"ok": ok, "k": k, "s": s, "kids": kids, "got": got, "want": want}


def prefixes() -> dict:
    oy = json.loads(OY_JSON.read_text())
    ow = json.loads(OW_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oy["checks"]["all_ok"]
        and ow["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oy["verdict"]["n3_xor_all_k"] == "LEMMA"
        and oy["verdict"]["r0_fold"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oy["verdict"]["covering_S"] == "PREFIX"
        and oy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tab, fold, split, k4, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and tab["ok"]
        and fold["ok"]
        and split["ok"]
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
    tab = doubling_tables()
    fold = r0_fold()
    split = covering_split()
    k4 = killed_pointwise()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tab, fold, split, k4, sc, pref)
    dump = {
        "cycle": "OZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "doubling_tables": {k: tab[k] for k in tab if k != "ok"},
        "r0_fold": {k: fold[k] for k in fold if k != "ok"},
        "covering_split": {k: split[k] for k in split if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_pointwise": {k: k4[k] for k in k4 if k != "ok"},
        "lemmas": {
            "r0_fold": True,
            "r0_xor_ep_prev": True,
            "n3_xor_all_k": True,
            "ep_xor_all_k": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "r0_fold": "LEMMA",
            "r0_xor_ep_prev": "LEMMA",
            "n3_xor_all_k": "LEMMA",
            "ep_xor": "CERTIFIED",
            "r123_xor": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "pointwise_4to1": "KILLED",
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
    print("covering_split", dump["covering_split"]["rows"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
