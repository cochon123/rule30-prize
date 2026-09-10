"""Radius-6 Jen certificates for isolated-zero center words 01^q.

Full enumeration via strip_graph.analyze; independent of strip_extend.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_graph import analyze, self_check


def main(qmax=30, radius=6):
    self_check()
    rows = []
    for q in range(1, qmax + 1):
        word = '0' + '1' * q
        a = analyze(radius, list(map(int, word)))
        rec = {
            'q': q,
            'word': word,
            'period': q + 1,
            'radius': radius,
            'recurrent_components': a['recurrent_components'],
            'residual_components': a['components_without_forced_periodic_neighbor'],
            'residual_sizes': a['residual_sizes'],
            'excluded_for_finite_seed': a['components_without_forced_periodic_neighbor'] == 0,
        }
        rows.append(rec)
        print(json.dumps({k: rec[k] for k in rec if k != 'residual_sizes'}), flush=True)
    path = Path(__file__).resolve().parent / 'isolated_zero_radius6.json'
    path.write_text(json.dumps(rows, indent=2) + '\n')
    excluded = [r['q'] for r in rows if r['excluded_for_finite_seed']]
    surviving = [r['q'] for r in rows if not r['excluded_for_finite_seed']]
    assert surviving == [1, 2, 3, 4, 5, 6, 8], surviving
    assert excluded == [q for q in range(1, qmax + 1) if q not in surviving]
    print('excluded q', excluded)
    print('surviving q', surviving)


if __name__ == '__main__':
    main()
