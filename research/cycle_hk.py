#!/usr/bin/env python3
"""Cycle HK: even-s AND without odd-s AND splits into three die patterns.

On covering (n,j), die (even-s AND live, odd-s AND dead) iff the
even-s 4-tuple is 0111, 1011, or 1111. Dual of Cycle HI fresh.
Die is not only 0111; die is not only on G=1; even-s AND is not
iff 0011. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_hk.py --certify
Dump: research/cycle_hk.json
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
from cycle_hj import slot_mask
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HI_JSON = Path(__file__).resolve().parent / "cycle_hi.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

DIE = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1))
DIE_SLOT = {
    (0, 1, 1, 1): "cob_jp1+copy_j+cob_j",
    (1, 0, 1, 1): "copy_jp1+copy_j+cob_j",
    (1, 1, 1, 1): "copy_jp1+cob_jp1+copy_j+cob_j",
}


def die_slots() -> dict:
    """DIE occupy the named copy/cob slots; disjoint from FRESH/CONT."""
    got = {t: slot_mask(t) for t in DIE}
    ok = got == DIE_SLOT
    ok = ok and not any(t in FRESH or t == CONT for t in DIE)
    ok = ok and all(t not in AND_ONES for t in DIE)
    return {"ok": ok, "slots": {str(t): got[t] for t in DIE}}


def _walk_die(k: int, q: int) -> dict:
    """Die split on covering (n,j) even-rho columns."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_die = n_cont = n_fresh = 0
    xor_all = 0
    fire = {t: 0 for t in DIE}
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
                tup = (
                    bit_at(prev, p - 3),
                    bit_at(prev, p - 2),
                    bit_at(prev, p - 1),
                    bit_at(prev, p),
                )
                o = (Aodd >> p) & 1
                e = (Aeven >> p) & 1
                if (e and not o) != (tup in DIE):
                    return {
                        "ok": False,
                        "die": True,
                        "k": k,
                        "q": q,
                        "s": s,
                        "p": p,
                        "tup": tup,
                        "o": o,
                        "e": e,
                    }
                if (o and not e) != (tup in FRESH):
                    return {"ok": False, "fresh": True, "k": k, "tup": tup}
                if (o and e) != (tup == CONT):
                    return {"ok": False, "cont": True, "k": k, "tup": tup}
                n_ok += 1
                if e and not o:
                    n_die += 1
                    fire[tup] += 1
                if o and e:
                    n_cont += 1
                if o and not e:
                    n_fresh += 1
                if o and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_die": n_die,
        "n_cont": n_cont,
        "n_fresh": n_fresh,
        "xor_all": xor_all,
        "fire": {str(t): fire[t] for t in DIE},
    }


def die_split() -> dict:
    """Die split on J6/J10, k<=6; XOR matches HF/HG; counts match HI."""
    n_ok = n_die = n_cont = n_fresh = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    hi = json.loads(HI_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_die(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_all"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_all"] != want:
                    return {"ok": False, "xor10": True, "k": k, "got": w["xor_all"], "want": want}
            hi_row = hi["and_split"]["rows"][str(k)][name]
            if w["n_die"] != hi_row["n_die"] or w["n_fresh"] != hi_row["n_fresh"]:
                return {
                    "ok": False,
                    "hi": True,
                    "k": k,
                    "name": name,
                    "n_die": w["n_die"],
                    "want_die": hi_row["n_die"],
                }
            n_ok += w["n_ok"]
            n_die += w["n_die"]
            n_cont += w["n_cont"]
            n_fresh += w["n_fresh"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_die": w["n_die"],
                "n_cont": w["n_cont"],
                "n_fresh": w["n_fresh"],
                "xor_all": w["xor_all"],
                "fire": w["fire"],
            }
        rows[str(k)] = krow
    return {
        "ok": True,
        "n_ok": n_ok,
        "n_die": n_die,
        "n_cont": n_cont,
        "n_fresh": n_fresh,
        "rows": rows,
    }


def killed_die_only_0111() -> dict:
    """Die is not only 0111: k=1, s=11, tup=1011."""
    k, s, n, j, p = 1, 11, 0, 0, 12
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    tup = (
        bit_at(prev, p - 3),
        bit_at(prev, p - 2),
        bit_at(prev, p - 1),
        bit_at(prev, p),
    )
    Aodd = (row << 1) & row
    Aeven = (prev << 1) & prev
    o, e = (Aodd >> p) & 1, (Aeven >> p) & 1
    ok = tup == (1, 0, 1, 1) and e == 1 and o == 0 and G(n, j) == 1
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "e": e,
        "o": o,
    }


def killed_die_only_g1() -> dict:
    """Die is not only on G=1: k=2, s=11, tup=1111."""
    k, s, n, j, p = 2, 11, 6, 5, 14
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    tup = (
        bit_at(prev, p - 3),
        bit_at(prev, p - 2),
        bit_at(prev, p - 1),
        bit_at(prev, p),
    )
    Aodd = (row << 1) & row
    Aeven = (prev << 1) & prev
    o, e = (Aodd >> p) & 1, (Aeven >> p) & 1
    g = G(n, j)
    ok = tup == (1, 1, 1, 1) and e == 1 and o == 0 and g == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "e": e,
        "o": o,
        "G": g,
    }


def killed_even_and_iff_0011() -> dict:
    """Even-s AND is not iff 0011: k=1, s=11, tup=1011."""
    w = killed_die_only_0111()
    ok = w["ok"] and w["tup"] != [0, 0, 1, 1] and w["e"] == 1
    return {
        "ok": ok,
        "k": w["k"],
        "s": w["s"],
        "n": w["n"],
        "j": w["j"],
        "p": w["p"],
        "tup": w["tup"],
        "e": w["e"],
    }


def prefixes() -> dict:
    hj = json.loads(HJ_JSON.read_text())
    hi = json.loads(HI_JSON.read_text())
    ok = (
        hj["checks"]["all_ok"]
        and hi["checks"]["all_ok"]
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hi["verdict"]["fresh_iff_0010_or_0100_or_1001"] == "LEMMA"
        and hj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ds: dict, sp: dict, k0111: dict, kg: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ds["ok"] and sp["ok"] and k0111["ok"] and kg["ok"] and ke["ok"] and pref["ok"]
    assert DIE_SLOT[(0, 1, 1, 1)] == "cob_jp1+copy_j+cob_j"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ds = die_slots()
    sp = die_split()
    k0111 = killed_die_only_0111()
    kg = killed_die_only_g1()
    ke = killed_even_and_iff_0011()
    pref = prefixes()
    checks = self_checks(c20, ds, sp, k0111, kg, ke, pref)
    dump = {
        "cycle": "HK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "die_slots": {k: ds[k] for k in ds if k != "ok"},
        "die_split": {k: sp[k] for k in sp if k != "ok"},
        "killed_die_only_0111": {k: k0111[k] for k in k0111 if k != "ok"},
        "killed_die_only_g1": {k: kg[k] for k in kg if k != "ok"},
        "killed_even_and_iff_0011": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "die_iff_0111_or_1011_or_1111": True,
            "die_0111_occupies_cob_jp1_copy_j_cob_j": True,
            "die_1011_occupies_copy_jp1_copy_j_cob_j": True,
            "die_1111_occupies_all_four": True,
            "die_only_0111": False,
            "die_only_on_G_eq_1": False,
            "even_s_AND_iff_0011": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "die_iff_0111_or_1011_or_1111": "LEMMA",
            "die_0111_occupies_cob_jp1_copy_j_cob_j": "LEMMA",
            "die_1011_occupies_copy_jp1_copy_j_cob_j": "LEMMA",
            "die_1111_occupies_all_four": "LEMMA",
            "die_only_0111": "KILLED",
            "die_only_on_G_eq_1": "KILLED",
            "even_s_AND_iff_0011": "KILLED",
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
    print(
        "die_split n_ok",
        dump["die_split"]["n_ok"],
        "n_die",
        dump["die_split"]["n_die"],
        "n_cont",
        dump["die_split"]["n_cont"],
        "n_fresh",
        dump["die_split"]["n_fresh"],
    )
    print("killed_die_only_0111", dump["killed_die_only_0111"])
    print("killed_die_only_g1", dump["killed_die_only_g1"])
    print("killed_even_and_iff_0011", dump["killed_even_and_iff_0011"])


if __name__ == "__main__":
    main()
