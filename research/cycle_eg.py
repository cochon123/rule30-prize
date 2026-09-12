#!/usr/bin/env python3
"""Cycle EG: even-52809 leaves no later odd in its k=15 landing.

Every length-8 T0 in Cycle DM's even-52809 family (16 words, including
prize 00000110 and all eight FAM372 unfolds) has first ident-0 extra
52809 even. From k=8 that extra lands in annulus k=15. The next odd
extra is 87468 on six words (remaining 34659) and none in 131000 on
the other ten (remaining >78191), both strictly larger than 2^15.
Worst-case leftover in k=15 is 2^15=32768<34659, so a later odd cannot
fit in that high half. The six 87468 words land in k=16, which is
threshold(34659); 2^16=65536>34659 so they can fit there. Kills:
leftover after even 52809 empty at every later k; next odd after 52809
forced before k=16. Do not claim a closed form for 34659/87468; do not
equate scar 87468 with packed 87867 on prize T0. Not a prize claim.

Run: python3 research/cycle_eg.py --certify
Dump: research/cycle_eg.json
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
from cycle_dn import census
from cycle_ed import threshold
from cycle_ee import image_one_annulus
from cycle_ef import (
    EXTRA52809,
    EXTRA87468,
    MAX_FIRST,
    MAX_ODD,
    PRIZE8,
    first_odd_continue,
)

OUT = Path(__file__).resolve().with_suffix(".json")
EF_JSON = Path(__file__).resolve().parent / "cycle_ef.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
REM87468 = EXTRA87468 - EXTRA52809  # 34659
K15_WORST = 1 << 15
K15_EVEN_P = 53208
PRIZE_K15_LEFT = (1 << 16) - K15_EVEN_P  # 12328


def bits(mask: int, n: int = 8) -> str:
    return "".join(str((mask >> i) & 1) for i in range(n))


def family_52809() -> dict:
    """All 16 even-52809 words; next odd is 87468 or none in 131000."""
    c = census(8, MAX_FIRST)
    fam = sorted(i for i, (e, sm) in c["first"].items() if e == EXTRA52809)
    if len(fam) != 16:
        return {"ok": False, "n": len(fam)}
    if any(c["first"][i][1] != 0 for i in fam):
        return {"ok": False, "odd": True}
    rows: dict[str, int | None] = {}
    hit: list[str] = []
    miss: list[str] = []
    for m in fam:
        s = bits(m)
        cur = first_odd_continue([int(ch) for ch in s], MAX_ODD)
        rows[s] = cur
        if cur == EXTRA87468:
            hit.append(s)
        elif cur is None:
            miss.append(s)
        else:
            return {"ok": False, "T0": s, "cur": cur}
    if len(hit) != 6 or len(miss) != 10:
        return {"ok": False, "hit": hit, "miss": miss}
    if PRIZE8 not in miss:
        return {"ok": False, "prize": True}
    rems = [EXTRA87468 - EXTRA52809] * 6
    if any(r <= K15_WORST for r in rems):
        return {"ok": False, "rem": rems}
    if MAX_ODD - EXTRA52809 <= K15_WORST:
        return {"ok": False, "floor": True}
    return {
        "ok": True,
        "n": 16,
        "n87468": 6,
        "n_none": 10,
        "hit": sorted(hit),
        "miss": sorted(miss),
        "rem87468": REM87468,
    }


def leftover_gap(fam: dict) -> dict:
    """k=15 worst leftover and prize leftover are both < remaining extra."""
    v = threshold(REM87468)
    land = image_one_annulus(8, EXTRA52809)
    ok = (
        fam.get("ok")
        and REM87468 == 34659
        and v == 16
        and (1 << 15) < REM87468 <= (1 << 16)
        and K15_WORST < REM87468
        and PRIZE_K15_LEFT < REM87468
        and land["ok"]
        and land["k_lo"] == 15
        and land["k_hi"] == 15
        and 400 + EXTRA52809 - 1 == K15_EVEN_P
        and image_one_annulus(8, EXTRA87468)["k_lo"] == 16
    )
    return {
        "ok": ok,
        "v_rem": v,
        "k15_worst": K15_WORST,
        "prize_k15_left": PRIZE_K15_LEFT,
        "rem87468": REM87468,
        "land15": {k: land[k] for k in ("lo", "hi", "k_lo", "k_hi")},
    }


def ef_prefix() -> dict:
    ef = json.loads(EF_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    ok = (
        ef["checks"]["all_ok"]
        and ef["verdict"]["fam372_unfolds_to_52809_even"] == "LEMMA"
        and ef["verdict"]["extra52809_k8_lands_k15"] == "LEMMA"
        and ef["verdict"]["k8_maps_to_k16_all_FAM372"] == "KILLED"
        and dm["checks"]["all_ok"]
        and dm["n8"]["hits"][str(EXTRA52809)]["n"] == 16
        and dm["n8"]["prize"]["T0"] == PRIZE8
    )
    return {"ok": ok}


def self_checks(c20, fam: dict, gap: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fam["ok"] and gap["ok"] and pref["ok"]
    assert fam["n"] == 16 and fam["n87468"] == 6 and fam["n_none"] == 10
    assert PRIZE8 in fam["miss"]
    assert fam["rem87468"] == 34659 > K15_WORST
    assert gap["v_rem"] == 16 and gap["prize_k15_left"] == 12328
    assert gap["land15"]["k_lo"] == 15
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fam = family_52809()
    gap = leftover_gap(fam)
    pref = ef_prefix()
    checks = self_checks(c20, fam, gap, pref)
    dump = {
        "cycle": "EG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "family": {
            "n": fam.get("n"),
            "n87468": fam.get("n87468"),
            "n_none": fam.get("n_none"),
            "hit": fam.get("hit"),
            "miss": fam.get("miss"),
            "rem87468": fam.get("rem87468"),
        },
        "gap": {
            "v_rem": gap.get("v_rem"),
            "k15_worst": gap.get("k15_worst"),
            "prize_k15_left": gap.get("prize_k15_left"),
            "rem87468": gap.get("rem87468"),
            "land15": gap.get("land15"),
        },
        "lemmas": {
            "all_52809_next_odd_87468_or_none_131000": True,
            "rem87468_gt_2_15": True,
            "k15_worst_leftover_cannot_fit_next_odd": True,
            "prize_k15_leftover_cannot_fit_next_odd": True,
            "threshold_rem87468_is_16": True,
            "leftover_after_52809_empty_every_later_k": False,
            "next_odd_after_52809_before_k16": False,
            "n87468_closed_form": None,
            "scar_87468_is_packed_87867_on_prize_T0": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "all_52809_next_odd_87468_or_none_131000": "LEMMA",
            "rem87468_gt_2_15": "LEMMA",
            "k15_worst_leftover_cannot_fit_next_odd": "LEMMA",
            "prize_k15_leftover_cannot_fit_next_odd": "LEMMA",
            "threshold_rem87468_is_16": "LEMMA",
            "leftover_after_52809_empty_every_later_k": "KILLED",
            "next_odd_after_52809_before_k16": "KILLED",
            "n87468_closed_form": "PREFIX",
            "scar_87468_is_packed_87867_on_prize_T0": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("family", dump["family"])
    print("gap", dump["gap"])


if __name__ == "__main__":
    main()
