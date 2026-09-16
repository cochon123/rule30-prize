#!/usr/bin/env python3
"""Period-2 unique left of a periodic even-right neighbor.

If a phase-01 period-2 centre has even right neighbor u of any finite
period p, the p-phase column FSM is a finite automaton. The global-zero
state is a fixed point with no other predecessor, hence unreachable from
G_0=1. Therefore F_k is not eventually 0: the unique left is spatially
eventually periodic and infinite. This is the Condrey-style infinitude
for the whole periodic-u class (period2_mod7 is the p=2 closed form).

Finite seeds with eventually-periodic u are already Jen-excluded. The
remaining obstruction is aperiodic u. Not a prize claim.

Run: python3 research/period2_periodic.py --certify
Dump: research/period2_periodic.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from period2_left_edge import compute_columns, eval_anf
from period2_mod7 import PAT0, PAT1, fsm as fsm_mod7
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")


def or2(a: int, b: int) -> int:
    return a | b


def step_phases(F1, F2, G1, G2):
    """One column step on p phases. F1=F_{k-1}, F2=F_{k-2}."""
    p = len(F1)
    Fnew = [G1[j] ^ or2(F1[j], F2[j]) for j in range(p)]
    Gnew = [F1[(j + 1) % p] ^ or2(G1[j], G2[j]) for j in range(p)]
    return Fnew, F1[:], Gnew, G1[:]


def zero_state(p: int):
    z = [0] * p
    return z, z, z, z


def is_zero(F1, F2, G1, G2) -> bool:
    return not any(F1) and not any(F2) and not any(G1) and not any(G2)


def initial_state(u_pat):
    p = len(u_pat)
    F1 = [1 ^ u_pat[j] for j in range(p)]  # F_1
    F2 = [0] * p  # F_0
    G1 = [1] * p  # G_1
    G2 = [1] * p  # G_0
    return F1, F2, G1, G2


def pack_state(F1, F2, G1, G2) -> tuple:
    return (tuple(F1), tuple(F2), tuple(G1), tuple(G2))


def unpack_int(s: int, p: int):
    """16-bit-per-phase packing is overkill; use 4 bits per phase."""
    F1, F2, G1, G2 = [], [], [], []
    for j in range(p):
        nibble = (s >> (4 * j)) & 15
        F1.append(nibble & 1)
        F2.append((nibble >> 1) & 1)
        G1.append((nibble >> 2) & 1)
        G2.append((nibble >> 3) & 1)
    return F1, F2, G1, G2


def preimages_of_zero(p: int) -> list:
    """Enumerate states mapping to global zero. Algebra: only zero."""
    n = 1 << (4 * p)
    hits = []
    z = zero_state(p)
    for s in range(n):
        st = unpack_int(s, p)
        nxt = step_phases(*st)
        if is_zero(*nxt):
            hits.append(st)
    return hits


def orbit(u_pat, kmax: int):
    st = initial_state(u_pat)
    F0 = [0, 1 ^ u_pat[0]]
    G0 = [1, 1]
    seen = {}
    F1, F2, G1, G2 = st
    for k in range(2, kmax + 1):
        key = pack_state(F1, F2, G1, G2)
        if key in seen:
            k0 = seen[key]
            return {
                "cycled": True,
                "k0": k0,
                "period": k - k0,
                "F": F0,
                "has1_cycle": 1 in F0[k0:],
                "n1_cycle": sum(F0[k0:]),
            }
        seen[key] = k
        F1, F2, G1, G2 = step_phases(F1, F2, G1, G2)
        F0.append(F1[0])
        G0.append(G1[0])
    return {
        "cycled": False,
        "kmax": kmax,
        "F": F0,
        "has1_cycle": 1 in F0,
        "n1_cycle": sum(F0),
    }


def fsm_F(u_pat, kmax: int) -> list[int]:
    F1, F2, G1, G2 = initial_state(u_pat)
    F0 = [0, 1 ^ u_pat[0]]
    for _k in range(2, kmax + 1):
        F1, F2, G1, G2 = step_phases(F1, F2, G1, G2)
        F0.append(F1[0])
    return F0


def spatial_ok(u_pat, kmax: int) -> bool:
    """G_k = F_{k+1} XOR (F_k OR F_{k-1}) on phase 0."""
    p = len(u_pat)
    F = [[0, 1 ^ u_pat[j]] for j in range(p)]
    G = [[1, 1] for j in range(p)]
    F1 = [F[j][1] for j in range(p)]
    F2 = [F[j][0] for j in range(p)]
    G1 = [G[j][1] for j in range(p)]
    G2 = [G[j][0] for j in range(p)]
    for k in range(2, kmax + 1):
        F1, F2, G1, G2 = step_phases(F1, F2, G1, G2)
        for j in range(p):
            F[j].append(F1[j])
            G[j].append(G1[j])
    for k in range(1, kmax):
        got = G[0][k]
        pred = F[0][k + 1] ^ or2(F[0][k], F[0][k - 1])
        if got != pred:
            return False
    return True


def circular_ugap(p: int) -> list[list[int]]:
    out: list[list[int]] = []

    def rec(seq: list[int]) -> None:
        if len(seq) == p:
            s = seq + seq
            run = 0
            ok = True
            for b in s:
                if b:
                    run = 0
                else:
                    run += 1
                    if run >= 5:
                        ok = False
                        break
            if ok:
                for i in range(p):
                    if seq[i] and seq[(i + 1) % p]:
                        ok = False
                        break
            if ok:
                out.append(seq[:])
            return
        if len(seq) < 4 or seq[-4:] != [0, 0, 0, 0]:
            seq.append(0)
            rec(seq)
            seq.pop()
        if not seq or seq[-1] == 0:
            seq.append(1)
            rec(seq)
            seq.pop()

    rec([])
    return out


def certify() -> dict:
    t0 = time.perf_counter()
    checks: dict = {}

    # Unique preimage of global zero for p=1,2,3,4.
    pre = {}
    for p in (1, 2, 3, 4):
        hits = preimages_of_zero(p)
        only_zero = len(hits) == 1 and is_zero(*hits[0])
        pre[str(p)] = {"n": len(hits), "only_zero": only_zero}
        assert only_zero, (p, hits)
        assert not is_zero(*initial_state([0] * p))
    checks["zero_unique_preimage_p_le_4"] = True
    checks["initial_G0_not_zero"] = True

    # p=1 vacuum: F_k = k mod 2.
    Fvac = fsm_F([0], 40)
    checks["vacuum_F_is_k_mod_2"] = Fvac == [k & 1 for k in range(41)]
    assert checks["vacuum_F_is_k_mod_2"]

    # p=2 recovers period2_mod7.
    F01 = fsm_F([0, 1], 30)
    F10 = fsm_F([1, 0], 30)
    pred01 = [0] + [int(PAT0[(k - 1) % 7]) for k in range(1, 31)]
    pred10 = [0] + [int(PAT1[(k - 1) % 7]) for k in range(1, 31)]
    checks["p2_01_is_PAT0"] = F01 == pred01
    checks["p2_10_is_PAT1"] = F10 == pred10
    Fm = fsm_mod7(0, 30)[0]
    checks["p2_matches_mod7_fsm"] = F01 == Fm
    assert checks["p2_01_is_PAT0"] and checks["p2_10_is_PAT1"]
    assert checks["p2_matches_mod7_fsm"]

    # FSM equals the ANF fold on a periodic prefix (exact for F_0..F_K).
    F_anf, _ = compute_columns(16, reduce=True)
    anf_ok = True
    for u_pat in ([0], [0, 1], [1, 0], [0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 0, 0]):
        K = 16
        nv = nvars(K)
        bits = 0
        for i in range(nv):
            if u_pat[i % len(u_pat)]:
                bits |= 1 << i
        fold = F_of_u([u_pat[i % len(u_pat)] for i in range(nv)], K)[0]
        fsmv = fsm_F(u_pat, K)
        ev = [eval_anf(F_anf[k], bits) for k in range(K + 1)]
        if fold != fsmv or ev != fsmv:
            anf_ok = False
    checks["fsm_matches_fold_and_anf"] = anf_ok
    assert anf_ok

    # Spatial identity on the p-phase recurrences.
    spat = True
    for u_pat in ([0], [0, 1], [1, 0], [0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0, 1]):
        if not spatial_ok(u_pat, 48):
            spat = False
    checks["spatial_identity_periodic"] = spat
    assert spat

    # Every circular ugap word of period p<=7 has a 1 in its F-cycle.
    scan = []
    all_have_1 = True
    for p in range(1, 8):
        words = circular_ugap(p)
        n_cyc = 0
        n1 = 0
        for w in words:
            info = orbit(w, 8000)
            if info["cycled"]:
                n_cyc += 1
                if info["has1_cycle"]:
                    n1 += 1
                else:
                    all_have_1 = False
            elif 1 in info["F"][1:]:
                n1 += 1
            else:
                all_have_1 = False
        scan.append({"p": p, "n": len(words), "cycled": n_cyc, "with_1": n1})
        assert n_cyc == len(words), (p, n_cyc, len(words))
        assert n1 == len(words)
    checks["p_le_7_all_cycled"] = True
    checks["p_le_7_cycle_has_1"] = all_have_1
    assert all_have_1

    # p=4 word 0001: explicit period-7 tail after 11 columns.
    F0001 = fsm_F([0, 0, 0, 1], 40)
    tail = "".join(str(b) for b in F0001[11:11 + 21])
    checks["p4_0001_tail"] = tail
    checks["p4_0001_period7"] = tail == "0000010" * 3
    assert checks["p4_0001_period7"]
    assert 1 in F0001[11:18]

    checks["all_ok"] = True
    wall = time.perf_counter() - t0
    dump = {
        "attack": "period2_periodic",
        "problem": (
            "unique left of a period-2 centre whose even right neighbor "
            "is periodic of any finite period"
        ),
        "verdict": "LEMMA",
        "kill": False,
        "survive": False,
        "prize": False,
        "kill_reason": (
            "periodic u forces a spatially eventually-periodic infinite "
            "left; finite seeds with eventually-periodic u are already "
            "Jen-excluded; aperiodic u remains open"
        ),
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "zero_preimages": pre,
        "p_le_7_scan": scan,
        "patterns": {"u=01": PAT0, "u=10": PAT1, "u=0001_tail": "0000010"},
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict=LEMMA wall={wall:.3f}s scan={scan}")
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
