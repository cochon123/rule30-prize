#!/usr/bin/env python3
"""Cycle SG: packed rest on odd n, odd j is 1 iff k in {4,9,10} through k<=10.

Covering packed rest cells split by n parity and j parity. Even-n
G=1 lives only on even j (Cycle QV). Odd-n odd-j packed rest xor
is 1 iff k in {4,9,10} through k<=10, so odd-n even-j tot equals
odd rest xor that bit. Cycle SD consecutive Green AND xor on G=1
odd-j covering is 0 through k<=8, so packed odd-j tot is not that
Green tot (k=4 is 1 vs 0). Not the exception set for all k. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sg.py --certify
Dump: research/cycle_sg.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QU_JSON = Path(__file__).resolve().parent / "cycle_qu.json"
SD_JSON = Path(__file__).resolve().parent / "cycle_sd.json"
SF_JSON = Path(__file__).resolve().parent / "cycle_sf.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10


def want_oo(k: int) -> int:
    """Packed rest xor on odd n, odd j, certified k<=10: 1 iff k in {4,9,10}."""
    return int(k in (4, 9, 10))


def even_odd(tot: list[int]) -> tuple[int, int]:
    return tot[0] ^ tot[2], tot[1] ^ tot[3]


def _walk_jpar(k: int) -> dict:
    """Covering q=10 packed rest xor split by n parity and j parity."""
    U = 1 << k
    q = 10
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    ee = oe = oo = 0
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
                if n % 2 == 0:
                    ee ^= 1
                elif j % 2 == 0:
                    oe ^= 1
                else:
                    oo ^= 1
        row = rule30_step(row)
        s += 1
    rest = ee ^ oe ^ oo
    return {"ee": ee, "oe": oe, "oo": oo, "rest": rest}


def jpar_walk() -> dict:
    """k<=10: odd-n odd-j packed rest xor equals want_oo; matches QO parity tots."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        w = _walk_jpar(k)
        tot = rows_in[str(k)]["tot"]
        e, o = even_odd(tot)
        if w["ee"] != e:
            return {"ok": False, "ee": True, "k": k, "w": w, "e": e}
        if (w["oe"] ^ w["oo"]) != o:
            return {"ok": False, "odd": True, "k": k, "w": w, "o": o}
        if w["oo"] != want_oo(k):
            return {"ok": False, "oo": True, "k": k, "w": w}
        if w["oe"] != (o ^ want_oo(k)):
            return {"ok": False, "oe": True, "k": k, "w": w, "o": o}
        if w["rest"] != want_rest_e0(k) or w["rest"] != rows_in[str(k)]["rest"]:
            return {"ok": False, "rest": True, "k": k, "w": w}
        n_ok += 1
        rows[str(k)] = {
            "ee": w["ee"],
            "oe": w["oe"],
            "oo": w["oo"],
            "rest": w["rest"],
        }
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["oo"] == 0
        and rows["4"]["oo"] == 1
        and rows["8"]["oo"] == 0
        and rows["9"]["oo"] == 1
        and rows["10"]["oo"] == 1
        and rows["4"]["oe"] == 1
        and rows["6"]["rest"] == 1
        and rows["10"]["rest"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def tot_form() -> dict:
    """want_oo is 1 only at 4,9,10; oe is odd rest xor that bit."""
    ok = (
        want_oo(4) == 1
        and want_oo(9) == 1
        and want_oo(10) == 1
        and want_oo(0) == 0
        and want_oo(8) == 0
        and want_oo(2) == 0
        and want_rest_e0(4) == 0
        and want_rest_e0(10) == 0
    )
    return {"ok": ok}


def killed_eq() -> dict:
    """Exception set for all k; oo=0; packed oo equals SD consecutive AND xor."""
    sd = json.loads(SD_JSON.read_text())
    n_and4 = sd["covering_chk"]["rows"]["4"]["n_and"]
    n_and0 = sd["covering_chk"]["rows"]["0"]["n_and"]
    ok = (
        want_oo(4) == 1
        and (n_and4 % 2) == 0
        and (n_and0 % 2) == 0
        and want_oo(4) != (n_and4 % 2)
        and want_oo(9) == 1
        and want_oo(3) == 0
        and want_oo(8) == 0
    )
    return {"ok": ok, "sd_n_and4": n_and4, "sd_n_and0": n_and0}


def prefixes() -> dict:
    qo = json.loads(QO_JSON.read_text())
    qu = json.loads(QU_JSON.read_text())
    sd = json.loads(SD_JSON.read_text())
    sf = json.loads(SF_JSON.read_text())
    ok = (
        qo["checks"]["all_ok"]
        and qu["checks"]["all_ok"]
        and sd["checks"]["all_ok"]
        and sf["checks"]["all_ok"]
        and qu["verdict"]["even_rest_eq_parent_odd_k_le_10"] == "CERTIFIED"
        and sd["verdict"]["odd_g1_oddj_cons_AND_iff_0011"] == "LEMMA"
        and sf["verdict"]["odd_child_oddj_cons_AND_iff_0011"] == "LEMMA"
        and qu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sf["verdict"]["prize"] == "unsolved"
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
    walk = jpar_walk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "SG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "jpar_walk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "packed_oo_eq_want_oo_k_le_10": True,
            "packed_oe_eq_odd_rest_xor_oo_k_le_10": True,
            "packed_oo_all_k": False,
            "packed_oo_eq_0": False,
            "packed_oo_eq_SD_cons_AND_xor": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "packed_oo_eq_want_oo_k_le_10": "CERTIFIED",
            "packed_oe_eq_odd_rest_xor_oo_k_le_10": "CERTIFIED",
            "packed_oo_all_k": "PREFIX",
            "packed_oo_eq_0": "KILLED",
            "packed_oo_eq_SD_cons_AND_xor": "KILLED",
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
        "jpar n_ok",
        dump["jpar_walk"]["n_ok"],
        "k4 oo",
        dump["jpar_walk"]["rows"]["4"]["oo"],
        "k10 oo",
        dump["jpar_walk"]["rows"]["10"]["oo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
