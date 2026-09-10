import json
import time
from strip_extend import initial, extend


def scan(q, cap=10000, max_radius=30):
    word = '0' + '1' * q
    start = time.monotonic()
    states, out, _ = initial(list(map(int, word)))
    rows = [{'radius': 1, 'states': len(states),
             'elapsed_seconds': time.monotonic() - start}]
    while states and len(states) <= cap and rows[-1]['radius'] < max_radius:
        r = rows[-1]['radius']
        states, out, _ = extend(states, out, r)
        rows.append({'radius': r + 1, 'states': len(states),
                     'elapsed_seconds': time.monotonic() - start})
    return {'q': q, 'word': word, 'scan': rows,
            'status': 'empty' if not states else ('cap' if len(states) > cap else 'radius')}


if __name__ == '__main__':
    results = [scan(q) for q in range(1, 33)]
    with open('research/isolated_zero_scan.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(json.dumps([{'q': x['q'], 'status': x['status'], 'final': x['scan'][-1]}
                      for x in results], indent=2))
