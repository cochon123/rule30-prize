#!/usr/bin/env python3
"""Cycle OW: covering even-parent rem is a partial R2 tail; xor=1 iff k>=6 and k%4==2.

Covering n=4p+1 in [0,4U) has p<2^k. Clip-active p starts at 5*2^{k-3}
(k>=3). Full R2 would need p>=5*2^{k-2}+1 > 2^k-1, so every covering
even-parent rem is r2_tail(p, 5*2^{k-2}-p+1). The left endpoint has
an empty tail. That xor is 1 iff k>=6 and k%4==2 on k<=10. Covering
n=8t+3 rem xor is 1 iff k>=2 even on k<=10. With Cycle OV, covering
rem recurses rem(k)=n3(k) xor rem(k-2) xor ep(k). Not rem for all k.
Not covering S for all k. Not E_k=0 for all k. Do not catalogue
further S/T subregions unless the experiment answers why E_k=0.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ow.py --certify
Dump: research/cycle_ow.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_os import even_parent_dmin, r2_tail
from cycle_ov import covering_rem_parts

OUT = Path(__file__).resolve().with_suffix(".json")
OV_JSON = Path(__file__).resolve().parent / "cycle_ov.json"
OU_JSON = Path(__file__).resolve().parent / "cycle_ou.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_PAL = 64
M_SLOTS = 64
K_COVER = 10


def want_ep_cover(k: int) -> int:
    """Covering even-parent rem xor on k<=10."""
    return int(k >= 6 and k % 4 == 2)


def want_n3_cover(k: int) -> int:
    """Covering n=8t+3 rem xor on k<=10."""
    return int(k >= 2 and k % 2 == 0)


def want_rem_cover(k: int) -> int:
    """Covering rem from n3, OV n7=rem(k-2), and ep."""
    if k < 2:
        return 0
    prev = [0, 0]
    for i in range(2, k + 1):
        prev.append(want_n3_cover(i) ^ prev[i - 2] ^ want_ep_cover(i))
    return prev[k]


def ep_shape() -> dict:
    """k=3..K_COVER: clip-active p is [5*2^{k-3}, 2^k); dmin=5*2^{k-2}-p+1; empty left."""
    n_ok = n_empty = 0
    sample = {}
    for k in range(3, K_COVER + 1):
        U = 1 << k
        jmax = 5 * U
        pmin = 5 << (k - 3)
        p_hi = U - 1
        p_full = (5 << (k - 2)) + 1
        n_clip = 0
        for p in range(0, U):
            n = 4 * p + 1
            active = 2 * n > jmax
            want_d = (5 << (k - 2)) - p + 1
            dmin = even_parent_dmin(p, jmax)
            if active:
                if p < pmin or p > p_hi:
                    return {"ok": False, "range": k, "p": p}
                if dmin != want_d:
                    return {"ok": False, "dmin": k, "p": p, "got": dmin, "want": want_d}
                if dmin <= 1:
                    return {"ok": False, "full": k, "p": p}
                n_clip += 1
                n_ok += 1
            elif p >= pmin:
                return {"ok": False, "inactive": k, "p": p}
        if n_clip != 3 << (k - 3):
            return {"ok": False, "count": k, "n_clip": n_clip}
        if p_full <= p_hi:
            return {"ok": False, "p_full": k, "p_full": p_full, "p_hi": p_hi}
        left = r2_tail(pmin, even_parent_dmin(pmin, jmax))
        if left != 0:
            return {"ok": False, "left": k, "left": left}
        n_empty += 1
        if k <= 6:
            sample[str(k)] = {"n_clip": n_clip, "pmin": pmin, "p_full": p_full, "p_hi": p_hi}
    ok = (
        n_ok > 0
        and n_empty == K_COVER - 2
        and sample["3"]["n_clip"] == 3
        and sample["6"]["n_clip"] == 24
        and sample["6"]["p_full"] > sample["6"]["p_hi"]
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_empty": n_empty,
        "k_lo": 3,
        "k_hi": K_COVER,
        "sample": sample,
    }


def rem_bits() -> dict:
    """k<=K_COVER: ep/n3 match wants; n7=tot(k-2); tot=n3 xor n7 xor ep = want_rem."""
    rows = {}
    n_ok = 0
    for k in range(0, K_COVER + 1):
        rows[str(k)] = covering_rem_parts(k)
    for k in range(0, K_COVER + 1):
        r = rows[str(k)]
        if r["ep"] != want_ep_cover(k):
            return {"ok": False, "ep": k, "got": r["ep"], "want": want_ep_cover(k)}
        if r["n3"] != want_n3_cover(k):
            return {"ok": False, "n3": k, "got": r["n3"], "want": want_n3_cover(k)}
        if r["even"] != 0 or r["recon"] != r["tot"]:
            return {"ok": False, "recon": k}
        if r["tot"] != want_rem_cover(k):
            return {"ok": False, "tot": k, "got": r["tot"], "want": want_rem_cover(k)}
        if k >= 2 and r["n7"] != rows[str(k - 2)]["tot"]:
            return {"ok": False, "n7": k, "got": r["n7"], "want": rows[str(k - 2)]["tot"]}
        n_ok += 1
    ok = (
        n_ok == K_COVER + 1
        and rows["6"]["ep"] == 1
        and rows["10"]["ep"] == 1
        and rows["8"]["ep"] == 0
        and rows["2"]["ep"] == 0
        and rows["10"]["tot"] == 1
        and want_rem_cover(2) == 1
        and want_rem_cover(8) == 1
        and want_rem_cover(10) == 1
    )
    slim = {
        str(k): {
            "tot": rows[str(k)]["tot"],
            "n3": rows[str(k)]["n3"],
            "n7": rows[str(k)]["n7"],
            "ep": rows[str(k)]["ep"],
            "want_tot": want_rem_cover(k),
        }
        for k in range(0, K_COVER + 1)
    }
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COVER, "rows": slim}


def killed_k2_mod4(bits: dict) -> dict:
    """k=2 is 2 mod 4 but ep rem xor is 0."""
    ok = bits["rows"]["2"]["ep"] == 0 and want_ep_cover(2) == 0 and (2 % 4 == 2)
    return {"ok": ok, "k": 2, "ep": bits["rows"]["2"]["ep"]}


def prefixes() -> dict:
    ov = json.loads(OV_JSON.read_text())
    ou = json.loads(OU_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        ov["checks"]["all_ok"]
        and ou["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and ov["verdict"]["n7_rec"] == "LEMMA"
        and ou["verdict"]["n3_rem"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and ov["verdict"]["covering_S"] == "PREFIX"
        and ov["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, shape, bits, k2, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and shape["ok"] and bits["ok"] and k2["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    shape = ep_shape()
    bits = rem_bits()
    k2 = killed_k2_mod4(bits)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, shape, bits, k2, sc, pref)
    dump = {
        "cycle": "OW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "ep_shape": {k: shape[k] for k in shape if k != "ok"},
        "rem_bits": {k: bits[k] for k in bits if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_k2_mod4": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "ep_shape": True,
            "n7_rec": True,
            "n3_rem": True,
            "ep_xor_all_k": False,
            "n3_xor_all_k": False,
            "covering_S": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ep_shape": "LEMMA",
            "n7_rec": "LEMMA",
            "n3_rem": "LEMMA",
            "ep_xor": "CERTIFIED",
            "n3_xor": "CERTIFIED",
            "rem_rec": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "k2_mod4": "KILLED",
            "ep_xor_all_k": "PREFIX",
            "n3_xor_all_k": "PREFIX",
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
    print("ep_shape n_ok", dump["ep_shape"]["n_ok"], "n_empty", dump["ep_shape"]["n_empty"])
    print("rem_bits", dump["rem_bits"]["rows"])
    print("killed_k2_mod4", dump["killed_k2_mod4"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
