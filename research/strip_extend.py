"""Extend only recurrent finite-strip states; avoid enumerating all bit rows.

With prune_neighbors=True, eliminate SCCs whose every infinite resident path
has a periodic neighbor. Jen's theorem excludes eventual residence in those
SCCs for the finite nonzero seed. Survivors remain an overapproximation.
"""
import argparse
import json
from math import gcd
from strip_graph import graph, components, analyze


def prune(states, out, radius, prune_neighbors=True):
    rev = [[] for _ in out]
    for v, edges in enumerate(out):
        for w in edges:
            rev[w].append(v)
    labels, groups = components(out, rev)
    keep, stats = [], []
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
        assert period
        fixed = []
        for j in (radius-1, radius, radius+1):
            classes = {}
            for v in group:
                key, bit = depth[v] % period, (states[v][1] >> j) & 1
                if key in classes and classes[key] != bit:
                    break
                classes[key] = bit
            else:
                fixed.append(j-radius)
        assert 0 in fixed
        excluded = -1 in fixed or 1 in fixed
        stats.append({'size': len(group), 'period': period, 'fixed': fixed,
                      'excluded': excluded})
        if not (prune_neighbors and excluded):
            keep.extend(group)
    remap = {v:i for i,v in enumerate(keep)}
    new_out = [[remap[w] for w in out[v]
                if w in remap and labels[w] == labels[v]] for v in keep]
    return [states[v] for v in keep], new_out, stats


def initial(word, prune_neighbors=True):
    out, _, rows = graph(1, word)
    states = [divmod(v, rows) for v in range(len(out))]
    return prune(states, out, 1, prune_neighbors)


def extend(states, out, radius, prune_neighbors=True):
    width = 2*radius+1
    expanded = [(phase, (row << 1) | (edge & 1) | ((edge >> 1) << (width+1)))
                for phase,row in states for edge in range(4)]
    expanded_out = [[] for _ in expanded]
    for v, (_, row) in enumerate(states):
        for edge in range(4):
            left, right = edge & 1, edge >> 1
            next_left = left ^ ((row & 1) | ((row >> 1) & 1))
            next_right = ((row >> (width-2)) & 1) ^ (((row >> (width-1)) & 1) | right)
            for w in out[v]:
                nextrow = states[w][1]
                if (nextrow & 1) == next_left and ((nextrow >> (width-1)) & 1) == next_right:
                    expanded_out[4*v+edge].extend(4*w+k for k in range(4))
    return prune(expanded, expanded_out, radius+1, prune_neighbors)


def self_check():
    # Independently compare incremental extension against full enumeration,
    # retaining all recurrent SCCs to avoid needing equality after Jen pruning.
    for word in ([0],[1],[0,1],[0,0,1]):
        states, out, _ = initial(word, False)
        for radius in range(2,5):
            states,out,_ = extend(states,out,radius-1,False)
            expected = analyze(radius,word,True)
            rows = 1 << (2*radius+1)
            expected_states = {divmod(v,rows) for g in expected['all_components']
                               for v in g['vertices_encoded']}
            assert set(states) == expected_states, (word,radius)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--word', default='01')
    p.add_argument('--max-radius', type=int, default=30)
    p.add_argument('--state-cap', type=int, default=200000)
    p.add_argument('--output', default='research/strip_extended.json')
    args=p.parse_args()
    self_check()
    word=list(map(int,args.word))
    states,out,stats=initial(word)
    results=[]
    for radius in range(1,args.max_radius+1):
        result={'radius':radius,'word':args.word,'surviving_states':len(states),
                'surviving_edges':sum(map(len,out)),'components':stats}
        results.append(result)
        print(json.dumps(result),flush=True)
        if not states or len(states)>args.state_cap or radius==args.max_radius:
            break
        states,out,stats=extend(states,out,radius)
    with open(args.output,'w') as f:
        json.dump(results,f,indent=2)
