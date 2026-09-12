# Cycle GV: at even \(s=t_0+2t\), \(m=2n+1\) with \(n=UQ-t-1\)

The reduced clock is the same integer as Cycle GU. Even-\(r\) Green
is \(G(n,d/2)\oplus G(n,d/2-1)\); odd-\(r\) Green is
\(G(n,(d-1)/2)\). That is **not** the odd-\(s\) single term
\(G(n,d/2)\); odd-\(r\) Green is **not** identically 0. Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: an even-\(s\) Green expansion does not prove
covering never-fail (AND still mixes).

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_gv.py --certify` (~0.02s). Dump:
`research/cycle_gv.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GM/GT/GU (clock \(k\le 11\); Green
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(m=2n+1\), \(n=UQ-t-1\) on every even \(s\))

Certified \(k\le 11\), 28665 times.

## Lemma (even-\(r\) two-term XOR; odd-\(r\) \(G(n,(d-1)/2)\))

Certified \(k\le 6\), all covering \(W\), every even \(s\) in the
window.

## Killed

Equals the odd-\(s\) single term: at \(k=0\), \(W=4U\), \(s=4\),
\(r=2\), \(G=1\) vs \(0\). Odd-\(r\) Green \(=0\): at \(k=1\),
\(W=4U\), \(s=8\), \(r=3\), \(G=1\). Even-\(r\) Green \(=0\): same
\(k=0\) witness.

## Verdict

`LEMMA` (even-\(s\) clock \(2n+1\); even-\(r\) two-term XOR; odd-\(r\)
single term).
`KILLED` (equals odd-\(s\) term; odd-\(r\) Green \(0\); even-\(r\)
Green \(0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gv.md` (this note)
- `research/cycle_gv.py`
- `research/cycle_gv.json`
