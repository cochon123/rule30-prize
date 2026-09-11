# Cycle AK: Fermat-odd spines; leftmost-11 parity is odd

Cycle AJ is the \(q=3\) case of a family indexed by \(q=2^a+1\).
Every such spine differs from \((c_{2^k})\) by a Green remainder on
\([2^k,q\cdot 2^k)\), and eventual period \(2^m\) forces all of them
to vanish. The XOR of leftmost-11 Green hits on that interval is
identically 1, by a doubling argument on \(G\) that does not use the
prize orbit. Not a prize claim: some \(\varphi^{(q)}_k=1\) infinitely
often is unproved.

Helper: `python3 research/cycle_ak.py --certify`. Dump:
`research/cycle_ak.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Fermat-odd identity)

Let \(U=2^k\) and \(q=2^a+1\) with \(a\ge 1\). Cycle AI from time
\(U\) by step \(2^{k+a}=(q-1)U\) has both extras at spatial offset
\(\pm(q-1)U\), strictly outside the light cone. Hence

\[
c_{qU}=c_U\oplus J^{(q)}_k,
\qquad
\varphi^{(q)}_k:=c_{qU}\oplus c_U=J^{(q)}_k,
\]

where \(J^{(q)}_k\) is the Green parity of AND injections on
\([U,qU)\) targeting packed bit \(qU\). Cycle AJ is \(a=1\) (\(q=3\)).
Certified for \(q=3,5,9\) and \(k\le 7\).

## Lemma (period \(2^m\) forces every \(\varphi^{(q)}=0\))

If \(c\) is eventually period \(2^m\), then for all large \(k\) and
every odd \(q\), both \(U\) and \(qU\) are multiples of \(2^m\), so
\(\varphi^{(q)}_k=0\). In particular this holds for every Fermat-odd
\(q=2^a+1\). Certified on synthetic periods \(2^m\) (\(m\le 4\), onset
5) for \(q\in\{3,5,9,17\}\). Infinitely many \(k\) with some
\(\varphi^{(q)}_k=1\) would therefore kill every eventual period
\(2^m\).

## Lemma (leftmost-11 hit parity is odd)

Packed bit 1 fires at every time \(s\ge 1\) (Cycle AA). It Green-hits
the target \(qU\) at time \(s\) iff \(G(qU-s-1,qU-1)=1\). As \(s\)
runs through \([U,qU)\), the degree \(m=qU-s-1\) runs through
\(\{0,1,\ldots,2^{k+a}-1\}\), and \(qU-1=2^{k+a}+2^k-1\). The parity
of hits is therefore

\[
\bigoplus_{m=0}^{2^n-1}G\bigl(m,\,2^n+2^{n-a}-1\bigr),\qquad n=k+a.
\]

This equals 1 for every \(a\ge 1\) and \(n\ge a\). Proof:

1. \(\bigoplus_{m<2^b}G(m,2^b-1)=1\) for all \(b\ge 0\). The target is
   odd, so even \(m\) contribute 0; odd \(m=2\ell+1\) give
   \(G(\ell,2^{b-1}-1)\), which is the same claim at \(b-1\). Base
   \(G(0,0)=1\).
2. For the diagonal \(n=a\), the target is \(2^a\). Splitting even/odd
   \(m\) and using the doubling of \(G\) reduces the XOR to
   \(\bigoplus_{\ell<2^{a-1}}G(\ell,2^{a-1}-1)=1\) by (1).
3. For \(n>a\) the target is odd, so only odd \(m\) contribute, and
   the XOR equals the same claim at \(n-1\).

Hence \(\varphi^{(q)}_k=1\oplus S^{(q)}_k\) for every Fermat-odd
\(q\), where \(S^{(q)}_k\) is the Green parity of hits with packed
bit \(\neq 1\). Certified: both XOR identities for \(a\le 4\) and
\(n\le a+6\); on the prize orbit the packed-bit-1 hit parity is 1
for \(q=3,5,9\) and \(k\le 7\).

The single-time evaluation at \(s=U\) is \(G(2^{k+a}-1,qU-1)\), which
equals \(a\bmod 2\) by the same odd doubling (Cycle AJ is \(a=1\)).
For even \(a\) (e.g. \(q=5\)) the time-\(U\) 11 does not hit; the odd
parity comes from later times in the interval. On the scanned range
the number of \(p=1\) hits is constant in \(k\): \(1,1,3,5\) for
\(a=1,2,3,4\).

## \(S^{(q)}\equiv 0\) — killed

If \(S^{(q)}\) vanished then \(\varphi^{(q)}\equiv 1\), already
killing every period \(2^m\). For \(q=3,5,9\) on \(k\le 7\) each
\(\varphi\) takes both values. **Killed.** On that prefix, from
\(k=2\) through \(k=10\) at least one of \(\varphi^{(3)},\varphi^{(5)},
\varphi^{(9)}\) is 1 (the only all-zero times are \(k=0,1\)). That is
finite evidence, not a proof that the vector
\((\varphi^{(q)}_k)_q\) is not eventually 0.

## Verdict

`LEMMA` (Fermat-odd identity; period \(2^m\) forces every
\(\varphi^{(q)}=0\); leftmost-11 hit parity odd, so
\(\varphi=1\oplus S\)). `KILLED` (\(S\equiv 0\)). `OPEN` (some
\(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ak.md` (this note)
- `research/cycle_ak.py`
- `research/cycle_ak.json`
