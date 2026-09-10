"""Exact finite-strip constraints under an imposed periodic center trace.

Outer boundary bits may vary arbitrarily. Every genuine Rule30 spacetime
strip obeying the imposed center is a path in this graph, but a graph path
need not extend to the single-seed global spacetime.
"""
import argparse
import json
from math import gcd


def graph(radius, word):
    width = 2*radius+1
    rows = 1 << width
    interior = ((1 << (width-1))-1) ^ 1
    out = [[] for _ in range(rows*len(word))]
    rev = [[] for _ in out]
    for phase, c in enumerate(word):
        next_phase = (phase+1) % len(word)
        for row in range(rows):
            if (row >> radius) & 1 != c:
                continue
            middle = ((row << 1) ^ (row | (row >> 1))) & interior
            if (middle >> radius) & 1 != word[next_phase]:
                continue
            v = phase*rows+row
            for left in range(2):
                for right in range(2):
                    w = next_phase*rows+(middle | left | (right << (width-1)))
                    out[v].append(w)
                    rev[w].append(v)
    return out, rev, rows


def components(out, rev):
    seen = bytearray(len(out))
    order = []
    for v in range(len(out)):
        if seen[v]:
            continue
        seen[v] = 1
        stack = [(v, 0)]
        while stack:
            v, i = stack[-1]
            if i == len(out[v]):
                order.append(v)
                stack.pop()
                continue
            stack[-1] = v, i+1
            w = out[v][i]
            if not seen[w]:
                seen[w] = 1
                stack.append((w, 0))
    labels = [-1]*len(out)
    groups = []
    for v in reversed(order):
        if labels[v] >= 0:
            continue
        group = []
        labels[v] = len(groups)
        stack = [v]
        while stack:
            u = stack.pop()
            group.append(u)
            for w in rev[u]:
                if labels[w] < 0:
                    labels[w] = len(groups)
                    stack.append(w)
        groups.append(group)
    return labels, groups


def analyze(radius, word, witnesses=False):
    out, rev, rows = graph(radius, word)
    labels, groups = components(out, rev)
    recurrent = []
    for label, group in enumerate(groups):
        if len(group) == 1 and group[0] not in out[group[0]]:
            continue
        depth = {group[0]: 0}
        stack = [group[0]]
        while stack:
            v = stack.pop()
            for w in out[v]:
                if labels[w] == label and w not in depth:
                    depth[w] = depth[v]+1
                    stack.append(w)
        period = 0
        for v in group:
            for w in out[v]:
                if labels[w] == label:
                    period = gcd(period, abs(depth[v]+1-depth[w]))
        assert period > 0
        fixed = []
        for j in range(2*radius+1):
            by_class = {}
            for v in group:
                cls = depth[v] % period
                bit = ((v % rows) >> j) & 1
                if cls in by_class and by_class[cls] != bit:
                    break
                by_class[cls] = bit
            else:
                fixed.append(j-radius)
        assert 0 in fixed
        info = {'vertices': len(group), 'graph_period': period,
                'periodic_columns_in_every_path': fixed,
                'neighbor_forced_periodic': -1 in fixed or 1 in fixed}
        if witnesses:
            info['vertices_encoded'] = group
        recurrent.append(info)
    residual = [g for g in recurrent if not g['neighbor_forced_periodic']]
    return {'radius': radius, 'center_word': ''.join(map(str, word)),
            'recurrent_components': len(recurrent),
            'components_without_forced_periodic_neighbor': len(residual),
            'residual_sizes': sorted([g['vertices'] for g in residual], reverse=True),
            'all_components': recurrent if witnesses else None}


def self_check():
    # Compare every finite-strip transition to direct local updates.
    radius, word = 2, [0, 1]
    out, rev, rows = graph(radius, word)
    for v, successors in enumerate(out):
        phase, row = divmod(v, rows)
        expected = set()
        for next_row in range(rows):
            if ((row >> radius)&1) != word[phase]:
                continue
            if ((next_row >> radius)&1) != word[(phase+1)%2]:
                continue
            if all(((next_row >> j)&1) == (((row >> (j-1))&1) ^
                   (((row >> j)&1) | ((row >> (j+1))&1))) for j in range(1,4)):
                expected.add(((phase+1)%2)*rows+next_row)
        assert set(successors) == expected
    # Constant-one center algebraically forces constant-zero left neighbor.
    assert analyze(2, [1])['components_without_forced_periodic_neighbor'] == 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--max-radius', type=int, default=5)
    p.add_argument('--output', default='research/strip_results.json')
    args = p.parse_args()
    self_check()
    results = []
    for word in ['0','1','01','001','011','0001','0011','0111']:
        for radius in range(1,args.max_radius+1):
            result = analyze(radius, list(map(int, word)))
            results.append(result)
            print(json.dumps(result), flush=True)
    with open(args.output,'w') as f:
        json.dump(results,f,indent=2)
