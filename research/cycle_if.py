#!/usr/bin/env python3
"""Cycle IF: covering center AND is determined by Hamming slots vs green4(n,n).

green4(n,n)=(w,1-w,1,1-w) with w=v2(n+1) mod 2. Packed center AND is 1
on slots (z,a,b) and (b,c); equals w on (z) and (z,c); equals 1-w on
(a) and (a,c); else 0. Center AND is not w, not 1-w, and mixed-with
green4 is not always AND. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_if.py --certify
Dump: research/cycle_if.json
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
from cycle_hh import bit_at
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IE_JSON = Path(__file__).resolve().parent / "cycle_ie.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

CTR_ALWAYS = ((0, 1, 2), (2, 3))
CTR_IF_W = ((0,), (0, 3))
CTR_IF_NOT_W = ((1,), (1, 3))


def center_green4(n: int) -> tuple[int, int, int, int]:
    """Even-s Green 4-tuple at the covering center j=n."""
    w = v2(n + 1) & 1
    return (w, 1 - w, 1, 1 - w)


def _slots(four, four2):
    return tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)


def center_and_from_slots(n: int, four) -> int:
    """Packed center AND from Hamming slots vs green4(n,n)."""
    g4 = center_green4(n)
    slots = _slots(g4, four)
    w = g4[0]
    if slots in CTR_ALWAYS:
        return 1
    if slots in CTR_IF_W:
        return w
    if slots in CTR_IF_NOT_W:
        return 1 - w
    return 0


def center_g4_table() -> dict:
    """n<64: green4(n,n)=center_green4; 16-row AND formula for w=0 and w=1."""
    n_ok = 0
    for n in range(0, 64):
        g4 = green4(n, n)
        cg = center_green4(n)
        if g4 != cg:
            return {"ok": False, "g4": True, "n": n, "got": list(g4), "want": list(cg)}
        if G(n, n) != 1:
            return {"ok": False, "diag": True, "n": n}
        if G(n, n + 1) != (v2(n + 1) & 1):
            return {"ok": False, "v": True, "n": n}
        n_ok += 1
    n_row = 0
    for n in (0, 1):
        for bits in range(16):
            four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
            if center_and_from_slots(n, four) != and_clause(*four):
                return {"ok": False, "row": True, "n": n, "four": four}
            n_row += 1
    ok = n_ok == 64 and n_row == 32 and center_green4(0) == (0, 1, 1, 1)
    ok = ok and center_green4(1) == (1, 0, 1, 0)
    return {"ok": ok, "n_ok": n_ok, "n_row": n_row}


def _walk_ctr(k: int, q: int) -> dict:
    """center_and_from_slots on covering centers; J XOR from G=1 AND."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_ctr = n_ctr_and = n_eqg4 = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = (Aodd >> p) & 1
                if packed != and_clause(*four):
                    return {"ok": False, "pack": True, "k": k, "four": four}
                n_ok += 1
                if packed and G(n, j):
                    xor_j ^= 1
                if j != n or p < 3:
                    continue
                n_ctr += 1
                pred = center_and_from_slots(n, four)
                if pred != packed:
                    return {
                        "ok": False,
                        "ctr": True,
                        "k": k,
                        "n": n,
                        "four": four,
                        "pred": pred,
                    }
                if packed:
                    n_ctr_and += 1
                if four == center_green4(n):
                    n_eqg4 += 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and n_ctr > 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_ctr": n_ctr,
        "n_ctr_and": n_ctr_and,
        "n_eqg4": n_eqg4,
        "xor_j": xor_j,
    }


def ctr_cover() -> dict:
    """Center slot formula on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_ctr = n_ctr_and = n_eqg4 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_ctr(k, q)
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
            n_ctr += w["n_ctr"]
            n_ctr_and += w["n_ctr_and"]
            n_eqg4 += w["n_eqg4"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_ctr": w["n_ctr"],
                "n_ctr_and": w["n_ctr_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_ctr == 762
        and n_ctr_and == 232
        and n_eqg4 == 32
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_ctr": n_ctr,
        "n_ctr_and": n_ctr_and,
        "n_eqg4": n_eqg4,
        "rows": rows,
    }


def killed_ctr_and_eq_w() -> dict:
    """Center AND is not w=v2(n+1) mod 2: k=0, s=5, 0100 vs green 0111."""
    k, s, n, p = 0, 5, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = center_green4(n)
    packed = and_clause(*four)
    w = g4[0]
    ok = (
        four == (0, 1, 0, 0)
        and g4 == (0, 1, 1, 1)
        and packed == 1
        and w == 0
        and packed != w
        and G(n, n) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
        "w": w,
    }


def killed_ctr_and_eq_not_w() -> dict:
    """Center AND is not 1-w: k=0, s=3, 1001 vs green 1010."""
    k, s, n, p = 0, 3, 1, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = center_green4(n)
    packed = and_clause(*four)
    w = g4[0]
    ok = (
        four == (1, 0, 0, 1)
        and g4 == (1, 0, 1, 0)
        and packed == 1
        and w == 1
        and packed != (1 - w)
        and G(n, n) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
        "w": w,
    }


def killed_ctr_mix_always_and() -> dict:
    """Mixed-with-green4 is not always AND: k=1, s=15, 1000 vs 0111."""
    k, s, n, p = 1, 15, 2, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = center_green4(n)
    packed = and_clause(*four)
    ok = (
        four == (1, 0, 0, 0)
        and g4 == (0, 1, 1, 1)
        and packed == 0
        and cob_shaped(*four) != cob_shaped(*g4)
        and _slots(g4, four) == (0, 1, 2, 3)
        and G(n, n) == 1
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
        "slots": list(_slots(g4, four)),
    }


def prefixes() -> dict:
    ie = json.loads(IE_JSON.read_text())
    ok = (
        ie["checks"]["all_ok"]
        and ie["verdict"]["mix_AND_xor_from_Hamming_slots"] == "LEMMA"
        and ie["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, cc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and cc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert center_and_from_slots(0, (0, 1, 0, 0)) == 1
    assert center_and_from_slots(1, (1, 0, 0, 1)) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = center_g4_table()
    cc = ctr_cover()
    k0 = killed_ctr_and_eq_w()
    k1 = killed_ctr_and_eq_not_w()
    k2 = killed_ctr_mix_always_and()
    pref = prefixes()
    checks = self_checks(c20, rt, cc, k0, k1, k2, pref)
    dump = {
        "cycle": "IF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "center_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "ctr_cover": {k: cc[k] for k in cc if k != "ok"},
        "killed_ctr_and_eq_w": {k: k0[k] for k in k0 if k != "ok"},
        "killed_ctr_and_eq_not_w": {k: k1[k] for k in k1 if k != "ok"},
        "killed_ctr_mix_always_and": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "green4_center_v2": True,
            "center_AND_from_green4_slots": True,
            "covering_center_AND_eq_slots": True,
            "ctr_and_eq_w": False,
            "ctr_and_eq_not_w": False,
            "ctr_mix_always_and": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "green4_center_v2": "LEMMA",
            "center_AND_from_green4_slots": "LEMMA",
            "covering_center_AND_eq_slots": "LEMMA",
            "ctr_and_eq_w": "KILLED",
            "ctr_and_eq_not_w": "KILLED",
            "ctr_mix_always_and": "KILLED",
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
    cov = dump["ctr_cover"]
    print(
        "ctr_cover n_ok",
        cov["n_ok"],
        "n_ctr",
        cov["n_ctr"],
        "n_ctr_and",
        cov["n_ctr_and"],
        "n_eqg4",
        cov["n_eqg4"],
    )
    print("killed_ctr_and_eq_w", dump["killed_ctr_and_eq_w"])
    print("killed_ctr_and_eq_not_w", dump["killed_ctr_and_eq_not_w"])
    print("killed_ctr_mix_always_and", dump["killed_ctr_mix_always_and"])


if __name__ == "__main__":
    main()
