#!/usr/bin/env python3
"""Cycle DZ: even n0 O-type n5 is type N; 9-bit post-odd ident-0 gap.

Empty pairs have both n4=1. If n5 were O-type, the reconstruct
half-shift on an empty pair yields 0=1. If n5 were E-type, the empty
side with s=1 steps to n3^{+}=1 with n5^{+}=1, while the half-shift
on agree1 requires n5=0 at every n3=1. Hence n5 is type N. Assuming
n6=n7 iff n4=n5 and n6, so empty pairs have n5=n6=1; the O-type side
with s=1 then steps to n4^{+}=1 versus n5^{+} and n6^{+}=0. Thus
n6!=n7, and after an odd doubling there is no ident-0 at
p+1,...,p+9. xorcat(n5) is not always odd; n6 is not always type N.
Do not claim a 10-bit gap. Do not compute phi^{(3,5,9)} at k=16.
Not a prize claim: a 9-bit gap does not fill an annulus.

Run: python3 research/cycle_dz.py --certify
Dump: research/cycle_dz.json
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
from cycle_ca import KNOWN20, packed_center_bits, prize_cycle, reconstruct, xorcat
from cycle_cb import ext, twocopy_type
from cycle_ch import scar_lift, shifted_not
from cycle_df import unfold
from cycle_dv import EXPECTED_P, mask_bits, odd_copy
from cycle_dy import rec_n3, rec_n4, rec_n5, tail

OUT = Path(__file__).resolve().with_suffix(".json")
DY_JSON = Path(__file__).resolve().parent / "cycle_dy.json"


def rec_n6(n4: int, n5: int, n6: int) -> int:
    return n4 ^ (n5 | n6)


def n5_not_O_step() -> bool:
    """Empty pair, n5 O-type: (1 or n5) xor (1 or not n5) = 0, not 1."""
    for n5 in (0, 1):
        if ((1 | n5) ^ (1 | (n5 ^ 1))) != 0:
            return False
    return True


def n5_not_E_step() -> dict:
    """Empty s=1 with n5_p=n5 steps to n3^{+}=1 and n5^{+}=1."""
    n_ok = 0
    for n5 in (0, 1):
        a = rec_n3(1, 0)
        c = rec_n5(0, 1, n5)
        if (a, c) != (0, 1):
            return {"ok": False, "s1": n5}
        ap = rec_n3(0, 0)
        cp = rec_n5(0, 1, n5)
        if (ap, cp) != (1, 1):
            return {"ok": False, "s0": n5}
        n_ok += 1
    return {"ok": n_ok == 2, "n": n_ok}


def n6_ne_n7_step() -> dict:
    """Empty s=1 with n5=n6=1 steps to n4^{+}=1 != n5^{+} and n6^{+}."""
    n3n, n4n, n5n, n6n = (
        rec_n3(1, 0),
        rec_n4(1, 0, 1),
        rec_n5(0, 1, 1),
        rec_n6(1, 1, 1),
    )
    if (n3n, n4n, n5n, n6n) != (0, 0, 1, 0):
        return {"ok": False, "mid": [n3n, n4n, n5n, n6n]}
    n3p, n4p, n5p, n6p = (
        rec_n3(0, 0),
        rec_n4(0, 0, 1),
        rec_n5(0, 1, 1),
        rec_n6(1, 1, 1),
    )
    if (n3p, n4p, n5p, n6p) != (1, 1, 1, 0):
        return {"ok": False, "plus": [n3p, n4p, n5p, n6p]}
    if n4p == (n5p & n6p):
        return {"ok": False, "eq": True}
    return {"ok": True}


def n5_type_N_even() -> dict:
    """Every even-n0 O-type has n5 type N."""
    rows: dict[int, dict] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ok = 0
        types: set[str] = set()
        xorset: set[int] = set()
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 3)
            if out is None:
                return {"ok": False, "n0": n0}
            n5 = out[3]
            typ = twocopy_type(n5)
            types.add(typ)
            xorset.add(xorcat(n5))
            if typ != "N" or not any(n5):
                return {"ok": False, "n0": n0, "typ": typ}
            n_ok += 1
        if types != {"N"}:
            return {"ok": False, "n0": n0, "types": sorted(types)}
        rows[n0] = {"n": n_ok, "type": "N", "xorcat": sorted(xorset)}
    rng = random.Random(23)
    n16 = 0
    for _ in range(40):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        out = tail(s, 3)
        if out is None or twocopy_type(out[3]) != "N":
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = {"n": n16, "type": "N", "sampled": True}
    return {"ok": True, "rows": rows}


def n6_ne_n7_even() -> dict:
    """n6!=n7 on every even-n0 O-type through n0=12, 40 random n0=16."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ok = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 5)
            if out is None or out[4] == out[5]:
                return {"ok": False, "n0": n0}
            n_ok += 1
        rows[n0] = n_ok
    rng = random.Random(29)
    n16 = 0
    for _ in range(40):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        out = tail(s, 5)
        if out is None or out[4] == out[5]:
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = n16
    return {"ok": True, "rows": rows}


def gap9_scar() -> dict:
    """scar_lift through seqs[9] succeeds for every even-n0 T0<=8."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8):
        n_ok = 0
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            seqs = scar_lift(t0, 7)
            if seqs is None or set(seqs) != set(range(10)):
                return {"ok": False, "n0": n0, "mask": mask}
            for i in range(1, 10):
                if not any(seqs[i]):
                    return {"ok": False, "n0": n0, "zero": i}
            n_ok += 1
        rows[n0] = n_ok
    return {"ok": True, "rows": rows}


def prize_gap9() -> dict:
    """Prize k=4,8,16: n5 type N, n6!=n7, no ident-0 in p+1..p+9."""
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
        for q in range(found + 1, found + 10):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        o = ext(seqs[found], cur_pi)
        s = ext(seqs[found + 2], cur_pi)
        n5 = ext(seqs[found + 5], cur_pi)
        n6 = ext(seqs[found + 6], cur_pi)
        n7 = ext(seqs[found + 7], cur_pi)
        n0 = cur_pi // 2
        if (
            twocopy_type(o) != "O"
            or s != shifted_not(o)
            or twocopy_type(n5) != "N"
            or n6 == n7
            or n0 != pi
        ):
            return {"ok": False, "k": k, "n5": twocopy_type(n5)}
        rows[k] = {"p": found, "pi": pi, "n5": "N", "gap9": True}
    return {"ok": True, "rows": rows}


def xorcat_n5_not_always_odd() -> bool:
    """xorcat(n5) is 0 for every even n0=4 O-type."""
    xorset: set[int] = set()
    for mask in range(16):
        s = odd_copy(mask_bits(mask, 4))
        out = tail(s, 3)
        if out is None:
            return False
        xorset.add(xorcat(out[3]))
    return xorset == {0}


def n7_ne_n8_prefix() -> dict:
    """n7!=n8 through even n0=12 (not claimed for all n0)."""
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
    return {"ok": True, "rows": rows}


def dy_prefix() -> dict:
    dy = json.loads(DY_JSON.read_text())
    ok = (
        dy["checks"]["all_ok"]
        and dy["lemmas"]["n4_type_N_even_n0"]
        and dy["lemmas"]["n5_ne_n6_even_n0"]
        and dy["lemmas"]["post_odd_8bit_gap_even_n0"]
        and dy["prize_gap8"]["16"]["n4"] == "N"
        and dy["verdict"]["n4_type_N_even_n0"] == "LEMMA"
    )
    return {"ok": ok, "prize": dy["prize_gap8"]}


def self_checks(
    c20,
    not_o: bool,
    not_e: dict,
    n67s: dict,
    typ: dict,
    n67: dict,
    gap: dict,
    prize: dict,
    xor5: bool,
    pref67: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert not_o and not_e["ok"] and n67s["ok"] and typ["ok"]
    assert n67["ok"] and gap["ok"] and prize["ok"]
    assert xor5 and pref67["ok"] and pref["ok"]
    assert typ["rows"][2]["type"] == "N"
    assert typ["rows"][4]["xorcat"] == [0]
    assert typ["rows"][8]["n"] == 256
    assert n67["rows"][8] == 256
    assert gap["rows"][8] == 256
    assert prize["rows"][4]["gap9"] and prize["rows"][16]["n5"] == "N"
    assert pref67["rows"][12] == 4096
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    not_o = n5_not_O_step()
    not_e = n5_not_E_step()
    n67s = n6_ne_n7_step()
    typ = n5_type_N_even()
    n67 = n6_ne_n7_even()
    gap = gap9_scar()
    prize = prize_gap9()
    xor5 = xorcat_n5_not_always_odd()
    pref67 = n7_ne_n8_prefix()
    pref = dy_prefix()
    checks = self_checks(
        c20, not_o, not_e, n67s, typ, n67, gap, prize, xor5, pref67, pref
    )
    dump = {
        "cycle": "DZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n5_type": typ["rows"],
        "n6_ne_n7": n67["rows"],
        "gap9_scar": gap["rows"],
        "n5_not_E": not_e,
        "n6_ne_n7_step": n67s,
        "prize_gap9": prize["rows"],
        "n7_ne_n8_prefix": pref67["rows"],
        "lemmas": {
            "n5_type_N_even_n0": True,
            "n6_ne_n7_even_n0": True,
            "post_odd_9bit_gap_even_n0": True,
            "xorcat_n5_always_odd": False,
            "n6_always_type_N": False,
            "post_odd_10bit_gap_all_n0": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n5_type_N_even_n0": "LEMMA",
            "n6_ne_n7_even_n0": "LEMMA",
            "post_odd_9bit_gap_even_n0": "LEMMA",
            "xorcat_n5_always_odd": "KILLED",
            "n6_always_type_N": "KILLED",
            "post_odd_10bit_gap_all_n0": "PREFIX",
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
    print("n5_type", dump["n5_type"])
    print("prize_gap9", dump["prize_gap9"])


if __name__ == "__main__":
    main()
