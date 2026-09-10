"""Finite checks for Rule 30; none proves a prize claim.

Run: python3 experiment.py --bits 100000 --output results.json
Only the Python standard library is required. Time 0 is the single seed.
"""
import argparse
import hashlib
import json
from pathlib import Path


def center_bits(count):
    # At time t, bit k represents spatial coordinate k-t (left to right).
    row = 1
    out = bytearray()
    for t in range(count):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row)
    return out


def reference_bits(count):
    row = {0: 1}
    out = bytearray()
    for t in range(count):
        out.append(row.get(0, 0))
        row = {j: row.get(j-1, 0) ^ (row.get(j, 0) | row.get(j+1, 0))
               for j in range(-t-1, t+2)}
    return out


def linear_complexity(bits):
    """Binary Berlekamp-Massey; integer bits encode connection coefficients."""
    connection = previous = 1
    length, last_change, history = 0, -1, 0
    for n, value in enumerate(bits):
        history = (history << 1) | value
        discrepancy = (connection & history).bit_count() & 1
        if discrepancy:
            old = connection
            connection ^= previous << (n-last_change)
            if 2*length <= n:
                length = n+1-length
                previous, last_change = old, n
    return length, connection


def check_recurrence(bits, length, connection):
    history = 0
    for n, value in enumerate(bits):
        history = (history << 1) | value
        if n >= length and (connection & history).bit_count() & 1:
            return n
    return None


def period_witnesses(bits, max_period):
    # A mismatch at t excludes that period for every proposed onset <= t.
    packed = int(''.join(map(str, reversed(bits))), 2)
    result = []
    for period in range(1, max_period+1):
        mismatch = (packed ^ (packed >> period)) & ((1 << (len(bits)-period))-1)
        result.append({'period': period, 'last_mismatch': mismatch.bit_length()-1})
    return result


def right_edge_periods(width):
    # Here bit k has the opposite orientation: u(t,k)=x(t,t-k).
    # u'=u XOR ((u<<1) OR (u<<2)); the prefix k<=width is closed.
    mask = (1 << (width+1))-1
    row = 1
    columns = [bytearray() for _ in range(width+1)]
    for _ in range(2**width):
        for k, col in enumerate(columns):
            col.append((row >> k) & 1)
        row = (row ^ ((row << 1) | (row << 2))) & mask
    assert row == 1
    periods = []
    for col in columns:
        p = 1
        while any(col[t] != col[t % p] for t in range(len(col))):
            p *= 2
        periods.append(p)
    return periods


def dyadic_annuli(bits):
    result = []
    start = 1
    while 2*start <= len(bits):
        discrepancy = maximum = 0
        for value in bits[start:2*start]:
            discrepancy += 2*value-1
            maximum = max(maximum, abs(discrepancy))
        result.append({'start': start, 'length': start,
                       'signed_imbalance': discrepancy,
                       'max_absolute_partial_imbalance': maximum,
                       'normalized_maximum': maximum/start})
        start *= 2
    return result


def self_check():
    assert center_bits(256) == reference_bits(256)
    assert list(center_bits(20)) == [1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1]
    for s, expected in [(bytes(40), 0), (bytes([1])*40, 1), (bytes([0,1])*20, 2)]:
        length, connection = linear_complexity(s)
        assert length == expected
        assert check_recurrence(s, length, connection) is None
    # Exhaustively compare BM's minimum with all recurrences for small words.
    for word in range(256):
        s = [(word >> n) & 1 for n in range(8)]
        expected = next(length for length in range(9)
                        if any(check_recurrence(s, length, 1 | (coeffs << 1)) is None
                               for coeffs in range(1 << length)))
        assert linear_complexity(s)[0] == expected
    sample = center_bits(100)
    for witness in period_witnesses(sample, 30):
        p = witness['period']
        assert witness['last_mismatch'] == max(t for t in range(len(sample)-p)
                                              if sample[t] != sample[t+p])
    # Independently verify the reflected edge-coordinate engine.
    from edge_audit import right_edge_table
    u = right_edge_table(256, 12)
    for k, p in enumerate(right_edge_periods(12)):
        assert all(u[t][k] == u[t+p][k] for t in range(257-p))
    assert [u[n][n] for n in range(13)] == list(center_bits(13))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bits', type=int, default=100000)
    parser.add_argument('--output', default='results.json')
    args = parser.parse_args()
    if args.bits < 64:
        parser.error('--bits must be at least 64')
    self_check()
    bits = center_bits(args.bits)
    checkpoints = [n for n in [10,100,1000,10000,100000,1000000] if n <= len(bits)]
    if len(bits) not in checkpoints:
        checkpoints.append(len(bits))
    stats = [{'bits': n, 'ones': sum(bits[:n]), 'density': sum(bits[:n])/n,
              'signed_imbalance': 2*sum(bits[:n])-n} for n in checkpoints]
    bm = []
    for n in [100,1000,10000,20000]:
        if n > len(bits):
            continue
        length, connection = linear_complexity(bits[:n])
        assert check_recurrence(bits[:n], length, connection) is None
        bm.append({'training_bits': n, 'linear_complexity': length,
                   'first_failure_index': check_recurrence(bits[:min(2*n,len(bits))],
                                                           length, connection)})
    witnesses = period_witnesses(bits, min(4096, len(bits)//2))
    report = {'status': 'finite evidence only; no prize problem solved',
              'convention': 'x(0,0)=1; samples t=0 through bits-1',
              'bits': len(bits), 'sha256_one_byte_per_bit': hashlib.sha256(bits).hexdigest(),
              'counts': stats, 'linear_recurrence_checks': bm,
              'periods_checked': len(witnesses),
              'all_checked_periods_excluded_for_onsets_through':
                  min(w['last_mismatch'] for w in witnesses),
              'period_witnesses': witnesses, 'dyadic_annuli': dyadic_annuli(bits),
              'right_edge_diagonal_periods_k_0_to_12': right_edge_periods(12)}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ('period_witnesses', 'dyadic_annuli')}, indent=2))


if __name__ == '__main__':
    main()
