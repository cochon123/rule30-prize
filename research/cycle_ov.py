#!/usr/bin/env python3
"""Cycle OV: covering n=8t+7 rem xor at k equals covering rem at k-2.

Cycle OT folds rem(8t+7, 5*2^k) to rem(2t+1, 5*2^{k-2}). Covering
n=8t+7 in [0,4U) is t=0..2^{k-1}-1, so 2t+1 runs through every
odd integer below 2^k. Covering at k-2 is n in [0,2^k) at the
same jmax=5*2^{k-2}. Even-n rem vanishes, and an unclipped child
has an unclipped parent, so the covering n=8t+7 rem xor at k is
the covering rem xor at k-2. Checked k=2..8. Not one step
(k=3: n7=0, tot(2)=1). Not covering S for all k. Not E_k=0 for
all k. Do not catalogue further S/T subregions unless the
experiment answers why E_k=0. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_ov.py --certify
Dump: research/cycle_ov.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_or import want_cover_s_e0, want_unclip_cover
from cycle_os import removed_s

OUT = Path(__file__).resolve().with_suffix(".json")
OU_JSON = Path(__file__).resolve().parent / "cycle_ou.json"
OT_JSON = Path(__file__).resolve().parent / "cycle_ot.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
K_COVER = 8


def covering_rem_parts(k: int) -> dict:
    """q=10 covering clip-removed S xor, split by n%8."""
    U = 1 << k
    T, t0, Q = 10 * U, 2 * U, covering_Q(10)
    jmax = T // 2
    tot = n3 = n7 = ep = even = 0
    n_n7 = 0
    tclk = 0
    sclk = t0 + 1
    while sclk < T:
        n = odd_clock(tclk, U, Q)
        r = removed_s(n, jmax)
        tot ^= r
        if n % 2 == 0:
            even ^= r
        elif n % 8 == 3:
            n3 ^= r
        elif n % 8 == 7:
            n7 ^= r
            n_n7 += 1
        elif n % 4 == 1:
            ep ^= r
        tclk += 1
        sclk += 2
    return {
        "tot": tot,
        "n3": n3,
        "n7": n7,
        "ep": ep,
        "even": even,
        "n_n7": n_n7,
        "recon": n3 ^ n7 ^ ep ^ even,
    }


def n7_rec() -> dict:
    """k=2..K_COVER: covering n7 rem xor equals tot rem at k-2."""
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        rows[str(k)] = covering_rem_parts(k)
    for k in range(2, K_COVER + 1):
        got = rows[str(k)]["n7"]
        want = rows[str(k - 2)]["tot"]
        if got != want:
            return {"ok": False, "k": k, "got": got, "want": want}
        if rows[str(k)]["even"] != 0:
            return {"ok": False, "even": k, "even_xor": rows[str(k)]["even"]}
        if rows[str(k)]["recon"] != rows[str(k)]["tot"]:
            return {"ok": False, "recon": k}
        n_ok += 1
    s = want_unclip_cover(K_COVER) ^ rows[str(K_COVER)]["tot"]
    ok = (
        n_ok == K_COVER - 1
        and rows["2"]["n7"] == 0
        and rows["4"]["n7"] == 1
        and rows["2"]["tot"] == 1
        and rows["0"]["tot"] == 0
        and rows["4"]["n7"] == rows["2"]["tot"]
        and s == want_cover_s_e0(K_COVER)
    )
    slim = {
        str(k): {
            "tot": rows[str(k)]["tot"],
            "n3": rows[str(k)]["n3"],
            "n7": rows[str(k)]["n7"],
            "ep": rows[str(k)]["ep"],
            "n_n7": rows[str(k)]["n_n7"],
        }
        for k in range(0, K_COVER + 1)
    }
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": slim}


def n7_index() -> dict:
    """k>=2: covering n=8t+7 gives every odd parent below 2^k."""
    n_ok = 0
    sample = {}
    for k in range(2, K_COVER + 1):
        odds = set()
        U = 1 << k
        for t in range(1 << (k - 1)):
            n = 8 * t + 7
            if n >= 4 * U:
                return {"ok": False, "k": k, "n": n}
            odds.add(2 * t + 1)
        want = set(range(1, 1 << k, 2))
        if odds != want:
            return {"ok": False, "k": k, "missing": sorted(want - odds)[:4]}
        n_ok += 1
        if k <= 4:
            sample[str(k)] = {"n_odd": len(odds), "hi": (1 << k) - 1}
    ok = n_ok == K_COVER - 1 and sample["2"]["n_odd"] == 2 and sample["2"]["hi"] == 3
    return {"ok": ok, "n_ok": n_ok, "sample": sample}


def killed_one_step(rec: dict) -> dict:
    """k=3: n7 rem xor is 0, tot at k=2 is 1."""
    n7 = rec["rows"]["3"]["n7"]
    tot2 = rec["rows"]["2"]["tot"]
    ok = n7 == 0 and tot2 == 1
    return {"ok": ok, "n7_k3": n7, "tot_k2": tot2}


def prefixes() -> dict:
    ou = json.loads(OU_JSON.read_text())
    ot = json.loads(OT_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        ou["checks"]["all_ok"]
        and ot["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and ou["verdict"]["n3_rem"] == "LEMMA"
        and ot["verdict"]["n7_clip_fold"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and ou["verdict"]["covering_S"] == "PREFIX"
        and ou["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, rec, idx, ko, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and rec["ok"] and idx["ok"] and ko["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    rec = n7_rec()
    idx = n7_index()
    ko = killed_one_step(rec)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, rec, idx, ko, sc, pref)
    dump = {
        "cycle": "OV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "n7_rec": {k: rec[k] for k in rec if k != "ok"},
        "n7_index": {k: idx[k] for k in idx if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_one_step": {k: ko[k] for k in ko if k != "ok"},
        "lemmas": {
            "n7_rec": True,
            "n7_index": True,
            "n7_clip_fold": True,
            "n3_rem": True,
            "one_step": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n7_rec": "LEMMA",
            "n7_index": "LEMMA",
            "n7_clip_fold": "LEMMA",
            "n3_rem": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "one_step": "KILLED",
            "covering_S": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("n7_rec n_ok", dump["n7_rec"]["n_ok"])
    print("n7_rec rows", dump["n7_rec"]["rows"])
    print("killed_one_step", dump["killed_one_step"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
