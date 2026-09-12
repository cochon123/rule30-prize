#!/usr/bin/env python3
"""Cycle HX: dual packed indices palindrome; both-cob pairs drop out of J.

In-support dual columns have p+p'=2(T-2n). Both-cob G=1 pairs have
AND xor 0, so they drop out of the palindrome fold. Bit-reverse sends
CONT to cob 1100 and permutes the three FRESH. Dual 4-tuple is not
bit-reverse; cob-shape is not palindromic; center is not green4.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hx.py --certify
Dump: research/cycle_hx.json
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
from cycle_hi import CONT, FRESH
from cycle_hj import green4
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HW_JSON = Path(__file__).resolve().parent / "cycle_hw.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def reverse_four(z: int, a: int, b: int, c: int) -> tuple[int, int, int, int]:
    return (c, b, a, z)


def reverse_and_table() -> dict:
    """16-row: reverse sends CONT to cob 1100; FRESH to FRESH."""
    n_ok = 0
    fresh_rev = []
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        rev = reverse_four(*four)
        n_ok += 1
        if four == CONT:
            if rev != (1, 1, 0, 0) or not cob_shaped(*rev) or rev in AND_ONES:
                return {"ok": False, "cont": True, "rev": rev}
        if four in FRESH:
            if rev not in FRESH:
                return {"ok": False, "fresh": True, "four": four, "rev": rev}
            fresh_rev.append(rev)
    ok = (
        n_ok == 16
        and tuple(sorted(fresh_rev)) == tuple(sorted(FRESH))
        and reverse_four(*CONT) == (1, 1, 0, 0)
    )
    return {"ok": ok, "n_ok": n_ok}


def _walk_dual(k: int, q: int) -> dict:
    """Dual p-sum palindrome; both-cob AND xor 0."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_bothcob = n_rev = 0
    xor_j = xor_bothcob = 0
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
            pc = T - 2 * n
            for j in range(0, n):
                j2 = 2 * n - j
                if j not in bits or j2 not in bits:
                    continue
                if G(n, j) == 0:
                    continue
                f, a, p = bits[j]
                g, b, p2 = bits[j2]
                if p + p2 != 2 * pc:
                    return {"ok": False, "psum": True, "k": k, "p": p, "p2": p2, "pc": pc}
                n_pair += 1
                if f == reverse_four(*g):
                    n_rev += 1
                if cob_shaped(*f) and cob_shaped(*g):
                    n_bothcob += 1
                    if a or b:
                        return {"ok": False, "bothcob_and": True, "k": k, "four": f, "four2": g}
                    xor_bothcob ^= a ^ b
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_bothcob == 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bothcob": n_bothcob,
        "n_rev": n_rev,
        "xor_j": xor_j,
        "xor_bothcob": xor_bothcob,
    }


def dual_cover() -> dict:
    """Dual palindrome / both-cob drop on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_bothcob = n_rev = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dual(k, q)
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
            n_bothcob += w["n_bothcob"]
            n_rev += w["n_rev"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_pair": w["n_pair"],
                "n_bothcob": w["n_bothcob"],
                "n_rev": w["n_rev"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_pair == 8944 and n_bothcob == 2438 and n_rev == 536
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_bothcob": n_bothcob,
        "n_rev": n_rev,
        "rows": rows,
    }


def killed_dual_eq_reverse() -> dict:
    """Dual 4-tuple is not bit-reverse: k=1, s=9, n=1, fours 1100 vs 0001."""
    k, s, n, j, j2, p, p2 = 1, 9, 1, 0, 2, 12, 8
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == (1, 1, 0, 0)
        and four2 == (0, 0, 0, 1)
        and reverse_four(*four) == (0, 0, 1, 1)
        and four2 != reverse_four(*four)
        and j2 == 2 * n - j
        and G(n, j) == 1
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
        "rev": list(reverse_four(*four)),
    }


def killed_cob_palindrome() -> dict:
    """Cob-shape is not palindromic on G=1: k=1, s=5, n=7, 0001 vs 1001."""
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
        and cob_shaped(*four)
        and (not cob_shaped(*four2))
        and G(n, j) == 1
        and G(n, j2) == 1
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


def killed_center_eq_green4() -> dict:
    """Center 4-tuple is not green4: k=0, s=3, n=1, 1001 vs 1010."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    g4 = green4(n, n)
    Aodd = (row << 1) & row
    packed = (Aodd >> p) & 1
    ok = j == n and four == (1, 0, 0, 1) and g4 == (1, 0, 1, 0) and four != g4 and packed == 1
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
        "packed": packed,
    }


def prefixes() -> dict:
    hw = json.loads(HW_JSON.read_text())
    ok = (
        hw["checks"]["all_ok"]
        and hw["verdict"]["covering_J_eq_center_XOR_pair_disagreements"] == "LEMMA"
        and hw["verdict"]["unpaired_G1_four_0000"] == "LEMMA"
        and hw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, dc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and dc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert reverse_four(0, 0, 1, 1) == (1, 1, 0, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = reverse_and_table()
    dc = dual_cover()
    k0 = killed_dual_eq_reverse()
    k1 = killed_cob_palindrome()
    k2 = killed_center_eq_green4()
    pref = prefixes()
    checks = self_checks(c20, rt, dc, k0, k1, k2, pref)
    dump = {
        "cycle": "HX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "reverse_and_table": {k: rt[k] for k in rt if k != "ok"},
        "dual_cover": {k: dc[k] for k in dc if k != "ok"},
        "killed_dual_eq_reverse": {k: k0[k] for k in k0 if k != "ok"},
        "killed_cob_palindrome": {k: k1[k] for k in k1 if k != "ok"},
        "killed_center_eq_green4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_packed_index_palindrome": True,
            "both_cob_pairs_AND_xor_0": True,
            "reverse_CONT_to_cob_1100": True,
            "dual_eq_bit_reverse": False,
            "cob_palindrome_on_G1": False,
            "center_eq_green4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_packed_index_palindrome": "LEMMA",
            "both_cob_pairs_AND_xor_0": "LEMMA",
            "reverse_CONT_to_cob_1100": "LEMMA",
            "dual_eq_bit_reverse": "KILLED",
            "cob_palindrome_on_G1": "KILLED",
            "center_eq_green4": "KILLED",
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
    print("reverse_and_table", dump["reverse_and_table"])
    cov = dump["dual_cover"]
    print(
        "dual_cover n_ok",
        cov["n_ok"],
        "n_pair",
        cov["n_pair"],
        "n_bothcob",
        cov["n_bothcob"],
        "n_rev",
        cov["n_rev"],
    )
    print("killed_dual_eq_reverse", dump["killed_dual_eq_reverse"])
    print("killed_cob_palindrome", dump["killed_cob_palindrome"])
    print("killed_center_eq_green4", dump["killed_center_eq_green4"])


if __name__ == "__main__":
    main()
