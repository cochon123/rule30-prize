#!/usr/bin/env python3
"""Cycle EU: reconstruct(A,1) and (1,S) closed forms; n0=16 ident-0 in k>=18.

Unique continuation against all-1s is a rotate-NOT:
reconstruct(A,1)_t = 1 xor A_{t-1}. For O-type T of half-length n0 that is
rot^{n0-1}(T), so n3 after (0,T,1) is a rotation of T. Unique continuation
against all-0s of a nonzero T is all-1s. Unique continuation of all-1s
against any nonzero S is gap-parity: reconstruct(1,S)_t = 1 iff the
backward distance to the previous 1 of S is even (NOR recurrence; isolated
1s). The pair map F(A,B)=(B, reconstruct(A,B)) inverts by
A_t = U_{t+1} xor (B_t or U_t). Two steps before ident-0 the bits are
D(W), W, W, 0. Cycle EP min extra 414990 for n0=16 exceeds 2^18, so every
n0=16 ident-0 has packed index >= 414990 and sits in annulus k>=18:
origin k<=15 lands only in k=18, origin k=16 splits 18/19, origin k=17,18
lands only in k=19. Kills: n0=16 ident-0 (even or odd) in k<=17; no closed
form for reconstruct(T,1). Do not claim a formula for extra 414990; do not
claim no n0=16 ident-0 in k=18; do not bump all n0=16 past 414990; do not
claim at-most-one-odd for all k. Not a prize claim.

Run: python3 research/cycle_eu.py --certify
Dump: research/cycle_eu.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import KNOWN20, deriv, packed_center_bits, reconstruct, xorcat
from cycle_cb import twocopy_type
from cycle_dv import mask_bits, odd_copy
from cycle_ee import annulus, image_one_annulus
from cycle_ep import EXTRA414990, FAM414990, N_FAM, N_NONE
from cycle_eq import PRED32
from cycle_er import T_STAR, U32
from cycle_es import rot

OUT = Path(__file__).resolve().with_suffix(".json")
EP_JSON = Path(__file__).resolve().parent / "cycle_ep.json"
ET_JSON = Path(__file__).resolve().parent / "cycle_et.json"


def back_dist(seq: list[int], t: int) -> int | None:
    """Least k>=1 with seq[t-k]=1, or None if seq is 0."""
    n = len(seq)
    for k in range(1, n + 1):
        if seq[(t - k) % n] == 1:
            return k
    return None


def gap_parity(seq: list[int]) -> list[int] | None:
    """1 at t iff backward distance to the previous 1 is even."""
    if not any(seq):
        return None
    out: list[int] = []
    for t in range(len(seq)):
        d = back_dist(seq, t)
        if d is None:
            return None
        out.append(1 if d % 2 == 0 else 0)
    return out


def inv_A(b: list[int], u: list[int]) -> list[int]:
    """Recover A from (B,U) via A_t = U_{t+1} xor (B_t or U_t)."""
    n = len(b)
    return [u[(t + 1) % n] ^ (b[t] | u[t]) for t in range(n)]


def reconstruct_ones() -> dict:
    """reconstruct(A,1)_t = 1 xor A_{t-1} for every A, length 1..10."""
    n_exh = 0
    for n in range(1, 11):
        ones = [1] * n
        for mask in range(1 << n):
            a = [(mask >> t) & 1 for t in range(n)]
            u = reconstruct(a, ones)
            want = [1 ^ a[(t - 1) % n] for t in range(n)]
            if u != want:
                return {"ok": False, "n": n, "mask": mask}
            n_exh += 1
    rng = random.Random(11)
    n_rand = 0
    for n in (12, 16, 24, 32):
        ones = [1] * n
        for _ in range(40):
            a = [rng.randint(0, 1) for _ in range(n)]
            u = reconstruct(a, ones)
            want = [1 ^ a[(t - 1) % n] for t in range(n)]
            if u != want:
                return {"ok": False, "n": n, "trial": True}
            n_rand += 1
    # all-1s yields 0 (ident-0 of A=B)
    if reconstruct([1, 1, 1, 1], [1, 1, 1, 1]) != [0, 0, 0, 0]:
        return {"ok": False, "ones": True}
    return {"ok": True, "n_exh": n_exh, "n_rand": n_rand}


def otype_n3_is_rot() -> dict:
    """O-type reconstruct(T,1) = rot^{n0-1}(T) for every n0=1..12."""
    rows: dict[int, int] = {}
    for n0 in range(1, 13):
        L = 2 * n0
        ones = [1] * L
        n = 0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            u = reconstruct(t, ones)
            if u != rot(t, n0 - 1):
                return {"ok": False, "n0": n0, "mask": mask}
            if twocopy_type(u) != "O":
                return {"ok": False, "n0": n0, "type": True}
            n += 1
        rows[n0] = n
    return {"ok": True, "rows": rows}


def reconstruct_zero() -> dict:
    """reconstruct(0,T)=1 for every nonzero T, length 1..10."""
    n_exh = 0
    for n in range(1, 11):
        z = [0] * n
        ones = [1] * n
        if reconstruct(z, z) is not None:
            return {"ok": False, "n": n, "zero": True}
        for mask in range(1, 1 << n):
            t = [(mask >> i) & 1 for i in range(n)]
            if reconstruct(z, t) != ones:
                return {"ok": False, "n": n, "mask": mask}
            n_exh += 1
    return {"ok": True, "n_exh": n_exh}


def gap_is_reconstruct_ones_S() -> dict:
    """reconstruct(1,S) = gap-parity(S) for every nonzero S, n=1..10."""
    n_exh = 0
    n_iso = 0
    for n in range(1, 11):
        ones = [1] * n
        for mask in range(1, 1 << n):
            s = [(mask >> i) & 1 for i in range(n)]
            u = reconstruct(ones, s)
            g = gap_parity(s)
            if u != g:
                return {"ok": False, "n": n, "mask": mask}
            # NOR recurrence
            for t in range(n):
                nxt = 0 if (s[t] or u[t]) else 1
                if u[(t + 1) % n] != nxt:
                    return {"ok": False, "n": n, "nor": True}
            # isolated 1s: even back-dist at t forces odd at t+1
            for t in range(n):
                if u[t] == 1 and u[(t + 1) % n] != 0:
                    return {"ok": False, "n": n, "iso": True}
                n_iso += int(u[t] == 1)
            n_exh += 1
    rng = random.Random(13)
    n_rand = 0
    for n in (12, 16, 24, 32):
        ones = [1] * n
        for _ in range(40):
            s = [rng.randint(0, 1) for _ in range(n)]
            if not any(s):
                s[0] = 1
            u = reconstruct(ones, s)
            if u != gap_parity(s):
                return {"ok": False, "n": n, "trial": True}
            n_rand += 1
    return {"ok": True, "n_exh": n_exh, "n_rand": n_rand, "n_iso": n_iso}


def f_inverse() -> dict:
    """inv_A(B, reconstruct(A,B)) = A whenever B is not 0, n=1..8."""
    n_exh = 0
    for n in range(1, 9):
        for am in range(1 << n):
            a = [(am >> t) & 1 for t in range(n)]
            for bm in range(1, 1 << n):
                b = [(bm >> t) & 1 for t in range(n)]
                u = reconstruct(a, b)
                if u is None or inv_A(b, u) != a:
                    return {"ok": False, "n": n}
                n_exh += 1
    return {"ok": True, "n_exh": n_exh}


def pred_ending() -> dict:
    """Two steps before ident-0: D(W), W then W, W then W, 0."""
    w = [int(c) for c in PRED32]
    dw = deriv(w)
    z = [0] * 32
    u = bits(U32)
    ones = [1] * 32
    n3 = reconstruct(u, ones)
    n4 = reconstruct(ones, n3)
    ok = (
        reconstruct(w, w) == z
        and reconstruct(dw, w) == w
        and inv_A(w, w) == dw
        and n3 == rot(u, 15)
        and n4 == gap_parity(n3)
        and twocopy_type(n3) == "O"
        and twocopy_type(n4) == "N"
        and xorcat(w) == 0
        and PRED32 != U32
    )
    return {
        "ok": ok,
        "n3_is_rot15_U": n3 == rot(u, 15),
        "n4_is_gap_n3": n4 == gap_parity(n3),
        "inv_WW_is_DW": inv_A(w, w) == dw,
    }


def bits(s: str) -> list[int]:
    return [int(c) for c in s]


def n16_landing() -> dict:
    """extra >= 414990 > 2^18 so packed >= 414990 sits in k>=18."""
    e = EXTRA414990
    a_e = annulus(e)
    rows: dict[str, dict] = {}
    for k in range(0, 22):
        img = image_one_annulus(k, e)
        rows[str(k)] = {
            "ok": img["ok"],
            "k_lo": img["k_lo"],
            "k_hi": img["k_hi"],
            "lo": img["lo"],
            "hi": img["hi"],
        }
    le15 = all(rows[str(k)]["ok"] and rows[str(k)]["k_lo"] == 18 for k in range(0, 16))
    k16 = rows["16"]
    k17 = rows["17"]
    k18 = rows["18"]
    k19 = rows["19"]
    ok = (
        e == 414990
        and e > (1 << 18)
        and e <= (1 << 19)
        and a_e == 18
        and le15
        and k16["k_lo"] == 18
        and k16["k_hi"] == 19
        and not k16["ok"]
        and k17["ok"]
        and k17["k_lo"] == 19
        and k18["ok"]
        and k18["k_lo"] == 19
        and k19["k_lo"] == 19
        and k19["k_hi"] == 20
        and not k19["ok"]
        and rows["0"]["lo"] == e + 1
    )
    return {
        "ok": ok,
        "extra": e,
        "annulus_extra": a_e,
        "origin_le15_k18": le15,
        "k16_split": [k16["k_lo"], k16["k_hi"]],
        "k17_k18_only19": k17["k_lo"] == 19 and k18["k_lo"] == 19,
        "rows": {k: {kk: rows[k][kk] for kk in ("ok", "k_lo", "k_hi")} for k in rows},
    }


def prefixes() -> dict:
    ep = json.loads(EP_JSON.read_text())
    et = json.loads(ET_JSON.read_text())
    ok = (
        ep["checks"]["all_ok"]
        and ep["n16"]["min_extra"] == EXTRA414990
        and ep["n16"]["n_hit"] == N_FAM
        and ep["n16"]["n_none"] == N_NONE
        and ep["n16"]["hits"]["414990"]["odd"] == 0
        and et["checks"]["all_ok"]
        and et["consecutive_equal"]["Tstar"]["zero"] == EXTRA414990
        and et["consecutive_equal"]["Tstar"]["eq"] == EXTRA414990 - 1
        and et["verdict"]["prize"] == "unsolved"
        and T_STAR in FAM414990
        and len(FAM414990) == N_FAM
    )
    return {"ok": ok}


def self_checks(
    c20,
    ones: dict,
    otype: dict,
    zero: dict,
    gap: dict,
    inv: dict,
    pred: dict,
    land: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ones["ok"] and otype["ok"] and zero["ok"] and gap["ok"]
    assert inv["ok"] and pred["ok"] and land["ok"] and pref["ok"]
    assert otype["rows"][12] == 1 << 12
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ones = reconstruct_ones()
    otype = otype_n3_is_rot()
    zero = reconstruct_zero()
    gap = gap_is_reconstruct_ones_S()
    inv = f_inverse()
    pred = pred_ending()
    land = n16_landing()
    pref = prefixes()
    checks = self_checks(c20, ones, otype, zero, gap, inv, pred, land, pref)
    dump = {
        "cycle": "EU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "ones": {k: ones[k] for k in ones if k != "ok"},
        "otype_n3": {"n0_1_12": otype["rows"]},
        "zero": {k: zero[k] for k in zero if k != "ok"},
        "gap": {k: gap[k] for k in gap if k != "ok"},
        "inverse": {k: inv[k] for k in inv if k != "ok"},
        "pred_ending": {k: pred[k] for k in pred if k != "ok"},
        "n16_land": {k: land[k] for k in land if k != "ok"},
        "lemmas": {
            "reconstruct_A_ones_is_rot_not": True,
            "otype_n3_is_rot_n0_minus_1": True,
            "reconstruct_0_T_is_ones": True,
            "reconstruct_ones_S_is_gap_parity": True,
            "F_inverse_A_from_BU": True,
            "ident0_ending_DW_W_W_0": True,
            "n16_ident0_packed_ge_414990": True,
            "n16_ident0_in_k_ge_18": True,
            "n16_ident0_in_k_le_17": False,
            "n16_ident0_never_in_k18": False,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "reconstruct_A_ones_is_rot_not": "LEMMA",
            "otype_n3_is_rot_n0_minus_1": "LEMMA",
            "reconstruct_0_T_is_ones": "LEMMA",
            "reconstruct_ones_S_is_gap_parity": "LEMMA",
            "F_inverse_A_from_BU": "LEMMA",
            "ident0_ending_DW_W_W_0": "LEMMA",
            "n16_ident0_in_k_ge_18": "LEMMA",
            "n16_ident0_in_k_le_17": "KILLED",
            "n16_ident0_never_in_k18": "KILLED",
            "no_closed_form_reconstruct_T_ones": "KILLED",
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
    print("n16_land", {k: land[k] for k in land if k in ("extra", "annulus_extra", "origin_le15_k18", "k16_split", "k17_k18_only19")})


if __name__ == "__main__":
    main()
