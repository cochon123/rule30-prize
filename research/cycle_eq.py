#!/usr/bin/env python3
"""Cycle EQ: FAM414990 predecessors are the 32 rotations of one 32-bit word.

Cycle EP: 32 type-N n0=16 T0s have first ident-0 at even extra 414990.
The 32 length-32 predecessors are exactly the rotation class of
W=00000001011101010010010000101011 (min period 32, weight 12, even
xorcat). The T0 family is closed under complement (16 pairs). After that
even, bitsliced first-odd continuation of the 32 words finds no odd
ident-0 through 2^21 extras. Kills: FAM414990 preds not a rotation
orbit; family not complement-closed; these 32 odd-double before 2^21.
Do not claim a closed form for the T0 strings beyond this necklace;
do not claim W on the n0=2 cascade; do not bump all n0=16 past 414990;
do not claim min odd extra for every n0=16 is >2^21. Not a prize claim.

Run: python3 research/cycle_eq.py --certify
Dump: research/cycle_eq.json
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
from cycle_ca import KNOWN20, packed_center_bits, xorcat
from cycle_cb import twocopy_type
from cycle_dn import alive_mask, pop_bits, prize_mask, reconstruct_slice
from cycle_ee import image_one_annulus
from cycle_ef import first_odd_continue
from cycle_eh import ident0_events
from cycle_el import unfold_slice
from cycle_ep import EXTRA414990, FAM414990, N_FAM, WITNESSES

OUT = Path(__file__).resolve().with_suffix(".json")
EP_JSON = Path(__file__).resolve().parent / "cycle_ep.json"
PRED32 = "00000001011101010010010000101011"
MAX_ODD = 1 << 21
N0 = 16


def rotations(s: str) -> frozenset[str]:
    return frozenset(s[i:] + s[:i] for i in range(len(s)))


def complement(s: str) -> str:
    return "".join("01"[ch == "0"] for ch in s)


ROTS_PRED32 = rotations(PRED32)


def bitslice_words(words: list[int], n0: int):
    n_words = len(words)
    L = 2 * n0
    mask = (1 << n_words) - 1
    T = []
    for t in range(n0):
        sl = 0
        for i, w in enumerate(words):
            if (w >> t) & 1:
                sl |= 1 << i
        T.append(sl)
    T += [(~sl) & mask for sl in T]
    return T, mask, n_words, L


def fam_events(words: list[int], n0: int, max_extra: int) -> dict:
    """Even then odd ident-0 on a bitsliced list; capture even predecessors."""
    T, mask, n_words, L = bitslice_words(words, n0)
    A, B = T, [mask] * L
    first_odd: dict[int, int] = {}
    pred: dict[int, str] = {}
    even_at: int | None = None
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
            if even_hit:
                if even_at is None:
                    even_at = cur
                for i in pop_bits(even_hit):
                    pred[i] = "".join(str((A[t] >> i) & 1) for t in range(L))
            for i in pop_bits(odd_hit):
                first_odd[i] = cur
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
        "even_at": even_at,
        "pred": pred,
        "first_odd": first_odd,
        "n_odd": len(first_odd),
        "n_none": remaining.bit_count(),
        "n_words": n_words,
        "stopped_at": cur,
    }


def pred_necklace() -> dict:
    """W has min period 32, weight 12, even xorcat, 32 distinct rotations."""
    w = [int(c) for c in PRED32]
    ok = (
        len(PRED32) == 32
        and len(ROTS_PRED32) == 32
        and PRED32.count("1") == 12
        and xorcat(w) == 0
        and twocopy_type(w) == "N"
        and PRED32 in ROTS_PRED32
    )
    return {"ok": ok, "period": 32, "wt": 12, "xorcat": 0, "type": "N"}


def complement_closed() -> dict:
    """FAM414990 is 16 complement pairs; EP witnesses are a pair."""
    fam = FAM414990
    pairs = []
    seen: set[str] = set()
    for s in sorted(fam):
        c = complement(s)
        if c not in fam:
            return {"ok": False, "missing": s}
        if s not in seen:
            pairs.append((s, c))
            seen.update((s, c))
    ok = (
        len(fam) == N_FAM
        and len(pairs) == 16
        and complement(WITNESSES[0]) in fam
        and complement(WITNESSES[1]) in fam
        and {WITNESSES[0], complement(WITNESSES[0])} <= fam
    )
    return {"ok": ok, "n_pairs": len(pairs)}


def scan_family() -> dict:
    """Even 414990 preds are exactly rots(W); no odd through 2^21."""
    fam = sorted(FAM414990)
    words = [prize_mask(s) for s in fam]
    got = fam_events(words, N0, MAX_ODD)
    preds = [got["pred"][i] for i in range(len(fam))]
    pred_set = set(preds)
    ok = (
        got["even_at"] == EXTRA414990
        and got["n_odd"] == 0
        and got["n_none"] == N_FAM
        and len(got["pred"]) == N_FAM
        and pred_set == set(ROTS_PRED32)
        and len(pred_set) == 32
        and all(xorcat([int(c) for c in p]) == 0 for p in preds)
        and all(p.count("1") == 12 for p in preds)
    )
    return {
        "ok": ok,
        "even_at": got["even_at"],
        "n_odd": got["n_odd"],
        "n_none": got["n_none"],
        "n_pred": len(pred_set),
        "stopped_at": got["stopped_at"],
        "pred_by_T0": {fam[i]: preds[i] for i in range(len(fam))},
    }


def scalar_match(scan: dict) -> dict:
    """Scalar ident0_events on both witnesses agrees on extra, kind, necklace."""
    rows: dict[str, dict] = {}
    for s in WITNESSES:
        ev = ident0_events([int(c) for c in s], EXTRA414990 + 1)
        if (
            len(ev) != 1
            or ev[0][0] != EXTRA414990
            or ev[0][1] != "even"
            or ev[0][2] not in ROTS_PRED32
        ):
            return {"ok": False, "T0": s, "ev": ev[:2]}
        if scan["pred_by_T0"].get(s) != ev[0][2]:
            return {"ok": False, "T0": s, "slice": scan["pred_by_T0"].get(s), "scalar": ev[0][2]}
        rows[s] = {"extra": EXTRA414990, "kind": "even", "pred": ev[0][2]}
    odd = first_odd_continue([int(c) for c in WITNESSES[0]], EXTRA414990 + 50)
    ok = odd is None and set(rows) == set(WITNESSES)
    return {"ok": ok, "rows": rows, "odd_just_after_even": odd}


def landings() -> dict:
    """No odd through 2^21 exceeds leftover at k<=21 from a k=16 origin."""
    k16_even = image_one_annulus(16, EXTRA414990)
    k19_even = image_one_annulus(19, EXTRA414990)
    ok = (
        not k16_even["ok"]
        and k16_even["k_lo"] == 18
        and k16_even["k_hi"] == 19
        and k19_even["ok"]
        and k19_even["k_lo"] == 19
        and MAX_ODD > EXTRA414990
        and MAX_ODD > (1 << 20)
        and (1 << 21) == MAX_ODD
    )
    return {
        "ok": ok,
        "k16_even": {kk: k16_even[kk] for kk in ("ok", "k_lo", "k_hi")},
        "k19_even": {kk: k19_even[kk] for kk in ("ok", "k_lo", "k_hi")},
        "max_odd": MAX_ODD,
    }


def prefixes() -> dict:
    ep = json.loads(EP_JSON.read_text())
    ok = (
        ep["checks"]["all_ok"]
        and ep["verdict"]["n16_min_extra_even_414990"] == "LEMMA"
        and ep["verdict"]["fam414990_32_type_N"] == "LEMMA"
        and ep["extra"] == EXTRA414990
        and ep["family"]["n"] == N_FAM
        and set(ep["family"]["words"]) == FAM414990
    )
    return {"ok": ok}


def self_checks(
    c20, neck: dict, comp: dict, scan: dict, match: dict, land: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert neck["ok"] and comp["ok"] and scan["ok"] and match["ok"]
    assert land["ok"] and pref["ok"]
    assert scan["even_at"] == EXTRA414990 and scan["n_odd"] == 0
    assert match["odd_just_after_even"] is None
    assert complement(WITNESSES[0]) in FAM414990
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    neck = pred_necklace()
    comp = complement_closed()
    scan = scan_family()
    match = scalar_match(scan)
    land = landings()
    pref = prefixes()
    checks = self_checks(c20, neck, comp, scan, match, land, pref)
    dump = {
        "cycle": "EQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "pred32": PRED32,
        "even": EXTRA414990,
        "max_odd": MAX_ODD,
        "n_fam": N_FAM,
        "scan": {
            "even_at": scan["even_at"],
            "n_odd": scan["n_odd"],
            "n_none": scan["n_none"],
            "n_pred": scan["n_pred"],
            "stopped_at": scan["stopped_at"],
        },
        "complement_pairs": comp["n_pairs"],
        "land": land,
        "lemmas": {
            "fam414990_preds_rots_of_W": True,
            "pred32_min_period_32": True,
            "fam414990_complement_closed": True,
            "fam414990_no_odd_through_2_21": True,
            "preds_not_rotation_orbit": False,
            "family_not_complement_closed": False,
            "odd_before_2_21": False,
            "T0_closed_form_beyond_necklace": None,
            "W_on_n0_2_cascade": False,
            "min_odd_all_n16_gt_2_21": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "fam414990_preds_rots_of_W": "LEMMA",
            "pred32_min_period_32": "LEMMA",
            "fam414990_complement_closed": "LEMMA",
            "fam414990_no_odd_through_2_21": "LEMMA",
            "preds_not_rotation_orbit": "KILLED",
            "family_not_complement_closed": "KILLED",
            "odd_before_2_21": "KILLED",
            "T0_closed_form_beyond_necklace": "PREFIX",
            "W_on_n0_2_cascade": "KILLED",
            "min_odd_all_n16_gt_2_21": "PREFIX",
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
    print("pred32", PRED32)
    print("scan", dump["scan"])
    print("complement_pairs", dump["complement_pairs"])


if __name__ == "__main__":
    main()
