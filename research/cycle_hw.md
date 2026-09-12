# Cycle HW: covering \(J\) folds through Green palindrome; unpaired is \(0000\)

\(G(n,j)=G(n,2n-j)\). Covering odd-\(s\) \(J\) is the XOR of AND at
the Green center \(j=n\) plus AND disagreements on in-support dual
pairs. \(G=1\) columns whose dual is clipped have even-\(s\) 4-tuple
\(0000\), so they drop out of \(J\). AND is **not** palindromic on
\(G=1\). Center AND is **not** always live. Unpaired is **not**
`green4`. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the palindrome fold is still not AND along Green
ones, so covering never-fail stays open.

Helper: `g_palindrome_table`. Certify: `python3 research/cycle_hw.py --certify`.
Dump: `research/cycle_hw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/HV (algebra \(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G\) palindrome)

\(G(n,j)=G(n,2n-j)\) and \(G(n,n)=1\), certified algebraically
\(n<64\).

## Lemma (covering \(J\) equals center XOR pair disagreements)

On packed covering \(J_6,J_{10}\) for \(k\le 6\), odd-\(s\) \(J\) is
AND at \(j=n\) XOR the disagreements \(\mathrm{AND}(n,j)\oplus\mathrm{AND}(n,2n-j)\)
on in-support \(G=1\) pairs. Census: \(n_{G=1}=22659\), centers
\(762\) of which \(232\) AND, unpaired \(4009\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Lemma (unpaired \(G=1\) is \(0000\))

If \(G(n,j)=1\) and the dual index \(2n-j\) is clipped (\(p<0\)),
the even-\(s\) 4-tuple is \(0000\). Those columns contribute 0 to
covering \(J\).

## Killed

AND palindrome on \(G=1\): at \(k=1\), \(s=5\), \(n=7\), \(j=6\) vs
\(8\), fours \(0001\) vs \(1001\). Center AND always live: at
\(k=0\), \(s=7\), \(n=1\), \(j=1\), \(p=8\), four \(0000\). Unpaired
equals `green4`: at \(k=0\), \(s=3\), \(n=3\), \(j=0\), \(p=10\), four
\(0000\) vs Green \(1011\).

## Verdict

`LEMMA` (\(G\) palindrome; covering \(J\) equals center XOR pair
disagreements; unpaired \(G=1\) is \(0000\)).
`KILLED` (AND palindrome on \(G=1\); center AND always live;
unpaired equals `green4`).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hw.md` (this note)
- `research/cycle_hw.py`
- `research/cycle_hw.json`
