# Cycle BU: defect chaining; small-degree Green sums vanish

For a power-of-two step \(M=2^a\) with \(2M>t\), the freshman extras
at spatial \(\pm 2M\) and \(\pm 3M\) lie outside the seed cone. The
palindrome defect therefore chains:

\[
d^{(a+1)}_{t+M}
=d^{(a)}_t
\oplus J_{[t,\,t+M)\to t-M}
\oplus J_{[t,\,t+M)\to t+3M}.
\]

On covering block \(B\) one has \(8U>6U\), so
\(d_C=d_B\oplus J_B^{\to 2U}\oplus J_B^{\to 18U}\). Those three Green
parities live on disjoint packed-bit ranges. The unweighted sum
\(S(2^a,d):=\bigoplus_{m<2^a}G(m,d)\) vanishes for every
\(d<2^{a-1}\), so the always-firing packed-bit-1 slice of the left
extra is 0. The fire-weighted \(J_B^{\to 2U}\) itself vanishes on a
prefix. Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bu.py --certify` (~0.3s). Dump:
`research/cycle_bu.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(S(2^a,d)=0\) for small \(d\))

Write \(S(N,d):=\bigoplus_{m<N}G(m,d)\). Even doubling gives
\(S(2M,2j)=S(M,j-1)\) and \(S(2M,2j+1)=S(M,j)\), with the convention
\(S(M,-1)=0\) and \(S(1,0)=1\). Iterating from \(N=2^a\) down to
\(S(1,\cdot)\), every target \(0\le d<2^{a-1}\) reduces to a negative
index or to \(S(1,d')\) with \(d'\ne 0\), hence \(S(2^a,d)=0\).
Certified: the recurrences against brute \(G\)-sums for \(M\le 24\);
the closed reduction against brute sums for \(a\le 8\); vanishing
for \(a\le 16\) and all \(d<2^{a-1}\).

On block \(B\) targeting packed bit \(2U\) at time \(10U\), the
unweighted Green count in \(s\in[0,4U)\) is exactly
\(S(4U,2U-p)\). For every \(p\in[1,2U]\) one has \(0\le 2U-p<2U\),
so that count is even. Packed bit 1 always fires (Cycle AA), and
this slice contributes 0 to \(J_B^{\to 2U}\). Fire-weighted
cancellation for \(p\ge 2\) is not included.

## Lemma (defect chaining)

Let \(M=2^a\) and \(2M>t\ge 0\). Freshman expansion of packed bit
\(t-M\) (resp. \(t+3M\)) after \(M\) steps pulls only the live cell
\(x(t,-M)\) (resp. \(x(t,M)\)), because \(|-2M|=|-3M|=2M,3M>t\).
Adding the Green AND remainders yields the displayed identity.
Certified for \(0\le t\le 24\) and \(0\le a\le 6\) with \(2M>t\)
(97 identities, zero failures).

## Lemma (\(d_C\) chains through \(B\))

Take \(t=6U\) and \(M=4U\). Then \(2M=8U>6U\) for every \(k\ge 1\),
the left extra is packed bit \(2U\), and the right extra is packed
bit \(18U\). Hence

\[
d_C=d_B\oplus J_B^{\to 2U}\oplus J_B^{\to 18U}.
\]

Certified \(1\le k\le 6\).

## Lemma (disjoint supports on \(B\))

On \(t=6U+s\) with \(s\in[0,4U)\):

- target \(2U\): \(p\le 2U\);
- target \(10U\): \(2U+2+2s\le p\le 10U\) (Cycle BR);
- target \(18U\): \(p\ge 10U+2+2s\).

The three ranges are pairwise disjoint (gaps at packed bits
\(2U+1\) and \(10U+1\)). Certified as inequalities for \(k\le 12\),
and by a Green scan of actual hits for \(1\le k\le 6\).

## Prefix (\(J_B^{\to 2U}=0\))

Freshman gives \(x(10U,-8U)=x(6U,-4U)\oplus J_B^{\to 2U}\), so the
left extra is invariant on \(B\) iff \(J_B^{\to 2U}=0\). The two
cells agree for \(1\le k\le 12\). **PREFIX**, not a theorem. Under
that prefix one has \(d_C=d_B\oplus J_B^{\to 18U}\).

## \(J_B^{\to 18U}\equiv 0\) and \(d_C\equiv d_B\) — killed

On \(1\le k\le 6\) the right extra Green parity is
`011101`, both values. Then \(d_C=d_B\) already fails at \(k=2\).
**Killed.** Covering still fails iff \(J_A=0\), \(J_B=d_B\), and
\(J_C=d_B\oplus J_B^{\to 2U}\oplus J_B^{\to 18U}\).

## Verdict

`LEMMA` (\(S(2^a,d)=0\) for \(d<2^{a-1}\); defect chaining when
\(2M>t\); \(d_C=d_B\oplus J_B^{\to 2U}\oplus J_B^{\to 18U}\);
disjoint supports on \(B\)).
`PREFIX` (\(J_B^{\to 2U}=0\); Fermat covering for all \(k\ge 2\)).
`KILLED` (\(J_B^{\to 18U}\equiv 0\); \(d_C\equiv d_B\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bu.md` (this note)
- `research/cycle_bu.py`
- `research/cycle_bu.json`
