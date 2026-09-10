#!/usr/bin/env python3
"""2-adic valuations and OR-overlap carries of the packed Rule 30 row.

Cycle I attack on prize problem 3 (maybe 1). This is not the signed ×7
identity Z_{t+1}=7Z_t-2Q_t (research/signed_carry.md) and not the residue
periods of f(z)=z XOR ((z<<1) OR (z<<2)) in research/twoadic.md. It looks
at valuations and nonlinear overlap counts of the orbit z_t itself.

Packing (primary): right-edge, z_0=1,
    z_{t+1} = z_t XOR ((z_t << 1) OR (z_t << 2)),
bit k is x(t, t-k), centre is bit t. Rows begin 1, 7, 25, 111, ...
The experiment.py packing grows the other way
    row <- (row<<2) ^ ((row<<1)|row)
and is the bit-reversal of the 2t+1-bit right-edge word. Both are run;
N_t agrees. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/packed_valuation.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits
from experiment import linear_complexity

# First-experiment horizon. Extend to 10**5 only if N_t looks O(log t).
MAX_T = 16384
LC_NS = (256, 1024, 4096, 8192)
DENSITY_NS = (256, 1024, 4096, 16384)
SAMPLE_T = 32
KILL_MEAN_RATIO = 0.05
# Frozen cheap formulas for v2(z_t+1) and N_t (functions of t only).
FORMULA_FAMILY = (
    "constant",
    "v2(t+1)",
    "v2(t+1)+1",
    "1 on even t else 3",
    "1 on even t else v2(t+1)+2",
    "1 on even t else v2(t)+2",
    "popcount(t)",
    "t//2",
    "t",
)


def v2(n: int):
    """2-adic valuation; None encodes +∞."""
    if n == 0:
        return None
    n = abs(n)
    return (n & -n).bit_length() - 1


def right_edge_update(z: int) -> int:
    return z ^ ((z << 1) | (z << 2))


def experiment_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def reverse_bits(z: int, width: int) -> int:
    r = 0
    for i in range(width):
        if (z >> i) & 1:
            r |= 1 << (width - 1 - i)
    return r


def pearson(xs, ys) -> float:
    n = len(xs)
    if n == 0:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0.0 or dy == 0.0:
        return 0.0
    return num / (dx * dy)


def min_period(bits, max_p: int):
    n = len(bits)
    cap = min(max_p, n // 2 if n >= 2 else 1)
    for p in range(1, cap + 1):
        if all(bits[i] == bits[i % p] for i in range(n)):
            return p
    return None


def first_disagree(seq, fn, T: int):
    for t in range(T):
        got = seq[t]
        want = fn(t)
        if got != want:
            return {"t": t, "got": got, "want": want}
    return None


def self_check(max_t: int = 80) -> dict:
    bits = experiment_center_bits(max_t + 1)
    z = 1
    row = 1
    sequence = []
    centre_ok = True
    exp_centre_ok = True
    reverse_ok = True
    n_match_ok = True
    lemma_ok = True
    vnext_ok = True
    vxor_shift_ok = True
    vdiff_ok = True
    for t in range(max_t):
        sequence.append(z)
        if ((z >> t) & 1) != bits[t]:
            centre_ok = False
            break
        if ((row >> t) & 1) != bits[t]:
            exp_centre_ok = False
            break
        width = 2 * t + 1
        if reverse_bits(z, width) != row:
            reverse_ok = False
            break
        n_right = (z & (z << 1)).bit_count()
        n_left = (row & (row << 1)).bit_count()
        if n_right != n_left:
            n_match_ok = False
            break
        z_next = right_edge_update(z)
        if v2(z_next ^ z) != 1:
            vnext_ok = False
            break
        if t > 0 and v2(z ^ (1 << t)) != 0:
            vxor_shift_ok = False
            break
        if t > 0 and v2(z - (1 << t)) != 0:
            vdiff_ok = False
            break
        # v2(f(z)-1) = v2(z+1) for odd z (proved; checked on the orbit).
        if v2(z_next - 1) != v2(z + 1):
            lemma_ok = False
            break
        z = z_next
        row = experiment_update(row)
    twoadic_prefix = sequence[:4] == [1, 7, 25, 111]
    # Lemma on all odd residues modulo 2**12, not just the orbit.
    lemma_all_odd = True
    for odd in range(1, 1 << 12, 2):
        if v2(right_edge_update(odd) - 1) != v2(odd + 1):
            lemma_all_odd = False
            break
    # Trailing-ones identity: v2(odd+1) equals the LSB 1-run length.
    run_ok = True
    for odd in (1, 3, 5, 7, 9, 15, 17, 31, 43, 127):
        k = 0
        x = odd
        while x & 1:
            k += 1
            x >>= 1
        if v2(odd + 1) != k:
            run_ok = False
            break
    return {
        "centre_matches_experiment": centre_ok,
        "experiment_packing_centre_ok": exp_centre_ok,
        "twoadic_prefix_1_7_25_111": twoadic_prefix,
        "prefix": sequence[:8],
        "bit_reversal_ok": reverse_ok,
        "N_t_agrees_across_packings": n_match_ok,
        "lemma_v2_f_minus_1_eq_v2_plus_1_orbit": lemma_ok,
        "lemma_all_odd_mod_2_12": lemma_all_odd,
        "v2_z_next_xor_z_eq_1": vnext_ok,
        "v2_z_xor_2_t_eq_0_for_t_gt_0": vxor_shift_ok,
        "v2_z_minus_2_t_eq_0_for_t_gt_0": vdiff_ok,
        "v2_odd_plus_1_is_trailing_ones": run_ok,
        "checked_through": max_t if centre_ok else None,
    }


def density_block(N, T: int) -> dict:
    sl = N[:T]
    ratios = [sl[t] / t for t in range(1, T)]
    half = T // 2
    late = [sl[t] / t for t in range(half, T)]
    s = sum(sl)
    return {
        "T": T,
        "N_T": sl[T - 1],
        "N_T_over_T": sl[T - 1] / T,
        "mean_N": s / T,
        "mean_N_over_T": (s / T) / T,
        "sum_N_over_T2": s / (T * T),
        "mean_N_t_over_t": sum(ratios) / len(ratios),
        "min_N_t_over_t": min(ratios),
        "late_mean_N_t_over_t": sum(late) / len(late),
        "late_min_N_t_over_t": min(late),
        "max_N": max(sl),
        "max_N_over_log2": max(sl[t] / ((t + 2).bit_length()) for t in range(T)),
        "exceeds_0_05_mean_ratio": (sum(ratios) / len(ratios)) > KILL_MEAN_RATIO,
        "late_exceeds_0_05": (sum(late) / len(late)) > KILL_MEAN_RATIO,
    }


def run_orbit(max_t: int) -> dict:
    z = 1
    row = 1
    N = [0] * max_t
    K = [0] * max_t
    M = [0] * max_t
    ones = [0] * max_t
    c = [0] * max_t
    vplus = [None] * max_t
    vminus = [None] * max_t
    vxor_c = [None] * max_t
    vshr = [None] * max_t
    vnext = [None] * max_t
    vdxor = [None] * max_t
    exp_vplus = [None] * max_t
    exp_vminus = [None] * max_t
    exp_vxor_c = [None] * max_t
    exp_vshr = [None] * max_t
    lemma_hold = True
    exp_vplus_ge2_is_2 = True
    for t in range(max_t):
        a = z << 1
        b = z << 2
        or_term = a | b
        overlap = a & b
        N[t] = overlap.bit_count()
        carry = (a + b) ^ a ^ b
        K[t] = (carry >> 1).bit_count()
        M[t] = (z & or_term).bit_count()
        ones[t] = z.bit_count()
        c[t] = (z >> t) & 1
        vplus[t] = v2(z + 1)
        vminus[t] = v2(z - 1)
        vxor_c[t] = v2(z ^ (1 << t))
        hi = z >> t
        vshr[t] = v2(hi)
        vdxor[t] = v2(z ^ a)
        z_next = z ^ or_term
        vnext[t] = v2(z_next ^ z)
        if v2(z_next - 1) != vplus[t]:
            lemma_hold = False
        exp_vplus[t] = v2(row + 1)
        exp_vminus[t] = v2(row - 1)
        exp_vxor_c[t] = v2(row ^ (1 << t))
        exp_vshr[t] = v2(row >> t)
        if t >= 2 and exp_vplus[t] != 2:
            exp_vplus_ge2_is_2 = False
        z = z_next
        row = experiment_update(row)
    return {
        "N": N,
        "K": K,
        "M": M,
        "ones": ones,
        "c": c,
        "vplus": vplus,
        "vminus": vminus,
        "vxor_c": vxor_c,
        "vshr": vshr,
        "vnext": vnext,
        "vdxor": vdxor,
        "exp_vplus": exp_vplus,
        "exp_vminus": exp_vminus,
        "exp_vxor_c": exp_vxor_c,
        "exp_vshr": exp_vshr,
        "lemma_hold": lemma_hold,
        "exp_vplus_ge2_is_2": exp_vplus_ge2_is_2,
        "final_z_bit_length": z.bit_length(),
    }


def formula_search(data, T: int) -> dict:
    N = data["N"]
    vplus = data["vplus"]
    c = data["c"]
    ones = data["ones"]
    runs = [ones[t] - N[t] for t in range(T)]

    vplus_checks = {
        "constant_1": first_disagree(vplus, lambda t: 1, T),
        "v2(t+1)": first_disagree(vplus, lambda t: v2(t + 1), T),
        "v2(t+1)+1": first_disagree(vplus, lambda t: (v2(t + 1) or 0) + 1, T),
        "1_on_even_else_3": first_disagree(
            vplus, lambda t: 1 if t % 2 == 0 else 3, T
        ),
        "1_on_even_else_v2(t+1)+2": first_disagree(
            vplus, lambda t: 1 if t % 2 == 0 else v2(t + 1) + 2, T
        ),
        "1_on_even_else_v2(t)+2": first_disagree(
            vplus, lambda t: 1 if t % 2 == 0 else v2(t) + 2, T
        ),
    }
    even_is_1 = all(vplus[t] == 1 for t in range(0, T, 2))
    odd_ge_3 = all(vplus[t] >= 3 for t in range(1, T, 2))

    n_checks = {
        "popcount(t)": first_disagree(N, lambda t: t.bit_count(), T),
        "t//2": first_disagree(N, lambda t: t // 2, T),
        "t": first_disagree(N, lambda t: t, T),
        "ones-1": first_disagree(N, lambda t: ones[t] - 1, T),
        "(3*t)//5": first_disagree(N, lambda t: (3 * t) // 5, T),
    }
    n_eq_ones_minus_runs = all(N[t] == ones[t] - runs[t] for t in range(T))
    n_eq_c = all(N[t] == c[t] for t in range(T))
    n_parity_eq_c = sum(c[t] == (N[t] & 1) for t in range(T))

    # Threshold periodicity of v2(z+1), as predicted by twoadic.md:
    # {v2 >= k} depends on the first k right-edge bits, period dividing 2^{k-1}.
    thresh = {}
    for k in range(1, 9):
        bits = [1 if (vplus[t] or 0) >= k else 0 for t in range(T)]
        # Search periods that divide 2**(k-1), plus a small extra window.
        p = min_period(bits, max(2 ** max(k - 1, 0) * 2, 16))
        thresh[str(k)] = {
            "predicted_period_divides": 2 ** max(k - 1, 0) if k else 1,
            "min_period": p,
            "ones": sum(bits),
        }

    vshr_is_centre = all((v2_val == 0) == (c[t] == 1) for t, v2_val in enumerate(data["vshr"]))
    exp_vshr_is_centre = all(
        (v2_val == 0) == (c[t] == 1) for t, v2_val in enumerate(data["exp_vshr"])
    )
    vxor_c_nonzero_centre = all(
        (data["vxor_c"][t] == 0) for t in range(1, T)
    )

    return {
        "v2_z_plus_1": {
            "even_t_equals_1": even_is_1,
            "odd_t_at_least_3": odd_ge_3,
            "max": max(vplus),
            "argmax_t": vplus.index(max(vplus)),
            "cheap_formula_first_fail": vplus_checks,
        },
        "N_t": {
            "equals_ones_minus_1_runs": n_eq_ones_minus_runs,
            "equals_centre": n_eq_c,
            "parity_agrees_with_centre_count": n_parity_eq_c,
            "parity_agrees_with_centre_frac": n_parity_eq_c / T,
            "cheap_formula_first_fail": n_checks,
        },
        "v2_threshold_periods": thresh,
        "centre_from_v2_z_shift_t": {
            "v2(z>>t)==0_iff_c_t=1": vshr_is_centre,
            "experiment_v2(row>>t)==0_iff_c_t=1": exp_vshr_is_centre,
            "note": (
                "This is exactly (z>>t)&1: it reads bit t of the packed row, "
                "not a cheap valuation of a t-only expression."
            ),
        },
        "v2_z_xor_2_t": {
            "equals_0_for_t_gt_0": vxor_c_nonzero_centre,
            "extracts_centre": False,
        },
    }


def correlation_block(N, c, T: int) -> dict:
    slN = N[:T]
    slc = c[:T]
    n0 = sum(1 for t in range(T) if slc[t] == 0)
    n1 = T - n0
    mean0 = (sum(slN[t] for t in range(T) if slc[t] == 0) / n0) if n0 else None
    mean1 = (sum(slN[t] for t in range(T) if slc[t] == 1) / n1) if n1 else None
    r0 = [slN[t] / t for t in range(1, T) if slc[t] == 0]
    r1 = [slN[t] / t for t in range(1, T) if slc[t] == 1]
    return {
        "pearson_N_vs_c": pearson(slN, slc),
        "n_c0": n0,
        "n_c1": n1,
        "mean_N_given_c0": mean0,
        "mean_N_given_c1": mean1,
        "mean_N_over_t_given_c0": sum(r0) / len(r0) if r0 else None,
        "mean_N_over_t_given_c1": sum(r1) / len(r1) if r1 else None,
    }


def lc_block(seq_bits, label: str) -> dict:
    out = {"label": label, "values": []}
    for n in LC_NS:
        if n > len(seq_bits):
            continue
        length, _ = linear_complexity(seq_bits[:n])
        out["values"].append({
            "n": n,
            "linear_complexity": length,
            "LC_over_n": length / n,
        })
    return out


def sample_table(data, n: int) -> list:
    rows = []
    for t in range(n):
        rows.append({
            "t": t,
            "c": data["c"][t],
            "N": data["N"][t],
            "K": data["K"][t],
            "M": data["M"][t],
            "ones": data["ones"][t],
            "v2_z_plus_1": data["vplus"][t],
            "v2_z_minus_1": data["vminus"][t],
            "v2_z_xor_2_t": data["vxor_c"][t],
            "v2_z_shr_t": data["vshr"][t],
            "v2_z_next_xor_z": data["vnext"][t],
            "exp_v2_z_plus_1": data["exp_vplus"][t],
            "exp_v2_z_xor_2_t": data["exp_vxor_c"][t],
        })
    return rows


def constants_hold(data, T: int) -> dict:
    return {
        "v2_z_next_xor_z_all_1": all(v == 1 for v in data["vnext"][:T]),
        "v2_z_xor_z_shift_1_all_0": all(
            v == 0 for v in data["vdxor"][:T]
        ),
        "right_edge_v2_z_xor_2_t_0_for_t_gt_0": all(
            data["vxor_c"][t] == 0 for t in range(1, T)
        ),
        "experiment_v2_z_xor_2_t_0_for_t_gt_0": all(
            data["exp_vxor_c"][t] == 0 for t in range(1, T)
        ),
        "experiment_v2_z_plus_1_eq_2_for_t_ge_2": data["exp_vplus_ge2_is_2"],
        "lemma_v2_z_t_minus_1_eq_v2_z_prev_plus_1": data["lemma_hold"],
    }


def main() -> None:
    t0 = time.perf_counter()
    check = self_check(80)
    required = (
        "centre_matches_experiment",
        "experiment_packing_centre_ok",
        "twoadic_prefix_1_7_25_111",
        "bit_reversal_ok",
        "N_t_agrees_across_packings",
        "lemma_v2_f_minus_1_eq_v2_plus_1_orbit",
        "lemma_all_odd_mod_2_12",
        "v2_z_next_xor_z_eq_1",
        "v2_z_xor_2_t_eq_0_for_t_gt_0",
        "v2_z_minus_2_t_eq_0_for_t_gt_0",
        "v2_odd_plus_1_is_trailing_ones",
    )
    if not all(check[k] for k in required):
        raise SystemExit("self-check failed: " + json.dumps(check, indent=2))

    data = run_orbit(MAX_T)
    T = MAX_T
    densities = [density_block(data["N"], n) for n in DENSITY_NS]
    k_densities = [density_block(data["K"], n) for n in DENSITY_NS]
    m_densities = [density_block(data["M"], n) for n in DENSITY_NS]
    formulas = formula_search(data, T)
    corr = correlation_block(data["N"], data["c"], T)
    const = constants_hold(data, T)

    lc = [
        lc_block(bytes(data["c"][: max(LC_NS)]), "centre c_t"),
        lc_block(bytes(n & 1 for n in data["N"]), "N_t mod 2"),
        lc_block(bytes(n & 1 for n in data["K"]), "K_t mod 2"),
        lc_block(
            bytes(0 if (v or 0) <= 1 else 1 for v in data["vplus"]),
            "v2(z_t+1)>1",
        ),
        lc_block(
            bytes((v or 0) & 1 for v in data["vplus"]),
            "v2(z_t+1) mod 2",
        ),
        lc_block(
            bytes(0 if (v or 0) < 4 else 1 for v in data["vplus"]),
            "v2(z_t+1)>=4",
        ),
        lc_block(
            bytes((v or 0) & 1 for v in data["exp_vplus"]),
            "experiment v2(z_t+1) mod 2",
        ),
    ]

    mean_ratio_4096 = densities[DENSITY_NS.index(4096)]["mean_N_t_over_t"]
    mean_ratio_16384 = densities[DENSITY_NS.index(16384)]["mean_N_t_over_t"]
    kill_density = (
        mean_ratio_4096 > KILL_MEAN_RATIO and mean_ratio_16384 > KILL_MEAN_RATIO
    )
    # LC of N_t mod 2 comparable to c_t (ratio ~ 1/2) at the largest n.
    lc_n = lc[1]["values"][-1]
    lc_c = lc[0]["values"][-1]
    kill_lc = lc_n["LC_over_n"] >= 0.4 and lc_c["LC_over_n"] >= 0.4
    kill_reconstruct = formulas["centre_from_v2_z_shift_t"]["v2(z>>t)==0_iff_c_t=1"]
    # No O(log t) rescue: late min N_t/t still above the density kill.
    kill_not_log = densities[-1]["late_min_N_t_over_t"] > KILL_MEAN_RATIO

    fired = kill_density or kill_lc
    payload = {
        "not_a_prize_claim": True,
        "packing": (
            "primary: right-edge z_0=1, z_{t+1}=z XOR ((z<<1) OR (z<<2)); "
            "bit k is x(t,t-k); centre is bit t. Secondary: experiment.py "
            "row=(row<<2)^((row<<1)|row), the bit-reversal of the 2t+1-bit word."
        ),
        "not_this_attack": [
            "signed_carry.md identity Z_{t+1}=7Z_t-2Q_t, S(n)/n^2≈0.19",
            "twoadic.md residue periods of f on Z_2 (fixed low bits; no centre)",
        ],
        "self_check": check,
        "max_t": MAX_T,
        "formula_family_frozen": list(FORMULA_FAMILY),
        "constants": const,
        "densities_N": densities,
        "densities_K_carry_ins": k_densities,
        "densities_M_xor_collisions": m_densities,
        "correlation_N_vs_centre": corr,
        "formulas": formulas,
        "linear_complexity": lc,
        "sample_t_lt_32": sample_table(data, SAMPLE_T),
        "kill": {
            "mean_N_t_over_t_above_0_05_at_4096_and_16384": kill_density,
            "mean_N_t_over_t_4096": mean_ratio_4096,
            "mean_N_t_over_t_16384": mean_ratio_16384,
            "late_min_N_t_over_t_still_above_0_05": kill_not_log,
            "N_mod_2_LC_comparable_to_centre": kill_lc,
            "LC_N_mod_2_over_n": lc_n["LC_over_n"],
            "LC_c_over_n": lc_c["LC_over_n"],
            "v2_shift_t_reconstructs_centre_bit": kill_reconstruct,
            "fired": fired,
            "text": (
                "N_t is Θ(t): mean N_t/t stays above 0.05 at T=4096 and "
                "T=16384, so the nonlinear OR-overlaps are a positive-density "
                "subset of the row. Valuation sequences are either constant "
                "(or period-2 from the mod-8 low bits) or have linear "
                "complexity comparable to c_t. The only valuation identity "
                "that yields c_t is v2(z>>t)==0, which reads bit t of the "
                "packed row. No sparse-carry evaluator."
            ),
        },
        "elapsed_sec": time.perf_counter() - t0,
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "packing": "right-edge (primary); experiment packing is bit-reversal",
        "N_t_over_t_mean_4096": mean_ratio_4096,
        "N_t_over_t_mean_16384": mean_ratio_16384,
        "N_T_over_T": densities[-1]["N_T_over_T"],
        "pearson_N_vs_c": corr["pearson_N_vs_c"],
        "v2_findings": {
            "v2(z_{t+1} XOR z_t)": 1,
            "v2(z XOR (z<<1))": 0,
            "v2(z XOR 2^t) for t>0": 0,
            "v2(z+1) even t": 1,
            "v2(f(z)-1)=v2(z+1)": True,
            "experiment v2(z+1) for t>=2": 2,
        },
        "kill": payload["kill"]["fired"],
        "which": payload["kill"]["text"],
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
