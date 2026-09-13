#!/usr/bin/env python3
"""Cycle MC: rest8 dies at k=10 q=10.

On covering J6,J10, Cycle MB's rest8 holds at k=10 q=6 but dies
at k=10 q=10: rest=0 while want_rest8=1 (10%4==2), so J=1 while
want_j8=0. want_forced still holds at k=10. Not rest8 for all k;
not want_j8 for all k; not a fail at k=10 q=6; not want_forced
dying at k=10. Do not claim J6=J10=0 implies J18=1 for all k; do
not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_mc.py --certify
Dump: research/cycle_mc.json
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
from cycle_mb import want_j8, want_rest8

OUT = Path(__file__).resolve().with_suffix(".json")
MB_JSON = Path(__file__).resolve().parent / "cycle_mb.json"

# Probe-checked k=10 covering walk sizes (q=6 ~6.3s, q=10 ~26.8s).
WANT_WALK = {
    (10, 6): {"n_ok": 3932672, "n_g1": 436770, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
    (10, 10): {"n_ok": 14419456, "n_g1": 1266210, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
}


def _pack(k: int, q: int) -> dict:
    """Walk covering rest at (k,q) and attach want_*."""
    w = _walk_rest(k, q)
    w["wr"] = want_rest(k, q)
    w["wr8"] = want_rest8(k, q)
    w["wf"] = want_forced(k, q)
    w["wj"] = want_j(k, q)
    w["wj8"] = want_j8(k, q)
    return w


def _row_ok(k: int, q: int, w: dict, *, match_rest8: bool) -> bool:
    """True if walk sizes match the probe and rest8 match/mismatch is as claimed."""
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
    if match_rest8:
        return size and w["xor_rest"] == w["wr8"] and w["xor_j"] == w["wj8"]
    return size and w["xor_rest"] != w["wr8"] and w["xor_j"] != w["wj8"]


def k10_kill() -> dict:
    """rest8 dies at k=10 q=10; still holds at q=6; want_forced holds."""
    rows = {}
    n_ok = n_g1 = 0
    for q, name in ((6, "j6"), (10, "j10")):
        w = _pack(10, q)
        match = q == 6
        if not _row_ok(10, q, w, match_rest8=match):
            return {
                "ok": False,
                "k": 10,
                "q": q,
                "xor_j": w.get("xor_j"),
                "xor_f": w.get("xor_f"),
                "xor_rest": w.get("xor_rest"),
                "wj8": w.get("wj8"),
                "wf": w.get("wf"),
                "wr8": w.get("wr8"),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[name] = {
            "xor_j": w["xor_j"],
            "xor_f": w["xor_f"],
            "xor_rest": w["xor_rest"],
            "wj8": w["wj8"],
            "wj": w["wj"],
            "wf": w["wf"],
            "wr8": w["wr8"],
            "wr": w["wr"],
        }
    ok = (
        rows["j6"]["xor_rest"] == 0
        and rows["j10"]["xor_rest"] == 0
        and rows["j10"]["wr8"] == 1
        and rows["j10"]["xor_j"] == 1
        and rows["j10"]["wj8"] == 0
        and rows["j10"]["wr"] == 1
        and rows["j10"]["wj"] == 0
        and rows["j6"]["xor_j"] == 1
        and want_forced(10, 6) == 1
        and want_forced(10, 10) == 1
        and want_rest8(10, 10) == 1
        and want_j8(10, 10) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_rest8_all(k10: dict) -> dict:
    """rest8 for all k: k=10 q=10 has rest=0, want_rest8=1."""
    r = k10["rows"]["j10"]
    ok = r["xor_rest"] == 0 and r["wr8"] == 1
    return {"ok": ok, "k": 10, "q": 10, "rest": r["xor_rest"], "wr8": r["wr8"]}


def killed_j8_all(k10: dict) -> dict:
    """want_j8 for all k: k=10 q=10 has J=1, want_j8=0."""
    r = k10["rows"]["j10"]
    ok = r["xor_j"] == 1 and r["wj8"] == 0
    return {"ok": ok, "k": 10, "q": 10, "xor_j": r["xor_j"], "wj8": r["wj8"]}


def killed_q6_fail(k10: dict) -> dict:
    """rest8 fails at k=10 q=6: it holds."""
    r = k10["rows"]["j6"]
    ok = r["xor_rest"] == 0 and r["wr8"] == 0 and r["xor_j"] == r["wj8"]
    return {"ok": ok, "k": 10, "q": 6, "rest": r["xor_rest"], "xor_j": r["xor_j"]}


def killed_forced10(k10: dict) -> dict:
    """want_forced dies at k=10: it holds (both q)."""
    ok = (
        k10["rows"]["j6"]["xor_f"] == want_forced(10, 6)
        and k10["rows"]["j10"]["xor_f"] == want_forced(10, 10)
        and want_forced(10, 6) == 1
        and want_forced(10, 10) == 1
    )
    return {
        "ok": ok,
        "k": 10,
        "f6": k10["rows"]["j6"]["xor_f"],
        "f10": k10["rows"]["j10"]["xor_f"],
    }


def prefixes() -> dict:
    mb = json.loads(MB_JSON.read_text())
    ok = (
        mb["checks"]["all_ok"]
        and mb["verdict"]["rest8"] == "LEMMA"
        and mb["verdict"]["k9_holds"] == "LEMMA"
        and mb["verdict"]["ge8"] == "KILLED"
        and mb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    k10: dict,
    sc: dict,
    kr8: dict,
    kj8: dict,
    kq6: dict,
    kforced: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        k10["ok"]
        and sc["ok"]
        and kr8["ok"]
        and kj8["ok"]
        and kq6["ok"]
        and kforced["ok"]
        and pref["ok"]
    )
    assert want_rest8(10, 6) == 0 and want_rest8(10, 10) == 1
    assert want_j8(10, 6) == 1 and want_j8(10, 10) == 0
    assert want_rest(10, 10) == 1 and want_j(10, 10) == 0
    assert k10["rows"]["j10"]["xor_rest"] == 0
    assert k10["rows"]["j10"]["xor_j"] == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    k10 = k10_kill()
    sc = g4_xor_cover()
    kr8 = killed_rest8_all(k10)
    kj8 = killed_j8_all(k10)
    kq6 = killed_q6_fail(k10)
    kforced = killed_forced10(k10)
    pref = prefixes()
    checks = self_checks(c20, k10, sc, kr8, kj8, kq6, kforced, pref)
    dump = {
        "cycle": "MC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "k10_kill": {k: k10[k] for k in k10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_rest8_all": {k: kr8[k] for k in kr8 if k != "ok"},
        "killed_j8_all": {k: kj8[k] for k in kj8 if k != "ok"},
        "killed_q6_fail": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_forced10": {k: kforced[k] for k in kforced if k != "ok"},
        "lemmas": {
            "k10_kill": True,
            "forced10": True,
            "q6_rest0": True,
            "rest8": True,
            "k9_holds": True,
            "forced9": True,
            "k7_holds": True,
            "forced8": True,
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "rest8_all": False,
            "j8_all": False,
            "q6_fail": False,
            "forced10_die": False,
            "ge8": False,
            "from8": False,
            "all_k": False,
            "rest_all_k": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "k10_kill": "KILLED",
            "forced10": "LEMMA",
            "q6_rest0": "LEMMA",
            "rest8": "LEMMA",
            "k9_holds": "LEMMA",
            "forced9": "LEMMA",
            "k7_holds": "LEMMA",
            "forced8": "LEMMA",
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "rest8_all": "KILLED",
            "j8_all": "KILLED",
            "q6_fail": "KILLED",
            "forced10_die": "KILLED",
            "ge8": "KILLED",
            "from8": "KILLED",
            "all_k": "KILLED",
            "rest_all_k": "KILLED",
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
    print("k10_kill n_ok", dump["k10_kill"]["n_ok"], "n_g1", dump["k10_kill"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_rest8_all", dump["killed_rest8_all"])
    print("killed_j8_all", dump["killed_j8_all"])
    print("killed_q6_fail", dump["killed_q6_fail"])
    print("killed_forced10", dump["killed_forced10"])


if __name__ == "__main__":
    main()
