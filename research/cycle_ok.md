# Cycle OK: the \(S\)-bit vanishes on every even row

If \(n\) is even and \(G(n,j)=1\), then \(j\) is even. Both neighbors
\(j-1\) and \(j+1\) are odd, so the even-\(n\) clause of \(G\) gives
\[
G(n,j-1)=G(n,j+1)=0.
\]
Cycle OI already used the left neighbor: palindrome-right \(T\) is
silent on every even row. The right neighbor is the \(S\)-bit. It
is silent at every live cell, whether or not \((j-n)\bmod 3=1\),
and whether or not the covering clip keeps the cell. An even row
therefore contributes neither \(S\) nor \(T\). On those rows the
error bit of \(E_k=R_k\oplus S_k\oplus T_k\) equals the packed rest
bit.

Odd rows are where \(S\) and \(T\) still live. \(T_k=1\) iff \(k=2\)
is Cycle OJ, and that bit is entirely an odd-row sum. Cancelling
the even-row rest still has to happen on odd rows. \(E_k=0\) for
all \(k\) is not proved. Do **not** catalogue further \(S\)/\(T\)
subregions. Do **not** claim \(E_k=0\) for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=12\)
\(T\)-bands. Do **not** walk \(k=11\) covering packed.

Not a prize claim: covering never-fail stays open. \(I_k=1\)
infinitely often stays open.

Certify: `python3 research/cycle_ok.py --certify` (~0.80s).
Dump: `research/cycle_ok.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OI/OJ (even-\(n\) neighbor bits on \(n<2048\); prefix
OI even-\(T\) vanish and OJ \(T_k=1\) iff \(k=2\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
walk, no \(k=12\) \(T\)-band).

## Lemma (even \(n\): both neighbor bits vanish)

Let \(n\) be even and \(G(n,j)=1\). Then \(j\) is even, hence
\(j\pm 1\) are odd, hence \(G(n,j\pm 1)=0\). Every palindrome-right
\(S\)-filter cell on an even row (that is, \(G(n,j)=1\),
\((j-n)\bmod 3=1\), \(G(n,j-1)=0\)) still contributes
\(G(n,j+1)=0\). Status: **lemma** for every even \(n\). Checked
on \(n<2048\), including cells that meet the mod-\(3\) filter.

## Killed

The \(S\)-bit fires on an even row: \(n=4\), \(j=8\),
\(d=4\equiv 1\pmod{3}\), \(G(4,8)=1\), and \(G(4,9)=0\).

## Verdict

`LEMMA` (even-row \(S\)-bit vanishes for every even \(n\);
even-row \(T\)-bit vanishes).
`KILLED` (\(S\) fires on an even row).
`OPEN` (\(E_k=0\) for all \(k\); \(I_k=1\) infinitely often;
some \(\varphi^{(q)}_k=1\) infinitely often).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
Prize unsolved.

## Files

- `research/cycle_ok.md` (this note)
- `research/cycle_ok.py`
- `research/cycle_ok.json`
- `research/cycle_oj.md` (\(T_k=1\) iff \(k=2\))
- `research/cycle_oi.md` (even-row \(T\)-bit)
