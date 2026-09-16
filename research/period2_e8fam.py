#!/usr/bin/env python3
"""Extra-8 through T=48 is two prefix families with T-dependent tails.

The T=35 10-tail prefixes (6 words) reappear as all of T=46 extra-8
and five of T=47 extra-8. The T=43 (00010010)^2 prefixes (12 words)
reappear as 12 of 15 T=48 extra-8 words. T=47 extra-8 is not an R=3
image. Census classification, not a T-independent bound.
Not a prize claim.

Run: python3 research/period2_e8fam.py --certify
Dump: research/period2_e8fam.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import extra_of_word, force
from period2_qshift import shift_u
from period2_r3pull import T35_ISO_EF_E7, r3_preimages
from period2_t35ten import T35_PREFIXES, T43_ISO_EF_E8, T43_TAIL
from period2_ugap_sat import wstr
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")
E8CAP = Path(__file__).resolve().with_name("period2_e8cap.json")

T44_ISO_11_E8 = [
    "0001001000010001000101",
    "0101001000010001000101",
    "1001001000010001000101",
]
T44_TAIL = "001000010001000101"

T46_TAIL = "10100101010001010"
T46_BUMP_EF_E8 = [p + T46_TAIL for p in T35_PREFIXES]

T47_TAIL = "010010101000010000"
T47_ISO_EF_E8 = [
    "000100" + T47_TAIL,
    "001000" + T47_TAIL,
    "010100" + T47_TAIL,
    "100100" + T47_TAIL,
    "101000" + T47_TAIL,
]

T48_TAIL_A = "000101001000100001"
T48_TAIL_B = "00100100100010100100"
T48_PREF_B = ["0001", "0101", "1001"]


def e8_words(T):
    data = json.loads(E8CAP.read_text())
    block = next(x for x in data["scan"]["e8"] if x["T"] == T)
    return [(w["kind"], w["stop"], w["u"]) for w in block["words"]]


def check_force(words, T, kind, stop, extra):
    rows = []
    n0 = nvars(T)
    for w in words:
        rec = force(u := [int(c) for c in w], T)
        assert rec is not None, w
        assert rec["kind"] == kind and rec["stop"] == stop, (w, rec)
        assert rec["extra"] == extra, (w, rec["extra"])
        rows.append({"u": w, "R": rec["R"], "extra_bits": wstr(rec["bits"][n0:])})
    return rows


def certify_t44():
    rows = check_force(T44_ISO_11_E8, 44, "iso", "11", 8)
    assert all(w.endswith(T44_TAIL) for w in T44_ISO_11_E8)
    cap = e8_words(44)
    assert sorted(u for _, _, u in cap) == sorted(T44_ISO_11_E8)
    assert all(k == "iso" and s == "11" for k, s, _ in cap)
    rec0 = force([int(c) for c in T44_ISO_11_E8[0]], 44)
    r2 = extra_of_word(shift_u(rec0["bits"]), 46)
    assert r2["kind"] == "bump" and r2["stop"] == "11" and r2["extra"] == 6
    return {"n": len(rows), "tail": T44_TAIL, "ok": True}


def certify_t46():
    assert T35_PREFIXES == [w[:6] for w in T35_ISO_EF_E7]
    assert T46_BUMP_EF_E8 == [p + T46_TAIL for p in T35_PREFIXES]
    rows = check_force(T46_BUMP_EF_E8, 46, "bump", "even_F", 8)
    extras = {r["extra_bits"] for r in rows}
    assert extras == {"00101010"}
    cap = e8_words(46)
    assert sorted(u for _, _, u in cap) == sorted(T46_BUMP_EF_E8)
    rec0 = force([int(c) for c in T46_BUMP_EF_E8[0]], 46)
    r2 = extra_of_word(shift_u(rec0["bits"]), 48)
    assert r2["kind"] == "bump" and r2["stop"] == "even_F" and r2["extra"] == 6
    return {"n": 6, "tail": T46_TAIL, "prefixes": T35_PREFIXES, "ok": True}


def certify_t47():
    rows = check_force(T47_ISO_EF_E8, 47, "iso", "even_F", 8)
    assert all(w.endswith(T47_TAIL) for w in T47_ISO_EF_E8)
    prefs = [w[:6] for w in T47_ISO_EF_E8]
    assert set(prefs) <= set(T35_PREFIXES)
    assert "010000" not in prefs
    for w in T47_ISO_EF_E8:
        assert r3_preimages([int(c) for c in w], 47) == []
    cap = e8_words(47)
    assert sorted(u for _, _, u in cap) == sorted(T47_ISO_EF_E8)
    return {"n": 5, "tail": T47_TAIL, "prefixes": prefs, "n_r3": 0, "ok": True}


def certify_t48():
    t43_prefs = [w[:6] for w in T43_ISO_EF_E8]
    fam_a = [p + T48_TAIL_A for p in t43_prefs]
    fam_b = [p + T48_TAIL_B for p in T48_PREF_B]
    rows_a = check_force(fam_a, 48, "bump", "even_F", 8)
    rows_b = check_force(fam_b, 48, "bump", "even_F", 8)
    cap = e8_words(48)
    got = sorted(u for _, _, u in cap)
    assert got == sorted(fam_a + fam_b)
    assert all(k == "bump" and s == "even_F" for k, s, _ in cap)
    return {
        "n_a": len(fam_a),
        "n_b": len(fam_b),
        "tail_a": T48_TAIL_A,
        "tail_b": T48_TAIL_B,
        "ok": True,
    }


def certify():
    t0 = time.perf_counter()
    checks = {}
    t44 = certify_t44()
    checks["t44_iso_11_e8_family"] = True
    t46 = certify_t46()
    checks["t46_is_t35_prefixes"] = True
    t47 = certify_t47()
    checks["t47_t35_prefixes_not_r3"] = True
    t48 = certify_t48()
    checks["t48_is_t43_prefixes_plus_3"] = True
    return {
        "checks": checks,
        "t44": t44,
        "t46": t46,
        "t47": t47,
        "t48": t48,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("t44", report["t44"]["n"], "t46", report["t46"]["n"], "t47", report["t47"]["n"])
    print("t48", report["t48"]["n_a"], "+", report["t48"]["n_b"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
