#!/usr/bin/env python3
"""Cycle SK: covering Green forced on n%4==3 even j is 1 iff k>=1.

Forced columns j=5U-2, 5U-3, 5U-7. For k>=1 those parities are
even, odd, odd, so even-j forced is p=4. Cycle PC's p=4 set on
n%4==3 has odd count for k>=1, xor 1; at k=0 even-j is p=6 on
{1,2}, so n3 even-j is 0. Odd-j is 1 iff k<=2 by Cycle RV n3 tot.
Even-j on n%4==1 is 1 for every k; odd-j is 0. Cycle SI rest n3e
is g1_n3e xor this bit (PREFIX all k via Cycle SJ clip-edge).
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sk.py --certify
Dump: research/cycle_sk.json
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
from cycle_pc import in_p4, live_lo
from cycle_qv import even_slots
from cycle_rv import want_f_n0, want_f_n1, want_f_n2, want_f_n3
from cycle_si import want_g_n1e, want_g_n3e
from cycle_sj import want_g1_n1e, want_g1_n3e
from cycle_qx import want_g_n0

OUT = Path(__file__).resolve().with_suffix(".json")
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"
RV_JSON = Path(__file__).resolve().parent / "cycle_rv.json"
SI_JSON = Path(__file__).resolve().parent / "cycle_si.json"
SJ_JSON = Path(__file__).resolve().parent / "cycle_sj.json"

N_PAL = 64
M_SLOTS = 64
K_WALK = 12
K_ALG = 64
FORCED_P = (4, 6, 14)


def want_f_n3e(k: int) -> int:
    """Green forced xor on n%4==3 even j, all k: 1 iff k>=1."""
    return int(k >= 1)


def want_f_n3o(k: int) -> int:
    """Green forced xor on n%4==3 odd j, all k: 1 iff k<=2."""
    return int(k <= 2)


def want_f_n1e(k: int) -> int:
    """Green forced xor on n%4==1 even j, all k: 1."""
    return 1


def want_f_n1o(k: int) -> int:
    """Green forced xor on n%4==1 odd j, all k: 0."""
    return 0


def forced_js(k: int) -> list[tuple[int, int, int]]:
    """(p, j, j%2) for the three covering forced columns."""
    U = 1 << k
    out = []
    for p in FORCED_P:
        j = 5 * U - p // 2
        out.append((p, j, j % 2))
    return out


def forced_nmodj(k: int) -> dict:
    """Green G=1 xor at forced columns, split n%4 and j parity."""
    U = 1 << k
    tot = [[0, 0] for _ in range(4)]
    js = forced_js(k)
    for n in range(0, 4 * U):
        hi = min(2 * n, 5 * U)
        for _p, j, jp in js:
            if 0 <= j <= hi and G(n, j):
                tot[n % 4][jp] ^= 1
    return {
        "n0e": tot[0][0],
        "n0o": tot[0][1],
        "n1e": tot[1][0],
        "n1o": tot[1][1],
        "n2e": tot[2][0],
        "n2o": tot[2][1],
        "n3e": tot[3][0],
        "n3o": tot[3][1],
    }


def p4_n3_xor(k: int) -> int:
    """Cycle PC p=4 set xor on n%4==3."""
    x = 0
    for n in range(live_lo(k, 2), 4 << k):
        if n % 4 == 3 and in_p4(n, k):
            x ^= 1
    return x


def p4_n3_count(k: int) -> int:
    """Closed count of p=4 ones with n%4==3, k>=0."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return (k - 1) + (k % 2)


def nmodj_walk() -> dict:
    """k<=12: forced n3 even-j equals want_f_n3e; n1 even-j is 1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_WALK + 1):
        w = forced_nmodj(k)
        if w["n0o"] != 0 or w["n2o"] != 0:
            return {"ok": False, "even_oddj": True, "k": k, "w": w}
        if w["n0e"] != want_f_n0(k) or w["n2e"] != want_f_n2(k):
            return {"ok": False, "even": True, "k": k, "w": w}
        if w["n1e"] != want_f_n1e(k) or w["n1o"] != want_f_n1o(k):
            return {"ok": False, "n1": True, "k": k, "w": w}
        if w["n3e"] != want_f_n3e(k) or w["n3o"] != want_f_n3o(k):
            return {"ok": False, "n3": True, "k": k, "w": w}
        if (w["n1e"] ^ w["n1o"]) != want_f_n1(k):
            return {"ok": False, "n1xor": True, "k": k, "w": w}
        if (w["n3e"] ^ w["n3o"]) != want_f_n3(k):
            return {"ok": False, "n3xor": True, "k": k, "w": w}
        if k >= 1:
            js = forced_js(k)
            if js[0][2] != 0 or js[1][2] != 1 or js[2][2] != 1:
                return {"ok": False, "jpar": True, "k": k, "js": js}
            if p4_n3_xor(k) != 1 or p4_n3_count(k) % 2 != 1:
                return {"ok": False, "p4n3": True, "k": k}
            if w["n3e"] != p4_n3_xor(k):
                return {"ok": False, "p4eq": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {"n1e": w["n1e"], "n3e": w["n3e"], "n3o": w["n3o"]}
    ok = (
        n_ok == K_WALK + 1
        and rows["0"]["n3e"] == 0
        and rows["0"]["n3o"] == 1
        and rows["1"]["n3e"] == 1
        and rows["2"]["n3e"] == 1
        and rows["2"]["n3o"] == 1
        and rows["3"]["n3o"] == 0
        and rows["12"]["n3e"] == 1
        and rows["12"]["n3o"] == 0
        and rows["0"]["n1e"] == 1
        and rows["12"]["n1e"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_WALK, "rows": rows}


def tot_form() -> dict:
    """k<=64: j-parity helpers recover RV tots and SI rest via SJ g1."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if (want_f_n3e(k) ^ want_f_n3o(k)) != want_f_n3(k):
            return {"ok": False, "n3": True, "k": k}
        if (want_f_n1e(k) ^ want_f_n1o(k)) != want_f_n1(k):
            return {"ok": False, "n1": True, "k": k}
        if (want_g1_n3e(k) ^ want_f_n3e(k)) != want_g_n3e(k):
            return {"ok": False, "rest_n3e": True, "k": k}
        if (want_g1_n1e(k) ^ want_f_n1e(k)) != want_g_n1e(k):
            return {"ok": False, "rest_n1e": True, "k": k}
        if k >= 1 and p4_n3_count(k) % 2 != 1:
            return {"ok": False, "p4cnt": True, "k": k}
        if k >= 1:
            U = 1 << k
            if ((5 * U - 2) % 2) != 0 or ((5 * U - 3) % 2) != 1:
                return {"ok": False, "jpar": True, "k": k}
            if ((5 * U - 7) % 2) != 1:
                return {"ok": False, "j14": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_f_n3e(0) == 0
        and want_f_n3e(1) == 1
        and want_f_n3o(2) == 1
        and want_f_n3o(3) == 0
        and want_f_n1e(0) == 1
        and want_f_n1o(5) == 0
        and p4_n3_count(0) == 0
        and p4_n3_count(1) == 1
        and p4_n3_count(2) == 1
        and p4_n3_count(3) == 3
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """Identically 1; identically 0; Green n0 tot equals n3 even-j forced."""
    ok = (
        want_f_n3e(0) == 0
        and want_f_n3e(1) == 1
        and want_f_n3o(0) == 1
        and want_f_n3o(3) == 0
        and want_g_n0(0) != want_f_n3e(0)
        and want_g_n0(3) != want_f_n3e(3)
        and want_g_n3e(1) != want_f_n3e(1)
    )
    return {"ok": ok}


def prefixes() -> dict:
    pc = json.loads(PC_JSON.read_text())
    rv = json.loads(RV_JSON.read_text())
    si = json.loads(SI_JSON.read_text())
    sj = json.loads(SJ_JSON.read_text())
    ok = (
        pc["checks"]["all_ok"]
        and rv["checks"]["all_ok"]
        and si["checks"]["all_ok"]
        and sj["checks"]["all_ok"]
        and pc["verdict"]["p4_set"] == "LEMMA"
        and rv["verdict"]["f_n1_all_k"] == "LEMMA"
        and si["verdict"]["green_n3e_iff_k_ne_1_k_le_10"] == "CERTIFIED"
        and sj["verdict"]["p0_odd_iff_k_eq_0_k_le_12"] == "CERTIFIED"
        and sj["verdict"]["g1_n3e_eq_rest_n3e"] == "KILLED"
        and si["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and si["verdict"]["prize"] == "unsolved"
        and want_f_n3e(0) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert walk["ok"] and tot["ok"] and kl["ok"]
    assert sc["ok"] and pref["ok"]
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
    walk = nmodj_walk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "SK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "nmodj_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "f_n3e_iff_k_ge_1": True,
            "f_n3o_iff_k_le_2": True,
            "f_n1e_all_k": True,
            "f_n1o_0_all_k": True,
            "si_rest_n3e_via_g1_xor_forced_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "f_n3e_iff_k_ge_1": "LEMMA",
            "f_n3o_iff_k_le_2": "LEMMA",
            "f_n1e_all_k": "LEMMA",
            "f_n1o_0_all_k": "LEMMA",
            "walk_k_le_12": "CERTIFIED",
            "si_rest_n3e_via_g1_xor_forced_all_k": "PREFIX",
            "f_n3e_identically_1": "KILLED",
            "g_n0_eq_f_n3e": "KILLED",
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
        "walk n_ok",
        dump["nmodj_walk"]["n_ok"],
        "k0 n3e",
        dump["nmodj_walk"]["rows"]["0"]["n3e"],
        "k12 n3e",
        dump["nmodj_walk"]["rows"]["12"]["n3e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
