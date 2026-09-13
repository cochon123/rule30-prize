#!/usr/bin/env python3
"""Cycle PB: covering S xor T is 1 iff k==2 or (k>=6 and k%8 in (0, 6)).

Cycle PA closed covering S; Cycle OJ closed covering T. Their xor
is the Green residual that packed rest must match for E_k=0: 1 iff
k==2 or (k>=6 and k%8 in (0, 6)). It equals Cycle MD's rest10 on
k<=10. Pal-left packed rest xor vanishes through k<=6 and dies at
k=7, so pal-left cancel is not why E_k=0. Even n still has S=T=0
(Cycles OK/OJ), so E=0 iff even-n rest equals odd-n error; that
is a rewrite, not a packed identity. Not rest=S xor T for all k.
Not E_k=0 for all k. Do not catalogue further S/T subregions
unless the experiment answers why E_k=0. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pb.py --certify
Dump: research/cycle_pb.json
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
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal, want_cover_t
from cycle_pa import want_cover_s
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PA_JSON = Path(__file__).resolve().parent / "cycle_pa.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"
MD_JSON = Path(__file__).resolve().parent / "cycle_md.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_LEFT = 7


def want_rest_e0(k: int) -> int:
    """Covering S xor T: predicted rest if E_k=0, all k."""
    return want_cover_s(k) ^ want_cover_t(k)


def rest_form() -> dict:
    """k<=24: want_rest_e0 matches S xor T; equals rest10 on k<=10."""
    n_ok = 0
    rows = {}
    for k in range(0, 25):
        st = want_cover_s(k) ^ want_cover_t(k)
        got = want_rest_e0(k)
        want = int(k == 2 or (k >= 6 and k % 8 in (0, 6)))
        if got != st or got != want:
            return {"ok": False, "k": k, "got": got, "st": st, "want": want}
        if k <= K_REST and got != want_rest10(k, 10):
            return {"ok": False, "mdk": k, "got": got, "md": want_rest10(k, 10)}
        if k <= 12:
            rows[str(k)] = {"ST": st, "S": want_cover_s(k), "T": want_cover_t(k)}
        n_ok += 1
    ok = (
        n_ok == 25
        and rows["2"]["ST"] == 1
        and rows["6"]["ST"] == 1
        and rows["8"]["ST"] == 1
        and rows["10"]["ST"] == 0
        and rows["0"]["ST"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": 24, "rows": rows}


def pal_left_rest() -> dict:
    """k<=K_LEFT: pal-left packed rest xor; 0 through k<=6, 1 at k=7."""
    n_ok = 0
    rows = {}
    for k in range(0, K_LEFT + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        xor_l = xor_r = xor_e = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                t = (s - t0) // 2
                n = odd_clock(t, U, Q)
                half = U >> 1
                for j in range(0, 2 * n + 1):
                    p = T - 2 * j
                    if p < 0:
                        continue
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    if G(n, j) == 0:
                        continue
                    rbit = packed if p not in FORCED else 0
                    pal = j > n
                    if pal:
                        xor_r ^= rbit
                        d = j - n
                        jm1, jp1 = G(n, j - 1), G(n, j + 1)
                        sbit = jp1 if (d % 3 == 1 and jm1 == 0) else 0
                        tbit = jm1 if n < half else 0
                        xor_e ^= rbit ^ sbit ^ tbit
                    else:
                        xor_l ^= rbit
            row = rule30_step(row)
            s += 1
        want_l = int(k == 7)
        if xor_l != want_l:
            return {"ok": False, "k": k, "got": xor_l, "want": want_l}
        if (xor_l ^ xor_e) != 0:
            return {"ok": False, "E": k, "L": xor_l, "eR": xor_e}
        rows[str(k)] = {"L": xor_l, "R": xor_r, "eR": xor_e}
        n_ok += 1
    ok = (
        n_ok == K_LEFT + 1
        and rows["6"]["L"] == 0
        and rows["7"]["L"] == 1
        and rows["2"]["R"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_LEFT, "rows": rows}


def prefixes() -> dict:
    pa = json.loads(PA_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    md = json.loads(MD_JSON.read_text())
    ok = (
        pa["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and md["checks"]["all_ok"]
        and pa["verdict"]["covering_S"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and pa["verdict"]["prize"] == "unsolved"
        and pa["verdict"]["packed_R_eq_ST"] == "PREFIX"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, form, left, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and form["ok"] and left["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    form = rest_form()
    left = pal_left_rest()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, form, left, sc, pref)
    dump = {
        "cycle": "PB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "rest_form": {k: form[k] for k in form if k != "ok"},
        "pal_left_rest": {k: left[k] for k in left if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ST_all_k": True,
            "pal_left_rest_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ST_all_k": "LEMMA",
            "pal_left_rest": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "pal_left_rest_all_k": "KILLED",
            "packed_R_eq_ST": "PREFIX",
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
    print("rest_form", dump["rest_form"]["rows"])
    print("pal_left_rest", dump["pal_left_rest"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
