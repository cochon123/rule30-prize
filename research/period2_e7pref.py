#!/usr/bin/env python3
"""Extra>=7 through T=48 lives only on 18 length-6 prefixes.

Every ugap onset with extra>=7 and T in [8,48] has u[:6] in P_35
union P_43 (the T=35 10-tail prefixes and the T=43 period-8-tail
prefixes). The two sets are disjoint and have size 6+12=18. High
extra is therefore confined to 18 ugap cylinders. This is a census
reduction, not a T-independent bound. Not a prize claim.

Run: python3 research/period2_e7pref.py --certify
Dump: research/period2_e7pref.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_exdesc import force
from period2_t35ten import T35_PREFIXES, T43_ISO_EF_E8
from period2_ugap_sat import ugap_ok, ugap_strings
from period2_vacuum import nvars

OUT = Path(__file__).resolve().with_suffix(".json")

P35 = tuple(T35_PREFIXES)
P43 = tuple(sorted({w[:6] for w in T43_ISO_EF_E8}))
SUPPORT = frozenset(P35) | frozenset(P43)


def legal_pref(p):
    u = [int(c) for c in p]
    return ugap_ok(u) and all(a + b < 2 for a, b in zip(u, u[1:]))


def scan(Tmin=8, Tmax=48, emin=7):
    n_hi = 0
    fam = Counter()
    by_T = []
    max_e = -1
    at_max = []
    for T in range(Tmin, Tmax + 1):
        n0 = nvars(T)
        if n0 < 6:
            continue
        n_T = 0
        c = Counter()
        for u in ugap_strings(n0):
            rec = force(u, T)
            if rec is None or rec["extra"] < emin:
                continue
            pref = rec["sample"][:6]
            assert pref in SUPPORT, (T, rec["sample"], rec["extra"])
            n_hi += 1
            n_T += 1
            tag = "P35" if pref in P35 else "P43"
            c[tag] += 1
            fam[tag] += 1
            if rec["extra"] > max_e:
                max_e = rec["extra"]
                at_max = [(T, rec["kind"], rec["stop"], rec["sample"], rec["extra"])]
            elif rec["extra"] == max_e:
                at_max.append((T, rec["kind"], rec["stop"], rec["sample"], rec["extra"]))
        if n_T:
            by_T.append({"T": T, "n": n_T, "P35": c["P35"], "P43": c["P43"]})
    return {
        "Tmin": Tmin,
        "Tmax": Tmax,
        "emin": emin,
        "n_extra_ge7": n_hi,
        "n_P35": fam["P35"],
        "n_P43": fam["P43"],
        "max_extra": max_e,
        "by_T": by_T,
        "n_at_max": len(at_max),
        "ok": True,
    }


def certify_support_set():
    assert len(P35) == 6
    assert len(P43) == 12
    assert len(SUPPORT) == 18
    assert set(P35).isdisjoint(P43)
    assert all(len(p) == 6 and legal_pref(p) for p in SUPPORT)
    return {"n_P35": 6, "n_P43": 12, "n_support": 18, "P35": list(P35), "P43": list(P43), "ok": True}


def certify():
    t0 = time.perf_counter()
    checks = {}
    supp = certify_support_set()
    checks["support_18_disjoint_ugap"] = True
    sc = scan(8, 48, 7)
    checks["extra_ge7_in_support_T8_48"] = True
    assert sc["n_extra_ge7"] > 0
    assert sc["n_P35"] > 0 and sc["n_P43"] > 0
    assert sc["max_extra"] == 8
    return {
        "checks": checks,
        "support": supp,
        "scan": sc,
        "wall_time_sec": time.perf_counter() - t0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("checks", report["checks"])
    print(
        "n",
        report["scan"]["n_extra_ge7"],
        "P35",
        report["scan"]["n_P35"],
        "P43",
        report["scan"]["n_P43"],
        "max",
        report["scan"]["max_extra"],
    )
    print("wall", round(report["wall_time_sec"], 3), "s")
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
