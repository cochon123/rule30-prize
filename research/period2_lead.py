#!/usr/bin/env python3
"""Leading variable of F_{2n+1} is u_n.

On a phase-01 period-2 centre, F_{2n+1}=u_n XOR Q_n(u_0,...,u_{n-1})
in the Fibonacci ring. So an L_0 tail F_k=0 for k>T forces a unique
continuation of u past nvars(T). This is the tail-forcing identity for
the uniform L_0 attack. It does not kill L_0: the T=20 last-sat words
obey the forcing through n=17 and still die only at F_37. Not a prize
claim.

Run: python3 research/period2_lead.py --certify
Dump: research/period2_lead.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from period2_left_edge import anf_vars, compute_columns
from period2_vacuum import F_of_u, nvars, vacuum_pair

OUT = Path(__file__).resolve().with_suffix(".json")

# T=20 last-sat words from research/period2_certificate.md
T20_WORDS = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
]


def lin_un(anf: int, n: int) -> int:
    """Coefficient of the monomial u_n in an ANF integer."""
    return (anf >> (1 << n)) & 1


def Q_n(u_prefix: list[int], n: int) -> int:
    """F_{2n+1} with u_n forced to 0 (equals Q_n on that prefix)."""
    bits = list(u_prefix)
    if len(bits) < n + 1:
        bits.extend([0] * (n + 1 - len(bits)))
    bits[n] = 0
    return F_of_u(bits, 2 * n + 1)[0][2 * n + 1]


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict = {}

    F_anf, G_anf = compute_columns(16, reduce=True)
    anf_rows = []
    for n in range(0, 8):
        k = 2 * n + 1
        lin = lin_un(F_anf[k], n)
        early = [j for j in range(k) if n in anf_vars(F_anf[j])]
        g_early = [j for j in range(2 * n) if n in anf_vars(G_anf[j])]
        rec = {
            "n": n,
            "k": k,
            "lin_un": lin,
            "early_F": early,
            "early_G_lt_2n": g_early,
            "G_2n_lin": lin_un(G_anf[2 * n], n) if (n >= 1 and 2 * n <= 16) else None,
        }
        anf_rows.append(rec)
        assert lin == 1, rec
        assert early == [], rec
        assert g_early == [], rec
        if n >= 1 and 2 * n <= 16:
            assert rec["G_2n_lin"] == 1, rec
    checks["anf_lin_un_n_le_7"] = True
    checks["anf_un_not_before_F_2n1"] = True
    checks["anf_G_2n_lin_un"] = True

    # Single-1 fold: F_{2n+1}(e_n)=0 = 1 XOR 1, and F_k for k<=2n is vacuum.
    n_max = 48
    Fvac, _ = vacuum_pair(2 * n_max + 4)
    fold_ok = True
    for n in range(0, n_max + 1):
        u = [0] * (n + 1)
        u[n] = 1
        Ff, _ = F_of_u(u, 2 * n + 4)
        if Ff[2 * n + 1] != 0:
            fold_ok = False
            break
        if any(Ff[j] != Fvac[j] for j in range(2 * n + 1)):
            fold_ok = False
            break
        if Fvac[2 * n + 1] != 1:
            fold_ok = False
            break
    checks["fold_en_n_le_48"] = fold_ok
    checks["vacuum_odd_is_one"] = all(Fvac[2 * n + 1] == 1 for n in range(0, n_max + 1))
    assert fold_ok and checks["vacuum_odd_is_one"]

    # Variable bound: nvars(2n+1)=n+1, nvars(2n)=n.
    vb = all(nvars(2 * n + 1) == n + 1 and nvars(2 * n) == n for n in range(1, 40))
    checks["nvars_2n1_is_n_plus_1"] = vb
    assert vb

    # T=20 last-sat words obey u_n = Q_n for n=10..17 (odd columns past T).
    t20 = []
    t20_ok = True
    for wi, w in enumerate(T20_WORDS):
        nv = nvars(38)
        bits = w + [0] * (nv - len(w))
        Ff, _ = F_of_u(bits, 38)
        force = []
        for n in range(10, 18):
            q = Q_n(bits, n)
            force.append({"n": n, "u": bits[n], "Q": q, "F_odd": Ff[2 * n + 1]})
            if bits[n] != q or Ff[2 * n + 1] != 0:
                t20_ok = False
        t20.append(
            {
                "i": wi,
                "F20": Ff[20],
                "F37": Ff[37],
                "force": force,
            }
        )
        assert Ff[20] == 1 and Ff[37] == 1
        assert all(Ff[k] == 0 for k in range(21, 37))
    checks["t20_forcing_n_10_17"] = t20_ok
    assert t20_ok

    checks["all_ok"] = True
    wall = time.perf_counter() - t0
    dump = {
        "attack": "period2_lead",
        "problem": "leading variable of F_{2n+1} and L_0 tail forcing",
        "verdict": "LEMMA",
        "kill": False,
        "survive": False,
        "prize": False,
        "kill_reason": (
            "u_n is the leading variable of F_{2n+1}, so an L_0 tail "
            "forces a unique continuation of u; the T=20 models obey "
            "that forcing and still only die at F_37. Not a uniform R."
        ),
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "anf": anf_rows,
        "t20_forcing": [
            {"i": r["i"], "F20": r["F20"], "F37": r["F37"],
             "u_eq_Q": [x["u"] == x["Q"] for x in r["force"]]}
            for r in t20
        ],
        "n_fold": n_max,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict=LEMMA wall={wall:.3f}s n_fold={n_max}")
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
