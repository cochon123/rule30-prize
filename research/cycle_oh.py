#!/usr/bin/env python3
"""Cycle OH: dyadic T-band xor of G(j-1) vanishes for 3<=k<=11.

Palindrome-right xor of G(n,j-1) on G=1 for n in [2^{k-1}, 2^k)
is 1 iff k in {1,2}, through k<=11 (no packed row, no covering
clip). This is the increment T_{k} = xor of bands i<k on covering
n<U/2, so it is why the T piece of E_k is 1 iff k=2 on the
certified range; do not claim T is 1 iff k=2 for all k. Not 0 at
k=1 (n_t=1); not 0 at k=2 (xor=1, n_t=3); not empty at k=11
(n_t=164352); not pointwise 0 (k=11 n_fire=62976); not rest; not
S; not the band vanish for all k. Do not walk k=12 T-bands. Do
not catalogue further S/T subregions unless the experiment
answers why E_k=0. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_oh.py --certify
Dump: research/cycle_oh.json
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
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10

OUT = Path(__file__).resolve().with_suffix(".json")
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"

WANT = {
    0: {"xor": 0, "n_t": 0, "n_fire": 0},
    1: {"xor": 1, "n_t": 1, "n_fire": 1},
    2: {"xor": 1, "n_t": 3, "n_fire": 1},
    3: {"xor": 0, "n_t": 12, "n_fire": 6},
    4: {"xor": 0, "n_t": 40, "n_fire": 16},
    5: {"xor": 0, "n_t": 136, "n_fire": 56},
    6: {"xor": 0, "n_t": 448, "n_fire": 176},
    7: {"xor": 0, "n_t": 1472, "n_fire": 576},
    8: {"xor": 0, "n_t": 4800, "n_fire": 1856},
    9: {"xor": 0, "n_t": 15616, "n_fire": 6016},
    10: {"xor": 0, "n_t": 50688, "n_fire": 19456},
    11: {"xor": 0, "n_t": 164352, "n_fire": 62976},
}


def want_t_band(k: int) -> int:
    """Dyadic T-band on n in [2^{k-1}, 2^k): 1 iff k in {1, 2}, k<=11."""
    return int(k in (1, 2))


def _band_t(k: int) -> dict:
    """Pal-right G=1 xor of G(j-1) for n in [2^{k-1}, 2^k). Unclipped."""
    lo = 0 if k == 0 else 1 << (k - 1)
    hi = 1 << k
    xor_t = n_t = n_fire = 0
    for n in range(lo, hi):
        for j in range(n + 1, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_t += 1
            b = G(n, j - 1)
            xor_t ^= b
            n_fire += b
    return {"ok": True, "xor": xor_t, "n_t": n_t, "n_fire": n_fire, "lo": lo, "hi": hi}


def t_bands_11() -> dict:
    """k<=11: band xor = want_t_band; k>=3 vanishes; covering Tcum = 1 iff k==2."""
    rows = {}
    n_t = n_fire = 0
    for k in range(0, 12):
        w = _band_t(k)
        pk = WANT[k]
        wh = want_t_band(k)
        if (
            w["xor"] != pk["xor"] == wh
            or w["n_t"] != pk["n_t"]
            or w["n_fire"] != pk["n_fire"]
        ):
            return {"ok": False, "k": k, "xor": w["xor"]}
        n_t += w["n_t"]
        n_fire += w["n_fire"]
        rows[str(k)] = {
            "xor": w["xor"],
            "want": wh,
            "n_t": w["n_t"],
            "n_fire": w["n_fire"],
            "lo": w["lo"],
            "hi": w["hi"],
        }
    acc = 0
    for k in range(0, 12):
        rows[str(k)]["cover_T"] = acc
        acc ^= rows[str(k)]["xor"]
        rows[str(k)]["tcum"] = acc
    ok = (
        all(rows[str(k)]["xor"] == want_t_band(k) for k in range(0, 12))
        and all(rows[str(k)]["xor"] == 0 for k in range(3, 12))
        and rows["1"]["n_t"] == 1
        and rows["1"]["xor"] == 1
        and rows["2"]["xor"] == 1
        and rows["2"]["n_t"] == 3
        and rows["11"]["n_t"] == 164352
        and rows["11"]["n_fire"] == 62976
        and all(rows[str(k)]["cover_T"] == int(k == 2) for k in range(0, 12))
        and want_t_band(1) == 1
        and want_t_band(3) == 0
        and n_t == 237568
        and n_fire == 91136
    )
    return {"ok": ok, "n_t": n_t, "n_fire": n_fire, "rows": rows}


def killed_b1(bands: dict) -> dict:
    r = bands["rows"]["1"]
    ok = r["xor"] == 1 and r["n_t"] == 1
    return {"ok": ok, "k": 1, "xor": r["xor"], "n_t": r["n_t"]}


def killed_b2(bands: dict) -> dict:
    r = bands["rows"]["2"]
    ok = r["xor"] == 1 and r["n_t"] == 3
    return {"ok": ok, "k": 2, "xor": r["xor"], "n_t": r["n_t"]}


def killed_empty(bands: dict) -> dict:
    r = bands["rows"]["11"]
    ok = r["n_t"] == 164352
    return {"ok": ok, "k": 11, "n_t": r["n_t"]}


def killed_pointwise(bands: dict) -> dict:
    r = bands["rows"]["11"]
    ok = r["n_fire"] == 62976 and r["xor"] == 0
    return {"ok": ok, "k": 11, "n_fire": r["n_fire"]}


def killed_eq_rest(bands: dict) -> dict:
    r = bands["rows"]["1"]
    ok = r["xor"] == 1 and want_rest10(1, 10) == 0
    return {"ok": ok, "k": 1, "xor": r["xor"], "rest": 0}


def killed_eq_s(bands: dict) -> dict:
    r = bands["rows"]["2"]
    ok = r["xor"] == 1
    return {"ok": ok, "k": 2, "xor": r["xor"], "note": "S covering k=2 is 0"}


def prefixes() -> dict:
    og = json.loads(OG_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    ok = (
        og["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and og["verdict"]["prize"] == "unsolved"
        and want_t_band(2) == 1
        and want_t_band(11) == 0
    )
    return {"ok": ok}


def self_checks(c20, bands: dict, kb1, kb2, kemp, kpw, kr, ks, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        bands["ok"]
        and kb1["ok"]
        and kb2["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kr["ok"]
        and ks["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert bands["n_t"] == 237568
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    bands = t_bands_11()
    kb1 = killed_b1(bands)
    kb2 = killed_b2(bands)
    kemp = killed_empty(bands)
    kpw = killed_pointwise(bands)
    kr = killed_eq_rest(bands)
    ks = killed_eq_s(bands)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, bands, kb1, kb2, kemp, kpw, kr, ks, sc, pref)
    dump = {
        "cycle": "OH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "t_bands_11": {k: bands[k] for k in bands if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_b1": {k: kb1[k] for k in kb1 if k != "ok"},
        "killed_b2": {k: kb2[k] for k in kb2 if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "lemmas": {
            "t_band_ge3": True,
            "E_q10_10": True,
            "b1_zero": False,
            "b2_zero": False,
            "empty": False,
            "pointwise": False,
            "eq_rest": False,
            "eq_s": False,
            "all_k": False,
            "T_iff_k2_all_k": False,
            "prize": False,
        },
        "verdict": {
            "t_band_ge3": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "b1_zero": "KILLED",
            "b2_zero": "KILLED",
            "empty": "KILLED",
            "pointwise": "KILLED",
            "eq_rest": "KILLED",
            "eq_s": "KILLED",
            "all_k": "KILLED",
            "T_iff_k2_all_k": "PREFIX",
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
        "t_bands_11 n_t",
        dump["t_bands_11"]["n_t"],
        "n_fire",
        dump["t_bands_11"]["n_fire"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_b1", dump["killed_b1"])
    print("killed_b2", dump["killed_b2"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_s", dump["killed_eq_s"])


if __name__ == "__main__":
    main()
