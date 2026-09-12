#!/usr/bin/env python3
"""Cycle IX: consecutive G=1 kind is the core-slot IMAGE_ONES offset.

On odd n, g_run_kind is SLOT_KIND[r,d]: r=1 d=0 left, d=1 right;
r=2 d=0/3 and r=3 d=0/5 iso. Even n and non-pairs are None.
r=1 d=1 is not left; r=2 is not a triple; even n has no slot_kind.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_ix.py --certify
Dump: research/cycle_ix.json
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
from cycle_in import g_run_kind
from cycle_it import g1_core_slot
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IW_JSON = Path(__file__).resolve().parent / "cycle_iw.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

SLOT_KIND = {
    (1, 0): "left",
    (1, 1): "right",
    (2, 0): "iso",
    (2, 3): "iso",
    (3, 0): "iso",
    (3, 5): "iso",
}

WANT_ALG = {
    (1, 0): 141,
    (1, 1): 141,
    (2, 0): 70,
    (2, 3): 70,
    (3, 0): 45,
    (3, 5): 45,
}

WANT_COV = {
    (1, 0): 2380,
    (1, 1): 2380,
    (2, 0): 1171,
    (2, 3): 1168,
    (3, 0): 741,
    (3, 5): 737,
}


def slot_kind(n: int, j: int):
    """g_run_kind from the core slot offset; None if no pair."""
    if n % 2 == 0:
        return None
    got = g1_core_slot(n, j)
    if got is None or got == "seed" or got == "bad":
        return None
    _start, r, d = got
    return SLOT_KIND.get((r, d))


def _kind_key(slots: dict) -> dict:
    return {f"{r},{d}": slots[(r, d)] for r, d in sorted(WANT_ALG)}


def kind_table() -> dict:
    """n<64: g_run_kind equals slot_kind; census matches SLOT_KIND."""
    n_g11 = 0
    slots = {k: 0 for k in WANT_ALG}
    n_left = n_right = n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = slot_kind(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j, "pred": pred}
                continue
            if pred != kind:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "pred": pred,
                }
            n_g11 += 1
            _start, r, d = g1_core_slot(n, j)
            slots[(r, d)] += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
    ok = (
        n_g11 == 512
        and n_left == 141
        and n_right == 141
        and n_iso == 230
        and slots == WANT_ALG
    )
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "slots": _kind_key(slots),
    }


def _walk_kind(k: int, q: int) -> dict:
    """Slot kind on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
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
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j) and packed:
                    xor_j ^= 1
                if G(n, j):
                    n_g1 += 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                pred = slot_kind(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                if pred != kind:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                        "pred": pred,
                    }
                n_g11 += 1
                _start, r, d = g1_core_slot(n, j)
                slots[(r, d)] += 1
                if kind == "left":
                    n_left += 1
                elif kind == "right":
                    n_right += 1
                else:
                    n_iso += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "slots": _kind_key(slots),
        "xor_j": xor_j,
        "_slots": slots,
    }


def kind_cover() -> dict:
    """Slot kind on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
    slots = {k: 0 for k in WANT_ALG}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_kind(k, q)
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
            n_g11 += w["n_g11"]
            n_left += w["n_left"]
            n_right += w["n_right"]
            n_iso += w["n_iso"]
            for key in slots:
                slots[key] += w["_slots"][key]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso": w["n_iso"],
                "slots": w["slots"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_left == 2380
        and n_right == 2380
        and n_iso == 3817
        and slots == WANT_COV
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "slots": _kind_key(slots),
        "rows": rows,
    }


def killed_r1d1_left() -> dict:
    """r=1 d=1 is left: G(1,1) is right of the triple."""
    k, s, n, j, p = 0, 3, 1, 1, 4
    got = g1_core_slot(n, j)
    kind = g_run_kind(n, j)
    ok = got == (0, 1, 1) and kind == "right" and slot_kind(n, j) == "right" and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "kind": kind,
    }


def killed_r2_triple() -> dict:
    """r=2 is a triple: G(7,0) is an isolated pair."""
    k, s, n, j, p = 2, 9, 7, 0, 24
    got = g1_core_slot(n, j)
    kind = g_run_kind(n, j)
    ok = got == (0, 2, 0) and kind == "iso" and slot_kind(n, j) == "iso" and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "kind": kind,
    }


def killed_even_kind() -> dict:
    """Even n has a slot_kind: G(2,0) is None."""
    k, s, n, j, p = 1, 7, 2, 0, 12
    ok = (
        n % 2 == 0
        and G(n, j) == 1
        and g_run_kind(n, j) is None
        and slot_kind(n, j) is None
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(g1_core_slot(n, j)),
        "kind": g_run_kind(n, j),
    }


def prefixes() -> dict:
    iw = json.loads(IW_JSON.read_text())
    ok = (
        iw["checks"]["all_ok"]
        and iw["verdict"]["center_core_slot"] == "LEMMA"
        and iw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert slot_kind(1, 0) == "left"
    assert slot_kind(1, 1) == "right"
    assert slot_kind(3, 0) == "iso"
    assert slot_kind(2, 0) is None
    assert slot_kind(3, 3) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = kind_table()
    sc = kind_cover()
    k0 = killed_r1d1_left()
    k1 = killed_r2_triple()
    k2 = killed_even_kind()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "kind_table": {k: rt[k] for k in rt if k != "ok"},
        "kind_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_r1d1_left": {k: k0[k] for k in k0 if k != "ok"},
        "killed_r2_triple": {k: k1[k] for k in k1 if k != "ok"},
        "killed_even_kind": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "slot_kind": True,
            "slot_kind_partition": True,
            "covering_slot_kind": True,
            "r1d1_is_left": False,
            "r2_is_triple": False,
            "even_has_slot_kind": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "slot_kind": "LEMMA",
            "slot_kind_partition": "LEMMA",
            "covering_slot_kind": "LEMMA",
            "r1d1_is_left": "KILLED",
            "r2_is_triple": "KILLED",
            "even_has_slot_kind": "KILLED",
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
    print("kind_table", dump["kind_table"])
    cov = dump["kind_cover"]
    print(
        "kind_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_g11",
        cov["n_g11"],
        "n_left",
        cov["n_left"],
        "n_right",
        cov["n_right"],
        "n_iso",
        cov["n_iso"],
    )
    print("killed_r1d1_left", dump["killed_r1d1_left"])
    print("killed_r2_triple", dump["killed_r2_triple"])
    print("killed_even_kind", dump["killed_even_kind"])


if __name__ == "__main__":
    main()
