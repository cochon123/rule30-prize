#!/usr/bin/env python3
"""Cycle ES: reconstruct is rotation-equivariant; 2-power n0 T0s partition
into rotation classes of size 2 n0 with one ident-0 extra per class.

Unique continuation u_{t+1}=a_t xor (b_t or u_t) is cyclic-shift
invariant, so reconstruct(rot^k a, rot^k b)=rot^k reconstruct(a,b) when
defined. Starting from (0, T0||not T0, 1), the all-0 and all-1 bits are
shift-invariant, so the first ident-0 extra and its even/odd kind are
constant on the rotation class of T=T0||not T0. For 2-power n0, T has
min period 2 n0 (any proper period would divide n0 and force T0[0]=not
T0[0]), so the classes have size 2 n0 and partition all 2^{n0} words:
n0=2 has 1 class (extra 22); n0=4 has FAM89 and FAM372; n0=8 has 16
classes of 16 (nine extras in 53000, seven none); n0=16 has 2048 classes
of 32, one of which is FAM414990. Kills: extras attach to isolated T0s;
n0=8 families of 16 are coincidental; T can have period <2 n0 for
2-power n0. Do not claim a formula for extra 414990; do not claim every
class eventually hits ident-0; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_es.py --certify
Dump: research/cycle_es.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_di import FAM372, FAM89, first_odd, mask_bits
from cycle_dm import N8_HITS, N8_NONE, PRIZE_EXTRA, PRIZE8
from cycle_dn import census
from cycle_ep import EXTRA414990, FAM414990, N_FAM
from cycle_er import T_STAR, U32, complement

OUT = Path(__file__).resolve().with_suffix(".json")
ER_JSON = Path(__file__).resolve().parent / "cycle_er.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
N8_NONE_REPS = (
    "00011000",
    "00100100",
    "00110100",
    "01010100",
    "01011000",
    "01101000",
    "01110000",
)


def rot(xs: list[int], k: int) -> list[int]:
    n = len(xs)
    k %= n
    return xs[k:] + xs[:k]


def rot_str(s: str, k: int) -> str:
    k %= len(s)
    return s[k:] + s[:k]


def min_period(s: str) -> int:
    n = len(s)
    for p in range(1, n + 1):
        if n % p == 0 and s == s[:p] * (n // p):
            return p
    return n


def bits(mask: int, n: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(n))


def otype(T0: str) -> str:
    return T0 + complement(T0)


def class_of(T0: str) -> frozenset[str]:
    T = otype(T0)
    n0 = len(T0)
    return frozenset(rot_str(T, k)[:n0] for k in range(len(T)))


def reconstruct_rot_equiv() -> dict:
    """reconstruct commutes with cyclic shift; exhaustive L=4,8 plus trials."""
    for L in (4, 8):
        for a_m in range(1 << L):
            a = [(a_m >> t) & 1 for t in range(L)]
            for b_m in range(1 << L):
                b = [(b_m >> t) & 1 for t in range(L)]
                u = reconstruct(a, b)
                for k in (1, L // 2):
                    ur = reconstruct(rot(a, k), rot(b, k))
                    if u is None:
                        if ur is not None:
                            return {"ok": False, "L": L}
                    elif ur != rot(u, k):
                        return {"ok": False, "L": L, "k": k}
    rng = random.Random(11)
    for L in (16, 32):
        for _ in range(60):
            a = [rng.randint(0, 1) for _ in range(L)]
            b = [rng.randint(0, 1) for _ in range(L)]
            u = reconstruct(a, b)
            k = 1 + rng.randrange(L - 1)
            ur = reconstruct(rot(a, k), rot(b, k))
            if u is None:
                if ur is not None:
                    return {"ok": False, "L": L, "trial": True}
            elif ur != rot(u, k):
                return {"ok": False, "L": L, "k": k, "trial": True}
    return {"ok": True, "exhaustive_L": [4, 8], "trials_L": [16, 32]}


def min_period_pow2() -> dict:
    """For 2-power n0, T=T0||not T0 has min period 2 n0 for every T0."""
    rows: dict[int, dict] = {}
    for n0 in (2, 4, 8, 16):
        L = 2 * n0
        bad = 0
        for mask in range(1 << n0):
            T = otype(bits(mask, n0))
            if min_period(T) != L:
                bad += 1
        n_class = (1 << n0) // L
        rows[n0] = {
            "L": L,
            "n_words": 1 << n0,
            "n_class": n_class,
            "class_size": L,
            "n_bad": bad,
        }
        if bad or n_class * L != (1 << n0):
            return {"ok": False, "n0": n0, "rows": rows}
    ok = (
        rows[2]["n_class"] == 1
        and rows[4]["n_class"] == 2
        and rows[8]["n_class"] == 16
        and rows[16]["n_class"] == 2048
    )
    return {"ok": ok, "rows": {str(k): v for k, v in rows.items()}}


def n2_one_class() -> dict:
    extras = []
    for mask in range(4):
        cur, _ = first_odd(mask_bits(mask, 2), 40)
        extras.append(cur)
        if class_of(bits(mask, 2)) != frozenset(bits(m, 2) for m in range(4)):
            return {"ok": False, "mask": mask}
    ok = extras == [22, 22, 22, 22]
    return {"ok": ok, "extra": 22, "n_class": 1}


def n4_two_classes() -> dict:
    all4 = {bits(m, 4) for m in range(16)}
    ok = (
        len(FAM89) == 8
        and len(FAM372) == 8
        and FAM89 | FAM372 == all4
        and not (FAM89 & FAM372)
        and class_of("0000") == FAM89
        and class_of("0010") == FAM372
        and min_period(otype("0000")) == 8
        and min_period(otype("0010")) == 8
    )
    return {"ok": ok, "n_class": 2}


def n8_sixteen_classes() -> dict:
    got = census(8, 53000)
    by: dict[tuple[int, int], list[str]] = defaultdict(list)
    for mask, (cur, sm) in got["first"].items():
        by[(cur, sm)].append(bits(mask, 8))
    rows: dict[str, dict] = {}
    for (cur, sm), words in sorted(by.items()):
        words_s = sorted(words)
        cls = sorted(class_of(words_s[0]))
        full = words_s == cls and len(words_s) == 16
        rows[str(cur)] = {"odd": sm, "n": len(words_s), "full16": full, "rep": words_s[0]}
        if not full:
            return {"ok": False, "extra": cur}
    none = [bits(m, 8) for m in range(256) if m not in got["first"]]
    seen: set[str] = set()
    none_reps: list[str] = []
    for s in sorted(none):
        if s in seen:
            continue
        cls = class_of(s)
        if len(cls) != 16 or not cls <= set(none):
            return {"ok": False, "none": s}
        none_reps.append(s)
        seen.update(cls)
    hits_ok = {
        int(k): (v["odd"], v["n"]) for k, v in rows.items()
    } == dict(N8_HITS)
    ok = (
        got["n_hit"] == 144
        and got["n_none"] == N8_NONE == 112
        and len(rows) == 9
        and all(v["full16"] for v in rows.values())
        and hits_ok
        and len(none_reps) == 7
        and tuple(none_reps) == N8_NONE_REPS
        and class_of(PRIZE8) == class_of("00000110")
        and rows[str(PRIZE_EXTRA)]["odd"] == 0
        and rows[str(PRIZE_EXTRA)]["n"] == 16
    )
    return {
        "ok": ok,
        "hits": {k: {"odd": v["odd"], "n": v["n"], "rep": v["rep"]} for k, v in rows.items()},
        "n_none_classes": len(none_reps),
        "none_reps": none_reps,
        "prize_extra": PRIZE_EXTRA,
    }


def n16_classes() -> dict:
    cls = class_of(T_STAR)
    ok = (
        cls == FAM414990
        and len(cls) == N_FAM == 32
        and U32 == otype(T_STAR)
        and min_period(U32) == 32
        and (1 << 16) // 32 == 2048
        and EXTRA414990 == 414990
    )
    return {"ok": ok, "n_class": 2048, "class_size": 32, "fam414990": True}


def prefixes() -> dict:
    er = json.loads(ER_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    ok = (
        er["checks"]["all_ok"]
        and er["verdict"]["fam414990_16_prefixes_of_rots_U"] == "LEMMA"
        and er["T_star"] == T_STAR
        and dm["checks"]["all_ok"]
        and dm["n8"]["n_none"] == 112
    )
    return {"ok": ok}


def self_checks(
    c20, eqv: dict, per: dict, n2: dict, n4: dict, n8: dict, n16: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert eqv["ok"] and per["ok"] and n2["ok"] and n4["ok"]
    assert n8["ok"] and n16["ok"] and pref["ok"]
    assert per["rows"]["16"]["n_class"] == 2048
    assert n8["prize_extra"] == 52809
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    eqv = reconstruct_rot_equiv()
    per = min_period_pow2()
    n2 = n2_one_class()
    n4 = n4_two_classes()
    n8 = n8_sixteen_classes()
    n16 = n16_classes()
    pref = prefixes()
    checks = self_checks(c20, eqv, per, n2, n4, n8, n16, pref)
    dump = {
        "cycle": "ES",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "period": per["rows"],
        "n2": {"extra": 22, "n_class": 1},
        "n4": {"n_class": 2, "extras": {"89": 8, "372": 8}},
        "n8": {
            "n_class": 16,
            "n_hit_classes": 9,
            "n_none_classes": n8["n_none_classes"],
            "hits": n8["hits"],
            "none_reps": n8["none_reps"],
            "prize_extra": 52809,
        },
        "n16": {"n_class": 2048, "class_size": 32, "fam414990_extra": EXTRA414990},
        "lemmas": {
            "reconstruct_rotation_equivariant": True,
            "ident0_extra_constant_on_rot_class": True,
            "pow2_n0_T_min_period_2n0": True,
            "n2_one_class_extra_22": True,
            "n4_two_classes_89_372": True,
            "n8_sixteen_classes_nine_hit": True,
            "n16_2048_classes_FAM414990_one": True,
            "extras_attach_to_isolated_T0": False,
            "n8_families_of_16_coincidental": False,
            "T_period_lt_2n0_for_pow2_n0": False,
            "extra_414990_formula": None,
            "every_class_eventually_hits": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reconstruct_rotation_equivariant": "LEMMA",
            "ident0_extra_constant_on_rot_class": "LEMMA",
            "pow2_n0_T_min_period_2n0": "LEMMA",
            "n2_one_class_extra_22": "LEMMA",
            "n4_two_classes_89_372": "LEMMA",
            "n8_sixteen_classes_nine_hit": "LEMMA",
            "n16_2048_classes_FAM414990_one": "LEMMA",
            "extras_attach_to_isolated_T0": "KILLED",
            "n8_families_of_16_coincidental": "KILLED",
            "T_period_lt_2n0_for_pow2_n0": "KILLED",
            "extra_414990_formula": "PREFIX",
            "every_class_eventually_hits": "PREFIX",
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
    print("n8_none_reps", dump["n8"]["none_reps"])
    print("n16_n_class", dump["n16"]["n_class"])


if __name__ == "__main__":
    main()
