#!/usr/bin/env python3
"""Cycle KC: dual of G=1 extra terms takes all 16 packed 4-tuples.

DIE 1111 and CONT 0011 are the packed-vs-trinomial AND extras.
Covering dual 4-tuples of each hit every 16-row. Dual of 1111 is
not 1111; dual of CONT is not bit-reverse; dual AND xor does not
vanish. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not
a prize claim.

Run: python3 research/cycle_kc.py --certify
Dump: research/cycle_kc.json
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
from cycle_hi import CONT
from cycle_hu import and_clause
from cycle_hx import reverse_four
from cycle_ka import DIE1111
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KB_JSON = Path(__file__).resolve().parent / "cycle_kb.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

CONT_REV = (1, 1, 0, 0)


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def extra_rev_table() -> dict:
    """16-row: reverse of 1111 is 1111; reverse of CONT is cob 1100."""
    n_ok = 0
    for bits in range(16):
        four = tuple((bits >> i) & 1 for i in range(3, -1, -1))
        n_ok += 1
        if reverse_four(*four) != four[::-1]:
            return {"ok": False, "rev": True, "four": list(four)}
    ok = (
        n_ok == 16
        and reverse_four(*DIE1111) == DIE1111
        and reverse_four(*CONT) == CONT_REV
        and and_clause(*DIE1111) == 0
        and and_clause(*CONT) == 1
        and and_clause(*CONT_REV) == 0
    )
    return {"ok": ok, "n_ok": n_ok}


def _walk_dual(k: int, q: int) -> dict:
    """Dual 4-tuple census of G=1 1111 and CONT; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_die = n_cont = 0
    n_die_pair = n_cont_pair = 0
    n_ctr_die = n_ctr_cont = 0
    n_die_self = n_die_to_cont = n_die_andxor = 0
    n_cont_self = n_cont_rev = n_cont_to_die = n_cont_andxor = 0
    types_die = {f"{i:04b}": 0 for i in range(16)}
    types_cont = {f"{i:04b}": 0 for i in range(16)}
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
                bits[j] = (four, packed, p)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j, (four, packed, p) in bits.items():
                if G(n, j) == 0:
                    continue
                extra = four == DIE1111 or four == CONT
                if not extra:
                    continue
                if four == DIE1111:
                    n_die += 1
                else:
                    n_cont += 1
                if j == n:
                    if four == DIE1111:
                        n_ctr_die += 1
                    else:
                        n_ctr_cont += 1
                    continue
                j2 = 2 * n - j
                if j2 not in bits:
                    continue
                four2, packed2, p2 = bits[j2]
                key = _fmt(four2)
                if four == DIE1111:
                    n_die_pair += 1
                    types_die[key] += 1
                    if four2 == DIE1111:
                        n_die_self += 1
                    if four2 == CONT:
                        n_die_to_cont += 1
                    if packed ^ packed2:
                        n_die_andxor += 1
                else:
                    n_cont_pair += 1
                    types_cont[key] += 1
                    if four2 == CONT:
                        n_cont_self += 1
                    if four2 == reverse_four(*CONT):
                        n_cont_rev += 1
                    if four2 == DIE1111:
                        n_cont_to_die += 1
                    if packed ^ packed2:
                        n_cont_andxor += 1
        row = rule30_step(row)
        s += 1
    n_die_types = sum(1 for v in types_die.values() if v)
    n_cont_types = sum(1 for v in types_cont.values() if v)
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_die": n_die,
        "n_cont": n_cont,
        "n_die_pair": n_die_pair,
        "n_cont_pair": n_cont_pair,
        "n_ctr_die": n_ctr_die,
        "n_ctr_cont": n_ctr_cont,
        "n_die_self": n_die_self,
        "n_die_to_cont": n_die_to_cont,
        "n_die_andxor": n_die_andxor,
        "n_cont_self": n_cont_self,
        "n_cont_rev": n_cont_rev,
        "n_cont_to_die": n_cont_to_die,
        "n_cont_andxor": n_cont_andxor,
        "n_die_types": n_die_types,
        "n_cont_types": n_cont_types,
        "types_die": types_die,
        "types_cont": types_cont,
        "xor_j": xor_j,
    }


def dual_extra_cover() -> dict:
    """Dual extra-term census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_die = n_cont = 0
    n_die_pair = n_cont_pair = 0
    n_ctr_die = n_ctr_cont = 0
    n_die_self = n_die_to_cont = n_die_andxor = 0
    n_cont_self = n_cont_rev = n_cont_to_die = n_cont_andxor = 0
    types_die = {f"{i:04b}": 0 for i in range(16)}
    types_cont = {f"{i:04b}": 0 for i in range(16)}
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
            n_die += w["n_die"]
            n_cont += w["n_cont"]
            n_die_pair += w["n_die_pair"]
            n_cont_pair += w["n_cont_pair"]
            n_ctr_die += w["n_ctr_die"]
            n_ctr_cont += w["n_ctr_cont"]
            n_die_self += w["n_die_self"]
            n_die_to_cont += w["n_die_to_cont"]
            n_die_andxor += w["n_die_andxor"]
            n_cont_self += w["n_cont_self"]
            n_cont_rev += w["n_cont_rev"]
            n_cont_to_die += w["n_cont_to_die"]
            n_cont_andxor += w["n_cont_andxor"]
            for key in types_die:
                types_die[key] += w["types_die"][key]
                types_cont[key] += w["types_cont"][key]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_die": w["n_die"],
                "n_cont": w["n_cont"],
                "n_die_pair": w["n_die_pair"],
                "n_cont_pair": w["n_cont_pair"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    n_die_types = sum(1 for v in types_die.values() if v)
    n_cont_types = sum(1 for v in types_cont.values() if v)
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_die == 1167
        and n_cont == 1146
        and n_ctr_die == 30
        and n_ctr_cont == 53
        and n_die_pair == 1137
        and n_cont_pair == 1093
        and n_die_pair == n_die - n_ctr_die
        and n_cont_pair == n_cont - n_ctr_cont
        and n_die_types == 16
        and n_cont_types == 16
        and n_die_andxor == 294
        and n_cont_andxor == 831
        and all(types_die[key] > 0 for key in types_die)
        and all(types_cont[key] > 0 for key in types_cont)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_die": n_die,
        "n_cont": n_cont,
        "n_die_pair": n_die_pair,
        "n_cont_pair": n_cont_pair,
        "n_ctr_die": n_ctr_die,
        "n_ctr_cont": n_ctr_cont,
        "n_die_self": n_die_self,
        "n_die_to_cont": n_die_to_cont,
        "n_die_andxor": n_die_andxor,
        "n_cont_self": n_cont_self,
        "n_cont_rev": n_cont_rev,
        "n_cont_to_die": n_cont_to_die,
        "n_cont_andxor": n_cont_andxor,
        "n_die_types": n_die_types,
        "n_cont_types": n_cont_types,
        "types_die": types_die,
        "types_cont": types_cont,
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


def killed_die_self() -> dict:
    """Dual of G=1 1111 is 1111: G(4,0) dual is 1010."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(2, 31, 4, 0, 40, 24)
    ok = (
        G(n, j) == 1
        and G(n, j2) == 1
        and four == DIE1111
        and four2 == (1, 0, 1, 0)
        and four2 != DIE1111
        and four2 != reverse_four(*four)
        and four2 != CONT
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


def killed_cont_rev() -> dict:
    """Dual of G=1 CONT is bit-reverse: G(3,1) dual is 0111, not 1100."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(1, 13, 3, 1, 18, 10)
    ok = (
        G(n, j) == 1
        and G(n, j2) == 1
        and four == CONT
        and four2 == (0, 1, 1, 1)
        and four2 != reverse_four(*CONT)
        and four2 != DIE1111
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
        "rev": list(reverse_four(*CONT)),
    }


def killed_die_andxor0() -> dict:
    """Dual AND xor of G=1 1111 vanishes: G(23,13) dual is CONT 0011."""
    k, s, n, j, j2, p, p2, four, four2 = _kill_pair(4, 49, 23, 13, 70, 30)
    ok = (
        G(n, j) == 1
        and G(n, j2) == 1
        and four == DIE1111
        and four2 == CONT
        and and_clause(*four) == 0
        and and_clause(*four2) == 1
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
    kb = json.loads(KB_JSON.read_text())
    ok = (
        kb["checks"]["all_ok"]
        and kb["verdict"]["die_g1_all_shapes"] == "LEMMA"
        and kb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert DIE1111 == (1, 1, 1, 1)
    assert CONT == (0, 0, 1, 1)
    assert reverse_four(*CONT) == CONT_REV
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = extra_rev_table()
    sc = dual_extra_cover()
    k0 = killed_die_self()
    k1 = killed_cont_rev()
    k2 = killed_die_andxor0()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "extra_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "dual_extra_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_die_self": {k: k0[k] for k in k0 if k != "ok"},
        "killed_cont_rev": {k: k1[k] for k in k1 if k != "ok"},
        "killed_die_andxor0": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "extra_reverse": True,
            "die_dual_all_16": True,
            "cont_dual_all_16": True,
            "covering_dual_extra": True,
            "die_self": False,
            "cont_rev": False,
            "die_andxor0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "extra_reverse": "LEMMA",
            "die_dual_all_16": "LEMMA",
            "cont_dual_all_16": "LEMMA",
            "covering_dual_extra": "LEMMA",
            "die_self": "KILLED",
            "cont_rev": "KILLED",
            "die_andxor0": "KILLED",
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
    print("extra_rev_table", dump["extra_rev_table"])
    cov = dump["dual_extra_cover"]
    print(
        "dual_extra_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_die",
        cov["n_die"],
        "n_cont",
        cov["n_cont"],
        "n_die_pair",
        cov["n_die_pair"],
        "n_cont_pair",
        cov["n_cont_pair"],
        "n_die_types",
        cov["n_die_types"],
        "n_cont_types",
        cov["n_cont_types"],
        "n_die_andxor",
        cov["n_die_andxor"],
        "n_cont_andxor",
        cov["n_cont_andxor"],
    )
    print("killed_die_self", dump["killed_die_self"])
    print("killed_cont_rev", dump["killed_cont_rev"])
    print("killed_die_andxor0", dump["killed_die_andxor0"])


if __name__ == "__main__":
    main()
