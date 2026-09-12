#!/usr/bin/env python3
"""Cycle EV: reconstruct(S, gap(S)) run-form; scar ham(n4,n5)=n0.

Even-n0 O-type always has a 00 (a 11 in one half is a 00 in the other;
Cycle CH: never alternating). After each 00 the next 1 of S has
back-distance >=3, so reconstruct(S, gap(S)) has U=1 there and free bit
0. Along the following 0-run, U is (free, free, 1, 1, ...); a next 1 at
distance 1 or 2 takes that free bit. Those 00-seeds determine the whole
word, so n5=reconstruct(n3, gap(n3)) is this function of
n3=rot^{n0-1}(T). Cycle DX on s=n3 gives ham(n4,n5)=n0 in scar indexing.
For even n0, n5 is type N and is not 0, n3, or n4. Kills: n5=gap(n4);
ham(n4,n5) not n0; no run-form for n5; even n0 O-type can lack 00.
Do not claim n5=gap(n4); do not claim 1-runs of n5 always alternate;
do not claim n6 type N; do not claim a formula for extra 414990; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ev.py --certify
Dump: research/cycle_ev.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_ch import ham
from cycle_dv import mask_bits, odd_copy
from cycle_er import U32
from cycle_eu import back_dist, gap_parity

OUT = Path(__file__).resolve().with_suffix(".json")
EU_JSON = Path(__file__).resolve().parent / "cycle_eu.json"
DX_JSON = Path(__file__).resolve().parent / "cycle_dx.json"


def has00(seq: list[int]) -> bool:
    n = len(seq)
    return any(seq[t] == 0 and seq[(t + 1) % n] == 0 for t in range(n))


def has11(seq: list[int]) -> bool:
    n = len(seq)
    return any(seq[t] == 1 and seq[(t + 1) % n] == 1 for t in range(n))


def is_alternating(seq: list[int]) -> bool:
    n = len(seq)
    return n >= 2 and all(seq[t] != seq[(t + 1) % n] for t in range(n))


def run_form(s: list[int]) -> list[int] | None:
    """reconstruct(S, gap(S)) filled from 00-seeds. None if no 00."""
    n = len(s)
    g = gap_parity(s)
    if g is None:
        return None
    ones = [t for t in range(n) if s[t] == 1]
    seeds = [p for p in ones if back_dist(s, p) >= 3]
    if not seeds:
        return None
    u: list[int | None] = [None] * n
    for p in seeds:
        u[p] = 1
    for _ in range(n + 2):
        changed = False
        for p in ones:
            if u[p] is None:
                continue
            free = 1 - (g[p] | u[p])
            k = 1
            while k <= n and s[(p + k) % n] == 0:
                val = free if k <= 2 else 1
                t = (p + k) % n
                if u[t] is None:
                    u[t] = val
                    changed = True
                elif u[t] != val:
                    return None
                k += 1
            if k < n and s[(p + k) % n] == 1 and k <= 2:
                t = (p + k) % n
                if u[t] is None:
                    u[t] = free
                    changed = True
                elif u[t] != free:
                    return None
        if not changed:
            break
    if any(x is None for x in u):
        return None
    return [int(x) for x in u]


def scar_n345(t: list[int]) -> tuple[list[int], list[int], list[int]] | None:
    n3 = reconstruct(t, [1] * len(t))
    if n3 is None:
        return None
    n4 = gap_parity(n3)
    if n4 is None:
        return None
    n5 = reconstruct(n3, n4)
    if n5 is None:
        return None
    return n3, n4, n5


def otype_00_iff_11() -> dict:
    """O-type has 00 iff 11; even n0 always both; odd n0 lacks both iff alt."""
    n_alt = 0
    n_even_00 = 0
    for n0 in range(1, 13):
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            h0, h1 = has00(t), has11(t)
            if h0 != h1:
                return {"ok": False, "n0": n0, "mismatch": True}
            if not h0 and not h1:
                if n0 % 2 == 0 or not is_alternating(t):
                    return {"ok": False, "n0": n0, "alt": True}
                n_alt += 1
            if n0 % 2 == 0:
                if not h0:
                    return {"ok": False, "n0": n0, "even": True}
                n_even_00 += 1
    ok = n_alt == 12 and n_even_00 == sum(1 << n0 for n0 in range(2, 13, 2))
    return {"ok": ok, "n_alt": n_alt, "n_even_00": n_even_00}


def run_identities() -> dict:
    """0-run (free,free,1...); seed U=1 free=0; matches reconstruct."""
    n_match = 0
    n_seed = 0
    for n0 in range(2, 11, 2):
        L = 2 * n0
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            g = gap_parity(s)
            u = reconstruct(s, g)
            got = run_form(s)
            if got != u:
                return {"ok": False, "n0": n0, "mask": mask}
            n_match += 1
            n = L
            for p in range(n):
                if s[p] != 1:
                    continue
                if back_dist(s, p) >= 3:
                    n_seed += 1
                    if u[p] != 1 or (1 - (g[p] | u[p])) != 0:
                        return {"ok": False, "n0": n0, "seed": True}
                run: list[int] = []
                k = 1
                while k <= n and s[(p + k) % n] == 0:
                    run.append(u[(p + k) % n])
                    k += 1
                if len(run) >= 2 and run[0] != run[1]:
                    return {"ok": False, "n0": n0, "copy": True}
                if any(run[i] != 1 for i in range(2, len(run))):
                    return {"ok": False, "n0": n0, "tail": True}
    # generic words with a 00, length 2..8
    n_gen = 0
    for n in range(2, 9):
        for mask in range(1, 1 << n):
            s = [(mask >> i) & 1 for i in range(n)]
            if not has00(s):
                continue
            g = gap_parity(s)
            u = reconstruct(s, g)
            if u is None or run_form(s) != u:
                return {"ok": False, "n": n, "generic": True}
            n_gen += 1
    return {"ok": True, "n_match": n_match, "n_seed": n_seed, "n_gen": n_gen}


def scar_ham_n4_n5() -> dict:
    """ham(n4,n5)=n0 in scar indexing; n5=run_form(n3); even n0 type N."""
    rows: dict[int, dict] = {}
    for n0 in range(1, 11):
        L = 2 * n0
        n_ok = 0
        n_n = 0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            trip = scar_n345(t)
            if trip is None:
                return {"ok": False, "n0": n0, "mask": mask}
            n3, n4, n5 = trip
            if ham(n4, n5) != n0:
                return {"ok": False, "n0": n0, "ham": True}
            if n0 % 2 == 0:
                rf = run_form(n3)
                if rf != n5:
                    return {"ok": False, "n0": n0, "run": True}
                if twocopy_type(n5) != "N" or not any(n5) or n5 == n3 or n5 == n4:
                    return {"ok": False, "n0": n0, "type": True}
                n_n += 1
            n_ok += 1
        rows[n0] = {"n": n_ok, "n_type_N": n_n}
    ok = (
        rows[2]["n_type_N"] == 4
        and rows[8]["n"] == 256
        and rows[10]["n"] == 1024
    )
    return {"ok": ok, "rows": rows}


def one_runs_not_always_alternate() -> dict:
    """Some consecutive 1s of S have equal U in reconstruct(S, gap(S))."""
    for n0 in (2, 4, 6, 8):
        for mask in range(1 << n0):
            s = odd_copy(mask_bits(mask, n0))
            u = reconstruct(s, gap_parity(s))
            n = len(s)
            for t in range(n):
                if s[t] == 1 and s[(t + 1) % n] == 1 and u[t] == u[(t + 1) % n]:
                    return {"ok": True, "n0": n0, "t": t}
    return {"ok": False}


def tstar() -> dict:
    """U=T*||~T*: n5=run_form(n3), ham(n4,n5)=16, n5 type N."""
    t = [int(c) for c in U32]
    trip = scar_n345(t)
    if trip is None:
        return {"ok": False}
    n3, n4, n5 = trip
    ok = (
        has00(n3)
        and run_form(n3) == n5
        and ham(n4, n5) == 16
        and twocopy_type(n5) == "N"
        and any(n5)
        and n5 != n4
    )
    return {"ok": ok, "wt5": sum(n5), "type5": twocopy_type(n5)}


def prefixes() -> dict:
    eu = json.loads(EU_JSON.read_text())
    dx = json.loads(DX_JSON.read_text())
    ok = (
        eu["checks"]["all_ok"]
        and eu["verdict"]["reconstruct_ones_S_is_gap_parity"] == "LEMMA"
        and eu["verdict"]["otype_n3_is_rot_n0_minus_1"] == "LEMMA"
        and eu["verdict"]["prize"] == "unsolved"
        and dx["checks"]["all_ok"]
        and dx["lemmas"]["ham_n3_n4_equals_n0_all_O_type"] is True
    )
    return {"ok": ok}


def self_checks(
    c20, oo: dict, run: dict, hamd: dict, ts: dict, alt: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert oo["ok"] and run["ok"] and hamd["ok"] and ts["ok"]
    assert alt["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    oo = otype_00_iff_11()
    run = run_identities()
    hamd = scar_ham_n4_n5()
    ts = tstar()
    alt = one_runs_not_always_alternate()
    pref = prefixes()
    checks = self_checks(c20, oo, run, hamd, ts, alt, pref)
    dump = {
        "cycle": "EV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "otype_00": {k: oo[k] for k in oo if k != "ok"},
        "run": {k: run[k] for k in run if k != "ok"},
        "ham_n4_n5": {str(k): v for k, v in hamd["rows"].items()},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "one_run_equal": {k: alt[k] for k in alt if k != "ok"},
        "lemmas": {
            "otype_00_iff_11": True,
            "even_n0_O_has_00": True,
            "reconstruct_S_gap_run_form": True,
            "scar_n5_is_run_form_of_n3": True,
            "scar_ham_n4_n5_equals_n0": True,
            "even_n0_n5_type_N": True,
            "n5_is_gap_n4": False,
            "even_n0_O_can_lack_00": False,
            "n5_one_runs_always_alternate": False,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "otype_00_iff_11": "LEMMA",
            "even_n0_O_has_00": "LEMMA",
            "reconstruct_S_gap_run_form": "LEMMA",
            "scar_n5_is_run_form_of_n3": "LEMMA",
            "scar_ham_n4_n5_equals_n0": "LEMMA",
            "even_n0_n5_type_N": "LEMMA",
            "n5_is_gap_n4": "KILLED",
            "even_n0_O_can_lack_00": "KILLED",
            "n5_one_runs_always_alternate": "KILLED",
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
    print("run", dump["run"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
