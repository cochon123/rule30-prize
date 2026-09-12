#!/usr/bin/env python3
"""Cycle IO: even-m ones lift to triples; isolated pairs come from half 11.

Freshman on n=2m+1 sends G(m,k)=1, G(m,k-1)=0, G(m,k+1)=0 to a run-3
at 2k. Even m has no 11, so every even-m one lifts to (0,1,1,1,0) on
n, which is why n%4==1 has only triples. Isolated pairs on n require
consecutive ones on m=n//2, so they occur only when m is odd (n%4==3).
Even-m ones do not lift to isolated pairs; odd-m ones can lift to
triples; isolated pairs are from half 11. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_io.py --certify
Dump: research/cycle_io.json
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
from cycle_in import g_run_kind
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
IN_JSON = Path(__file__).resolve().parent / "cycle_in.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def even_one_neigh(m: int, k: int):
    """5-window of G(2m+1) around the lift of index k."""
    n = 2 * m + 1
    return tuple(G(n, 2 * k + i) for i in range(-1, 4))


def iso_from_half11(n: int, j: int) -> bool:
    """Whether isolated pair at j comes from consecutive ones on n//2."""
    m = n // 2
    if j % 2 == 0:
        k = j // 2
        return G(m, k) == 1 and G(m, k + 1) == 1
    k = (j - 1) // 2
    return G(m, k) == 1 and G(m, k - 1) == 1


def half_lift_table() -> dict:
    """n<64: even-m ones lift to 111; n%4==1 run-3 from those; iso from half 11."""
    n_lift = n_run3_n1 = n_iso = n_iso_from11 = 0
    for m in range(0, 32):
        if m % 2:
            continue
        for k in range(0, 2 * m + 1):
            if G(m, k) != 1:
                continue
            if even_one_neigh(m, k) != (0, 1, 1, 1, 0):
                return {"ok": False, "lift": True, "m": m, "k": k}
            n_lift += 1
    for n in range(1, 64, 4):
        m = n // 2
        for j in range(0, 2 * n - 1):
            if not (G(n, j) and G(n, j + 1) and G(n, j + 2)):
                continue
            if j % 2 or G(m, j // 2) != 1:
                return {"ok": False, "n1": True, "n": n, "j": j}
            n_run3_n1 += 1
    for n in range(3, 64, 4):
        for j in range(0, 2 * n):
            if g_run_kind(n, j) != "iso":
                continue
            n_iso += 1
            if iso_from_half11(n, j):
                n_iso_from11 += 1
            else:
                return {"ok": False, "iso": True, "n": n, "j": j}
    ok = (
        n_lift == 128
        and n_run3_n1 == 128
        and n_iso == 230
        and n_iso_from11 == 230
    )
    return {
        "ok": ok,
        "n_lift": n_lift,
        "n_run3_n1": n_run3_n1,
        "n_iso": n_iso,
        "n_iso_from11": n_iso_from11,
    }


def _walk_half(k: int, q: int) -> dict:
    """Half-lift on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = n_g11_n1 = n_iso_n3 = 0
    n_cov_lift = n_cov_iso = 0
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
                if n % 4 == 1:
                    m = n // 2
                    for j in range(0, 2 * n - 1):
                        if not (G(n, j) and G(n, j + 1) and G(n, j + 2)):
                            continue
                        if j % 2 or G(m, j // 2) != 1:
                            return {"ok": False, "n1": True, "k": k, "n": n, "j": j}
                        if even_one_neigh(m, j // 2) != (0, 1, 1, 1, 0):
                            return {"ok": False, "neigh": True, "k": k, "n": n, "j": j}
                        n_cov_lift += 1
                if n % 4 == 3:
                    for j in range(0, 2 * n):
                        if g_run_kind(n, j) != "iso":
                            continue
                        if not iso_from_half11(n, j):
                            return {"ok": False, "iso": True, "k": k, "n": n, "j": j}
                        n_cov_iso += 1
            bits = {}
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                if p < 0:
                    continue
                four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                packed = and_clause(*four)
                bits[j] = packed
                n_ok += 1
                if G(n, j):
                    n_g1 += 1
                    if packed:
                        xor_j ^= 1
            for j in range(0, 2 * n):
                if j not in bits or (j + 1) not in bits:
                    continue
                kind = g_run_kind(n, j)
                if kind is None:
                    continue
                n_g11 += 1
                if n % 4 == 1:
                    n_g11_n1 += 1
                    if kind == "iso":
                        return {"ok": False, "cov_iso": True, "k": k, "n": n, "j": j}
                elif n % 4 == 3 and kind == "iso":
                    n_iso_n3 += 1
                    if not iso_from_half11(n, j):
                        return {"ok": False, "cov_half": True, "k": k, "n": n, "j": j}
                elif n % 2 == 0:
                    return {"ok": False, "cov_even": True, "k": k, "n": n, "j": j}
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_n1": n_g11_n1,
        "n_iso_n3": n_iso_n3,
        "n_cov_lift": n_cov_lift,
        "n_cov_iso": n_cov_iso,
        "xor_j": xor_j,
    }


def half_cover() -> dict:
    """Half-lift on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_g11_n1 = n_iso_n3 = 0
    n_cov_lift = n_cov_iso = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_half(k, q)
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
            n_g11 += w["n_g11"]
            n_g11_n1 += w["n_g11_n1"]
            n_iso_n3 += w["n_iso_n3"]
            n_cov_lift += w["n_cov_lift"]
            n_cov_iso += w["n_cov_iso"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_g11_n1": w["n_g11_n1"],
                "n_iso_n3": w["n_iso_n3"],
                "n_cov_lift": w["n_cov_lift"],
                "n_cov_iso": w["n_cov_iso"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_g11_n1 == 4294
        and n_iso_n3 == 3817
        and n_cov_lift == 2547
        and n_cov_iso == 4550
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_g11_n1": n_g11_n1,
        "n_iso_n3": n_iso_n3,
        "n_cov_lift": n_cov_lift,
        "n_cov_iso": n_cov_iso,
        "rows": rows,
    }


def killed_even_one_iso() -> dict:
    """Even-m 1 lifts to an isolated pair: G(0,0)=1 lifts to G(1)=111."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    m = n // 2
    neigh = even_one_neigh(m, 0)
    ok = (
        m % 2 == 0
        and G(m, 0) == 1
        and neigh == (0, 1, 1, 1, 0)
        and g_run_kind(n, j) == "left"
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "m": m,
        "neigh": list(neigh),
        "kind": g_run_kind(n, j),
    }


def killed_iso_not_half11() -> dict:
    """Isolated pair is not from half 11: G(3) pair at j=0 from G(1)=111."""
    k, s, n, j, p = 0, 3, 3, 0, 10
    ok = (
        n % 4 == 3
        and g_run_kind(n, j) == "iso"
        and iso_from_half11(n, j)
        and [G(n // 2, i) for i in range(0, 3)] == [1, 1, 1]
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "half": [G(n // 2, i) for i in range(0, 3)],
    }


def killed_odd_m_no_triple() -> dict:
    """Odd-m 1 never lifts to a triple: G(3,3)=1 lifts to G(7) 111 at j=6."""
    k, s, n, j, p = 1, 5, 7, 6, 8
    m, kk = n // 2, j // 2
    ok = (
        m % 2 == 1
        and G(m, kk) == 1
        and [G(n, j + i) for i in range(3)] == [1, 1, 1]
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "m": m,
        "G_m": G(m, kk),
        "G": [G(n, j + i) for i in range(3)],
    }


def prefixes() -> dict:
    inn = json.loads(IN_JSON.read_text())
    ok = (
        inn["checks"]["all_ok"]
        and inn["verdict"]["n1_only_triples"] == "LEMMA"
        and inn["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert even_one_neigh(0, 0) == (0, 1, 1, 1, 0)
    assert iso_from_half11(3, 0)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = half_lift_table()
    sc = half_cover()
    k0 = killed_even_one_iso()
    k1 = killed_iso_not_half11()
    k2 = killed_odd_m_no_triple()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "half_lift_table": {k: rt[k] for k in rt if k != "ok"},
        "half_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_even_one_iso": {k: k0[k] for k in k0 if k != "ok"},
        "killed_iso_not_half11": {k: k1[k] for k in k1 if k != "ok"},
        "killed_odd_m_no_triple": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "even_m_ones_lift_triples": True,
            "iso_from_half11": True,
            "covering_half_lift": True,
            "even_m_one_lifts_iso": False,
            "iso_not_from_half11": False,
            "odd_m_one_never_triple": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_m_ones_lift_triples": "LEMMA",
            "iso_from_half11": "LEMMA",
            "covering_half_lift": "LEMMA",
            "even_m_one_lifts_iso": "KILLED",
            "iso_not_from_half11": "KILLED",
            "odd_m_one_never_triple": "KILLED",
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
    print("half_lift_table", dump["half_lift_table"])
    cov = dump["half_cover"]
    print(
        "half_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_cov_lift",
        cov["n_cov_lift"],
        "n_cov_iso",
        cov["n_cov_iso"],
        "n_iso_n3",
        cov["n_iso_n3"],
    )
    print("killed_even_one_iso", dump["killed_even_one_iso"])
    print("killed_iso_not_half11", dump["killed_iso_not_half11"])
    print("killed_odd_m_no_triple", dump["killed_odd_m_no_triple"])


if __name__ == "__main__":
    main()
