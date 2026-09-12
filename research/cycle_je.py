#!/usr/bin/env python3
"""Cycle JE: dual of iso1_lift5 is the bit-reverse of the parent 5-window.

Palindrome dual j -> 2n-j reverses the parent 5-window, swapping
11000 with 00011. Windows 01110 and 10101 are palindromes, so odd-n
isolated ones (all 10101) are self-dual on the window. Dual of 00011
is not 00011; dual of 10101 is not 00011; dual lift is the reverse.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_je.py --certify
Dump: research/cycle_je.json
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
from cycle_ir import isolated_one
from cycle_jd import LIFT1, LIFT1_ODD, iso1_lift5
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JD_JSON = Path(__file__).resolve().parent / "cycle_jd.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT1_SWAP = ((1, 1, 0, 0, 0), (0, 0, 0, 1, 1))
LIFT1_PAL = ((0, 1, 1, 1, 0), (1, 0, 1, 0, 1))


def lift5_rev(five):
    """Bit-reverse of a parent 5-window."""
    return five[::-1]


def dual_iso_start(n: int, j: int) -> int:
    """Palindrome dual of an isolated one at j."""
    return 2 * n - j


def lift_rev_table() -> dict:
    """n<64: dual iso1_lift5 is reverse; LIFT1 swap/palindrome split."""
    if lift5_rev(LIFT1_SWAP[0]) != LIFT1_SWAP[1]:
        return {"ok": False, "swap": True}
    if lift5_rev(LIFT1_SWAP[1]) != LIFT1_SWAP[0]:
        return {"ok": False, "swap2": True}
    for five in LIFT1_PAL:
        if lift5_rev(five) != five:
            return {"ok": False, "pal": True, "five": list(five)}
    if set(LIFT1) != set(LIFT1_SWAP + LIFT1_PAL):
        return {"ok": False, "fam": True}
    n_iso = n_seed = n_pal = n_swap = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            j2 = dual_iso_start(n, j)
            if not isolated_one(n, j2):
                return {"ok": False, "dual": True, "n": n, "j": j}
            if n == 0:
                n_seed += 1
                continue
            five = iso1_lift5(n, j)
            five2 = iso1_lift5(n, j2)
            if five2 != lift5_rev(five):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "j2": j2,
                }
            if five == five2:
                n_pal += 1
            else:
                n_swap += 1
    ok = n_iso == 461 and n_seed == 1 and n_pal == 230 and n_swap == 230
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_pal": n_pal,
        "n_swap": n_swap,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support iso1_lift5 reverse on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_dual = n_seed = n_pal = n_swap = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in bits:
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                if n == 0:
                    n_seed += 1
                    continue
                j2 = dual_iso_start(n, j)
                if j2 not in bits:
                    continue
                five = iso1_lift5(n, j)
                five2 = iso1_lift5(n, j2)
                if five2 != lift5_rev(five):
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if five == five2:
                    n_pal += 1
                else:
                    n_swap += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_dual": n_dual,
        "n_seed": n_seed,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "xor_j": xor_j,
    }


def lift_rev_cover() -> dict:
    """Dual-in-support reverse on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_dual = n_seed = n_pal = n_swap = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rev(k, q)
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
            n_dual += w["n_dual"]
            n_seed += w["n_seed"]
            n_pal += w["n_pal"]
            n_swap += w["n_swap"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_iso": w["n_iso"],
                "n_dual": w["n_dual"],
                "n_seed": w["n_seed"],
                "n_pal": w["n_pal"],
                "n_swap": w["n_swap"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_seed == 14
        and n_dual == 6442
        and n_pal == 3146
        and n_swap == 3296
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_dual": n_dual,
        "n_seed": n_seed,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "rows": rows,
    }


def killed_00011_stays() -> dict:
    """Dual of 00011 is 00011: G(2,0) reverses to 11000."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n, j2)
    ok = (
        isolated_one(n, j)
        and five == (0, 0, 0, 1, 1)
        and five2 == lift5_rev(five) == (1, 1, 0, 0, 0)
        and five2 != five
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
        "five": list(five),
        "five2": list(five2),
    }


def killed_10101_to_00011() -> dict:
    """Dual of 10101 is 00011: G(3,3) is self-dual 10101."""
    k, s, n, j, p = 0, 3, 3, 3, 4
    j2 = dual_iso_start(n, j)
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n, j2)
    ok = (
        isolated_one(n, j)
        and j2 == j
        and five == LIFT1_ODD
        and five2 == five
        and five != (0, 0, 0, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "five": list(five),
        "five2": list(five2),
    }


def killed_dual_not_reverse() -> dict:
    """Dual lift is not reverse: G(2,0) dual equals reverse."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    five = iso1_lift5(n, j)
    five2 = iso1_lift5(n, j2)
    ok = five2 == lift5_rev(five) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def prefixes() -> dict:
    jd = json.loads(JD_JSON.read_text())
    ok = (
        jd["checks"]["all_ok"]
        and jd["verdict"]["LIFT1_sat"] == "LEMMA"
        and jd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert lift5_rev((0, 0, 0, 1, 1)) == (1, 1, 0, 0, 0)
    assert lift5_rev(LIFT1_ODD) == LIFT1_ODD
    assert dual_iso_start(2, 0) == 4
    assert iso1_lift5(2, 4) == lift5_rev(iso1_lift5(2, 0))
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift_rev_table()
    sc = lift_rev_cover()
    k0 = killed_00011_stays()
    k1 = killed_10101_to_00011()
    k2 = killed_dual_not_reverse()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "lift_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_00011_stays": {k: k0[k] for k in k0 if k != "ok"},
        "killed_10101_to_00011": {k: k1[k] for k in k1 if k != "ok"},
        "killed_dual_not_reverse": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "dual_lift5_rev": True,
            "lift5_rev_swap": True,
            "covering_lift5_rev": True,
            "00011_stays": False,
            "10101_to_00011": False,
            "dual_not_reverse": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "dual_lift5_rev": "LEMMA",
            "lift5_rev_swap": "LEMMA",
            "covering_lift5_rev": "LEMMA",
            "00011_stays": "KILLED",
            "10101_to_00011": "KILLED",
            "dual_not_reverse": "KILLED",
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
    print("lift_rev_table", dump["lift_rev_table"])
    cov = dump["lift_rev_cover"]
    print(
        "lift_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_iso",
        cov["n_iso"],
        "n_dual",
        cov["n_dual"],
        "n_seed",
        cov["n_seed"],
        "n_pal",
        cov["n_pal"],
        "n_swap",
        cov["n_swap"],
    )
    print("killed_00011_stays", dump["killed_00011_stays"])
    print("killed_10101_to_00011", dump["killed_10101_to_00011"])
    print("killed_dual_not_reverse", dump["killed_dual_not_reverse"])


if __name__ == "__main__":
    main()
