#!/usr/bin/env python3
"""Cycle DY: even n0 O-type n4 is type N; 8-bit post-odd ident-0 gap.

For even half-length n0>=2, no O-type word is alternating (the two
alternating words are E-type), so n4=reconstruct(s,n3) is not 0.
Pair invariants then force at least one empty pair (Z=0 would make
n4=0 via ov=Z). Empty pairs have both n4=1, so n4 is not O-type;
ov=Z>=1 gives a disagreeing pair, so n4 is not E-type. Hence n4 is
type N. Moreover n3=D(n4) iff s=n3 and n4, which on an empty pair
forces s_t=s_{t+n0}=0, contradicting O-type, so n4!=n5. Assuming
n5=n6 forces n5=0 on empty pairs; the O-type side with s=1 then
two-steps to n3=not s' versus n4=s'. Thus n5!=n6, and after an odd
doubling there is no ident-0 at p+1,...,p+8. Odd n0 can have n4=0;
ham(n4,n5) is not n0; n6 is not always type N. Do not compute
phi^{(3,5,9)} at k=16. Not a prize claim: an 8-bit gap does not fill
an annulus.

Run: python3 research/cycle_dy.py --certify
Dump: research/cycle_dy.json
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
from cycle_ca import KNOWN20, deriv, packed_center_bits, prize_cycle, reconstruct
from cycle_cb import ext, twocopy_type
from cycle_ch import ham, scar_lift, shifted_not
from cycle_df import unfold
from cycle_dv import EXPECTED_P, mask_bits, n3n4_of, odd_copy
from cycle_dw import xorv

OUT = Path(__file__).resolve().with_suffix(".json")
DX_JSON = Path(__file__).resolve().parent / "cycle_dx.json"


def is_alternating(seq: list[int]) -> bool:
    n = len(seq)
    return n >= 2 and all(seq[t] != seq[(t + 1) % n] for t in range(n))


def only_two_alternating() -> bool:
    """Alternating words are exactly the 01- and 10-repeats; even n0 => E-type."""
    for n in range(2, 33, 2):
        alt01 = [i % 2 for i in range(n)]
        alt10 = [1 - (i % 2) for i in range(n)]
        if not (is_alternating(alt01) and is_alternating(alt10)):
            return False
        for b0 in (0, 1):
            s = [(b0 + i) % 2 for i in range(n)]
            if not is_alternating(s):
                return False
            if s != (alt01 if b0 == 0 else alt10):
                return False
        n0 = n // 2
        want = "E" if n0 % 2 == 0 else "O"
        if twocopy_type(alt01) != want or twocopy_type(alt10) != want:
            return False
    return True


def even_O_never_alternating() -> bool:
    """Every O-type of even n0>=2 is non-alternating, so s!=n3 and n4!=0."""
    for n0 in (2, 4, 6, 8, 10, 12):
        L = 2 * n0
        ones = [1] * L
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            if twocopy_type(s) != "O" or is_alternating(s):
                return False
            n3 = reconstruct(ones, s)
            if n3 is None or n3 == s or not any(n3):
                return False
            n4 = reconstruct(s, n3)
            if n4 is None or not any(n4):
                return False
    return True


def dn4_identity() -> bool:
    """D(n4)_t = s_t xor (n3_t and not n4_t); n3=D(n4) iff s=n3 and n4."""
    for n0 in range(2, 9):
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(s)
            if pair is None:
                return False
            n3, n4 = pair
            L = len(s)
            dn4 = deriv(n4)
            pred = [s[t] ^ (n3[t] & (1 - n4[t])) for t in range(L)]
            if dn4 != pred:
                return False
            eq = n3 == dn4
            iff = s == [n3[t] & n4[t] for t in range(L)]
            if eq != iff:
                return False
    return True


def empty_pair_stats(s: list[int]) -> tuple[int, int, bool, bool] | None:
    """Z, ov, empty-both-n4-1, some n4 disagree. None if reconstruct fails."""
    n0 = len(s) // 2
    pair = n3n4_of(s)
    if pair is None:
        return None
    n3, n4 = pair
    d = xorv(n3, n4)
    z = 0
    ov = 0
    empty_ones = True
    disagree = False
    for t in range(n0):
        a, b = n3[t], n3[t + n0]
        if a and b:
            return None
        if a == 0 and b == 0:
            z += 1
            if n4[t] != 1 or n4[t + n0] != 1:
                empty_ones = False
            if s[t] == s[t + n0]:
                return None
        if n4[t] != n4[t + n0]:
            disagree = True
        if n3[t] == 1 and d[t] == 0:
            ov += 1
        if n3[t + n0] == 1 and d[t + n0] == 0:
            ov += 1
    return z, ov, empty_ones, disagree


def n4_type_N_even() -> dict:
    """Even n0 O-type: Z=ov>=1, empty n4=11, type N, n3!=D(n4)."""
    rows: dict[int, dict] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ok = 0
        types: set[str] = set()
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            st = empty_pair_stats(s)
            if st is None:
                return {"ok": False, "n0": n0, "why": "stats"}
            z, ov, empty_ones, disagree = st
            pair = n3n4_of(s)
            if pair is None:
                return {"ok": False, "n0": n0}
            n3, n4 = pair
            typ = twocopy_type(n4)
            types.add(typ)
            if z < 1 or ov != z or not empty_ones or not disagree:
                return {"ok": False, "n0": n0, "z": z, "ov": ov}
            if typ != "N" or n3 == deriv(n4) or n4 == n3:
                return {"ok": False, "n0": n0, "typ": typ}
            n_ok += 1
        if types != {"N"}:
            return {"ok": False, "n0": n0, "types": sorted(types)}
        rows[n0] = {"n": n_ok, "type": "N"}
    rng = random.Random(17)
    n16 = 0
    for _ in range(40):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        st = empty_pair_stats(s)
        pair = n3n4_of(s)
        if st is None or pair is None:
            return {"ok": False, "n0": 16}
        z, ov, empty_ones, disagree = st
        n3, n4 = pair
        if z < 1 or ov != z or not empty_ones or twocopy_type(n4) != "N":
            return {"ok": False, "n0": 16, "z": z}
        if not disagree or n3 == deriv(n4):
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = {"n": n16, "type": "N", "sampled": True}
    return {"ok": True, "rows": rows}


def rec_n3(s: int, n3: int) -> int:
    return 0 if (s or n3) else 1


def rec_n4(s: int, n3: int, n4: int) -> int:
    return s ^ (n3 | n4)


def rec_n5(n3: int, n4: int, n5: int) -> int:
    return n3 ^ (n4 | n5)


def two_step_kills_n5_eq_n6() -> dict:
    """Empty pair with s=1 and n5=0 two-steps to n3=not s' vs n4=s'."""
    s, n3, n4, n5 = 1, 0, 1, 0
    a, b, c = rec_n3(s, n3), rec_n4(s, n3, n4), rec_n5(n3, n4, n5)
    if (a, b, c) != (0, 0, 1):
        return {"ok": False, "mid": [a, b, c]}
    n_ok = 0
    for s2 in (0, 1):
        n3b = rec_n3(s2, a)
        n4b = rec_n4(s2, a, b)
        n5b = rec_n5(a, b, c)
        if (n3b, n4b, n5b) != (s2 ^ 1, s2, 1):
            return {"ok": False, "s2": s2}
        if n3b == (n4b & n5b):
            return {"ok": False, "eq": s2}
        n_ok += 1
    return {"ok": n_ok == 2, "n": n_ok}


def tail(s: list[int], n_extra: int) -> list[list[int]] | None:
    """ones,s -> n3,n4,... ; returns [s,n3,n4,...] of length 1+n_extra."""
    L = len(s)
    prev, cur = [1] * L, s
    out = [cur]
    for _ in range(n_extra):
        u = reconstruct(prev, cur)
        if u is None:
            return None
        out.append(u)
        prev, cur = cur, u
    return out


def n5_ne_n6_even() -> dict:
    """n5!=n6 on every even-n0 O-type through n0=12, 40 random n0=16."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8, 10, 12):
        n_ok = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            out = tail(s, 4)
            if out is None:
                return {"ok": False, "n0": n0}
            n4, n5, n6 = out[2], out[3], out[4]
            if n4 == n5 or n5 == n6:
                return {"ok": False, "n0": n0, "mask": mask}
            n_ok += 1
        rows[n0] = n_ok
    rng = random.Random(19)
    n16 = 0
    for _ in range(40):
        s = odd_copy([rng.randint(0, 1) for _ in range(16)])
        out = tail(s, 4)
        if out is None or out[2] == out[3] or out[3] == out[4]:
            return {"ok": False, "n0": 16}
        n16 += 1
    rows[16] = n16
    return {"ok": True, "rows": rows}


def gap8_scar() -> dict:
    """scar_lift through seqs[8] succeeds for every even-n0 T0<=8."""
    rows: dict[int, int] = {}
    for n0 in (2, 4, 6, 8):
        n_ok = 0
        for mask in range(1 << n0):
            t0 = mask_bits(mask, n0)
            seqs = scar_lift(t0, 6)
            if seqs is None or set(seqs) != set(range(9)):
                return {"ok": False, "n0": n0, "mask": mask}
            for i in range(1, 9):
                if not any(seqs[i]):
                    return {"ok": False, "n0": n0, "zero": i}
            n_ok += 1
        rows[n0] = n_ok
    return {"ok": True, "rows": rows}


def prize_gap8() -> dict:
    """Prize k=4,8,16: n4 type N, n3!=D(n4), n5!=n6, no ident-0 in p+1..p+8."""
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
        for q in range(found + 1, found + 9):
            aa = ext(seqs[q - 2], cur_pi)
            bb = ext(seqs[q - 1], cur_pi)
            if all(x == 0 for x in bb):
                return {"ok": False, "k": k, "why": "gap", "q": q}
            seqs[q] = reconstruct(aa, bb)
        o = ext(seqs[found], cur_pi)
        s = ext(seqs[found + 2], cur_pi)
        n3 = ext(seqs[found + 3], cur_pi)
        n4 = ext(seqs[found + 4], cur_pi)
        n5 = ext(seqs[found + 5], cur_pi)
        n6 = ext(seqs[found + 6], cur_pi)
        n0 = cur_pi // 2
        if (
            twocopy_type(o) != "O"
            or s != shifted_not(o)
            or twocopy_type(n4) != "N"
            or n3 == deriv(n4)
            or n4 == n5
            or n5 == n6
            or n0 != pi
        ):
            return {"ok": False, "k": k, "n4": twocopy_type(n4)}
        rows[k] = {
            "p": found,
            "pi": pi,
            "n4": "N",
            "gap8": True,
        }
    return {"ok": True, "rows": rows}


def n4_zero_odd_n0() -> bool:
    """Odd n0: the two alternating O-types have n4=0."""
    for n0 in (1, 3, 5, 7):
        L = 2 * n0
        n_zero = 0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            pair = n3n4_of(s)
            if pair is None:
                if is_alternating(s):
                    n_zero += 1
                    continue
                return False
            n3, n4 = pair
            if not any(n4):
                if not is_alternating(s) or n3 != s:
                    return False
                n_zero += 1
        if n_zero != 2:
            return False
        if twocopy_type([i % 2 for i in range(L)]) != "O":
            return False
    return True


def ham_n4_n5_not_n0() -> bool:
    """ham(n4,n5)=n0 fails on even n0=4 (hamset includes 3)."""
    hamset: set[int] = set()
    for mask in range(16):
        s = odd_copy(mask_bits(mask, 4))
        out = tail(s, 3)
        if out is None:
            return False
        hamset.add(ham(out[2], out[3]))
    return hamset != {4} and 3 in hamset


def n6_not_always_N() -> bool:
    """n6 can be O-type on even n0=4."""
    types: set[str] = set()
    for mask in range(16):
        s = odd_copy(mask_bits(mask, 4))
        out = tail(s, 4)
        if out is None:
            return False
        types.add(twocopy_type(out[4]))
    return types == {"O", "N"}


def dx_prefix() -> dict:
    dx = json.loads(DX_JSON.read_text())
    ok = (
        dx["checks"]["all_ok"]
        and dx["lemmas"]["pair_invariants_all_n0"]
        and dx["lemmas"]["ham_n3_n4_equals_n0_all_O_type"]
        and dx["prize_ham"]["16"]["ham_n3_n4"] == 16
        and dx["verdict"]["pair_invariants_all_n0"] == "LEMMA"
    )
    return {"ok": ok, "prize": dx["prize_ham"]}


def self_checks(
    c20,
    alt: bool,
    never_alt: bool,
    dn4: bool,
    typ: dict,
    step: dict,
    n56: dict,
    gap: dict,
    prize: dict,
    oddz: bool,
    ham45: bool,
    n6n: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert alt and never_alt and dn4 and typ["ok"] and step["ok"]
    assert n56["ok"] and gap["ok"] and prize["ok"]
    assert oddz and ham45 and n6n and pref["ok"]
    assert typ["rows"][2]["type"] == "N"
    assert typ["rows"][8]["n"] == 256
    assert n56["rows"][8] == 256
    assert gap["rows"][8] == 256
    assert prize["rows"][4]["gap8"] and prize["rows"][16]["n4"] == "N"
    assert step["n"] == 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    alt = only_two_alternating()
    never_alt = even_O_never_alternating()
    dn4 = dn4_identity()
    typ = n4_type_N_even()
    step = two_step_kills_n5_eq_n6()
    n56 = n5_ne_n6_even()
    gap = gap8_scar()
    prize = prize_gap8()
    oddz = n4_zero_odd_n0()
    ham45 = ham_n4_n5_not_n0()
    n6n = n6_not_always_N()
    pref = dx_prefix()
    checks = self_checks(
        c20, alt, never_alt, dn4, typ, step, n56, gap, prize,
        oddz, ham45, n6n, pref,
    )
    dump = {
        "cycle": "DY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n4_type": typ["rows"],
        "n5_ne_n6": n56["rows"],
        "gap8_scar": gap["rows"],
        "two_step": step,
        "prize_gap8": prize["rows"],
        "lemmas": {
            "even_O_never_alternating": True,
            "n4_type_N_even_n0": True,
            "n3_ne_deriv_n4_even_n0": True,
            "n5_ne_n6_even_n0": True,
            "post_odd_8bit_gap_even_n0": True,
            "n4_never_zero_odd_n0": False,
            "ham_n4_n5_equals_n0": False,
            "n6_always_type_N": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_O_never_alternating": "LEMMA",
            "n4_type_N_even_n0": "LEMMA",
            "n3_ne_deriv_n4_even_n0": "LEMMA",
            "n5_ne_n6_even_n0": "LEMMA",
            "post_odd_8bit_gap_even_n0": "LEMMA",
            "n4_never_zero_odd_n0": "KILLED",
            "ham_n4_n5_equals_n0": "KILLED",
            "n6_always_type_N": "KILLED",
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
    print("n4_type", dump["n4_type"])
    print("prize_gap8", dump["prize_gap8"])


if __name__ == "__main__":
    main()
