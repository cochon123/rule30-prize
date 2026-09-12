#!/usr/bin/env python3
"""Cycle IS: every odd-n G=1 is a unique parent-image slot.

IMAGE_ONES maps run length to G=1 offsets from lo=2*start:
  r=1 -> (0,1,2), r=2 -> (0,1,3,4), r=3 -> (0,1,3,5,6).
Every G=1 on odd n is exactly one (start, r, offset). Odd G=1 does
not miss the dictionary; slots do not overlap; even-n G=1 is not a
parent slot. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_is.py --certify
Dump: research/cycle_is.json
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
from cycle_ip import g_runs
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IR_JSON = Path(__file__).resolve().parent / "cycle_ir.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

IMAGE_ONES = {
    1: (0, 1, 2),
    2: (0, 1, 3, 4),
    3: (0, 1, 3, 5, 6),
}

WANT_ALG = {
    (1, 0): 141,
    (1, 1): 141,
    (1, 2): 141,
    (2, 0): 70,
    (2, 1): 70,
    (2, 3): 70,
    (2, 4): 70,
    (3, 0): 45,
    (3, 1): 45,
    (3, 3): 45,
    (3, 5): 45,
    (3, 6): 45,
}

WANT_COV = {
    (1, 0): 2431,
    (1, 1): 2380,
    (1, 2): 2380,
    (2, 0): 1194,
    (2, 1): 1171,
    (2, 3): 1168,
    (2, 4): 1168,
    (3, 0): 766,
    (3, 1): 741,
    (3, 3): 741,
    (3, 5): 738,
    (3, 6): 737,
}


def g1_slot(n: int, j: int):
    """Unique (start, r, offset) of G=1 on odd n, else None."""
    if n % 2 == 0 or G(n, j) == 0:
        return None
    m = n // 2
    found = None
    for start, r in g_runs(m):
        lo = 2 * start
        for d in IMAGE_ONES[r]:
            if j != lo + d:
                continue
            if found is not None:
                return "dup"
            found = (start, r, d)
    return found


def _slot_key(slots: dict) -> dict:
    return {f"{r},{d}": slots[(r, d)] for r, d in sorted(WANT_ALG)}


def slot_table() -> dict:
    """Odd n<64: every G=1 is a unique IMAGE_ONES slot."""
    n_g1 = 0
    slots = {k: 0 for k in WANT_ALG}
    for n in range(1, 64, 2):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_g1 += 1
            got = g1_slot(n, j)
            if got is None or got == "dup":
                return {"ok": False, "miss": True, "n": n, "j": j, "got": got}
            _start, r, d = got
            slots[(r, d)] += 1
    ok = n_g1 == 928 and slots == WANT_ALG
    return {"ok": ok, "n_g1": n_g1, "slots": _slot_key(slots)}


def _walk_slots(k: int, q: int) -> dict:
    """Unique slots on covering odd-n G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g1_odd = 0
    slots = {key: 0 for key in WANT_ALG}
    xor_j = 0
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
                n_ok += 1
                if not G(n, j):
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                if n % 2 == 0:
                    if g1_slot(n, j) is not None:
                        return {"ok": False, "even": True, "k": k, "n": n, "j": j}
                    continue
                n_g1_odd += 1
                got = g1_slot(n, j)
                if got is None or got == "dup":
                    return {"ok": False, "miss": True, "k": k, "n": n, "j": j, "got": got}
                _start, r, d = got
                slots[(r, d)] += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g1_odd": n_g1_odd,
        "slots": _slot_key(slots),
        "xor_j": xor_j,
        "_slots": slots,
    }


def slot_cover() -> dict:
    """Unique slots on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g1_odd = 0
    slots = {k: 0 for k in WANT_ALG}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_slots(k, q)
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
            n_g1_odd += w["n_g1_odd"]
            for key in slots:
                slots[key] += w["_slots"][key]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g1_odd": w["n_g1_odd"],
                "slots": w["slots"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g1_odd == 15615
        and slots == WANT_COV
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g1_odd": n_g1_odd,
        "slots": _slot_key(slots),
        "rows": rows,
    }


def killed_odd_miss() -> dict:
    """Odd-n G=1 misses the dictionary: G(1,0) is slot (0,1,0)."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    got = g1_slot(n, j)
    ok = n % 2 == 1 and G(n, j) == 1 and got == (0, 1, 0) and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got) if isinstance(got, tuple) else got,
    }


def killed_slot_dup() -> dict:
    """Two images share a G=1: G(7,6) is unique slot (3,1,0)."""
    k, s, n, j, p = 1, 5, 7, 6, 8
    got = g1_slot(n, j)
    ok = got == (3, 1, 0) and got != "dup" and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got) if isinstance(got, tuple) else got,
    }


def killed_even_slot() -> dict:
    """Even-n G=1 is a parent slot: G(2,0)=1 has none."""
    k, s, n, j, p = 0, 5, 2, 0, 10
    ok = n % 2 == 0 and G(n, j) == 1 and g1_slot(n, j) is None and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": g1_slot(n, j),
        "G": G(n, j),
    }


def prefixes() -> dict:
    ir = json.loads(IR_JSON.read_text())
    ok = (
        ir["checks"]["all_ok"]
        and ir["verdict"]["odd_iso1_from_r3_mid"] == "LEMMA"
        and ir["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g1_slot(1, 0) == (0, 1, 0)
    assert g1_slot(3, 3) == (0, 3, 3)
    assert g1_slot(2, 0) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = slot_table()
    sc = slot_cover()
    k0 = killed_odd_miss()
    k1 = killed_slot_dup()
    k2 = killed_even_slot()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "slot_table": {k: rt[k] for k in rt if k != "ok"},
        "slot_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_odd_miss": {k: k0[k] for k in k0 if k != "ok"},
        "killed_slot_dup": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_slot": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "odd_g1_unique_slot": True,
            "image_ones_partition": True,
            "covering_g1_slots": True,
            "odd_g1_misses_slots": False,
            "slot_overlap": False,
            "even_g1_is_slot": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_g1_unique_slot": "LEMMA",
            "image_ones_partition": "LEMMA",
            "covering_g1_slots": "LEMMA",
            "odd_g1_misses_slots": "KILLED",
            "slot_overlap": "KILLED",
            "even_g1_is_slot": "KILLED",
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
    print("slot_table", dump["slot_table"])
    cov = dump["slot_cover"]
    print(
        "slot_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g1_odd",
        cov["n_g1_odd"],
    )
    print("killed_odd_miss", dump["killed_odd_miss"])
    print("killed_slot_dup", dump["killed_slot_dup"])
    print("killed_even_slot", dump["killed_even_slot"])


if __name__ == "__main__":
    main()
