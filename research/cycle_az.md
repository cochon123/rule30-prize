# Cycle AZ: five quads; \(e_{19}\); bit 19 contributes 1; \(I_k=B^{\ge 20}\)

Cycle AX listed five half-window quads as a prefix. For \(a\ge 6\)
there are no even quads, so those five are the odd-lift orbit of
\(a=5\)’s packed bits \(\{18,19,23,27,29\}\). Packed bit 19 is the
\(j=1\) member of the 9-family, hence a triple for \(k\ge 6\). The
period-4 tail of \(e_{19}\) makes its contribution 1, so
\(I_k=B_k^{\ge 20}\) for \(k\ge 6\). Nested depth 19 is not a closed
form. Quad XOR is not \(I_k\). Not a prize claim: \(I_k=1\) infinitely
often remains open.

Helper: `python3 research/cycle_az.py --certify` (~4s). Dump:
`research/cycle_az.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (no even quads for \(a\ge 6\))

Cycle AV’s even count: \(|S(b,2e)|=4\) iff \(|B|=0\) and \(|A|=2\), or
\(|B|=2\) and \(|A\setminus B|=1\), or \(|B|=4\) and \(A\subseteq B\).

- (i) If \(e\) is a double at level \(c\ge 5\), then \(e-1\) has
  nonempty support (Cycle AW’s cone point, or the 5-double
  predecessor).
- (ii) The Mersenne-double neighbour \(e=2^{c-2}\) has
  \(G(e,e)=1\) off that double’s support. The 5-double neighbour
  \(e=3\cdot 2^{c-3}\) has \(|A\setminus B|\ge 2\), so the next even
  target has size at least 6.
- (iii) If \(D\) is a quad at level \(c\), then
  \(S(c,D+1)\not\subseteq S(c,D)\).

Certified \(a\le 12\), blockers \(c\le 11\).

## Lemma (exactly five quads)

At \(a=5\) the packed bits with \(|S|=4\) are \(18,19,23,27,29\).
Odd doubling sends quads to quads. With no even quads, for every
\(a\ge 5\) there are exactly five, namely
\(p=2^{a-5}(s-1)+1\) for \(s\in\{18,19,23,27,29\}\). On the dyadic
annulus these are the double-Green cutoffs of the 7, 9, 13 families
together with the 17- and 23-lifts of 18 and 23. Certified \(a\le 12\),
and on the annulus for \(5\le k\le 8\).

## Lemma (\(e_{19}\) is period 4)

The recurrence is \(e_{19}(t+1)=e_{17}(t)\oplus(e_{18}(t)\lor e_{19}(t))\).
Cycles AV–AY supply \(e_{17}(t)=1\) iff \(t\equiv 3\pmod{4}\) and
\(e_{18}(t)=1\) iff \(t\equiv 1,2\pmod{4}\). The tail
\(e_{19}(t)=1\) iff \(t\equiv 2,3\pmod{4}\) is invariant, and holds
from \(t=20\). Certified on \(t<256\), including the recurrence.

## Lemma (bit 19 contributes 1)

For \(k\ge 6\), packed bit \(19=9\cdot 2+1\) is the \(j=1\) member of
Cycle AX’s 9-family, times \(T+2,T+4,T+8\). The AND is
\(e_{19}\land e_{18}\), which fires iff \(t\equiv 2\pmod{4}\). Residues
of the three times are \(2,0,0\), hence fires \(1,0,0\) and XOR \(1\).
Certified \(6\le k\le 8\).

## Lemma (\(I_k=B^{\ge 20}\))

Cycle AY: \(I_k=1\oplus B_k^{\ge 19}\) for \(k\ge 5\). Bit 19
contributes 1 for \(k\ge 6\), so

\[
I_k=B_k^{\ge 20}\qquad(k\ge 6).
\]

Certified \(6\le k\le 8\).

## Nested depth 19 — killed as a formula for \(I_k\)

The identity still has a bulk of packed bits \(\ge 20\). On
\(6\le k\le 8\), \(I_k\) takes both values, so \(B^{\ge 20}\) is
neither identically 0 nor identically 1. **Killed.** Do not hunt
another finite nested-left family.

## Quad XOR — killed as a formula for \(I_k\)

On \(5\le k\le 8\) the XOR of the five quad firings disagrees with
\(I_k\). **Killed.**

## Verdict

`LEMMA` (no even quads for \(a\ge 6\); exactly five quads;
\(e_{19}\) period 4; bit 19 contributes 1; \(I_k=B^{\ge 20}\) for
\(k\ge 6\)).
`KILLED` (nested depth 19 as a formula for \(I_k\); quad XOR as \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_az.md` (this note)
- `research/cycle_az.py`
- `research/cycle_az.json`
