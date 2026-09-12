# Cycle GW: even-\(s\) Green is the coboundary of the next odd-\(s\) row

Odd-\(r\): \(G(s,r)=G(s+1,r+1)\), and \(r+1\) is always in the odd-\(s\)
band. Even-\(r\): \(G(s,r)=G(s+1,r)\oplus G(s+1,r+2)\) whenever
\(r+2\) is in-band; that **fails** at the clipped right edge \(r=W\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a Green coboundary relating consecutive times does
not prove covering never-fail (AND still mixes).

Helper: `python3 research/cycle_gw.py --certify` (~0.03s). Dump:
`research/cycle_gw.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GT/GU/GV (Green \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(r\) copy \(G(s,r)=G(s+1,r+1)\))

Certified \(k\le 6\). The shifted index \(r+1\) always lies in the
next odd-\(s\) band.

## Lemma (even-\(r\) coboundary when \(r+2\) in-band)

Certified \(k\le 6\). The only even-\(r\) exceptions are the clipped
right edge \(r=W\) after \(s\ge U+W\).

## Killed

Coboundary at clipped \(r=W\): at \(k=1\), \(W=4U\), \(s=10\),
\(r=8\), \(G=1\) but \(r+2\) is out of band. Copy on even \(r\): at
\(k=0\), \(W=4U\), \(s=4\), \(r=2\), \(1\neq 0\). Even-\(s\) Green
independent of the next odd-\(s\) row: odd-\(r\) copy is an equality.

## Verdict

`LEMMA` (odd-\(r\) copy; \(r+1\) in-band; even-\(r\) coboundary when
\(r+2\) in-band).
`KILLED` (coboundary at clipped \(r=W\); copy on even \(r\);
independent of odd-\(s\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gw.md` (this note)
- `research/cycle_gw.py`
- `research/cycle_gw.json`
