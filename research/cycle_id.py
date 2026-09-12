#!/usr/bin/env python3
"""Cycle ID: mixed Hamming 1 never includes cob(j); Hamming 2 always does.

Odd zab Hamming (mixed cob/non-cob) forces the complementary slot
pattern of Cycles IA/IB: Hamming 1 is a single z/a/b flip, Hamming 2
is that plus c, Hamming 3 is exactly (z,a,b). Mixed Hamming 1 is not
flip_c; mixed Hamming 2 is not c-free; mixed Hamming 3 is not
c-always. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_id.py --certify
Dump: research/cycle_id.json
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
from cycle_hy import mixed_oneside
from cycle_ia import flip_c
from cycle_ib import zab_parity
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IC_JSON = Path(__file__).resolve().parent / "cycle_ic.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

MIX_HAM1_SLOTS = ((0,), (1,), (2,))
MIX_HAM2_SLOTS = ((0, 3), (1, 3), (2, 3))
MIX_HAM3_SLOTS = ((0, 1, 2),)
MIX_HAM4_SLOTS = ((0, 1, 2, 3),)


def mix_slots_table() -> dict:
    """16x16: mixed slots are the odd-zab patterns; never flip_c alone."""
    n_ok = n_mix = n_h1 = n_h2 = n_h3 = n_h4 = 0
    for b1 in range(16):
        four = tuple((b1 >> i) & 1 for i in range(3, -1, -1))
        for b2 in range(16):
            four2 = tuple((b2 >> i) & 1 for i in range(3, -1, -1))
            n_ok += 1
            c1, c2 = cob_shaped(*four), cob_shaped(*four2)
            slots = tuple(
                i for i, (x, y) in enumerate(zip(four, four2)) if x != y
            )
            if c1 == c2:
                if zab_parity(four, four2) != 0:
                    return {"ok": False, "even": True, "four": four}
                continue
            n_mix += 1
            if zab_parity(four, four2) != 1:
                return {"ok": False, "odd": True, "four": four, "four2": four2}
            ham = len(slots)
            if ham == 1:
                n_h1 += 1
                if slots not in MIX_HAM1_SLOTS or 3 in slots:
                    return {"ok": False, "h1": True, "slots": slots}
            elif ham == 2:
                n_h2 += 1
                if slots not in MIX_HAM2_SLOTS or 3 not in slots:
                    return {"ok": False, "h2": True, "slots": slots}
            elif ham == 3:
                n_h3 += 1
                if slots not in MIX_HAM3_SLOTS or 3 in slots:
                    return {"ok": False, "h3": True, "slots": slots}
            elif ham == 4:
                n_h4 += 1
                if slots not in MIX_HAM4_SLOTS:
                    return {"ok": False, "h4": True, "slots": slots}
            else:
                return {"ok": False, "ham": True, "slots": slots}
    ok = (
        n_ok == 256
        and n_mix == 128
        and n_h1 == 48
        and n_h2 == 48
        and n_h3 == 16
        and n_h4 == 16
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_mix": n_mix,
        "n_h1": n_h1,
        "n_h2": n_h2,
        "n_h3": n_h3,
        "n_h4": n_h4,
    }


def _walk_mix(k: int, q: int) -> dict:
    """Mixed covering slots: ham1 no c, ham2 always c, ham3 is (z,a,b)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_mix = n_mix_xor = 0
    n_h1 = n_h2 = n_h3 = n_h4 = 0
    xor_j = xor_fold = 0
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
            if n in bits and bits[n][1]:
                xor_fold ^= 1
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
                if c1 == c2:
                    if a ^ b:
                        xor_fold ^= 1
                    continue
                n_mix += 1
                if zab_parity(f, g) != 1:
                    return {"ok": False, "zab": True, "k": k, "four": f}
                slots = tuple(i for i, (x, y) in enumerate(zip(f, g)) if x != y)
                ham = len(slots)
                mo = mixed_oneside(f, g)
                if mo != (a ^ b):
                    return {"ok": False, "oneside": True, "k": k}
                if ham == 1:
                    n_h1 += 1
                    if slots not in MIX_HAM1_SLOTS or 3 in slots:
                        return {"ok": False, "h1": True, "k": k, "slots": slots}
                elif ham == 2:
                    n_h2 += 1
                    if slots not in MIX_HAM2_SLOTS or 3 not in slots:
                        return {"ok": False, "h2": True, "k": k, "slots": slots}
                elif ham == 3:
                    n_h3 += 1
                    if slots not in MIX_HAM3_SLOTS or 3 in slots:
                        return {"ok": False, "h3": True, "k": k, "slots": slots}
                elif ham == 4:
                    n_h4 += 1
                    if slots not in MIX_HAM4_SLOTS:
                        return {"ok": False, "h4": True, "k": k, "slots": slots}
                else:
                    return {"ok": False, "ham": True, "k": k, "slots": slots}
                if a ^ b:
                    n_mix_xor += 1
                    xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_h1": n_h1,
        "n_h2": n_h2,
        "n_h3": n_h3,
        "n_h4": n_h4,
        "xor_j": xor_j,
    }


def mix_cover() -> dict:
    """Mixed slot split on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_mix = n_mix_xor = 0
    n_h1 = n_h2 = n_h3 = n_h4 = 0
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
            n_mix += w["n_mix"]
            n_mix_xor += w["n_mix_xor"]
            n_h1 += w["n_h1"]
            n_h2 += w["n_h2"]
            n_h3 += w["n_h3"]
            n_h4 += w["n_h4"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_mix": w["n_mix"],
                "n_h1": w["n_h1"],
                "n_h2": w["n_h2"],
                "n_h3": w["n_h3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_mix == 4383
        and n_mix_xor == 2216
        and n_h1 == 1666
        and n_h2 == 1672
        and n_h3 == 521
        and n_h4 == 524
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_xor": n_mix_xor,
        "n_h1": n_h1,
        "n_h2": n_h2,
        "n_h3": n_h3,
        "n_h4": n_h4,
        "rows": rows,
    }


def killed_mix_ham1_eq_flip_c() -> dict:
    """Mixed Hamming 1 is not flip_c: k=1, s=5, n=7, 0001 vs 1001."""
    k, s, n, j, j2, p, p2 = 1, 5, 7, 6, 8, 8, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (0, 0, 0, 1)
        and four2 == (1, 0, 0, 1)
        and four2 != flip_c(*four)
        and cob_shaped(*four) != cob_shaped(*four2)
        and zab_parity(four, four2) == 1
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
        "flip": list(flip_c(*four)),
    }


def killed_mix_ham2_no_c() -> dict:
    """Mixed Hamming 2 is not c-free: k=2, s=17, n=3, 0000 vs 0011."""
    k, s, n, j, j2, p, p2 = 2, 17, 3, 1, 5, 22, 14
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    slots = tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)
    ok = (
        four == (0, 0, 0, 0)
        and four2 == (0, 0, 1, 1)
        and slots == (2, 3)
        and 3 in slots
        and cob_shaped(*four) != cob_shaped(*four2)
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
        "slots": list(slots),
    }


def killed_mix_ham3_never_zab() -> dict:
    """Mixed Hamming 3 can be (z,a,b): k=2, s=19, n=2, 0111 vs 1001."""
    k, s, n, j, j2, p, p2 = 2, 19, 2, 0, 4, 24, 16
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    slots = tuple(i for i, (x, y) in enumerate(zip(four, four2)) if x != y)
    ok = (
        four == (0, 1, 1, 1)
        and four2 == (1, 0, 0, 1)
        and slots == (0, 1, 2)
        and 3 not in slots
        and cob_shaped(*four) != cob_shaped(*four2)
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
        "slots": list(slots),
    }


def prefixes() -> dict:
    ic = json.loads(IC_JSON.read_text())
    ok = (
        ic["checks"]["all_ok"]
        and ic["verdict"]["bn_AND_xor_from_Hamming_slots"] == "LEMMA"
        and ic["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, mc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and mc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert zab_parity((0, 0, 0, 1), (1, 0, 0, 1)) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = mix_slots_table()
    mc = mix_cover()
    k0 = killed_mix_ham1_eq_flip_c()
    k1 = killed_mix_ham2_no_c()
    k2 = killed_mix_ham3_never_zab()
    pref = prefixes()
    checks = self_checks(c20, rt, mc, k0, k1, k2, pref)
    dump = {
        "cycle": "ID",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "mix_slots_table": {k: rt[k] for k in rt if k != "ok"},
        "mix_cover": {k: mc[k] for k in mc if k != "ok"},
        "killed_mix_ham1_eq_flip_c": {k: k0[k] for k in k0 if k != "ok"},
        "killed_mix_ham2_no_c": {k: k1[k] for k in k1 if k != "ok"},
        "killed_mix_ham3_never_zab": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "mix_ham1_slots_no_c": True,
            "mix_ham2_slots_always_c": True,
            "mix_ham3_is_zab": True,
            "mix_ham1_eq_flip_c": False,
            "mix_ham2_no_c": False,
            "mix_ham3_never_zab": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mix_ham1_slots_no_c": "LEMMA",
            "mix_ham2_slots_always_c": "LEMMA",
            "mix_ham3_is_zab": "LEMMA",
            "mix_ham1_eq_flip_c": "KILLED",
            "mix_ham2_no_c": "KILLED",
            "mix_ham3_never_zab": "KILLED",
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
    print("mix_slots_table", dump["mix_slots_table"])
    cov = dump["mix_cover"]
    print(
        "mix_cover n_ok",
        cov["n_ok"],
        "n_mix",
        cov["n_mix"],
        "n_h1",
        cov["n_h1"],
        "n_h2",
        cov["n_h2"],
        "n_h3",
        cov["n_h3"],
        "n_h4",
        cov["n_h4"],
        "n_mix_xor",
        cov["n_mix_xor"],
    )
    print("killed_mix_ham1_eq_flip_c", dump["killed_mix_ham1_eq_flip_c"])
    print("killed_mix_ham2_no_c", dump["killed_mix_ham2_no_c"])
    print("killed_mix_ham3_never_zab", dump["killed_mix_ham3_never_zab"])


if __name__ == "__main__":
    main()
