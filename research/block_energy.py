"""Mesoscopic block energy of the Rule 30 center column (prize problem 2).

Measures E_m and in-block pairwise correlations on the actual seed orbit.
Does not prove density, and does not claim a prize result.

Run: python3 research/block_energy.py --bits 262144 --output research/block_energy_results.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits, reference_bits


def packed_row_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def center_lr_bits(count: int):
    """Center, left neighbor, and right neighbor of the single-seed orbit.

    Packed convention matches experiment.center_bits: at time t, bit k is
    spatial coordinate k-t. Spatial -1 is bit t-1; spatial +1 is bit t+1.
    """
    row = 1
    center = bytearray(count)
    left = bytearray(count)
    right = bytearray(count)
    for t in range(count):
        center[t] = (row >> t) & 1
        left[t] = (row >> (t - 1)) & 1 if t else 0
        right[t] = (row >> (t + 1)) & 1
        row = packed_row_update(row)
    return center, left, right


def signed(bits) -> list[int]:
    return [2 * int(v) - 1 for v in bits]


def dyadic_A(a: list[int], N: int) -> tuple[int, int]:
    """Return (A_m, signed annulus sum) on [N, 2N)."""
    partial = 0
    maximum = 0
    for t in range(N, 2 * N):
        partial += a[t]
        if abs(partial) > maximum:
            maximum = abs(partial)
    return maximum, partial


def block_sums(a: list[int], N: int, L: int) -> list[int]:
    B = N // L
    out = [0] * B
    for b in range(B):
        start = N + b * L
        s = 0
        for t in range(start, start + L):
            s += a[t]
        out[b] = s
    return out


def energy_from_blocks(S: list[int]) -> int:
    return sum(s * s for s in S)


def haar_cross(S_fine: list[int]) -> tuple[int, list[int]]:
    """Merge adjacent length-ℓ blocks. Return (cross, coarse sums).

    Identity: S_coarse[b]^2 = S[2b]^2 + S[2b+1]^2 + 2 S[2b] S[2b+1].
    """
    coarse = []
    cross = 0
    for i in range(0, len(S_fine) - 1, 2):
        left, right = S_fine[i], S_fine[i + 1]
        cross += left * right
        coarse.append(left + right)
    return cross, coarse


def inblock_C(a: list[int], N: int, L: int, lags: list[int] | None = None):
    """C_m(h) = sum over in-block pairs at lag h of a_t a_{t+h}.

    If lags is None, compute every h in 1..L-1.
    """
    if lags is None:
        wanted = range(1, L)
        C = [0] * L
        full = True
    else:
        wanted = lags
        C = {h: 0 for h in lags}
        full = False
    B = N // L
    for b in range(B):
        start = N + b * L
        blk = a[start:start + L]
        for h in wanted:
            s = 0
            stop = L - h
            for i in range(stop):
                s += blk[i] * blk[i + h]
            if full:
                C[h] += s
            else:
                C[h] += s
    return C


def lag1_background_split(c, left, right, N: int, L: int):
    """Split the lag-1 in-block correlation by the background pair (c_t, r_t).

    Exact identity: c_t XOR c_{t+1} = l_t XOR r_t XOR (c_t AND r_t),
    so a_t a_{t+1} = (-1)^{l XOR r XOR c r}.
    """
    B = N // L
    buckets = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    counts = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    quadratic_ones = 0
    formula_mismatch = 0
    total_pairs = 0
    for b in range(B):
        start = N + b * L
        # pairs t, t+1 both in the block: t in [start, start+L-2]
        for t in range(start, start + L - 1):
            ct, lt, rt = c[t], left[t], right[t]
            xor = ct ^ c[t + 1]
            formula = lt ^ rt ^ (ct & rt)
            if xor != formula:
                formula_mismatch += 1
            corr = 1 if xor == 0 else -1
            key = (int(ct), int(rt))
            buckets[key] += corr
            counts[key] += 1
            e0 = ct ^ c[t + 1]
            e1 = rt ^ right[t + 1]
            quadratic_ones += e0 & e1
            total_pairs += 1
    return {
        'pairs': total_pairs,
        'formula_mismatch': formula_mismatch,
        'quadratic_term_ones': quadratic_ones,
        'by_cr': {f'{p}{q}': buckets[(p, q)] for p, q in buckets},
        'count_cr': {f'{p}{q}': counts[(p, q)] for p, q in counts},
    }


def sample_lags(L: int) -> list[int]:
    lags = list(range(1, min(L, 17)))
    h = 16
    while h < L:
        if h not in lags:
            lags.append(h)
        h *= 2
    if L // 2 not in lags and L // 2 > 0:
        lags.append(L // 2)
    if L - 1 not in lags and L > 1:
        lags.append(L - 1)
    return sorted(h for h in lags if 1 <= h < L)


def measure_annulus(a, c, left, right, m: int, full_corr_limit: int):
    N = 1 << m
    L = 1 << (m // 2)
    B = N // L
    S = block_sums(a, N, L)
    E = energy_from_blocks(S)
    A, annulus_sum = dyadic_A(a, N)
    cs_bound = (B * E) ** 0.5 + L
    NL = N * L

    cascade = []
    S_scale = block_sums(a, N, 1)
    E_scale = energy_from_blocks(S_scale)
    assert E_scale == N
    for ell in range(1, m + 1):
        cross, S_scale = haar_cross(S_scale)
        E_next = energy_from_blocks(S_scale)
        cascade.append({
            'block_len': 1 << ell,
            'cross': cross,
            'energy': E_next,
            'energy_over_N': E_next / N,
            'energy_over_NL_at_prescribed': E_next / NL,
        })
        E_scale = E_next
    assert S_scale[0] == annulus_sum
    assert cascade[m // 2 - 1]['block_len'] == L
    assert cascade[m // 2 - 1]['energy'] == E

    compute_full = L <= full_corr_limit
    if compute_full:
        C = inblock_C(a, N, L, None)
        C_list = [{'h': h, 'C': C[h], 'pairs': B * (L - h),
                   'mean': C[h] / (B * (L - h))}
                  for h in range(1, L)]
        sum_C = sum(C[h] for h in range(1, L))
        sum_abs_C = sum(abs(C[h]) for h in range(1, L))
        even_C = sum(C[h] for h in range(2, L, 2))
        odd_C = sum(C[h] for h in range(1, L, 2))
        alt_C = sum((1 - 2 * (h & 1)) * C[h] for h in range(1, L))
        expansion_E = N + 2 * sum_C
        assert expansion_E == E
        selected = []
        seen = set()
        for row in C_list:
            if row['h'] <= 16 or h_pow2(row['h']) or row['h'] == L - 1:
                if row['h'] not in seen:
                    selected.append(row)
                    seen.add(row['h'])
        C_summary = {
            'full': True,
            'sum_C': sum_C,
            'sum_abs_C': sum_abs_C,
            'abs_sum_over_sum_abs': (abs(sum_C) / sum_abs_C) if sum_abs_C else 0.0,
            'even_C': even_C,
            'odd_C': odd_C,
            'alternating_signed_C': alt_C,
            'selected': selected,
        }
    else:
        lags = sample_lags(L)
        C = inblock_C(a, N, L, lags)
        C_summary = {
            'full': False,
            'selected': [{'h': h, 'C': C[h], 'pairs': B * (L - h),
                          'mean': C[h] / (B * (L - h))}
                         for h in lags],
        }

    lag1 = lag1_background_split(c, left, right, N, L)
    max_abs_S = max(abs(s) for s in S)
    mean_sq_bias = E / NL
    rms_S = (E / B) ** 0.5
    n_pos = sum(1 for s in S if s > 0)
    n_neg = sum(1 for s in S if s < 0)
    n_zero = sum(1 for s in S if s == 0)

    return {
        'm': m,
        'N': N,
        'L': L,
        'B': B,
        'NL': NL,
        'E_m': E,
        'E_over_NL': E / NL,
        'E_over_N': E / N,
        'A_m': A,
        'A_over_N': A / N,
        'annulus_sum': annulus_sum,
        'cs_bound': cs_bound,
        'cs_bound_over_N': cs_bound / N,
        'max_abs_block_sum': max_abs_S,
        'rms_block_sum': rms_S,
        'rms_over_sqrt_L': rms_S / (L ** 0.5),
        'block_sign_pos': n_pos,
        'block_sign_neg': n_neg,
        'block_sign_zero': n_zero,
        'lag1_background': lag1,
        'correlations': C_summary,
        'haar_cascade': cascade,
    }


def h_pow2(h: int) -> bool:
    return h > 0 and (h & (h - 1)) == 0


def self_check():
    c, left, right = center_lr_bits(64)
    assert bytes(c) == bytes(center_bits(64))
    assert bytes(center_bits(64)) == bytes(reference_bits(64))
    assert list(c[:20]) == [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    for t in range(63):
        assert c[t + 1] == left[t] ^ (c[t] | right[t])
        xor = c[t] ^ c[t + 1]
        formula = left[t] ^ right[t] ^ (c[t] & right[t])
        assert xor == formula

    a = signed(c)
    # Expansion vs block squares on a tiny annulus.
    N, L = 16, 4
    S = block_sums(a, N, L)
    E = energy_from_blocks(S)
    C = inblock_C(a, N, L, None)
    assert E == N + 2 * sum(C[h] for h in range(1, L))
    # Haar cascade from length 1 to L.
    S1 = block_sums(a, N, 1)
    cross, S2 = haar_cross(S1)
    assert energy_from_blocks(S2) == energy_from_blocks(S1) + 2 * cross
    cross2, S4 = haar_cross(S2)
    assert S4 == S
    assert energy_from_blocks(S4) == E

    # Cauchy-Schwarz bound on this annulus.
    A, _ = dyadic_A(a, N)
    B = N // L
    assert A <= (B * E) ** 0.5 + L + 1e-9

    # iid-scale sanity: E_m is at least N (equality at L=1).
    S_one = block_sums(a, N, 1)
    assert energy_from_blocks(S_one) == N


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bits', type=int, default=131072)
    parser.add_argument('--output', default='research/block_energy_results.json')
    parser.add_argument('--full-corr-limit', type=int, default=256,
                        help='Compute every in-block lag when L is at most this.')
    args = parser.parse_args()
    if args.bits < 64:
        parser.error('--bits must be at least 64')
    self_check()
    n = args.bits
    c, left, right = center_lr_bits(n)
    assert bytes(c[: min(n, 256)]) == bytes(center_bits(min(n, 256)))
    a = signed(c)

    max_m = 0
    while 2 * (1 << (max_m + 1)) <= n:
        max_m += 1
    annuli = []
    for m in range(4, max_m + 1):
        rec = measure_annulus(a, c, left, right, m, args.full_corr_limit)
        assert rec['lag1_background']['formula_mismatch'] == 0
        annuli.append(rec)
        print(
            f"m={m:2d} N={rec['N']:7d} L={rec['L']:5d} "
            f"E/(NL)={rec['E_over_NL']:.5f} E/N={rec['E_over_N']:.3f} "
            f"A/N={rec['A_over_N']:.5f} rms/sqrt(L)={rec['rms_over_sqrt_L']:.3f} "
            f"CS/N={rec['cs_bound_over_N']:.4f}",
            flush=True,
        )
        if rec['correlations'].get('full'):
            cs = rec['correlations']
            print(
                f"     sumC={cs['sum_C']:8d} |sum|/sum|C|={cs['abs_sum_over_sum_abs']:.4f} "
                f"evenC={cs['even_C']:8d} oddC={cs['odd_C']:8d} "
                f"altC={cs['alternating_signed_C']}",
                flush=True,
            )
        cr = rec['lag1_background']['by_cr']
        print(
            f"     lag1 by (c,r): 00={cr['00']} 01={cr['01']} "
            f"10={cr['10']} 11={cr['11']} "
            f"quadratic_ones={rec['lag1_background']['quadratic_term_ones']}"
            f"/{rec['lag1_background']['pairs']}",
            flush=True,
        )

    # Candidate closed values for sum_C, checked where full C is available.
    identity_failures = []
    for rec in annuli:
        if not rec['correlations'].get('full'):
            continue
        N, E = rec['N'], rec['E_m']
        sum_C = rec['correlations']['sum_C']
        candidates = {
            'sum_C=0 (would give E=N)': sum_C,
            'sum_C=-N/2 (would give E=0)': sum_C + N / 2,
            'even_C+odd_C=0': rec['correlations']['even_C'] + rec['correlations']['odd_C'] - sum_C,
            'even_C=0': rec['correlations']['even_C'],
            'odd_C=0': rec['correlations']['odd_C'],
            'alternating_C=0': rec['correlations']['alternating_signed_C'],
        }
        # even_C+odd_C=sum_C always; the third candidate is a tautology check.
        del candidates['even_C+odd_C=0']
        failed = {name: val for name, val in candidates.items() if val != 0}
        identity_failures.append({
            'm': rec['m'],
            'E_m': E,
            'E_minus_N': E - N,
            'failed_closed_forms': failed,
        })

    payload = {
        'status': 'finite measurement only; no density proof; no prize claim',
        'seed': 'x(0,0)=1; packed generator matches experiment.center_bits',
        'bits': n,
        'full_corr_limit': args.full_corr_limit,
        'target': 'E_m = o(N L) with L=2^{floor(m/2)} would imply A_m=o(N) via CS',
        'annuli': annuli,
        'closed_form_identity_failures': identity_failures,
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.write_text(json.dumps(payload, indent=2) + '\n')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
