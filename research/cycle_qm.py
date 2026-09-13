#!/usr/bin/env python3
"""Cycle QM: covering leftover even-j Green xor on n%4==0 is 1 iff k in {0,1,3,5}.

For k>=2, G(4t, even j) vanishes unless j%4==0, and G(4t, 4r)=G(t,r)
maps the covering n%4==0 window onto the parent covering window at
k-2, so all even-j n%4==0 tot is A(k-2). Cycle PC p=4 even n is
3U-2, which is 2 mod 4, so forced even-j n%4==0 tot vanishes.
UNIQUE_EVEN p%8==0 columns 16,32,72,88 double to Green p=4,8,18,22
at k-2 (n0 xor 1 iff k>=2, k>=4, k>=5, k>=6), so unique even n%4==0
tot is 1 iff k in {2,3,5}. Leftover n%4==0 tot is A(k-2) xor that
bit. Cycle QL leftover even-j even-n tot xor this bit is leftover
even-j on n%4==2, which is 1 iff k in {1,2,3,4}. Not rest=S xor T
(k=3: leftover n%4==0 is 1, rest=0; k=6: 0 vs 1). Not leftover
n%4==0 tot equals leftover even-j even-n tot. Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qm.py --certify
Dump: research/cycle_qm.json
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
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import in_p4, live_lo, want_p4_xor
from cycle_pt import want_p18_gxor
from cycle_qa import want_p22_gxor
from cycle_qh import want_clip_g1
from cycle_qj import UNIQUE_EVEN
from cycle_qk import want_p8_gxor
from cycle_ql import want_lo_ee

OUT = Path(__file__).resolve().with_suffix(".json")
QL_JSON = Path(__file__).resolve().parent / "cycle_ql.json"
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_G = 12
K_ALG = 64
# Child p%8==0 unique-even, parent p/4 at k-2.
PAIRS = (
    (16, 4),
    (32, 8),
    (72, 18),
    (88, 22),
)


def want_lo_n0(k: int) -> int:
    """Covering leftover even-j Green xor on n%4==0, all k."""
    return int(k in (0, 1, 3, 5))


def want_lo_n2(k: int) -> int:
    """Covering leftover even-j Green xor on n%4==2, all k."""
    return int(k in (1, 2, 3, 4))


def want_u_n0(k: int) -> int:
    """UNIQUE_EVEN Green xor on n%4==0, all k: 1 iff k in {2,3,5}."""
    return int(k in (2, 3, 5))


def want_parent_n0(p: int, k: int) -> int:
    """Closed Green xor at a 4-fold n%4==0 parent packed index."""
    if p == 4:
        return want_p4_xor(k)
    if p == 8:
        return want_p8_gxor(k)
    if p == 18:
        return want_p18_gxor(k)
    if p == 22:
        return want_p22_gxor(k)
    raise ValueError(p)


def gxor_n0(p: int, k: int) -> int:
    """Covering Green xor at packed p on n%4==0."""
    U = 1 << k
    delta = p // 2
    j = 5 * U - delta
    if j < 0:
        return 0
    acc = 0
    n0 = live_lo(k, delta)
    n0 = n0 + ((-n0) % 4)
    for n in range(n0, 4 * U, 4):
        if 0 <= j <= 2 * n:
            acc ^= G(n, j)
    return acc


def leftover_nmod(k: int) -> dict:
    """Walk covering even-j G=1 xor split leftover/unique/forced by n%4."""
    U = 1 << k
    t_pack = 10 * U
    clip = 5 * U
    lo = [0, 0, 0, 0]
    u = [0, 0, 0, 0]
    f = [0, 0, 0, 0]
    all_e = [0, 0, 0, 0]
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        nm = n % 4
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            p = t_pack - 2 * j
            if p < 0:
                continue
            all_e[nm] ^= 1
            if p in FORCED:
                f[nm] ^= 1
            elif p in UNIQUE_REST:
                u[nm] ^= 1
            else:
                lo[nm] ^= 1
    return {"lo": lo, "u": u, "f": f, "all_e": all_e}


def lo_n0_walk() -> dict:
    """k<=K_CHK: leftover n%4==0/2 match want_*; doubling vs A(k-2)."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = leftover_nmod(k)
        lo0, lo2 = w["lo"][0], w["lo"][2]
        if lo0 != want_lo_n0(k) or lo2 != want_lo_n2(k):
            return {
                "ok": False,
                "lo": True,
                "k": k,
                "lo0": lo0,
                "lo2": lo2,
            }
        if (lo0 ^ lo2) != want_lo_ee(k):
            return {"ok": False, "ql": True, "k": k}
        if w["u"][0] != want_u_n0(k):
            return {"ok": False, "u": True, "k": k, "u0": w["u"][0]}
        if k >= 2:
            if w["all_e"][0] != want_clip_g1(k - 2):
                return {"ok": False, "A": True, "k": k, "all0": w["all_e"][0]}
            if w["f"][0] != 0:
                return {"ok": False, "f": True, "k": k}
            alg = want_clip_g1(k - 2) ^ want_u_n0(k)
            if lo0 != alg:
                return {"ok": False, "alg": True, "k": k, "got": lo0}
            U = 1 << k
            ev = [n for n in range(0, 4 * U, 2) if in_p4(n, k)]
            if ev != [3 * U - 2] or (3 * U - 2) % 4 != 2:
                return {"ok": False, "p4": True, "k": k, "ev": ev}
            n_ok += 1
        rows[str(k)] = {
            "lo0": lo0,
            "lo2": lo2,
            "u0": w["u"][0],
            "u2": w["u"][2],
            "f0": w["f"][0],
            "all0": w["all_e"][0],
        }
    ok = (
        rows["0"]["lo0"] == 1
        and rows["1"]["lo0"] == 1
        and rows["2"]["lo0"] == 0
        and rows["3"]["lo0"] == 1
        and rows["5"]["lo0"] == 1
        and rows["6"]["lo0"] == 0
        and rows["8"]["lo0"] == 0
        and rows["2"]["lo2"] == 1
        and rows["4"]["lo2"] == 1
        and rows["5"]["lo2"] == 0
        and rows["8"]["lo2"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def unique_n0() -> dict:
    """k<=K_G: UNIQUE_EVEN n%4==0 xor matches 4-fold parents; tot want_u_n0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        tot = 0
        per = {}
        for child, par in PAIRS:
            got = gxor_n0(child, k)
            want = want_parent_n0(par, k - 2) if k >= 2 else 0
            if k >= 2 and got != want:
                return {
                    "ok": False,
                    "walk": True,
                    "k": k,
                    "child": child,
                    "got": got,
                    "want": want,
                }
            tot ^= got
            per[str(child)] = got
            n_ok += 1
        # p%8==4 unique even cannot fire on n%4==0 for k>=2
        if k >= 2:
            for p in UNIQUE_EVEN:
                if p % 8 == 4 and gxor_n0(p, k) != 0:
                    return {"ok": False, "mod4": True, "p": p, "k": k}
        if tot != want_u_n0(k):
            return {"ok": False, "tot": True, "k": k, "tot": tot}
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"tot": tot, "per": per}
    ok = (
        rows["2"]["per"]["16"] == 1
        and rows["4"]["per"]["32"] == 1
        and rows["5"]["per"]["72"] == 1
        and rows["6"]["per"]["88"] == 1
        and rows["5"]["tot"] == 1
        and rows["6"]["tot"] == 0
        and rows["12"]["tot"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: closed leftover n0/n2 and unique n0 vs 4-fold parents."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_lo_n0(k) != (want_lo_ee(k) ^ want_lo_n2(k)):
            return {"ok": False, "xor": True, "k": k}
        if k >= 2:
            alg = want_clip_g1(k - 2) ^ want_u_n0(k)
            if want_lo_n0(k) != alg:
                return {"ok": False, "alg": True, "k": k, "alg": alg}
            acc = 0
            for child, par in PAIRS:
                bit = want_parent_n0(par, k - 2)
                acc ^= bit
            if acc != want_u_n0(k):
                return {"ok": False, "u": True, "k": k, "acc": acc}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_n0(0) == 1
        and want_lo_n0(1) == 1
        and want_lo_n0(3) == 1
        and want_lo_n0(5) == 1
        and want_lo_n0(6) == 0
        and want_lo_n2(4) == 1
        and want_lo_n2(5) == 0
        and want_u_n0(2) == 1
        and want_u_n0(4) == 0
        and want_u_n0(5) == 1
        and want_p4_xor(0) == 1
        and want_p8_gxor(2) == 1
        and want_p18_gxor(3) == 1
        and want_p22_gxor(4) == 1
        and want_clip_g1(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_n0_eq_st() -> dict:
    """Leftover even-j n%4==0 tot equals ST / leftover even-n tot."""
    ok = (
        want_lo_n0(3) == 1
        and want_rest_e0(3) == 0
        and want_rest10(3, 10) == 0
        and want_lo_n0(6) == 0
        and want_rest_e0(6) == 1
        and want_lo_n0(2) == 0
        and want_lo_ee(2) == 1
        and want_lo_n2(2) == 1
    )
    return {"ok": ok, "k3": 1, "ST3": 0, "k6": 0, "ST6": 1}


def prefixes() -> dict:
    ql = json.loads(QL_JSON.read_text())
    qh = json.loads(QH_JSON.read_text())
    ok = (
        ql["checks"]["all_ok"]
        and qh["checks"]["all_ok"]
        and ql["verdict"]["lo_ee_iff_k_in_0_2_4_5"] == "LEMMA"
        and qh["verdict"]["clip_g1_0_k_ge_1"] == "LEMMA"
        and ql["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ql["verdict"]["prize"] == "unsolved"
        and want_lo_ee(2) == 1
        and want_clip_g1(0) == 1
        and want_clip_g1(2) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, lo, uniq, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and lo["ok"] and uniq["ok"]
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
    lo = lo_n0_walk()
    uniq = unique_n0()
    tot = tot_form()
    kl = killed_n0_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, lo, uniq, tot, kl, sc, pref)
    dump = {
        "cycle": "QM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "lo_n0_walk": {k: lo[k] for k in lo if k != "ok"},
        "unique_n0": {k: uniq[k] for k in uniq if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_n0_iff_k_in_0_1_3_5": True,
            "lo_n2_iff_k_in_1_2_3_4": True,
            "u_n0_iff_k_in_2_3_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "lo_n0_eq_ST": False,
            "lo_n0_eq_lo_ee": False,
            "prize": False,
        },
        "verdict": {
            "lo_n0_iff_k_in_0_1_3_5": "LEMMA",
            "lo_n2_iff_k_in_1_2_3_4": "LEMMA",
            "u_n0_iff_k_in_2_3_5": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "lo_n0_eq_ST": "KILLED",
            "lo_n0_eq_lo_ee": "KILLED",
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
        "lo_n0_walk n_ok",
        dump["lo_n0_walk"]["n_ok"],
        "k_hi",
        dump["lo_n0_walk"]["k_hi"],
        "lo0_8",
        dump["lo_n0_walk"]["rows"]["8"]["lo0"],
        "lo2_8",
        dump["lo_n0_walk"]["rows"]["8"]["lo2"],
    )
    print("unique_n0 n_ok", dump["unique_n0"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
