# Cycle AU: Fermat-subtract \(G\); \(e_{11},e_{12}\); \(I_k=1\oplus B^{\ge 13}\)

Cycle AM proved \(I_k=1\oplus B_k^{\ge 10}\) for \(k\ge 5\), and that
packed bit 10 has odd Green parity on a prefix. The half-window laws
for \(2^a-5,6,7,10,12\) make bits 10–12 explicit. With the period-4
tails of \(e_{11}\) and \(e_{12}\), those three contributions are
\(1,0,1\), so \(I_k=1\oplus B_k^{\ge 13}\). Nested depth 12 is not a
closed form. Not a prize claim: \(I_k=1\) infinitely often remains
open.

Helper: `python3 research/cycle_au.py --certify` (~0.02s). Dump:
`research/cycle_au.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Fermat-subtract)

For \(1\le c<a\) and \(n<2^{a-1}\),

\[
G(n,2^a-2^c-1)=1 \quad\text{iff}\quad n=2^{a-1}-1.
\]

The target is \((2^{a-c}-1)2^c-1\). Cycle AR’s lift requires
\(2^c\mid(n+1)\) and \(G((n+1)/2^c-1,2^{a-c}-2)=1\). In the
half-window the second factor is Cycle AS’s unique all-ones argument,
forcing \(n=2^{a-1}-1\). Cases \(c=1,2\) are \(G(n,2^a-3)\) (Cycle AS)
and \(G(n,2^a-5)\). Certified \(a\le 12\).

## Lemma (derived half-windows)

Doubling from the previous lemma and Cycle AS yields, for
\(n<2^{a-1}\):

| target | \(a\ge\) | \(s=2^{a-1}-1-n\) |
| --- | ---: | --- |
| \(2^a-6\) | 4 | \(\{0,1,2\}\) |
| \(2^a-7\) | 4 | \(\{2\}\) |
| \(2^a-10\) | 5 | \(\{1,2,4\}\) |
| \(2^a-12\) | 5 | \(\{0,1,2,3,5\}\) |

Certified \(a\le 12\). On the dyadic annulus packed bit \(p\) with
these targets (no extra lift) Green-hits at times \(t=T+s\).

## Lemma (\(e_{11}\) and \(e_{12}\) are period 4)

The left-diagonal recurrence is
\(e_j(t+1)=e_{j-2}(t)\oplus(e_{j-1}(t)\lor e_j(t))\) (Cycle AC). For
\(t\ge 9\), \(e_9\equiv 1\), so
\(e_{11}(t+1)=1\oplus(e_{10}(t)\lor e_{11}(t))\). With Cycle AM’s
\(e_{10}(t)=1\) iff \(t\equiv 0,3\pmod{4}\) and \(e_{11}(14)=1\), the
tail is \(e_{11}(t)=1\) iff \(t\equiv 2\pmod{4}\), for \(t\ge 11\).

Then \(e_{12}(t+1)=e_{10}(t)\oplus(e_{11}(t)\lor e_{12}(t))\). The
state \((0,1,1,1)\) on residues \(0,1,2,3\) is invariant, and holds
from \(t=12\): \(e_{12}(t)=1\) iff \(t\not\equiv 0\pmod{4}\), for
\(t\ge 12\). Certified on \(t<256\), including the recurrences.

## Lemma (bits 10, 11, 12)

Let \(T=2^{k-1}\) with \(k\ge 5\), so \(T\ge 16\) is past those onsets.

- Packed bit 10 has times \(T+1,T+2,T+4\). The AND is \(e_{10}\land e_9\);
  only \(t=T+4\equiv 0\pmod{4}\) fires. Contribution \(1\).
- Packed bit 11 has times \(T,T+2,T+4\). The AND is \(e_{11}\land e_{10}\),
  which is identically 0 on the tail (residues \(2\) and \(\{0,3\}\)
  are disjoint). Contribution \(0\).
- Packed bit 12 has times \(T+s\) for \(s\in\{0,1,2,3,5\}\). The AND
  \(e_{12}\land e_{11}\) fires iff \(t\equiv 2\pmod{4}\), hence only
  at \(s=2\). Contribution \(1\).

Certified \(5\le k\le 8\). Combined with Cycle AM’s
\(I_k=1\oplus B_k^{\ge 10}\),

\[
I_k=B_k^{\ge 11}=B_k^{\ge 12}=1\oplus B_k^{\ge 13}\qquad(k\ge 5).
\]

## Nested depth 12 — killed as a formula for \(I_k\)

The identity \(I_k=1\oplus B^{\ge 13}\) still has a bulk of packed
bits \(\ge 13\). On \(5\le k\le 8\), \(I_k\) takes both values, so
\(B^{\ge 13}\) is neither identically 0 nor identically 1.
**Killed** as a closed form, for the same reason Cycle AM killed
depth 9. Do not hunt another finite nested-left family.

## Verdict

`LEMMA` (Fermat-subtract \(G(n,2^a-2^c-1)\); derived \(2^a-6,7,10,12\);
\(e_{11},e_{12}\) period 4; bits 10, 11, 12 contribute \(1,0,1\);
\(I_k=1\oplus B^{\ge 13}\) for \(k\ge 5\)).
`KILLED` (nested depth 12 as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_au.md` (this note)
- `research/cycle_au.py`
- `research/cycle_au.json`
