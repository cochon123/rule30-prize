# Cycle HU: odd-\(s\) AND iff non-coboundary and \(a\oplus(b\lor c)\)

Packed AND fires iff the even-\(s\) 4-tuple \((z,a,b,c)\) is not
coboundary-shaped and \(a\oplus(b\lor c)=1\). That is `AND_ONES` as
two Boolean clauses: Cycle HT kills cob; the leftover 8 non-cob
tuples fire iff the first AND factor \(a\oplus(b\lor c)\) is 1.
AND is **not** iff non-cob. AND is **not** iff \(a\oplus(b\lor c)=1\).
\(G=1\) AND is **not** iff FRESH. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the two-clause formula is still not AND along
Green ones, so covering never-fail stays open.

Helper: `and_clause`. Certify: `python3 research/cycle_hu.py --certify`.
Dump: `research/cycle_hu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HT (16-row table; covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (AND iff non-cob and \(a\oplus(b\lor c)\))

16-row identity, equal to `AND_ONES`. On non-cob tuples the second
AND factor \(z\oplus(a\lor b)\) is redundant: if \(a\oplus(b\lor c)=1\)
then \(z\oplus(a\lor b)=1\). Certified on packed covering \(J_6,J_{10}\)
for \(k\le 6\). Every covering AND is FRESH or CONT. Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

AND iff non-cob: at \(k=1\), \(s=11\), \(n=4\), \(j=3\), \(p=14\),
four \(1111\). AND iff \(a\oplus(b\lor c)\): at \(k=0\), \(s=5\),
\(n=2\), \(j=1\), \(p=8\), cob four \(0001\). \(G=1\) AND iff FRESH:
at \(k=1\), \(s=13\), \(n=3\), \(j=1\), \(p=18\), CONT \(0011\).

## Verdict

`LEMMA` (AND iff non-cob and \(a\oplus(b\lor c)\); clause equals
`AND_ONES`).
`KILLED` (AND iff non-cob; AND iff \(a\oplus(b\lor c)\); \(G=1\) AND
iff FRESH).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hu.md` (this note)
- `research/cycle_hu.py`
- `research/cycle_hu.json`
