# Cycle AV: unique half-window \(G\)-supports are the AS families

Cycle AS listed \(2k-2\) unique-Green packed bits for \(I_k\) as a
prefix. The doubling recurrence of \(G\), with Cycle AN’s interval
for \(W(2^{a-1},D)\), makes that list exhaustive: the only
half-window singletons are the \(2\)-family and \(3\)-family targets.
Packed bits \(13\) and \(17\) then contribute \(0\) by the period-4
tails of \(e_{13},\ldots,e_{17}\). The remaining unique \(3\)-family
is not identically \(0\), and the right-half double \(p=3T/2+1\) does
not have XOR \(0\). Not a prize claim: \(I_k=1\) infinitely often
remains open.

Helper: `python3 research/cycle_av.py --certify` (~8s). Dump:
`research/cycle_av.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (odd doubling)

For odd targets, \(G(2\ell+1,2d+1)=G(\ell,d)\) and even \(n\) vanish.
Thus if \(S(a,D)=\{n<2^{a-1}:G(n,D)=1\}\),

\[
S(a,2d+1)=\{2\ell+1:\ell\in S(a-1,d)\}.
\]

In particular \(|S(a,2d+1)|=|S(a-1,d)|\), so an odd target is unique
in the half-window if and only if its halved target is unique one
level down. Certified \(a\le 12\).

## Lemma (even count)

For even targets \(E=2e\), write \(A=S(b-1,e)\) and
\(B=S(b-1,e-1)\) (with \(B=\emptyset\) if \(e=0\)). Even \(n=2\ell\)
hit iff \(\ell\in A\); odd \(n=2\ell+1\) hit iff \(\ell\in A\,\triangle\,B\).
Hence

\[
|S(b,2e)|
=|B|+2|A\setminus B|.
\]

This is \(1\) if and only if \(|B|=1\) and \(A\subseteq B\): either
\(A=\emptyset\) and \(B\) a singleton, or \(A=B\) a singleton.
Certified \(b\le 10\).

## Lemma (unique even targets are \(2^b-2\) and \(2^b-4\))

For \(b=2\), the only unique even target is \(2^b-2=2\). For
\(b\ge 3\), the only unique even targets on \(n<2^{b-1}\) are
\(2^b-2\) and \(2^b-4\).

Cycle AN gives \(W(2^{c},D)=1\) iff \(2^{c}-1\le D\le 2^{c+1}-2\).
A singleton has odd multiplicity, so every unique \(D\) at level \(c\)
lies in that interval. Inductively, unique targets at level \(b-1\)
are exactly Cycle AS’s two families (the next lemma). Then
\(|B|=1\) forces \(e-1\) unique at level \(b-1\), hence
\(e\in[2^{b-2},2^{b-1}-1]\).

- If \(A=\emptyset\), then \(e\) is outside the \(W=1\) interval at
  level \(b-1\). The only remaining value in range is
  \(e=2^{b-1}-1\), i.e. \(E=2^b-2\). Here \(A=S(b-1,2^{b-1}-1)\) is
  empty by Cycle AP (Mersenne: \(2^{b-1}\nmid(n+1)\) for
  \(n<2^{b-2}\)), and \(B=S(b-1,2^{b-1}-2)\) is a singleton by Cycle
  AS. This is the \(G(n,2^b-2)\) law.
- If \(A=B\) a singleton, then \(e\) and \(e-1\) are consecutive
  unique targets at level \(b-1\) with the same support. Among the
  two families the only such pair is \((2^{b-1}-3,2^{b-1}-2)\), both
  supported at \(n=2^{b-2}-1\). That pair is \(e=2^{b-1}-2\), i.e.
  \(E=2^b-4\), the \(G(n,2^b-4)\) law. The   \(2\)-family all share
  support \(\{2^{c-1}-1\}\); the \(3\)-family have distinct supports
  \(\{2^{c-1}-1-2^j\}\). Consecutive family targets with difference
  \(1\) occur only in the cluster \(\{2^{c}-5,\ldots,2^{c}-2\}\), and
  the only equal-support consecutive pair there is
  \((2^{c}-3,2^{c}-2)\).

Certified \(b\le 12\).

## Lemma (unique \(D\) are exactly the AS families)

For \(a\ge 2\), \(|S(a,D)|=1\) if and only if

\[
D=2^a-2^j-1\qquad(0\le j<a)
\]

or

\[
D=2^a-3\cdot 2^j-1\qquad(0\le j\le a-3).
\]

Base \(a=2\) is the two \(2\)-family targets \(D=1,2\). Odd unique
targets at level \(a\) are \(2d+1\) with \(d\) unique at \(a-1\),
which by induction are the \(2\)-family with \(j\ge 1\) and the
\(3\)-family with \(j\ge 1\). Even unique targets are
\(2^a-2\) and \(2^a-4\) (the \(j=0\) members). Every \(2\)-family
target has unique \(n=2^{a-1}-1\); every unique \(3\)-family target
has unique \(n=2^{a-1}-1-2^j\). The only same-support consecutive
unique pair is \((2^a-3,2^a-2)\). Certified \(a\le 12\).

## Lemma (unique-Green bits for \(I_k\))

Let \(T=2^{k-1}\) and \(k\ge 2\). Packed bit \(p\) is unique-Green on
the dyadic annulus iff \(p=2^j+1\) for \(j=0,\ldots,k-1\) (time
\(t=T\)) or \(p=3\cdot 2^j+1\) for \(j=0,\ldots,k-3\) (time
\(t=T+2^j\)). There are exactly \(2k-2\) such bits. Cone holds as in
Cycle AS. This upgrades Cycle AS’s prefix to a theorem. (Exactly two
double-Green bits remains a prefix: even multiplicity is a different
count.) Certified on the annulus for \(4\le k\le 8\).

## Lemma (\(e_{13}\) through \(e_{17}\) are period 4)

The left-diagonal recurrence is
\(e_j(t+1)=e_{j-2}(t)\oplus(e_{j-1}(t)\lor e_j(t))\) (Cycle AC).
Cycle AU supplies \(e_{11}(t)=1\) iff \(t\equiv 2\pmod{4}\) and
\(e_{12}(t)=1\) iff \(t\not\equiv 0\pmod{4}\). The following tails
are invariant under the recurrence and hold from onset \(t=j\)
(\(e_{17}\) from \(t=16\)):

| \(j\) | \(e_j(t)=1\) iff |
| ---: | --- |
| \(13\) | \(t\not\equiv 3\pmod{4}\) |
| \(14\) | \(t\equiv 0,1\pmod{4}\) |
| \(15\) | \(t\equiv 0,3\pmod{4}\) |
| \(16\) | \(t\not\equiv 1\pmod{4}\) |
| \(17\) | \(t\equiv 3\pmod{4}\) |

Certified on \(t<256\), including the recurrences.

## Lemma (bits 13 and 17 contribute 0)

For \(k\ge 5\), \(T=2^{k-1}\) is divisible by \(16\). Packed bit
\(13=3\cdot 2^2+1\) is unique-Green at \(t=T+4\equiv 0\pmod{4}\).
The AND is \(e_{13}\land e_{12}\); \(e_{12}\) vanishes on residue
\(0\), so the contribution is \(0\). Packed bit \(17=2^4+1\) is
unique-Green at \(t=T\equiv 0\pmod{4}\). The AND is
\(e_{17}\land e_{16}\); \(e_{17}\) vanishes on residue \(0\), so
the contribution is \(0\). Certified \(5\le k\le 12\). These are
the \(j=2\) member of the \(3\)-family and the \(j=4\) member of
the \(2\)-family. They are not a nested-left formula for \(I_k\).

## Unique \(3\)-family \(p\ge 13\) identically 0 — killed

Bits \(13,25,49,\ldots\) contribute \(0\) through \(k=14\), but at
\(k=15\) the largest unique member \(j=k-3=12\), packed bit
\(p=3\cdot 2^{12}+1=12289\) at time \(t=T+2^{12}=20480\), fires.
**Killed.** The live unique \(3\)-family starts at \(p=25\).

## Double \(p=3T/2+1\) has XOR 0 — killed

The two Green times are \(t=T\) (mid-cone) and \(t=3T/2\)
(centre-right). Their fires agree through \(k=11\), but at \(k=12\)
they are \(0,1\). **Killed.** Exactly two doubles remains a prefix.

## Nested left — still not a formula for \(I_k\)

Cycle AU gave \(I_k=1\oplus B_k^{\ge 13}\) for \(k\ge 5\). Bits 13
and 17 contribute \(0\), so the identity still has a bulk of packed
bits \(\ge 14\) together with the scaling unique \(2\)-family
\(j\ge 5\) (\(p=33,65,\ldots,T+1\)) and unique \(3\)-family
\(j\ge 3\) (\(p=25,\ldots,3T/8+1\)). **Killed** as a closed form, as
in Cycles AM and AU. Do not hunt another finite nested-left family.

## Verdict

`LEMMA` (unique even targets \(2^b-2,2^b-4\); unique \(D\) are the
AS families; exactly \(2k-2\) unique-Green bits for \(I_k\);
\(e_{13},\ldots,e_{17}\) period 4; bits 13 and 17 contribute \(0\)).
`PREFIX` (exactly two double-Green bits).
`KILLED` (unique \(3\)-family \(p\ge 13\) identically \(0\); double
\(p=3T/2+1\) XOR \(0\); nested left as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_av.md` (this note)
- `research/cycle_av.py`
- `research/cycle_av.json`
