import json, time
from strip_extend import initial, extend

def necklaces(n):
    out=[]
    for x in range(1<<n):
        w=''.join(str((x>>(n-1-i))&1) for i in range(n))
        if any(w == w[:d]*(n//d) for d in range(1,n) if n%d==0):
            continue
        if w != min(w[i:]+w[:i] for i in range(n)):
            continue
        out.append(w)
    return out

results=[]
for n in range(2,6):
  for word in necklaces(n):
    start=time.monotonic()
    states,out,stats=initial(list(map(int,word)))
    rec=[]
    stop='radius30'
    radius=1
    while True:
      rec.append({'radius':radius,'states':len(states),'edges':sum(map(len,out))})
      if not states:
        stop='empty'; break
      if len(states)>20000:
        stop='state_cap'; break
      if radius>=30:
        break
      states,out,stats=extend(states,out,radius)
      radius+=1
    results.append({'word':word,'length':n,'stop':stop,'last_radius':radius,
                    'last_states':len(states),'elapsed_sec':time.monotonic()-start,
                    'trajectory':rec})
    print(results[-1],flush=True)
with open('period_scan_2_5.json','w') as f:
  json.dump(results,f,indent=2)
