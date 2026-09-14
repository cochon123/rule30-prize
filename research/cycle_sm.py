#!/usr/bin/env python3
"""Cycle SM: odd-child even-j clip equals parent p=0; SI n3e rest all k.

For k>=1 and n=2m+1, G(2m+1, 2r)=G(m,r) xor G(m,r-1). Even-j clipped
G=1 xor telescopes to G(m, min(2m+1, 5*2^{k-1})), which is G(m,
5*2^{k-1}) (0 off the parent live window). So n%4==3 even-j clip
equals parent odd p=0 and n%4==1 equals parent even p=0. Cycle SL
makes those 1 iff k==1 / k>=2. Cycle SK forced n3 even-j is 1 iff
k>=1, so Green rest n3e is 1 iff k!=1 for all k; n1e is 1 iff k<=1.
Not packed rest. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_sm.py --certify
Dump: research/cycle_sm.json
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
from cycle_qv import even_slots
from cycle_si import want_g_n1e, want_g_n1o, want_g_n3e, want_g_n3o
from cycle_sj import p0_par, want_g1_n1e, want_g1_n3e, want_p0_even, want_p0_odd
from cycle_sk import want_f_n1e, want_f_n3e
from cycle_qx import want_g_n1, want_g_n3

OUT = Path(__file__).resolve().with_suffix(".json")
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
QI_JSON = Path(__file__).resolve().parent / "cycle_qi.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
SI_JSON = Path(__file__).resolve().parent / "cycle_si.json"
SJ_JSON = Path(__file__).resolve().parent / "cycle_sj.json"
SK_JSON = Path(__file__).resolve().parent / "cycle_sk.json"
SL_JSON = Path(__file__).resolve().parent / "cycle_sl.json"

N_PAL = 64
M_SLOTS = 64
K_TEL = 8
K_FOLD = 12
K_ALG = 64


def evenj_clip(n: int, k: int) -> int:
    """Xor of G(n,j) on even j, 0<=j<=min(2n, 5*2^k)."""
    hi = min(2 * n, 5 << k)
    acc = 0
    for j in range(0, hi + 1, 2):
        acc ^= G(n, j)
    return acc


def tel_pred(n: int, k: int) -> int:
    """G(m, min(2m+1, 5*2^{k-1})) for odd n=2m+1, k>=1."""
    m = n // 2
    hi = min(2 * m + 1, 5 << (k - 1))
    if hi < 0 or hi > 2 * m:
        return 0
    return G(m, hi)


def parent_p0(m: int, k: int) -> int:
    """G(m, 5*2^{k-1}) with the usual out-of-range 0, k>=1."""
    j = 5 << (k - 1)
    if j < 0 or j > 2 * m:
        return 0
    return G(m, j)


def tel_cell() -> dict:
    """1<=k<=8: odd-n even-j clip equals tel_pred equals parent p=0."""
    n_ok = 0
    rows = {}
    for k in range(1, K_TEL + 1):
        U = 1 << k
        n_odd = 0
        for n in range(1, 4 * U, 2):
            got = evenj_clip(n, k)
            pred = tel_pred(n, k)
            p0 = parent_p0(n // 2, k)
            if got != pred or pred != p0:
                return {
                    "ok": False,
                    "k": k,
                    "n": n,
                    "got": got,
                    "pred": pred,
                    "p0": p0,
                }
            n_odd += 1
            n_ok += 1
        rows[str(k)] = {"n_odd": n_odd}
    ok = (
        n_ok > 0
        and rows["1"]["n_odd"] == 4
        and rows["8"]["n_odd"] == 512
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_TEL, "rows": rows}


def k0_four() -> dict:
    """k=0 covering n=0..3 even-j clip: n1e=0, n3e=1."""
    bits = [evenj_clip(n, 0) for n in range(0, 4)]
    n1e = bits[1]
    n3e = bits[3]
    ok = (
        bits == [1, 0, 1, 1]
        and n1e == want_g1_n1e(0)
        and n3e == want_g1_n3e(0)
        and (n1e ^ want_f_n1e(0)) == want_g_n1e(0)
        and (n3e ^ want_f_n3e(0)) == want_g_n3e(0)
    )
    return {"ok": ok, "bits": bits, "n1e": n1e, "n3e": n3e}


def fold_tot() -> dict:
    """1<=k<=12: n3e clip helper is parent odd p=0; n1e is parent even."""
    n_ok = 0
    rows = {}
    for k in range(1, K_FOLD + 1):
        w = p0_par(k - 1)
        if want_g1_n3e(k) != want_p0_odd(k - 1) or want_g1_n3e(k) != w["o"]:
            return {"ok": False, "n3e": True, "k": k, "w": w}
        if want_g1_n1e(k) != want_p0_even(k - 1) or want_g1_n1e(k) != w["e"]:
            return {"ok": False, "n1e": True, "k": k, "w": w}
        if (want_g1_n3e(k) ^ want_f_n3e(k)) != want_g_n3e(k):
            return {"ok": False, "rest_n3e": True, "k": k}
        if (want_g1_n1e(k) ^ want_f_n1e(k)) != want_g_n1e(k):
            return {"ok": False, "rest_n1e": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"n1e": w["e"], "n3e": w["o"]}
    ok = (
        n_ok == K_FOLD
        and rows["1"]["n3e"] == 1
        and rows["2"]["n3e"] == 0
        and rows["12"]["n3e"] == 0
        and rows["1"]["n1e"] == 0
        and rows["2"]["n1e"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_FOLD, "rows": rows}


def tot_form() -> dict:
    """k<=64: SI even-j rest helpers are g1 xor forced; n3o from QY tot."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if k >= 1 and want_g1_n3e(k) != want_p0_odd(k - 1):
            return {"ok": False, "fold3": True, "k": k}
        if k >= 1 and want_g1_n1e(k) != want_p0_even(k - 1):
            return {"ok": False, "fold1": True, "k": k}
        if (want_g1_n3e(k) ^ want_f_n3e(k)) != want_g_n3e(k):
            return {"ok": False, "n3e": True, "k": k}
        if (want_g1_n1e(k) ^ want_f_n1e(k)) != want_g_n1e(k):
            return {"ok": False, "n1e": True, "k": k}
        if (want_g_n3e(k) ^ want_g_n3o(k)) != want_g_n3(k):
            return {"ok": False, "n3tot": True, "k": k}
        if (want_g_n1e(k) ^ want_g_n1o(k)) != want_g_n1(k):
            return {"ok": False, "n1tot": True, "k": k}
        if k >= 1 and ((5 << k) % 2) != 0:
            return {"ok": False, "clip_even": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_g_n3e(0) == 1
        and want_g_n3e(1) == 0
        and want_g_n3e(2) == 1
        and want_g_n1e(0) == 1
        and want_g_n1e(2) == 0
        and want_g_n3o(1) == 1
        and want_g_n3o(2) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Clip equals rest; n3e identically 1; Green n0 tot equals n3e rest."""
    ok = (
        want_g1_n3e(1) != want_g_n3e(1)
        and want_g_n3e(1) == 0
        and want_g_n3e(0) == 1
        and want_g_n3e(2) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    qh = json.loads(QH_JSON.read_text())
    qi = json.loads(QI_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    si = json.loads(SI_JSON.read_text())
    sj = json.loads(SJ_JSON.read_text())
    sk = json.loads(SK_JSON.read_text())
    sl = json.loads(SL_JSON.read_text())
    ok = (
        qh["checks"]["all_ok"]
        and qi["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and si["checks"]["all_ok"]
        and sj["checks"]["all_ok"]
        and sk["checks"]["all_ok"]
        and sl["checks"]["all_ok"]
        and qh["verdict"]["clip_g1_0_k_ge_1"] == "LEMMA"
        and qi["verdict"]["p0_gxor_1_all_k"] == "LEMMA"
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and sl["verdict"]["p0_odd_iff_k_eq_0_all_k"] == "LEMMA"
        and sk["verdict"]["f_n3e_iff_k_ge_1"] == "LEMMA"
        and sk["verdict"]["f_n1e_all_k"] == "LEMMA"
        and si["verdict"]["green_n3e_iff_k_ne_1_k_le_10"] == "CERTIFIED"
        and sl["verdict"]["si_rest_n3e_all_k"] == "PREFIX"
        and sl["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sl["verdict"]["prize"] == "unsolved"
        and want_g_n3e(1) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tel, k0, fold, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tel["ok"] and k0["ok"] and fold["ok"] and tot["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    tel = tel_cell()
    k0 = k0_four()
    fold = fold_tot()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tel, k0, fold, tot, kl, sc, pref)
    dump = {
        "cycle": "SM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tel_cell": {k: tel[k] for k in tel if k != "ok"},
        "k0_four": {k: k0[k] for k in k0 if k != "ok"},
        "fold_tot": {k: fold[k] for k in fold if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_child_evenj_eq_parent_p0": True,
            "g1_n3e_iff_k_le_1_all_k": True,
            "green_n3e_iff_k_ne_1_all_k": True,
            "green_n1e_iff_k_le_1_all_k": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_child_evenj_eq_parent_p0": "LEMMA",
            "g1_n3e_iff_k_le_1_all_k": "LEMMA",
            "green_n3e_iff_k_ne_1_all_k": "LEMMA",
            "green_n1e_iff_k_le_1_all_k": "LEMMA",
            "green_n3o_iff_k_eq_1_all_k": "LEMMA",
            "tel_k_le_8": "CERTIFIED",
            "g1_eq_rest_n3e": "KILLED",
            "n3e_identically_1": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
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
    print(
        "tel n_ok",
        dump["tel_cell"]["n_ok"],
        "k0 n3e",
        dump["k0_four"]["n3e"],
        "fold n_ok",
        dump["fold_tot"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
