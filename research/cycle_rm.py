#!/usr/bin/env python3
"""Cycle RM: leftover Green n%4 is (0,0,0,1) for every k>=6.

Cycle RL leftover even-n tot is 0 for k>=6 and odd-n tot is 1.
Leftover Green n%4==3 tot is 1 iff k<=1 or k>=6 (Green n3 tot 1
xor unique Green n3 tot, the latter 1 iff 2<=k<=5). Hence for
k>=6 the tuple is (0,0,0,1): leftover Green lives only on n%4==3.
Not that tuple for all k (k=0 is (1,0,0,1)). Not leftover n3 tot
equals packed leftover n3 tot (k=0 and k=9). Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rm.py --certify
Dump: research/cycle_rm.json
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
from cycle_md import UNIQUE_REST
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qg import want_unique_gxor_tot_closed
from cycle_qj import want_unique_even, want_unique_odd
from cycle_qx import want_g_n0, want_g_n1, want_g_n2, want_g_n3
from cycle_rb import want_u_n3
from cycle_rl import want_lo_g_even, want_lo_g_odd

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
RL_JSON = Path(__file__).resolve().parent / "cycle_rl.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64
Q = 10


def want_u_g_n0(k: int) -> int:
    """UNIQUE_REST Green xor on n%4==0: 1 iff k in {2,3,5}."""
    return int(k in (2, 3, 5))


def want_u_g_n1(k: int) -> int:
    """UNIQUE_REST Green xor on n%4==1: 1 iff k in {2,3} or k>=6."""
    return int(k in (2, 3) or k >= 6)


def want_u_g_n2(k: int) -> int:
    """UNIQUE_REST Green xor on n%4==2: 1 iff k==2 or k>=5."""
    return int(k == 2 or k >= 5)


def want_u_g_n3(k: int) -> int:
    """UNIQUE_REST Green xor on n%4==3: 1 iff 2<=k<=5."""
    return int(2 <= k <= 5)


def want_u_g_nmod(k: int) -> list[int]:
    return [want_u_g_n0(k), want_u_g_n1(k), want_u_g_n2(k), want_u_g_n3(k)]


def want_lo_g_n0(k: int) -> int:
    """Leftover Green xor on n%4==0: 1 iff k in {0,1,3,5}."""
    return want_g_n0(k) ^ want_u_g_n0(k)


def want_lo_g_n1(k: int) -> int:
    """Leftover Green xor on n%4==1: 1 iff k in {1,2,4,5}."""
    return want_g_n1(k) ^ want_u_g_n1(k)


def want_lo_g_n2(k: int) -> int:
    """Leftover Green xor on n%4==2: 1 iff k in {1,2,3,4}."""
    return want_g_n2(k) ^ want_u_g_n2(k)


def want_lo_g_n3(k: int) -> int:
    """Leftover Green xor on n%4==3: 1 iff k<=1 or k>=6."""
    return want_g_n3(k) ^ want_u_g_n3(k)


def want_lo_g_nmod(k: int) -> list[int]:
    return [want_lo_g_n0(k), want_lo_g_n1(k), want_lo_g_n2(k), want_lo_g_n3(k)]


def tot_form() -> dict:
    """k<=K_ALG: leftover n%4 is Green xor unique Green; k>=6 is (0,0,0,1)."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = want_u_g_nmod(k)
        lo = want_lo_g_nmod(k)
        if (u[0] ^ u[2]) != want_unique_even(k):
            return {"ok": False, "ue": True, "k": k, "u": u}
        if (u[1] ^ u[3]) != want_unique_odd(k):
            return {"ok": False, "uo": True, "k": k, "u": u}
        if (u[0] ^ u[1] ^ u[2] ^ u[3]) != want_unique_gxor_tot_closed(k):
            return {"ok": False, "qg": True, "k": k}
        if (lo[0] ^ lo[2]) != want_lo_g_even(k):
            return {"ok": False, "ee": True, "k": k, "lo": lo}
        if (lo[1] ^ lo[3]) != want_lo_g_odd(k):
            return {"ok": False, "eo": True, "k": k, "lo": lo}
        if lo[3] != int(k <= 1 or k >= 6):
            return {"ok": False, "n3": True, "k": k}
        if k >= 6 and lo != [0, 0, 0, 1]:
            return {"ok": False, "ge6": True, "k": k, "lo": lo}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_g_nmod(0) == [1, 0, 0, 1]
        and want_lo_g_nmod(5) == [1, 1, 0, 0]
        and want_lo_g_nmod(6) == [0, 0, 0, 1]
        and want_u_g_n3(2) == 1
        and want_u_g_n3(5) == 1
        and want_u_g_n3(6) == 0
        and want_g_n3(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok}


def nmod_walk(kind: str, k: int) -> list[int]:
    """Covering Green xor split by n%4 on unique or leftover columns."""
    U = 1 << k
    T = Q * U
    clip = 5 * U
    tot = [0, 0, 0, 0]
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = T - 2 * j
            if p < 0 or p in FORCED:
                continue
            if kind == "unique":
                if p not in UNIQUE_REST:
                    continue
            else:
                if p in UNIQUE_REST:
                    continue
            tot[n % 4] ^= 1
    return tot


def green_walk() -> dict:
    """k<=K_CHK: unique and leftover Green n%4 match the closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        u = nmod_walk("unique", k)
        lo = nmod_walk("leftover", k)
        if u != want_u_g_nmod(k):
            return {"ok": False, "u": True, "k": k, "u": u}
        if lo != want_lo_g_nmod(k):
            return {"ok": False, "lo": True, "k": k, "lo": lo}
        n_ok += 1
        if k <= 8:
            rows[str(k)] = {"u": u, "lo": lo}
    ok = (
        n_ok == K_CHK + 1
        and rows["0"]["lo"] == [1, 0, 0, 1]
        and rows["6"]["lo"] == [0, 0, 0, 1]
        and rows["8"]["lo"] == [0, 0, 0, 1]
        and rows["5"]["u"] == [1, 0, 1, 1]
        and rows["6"]["u"] == [0, 1, 1, 0]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def killed_eq() -> dict:
    """Leftover Green n%4==(0,0,0,1) all k; leftover n3 equals packed leftover n3."""
    qo = json.loads(QO_JSON.read_text())
    tot0 = qo["rest_n0_walk"]["rows"]["0"]["tot"]
    tot9 = qo["rest_n0_walk"]["rows"]["9"]["tot"]
    lo_pack0 = tot0[3] ^ want_u_n3(0)
    lo_pack9 = tot9[3] ^ want_u_n3(9)
    ok = (
        want_lo_g_nmod(0) != [0, 0, 0, 1]
        and want_lo_g_n3(0) == 1
        and lo_pack0 == 0
        and want_lo_g_n3(0) != lo_pack0
        and want_lo_g_n3(9) == 1
        and lo_pack9 == 0
        and want_lo_g_n3(9) != lo_pack9
        and want_u_n3(9) == 1
        and tot9[3] == 1
    )
    return {"ok": ok, "lo_pack0": lo_pack0, "lo_pack9": lo_pack9}


def prefixes() -> dict:
    qh = json.loads(QH_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    rl = json.loads(RL_JSON.read_text())
    ok = (
        qh["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and rl["checks"]["all_ok"]
        and qh["verdict"]["green_lo_iff_k_ge_6"] == "LEMMA"
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and rl["verdict"]["lo_g_odd_iff_k_not_1_3"] == "LEMMA"
        and rl["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and walk["ok"]
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
    tot = tot_form()
    walk = green_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "RM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "green_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_g_nmod_0001_k_ge_6": True,
            "lo_g_n3_iff_le1_or_ge6": True,
            "lo_g_nmod_0001_all_k": False,
            "lo_g_n3_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_g_nmod_0001_k_ge_6": "LEMMA",
            "lo_g_n3_iff_le1_or_ge6": "LEMMA",
            "lo_g_nmod_0001_all_k": "KILLED",
            "lo_g_n3_eq_packed": "KILLED",
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
        "green_walk n_ok",
        dump["green_walk"]["n_ok"],
        "lo6",
        dump["green_walk"]["rows"]["6"]["lo"],
        "lo0",
        dump["green_walk"]["rows"]["0"]["lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
