"""Cycle Q: Morse–Hedlund of L_0 germs, realizable (u,e,f) automaton, q=8 drive.

Three attacks from ideas14. None is claimed as a prize result until a
named lemma actually excludes a residual period.

1. Factor complexity p(n) of last-sat L_0 words with R>=12. Kill rigidity
   if some model has p(n)>n on every n <= |u|/2.
2. Complete 2-step map including u=1; language of u for an arbitrary
   (possibly infinite) right. Compare to the SFT {11,00000}.
3. Drive a finite right by the isolated-zero word 01^8; subsequence
   sigma = left neighbor on the isolated 0. Survive if every small
   right makes sigma eventually periodic (Jen would then exclude q=8
   for every finite seed). Kill if some right keeps mixing sigma.

Run: python3 research/cycle_q.py --certify
Dump: research/cycle_q.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_certificate import survivors
from period2_fiber import forced_right_traces
from period2_ugap import two_step
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")

# Last-sat (T,R) from Cycles D and O. T=12 R=6 was empty in germ.py.
WORST = [(8, 9), (16, 9), (20, 16), (22, 12), (15, 6), (33, 14), (34, 12)]


def factor_complexity(word):
    """p(n) = number of length-n factors; first n with p(n)<=n, else None."""
    s = "".join(map(str, word))
    L = len(s)
    p = []
    mh = None
    for n in range(1, L + 1):
        fac = {s[i : i + n] for i in range(L - n + 1)}
        pn = len(fac)
        p.append(pn)
        if mh is None and pn <= n:
            mh = n
    return {"p": p, "mh_n": mh, "p_at_half": p[L // 2 - 1] if L >= 2 else None, "L": L}


def morse_hedlund_lastsat():
    rows = []
    kill = False
    for T, R in WORST:
        mods = survivors(T, R)
        if not mods:
            rows.append({"T": T, "R": R, "n": 0})
            continue
        comps = []
        all_positive = True
        for u in mods:
            c = factor_complexity(u)
            comps.append(
                {
                    "u_head": "".join(map(str, u[:24])),
                    "L": c["L"],
                    "mh_n": c["mh_n"],
                    "p_at_half": c["p_at_half"],
                    "p_max": max(c["p"]) if c["p"] else 0,
                    "zero_run": max_zero_run(u),
                }
            )
            half = c["L"] // 2
            # positive-entropy germ: p(n)>n for all n<=half
            if c["mh_n"] is None or c["mh_n"] > half:
                all_positive = True
            else:
                all_positive = False
        # Kill rigidity if ANY model has p(n)>n for all n<=|u|/2
        model_kill = any(
            (c["mh_n"] is None or c["mh_n"] > c["L"] // 2) for c in comps
        )
        if model_kill and T in (16, 20, 22, 8) and R >= 9:
            kill = True
        rows.append(
            {
                "T": T,
                "R": R,
                "n": len(mods),
                "models": comps,
                "any_p_gt_n_through_half": model_kill,
                "all_obey_mh_by_half": not model_kill,
            }
        )
    return {"rows": rows, "kill_rigidity": kill}


def max_zero_run(seq):
    best = 0
    z = 0
    for b in seq:
        if b == 0:
            z += 1
            best = max(best, z)
        else:
            z = 0
    return best


def full_uef_automaton():
    """(u,e,f,g,h) even-time -> next, both u=0 and u=1. Centre forced 01."""
    rows = []
    for u, e, f, g, h in product([0, 1], repeat=5):
        bits = [0, u, e, f, g, h, 0, 0]
        nxt = two_step(bits)
        rows.append(
            {
                "uef": (u, e, f),
                "gh": (g, h),
                "u_next": nxt[1],
                "uef_next": (nxt[1], nxt[2], nxt[3]),
            }
        )
    # language of u: projection of a 5-bit state plus free (g,h)
    # consecutive 1s already forbidden; check whether every X-word is hit
    # by some infinite (g,h)-stream, via finite reachability of u-prefixes
    # BFS on (u,e,f) with free (g,h)
    start = (0, 0, 0)  # vacuum even, or all 8 states as possible starts
    seen_u_factors = set()
    # states: (u,e,f)
    from collections import deque

    st = deque()
    vis = set()
    for s in product([0, 1], repeat=3):
        st.append((s, ()))
        vis.add((s, ()))
    while st:
        (uef, upath) = st.popleft()
        if len(upath) >= 8:
            seen_u_factors.add(upath)
            continue
        u, e, f = uef
        for g, h in product([0, 1], repeat=2):
            bits = [0, u, e, f, g, h, 0, 0]
            nxt = two_step(bits)
            nuef = (nxt[1], nxt[2], nxt[3])
            npath = upath + (nxt[1],)
            key = (nuef, npath)
            if len(npath) <= 8 and key not in vis:
                vis.add(key)
                st.append((nuef, npath))
    X8 = set()

    def rec_x(pos, last, zrun, acc):
        if pos == 8:
            X8.add(acc)
            return
        if zrun < 4:
            rec_x(pos + 1, 0, zrun + 1, acc + (0,))
        if last == 0:
            rec_x(pos + 1, 1, 0, acc + (1,))

    rec_x(0, 0, 0, ())
    rec_x(0, 1, 0, ())

    missing = X8 - seen_u_factors
    extra = seen_u_factors - X8
    # u=1 always followed by u'=0?
    u1_next = {r["u_next"] for r in rows if r["uef"][0] == 1}
    return {
        "n_table": len(rows),
        "u1_next_values": sorted(u1_next),
        "X8_size": len(X8),
        "realized_8": len(seen_u_factors),
        "missing_from_X": ["".join(map(str, w)) for w in sorted(missing)],
        "extra_not_X": ["".join(map(str, w)) for w in sorted(extra)],
        "proper_subshift": len(missing) > 0,
    }


def infinite_germ_identities():
    """On L_0 with R>=6, F(Su) and F(S^2 u) windows at T. Algebraic checks
    already in period2_germ; here record whether T decreases."""
    T, R = 20, 16
    mods = survivors(T, R)
    chains = []
    for u in mods:
        kmax = max(T + R + 12, 2 * nvars(T + R) + 4)
        F, _ = F_of_u(u, kmax)
        uu = list(u)
        win = []
        for step in range(5):
            # first 1 at or after T, and zeros after last 1 in [T, T+R]
            ones = [i for i in range(T, min(T + R + 1, len(F))) if F[i] == 1]
            win.append(
                {
                    "step": step,
                    "F_from_T": "".join(str(F[i]) if i < len(F) else "?" for i in range(T, T + 10)),
                    "ones_ge_T": ones[:6],
                    "min_one_ge_T": ones[0] if ones else None,
                }
            )
            uu = uu[1:] + [0]
            F, _ = F_of_u(uu, kmax)
        chains.append(win)
    decrease = all(
        ch[1]["min_one_ge_T"] is not None
        and ch[0]["min_one_ge_T"] is not None
        and ch[1]["min_one_ge_T"] < ch[0]["min_one_ge_T"]
        for ch in chains
    )
    return {"n": len(mods), "T_decreases_under_S": decrease, "sample": chains[:2]}


def period_of_suffix(seq, min_pre, max_p):
    n = len(seq)
    for p in range(1, max_p + 1):
        if n < min_pre + 3 * p:
            continue
        start = n - 3 * p
        block = seq[start : start + p]
        if seq[start + p : start + 2 * p] == block and seq[start + 2 * p : start + 3 * p] == block:
            pre = start
            while pre >= p and seq[pre - p : pre] == block:
                pre -= p
            return p, pre
    return None, None


def q8_drive(Wmax=5, T=90):
    """Force centre to 01^8, evolve finite right, sigma = l at times 0 mod 9.
    l_t = c_{t+1} XOR (c_t OR r_t). Word w[t%9], w=[0,1,1,1,1,1,1,1,1].
    """
    w = [0, 1, 1, 1, 1, 1, 1, 1, 1]
    results = []
    n_mix = 0
    n_per = 0
    for W in range(0, Wmax + 1):
        for mask in range(1 << W) if W else [0]:
            if W and mask == 0:
                continue
            right = 0
            for j in range(W):
                if (mask >> j) & 1:
                    right |= 1 << (j + 1)
            # bit0 = centre
            row = (0) | right  # c0=0 = w[0]
            c_trace = []
            r_trace = []
            for t in range(T):
                c_trace.append(row & 1)
                r_trace.append((row >> 1) & 1)
                nxt = (row << 1) ^ (row | (row >> 1))
                nxt_c = w[(t + 1) % 9]
                row = (nxt & ~1) | nxt_c
            # sigma at t=0,9,18,... : l_t = c_{t+1} XOR (c_t OR r_t)
            sigma = []
            for n in range((T - 2) // 9):
                t = 9 * n
                l = c_trace[t + 1] ^ (c_trace[t] | r_trace[t])
                sigma.append(l)
            p, pre = period_of_suffix(sigma, min_pre=4, max_p=12)
            dens = sum(sigma) / max(len(sigma), 1)
            mix = 0 < dens < 1
            rec = {
                "W": W,
                "mask": mask,
                "sigma_len": len(sigma),
                "sigma_head": "".join(map(str, sigma[:16])),
                "sigma_tail": "".join(map(str, sigma[-16:])),
                "period": p,
                "pre": pre,
                "dens": round(dens, 3),
                "mixes": mix and p is None,
            }
            results.append(rec)
            if rec["mixes"]:
                n_mix += 1
            if p is not None:
                n_per += 1
    return {
        "n": len(results),
        "n_mix_no_period": n_mix,
        "n_eventual_period": n_per,
        "kill_all_periodic": n_mix > 0,
        "survive_all_periodic": n_mix == 0 and n_per == len(results),
        "samples": [r for r in results if r["W"] <= 2][:8],
        "a_mixer": next((r for r in results if r["mixes"]), None),
    }


def certify():
    mh = morse_hedlund_lastsat()
    auto = full_uef_automaton()
    germ = infinite_germ_identities()
    q8 = q8_drive(5, 180)
    return {"mh": mh, "automaton": auto, "germ": germ, "q8": q8}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("MH kill_rigidity", report["mh"]["kill_rigidity"])
    for row in report["mh"]["rows"]:
        print(
            f"  T={row['T']} R={row.get('R')} n={row['n']} "
            f"p>n through half={row.get('any_p_gt_n_through_half')}"
        )
        if row.get("models"):
            m = row["models"][0]
            print(f"    e.g. L={m['L']} mh_n={m['mh_n']} p_half={m['p_at_half']} zrun={m['zero_run']}")
    print("automaton", {k: report["automaton"][k] for k in report["automaton"] if k != "missing_from_X"})
    print("missing X8", report["automaton"]["missing_from_X"][:20])
    print("germ T-decrease", report["germ"]["T_decreases_under_S"])
    print(
        "q8 mix",
        report["q8"]["n_mix_no_period"],
        "periodic",
        report["q8"]["n_eventual_period"],
        "kill",
        report["q8"]["kill_all_periodic"],
        "mixer",
        report["q8"]["a_mixer"],
    )
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
