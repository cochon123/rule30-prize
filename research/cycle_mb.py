#!/usr/bin/env python3
"""Cycle MB: covering rest through k<=9 is a rest8 form.

On covering J6,J10, AND xor off {4,6,14} is 1 iff q==10 and
(k%4==2 or (k>0 and k%8==0)) for k<=9. That fits the Cycle MA
k=8 q=10 kill (8%8==0) and restores J=want_forced xor rest8 at
k=9. Not rest=1 once k>=8 (k=9 q=10 is 0); not the form dead
for all k>=8; not rest8 for all k; not want_forced dying at k=9.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mb.py --certify
Dump: research/cycle_mb.json
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
MA_JSON = Path(__file__).resolve().parent / "cycle_ma.json"

# Probe-checked k=9 covering walk sizes (q=6 ~1.38s, q=10 ~4.98s).
WANT_WALK = {
    (9, 6): {"n_ok": 983296, "n_g1": 135032, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
    (9, 10): {"n_ok": 3605248, "n_g1": 391544, "xor_j": 1, "xor_f": 1, "xor_rest": 0},
}


def want_rest8(k: int, q: int) -> int:
    """AND xor off {4,6,14} on k<=9: 1 iff q==10 and (k%4==2 or k>0 and k%8==0)."""
    return int(q == 10 and (k % 4 == 2 or (k > 0 and k % 8 == 0)))


def want_j8(k: int, q: int) -> int:
    """Covering odd-s J on k<=9 via rest8."""
    return want_forced(k, q) ^ want_rest8(k, q)


def want_rest_ge8(k: int, q: int) -> int:
    """Killed: rest=1 iff q==10 and (k%4==2 or k>=8)."""
    return int(q == 10 and (k % 4 == 2 or k >= 8))


def _pack(k: int, q: int) -> dict:
    """Walk covering rest at (k,q) and attach want_*."""
    w = _walk_rest(k, q)
    w["wr"] = want_rest(k, q)
    w["wr8"] = want_rest8(k, q)
    w["wf"] = want_forced(k, q)
    w["wj"] = want_j(k, q)
    w["wj8"] = want_j8(k, q)
    return w


def _row_ok(k: int, q: int, w: dict) -> bool:
    """True if walk sizes match the probe and rest8 holds."""
    want = WANT_WALK[(k, q)]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["xor_j"] == want["xor_j"]
        and w["xor_f"] == want["xor_f"]
        and w["xor_rest"] == want["xor_rest"]
        and w["xor_j"] == w["xor_f"] ^ w["xor_rest"]
        and w["xor_f"] == w["wf"]
        and w["xor_rest"] == w["wr8"]
        and w["xor_j"] == w["wj8"]
    )


def rest8_prefix() -> dict:
    """k<=8: dumped rest XOR equals want_rest8 (no re-walk)."""
    lz = json.loads(LZ_JSON.read_text())
    ma = json.loads(MA_JSON.read_text())
    rows = {}
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            got = lz["j_form"]["rows"][str(k)][name]["xor_rest"]
            wr8 = want_rest8(k, q)
            if got != wr8 or wr8 != want_rest(k, q):
                return {"ok": False, "k": k, "q": q, "got": got, "wr8": wr8}
            krow[name] = {"xor_rest": got, "wr8": wr8}
        rows[str(k)] = krow
    for k, key in ((7, "k7_holds"), (8, "k8_kill")):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            row = ma[key]["rows"][name]
            got = row["xor_rest"]
            wr8 = want_rest8(k, q)
            wj8 = want_j8(k, q)
            if got != wr8 or row["xor_j"] != wj8 or row["xor_f"] != want_forced(k, q):
                return {
                    "ok": False,
                    "k": k,
                    "q": q,
                    "got": got,
                    "wr8": wr8,
                    "xor_j": row["xor_j"],
                    "wj8": wj8,
                }
            krow[name] = {
                "xor_rest": got,
                "wr8": wr8,
                "xor_j": row["xor_j"],
                "wj8": wj8,
            }
        rows[str(k)] = krow
    ok = (
        want_rest8(8, 10) == 1
        and want_rest(8, 10) == 0
        and want_j8(8, 10) == 0
        and want_j(8, 10) == 1
        and want_rest8(0, 10) == 0
        and want_rest8(2, 10) == 1
        and want_rest8(6, 10) == 1
        and rows["8"]["j6"]["xor_rest"] == 0
    )
    return {"ok": ok, "rows": rows}


def k9_holds() -> dict:
    """rest8 and want_forced hold at k=9 for both covering q."""
    rows = {}
    n_ok = n_g1 = 0
    for q, name in ((6, "j6"), (10, "j10")):
        w = _pack(9, q)
        if not _row_ok(9, q, w):
            return {
                "ok": False,
                "k": 9,
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
            "wf": w["wf"],
            "wr8": w["wr8"],
            "wr": w["wr"],
            "ge8": want_rest_ge8(9, q),
        }
    ok = (
        rows["j6"]["xor_rest"] == 0
        and rows["j10"]["xor_rest"] == 0
        and rows["j10"]["ge8"] == 1
        and rows["j10"]["wr"] == 0
        and want_j8(9, 6) == 1
        and want_j8(9, 10) == 1
        and want_forced(9, 6) == 1
        and want_forced(9, 10) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_ge8(k9: dict) -> dict:
    """rest=1 once k>=8: k=9 q=10 has rest=0, ge8=1."""
    r = k9["rows"]["j10"]
    ok = r["xor_rest"] == 0 and r["ge8"] == 1
    return {"ok": ok, "k": 9, "q": 10, "rest": r["xor_rest"], "ge8": r["ge8"]}


def killed_from8(k9: dict) -> dict:
    """form dead for all k>=8: k=9 both q match want_j8."""
    ok = (
        k9["rows"]["j6"]["xor_j"] == want_j8(9, 6)
        and k9["rows"]["j10"]["xor_j"] == want_j8(9, 10)
        and want_j8(9, 6) == 1
        and want_j8(9, 10) == 1
    )
    return {
        "ok": ok,
        "k": 9,
        "j6": k9["rows"]["j6"]["xor_j"],
        "j10": k9["rows"]["j10"]["xor_j"],
    }


def killed_rest8_k9(k9: dict) -> dict:
    """rest8 fails at k=9: it holds (both q)."""
    ok = (
        k9["rows"]["j6"]["xor_rest"] == want_rest8(9, 6)
        and k9["rows"]["j10"]["xor_rest"] == want_rest8(9, 10)
    )
    return {
        "ok": ok,
        "k": 9,
        "r6": k9["rows"]["j6"]["xor_rest"],
        "r10": k9["rows"]["j10"]["xor_rest"],
    }


def killed_forced9(k9: dict) -> dict:
    """want_forced dies at k=9: it holds (both q)."""
    ok = (
        k9["rows"]["j6"]["xor_f"] == want_forced(9, 6)
        and k9["rows"]["j10"]["xor_f"] == want_forced(9, 10)
        and want_forced(9, 6) == 1
        and want_forced(9, 10) == 1
    )
    return {
        "ok": ok,
        "k": 9,
        "f6": k9["rows"]["j6"]["xor_f"],
        "f10": k9["rows"]["j10"]["xor_f"],
    }


def prefixes() -> dict:
    lz = json.loads(LZ_JSON.read_text())
    ma = json.loads(MA_JSON.read_text())
    ok = (
        lz["checks"]["all_ok"]
        and lz["verdict"]["j_form"] == "LEMMA"
        and ma["checks"]["all_ok"]
        and ma["verdict"]["k7_holds"] == "LEMMA"
        and ma["verdict"]["all_k"] == "KILLED"
        and ma["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    pref8: dict,
    k9: dict,
    sc: dict,
    kge: dict,
    kfrom: dict,
    kr8: dict,
    kforced: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pref8["ok"]
        and k9["ok"]
        and sc["ok"]
        and kge["ok"]
        and kfrom["ok"]
        and kr8["ok"]
        and kforced["ok"]
        and pref["ok"]
    )
    assert want_rest8(8, 10) == 1 and want_rest(8, 10) == 0
    assert want_rest8(9, 10) == 0 and want_rest_ge8(9, 10) == 1
    assert want_j8(8, 10) == 0 and want_j(8, 10) == 1
    assert want_j8(9, 10) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pref8 = rest8_prefix()
    k9 = k9_holds()
    sc = g4_xor_cover()
    kge = killed_ge8(k9)
    kfrom = killed_from8(k9)
    kr8 = killed_rest8_k9(k9)
    kforced = killed_forced9(k9)
    pref = prefixes()
    checks = self_checks(c20, pref8, k9, sc, kge, kfrom, kr8, kforced, pref)
    dump = {
        "cycle": "MB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "rest8_prefix": {k: pref8[k] for k in pref8 if k != "ok"},
        "k9_holds": {k: k9[k] for k in k9 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_ge8": {k: kge[k] for k in kge if k != "ok"},
        "killed_from8": {k: kfrom[k] for k in kfrom if k != "ok"},
        "killed_rest8_k9": {k: kr8[k] for k in kr8 if k != "ok"},
        "killed_forced9": {k: kforced[k] for k in kforced if k != "ok"},
        "lemmas": {
            "rest8": True,
            "k9_holds": True,
            "forced9": True,
            "k7_holds": True,
            "k8_kill": True,
            "forced8": True,
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "ge8": False,
            "from8": False,
            "rest8_k9_fail": False,
            "forced9_die": False,
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
            "rest8": "LEMMA",
            "k9_holds": "LEMMA",
            "forced9": "LEMMA",
            "k7_holds": "LEMMA",
            "k8_kill": "KILLED",
            "forced8": "LEMMA",
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "ge8": "KILLED",
            "from8": "KILLED",
            "rest8_k9_fail": "KILLED",
            "forced9_die": "KILLED",
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
    print("k9_holds n_ok", dump["k9_holds"]["n_ok"], "n_g1", dump["k9_holds"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_ge8", dump["killed_ge8"])
    print("killed_from8", dump["killed_from8"])
    print("killed_rest8_k9", dump["killed_rest8_k9"])
    print("killed_forced9", dump["killed_forced9"])


if __name__ == "__main__":
    main()
