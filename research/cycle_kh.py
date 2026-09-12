#!/usr/bin/env python3
"""Cycle KH: every Green row XORs green4 to 0111; covering clip is closed-form.

Every n has XOR of green4 over G=1 columns equal to 0111 (palindrome,
center G(n,n)=1, odd length, even consecutive-pair count). Covering
clipped XOR of green4 is (1,1,0,(k+1) mod 2) for k>=2, independent of
q in {6,10}. Packed XOR is not that value; this is not J. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_kh.py --certify
Dump: research/cycle_kh.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KG_JSON = Path(__file__).resolve().parent / "cycle_kg.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

ROW_XOR = (0, 1, 1, 1)
N_ALG = 256
CLIP_SMALL = {
    (0, 6): (0, 0, 0, 0),
    (0, 10): (0, 1, 1, 0),
    (1, 6): (0, 0, 0, 0),
    (1, 10): (1, 1, 0, 0),
}


def xor4(left, right):
    return tuple(x ^ y for x, y in zip(left, right))


def clip_want(k: int, q: int):
    """Covering clipped XOR of green4 on G=1."""
    if k >= 2:
        return (1, 1, 0, (k + 1) % 2)
    return CLIP_SMALL[(k, q)]


def g4_row_xor(n: int):
    """XOR of green4 over G=1 columns; pair and run-2 parities."""
    acc = (0, 0, 0, 0)
    n_g1 = n_pairs = n_run2 = 0
    run = 0
    for j in range(0, 2 * n + 2):
        bit = G(n, j) if j <= 2 * n else 0
        if j <= 2 * n and G(n, 2 * n - j) != G(n, j):
            return {"ok": False, "pal": True, "n": n, "j": j}
        if bit:
            run += 1
            if j <= 2 * n:
                n_g1 += 1
                g4 = green4(n, j)
                if g4 != g1_green4(n, j):
                    return {"ok": False, "g4": True, "n": n, "j": j}
                acc = xor4(acc, g4)
                if j < 2 * n and G(n, j + 1) == 1:
                    n_pairs += 1
            continue
        if run >= 4:
            return {"ok": False, "run4": True, "n": n, "r": run}
        if run == 2:
            n_run2 += 1
        run = 0
    if G(n, n) != 1:
        return {"ok": False, "center": True, "n": n}
    return {
        "ok": True,
        "xor": acc,
        "n_g1": n_g1,
        "n_pairs": n_pairs,
        "n_run2": n_run2,
    }


def g4_row_table() -> dict:
    """n<256: every row XORs green4 to 0111; pair and run-2 counts even."""
    n_ok = n_g1 = 0
    n_pairs_odd = n_run2_odd = 0
    for n in range(0, N_ALG):
        rec = g4_row_xor(n)
        if not rec.get("ok"):
            return rec
        if rec["xor"] != ROW_XOR:
            return {"ok": False, "xor": True, "n": n, "got": list(rec["xor"])}
        if rec["n_pairs"] % 2:
            n_pairs_odd += 1
        if rec["n_run2"] % 2:
            n_run2_odd += 1
        n_ok += 1
        n_g1 += rec["n_g1"]
    unclip_even = (0, 0, 0, 0)
    unclip_odd = ROW_XOR
    tot = (0, 0, 0, 0)
    for n in range(0, N_ALG):
        tot = xor4(tot, ROW_XOR)
        want = unclip_even if (n + 1) % 2 == 0 else unclip_odd
        if tot != want:
            return {"ok": False, "unclip": True, "N": n + 1, "got": list(tot)}
    ok = n_ok == N_ALG and n_pairs_odd == 0 and n_run2_odd == 0 and tot == unclip_even
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_pairs_odd": n_pairs_odd,
        "n_run2_odd": n_run2_odd,
        "unclip_even": list(unclip_even),
        "unclip_odd": list(unclip_odd),
        "row_xor": list(ROW_XOR),
    }


def _walk_xor(k: int, q: int) -> dict:
    """Covering clipped XOR of green4 and packed 4-tuples; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    xor_g4 = (0, 0, 0, 0)
    xor_pack = (0, 0, 0, 0)
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
                if G(n, j) == 0:
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                g4 = green4(n, j)
                if g4 != g1_green4(n, j):
                    return {"ok": False, "g4": True, "n": n, "j": j}
                xor_g4 = xor4(xor_g4, g4)
                xor_pack = xor4(xor_pack, four)
        row = rule30_step(row)
        s += 1
    N = U * Q
    unclip = (0, 0, 0, 0) if N % 2 == 0 else ROW_XOR
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "xor_j": xor_j,
        "xor_g4": xor_g4,
        "xor_pack": xor_pack,
        "unclip": unclip,
        "N": N,
    }


def g4_xor_cover() -> dict:
    """Covering k<=6 clipped green4 XOR matches clip_want; J XOR matches HF/HG."""
    n_ok = n_g1 = n_eq_pack = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_xor(k, q)
            if not w.get("ok"):
                return w
            want = clip_want(k, q)
            if w["xor_g4"] != want:
                return {
                    "ok": False,
                    "clip": True,
                    "k": k,
                    "q": q,
                    "got": list(w["xor_g4"]),
                    "want": list(want),
                }
            if w["unclip"] != (0, 0, 0, 0):
                return {"ok": False, "unclip": True, "k": k, "q": q, "N": w["N"]}
            if q == 6:
                jwant = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != jwant:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": jwant}
            else:
                jwant = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != jwant:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": jwant,
                    }
            if w["xor_g4"] == w["xor_pack"]:
                n_eq_pack += 1
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "xor_j": w["xor_j"],
                "xor_g4": list(w["xor_g4"]),
                "xor_pack": list(w["xor_pack"]),
                "unclip": list(w["unclip"]),
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_eq_pack == 1
        and rows["0"]["j6"]["xor_g4"] == [0, 0, 0, 0]
        and rows["0"]["j10"]["xor_g4"] == [0, 1, 1, 0]
        and rows["1"]["j6"]["xor_g4"] == [0, 0, 0, 0]
        and rows["1"]["j10"]["xor_g4"] == [1, 1, 0, 0]
        and rows["2"]["j6"]["xor_g4"] == [1, 1, 0, 1]
        and rows["3"]["j6"]["xor_g4"] == [1, 1, 0, 0]
        and rows["0"]["j6"]["xor_pack"] == [1, 1, 1, 1]
        and rows["5"]["j6"]["xor_g4"] == rows["5"]["j6"]["xor_pack"]
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_eq_pack": n_eq_pack,
        "rows": rows,
    }


def killed_row_zero() -> dict:
    """Row-XOR of green4 is 0000: seed n=0 is 0111."""
    rec = g4_row_xor(0)
    ok = rec.get("ok") and rec["xor"] == ROW_XOR and rec["n_g1"] == 1
    return {"ok": ok, "n": 0, "xor": list(rec["xor"]), "n_g1": rec["n_g1"]}


def killed_indep_k() -> dict:
    """Covering green4 XOR is independent of k: k=2 is 1101, k=3 is 1100."""
    a = clip_want(2, 6)
    b = clip_want(3, 6)
    ok = a == (1, 1, 0, 1) and b == (1, 1, 0, 0) and a != b
    return {"ok": ok, "k2": list(a), "k3": list(b)}


def killed_eq_pack() -> dict:
    """Covering green4 XOR equals packed XOR: k=0 q=6 is 0000 vs 1111."""
    w = _walk_xor(0, 6)
    ok = (
        w.get("ok")
        and w["xor_g4"] == (0, 0, 0, 0)
        and w["xor_pack"] == (1, 1, 1, 1)
        and w["xor_g4"] != w["xor_pack"]
    )
    return {
        "ok": ok,
        "k": 0,
        "q": 6,
        "xor_g4": list(w["xor_g4"]),
        "xor_pack": list(w["xor_pack"]),
    }


def killed_indep_clip() -> dict:
    """Covering green4 XOR is independent of clip: k=0 q=10 is 0110 vs 0000."""
    clip = clip_want(0, 10)
    unclip = (0, 0, 0, 0)
    ok = clip == (0, 1, 1, 0) and clip != unclip
    return {"ok": ok, "k": 0, "q": 10, "clip": list(clip), "unclip": list(unclip)}


def prefixes() -> dict:
    kg = json.loads(KG_JSON.read_text())
    ok = (
        kg["checks"]["all_ok"]
        and kg["verdict"]["pack_g4_all_64"] == "LEMMA"
        and kg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert g4_row_xor(0)["xor"] == ROW_XOR
    assert clip_want(4, 6) == clip_want(4, 10) == (1, 1, 0, 1)
    assert clip_want(5, 6) == clip_want(5, 10) == (1, 1, 0, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = g4_row_table()
    sc = g4_xor_cover()
    k0 = killed_row_zero()
    k1 = killed_indep_k()
    k2 = killed_eq_pack()
    k3 = killed_indep_clip()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g4_row_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_row_zero": {k: k0[k] for k in k0 if k != "ok"},
        "killed_indep_k": {k: k1[k] for k in k1 if k != "ok"},
        "killed_eq_pack": {k: k2[k] for k in k2 if k != "ok"},
        "killed_indep_clip": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "g4_row_xor_0111": True,
            "covering_clip_g4": True,
            "pack_g4_all_64": True,
            "row_xor_0000": False,
            "clip_indep_k": False,
            "clip_eq_pack": False,
            "clip_indep_clip": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g4_row_xor_0111": "LEMMA",
            "covering_clip_g4": "LEMMA",
            "pack_g4_all_64": "LEMMA",
            "row_xor_0000": "KILLED",
            "clip_indep_k": "KILLED",
            "clip_eq_pack": "KILLED",
            "clip_indep_clip": "KILLED",
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
    print("g4_row_table", dump["g4_row_table"])
    cov = dump["g4_xor_cover"]
    print(
        "g4_xor_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_eq_pack",
        cov["n_eq_pack"],
    )
    print("killed_row_zero", dump["killed_row_zero"])
    print("killed_indep_k", dump["killed_indep_k"])
    print("killed_eq_pack", dump["killed_eq_pack"])
    print("killed_indep_clip", dump["killed_indep_clip"])


if __name__ == "__main__":
    main()
