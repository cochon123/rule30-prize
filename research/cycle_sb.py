#!/usr/bin/env python3
"""Cycle SB: odd-child G=1 odd-j green4 is (g1 xor 1, g1, 1, gm).

Cycle RZ odd-child green4 at odd j=2r+1 is
(G(m,r+1)^G(m,r), G(m,r+1), G(m,r), G(m,r-1)). On G=1, G(m,r)=1,
so the 4-tuple equals (g1^1, g1, 1, gm) with g1=G(m,r+1) and
gm=G(m,r-1): one of (1,0,1,0), (1,0,1,1), (0,1,1,0), (0,1,1,1).
None is in AND_ONES. Palindrome swaps (g1, gm), so unclipped
counts of (1,0,1,1) and (0,1,1,0) are equal. Clipped counts are
not (k=2 is 8 vs 9). Cycle SA even-j form is not this 4-tuple.
Packed AND at consecutive-p can still fire (Cycle QV mismatch).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sb.py --certify
Dump: research/cycle_sb.json
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
from cycle_hh import AND_ONES, and_from_tuple
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_rz import odd_child_green4_oddj
from cycle_sa import odd_g1_green4

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HS_JSON = Path(__file__).resolve().parent / "cycle_hs.json"
SA_JSON = Path(__file__).resolve().parent / "cycle_sa.json"
RZ_JSON = Path(__file__).resolve().parent / "cycle_rz.json"

N_PAL = 64
M_SLOTS = 64
M_HI = 64
K_COV = 8

T00 = (1, 0, 1, 0)
T01 = (1, 0, 1, 1)
T10 = (0, 1, 1, 0)
T11 = (0, 1, 1, 1)


def odd_g1_oddj_green4(m: int, r: int) -> tuple[int, int, int, int]:
    """Odd-child G=1 odd-j green4 from parent bits G(m,r+1), G(m,r-1)."""
    g1 = G(m, r + 1)
    gm = G(m, r - 1)
    return (g1 ^ 1, g1, 1, gm)


def identity() -> dict:
    """m<M_HI: odd-child G=1 odd-j green4 equals (g1 xor 1, g1, 1, gm)."""
    n_ok = n00 = n01 = n10 = n11 = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(1, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            r = j // 2
            if G(m, r) != 1:
                return {"ok": False, "g": True, "m": m, "j": j}
            got = green4(n, j)
            want = odd_g1_oddj_green4(m, r)
            if got != want or got != odd_child_green4_oddj(m, r):
                return {"ok": False, "id": True, "m": m, "j": j, "got": list(got)}
            if got in AND_ONES or and_from_tuple(*got) or and_clause(*got):
                return {"ok": False, "and": True, "m": m, "j": j, "got": list(got)}
            n_ok += 1
            if got == T00:
                n00 += 1
            elif got == T01:
                n01 += 1
            elif got == T10:
                n10 += 1
            elif got == T11:
                n11 += 1
            else:
                return {"ok": False, "pair": True, "m": m, "j": j, "got": list(got)}
    ok = (
        n_ok == n00 + n01 + n10 + n11
        and n_ok == 1344
        and n01 == n10 == 371
        and n00 == 461
        and n11 == 141
        and odd_g1_oddj_green4(0, 0) == T00
        and odd_g1_oddj_green4(1, 1) == T11
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n00": n00,
        "n01": n01,
        "n10": n10,
        "n11": n11,
        "m_hi": M_HI,
    }


def covering_chk() -> dict:
    """k<=8: covering odd n, odd j, G=1 green4 matches odd_g1_oddj_green4."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COV + 1):
        U = 1 << k
        n_cell = n00 = n01 = n10 = n11 = 0
        for n in range(1, 4 * U, 2):
            m = n // 2
            for j in range(1, 2 * n + 1, 2):
                if G(n, j) != 1:
                    continue
                r = j // 2
                got = green4(n, j)
                if got != odd_g1_oddj_green4(m, r):
                    return {"ok": False, "id": True, "k": k, "n": n, "j": j}
                if got in AND_ONES or and_clause(*got):
                    return {"ok": False, "and": True, "k": k, "n": n, "j": j}
                n_cell += 1
                if got == T00:
                    n00 += 1
                elif got == T01:
                    n01 += 1
                elif got == T10:
                    n10 += 1
                else:
                    n11 += 1
        n_ok += 1
        rows[str(k)] = {
            "n_cell": n_cell,
            "n00": n00,
            "n01": n01,
            "n10": n10,
            "n11": n11,
        }
    ok = (
        n_ok == K_COV + 1
        and rows["0"]["n_cell"] == 4
        and rows["5"]["n_cell"] == 1344
        and all(rows[str(k)]["n01"] == rows[str(k)]["n10"] for k in range(0, K_COV + 1))
        and rows["8"]["n_cell"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COV, "rows": rows}


def pal_pair() -> dict:
    """On G=1 odd j, palindrome partner swaps (g1, gm)."""
    n_ok = 0
    for m in range(0, M_HI):
        n = 2 * m + 1
        for j in range(1, 2 * n + 1, 2):
            if G(n, j) != 1:
                continue
            jp = 2 * n - j
            if jp % 2 == 0 or G(n, jp) != 1:
                return {"ok": False, "pal": True, "m": m, "j": j}
            r = j // 2
            rp = jp // 2
            g1, gm = G(m, r + 1), G(m, r - 1)
            if (G(m, rp + 1), G(m, rp - 1)) != (gm, g1):
                return {"ok": False, "swap": True, "m": m, "j": j}
            n_ok += 1
    ok = n_ok == 1344
    return {"ok": ok, "n_ok": n_ok}


def tot_form() -> dict:
    """Four odd-j G=1 tuples sit outside AND_ONES; not SA even-j only."""
    t00 = odd_g1_oddj_green4(0, 0)
    t11 = odd_g1_oddj_green4(1, 1)
    ok = (
        t00 == T00
        and t11 == T11
        and all(t not in AND_ONES for t in (T00, T01, T10, T11))
        and all(and_from_tuple(*t) == 0 for t in (T00, T01, T10, T11))
        and T01 == odd_g1_green4(0, 0)
        and T11 != odd_g1_green4(0, 0)
        and T00 != T11
    )
    return {"ok": ok}


def clip_split() -> dict:
    """k=2 clipped j<=5U: T01 and T10 counts differ (8 vs 9)."""
    U = 4
    clip = 5 * U
    n01 = n10 = 0
    for n in range(1, 4 * U, 2):
        m = n // 2
        hi = min(2 * n, clip)
        for j in range(1, hi + 1, 2):
            if G(n, j) != 1:
                continue
            got = green4(n, j)
            if got == T01:
                n01 += 1
            elif got == T10:
                n10 += 1
    ok = n01 == 8 and n10 == 9
    return {"ok": ok, "n01": n01, "n10": n10}


def killed_eq() -> dict:
    """Identically one tuple; T00 equals T11; clipped T01 equals T10."""
    clip = clip_split()
    ok = (
        T00 != T11
        and T00 != T01
        and T11 != odd_g1_green4(0, 0)
        and clip["ok"]
        and clip["n01"] != clip["n10"]
        and green4(1, 1) == T00
        and green4(3, 3) == T11
    )
    return {"ok": ok, "clip_n01": clip["n01"], "clip_n10": clip["n10"]}


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hs = json.loads(HS_JSON.read_text())
    sa = json.loads(SA_JSON.read_text())
    rz = json.loads(RZ_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hs["checks"]["all_ok"]
        and sa["checks"]["all_ok"]
        and rz["checks"]["all_ok"]
        and sa["verdict"]["odd_g1_evenj_green4_eq_g_g1_1_g"] == "LEMMA"
        and sa["verdict"]["odd_g1_evenj_pal_pairs_types"] == "LEMMA"
        and sa["verdict"]["odd_g1_evenj_clip_split_eq"] == "KILLED"
        and rz["verdict"]["odd_child_green4_eq_G_Gm_xor_G"] == "LEMMA"
        and sa["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sa["verdict"]["prize"] == "unsolved"
        and odd_g1_oddj_green4(0, 0) == T00
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, ident, cov, pair, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert ident["ok"] and cov["ok"] and pair["ok"] and tot["ok"]
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
    ident = identity()
    cov = covering_chk()
    pair = pal_pair()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, ident, cov, pair, tot, kl, sc, pref)
    dump = {
        "cycle": "SB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "identity": {k: ident[k] for k in ident if k != "ok"},
        "covering_chk": {k: cov[k] for k in cov if k != "ok"},
        "pal_pair": {k: pair[k] for k in pair if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_g1_oddj_green4_eq_g1x_g1_1_gm": True,
            "odd_g1_oddj_green4_never_AND": True,
            "odd_g1_oddj_pal_swaps_g1_gm": True,
            "odd_g1_oddj_unclip_T01_eq_T10": True,
            "odd_g1_oddj_green4_eq_one_tuple": False,
            "odd_g1_oddj_T00_eq_T11": False,
            "odd_g1_oddj_clip_T01_eq_T10": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_g1_oddj_green4_eq_g1x_g1_1_gm": "LEMMA",
            "odd_g1_oddj_green4_never_AND": "LEMMA",
            "odd_g1_oddj_pal_swaps_g1_gm": "LEMMA",
            "odd_g1_oddj_unclip_T01_eq_T10": "LEMMA",
            "odd_g1_oddj_green4_eq_one_tuple": "KILLED",
            "odd_g1_oddj_T00_eq_T11": "KILLED",
            "odd_g1_oddj_clip_T01_eq_T10": "KILLED",
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
        "identity n_ok",
        dump["identity"]["n_ok"],
        "n01",
        dump["identity"]["n01"],
        "n10",
        dump["identity"]["n10"],
        "cover n_ok",
        dump["covering_chk"]["n_ok"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
