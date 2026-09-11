# Cycle BH: exactly two / three double-Green bits on the covering annuli

Cycle BG closed the unique-Green remainder on the 5-fold and 9-fold
Fermat annuli. The even-multiplicity remainder starts at multiplicity
2. Green lift reduces that count to \(C_{\le}(N,r-1)\) with even
target \(r-1\). The diagonal \(G(m,2m)=1\), a third hit at most
\(2m\) for \(m\ge 3\), Cycle AW’s absence of even half-window
doubles, and the cone inequality \(d\le n_{\mathrm{cone}}\) leave no
\(C_{\le}=2\) slots for \(M=k-j\ge 1\). The surviving doubles are
exactly two packed bits on the 5-fold annulus and three on the
9-fold, for every \(k\ge 3\), with closed times. Their firing XOR
takes both values, so they are not identically-1 productions. Not a
prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bh.py --certify` (~0.4s). Dump:
`research/cycle_bh.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(G(n,n)=1\))

\(G(0,0)=1\). Even doubling gives \(G(2k,2k)=G(k,k)\). Odd doubling
gives \(G(2k+1,2k+1)=G(k,k)\). Hence \(G(n,n)=1\) for every
\(n\ge 0\). In particular \(G(m,2m)=1\) (Cycle BG) is the diagonal
case of this identity after even doubling. Certified \(n\le 128\).

## Lemma (third hit)

Cycle BG: the first hit of \(G(\,\cdot\,,2m)\) is \(n=m\), and a
second hit \(n_2\) lies in \((m,3m/2+1]\). For \(m\ge 3\) one has
\(3m/2+1<2m\), so \(n_2<2m\). Combined with \(G(2m,2m)=1\), there is
a Green hit at \(2m\) strictly after \(n_2\), hence a third hit
\(n_3\le 2m\). Certified: \(n_2<2m\) and \(G(2m,2m)=1\) for
\(3\le m\le 128\). The cases \(m=1,2\) are the only exceptions
(\(n_2=2m\)); they are \(d=2\) and \(d=4\), handled by a direct
count below.

## Lemma (cone dominates the target for \(M\ge 1\))

On the \(q\)-fold annulus write \(qU+1-p=r\cdot 2^j\) with \(r\) odd
and \(M=k-j\). For \(j\ge 1\) Green lift (Cycle AR) reduces the hit
count to \(C_{\le}(N,r-1)\) with
\(N=\min(W,n_{\mathrm{cone}})\),
\(W=2^{M+a}-1\) (\(a=2\) if \(q=5\), \(a=3\) if \(q=9\)), and
\(n_{\mathrm{cone}}=(q\cdot 2^M+r-3)/2\). For \(M\ge 1\),
\(q\cdot 2^M\) is even, so the displayed \(n_{\mathrm{cone}}\) is
exact (no floor). Then \(d=r-1>n_{\mathrm{cone}}\) iff
\(r>q\cdot 2^M-1\). The largest odd \(r\) is \(q\cdot 2^M-1\), so
\(d\le n_{\mathrm{cone}}\) always, with equality at that maximal
\(r\). Certified \(1\le M\le 11\).

## Lemma (no doubles for \(M\ge 1\))

Let \(M\ge 1\) and \(d=r-1\ge 2\).

- If \(N=n_{\mathrm{cone}}\), the previous lemma gives \(d\le N\).
  For \(m=d/2\ge 3\) the third-hit lemma yields \(n_3\le 2m=d\le N\),
  so \(C_{\le}\ge 3\). The remaining targets \(d=2,4\) have
  \(n_3\in\{5,5\}\) and \(N\ge 5\) on both covering annuli
  (\(q\ge 5\), \(M\ge 1\)).
- If \(N=W=2^{M+a}-1\), the count is the half-window
  \(S(M+a+1,d)\) of Cycle AW. For \(q=5\) one has \(a=2\), so the
  level is \(M+3\ge 4\); for \(q=9\), \(a=3\) and the level is
  \(M+4\ge 5\). Cycle AW: there are no even half-window doubles for
  level \(\ge 4\). (The scanned even degrees cover every \(r\le q\cdot 2^M\).)

The \(r=1\) count \(C_{\le}(N,0)=N+1\) equals 2 iff \(N=1\), which
does not occur for \(M\ge 1\). Thus there are no double-Green bits
with \(M\ge 1\). Certified: \(C_{\le}=2\) scan empty for
\(q=5\), \(1\le M\le 8\) and \(q=9\), \(1\le M\le 7\).

## Lemma (\(M=0\) classification)

Here \(j=k\) and \(r\le q\), a finite check independent of \(k\).

- 5-fold: \(C_{\le}=2\) precisely at \((r,N,d)=(1,1,0)\) and
  \((3,2,2)\). These are packed bits \(p=4U+1\) (times \(t=3U,4U\))
  and \(p=2U+1\) (times \(t=2U,3U\)). At \(t=2U\) the latter is the
  centre-right AND \(c_{2U}\land r_{2U}=\alpha_{k+1}\); at \(t=4U\)
  the former is \(c_{4U}\land r_{4U}\). The remaining odd \(r=5\) is
  packed bit 1, unique (\(N(5)=1\)).
- 9-fold: \(C_{\le}=2\) precisely at \((r,N,d)=(3,4,2)\), packed bit
  \(p=6U+1\) (times \(t=6U,7U\)). Packed bit 1 (\(r=9\)) is triple;
  \(r=1\) has count \(4\); \(r=5,7\) have count at least 3.

Certified against \(C_{\le}\) and against a full Green census for
\(3\le k\le 7\).

## Lemma (\(M<0\): only two 9-fold extras)

For \(j>k\) one has \(r\cdot 2^{j-k}\le q\).

- 5-fold: only \(r=1\), and Cycle BG already makes those unique
  (\(j=k+1,k+2\)).
- 9-fold: \(r=1\) is double precisely at \(j=k+1\) (packed bit
  \(p=7U+1\), times \(t=5U,7U\)); unique at \(j=k+2,k+3\). The
  residue \(r=3\) at \(j=k+1\) is double (packed bit \(p=3U+1\),
  times \(t=3U,5U\)); \(r\ge 5\) is off-range.

Certified for \(3\le k\le 7\).

## Lemma (exactly two / three double-Green bits)

Let \(k\ge 3\). The double-Green packed bits are exactly

- 5-fold: \(\{2U+1,\,4U+1\}\), times \(\{2U,3U\}\) and
  \(\{3U,4U\}\);
- 9-fold: \(\{3U+1,\,6U+1,\,7U+1\}\), times \(\{3U,5U\}\),
  \(\{6U,7U\}\), and \(\{5U,7U\}\).

## Extra double bits — killed as forced 1s

On \(3\le k\le 8\) the XOR of the two 5-fold double firings takes
both values, as does the XOR of the three 9-fold double firings.
Neither XOR equals the corresponding Fermat spine
\(\varphi^{(5)}\) or \(\varphi^{(9)}\). **Killed** as identically-1
productions for the covering. The remainder after unique and double
bits is triples and higher even-multiplicity terms. The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix
through \(k=15\).

## Verdict

`LEMMA` (\(G(n,n)=1\); third hit \(n_3\le 2m\) for \(m\ge 3\);
cone dominates \(d\) for \(M\ge 1\); exactly two double-Green bits
on the 5-fold annulus and exactly three on the 9-fold, for every
\(k\ge 3\)).
`KILLED` (those bits as identically-1 productions).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bh.md` (this note)
- `research/cycle_bh.py`
- `research/cycle_bh.json`
