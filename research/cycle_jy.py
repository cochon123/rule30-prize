#!/usr/bin/env python3
"""Cycle JY: covering center packed 4-tuples take all 16 values.

G(n,n)=1. Covering packed centers hit every 16-row on both w=0
isolated centers and w=1 run-3 middles; AND fires all four AND_ONES.
Center packed is not always green4; not always cob; center AND does
not vanish. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_jy.py --certify
Dump: research/cycle_jy.json
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
from cycle_al import G, v2
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import AND_ONES, bit_at
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from cycle_if import center_green4
from cycle_ir import isolated_one
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JX_JSON = Path(__file__).resolve().parent / "cycle_jx.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def center_g4_table() -> dict:
    """n<64: center green4 is center_green4; isolated iff w=0."""
    n_ctr = n_iso = n_mid = n_seed = 0
    for n in range(0, 64):
        w = v2(n + 1) & 1
        g4 = green4(n, n)
        iso = isolated_one(n, n)
        if g4 != center_green4(n) or iso != (w == 0) or G(n, n) != 1:
            return {
                "ok": False,
                "miss": True,
                "n": n,
                "g4": list(g4),
                "w": w,
                "iso": iso,
            }
        n_ctr += 1
        if iso:
            n_iso += 1
        else:
            n_mid += 1
        if n == 0:
            n_seed += 1
    ok = n_ctr == 64 and n_iso == 43 and n_mid == 21 and n_seed == 1
    return {
        "ok": ok,
        "n_ctr": n_ctr,
        "n_iso": n_iso,
        "n_mid": n_mid,
        "n_seed": n_seed,
    }


def _walk_center(k: int, q: int) -> dict:
    """Center packed 4-tuple census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_ctr = n_and = n_cob = n_0000 = n_g4 = 0
    n_iso = n_mid = 0
    n_and_ones = {four: 0 for four in AND_ONES}
    types = set()
    iso_t = set()
    mid_t = set()
    w0_t = set()
    w1_t = set()
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
                if j != n:
                    continue
                n_ctr += 1
                types.add(four)
                w = v2(n + 1) & 1
                (w0_t if w == 0 else w1_t).add(four)
                if isolated_one(n, n):
                    n_iso += 1
                    iso_t.add(four)
                else:
                    n_mid += 1
                    mid_t.add(four)
                if four == (0, 0, 0, 0):
                    n_0000 += 1
                if cob_shaped(*four):
                    n_cob += 1
                if four == green4(n, n):
                    n_g4 += 1
                if packed:
                    n_and += 1
                    n_and_ones[four] += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ctr": n_ctr,
        "n_and": n_and,
        "n_cob": n_cob,
        "n_0000": n_0000,
        "n_g4": n_g4,
        "n_iso": n_iso,
        "n_mid": n_mid,
        "n_and_ones": {_fmt(f): n_and_ones[f] for f in AND_ONES},
        "n_types": len(types),
        "n_iso_types": len(iso_t),
        "n_mid_types": len(mid_t),
        "n_w0_types": len(w0_t),
        "n_w1_types": len(w1_t),
        "types": [_fmt(f) for f in sorted(types)],
        "iso_types": [_fmt(f) for f in sorted(iso_t)],
        "mid_types": [_fmt(f) for f in sorted(mid_t)],
        "xor_j": xor_j,
    }


def center_four_cover() -> dict:
    """Center 4-tuple census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_ctr = n_and = n_cob = n_0000 = n_g4 = 0
    n_iso = n_mid = 0
    n_and_ones = {_fmt(f): 0 for f in AND_ONES}
    types = set()
    iso_t = set()
    mid_t = set()
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_center(k, q)
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
            n_ctr += w["n_ctr"]
            n_and += w["n_and"]
            n_cob += w["n_cob"]
            n_0000 += w["n_0000"]
            n_g4 += w["n_g4"]
            n_iso += w["n_iso"]
            n_mid += w["n_mid"]
            for key, val in w["n_and_ones"].items():
                n_and_ones[key] += val
            types.update(w["types"])
            iso_t.update(w["iso_types"])
            mid_t.update(w["mid_types"])
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_ctr": w["n_ctr"],
                "n_and": w["n_and"],
                "n_types": w["n_types"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_ctr == 762
        and n_and == 232
        and n_0000 == 50
        and n_g4 == 32
        and n_iso == 508
        and n_mid == 254
        and n_and_ones["0010"] == 85
        and n_and_ones["0011"] == 53
        and n_and_ones["0100"] == 68
        and n_and_ones["1001"] == 26
        and n_and == sum(n_and_ones.values())
        and len(types) == 16
        and len(iso_t) == 16
        and len(mid_t) == 16
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ctr": n_ctr,
        "n_and": n_and,
        "n_cob": n_cob,
        "n_0000": n_0000,
        "n_g4": n_g4,
        "n_iso": n_iso,
        "n_mid": n_mid,
        "n_and_ones": n_and_ones,
        "n_types": len(types),
        "n_iso_types": len(iso_t),
        "n_mid_types": len(mid_t),
        "rows": rows,
    }


def _kill_center():
    """Packed center at k=0, s=3, n=1, j=1, p=4."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    row = 1
    prev = None
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    return k, s, n, j, p, four


def killed_always_green4() -> dict:
    """Center packed always equals green4: G(1,1) is 1001 vs 1010."""
    k, s, n, j, p, four = _kill_center()
    g4 = green4(n, n)
    ok = (
        j == n
        and G(n, n) == 1
        and g4 == center_green4(n) == (1, 0, 1, 0)
        and four == (1, 0, 0, 1)
        and four != g4
        and and_clause(*four) == 1
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


def killed_always_cob() -> dict:
    """Center packed is always cob: G(1,1) 1001 is not cob-shaped."""
    k, s, n, j, p, four = _kill_center()
    ok = (
        j == n
        and four == (1, 0, 0, 1)
        and (not cob_shaped(*four))
        and four != green4(n, n)
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
    }


def killed_and_vanishes() -> dict:
    """Center AND vanishes: G(1,1) 1001 is in AND_ONES."""
    k, s, n, j, p, four = _kill_center()
    ok = (
        j == n
        and four in AND_ONES
        and and_clause(*four) == 1
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
    }


def prefixes() -> dict:
    jx = json.loads(JX_JSON.read_text())
    ok = (
        jx["checks"]["all_ok"]
        and jx["verdict"]["pair_all_64"] == "LEMMA"
        and jx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert center_green4(1) == (1, 0, 1, 0)
    assert (1, 0, 0, 1) in AND_ONES
    assert not cob_shaped(1, 0, 0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = center_g4_table()
    sc = center_four_cover()
    k0 = killed_always_green4()
    k1 = killed_always_cob()
    k2 = killed_and_vanishes()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "center_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "center_four_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_always_green4": {k: k0[k] for k in k0 if k != "ok"},
        "killed_always_cob": {k: k1[k] for k in k1 if k != "ok"},
        "killed_and_vanishes": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "center_green4_w": True,
            "center_all_16": True,
            "covering_center_four": True,
            "always_green4": False,
            "always_cob": False,
            "and_vanishes": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "center_green4_w": "LEMMA",
            "center_all_16": "LEMMA",
            "covering_center_four": "LEMMA",
            "always_green4": "KILLED",
            "always_cob": "KILLED",
            "and_vanishes": "KILLED",
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
    print("center_g4_table", dump["center_g4_table"])
    cov = dump["center_four_cover"]
    print(
        "center_four_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_ctr",
        cov["n_ctr"],
        "n_and",
        cov["n_and"],
        "n_0000",
        cov["n_0000"],
        "n_g4",
        cov["n_g4"],
        "n_iso",
        cov["n_iso"],
        "n_mid",
        cov["n_mid"],
        "n_types",
        cov["n_types"],
        "n_iso_types",
        cov["n_iso_types"],
        "n_mid_types",
        cov["n_mid_types"],
        "n_and_ones",
        cov["n_and_ones"],
    )
    print("killed_always_green4", dump["killed_always_green4"])
    print("killed_always_cob", dump["killed_always_cob"])
    print("killed_and_vanishes", dump["killed_and_vanishes"])


if __name__ == "__main__":
    main()
