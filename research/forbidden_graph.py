"""Finite-strip exclusion certificates for an ultimately missing center word.

Keeps center history and arbitrary outer boundary values. SCCs where every
resident path has a periodic adjacent pair are excluded by Jen's theorem.
The graph is an overapproximation of actual finite-seed spacetime tails.
"""
import argparse
import json
from math import gcd
from strip_graph import components


def initial(word):
    length = len(word)
    forbidden = int(word,2)
    histmask = (1 << (length-1))-1
    states = [(h,row) for h in range(histmask+1) for row in range(8)
              if length == 1 or (h&1) == ((row>>1)&1)]
    if length == 1:
        states = [(h,row) for h,row in states if ((row>>1)&1) != forbidden]
    index = {state:i for i,state in enumerate(states)}
    out = [[] for _ in states]
    for i,(history,row) in enumerate(states):
        center = (row&1)^(((row>>1)&1)|((row>>2)&1))
        full = (history << 1)|center
        if full == forbidden:
            continue
        nh=full&histmask
        for edge in range(4):
            nr=(edge&1)|(center<<1)|((edge>>1)<<2)
            if (nh,nr) in index:
                out[i].append(index[nh,nr])
    return prune(states,out,1)


def prune(states,out,radius):
    rev=[[] for _ in out]
    for v,edges in enumerate(out):
        for w in edges:
            rev[w].append(v)
    labels,groups=components(out,rev)
    keep=[]
    stats=[]
    for label,group in enumerate(groups):
        if len(group)==1 and group[0] not in out[group[0]]:
            continue
        depth={group[0]:0}
        stack=[group[0]]
        while stack:
            v=stack.pop()
            for w in out[v]:
                if labels[w]==label and w not in depth:
                    depth[w]=depth[v]+1
                    stack.append(w)
        period=0
        for v in group:
            for w in out[v]:
                if labels[w]==label:
                    period=gcd(period,abs(depth[v]+1-depth[w]))
        fixed=[]
        for j in range(2*radius+1):
            vals={}
            for v in group:
                cls=depth[v]%period
                bit=(states[v][1]>>j)&1
                if cls in vals and vals[cls]!=bit:
                    break
                vals[cls]=bit
            else:
                fixed.append(j-radius)
        excluded=any(j+1 in fixed for j in fixed)
        stats.append({'size':len(group),'period':period,'fixed':fixed,'excluded':excluded})
        if not excluded:
            keep.extend(group)
    remap={v:i for i,v in enumerate(keep)}
    return ([states[v] for v in keep],
            [[remap[w] for w in out[v] if w in remap and labels[w]==labels[v]] for v in keep],
            stats)


def extend(states,out,radius):
    width=2*radius+1
    ns=[(h,(row<<1)|(edge&1)|((edge>>1)<<(width+1)))
        for h,row in states for edge in range(4)]
    no=[[] for _ in ns]
    for v,(_,row) in enumerate(states):
        for edge in range(4):
            nl=(edge&1)^((row&1)|((row>>1)&1))
            nr=((row>>(width-2))&1)^(((row>>(width-1))&1)|(edge>>1))
            for w in out[v]:
                target=states[w][1]
                if (target&1)==nl and ((target>>(width-1))&1)==nr:
                    no[4*v+edge].extend(4*w+k for k in range(4))
    return prune(ns,no,radius+1)


def run(word,maxradius,cap):
    states,out,stats=initial(word)
    results=[]
    for radius in range(1,maxradius+1):
        result={'forbidden_word':word,'radius':radius,'surviving_states':len(states),
                'surviving_edges':sum(map(len,out)),'components':stats}
        print(json.dumps(result),flush=True)
        results.append(result)
        if not states or len(states)>cap or radius==maxradius:
            break
        states,out,stats=extend(states,out,radius)
    return results


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--word',default='00')
    p.add_argument('--max-radius',type=int,default=12)
    p.add_argument('--state-cap',type=int,default=100000)
    p.add_argument('--output',default='research/forbidden_results.json')
    a=p.parse_args()
    results=run(a.word,a.max_radius,a.state_cap)
    with open(a.output,'w') as f:
        json.dump(results,f,indent=2)
