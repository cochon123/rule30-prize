#!/usr/bin/env python3
"""Cycle KD: G=1 CONT 0011 hits all four g1_green4 shapes.

Packed AND's extra term CONT occurs on isolated ones, all three
pair kinds, centers, and both n-parities. It is not only G=0; not
only isolated; not a function of green4. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kd.py --certify
Dump: research/cycle_kd.json
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
from cycle_hi import CONT
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_ig import g1_green4
from cycle_in import g_run_kind
from cycle_ir import isolated_one
from cycle_kb import G1_SHAPES, KINDS, die_g4_table
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KC_JSON = Path(__file__).resolve().parent / "cycle_kc.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def _walk_cont(k: int, q: int) -> dict:
    """G=1 CONT census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_cont = n_cont_g0 = n_iso = n_ctr = n_even = n_odd = 0
    n_g4 = {sh: 0 for sh in G1_SHAPES}
    n_kind = {kind: 0 for kind in KINDS}
    xor_j = 0
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
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
                    if four == CONT:
                        n_cont += 1
                        key = _fmt(green4(n, j))
                        n_g4[key] += 1
                        if isolated_one(n, j):
                            n_iso += 1
                        if j == n:
                            n_ctr += 1
                        if n % 2 == 0:
                            n_even += 1
                        else:
                            n_odd += 1
                        if j < 2 * n:
                            kind = g_run_kind(n, j)
                            if kind is not None:
                                n_kind[kind] += 1
                elif four == CONT:
                    n_cont_g0 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_cont": n_cont,
        "n_cont_g0": n_cont_g0,
        "n_iso": n_iso,
        "n_ctr": n_ctr,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_g4": n_g4,
        "n_kind": n_kind,
        "xor_j": xor_j,
    }


def cont_g1_cover() -> dict:
    """G=1 CONT census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_cont = n_cont_g0 = n_iso = n_ctr = n_even = n_odd = 0
    n_g4 = {sh: 0 for sh in G1_SHAPES}
    n_kind = {kind: 0 for kind in KINDS}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_cont(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_cont += w["n_cont"]
            n_cont_g0 += w["n_cont_g0"]
            n_iso += w["n_iso"]
            n_ctr += w["n_ctr"]
            n_even += w["n_even"]
            n_odd += w["n_odd"]
            for sh in G1_SHAPES:
                n_g4[sh] += w["n_g4"][sh]
            for kind in KINDS:
                n_kind[kind] += w["n_kind"][kind]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_cont": w["n_cont"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_cont == 1146
        and n_cont_g0 == 3829
        and n_iso == 343
        and n_ctr == 53
        and n_even == 279
        and n_odd == 867
        and n_g4["0111"] == 343
        and n_g4["1011"] == 288
        and n_g4["0110"] == 364
        and n_g4["1010"] == 151
        and n_kind["left"] == 89
        and n_kind["right"] == 151
        and n_kind["iso"] == 199
        and n_cont == sum(n_g4.values())
        and n_cont == n_even + n_odd
        and n_iso == n_g4["0111"]
        and all(n_g4[sh] > 0 for sh in G1_SHAPES)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_cont": n_cont,
        "n_cont_g0": n_cont_g0,
        "n_iso": n_iso,
        "n_ctr": n_ctr,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_g4": n_g4,
        "n_kind": n_kind,
        "rows": rows,
    }


def _kill_four(k: int, s_hit: int, n_hit: int, j_hit: int, p_hit: int):
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p_hit - 3 + i) for i in range(4))
    return k, s_hit, n_hit, j_hit, p_hit, four


def killed_only_g0() -> dict:
    """CONT only on G=0: G(3,1) is CONT."""
    k, s, n, j, p, four = _kill_four(1, 13, 3, 1, 18)
    ok = (
        G(n, j) == 1
        and four == CONT
        and green4(n, j) == g1_green4(n, j) == (0, 1, 1, 0)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(green4(n, j)),
    }


def killed_only_iso() -> dict:
    """CONT only isolated: G(9,8) is left of a triple."""
    k, s, n, j, p, four = _kill_four(3, 61, 9, 8, 64)
    ok = (
        G(n, j) == 1
        and four == CONT
        and g_run_kind(n, j) == "left"
        and (not isolated_one(n, j))
        and green4(n, j) == (1, 0, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(green4(n, j)),
    }


def killed_fn_of_g4() -> dict:
    """CONT is a function of green4: isolated G(3,3) is CONT vs 0111."""
    k, s, n, j, p, four = _kill_four(1, 13, 3, 3, 14)
    g4 = green4(n, j)
    ok = (
        isolated_one(n, j)
        and four == CONT
        and g4 == (0, 1, 1, 1)
        and four != g4
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
    }


def prefixes() -> dict:
    kc = json.loads(KC_JSON.read_text())
    ok = (
        kc["checks"]["all_ok"]
        and kc["verdict"]["covering_dual_extra"] == "LEMMA"
        and kc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert CONT == (0, 0, 1, 1)
    assert and_clause(*CONT) == 1
    assert g1_green4(0, 0) == (0, 1, 1, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = die_g4_table()
    sc = cont_g1_cover()
    k0 = killed_only_g0()
    k1 = killed_only_iso()
    k2 = killed_fn_of_g4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "die_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "cont_g1_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_only_g0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_only_iso": {k: k1[k] for k in k1 if k != "ok"},
        "killed_fn_of_g4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g1_four_shapes": True,
            "cont_g1_all_shapes": True,
            "covering_cont_g1": True,
            "only_g0": False,
            "only_iso": False,
            "fn_of_g4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g1_four_shapes": "LEMMA",
            "cont_g1_all_shapes": "LEMMA",
            "covering_cont_g1": "LEMMA",
            "only_g0": "KILLED",
            "only_iso": "KILLED",
            "fn_of_g4": "KILLED",
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
    print("die_g4_table", dump["die_g4_table"])
    cov = dump["cont_g1_cover"]
    print(
        "cont_g1_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_cont",
        cov["n_cont"],
        "n_cont_g0",
        cov["n_cont_g0"],
        "n_iso",
        cov["n_iso"],
        "n_ctr",
        cov["n_ctr"],
        "n_g4",
        cov["n_g4"],
        "n_kind",
        cov["n_kind"],
    )
    print("killed_only_g0", dump["killed_only_g0"])
    print("killed_only_iso", dump["killed_only_iso"])
    print("killed_fn_of_g4", dump["killed_fn_of_g4"])


if __name__ == "__main__":
    main()
