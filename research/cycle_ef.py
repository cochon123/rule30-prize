#!/usr/bin/env python3
"""Cycle EF: every FAM372 scar lifts to the even-52809 n0=8 family.

Every n0=4 extra-372 T0 has first-odd predecessor a a rotation of 00001011.
unfold(a) is an n0=8 word whose first ident-0 extra is the even 52809
family (Cycle DM; 16 words, prize T0=00000110 included). Extra 52809 from
k=8 lands in annulus k=15 (even, no period doubling). The odd n0=8 extras
26357 (k=14) and 44842 (k=15) are unreachable as first ident-0 after
FAM372. FAM89 unfolds have no ident-0 in 53000 extras. Among the eight
FAM372 lifts, three scar-odd-double at extra 87468 (k=16) and five,
including prize T0=00000110, have no odd ident-0 in 131000 extras (the
k=16 window from k=8). Kills: FAM372 can hit odd extra 26357; k=8 maps
to k=16 for every FAM372 scar. Do not claim a closed form for 52809 or
87468; do not equate scar extra 87468 with packed bit 87867 on prize T0.
Not a prize claim.

Run: python3 research/cycle_ef.py --certify
Dump: research/cycle_ef.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct, xorcat
from cycle_df import unfold
from cycle_di import FAM372, FAM89, PRIZE4, first_odd
from cycle_dm import first_ident0_int
from cycle_ee import LIFT372, image_one_annulus

OUT = Path(__file__).resolve().with_suffix(".json")
EE_JSON = Path(__file__).resolve().parent / "cycle_ee.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
PRIZE8 = "00000110"
PRIZE_A8 = "00001011"
EXTRA52809 = 52809
EXTRA87468 = 87468
MAX_FIRST = 53000
MAX_ODD = 131000
HIT87468 = {"0010", "1001", "1011"}


def first_odd_continue(T0: list[int], max_extra: int) -> int | None:
    """First odd ident-0 extra, continuing through even ident-0 via unfold."""
    n0 = len(T0)
    T = T0 + [x ^ 1 for x in T0]
    L = 2 * n0
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    for cur in range(3, 3 + max_extra):
        a, b = seqs[cur - 2], seqs[cur - 1]
        if all(x == 0 for x in b):
            if xorcat(a) == 1:
                return cur
            u = [0] * L
            for t in range(L - 1):
                u[t + 1] = a[t] ^ u[t]
            seqs[cur] = u
        else:
            u = reconstruct(a, b)
            if u is None:
                return None
            seqs[cur] = u
    return None


def unfold_fam(fam: set[str], extra4: int) -> dict[str, str] | dict:
    rows: dict[str, str] = {}
    for key in sorted(fam):
        cur, a = first_odd([int(c) for c in key], 400)
        if cur != extra4 or a is None:
            return {"ok": False, "T0": key, "cur": cur}
        u = "".join(map(str, unfold([int(c) for c in a])))
        rows[key] = u
    return {"ok": True, "rows": rows}


def fam372_to_52809() -> dict:
    """Every FAM372 T0 unfolds to an n0=8 word with first ident-0 extra 52809 even."""
    unf = unfold_fam(FAM372, 372)
    if not unf.get("ok"):
        return unf
    rows = unf["rows"]
    if len(set(rows.values())) != 8:
        return {"ok": False, "dup": True}
    if PRIZE4 not in FAM372:
        return {"ok": False, "prize4": True}
    if rows["1101"] != PRIZE8:
        return {"ok": False, "prize8": rows["1101"]}
    cur, a = first_odd([1, 1, 0, 1], 400)
    if a != PRIZE_A8:
        return {"ok": False, "a": a}
    for key, u in rows.items():
        e0, sm = first_ident0_int([int(c) for c in u], MAX_FIRST)
        if e0 != EXTRA52809 or sm != 0:
            return {"ok": False, "T0": key, "u": u, "e0": e0, "sm": sm}
    lift = {k: rows[k] for k in LIFT372}
    if set(lift) != LIFT372:
        return {"ok": False, "lift": True}
    return {"ok": True, "rows": rows, "lift372": lift}


def fam89_none() -> dict:
    """FAM89 unfolds have no ident-0 in 53000 extras (not 26357/44842/52809)."""
    unf = unfold_fam(FAM89, 89)
    if not unf.get("ok"):
        return unf
    rows = unf["rows"]
    if len(set(rows.values())) != 8:
        return {"ok": False, "dup": True}
    for key, u in rows.items():
        e0, sm = first_ident0_int([int(c) for c in u], MAX_FIRST)
        if e0 is not None:
            return {"ok": False, "T0": key, "u": u, "e0": e0, "sm": sm}
    return {"ok": True, "n": 8}


def odd_split(rows: dict[str, str]) -> dict:
    """Three FAM372 lifts scar-odd-double at 87468; five none in 131000."""
    hit: list[str] = []
    miss: list[str] = []
    extras: dict[str, int | None] = {}
    for key, u in rows.items():
        cur = first_odd_continue([int(c) for c in u], MAX_ODD)
        extras[key] = cur
        if cur == EXTRA87468:
            hit.append(key)
        elif cur is None:
            miss.append(key)
        else:
            return {"ok": False, "T0": key, "cur": cur}
    if set(hit) != HIT87468 or len(miss) != 5:
        return {"ok": False, "hit": hit, "miss": miss}
    if "1101" not in miss or rows["1101"] != PRIZE8:
        return {"ok": False, "prize": True}
    return {
        "ok": True,
        "n87468": 3,
        "n_none": 5,
        "hit": sorted(hit),
        "miss": sorted(miss),
        "extras": extras,
    }


def landings() -> dict:
    """k=8 extra 52809 -> k=15; 26357 -> k=14; 44842 -> k=15; 87468 -> k=16."""
    rows = {
        "52809_from_8": image_one_annulus(8, EXTRA52809),
        "26357_from_8": image_one_annulus(8, 26357),
        "44842_from_8": image_one_annulus(8, 44842),
        "87468_from_8": image_one_annulus(8, EXTRA87468),
    }
    ok = (
        rows["52809_from_8"]["ok"]
        and rows["52809_from_8"]["k_lo"] == 15
        and rows["26357_from_8"]["ok"]
        and rows["26357_from_8"]["k_lo"] == 14
        and rows["44842_from_8"]["ok"]
        and rows["44842_from_8"]["k_lo"] == 15
        and rows["87468_from_8"]["ok"]
        and rows["87468_from_8"]["k_lo"] == 16
    )
    even_packed = 400 + EXTRA52809 - 1
    if even_packed != 53208:
        return {"ok": False, "even_packed": even_packed}
    return {"ok": ok, "rows": rows, "even_packed": even_packed}


def ee_prefix() -> dict:
    ee = json.loads(EE_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    ok = (
        ee["checks"]["all_ok"]
        and ee["verdict"]["n0_2_lifts_to_FAM372"] == "LEMMA"
        and ee["verdict"]["FAM89_reachable_from_n0_2"] == "KILLED"
        and dm["checks"]["all_ok"]
        and dm["n8"]["prize"]["extra"] == EXTRA52809
        and dm["n8"]["prize"]["odd"] == 0
        and dm["n8"]["hits"][str(EXTRA52809)]["n"] == 16
        and dm["n8"]["odd_extras"] == [26357, 44842]
    )
    return {"ok": ok}


def self_checks(
    c20, fam: dict, fam89: dict, split: dict, land: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fam["ok"] and fam89["ok"] and split["ok"] and land["ok"] and pref["ok"]
    assert fam["rows"]["1101"] == PRIZE8
    assert fam["rows"]["0010"] == "01101111"
    assert split["n87468"] == 3 and "0010" in split["hit"]
    assert "1101" in split["miss"]
    assert land["rows"]["52809_from_8"]["k_lo"] == 15
    assert land["rows"]["26357_from_8"]["k_lo"] == 14
    assert land["even_packed"] == 53208
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fam = fam372_to_52809()
    fam89 = fam89_none()
    split = odd_split(fam["rows"] if fam.get("ok") else {})
    land = landings()
    pref = ee_prefix()
    checks = self_checks(c20, fam, fam89, split, land, pref)
    dump = {
        "cycle": "EF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "fam372_u8": fam.get("rows"),
        "odd_split": {
            "n87468": split.get("n87468"),
            "n_none": split.get("n_none"),
            "hit": split.get("hit"),
            "miss": split.get("miss"),
        },
        "landings": {
            k: {kk: vv for kk, vv in row.items() if kk != "ok"}
            for k, row in land["rows"].items()
        },
        "even_packed": land["even_packed"],
        "lemmas": {
            "fam372_unfolds_to_52809_even": True,
            "prize_u8_from_1101": True,
            "extra52809_k8_lands_k15": True,
            "fam89_unfolds_none_in_53000": True,
            "fam372_first_ident0_odd_26357": False,
            "k8_maps_to_k16_all_FAM372": False,
            "n87468_closed_form": None,
            "scar_87468_is_packed_87867_on_prize_T0": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "fam372_unfolds_to_52809_even": "LEMMA",
            "prize_u8_from_1101": "LEMMA",
            "extra52809_k8_lands_k15": "LEMMA",
            "fam89_unfolds_none_in_53000": "LEMMA",
            "fam372_first_ident0_odd_26357": "KILLED",
            "k8_maps_to_k16_all_FAM372": "KILLED",
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
    print("fam372_u8", dump["fam372_u8"])
    print("odd_split", dump["odd_split"])
    print("landings", dump["landings"])


if __name__ == "__main__":
    main()
