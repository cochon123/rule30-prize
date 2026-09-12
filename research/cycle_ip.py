#!/usr/bin/env python3
"""Cycle IP: ones-runs on m lift to a closed dictionary on n=2m+1.

Freshman sends a length-r ones-run to half_run_image(r):
  r=1 -> 01110, r=2 -> 0110110, r=3 -> 011010110
(flanking zeros included). Run-2 does not lift to a triple; run-3 on m
does not lift to one run-3 on n; run-1 is not an isolated pair.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ip.py --certify
Dump: research/cycle_ip.json
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
IO_JSON = Path(__file__).resolve().parent / "cycle_io.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"


def half_run_image(r: int) -> tuple:
    """Lift of a length-r ones-run, including flanking zeros."""
    bits = [0]
    for i in range(r):
        bits.append(1 if i == 0 else 0)
        bits.append(1)
    bits.append(1)
    bits.append(0)
    return tuple(bits)


def g_runs(n: int) -> list:
    """Ones-runs of G(n) as (start, length)."""
    out = []
    run = 0
    start = 0
    for j in range(0, 2 * n + 2):
        bit = G(n, j) if j <= 2 * n else 0
        if bit:
            if run == 0:
                start = j
            run += 1
            continue
        if run:
            out.append((start, run))
        run = 0
    return out


def run_dict_table() -> dict:
    """m<32: every ones-run lifts by half_run_image; odd-n run-3 from run-1."""
    n_ok = 0
    by_r = [0, 0, 0, 0]
    for m in range(0, 32):
        n = 2 * m + 1
        for start, r in g_runs(m):
            if r >= 4:
                return {"ok": False, "run4": True, "m": m, "r": r}
            pred = half_run_image(r)
            got = tuple(G(n, 2 * start + i) for i in range(-1, 2 * r + 2))
            if got != pred:
                return {
                    "ok": False,
                    "img": True,
                    "m": m,
                    "start": start,
                    "r": r,
                    "got": list(got),
                }
            n_ok += 1
            by_r[r] += 1
    n_r3 = n_r3_from1 = 0
    for n in range(1, 64, 2):
        m = n // 2
        half = set(g_runs(m))
        for start, r in g_runs(n):
            if r != 3:
                continue
            n_r3 += 1
            if start % 2 == 0 and (start // 2, 1) in half:
                n_r3_from1 += 1
            else:
                return {"ok": False, "r3": True, "n": n, "start": start}
    ok = (
        n_ok == 256
        and by_r[1] == 141
        and by_r[2] == 70
        and by_r[3] == 45
        and n_r3 == 141
        and n_r3_from1 == 141
        and half_run_image(1) == (0, 1, 1, 1, 0)
        and half_run_image(2) == (0, 1, 1, 0, 1, 1, 0)
        and half_run_image(3) == (0, 1, 1, 0, 1, 0, 1, 1, 0)
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_r1": by_r[1],
        "n_r2": by_r[2],
        "n_r3": by_r[3],
        "n_r3_odd": n_r3,
        "n_r3_from1": n_r3_from1,
    }


def _walk_dict(k: int, q: int) -> dict:
    """Run dictionary on covering clocks; packed J XOR."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    n_ok = n_g1 = n_g11 = 0
    n_cov = [0, 0, 0, 0]
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
                if n % 2 == 1:
                    m = n // 2
                    for start, r in g_runs(m):
                        if r >= 4:
                            return {"ok": False, "run4": True, "k": k, "m": m}
                        pred = half_run_image(r)
                        got = tuple(G(n, 2 * start + i) for i in range(-1, 2 * r + 2))
                        if got != pred:
                            return {
                                "ok": False,
                                "img": True,
                                "k": k,
                                "n": n,
                                "start": start,
                                "r": r,
                            }
                        n_cov[r] += 1
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
                if G(n, j) and G(n, j + 1):
                    n_g11 += 1
        row = rule30_step(row)
        s += 1
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_cov1": n_cov[1],
        "n_cov2": n_cov[2],
        "n_cov3": n_cov[3],
        "xor_j": xor_j,
    }


def run_dict_cover() -> dict:
    """Run dictionary on covering clocks k<=6; XOR matches HF/HG."""
    n_ok = n_g1 = n_g11 = n_cov1 = n_cov2 = n_cov3 = 0
    rows = {}
    hf = json.loads(HF_JSON.read_text())
    hg = json.loads(HG_JSON.read_text())
    for k in range(0, 7):
        krow = {}
        for q, name in ((6, "j6"), (10, "j10")):
            w = _walk_dict(k, q)
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
            n_cov1 += w["n_cov1"]
            n_cov2 += w["n_cov2"]
            n_cov3 += w["n_cov3"]
            krow[name] = {
                "n_ok": w["n_ok"],
                "n_g1": w["n_g1"],
                "n_g11": w["n_g11"],
                "n_cov1": w["n_cov1"],
                "n_cov2": w["n_cov2"],
                "n_cov3": w["n_cov3"],
                "xor_j": w["xor_j"],
            }
        rows[str(k)] = krow
    ok = (
        n_ok == 95821
        and n_g1 == 22659
        and n_g11 == 8577
        and n_cov1 == 2818
        and n_cov2 == 1402
        and n_cov3 == 873
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_g11": n_g11,
        "n_cov1": n_cov1,
        "n_cov2": n_cov2,
        "n_cov3": n_cov3,
        "rows": rows,
    }


def killed_run2_triple() -> dict:
    """Run-2 lifts to a triple: G(3) run-2 at 0 lifts to 11011 on G(7)."""
    k, s, n, j, p = 1, 5, 7, 0, 20
    m, start, r = 3, 0, 2
    img = half_run_image(r)
    got = tuple(G(n, 2 * start + i) for i in range(-1, 2 * r + 2))
    ok = (
        g_runs(m)[0] == (start, r)
        and img == (0, 1, 1, 0, 1, 1, 0)
        and got == img
        and g_run_kind(n, j) == "iso"
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "img": list(img),
        "kind": g_run_kind(n, j),
    }


def killed_run3_one_triple() -> dict:
    """Run-3 on m lifts to one run-3 on n: G(1)=111 lifts to G(3)=1101011."""
    k, s, n, j, p = 0, 3, 3, 0, 10
    img = half_run_image(3)
    got = tuple(G(n, i) for i in range(-1, 8))
    ok = (
        g_runs(1) == [(0, 3)]
        and img == (0, 1, 1, 0, 1, 0, 1, 1, 0)
        and got == img
        and g_run_kind(n, j) == "iso"
        and [G(n, i) for i in range(0, 7)] == [1, 1, 0, 1, 0, 1, 1]
        and p >= 4
    )
    return {
        "ok": ok,
        "k": k,
        "s": s,
        "n": n,
        "j": j,
        "p": p,
        "img": list(img),
        "G": [G(n, i) for i in range(0, 7)],
    }


def killed_run1_iso() -> dict:
    """Run-1 image is an isolated pair 0110: G(0)=1 lifts to G(1)=111."""
    k, s, n, j, p = 0, 3, 1, 0, 6
    img = half_run_image(1)
    ok = (
        img == (0, 1, 1, 1, 0)
        and img != (0, 1, 1, 0)
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
        "img": list(img),
        "kind": g_run_kind(n, j),
    }


def prefixes() -> dict:
    io = json.loads(IO_JSON.read_text())
    ok = (
        io["checks"]["all_ok"]
        and io["verdict"]["even_m_ones_lift_triples"] == "LEMMA"
        and io["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and pref["ok"]
    assert half_run_image(1) == (0, 1, 1, 1, 0)
    assert g_runs(0) == [(0, 1)]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = run_dict_table()
    sc = run_dict_cover()
    k0 = killed_run2_triple()
    k1 = killed_run3_one_triple()
    k2 = killed_run1_iso()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, pref)
    dump = {
        "cycle": "IP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "run_dict_table": {k: rt[k] for k in rt if k != "ok"},
        "run_dict_cover": {k: sc[k] for k in sc if k != "ok"},
        "killed_run2_triple": {k: k0[k] for k in k0 if k != "ok"},
        "killed_run3_one_triple": {k: k1[k] for k in k1 if k != "ok"},
        "killed_run1_iso": {k: k2[k] for k in k2 if k != "ok"},
        "lemmas": {
            "half_run_dictionary": True,
            "odd_n_run3_from_run1": True,
            "covering_run_dictionary": True,
            "run2_lifts_triple": False,
            "run3_lifts_one_triple": False,
            "run1_is_iso_pair": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "half_run_dictionary": "LEMMA",
            "odd_n_run3_from_run1": "LEMMA",
            "covering_run_dictionary": "LEMMA",
            "run2_lifts_triple": "KILLED",
            "run3_lifts_one_triple": "KILLED",
            "run1_is_iso_pair": "KILLED",
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
    print("run_dict_table", dump["run_dict_table"])
    cov = dump["run_dict_cover"]
    print(
        "run_dict_cover n_ok",
        cov["n_ok"],
        "n_g11",
        cov["n_g11"],
        "n_cov1",
        cov["n_cov1"],
        "n_cov2",
        cov["n_cov2"],
        "n_cov3",
        cov["n_cov3"],
    )
    print("killed_run2_triple", dump["killed_run2_triple"])
    print("killed_run3_one_triple", dump["killed_run3_one_triple"])
    print("killed_run1_iso", dump["killed_run1_iso"])


if __name__ == "__main__":
    main()
