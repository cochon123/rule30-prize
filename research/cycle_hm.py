#!/usr/bin/env python3
"""Cycle HM: even-s Green 6-slot; odd-s 4-tuple is Rule 30 of that 6-tuple.

On covering (n,j), even-s Green at packed bits p-5..p is
green6(n,j)=(G(n,j+2), cob(j+2), G(n,j+1), cob(j+1), G(n,j), cob(j)),
overlapping green4(n,j+1) and green4(n,j). The odd-s 4-tuple is
Rule 30 of the even-s 6-tuple; adjacent AND is the two overlapping
4-tuple productions. The 6-tuple is not green6; the AND pair is not
(G(n,j+1), G(n,j)); adjacent AND is not independent. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hm.py --certify
Dump: research/cycle_hm.json
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
from cycle_hh import and_from_tuple, bit_at
from cycle_hj import green4
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HL_JSON = Path(__file__).resolve().parent / "cycle_hl.json"
HJ_JSON = Path(__file__).resolve().parent / "cycle_hj.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def green6(n: int, j: int) -> tuple[int, int, int, int, int, int]:
    """Even-s Green at p-5..p on covering (n,j)."""
    gj = G(n, j)
    gj1 = G(n, j + 1)
    gj2 = G(n, j + 2)
    return (gj2, gj2 ^ gj1, gj1, gj1 ^ gj, gj, gj ^ G(n, j - 1))


def r30_4(six: tuple[int, int, int, int, int, int]) -> tuple[int, int, int, int]:
    """Odd-s 4-tuple at p-3..p from even-s bits p-5..p."""
    u, v, z, a, b, c = six
    return (u ^ (v | z), v ^ (z | a), z ^ (a | b), a ^ (b | c))


def green6_identity() -> dict:
    """G(2n+1, 2j..2j+5) equals green6; overlaps green4. n<64."""
    n_ok = 0
    for n in range(0, 64):
        m = 2 * n + 1
        for j in range(0, 2 * n + 1):
            gm = tuple(G(m, 2 * j + 5 - i) for i in range(6))
            g6 = green6(n, j)
            if gm != g6:
                return {"ok": False, "n": n, "j": j, "gm": gm, "g6": list(g6)}
            if g6[2:] != green4(n, j) or g6[:4] != green4(n, j + 1):
                return {"ok": False, "overlap": True, "n": n, "j": j}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def _walk_g6(k: int, q: int) -> dict:
    """green6 on even s; r30_4 and adjacent AND on odd s."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = xor_all = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            m = T - s - 1
            if m != 2 * n + 1:
                return {"ok": False, "m": True, "k": k, "s": s, "n": n, "m_got": m}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                gm = tuple(G(m, 2 * j + 5 - i) for i in range(6))
                if gm != green6(n, j):
                    return {
                        "ok": False,
                        "g6": True,
                        "k": k,
                        "s": s,
                        "n": n,
                        "j": j,
                    }
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
                otup = tuple(bit_at(row, p - 3 + i) for i in range(4))
                if r30_4(six) != otup:
                    return {
                        "ok": False,
                        "r30": True,
                        "k": k,
                        "s": s,
                        "n": n,
                        "j": j,
                    }
                u, v, z, a, b, c = six
                o = (Aodd >> p) & 1
                o1 = (Aodd >> (p - 2)) & 1 if p >= 2 else 0
                if and_from_tuple(z, a, b, c) != o:
                    return {"ok": False, "Aj": True, "k": k, "s": s, "p": p}
                if and_from_tuple(u, v, z, a) != o1:
                    return {"ok": False, "Aj1": True, "k": k, "s": s, "p": p}
                n_ok += 1
                if o and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_all": xor_all}


def g6_cover() -> dict:
    """green6 / r30_4 / adjacent AND on J6/J10, k<=6."""
    n_ok = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g6(k, q)
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
            krow[name] = {"n_ok": w["n_ok"], "xor_all": w["xor_all"]}
        rows[str(k)] = krow
    return {"ok": True, "n_ok": n_ok, "rows": rows}


def killed_six_eq_g6() -> dict:
    """Even-s 6-tuple is not green6: k=0, s=2, n=1, j=0."""
    k, s, n, j, p = 0, 2, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    six = tuple(bit_at(row, p - 5 + i) for i in range(6))
    g6 = green6(n, j)
    ok = six == (1, 0, 0, 1, 0, 0) and g6 == (1, 0, 1, 0, 1, 1) and six != g6
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
        "g6": list(g6),
    }


def killed_pair_eq_G() -> dict:
    """Adjacent AND pair is not (G(n,j+1), G(n,j)): k=0, s=3, n=1, j=1."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    u, v, z, a, b, c = six
    pair = (and_from_tuple(u, v, z, a), and_from_tuple(z, a, b, c))
    gpair = (G(n, j + 1), G(n, j))
    ok = pair == (0, 1) and gpair == (1, 1) and pair != gpair
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "pair": list(pair),
        "gpair": list(gpair),
    }


def killed_and_indep_adj() -> dict:
    """Adjacent AND is not independent: k=0, s=3, n=1, j=0, both live."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    row = 1
    for _ in range(s):
        prev = row
        row = rule30_step(row)
    six = tuple(bit_at(prev, p - 5 + i) for i in range(6))
    u, v, z, a, b, c = six
    pair = (and_from_tuple(u, v, z, a), and_from_tuple(z, a, b, c))
    ok = pair == (1, 1)
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "pair": list(pair),
    }


def prefixes() -> dict:
    hl = json.loads(HL_JSON.read_text())
    hj = json.loads(HJ_JSON.read_text())
    ok = (
        hl["checks"]["all_ok"]
        and hj["checks"]["all_ok"]
        and hl["verdict"]["odd_s_Green_4slot_eq_odd_green4"] == "LEMMA"
        and hj["verdict"]["even_s_Green_4slot_eq_green4"] == "LEMMA"
        and hl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gid: dict, gc: dict, ks: dict, kp: dict, ka: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gid["ok"] and gc["ok"] and ks["ok"] and kp["ok"] and ka["ok"] and pref["ok"]
    assert green6(1, 0)[2:] == green4(1, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gid = green6_identity()
    gc = g6_cover()
    ks = killed_six_eq_g6()
    kp = killed_pair_eq_G()
    ka = killed_and_indep_adj()
    pref = prefixes()
    checks = self_checks(c20, gid, gc, ks, kp, ka, pref)
    dump = {
        "cycle": "HM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green6_identity": {k: gid[k] for k in gid if k != "ok"},
        "g6_cover": {k: gc[k] for k in gc if k != "ok"},
        "killed_six_eq_g6": {k: ks[k] for k in ks if k != "ok"},
        "killed_pair_eq_G": {k: kp[k] for k in kp if k != "ok"},
        "killed_and_indep_adj": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "even_s_Green_6slot_eq_green6": True,
            "green6_overlaps_green4": True,
            "odd_s_4tuple_eq_r30_of_6tuple": True,
            "adjacent_AND_eq_overlapping_4tuples": True,
            "6tuple_eq_green6": False,
            "AND_pair_eq_G_pair": False,
            "adjacent_AND_independent": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_Green_6slot_eq_green6": "LEMMA",
            "green6_overlaps_green4": "LEMMA",
            "odd_s_4tuple_eq_r30_of_6tuple": "LEMMA",
            "adjacent_AND_eq_overlapping_4tuples": "LEMMA",
            "6tuple_eq_green6": "KILLED",
            "AND_pair_eq_G_pair": "KILLED",
            "adjacent_AND_independent": "KILLED",
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
    print("green6_identity n_ok", dump["green6_identity"]["n_ok"])
    print("g6_cover n_ok", dump["g6_cover"]["n_ok"])
    print("killed_six_eq_g6", dump["killed_six_eq_g6"])
    print("killed_pair_eq_G", dump["killed_pair_eq_G"])
    print("killed_and_indep_adj", dump["killed_and_indep_adj"])


if __name__ == "__main__":
    main()
