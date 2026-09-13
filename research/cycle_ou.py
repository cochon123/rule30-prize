#!/usr/bin/env python3
"""Cycle OU: clip-removed S of n=8t+3 is the 8-scale off0 image of G(t).

Unclipped S(8t+3) is pal-right off-residue-0 xor of G(t) (Cycle OL),
equal to 1 for t>=1 (Cycle OO). Two Green doublings plus even-halve
place those cells on pal-right of n at j=8(t+d)+5 (d%3==1) and
j=8(t+d) (d%3==2); residue-2 also has a silent partner at
j=8(t+d)+3. Clip-removed S is the xor of G(t,t+d) over off0 d
with that fire-image past jmax. Any jmax, not only covering
5*2^k. Covering n=8t+3 rem xor is 1 iff k>=2 and k even, on
k<=8. Not a single dmin tail of off0 (n=11, jmax=20). Not
Cycle OT's 8t+7 fold. Not covering S for all k. Not E_k=0 for
all k. Do not catalogue further S/T subregions unless the
experiment answers why E_k=0. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_ou.py --certify
Dump: research/cycle_ou.json
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
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_ol import pal_right_off0
from cycle_os import even_parent_rem, removed_s
from cycle_ot import n7_rem_fold

OUT = Path(__file__).resolve().with_suffix(".json")
OT_JSON = Path(__file__).resolve().parent / "cycle_ot.json"
OS_JSON = Path(__file__).resolve().parent / "cycle_os.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
T_HI = 48
K_COVER = 8


def n3_image_j(t: int, d: int) -> int:
    """Fire-image j on n=8t+3 of pal-right offset d of t."""
    if d % 3 == 1:
        return 8 * (t + d) + 5
    if d % 3 == 2:
        return 8 * (t + d)
    raise ValueError("off0 d required")


def n3_rem(t: int, jmax: int) -> int:
    """Clip-removed pal-right S of n=8t+3 at jmax."""
    acc = 0
    for d in range(1, t + 1):
        if d % 3 == 0:
            continue
        if n3_image_j(t, d) > jmax:
            acc ^= G(t, t + d)
    return acc


def n3_fires(t: int) -> set[int]:
    """Predicted S-fire j on n=8t+3."""
    out = set()
    for d in range(1, t + 1):
        if d % 3 == 0:
            continue
        if G(t, t + d):
            out.add(n3_image_j(t, d))
    return out


def s_fires(n: int) -> set[int]:
    out = set()
    for j in range(n + 1, 2 * n + 1):
        if G(n, j) == 0:
            continue
        if (j - n) % 3 != 1:
            continue
        if G(n, j - 1) != 0:
            continue
        if G(n, j + 1):
            out.add(j)
    return out


def fire_map() -> dict:
    """t<T_HI: S-fires of n=8t+3 equal the 8-scale off0 images."""
    n_ok = n_one = 0
    sample = {}
    for t in range(0, T_HI):
        n = 8 * t + 3
        got = s_fires(n)
        want = n3_fires(t)
        if got != want:
            return {"ok": False, "t": t, "n": n, "got": sorted(got), "want": sorted(want)}
        n_ok += 1
        n_one += pal_right_off0(t)
        if t <= 3:
            sample[str(t)] = {
                "n": n,
                "n_fire": len(got),
                "off0": pal_right_off0(t),
            }
    ok = (
        n_ok == T_HI
        and sample["0"]["n_fire"] == 0
        and sample["1"]["n_fire"] == 1
        and sample["0"]["off0"] == 0
        and sample["1"]["off0"] == 1
        and n_one > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "t_hi": T_HI, "sample": sample}


def n3_any_j() -> dict:
    """t<T_HI, several jmax: removed_s(8t+3)==n3_rem."""
    n_ok = n_one = 0
    sample = {}
    extras = (0, 1, 5, 10, 20, 40, 44, 80, 160)
    for t in range(0, T_HI):
        n = 8 * t + 3
        jmaxes = set(extras)
        jmaxes.update((n // 2, n, 2 * n - 1, 2 * n, n + 10, (5 * n) // 2))
        for jmax in jmaxes:
            got = removed_s(n, jmax)
            want = n3_rem(t, jmax)
            if got != want:
                return {
                    "ok": False,
                    "t": t,
                    "n": n,
                    "jmax": jmax,
                    "got": got,
                    "want": want,
                }
            n_ok += 1
            n_one += got
        if t <= 2:
            sample[str(t)] = {
                "n": n,
                "full": n3_rem(t, n),
                "off0": pal_right_off0(t),
            }
    ok = (
        n_ok > 0
        and n_one > 0
        and sample["0"]["full"] == 0
        and sample["1"]["full"] == 1
        and sample["1"]["full"] == sample["1"]["off0"]
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "t_hi": T_HI, "sample": sample}


def covering_n3() -> dict:
    """q=10 k<=K_COVER: covering n=8t+3 rem equals n3_rem; xor=1 iff k even >=2."""
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        jmax = T // 2
        xor_rem = 0
        n_n3 = 0
        tclk = 0
        sclk = t0 + 1
        while sclk < T:
            n = odd_clock(tclk, U, Q)
            if n % 8 == 3:
                t = (n - 3) // 8
                got = removed_s(n, jmax)
                want = n3_rem(t, jmax)
                if got != want:
                    return {"ok": False, "k": k, "n": n, "got": got, "want": want}
                xor_rem ^= got
                n_n3 += 1
                n_ok += 1
            tclk += 1
            sclk += 2
        want_xor = int(k >= 2 and k % 2 == 0)
        rows[str(k)] = {"xor_rem": xor_rem, "n_n3": n_n3, "want": want_xor}
        if xor_rem != want_xor:
            return {"ok": False, "k": k, "xor_rem": xor_rem, "want": want_xor}
    ok = (
        rows["2"]["xor_rem"] == 1
        and rows["3"]["xor_rem"] == 0
        and rows["8"]["xor_rem"] == 1
        and n_ok > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": rows}


def killed_dmin() -> dict:
    """n=11, jmax=20: rem=1, naive off0 tail dmin=jmax/8-t+1 is 0."""
    t, n, jmax = 1, 11, 20
    rem = removed_s(n, jmax)
    dmin = jmax // 8 - t + 1
    tail = 0
    for d in range(max(dmin, 1), t + 1):
        if d % 3:
            tail ^= G(t, t + d)
    ok = rem == 1 and tail == 0 and n3_rem(t, jmax) == 1
    return {"ok": ok, "n": n, "jmax": jmax, "rem": rem, "tail": tail, "dmin": dmin}


def killed_ot_fold() -> dict:
    """n=51=8*6+3, jmax=80: rem=1, not n7_rem_fold."""
    n, jmax = 51, 80
    rem = removed_s(n, jmax)
    t = (n - 3) // 8
    wrong = n7_rem_fold(t, 4)
    ok = n % 8 == 3 and rem == 1 and rem == n3_rem(t, jmax) and wrong == 0
    return {"ok": ok, "n": n, "jmax": jmax, "rem": rem, "n7_fold": wrong}


def killed_even_parent() -> dict:
    """n=51, jmax=80: even_parent_rem of nearby 4p+1 is not this rem."""
    n, jmax = 51, 80
    rem = removed_s(n, jmax)
    near = even_parent_rem(49, jmax)
    ok = rem == 1 and near == 0
    return {"ok": ok, "n": n, "jmax": jmax, "rem": rem, "near49": near}


def prefixes() -> dict:
    otj = json.loads(OT_JSON.read_text())
    osj = json.loads(OS_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        otj["checks"]["all_ok"]
        and osj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and otj["verdict"]["n7_clip_fold"] == "LEMMA"
        and osj["verdict"]["even_parent_rem"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and otj["verdict"]["covering_S"] == "PREFIX"
        and otj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fmap, anyj, cover, kd, ko, ke, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and fmap["ok"]
        and anyj["ok"]
        and cover["ok"]
        and kd["ok"]
        and ko["ok"]
        and ke["ok"]
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
    fmap = fire_map()
    anyj = n3_any_j()
    cover = covering_n3()
    kd = killed_dmin()
    ko = killed_ot_fold()
    ke = killed_even_parent()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fmap, anyj, cover, kd, ko, ke, sc, pref)
    dump = {
        "cycle": "OU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "fire_map": {k: fmap[k] for k in fmap if k != "ok"},
        "n3_any_j": {k: anyj[k] for k in anyj if k != "ok"},
        "covering_n3": {k: cover[k] for k in cover if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_dmin": {k: kd[k] for k in kd if k != "ok"},
        "killed_ot_fold": {k: ko[k] for k in ko if k != "ok"},
        "killed_even_parent": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "n3_image": True,
            "n3_rem": True,
            "n7_clip_fold": True,
            "even_parent_rem": True,
            "dmin_tail": False,
            "ot_fold_n3": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n3_image": "LEMMA",
            "n3_rem": "LEMMA",
            "n7_clip_fold": "LEMMA",
            "even_parent_rem": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "covering_n3": "CERTIFIED",
            "dmin_tail": "KILLED",
            "ot_fold_n3": "KILLED",
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
    print("fire_map n_ok", dump["fire_map"]["n_ok"])
    print("n3_any_j n_ok", dump["n3_any_j"]["n_ok"], "n_one", dump["n3_any_j"]["n_one"])
    print("covering_n3", dump["covering_n3"]["rows"])
    print("killed_dmin", dump["killed_dmin"])
    print("killed_ot_fold", dump["killed_ot_fold"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
