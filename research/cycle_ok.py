#!/usr/bin/env python3
"""Cycle OK: pal-right S-xor of G(j+1) vanishes on every even n.

S contributes G(n,j+1) on pal-right d%3==1 cells with G(n,j)=1 and
G(n,j-1)=0. If n is even and G(n,j)=1 then j is even, so j+1 is
odd, so G(n,j+1)=0. Pal-right S-xor and S-fire therefore vanish on
every even n (same Green even-n / odd-d rule as Cycle OI's T).
Covering S is an odd-n xor. Odd n is not identically 0 (n=9 xor=1)
and not identically 1 (n=1 xor=0). Odd n=2m+1 reduces by Green
doubling to parent 01-flips (r%3==1) xor parent 11-flips times
NOT G(m, m+r+1) (r%3==2); that is not a closed evaluation. Even-n
packed rest R does not vanish (q=10 k=0: R_even=1). Do not claim
E_k=0 for all k. Do not claim S equals T or rest. Do not catalogue
further S/T subregions unless the experiment answers why E_k=0.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ok.py --certify
Dump: research/cycle_ok.json
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
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oi import pal_right_t
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_ALG = 256
M_ALG = 128


def pal_right_s(n: int) -> tuple[int, int, int]:
    """Pal-right d%3==1, G(j-1)=0: xor of G(j+1), cell count, fire count."""
    xor_s = n_s = n_fire = 0
    for j in range(n + 1, 2 * n + 1):
        if G(n, j) == 0:
            continue
        if (j - n) % 3 != 1:
            continue
        if G(n, j - 1) != 0:
            continue
        n_s += 1
        b = G(n, j + 1)
        xor_s ^= b
        n_fire += b
    return xor_s, n_s, n_fire


def doubling_s(m: int) -> int:
    """Odd n=2m+1 pal-right S from parent 01 (r%3==1) and 11 (r%3==2)."""
    ev = od = 0
    for k in range(m + 1, 2 * m + 2):
        r = k - m
        if r % 3 == 1 and G(m, k - 1) == 0 and G(m, k) == 1:
            ev ^= 1
    for k in range(m + 1, 2 * m + 1):
        r = k - m
        if r % 3 == 2 and G(m, k - 1) == 1 and G(m, k) == 1:
            od ^= 1 ^ G(m, k + 1)
    return ev ^ od


def even_s_vanish(n_hi: int) -> dict:
    """Even n<n_hi: pal-right S-fire 0; n_s may be positive."""
    n_s = n_fire = n_even_s = 0
    for n in range(0, n_hi, 2):
        xor_s, ns, nf = pal_right_s(n)
        if xor_s != 0 or nf != 0:
            return {"ok": False, "n": n, "xor": xor_s, "n_fire": nf}
        n_s += ns
        n_fire += nf
        if ns:
            n_even_s += 1
            for j in range(n + 1, 2 * n + 1):
                if G(n, j) == 0:
                    continue
                if j % 2:
                    return {"ok": False, "odd_j": n, "j": j}
                if G(n, j + 1) != 0:
                    return {"ok": False, "jp1": n, "j": j}
    ok = n_fire == 0 and n_s > 0 and n_even_s > 0
    return {
        "ok": ok,
        "n_hi": n_hi,
        "n_s": n_s,
        "n_fire": n_fire,
        "n_even_s": n_even_s,
    }


def odd_s_doubling(m_hi: int) -> dict:
    """Odd n=2m+1 pal-right S equals doubling_s(m)."""
    n_ok = n_one = 0
    sample = {}
    for m in range(0, m_hi):
        n = 2 * m + 1
        xor_s, n_s, n_fire = pal_right_s(n)
        want = doubling_s(m)
        if xor_s != want:
            return {"ok": False, "n": n, "xor": xor_s, "want": want}
        n_ok += 1
        n_one += xor_s
        if n <= 15:
            sample[str(n)] = {"xor": xor_s, "n_s": n_s, "n_fire": n_fire}
    ok = (
        n_ok == m_hi
        and sample["1"]["xor"] == 0
        and sample["9"]["xor"] == 1
        and sample["9"]["n_fire"] == 1
        and pal_right_t(1)[0] == 1
        and n_one > 0
        and n_one < m_hi
    )
    return {
        "ok": ok,
        "m_hi": m_hi,
        "n_ok": n_ok,
        "n_one": n_one,
        "sample": sample,
    }


def even_r_k0() -> dict:
    """q=10 k=0: packed rest xor on even n is 1 (does not vanish)."""
    k, q = 0, 10
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    r_e = r_o = n_r_e = 0
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
                if G(n, j) == 0 or not packed or p in FORCED:
                    continue
                if n % 2 == 0:
                    r_e ^= 1
                    n_r_e += 1
                else:
                    r_o ^= 1
        row = rule30_step(row)
        s += 1
    ok = r_e == 1 and n_r_e == 1 and r_o == 1
    return {"ok": ok, "k": 0, "q": 10, "r_e": r_e, "r_o": r_o, "n_r_e": n_r_e}


def killed_odd_zero(odd: dict) -> dict:
    r = odd["sample"]["9"]
    ok = r["xor"] == 1
    return {"ok": ok, "n": 9, "xor": r["xor"]}


def killed_eq_t(odd: dict) -> dict:
    r = odd["sample"]["1"]
    ok = r["xor"] == 0 and pal_right_t(1)[0] == 1
    return {"ok": ok, "n": 1, "S": 0, "T": 1}


def killed_even_r(er: dict) -> dict:
    ok = er["r_e"] == 1
    return {"ok": ok, "k": 0, "r_e": er["r_e"], "n_r_e": er["n_r_e"]}


def prefixes() -> dict:
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oj["verdict"]["odd_t_xor_all_n"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and oj["verdict"]["even_t_vanish"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, even, odd, er, ko, kt, kr, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        even["ok"]
        and odd["ok"]
        and er["ok"]
        and ko["ok"]
        and kt["ok"]
        and kr["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert even["n_fire"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    even = even_s_vanish(N_ALG)
    odd = odd_s_doubling(M_ALG)
    er = even_r_k0()
    ko = killed_odd_zero(odd)
    kt = killed_eq_t(odd)
    kr = killed_even_r(er)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, even, odd, er, ko, kt, kr, sc, pref)
    dump = {
        "cycle": "OK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_s_vanish": {k: even[k] for k in even if k != "ok"},
        "odd_s_doubling": {k: odd[k] for k in odd if k != "ok"},
        "even_r_k0": {k: er[k] for k in er if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_odd_zero": {k: ko[k] for k in ko if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_even_r": {k: kr[k] for k in kr if k != "ok"},
        "lemmas": {
            "even_s_vanish": True,
            "odd_s_doubling": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "odd_s_zero": False,
            "eq_t": False,
            "even_r_vanish": False,
            "odd_s_closed": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_s_vanish": "LEMMA",
            "odd_s_doubling": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "odd_s_zero": "KILLED",
            "eq_t": "KILLED",
            "even_r_vanish": "KILLED",
            "odd_s_closed": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("even_s_vanish", dump["even_s_vanish"])
    print("odd_s_doubling n_ok", dump["odd_s_doubling"]["n_ok"], "n_one", dump["odd_s_doubling"]["n_one"])
    print("even_r_k0", dump["even_r_k0"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_odd_zero", dump["killed_odd_zero"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_even_r", dump["killed_even_r"])


if __name__ == "__main__":
    main()
