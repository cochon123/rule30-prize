#!/usr/bin/env python3
"""Period-2 unique left of an alternating even-right neighbor.

If a phase-01 period-2 centre has even right neighbor u strictly
alternating, the unique left is an explicit period-7 word (1000000 if
u_0=0, 0110010 if u_0=1). The 8-bit (F,G,F',G') FSM returns after 7
column steps, so the formula is infinite — a Condrey-style closed form
for this class. The finite rights 000001 and 1001 realise the two
oscillators through the certified horizon; generic rights do not.

This does not exclude eventual period 2 for every finite row: Jen
already forbids eventually-periodic u for a finite seed, and the
remaining obstruction is aperiodic u. Not a prize claim.

Run: python3 research/period2_mod7.py --certify
Dump: research/period2_mod7.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from period2_fiber import bits_from_int, evolve_centers, fiber_left
from period2_left_edge import anf_str, compute_columns, eval_anf

OUT = Path(__file__).resolve().with_suffix(".json")

PAT0 = "1000000"  # u_0 = 0, L_k = 1 iff k ≡ 1 (mod 7)
PAT1 = "0110010"  # u_0 = 1


def word(pat: str, T: int) -> list[int]:
    return [int(pat[(k - 1) % 7]) for k in range(1, T + 1)]


def fsm(u0: int, kmax: int):
    """Column recurrences on u = (u0, 1-u0, u0, ...) and its shift."""
    F = [0, 1 ^ u0]
    G = [1, 1]
    Fp = [0, 1 ^ (1 - u0)]
    Gp = [1, 1]
    states = []
    for k in range(2, kmax + 1):
        states.append(
            (
                F[k - 1],
                F[k - 2],
                G[k - 1],
                G[k - 2],
                Fp[k - 1],
                Fp[k - 2],
                Gp[k - 1],
                Gp[k - 2],
            )
        )
        F.append(G[k - 1] ^ (F[k - 1] | F[k - 2]))
        G.append(Fp[k - 1] ^ (G[k - 1] | G[k - 2]))
        Fp.append(Gp[k - 1] ^ (Fp[k - 1] | Fp[k - 2]))
        Gp.append(F[k - 1] ^ (Gp[k - 1] | Gp[k - 2]))
    return F, G, Fp, Gp, states


def pack_u_bits(u0: int, nvars: int) -> int:
    bits = 0
    for i in range(nvars):
        if (u0 + i) & 1:
            bits |= 1 << i
    return bits


def scan_ef0(w_max: int, T: int) -> list[dict]:
    hits = []
    for w in range(0, w_max + 1):
        for n in range(1 << w):
            right = bits_from_int(n, w)
            fib = fiber_left(right, 0, T)
            if any(fib["eu"]) or any(fib["fu"]):
                continue
            u = fib["u"]
            u0 = u[0] if u else 0
            osc = all(u[i] == ((u0 + i) & 1) for i in range(len(u)))
            pat = PAT0 if u0 == 0 else PAT1
            left = fib["left"]
            pred = word(pat, T)
            hits.append(
                {
                    "w": w,
                    "right": "".join(map(str, right)) or "vac",
                    "u0": u0,
                    "u_alternating": osc,
                    "left_matches_mod7": left == pred,
                }
            )
    return hits


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict = {}

    prize = evolve_centers(1, 0, 16)
    checks["prize_prefix16"] = "".join(map(str, prize))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == "1101110011000101"

    # FSM 7-cycle for both oscillators.
    fsm_info = {}
    for u0, pat in ((0, PAT0), (1, PAT1)):
        F, G, Fp, Gp, states = fsm(u0, 30)
        fbits = "".join(map(str, F[1:]))
        pred = pat * 5
        cycle = all(states[i] == states[i + 7] for i in range(len(states) - 7))
        match = fbits.startswith(pat * 3)
        ones = pat.count("1")
        fsm_info[str(u0)] = {
            "pat": pat,
            "F_1_to_21": fbits[:21],
            "state_7cycle": cycle,
            "F_matches_pat": match,
            "ones_per_period": ones,
        }
        assert cycle, u0
        assert match, (u0, fbits[:21])
        assert ones >= 1
        # A 1 in every period => infinitely many 1s on the infinite word.
        assert all(F[1 + 7 * m] == int(pat[0]) for m in range(4))
    checks["fsm_7cycle_both"] = True
    checks["fsm_F_matches_both"] = True

    # ANF F_k on (01)^∞ and (10)^∞ agrees through k=16.
    F_anf, _G_anf = compute_columns(16, reduce=True)
    anf_ok = True
    anf_rows = []
    for u0, pat in ((0, PAT0), (1, PAT1)):
        ubits = pack_u_bits(u0, 16)
        pred = word(pat, 16)
        got = [eval_anf(F_anf[k], ubits) for k in range(1, 17)]
        if got != pred:
            anf_ok = False
        anf_rows.append(
            {
                "u0": u0,
                "F_anf": [anf_str(F_anf[k]) for k in range(0, 17)],
                "eval": got,
                "pred": pred,
            }
        )
    checks["anf_matches_fsm_k_le_16"] = anf_ok
    assert anf_ok

    # L_1 XOR L_2 = 1 for every u (polynomial identity).
    checks["F1_xor_F2_is_one"] = anf_str(F_anf[1] ^ F_anf[2]) == "1"
    assert checks["F1_xor_F2_is_one"]

    # Kernel 000001 and dual 1001: even-time e=f=0 and u alternating.
    T = 256
    kernels = []
    for right, u0, pat in (
        ([0, 0, 0, 0, 0, 1], 0, PAT0),
        ([1, 0, 0, 1], 1, PAT1),
    ):
        fib = fiber_left(right, 0, T)
        u_ok = all(fib["u"][i] == ((u0 + i) & 1) for i in range(len(fib["u"])))
        ef0 = (not any(fib["eu"])) and (not any(fib["fu"]))
        left_ok = fib["left"] == word(pat, T)
        # Prefix stable.
        left64 = fiber_left(right, 0, 64)["left"]
        stable = left64 == fib["left"][:64]
        rec = {
            "right": "".join(map(str, right)),
            "u0": u0,
            "T": T,
            "u_alternating": u_ok,
            "even_ef_zero": ef0,
            "left_mod7": left_ok,
            "prefix_stable": stable,
            "n_u": len(fib["u"]),
        }
        kernels.append(rec)
        assert u_ok and ef0 and left_ok and stable, rec
    checks["kernels_T256"] = True

    # Vacuum triple at t=0 for 000001: (u,e,f)=(0,0,0) forces u_1=1.
    k0 = fiber_left([0, 0, 0, 0, 0, 1], 0, 8)
    checks["kernel_u0_ef0"] = k0["u"][0] == 0 and k0["eu"][0] == 0 and k0["fu"][0] == 0
    checks["kernel_u1"] = k0["u"][1] == 1
    assert checks["kernel_u0_ef0"] and checks["kernel_u1"]

    # Vacuum right is NOT an oscillator (period-7 u-attractor is only transient).
    vac = fiber_left([], 0, 80)
    vac_osc = all(vac["u"][i] == (i & 1) for i in range(len(vac["u"])))
    checks["vacuum_not_oscillator"] = not vac_osc
    assert checks["vacuum_not_oscillator"]

    # Prefix 000001 is not freely extendable: 00000111 breaks e=f=0.
    bad = fiber_left([0, 0, 0, 0, 0, 1, 1, 1], 0, 64)
    checks["00000111_breaks_ef0"] = any(bad["eu"]) or any(bad["fu"])
    assert checks["00000111_breaks_ef0"]

    family = scan_ef0(8, 64)
    checks["family_all_alternating"] = all(h["u_alternating"] for h in family)
    checks["family_all_mod7"] = all(h["left_matches_mod7"] for h in family)
    checks["family_n"] = len(family)
    checks["family_has_kernel"] = any(h["right"] == "000001" for h in family)
    checks["family_has_dual"] = any(h["right"] == "1001" for h in family)
    checks["family_no_vacuum"] = all(h["right"] != "vac" for h in family)
    assert checks["family_all_alternating"] and checks["family_all_mod7"]
    assert checks["family_has_kernel"] and checks["family_has_dual"]
    assert checks["family_no_vacuum"]

    # e=f=0 implies u_{n+1}=1-u_n via the vacuum-triple identity.
    # Checked on every family member's u (already u_alternating).
    checks["ef0_implies_alternating"] = True

    checks["all_ok"] = all(
        v is True
        for k, v in checks.items()
        if k
        not in (
            "prize_prefix16",
            "family_n",
        )
    )
    assert checks["all_ok"]

    wall = time.perf_counter() - t0
    dump = {
        "attack": "period2_mod7",
        "problem": (
            "closed-form unique left for a period-2 centre whose even "
            "right neighbor is strictly alternating"
        ),
        "verdict": "LEMMA",
        "kill": False,
        "survive": False,
        "prize": False,
        "kill_reason": (
            "alternating u gives an explicit period-7 infinite left; "
            "finite seeds with eventually-periodic u are already "
            "Jen-excluded; aperiodic u remains open"
        ),
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "fsm": fsm_info,
        "kernels": kernels,
        "family_w_le_8": family,
        "patterns": {"u0=0": PAT0, "u0=1": PAT1},
        "anf_eval": [
            {"u0": r["u0"], "eval": r["eval"], "pred": r["pred"]} for r in anf_rows
        ],
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict=LEMMA wall={wall:.3f}s family={len(family)}")
    print(f"fsm0={fsm_info['0']['F_1_to_21']} fsm1={fsm_info['1']['F_1_to_21']}")
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
