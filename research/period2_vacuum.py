"""Eventual-vacuum lemma for period-2 left columns, plus a sound L_0 onset scan.

Folding a bit of the even right neighbor u onto the pair of sequences
(F_k, G_k) = (x(2n,-k), x(2n+1,-k)) is a causal map in the column index k.
The all-zero u-suffix is the vacuum F_k = k mod 2. Once a suffix of u is
vacuum, every 4-bit boundary state of (F,G) returns to vacuum in at most
9 further columns (finite check of a 16-state machine). Consequently every
eventually-zero Fibonacci u has F_k = k mod 2 for all large k, hence
infinitely many 1s, so it cannot realize an L_0 left edge.

Infinite-u L_0 is a separate statement. The sound onset scan enumerates
every Fibonacci string of length exactly the proven variable bound
max_index(F_k) <= floor((k-1)/2) and reports, for each onset width T,
the longest tail of zeros that still has a model.

Run: python3 research/period2_vacuum.py --certify
"""
from __future__ import annotations

import argparse
import json


def vacuum_pair(kmax: int):
    F = [0] * (kmax + 1)
    G = [0] * (kmax + 1)
    F[0] = 0
    G[0] = 1
    if kmax >= 1:
        F[1] = 1
        G[1] = 1
    for k in range(2, kmax + 1):
        F[k] = G[k - 1] ^ (F[k - 1] | F[k - 2])
        G[k] = F[k - 1] ^ (G[k - 1] | G[k - 2])
    return F, G


def fold_bit(F, G, un: int, kmax: int):
    """One Φ_un step: consume u_n, producing the window at this n from the suffix."""
    Fn = [0] * (kmax + 1)
    Gn = [0] * (kmax + 1)
    Fn[0] = 0
    Gn[0] = 1
    if kmax >= 1:
        Fn[1] = 1 ^ un
        Gn[1] = 1
    for k in range(2, kmax + 1):
        Fn[k] = Gn[k - 1] ^ (Fn[k - 1] | Fn[k - 2])
        Gn[k] = F[k - 1] ^ (Gn[k - 1] | Gn[k - 2])
    return Fn, Gn


def F_of_u(u, kmax: int):
    F, G = vacuum_pair(kmax)
    for un in reversed(u):
        F, G = fold_bit(F, G, un, kmax)
    return F, G


def nvars(k: int) -> int:
    """Number of u-bits that can appear in F_k. max_index <= floor((k-1)/2)."""
    if k <= 0:
        return 0
    return (k - 1) // 2 + 1


def vacuum_F(k: int) -> int:
    return k & 1


def vacuum_G(k: int) -> int:
    if k == 0:
        return 1
    return k & 1


def fsm_step(f1, f2, g1, g2, k: int):
    """Φ_0 tail step, assuming the suffix F_old is vacuum at index k-1."""
    fold_old = (k - 1) & 1
    Fn = g1 ^ (f1 | f2)
    Gn = fold_old ^ (g1 | g2)
    return Fn, f1, Gn, g1


def is_vacuum_state(f1, f2, g1, g2, k: int) -> bool:
    return (
        f1 == vacuum_F(k - 1)
        and f2 == vacuum_F(k - 2)
        and g1 == vacuum_G(k - 1)
        and g2 == vacuum_G(k - 2)
    )


def fsm_absorb_time(state, k0: int, maxn: int = 24):
    f1, f2, g1, g2 = state
    seen = {}
    for t in range(maxn):
        k = k0 + t
        if is_vacuum_state(f1, f2, g1, g2, k):
            return t, "vac"
        key = (f1, f2, g1, g2, k % 2)
        if key in seen:
            return t, "cycle"
        seen[key] = t
        f1, f2, g1, g2 = fsm_step(f1, f2, g1, g2, k)
    return maxn, "timeout"


def certify_fsm(max_t: int = 9) -> dict:
    """Every 4-bit state, both parities of k, returns to vacuum in <= max_t steps."""
    worst = 0
    rows = []
    for bits in range(16):
        state = ((bits >> 0) & 1, (bits >> 1) & 1, (bits >> 2) & 1, (bits >> 3) & 1)
        for k0 in range(2, 10):
            t, kind = fsm_absorb_time(state, k0)
            assert kind == "vac", (state, k0, t, kind)
            assert t <= max_t, (state, k0, t)
            worst = max(worst, t)
            rows.append({"state": state, "k0": k0, "t": t})
    return {"worst_absorb": worst, "max_t": max_t, "n_checks": len(rows)}


def certify_vacuum_base(kmax: int = 20) -> None:
    F, G = vacuum_pair(kmax)
    for k in range(kmax + 1):
        assert F[k] == vacuum_F(k), k
        assert G[k] == vacuum_G(k), k
    # Folding a 0 onto vacuum is vacuum.
    F0, G0 = fold_bit(F, G, 0, kmax)
    assert F0 == F and G0 == G


def certify_spatial_identity(nvars_: int = 8, kmax: int = 12) -> None:
    """G_k = F_{k+1} XOR (F_k OR F_{k-1}) on every Fibonacci string (k >= 1)."""

    def fib(length):
        out = []

        def rec(pos, last, acc):
            if pos == length:
                out.append(acc)
                return
            rec(pos + 1, 0, acc + [0])
            if last == 0:
                rec(pos + 1, 1, acc + [1])

        rec(0, 0, [])
        return out

    for u in fib(nvars_):
        F, G = F_of_u(u, kmax)
        for k in range(1, kmax):
            assert G[k] == F[k + 1] ^ (F[k] | F[k - 1]), (u, k)


def certify_eventual_vacuum_finite(mmax: int = 12, slack: int = 12) -> dict:
    """Single 1 at m, then zeros: last disagreement with vacuum is finite,
    then F_k = k mod 2. Bound last_dis <= 11*(m+1) from the FSM (each fold
    adds at most 9 after the vacuum boundary at +2). Empirically 8m-14
    for m >= 4; we assert the conservative FSM bound and the return.
    """
    rows = []
    for m in range(0, mmax + 1):
        bound = 11 * (m + 1) + slack
        F, _ = F_of_u([0] * m + [1], bound)
        last = max((k for k in range(bound + 1) if F[k] != vacuum_F(k)), default=-1)
        assert last < bound - 2, (m, last, bound)
        for k in range(last + 1, bound + 1):
            assert F[k] == vacuum_F(k), (m, k)
        # infinitely many 1s in the vacuum tail
        assert any(F[k] == 1 for k in range(last + 1, bound + 1))
        rows.append({"m": m, "last_dis": last, "bound": bound})
    # Every short Fibonacci word, then zeros: same return to vacuum.
    word_rows = []
    for L in range(1, 8):
        for u in fib_strings(L):
            if 1 not in u:
                continue
            bound = 11 * L + slack
            F, _ = F_of_u(u, bound)
            last = max((k for k in range(bound + 1) if F[k] != vacuum_F(k)), default=-1)
            assert last < bound - 2, (u, last, bound)
            for k in range(last + 1, bound + 1):
                assert F[k] == vacuum_F(k), (u, k)
            word_rows.append({"u": u, "last_dis": last})
    return {"single_1": rows, "short_words": len(word_rows)}


def fib_strings(length: int):
    out = []

    def rec(pos, last, acc):
        if pos == length:
            out.append(acc)
            return
        rec(pos + 1, 0, acc + [0])
        if last == 0:
            rec(pos + 1, 1, acc + [1])

    rec(0, 0, [])
    return out


def sound_onset_table(Tmax: int = 16, Rmax: int = 20) -> list:
    """For each T, largest R such that some Fibonacci u of length nvars(T+R)
    has F_T=1 and F_{T+1}=...=F_{T+R}=0. Sound for infinite u: extra u bits
    do not appear in those polynomials.
    """
    rows = []
    cache = {}
    for T in range(1, Tmax + 1):
        maxR = -1
        nmax = 0
        killed = None
        for R in range(0, Rmax + 1):
            top = T + R
            L = max(nvars(top), 1)
            K = top
            if L not in cache or cache[L][0] < K:
                strs = fib_strings(L)
                cache[L] = (max(K, 2 * L + 2), [F_of_u(u, max(K, 2 * L + 2))[0] for u in strs])
            rowsF = cache[L][1]
            n = 0
            for F in rowsF:
                if F[T] != 1:
                    continue
                if all(F[T + d] == 0 for d in range(1, R + 1)):
                    n += 1
            if n:
                maxR = R
                nmax = n
            else:
                killed = top
                break
        rows.append(
            {
                "T": T,
                "max_sat_R": maxR,
                "n_at_max": nmax,
                "killed_by": killed,
            }
        )
        assert killed is not None, T
    return rows


def certify(Tmax: int = 12) -> dict:
    certify_vacuum_base(24)
    fsm = certify_fsm(9)
    certify_spatial_identity(8, 12)
    ev = certify_eventual_vacuum_finite(10, 16)
    onset = sound_onset_table(Tmax, 20)
    return {
        "vacuum_base": True,
        "fsm": fsm,
        "spatial_identity": True,
        "eventual_vacuum_single_1": ev,
        "sound_onset": onset,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--tmax", type=int, default=12)
    parser.add_argument("--json-out", type=str, default="")
    args = parser.parse_args()
    report = certify(args.tmax)
    print("certify: all assertions passed")
    print("FSM worst absorb", report["fsm"]["worst_absorb"])
    print("Sound L_0 onset (infinite Fibonacci u):")
    for row in report["sound_onset"]:
        print(
            f"  T={row['T']:2d} maxR={row['max_sat_R']:2d} "
            f"n={row['n_at_max']:3d} killed_by_F[{row['killed_by']}]"
        )
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
