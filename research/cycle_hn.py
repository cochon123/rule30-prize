#!/usr/bin/env python3
"""Cycle HN: both-AND 6-tuples; odd AND forbids even AND at p-2.

Odd-s AND at p and even-s AND at p-2 cannot both be 1: AND_ONES
never starts with 11. Both adjacent odd-s AND iff the even-s
6-tuple is one of 001001, 010010, 010011, 100100. Both-AND is not
only 100100; not only when G(n,j)=G(n,j+1)=1; not only on G=1.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_hn.py --certify
Dump: research/cycle_hn.json
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
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HM_JSON = Path(__file__).resolve().parent / "cycle_hm.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

BOTH_AND = (
    (0, 0, 1, 0, 0, 1),
    (0, 1, 0, 0, 1, 0),
    (0, 1, 0, 0, 1, 1),
    (1, 0, 0, 1, 0, 0),
)


def both_and_table() -> dict:
    """64-row: both adjacent AND iff 6-tuple in BOTH_AND; AND_ONES no 11 prefix."""
    if any(t[:2] == (1, 1) for t in AND_ONES):
        return {"ok": False, "prefix": True}
    got = []
    n_ok = 0
    for bits in range(64):
        six = tuple((bits >> i) & 1 for i in range(5, -1, -1))
        u, v, z, a, b, c = six
        both = and_from_tuple(u, v, z, a) and and_from_tuple(z, a, b, c)
        if both:
            got.append(six)
        n_ok += 1
    ok = tuple(got) == BOTH_AND and n_ok == 64
    return {"ok": ok, "n_ok": n_ok, "n_both": len(got)}


def _walk_both(k: int, q: int) -> dict:
    """Forbid + both-AND 6-tuples on covering (n,j)."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_both = xor_all = 0
    fire = {t: 0 for t in BOTH_AND}
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            Aeven = (prev << 1) & prev
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
                u, v, z, a, b, c = six
                o = (Aodd >> p) & 1
                e1 = (Aeven >> (p - 2)) & 1 if p >= 2 else 0
                if o and e1:
                    return {"ok": False, "forbid": True, "k": k, "s": s, "p": p}
                Aj = and_from_tuple(z, a, b, c)
                Aj1 = and_from_tuple(u, v, z, a)
                if (Aj and Aj1) != (six in BOTH_AND):
                    return {"ok": False, "both": True, "k": k, "six": six}
                n_ok += 1
                if Aj and Aj1:
                    n_both += 1
                    fire[six] += 1
                if o and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_both": n_both,
        "xor_all": xor_all,
        "fire": {str(t): fire[t] for t in BOTH_AND},
    }


def both_cover() -> dict:
    """Forbid + both-AND on J6/J10, k<=6; XOR matches HF/HG."""
    n_ok = n_both = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_both(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_all"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_all"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_all"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_both += w["n_both"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_both": w["n_both"],
                "xor_all": w["xor_all"],
                "fire": w["fire"],
            }
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "n_both": n_both, "rows": rows}


def killed_both_only_100100() -> dict:
    """Both-AND is not only 100100: k=1, s=7, six=001001."""
    k, s, n, j, p = 1, 7, 2, 0, 12
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    u, v, z, a, b, c = six
    ok = six == (0, 0, 1, 0, 0, 1) and and_from_tuple(u, v, z, a) and and_from_tuple(z, a, b, c)
    return {"ok": ok, "k": k, "s": s, "n": n, "j": j, "p": p, "six": list(six)}


def killed_both_eq_Gpair() -> dict:
    """Both-AND is not only when G(n,j)=G(n,j+1)=1: k=0, s=5."""
    k, s, n, j, p = 0, 5, 0, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    u, v, z, a, b, c = six
    g, gj1 = G(n, j), G(n, j + 1)
    ok = (
        six == (1, 0, 0, 1, 0, 0)
        and and_from_tuple(u, v, z, a)
        and and_from_tuple(z, a, b, c)
        and g == 1
        and gj1 == 0
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
        "G": g,
        "Gj1": gj1,
    }


def killed_both_only_g1() -> dict:
    """Both-AND is not only on G=1: k=2, s=9, n=7, j=9."""
    k, s, n, j, p = 2, 9, 7, 9, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    u, v, z, a, b, c = six
    g = G(n, j)
    ok = (
        six == (1, 0, 0, 1, 0, 0)
        and and_from_tuple(u, v, z, a)
        and and_from_tuple(z, a, b, c)
        and g == 0
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
        "G": g,
    }


def prefixes() -> dict:
    hm = json.loads(HM_JSON.read_text())
    ok = (
        hm["checks"]["all_ok"]
        and hm["verdict"]["even_s_Green_6slot_eq_green6"] == "LEMMA"
        and hm["verdict"]["adjacent_AND_eq_overlapping_4tuples"] == "LEMMA"
        and hm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, bt: dict, bc: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert bt["ok"] and bc["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert (1, 0, 0, 1, 0, 0) in BOTH_AND
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    bt = both_and_table()
    bc = both_cover()
    k1 = killed_both_only_100100()
    k2 = killed_both_eq_Gpair()
    k3 = killed_both_only_g1()
    pref = prefixes()
    checks = self_checks(c20, bt, bc, k1, k2, k3, pref)
    dump = {
        "cycle": "HN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "both_and_table": {k: bt[k] for k in bt if k != "ok"},
        "both_cover": {k: bc[k] for k in bc if k != "ok"},
        "killed_both_only_100100": {k: k1[k] for k in k1 if k != "ok"},
        "killed_both_eq_Gpair": {k: k2[k] for k in k2 if k != "ok"},
        "killed_both_only_g1": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "both_AND_iff_4_six_tuples": True,
            "odd_AND_forbids_even_AND_at_p_minus_2": True,
            "AND_ONES_no_11_prefix": True,
            "both_AND_only_100100": False,
            "both_AND_only_when_G_pair_11": False,
            "both_AND_only_on_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "both_AND_iff_4_six_tuples": "LEMMA",
            "odd_AND_forbids_even_AND_at_p_minus_2": "LEMMA",
            "AND_ONES_no_11_prefix": "LEMMA",
            "both_AND_only_100100": "KILLED",
            "both_AND_only_when_G_pair_11": "KILLED",
            "both_AND_only_on_G_eq_1": "KILLED",
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
    print("both_and_table n_both", dump["both_and_table"]["n_both"])
    print("both_cover n_ok", dump["both_cover"]["n_ok"], "n_both", dump["both_cover"]["n_both"])
    print("killed_both_only_100100", dump["killed_both_only_100100"])
    print("killed_both_eq_Gpair", dump["killed_both_eq_Gpair"])
    print("killed_both_only_g1", dump["killed_both_only_g1"])


if __name__ == "__main__":
    main()
