#!/usr/bin/env python3
"""T=33 isolated extra-7 is the R=3 image of even-F extra-2 at T=32.

The three T=33 isolated even-F extra-7 ugap onsets of period2_alldesc
(shared tail 00010100100100) are exactly the isolated images under S
of bump even-F extra-2 onsets at T=32. They are therefore not
S-minimal. The R=3 map does not absorb later isolated extra-7: the
six T=35 isolated even-F extra-7 words with 10-periodic tail
101010101010 have no such preimage. Not a prize claim.

Run: python3 research/period2_r3pull.py --certify
Dump: research/period2_r3pull.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_alldesc import T33_ISO_EF_E7
from period2_exdesc import force
from period2_qshift import shift_u
from period2_ugap_sat import ugap_ok, ugap_strings, wstr
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")

T35_ISO_EF_E7 = [
    "000100101010101010",
    "001000101010101010",
    "010000101010101010",
    "010100101010101010",
    "100100101010101010",
    "101000101010101010",
]

T32_E2_TO_T33_E7 = [
    ("0001000101001001", "00100010100100100"),
    ("1001000101001001", "00100010100100100"),
    ("0010000101001001", "01000010100100100"),
    ("1010000101001001", "01000010100100100"),
    ("0101000101001001", "10100010100100100"),
]


def image_prefix(bits, T_src):
    n0p = nvars(T_src + 1)
    Su = shift_u(bits)
    return (list(Su) + [0] * n0p)[:n0p]


def legal(u):
    return ugap_ok(u) and all(a + b < 2 for a, b in zip(u, u[1:]))


def r3_preimages(u, T_odd):
    """Ugap even-F extra-2 prefixes at T-1 whose R=3 image is u."""
    T = T_odd - 1
    n0s = nvars(T)
    n0 = nvars(T_odd)
    hits = []
    seen = set()
    for b in (0, 1):
        pref = ([b] + list(u))[:n0s]
        if not legal(pref):
            continue
        rec = force(pref, T)
        if rec is None or rec["stop"] != "even_F" or rec["extra"] != 2:
            continue
        if not legal(rec["bits"]):
            continue
        ip = image_prefix(rec["bits"], T)
        if ip != list(u[:n0]):
            continue
        key = rec["sample"]
        if key in seen:
            continue
        seen.add(key)
        hits.append(rec)
    return hits


def certify_t33_family():
    T = 33
    n0 = nvars(T)
    assert n0 == 17
    assert nvars(32) == 16
    rows = []
    all_src = []
    for w in T33_ISO_EF_E7:
        u = [int(c) for c in w]
        rec = force(u, T)
        assert rec is not None
        assert rec["kind"] == "iso" and rec["stop"] == "even_F"
        assert rec["extra"] == 7
        assert rec["R"] == 14
        assert w.endswith("00010100100100")
        hits = r3_preimages(u, T)
        assert hits, w
        for h in hits:
            assert h["kind"] == "bump"
            assert h["stop"] == "even_F"
            assert h["extra"] == 2
            assert h["R"] == 3
            all_src.append(h["sample"])
        rows.append(
            {
                "u": w,
                "extra": rec["extra"],
                "R": rec["R"],
                "n_pre": len(hits),
                "src": [h["sample"] for h in hits],
            }
        )
    assert set(all_src) == {s for s, _ in T32_E2_TO_T33_E7}
    return {"n": len(rows), "words": rows, "ok": True}


def certify_t33_complete():
    """Every T=33 isolated extra-7 ugap onset is in the alldesc family."""
    T = 33
    n0 = nvars(T)
    found = []
    for u in ugap_strings(n0):
        rec = force(u, T)
        if rec is None or rec["kind"] != "iso" or rec["extra"] != 7:
            continue
        found.append(rec["sample"])
        assert rec["stop"] == "even_F"
        assert rec["sample"] in T33_ISO_EF_E7
        assert r3_preimages(u, T)
    assert sorted(found) == sorted(T33_ISO_EF_E7)
    return {"n": len(found), "ok": True}


def certify_t32_images():
    """R=3 images of extra-2 at T=32 that have extra 7 are exactly T33."""
    T = 32
    n0 = nvars(T)
    imgs = []
    n_src = 0
    for u in ugap_strings(n0):
        rec = force(u, T)
        if rec is None or rec["stop"] != "even_F" or rec["extra"] != 2:
            continue
        n_src += 1
        if rec["kind"] != "bump":
            pref = image_prefix(rec["bits"], T)
            r2 = force(pref, T + 1)
            assert r2 is None or r2["extra"] != 7
            continue
        pref = image_prefix(rec["bits"], T)
        r2 = force(pref, T + 1)
        if r2 is None or r2["extra"] != 7:
            continue
        assert r2["kind"] == "iso" and r2["stop"] == "even_F"
        imgs.append((rec["sample"], r2["sample"]))
    assert sorted(imgs) == sorted(T32_E2_TO_T33_E7)
    assert {im for _, im in imgs} == set(T33_ISO_EF_E7)
    return {"n_evenF_e2": n_src, "n_to_e7": len(imgs), "pairs": imgs, "ok": True}


def certify_t35_not_pullback():
    T = 35
    n0 = nvars(T)
    found = []
    for u in ugap_strings(n0):
        rec = force(u, T)
        if rec is None or rec["kind"] != "iso" or rec["extra"] != 7:
            continue
        found.append(rec["sample"])
        assert rec["stop"] == "even_F"
        assert rec["sample"].endswith("101010101010")
        assert rec["sample"] in T35_ISO_EF_E7
        assert r3_preimages(u, T) == []
    assert sorted(found) == sorted(T35_ISO_EF_E7)
    return {"n": len(found), "words": found, "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    fam = certify_t33_family()
    checks["t33_e7_all_r3_preimages"] = True
    comp = certify_t33_complete()
    checks["t33_iso_e7_exactly_three"] = True
    src = certify_t32_images()
    checks["t32_e2_images_e7_exactly_t33"] = True
    t35 = certify_t35_not_pullback()
    checks["t35_iso_e7_not_r3"] = True
    return {
        "checks": checks,
        "t33_family": fam,
        "t33_complete": comp,
        "t32_images": src,
        "t35_not_pullback": t35,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print("t33", report["t33_family"]["n"], "srcs", [w["src"] for w in report["t33_family"]["words"]])
    print("t32_to_e7", report["t32_images"]["n_to_e7"])
    print("t35", report["t35_not_pullback"]["n"])
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
