#!/usr/bin/env python3
"""Cycle RO: UNIQUE_ODD Green n%4 is (0,0,0,1) for every k>=6.

Cycle RK UNIQUE_ODD even-n tot is 0, and for k>=2 covering j is odd
so G(even,odd)=0 columnwise: n%4 in {0,2} vanish. Odd tot is UNIQUE_ODD
tot, 1 iff k>=4. The n%4==1 slice is 1 iff k==5, so n%4==3 is 1 iff
k==4 or k>=6, and for k>=6 the tuple is (0,0,0,1). Dual of Cycle RN
unique Green (0,1,1,0) xor UNIQUE_EVEN Green (0,1,1,1). Not that
tuple for all k (k=5 is (0,1,0,0)). Not UNIQUE_ODD Green n3 tot
equals packed UNIQUE_ODD n3 tot (k=2). Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ro.py --certify
Dump: research/cycle_ro.json
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
from cycle_pc import live_lo
from cycle_qj import UNIQUE_ODD, want_unique_even, want_unique_odd
from cycle_qz import want_uo_n3
from cycle_rk import want_uo_even_n, want_u_even_n, want_u_odd_n
from cycle_rm import want_u_g_nmod

OUT = Path(__file__).resolve().with_suffix(".json")
RK_JSON = Path(__file__).resolve().parent / "cycle_rk.json"
RN_JSON = Path(__file__).resolve().parent / "cycle_rn.json"
QZ_JSON = Path(__file__).resolve().parent / "cycle_qz.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64
Q = 10


def want_uo_g_n0(_k: int) -> int:
    """UNIQUE_ODD Green xor on n%4==0, all k."""
    return 0


def want_uo_g_n1(k: int) -> int:
    """UNIQUE_ODD Green xor on n%4==1: 1 iff k==5."""
    return int(k == 5)


def want_uo_g_n2(_k: int) -> int:
    """UNIQUE_ODD Green xor on n%4==2, all k."""
    return 0


def want_uo_g_n3(k: int) -> int:
    """UNIQUE_ODD Green xor on n%4==3: 1 iff k==4 or k>=6."""
    return int(k == 4 or k >= 6)


def want_uo_g_nmod(k: int) -> list[int]:
    return [want_uo_g_n0(k), want_uo_g_n1(k), want_uo_g_n2(k), want_uo_g_n3(k)]


def want_ue_g_nmod(k: int) -> list[int]:
    """UNIQUE_EVEN Green n%4: unique Green xor UNIQUE_ODD Green."""
    u = want_u_g_nmod(k)
    uo = want_uo_g_nmod(k)
    return [u[i] ^ uo[i] for i in range(4)]


def gxor_nmod(p: int, k: int) -> list[int]:
    """Covering Green xor at packed p, split by n%4."""
    U = 1 << k
    delta = p // 2
    j = 5 * U - delta
    tot = [0, 0, 0, 0]
    if j < 0:
        return tot
    for n in range(live_lo(k, delta), 4 * U):
        if 0 <= j <= 2 * n and G(n, j):
            tot[n % 4] ^= 1
    return tot


def tot_form() -> dict:
    """k<=K_ALG: UO n%4 is closed; k>=6 is (0,0,0,1); UE k>=6 is (0,1,1,1)."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        uo = want_uo_g_nmod(k)
        if uo[0] != 0 or uo[2] != 0:
            return {"ok": False, "even": True, "k": k, "uo": uo}
        if (uo[0] ^ uo[2]) != want_uo_even_n():
            return {"ok": False, "rk": True, "k": k}
        if (uo[1] ^ uo[3]) != want_unique_odd(k):
            return {"ok": False, "odd": True, "k": k, "uo": uo}
        if (uo[1] ^ uo[3]) != want_u_odd_n(k):
            return {"ok": False, "rk_odd": True, "k": k}
        if k >= 6 and uo != [0, 0, 0, 1]:
            return {"ok": False, "ge6": True, "k": k, "uo": uo}
        ue = want_ue_g_nmod(k)
        if (ue[0] ^ ue[2]) != want_unique_even(k):
            return {"ok": False, "ue": True, "k": k, "ue": ue}
        if (ue[0] ^ ue[2]) != want_u_even_n(k):
            return {"ok": False, "rk_ue": True, "k": k}
        if k >= 6 and ue != [0, 1, 1, 1]:
            return {"ok": False, "ue6": True, "k": k, "ue": ue}
        if k >= 6 and want_u_g_nmod(k) != [0, 1, 1, 0]:
            return {"ok": False, "rn": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_uo_g_nmod(0) == [0, 0, 0, 0]
        and want_uo_g_nmod(4) == [0, 0, 0, 1]
        and want_uo_g_nmod(5) == [0, 1, 0, 0]
        and want_uo_g_nmod(6) == [0, 0, 0, 1]
        and want_ue_g_nmod(6) == [0, 1, 1, 1]
        and want_uo_g_n1(5) == 1
        and want_uo_g_n3(4) == 1
        and want_uo_g_n3(5) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def uo_walk() -> dict:
    """k<=K_CHK: UNIQUE_ODD Green n%4 matches the closed form."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        tot = [0, 0, 0, 0]
        for p in UNIQUE_ODD:
            got = gxor_nmod(p, k)
            for i in range(4):
                tot[i] ^= got[i]
        if tot != want_uo_g_nmod(k):
            return {"ok": False, "form": True, "k": k, "tot": tot}
        n_ok += 1
        rows[str(k)] = tot
    ok = (
        n_ok == K_CHK + 1
        and rows["0"] == [0, 0, 0, 0]
        and rows["4"] == [0, 0, 0, 1]
        and rows["5"] == [0, 1, 0, 0]
        and rows["6"] == [0, 0, 0, 1]
        and rows["8"] == [0, 0, 0, 1]
        and len(UNIQUE_ODD) == 9
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def killed_eq() -> dict:
    """UNIQUE_ODD Green n%4==(0,0,0,1) all k; Green n3 equals packed n3."""
    rk = json.loads(RK_JSON.read_text())
    tot5 = rk["killed_eq"]["tot5"]
    ok = (
        tot5 == [0, 1, 0, 0]
        and want_uo_g_nmod(5) == [0, 1, 0, 0]
        and want_uo_g_nmod(5) != [0, 0, 0, 1]
        and want_uo_g_nmod(0) == [0, 0, 0, 0]
        and want_uo_g_nmod(0) != [0, 0, 0, 1]
        and want_uo_g_n3(2) == 0
        and want_uo_n3(2) == 1
        and want_uo_g_n3(2) != want_uo_n3(2)
        and want_uo_g_n3(6) == 1
        and want_uo_n3(6) == 1
    )
    return {"ok": ok, "tot5": tot5}


def prefixes() -> dict:
    rk = json.loads(RK_JSON.read_text())
    rn = json.loads(RN_JSON.read_text())
    qz = json.loads(QZ_JSON.read_text())
    ok = (
        rk["checks"]["all_ok"]
        and rn["checks"]["all_ok"]
        and qz["checks"]["all_ok"]
        and rk["verdict"]["uo_even_n_0"] == "LEMMA"
        and rn["verdict"]["u_g_nmod_0110_k_ge_6"] == "LEMMA"
        and qz["verdict"]["unique_odd_n3_iff_k_ge_2"] == "LEMMA"
        and rk["verdict"]["uo_nmod_0011_all_k"] == "KILLED"
        and rn["verdict"]["u_g_nmod_eq_packed"] == "KILLED"
        and rn["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rn["verdict"]["prize"] == "unsolved"
        and want_uo_g_nmod(6) == [0, 0, 0, 1]
        and want_u_g_nmod(6) == [0, 1, 1, 0]
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
    walk = uo_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "RO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "uo_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "uo_g_nmod_0001_k_ge_6": True,
            "uo_g_n1_iff_k_eq_5": True,
            "uo_g_n3_iff_k_eq_4_or_ge_6": True,
            "uo_g_nmod_0001_all_k": False,
            "uo_g_n3_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "uo_g_nmod_0001_k_ge_6": "LEMMA",
            "uo_g_n1_iff_k_eq_5": "LEMMA",
            "uo_g_n3_iff_k_eq_4_or_ge_6": "LEMMA",
            "uo_g_nmod_0001_all_k": "KILLED",
            "uo_g_n3_eq_packed": "KILLED",
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
        "uo_walk n_ok",
        dump["uo_walk"]["n_ok"],
        "uo6",
        dump["uo_walk"]["rows"]["6"],
        "uo5",
        dump["uo_walk"]["rows"]["5"],
        "uo4",
        dump["uo_walk"]["rows"]["4"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
