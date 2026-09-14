#!/usr/bin/env python3
"""Cycle RL: leftover Green odd-n tot is 1 iff k not in {1,3}.

Cycle QW Green odd-n rest is 1 iff k in {0,2}. Cycle RK unique Green
odd-n tot equals UNIQUE_ODD tot, 1 iff k>=4 (Cycle QJ). Their xor is
leftover Green odd-n tot, 1 iff k not in {1,3}. Equivalently QH
leftover tot xor leftover even-n (QK even-j even-n, since
G(even,odd)=0). Not leftover Green odd-n equals packed leftover
odd-n (k=6: Green 1, packed 0). Not leftover Green odd-n equals ST.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rl.py --certify
Dump: research/cycle_rl.json
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
from cycle_pb import want_rest_e0
from cycle_qh import want_green_lo
from cycle_qj import want_unique_odd
from cycle_qk import want_lo_ee, want_lo_oe
from cycle_qw import want_green_even, want_green_odd
from cycle_rb import want_u_n1, want_u_n3
from cycle_rk import want_u_even_n, want_u_odd_n

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QH_JSON = Path(__file__).resolve().parent / "cycle_qh.json"
QK_JSON = Path(__file__).resolve().parent / "cycle_qk.json"
QW_JSON = Path(__file__).resolve().parent / "cycle_qw.json"
RK_JSON = Path(__file__).resolve().parent / "cycle_rk.json"

N_PAL = 64
M_SLOTS = 64
K_CHK = 8
K_ALG = 64
Q = 10


def want_lo_g_odd(k: int) -> int:
    """Leftover Green xor on odd n, all k: 1 iff k not in {1,3}."""
    return int(k not in (1, 3))


def want_lo_g_even(k: int) -> int:
    """Leftover Green xor on even n, all k: 1 iff k in {0,2,4,5}."""
    return want_green_lo(k) ^ want_lo_g_odd(k)


def tot_form() -> dict:
    """Odd leftover Green is Green odd rest xor unique odd; even is QK lo_ee."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        odd = want_green_odd(k) ^ want_u_odd_n(k)
        even = want_green_even(k) ^ want_u_even_n(k)
        if odd != want_lo_g_odd(k):
            return {"ok": False, "odd": True, "k": k, "odd": odd}
        if even != want_lo_g_even(k):
            return {"ok": False, "even": True, "k": k, "even": even}
        if even != want_lo_ee(k):
            return {"ok": False, "qk": True, "k": k, "even": even}
        if even != int(k in (0, 2, 4, 5)):
            return {"ok": False, "ee": True, "k": k}
        if (even ^ odd) != want_green_lo(k):
            return {"ok": False, "qh": True, "k": k}
        if want_u_odd_n(k) != want_unique_odd(k):
            return {"ok": False, "rk": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_g_odd(0) == 1
        and want_lo_g_odd(1) == 0
        and want_lo_g_odd(3) == 0
        and want_lo_g_odd(4) == 1
        and want_lo_g_odd(6) == 1
        and want_lo_g_even(5) == 1
        and want_lo_g_even(6) == 0
        and want_lo_oe(1) == 1
    )
    return {"ok": ok, "n_ok": n_ok}


def leftover_npar(k: int) -> dict:
    """Covering leftover Green xor split by n parity."""
    U = 1 << k
    T = Q * U
    clip = 5 * U
    ee = eo = 0
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            p = T - 2 * j
            if p < 0 or p in FORCED or p in UNIQUE_REST:
                continue
            if n % 2:
                eo ^= 1
            else:
                ee ^= 1
    return {"ee": ee, "eo": eo}


def leftover_walk() -> dict:
    """k<=K_CHK: leftover Green odd-n tot matches want_lo_g_odd."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = leftover_npar(k)
        if w["eo"] != want_lo_g_odd(k) or w["ee"] != want_lo_g_even(k):
            return {"ok": False, "form": True, "k": k, "w": w}
        if (w["ee"] ^ w["eo"]) != want_green_lo(k):
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
        rows[str(k)] = w
    ok = (
        n_ok == K_CHK + 1
        and rows["0"]["eo"] == 1
        and rows["1"]["eo"] == 0
        and rows["3"]["eo"] == 0
        and rows["6"]["eo"] == 1
        and rows["8"]["eo"] == 1
        and rows["6"]["ee"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CHK, "rows": rows}


def killed_eq() -> dict:
    """Leftover Green odd-n equals packed leftover odd-n / ST."""
    qo = json.loads(QO_JSON.read_text())
    tot6 = qo["rest_n0_walk"]["rows"]["6"]["tot"]
    pack_odd6 = tot6[1] ^ tot6[3]
    u_odd6 = want_u_n1(6) ^ want_u_n3(6)
    lo_pack6 = pack_odd6 ^ u_odd6
    ok = (
        want_lo_g_odd(6) == 1
        and lo_pack6 == 0
        and want_lo_g_odd(6) != lo_pack6
        and want_lo_g_odd(7) == 1
        and want_rest_e0(7) == 0
        and want_lo_g_odd(7) != want_rest_e0(7)
        and want_u_n1(6) == 0
        and want_u_n3(6) == 1
    )
    return {"ok": ok, "lo_pack6": lo_pack6, "pack_odd6": pack_odd6}


def prefixes() -> dict:
    qh = json.loads(QH_JSON.read_text())
    qk = json.loads(QK_JSON.read_text())
    qw = json.loads(QW_JSON.read_text())
    rk = json.loads(RK_JSON.read_text())
    ok = (
        qh["checks"]["all_ok"]
        and qk["checks"]["all_ok"]
        and qw["checks"]["all_ok"]
        and rk["checks"]["all_ok"]
        and qh["verdict"]["green_lo_iff_k_ge_6"] == "LEMMA"
        and qw["verdict"]["green_odd_rest_iff_k_in_0_2"] == "LEMMA"
        and rk["verdict"]["uo_even_n_0"] == "LEMMA"
        and qk["verdict"]["lo_oe_iff_k_ge_1"] == "LEMMA"
        and rk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rk["verdict"]["prize"] == "unsolved"
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
    walk = leftover_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "RL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_g_odd_iff_k_not_1_3": True,
            "lo_g_odd_eq_packed": False,
            "lo_g_odd_eq_ST": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_g_odd_iff_k_not_1_3": "LEMMA",
            "lo_g_odd_eq_packed": "KILLED",
            "lo_g_odd_eq_ST": "KILLED",
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
        "leftover_walk n_ok",
        dump["leftover_walk"]["n_ok"],
        "eo6",
        dump["leftover_walk"]["rows"]["6"]["eo"],
        "ee6",
        dump["leftover_walk"]["rows"]["6"]["ee"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
