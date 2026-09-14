#!/usr/bin/env python3
"""Cycle SH: packed rest on n%4==0 equals n%4==3 even-j through k<=10.

Covering packed rest split by n%4 and j parity. Even-n G=1 lives
only on even j (Cycle QV), so n%4 in {0,2} odd-j tot is 0. Packed
rest on n%4==0 equals packed rest on n%4==3 even j through k<=10,
not n%4==3 tot (odd j is extra). Packed rest on n%4==1 even j is
1 iff k not in {3,4,5} through k<=10; that is not identically 1,
not parent even tot (Cycle RU packed analogue dies at k=3), and
not Green n%4==1 rest. Not the identities for all k. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sh.py --certify
Dump: research/cycle_sh.json
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
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_qx import want_g_n1
from cycle_sg import want_oo
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
SG_JSON = Path(__file__).resolve().parent / "cycle_sg.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10


def want_n1e(k: int) -> int:
    """Packed rest xor on n%4==1, even j, certified k<=10: 1 iff k not in {3,4,5}."""
    return int(k not in (3, 4, 5))


def even_odd(tot: list[int]) -> tuple[int, int]:
    return tot[0] ^ tot[2], tot[1] ^ tot[3]


def _walk_nmodj(k: int) -> dict:
    """Covering q=10 packed rest xor split by n%4 and j parity."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    tot = [[0, 0] for _ in range(4)]
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                if G(n, j) == 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                if not packed or p in FORCED:
                    continue
                tot[n % 4][j % 2] ^= 1
        row = rule30_step(row)
        s += 1
    n0e, n1e, n2e, n3e = tot[0][0], tot[1][0], tot[2][0], tot[3][0]
    n0o, n1o, n2o, n3o = tot[0][1], tot[1][1], tot[2][1], tot[3][1]
    return {
        "n0e": n0e,
        "n0o": n0o,
        "n1e": n1e,
        "n1o": n1o,
        "n2e": n2e,
        "n2o": n2o,
        "n3e": n3e,
        "n3o": n3o,
        "ee": n0e ^ n2e,
        "oe": n1e ^ n3e,
        "oo": n1o ^ n3o,
        "rest": n0e ^ n1e ^ n1o ^ n2e ^ n3e ^ n3o,
    }


def nmodj_walk() -> dict:
    """k<=10: n0e equals n3e; n1e equals want_n1e; matches QO/SG tots."""
    qo = json.loads(QO_JSON.read_text())
    sg = json.loads(SG_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    sg_rows = sg["jpar_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        w = _walk_nmodj(k)
        tot = rows_in[str(k)]["tot"]
        e, o = even_odd(tot)
        if w["n0o"] != 0 or w["n2o"] != 0:
            return {"ok": False, "even_oddj": True, "k": k, "w": w}
        if w["n0e"] != tot[0] or w["n2e"] != tot[2]:
            return {"ok": False, "even": True, "k": k, "w": w, "tot": tot}
        if (w["n1e"] ^ w["n1o"]) != tot[1]:
            return {"ok": False, "n1": True, "k": k, "w": w, "tot": tot}
        if (w["n3e"] ^ w["n3o"]) != tot[3]:
            return {"ok": False, "n3": True, "k": k, "w": w, "tot": tot}
        if w["n0e"] != w["n3e"]:
            return {"ok": False, "n0_n3e": True, "k": k, "w": w}
        if w["n1e"] != want_n1e(k):
            return {"ok": False, "n1e": True, "k": k, "w": w}
        if w["ee"] != e or w["oe"] != sg_rows[str(k)]["oe"]:
            return {"ok": False, "parity": True, "k": k, "w": w}
        if w["oo"] != want_oo(k) or w["oo"] != sg_rows[str(k)]["oo"]:
            return {"ok": False, "oo": True, "k": k, "w": w}
        if w["rest"] != want_rest_e0(k) or w["rest"] != rows_in[str(k)]["rest"]:
            return {"ok": False, "rest": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {
            "n0e": w["n0e"],
            "n1e": w["n1e"],
            "n1o": w["n1o"],
            "n2e": w["n2e"],
            "n3e": w["n3e"],
            "n3o": w["n3o"],
            "rest": w["rest"],
        }
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["n0e"] == 0
        and rows["2"]["n0e"] == 1
        and rows["0"]["n3e"] == 0
        and rows["2"]["n3e"] == 1
        and rows["10"]["n0e"] == 0
        and rows["10"]["n3e"] == 0
        and rows["0"]["n1e"] == 1
        and rows["3"]["n1e"] == 0
        and rows["4"]["n1e"] == 0
        and rows["5"]["n1e"] == 0
        and rows["6"]["n1e"] == 1
        and rows["10"]["n1e"] == 1
        and rows["1"]["n0e"] != rows_in["1"]["tot"][3]
        and rows["6"]["rest"] == 1
        and rows["10"]["rest"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """want_n1e is 0 only at 3,4,5; n0e equals n3e is not n3 tot."""
    qo = json.loads(QO_JSON.read_text())
    tot1 = qo["rest_n0_walk"]["rows"]["1"]["tot"]
    ok = (
        want_n1e(0) == 1
        and want_n1e(3) == 0
        and want_n1e(4) == 0
        and want_n1e(5) == 0
        and want_n1e(6) == 1
        and want_n1e(10) == 1
        and tot1[0] != tot1[3]
        and want_rest_e0(6) == 1
        and want_rest_e0(10) == 0
    )
    return {"ok": ok, "n0_k1": tot1[0], "n3_k1": tot1[3]}


def killed_eq() -> dict:
    """n0 equals n3 tot; n1e identically 1; n1e equals parent even / Green n1."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n0_1 = rows_in["1"]["tot"][0]
    n3_1 = rows_in["1"]["tot"][3]
    pe_3 = even_odd(rows_in["2"]["tot"])[0]
    ok = (
        n0_1 != n3_1
        and want_n1e(3) == 0
        and want_n1e(3) != pe_3
        and want_n1e(0) != want_g_n1(0)
        and want_n1e(3) != want_g_n1(3)
        and want_n1e(16) == 1
        and want_n1e(4) == 0
    )
    return {"ok": ok, "n0_1": n0_1, "n3_1": n3_1, "pe_3": pe_3}


def prefixes() -> dict:
    qo = json.loads(QO_JSON.read_text())
    qu = json.loads(QU_JSON.read_text())
    sg = json.loads(SG_JSON.read_text())
    ok = (
        qo["checks"]["all_ok"]
        and qu["checks"]["all_ok"]
        and sg["checks"]["all_ok"]
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and sg["verdict"]["packed_oo_eq_want_oo_k_le_10"] == "CERTIFIED"
        and sg["verdict"]["packed_oo_eq_0"] == "KILLED"
        and qu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sg["verdict"]["prize"] == "unsolved"
        and want_n1e(3) == 0
        and want_oo(4) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert walk["ok"] and tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
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
        "cycle": "SH",
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
            "packed_n0_eq_n3e_k_le_10": True,
            "packed_n1e_eq_want_n1e_k_le_10": True,
            "packed_n0_eq_n3e_all_k": False,
            "packed_n1e_all_k": False,
            "packed_n0_eq_n3_tot": False,
            "packed_n1e_eq_1": False,
            "packed_n1e_eq_parent_even": False,
            "packed_n1e_eq_green_n1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "packed_n0_eq_n3e_k_le_10": "CERTIFIED",
            "packed_n1e_eq_want_n1e_k_le_10": "CERTIFIED",
            "packed_n0_eq_n3e_all_k": "PREFIX",
            "packed_n1e_all_k": "PREFIX",
            "packed_n0_eq_n3_tot": "KILLED",
            "packed_n1e_eq_1": "KILLED",
            "packed_n1e_eq_parent_even": "KILLED",
            "packed_n1e_eq_green_n1": "KILLED",
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
        "nmodj n_ok",
        dump["nmodj_walk"]["n_ok"],
        "k0 n0e",
        dump["nmodj_walk"]["rows"]["0"]["n0e"],
        "k3 n1e",
        dump["nmodj_walk"]["rows"]["3"]["n1e"],
        "k10 n1e",
        dump["nmodj_walk"]["rows"]["10"]["n1e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
