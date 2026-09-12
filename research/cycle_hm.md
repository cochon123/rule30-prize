# Cycle HM: even-\(s\) Green 6-slot; odd-\(s\) 4-tuple is Rule 30 of that 6-tuple

On covering \((n,j)\), even-\(s\) Green at packed bits
\(p-5,\ldots,p\) (\(\rho=2j+5,\ldots,2j\)) is
\(\mathrm{green6}(n,j)=(G(n,j+2),\,\mathrm{cob}(j+2),\,G(n,j+1),\,\mathrm{cob}(j+1),\,G(n,j),\,\mathrm{cob}(j))\).
That overlaps \(\mathrm{green4}(n,j+1)\) and \(\mathrm{green4}(n,j)\).
The odd-\(s\) 4-tuple is Rule 30 of the even-\(s\) 6-tuple; adjacent
odd-\(s\) AND is the two overlapping 4-tuple productions. The 6-tuple
is **not** `green6`. The AND pair is **not**
\((G(n,j+1),G(n,j))\). Adjacent AND is **not** independent. Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a 6-slot Green formula plus a Rule 30 lift does
not give a closed form for the row along Green ones, so covering
never-fail stays open.

Helper: `green6` / `r30_4`. Certify:
`python3 research/cycle_hm.py --certify` (~0.37s). Dump:
`research/cycle_hm.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HJ/HL (algebra \(n<64\);
covering \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (even-\(s\) Green 6-slot \(=\) `green6`; overlaps `green4`)

\(G(2n+1,2j+r)\) for \(r=0,\ldots,5\). Certified algebraically
\(n<64\), and on \(J_6,J_{10}\) for \(k\le 6\).
`green6(n,j)[:4]=green4(n,j+1)` and `green6(n,j)[2:]=green4(n,j)`.

## Lemma (odd-\(s\) 4-tuple \(=\) Rule 30 of the 6-tuple)

Adjacent odd-\(s\) AND is
\((\mathrm{and\_from\_tuple}(u,v,z,a),\,\mathrm{and\_from\_tuple}(z,a,b,c))\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

6-tuple \(=\) `green6`: at \(k=0\), \(s=2\), \(n=1\), \(j=0\), \(p=6\),
row \(100100\) vs Green \(101011\). AND pair \(=\)
\((G(n,j+1),G(n,j))\): at \(k=0\), \(s=3\), \(n=1\), \(j=1\),
\((0,1)\neq(1,1)\). Adjacent AND independent: at \(k=0\), \(s=3\),
\(n=1\), \(j=0\), both live.

## Verdict

`LEMMA` (even-\(s\) Green 6-slot; overlaps `green4`; odd-\(s\) 4-tuple
\(=\) Rule 30 of the 6-tuple; adjacent AND from overlapping 4-tuples).
`KILLED` (6-tuple \(=\) `green6`; AND pair \(=\) Green pair; adjacent
AND independent).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hm.md` (this note)
- `research/cycle_hm.py`
- `research/cycle_hm.json`
