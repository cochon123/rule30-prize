#!/usr/bin/env python3
"""Cycle IN: n%4==1 has only Green triples; isolated pairs only n%4==3.

Even n has no consecutive ones (Cycle IM), so consecutive G=1 lives on
odd n=2m+1. When m is even (n%4==1), G(m) has no 11, and every
G=1 lifts to a run-3; there are no isolated pairs or isolated ones.
Isolated pairs occur only for n%4==3. n%4==1 does have ones
(all in triples); n%4==3 does have run-3. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_in.py --certify
Dump: research/cycle_in.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IM_JSON = Path(__file__).resolve().parent / "cycle_im.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

KIND = {(0, 0): "iso", (0, 1): "left", (1, 0): "right"}


def g_run_kind(n: int, j: int):
    """iso/left/right on G(j)=G(j+1)=1, else None."""
    if G(n, j) == 0 or G(n, j + 1) == 0:
        return None
    gm, gp2 = G(n, j - 1), G(n, j + 2)
    return KIND.get((gm, gp2), "bad")


def mod4_run_table() -> dict:
    """n<64: n%4==1 only triples; isolated pairs only n%4==3."""
    n_r1 = [0, 0, 0, 0]
    n_r2 = [0, 0, 0, 0]
    n_r3 = [0, 0, 0, 0]
    n_g11 = [0, 0, 0, 0]
    n_iso = [0, 0, 0, 0]
    n_left = [0, 0, 0, 0]
    n_right = [0, 0, 0, 0]
    for n in range(0, 64):
        r = n % 4
        run = 0
        for j in range(0, 2 * n + 2):
            bit = G(n, j) if j <= 2 * n else 0
            if bit:
                run += 1
                continue
            if run == 1:
                n_r1[r] += 1
            elif run == 2:
                n_r2[r] += 1
            elif run == 3:
                n_r3[r] += 1
            elif run >= 4:
                return {"ok": False, "run4": True, "n": n}
            run = 0
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            if kind is None:
                continue
            if kind == "bad":
                return {"ok": False, "bad": True, "n": n, "j": j}
            if r % 2 == 0:
                return {"ok": False, "even11": True, "n": n, "j": j}
            if kind == "iso" and r != 3:
                return {"ok": False, "iso": True, "n": n, "j": j}
            n_g11[r] += 1
            if kind == "iso":
                n_iso[r] += 1
            elif kind == "left":
                n_left[r] += 1
            else:
                n_right[r] += 1
    ok = (
        n_r1[1] == 0
        and n_r2[1] == 0
        and n_r3[1] == 128
        and n_r2[3] == 230
        and n_r3[3] == 13
        and n_r1[3] == 45
        and n_r2[0] == 0
        and n_r2[2] == 0
        and n_r3[0] == 0
        and n_r3[2] == 0
        and n_iso[1] == 0
        and n_iso[3] == 230
        and n_left[1] == 128
        and n_right[1] == 128
        and n_left[3] == 13
        and n_right[3] == 13
        and n_g11[1] == 256
        and n_g11[3] == 256
        and n_g11[0] == 0
        and n_g11[2] == 0
    )
    return {
        "ok": ok,
        "n_r1": n_r1,
        "n_r2": n_r2,
        "n_r3": n_r3,
        "n_g11": n_g11,
        "n_iso": n_iso,
        "n_left": n_left,
        "n_right": n_right,
    }


def _walk_mod4(k: int, q: int) -> dict:
    """n%4==1 only triples on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = 0
    n_g11_n1 = n_g11_n3 = 0
    n_iso_n3 = n_left_n1 = n_right_n1 = n_left_n3 = n_right_n3 = 0
    xor_j = 0
    s = t0
    prev = None
    seen = set()
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            if n not in seen:
                seen.add(n)
                for j in range(0, 2 * n):
                    kind = g_run_kind(n, j)
                    if kind is None:
                        continue
                    if kind == "bad":
                        return {"ok": False, "bad": True, "k": k, "n": n, "j": j}
                    if n % 2 == 0:
                        return {"ok": False, "even11": True, "k": k, "n": n, "j": j}
                    if kind == "iso" and n % 4 != 3:
                        return {
                            "ok": False,
                            "iso_n1": True,
                            "k": k,
                            "n": n,
                            "j": j,
                        }
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                bits[j] = packed
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                if kind is None:
                    continue
                n_g11 += 1
                r = n % 4
                if r == 1:
                    n_g11_n1 += 1
                    if kind == "iso":
                        return {"ok": False, "cov_iso": True, "k": k, "n": n, "j": j}
                    if kind == "left":
                        n_left_n1 += 1
                    else:
                        n_right_n1 += 1
                elif r == 3:
                    n_g11_n3 += 1
                    if kind == "iso":
                        n_iso_n3 += 1
                    elif kind == "left":
                        n_left_n3 += 1
                    else:
                        n_right_n3 += 1
                else:
                    return {"ok": False, "cov_even": True, "k": k, "n": n, "j": j}
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_n1": n_g11_n1,
        "n_g11_n3": n_g11_n3,
        "n_iso_n3": n_iso_n3,
        "n_left_n1": n_left_n1,
        "n_right_n1": n_right_n1,
        "n_left_n3": n_left_n3,
        "n_right_n3": n_right_n3,
        "xor_j": xor_j,
    }


def mod4_cover() -> dict:
    """n%4==1 only triples on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = 0
    n_g11_n1 = n_g11_n3 = 0
    n_iso_n3 = n_left_n1 = n_right_n1 = n_left_n3 = n_right_n3 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_mod4(k, q)
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
            n_g11 += w["n_g11"]
            n_g11_n1 += w["n_g11_n1"]
            n_g11_n3 += w["n_g11_n3"]
            n_iso_n3 += w["n_iso_n3"]
            n_left_n1 += w["n_left_n1"]
            n_right_n1 += w["n_right_n1"]
            n_left_n3 += w["n_left_n3"]
            n_right_n3 += w["n_right_n3"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_g11_n1": w["n_g11_n1"],
                "n_g11_n3": w["n_g11_n3"],
                "n_iso_n3": w["n_iso_n3"],
                "n_left_n1": w["n_left_n1"],
                "n_right_n1": w["n_right_n1"],
                "n_left_n3": w["n_left_n3"],
                "n_right_n3": w["n_right_n3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_g11_n1 == 4294
        and n_g11_n3 == 4283
        and n_iso_n3 == 3817
        and n_left_n1 == 2147
        and n_right_n1 == 2147
        and n_left_n3 == 233
        and n_right_n3 == 233
        and n_g11_n1 + n_g11_n3 == n_g11
        and n_left_n1 + n_right_n1 == n_g11_n1
        and n_iso_n3 + n_left_n3 + n_right_n3 == n_g11_n3
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_n1": n_g11_n1,
        "n_g11_n3": n_g11_n3,
        "n_iso_n3": n_iso_n3,
        "n_left_n1": n_left_n1,
        "n_right_n1": n_right_n1,
        "n_left_n3": n_left_n3,
        "n_right_n3": n_right_n3,
        "rows": rows,
    }


def killed_n1_has_iso() -> dict:
    """n%4==1 has an isolated Green pair: G(1)=111 is a triple."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    kind = g_run_kind(n, j)
    ok = (
        n % 4 == 1
        and [G(n, i) for i in range(0, 3)] == [1, 1, 1]
        and kind == "left"
        and kind != "iso"
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": kind,
        "G": [G(n, i) for i in range(0, 3)],
    }


def killed_n3_no_run3() -> dict:
    """n%4==3 has no run-3: G(7) has 111 at j=6."""
    k, s, n, j, p = 1, 5, 7, 6, 8
    kind = g_run_kind(n, j)
    ok = (
        n % 4 == 3
        and [G(n, i) for i in range(j, j + 3)] == [1, 1, 1]
        and kind == "left"
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": kind,
        "G": [G(n, i) for i in range(j, j + 3)],
    }


def killed_n1_no_ones() -> dict:
    """n%4==1 has no Green ones: G(1,0)=1."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    ok = n % 4 == 1 and G(n, j) == 1 and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
    }


def prefixes() -> dict:
    im = json.loads(IM_JSON.read_text())
    ok = (
        im["checks"]["all_ok"]
        and im["verdict"]["even_n_no_Green_11"] == "LEMMA"
        and im["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g_run_kind(1, 0) == "left"
    assert g_run_kind(3, 0) == "iso"
    assert g_run_kind(7, 6) == "left"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mod4_run_table()
    sc = mod4_cover()
    k0 = killed_n1_has_iso()
    k1 = killed_n3_no_run3()
    k2 = killed_n1_no_ones()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mod4_run_table": {k: rt[k] for k in rt if k != "ok"},
        "mod4_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_n1_has_iso": {k: k0[k] for k in k0 if k != "ok"},
        "killed_n3_no_run3": {k: k1[k] for k in k1 if k != "ok"},
        "killed_n1_no_ones": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "n1_only_triples": True,
            "isolated_pairs_only_n3": True,
            "covering_g11_mod4": True,
            "n1_has_iso": False,
            "n3_no_run3": False,
            "n1_no_ones": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n1_only_triples": "LEMMA",
            "isolated_pairs_only_n3": "LEMMA",
            "covering_g11_mod4": "LEMMA",
            "n1_has_iso": "KILLED",
            "n3_no_run3": "KILLED",
            "n1_no_ones": "KILLED",
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
    print("mod4_run_table", dump["mod4_run_table"])
    cov = dump["mod4_cover"]
    print(
        "mod4_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_g11_n1",
        cov["n_g11_n1"],
        "n_g11_n3",
        cov["n_g11_n3"],
        "n_iso_n3",
        cov["n_iso_n3"],
    )
    print("killed_n1_has_iso", dump["killed_n1_has_iso"])
    print("killed_n3_no_run3", dump["killed_n3_no_run3"])
    print("killed_n1_no_ones", dump["killed_n1_no_ones"])


if __name__ == "__main__":
    main()
