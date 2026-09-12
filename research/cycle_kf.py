#!/usr/bin/env python3
"""Cycle KF: dual of each G=1 FRESH pattern takes all 16 packed 4-tuples.

Covering dual 4-tuples of 0010, 0100, and 1001 each hit every 16-row.
Dual of 0010 is not 0010; dual of 0010 is not bit-reverse 0100; dual
AND xor does not vanish. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_kf.py --certify
Dump: research/cycle_kf.json
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
from cycle_hi import FRESH
from cycle_hu import and_clause
from cycle_hx import reverse_four
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KE_JSON = Path(__file__).resolve().parent / "cycle_ke.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

FRESH_KEYS = tuple("".join(map(str, four)) for four in FRESH)
F0010 = (0, 0, 1, 0)
F0010_REV = (0, 1, 0, 0)

WANT = {
    "0010": {"n": 1014, "ctr": 85, "pair": 929, "andxor": 686},
    "0100": {"n": 1280, "ctr": 68, "pair": 1212, "andxor": 919},
    "1001": {"n": 1082, "ctr": 26, "pair": 1056, "andxor": 810},
}


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def _empty_pat() -> dict:
    return {
        "n": 0,
        "ctr": 0,
        "pair": 0,
        "andxor": 0,
        "types": {f"{i:04b}": 0 for i in range(16)},
    }


def fresh_rev_table() -> dict:
    """16-row: reverse permutes FRESH; 1001 is a palindrome."""
    n_ok = 0
    rev = []
    for four in FRESH:
        n_ok += 1
        r = reverse_four(*four)
        if r not in FRESH:
            return {"ok": False, "fresh": True, "four": list(four), "rev": list(r)}
        rev.append(r)
        if and_clause(*four) != 1:
            return {"ok": False, "and": True, "four": list(four)}
    ok = (
        n_ok == 3
        and reverse_four(*F0010) == F0010_REV
        and reverse_four(*F0010_REV) == F0010
        and reverse_four(*(1, 0, 0, 1)) == (1, 0, 0, 1)
        and tuple(sorted(rev)) == tuple(sorted(FRESH))
    )
    return {"ok": ok, "n_ok": n_ok}


def _walk_dual(k: int, q: int) -> dict:
    """Dual 4-tuple census of G=1 FRESH; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    pats = {key: _empty_pat() for key in FRESH_KEYS}
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
                bits[j] = (four, packed, p)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
                    if four in FRESH:
                        rec = pats[_fmt(four)]
                        rec["n"] += 1
                        if j == n:
                            rec["ctr"] += 1
            for j, (four, packed, p) in bits.items():
                if G(n, j) == 0 or four not in FRESH or j == n:
                    continue
                j2 = 2 * n - j
                if j2 not in bits:
                    continue
                four2, packed2, p2 = bits[j2]
                rec = pats[_fmt(four)]
                rec["pair"] += 1
                rec["types"][_fmt(four2)] += 1
                if packed ^ packed2:
                    rec["andxor"] += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "pats": pats,
        "xor_j": xor_j,
    }


def _add_pat(dst: dict, src: dict) -> None:
    dst["n"] += src["n"]
    dst["ctr"] += src["ctr"]
    dst["pair"] += src["pair"]
    dst["andxor"] += src["andxor"]
    for key in dst["types"]:
        dst["types"][key] += src["types"][key]


def _pat_ok(got: dict, want: dict) -> bool:
    n_types = sum(1 for v in got["types"].values() if v)
    return (
        got["n"] == want["n"]
        and got["ctr"] == want["ctr"]
        and got["pair"] == want["pair"]
        and got["andxor"] == want["andxor"]
        and got["pair"] == got["n"] - got["ctr"]
        and n_types == 16
        and all(got["types"][key] > 0 for key in got["types"])
    )


def fresh_dual_cover() -> dict:
    """Dual FRESH census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = 0
    pats = {key: _empty_pat() for key in FRESH_KEYS}
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
            n_g1 += w["n_g1"]
            for key in FRESH_KEYS:
                _add_pat(pats[key], w["pats"][key])
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_fresh": sum(w["pats"][key]["n"] for key in FRESH_KEYS),
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    n_fresh = sum(pats[key]["n"] for key in FRESH_KEYS)
    n_pair = sum(pats[key]["pair"] for key in FRESH_KEYS)
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_fresh == 3376
        and n_pair == 3197
        and all(_pat_ok(pats[key], WANT[key]) for key in FRESH_KEYS)
    )
    for key in FRESH_KEYS:
        pats[key]["n_types"] = sum(1 for v in pats[key]["types"].values() if v)
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_fresh": n_fresh,
        "n_pair": n_pair,
        "pats": pats,
        "rows": rows,
    }


def _kill_pair(k: int, s_hit: int, n_hit: int, j_hit: int, p_hit: int, p2_hit: int):
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p_hit - 3 + i) for i in range(4))
    four2 = tuple(bit_at(prev, p2_hit - 3 + i) for i in range(4))
    j2 = 2 * n_hit - j_hit
    return k, s_hit, n_hit, j_hit, j2, p_hit, p2_hit, four, four2


def killed_fresh_self() -> dict:
    """Dual of G=1 0010 is 0010: G(7,4) dual is 0001."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(2, 25, 7, 4, 32, 20)
    ok = (
        G(n, j) == 1
        and G(n, j2) == 1
        and four == F0010
        and four2 == (0, 0, 0, 1)
        and four2 != four
        and four2 != reverse_four(*four)
        and j2 == 2 * n - j
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


def killed_fresh_rev() -> dict:
    """Dual of G=1 0010 is bit-reverse 0100: same witness is 0001."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(2, 25, 7, 4, 32, 20)
    ok = (
        G(n, j) == 1
        and four == F0010
        and reverse_four(*four) == F0010_REV
        and four2 == (0, 0, 0, 1)
        and four2 != reverse_four(*four)
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
        "rev": list(reverse_four(*four)),
    }


def killed_fresh_andxor0() -> dict:
    """Dual AND xor of G=1 0010 vanishes: dual 0001 has packed AND 0."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(2, 25, 7, 4, 32, 20)
    ok = (
        G(n, j) == 1
        and four == F0010
        and four2 == (0, 0, 0, 1)
        and and_clause(*four) == 1
        and and_clause(*four2) == 0
        and (and_clause(*four) ^ and_clause(*four2)) == 1
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
    ke = json.loads(KE_JSON.read_text())
    ok = (
        ke["checks"]["all_ok"]
        and ke["verdict"]["fresh_g1_all_shapes"] == "LEMMA"
        and ke["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert FRESH == ((0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1))
    assert reverse_four(*F0010) == F0010_REV
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = fresh_rev_table()
    sc = fresh_dual_cover()
    k0 = killed_fresh_self()
    k1 = killed_fresh_rev()
    k2 = killed_fresh_andxor0()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "fresh_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "fresh_dual_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_fresh_self": {k: k0[k] for k in k0 if k != "ok"},
        "killed_fresh_rev": {k: k1[k] for k in k1 if k != "ok"},
        "killed_fresh_andxor0": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "fresh_reverse": True,
            "fresh_dual_all_16": True,
            "covering_fresh_dual": True,
            "fresh_self": False,
            "fresh_rev": False,
            "fresh_andxor0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "fresh_reverse": "LEMMA",
            "fresh_dual_all_16": "LEMMA",
            "covering_fresh_dual": "LEMMA",
            "fresh_self": "KILLED",
            "fresh_rev": "KILLED",
            "fresh_andxor0": "KILLED",
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
    print("fresh_rev_table", dump["fresh_rev_table"])
    cov = dump["fresh_dual_cover"]
    print(
        "fresh_dual_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_fresh",
        cov["n_fresh"],
        "n_pair",
        cov["n_pair"],
        "pats",
        {
            key: {
                k: cov["pats"][key][k]
                for k in ("n", "ctr", "pair", "andxor", "n_types")
            }
            for key in FRESH_KEYS
        },
    )
    print("killed_fresh_self", dump["killed_fresh_self"])
    print("killed_fresh_rev", dump["killed_fresh_rev"])
    print("killed_fresh_andxor0", dump["killed_fresh_andxor0"])


if __name__ == "__main__":
    main()
