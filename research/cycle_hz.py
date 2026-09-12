#!/usr/bin/env python3
"""Cycle HZ: bitwise complement swaps cob/non-cob; same-class never Hamming 4.

complement_four flips all four bits. That swaps cob-shape with non-cob,
so AND_ONES maps to cob (AND=0). CONT complement is cob 1100, same as
reverse. Covering same-class duals (both-cob and both-non-cob) never
have Hamming 4. Dual is not complement; complement is not reverse;
complement does not preserve AND. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_hz.py --certify
Dump: research/cycle_hz.json
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
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from cycle_hx import reverse_four
from cycle_hy import mixed_oneside
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HY_JSON = Path(__file__).resolve().parent / "cycle_hy.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def complement_four(z: int, a: int, b: int, c: int) -> tuple[int, int, int, int]:
    return (1 - z, 1 - a, 1 - b, 1 - c)


def complement_and_table() -> dict:
    """16-row: complement swaps cob/non-cob; AND maps to cob; CONT to 1100."""
    n_ok = n_cob = n_nc = 0
    and_comp = []
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        comp = complement_four(*four)
        n_ok += 1
        cs, cc = cob_shaped(*four), cob_shaped(*comp)
        if cs == cc:
            return {"ok": False, "swap": True, "four": four, "comp": comp}
        if cs:
            n_cob += 1
        else:
            n_nc += 1
        ham = sum(x != y for x, y in zip(four, comp))
        if ham != 4:
            return {"ok": False, "ham": True, "four": four}
        if four in AND_ONES:
            if (not cc) or and_clause(*comp):
                return {"ok": False, "and": True, "four": four, "comp": comp}
            and_comp.append(comp)
        if four == CONT:
            if comp != (1, 1, 0, 0) or comp != reverse_four(*four):
                return {"ok": False, "cont": True, "comp": comp}
        if four in FRESH and cob_shaped(*reverse_four(*four)):
            return {"ok": False, "fresh_rev": True, "four": four}
    ok = (
        n_ok == 16
        and n_cob == 8
        and n_nc == 8
        and len(and_comp) == 4
        and complement_four(*CONT) == (1, 1, 0, 0)
    )
    return {"ok": ok, "n_ok": n_ok, "n_cob": n_cob, "n_nc": n_nc}


def _walk_comp(k: int, q: int) -> dict:
    """Same-class duals never Hamming 4; mixed Hamming 4 iff complement."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_pair = n_mix = n_bn = n_bc = 0
    n_mix_ham4 = n_bn_ham4 = n_bc_ham4 = 0
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
                ham = sum(x != y for x, y in zip(f, g))
                is_comp = f == complement_four(*g)
                if is_comp != (ham == 4):
                    return {"ok": False, "ham4": True, "k": k, "four": f, "four2": g}
                c1, c2 = cob_shaped(*f), cob_shaped(*g)
                mo = mixed_oneside(f, g)
                if c1 != c2:
                    n_mix += 1
                    if ham == 4:
                        n_mix_ham4 += 1
                    if mo != (a ^ b):
                        return {"ok": False, "oneside": True, "k": k}
                    if a ^ b:
                        xor_fold ^= 1
                elif c1 and c2:
                    n_bc += 1
                    if ham == 4 or is_comp or a or b:
                        return {
                            "ok": False,
                            "bc_ham4": True,
                            "k": k,
                            "four": f,
                            "four2": g,
                        }
                    n_bc_ham4 += int(ham == 4)
                else:
                    n_bn += 1
                    if ham == 4 or is_comp:
                        return {
                            "ok": False,
                            "bn_ham4": True,
                            "k": k,
                            "four": f,
                            "four2": g,
                        }
                    n_bn_ham4 += int(ham == 4)
                    if a ^ b:
                        xor_fold ^= 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and xor_fold == xor_j and n_bn_ham4 == 0 and n_bc_ham4 == 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_ham4": n_mix_ham4,
        "n_bn": n_bn,
        "n_bn_ham4": n_bn_ham4,
        "n_bc": n_bc,
        "n_bc_ham4": n_bc_ham4,
        "xor_j": xor_j,
    }


def comp_cover() -> dict:
    """Complement Hamming-4 split on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_pair = n_mix = n_mix_ham4 = 0
    n_bn = n_bn_ham4 = n_bc = n_bc_ham4 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_comp(k, q)
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
            n_mix_ham4 += w["n_mix_ham4"]
            n_bn += w["n_bn"]
            n_bn_ham4 += w["n_bn_ham4"]
            n_bc += w["n_bc"]
            n_bc_ham4 += w["n_bc_ham4"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_pair": w["n_pair"],
                "n_mix_ham4": w["n_mix_ham4"],
                "n_bn_ham4": w["n_bn_ham4"],
                "n_bc_ham4": w["n_bc_ham4"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_pair == 8944
        and n_mix == 4383
        and n_mix_ham4 == 524
        and n_bn == 2123
        and n_bn_ham4 == 0
        and n_bc == 2438
        and n_bc_ham4 == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pair": n_pair,
        "n_mix": n_mix,
        "n_mix_ham4": n_mix_ham4,
        "n_bn": n_bn,
        "n_bn_ham4": n_bn_ham4,
        "n_bc": n_bc,
        "n_bc_ham4": n_bc_ham4,
        "rows": rows,
    }


def killed_dual_eq_complement() -> dict:
    """Dual 4-tuple is not complement: k=1, s=5, n=7, 0001 vs 1001."""
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
        and four != complement_four(*four2)
        and sum(x != y for x, y in zip(four, four2)) == 1
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
        "comp": list(complement_four(*four2)),
    }


def killed_complement_eq_reverse() -> dict:
    """Complement is not reverse: k=0, s=7, n=1, four 0010."""
    k, s, n, j, p = 0, 7, 1, 0, 10
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    rev = reverse_four(*four)
    comp = complement_four(*four)
    ok = (
        four == (0, 0, 1, 0)
        and rev == (0, 1, 0, 0)
        and comp == (1, 1, 0, 1)
        and rev != comp
        and four in FRESH
        and cob_shaped(*comp)
        and G(n, j) == 1
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
        "rev": list(rev),
        "comp": list(comp),
    }


def killed_complement_preserves_and() -> dict:
    """Complement does not preserve AND: mixed pair 0011 vs 1100."""
    k, s, n, j, j2, p, p2 = 2, 17, 3, 0, 6, 24, 12
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    ok = (
        four == CONT
        and four2 == (1, 1, 0, 0)
        and four2 == complement_four(*four)
        and and_clause(*four) == 1
        and and_clause(*four2) == 0
        and cob_shaped(*four2)
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


def prefixes() -> dict:
    hy = json.loads(HY_JSON.read_text())
    ok = (
        hy["checks"]["all_ok"]
        and hy["verdict"]["mixed_oneside_AND_xor"] == "LEMMA"
        and hy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, cc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and cc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert complement_four(0, 0, 1, 1) == (1, 1, 0, 0)
    assert complement_four(0, 0, 1, 0) == (1, 1, 0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = complement_and_table()
    cc = comp_cover()
    k0 = killed_dual_eq_complement()
    k1 = killed_complement_eq_reverse()
    k2 = killed_complement_preserves_and()
    pref = prefixes()
    checks = self_checks(c20, rt, cc, k0, k1, k2, pref)
    dump = {
        "cycle": "HZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "complement_and_table": {k: rt[k] for k in rt if k != "ok"},
        "comp_cover": {k: cc[k] for k in cc if k != "ok"},
        "killed_dual_eq_complement": {k: k0[k] for k in k0 if k != "ok"},
        "killed_complement_eq_reverse": {k: k1[k] for k in k1 if k != "ok"},
        "killed_complement_preserves_and": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "complement_swaps_cob_noncob": True,
            "AND_complement_is_cob": True,
            "same_class_duals_never_hamming4": True,
            "dual_eq_complement": False,
            "complement_eq_reverse": False,
            "complement_preserves_and": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "complement_swaps_cob_noncob": "LEMMA",
            "AND_complement_is_cob": "LEMMA",
            "same_class_duals_never_hamming4": "LEMMA",
            "dual_eq_complement": "KILLED",
            "complement_eq_reverse": "KILLED",
            "complement_preserves_and": "KILLED",
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
    print("complement_and_table", dump["complement_and_table"])
    cov = dump["comp_cover"]
    print(
        "comp_cover n_ok",
        cov["n_ok"],
        "n_pair",
        cov["n_pair"],
        "n_mix_ham4",
        cov["n_mix_ham4"],
        "n_bn_ham4",
        cov["n_bn_ham4"],
        "n_bc_ham4",
        cov["n_bc_ham4"],
    )
    print("killed_dual_eq_complement", dump["killed_dual_eq_complement"])
    print("killed_complement_eq_reverse", dump["killed_complement_eq_reverse"])
    print("killed_complement_preserves_and", dump["killed_complement_preserves_and"])


if __name__ == "__main__":
    main()
