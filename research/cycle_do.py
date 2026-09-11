#!/usr/bin/env python3
"""Cycle DO: π formula and odd-iff-pow2 through k=19; k=17..19 high halves empty.

Cycle DE gave π_k=2^{ceil(log2 k)} and the period-H seed through k=18, with
odd ident-0 in (W,2W] iff k is a 2-power through k=16. Packed unique
continuation extends that odd census through k=19: the k=17,18,19 high
halves contain neither odd nor even ident-0, π_19=32, and F^H(L_19(2W))
equals L_19(2W). Combined with DE, odd-iff-pow2 holds through k=19.
Not a prize claim: the formula remains a prefix.

Run: python3 research/cycle_do.py --certify
Dump: research/cycle_do.json
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
from cycle_ca import (
    KNOWN20,
    apply_n,
    left_at_2W,
    left_step,
    min_period,
    packed_center_bits,
    prize_cycle,
)
from cycle_de import EXPECTED_ODD_P, formula_divides_H, pi_formula
from cycle_df import unfold
from cycle_dm import pack_bits, reconstruct_int

OUT = Path(__file__).resolve().with_suffix(".json")
DE_JSON = Path(__file__).resolve().parent / "cycle_de.json"
NEW_K = (17, 18, 19)


def unfold_int(a: int, n: int) -> int:
    """u_0=0, u_{t+1}=a_t xor u_t, packed, length n."""
    u = 0
    acc = 0
    for t in range(n - 1):
        acc ^= (a >> t) & 1
        u |= acc << (t + 1)
    return u


def unfold_int_matches() -> bool:
    for n in (4, 8, 16, 32):
        for mask in range(min(1 << n, 64)):
            a = [(mask >> i) & 1 for i in range(n)]
            if unfold_int(pack_bits(a), n) != pack_bits(unfold(a)):
                return False
    return True


def de_prefix() -> dict:
    de = json.loads(DE_JSON.read_text())
    pis = de["pis"]
    odd = {int(k): v for k, v in de["odd_high_p"].items()}
    ok = (
        de["checks"]["all_ok"]
        and pis == [pi_formula(k) for k in range(1, 19)]
        and odd == EXPECTED_ODD_P
        and de["even_high_n15"] == 2
        and formula_divides_H()
    )
    return {"ok": ok, "pis": pis, "odd": odd}


def seed_k19() -> dict:
    k = 19
    W = 1 << k
    H = W >> 1
    w = left_at_2W(k)
    pi = min_period(w, W)
    seed = apply_n(w, W, H) == w
    ok = pi == pi_formula(k) == 32 and seed and H % pi == 0
    return {"ok": ok, "pi": pi, "seed": seed, "word": w}


def pack_cols(cyc: list[int], n_cols: int, pi: int) -> list[int]:
    cols = [0] * n_cols
    for t, word in enumerate(cyc):
        ww = word
        for p in range(n_cols):
            cols[p] |= (ww & 1) << t
            ww >>= 1
            if ww == 0:
                break
    return cols


def cycle_from(word: int, k: int) -> tuple[int, list[int]]:
    W = 1 << k
    pi = min_period(word, W)
    cyc: list[int] = []
    x = word
    for _ in range(pi):
        cyc.append(x)
        x = left_step(x, W)
    return pi, cyc


def high_half_packed(k: int, word: int | None = None) -> dict:
    """Ident-0 census in (W,2W] via packed reconstruct. Expect none for k=17..19."""
    if word is None:
        pi, cyc = prize_cycle(k)
    else:
        pi, cyc = cycle_from(word, k)
    W = 1 << k
    if pi != pi_formula(k):
        return {"ok": False, "k": k, "pi": pi}
    cols = pack_cols(cyc, W + 1, pi)
    # extend array for high half
    cols.extend([0] * W)
    n_odd = 0
    n_even = 0
    odds: list[int] = []
    for p in range(W + 1, 2 * W + 1):
        a = cols[p - 2]
        b = cols[p - 1]
        if b == 0:
            sm = a.bit_count() & 1
            if sm == 1:
                n_odd += 1
                odds.append(p)
                u = unfold_int(a, pi)
                u |= ((u ^ ((1 << pi) - 1)) << pi)
                cols[p] = u
                return {"ok": False, "k": k, "odd_p": p, "n_odd": n_odd}
            n_even += 1
            cols[p] = unfold_int(a, pi)
        else:
            u = reconstruct_int(a, b, pi)
            if u is None:
                return {"ok": False, "k": k, "p": p, "why": "recon"}
            cols[p] = u
    pow2 = k > 0 and (k & (k - 1)) == 0
    ok = n_odd == (1 if pow2 else 0) and n_even == 0
    return {
        "ok": ok,
        "k": k,
        "pi": pi,
        "n_odd": n_odd,
        "n_even": n_even,
        "odds": odds,
    }


def self_checks(c20, unfold_ok: bool, de: dict, seed: dict, highs: list[dict]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert unfold_ok and de["ok"] and seed["ok"]
    assert seed["pi"] == 32
    assert all(h["ok"] and h["n_odd"] == 0 and h["n_even"] == 0 for h in highs)
    assert [h["k"] for h in highs] == list(NEW_K)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    unfold_ok = unfold_int_matches()
    de = de_prefix()
    seed = seed_k19()
    highs = [
        high_half_packed(k, seed["word"] if k == 19 else None)
        for k in NEW_K
    ]
    checks = self_checks(c20, unfold_ok, de, seed, highs)
    dump = {
        "cycle": "DO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "pi_19": seed["pi"],
        "high": {str(h["k"]): {"n_odd": h["n_odd"], "n_even": h["n_even"], "pi": h["pi"]} for h in highs},
        "lemmas": {
            "unfold_int_matches_list": True,
            "pi_formula_k_le_19": True,
            "period_H_seed_k_le_19": True,
            "odd_high_toggle_iff_k_pow2_le_19": True,
            "k_17_18_19_high_no_ident0": True,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "unfold_int_matches_list": "LEMMA",
            "pi_formula_k_le_19": "LEMMA",
            "period_H_seed_k_le_19": "LEMMA",
            "odd_high_toggle_iff_k_pow2_le_19": "LEMMA",
            "k_17_18_19_high_no_ident0": "LEMMA",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("pi_19", dump["pi_19"])
    print("high", dump["high"])


if __name__ == "__main__":
    main()
