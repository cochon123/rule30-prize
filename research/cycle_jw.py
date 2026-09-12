#!/usr/bin/env python3
"""Cycle JW: isolated-one packed 4-tuples take all 16 values.

On isolated ones green4 is 0111. Covering packed 4-tuples hit every
16-row; AND fires all four AND_ONES. Isolated packed is not always
0000; not always cob; isolated AND does not vanish. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_jw.py --certify
Dump: research/cycle_jw.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from cycle_ir import isolated_one
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JV_JSON = Path(__file__).resolve().parent / "cycle_jv.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

G4_ISO = (0, 1, 1, 1)


def iso_g4_table() -> dict:
    """n<64: every isolated one has green4 0111."""
    n_iso = n_seed = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if green4(n, j) != G4_ISO:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "g4": list(green4(n, j)),
                }
            if n == 0:
                n_seed += 1
    ok = n_iso == 461 and n_seed == 1 and green4(3, 3) == G4_ISO
    return {"ok": ok, "n_iso": n_iso, "n_seed": n_seed}


def _walk_four(k: int, q: int) -> dict:
    """Isolated packed 4-tuple census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_and = n_cob = n_0000 = n_g4 = 0
    n_and_ones = {four: 0 for four in AND_ONES}
    types = set()
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
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                types.add(four)
                if four == (0, 0, 0, 0):
                    n_0000 += 1
                if cob_shaped(*four):
                    n_cob += 1
                if four == G4_ISO:
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
        "n_iso": n_iso,
        "n_and": n_and,
        "n_cob": n_cob,
        "n_0000": n_0000,
        "n_g4": n_g4,
        "n_types": len(types),
        "n_and_ones": {"".join(map(str, f)): n_and_ones[f] for f in AND_ONES},
        "types": ["".join(map(str, f)) for f in sorted(types)],
        "xor_j": xor_j,
    }


def iso_four_cover() -> dict:
    """Isolated 4-tuple census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_and = n_cob = n_0000 = n_g4 = 0
    n_and_ones = {"".join(map(str, f)): 0 for f in AND_ONES}
    types = set()
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_four(k, q)
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
            n_iso += w["n_iso"]
            n_and += w["n_and"]
            n_cob += w["n_cob"]
            n_0000 += w["n_0000"]
            n_g4 += w["n_g4"]
            for key, val in w["n_and_ones"].items():
                n_and_ones[key] += val
            types.update(w["types"])
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_and": w["n_and"],
                "n_types": w["n_types"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_and == 1489
        and n_0000 == 1892
        and n_g4 == 356
        and n_and_ones["0010"] == 354
        and n_and_ones["0011"] == 343
        and n_and_ones["0100"] == 385
        and n_and_ones["1001"] == 407
        and n_and == sum(n_and_ones.values())
        and len(types) == 16
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_and": n_and,
        "n_cob": n_cob,
        "n_0000": n_0000,
        "n_g4": n_g4,
        "n_and_ones": n_and_ones,
        "n_types": len(types),
        "rows": rows,
    }


def _kill_four():
    """Packed 4-tuple at k=1, s=5, n=3, j=3, p=6."""
    k, s, n, j, p = 1, 5, 3, 3, 6
    row = 1
    prev = None
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    return k, s, n, j, p, four


def killed_always_0000() -> dict:
    """Isolated packed is always 0000: G(3,3) is 0100."""
    k, s, n, j, p, four = _kill_four()
    ok = (
        isolated_one(n, j)
        and green4(n, j) == G4_ISO
        and four == (0, 1, 0, 0)
        and four != (0, 0, 0, 0)
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


def killed_always_cob() -> dict:
    """Isolated packed is always cob: G(3,3) 0100 is not cob-shaped."""
    k, s, n, j, p, four = _kill_four()
    ok = (
        isolated_one(n, j)
        and four == (0, 1, 0, 0)
        and (not cob_shaped(*four))
        and four != G4_ISO
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
    """Isolated AND vanishes: G(3,3) 0100 is in AND_ONES."""
    k, s, n, j, p, four = _kill_four()
    ok = (
        isolated_one(n, j)
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
    jv = json.loads(JV_JSON.read_text())
    ok = (
        jv["checks"]["all_ok"]
        and jv["verdict"]["cob_pair"] == "LEMMA"
        and jv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert green4(3, 3) == G4_ISO
    assert (0, 1, 0, 0) in AND_ONES
    assert not cob_shaped(0, 1, 0, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = iso_g4_table()
    sc = iso_four_cover()
    k0 = killed_always_0000()
    k1 = killed_always_cob()
    k2 = killed_and_vanishes()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "iso_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "iso_four_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_always_0000": {k: k0[k] for k in k0 if k != "ok"},
        "killed_always_cob": {k: k1[k] for k in k1 if k != "ok"},
        "killed_and_vanishes": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "iso_green4_0111": True,
            "iso_all_16": True,
            "covering_iso_four": True,
            "always_0000": False,
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
            "iso_green4_0111": "LEMMA",
            "iso_all_16": "LEMMA",
            "covering_iso_four": "LEMMA",
            "always_0000": "KILLED",
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
    print("iso_g4_table", dump["iso_g4_table"])
    cov = dump["iso_four_cover"]
    print(
        "iso_four_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_and",
        cov["n_and"],
        "n_0000",
        cov["n_0000"],
        "n_g4",
        cov["n_g4"],
        "n_types",
        cov["n_types"],
        "n_and_ones",
        cov["n_and_ones"],
    )
    print("killed_always_0000", dump["killed_always_0000"])
    print("killed_always_cob", dump["killed_always_cob"])
    print("killed_and_vanishes", dump["killed_and_vanishes"])


if __name__ == "__main__":
    main()
