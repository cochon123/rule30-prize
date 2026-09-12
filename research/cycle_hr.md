# Cycle HR: odd-\(s\) Green 6-slot; AND of `odd_green4` is \(G(j+1)\) and not \(G(j)\)

On covering \((n,j)\), odd-\(s\) Green at packed bits
\(p-5,\ldots,p\) (\(\rho=2j+5,\ldots,2j\)) is
\(\mathrm{odd\_green6}(n,j)=(0,\,G(n,j+2),\,0,\,G(n,j+1),\,0,\,G(n,j))\).
That overlaps \(\mathrm{odd\_green4}(n,j+1)\) and
\(\mathrm{odd\_green4}(n,j)\). Dual of Cycle HM `green6`.
AND of `odd_green4` fires iff \(G(n,j+1)=1\) and \(G(n,j)=0\) (only
\(0100\) among the four vanishing-copy 4-tuples). The 6-tuple is
**not** `odd_green6`. `odd_green6` is **not** even-\(s\) `green6`.
Packed AND is **not** that Green formula. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the would-be AND-along-Green formula
\(G(j+1)\land\lnot G(j)\) fails on the packed row, so covering
never-fail stays open.

Helper: `odd_green6`. Certify: `python3 research/cycle_hr.py --certify` (~0.16s).
Dump: `research/cycle_hr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HL/HM/HQ (algebra \(n<64\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(s\) Green 6-slot \(=\) `odd_green6`; overlaps `odd_green4`)

\(G(2n,2j+r)\) for \(r=0,\ldots,5\). Certified algebraically
\(n<64\), and on \(J_6,J_{10}\) for \(k\le 6\).
`odd_green6(n,j)[:4]=odd_green4(n,j+1)` and
`odd_green6(n,j)[2:]=odd_green4(n,j)`. Copy slots vanish.

## Lemma (AND of `odd_green4` iff \(G(j+1)=1\) and \(G(j)=0\))

Four vanishing-copy 4-tuples; only \(0100\) is in `AND_ONES`.
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

6-tuple \(=\) `odd_green6`: at \(k=0\), \(s=3\), \(n=1\), \(j=0\),
\(p=6\), row \(101111\) vs Green \(010101\). `odd_green6` \(=\)
`green6`: same \((n,j)\), \(010101\neq 101011\). Packed AND \(=\)
\(G(j+1)\land\lnot G(j)\): same column, even-s \(0100\) so AND \(=1\),
but \(G(1,0)=G(1,1)=1\) so the Green formula is \(0\).

## Verdict

`LEMMA` (odd-\(s\) Green 6-slot; overlaps `odd_green4`; AND of
`odd_green4` iff \(G(j+1)=1\) and \(G(j)=0\)).
`KILLED` (6-tuple \(=\) `odd_green6`; `odd_green6` \(=\) `green6`;
AND \(=\) \(G(j+1)\land\lnot G(j)\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hr.md` (this note)
- `research/cycle_hr.py`
- `research/cycle_hr.json`
