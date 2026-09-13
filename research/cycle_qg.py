#!/usr/bin/env python3
"""Cycle QG: covering Green UNIQUE_REST xor tot is 1 iff k in {3,4,5}.

Each unique packed p doubles to a known Green parent: if p%4==2
then odd j, even n vanish, and odd n map onto parent (p+2)/2 at
k-1; if p%4==0 then even-n xor parent p/2 cancels the odd-n p/2
piece and tot is parent p/2+2 at k-1. Live windows match for k>=3.
Parents reduce to Cycles PM/PN/PC/PV/PT/PY/QA/QC/QD/QE (p=10..30).
Hence Green xor at every UNIQUE_REST column is 1 for k>=6 (16 ones,
tot 0), and tot is 1 iff k in {3,4,5}. Dual of Cycle QF's packed
unique tot=0 (packed is 0 at k=3,4,5; Green is 1). Not rest=S xor T.
Not E_k=0 for all k. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qg.py --certify
Dump: research/cycle_qg.json
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
from cycle_md import UNIQUE_REST
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import live_lo, want_p14_gxor
from cycle_pm import want_p10_gxor
from cycle_pn import want_p12_gxor
from cycle_pt import want_p18_gxor
from cycle_pv import want_p16_gxor
from cycle_py import want_p20_gxor
from cycle_qa import want_p22_gxor, want_p24_gxor
from cycle_qc import want_p26_gxor
from cycle_qd import want_p28_gxor
from cycle_qe import want_p30_gxor
from cycle_qf import want_unique_tot

OUT = Path(__file__).resolve().with_suffix(".json")
QF_JSON = Path(__file__).resolve().parent / "cycle_qf.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_WIN = 64
K_ALG = 64
PS = tuple(sorted(UNIQUE_REST))
EXTRAS = (40, 44, 46, 50)
KNOWN_GXOR = {
    10: want_p10_gxor,
    12: want_p12_gxor,
    14: want_p14_gxor,
    16: want_p16_gxor,
    18: want_p18_gxor,
    20: want_p20_gxor,
    22: want_p22_gxor,
    24: want_p24_gxor,
    26: want_p26_gxor,
    28: want_p28_gxor,
    30: want_p30_gxor,
}


def parent_p(p: int) -> int:
    """Green doubling parent packed index."""
    if p % 4 == 0:
        return p // 2 + 2
    return (p + 2) // 2


def want_col_gxor(p: int, k: int) -> int:
    """Covering Green G=1 xor at packed p, via known bases and doubling."""
    if k < 0:
        return 0
    if p in KNOWN_GXOR:
        return KNOWN_GXOR[p](k)
    if k < 3:
        return 0
    return want_col_gxor(parent_p(p), k - 1)


def want_unique_gxor_tot(k: int) -> int:
    """XOR of Green G=1 xor over UNIQUE_REST, all k."""
    acc = 0
    for p in PS:
        acc ^= want_col_gxor(p, k)
    return acc


def want_unique_gxor_tot_closed(k: int) -> int:
    """Closed form: 1 iff k in {3,4,5}."""
    return int(k in (3, 4, 5))


def gxor_p(p: int, k: int) -> int:
    """Covering xor of G(n, 5*2^k - p/2) on the live window."""
    U = 1 << k
    delta = p // 2
    j = 5 * U - delta
    if j < 0:
        return 0
    acc = 0
    for n in range(live_lo(k, delta), 4 * U):
        if 0 <= j <= 2 * n:
            acc ^= G(n, j)
    return acc


def odd_m_range(p: int, k: int) -> tuple[int, int]:
    """m-window for odd covering n=2m+1 at child p."""
    U = 1 << k
    lo = live_lo(k, p // 2)
    n0 = lo if lo % 2 else lo + 1
    return (n0 - 1) // 2, 2 * U


def even_m_range(p: int, k: int) -> tuple[int, int]:
    """m-window for even covering n=2m at child p."""
    U = 1 << k
    lo = live_lo(k, p // 2)
    n0 = lo if lo % 2 == 0 else lo + 1
    return n0 // 2, 2 * U


def parent_range(p_par: int, k_par: int) -> tuple[int, int]:
    U = 1 << k_par
    return live_lo(k_par, p_par // 2), 4 * U


def windows_ok() -> dict:
    """k>=3: unique and extra parents have matching doubling windows."""
    n_ok = 0
    cols = tuple(sorted(set(PS) | set(EXTRAS)))
    for k in range(3, K_WIN + 1):
        for p in cols:
            par = parent_p(p)
            pr = parent_range(par, k - 1)
            if p % 4 == 2:
                if odd_m_range(p, k) != pr:
                    return {"ok": False, "odd": True, "p": p, "k": k}
            else:
                p_half = p // 2
                if even_m_range(p, k) != parent_range(p_half, k - 1):
                    return {"ok": False, "even_n": True, "p": p, "k": k}
                if odd_m_range(p, k) != parent_range(p_half + 2, k - 1):
                    return {"ok": False, "odd_n": True, "p": p, "k": k}
            n_ok += 1
    return {"ok": n_ok == (K_WIN - 2) * len(cols), "n_ok": n_ok, "k_hi": K_WIN}


def green_unique() -> dict:
    """k<=K_G: G xor matches want_col_gxor; tot is 1 iff k in {3,4,5}."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        per = {}
        tot = 0
        for p in PS:
            got = gxor_p(p, k)
            want = want_col_gxor(p, k)
            if got != want:
                return {"ok": False, "p": p, "k": k, "got": got, "want": want}
            per[str(p)] = got
            tot ^= got
            n_ok += 1
        if tot != want_unique_gxor_tot(k) or tot != want_unique_gxor_tot_closed(k):
            return {"ok": False, "tot": True, "k": k, "got": tot}
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"tot": tot, "n_fire": sum(per.values()), "per": per}
    extras = {}
    for p in EXTRAS:
        extras[str(p)] = [gxor_p(p, k) for k in range(0, 9)]
        for k in range(0, 9):
            if gxor_p(p, k) != want_col_gxor(p, k):
                return {"ok": False, "extra": p, "k": k}
    ok = (
        rows["0"]["tot"] == 0
        and rows["3"]["tot"] == 1
        and rows["4"]["tot"] == 1
        and rows["5"]["tot"] == 1
        and rows["6"]["tot"] == 0
        and rows["12"]["tot"] == 0
        and rows["5"]["n_fire"] == 9
        and rows["6"]["n_fire"] == 16
        and all(want_col_gxor(p, 6) == 1 for p in PS)
        and want_unique_tot(3) == 0
        and want_unique_tot(5) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows, "extras": extras}


def tot_form() -> dict:
    """k<=K_ALG: recurrence tot equals 1 iff k in {3,4,5}."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_unique_gxor_tot(k) != want_unique_gxor_tot_closed(k):
            return {"ok": False, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_col_gxor(16, 3) == 1
        and want_col_gxor(30, 4) == 1
        and want_col_gxor(32, 4) == 1
        and want_col_gxor(76, 6) == 1
        and want_col_gxor(40, 5) == 1
        and want_col_gxor(44, 5) == 1
        and parent_p(16) == 10
        and parent_p(30) == 16
        and parent_p(76) == 40
        and parent_p(86) == 44
        and parent_p(88) == 46
        and parent_p(98) == 50
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_g_eq_pack() -> dict:
    """Green unique tot equals packed unique tot: k=3 Green=1 packed=0."""
    ok = want_unique_gxor_tot_closed(3) == 1 and want_unique_tot(3) == 0
    return {"ok": ok, "k": 3, "green": 1, "pack": 0}


def prefixes() -> dict:
    qf = json.loads(QF_JSON.read_text())
    ok = (
        qf["checks"]["all_ok"]
        and qf["verdict"]["unique_tot_0_all_k"] == "LEMMA"
        and qf["lemmas"]["unique_tot_0_all_k"] is True
        and qf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qf["verdict"]["prize"] == "unsolved"
        and want_unique_tot(0) == 0
        and want_unique_gxor_tot_closed(5) == 1
        and want_unique_gxor_tot_closed(6) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, win, gr, tot, kg, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and win["ok"] and gr["ok"]
    assert tot["ok"] and kg["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    win = windows_ok()
    gr = green_unique()
    tot = tot_form()
    kg = killed_g_eq_pack()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, win, gr, tot, kg, sc, pref)
    dump = {
        "cycle": "QG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "windows_ok": {k: win[k] for k in win if k != "ok"},
        "green_unique": {k: gr[k] for k in gr if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_gxor_doubling": True,
            "unique_gxor_tot_iff_k_in_3_4_5": True,
            "unique_gxor_1_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "g_eq_pack": False,
            "prize": False,
        },
        "verdict": {
            "unique_gxor_doubling": "LEMMA",
            "unique_gxor_tot_iff_k_in_3_4_5": "LEMMA",
            "unique_gxor_1_k_ge_6": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "g_eq_pack": "KILLED",
            "unique_eq_rest": "KILLED",
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
        "green_unique n_ok",
        dump["green_unique"]["n_ok"],
        "k_hi",
        dump["green_unique"]["k_hi"],
        "n_fire5",
        dump["green_unique"]["rows"]["5"]["n_fire"],
        "n_fire6",
        dump["green_unique"]["rows"]["6"]["n_fire"],
    )
    print("windows n_ok", dump["windows_ok"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
