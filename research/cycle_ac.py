#!/usr/bin/env python3
"""Cycle AC: 00-preimages, and left-diagonals are eventually periodic.

A centre 00 is the triple 000 or 101, not 000 alone (Cycle AB overstated).
The 5-windows that produce those triples are a 32-case local check.
Packed bit j as a function of t (the left-diagonal e_j) satisfies
    e_j(t+1) = e_{j-2}(t) XOR (e_{j-1}(t) OR e_j(t))
and is eventually periodic for every j, by induction on a 2p-state
driven bit. The centre is the onset c_t = e_t(t), typically still in
the transient, so the tails do not give a closed form for c.

Not a prize claim: infinitely many 00s (which would kill every
isolated-zero eventual period, including period 2) remain unproved.

Run: python3 research/cycle_ac.py --certify
Dump: research/cycle_ac.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def step_cell(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def all_triples() -> dict:
    """Which centred triples produce 00 / 11."""
    recs = {}
    for mask in range(8):
        ell, c, r = (mask >> 2) & 1, (mask >> 1) & 1, mask & 1
        nxt = step_cell(ell, c, r)
        word = f"{ell}{c}{r}"
        recs[word] = {
            "c": c,
            "c_next": nxt,
            "is_00": c == 0 and nxt == 0,
            "is_11": c == 1 and nxt == 1,
        }
    zeros = sorted(w for w, v in recs.items() if v["is_00"])
    ones = sorted(w for w, v in recs.items() if v["is_11"])
    return {"triples": recs, "00": zeros, "11": ones}


def all_5windows() -> dict:
    """Which centred 5-windows produce 000 / 101."""
    w000 = []
    w101 = []
    for mask in range(32):
        bits = [(mask >> (4 - i)) & 1 for i in range(5)]
        a, b, c, d, e = bits
        left = step_cell(a, b, c)
        mid = step_cell(b, c, d)
        right = step_cell(c, d, e)
        word = "".join(map(str, bits))
        if (left, mid, right) == (0, 0, 0):
            w000.append(word)
        if (left, mid, right) == (1, 0, 1):
            w101.append(word)
    return {"000": sorted(w000), "101": sorted(w101)}


def tail_period(seq: list[int], min_len: int = 32) -> tuple[int | None, int | None]:
    n = len(seq)
    for p in range(1, 33):
        need = max(min_len, 4 * p)
        if need > n:
            continue
        tail = seq[-need:]
        if all(tail[i] == tail[i % p] for i in range(need)):
            T = 0
            for i in range(n - p):
                if seq[i] != seq[i + p]:
                    T = i + 1
            return T, p
    return None, None


def self_checks(c20, triples, windows, rows, rec_ok, diags) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert triples["00"] == ["000", "101"]
    assert triples["11"] == ["010", "011"]
    assert windows["000"] == ["00000", "11101", "11110", "11111"]
    assert set(windows["101"]) == {"01100", "10001", "01010", "01011"}
    assert rec_ok
    # base diagonals
    assert all((rows[t] & 1) == 1 for t in range(len(rows)))
    assert all(((rows[t] >> 1) & 1) == 1 for t in range(1, len(rows)))
    assert all(((rows[t] >> 2) & 1) == 0 for t in range(2, len(rows)))
    # 00 occurs as both 000 and 101 in the known prefix
    assert c20[6] == 0 and c20[7] == 0
    assert any(d["T"] == 0 for d in diags)
    assert any(d["T"] not in (0, None) for d in diags)
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--tmax", type=int, default=12)
    args = parser.parse_args()
    t0 = time.perf_counter()
    tmax = 1 << args.tmax
    c20 = packed_center_bits(20)
    triples = all_triples()
    windows = all_5windows()
    rows = evolve_rows(tmax)

    rec_fail = 0
    rec_n = 0
    rec_tcap = min(tmax, 256)
    for t in range(rec_tcap):
        R, Rp = rows[t], rows[t + 1] if t + 1 <= tmax else None
        if Rp is None:
            break
        width = 2 * t + 1
        for j in range(0, min(width + 2, 2 * (t + 1) + 1)):
            e0 = (R >> (j - 2)) & 1 if j >= 2 else 0
            e1 = (R >> (j - 1)) & 1 if j >= 1 else 0
            e2 = (R >> j) & 1
            got = (Rp >> j) & 1
            rec_n += 1
            if got != (e0 ^ (e1 | e2)):
                rec_fail += 1
    rec_ok = rec_fail == 0

    diags = []
    first_transient = None
    for j in range(0, 24):
        seq = [(rows[t] >> j) & 1 for t in range(j, tmax + 1)]
        T, p = tail_period(seq)
        rec = {
            "j": j,
            "c": seq[0] if seq else None,
            "T": T,
            "p": p,
            "onset_in_tail": T == 0,
        }
        diags.append(rec)
        if first_transient is None and T not in (0, None):
            first_transient = j

    # orbit: 00 split and 5-window preds
    n00 = n000 = n101 = n11 = 0
    pred_000 = {w: 0 for w in windows["000"]}
    pred_101 = {w: 0 for w in windows["101"]}
    illegal_000 = 0
    for t in range(1, tmax):
        def bit(tt, jj):
            k = jj + tt
            if k < 0:
                return 0
            return (rows[tt] >> k) & 1

        ell, c, r = bit(t, -1), bit(t, 0), bit(t, 1)
        nxt = bit(t + 1, 0) if t + 1 <= tmax else None
        if nxt is None:
            break
        if c == 1 and nxt == 1:
            n11 += 1
        if c == 0 and nxt == 0:
            n00 += 1
            if ell == 0 and r == 0:
                n000 += 1
            elif ell == 1 and r == 1:
                n101 += 1
        if t >= 1:
            w5 = "".join(str(bit(t - 1, jj)) for jj in range(-2, 3))
            nleft = bit(t, -1)
            nmid = bit(t, 0)
            nright = bit(t, 1)
            if (nleft, nmid, nright) == (0, 0, 0):
                if w5 in pred_000:
                    pred_000[w5] += 1
                else:
                    illegal_000 += 1
            if (nleft, nmid, nright) == (1, 0, 1):
                if w5 in pred_101:
                    pred_101[w5] += 1

    checks = self_checks(c20, triples, windows, rows, rec_ok, diags)

    dump = {
        "cycle": "AC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "triples_00": triples["00"],
        "triples_11": triples["11"],
        "windows_000": windows["000"],
        "windows_101": windows["101"],
        "recurrence_ok": rec_ok,
        "recurrence_n": rec_n,
        "diagonals": diags,
        "first_onset_not_in_tail": first_transient,
        "n00": n00,
        "n000": n000,
        "n101": n101,
        "n11": n11,
        "pred_000": pred_000,
        "pred_101": pred_101,
        "illegal_000_pred": illegal_000,
        "lemmas": {
            "00_is_000_or_101": triples["00"] == ["000", "101"],
            "000_preimages": windows["000"] == ["00000", "11101", "11110", "11111"],
            "left_diagonal_recurrence": rec_ok,
            "left_diagonals_eventually_periodic": True,
            "onset_is_periodic_tail": False,
            "infinitely_many_00": None,
            "prize": False,
        },
        "verdict": {
            "00_triples": "LEMMA",
            "000_5windows": "LEMMA",
            "101_5windows": "LEMMA",
            "left_diagonal_recurrence": "LEMMA",
            "left_diagonals_eventually_periodic": "LEMMA",
            "c_from_diagonal_tail": "KILLED",
            "00_is_only_000": "KILLED",
            "infinitely_many_00": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("00 triples", triples["00"], "11", triples["11"])
    print("000 windows", windows["000"])
    print("101 windows", windows["101"])
    print("n00", n00, "n000", n000, "n101", n101, "n11", n11)
    print("first_transient_onset", first_transient)
    print("illegal_000", illegal_000, "rec_fail", rec_fail)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
