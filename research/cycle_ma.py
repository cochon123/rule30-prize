#!/usr/bin/env python3
"""Cycle MA: LZ J form holds at k=7 and dies at k=8 q=10.

On covering J6,J10, Cycle LZ's want_j holds at k=7 (both q) and at
k=8 q=6, but dies at k=8 q=10: J=0 while want_j=1 because rest=1
while want_rest=0 (8%4 is 0, not 2). want_forced still holds at
k=8. Not the form for all k; not rest formula for all k; not a
fail at k=7; not want_forced dying at k=8. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ma.py --certify
Dump: research/cycle_ma.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_lz import _walk_rest, want_forced, want_j, want_rest

OUT = Path(__file__).resolve().with_suffix(".json")
LZ_JSON = Path(__file__).resolve().parent / "cycle_lz.json"

# Probe-checked covering walk sizes (authoritative; k=7 ~0.34s, k=8 ~1.45s).
WANT_WALK = {
    (7, 6): {"n_ok": 61504, "n_g1": 12920, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
    (7, 10): {"n_ok": 225472, "n_g1": 37496, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
    (8, 6): {"n_ok": 245888, "n_g1": 41762, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
    (8, 10): {"n_ok": 901504, "n_g1": 121122, "xor_j": 0, "xor_f": 1, "xor_rest": 1},
}


def _pack(k: int, q: int) -> dict:
    """Walk covering rest at (k,q) and attach want_*."""
    w = _walk_rest(k, q)
    w["wr"] = want_rest(k, q)
    w["wf"] = want_forced(k, q)
    w["wj"] = want_j(k, q)
    return w


def _row_ok(k: int, q: int, w: dict, *, match_form: bool) -> bool:
    """True if walk sizes match the probe and form match/mismatch is as claimed."""
    want = WANT_WALK[(k, q)]
    size = (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["xor_j"] == want["xor_j"]
        and w["xor_f"] == want["xor_f"]
        and w["xor_rest"] == want["xor_rest"]
        and w["xor_j"] == w["xor_f"] ^ w["xor_rest"]
        and w["xor_f"] == w["wf"]
    )
    if match_form:
        return size and w["xor_j"] == w["wj"] and w["xor_rest"] == w["wr"]
    return size and w["xor_j"] != w["wj"] and w["xor_rest"] != w["wr"]


def k7_holds() -> dict:
    """LZ form holds at k=7 for both covering q."""
    rows = {}
    n_ok = n_g1 = 0
    for q, name in ((6, "j6"), (10, "j10")):
        w = _pack(7, q)
        if not _row_ok(7, q, w, match_form=True):
            return {
                "ok": False,
                "k": 7,
                "q": q,
                "xor_j": w.get("xor_j"),
                "xor_f": w.get("xor_f"),
                "xor_rest": w.get("xor_rest"),
                "wj": w.get("wj"),
                "wf": w.get("wf"),
                "wr": w.get("wr"),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[name] = {
            "xor_j": w["xor_j"],
            "xor_f": w["xor_f"],
            "xor_rest": w["xor_rest"],
        }
    return {"ok": True, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def k8_kill() -> dict:
    """LZ form dies at k=8 q=10; still holds at q=6; want_forced holds."""
    rows = {}
    n_ok = n_g1 = 0
    for q, name in ((6, "j6"), (10, "j10")):
        w = _pack(8, q)
        match = q == 6
        if not _row_ok(8, q, w, match_form=match):
            return {
                "ok": False,
                "k": 8,
                "q": q,
                "xor_j": w.get("xor_j"),
                "xor_f": w.get("xor_f"),
                "xor_rest": w.get("xor_rest"),
                "wj": w.get("wj"),
                "wf": w.get("wf"),
                "wr": w.get("wr"),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[name] = {
            "xor_j": w["xor_j"],
            "xor_f": w["xor_f"],
            "xor_rest": w["xor_rest"],
            "wj": w["wj"],
            "wf": w["wf"],
            "wr": w["wr"],
        }
    ok = (
        rows["j6"]["xor_j"] == 1
        and rows["j10"]["xor_j"] == 0
        and rows["j10"]["xor_rest"] == 1
        and rows["j10"]["wj"] == 1
        and rows["j10"]["wr"] == 0
        and rows["j10"]["xor_f"] == 1
        and want_j(8, 10) == 1
        and want_rest(8, 10) == 0
        and want_forced(8, 10) == 1
        and want_forced(8, 6) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_all_k(k8: dict) -> dict:
    """form for all k: k=8 q=10 has J=0, want_j=1."""
    r = k8["rows"]["j10"]
    ok = r["xor_j"] == 0 and r["wj"] == 1
    return {"ok": ok, "k": 8, "q": 10, "xor_j": r["xor_j"], "wj": r["wj"]}


def killed_rest_all(k8: dict) -> dict:
    """rest formula for all k: rest=1, want_rest=0 at k=8 q=10."""
    r = k8["rows"]["j10"]
    ok = r["xor_rest"] == 1 and r["wr"] == 0
    return {"ok": ok, "k": 8, "q": 10, "rest": r["xor_rest"], "wr": r["wr"]}


def killed_k7_fail(k7: dict) -> dict:
    """form fails at k=7: it holds (both q)."""
    ok = (
        k7["ok"]
        and k7["rows"]["j6"]["xor_j"] == want_j(7, 6)
        and k7["rows"]["j10"]["xor_j"] == want_j(7, 10)
    )
    return {
        "ok": ok,
        "k": 7,
        "j6": k7["rows"]["j6"]["xor_j"],
        "j10": k7["rows"]["j10"]["xor_j"],
    }


def killed_forced8(k8: dict) -> dict:
    """want_forced dies at k=8: it holds (both q)."""
    ok = (
        k8["rows"]["j6"]["xor_f"] == want_forced(8, 6)
        and k8["rows"]["j10"]["xor_f"] == want_forced(8, 10)
        and want_forced(8, 6) == 1
        and want_forced(8, 10) == 1
    )
    return {
        "ok": ok,
        "k": 8,
        "f6": k8["rows"]["j6"]["xor_f"],
        "f10": k8["rows"]["j10"]["xor_f"],
    }


def prefixes() -> dict:
    lz = json.loads(LZ_JSON.read_text())
    ok = (
        lz["checks"]["all_ok"]
        and lz["verdict"]["j_form"] == "LEMMA"
        and lz["verdict"]["rest_q10"] == "LEMMA"
        and lz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    k7: dict,
    k8: dict,
    sc: dict,
    ka: dict,
    kr: dict,
    kf: dict,
    kforced: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        k7["ok"]
        and k8["ok"]
        and sc["ok"]
        and ka["ok"]
        and kr["ok"]
        and kf["ok"]
        and kforced["ok"]
        and pref["ok"]
    )
    assert want_j(7, 6) == 1 and want_j(7, 10) == 1
    assert want_j(8, 6) == 1 and want_j(8, 10) == 1
    assert want_rest(8, 10) == 0
    assert k8["rows"]["j6"]["xor_j"] == 1
    assert k8["rows"]["j10"]["xor_j"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    k7 = k7_holds()
    k8 = k8_kill()
    sc = g4_xor_cover()
    ka = killed_all_k(k8)
    kr = killed_rest_all(k8)
    kf = killed_k7_fail(k7)
    kforced = killed_forced8(k8)
    pref = prefixes()
    checks = self_checks(c20, k7, k8, sc, ka, kr, kf, kforced, pref)
    dump = {
        "cycle": "MA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "k7_holds": {k: k7[k] for k in k7 if k != "ok"},
        "k8_kill": {k: k8[k] for k in k8 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_all_k": {k: ka[k] for k in ka if k != "ok"},
        "killed_rest_all": {k: kr[k] for k in kr if k != "ok"},
        "killed_k7_fail": {k: kf[k] for k in kf if k != "ok"},
        "killed_forced8": {k: kforced[k] for k in kforced if k != "ok"},
        "lemmas": {
            "k7_holds": True,
            "k8_kill": True,
            "forced8": True,
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "p114_0100": True,
            "p76_0011": True,
            "p86_0011": True,
            "p58_0011": True,
            "p88_0100": True,
            "p72_1001": True,
            "p42_0011": True,
            "p38_0100": True,
            "p52_1001": True,
            "p60_0100": True,
            "p30_0011": True,
            "p98_0010": True,
            "p106_1001": True,
            "p54_0100": True,
            "p32_0100": True,
            "p16_1001": True,
            "p14_0011": True,
            "p6_0100": True,
            "p4_1001": True,
            "pat1001_rem": True,
            "all_k": False,
            "rest_all_k": False,
            "k7_fail": False,
            "forced8_die": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "k7_holds": "LEMMA",
            "k8_kill": "KILLED",
            "forced8": "LEMMA",
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "p114_0100": "LEMMA",
            "p76_0011": "LEMMA",
            "p86_0011": "LEMMA",
            "p58_0011": "LEMMA",
            "p88_0100": "LEMMA",
            "p72_1001": "LEMMA",
            "p42_0011": "LEMMA",
            "p38_0100": "LEMMA",
            "p52_1001": "LEMMA",
            "p60_0100": "LEMMA",
            "p30_0011": "LEMMA",
            "p98_0010": "LEMMA",
            "p106_1001": "LEMMA",
            "p54_0100": "LEMMA",
            "p32_0100": "LEMMA",
            "p16_1001": "LEMMA",
            "p14_0011": "LEMMA",
            "p6_0100": "LEMMA",
            "p4_1001": "LEMMA",
            "pat1001_rem": "LEMMA",
            "all_k": "KILLED",
            "rest_all_k": "KILLED",
            "k7_fail": "KILLED",
            "forced8_die": "KILLED",
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
    print("k7_holds n_ok", dump["k7_holds"]["n_ok"], "n_g1", dump["k7_holds"]["n_g1"])
    print("k8_kill n_ok", dump["k8_kill"]["n_ok"], "n_g1", dump["k8_kill"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_all_k", dump["killed_all_k"])
    print("killed_rest_all", dump["killed_rest_all"])
    print("killed_k7_fail", dump["killed_k7_fail"])
    print("killed_forced8", dump["killed_forced8"])


if __name__ == "__main__":
    main()
