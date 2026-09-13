#!/usr/bin/env python3
"""Cycle OT: clip-removed S(8t+7) at 5*2^k equals rem(2t+1) at 5*2^{k-2}.

Unclipped pal-right S folds S(4s+3)=S(s) for odd s (Cycle ON), so
S(8t+7)=S(2t+1). The same two doublings map clip j>5*2^k on n=8t+7
to clip j>5*2^{k-2} on s=2t+1. Hence clip-removed S folds on
covering-shaped clip lines. When t is even, s=4p+1 and Cycle OS
evaluates the parent rem as an R2 tail. Not the fold for n=8t+3
(even s: n=51, jmax=80 rem=1, R2-tail=0). Not one doubling
(n=11, jmax=10). Not arbitrary jmax (jmax=44). Not covering S
for all k. Not E_k=0 for all k. Do not catalogue further S/T
subregions unless the experiment answers why E_k=0. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ot.py --certify
Dump: research/cycle_ot.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_oq import pal_right_s_pc
from cycle_os import even_parent_rem, removed_s

OUT = Path(__file__).resolve().with_suffix(".json")
OS_JSON = Path(__file__).resolve().parent / "cycle_os.json"
OR_JSON = Path(__file__).resolve().parent / "cycle_or.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
T_HI = 40
K_HI = 8
K_COVER = 8


def n7_rem_fold(t: int, k: int) -> int:
    """Clip-removed S(8t+7) at 5*2^k from parent rem at 5*2^{k-2}."""
    return removed_s(2 * t + 1, 5 << (k - 2))


def n7_fold() -> dict:
    """t<T_HI, k=2..K_HI: rem(8t+7, 5*2^k)==rem(2t+1, 5*2^{k-2}) when clipped."""
    n_ok = n_one = n_skip = 0
    sample = {}
    for t in range(0, T_HI):
        n = 8 * t + 7
        s = 2 * t + 1
        for k in range(2, K_HI + 1):
            jmax = 5 << k
            if 2 * n <= jmax:
                n_skip += 1
                continue
            got = removed_s(n, jmax)
            want = n7_rem_fold(t, k)
            if got != want or want != removed_s(s, 5 << (k - 2)):
                return {"ok": False, "t": t, "k": k, "got": got, "want": want}
            n_ok += 1
            n_one += got
        if t <= 4:
            sample[str(t)] = {
                "n": n,
                "unclip": pal_right_s_pc(n),
                "un_s": pal_right_s_pc(s),
            }
    ok = (
        n_ok > 0
        and n_one > 0
        and sample["0"]["unclip"] == sample["0"]["un_s"]
        and sample["1"]["unclip"] == sample["1"]["un_s"]
        and sample["0"]["unclip"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_one": n_one,
        "n_skip": n_skip,
        "t_hi": T_HI,
        "sample": sample,
    }


def n7_even_t_os() -> dict:
    """Even t: rem(8t+7, 5*2^k)==even_parent_rem(2t+1, 5*2^{k-2})."""
    n_ok = n_one = 0
    sample = {}
    for t in range(0, T_HI, 2):
        n = 8 * t + 7
        s = 2 * t + 1
        for k in range(2, K_HI + 1):
            jmax = 5 << k
            if 2 * n <= jmax:
                continue
            got = removed_s(n, jmax)
            want = even_parent_rem(s, 5 << (k - 2))
            if got != want or s % 4 != 1:
                return {"ok": False, "t": t, "k": k, "got": got, "want": want}
            n_ok += 1
            n_one += got
        if t <= 4:
            sample[str(t)] = {"n": n, "s": s, "s_mod4": s % 4}
    ok = n_ok > 0 and sample["0"]["s_mod4"] == 1 and sample["2"]["s_mod4"] == 1
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "sample": sample}


def covering_n7() -> dict:
    """q=10 k<=K_COVER: covering n=8t+7 rem equals the fold."""
    rows = {}
    n_ok = 0
    for k in range(2, K_COVER + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        jmax = T // 2
        xor_rem = 0
        n_n7 = 0
        tclk = 0
        sclk = t0 + 1
        while sclk < T:
            n = odd_clock(tclk, U, Q)
            if n % 8 == 7:
                got = removed_s(n, jmax)
                tt = (n - 7) // 8
                want = n7_rem_fold(tt, k)
                if got != want:
                    return {"ok": False, "k": k, "n": n, "got": got, "want": want}
                xor_rem ^= got
                n_n7 += 1
                n_ok += 1
            tclk += 1
            sclk += 2
        rows[str(k)] = {"xor_rem": xor_rem, "n_n7": n_n7}
    ok = (
        rows["2"]["n_n7"] > 0
        and rows["6"]["xor_rem"] == 0
        and rows["8"]["xor_rem"] == 0
        and n_ok > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": rows}


def killed_even_s() -> dict:
    """n=51=8*6+3, jmax=80: rem=1, not an 8t+7 fold."""
    n, jmax = 51, 80
    rem = removed_s(n, jmax)
    ok = n % 8 == 3 and rem == 1
    return {"ok": ok, "n": n, "jmax": jmax, "rem": rem, "unclip": pal_right_s_pc(n)}


def killed_one_step() -> dict:
    """n=11, jmax=10: rem(2m+1,5*2^1) != rem(m,5)."""
    n, m, jmax = 11, 5, 10
    got = removed_s(n, jmax)
    want = removed_s(m, 5)
    ok = got != want
    return {"ok": ok, "n": n, "m": m, "got": got, "want": want}


def killed_jmax44() -> dict:
    """n=23, jmax=44: rem != rem(s,11)."""
    n, s, jmax = 23, 5, 44
    got = removed_s(n, jmax)
    want = removed_s(s, 11)
    ok = got != want and n == 4 * s + 3
    return {"ok": ok, "n": n, "s": s, "got": got, "want": want}


def prefixes() -> dict:
    osj = json.loads(OS_JSON.read_text())
    orj = json.loads(OR_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        osj["checks"]["all_ok"]
        and orj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and osj["verdict"]["even_parent_rem"] == "LEMMA"
        and orj["verdict"]["unclip_cover"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and osj["verdict"]["covering_S"] == "PREFIX"
        and osj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, fold, ev, cover, ke, ko, kj, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and fold["ok"]
        and ev["ok"]
        and cover["ok"]
        and ke["ok"]
        and ko["ok"]
        and kj["ok"]
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
    fold = n7_fold()
    ev = n7_even_t_os()
    cover = covering_n7()
    ke = killed_even_s()
    ko = killed_one_step()
    kj = killed_jmax44()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, fold, ev, cover, ke, ko, kj, sc, pref)
    dump = {
        "cycle": "OT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "n7_fold": {k: fold[k] for k in fold if k != "ok"},
        "n7_even_t_os": {k: ev[k] for k in ev if k != "ok"},
        "covering_n7": {k: cover[k] for k in cover if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_even_s": {k: ke[k] for k in ke if k != "ok"},
        "killed_one_step": {k: ko[k] for k in ko if k != "ok"},
        "killed_jmax44": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "n7_clip_fold": True,
            "n7_even_t_os": True,
            "even_parent_rem": True,
            "unclip_cover": True,
            "even_s": False,
            "one_step": False,
            "jmax44": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n7_clip_fold": "LEMMA",
            "n7_even_t_os": "LEMMA",
            "even_parent_rem": "LEMMA",
            "unclip_cover": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "covering_n7": "CERTIFIED",
            "even_s": "KILLED",
            "one_step": "KILLED",
            "jmax44": "KILLED",
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
    print("n7_fold n_ok", dump["n7_fold"]["n_ok"], "n_one", dump["n7_fold"]["n_one"])
    print("n7_even_t_os n_ok", dump["n7_even_t_os"]["n_ok"])
    print("covering_n7", dump["covering_n7"]["rows"])
    print("killed_even_s", dump["killed_even_s"])
    print("killed_one_step", dump["killed_one_step"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
