#!/usr/bin/env python3
"""Cycle IK: Green avoids the four 6-windows that lift to a 4-run.

G(n,j)=G(n-1,j) XOR G(n-1,j-1) XOR G(n-1,j-2). The 6-windows that
map to 1111 under that trinomial are 001001, 010010, 100100, 111111
(odd-weight (abc)^2). None of those windows appear in G (n<64, and
covering clocks). G does have even-weight period-3 6-windows; the
recurrence is not two-term; G does contain 001. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ik.py --certify
Dump: research/cycle_ik.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IJ_JSON = Path(__file__).resolve().parent / "cycle_ij.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"

LIFT4 = (
    (0, 0, 1, 0, 0, 1),
    (0, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0),
    (1, 1, 1, 1, 1, 1),
)


def g_step(n: int, j: int) -> int:
    """Trinomial recurrence for G."""
    return G(n - 1, j) ^ G(n - 1, j - 1) ^ G(n - 1, j - 2)


def g6(n: int, j: int) -> tuple[int, int, int, int, int, int]:
    """Length-6 Green window starting at j (0 off-support)."""
    return tuple(G(n, j + i) for i in range(6))  # type: ignore[return-value]


def lift_table() -> dict:
    """n<64: trinomial recurrence; no LIFT4 6-windows (padded)."""
    n_rec = n_win = n_lift = 0
    for n in range(1, 64):
        for j in range(-2, 2 * n + 3):
            if G(n, j) != g_step(n, j):
                return {"ok": False, "rec": True, "n": n, "j": j}
            n_rec += 1
    for n in range(0, 64):
        for j in range(-2, 2 * n - 2):
            six = g6(n, j)
            n_win += 1
            if six in LIFT4:
                n_lift += 1
                return {"ok": False, "lift": True, "n": n, "j": j, "six": list(six)}
    ok = n_rec == 4347 and n_win == 4032 and n_lift == 0
    return {"ok": ok, "n_rec": n_rec, "n_win": n_win, "n_lift": n_lift}


def _walk_lift(k: int, q: int) -> dict:
    """No LIFT4 on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_win = n_g1 = 0
    xor_j = 0
    s = t0
    prev = None
    seen = set()
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            if n not in seen:
                seen.add(n)
                for j in range(-2, 2 * n - 2):
                    six = g6(n, j)
                    n_win += 1
                    if six in LIFT4:
                        return {"ok": False, "lift": True, "k": k, "n": n, "j": j}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
        row = rule30_step(row)
        s += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_win": n_win, "n_g1": n_g1, "xor_j": xor_j}


def lift_cover() -> dict:
    """No LIFT4 on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_win = n_g1 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_lift(k, q)
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
            n_win += w["n_win"]
            n_g1 += w["n_g1"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_win": w["n_win"],
                "n_g1": w["n_g1"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = n_ok == 95821 and n_g1 == 22659
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_win": n_win,
        "n_g1": n_g1,
        "rows": rows,
    }


def killed_no_per3_six() -> dict:
    """G has even-weight period-3 6-windows: 101101 at n=7, j=1."""
    k, s, n, j, p = 1, 5, 7, 1, 18
    six = g6(n, j)
    ok = (
        six == (1, 0, 1, 1, 0, 1)
        and six[0] == six[3]
        and six[1] == six[4]
        and six[2] == six[5]
        and (six[0] + six[1] + six[2]) % 2 == 0
        and six not in LIFT4
        and p == (10 * (1 << k)) - 2 * j
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "six": list(six),
    }


def killed_two_term_rec() -> dict:
    """Recurrence is not two-term: n=2, j=2 needs the j-2 term."""
    k, s, n, j, p = 0, 5, 2, 2, 6
    two = G(n - 1, j) ^ G(n - 1, j - 1)
    three = g_step(n, j)
    ok = (
        G(n, j) == 1
        and two == 0
        and three == 1
        and two != three
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "G": G(n, j),
        "two": two,
        "three": three,
    }


def killed_no_001() -> dict:
    """G contains 001: n=4, j=2."""
    k, s, n, j, p = 2, 15, 4, 2, 20
    trip = tuple(G(n, j + i) for i in range(3))
    ok = trip == (0, 0, 1) and p >= 4 and G(n, 0) == 1
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "three": list(trip),
    }


def prefixes() -> dict:
    ij = json.loads(IJ_JSON.read_text())
    ok = (
        ij["checks"]["all_ok"]
        and ij["verdict"]["G_no_4run"] == "LEMMA"
        and ij["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert g_step(1, 0) == 1
    assert g6(7, 1) == (1, 0, 1, 1, 0, 1)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = lift_table()
    sc = lift_cover()
    k0 = killed_no_per3_six()
    k1 = killed_two_term_rec()
    k2 = killed_no_001()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lift_table": {k: rt[k] for k in rt if k != "ok"},
        "lift_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_no_per3_six": {k: k0[k] for k in k0 if k != "ok"},
        "killed_two_term_rec": {k: k1[k] for k in k1 if k != "ok"},
        "killed_no_001": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "G_trinomial_recurrence": True,
            "G_no_LIFT4_windows": True,
            "covering_no_LIFT4": True,
            "G_no_period3_six": False,
            "G_two_term_rec": False,
            "G_no_001": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_trinomial_recurrence": "LEMMA",
            "G_no_LIFT4_windows": "LEMMA",
            "covering_no_LIFT4": "LEMMA",
            "G_no_period3_six": "KILLED",
            "G_two_term_rec": "KILLED",
            "G_no_001": "KILLED",
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
    print("lift_table", dump["lift_table"])
    cov = dump["lift_cover"]
    print(
        "lift_cover n_ok",
        cov["n_ok"],
        "n_win",
        cov["n_win"],
        "n_g1",
        cov["n_g1"],
    )
    print("killed_no_per3_six", dump["killed_no_per3_six"])
    print("killed_two_term_rec", dump["killed_two_term_rec"])
    print("killed_no_001", dump["killed_no_001"])


if __name__ == "__main__":
    main()
