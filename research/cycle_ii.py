#!/usr/bin/env python3
"""Cycle II: consecutive 4-tuples overlap stride-2; error is a bit-string.

Packed, green4, and packed-XOR-green4 4-tuples at j and j+1 share
(z,a)_j = (b,c)_{j+1}. Error is cob-shaped iff the packed 4-tuple is.
Consecutive packed 4-tuples are not independent; consecutive green4
are not equal; consecutive G=1 AND does fire. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ii.py --certify
Dump: research/cycle_ii.json
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
from cycle_ht import cob_shaped
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IH_JSON = Path(__file__).resolve().parent / "cycle_ih.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def xor4(four, four2) -> tuple[int, int, int, int]:
    """Componentwise GF(2) difference of two 4-tuples."""
    return tuple(x ^ y for x, y in zip(four, four2))  # type: ignore[return-value]


def stride2_overlap(left, right) -> bool:
    """(z,a) of left equals (b,c) of right (j vs j+1)."""
    return left[:2] == right[2:]


def error4(four, g4) -> tuple[int, int, int, int]:
    """Packed-vs-Green discrepancy 4-tuple."""
    return xor4(four, g4)


def cob_g4s() -> tuple[tuple[int, int, int, int], ...]:
    """The 8 coboundary-shaped 4-tuples."""
    out = []
    for z in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                out.append((z, z ^ b, b, c))
    return tuple(out)


def overlap_table() -> dict:
    """n<64: green4 stride-2 overlap; 16x8 error cob iff packed cob."""
    n_g4 = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            if not stride2_overlap(green4(n, j), green4(n, j + 1)):
                return {"ok": False, "g4": True, "n": n, "j": j}
            n_g4 += 1
    n_row = 0
    for g4 in cob_g4s():
        if not cob_shaped(*g4):
            return {"ok": False, "g4cob": True, "g4": g4}
        for bits in range(16):
            four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
            err = error4(four, g4)
            if cob_shaped(*err) != cob_shaped(*four):
                return {"ok": False, "cob": True, "four": four, "g4": g4}
            n_row += 1
    ok = n_g4 == 4032 and n_row == 128
    return {"ok": ok, "n_g4": n_g4, "n_row": n_row}


def _walk_ov(k: int, q: int) -> dict:
    """Stride-2 overlap of packed/green4/error; cob error iff packed cob."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_ov = n_g1 = n_g1_and = 0
    n_consec_g1 = n_both_and = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                g4 = green4(n, j)
                err = error4(four, g4)
                if cob_shaped(*err) != cob_shaped(*four):
                    return {"ok": False, "cob": True, "k": k, "four": four}
                bits[j] = (four, g4, err, packed, p)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        n_g1_and += 1
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                f, g4, e, a, p = bits[j]
                f2, g42, e2, a2, p2 = bits[j + 1]
                if p2 != p - 2:
                    return {"ok": False, "p": True, "k": k, "j": j}
                if not stride2_overlap(f, f2):
                    return {"ok": False, "pack_ov": True, "k": k, "four": f}
                if not stride2_overlap(g4, g42):
                    return {"ok": False, "g4_ov": True, "k": k, "g4": g4}
                if not stride2_overlap(e, e2):
                    return {"ok": False, "err_ov": True, "k": k, "err": e}
                n_ov += 1
                if G(n, j) and G(n, j + 1):
                    n_consec_g1 += 1
                    if a and a2:
                        n_both_and += 1
        row = rule30_step(row)
        s += 1
    ok = n_ok > 0 and n_ov > 0
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_ov": n_ov,
        "n_g1": n_g1,
        "n_g1_and": n_g1_and,
        "n_consec_g1": n_consec_g1,
        "n_both_and": n_both_and,
        "xor_j": xor_j,
    }


def ov_cover() -> dict:
    """Stride-2 overlap on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_ov = n_g1 = n_g1_and = 0
    n_consec_g1 = n_both_and = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_ov(k, q)
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
            n_ov += w["n_ov"]
            n_g1 += w["n_g1"]
            n_g1_and += w["n_g1_and"]
            n_consec_g1 += w["n_consec_g1"]
            n_both_and += w["n_both_and"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_ov": w["n_ov"],
                "n_g1": w["n_g1"],
                "n_g1_and": w["n_g1_and"],
                "n_consec_g1": w["n_consec_g1"],
                "n_both_and": w["n_both_and"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_ov == 95059
        and n_g1 == 22659
        and n_g1_and == 4522
        and n_consec_g1 == 8577
        and n_both_and == 463
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_ov": n_ov,
        "n_g1": n_g1,
        "n_g1_and": n_g1_and,
        "n_consec_g1": n_consec_g1,
        "n_both_and": n_both_and,
        "rows": rows,
    }


def _seed_pair():
    """k=0, s=3, n=1, j=0 vs 1 on q=6."""
    k, s, n, j, j2, p, p2 = 0, 3, 1, 0, 1, 6, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2 - 3 + i) for i in range(4))
    g4 = green4(n, j)
    g42 = green4(n, j2)
    err = error4(four, g4)
    err2 = error4(four2, g42)
    return k, s, n, j, j2, p, p2, four, four2, g4, g42, err, err2


def killed_pack_independent() -> dict:
    """Consecutive packed 4-tuples are not independent: 0100 vs 1001."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, err, err2 = _seed_pair()
    ok = (
        four == (0, 1, 0, 0)
        and four2 == (1, 0, 0, 1)
        and four != four2
        and stride2_overlap(four, four2)
        and j2 == j + 1
        and p2 == p - 2
        and p >= 4
        and p2 >= 4
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


def killed_g4_equal() -> dict:
    """Consecutive green4 are not equal: 1011 vs 1010."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, err, err2 = _seed_pair()
    ok = (
        g4 == (1, 0, 1, 1)
        and g42 == (1, 0, 1, 0)
        and g4 != g42
        and stride2_overlap(g4, g42)
        and j2 == j + 1
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
        "g4": list(g4),
        "g42": list(g42),
    }


def killed_no_consec_g1_and() -> dict:
    """Consecutive G=1 AND does fire: 0100 vs 1001, both AND."""
    k, s, n, j, j2, p, p2, four, four2, g4, g42, err, err2 = _seed_pair()
    ok = (
        four == (0, 1, 0, 0)
        and four2 == (1, 0, 0, 1)
        and and_clause(*four) == 1
        and and_clause(*four2) == 1
        and G(n, j) == 1
        and G(n, j2) == 1
        and stride2_overlap(err, err2)
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
        "err": list(err),
        "err2": list(err2),
        "and": and_clause(*four),
        "and2": and_clause(*four2),
    }


def prefixes() -> dict:
    ih = json.loads(IH_JSON.read_text())
    ok = (
        ih["checks"]["all_ok"]
        and ih["verdict"]["dual_swaps_G_neighbors"] == "LEMMA"
        and ih["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert stride2_overlap((0, 1, 0, 0), (1, 0, 0, 1))
    assert error4((0, 1, 0, 0), (1, 0, 1, 1)) == (1, 1, 1, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = overlap_table()
    sc = ov_cover()
    k0 = killed_pack_independent()
    k1 = killed_g4_equal()
    k2 = killed_no_consec_g1_and()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "II",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "overlap_table": {k: rt[k] for k in rt if k != "ok"},
        "ov_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_pack_independent": {k: k0[k] for k in k0 if k != "ok"},
        "killed_g4_equal": {k: k1[k] for k in k1 if k != "ok"},
        "killed_no_consec_g1_and": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "stride2_overlap_packed_green4_error": True,
            "error_cob_iff_packed_cob": True,
            "covering_stride2_overlap": True,
            "pack_independent": False,
            "g4_equal": False,
            "no_consec_g1_and": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "stride2_overlap_packed_green4_error": "LEMMA",
            "error_cob_iff_packed_cob": "LEMMA",
            "covering_stride2_overlap": "LEMMA",
            "pack_independent": "KILLED",
            "g4_equal": "KILLED",
            "no_consec_g1_and": "KILLED",
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
    print("overlap_table", dump["overlap_table"])
    cov = dump["ov_cover"]
    print(
        "ov_cover n_ok",
        cov["n_ok"],
        "n_ov",
        cov["n_ov"],
        "n_g1",
        cov["n_g1"],
        "n_both_and",
        cov["n_both_and"],
    )
    print("killed_pack_independent", dump["killed_pack_independent"])
    print("killed_g4_equal", dump["killed_g4_equal"])
    print("killed_no_consec_g1_and", dump["killed_no_consec_g1_and"])


if __name__ == "__main__":
    main()
