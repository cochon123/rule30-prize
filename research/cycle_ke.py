#!/usr/bin/env python3
"""Cycle KE: each FRESH pattern on G=1 hits all four g1_green4 shapes.

Packed AND's shared FRESH terms 0010, 0100, 1001 each occur on
isolated ones, all three pair kinds, centers, and both n-parities.
FRESH is not only G=0; not only isolated; not a function of green4.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ke.py --certify
Dump: research/cycle_ke.json
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
from cycle_hi import FRESH
from cycle_hj import green4
from cycle_hu import and_clause
from cycle_ig import g1_green4
from cycle_in import g_run_kind
from cycle_ir import isolated_one
from cycle_kb import G1_SHAPES, KINDS, die_g4_table
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KD_JSON = Path(__file__).resolve().parent / "cycle_kd.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

FRESH_KEYS = tuple("".join(map(str, four)) for four in FRESH)
F0010 = (0, 0, 1, 0)

WANT = {
    "0010": {
        "n": 1014,
        "g0": 3828,
        "iso": 354,
        "ctr": 85,
        "even": 308,
        "odd": 706,
        "g4": {"0110": 253, "0111": 354, "1010": 117, "1011": 290},
        "kind": {"left": 123, "right": 117, "iso": 167},
    },
    "0100": {
        "n": 1280,
        "g0": 4335,
        "iso": 385,
        "ctr": 68,
        "even": 361,
        "odd": 919,
        "g4": {"0110": 361, "0111": 385, "1010": 193, "1011": 341},
        "kind": {"left": 127, "right": 193, "iso": 214},
    },
    "1001": {
        "n": 1082,
        "g0": 4507,
        "iso": 407,
        "ctr": 26,
        "even": 382,
        "odd": 700,
        "g4": {"0110": 344, "0111": 407, "1010": 73, "1011": 258},
        "kind": {"left": 92, "right": 73, "iso": 166},
    },
}


def _fmt(tup) -> str:
    return "".join(map(str, tup))


def _empty_pat() -> dict:
    return {
        "n": 0,
        "g0": 0,
        "iso": 0,
        "ctr": 0,
        "even": 0,
        "odd": 0,
        "g4": {sh: 0 for sh in G1_SHAPES},
        "kind": {kind: 0 for kind in KINDS},
    }


def _walk_fresh(k: int, q: int) -> dict:
    """G=1 FRESH census on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = xor_j = 0
    pats = {key: _empty_pat() for key in FRESH_KEYS}
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
                key = _fmt(four)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
                    if four in FRESH:
                        rec = pats[key]
                        rec["n"] += 1
                        rec["g4"][_fmt(green4(n, j))] += 1
                        if isolated_one(n, j):
                            rec["iso"] += 1
                        if j == n:
                            rec["ctr"] += 1
                        if n % 2 == 0:
                            rec["even"] += 1
                        else:
                            rec["odd"] += 1
                        if j < 2 * n:
                            kind = g_run_kind(n, j)
                            if kind is not None:
                                rec["kind"][kind] += 1
                elif four in FRESH:
                    pats[key]["g0"] += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "pats": pats,
        "xor_j": xor_j,
    }


def _add_pat(dst: dict, src: dict) -> None:
    dst["n"] += src["n"]
    dst["g0"] += src["g0"]
    dst["iso"] += src["iso"]
    dst["ctr"] += src["ctr"]
    dst["even"] += src["even"]
    dst["odd"] += src["odd"]
    for sh in G1_SHAPES:
        dst["g4"][sh] += src["g4"][sh]
    for kind in KINDS:
        dst["kind"][kind] += src["kind"][kind]


def _pat_ok(got: dict, want: dict) -> bool:
    return (
        got["n"] == want["n"]
        and got["g0"] == want["g0"]
        and got["iso"] == want["iso"]
        and got["ctr"] == want["ctr"]
        and got["even"] == want["even"]
        and got["odd"] == want["odd"]
        and got["n"] == got["even"] + got["odd"]
        and got["n"] == sum(got["g4"].values())
        and got["iso"] == got["g4"]["0111"]
        and got["kind"]["right"] == got["g4"]["1010"]
        and got["kind"]["left"] + got["kind"]["iso"] == got["g4"]["1011"]
        and all(got["g4"][sh] == want["g4"][sh] for sh in G1_SHAPES)
        and all(got["kind"][kind] == want["kind"][kind] for kind in KINDS)
        and all(got["g4"][sh] > 0 for sh in G1_SHAPES)
        and all(got["kind"][kind] > 0 for kind in KINDS)
    )


def fresh_g1_cover() -> dict:
    """G=1 FRESH census on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = 0
    pats = {key: _empty_pat() for key in FRESH_KEYS}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_fresh(k, q)
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
            for key in FRESH_KEYS:
                _add_pat(pats[key], w["pats"][key])
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_fresh": sum(w["pats"][key]["n"] for key in FRESH_KEYS),
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    n_fresh = sum(pats[key]["n"] for key in FRESH_KEYS)
    n_fresh_g0 = sum(pats[key]["g0"] for key in FRESH_KEYS)
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_fresh == 3376
        and n_fresh_g0 == 12670
        and all(_pat_ok(pats[key], WANT[key]) for key in FRESH_KEYS)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_fresh": n_fresh,
        "n_fresh_g0": n_fresh_g0,
        "pats": pats,
        "rows": rows,
    }


def _kill_four(k: int, s_hit: int, n_hit: int, j_hit: int, p_hit: int):
    row = 1
    prev = None
    for _ in range(s_hit):
        prev = row
        row = rule30_step(row)
    four = tuple(bit_at(prev, p_hit - 3 + i) for i in range(4))
    return k, s_hit, n_hit, j_hit, p_hit, four


def killed_only_g0() -> dict:
    """FRESH only on G=0: G(1,0) is 0010."""
    k, s, n, j, p, four = _kill_four(0, 7, 1, 0, 10)
    ok = (
        G(n, j) == 1
        and four == F0010
        and four in FRESH
        and green4(n, j) == g1_green4(n, j) == (1, 0, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(green4(n, j)),
    }


def killed_only_iso() -> dict:
    """FRESH only isolated: G(1,0) is left of a pair."""
    k, s, n, j, p, four = _kill_four(0, 7, 1, 0, 10)
    ok = (
        G(n, j) == 1
        and four == F0010
        and g_run_kind(n, j) == "left"
        and (not isolated_one(n, j))
        and green4(n, j) == (1, 0, 1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(green4(n, j)),
    }


def killed_fn_of_g4() -> dict:
    """FRESH is a function of green4: seed G(0,0) is 0010 vs 0111."""
    k, s, n, j, p, four = _kill_four(2, 39, 0, 0, 40)
    g4 = green4(n, j)
    ok = (
        isolated_one(n, j)
        and four == F0010
        and g4 == (0, 1, 1, 1)
        and four != g4
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "four": list(four),
        "g4": list(g4),
    }


def prefixes() -> dict:
    kd = json.loads(KD_JSON.read_text())
    ok = (
        kd["checks"]["all_ok"]
        and kd["verdict"]["cont_g1_all_shapes"] == "LEMMA"
        and kd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert FRESH == ((0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1))
    assert all(and_clause(*four) == 1 for four in FRESH)
    assert g1_green4(0, 0) == (0, 1, 1, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = die_g4_table()
    sc = fresh_g1_cover()
    k0 = killed_only_g0()
    k1 = killed_only_iso()
    k2 = killed_fn_of_g4()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "KE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "die_g4_table": {k: rt[k] for k in rt if k != "ok"},
        "fresh_g1_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_only_g0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_only_iso": {k: k1[k] for k in k1 if k != "ok"},
        "killed_fn_of_g4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "g1_four_shapes": True,
            "fresh_g1_all_shapes": True,
            "covering_fresh_g1": True,
            "only_g0": False,
            "only_iso": False,
            "fn_of_g4": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "g1_four_shapes": "LEMMA",
            "fresh_g1_all_shapes": "LEMMA",
            "covering_fresh_g1": "LEMMA",
            "only_g0": "KILLED",
            "only_iso": "KILLED",
            "fn_of_g4": "KILLED",
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
    print("die_g4_table", dump["die_g4_table"])
    cov = dump["fresh_g1_cover"]
    print(
        "fresh_g1_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_fresh",
        cov["n_fresh"],
        "n_fresh_g0",
        cov["n_fresh_g0"],
        "pats",
        {key: {k: cov["pats"][key][k] for k in ("n", "g0", "iso", "ctr", "g4", "kind")} for key in FRESH_KEYS},
    )
    print("killed_only_g0", dump["killed_only_g0"])
    print("killed_only_iso", dump["killed_only_iso"])
    print("killed_fn_of_g4", dump["killed_fn_of_g4"])


if __name__ == "__main__":
    main()
