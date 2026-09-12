#!/usr/bin/env python3
"""Cycle HY: mixed cob/non-cob pairs contribute one-sided non-cob AND.

If exactly one dual 4-tuple is coboundary-shaped, cob AND is 0 so
the pair XOR equals the non-cob AND. Covering J is then center AND
XOR that mixed slice XOR both-non-cob AND disagreements. Mixed cob
is not always the left column; mixed non-cob is not always AND;
both-non-cob XOR is not 4-tuple inequality. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hy.py --certify
Dump: research/cycle_hy.json
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
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HX_JSON = Path(__file__).resolve().parent / "cycle_hx.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def mixed_oneside(four, four2) -> int:
    """Non-cob AND if mixed cob/non-cob; else -1."""
    c1, c2 = cob_shaped(*four), cob_shaped(*four2)
    if c1 == c2:
        return -1
    return and_clause(*(four2 if c1 else four))


def mixed_oneside_table() -> dict:
    """16x16: mixed XOR equals non-cob AND; cob AND is 0."""
    n_ok = n_mix = 0
    for b1 in range(16):
        four = tuple((b1 >> i) & 1 for i in range(3, -1, -1))
        for b2 in range(16):
            four2 = tuple((b2 >> i) & 1 for i in range(3, -1, -1))
            c1, c2 = cob_shaped(*four), cob_shaped(*four2)
            a, b = and_clause(*four), and_clause(*four2)
            mo = mixed_oneside(four, four2)
            n_ok += 1
            if c1 != c2:
                n_mix += 1
                cob_and = a if c1 else b
                nc = b if c1 else a
                if cob_and or mo != (a ^ b) or mo != nc:
                    return {
                        "ok": False,
                        "mix": True,
                        "four": four,
                        "four2": four2,
                        "mo": mo,
                    }
            elif mo != -1:
                return {"ok": False, "nonmix": True, "four": four, "four2": four2}
    ok = n_ok == 256 and n_mix == 128
    return {"ok": ok, "n_ok": n_ok, "n_mix": n_mix}


def _walk_mix(k: int, q: int) -> dict:
    """J = center XOR mixed oneside XOR both-non-cob AND xor."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_center = n_center_and = 0
    n_bothcob = n_mix = n_mix_xor = n_bn = n_bn_xor = 0
    xor_j = xor_c = xor_m = xor_b = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                if packed != and_clause(*four):
                    return {"ok": False, "pack": True, "k": k, "four": four}
                bits[j] = (four, packed, p)
                n_ok += 1
                if packed and G(n, j):
                    xor_j ^= 1
            if n in bits:
                n_center += 1
                if bits[n][1]:
                    n_center_and += 1
                    xor_c ^= 1
            for j in range(0, n):
                j2 = 2 * n - j
                if j not in bits or j2 not in bits:
                    continue
                if G(n, j) == 0:
                    continue
                f, a, p = bits[j]
                g, b, p2 = bits[j2]
                n_pair += 1
                c1, c2 = cob_shaped(*f), cob_shaped(*g)
                mo = mixed_oneside(f, g)
                if c1 != c2:
                    n_mix += 1
                    if mo != (a ^ b):
                        return {
                            "ok": False,
                            "oneside": True,
                            "k": k,
                            "four": f,
                            "four2": g,
                        }
                    if a ^ b:
                        n_mix_xor += 1
                        xor_m ^= 1
                elif c1 and c2:
                    n_bothcob += 1
                    if a or b or mo != -1:
                        return {"ok": False, "bothcob": True, "k": k, "four": f}
                else:
                    n_bn += 1
                    if mo != -1:
                        return {"ok": False, "bn": True, "k": k, "four": f}
                    if a ^ b:
                        n_bn_xor += 1
                        xor_b ^= 1
        row = rule30_step(row)
        s += 1
    xor_fold = xor_c ^ xor_m ^ xor_b
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_center": n_center,
        "n_center_and": n_center_and,
        "n_bothcob": n_bothcob,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_bn": n_bn,
        "n_bn_xor": n_bn_xor,
        "xor_j": xor_j,
        "xor_fold": xor_fold,
    }


def mix_cover() -> dict:
    """Mixed oneside / J split on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_center = n_center_and = 0
    n_bothcob = n_mix = n_mix_xor = n_bn = n_bn_xor = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_mix(k, q)
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
            n_pair += w["n_pair"]
            n_center += w["n_center"]
            n_center_and += w["n_center_and"]
            n_bothcob += w["n_bothcob"]
            n_mix += w["n_mix"]
            n_mix_xor += w["n_mix_xor"]
            n_bn += w["n_bn"]
            n_bn_xor += w["n_bn_xor"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_pair": w["n_pair"],
                "n_mix": w["n_mix"],
                "n_mix_xor": w["n_mix_xor"],
                "n_bn": w["n_bn"],
                "n_bn_xor": w["n_bn_xor"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_center == 762
        and n_center_and == 232
        and n_bothcob == 2438
        and n_mix == 4383
        and n_mix_xor == 2216
        and n_bn == 2123
        and n_bn_xor == 1030
        and n_bothcob + n_mix + n_bn == n_pair
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_center": n_center,
        "n_center_and": n_center_and,
        "n_bothcob": n_bothcob,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_bn": n_bn,
        "n_bn_xor": n_bn_xor,
        "rows": rows,
    }


def killed_mix_cob_always_left() -> dict:
    """Mixed cob is not always the left column: k=1, s=13, n=3, 0011 vs 0111."""
    k, s, n, j, j2, p, p2 = 1, 13, 3, 1, 5, 18, 10
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (0, 0, 1, 1)
        and four2 == (0, 1, 1, 1)
        and (not cob_shaped(*four))
        and cob_shaped(*four2)
        and mixed_oneside(four, four2) == 1
        and j2 == 2 * n - j
        and G(n, j) == 1
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "four": list(four),
        "four2": list(four2),
    }


def killed_mix_nc_always_and() -> dict:
    """Mixed non-cob is not always AND: k=2, s=17, n=11, 1000 vs 0001."""
    k, s, n, j, j2, p, p2 = 2, 17, 11, 6, 16, 28, 8
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (1, 0, 0, 0)
        and four2 == (0, 0, 0, 1)
        and (not cob_shaped(*four))
        and cob_shaped(*four2)
        and mixed_oneside(four, four2) == 0
        and and_clause(*four) == 0
        and j2 == 2 * n - j
        and G(n, j) == 1
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "four": list(four),
        "four2": list(four2),
    }


def killed_bn_xor_eq_neq() -> dict:
    """Both-non-cob AND xor is not 4-tuple inequality: k=0, s=7, n=1, 0010 vs 0100."""
    k, s, n, j, j2, p, p2 = 0, 7, 1, 0, 2, 10, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    a, b = and_clause(*four), and_clause(*four2)
    ok = (
        four == (0, 0, 1, 0)
        and four2 == (0, 1, 0, 0)
        and (not cob_shaped(*four))
        and (not cob_shaped(*four2))
        and a == 1
        and b == 1
        and (a ^ b) == 0
        and four != four2
        and mixed_oneside(four, four2) == -1
        and j2 == 2 * n - j
        and G(n, j) == 1
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "four": list(four),
        "four2": list(four2),
        "a": a,
        "b": b,
    }


def prefixes() -> dict:
    hx = json.loads(HX_JSON.read_text())
    ok = (
        hx["checks"]["all_ok"]
        and hx["verdict"]["both_cob_pairs_AND_xor_0"] == "LEMMA"
        and hx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, mc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and mc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert mixed_oneside((0, 0, 1, 1), (0, 1, 1, 1)) == 1
    assert mixed_oneside((0, 0, 1, 0), (0, 1, 0, 0)) == -1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mixed_oneside_table()
    mc = mix_cover()
    k0 = killed_mix_cob_always_left()
    k1 = killed_mix_nc_always_and()
    k2 = killed_bn_xor_eq_neq()
    pref = prefixes()
    checks = self_checks(c20, rt, mc, k0, k1, k2, pref)
    dump = {
        "cycle": "HY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mixed_oneside_table": {k: rt[k] for k in rt if k != "ok"},
        "mix_cover": {k: mc[k] for k in mc if k != "ok"},
        "killed_mix_cob_always_left": {k: k0[k] for k in k0 if k != "ok"},
        "killed_mix_nc_always_and": {k: k1[k] for k in k1 if k != "ok"},
        "killed_bn_xor_eq_neq": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "mixed_oneside_AND_xor": True,
            "covering_J_eq_center_XOR_mix_XOR_bn": True,
            "mixed_cob_AND_0": True,
            "mix_cob_always_left": False,
            "mix_nc_always_and": False,
            "bn_xor_eq_neq": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mixed_oneside_AND_xor": "LEMMA",
            "covering_J_eq_center_XOR_mix_XOR_bn": "LEMMA",
            "mixed_cob_AND_0": "LEMMA",
            "mix_cob_always_left": "KILLED",
            "mix_nc_always_and": "KILLED",
            "bn_xor_eq_neq": "KILLED",
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
    print("mixed_oneside_table", dump["mixed_oneside_table"])
    cov = dump["mix_cover"]
    print(
        "mix_cover n_ok",
        cov["n_ok"],
        "n_pair",
        cov["n_pair"],
        "n_mix",
        cov["n_mix"],
        "n_mix_xor",
        cov["n_mix_xor"],
        "n_bn",
        cov["n_bn"],
        "n_bn_xor",
        cov["n_bn_xor"],
        "n_center_and",
        cov["n_center_and"],
    )
    print("killed_mix_cob_always_left", dump["killed_mix_cob_always_left"])
    print("killed_mix_nc_always_and", dump["killed_mix_nc_always_and"])
    print("killed_bn_xor_eq_neq", dump["killed_bn_xor_eq_neq"])


if __name__ == "__main__":
    main()
