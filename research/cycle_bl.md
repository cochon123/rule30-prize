# Cycle BL: exact unique through pentuple Green bits on the 3-fold annulus

Cycles AP–AR listed four unique-Green bits, one double, five triples,
and four quadruples on the 3-fold Fermat annulus
\([2^k,3\cdot 2^k)\), with closed times but exhaustiveness left as a
prefix. The \(C_{\le}\) / Green-lift count of Cycles BG–BK upgrades
those prefixes to lemmas and adds eight pentuples for every
\(k\ge 5\). Extra bits of those multiplicities are identically 0.
The classified bits are not identically-1 productions, and the XOR of
unique, triple, and pentuple firings is not \(\theta_k=\varphi^{(3)}_k\).
Septuples still grow with \(k\). Not a prize claim: the Fermat
covering remains a prefix.

Helper: `python3 research/cycle_bl.py --certify` (~0.2s). Dump:
`research/cycle_bl.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Setup

Write \(U=2^k\) and factor \(3U+1-p=r\cdot 2^j\) with \(r\) odd,
\(M=k-j\). Green lift (Cycle AR) reduces the hit count on packed bit
\(p\) to \(C_{\le}(N,r-1)\) with \(N=\min(W,n_{\mathrm{cone}})\),
\(W=2^{M+1}-1\), and \(n_{\mathrm{cone}}=(3\cdot 2^M+r-3)/2\). Then
\(N=W\) iff \(r\ge 2^M+1\). For \(M\ge 1\), \(d=r-1\le n_{\mathrm{cone}}\)
always (the largest odd \(r\) is \(3\cdot 2^M-1\)). The full-window
count \(C_{\le}(W,d)\) is Cycle AV’s half-window \(S(M+2,d)\).

## Lemma (exactly four unique-Green bits)

\(C_{\le}=1\) for \(M\ge 0\) occurs only at
\((M,r)\in\{(0,1),(0,3),(1,5)\}\). The remaining unique bit is
\(M=-1\), \(r=1\) (packed bit \(U+1\)). Unique even residues on
\(N=W\) are Cycle BG’s pair \(r=2^{M+2}-3,2^{M+2}-1\), both larger
than \(3\cdot 2^M-1\) for every \(M\ge 2\); the \(M=1\) survivor is
\(r=5\). Truncated windows have \(C_{\le}\ge 3\) for \(m=d/2\ge 3\)
by Cycle BH’s third hit. The \(d=0,2,4\) thresholds leave only the
three \(M\ge 0\) slots above. For \(j>k\) the only in-range bit is
\(r=1\), \(j=k+1\). Thus for every \(k\ge 3\) the unique-Green packed
bits are exactly
\(\{1,\,2^{k-1}+1,\,U+1,\,2U+1\}\),
at times \(U\), \(3U/2\), \(U\), and \(2U\). This upgrades Cycle AP’s
prefix. Certified: \(C_{\le}=1\) scan \(0\le M\le 8\), census
\(3\le k\le 7\), and \(M<0\) for \(3\le k\le 7\).

## Lemma (exactly one double-Green bit)

\(C_{\le}=2\) occurs only at \((M,r)=(1,3)\). Cycle AW: no even
half-window doubles for level \(a=M+2\ge 4\), i.e. \(M\ge 2\).
Truncated windows have \(C_{\le}\ge 3\) for \(m\ge 3\); \(d=2,4\)
have \(C_{\le}=2\) only for \(N\le 4\), which is not a truncated
3-fold window with \(M\ge 1\). No \(M<0\) doubles. The unique double
is \(p=3\cdot 2^{k-1}+1\) at times \(3U/2,2U\), Cycle AQ’s bit,
now exhaustive for every \(k\ge 3\).

## Lemma (exactly five triples and four quads)

\(C_{\le}=3\) occurs at
\((1,1),(2,9),(2,11),(3,19),(3,23)\). Cycle AX: even triples for
\(a\ge 5\) are \(d=2^a-\{6,8,10,14\}\). For \(M\ge 4\) even the
smallest \(r=2^{M+2}-13\) exceeds \(3\cdot 2^M-1\); at \(M=3\) only
\(r=19,23\) survive. The truncated slot is \(r=1\), \(M=1\)
(\(C_{\le}(N,0)=N+1=3\) iff \(N=2\)).

\(C_{\le}=4\) occurs at \((2,3),(2,5),(2,7),(3,15)\). Cycle AZ: no
even quads for \(a\ge 6\), i.e. \(M\ge 4\). The truncated slot is
\((2,3)\) (\(d=2\), \(N=6\), \(C_{\le}=4\)).

These are Cycle AR’s five triples and four quadruples, now
exhaustive for every \(k\ge 3\), with the same Green-lift times.

## Lemma (exactly eight pentuples for \(k\ge 5\))

\(C_{\le}=5\) occurs at
\((3,17),(3,21),(4,37),(4,39),(4,45),(4,47),(5,79),(5,95)\),
all with \(N=W\). Cycle BA: even pentuples for \(a\ge 7\) are
\(d=2^a-\{12,16,18,20,26,28,34,50\}\). For \(M\ge 6\) the smallest
\(r=2^{M+2}-49\) exceeds \(3\cdot 2^M-1\); at \(M=5\) only
\(r=79,95\) survive; at \(M=4\) the \(a=6\) seeds give
\(r=37,39,45,47\); at \(M=3\) the \(a=5\) seeds give \(r=17,21\).
There are no truncated pentuples and no \(M<0\) pentuples. For
\(k\ge 5\) there are exactly eight pentuple packed bits; six at
\(k=4\) and two at \(k=3\), before the \(M=4\) and \(M=5\) families
appear. Times are Green lift:
\(p=3U+1-r\cdot 2^{k-M}\) and \(t=3U-2^{k-M}(n+1)\) for the five
\(n\le N\) with \(G(n,r-1)=1\).

## Extra bits and closed forms — killed

On \(3\le k\le 9\) the XOR of unique, double, triple, quad, and
pentuple firings each takes both values, so none of those families
is an identically-1 production. The XOR of the odd families
(unique, triple, pentuple) disagrees with \(\theta_k\) already at
\(k=4\). Extra unique, double, triple, quad, and pentuple bits are
identically 0 by the lemmas above. Septuple families still grow
with \(k\) (2, 4, 6, 10, 12 on \(k=3..7\)). The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix
through \(k=15\).

## Verdict

`LEMMA` (exactly four unique-Green bits, one double, five triples,
and four quads on the 3-fold annulus for every \(k\ge 3\); exactly
eight pentuples for every \(k\ge 5\)).
`KILLED` (those bits as identically-1 productions, and unique XOR
triple XOR pentuple as a formula for \(\theta_k\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bl.md` (this note)
- `research/cycle_bl.py`
- `research/cycle_bl.json`
