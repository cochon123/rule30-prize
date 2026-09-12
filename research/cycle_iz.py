#!/usr/bin/env python3
"""Cycle IZ: consecutive G=1 green4 pair is determined by slot_kind.

KIND_GREEN4: left (1011,1010), right (1010,0110), iso (1011,0110).
Equals g11_green4 and the slot_green4 pair. Iso is not the left
shape; left second is not 0110; right first is not 1011. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_iz.py --certify
Dump: research/cycle_iz.json
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
from cycle_ij import g11_green4
from cycle_in import g_run_kind
from cycle_iv import slot_green4
from cycle_ix import slot_kind
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IY_JSON = Path(__file__).resolve().parent / "cycle_iy.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

KIND_GREEN4 = {
    "left": ((1, 0, 1, 1), (1, 0, 1, 0)),
    "right": ((1, 0, 1, 0), (0, 1, 1, 0)),
    "iso": ((1, 0, 1, 1), (0, 1, 1, 0)),
}


def kind_green4(n: int, j: int):
    """g11_green4 from slot_kind; None if no pair."""
    kind = slot_kind(n, j)
    if kind is None:
        return None
    return KIND_GREEN4[kind]


def _pair_key(pair) -> list:
    return [list(pair[0]), list(pair[1])]


def g4_table() -> dict:
    """n<64: g11_green4 equals KIND_GREEN4[slot_kind]."""
    n_g11 = n_left = n_right = n_iso = 0
    for n in range(0, 64):
        for j in range(0, 2 * n):
            kind = g_run_kind(n, j)
            pred = kind_green4(n, j)
            if kind is None:
                if pred is not None:
                    return {"ok": False, "extra": True, "n": n, "j": j}
                continue
            got = g11_green4(n, j)
            s0, s1 = slot_green4(n, j), slot_green4(n, j + 1)
            if pred != KIND_GREEN4[kind] or got != pred or (s0, s1) != pred:
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "kind": kind,
                    "got": got,
                    "pred": pred,
                }
            n_g11 += 1
            if kind == "left":
                n_left += 1
            elif kind == "right":
                n_right += 1
            else:
                n_iso += 1
    ok = n_g11 == 512 and n_left == 141 and n_right == 141 and n_iso == 230
    return {
        "ok": ok,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
    }


def _walk_g4(k: int, q: int) -> dict:
    """Kind green4 on covering consecutive G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
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
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                pred = kind_green4(n, j)
                if kind is None:
                    if pred is not None:
                        return {"ok": False, "extra": True, "k": k, "n": n, "j": j}
                    continue
                got = g11_green4(n, j)
                if pred != KIND_GREEN4[kind] or got != pred:
                    return {
                        "ok": False,
                        "miss": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "kind": kind,
                    }
                n_g11 += 1
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
        "xor_j": xor_j,
    }


def g4_cover() -> dict:
    """Kind green4 on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_left = n_right = n_iso = 0
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
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_left": w["n_left"],
                "n_right": w["n_right"],
                "n_iso": w["n_iso"],
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
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_left": n_left,
        "n_right": n_right,
        "n_iso": n_iso,
        "rows": rows,
    }


def killed_iso_is_left() -> dict:
    """Iso has the left green4: G(3,0) is (1011, 0110)."""
    k, s, n, j, p = 1, 5, 3, 0, 12
    got = g11_green4(n, j)
    ok = (
        g_run_kind(n, j) == "iso"
        and got == KIND_GREEN4["iso"]
        and got != KIND_GREEN4["left"]
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "iso",
        "green4": _pair_key(got),
    }


def killed_left_second_0110() -> dict:
    """Left second is 0110: G(1,0) second is 1010."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    got = g11_green4(n, j)
    ok = (
        g_run_kind(n, j) == "left"
        and got == KIND_GREEN4["left"]
        and got[1] != (0, 1, 1, 0)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "left",
        "green4": _pair_key(got),
    }


def killed_right_first_1011() -> dict:
    """Right first is 1011: G(1,1) first is 1010."""
    k, s, n, j, p = 1, 9, 1, 1, 10
    got = g11_green4(n, j)
    ok = (
        g_run_kind(n, j) == "right"
        and got == KIND_GREEN4["right"]
        and got[0] != (1, 0, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "kind": "right",
        "green4": _pair_key(got),
    }


def prefixes() -> dict:
    iy = json.loads(IY_JSON.read_text())
    ok = (
        iy["checks"]["all_ok"]
        and iy["verdict"]["dual_pair_kind"] == "LEMMA"
        and iy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert kind_green4(1, 0) == KIND_GREEN4["left"]
    assert kind_green4(1, 1) == KIND_GREEN4["right"]
    assert kind_green4(3, 0) == KIND_GREEN4["iso"]
    assert kind_green4(2, 0) is None
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = g4_table()
    sc = g4_cover()
    k0 = killed_iso_is_left()
    k1 = killed_left_second_0110()
    k2 = killed_right_first_1011()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "g4_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_iso_is_left": {k: k0[k] for k in k0 if k != "ok"},
        "killed_left_second_0110": {k: k1[k] for k in k1 if k != "ok"},
        "killed_right_first_1011": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "kind_green4": True,
            "kind_green4_shapes": True,
            "covering_kind_green4": True,
            "iso_is_left_g4": False,
            "left_second_0110": False,
            "right_first_1011": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "kind_green4": "LEMMA",
            "kind_green4_shapes": "LEMMA",
            "covering_kind_green4": "LEMMA",
            "iso_is_left_g4": "KILLED",
            "left_second_0110": "KILLED",
            "right_first_1011": "KILLED",
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
    print("g4_table", dump["g4_table"])
    cov = dump["g4_cover"]
    print(
        "g4_cover n_ok",
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
    print("killed_iso_is_left", dump["killed_iso_is_left"])
    print("killed_left_second_0110", dump["killed_left_second_0110"])
    print("killed_right_first_1011", dump["killed_right_first_1011"])


if __name__ == "__main__":
    main()
