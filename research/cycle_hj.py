#!/usr/bin/env python3
"""Cycle HJ: fresh AND occupies even-s Green copy/cob slots.

On covering (n,j), even-s Green at packed bits p-3..p is
(G(n,j+1), cob(j+1), G(n,j), cob(j)). Fresh 0010 occupies only
copy(j); 0100 only cob(j+1); 1001 occupies copy(j+1) and cob(j).
The 4-tuple is not that Green 4-tuple; 0010 is not only on G=1;
0100 is not only on cob(j+1)=1. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hj.py --certify
Dump: research/cycle_hj.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HI_JSON = Path(__file__).resolve().parent / "cycle_hi.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

# Even-s Green slots at packed bits (p-3, p-2, p-1, p).
SLOT_NAMES = ("copy_jp1", "cob_jp1", "copy_j", "cob_j")
FRESH_SLOT = {
    (0, 0, 1, 0): "copy_j",
    (0, 1, 0, 0): "cob_jp1",
    (1, 0, 0, 1): "copy_jp1+cob_j",
}


def green4(n: int, j: int) -> tuple[int, int, int, int]:
    """Even-s Green at p-3..p on covering (n,j)."""
    gj = G(n, j)
    gj1 = G(n, j + 1)
    return (gj1, gj1 ^ gj, gj, gj ^ G(n, j - 1))


def slot_mask(tup: tuple[int, int, int, int]) -> str:
    parts = [name for name, bit in zip(SLOT_NAMES, tup) if bit]
    return "+".join(parts) if parts else "empty"


def green4_identity() -> dict:
    """G(2n+1, 2j..2j+3) equals green4(n,j). n<64."""
    n_ok = 0
    for n in range(0, 64):
        m = 2 * n + 1
        for j in range(0, 2 * n + 1):
            gm = (
                G(m, 2 * j + 3),
                G(m, 2 * j + 2),
                G(m, 2 * j + 1),
                G(m, 2 * j),
            )
            if gm != green4(n, j):
                return {"ok": False, "n": n, "j": j, "gm": gm, "g4": list(green4(n, j))}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def fresh_slots() -> dict:
    """AND_ONES occupy the named copy/cob slots."""
    got = {t: slot_mask(t) for t in AND_ONES}
    want = {
        (0, 0, 1, 0): "copy_j",
        (0, 0, 1, 1): "copy_j+cob_j",
        (0, 1, 0, 0): "cob_jp1",
        (1, 0, 0, 1): "copy_jp1+cob_j",
    }
    ok = got == want and FRESH_SLOT[(0, 0, 1, 0)] == "copy_j"
    ok = ok and all(t in AND_ONES for t in FRESH) and CONT in AND_ONES
    return {
        "ok": ok,
        "slots": {str(t): got[t] for t in AND_ONES},
    }


def _walk_g4(k: int, q: int) -> dict:
    """Even-s Green 4-slot on covering (n,j); odd-s XOR on G=1."""
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
                gm = (
                    G(m, 2 * j + 3),
                    G(m, 2 * j + 2),
                    G(m, 2 * j + 1),
                    G(m, 2 * j),
                )
                if gm != green4(n, j):
                    return {
                        "ok": False,
                        "g4": True,
                        "k": k,
                        "s": s,
                        "n": n,
                        "j": j,
                        "gm": gm,
                        "g4v": list(green4(n, j)),
                    }
                n_ok += 1
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            Aodd = (row << 1) & row
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                if ((Aodd >> p) & 1) and G(n, j):
                    xor_all ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "xor_all": xor_all}


def g4_cover() -> dict:
    """Green 4-slot on J6/J10, k<=6; odd-s XOR matches HF/HG."""
    n_ok = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_g4(k, q)
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


def killed_tup_eq_g4() -> dict:
    """Even-s 4-tuple is not the Green 4-tuple: k=0, s=2, n=1, j=0."""
    k, s, n, j, p = 0, 2, 1, 0, 6
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    tup = (
        bit_at(row, p - 3),
        bit_at(row, p - 2),
        bit_at(row, p - 1),
        bit_at(row, p),
    )
    g4 = green4(n, j)
    ok = tup == (0, 1, 0, 0) and g4 == (1, 0, 1, 1) and tup != g4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "g4": list(g4),
    }


def killed_0010_only_g1() -> dict:
    """Fresh 0010 is not only on G(n,j)=1: k=1, s=7, n=2, j=1."""
    k, s, n, j, p = 1, 7, 2, 1, 10
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
    o = (Aodd >> p) & 1
    g = G(n, j)
    ok = tup == (0, 0, 1, 0) and o == 1 and g == 0
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "o": o,
        "G": g,
    }


def killed_0100_only_cob1() -> dict:
    """Fresh 0100 is not only on cob(j+1)=1: k=0, s=3, n=1, j=0."""
    k, s, n, j, p = 0, 3, 1, 0, 6
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
    o = (Aodd >> p) & 1
    cob1 = G(n, j + 1) ^ G(n, j)
    ok = tup == (0, 1, 0, 0) and o == 1 and cob1 == 0 and G(n, j) == 1
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "tup": list(tup),
        "o": o,
        "cob1": cob1,
        "G": G(n, j),
    }


def prefixes() -> dict:
    hi = json.loads(HI_JSON.read_text())
    ok = (
        hi["checks"]["all_ok"]
        and hi["verdict"]["odd_s_AND_eq_even_s_4tuple"] == "LEMMA"
        and hi["verdict"]["fresh_iff_0010_or_0100_or_1001"] == "LEMMA"
        and hi["verdict"]["continuation_iff_0011"] == "LEMMA"
        and hi["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gid: dict, fs: dict, gc: dict, kt: dict, k0: dict, k1: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gid["ok"] and fs["ok"] and gc["ok"] and kt["ok"] and k0["ok"] and k1["ok"] and pref["ok"]
    assert FRESH_SLOT[(0, 0, 1, 0)] == "copy_j"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gid = green4_identity()
    fs = fresh_slots()
    gc = g4_cover()
    kt = killed_tup_eq_g4()
    k0 = killed_0010_only_g1()
    k1 = killed_0100_only_cob1()
    pref = prefixes()
    checks = self_checks(c20, gid, fs, gc, kt, k0, k1, pref)
    dump = {
        "cycle": "HJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green4_identity": {k: gid[k] for k in gid if k != "ok"},
        "fresh_slots": {k: fs[k] for k in fs if k != "ok"},
        "g4_cover": {k: gc[k] for k in gc if k != "ok"},
        "killed_tup_eq_g4": {k: kt[k] for k in kt if k != "ok"},
        "killed_0010_only_g1": {k: k0[k] for k in k0 if k != "ok"},
        "killed_0100_only_cob1": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "even_s_Green_4slot_eq_green4": True,
            "fresh_0010_occupies_copy_j": True,
            "fresh_0100_occupies_cob_jp1": True,
            "fresh_1001_occupies_copy_jp1_and_cob_j": True,
            "4tuple_eq_Green_4tuple": False,
            "0010_only_on_G_eq_1": False,
            "0100_only_on_cob_jp1_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_Green_4slot_eq_green4": "LEMMA",
            "fresh_0010_occupies_copy_j": "LEMMA",
            "fresh_0100_occupies_cob_jp1": "LEMMA",
            "fresh_1001_occupies_copy_jp1_and_cob_j": "LEMMA",
            "4tuple_eq_Green_4tuple": "KILLED",
            "0010_only_on_G_eq_1": "KILLED",
            "0100_only_on_cob_jp1_eq_1": "KILLED",
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
    print("green4_identity n_ok", dump["green4_identity"]["n_ok"])
    print("g4_cover n_ok", dump["g4_cover"]["n_ok"])
    print("killed_tup_eq_g4", dump["killed_tup_eq_g4"])
    print("killed_0010_only_g1", dump["killed_0010_only_g1"])
    print("killed_0100_only_cob1", dump["killed_0100_only_cob1"])


if __name__ == "__main__":
    main()
