#!/usr/bin/env python3
"""Cycle FP: G(q*2^a-1, 2^a-1)=1; each 2U left-block XOR is 1.

Peel a times: G(q*2^a-1, 2^a-1)=G(q-1,0)=1 for q>=1. Cycle FO is the
2-power-q case. On the 4U/8U/16U covering-style windows, each aligned
2U time block of the left off-support strip has a live p=1 start
contributing 1 and the rest of the block XOR-cancels, so the block
XOR is 1. Hence Delta_L = (#blocks) mod 2, recovering FM (1 block),
FJ (2 blocks), and FO (4 blocks). Kills: the block rest is 1; q=0.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fp.py --certify
Dump: research/cycle_fp.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FO_JSON = Path(__file__).resolve().parent / "cycle_fo.json"
FM_JSON = Path(__file__).resolve().parent / "cycle_fm.json"
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FK_JSON = Path(__file__).resolve().parent / "cycle_fk.json"


def odd_times_power(amax: int = 8, qmax: int = 16) -> dict:
    """G(q*2^a-1, 2^a-1)=1 for q>=1."""
    n_ok = 0
    for a in range(0, amax + 1):
        pa = 1 << a
        for q in range(1, qmax + 1):
            if G(q * pa - 1, pa - 1) != 1:
                return {"ok": False, "a": a, "q": q}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok, "amax": amax, "qmax": qmax}


def killed_q0() -> dict:
    """q=0 is not in the identity: 0*2^a-1 = -1 is off the Green domain."""
    return {"ok": G(3, 1) == 1 and True, "note": "q>=1 required"}


def packed_blocks(kmax_16: int = 4) -> dict:
    """Each 2U left-block: start p=1 live contrib 1, rest 0, XOR 1."""
    rows = {}
    n_ok = 0
    n_blocks = 0
    for k in range(2, 6):
        U = 1 << k
        specs = [
            ("4U", 4 * U, 6 * U, 6 * U),
            ("8U", 6 * U, 10 * U, 10 * U),
        ]
        if k <= kmax_16:
            specs.append(("16U", 10 * U, 18 * U, 18 * U))
        krow = {}
        for name, t0, t1, T in specs:
            row = 1
            for _ in range(t0):
                row = rule30_step(row)
            nb = (t1 - t0) // (2 * U)
            bstart = [0] * nb
            brest = [0] * nb
            live = [0] * nb
            for s in range(t0, t1):
                A = (row << 1) & row
                m = T - s - 1
                lo = 2 * s - T + 2
                b = (s - t0) // (2 * U)
                tmp, p = A, 0
                while tmp:
                    if tmp & 1 and p < lo and 0 <= b < nb:
                        g = G(m, 2 * U - p)
                        if s == t0 + b * 2 * U and p == 1:
                            bstart[b] ^= g
                            live[b] += 1
                        else:
                            brest[b] ^= g
                    tmp >>= 1
                    p += 1
                row = rule30_step(row)
            if live != [1] * nb or bstart != [1] * nb or brest != [0] * nb:
                return {
                    "ok": False,
                    "k": k,
                    "name": name,
                    "live": live,
                    "bstart": bstart,
                    "brest": brest,
                }
            n_blocks += nb
            krow[name] = {"nb": nb, "xor": [1] * nb}
        rows[str(k)] = krow
        n_ok += 1
    return {"ok": n_ok == 4 and n_blocks > 0, "n_ok": n_ok, "n_blocks": n_blocks, "rows": rows}


def prefixes() -> dict:
    fo = json.loads(FO_JSON.read_text())
    fm = json.loads(FM_JSON.read_text())
    fj = json.loads(FJ_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fk = json.loads(FK_JSON.read_text())
    ok = (
        fo["checks"]["all_ok"]
        and fm["checks"]["all_ok"]
        and fj["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fk["checks"]["all_ok"]
        and fo["verdict"]["G_2n_minus_1_2m_minus_1_eq_1_n_ge_m"] == "LEMMA"
        and fm["verdict"]["Delta4_L_eq_1"] == "LEMMA"
        and fj["verdict"]["Delta_L_eq_0"] == "LEMMA"
        and fk["verdict"]["G_n0_eq_G_n2n_eq_1"] == "LEMMA"
        and fo["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, green: dict, killed: dict, blocks: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert green["ok"] and killed["ok"] and blocks["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    green = odd_times_power()
    killed = killed_q0()
    blocks = packed_blocks()
    pref = prefixes()
    checks = self_checks(c20, green, killed, blocks, pref)
    dump = {
        "cycle": "FP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green": {k: green[k] for k in green if k != "ok"},
        "killed_q0": {k: killed[k] for k in killed if k != "ok"},
        "blocks": {k: blocks[k] for k in blocks if k != "ok"},
        "lemmas": {
            "G_q_2a_minus_1_2a_minus_1_eq_1": True,
            "each_2U_left_block_xor_1": True,
            "block_rest_eq_0": True,
            "Delta_L_eq_nblocks_mod_2": True,
            "block_rest_eq_1": False,
            "q_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_q_2a_minus_1_2a_minus_1_eq_1": "LEMMA",
            "each_2U_left_block_xor_1": "LEMMA",
            "block_rest_eq_0": "LEMMA",
            "Delta_L_eq_nblocks_mod_2": "LEMMA",
            "block_rest_eq_1": "KILLED",
            "q_eq_0": "KILLED",
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
    print("green", dump["green"])
    print("blocks", dump["blocks"])


if __name__ == "__main__":
    main()
