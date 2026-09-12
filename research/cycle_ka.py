#!/usr/bin/env python3
"""Cycle KA: packed AND is not the trinomial adjacent AND.

Rule 30 is a XOR (b OR c) = (a XOR b XOR c) XOR (b AND c). Packed
AND fires on AND_ONES = FRESH cup CONT; trinomial AND fires on
FRESH cup 1111. They disagree on CONT vs 1111. Covering J is packed
AND on G=1, not trinomial AND. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_ka.py --certify
Dump: research/cycle_ka.json
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
from cycle_hu import and_clause
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JZ_JSON = Path(__file__).resolve().parent / "cycle_jz.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

TRI_ONES = FRESH + ((1, 1, 1, 1),)
DIE1111 = (1, 1, 1, 1)


def tri_bit(z: int, a: int, b: int, c: int) -> int:
    """Rule-30 bit as trinomial XOR adjacent AND."""
    return a ^ b ^ c ^ (b & c)


def tri_and(z: int, a: int, b: int, c: int) -> int:
    """Adjacent-bit AND of the trinomial (Rule 150) image."""
    return (a ^ b ^ c) & (z ^ a ^ b)


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def tri_table() -> dict:
    """16-row: Rule 30 = trinomial XOR AND; packed vs tri AND sets."""
    n_ok = n_and = n_tri = n_xor = 0
    packed_ones = []
    tri_ones = []
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        z, a, b, c = four
        new_p = a ^ (b | c)
        new_pm = z ^ (a | b)
        if new_p != tri_bit(*four) or new_p != ((a ^ b ^ c) ^ (b & c)):
            return {"ok": False, "bit": True, "four": list(four)}
        if new_pm != ((z ^ a ^ b) ^ (a & b)):
            return {"ok": False, "bitm": True, "four": list(four)}
        an = and_clause(*four)
        ta = tri_and(*four)
        if an != int(four in AND_ONES) or ta != int(four in TRI_ONES):
            return {"ok": False, "set": True, "four": list(four)}
        if an != (new_p & new_pm):
            return {"ok": False, "prod": True, "four": list(four)}
        n_ok += 1
        if an:
            n_and += 1
            packed_ones.append(four)
        if ta:
            n_tri += 1
            tri_ones.append(four)
        if an ^ ta:
            n_xor += 1
    ok = (
        n_ok == 16
        and n_and == 4
        and n_tri == 4
        and n_xor == 2
        and tuple(packed_ones) == AND_ONES
        and tuple(tri_ones) == TRI_ONES
        and CONT not in TRI_ONES
        and DIE1111 not in AND_ONES
        and CONT in AND_ONES
        and DIE1111 in TRI_ONES
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_and": n_and,
        "n_tri": n_tri,
        "n_xor": n_xor,
    }


def _walk_tri(k: int, q: int) -> dict:
    """Packed vs trinomial AND on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_and = n_tri = n_xor = 0
    n_cont = n_die = 0
    xor_j = xor_tri = 0
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
                ta = tri_and(*four)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        n_and += 1
                        xor_j ^= 1
                    if ta:
                        n_tri += 1
                        xor_tri ^= 1
                    if packed ^ ta:
                        n_xor += 1
                    if four == CONT and packed:
                        n_cont += 1
                    if four == DIE1111 and ta:
                        n_die += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_and": n_and,
        "n_tri": n_tri,
        "n_xor": n_xor,
        "n_cont": n_cont,
        "n_die": n_die,
        "xor_j": xor_j,
        "xor_tri": xor_tri,
    }


def tri_and_cover() -> dict:
    """Packed vs trinomial AND on covering k<=6; packed XOR matches HF/HG."""
    n_ok = n_g1 = n_and = n_tri = n_xor = n_cont = n_die = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    n_tri_ne_j = 0
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_tri(k, q)
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
            if w["xor_tri"] != w["xor_j"]:
                n_tri_ne_j += 1
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_and += w["n_and"]
            n_tri += w["n_tri"]
            n_xor += w["n_xor"]
            n_cont += w["n_cont"]
            n_die += w["n_die"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_and": w["n_and"],
                "n_tri": w["n_tri"],
                "n_xor": w["n_xor"],
                "xor_j": w["xor_j"],
                "xor_tri": w["xor_tri"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_and == 4522
        and n_tri == 4543
        and n_xor == 2313
        and n_cont == 1146
        and n_die == 1167
        and n_xor == n_cont + n_die
        and n_and == 3376 + n_cont
        and n_tri == 3376 + n_die
        and n_tri_ne_j > 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_and": n_and,
        "n_tri": n_tri,
        "n_xor": n_xor,
        "n_cont": n_cont,
        "n_die": n_die,
        "n_tri_ne_j": n_tri_ne_j,
        "rows": rows,
    }


def _kill_four(s_hit: int, n_hit: int, j_hit: int, p_hit: int):
    k, T = 1, 20
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p_hit - 3 + i) for i in range(4))
    return k, s_hit, n_hit, j_hit, p_hit, four


def killed_packed_eq_tri() -> dict:
    """Packed AND equals trinomial AND: G(3,1) is CONT 0011."""
    k, s, n, j, p, four = _kill_four(13, 3, 1, 18)
    ok = (
        G(n, j) == 1
        and four == CONT
        and and_clause(*four) == 1
        and tri_and(*four) == 0
        and four not in TRI_ONES
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


def killed_j_eq_tri() -> dict:
    """Covering J equals XOR of trinomial AND on G=1: same CONT witness."""
    k, s, n, j, p, four = _kill_four(13, 3, 1, 18)
    ok = (
        G(n, j) == 1
        and four == CONT
        and and_clause(*four) == 1
        and tri_and(*four) == 0
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


def killed_tri_vanishes() -> dict:
    """Trinomial AND vanishes on G=1: G(1,2) is 1111."""
    k, s, n, j, p, four = _kill_four(17, 1, 2, 16)
    ok = (
        G(n, j) == 1
        and four == DIE1111
        and tri_and(*four) == 1
        and and_clause(*four) == 0
        and four in TRI_ONES
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
    jz = json.loads(JZ_JSON.read_text())
    ok = (
        jz["checks"]["all_ok"]
        and jz["verdict"]["cob_commute_revsw"] == "LEMMA"
        and jz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert tri_bit(0, 0, 1, 1) == (0 ^ (1 | 1))
    assert CONT not in TRI_ONES
    assert DIE1111 in TRI_ONES
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = tri_table()
    sc = tri_and_cover()
    k0 = killed_packed_eq_tri()
    k1 = killed_j_eq_tri()
    k2 = killed_tri_vanishes()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "tri_table": {k: rt[k] for k in rt if k != "ok"},
        "tri_and_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_packed_eq_tri": {k: k0[k] for k in k0 if k != "ok"},
        "killed_j_eq_tri": {k: k1[k] for k in k1 if k != "ok"},
        "killed_tri_vanishes": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "rule30_eq_tri_xor_and": True,
            "tri_ones_fresh_1111": True,
            "covering_packed_ne_tri": True,
            "packed_eq_tri": False,
            "J_eq_tri": False,
            "tri_vanishes": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "rule30_eq_tri_xor_and": "LEMMA",
            "tri_ones_fresh_1111": "LEMMA",
            "covering_packed_ne_tri": "LEMMA",
            "packed_eq_tri": "KILLED",
            "J_eq_tri": "KILLED",
            "tri_vanishes": "KILLED",
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
    print("tri_table", dump["tri_table"])
    cov = dump["tri_and_cover"]
    print(
        "tri_and_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_and",
        cov["n_and"],
        "n_tri",
        cov["n_tri"],
        "n_xor",
        cov["n_xor"],
        "n_cont",
        cov["n_cont"],
        "n_die",
        cov["n_die"],
        "n_tri_ne_j",
        cov["n_tri_ne_j"],
    )
    print("killed_packed_eq_tri", dump["killed_packed_eq_tri"])
    print("killed_j_eq_tri", dump["killed_j_eq_tri"])
    print("killed_tri_vanishes", dump["killed_tri_vanishes"])


if __name__ == "__main__":
    main()
