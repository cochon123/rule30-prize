# Cycle BK: exact pentuple-Green bits on the covering annuli

Cycle BJ closed the quad-Green remainder on the 5-fold and 9-fold
Fermat annuli. Pentuples are odd multiplicity, so they contribute to
the covering spines. \(C_{\le}=5\) occurs at nine \((M,r)\) slots on
the 5-fold annulus and seven on the 9-fold. Those match Cycle BA’s
even pentuple seeds on full power-of-two windows (only
\(r=17,37,39,79\) survive the \(r\)-bound) together with five
truncated residues. For \(k\ge 4\) there are exactly nine pentuple
packed bits on the 5-fold annulus and exactly seven on the 9-fold
(eight and seven at \(k=3\), before the \(M=4\) family appears),
with times from Green lift. Their firing XOR takes both values, so
they are not identically-1 productions. Not a prize claim: the
Fermat covering remains a prefix.

Helper: `python3 research/cycle_bk.py --certify` (~0.4s). Dump:
`research/cycle_bk.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(H(m)=5\) at \(5,9,15,30\))

The values with \(H(m)\le 5\) for \(1\le m\le 64\) are
\(\{1,2,3,4,5,6,7,9,14,15,30\}\). Cycles BI–BJ already give
\(H\le 4\) on \(\{1,2,3,4,6,7,14\}\). The remaining four have
\(H=5\), with hits \(\{5,6,7,9,10\}\), \(\{9,10,15,17,18\}\),
\(\{15,23,27,29,30\}\), and \(\{30,46,54,58,60\}\). Certified
\(m\le 64\).

## Lemma (full-window even pentuples)

If \(N=W\), the count is Cycle BA’s half-window \(S(a,d)\) with
\(a=M+3\) (5-fold) or \(a=M+4\) (9-fold). Even \(|S|=5\) for
\(a\ge 7\) are \(d=2^a-\{12,16,18,20,26,28,34,50\}\). The smallest
corresponding \(r=2^a-49\) exceeds \(5\cdot 2^M\) for every
\(M\ge 5\) and exceeds \(9\cdot 2^M\) for every \(M\ge 3\). Finite
seeds: no even \(|S|=5\) at \(a=4\); \(\{16,20\}\) at \(a=5\)
(5-fold \(M=2\), \(r=17\) and 9-fold \(M=1\), \(r=17\));
\(\{36,38,44,46,48,52\}\) at \(a=6\) (5-fold \(M=3\), \(r=37,39\)).
At \(a=7\) the only 5-fold survivor is \(r=79\). Certified \(a=4\)
through \(a=8\), and the \(r\)-bound inequality.

## Lemma (truncated windows and \(M<0\))

The \(C_{\le}=5\) scan for \(M\ge 0\) yields exactly
\((M,r)\in\{(1,1),(2,5),(2,7),(2,11),(2,17),(3,15),(3,37),(3,39),(4,79)\}\)
on the 5-fold annulus and
\(\{(1,3),(1,5),(1,7),(1,11),(1,13),(1,17),(2,15)\}\) on the 9-fold.
The \(N=W\) members are the BA survivors above; the rest are
truncated. For \(j>k\), \(r=1\) is unique or double, never a
pentuple. Certified \(q=5\), \(0\le M\le 8\) and \(q=9\),
\(0\le M\le 6\), and \(3\le k\le 7\) for \(M<0\).

## Lemma (exactly nine / seven pentuple-Green bits)

Let \(U=2^k\). Green lift on those \((r,M)\) produces packed bits
\(p=qU+1-r\cdot 2^{k-M}\) and times \(t=qU-2^{k-M}(n+1)\) for the
five \(n\le N\) with \(G(n,r-1)=1\). For \(k\ge 4\) the 5-fold list
has nine bits (the \(M=4\), \(r=79\) family needs \(k\ge 4\)); at
\(k=3\) it has eight. The 9-fold list has seven bits for every
\(k\ge 3\). Certified against a full Green census for \(3\le k\le 7\).

## Extra pentuple bits — killed as forced 1s

On \(3\le k\le 10\) the XOR of the 5-fold pentuple firings takes both
values, as does the XOR of the 9-fold pentuple firings. The 9-fold
XOR agrees with \(\varphi^{(9)}\) through \(k=9\) and disagrees at
\(k=10\); the 5-fold XOR already disagrees with \(\varphi^{(5)}\) at
\(k=3\). **Killed** as identically-1 productions, and as closed forms
for the spines. The odd remainder after
unique, triple, and pentuple bits is septuples and higher odd
multiplicity. The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix
through \(k=15\).

## Verdict

`LEMMA` (\(H(m)=5\) at \(5,9,15,30\); exactly nine pentuple-Green
bits on the 5-fold annulus for \(k\ge 4\), eight at \(k=3\); exactly
seven on the 9-fold, for every \(k\ge 3\)).
`KILLED` (those bits as identically-1 productions, and as closed
forms for \(\varphi^{(5)}\) or \(\varphi^{(9)}\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bk.md` (this note)
- `research/cycle_bk.py`
- `research/cycle_bk.json`
