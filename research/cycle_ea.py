#!/usr/bin/env python3
"""Cycle EA: n7!=n8 for even n0 O-type; 10-bit post-odd ident-0 gap.

n3=n4=1 forces n5=1 (n3=1 => s_prev=n3_prev=0, hence n4_prev=1 and
n5=1). Empty pairs cannot follow empty pairs. n7=n8 iff n5=n6 and n7;
on an empty pair the 16 allowed triples preserve that iff both sides
are (n5,n6,n7)=(0,0,1), which needs both n6=0. That empty n6_00 can
only come from agree1 with zero-side n5=n6=0. Pair invariants on the
predecessor then force the one-side to (n4,n5,n6)=(0,1,1), so
n4!=n5|n6 and next n6 cannot both vanish. Hence n7!=n8, and after an
odd doubling there is no ident-0 at p+1,...,p+10. Do not claim an
11-bit gap. Do not compute phi^{(3,5,9)} at k=16. Not a prize claim:
a 10-bit gap does not fill an annulus.

Run: python3 research/cycle_ea.py --certify
Dump: research/cycle_ea.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct
from cycle_cb import ext, twocopy_type
from cycle_ch import scar_lift, shifted_not
from cycle_df import unfold
from cycle_dv import EXPECTED_P, mask_bits, odd_copy
from cycle_dy import rec_n3, rec_n4, rec_n5, tail
from cycle_dz import rec_n6

OUT = Path(__file__).resolve().with_suffix(".json")
DZ_JSON = Path(__file__).resolve().parent / "cycle_dz.json"
ALLOWED = ((0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 1))


def rec_n7(n5: int, n6: int, n7: int) -> int:
    return n5 ^ (n6 | n7)


def ov_implies_n5_one() -> dict:
    """n3=n4=1 implies n5=1, via s_prev=n3_prev=0 and n4_prev=1."""
    if rec_n5(0, 1, 0) != 1 or rec_n5(0, 1, 1) != 1:
        return {"ok": False, "local": True}
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ov = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 3)
            if out is None:
                return {"ok": False, "n0": n0}
            n3, n4, n5 = out[1], out[2], out[3]
            L = 2 * n0
            for t in range(L):
                if n3[t] == 1 and n4[t] == 1:
                    n_ov += 1
                    if n5[t] != 1:
                        return {"ok": False, "n0": n0, "t": t}
                    prev = (t - 1) % L
                    if s[prev] != 0 or n3[prev] != 0 or n4[prev] != 1:
                        return {"ok": False, "n0": n0, "prev": prev}
        rows[n0] = n_ov
    return {"ok": True, "rows": rows}


def empty_not_follow_empty() -> bool:
    """NOR(s,0)=0 and NOR(not s,0)=0 cannot both hold."""
    for s in (0, 1):
        if rec_n3(s, 0) == 0 and rec_n3(s ^ 1, 0) == 0:
            return False
    return True


def n78_only_both_001() -> dict:
    """Empty-pair triples preserve n5=n6 and n7 iff both sides are 001."""
    hold = 0
    hold_keys = []
    for a in ALLOWED:
        for b in ALLOWED:
            na = (
                rec_n3(1, 0),
                rec_n4(1, 0, 1),
                rec_n5(0, 1, a[0]),
                rec_n6(1, a[0], a[1]),
                rec_n7(a[0], a[1], a[2]),
            )
            nb = (
                rec_n3(0, 0),
                rec_n4(0, 0, 1),
                rec_n5(0, 1, b[0]),
                rec_n6(1, b[0], b[1]),
                rec_n7(b[0], b[1], b[2]),
            )
            oka = na[2] == (na[3] & na[4])
            okb = nb[2] == (nb[3] & nb[4])
            if oka and okb:
                hold += 1
                hold_keys.append((a, b))
    ok = hold == 1 and hold_keys == [((0, 0, 1), (0, 0, 1))]
    return {"ok": ok, "hold": hold, "keys": hold_keys}


def critical_agree1_is_011() -> dict:
    """n3=1, n3p=0, n5p=n6p=0 implies (n4,n5,n6)=(0,1,1)."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_hit = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 4)
            if out is None:
                return {"ok": False, "n0": n0}
            n3, n4, n5, n6 = out[1], out[2], out[3], out[4]
            L = 2 * n0
            for t in range(L):
                tp = (t + n0) % L
                if n3[t] == 1 and n3[tp] == 0 and n5[tp] == 0 and n6[tp] == 0:
                    n_hit += 1
                    if (n4[t], n5[t], n6[t], n4[tp]) != (0, 1, 1, 0):
                        return {"ok": False, "n0": n0, "t": t}
        rows[n0] = n_hit
    return {"ok": True, "rows": rows}


def empty_n6_or() -> dict:
    """Empty pairs have n6_t or n6_{t+n0} = 1."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_empty = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 4)
            if out is None:
                return {"ok": False, "n0": n0}
            n3, n6 = out[1], out[4]
            for t in range(n0):
                if n3[t] == 0 and n3[t + n0] == 0:
                    n_empty += 1
                    if n6[t] == 0 and n6[t + n0] == 0:
                        return {"ok": False, "n0": n0, "t": t}
        rows[n0] = n_empty
    return {"ok": True, "rows": rows}


def n7_ne_n8_even() -> dict:
    """n7!=n8 on every even-n0 O-type through n0=12, 40 random n0=16."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ok = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 6)
            if out is None or out[5] == out[6]:
                return {"ok": False, "n0": n0}
            n_ok += 1
        rows[n0] = n_ok
    rng = random.Random(31)
    n16 = 0
    for _ in range(40):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        out = tail(s, 6)
        if out is None or out[5] == out[6]:
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = n16
    return {"ok": True, "rows": rows}


def gap10_scar() -> dict:
    """scar_lift through seqs[10] succeeds for every even-n0 T0<=8."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8):
        n_ok = 0
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            seqs = scar_lift(t0, 8)
            if seqs is None or set(seqs) != set(range(11)):
                return {"ok": False, "n0": n0, "mask": mask}
            for i in range(1, 11):
                if not any(seqs[i]):
                    return {"ok": False, "n0": n0, "zero": i}
            n_ok += 1
        rows[n0] = n_ok
    return {"ok": True, "rows": rows}


def prize_gap10() -> dict:
    """Prize k=4,8,16: n7!=n8, no ident-0 in p+1..p+10."""
    rows: dict[int, dict] = {}
    for k, p_odd in EXPECTED_P.items():
        pi, cyc = prize_cycle(k)
        w = 1 << k
        seqs = {p: [(word >> p) & 1 for word in cyc] for p in range(w + 1)}
        cur_pi = pi
        found = None
        p = w + 1
        while p <= 2 * w:
            a = ext(seqs[p - 2], cur_pi)
            b = ext(seqs[p - 1], cur_pi)
            if all(x == 0 for x in b):
                u = unfold(a)
                if sum(a) % 2 == 1:
                    found = p
                    seqs[p] = u + [x ^ 1 for x in u]
                    cur_pi *= 2
                    break
                seqs[p] = u
            else:
                seqs[p] = reconstruct(a, b)
            p += 1
        if found != p_odd:
            return {"ok": False, "k": k, "p": found}
        for q in range(found + 1, found + 11):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        o = ext(seqs[found], cur_pi)
        s = ext(seqs[found + 2], cur_pi)
        n7 = ext(seqs[found + 7], cur_pi)
        n8 = ext(seqs[found + 8], cur_pi)
        n0 = cur_pi // 2
        if (
            twocopy_type(o) != "O"
            or s != shifted_not(o)
            or n7 == n8
            or n0 != pi
        ):
            return {"ok": False, "k": k}
        rows[k] = {"p": found, "pi": pi, "gap10": True}
    return {"ok": True, "rows": rows}


def n8_ne_n9_prefix() -> dict:
    """n8!=n9 through even n0=10 (not claimed for all n0)."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10):
        n_ok = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 7)
            if out is None or out[6] == out[7]:
                return {"ok": False, "n0": n0}
            n_ok += 1
        rows[n0] = n_ok
    return {"ok": True, "rows": rows}


def dz_prefix() -> dict:
    dz = json.loads(DZ_JSON.read_text())
    ok = (
        dz["checks"]["all_ok"]
        and dz["lemmas"]["n5_type_N_even_n0"]
        and dz["lemmas"]["n6_ne_n7_even_n0"]
        and dz["lemmas"]["post_odd_9bit_gap_even_n0"]
        and dz["prize_gap9"]["16"]["n5"] == "N"
        and dz["verdict"]["n5_type_N_even_n0"] == "LEMMA"
    )
    return {"ok": ok, "prize": dz["prize_gap9"]}


def self_checks(
    c20,
    ov: dict,
    noemp: bool,
    only: dict,
    crit: dict,
    n6or: dict,
    n78: dict,
    gap: dict,
    prize: dict,
    pref89: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ov["ok"] and noemp and only["ok"] and crit["ok"]
    assert n6or["ok"] and n78["ok"] and gap["ok"] and prize["ok"]
    assert pref89["ok"] and pref["ok"]
    assert only["hold"] == 1
    assert n78["rows"][8] == 256
    assert gap["rows"][8] == 256
    assert prize["rows"][4]["gap10"] and prize["rows"][16]["gap10"]
    assert n6or["rows"][2] == 4
    assert pref89["rows"][10] == 1024
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ov = ov_implies_n5_one()
    noemp = empty_not_follow_empty()
    only = n78_only_both_001()
    crit = critical_agree1_is_011()
    n6or = empty_n6_or()
    n78 = n7_ne_n8_even()
    gap = gap10_scar()
    prize = prize_gap10()
    pref89 = n8_ne_n9_prefix()
    pref = dz_prefix()
    checks = self_checks(
        c20, ov, noemp, only, crit, n6or, n78, gap, prize, pref89, pref
    )
    dump = {
        "cycle": "EA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "ov_n5": ov["rows"],
        "n78_hold": only,
        "critical_agree1": crit["rows"],
        "empty_n6_or": n6or["rows"],
        "n7_ne_n8": n78["rows"],
        "gap10_scar": gap["rows"],
        "prize_gap10": prize["rows"],
        "n8_ne_n9_prefix": pref89["rows"],
        "lemmas": {
            "ov_implies_n5_one": True,
            "empty_not_follow_empty": True,
            "n7_eq_n8_only_both_001": True,
            "empty_n6_or": True,
            "n7_ne_n8_even_n0": True,
            "post_odd_10bit_gap_even_n0": True,
            "post_odd_11bit_gap_all_n0": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "ov_implies_n5_one": "LEMMA",
            "empty_not_follow_empty": "LEMMA",
            "n7_eq_n8_only_both_001": "LEMMA",
            "empty_n6_or": "LEMMA",
            "n7_ne_n8_even_n0": "LEMMA",
            "post_odd_10bit_gap_even_n0": "LEMMA",
            "post_odd_11bit_gap_all_n0": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("prize_gap10", dump["prize_gap10"])


if __name__ == "__main__":
    main()
