# Cycle BI: exactly four / three triple-Green bits on the covering annuli

Cycle BH closed the double-Green remainder on the 5-fold and 9-fold
Fermat annuli. The even-target interval \([m,2m]\) has two hits for
\(m\in\{1,2\}\), three for \(m\in\{3,6\}\), and at least four for
every other \(m\ge 4\): for \(m\ge 8\) the second-hit cap lies at or
before \(2m-3\), and exactly one of \(G(2m-2,2m)\), \(G(2m-1,2m)\)
is 1 (they are complementary via \(G(n,n)=1\)). Truncated covering
windows therefore have \(C_{\le}\ge 4\) except two 5-fold \(M=1\)
slots and the three 9-fold \(M=0\) Fermat-odd targets. Full
power-of-two windows have no extra even triples by Cycle AX (the
only surviving seed is 5-fold \(M=2\), \(r=19\)). The surviving
triples are exactly four packed bits on the 5-fold annulus and three
on the 9-fold, for every \(k\ge 3\), with closed times. Their firing
XOR takes both values, so they are not identically-1 productions.
Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bi.py --certify` (~0.4s). Dump:
`research/cycle_bi.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (interval count \(H(m)\))

Write \(H(m)=\#\{n\in[m,2m]:G(n,2m)=1\}\). Cycle BG: the first hit
is \(n=m\) and a second hit \(n_2\) lies in \((m,3m/2+1]\). Cycle BH:
\(G(n,n)=1\), so \(G(2m,2m)=1\). Directly:

- \(H(1)=H(2)=2\) (\(n_2=2m\));
- \(H(3)=3\) with hits \(\{3,5,6\}\);
- \(H(6)=3\) with hits \(\{6,10,12\}\);
- \(H(4)=H(7)=4\) and \(H(5)=5\).

## Lemma (complementary near-diagonal)

For every \(m\ge 8\), \(n_2\le 3m/2+1\le 2m-3\) (for odd \(m\),
\(\lfloor 3m/2+1\rfloor=(3m+1)/2\le 2m-3\) already at \(m=7\)).
Even doubling gives \(G(2m-2,2m)=G(m-1,m)\). Odd doubling and
\(G(m-1,m-1)=1\) give \(G(2m-1,2m)=1\oplus G(m-1,m)\). Hence
exactly one of \(2m-2\), \(2m-1\) is a Green hit, both strictly
after \(n_2\) and strictly before \(2m\). Therefore \(n_3<2m\) and
\(H(m)\ge 4\) for every \(m\ge 8\). Certified \(8\le m\le 64\).

Thus \(H(m)=3\) iff \(m\in\{3,6\}\), and \(H(m)\ge 4\) for every
\(m\ge 4\) except \(m=6\).

## Lemma (truncated windows)

Cycle BH: for \(M\ge 1\), \(d\le n_{\mathrm{cone}}\). On a truncated
window \(N=n_{\mathrm{cone}}\) one has \(N\ge d=2m\), so
\(C_{\le}(N,2m)\ge H(m)\).

- \(m=1\) (\(d=2\), \(r=3\)): \(C_{\le}=3\) iff \(N=5\), which is
  5-fold \(M=1\) only. 9-fold \(M\ge 1\) has \(N\ge 9\).
- \(m=2\) (\(d=4\), \(r=5\)): \(C_{\le}=3\) iff \(N\in\{5,6\}\),
  which is 5-fold \(M=1\) (\(N=6\)) only.
- \(m=3,6\) (\(r=7,13\)): \(C_{\le}=3\) only at \(N=d\). On both
  covering annuli the appearing windows have \(N>d\), so
  \(C_{\le}\ge 4\).
- every other \(m\ge 4\): \(H(m)\ge 4\), hence \(C_{\le}\ge 4\).

So the only truncated triples with \(M\ge 1\) are 5-fold
\((M,r)=(1,3)\) and \((1,5)\). There are none on the 9-fold annulus
for \(M\ge 1\). Certified: \(C_{\le}=3\) scan for \(q=5\),
\(0\le M\le 8\) and \(q=9\), \(0\le M\le 7\).

## Lemma (full-window even triples)

If \(N=W\), the count is Cycle AW/AX’s half-window \(S(a,d)\) with
\(a=M+3\) (5-fold) or \(a=M+4\) (9-fold). Cycle AX: for \(a\ge 5\),
even \(|S|=3\) iff \(d=2^a-\{6,8,10,14\}\), i.e.
\(r=2^a-\{5,7,9,13\}\).

- 5-fold: \(r\le 5\cdot 2^M\). For \(M\ge 3\) even the smallest
  such \(r=2^{M+3}-13\) exceeds \(5\cdot 2^M\). For \(M=2\) the
  only survivor is \(r=19\) (\(d=2^5-14\)).
- 9-fold: \(r\le 9\cdot 2^M\). For \(M\ge 1\) the smallest
  \(r=2^{M+4}-13\) exceeds \(9\cdot 2^M\).

At 5-fold \(M=1\) the level is \(a=4\), outside AX. Finite:
even \(|S(4,D)|=3\) iff \(D\in\{8,10\}\); only \(D=8\) has
\(r=9\le 10\). That is packed bit \(p=2^{k-1}+1\).

The \(r=1\) count \(N+1=3\) never occurs on either covering annulus.

## Lemma (\(M=0\) and \(M<0\))

9-fold \(M=0\): \(C_{\le}=3\) precisely at \(r\in\{5,7,9\}\), packed
bits \(p=4U+1\), \(p=2U+1\), and packed bit 1 (Cycle BF,
\(N(9)=3\)). 5-fold \(M=0\) has no triples (the two doubles and the
unique bit 1). For \(j>k\), \(r=1\) is unique or double (Cycles
BG–BH) and \(r=3\) at \(j=k+1\) is the 9-fold double; no triples.
Certified \(3\le k\le 7\).

## Lemma (exactly four / three triple-Green bits)

Let \(k\ge 3\). The triple-Green packed bits are exactly

- 5-fold: \(\{2^{k-2}+1,\,2^{k-1}+1,\,5\cdot 2^{k-1}+1,\,7\cdot 2^{k-1}+1\}\),
  times \(\{U,9U/4,5U/2\}\), \(\{U,2U,5U/2\}\),
  \(\{2U,5U/2,7U/2\}\), and \(\{2U,7U/2,4U\}\);
- 9-fold: \(\{1,\,2U+1,\,4U+1\}\), times \(\{U,3U,4U\}\),
  \(\{2U,3U,5U\}\), and \(\{3U,4U,6U\}\).

Certified against a full Green census for \(3\le k\le 7\).

## Extra triple bits — killed as forced 1s

On \(3\le k\le 8\) the XOR of the four 5-fold triple firings takes
both values, as does the XOR of the three 9-fold triple firings.
Neither XOR equals \(\varphi^{(5)}\) or \(\varphi^{(9)}\). **Killed**
as identically-1 productions for the covering. The remainder after
unique, double, and triple bits is quadruples and higher
even-multiplicity terms. The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix
through \(k=15\).

## Verdict

`LEMMA` (interval \(H(m)\); complementary near-diagonal;
exactly four triple-Green bits on the 5-fold annulus and exactly
three on the 9-fold, for every \(k\ge 3\)).
`KILLED` (those bits as identically-1 productions).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bi.md` (this note)
- `research/cycle_bi.py`
- `research/cycle_bi.json`
