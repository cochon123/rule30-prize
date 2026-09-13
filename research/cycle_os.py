#!/usr/bin/env python3
"""Cycle OS: even-parent clip-removed pal-right S is the R2 tail of p.

For even m=2p, unclipped S(2m+1) is R2(p) (Cycle OP). Green even-first
argument halves: G(2p,2e)=G(p,e) and odd offsets vanish. Clip-removed
S of n=2m+1 at any jmax is therefore the residue-2 xor of G(p,p+d)
over those d with 2(p+d)>jmax/2. Covering q=10 uses jmax=5U, so
dmin=5U/4-p+1 on n=4p+1 in the clip window. Not the odd-parent
clip-removed xor (n=51, jmax=80: rem=1, R2-tail=0). Not covering S
for all k. Not E_k=0 for all k. Do not catalogue further S/T
subregions unless the experiment answers why E_k=0. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_os.py --certify
Dump: research/cycle_os.json
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
from cycle_op import pal_right_R
from cycle_oq import pal_right_s_pc
from cycle_or import clipped_s

OUT = Path(__file__).resolve().with_suffix(".json")
OR_JSON = Path(__file__).resolve().parent / "cycle_or.json"
OQ_JSON = Path(__file__).resolve().parent / "cycle_oq.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
P_HI = 40
K_COVER = 8


def r2_tail(p: int, dmin: int) -> int:
    """Xor G(p,p+d) for d%3==2, d>=dmin, 1<=d<=p."""
    acc = 0
    for d in range(max(dmin, 1), p + 1):
        acc ^= G(p, p + d) if d % 3 == 2 else 0
    return acc


def even_parent_dmin(p: int, jmax: int) -> int:
    """First d with 2(p+d) > jmax/2; 1 if the tail is the whole R2."""
    m = 2 * p
    num = jmax // 2 + 1 - m
    if num <= 0:
        return 1
    return (num + 1) // 2


def even_parent_rem(n: int, jmax: int) -> int:
    """Clip-removed pal-right S of n=4p+1."""
    p = (n - 1) // 4
    return r2_tail(p, even_parent_dmin(p, jmax))


def removed_s(n: int, jmax: int) -> int:
    """Pal-right S-xor of G(j+1) on cells with j>jmax."""
    xor_s = 0
    for j in range(max(n + 1, jmax + 1), 2 * n + 1):
        if G(n, j) == 0:
            continue
        if (j - n) % 3 != 1:
            continue
        if G(n, j - 1) != 0:
            continue
        xor_s ^= G(n, j + 1)
    return xor_s


def even_halve() -> dict:
    """p<P_HI: G(2p,2e)==G(p,e); odd offsets of 2p vanish."""
    n_ok = n_odd = 0
    sample = {}
    for p in range(0, P_HI):
        t = 2 * p
        for e in range(0, 2 * p + 1):
            if G(t, 2 * e) != G(p, e):
                return {"ok": False, "p": p, "e": e}
            n_ok += 1
        for d in range(1, t + 1, 2):
            if G(t, t + d) != 0:
                return {"ok": False, "odd": t, "d": d}
            n_odd += 1
        if p <= 4:
            sample[str(p)] = {"G2p_2p": G(t, t), "Gp_p": G(p, p)}
    ok = n_ok > 0 and n_odd > 0 and sample["1"]["G2p_2p"] == 1
    return {"ok": ok, "n_ok": n_ok, "n_odd": n_odd, "sample": sample}


def even_parent_any_j() -> dict:
    """p<P_HI, several jmax: removed_s(4p+1)==even_parent_rem; rem xor clip == unclip."""
    n_ok = n_one = 0
    sample = {}
    for p in range(0, P_HI):
        n = 4 * p + 1
        for jmax in (0, n // 2, n, 2 * n - 1, 2 * n, 2 * n + 5, 5 * n // 2):
            got = removed_s(n, jmax)
            want = even_parent_rem(n, jmax)
            cl = clipped_s(n, jmax)
            un = pal_right_s_pc(n)
            if got != want or (got ^ cl) != un:
                return {
                    "ok": False,
                    "n": n,
                    "jmax": jmax,
                    "got": got,
                    "want": want,
                    "cl": cl,
                    "un": un,
                }
            n_ok += 1
            n_one += got
        if p <= 3:
            sample[str(n)] = {
                "full": pal_right_R(p)[2],
                "unclip": pal_right_s_pc(n),
            }
    ok = (
        n_ok == P_HI * 7
        and sample["1"]["unclip"] == 0
        and sample["5"]["unclip"] == pal_right_R(1)[2]
        and n_one > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_one": n_one, "p_hi": P_HI, "sample": sample}


def covering_even_parent() -> dict:
    """q=10 k<=K_COVER: even-parent clip-removed == R2 tail."""
    rows = {}
    n_ok = 0
    xor_all = 0
    for k in range(0, K_COVER + 1):
        U = 1 << k
        T, t0, Q = 10 * U, 2 * U, covering_Q(10)
        jmax = T // 2
        xor_rem = 0
        n_ep = 0
        t = 0
        s = t0 + 1
        while s < T:
            n = odd_clock(t, U, Q)
            if n % 4 == 1:
                got = removed_s(n, jmax)
                want = even_parent_rem(n, jmax)
                if got != want:
                    return {"ok": False, "k": k, "n": n, "got": got, "want": want}
                xor_rem ^= got
                n_ep += 1
                n_ok += 1
            t += 1
            s += 2
        rows[str(k)] = {"xor_rem": xor_rem, "n_ep": n_ep}
        xor_all ^= xor_rem
    ok = (
        rows["0"]["xor_rem"] == 0
        and rows["6"]["xor_rem"] == 1
        and rows["8"]["xor_rem"] == 0
        and n_ok > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "xor_all": xor_all, "rows": rows}


def killed_odd_parent() -> dict:
    """n=51 jmax=80: rem=1, R2-tail of floor((n-1)/4)=0."""
    n, jmax = 51, 80
    rem = removed_s(n, jmax)
    p = (n - 1) // 4
    wrong = r2_tail(p, even_parent_dmin(p, jmax))
    ok = n % 4 == 3 and rem == 1 and wrong == 0
    return {"ok": ok, "n": n, "jmax": jmax, "rem": rem, "r2_tail": wrong, "p": p}


def killed_full_r2(anyj: dict) -> dict:
    """First covering even-parent at k=6 has empty R2 tail, not full R2."""
    U = 64
    cut = (5 * U) // 2
    n0 = cut + 1
    p = (n0 - 1) // 4
    rem0 = even_parent_rem(n0, 5 * U)
    full = pal_right_R(p)[2]
    ok = n0 % 4 == 1 and rem0 == 0 and anyj["n_one"] > 0
    return {"ok": ok, "n0": n0, "p": p, "rem0": rem0, "full": full}


def prefixes() -> dict:
    orj = json.loads(OR_JSON.read_text())
    oq = json.loads(OQ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        orj["checks"]["all_ok"]
        and oq["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and orj["verdict"]["P_pow2"] == "LEMMA"
        and orj["verdict"]["unclip_cover"] == "LEMMA"
        and orj["verdict"]["hi_unclip"] == "LEMMA"
        and oq["verdict"]["s_pc"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and orj["verdict"]["covering_S"] == "PREFIX"
        and orj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, half, anyj, cover, ko, kf, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and half["ok"]
        and anyj["ok"]
        and cover["ok"]
        and ko["ok"]
        and kf["ok"]
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
    half = even_halve()
    anyj = even_parent_any_j()
    cover = covering_even_parent()
    ko = killed_odd_parent()
    kf = killed_full_r2(anyj)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, half, anyj, cover, ko, kf, sc, pref)
    dump = {
        "cycle": "OS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_halve": {k: half[k] for k in half if k != "ok"},
        "even_parent_any_j": {k: anyj[k] for k in anyj if k != "ok"},
        "covering_even_parent": {k: cover[k] for k in cover if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_odd_parent": {k: ko[k] for k in ko if k != "ok"},
        "killed_full_r2": {k: kf[k] for k in kf if k != "ok"},
        "lemmas": {
            "even_halve": True,
            "even_parent_rem": True,
            "P_pow2": True,
            "unclip_cover": True,
            "hi_unclip": True,
            "s_pc": True,
            "E_q10_10": True,
            "odd_parent_rem": False,
            "full_r2": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_halve": "LEMMA",
            "even_parent_rem": "LEMMA",
            "P_pow2": "LEMMA",
            "unclip_cover": "LEMMA",
            "hi_unclip": "LEMMA",
            "s_pc": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "covering_even_parent": "CERTIFIED",
            "odd_parent_rem": "KILLED",
            "full_r2": "KILLED",
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
    print("even_halve n_ok", dump["even_halve"]["n_ok"])
    print("even_parent_any_j n_ok", dump["even_parent_any_j"]["n_ok"], "n_one", dump["even_parent_any_j"]["n_one"])
    print("covering_even_parent", dump["covering_even_parent"]["rows"])
    print("killed_odd_parent", dump["killed_odd_parent"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
