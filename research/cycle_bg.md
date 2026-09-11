# Cycle BG: exactly three / two unique-Green bits on the covering annuli

Cycle BF produced two Mersenne centre-right unique bits on every
Fermat-odd annulus and left exhaustiveness as a prefix. The even-target
identity \(G(m,2m)=1\), vanishing for \(n<m\), and a second hit in
\((m,3m/2+1]\) (mod-4 / 2-adic cases) force a weight bound on unique even Green windows. That
bound contradicts uniqueness on the 5-fold and 9-fold annuli whenever
\(M=k-j\ge 1\). Combined with the \(r=1\) count, exhaustiveness is a
lemma: exactly three unique-Green packed bits on the 5-fold annulus and
exactly two on the 9-fold, for every \(k\ge 3\). Extra unique bits are
still not identically-1 productions. Not a prize claim: the Fermat
covering remains a prefix.

Helper: `python3 research/cycle_bg.py --certify` (~0.09s). Dump:
`research/cycle_bg.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(C(a,d)=1\))

Write \(C(a,d)=\#\{n<2^a:G(n,d)=1\}\). For \(a\ge 2\),

\[
\{d:C(a,d)=1\}
=\{2s+1:C(a-1,s)=1\}
\cup\{2^{a+1}-4,\,2^{a+1}-2\}.
\]

Odd \(d=2s+1\) reduce by the doubling recurrence. Even unique values are
the two near-maximal degrees: \(G(2^a-1,2^{a+1}-2)=1\) is the diagonal,
and \(2^{a+1}-4\) is the inductive even lift with vanishing xor-count.
Certified \(a\le 8\) against brute \(C\).

## Lemma (diagonal even target)

\(G(m,2m)=1\) for every \(m\ge 0\) (\(\,[x^{2m}](x^2)^m=1\)). If \(n<m\)
then \(2m>2n\), so \(G(n,2m)=0\). Thus the first hit of \(G(\,\cdot\,,2m)\)
is exactly \(n=m\). A second diagonal hit \(G(2m,2m)=1\) lies in a window
of length \(N\) iff \(2m\le N\), i.e. \(d\le N\). Unique even-\(d\) windows
therefore have \(d>N\).

## Lemma (second hit)

For every \(m\ge 1\) there is an \(n\) with \(m<n\le 3m/2+1\) and
\(G(n,2m)=1\). An explicit choice:

- \(m\equiv 0\pmod{4}\): \(n=m+1\). Here \(m=2p\) with \(p\) even, so
  \(G(m,2m-1)=0\) and \(G(p,2p-1)=0\), hence
  \(G(m+1,2m)=1\oplus G(m,2m-2)=1\).
- \(m\equiv 1\pmod{4}\): \(n=m+1\). Write \(m=4k+1\). Even doubling
  yields \(G(m+1,2m)=G(k,2k)=1\).
- \(m\equiv 2\pmod{4}\): \(n=m+2^{v_2(m+2)-1}\). When
  \(v_2(m+2)=2\) this is \(m+2\); when \(m+2=2^a\) it attains the
  bound \(3m/2+1\).
- \(m\equiv 3\pmod{4}\): \(n=m+2^{v_2(m+1)-1}\), the odd shift of the
  previous case.

Certified: the formula's \(n\) lies in the interval, \(G(n,2m)=1\), and
no strictly earlier second hit, for \(1\le m\le 256\). Also the mod-4
identities for \(G(m+1,2m)\) on that range.

## Lemma (weight of a unique even window)

If \(C_{\le}(N,2m)=1\) with \(m\ge 1\), the second hit is \(>N\), so
\(3m/2+1>N\), hence \(6m\ge 4N-2\). Writing \(d=2m\), \(3d\ge 4N-2\).

## Lemma (\(r=1\) unique iff \(j\in\{k+a-1,k+a\}\))

On the \(q\)-fold annulus with \(q=2^a+1\), packed bit
\(p=qU+1-2^j\) has \(G(n,0)\equiv 1\). The surviving count is the length
of \(\{0,\ldots,\min(W,N_{\mathrm{max}}-1)\}\). This equals 1 iff
\(j=k+a-1\) or \(j=k+a\), recovering Cycle BF's two Mersenne
centre-right bits. Certified for \(q\in\{5,9\}\) and \(3\le k\le 7\).

## Lemma (exactly three / two unique-Green bits)

Let \(k\ge 3\). Write \(5U+1-p=r\cdot 2^j\) with \(r\) odd and
\(M=k-j\).

- \(r=1\): unique iff \(j\in\{k+1,k+2\}\), i.e. \(p=3U+1\) and
  \(p=U+1\).
- \(r=5\), \(j=k\): packed bit \(p=1\), unique by Cycle AO/BF
  (\(N(5)=1\)).
- \(M=0\), even \(d=r-1\ge 2\): the only even \(C(2,\,\cdot\,)=1\)
  values in range are \(d=4\), i.e. \(r=5\), already counted.
- \(M\ge 1\), even \(d\ge 2\): the annulus forces
  \(3d\le 4N-4<4N-2\), contradicting the weight lemma. Here
  \(N=\min(2^{M+2}-1,\,(5\cdot 2^M+r-3)/2)\).

Thus the unique-Green 5-fold bits are exactly \(\{1,U+1,3U+1\}\).

The same weight contradiction on the 9-fold annulus
(\(N=\min(2^{M+3}-1,\,(9\cdot 2^M+r-3)/2)\), \(r\le 9\cdot 2^M\))
together with \(r=1\) unique at \(j=k+2,k+3\) yields exactly
\(\{U+1,5U+1\}\). Packed bit 1 is triple (\(N(9)=3\)), not unique.
Certified against a full Green census for \(3\le k\le 7\), and the
annulus inequality for \(1\le M\le 11\).

## Extra unique bits — still killed as forced 1s

Cycle BF: \(\alpha_k=c_U\land r_U\) takes both values, as does
\(c_{3U}\land r_{3U}\). The unique bits are now known completely, but
they are not identically-1 productions for \(\varphi^{(5)}\) or
\(\varphi^{(9)}\). Even-multiplicity hits remain in \(S_{\mathrm{rest}}\).
**Killed** as a covering closed form. The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix through
\(k=15\).

## Verdict

`LEMMA` (\(C(a,d)=1\) even members; second hit for \(G(\,\cdot\,,2m)\);
\(r=1\) unique \(j\); exactly three unique-Green bits on the 5-fold
annulus and exactly two on the 9-fold, for every \(k\ge 3\)).
`KILLED` (those bits as identically-1 productions).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bg.md` (this note)
- `research/cycle_bg.py`
- `research/cycle_bg.json`
