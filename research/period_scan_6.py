"""Primitive period-six words, modulo cyclic phase; finite strip exclusions."""
import json
import time
from pathlib import Path
from strip_extend import initial, extend


def primitive_necklaces(length):
    for code in range(1<<length):
        word=f'{code:0{length}b}'
        if word!=min(word[i:]+word[:i] for i in range(length)):
            continue
        if any(length%d==0 and word==word[:d]*(length//d) for d in range(1,length)):
            continue
        yield word


if __name__=='__main__':
    results=[]
    path=Path('research/period_scan_6.json')
    for word in primitive_necklaces(6):
        start=time.monotonic()
        states,out,_=initial(list(map(int,word)))
        for radius in range(1,31):
            if not states or len(states)>20000 or radius==30:
                break
            states,out,_=extend(states,out,radius)
        r={'word':word,'radius':radius,'states':len(states),'excluded':not states,
           'seconds':round(time.monotonic()-start,3)}
        results.append(r)
        path.write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(r),flush=True)
