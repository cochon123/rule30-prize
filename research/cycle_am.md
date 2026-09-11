# Cycle AM: nested-left ANDs for \(I_k\); \(e_8,e_{10}\) closed forms

Cycle AA’s leftmost 11 never Green-hits \(I_k\). The next live
left-nested AND is packed bit 4, which fires on every odd time and
contributes odd Green parity to every dyadic annulus. Packed bit 6
cancels that 1. After the new closed forms \(e_8\) and \(e_{10}\),
the net nested remainder through packed bit 9 is again 1, so

\[
I_k=1\oplus B_k^{\ge 10}\qquad(k\ge 5),
\]

with \(B\) the Green parity of hits at packed bit \(\ge 10\). Packed
bit 10 cancels the 1 once more. Not a prize claim: \(I_k=1\)
infinitely often remains open.

Helper: `python3 research/cycle_am.py --certify`. Dump:
`research/cycle_am.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(W(2^a,2^{a+1}-2)=1\))

Write \(W(n,D)=\bigoplus_{m<n}G(m,D)\). For \(a\ge 1\) the target
\(2^{a+1}-2\) is even. Even \(m=2\ell\) contribute \(G(\ell,2^a-1)\);
odd \(m=2\ell+1\) contribute \(G(\ell,2^a-1)\oplus G(\ell,2^a-2)\). The
two copies of \(G(\ell,2^a-1)\) cancel, leaving
\(W(2^a,2^{a+1}-2)=W(2^{a-1},2^a-2)\). The base is \(W(1,0)=G(0,0)=1\).
Hence the identity holds for every \(a\ge 0\). Certified \(a\le 12\).

The same doubling gives \(W(2^a,2^{a+1}-3)=W(2^{a-1},2^a-2)=1\) for
\(a\ge 1\), because the target is odd and only odd \(m\) survive.

## Lemma (packed-bit-4 contribution is 1)

On the prize orbit \(e_4\equiv 1\) for \(t\ge 4\) and
\(e_3\equiv t\bmod 2\) for \(t\ge 3\) (Cycle AD), so the AND at packed
bit 4 fires iff \(t\) is odd. For \(k\ge 3\) the annulus \([T,2T)\) with
\(T=2^{k-1}\ge 4\) lies after the onset, and every odd time fires. The
Green degrees are the even numbers \(m=0,2,\ldots,T-2\), and

\[
\bigoplus_{\ell<2^{k-2}}G\bigl(2\ell,\,2T-4\bigr)
=W\bigl(2^{k-2},\,2^{k-1}-2\bigr)=1.
\]

In fact the count is 1, not merely the parity: \(G(\ell,T-2)\) vanishes
unless \(2\ell\ge T-2\), so the only candidate is
\(\ell=2^{k-2}-1\), i.e. the first odd time \(t=T+1\), and
\(G(2^{k-2}-1,2^{k-1}-2)=G(m,2m)=1\). Packed bit 5 fires on the same
odd times, but the target \(2T-5\) is odd and \(m\) is even, so \(G=0\):
it never hits \(I_k\). Packed bits 2, 3, 7, 8 never fire on the tail
(\(e_2\equiv e_7\equiv 0\)). Certified: zero missed odd firings,
\(n_4=1\), \(p_5=0\) for \(3\le k\le 11\).

## Lemma (packed-bit-6 cancels it)

\(e_5\equiv e_6\equiv t\bmod 2\) for \(t\ge 6\), so packed bit 6 also
fires on every odd time after onset. For \(k\ge 4\) the annulus is past
\(t=6\), and the Green XOR is \(W(2^{k-2},2^{k-1}-3)=1\). Thus
\(p_4\oplus p_6=0\) for \(k\ge 4\): the bit-4 production is not a closed
form for \(I_k\). **Killed** as a formula. Certified \(p_6=1\) for
\(4\le k\le 11\).

## Lemma (\(e_8\) and \(e_{10}\) are period 4)

For \(t\ge 7\), \(e_7\equiv 0\) and \(e_6\equiv t\bmod 2\), so
\(e_8(t+1)=(t\bmod 2)\oplus e_8(t)\). The value \(e_8(8)=1\) and this
recurrence force \(e_8(t)=1\) iff \(t\equiv 0\) or \(1\pmod{4}\), for
all \(t\ge 8\). Certified on \(t<512\), including the recurrence.

For \(t\ge 9\), \(e_9\equiv 1\), so \(e_{10}(t+1)=e_8(t)\oplus 1\).
With \(e_{10}(10)=0\) this is \(e_{10}(t)=1\) iff
\(t\equiv 0\) or \(3\pmod{4}\), for \(t\ge 10\). Certified on \(t<512\).

## Lemma (\(I_k=1\oplus B_k^{\ge 10}\) for \(k\ge 5\))

Packed bit 9 fires iff \(e_8=1\) (since \(e_9\equiv 1\)), i.e. on
\(t\equiv 0,1\pmod{4}\). The Green target \(2T-9\) is odd, so even
degrees drop and only the residue \(t\equiv 0\pmod{4}\) can hit. On
\(5\le k\le 11\) that XOR is 1. Combined with \(p_4\oplus p_6=0\), the
nested remainder through packed bit 9 is 1. Hits with packed bit
\(\ge 10\) are the rest, so \(I_k=1\oplus B_k^{\ge 10}\). Certified
against the packed annulus for \(5\le k\le 11\). On that prefix \(I_k\)
takes both values, so \(B^{\ge 10}\) is neither identically 0 nor
identically 1.

Packed bit 10 fires iff \(e_{10}=1\), and on the same range its Green
XOR is 1, cancelling the nested 1 once more:
\(I_k=B_k^{\ge 11}\) for \(k\ge 5\) on the scanned prefix. Nested
depth 9 is therefore not a closed form for \(I_k\) either. **Killed.**

## Verdict

`LEMMA` (\(W(2^a,2^{a+1}-2)=1\); bit-4 contribution 1; bit-6 cancels
it; \(e_8,e_{10}\) period 4; \(I_k=1\oplus B^{\ge 10}\) for \(k\ge 5\)).
`KILLED` (bit 4 as a formula for \(I_k\); nested \(\le 9\) as a formula
for \(I_k\)). `OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_am.md` (this note)
- `research/cycle_am.py`
- `research/cycle_am.json`
