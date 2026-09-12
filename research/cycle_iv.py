#!/usr/bin/env python3
"""Cycle IV: G=1 Green neighbors are the core-slot IMAGE_ONES offset.

Odd n: (G(j+1), G(j-1)) is SLOT_NEIGH[r,d] from half_run_image.
Even n and the seed vanish to (0,0). g1_green4 is that pair as
(gp, 1-gp, 1, 1-gm). Even G=1 is not the odd-core green4; run-3
middle is not neighbors 11; same (r,d) is not parity-independent.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_iv.py --certify
Dump: research/cycle_iv.json
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
from cycle_ig import g1_green4
from cycle_ih import g_neigh
from cycle_ip import half_run_image
from cycle_is import IMAGE_ONES
from cycle_it import g1_core_slot, odd_core
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IU_JSON = Path(__file__).resolve().parent / "cycle_iu.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

SLOT_NEIGH = {
    (1, 0): (1, 0),
    (1, 1): (1, 1),
    (1, 2): (0, 1),
    (2, 0): (1, 0),
    (2, 1): (0, 1),
    (2, 3): (1, 0),
    (2, 4): (0, 1),
    (3, 0): (1, 0),
    (3, 1): (0, 1),
    (3, 3): (0, 0),
    (3, 5): (1, 0),
    (3, 6): (0, 1),
}

WANT_G4 = {
    (1, 0, 1, 1): 371,
    (1, 0, 1, 0): 141,
    (0, 1, 1, 0): 371,
    (0, 1, 1, 1): 461,
}

WANT_COV_G4 = {
    (1, 0, 1, 1): 6297,
    (1, 0, 1, 0): 2380,
    (0, 1, 1, 0): 6197,
    (0, 1, 1, 1): 7785,
}


def slot_neigh(n: int, j: int):
    """(G(j+1), G(j-1)) from the core slot; seed/even n vanish."""
    got = g1_core_slot(n, j)
    if got == "seed":
        return (0, 0)
    if got is None or got == "bad":
        return None
    _start, r, d = got
    if n % 2 == 0:
        return (0, 0)
    return SLOT_NEIGH[(r, d)]


def slot_green4(n: int, j: int):
    """g1_green4 from slot_neigh: (gp, 1-gp, 1, 1-gm)."""
    neigh = slot_neigh(n, j)
    if neigh is None:
        return None
    gp, gm = neigh
    return (gp, 1 - gp, 1, 1 - gm)


def _g4_key(g4: dict) -> dict:
    return {f"{a}{b}{c}{d}": g4[(a, b, c, d)] for a, b, c, d in sorted(WANT_G4)}


def neigh_table() -> dict:
    """n<64: G=1 neighbors equal slot_neigh; g1_green4 equals slot_green4."""
    n_g1 = n_hit = n_even = n_odd = n_seed = 0
    g4 = {k: 0 for k in WANT_G4}
    for r, offs in IMAGE_ONES.items():
        img = half_run_image(r)
        for d in offs:
            if (img[d + 2], img[d]) != SLOT_NEIGH[(r, d)]:
                return {"ok": False, "img": True, "r": r, "d": d}
    for n in range(0, 64):
        for j in range(0, 2 * n + 1):
            if G(n, j) == 0:
                continue
            n_g1 += 1
            if slot_neigh(n, j) != g_neigh(n, j):
                return {"ok": False, "neigh": True, "n": n, "j": j}
            got4 = slot_green4(n, j)
            if got4 != g1_green4(n, j):
                return {"ok": False, "g4": True, "n": n, "j": j}
            g4[got4] += 1
            got = g1_core_slot(n, j)
            if got == "seed":
                n_seed += 1
                continue
            n_hit += 1
            if n % 2 == 0:
                n_even += 1
            else:
                n_odd += 1
    ok = (
        n_g1 == 1344
        and n_hit == 1343
        and n_seed == 1
        and n_even == 415
        and n_odd == 928
        and g4 == WANT_G4
    )
    return {
        "ok": ok,
        "n_g1": n_g1,
        "n_hit": n_hit,
        "n_seed": n_seed,
        "n_even": n_even,
        "n_odd": n_odd,
        "g4": _g4_key(g4),
    }


def _walk_neigh(k: int, q: int) -> dict:
    """Slot neighbors on covering G=1; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_seed = 0
    g4 = {key: 0 for key in WANT_G4}
    xor_j = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if not G(n, j):
                    continue
                n_g1 += 1
                if packed:
                    xor_j ^= 1
                if slot_neigh(n, j) != g_neigh(n, j):
                    return {"ok": False, "neigh": True, "k": k, "n": n, "j": j}
                got4 = slot_green4(n, j)
                if got4 != g1_green4(n, j):
                    return {"ok": False, "g4": True, "k": k, "n": n, "j": j}
                g4[got4] += 1
                if g1_core_slot(n, j) == "seed":
                    n_seed += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_seed": n_seed,
        "g4": _g4_key(g4),
        "xor_j": xor_j,
        "_g4": g4,
    }


def neigh_cover() -> dict:
    """Slot neighbors on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_seed = 0
    g4 = {k: 0 for k in WANT_G4}
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_neigh(k, q)
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
            n_seed += w["n_seed"]
            for key in g4:
                g4[key] += w["_g4"][key]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_seed": w["n_seed"],
                "g4": w["g4"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_ok == 95821 and n_g1 == 22659 and n_seed == 14 and g4 == WANT_COV_G4
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_seed": n_seed,
        "g4": _g4_key(g4),
        "rows": rows,
    }


def killed_even_eq_core() -> dict:
    """Even G=1 has the odd-core green4: G(2,0) is 0111, core 1011."""
    k, s, n, j, p = 1, 7, 2, 0, 12
    core, v = odd_core(n)
    j2 = j >> v
    got = g1_green4(n, j)
    core4 = g1_green4(core, j2)
    ok = (
        n % 2 == 0
        and got == (0, 1, 1, 1)
        and core4 == (1, 0, 1, 1)
        and got != core4
        and got == slot_green4(n, j)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "green4": list(got),
        "core": list(odd_core(n)),
        "core_j": j2,
        "core_green4": list(core4),
    }


def killed_r3_mid_11() -> dict:
    """Run-3 middle has neighbors 11: G(3,3) is (0,0)."""
    k, s, n, j, p = 1, 5, 3, 3, 6
    got = g1_core_slot(n, j)
    neigh = g_neigh(n, j)
    ok = got == (0, 3, 3) and neigh == (0, 0) and neigh != (1, 1) and p >= 4
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "neigh": list(neigh),
    }


def killed_parity_indep() -> dict:
    """Same (r,d) is parity-independent: even (1,1) is 0111 not 1010."""
    k, s, n, j, p = 1, 7, 2, 2, 8
    got = g1_core_slot(n, j)
    neigh = g_neigh(n, j)
    g4 = g1_green4(n, j)
    ok = (
        n % 2 == 0
        and got == (0, 1, 1)
        and neigh == (0, 0)
        and g4 == (0, 1, 1, 1)
        and SLOT_NEIGH[(1, 1)] == (1, 1)
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "slot": list(got),
        "neigh": list(neigh),
        "green4": list(g4),
    }


def prefixes() -> dict:
    iu = json.loads(IU_JSON.read_text())
    ok = (
        iu["checks"]["all_ok"]
        and iu["verdict"]["dual_core_slot"] == "LEMMA"
        and iu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert slot_neigh(1, 0) == (1, 0)
    assert slot_green4(1, 0) == (1, 0, 1, 1)
    assert slot_neigh(1, 1) == (1, 1)
    assert slot_green4(2, 0) == (0, 1, 1, 1)
    assert slot_neigh(0, 0) == (0, 0)
    assert slot_neigh(3, 3) == (0, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = neigh_table()
    sc = neigh_cover()
    k0 = killed_even_eq_core()
    k1 = killed_r3_mid_11()
    k2 = killed_parity_indep()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "neigh_table": {k: rt[k] for k in rt if k != "ok"},
        "neigh_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_eq_core": {k: k0[k] for k in k0 if k != "ok"},
        "killed_r3_mid_11": {k: k1[k] for k in k1 if k != "ok"},
        "killed_parity_indep": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "slot_neigh": True,
            "slot_green4": True,
            "covering_slot_neigh": True,
            "even_g1_eq_core_green4": False,
            "r3_middle_neigh_11": False,
            "green4_parity_indep": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "slot_neigh": "LEMMA",
            "slot_green4": "LEMMA",
            "covering_slot_neigh": "LEMMA",
            "even_g1_eq_core_green4": "KILLED",
            "r3_middle_neigh_11": "KILLED",
            "green4_parity_indep": "KILLED",
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
    print("neigh_table", dump["neigh_table"])
    cov = dump["neigh_cover"]
    print(
        "neigh_cover n_ok",
        cov["n_ok"],
        "n_g1",
        cov["n_g1"],
        "n_seed",
        cov["n_seed"],
        "g4",
        cov["g4"],
    )
    print("killed_even_eq_core", dump["killed_even_eq_core"])
    print("killed_r3_mid_11", dump["killed_r3_mid_11"])
    print("killed_parity_indep", dump["killed_parity_indep"])


if __name__ == "__main__":
    main()
