#!/usr/bin/env python3
"""Cycle EL: every n0=2 scar has at most one odd in k=17; seed at k=18.

Cycle EK: n0=2 scars have at most one odd in k=16 and the period-H seed
at k=17. The ten even-52809 words with no odd in 131000 extras first-odd
at 228939 (six 57888-miss words, including prize T0), 182785 (two),
195790 (one), or none in 261633 (00001101). Those three extras land in
k=17. Cycle DR: an n0=16 odd at k=16 skips k=17, so the six extra-87468
words have no second odd there. Hence at most one odd in k=17 on every
n0=2 scar, and pi_18 in {16,32} divides 2^17. Kills: prize T0 has no
scar odd after the two k=15 evens; every n0=2 scar skips k=17. Do not
claim a closed form for 228939; do not equate it with packed 87867; do
not claim 00001101 never odd-doubles; do not claim the seed for all k.
Not a prize claim.

Run: python3 research/cycle_el.py --certify
Dump: research/cycle_el.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, packed_center_bits
from cycle_dn import alive_mask, bitslice_T, pop_bits, reconstruct_slice
from cycle_du import pi_from_odds, seed_from_at_most_one
from cycle_ee import image_one_annulus
from cycle_ef import EXTRA87468, PRIZE8, first_odd_continue
from cycle_ek import E16, ODD_COUNTS_1_15

OUT = Path(__file__).resolve().with_suffix(".json")
EK_JSON = Path(__file__).resolve().parent / "cycle_ek.json"
EH_JSON = Path(__file__).resolve().parent / "cycle_eh.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
K18 = 1 << 18
MAX_K17 = K18 - ((1 << 9) - 1)  # 261633: image hi=511+E stays <= 2^18
EXTRA228939 = 228939
EXTRA182785 = 182785
EXTRA195790 = 195790
MISS57888 = {
    "00000110",
    "00011011",
    "10000011",
    "11011111",
    "11100100",
    "11111001",
}
G72177 = {"00001101", "00100000", "01111100", "10010000"}
HIT87468_8 = {
    "00110111",
    "01000001",
    "01101111",
    "10111110",
    "11001000",
    "11110010",
}
EXPECT_MISS = {
    "00000110": EXTRA228939,
    "00011011": EXTRA228939,
    "10000011": EXTRA228939,
    "11011111": EXTRA228939,
    "11100100": EXTRA228939,
    "11111001": EXTRA228939,
    "00001101": None,
    "00100000": EXTRA182785,
    "01111100": EXTRA195790,
    "10010000": EXTRA182785,
}


def key_mask(s: str) -> int:
    w = 0
    for i, ch in enumerate(s):
        w |= int(ch) << i
    return w


def unfold_slice(A: list[int], mask: int, L: int) -> list[int]:
    """Bitsliced unfold with u_0=0: u_{t+1}=A_t xor u_t."""
    U = [0] * L
    u = 0
    for t in range(L - 1):
        u = (A[t] ^ u) & mask
        U[t + 1] = u
    return U


def first_odd_slice(n0: int, max_extra: int) -> dict:
    """First odd ident-0 extra per T0, continuing even via unfold."""
    T, mask, n_words, L = bitslice_T(n0)
    A, B = T, [mask] * L
    first: dict[int, int] = {}
    remaining = mask
    for cur in range(3, 3 + max_extra):
        live = alive_mask(B, mask)
        newly = remaining & (~live) & mask
        if newly:
            xorA = 0
            for sl in A:
                xorA ^= sl
            odd_hit = newly & xorA
            even_hit = newly & (~xorA) & mask
            for i in pop_bits(odd_hit):
                first[i] = cur
            remaining &= ~odd_hit
            if remaining == 0:
                break
            prev_B = B
            U_rec = reconstruct_slice(A, B, mask, L)
            if even_hit:
                U_unf = unfold_slice(A, mask, L)
                keep = (~even_hit) & mask
                nxt = [(even_hit & U_unf[t]) | (keep & U_rec[t]) for t in range(L)]
            else:
                nxt = U_rec
            A, B = prev_B, nxt
        else:
            A, B = B, reconstruct_slice(A, B, mask, L)
    return {
        "first": first,
        "remaining": remaining,
        "n_words": n_words,
        "n_hit": len(first),
        "n_none": remaining.bit_count(),
    }


def family_odds(scan: dict) -> dict:
    """Split the 16-word 52809 family by first-odd extra in the k=17 window."""
    by: dict[str, list[str]] = defaultdict(list)
    extras: dict[str, int | None] = {}
    fam = MISS57888 | G72177 | HIT87468_8
    if len(fam) != 16:
        return {"ok": False, "n": len(fam)}
    first = scan["first"]
    for s in sorted(fam):
        m = key_mask(s)
        cur = first.get(m)
        extras[s] = cur
        by[str(cur)].append(s)
        if s in HIT87468_8:
            if cur != EXTRA87468:
                return {"ok": False, "hit": s, "cur": cur}
        elif s in EXPECT_MISS:
            if cur != EXPECT_MISS[s]:
                return {"ok": False, "miss": s, "cur": cur, "want": EXPECT_MISS[s]}
        else:
            return {"ok": False, "extra": s}
    g228 = by[str(EXTRA228939)]
    g182 = by[str(EXTRA182785)]
    g195 = by[str(EXTRA195790)]
    gnone = by["None"]
    ok = (
        set(g228) == MISS57888
        and set(g182) == {"00100000", "10010000"}
        and g195 == ["01111100"]
        and gnone == ["00001101"]
        and PRIZE8 in g228
        and scan["n_hit"] == 214
        and scan["n_none"] == 42
    )
    return {
        "ok": ok,
        "n87468": 6,
        "n228939": 6,
        "n182785": 2,
        "n195790": 1,
        "n_none": 1,
        "g228939": sorted(g228),
        "g182785": sorted(g182),
        "g195790": g195,
        "none": gnone,
        "prize_odd": extras[PRIZE8],
    }


def scalar_match(scan: dict) -> dict:
    """Bitslice first-odd agrees with first_odd_continue on prize and 00001101."""
    pz = first_odd_continue([int(c) for c in PRIZE8], MAX_K17)
    none = first_odd_continue([int(c) for c in "00001101"], MAX_K17)
    hit = first_odd_continue([int(c) for c in "00110111"], EXTRA87468 + 1)
    ok = (
        pz == EXTRA228939
        and scan["first"][key_mask(PRIZE8)] == EXTRA228939
        and none is None
        and key_mask("00001101") not in scan["first"]
        and hit == EXTRA87468
        and scan["first"][key_mask("00110111")] == EXTRA87468
    )
    return {"ok": ok, "prize": pz, "none": none, "hit": hit}


def k17_window() -> dict:
    rows = {
        "228939": image_one_annulus(8, EXTRA228939),
        "182785": image_one_annulus(8, EXTRA182785),
        "195790": image_one_annulus(8, EXTRA195790),
        "87468": image_one_annulus(8, EXTRA87468),
    }
    left = {k: K18 - rows[k]["hi"] for k in ("228939", "182785", "195790")}
    ok = (
        all(rows[k]["ok"] and rows[k]["k_lo"] == 17 for k in ("228939", "182785", "195790"))
        and rows["87468"]["ok"]
        and rows["87468"]["k_lo"] == 16
        and rows["228939"]["lo"] == 229195
        and rows["228939"]["hi"] == 229450
        and left["228939"] == 32694
        and left["228939"] < E16
        and left["182785"] < E16
        and left["195790"] < E16
        and MAX_K17 == 261633
    )
    return {
        "ok": ok,
        "land": {
            k: {kk: rows[k][kk] for kk in ("lo", "hi", "k_lo", "k_hi")} for k in rows
        },
        "leftover": left,
        "k17_need": MAX_K17,
    }


def seed_k18() -> dict:
    pi00 = pi_from_odds(ODD_COUNTS_1_15 + [0, 0])
    pi10 = pi_from_odds(ODD_COUNTS_1_15 + [1, 0])
    pi01 = pi_from_odds(ODD_COUNTS_1_15 + [0, 1])
    h = 1 << 17
    ok = (
        pi00 == 16
        and pi10 == 32
        and pi01 == 32
        and h % pi00 == 0
        and h % pi10 == 0
        and h % pi01 == 0
        and seed_from_at_most_one(18)
        and max(ODD_COUNTS_1_15) <= 1
    )
    return {
        "ok": ok,
        "pi_no_k16_no_k17": pi00,
        "pi_k16_only": pi10,
        "pi_k17_only": pi01,
        "H18": h,
    }


def prefixes() -> dict:
    ek = json.loads(EK_JSON.read_text())
    eh = json.loads(EH_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    hit = set(eh["family"]["hit"])
    g72177 = set(eh["family"]["g72177"])
    ok = (
        ek["checks"]["all_ok"]
        and ek["verdict"]["at_most_one_odd_k16_on_n0_2"] == "LEMMA"
        and ek["verdict"]["period_H_seed_at_k17_every_n0_2"] == "LEMMA"
        and ek["n87468"] == 6
        and ek["n_none"] == 10
        and eh["checks"]["all_ok"]
        and hit == HIT87468_8
        and g72177 == G72177
        and PRIZE8 not in g72177
        and PRIZE8 not in hit
        and dr["checks"]["all_ok"]
        and dr["n16"]["n_hit"] == 0
        and dr["n16"]["E16"] == E16
        and dr["verdict"]["n0_16_odd_at_k_9_to_16_skips_k17"] == "LEMMA"
    )
    return {"ok": ok, "n87468": 6, "n_none": 10}


def self_checks(
    c20, scan: dict, fam: dict, scalar: dict, win: dict, seed: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fam["ok"] and scalar["ok"] and win["ok"] and seed["ok"] and pref["ok"]
    assert fam["prize_odd"] == EXTRA228939
    assert scalar["prize"] == EXTRA228939 and scalar["none"] is None
    assert win["land"]["228939"]["k_lo"] == 17
    assert win["leftover"]["228939"] < E16
    assert seed["pi_k17_only"] == 32 and seed["H18"] == 1 << 17
    assert scan["n_hit"] == 214
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    scan = first_odd_slice(8, MAX_K17)
    fam = family_odds(scan)
    scalar = scalar_match(scan)
    win = k17_window()
    seed = seed_k18()
    pref = prefixes()
    checks = self_checks(c20, scan, fam, scalar, win, seed, pref)
    dump = {
        "cycle": "EL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "family": {
            "n87468": fam.get("n87468"),
            "n228939": fam.get("n228939"),
            "n182785": fam.get("n182785"),
            "n195790": fam.get("n195790"),
            "n_none": fam.get("n_none"),
            "g228939": fam.get("g228939"),
            "g182785": fam.get("g182785"),
            "g195790": fam.get("g195790"),
            "none": fam.get("none"),
            "prize_odd": fam.get("prize_odd"),
        },
        "scan": {"n_hit": scan["n_hit"], "n_none": scan["n_none"], "max_extra": MAX_K17},
        "k17": {
            "ok": win["ok"],
            "land": win["land"],
            "leftover": win["leftover"],
            "k17_need": win["k17_need"],
        },
        "seed_k18": {
            "pi_no_k16_no_k17": seed["pi_no_k16_no_k17"],
            "pi_k16_only": seed["pi_k16_only"],
            "pi_k17_only": seed["pi_k17_only"],
            "H18": seed["H18"],
        },
        "lemmas": {
            "extra228939_k8_lands_k17": True,
            "k17_leftover_after_228939_lt_E16": True,
            "max_k17_covers_window_from_k8": True,
            "prize_scar_odd_228939": True,
            "n0_16_k16_odd_skips_k17": True,
            "at_most_one_odd_k17_on_n0_2": True,
            "period_H_seed_at_k18_every_n0_2": True,
            "prize_no_scar_odd_after_k15_evens": False,
            "every_n0_2_skips_k17": False,
            "n228939_closed_form": None,
            "scar_228939_is_packed_87867_on_prize_T0": None,
            "word_00001101_never_odd": None,
            "leftover_after_228939_empty_later_k": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "extra228939_k8_lands_k17": "LEMMA",
            "k17_leftover_after_228939_lt_E16": "LEMMA",
            "max_k17_covers_window_from_k8": "LEMMA",
            "prize_scar_odd_228939": "LEMMA",
            "n0_16_k16_odd_skips_k17": "LEMMA",
            "at_most_one_odd_k17_on_n0_2": "LEMMA",
            "period_H_seed_at_k18_every_n0_2": "LEMMA",
            "prize_no_scar_odd_after_k15_evens": "KILLED",
            "every_n0_2_skips_k17": "KILLED",
            "n228939_closed_form": "PREFIX",
            "scar_228939_is_packed_87867_on_prize_T0": "PREFIX",
            "word_00001101_never_odd": "PREFIX",
            "leftover_after_228939_empty_later_k": "PREFIX",
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
    print("family", dump["family"])
    print("k17", {k: win[k] for k in ("land", "leftover", "k17_need")})
    print("seed_k18", dump["seed_k18"])


if __name__ == "__main__":
    main()
