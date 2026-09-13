#!/usr/bin/env python3
"""Cycle OX: covering n=8t+3 rem is two-threshold R1/R2 tails.

For k>=3, n3_rem(t, 5*2^k) is r1_tail(t, L-t) xor r2_tail(t, L-t+1)
with L=5*2^{k-3}. Covering clip-active t is {5*2^{k-4},...,2^{k-1}-1}
for k>=4, count 3*2^{k-4}. L>t always, so neither residue is the
full R1 or R2. That xor is 1 iff k>=2 even on k<=12. Not a single
dmin tail. Not full A(t) xor over clip t (k>=6 that xor is 0). Not
n3 xor for all k. Not covering S for all k. Not E_k=0 for all k.
Do not catalogue further S/T subregions unless the experiment
answers why E_k=0. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ox.py --certify
Dump: research/cycle_ox.json
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
from cycle_ol import pal_right_off0
from cycle_ou import n3_rem
from cycle_ow import want_n3_cover

OUT = Path(__file__).resolve().with_suffix(".json")
OW_JSON = Path(__file__).resolve().parent / "cycle_ow.json"
OU_JSON = Path(__file__).resolve().parent / "cycle_ou.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
K_COVER = 12


def r_tail(t: int, r: int, dmin: int) -> int:
    """Xor G(t,t+d) for d%3==r, d>=dmin, 1<=d<=t."""
    acc = 0
    for d in range(max(dmin, 1), t + 1):
        if d % 3 == r:
            acc ^= G(t, t + d)
    return acc


def n3_cover_rem(t: int, k: int) -> int:
    """Covering-shaped two-threshold rem of n=8t+3 at k>=3."""
    L = 5 << (k - 3)
    return r_tail(t, 1, L - t) ^ r_tail(t, 2, L - t + 1)


def n3_shape() -> dict:
    """k=4..K_COVER: clip-active t is [5*2^{k-4}, 2^{k-1}); tails match; L>t."""
    n_ok = n_match = 0
    sample = {}
    for k in range(4, K_COVER + 1):
        U = 1 << k
        jmax = 5 * U
        tmin = 5 << (k - 4)
        t_hi = (U >> 1) - 1
        L = 5 << (k - 3)
        n_clip = 0
        xor_rem = xor_A = 0
        for t in range(U >> 1):
            n = 8 * t + 3
            active = 2 * n > jmax
            if active:
                if t < tmin or t > t_hi:
                    return {"ok": False, "range": k, "t": t}
                if L <= t:
                    return {"ok": False, "full": k, "t": t, "L": L}
                got = n3_rem(t, jmax)
                want = n3_cover_rem(t, k)
                if got != want:
                    return {"ok": False, "tail": k, "t": t, "got": got, "want": want}
                n_clip += 1
                n_match += 1
                xor_rem ^= got
                if t:
                    xor_A ^= pal_right_off0(t)
            elif t >= tmin:
                return {"ok": False, "inactive": k, "t": t}
            n_ok += 1
        if n_clip != 3 << (k - 4):
            return {"ok": False, "count": k, "n_clip": n_clip}
        if xor_rem != want_n3_cover(k):
            return {"ok": False, "xor": k, "got": xor_rem, "want": want_n3_cover(k)}
        if k <= 6:
            sample[str(k)] = {
                "n_clip": n_clip,
                "tmin": tmin,
                "L": L,
                "t_hi": t_hi,
                "xor": xor_rem,
                "xor_A": xor_A,
            }
    ok = (
        n_match > 0
        and sample["4"]["n_clip"] == 3
        and sample["6"]["n_clip"] == 12
        and sample["4"]["xor"] == 1
        and sample["5"]["xor"] == 0
        and sample["6"]["xor"] == 1
        and sample["6"]["xor_A"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_match": n_match,
        "k_lo": 4,
        "k_hi": K_COVER,
        "sample": sample,
    }


def n3_xor_bits() -> dict:
    """k<=K_COVER: covering n3 rem xor equals want_n3_cover."""
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        U = 1 << k
        jmax = 5 * U
        xor_rem = n_clip = 0
        for t in range(U >> 1):
            n = 8 * t + 3
            if 2 * n <= jmax:
                continue
            xor_rem ^= n3_rem(t, jmax)
            n_clip += 1
        want = want_n3_cover(k)
        rows[str(k)] = {"xor_rem": xor_rem, "n_clip": n_clip, "want": want}
        if xor_rem != want:
            return {"ok": False, "k": k, "got": xor_rem, "want": want}
        n_ok += 1
    ok = (
        n_ok == K_COVER + 1
        and rows["2"]["xor_rem"] == 1
        and rows["12"]["xor_rem"] == 1
        and rows["11"]["xor_rem"] == 0
        and rows["6"]["xor_rem"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": rows}


def killed_full_A(shape: dict) -> dict:
    """k=6: xor of unclipped A(t) over clip t is 0, but n3 rem xor is 1."""
    xor_A = shape["sample"]["6"]["xor_A"]
    xor_rem = shape["sample"]["6"]["xor"]
    ok = xor_A == 0 and xor_rem == 1
    return {"ok": ok, "k": 6, "xor_A": xor_A, "xor_rem": xor_rem}


def prefixes() -> dict:
    ow = json.loads(OW_JSON.read_text())
    ou = json.loads(OU_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        ow["checks"]["all_ok"]
        and ou["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and ow["verdict"]["ep_shape"] == "LEMMA"
        and ou["verdict"]["n3_rem"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and ow["verdict"]["covering_S"] == "PREFIX"
        and ow["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, shape, bits, ka, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and shape["ok"] and bits["ok"] and ka["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    shape = n3_shape()
    bits = n3_xor_bits()
    ka = killed_full_A(shape)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, shape, bits, ka, sc, pref)
    dump = {
        "cycle": "OX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "n3_shape": {k: shape[k] for k in shape if k != "ok"},
        "n3_xor_bits": {k: bits[k] for k in bits if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_full_A": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "n3_shape": True,
            "n3_rem": True,
            "ep_shape": True,
            "n3_xor_all_k": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n3_shape": "LEMMA",
            "n3_rem": "LEMMA",
            "ep_shape": "LEMMA",
            "n3_xor": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "full_A": "KILLED",
            "n3_xor_all_k": "PREFIX",
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
    print("n3_shape n_ok", dump["n3_shape"]["n_ok"], "n_match", dump["n3_shape"]["n_match"])
    print("n3_xor_bits", dump["n3_xor_bits"]["rows"])
    print("killed_full_A", dump["killed_full_A"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
