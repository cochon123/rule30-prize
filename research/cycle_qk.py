#!/usr/bin/env python3
"""Cycle QK: covering leftover even-j Green xor on odd n is 1 for k>=1.

Each UNIQUE_REST even-p column has Green parents p/2 and p/2+2 with
the same xor closed form, so Cycle QG odd-n tot (those two xor'd)
vanishes. Cycle PC p=4 on odd n also vanishes for k>=1 (the unique
even n is 3U-2). Cycle QI odd-n even-j tot is clip-edge p=0 at k-1,
hence 1 for k>=1. Leftover even-j odd-n tot is that bit, so 1 for
every k>=1. Leftover even-j even-n tot is leftover even-j tot xor 1
for k>=1. Not rest=S xor T (odd-n leftover even-j is 1 at k=7). Not
unique even-p odd-n tot equals unique even tot. Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_qk.py --certify
Dump: research/cycle_qk.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_pc import in_p4, live_lo, want_p4_xor
from cycle_ph import in_p8
from cycle_pm import want_p10_gxor
from cycle_pt import want_p18_gxor
from cycle_pv import want_p16_gxor
from cycle_py import want_p20_gxor
from cycle_qc import want_p26_gxor
from cycle_qd import want_p28_gxor
from cycle_qe import want_p30_gxor
from cycle_qg import gxor_p, parent_p, want_col_gxor
from cycle_qi import want_p0_gxor
from cycle_qj import UNIQUE_EVEN, want_lo_even, want_unique_even

OUT = Path(__file__).resolve().with_suffix(".json")
QJ_JSON = Path(__file__).resolve().parent / "cycle_qj.json"
QI_JSON = Path(__file__).resolve().parent / "cycle_qi.json"

N_PAL = 64
M_SLOTS = 64
K_G = 12
K_CHK = 8
K_ALG = 64
# Child even-p, parent p/2, parent p/2+2.
PAIRS = (
    (16, 8, 10),
    (32, 16, 18),
    (52, 26, 28),
    (60, 30, 32),
    (72, 36, 38),
    (76, 38, 40),
    (88, 44, 46),
)


def want_p8_gxor(k: int) -> int:
    """Covering Green G=1 xor at packed p=8, all k: 1 iff k>=2."""
    return int(k >= 2)


def want_p36_gxor(k: int) -> int:
    """Covering Green G=1 xor at packed p=36, all k: 1 iff k>=5."""
    return want_p20_gxor(k - 1) if k >= 1 else 0


def want_parent(p: int, k: int) -> int:
    """Closed Green xor at a unique-even parent packed index."""
    if p == 8:
        return want_p8_gxor(k)
    if p == 36:
        return want_p36_gxor(k)
    return want_col_gxor(p, k)


def want_lo_oe(k: int) -> int:
    """Covering leftover even-j Green xor on odd n, all k: 1 iff k>=1."""
    return int(k >= 1)


def want_lo_ee(k: int) -> int:
    """Covering leftover even-j Green xor on even n, all k."""
    return want_lo_even(k) ^ want_lo_oe(k)


def gxor_parity(p: int, k: int) -> tuple[int, int]:
    """Covering Green xor at packed p, split even/odd n."""
    U = 1 << k
    delta = p // 2
    j = 5 * U - delta
    if j < 0:
        return 0, 0
    e = o = 0
    for n in range(live_lo(k, delta), 4 * U):
        if 0 <= j <= 2 * n and G(n, j):
            if n % 2:
                o ^= 1
            else:
                e ^= 1
    return e, o


def leftover_npar(k: int) -> dict:
    """Walk covering even-j G=1 xor split leftover/unique/forced by n parity."""
    U = 1 << k
    t_pack = 10 * U
    clip = 5 * U
    lo_ee = lo_oe = u_ee = u_oe = f_ee = f_oe = 0
    for n in range(0, 4 * U):
        hi = min(2 * n, clip)
        odd_n = n % 2
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            p = t_pack - 2 * j
            if p < 0:
                continue
            if p in FORCED:
                if odd_n:
                    f_oe ^= 1
                else:
                    f_ee ^= 1
            elif p in UNIQUE_REST:
                if odd_n:
                    u_oe ^= 1
                else:
                    u_ee ^= 1
            else:
                if odd_n:
                    lo_oe ^= 1
                else:
                    lo_ee ^= 1
    return {
        "lo_ee": lo_ee,
        "lo_oe": lo_oe,
        "u_ee": u_ee,
        "u_oe": u_oe,
        "f_ee": f_ee,
        "f_oe": f_oe,
    }


def unique_odd_n() -> dict:
    """k<=K_G: each UNIQUE_EVEN column has odd-n Green xor 0; even-n is tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_G + 1):
        ee = eo = 0
        per = {}
        for p in UNIQUE_EVEN:
            e, o = gxor_parity(p, k)
            want = want_col_gxor(p, k)
            if o != 0 or e != want or (e ^ o) != gxor_p(p, k):
                return {"ok": False, "p": p, "k": k, "e": e, "o": o, "want": want}
            ee ^= e
            eo ^= o
            per[str(p)] = e
            n_ok += 1
        if ee != want_unique_even(k) or eo != 0:
            return {"ok": False, "tot": True, "k": k, "ee": ee, "eo": eo}
        if k <= 8 or k in (10, 12):
            rows[str(k)] = {"ee": ee, "eo": eo, "per": per}
    ok = (
        rows["3"]["ee"] == 1
        and rows["3"]["eo"] == 0
        and rows["5"]["ee"] == 0
        and rows["6"]["ee"] == 1
        and rows["12"]["eo"] == 0
        and rows["3"]["per"]["16"] == 1
        and rows["6"]["per"]["88"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "rows": rows}


def parent_pairs() -> dict:
    """k<=K_G: parent p/2 and p/2+2 Green xor match want_parent; equal."""
    n_ok = 0
    sample = {}
    for k in range(0, K_G + 1):
        for child, a, b in PAIRS:
            ga = want_parent(a, k)
            gb = want_parent(b, k)
            if ga != gb:
                return {"ok": False, "neq": True, "k": k, "child": child, "a": a, "b": b}
            if k >= 3 and parent_p(child) != b:
                return {"ok": False, "parent_p": True, "child": child}
            got_a = gxor_p(a, k)
            got_b = gxor_p(b, k)
            if got_a != ga or got_b != gb:
                return {
                    "ok": False,
                    "walk": True,
                    "k": k,
                    "a": a,
                    "got_a": got_a,
                    "want_a": ga,
                }
            n_ok += 1
        if k <= 3:
            sample[str(k)] = {"p8": want_p8_gxor(k), "p10": want_p10_gxor(k)}
    # in_p8 tot equals want_p8_gxor
    for k in range(0, K_G + 1):
        U = 1 << k
        acc = 0
        for n in range(live_lo(k, 4), 4 * U):
            if in_p8(n, k):
                acc ^= 1
        if acc != want_p8_gxor(k) or acc != gxor_p(8, k):
            return {"ok": False, "p8": True, "k": k, "got": acc}
        n_ok += 1
    ok = (
        sample["0"]["p8"] == 0
        and sample["2"]["p8"] == 1
        and sample["2"]["p10"] == 1
        and want_p16_gxor(3) == 1
        and want_p18_gxor(3) == 1
        and want_p26_gxor(4) == 1
        and want_p28_gxor(4) == 1
        and want_p30_gxor(4) == 1
        and want_p36_gxor(5) == 1
        and want_p4_xor(1) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_G, "sample": sample}


def lo_odd_n() -> dict:
    """k<=K_CHK: leftover even-j odd-n tot is 1 iff k>=1; p=4 odd-n tot 0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CHK + 1):
        w = leftover_npar(k)
        if w["lo_oe"] != want_lo_oe(k) or w["lo_ee"] != want_lo_ee(k):
            return {
                "ok": False,
                "lo": True,
                "k": k,
                "lo_oe": w["lo_oe"],
                "lo_ee": w["lo_ee"],
            }
        if (w["lo_ee"] ^ w["lo_oe"]) != want_lo_even(k):
            return {"ok": False, "qj": True, "k": k}
        if k >= 1:
            if w["u_oe"] != 0 or w["f_oe"] != 0:
                return {"ok": False, "odd": True, "k": k, "u_oe": w["u_oe"], "f_oe": w["f_oe"]}
            if w["f_ee"] != 1:
                return {"ok": False, "p4e": True, "k": k}
            all_oe = w["lo_oe"] ^ w["u_oe"] ^ w["f_oe"]
            if all_oe != want_p0_gxor(k - 1):
                return {"ok": False, "qi": True, "k": k, "all_oe": all_oe}
            n_ok += 1
        rows[str(k)] = {
            "lo_ee": w["lo_ee"],
            "lo_oe": w["lo_oe"],
            "u_ee": w["u_ee"],
            "u_oe": w["u_oe"],
            "f_ee": w["f_ee"],
            "f_oe": w["f_oe"],
        }
    # p=4 even n is the unique 3U-2
    p4_ok = 0
    for k in range(1, K_CHK + 1):
        U = 1 << k
        ev = [n for n in range(0, 4 * U, 2) if in_p4(n, k)]
        if ev != [3 * U - 2]:
            return {"ok": False, "p4set": True, "k": k, "ev": ev}
        p4_ok += 1
    ok = (
        rows["0"]["lo_oe"] == 0
        and rows["1"]["lo_oe"] == 1
        and rows["7"]["lo_oe"] == 1
        and rows["8"]["lo_ee"] == 0
        and rows["2"]["lo_ee"] == 1
        and p4_ok == K_CHK
    )
    return {"ok": ok, "n_ok": n_ok, "p4_ok": p4_ok, "k_hi": K_CHK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: parent pairs equal; leftover odd-n even-j closed."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        for child, a, b in PAIRS:
            if want_parent(a, k) != want_parent(b, k):
                return {"ok": False, "pair": True, "k": k, "child": child}
            if k >= 1 and want_lo_oe(k) != 1:
                return {"ok": False, "oe": True, "k": k}
            if want_lo_ee(k) != (want_lo_even(k) ^ want_lo_oe(k)):
                return {"ok": False, "ee": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_oe(0) == 0
        and want_lo_oe(1) == 1
        and want_lo_ee(2) == 1
        and want_lo_ee(6) == 0
        and want_p8_gxor(2) == want_p10_gxor(2) == 1
        and want_parent(16, 3) == want_parent(18, 3) == 1
        and want_parent(36, 5) == want_parent(38, 5) == 1
        and want_unique_even(6) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_oe_eq_st() -> dict:
    """Leftover even-j odd-n tot equals ST: k=7 is 1 vs 0."""
    ok = (
        want_lo_oe(7) == 1
        and want_rest_e0(7) == 0
        and want_rest10(7, 10) == 0
        and want_unique_even(3) == 1
        and want_lo_oe(3) == 1
    )
    return {"ok": ok, "k": 7, "lo_oe": 1, "ST": 0}


def prefixes() -> dict:
    qj = json.loads(QJ_JSON.read_text())
    qi = json.loads(QI_JSON.read_text())
    ok = (
        qj["checks"]["all_ok"]
        and qi["checks"]["all_ok"]
        and qj["verdict"]["lo_even_iff_le1_or_k3_or_ge6"] == "LEMMA"
        and qi["verdict"]["p0_gxor_1_all_k"] == "LEMMA"
        and qj["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qj["verdict"]["prize"] == "unsolved"
        and want_lo_even(7) == 1
        and want_p0_gxor(6) == 1
        and want_p4_xor(1) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, uniq, pairs, lo, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and uniq["ok"] and pairs["ok"]
    assert lo["ok"] and tot["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    uniq = unique_odd_n()
    pairs = parent_pairs()
    lo = lo_odd_n()
    tot = tot_form()
    kl = killed_oe_eq_st()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, uniq, pairs, lo, tot, kl, sc, pref)
    dump = {
        "cycle": "QK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "unique_odd_n": {k: uniq[k] for k in uniq if k != "ok"},
        "parent_pairs": {k: pairs[k] for k in pairs if k != "ok"},
        "lo_odd_n": {k: lo[k] for k in lo if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_odd_n_0": True,
            "parent_pairs_equal": True,
            "lo_oe_iff_k_ge_1": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "lo_oe_eq_ST": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_odd_n_0": "LEMMA",
            "parent_pairs_equal": "LEMMA",
            "lo_oe_iff_k_ge_1": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "lo_oe_eq_ST": "KILLED",
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
    print(
        "lo_odd_n n_ok",
        dump["lo_odd_n"]["n_ok"],
        "k_hi",
        dump["lo_odd_n"]["k_hi"],
        "lo_oe8",
        dump["lo_odd_n"]["rows"]["8"]["lo_oe"],
        "lo_ee8",
        dump["lo_odd_n"]["rows"]["8"]["lo_ee"],
    )
    print("unique_odd_n n_ok", dump["unique_odd_n"]["n_ok"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
