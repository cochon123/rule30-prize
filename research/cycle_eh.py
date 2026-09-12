#!/usr/bin/env python3
"""Cycle EH: 52809-family two-even split; prize is not the 72177 fork.

Every even-52809 n0=8 word has a second even ident-0 at extra 57888
(12 words) or 72177 (4 words). The six extra-87468 odds are exactly a
subset of the 57888 group; prize T0=00000110 is in that group and has
no odd in 131000 extras. First-even a on prize T0 is Cycle DF's k=15
predecessor 1100001100010100; packed image 400+52809-1=53208. Extra
57888 from k=8 lands in k=15; extra 72177 lands in k=16 (packed image
72576). Kills: prize T0 hits the 72177/Rowland-adjacent fork. Do not
identify 72576 with Rowland 72577; do not claim packed 58287 without a
high-half dump; do not claim a closed form for 57888/72177/87468. Not
a prize claim.

Run: python3 research/cycle_eh.py --certify
Dump: research/cycle_eh.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct, xorcat
from cycle_df import K15_A, K15_EVEN_P
from cycle_dn import census
from cycle_ee import image_one_annulus
from cycle_ef import EXTRA52809, EXTRA87468, MAX_FIRST, MAX_ODD, PRIZE8

OUT = Path(__file__).resolve().with_suffix(".json")
EG_JSON = Path(__file__).resolve().parent / "cycle_eg.json"
DF_JSON = Path(__file__).resolve().parent / "cycle_df.json"
DE_JSON = Path(__file__).resolve().parent / "cycle_de.json"
EXTRA57888 = 57888
EXTRA72177 = 72177
IMG57888 = 400 + EXTRA57888 - 1  # 58287
IMG72177 = 400 + EXTRA72177 - 1  # 72576


def bits(mask: int, n: int = 8) -> str:
    return "".join(str((mask >> i) & 1) for i in range(n))


def ident0_events(T0: list[int], max_extra: int) -> list[tuple[int, str, str]]:
    """Ident-0 extras through max_extra, continuing even via unfold."""
    n0 = len(T0)
    T = T0 + [x ^ 1 for x in T0]
    L = 2 * n0
    seqs: dict[int, list[int]] = {0: [0] * L, 1: T, 2: [1] * L}
    ev: list[tuple[int, str, str]] = []
    for cur in range(3, 3 + max_extra):
        a, b = seqs[cur - 2], seqs[cur - 1]
        if all(x == 0 for x in b):
            sm = xorcat(a)
            kind = "odd" if sm == 1 else "even"
            astr = "".join(map(str, a))
            ev.append((cur, kind, astr))
            if sm == 1:
                return ev
            u = [0] * L
            for t in range(L - 1):
                u[t + 1] = a[t] ^ u[t]
            seqs[cur] = u
        else:
            u = reconstruct(a, b)
            if u is None:
                ev.append((cur, "wrap", "".join(map(str, a))))
                return ev
            seqs[cur] = u
    return ev


def family_events() -> dict:
    """16-word 52809 family: second even 57888 or 72177; odds only at 87468."""
    c = census(8, MAX_FIRST)
    fam = sorted(i for i, (e, sm) in c["first"].items() if e == EXTRA52809)
    if len(fam) != 16:
        return {"ok": False, "n": len(fam)}
    by2: dict[int, list[str]] = defaultdict(list)
    odd_of: dict[str, int | None] = {}
    prize_ev: list | None = None
    for m in fam:
        s = bits(m)
        ev = ident0_events([int(ch) for ch in s], MAX_ODD)
        if not ev or ev[0][0] != EXTRA52809 or ev[0][1] != "even":
            return {"ok": False, "T0": s, "ev0": ev[:1]}
        if len(ev) < 2 or ev[1][1] != "even":
            return {"ok": False, "T0": s, "ev": ev}
        e2 = ev[1][0]
        if e2 not in (EXTRA57888, EXTRA72177):
            return {"ok": False, "T0": s, "e2": e2}
        by2[e2].append(s)
        odd = next((cur for cur, kind, _ in ev[2:] if kind == "odd"), None)
        wrap = any(kind == "wrap" for _, kind, _ in ev)
        if wrap:
            return {"ok": False, "wrap": s}
        if odd not in (EXTRA87468, None):
            return {"ok": False, "T0": s, "odd": odd}
        if e2 == EXTRA72177 and odd is not None:
            return {"ok": False, "72177_odd": s}
        odd_of[s] = odd
        if s == PRIZE8:
            prize_ev = ev
            if ev[0][2] != K15_A or e2 != EXTRA57888 or odd is not None:
                return {"ok": False, "prize": ev}
    if len(by2[EXTRA57888]) != 12 or len(by2[EXTRA72177]) != 4:
        return {"ok": False, "n2": {k: len(v) for k, v in by2.items()}}
    hit = sorted(s for s, o in odd_of.items() if o == EXTRA87468)
    if len(hit) != 6 or any(s not in by2[EXTRA57888] for s in hit):
        return {"ok": False, "hit": hit}
    if PRIZE8 not in by2[EXTRA57888] or odd_of[PRIZE8] is not None:
        return {"ok": False, "prize_group": True}
    return {
        "ok": True,
        "n57888": 12,
        "n72177": 4,
        "n87468": 6,
        "hit": hit,
        "g57888": sorted(by2[EXTRA57888]),
        "g72177": sorted(by2[EXTRA72177]),
        "prize_a": prize_ev[0][2] if prize_ev else None,
        "prize_e2": EXTRA57888,
    }


def landings() -> dict:
    rows = {
        "57888_from_8": image_one_annulus(8, EXTRA57888),
        "72177_from_8": image_one_annulus(8, EXTRA72177),
        "87468_from_8": image_one_annulus(8, EXTRA87468),
    }
    ok = (
        rows["57888_from_8"]["ok"]
        and rows["57888_from_8"]["k_lo"] == 15
        and rows["72177_from_8"]["ok"]
        and rows["72177_from_8"]["k_lo"] == 16
        and rows["87468_from_8"]["ok"]
        and rows["87468_from_8"]["k_lo"] == 16
        and 400 + EXTRA52809 - 1 == K15_EVEN_P
        and IMG57888 == 58287
        and IMG72177 == 72576
    )
    return {
        "ok": ok,
        "rows": rows,
        "img52809": K15_EVEN_P,
        "img57888": IMG57888,
        "img72177": IMG72177,
    }


def eg_prefix() -> dict:
    eg = json.loads(EG_JSON.read_text())
    df = json.loads(DF_JSON.read_text())
    de = json.loads(DE_JSON.read_text())
    ok = (
        eg["checks"]["all_ok"]
        and eg["family"]["n87468"] == 6
        and eg["family"]["n_none"] == 10
        and PRIZE8 in eg["family"]["miss"]
        and df["checks"]["all_ok"]
        and df["k15_even"]["p"] == K15_EVEN_P
        and df["k15_even"]["a"] == K15_A
        and de["checks"]["all_ok"]
        and de["even_high_n15"] == 2
    )
    return {"ok": ok}


def self_checks(c20, fam: dict, land: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fam["ok"] and land["ok"] and pref["ok"]
    assert fam["n57888"] == 12 and fam["n72177"] == 4 and fam["n87468"] == 6
    assert fam["prize_a"] == K15_A and PRIZE8 not in fam["g72177"]
    assert land["img52809"] == 53208 and land["img57888"] == 58287
    assert land["rows"]["72177_from_8"]["k_lo"] == 16
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fam = family_events()
    land = landings()
    pref = eg_prefix()
    checks = self_checks(c20, fam, land, pref)
    dump = {
        "cycle": "EH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "family": {
            "n57888": fam.get("n57888"),
            "n72177": fam.get("n72177"),
            "n87468": fam.get("n87468"),
            "hit": fam.get("hit"),
            "g72177": fam.get("g72177"),
            "prize_a": fam.get("prize_a"),
            "prize_e2": fam.get("prize_e2"),
        },
        "landings": {
            k: {kk: vv for kk, vv in row.items() if kk != "ok"}
            for k, row in land["rows"].items()
        },
        "packed_image": {
            "52809": land["img52809"],
            "57888": land["img57888"],
            "72177": land["img72177"],
        },
        "lemmas": {
            "all_52809_second_even_57888_or_72177": True,
            "87468_only_inside_57888_group": True,
            "prize_in_57888_group_no_odd_131000": True,
            "prize_first_even_a_is_K15_A": True,
            "extra57888_k8_lands_k15": True,
            "extra72177_k8_lands_k16": True,
            "prize_hits_72177_or_rowland_72577": False,
            "packed_second_k15_even_is_58287": None,
            "img72177_is_rowland_72577": False,
            "n57888_closed_form": None,
            "scar_87468_is_packed_87867_on_prize_T0": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "all_52809_second_even_57888_or_72177": "LEMMA",
            "87468_only_inside_57888_group": "LEMMA",
            "prize_in_57888_group_no_odd_131000": "LEMMA",
            "prize_first_even_a_is_K15_A": "LEMMA",
            "extra57888_k8_lands_k15": "LEMMA",
            "extra72177_k8_lands_k16": "LEMMA",
            "prize_hits_72177_or_rowland_72577": "KILLED",
            "packed_second_k15_even_is_58287": "PREFIX",
            "img72177_is_rowland_72577": "KILLED",
            "n57888_closed_form": "PREFIX",
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
    print("packed_image", dump["packed_image"])


if __name__ == "__main__":
    main()
