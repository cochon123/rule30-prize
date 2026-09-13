# Cycle LX: only \(p=4\) and \(p=6\) are silent-free on covering \(G=1\)

On covering \(J_6,J_{10}\) for \(k\le 6\), the only packed indices
at which every Green one has packed AND (no silent \(G=1\) columns)
are \(p=4\) and \(p=6\). This is **not** only \(p=4\), **not**
silent-free at \(p=14\) on the census, **not** silent-free only
those two in each walk, and **not** rest XOR \(0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the two Green-forced slots do not make packed AND
XOR \(J\) Green-only, so covering never-fail stays open.

Certify: `python3 research/cycle_lx.py --certify` (~0.22s).
Dump: `research/cycle_lx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH (covering \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (only \(p=4\) and \(p=6\) are silent-free)

Certified \(k\le 6\). Aggregate silent-free set is \(\{4,6\}\)
(\(56\) and \(46\) Green ones). Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(G=1\) at \(p=6\) always has packed AND)

Cycle LW. Every Green one at packed \(p=6\) has packed AND.

## Lemma (\(G=1\) at \(p=4\) always has packed AND)

Cycle LV. Every Green one at packed \(p=4\) has packed AND.

## Killed

Only \(p=4\): \(p=6\) is also silent-free. Silent-free at \(p=14\)
on the census: \(k=1\), \(q=10\) has a silent column. Per-walk set
is only \(\{4,6\}\): \(k=2\), \(q=6\) also has \(p=14\). Rest XOR
\(0\): \(k=1\), \(q=10\) has rest XOR \(1\).

## Verdict

`LEMMA` (only \(p=4\) and \(p=6\) are silent-free; \(G=1\) at
\(p=6\) always has packed AND; \(G=1\) at \(p=4\) always has packed
AND; \(p=4\) AND is \(1001\) with odd count; \(1001\) AND xor
remainder).
`KILLED` (only \(p=4\); silent-free at \(p=14\) on the census;
per-walk set is only \(\{4,6\}\); rest XOR \(0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lx.md` (this note)
- `research/cycle_lx.py`
- `research/cycle_lx.json`
