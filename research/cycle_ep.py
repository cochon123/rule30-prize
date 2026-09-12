#!/usr/bin/env python3
"""Cycle EP: n0=16 first ident-0 is even extra 414990 on 32 words.

Cycle DR: every length-16 T0 is ident-0-free in 262144 extras. Bitsliced
census of all 65536 words through extra 414990 finds a unique first
ident-0: even extra 414990 on exactly 32 type-N words, and none earlier.
The 16 n0=2 unfolds and packed prize u16 miss it (they sit in the 65504
with no ident-0 through 414990). Kills: all n0=16 ident-0-free through
extras covering k=20; the 16 unfolds are a sparse ident-0-free family at
this window; min n0=16 extra still only the DR lower bound 262145.
Do not claim extra 414990 is odd; do not claim FAM414990 on the n0=2
cascade; do not claim a one-annulus image from k=16; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ep.py --certify
Dump: research/cycle_ep.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits, xorcat
from cycle_cb import twocopy_type
from cycle_dj import leftover
from cycle_dk import PRIZE_U16
from cycle_dn import census, prize_mask
from cycle_ee import image_one_annulus
from cycle_eh import ident0_events
from cycle_ef import PRIZE8

OUT = Path(__file__).resolve().with_suffix(".json")
EN_JSON = Path(__file__).resolve().parent / "cycle_en.json"
EO_JSON = Path(__file__).resolve().parent / "cycle_eo.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
EXTRA414990 = 414990
N_FAM = 32
N_NONE = 65504
N_WORDS = 1 << 16
WITNESSES = ("1110100110001101", "0110011100101110")


def bits(mask: int, n: int = 16) -> str:
    return "".join(str((mask >> i) & 1) for i in range(n))


def n16_census() -> dict:
    """All 65536 n0=16 words: first ident-0 is even 414990 on 32 words."""
    got = census(16, EXTRA414990)
    fam = []
    for mask, (cur, sm) in got["first"].items():
        if cur != EXTRA414990 or sm != 0:
            return {"ok": False, "mask": mask, "cur": cur, "sm": sm}
        fam.append(bits(mask))
    fam.sort()
    hits = got["hits"]
    ok = (
        got["n_hit"] == N_FAM
        and got["n_none"] == N_NONE
        and got["n_words"] == N_WORDS
        and got["min_extra"] == EXTRA414990
        and hits == {str(EXTRA414990): {"odd": 0, "n": N_FAM}}
        and len(fam) == N_FAM
        and len(set(fam)) == N_FAM
    )
    return {
        "ok": ok,
        "n_hit": got["n_hit"],
        "n_none": got["n_none"],
        "min_extra": got["min_extra"],
        "hits": hits,
        "family": fam,
    }


def family_stats(fam: list[str]) -> dict:
    """32 type-N words; bit0 and xorcat each split 16/16; mixed weights."""
    wts: Counter[int] = Counter()
    xors: Counter[int] = Counter()
    types: Counter[str] = Counter()
    bit0: Counter[int] = Counter()
    for s in fam:
        seq = [int(c) for c in s]
        wts[sum(seq)] += 1
        xors[xorcat(seq)] += 1
        types[twocopy_type(seq)] += 1
        bit0[seq[0]] += 1
    ok = (
        len(fam) == N_FAM
        and types == {"N": N_FAM}
        and bit0 == {0: 16, 1: 16}
        and xors == {0: 16, 1: 16}
        and wts == {6: 3, 7: 8, 8: 10, 9: 8, 10: 3}
    )
    return {
        "ok": ok,
        "wt": {str(k): wts[k] for k in sorted(wts)},
        "xorcat": {str(k): xors[k] for k in sorted(xors)},
        "type": dict(types),
        "bit0": {str(k): bit0[k] for k in sorted(bit0)},
    }


def witnesses_in_family(fam: list[str]) -> dict:
    """Sample T0s hit even 414990; scalar ident0_events agrees."""
    fam_set = set(fam)
    rows: dict[str, dict] = {}
    for s in WITNESSES:
        if s not in fam_set:
            return {"ok": False, "missing": s}
        ev = ident0_events([int(c) for c in s], EXTRA414990 + 1)
        if len(ev) != 1 or ev[0][0] != EXTRA414990 or ev[0][1] != "even":
            return {"ok": False, "T0": s, "ev": ev[:2]}
        rows[s] = {"extra": EXTRA414990, "kind": "even"}
    ok = set(rows) == set(WITNESSES)
    return {"ok": ok, "rows": rows}


def unfolds_miss(fam: list[str]) -> dict:
    """n0=2 unfolds and packed prize u16 are not in FAM414990."""
    en = json.loads(EN_JSON.read_text())
    u16 = en["u16"]
    fam_set = set(fam)
    hits = [s for s in u16.values() if s in fam_set]
    prize_in = PRIZE_U16 in fam_set
    types = {s: twocopy_type([int(c) for c in u16[s]]) for s in u16}
    ok = (
        len(u16) == 16
        and not hits
        and not prize_in
        and u16[PRIZE8] != PRIZE_U16
        and set(types.values()) == {"N"}
        and twocopy_type([int(c) for c in PRIZE_U16]) == "O"
        and all(u16[s][0] == "0" for s in u16)
    )
    return {
        "ok": ok,
        "n_unfold_in_fam": len(hits),
        "packed_prize_in_fam": prize_in,
        "unfold_types": "N",
        "packed_prize_type": "O",
    }


def landings() -> dict:
    """Image from k=16 splits k=18/19; from k=17 and k=18 it is k=19."""
    k16 = image_one_annulus(16, EXTRA414990)
    k17 = image_one_annulus(17, EXTRA414990)
    k18 = image_one_annulus(18, EXTRA414990)
    ok = (
        not k16["ok"]
        and k16["k_lo"] == 18
        and k16["k_hi"] == 19
        and k16["lo"] == 480526
        and k16["hi"] == 546061
        and k17["ok"]
        and k17["k_lo"] == 19
        and k18["ok"]
        and k18["k_lo"] == 19
        and leftover(16) == 43205
        and leftover(16) < EXTRA414990
    )
    return {
        "ok": ok,
        "k16": {kk: k16[kk] for kk in ("ok", "lo", "hi", "k_lo", "k_hi")},
        "k17": {kk: k17[kk] for kk in ("ok", "lo", "hi", "k_lo", "k_hi")},
        "k18": {kk: k18[kk] for kk in ("ok", "lo", "hi", "k_lo", "k_hi")},
        "leftover16": leftover(16),
    }


def prefixes() -> dict:
    eo = json.loads(EO_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    en = json.loads(EN_JSON.read_text())
    ok = (
        eo["checks"]["all_ok"]
        and eo["verdict"]["n16_unfold_ident0_free_through_k20"] == "LEMMA"
        and eo["verdict"]["period_H_seed_at_k21_every_n0_2"] == "LEMMA"
        and dr["checks"]["all_ok"]
        and dr["n16"]["n_hit"] == 0
        and dr["n16"]["n_extra"] == 262144
        and en["checks"]["all_ok"]
        and len(en["u16"]) == 16
        and PRIZE8 in en["u16"]
    )
    return {"ok": ok}


def self_checks(
    c20, scan: dict, stats: dict, wit: dict, miss: dict, land: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert scan["ok"] and stats["ok"] and wit["ok"] and miss["ok"]
    assert land["ok"] and pref["ok"]
    assert scan["n_hit"] == N_FAM and scan["min_extra"] == EXTRA414990
    assert WITNESSES[0] in scan["family"] and WITNESSES[1] in scan["family"]
    assert prize_mask(WITNESSES[0]) != prize_mask(WITNESSES[1])
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    scan = n16_census()
    fam = scan.get("family") or []
    stats = family_stats(fam)
    wit = witnesses_in_family(fam)
    miss = unfolds_miss(fam)
    land = landings()
    pref = prefixes()
    checks = self_checks(c20, scan, stats, wit, miss, land, pref)
    dump = {
        "cycle": "EP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "extra": EXTRA414990,
        "n16": {
            "n_words": N_WORDS,
            "n_extra": EXTRA414990,
            "n_hit": scan["n_hit"],
            "n_none": scan["n_none"],
            "min_extra": scan["min_extra"],
            "hits": scan["hits"],
        },
        "family": {
            "n": len(fam),
            "words": fam,
            "stats": {k: stats[k] for k in ("wt", "xorcat", "type", "bit0")},
            "witnesses": list(WITNESSES),
        },
        "unfolds_miss": {
            "n_unfold_in_fam": miss["n_unfold_in_fam"],
            "packed_prize_in_fam": miss["packed_prize_in_fam"],
            "unfold_types": miss["unfold_types"],
            "packed_prize_type": miss["packed_prize_type"],
        },
        "land": {
            "k16": land["k16"],
            "k17": land["k17"],
            "k18": land["k18"],
            "leftover16": land["leftover16"],
        },
        "lemmas": {
            "n16_min_extra_even_414990": True,
            "fam414990_32_type_N": True,
            "n0_2_unfolds_and_packed_prize_miss_414990": True,
            "k16_leftover_shorter_than_414990": True,
            "all_n16_ident0_free_through_k20": False,
            "unfolds_sparse_ident0_free_family_at_2M": False,
            "extra_414990_odd": False,
            "fam414990_on_n0_2": False,
            "n16_u16_closed_form": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n16_min_extra_even_414990": "LEMMA",
            "fam414990_32_type_N": "LEMMA",
            "n0_2_unfolds_and_packed_prize_miss_414990": "LEMMA",
            "k16_leftover_shorter_than_414990": "LEMMA",
            "all_n16_ident0_free_through_k20": "KILLED",
            "unfolds_sparse_ident0_free_family_at_2M": "KILLED",
            "extra_414990_odd": "KILLED",
            "fam414990_on_n0_2": "KILLED",
            "n16_u16_closed_form": "PREFIX",
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
    print("n16", dump["n16"])
    print("family_n", dump["family"]["n"])
    print("unfolds_miss", dump["unfolds_miss"])
    print("land_k16", dump["land"]["k16"])


if __name__ == "__main__":
    main()
