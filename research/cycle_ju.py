#!/usr/bin/env python3
"""Cycle JU: cob-stretch commutes with reverse, so even-n dual iso1_even is reverse.

freshman_lift5(iso3_rev(three), odd parent) equals lift5_rev of the
cob-stretch. Dual of even-n iso1_even is therefore lift5_rev, recovering
JE on even n from JP+JI. Cob does not fail to commute; dual of 00011
does not stay 00011; dual iso1_even is the reverse. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ju.py --certify
Dump: research/cycle_ju.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_ir import isolated_one
from cycle_je import dual_iso_start, lift5_rev
from cycle_jf import ISO3_001, ISO3_010, ISO3_100, ISO3_111, freshman_lift5
from cycle_jh import iso3_even
from cycle_ji import LIFT1_HI, LIFT1_LO, LIFT1_MID_EVEN, LIFT1_MID_ODD, iso1_even
from cycle_jp import iso3_rev
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
JT_JSON = Path(__file__).resolve().parent / "cycle_jt.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def cob_lift5(three):
    """Odd-parent cob-stretch of an iso3 window onto LIFT1."""
    if three is None:
        return None
    return freshman_lift5(three, False)


def cob_rev_table() -> dict:
    """n<64: cob commutes with reverse; even dual iso1_even is lift5_rev."""
    for three in (ISO3_001, ISO3_010, ISO3_100, ISO3_111):
        if cob_lift5(iso3_rev(three)) != lift5_rev(cob_lift5(three)):
            return {"ok": False, "commute": True, "three": list(three)}
    if cob_lift5(ISO3_001) != LIFT1_LO or cob_lift5(ISO3_100) != LIFT1_HI:
        return {"ok": False, "ends": True}
    if cob_lift5(ISO3_010) != LIFT1_MID_ODD or cob_lift5(ISO3_111) != LIFT1_MID_EVEN:
        return {"ok": False, "mids": True}
    n_iso = n_seed = n_even = n_pal = n_swap = 0
    n_lo = n_hi = n_mid_odd = n_mid_even = 0
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if not isolated_one(n, j):
                continue
            n_iso += 1
            if n == 0:
                n_seed += 1
                continue
            if n % 2:
                continue
            n_even += 1
            five = iso1_even(n, j)
            five2 = iso1_even(n, dual_iso_start(n, j))
            pred = lift5_rev(five)
            cobpred = cob_lift5(iso3_rev(iso3_even(n, j)))
            if five2 != pred or five2 != cobpred or five != cob_lift5(iso3_even(n, j)):
                return {
                    "ok": False,
                    "miss": True,
                    "n": n,
                    "j": j,
                    "five": list(five) if five else None,
                    "five2": list(five2) if five2 else None,
                }
            if five == pred:
                n_pal += 1
            else:
                n_swap += 1
            if five == LIFT1_LO:
                n_lo += 1
            elif five == LIFT1_HI:
                n_hi += 1
            elif five == LIFT1_MID_ODD:
                n_mid_odd += 1
            else:
                n_mid_even += 1
    ok = (
        n_iso == 461
        and n_seed == 1
        and n_even == 415
        and n_pal == 185
        and n_swap == 230
        and n_lo == 115
        and n_hi == 115
        and n_mid_odd == 141
        and n_mid_even == 44
        and iso1_even(2, 4) == lift5_rev(iso1_even(2, 0)) == LIFT1_HI
    )
    return {
        "ok": ok,
        "n_iso": n_iso,
        "n_seed": n_seed,
        "n_even": n_even,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
    }


def _walk_rev(k: int, q: int) -> dict:
    """Dual-in-support even iso1_even reverse via cob; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_iso = n_even = n_dual = 0
    n_pal = n_swap = n_lo = n_hi = n_mid_odd = n_mid_even = 0
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            bits = set()
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                bits.add(j)
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in bits:
                if not isolated_one(n, j):
                    continue
                n_iso += 1
                if n % 2 or n <= 0:
                    continue
                n_even += 1
                five = iso1_even(n, j)
                j2 = dual_iso_start(n, j)
                if j2 not in bits:
                    continue
                five2 = iso1_even(n, j2)
                pred = lift5_rev(five)
                cobpred = cob_lift5(iso3_rev(iso3_even(n, j)))
                if five2 != pred or five2 != cobpred:
                    return {
                        "ok": False,
                        "rev": True,
                        "k": k,
                        "n": n,
                        "j": j,
                        "j2": j2,
                    }
                n_dual += 1
                if five == pred:
                    n_pal += 1
                else:
                    n_swap += 1
                if five == LIFT1_LO:
                    n_lo += 1
                elif five == LIFT1_HI:
                    n_hi += 1
                elif five == LIFT1_MID_ODD:
                    n_mid_odd += 1
                else:
                    n_mid_even += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_even": n_even,
        "n_dual": n_dual,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "xor_j": xor_j,
    }


def cob_rev_cover() -> dict:
    """Dual-in-support cob-reverse on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_iso = n_even = n_dual = 0
    n_pal = n_swap = n_lo = n_hi = n_mid_odd = n_mid_even = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_rev(k, q)
            if not w.get("ok"):
                return w
            if q == 6:
                want = hf["j6_j_index"]["rows"][str(k)]["xor_odd"]
                if w["xor_j"] != want:
                    return {"ok": False, "xor": True, "k": k, "got": w["xor_j"], "want": want}
            else:
                want = hg["j10_j18_index"]["rows"][str(k)]["xor_odd10"]
                if w["xor_j"] != want:
                    return {
                        "ok": False,
                        "xor10": True,
                        "k": k,
                        "got": w["xor_j"],
                        "want": want,
                    }
            n_ok += w["n_ok"]
            n_g1 += w["n_g1"]
            n_iso += w["n_iso"]
            n_even += w["n_even"]
            n_dual += w["n_dual"]
            n_pal += w["n_pal"]
            n_swap += w["n_swap"]
            n_lo += w["n_lo"]
            n_hi += w["n_hi"]
            n_mid_odd += w["n_mid_odd"]
            n_mid_even += w["n_mid_even"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_even": w["n_even"],
                "n_dual": w["n_dual"],
                "n_pal": w["n_pal"],
                "n_swap": w["n_swap"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_iso == 7785
        and n_even == 7030
        and n_dual == 5833
        and n_pal == 2537
        and n_swap == 3296
        and n_lo == 1648
        and n_hi == 1648
        and n_mid_odd == 1935
        and n_mid_even == 602
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_iso": n_iso,
        "n_even": n_even,
        "n_dual": n_dual,
        "n_pal": n_pal,
        "n_swap": n_swap,
        "n_lo": n_lo,
        "n_hi": n_hi,
        "n_mid_odd": n_mid_odd,
        "n_mid_even": n_mid_even,
        "rows": rows,
    }


def killed_no_commute() -> dict:
    """Cob does not commute with reverse: cob(rev(001))=rev(cob(001))=11000."""
    three = ISO3_001
    five = cob_lift5(three)
    five2 = cob_lift5(iso3_rev(three))
    ok = (
        five == LIFT1_LO
        and five2 == lift5_rev(five) == LIFT1_HI
        and five2 != five
    )
    return {
        "ok": ok,
        "three": list(three),
        "five": list(five),
        "five2": list(five2),
    }


def killed_lo_stays() -> dict:
    """Dual of 00011 stays 00011: G(2,0) dualizes to 11000."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    five = iso1_even(n, j)
    five2 = iso1_even(n, j2)
    ok = (
        five == LIFT1_LO
        and five2 == lift5_rev(five) == LIFT1_HI
        and five2 != LIFT1_LO
        and p >= 4
        and p2 >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def killed_not_rev() -> dict:
    """Dual iso1_even is not reverse: same first witness, 11000=rev(00011)."""
    k, s, n, j, p, p2 = 1, 15, 2, 0, 20, 12
    j2 = dual_iso_start(n, j)
    five = iso1_even(n, j)
    five2 = iso1_even(n, j2)
    ok = five2 == lift5_rev(five) and p >= 4 and p2 >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "j2": j2,
        "p": p,
        "p2": p2,
        "five": list(five),
        "five2": list(five2),
    }


def prefixes() -> dict:
    jt = json.loads(JT_JSON.read_text())
    ok = (
        jt["checks"]["all_ok"]
        and jt["verdict"]["pair_dbl_rev"] == "LEMMA"
        and jt["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert cob_lift5(iso3_rev(ISO3_001)) == lift5_rev(cob_lift5(ISO3_001))
    assert iso1_even(2, 4) == lift5_rev(iso1_even(2, 0))
    assert cob_lift5(ISO3_010) == LIFT1_MID_ODD
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = cob_rev_table()
    sc = cob_rev_cover()
    k0 = killed_no_commute()
    k1 = killed_lo_stays()
    k2 = killed_not_rev()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "JU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cob_rev_table": {k: rt[k] for k in rt if k != "ok"},
        "cob_rev_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_no_commute": {k: k0[k] for k in k0 if k != "ok"},
        "killed_lo_stays": {k: k1[k] for k in k1 if k != "ok"},
        "killed_not_rev": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "cob_commute_rev": True,
            "iso1_even_dual_rev": True,
            "covering_cob_rev": True,
            "no_commute": False,
            "lo_stays": False,
            "not_rev": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cob_commute_rev": "LEMMA",
            "iso1_even_dual_rev": "LEMMA",
            "covering_cob_rev": "LEMMA",
            "no_commute": "KILLED",
            "lo_stays": "KILLED",
            "not_rev": "KILLED",
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
    print("cob_rev_table", dump["cob_rev_table"])
    cov = dump["cob_rev_cover"]
    print(
        "cob_rev_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_even",
        cov["n_even"],
        "n_dual",
        cov["n_dual"],
        "n_pal",
        cov["n_pal"],
        "n_swap",
        cov["n_swap"],
    )
    print("killed_no_commute", dump["killed_no_commute"])
    print("killed_lo_stays", dump["killed_lo_stays"])
    print("killed_not_rev", dump["killed_not_rev"])


if __name__ == "__main__":
    main()
