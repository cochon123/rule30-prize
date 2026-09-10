import json
import time
from pathlib import Path
from strip_extend import initial, extend


def necklaces(n):
    out = []
    for x in range(1 << n):
        w = ''.join(str((x >> (n - 1 - i)) & 1) for i in range(n))
        rots = [w[i:] + w[:i] for i in range(n)]
        if min(rots) != w:
            continue
        if any(n % d == 0 and w == w[:d] * (n // d) for d in range(1, n)):
            continue
        out.append(w)
    return out


def scan(word, max_radius=30, cap=20000):
    start = time.monotonic()
    states, out, _ = initial(list(map(int, word)))
    rows = [{'radius': 1, 'surviving_states': len(states),
             'elapsed_seconds': time.monotonic() - start}]
    while states and len(states) <= cap and rows[-1]['radius'] < max_radius:
        radius = rows[-1]['radius']
        states, out, _ = extend(states, out, radius)
        rows.append({'radius': radius + 1, 'surviving_states': len(states),
                     'elapsed_seconds': time.monotonic() - start})
    return {'word': word, 'primitive_period': 8, 'scan': rows,
            'status': 'empty' if not states else ('cap' if len(states) > cap else 'radius')}


if __name__ == '__main__':
    results = [scan(w) for w in necklaces(8)]
    Path('research/period_scan_8.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps([{'word': r['word'], 'status': r['status'],
                       'final': r['scan'][-1]} for r in results], indent=2))
