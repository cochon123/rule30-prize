"""Renewal / insulation scan for period-2 left columns.

For a finite Fibonacci word w (no consecutive 1s), E(w) is the last index
at which the zero-padded reconstruction F disagrees with vacuum F_k = k mod 2.
Legal left extensions are prepend-0 and prepend-10. This script measures
how the disagreement front moves under those maps, tests the candidate bound
E(w) <= 2|w| + C, and records explicit families that violate it.

Run: python3 research/period2_renewal.py --certify
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_vacuum import (  # noqa: E402
    F_of_u,
    fold_bit,
    nvars,
    vacuum_F,
    vacuum_G,
    vacuum_pair,
)


def last_disagreement(F) -> int:
    last = -1
    for k, fk in enumerate(F):
        if fk != vacuum_F(k):
            last = k
    return last


def last_disagreement_pair(F, G) -> int:
    last = -1
    for k in range(len(F)):
        if F[k] != vacuum_F(k) or G[k] != vacuum_G(k):
            last = k
    return last


def E_of_u(u, kmax: int) -> int:
    F, _ = F_of_u(u, kmax)
    last = last_disagreement(F)
    if last >= kmax - 2:
        raise AssertionError(f"E hit kmax={kmax} on {u}")
    return last


def defect_mask(F, G, upto: int | None = None) -> list[int]:
    n = len(F) if upto is None else min(upto + 1, len(F))
    out = []
    for k in range(n):
        df = F[k] ^ vacuum_F(k)
        dg = G[k] ^ vacuum_G(k)
        out.append(df + 2 * dg)
    return out


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


def needed_kmax(L: int, extra: int = 24) -> int:
    # FSM: each fold adds at most 11 to the last disagreement.
    return 11 * max(L, 1) + extra


def scan_all_words(Lmax: int) -> dict:
    """All Fibonacci words of length 1..Lmax: E, excess over 2L, ratio."""
    rows = []
    worst_excess = []
    worst_ratio = []
    for L in range(0, Lmax + 1):
        kmax = needed_kmax(L)
        best_ex = -10**9
        best_ex_u = []
        best_r = -1.0
        best_r_u = []
        e_vals = []
        if L == 0:
            F, G = vacuum_pair(kmax)
            e = last_disagreement(F)
            rows.append({"L": 0, "u": [], "E": e, "excess2": e, "ratio": None})
            worst_excess.append({"L": 0, "E": e, "excess2": e, "u": []})
            worst_ratio.append({"L": 0, "E": e, "ratio": None, "u": []})
            continue
        for u in fib_strings(L):
            e = E_of_u(u, kmax)
            ex = e - 2 * L
            r = e / L
            e_vals.append(e)
            rec = {"L": L, "u": u, "E": e, "excess2": ex, "ratio": r}
            rows.append(rec)
            if ex > best_ex or (ex == best_ex and u > best_ex_u):
                best_ex = ex
                best_ex_u = u
            if r > best_r or (r == best_r and u > best_r_u):
                best_r = r
                best_r_u = u
        worst_excess.append(
            {
                "L": L,
                "E": E_of_u(best_ex_u, kmax),
                "excess2": best_ex,
                "u": best_ex_u,
            }
        )
        worst_ratio.append(
            {
                "L": L,
                "E": E_of_u(best_r_u, kmax),
                "ratio": best_r,
                "u": best_r_u,
            }
        )
    return {
        "worst_excess": worst_excess,
        "worst_ratio": worst_ratio,
    }


def single_1_family(mmax: int) -> list[dict]:
    rows = []
    for m in range(0, mmax + 1):
        u = [0] * m + [1]
        kmax = needed_kmax(m + 1, extra=40)
        e = E_of_u(u, kmax)
        rows.append(
            {
                "m": m,
                "L": m + 1,
                "E": e,
                "excess2": e - 2 * (m + 1),
                "E_minus_8m": e - 8 * m,
                "pred_8m_14": (8 * m - 14) if m >= 5 else None,
            }
        )
    return rows


def prepend_deltas(Lmax: int) -> dict:
    """E(0w)-E(w) and E(10w)-E(w) for every Fibonacci w of length <= Lmax."""
    d0 = []
    d10 = []
    samples = []
    for L in range(0, Lmax + 1):
        kmax = needed_kmax(L + 2)
        words = [[]] if L == 0 else fib_strings(L)
        for w in words:
            ew = E_of_u(w, kmax) if w else -1
            u0 = [0] + w
            e0 = E_of_u(u0, kmax)
            d0.append(e0 - ew)
            rec = {
                "w": w,
                "E_w": ew,
                "E_0w": e0,
                "d0": e0 - ew,
            }
            u10 = [1, 0] + w
            e10 = E_of_u(u10, kmax)
            d10.append(e10 - ew)
            rec["E_10w"] = e10
            rec["d10"] = e10 - ew
            samples.append(rec)
    from collections import Counter

    return {
        "d0_counter": dict(sorted(Counter(d0).items())),
        "d10_counter": dict(sorted(Counter(d10).items())),
        "d0_min": min(d0),
        "d0_max": max(d0),
        "d10_min": min(d10),
        "d10_max": max(d10),
        "n_samples": len(samples),
        # keep a few extremal samples
        "d0_max_examples": [
            s for s in samples if s["d0"] == max(d0)
        ][:6],
        "d10_max_examples": [
            s for s in samples if s["d10"] == max(d10)
        ][:6],
        "d0_min_examples": [
            s for s in samples if s["d0"] == min(d0)
        ][:4],
        "d10_min_examples": [
            s for s in samples if s["d10"] == min(d10)
        ][:4],
    }


def fold0_orbit_after_one(mmax: int) -> list[dict]:
    """After folding a single 1 onto vacuum, iterate fold-0 and record E."""
    kmax = needed_kmax(mmax + 1, extra=40)
    F, G = vacuum_pair(kmax)
    F, G = fold_bit(F, G, 1, kmax)
    rows = []
    for m in range(0, mmax + 1):
        eF = last_disagreement(F)
        eFG = last_disagreement_pair(F, G)
        mask = defect_mask(F, G, upto=min(eFG + 4, kmax))
        # trim trailing zeros in the mask
        while mask and mask[-1] == 0:
            mask.pop()
        rows.append({"m": m, "E_F": eF, "E_FG": eFG, "mask": mask})
        F, G = fold_bit(F, G, 0, kmax)
    return rows


def repeating_10(nmax: int) -> list[dict]:
    rows = []
    for n in range(1, nmax + 1):
        u = ([1, 0] * n)
        kmax = needed_kmax(len(u), extra=40)
        e = E_of_u(u, kmax)
        rows.append(
            {
                "n": n,
                "L": len(u),
                "E": e,
                "excess2": e - 2 * len(u),
                "ratio": e / len(u),
            }
        )
    return rows


def repeating_100(nmax: int) -> list[dict]:
    rows = []
    for n in range(1, nmax + 1):
        u = ([1, 0, 0] * n)
        kmax = needed_kmax(len(u), extra=40)
        e = E_of_u(u, kmax)
        rows.append(
            {
                "n": n,
                "L": len(u),
                "E": e,
                "excess2": e - 2 * len(u),
                "ratio": e / len(u),
            }
        )
    return rows


def rightmost_1_family(mmax: int, prefix_kind: str) -> list[dict]:
    """Words of the form p + 0^m + [1], various short prefixes p."""
    prefixes = {
        "empty": [],
        "1": [1],
        "10": [1, 0],
        "01": [0, 1],
        "101": [1, 0, 1],
        "010": [0, 1, 0],
        "1010": [1, 0, 1, 0],
        "0101": [0, 1, 0, 1],
    }
    p = prefixes[prefix_kind]
    rows = []
    for m in range(0, mmax + 1):
        u = p + [0] * m + [1]
        # skip illegal consecutive 1s (only if p ends with 1 and m=0)
        if p and p[-1] == 1 and m == 0:
            continue
        kmax = needed_kmax(len(u), extra=40)
        e = E_of_u(u, kmax)
        rows.append(
            {
                "m": m,
                "L": len(u),
                "E": e,
                "excess2": e - 2 * len(u),
                "ratio": e / len(u),
            }
        )
    return rows


def gap_window_lemma_check(amax: int = 8, extra: int = 6) -> list[dict]:
    """If u_i=0 for a<=i<b, truncated (zeros from a) and true F agree
    through k=2b, and truncated is vacuum past E(prefix)."""
    rows = []
    for a in range(1, amax + 1):
        for pref in fib_strings(a):
            if 1 not in pref:
                continue
            e_pref = E_of_u(pref, needed_kmax(a))
            # pick several gaps
            for gap in (1, 2, 4, 8, extra):
                b = a + gap
                # true word: prefix + gap zeros + a trailing 1 (so not eventually zero)
                u = pref + [0] * gap + [1]
                kmax = max(2 * b + 4, e_pref + 8, needed_kmax(len(u)))
                F_true, _ = F_of_u(u, kmax)
                F_tr, _ = F_of_u(pref, kmax)
                agree_upto = -1
                for k in range(kmax + 1):
                    if F_true[k] == F_tr[k]:
                        agree_upto = k
                    else:
                        break
                # variable bound: agree through k with nvars(k) <= a? 
                # F_k depends on u_0..u_{floor((k-1)/2)}, so through k=2b
                # wait: they differ only when a bit at index >= a is read,
                # i.e. floor((k-1)/2) >= a, k-1 >= 2a, k >= 2a+1.
                # The note said k=2b because the NEXT 1 is at b, so they
                # agree as long as floor((k-1)/2) < b, i.e. k <= 2b.
                k_var = 2 * b
                agree_at_2b = all(
                    F_true[k] == F_tr[k] for k in range(min(k_var, kmax) + 1)
                )
                vacuum_lo = e_pref + 1
                vacuum_hi = 2 * b
                nonempty = vacuum_lo <= vacuum_hi
                exposed = []
                if nonempty:
                    for k in range(vacuum_lo, min(vacuum_hi, kmax) + 1):
                        if F_true[k] != vacuum_F(k):
                            exposed.append(k)
                            break
                    else:
                        exposed = None  # none: window is truly vacuum
                rows.append(
                    {
                        "a": a,
                        "b": b,
                        "e_pref": e_pref,
                        "agree_upto": agree_upto,
                        "agree_through_2b": agree_at_2b,
                        "window": [vacuum_lo, vacuum_hi],
                        "nonempty": nonempty,
                        "first_break_in_window": exposed,
                    }
                )
    return rows


def worst_ratio_search(Lmax: int) -> list[dict]:
    out = []
    for L in range(1, Lmax + 1):
        kmax = needed_kmax(L)
        best = -1.0
        best_u = None
        best_e = None
        for u in fib_strings(L):
            e = E_of_u(u, kmax)
            r = e / L
            if r > best:
                best = r
                best_u = u
                best_e = e
        out.append(
            {
                "L": L,
                "E": best_e,
                "ratio": best,
                "excess2": best_e - 2 * L,
                "u": best_u,
            }
        )
    return out


def certify_single_1_formula(mmax: int = 40) -> dict:
    """For m>=5, E(0^m 1) = 8m-14. Also record E_FG growth."""
    rows = single_1_family(mmax)
    for row in rows:
        if row["m"] >= 5:
            assert row["E"] == 8 * row["m"] - 14, row
            assert row["excess2"] == 6 * row["m"] - 16, row
    # prepend-0 on this family: 0^{m+1}1 from 0^m 1 is d0 = 8 for m>=5
    for m in range(5, min(mmax, 20)):
        assert rows[m + 1]["E"] - rows[m]["E"] == 8, (m, rows[m], rows[m + 1])
    return {"mmax": mmax, "ok": True, "tail": rows[-5:]}


def certify_variable_bound_gap(a: int = 6, gap: int = 10) -> dict:
    pref_list = [u for u in fib_strings(a) if 1 in u]
    b = a + gap
    k_agree = 2 * b
    kmax = max(k_agree + 4, needed_kmax(b + 1))
    n_ok = 0
    for pref in pref_list:
        u = pref + [0] * gap + [1]
        F_true, _ = F_of_u(u, kmax)
        F_tr, _ = F_of_u(pref, kmax)
        for k in range(k_agree + 1):
            assert F_true[k] == F_tr[k], (pref, k)
        n_ok += 1
    return {"a": a, "gap": gap, "n": n_ok, "ok": True}


def max_E_vs_length(Lmax: int) -> dict:
    """Is max E(w) over |w|=L always achieved by 0^{L-1}1?"""
    rows = []
    for L in range(1, Lmax + 1):
        kmax = needed_kmax(L)
        e_single = E_of_u([0] * (L - 1) + [1], kmax)
        e_max = -1
        n_at_max = 0
        other = None
        for u in fib_strings(L):
            e = E_of_u(u, kmax)
            if e > e_max:
                e_max = e
                n_at_max = 1
                other = u
            elif e == e_max:
                n_at_max += 1
        rows.append(
            {
                "L": L,
                "E_max": e_max,
                "E_single": e_single,
                "single_is_max": e_max == e_single,
                "n_at_max": n_at_max,
                "example": other,
            }
        )
    return rows


def potential_candidates(Lmax: int) -> dict:
    """Test E <= 8|w|+C, E <= 8*#zeros_after_first_1_from_right, etc."""
    slack_8L = []
    slack_8m = []  # m = index of rightmost 1 = last 1 position
    slack_11L = []
    for L in range(1, Lmax + 1):
        kmax = needed_kmax(L)
        for u in fib_strings(L):
            e = E_of_u(u, kmax)
            slack_8L.append(8 * L - e)
            slack_11L.append(11 * L - e)
            # rightmost 1 index
            r = max(i for i, b in enumerate(u) if b == 1) if 1 in u else -1
            # zeros folded after the first 1: the 1 is folded first (rightmost),
            # then L-1-r zeros? Wait: bits to the LEFT of rightmost 1 are
            # folded after it. There are r of them (indices 0..r-1), plus
            # the rightmost 1 is at r, length L, bits r+1..L-1 are zeros
            # folded BEFORE the 1 (onto vacuum, no-op). So E should depend
            # on r (folds after the 1), not on trailing zeros.
            slack_8m.append(8 * (r + 1) - e if r >= 0 else 0)
    return {
        "min_slack_8L": min(slack_8L),
        "min_slack_8_rightmost": min(slack_8m),
        "min_slack_11L": min(slack_11L),
        "all_8L_nonneg_plus": min(slack_8L),
        "all_8_rightmost_nonneg": min(slack_8m),
    }


def scattering_two_defects(gmax: int = 20) -> list[dict]:
    """Two isolated 1s: 1 0^g 1. Track E vs g."""
    rows = []
    for g in range(1, gmax + 1):
        u = [1] + [0] * g + [1]
        kmax = needed_kmax(len(u), extra=40)
        e = E_of_u(u, kmax)
        e1 = E_of_u([0] * g + [1], kmax)
        rows.append(
            {
                "g": g,
                "L": len(u),
                "E": e,
                "E_right_1_only": e1,
                "collision_shift": e - e1,
                "excess2": e - 2 * len(u),
            }
        )
    return rows


def certify_maximizers(Lmax: int = 12) -> list[dict]:
    """For L>=4, max E is 8L-14, achieved exactly on words ending in 0101."""
    rows = []
    for L in range(4, Lmax + 1):
        kmax = needed_kmax(L)
        emax = 8 * L - 14
        n_max = 0
        n_end = 0
        for u in fib_strings(L):
            e = E_of_u(u, kmax)
            ends = u[-4:] == [0, 1, 0, 1]
            if e == emax:
                n_max += 1
                assert ends, (u, e, emax)
            if ends:
                n_end += 1
                assert e == emax, (u, e, emax)
        assert n_max == n_end and n_max > 0, (L, n_max, n_end)
        rows.append({"L": L, "E_max": emax, "n": n_max})
    return rows


def certify_cruise_E18(Lmax: int = 11) -> dict:
    """Every Fibonacci word with E>=18 has prepend-0 increment exactly 8."""
    n = 0
    for L in range(1, Lmax + 1):
        kmax = needed_kmax(L + 1)
        for w in fib_strings(L):
            ew = E_of_u(w, kmax)
            d0 = E_of_u([0] + w, kmax) - ew
            if ew >= 18:
                assert d0 == 8, (w, ew, d0)
                n += 1
            else:
                assert d0 in (0, 3, 5, 8), (w, ew, d0)
    return {"Lmax": Lmax, "n_with_E_ge_18": n}


def certify_repeating_10(nmax: int = 12) -> list[dict]:
    rows = repeating_10(nmax)
    for row in rows:
        if row["n"] >= 3:
            assert row["E"] == 16 * row["n"] - 22, row
    return rows


def certify() -> dict:
    s1 = certify_single_1_formula(36)
    vb = certify_variable_bound_gap(5, 12)
    wex = scan_all_words(12)
    deltas = prepend_deltas(8)
    orbit = fold0_orbit_after_one(16)
    r10 = certify_repeating_10(12)
    r100 = repeating_100(10)
    mx = max_E_vs_length(12)
    pot = potential_candidates(10)
    sc = scattering_two_defects(24)
    maximizers = certify_maximizers(12)
    cruise = certify_cruise_E18(11)
    # two isolated 1s, g>=4: left 1 adds exactly 8 to the right-1 front
    for row in sc:
        if row["g"] >= 4:
            assert row["collision_shift"] == 8, row
    # explicit kill of E <= 2L+C: excess of single-1 family
    excesses = [row["excess2"] for row in wex["worst_excess"] if row["L"] > 0]
    assert max(excesses) >= 6 * 11 - 16  # L=12 => m=11, but worst may be that
    # single-1 at L=12, m=11: excess = 6*11-16 = 50
    assert E_of_u([0] * 11 + [1], needed_kmax(12)) - 24 == 6 * 11 - 16
    # prepend increments never exceed the speed-8 budget on the scanned range
    assert deltas["d0_max"] == 8 and deltas["d10_max"] == 16
    assert deltas["d0_min"] == 0 and deltas["d10_min"] == 3

    report = {
        "single_1_formula": s1,
        "variable_bound_gap": vb,
        "worst_excess_by_L": wex["worst_excess"],
        "worst_ratio_by_L": wex["worst_ratio"],
        "prepend_deltas": {
            k: v
            for k, v in deltas.items()
            if k
            in {
                "d0_counter",
                "d10_counter",
                "d0_min",
                "d0_max",
                "d10_min",
                "d10_max",
                "n_samples",
                "d0_max_examples",
                "d10_max_examples",
                "d0_min_examples",
                "d10_min_examples",
            }
        },
        "fold0_orbit_E": [{"m": r["m"], "E_F": r["E_F"], "E_FG": r["E_FG"]} for r in orbit],
        "repeating_10": r10,
        "repeating_100": r100,
        "max_E_vs_length": mx,
        "potential_slacks": pot,
        "two_defect_scattering": sc,
        "maximizers_end_0101": maximizers,
        "cruise_E_ge_18": cruise,
        "insulation_2L_C": "FALSE",
        "kill_family": "0^{m}1 with E=8m-14 for m>=5, excess2=6m-16 unbounded",
        "period2_excluded": False,
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--json-out", type=str, default="")
    parser.add_argument("--mmax", type=int, default=36)
    args = parser.parse_args()
    if args.certify:
        report = certify()
        print("certify: all assertions passed")
        print("single-1 formula E(0^m 1)=8m-14 for m>=5, mmax", report["single_1_formula"]["mmax"])
        print("2|w|+C insulation: FALSE")
        print("kill family: 0^m 1, excess2 = 6m-16 -> +infty")
        print("prepend-0 delta range", report["prepend_deltas"]["d0_min"], report["prepend_deltas"]["d0_max"])
        print("prepend-10 delta range", report["prepend_deltas"]["d10_min"], report["prepend_deltas"]["d10_max"])
        print("potential slacks", report["potential_slacks"])
        print("cruise E>=18 => d0=8 on", report["cruise_E_ge_18"]["n_with_E_ge_18"], "words")
        print("maximizers: E_max=8L-14 on words ending 0101, L=4..12")
        print("max E vs single-1:")
        for row in report["max_E_vs_length"]:
            print(
                f"  L={row['L']:2d} Emax={row['E_max']:3d} "
                f"Esingle={row['E_single']:3d} n={row['n_at_max']} "
                f"single_is_max={row['single_is_max']}"
            )
        print("worst excess by L:")
        for row in report["worst_excess_by_L"]:
            if row["L"] == 0:
                continue
            print(
                f"  L={row['L']:2d} E={row['E']:3d} excess2={row['excess2']:3d} u={row['u']}"
            )
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        return
    # ad-hoc family dump
    print("single-1 family")
    for row in single_1_family(args.mmax):
        if row["m"] >= 5:
            assert row["E"] == 8 * row["m"] - 14
        print(row)


if __name__ == "__main__":
    main()
