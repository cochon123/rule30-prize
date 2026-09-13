# Cycle LY: \(G=1\) at \(p=14\) has packed AND except two \(t=0\) cells

On covering \(J_6,J_{10}\) for \(k\le 6\), every Green one at packed
\(p=14\) has packed AND except \((k,q)=(1,10)\) and \((2,10)\), each
with one silent `0000` at \(t=0\). The AND count is still Cycle LF's
\(want_{p=14}\); the \(G=1\) count is that plus the two silents.
This is **not** silent-free, **not** only \(k=1\), **not** silent on
\(q=6\), and **not** AND at those cells. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: \(p=14\) is Green-forced except two explicit
cells, but the rest of packed AND XOR \(J\) still reads the packed
row, so covering never-fail stays open.

Certify: `python3 research/cycle_ly.py --certify`.
Dump: `research/cycle_ly.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH/LF (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) at \(p=14\) has AND except two \(t=0\) cells)

Certified \(k\le 6\) (\(52\) Green ones, \(2\) silent, \(50\) AND).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (only \(p=4\) and \(p=6\) are silent-free)

Cycle LX. Aggregate silent-free packed indices on covering \(G=1\)
are \(\{4,6\}\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Killed

Silent-free at \(p=14\): \(k=1\), \(q=10\) is silent. Only \(k=1\):
\(k=2\), \(q=10\) is also silent. Silent on \(q=6\): \(k=1\),
\(q=6\) has no silent. AND at the silent cells: \(k=1\), \(q=10\) is
`0000`.

## Verdict

`LEMMA` (\(G=1\) at \(p=14\) has AND except two \(t=0\) cells; only
\(p=4\) and \(p=6\) are silent-free; \(p=14\) AND is \(0011\);
\(G=1\) at \(p=4\) always has packed AND; \(1001\) AND xor
remainder).
`KILLED` (silent-free at \(p=14\); only \(k=1\); silent on \(q=6\);
AND at the silent cells).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ly.md` (this note)
- `research/cycle_ly.py`
- `research/cycle_ly.json`
