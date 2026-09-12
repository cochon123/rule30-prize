#!/usr/bin/env python3
"""Cycle KB: G=1 DIE 1111 hits all four g1_green4 shapes.

Trinomial AND's extra term 1111 occurs on isolated ones, all three
pair kinds, centers, and both n-parities. It is not only G=0; not
only isolated; not a function of green4. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kb.py --certify
Dump: research/cycle_kb.json
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
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_ig import g1_green4
from cycle_in import g_run_kind
from cycle_ir import isolated_one
from cycle_ka import DIE1111
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KA_JSON = Path(__file__).resolve().parent / "cycle_ka.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

G1_SHAPES = ("0110", "0111", "1010", "1011")
KINDS = ("left", "right", "iso")


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def die_g4_table() -> dict:
    """n<64: every G=1 green4 is one of the four g1_green4 shapes."""
    n_g1 = {sh: 0 for sh in G1_SHAPES}
    n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            g4 = green4(n, j)
            if g4 != g1_green4(n, j):
                return {"ok": False, "g4": True, "n": n, "j": j}
            key = _fmt(g4)
            if key not in n_g1:
                return {"ok": False, "extra": True, "n": n, "j": j, "g4": key}
            n_g1[key] += 1
            if isolated_one(n, j):
                n_iso += 1
                if g4 != (0, 1, 1, 1):
                    return {"ok": False, "iso": True, "n": n, "j": j}
    n_tot = sum(n_g1.values())
    ok = n_tot == 1344 and n_iso == 461 and n_g1["0111"] == 461
    return {"ok": ok, "n_g1": n_g1, "n_iso": n_iso, "n_tot": n_tot}


def _walk_die(k: int, q: int) -> dict:
    """G=1 1111 census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_die = n_die_g0 = n_iso = n_ctr = n_even = n_odd = 0
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
                    if four == DIE1111:
                        n_die += 1
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
                elif four == DIE1111:
                    n_die_g0 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_die": n_die,
        "n_die_g0": n_die_g0,
        "n_iso": n_iso,
        "n_ctr": n_ctr,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_g4": n_g4,
        "n_kind": n_kind,
        "xor_j": xor_j,
    }


def die_g1_cover() -> dict:
    """G=1 1111 census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_die = n_die_g0 = n_iso = n_ctr = n_even = n_odd = 0
    n_g4 = {sh: 0 for sh in G1_SHAPES}
    n_kind = {kind: 0 for kind in KINDS}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_die(k, q)
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
            n_die += w["n_die"]
            n_die_g0 += w["n_die_g0"]
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
                "n_die": w["n_die"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_die == 1167
        and n_die_g0 == 3614
        and n_iso == 359
        and n_ctr == 30
        and n_even == 285
        and n_odd == 882
        and n_g4["0111"] == 359
        and n_g4["1011"] == 361
        and n_g4["0110"] == 313
        and n_g4["1010"] == 134
        and n_kind["left"] == 98
        and n_kind["right"] == 134
        and n_kind["iso"] == 263
        and n_die == sum(n_g4.values())
        and n_die == n_even + n_odd
        and all(n_g4[sh] > 0 for sh in G1_SHAPES)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_die": n_die,
        "n_die_g0": n_die_g0,
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
    """1111 only on G=0: G(1,2) is 1111."""
    k, s, n, j, p, four = _kill_four(1, 17, 1, 2, 16)
    ok = (
        G(n, j) == 1
        and four == DIE1111
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
    """1111 only isolated: G(9,16) is left of a triple."""
    k, s, n, j, p, four = _kill_four(3, 29, 9, 16, 16)
    ok = (
        G(n, j) == 1
        and four == DIE1111
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
    """1111 is a function of green4: isolated G(4,0) is 1111 vs 0111."""
    k, s, n, j, p, four = _kill_four(2, 31, 4, 0, 40)
    g4 = green4(n, j)
    ok = (
        isolated_one(n, j)
        and four == DIE1111
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
    ka = json.loads(KA_JSON.read_text())
    ok = (
        ka["checks"]["all_ok"]
        and ka["verdict"]["covering_packed_ne_tri"] == "LEMMA"
        and ka["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert DIE1111 == (1, 1, 1, 1)
    assert g1_green4(0, 0) == (0, 1, 1, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = die_g4_table()
    sc = die_g1_cover()
    k0 = killed_only_g0()
    k1 = killed_only_iso()
    k2 = killed_fn_of_g4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "die_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "die_g1_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_only_g0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_only_iso": {k: k1[k] for k in k1 if k != "ok"},
        "killed_fn_of_g4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g1_four_shapes": True,
            "die_g1_all_shapes": True,
            "covering_die_g1": True,
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
            "die_g1_all_shapes": "LEMMA",
            "covering_die_g1": "LEMMA",
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
    cov = dump["die_g1_cover"]
    print(
        "die_g1_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_die",
        cov["n_die"],
        "n_die_g0",
        cov["n_die_g0"],
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
