#!/usr/bin/env python3
"""Cycle KO: piecewise residues for G(3*2^a-1, d).

For U=2^a and n=3U-1 the XOR of Cycle KN splits by bands:
d<U is 1 iff d%3 != 2; U<=d<3U is 1 iff d%3 != (1 if a even else 0);
3U<=d<5U is f_mod3(d-U); d>=5U is the U..3U rule at d-U. Not the
low-band rule on the whole row; not forbid 2 on the middle band;
not f(d) on [3U,5U); not d%3 on the high band. This is Green-only,
not J. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_ko.py --certify
Dump: research/cycle_ko.json
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
from cycle_an import f_mod3
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_kn import g_tri, g_tri_row

OUT = Path(__file__).resolve().with_suffix(".json")
KN_JSON = Path(__file__).resolve().parent / "cycle_kn.json"

A_MAX = 8


def mid_forbid(a: int) -> int:
    """Zero residue on U<=d<3U: 1 if a even, else 0."""
    return 1 if a % 2 == 0 else 0


def g_tri_piece(a: int, d: int) -> int:
    """Piecewise G(3*2^a-1, d) by residue bands."""
    U = 1 << a
    n = 3 * U - 1
    if d < 0 or d > 2 * n:
        return 0
    if d < U:
        return int(d % 3 != 2)
    if d < 3 * U:
        return int(d % 3 != mid_forbid(a))
    if d < 5 * U:
        return f_mod3(d - U)
    return int((d - U) % 3 != mid_forbid(a))


def piece_table() -> dict:
    """a<=8: piecewise matches G, g_tri, and g_tri_row."""
    n_a = n_ok = 0
    ns = []
    for a in range(0, A_MAX + 1):
        n = 3 * (1 << a) - 1
        ns.append(n)
        for d in range(0, 2 * n + 1):
            got = G(n, d)
            piece = g_tri_piece(a, d)
            if piece != got or piece != g_tri(a, d) or piece != g_tri_row(a, d):
                return {
                    "ok": False,
                    "g": True,
                    "a": a,
                    "n": n,
                    "d": d,
                    "got": got,
                    "piece": piece,
                    "tri": g_tri(a, d),
                }
            n_ok += 1
        n_a += 1
    ok = (
        n_a == A_MAX + 1
        and ns[0] == 2
        and ns[1] == 5
        and ns[8] == 767
        and g_tri_piece(1, 0) == 1
        and g_tri_piece(1, 2) == 1
        and g_tri_piece(1, 3) == 0
        and g_tri_piece(1, 7) == 0
        and g_tri_piece(2, 20) == 0
        and mid_forbid(0) == 1
        and mid_forbid(1) == 0
        and mid_forbid(2) == 1
    )
    return {"ok": ok, "n_a": n_a, "n_ok": n_ok, "n": ns}


def killed_all_not2() -> dict:
    """Whole row is 1 iff d%3 != 2: n=5 d=2 is 1."""
    n, d = 5, 2
    got = G(n, d)
    ok = got == 1 and d % 3 == 2 and g_tri_piece(1, d) == 1
    return {"ok": ok, "n": n, "d": d, "G": got}


def killed_mid_forbid2() -> dict:
    """Middle band U<=d<3U zeros at d%3==2: n=5 d=2 is 1."""
    a, d = 1, 2
    n = 3 * (1 << a) - 1
    U = 1 << a
    got = G(n, d)
    ok = (
        n == 5
        and U <= d < 3 * U
        and d % 3 == 2
        and got == 1
        and mid_forbid(a) == 0
        and g_tri_piece(a, d) == 1
    )
    return {"ok": ok, "n": n, "d": d, "G": got, "forbid": mid_forbid(a)}


def killed_band_f_d() -> dict:
    """Band [3U,5U) equals f(d): n=5 d=7 is 0 vs f(7)=1."""
    a, d = 1, 7
    n = 3 * (1 << a) - 1
    U = 1 << a
    got, f = G(n, d), f_mod3(d)
    ok = (
        n == 5
        and 3 * U <= d < 5 * U
        and got == 0
        and f == 1
        and got != f
        and g_tri_piece(a, d) == 0
        and f_mod3(d - U) == 0
    )
    return {"ok": ok, "n": n, "d": d, "G": got, "f": f}


def killed_hi_d_mod() -> dict:
    """High band d>=5U uses d%3: n=11 d=20 is 0 vs (d%3)!=1."""
    a, d = 2, 20
    n = 3 * (1 << a) - 1
    U = 1 << a
    got = G(n, d)
    wrong = int(d % 3 != mid_forbid(a))
    ok = (
        n == 11
        and d >= 5 * U
        and got == 0
        and wrong == 1
        and got != wrong
        and g_tri_piece(a, d) == 0
        and (d - U) % 3 == mid_forbid(a)
    )
    return {"ok": ok, "n": n, "d": d, "G": got, "d_mod": wrong}


def prefixes() -> dict:
    kn = json.loads(KN_JSON.read_text())
    ok = (
        kn["checks"]["all_ok"]
        and kn["verdict"]["g_tri_closed"] == "LEMMA"
        and kn["verdict"]["g_tri_row_no6U"] == "LEMMA"
        and kn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert g_tri_piece(0, 1) == G(2, 1) == 0
    assert g_tri_piece(3, 0) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = piece_table()
    sc = g4_xor_cover()
    k0 = killed_all_not2()
    k1 = killed_mid_forbid2()
    k2 = killed_band_f_d()
    k3 = killed_hi_d_mod()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "piece_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_not2": {k: k0[k] for k in k0 if k != "ok"},
        "killed_mid_forbid2": {k: k1[k] for k in k1 if k != "ok"},
        "killed_band_f_d": {k: k2[k] for k in k2 if k != "ok"},
        "killed_hi_d_mod": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "g_tri_piece": True,
            "g_tri_closed": True,
            "g_tri_row_no6U": True,
            "g_tri_all_not2": False,
            "g_tri_mid_forbid2": False,
            "g_tri_band_f_d": False,
            "g_tri_hi_d_mod": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g_tri_piece": "LEMMA",
            "g_tri_closed": "LEMMA",
            "g_tri_row_no6U": "LEMMA",
            "g_tri_all_not2": "KILLED",
            "g_tri_mid_forbid2": "KILLED",
            "g_tri_band_f_d": "KILLED",
            "g_tri_hi_d_mod": "KILLED",
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
    print("piece_table", dump["piece_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_not2", dump["killed_all_not2"])
    print("killed_mid_forbid2", dump["killed_mid_forbid2"])
    print("killed_band_f_d", dump["killed_band_f_d"])
    print("killed_hi_d_mod", dump["killed_hi_d_mod"])


if __name__ == "__main__":
    main()
