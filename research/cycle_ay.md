# Cycle AY: bit 16 \(S_4\); \(e_{18}\); \(I_k=1\oplus B^{\ge 19}\)

Cycle AU gave \(I_k=1\oplus B_k^{\ge 13}\) for \(k\ge 5\). Bits 13,
14, 15, and 17 already contribute 0 (Cycles AV–AX). Packed bit 16 is
Jacobsthal \(S_4\), and with those period-4 tails its five AND fires
XOR to 0. The next left-diagonal \(e_{18}\) is period 4 from
\(t\ge 20\), and \(e_{18}\land e_{17}\) is identically 0, so bit 18
never fires. Hence \(I_k=1\oplus B_k^{\ge 19}\). Nested depth 18 is
not a closed form. Not a prize claim: \(I_k=1\) infinitely often
remains open.

Helper: `python3 research/cycle_ay.py --certify` (~0.01s). Dump:
`research/cycle_ay.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (bit 16 is Jacobsthal \(S_4\))

Cycle AT: for \(1\le b<a\) and \(n<2^{a-1}\), \(G(n,2^a-2^b)=1\) iff
\(2^{a-1}-1-n\in S_b\). Here \(b=4\) and \(S_4=\{1,4,5,6,7\}\). Packed
bit \(p=16\) therefore Green-hits at \(t=T+s\) for \(s\in S_4\), all
in cone for \(k\ge 5\). Certified \(a\le 12\), and on the annulus for
\(5\le k\le 8\).

## Lemma (bit 16 contributes 0)

The AND is \(e_{16}\land e_{15}\). Cycle AV: this fires iff
\(t\equiv 0,3\pmod{4}\). The five times have residues
\(1,0,1,2,3\), hence fires \(0,1,0,0,1\) and XOR \(0\). Certified
\(5\le k\le 8\).

## Lemma (\(e_{18}\) is period 4)

The recurrence is \(e_{18}(t+1)=e_{16}(t)\oplus(e_{17}(t)\lor e_{18}(t))\).
Cycle AV supplies \(e_{16}(t)=1\) iff \(t\not\equiv 1\pmod{4}\) and
\(e_{17}(t)=1\) iff \(t\equiv 3\pmod{4}\). The tail
\(e_{18}(t)=1\) iff \(t\equiv 1,2\pmod{4}\) is invariant, and holds
from \(t=20\). In particular \(e_{18}\land e_{17}\) is identically 0
on that tail (residues \(\{1,2\}\) and \(\{3\}\) are disjoint).
Certified on \(t<256\), including the recurrence.

## Lemma (bit 18 never fires)

Packed bit 18 is a quad seed (Cycle AX prefix). Every Green time has
AND \(e_{18}\land e_{17}\). For \(k\ge 6\), \(T\ge 32\) is past the
onset, so every fire is 0. At \(k=5\) the four Green times
\(17,18,20,24\) also fail to fire. Contribution \(0\). Certified
\(5\le k\le 8\).

## Lemma (\(I_k=1\oplus B^{\ge 19}\))

Bits 13, 14, 15, 17 contribute 0 (Cycles AV–AX), and bits 16 and 18
contribute 0. Cycle AU’s identity therefore upgrades to

\[
I_k=1\oplus B_k^{\ge 19}\qquad(k\ge 5).
\]

Certified \(5\le k\le 8\).

## Nested depth 18 — killed as a formula for \(I_k\)

The identity still has a bulk of packed bits \(\ge 19\). On
\(5\le k\le 8\), \(I_k\) takes both values, so \(B^{\ge 19}\) is
neither identically 0 nor identically 1. **Killed** as a closed form.
Do not hunt another finite nested-left family.

## Verdict

`LEMMA` (bit 16 is \(S_4\) and contributes 0; \(e_{18}\) period 4;
bit 18 never fires; \(I_k=1\oplus B^{\ge 19}\) for \(k\ge 5\)).
`KILLED` (nested depth 18 as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ay.md` (this note)
- `research/cycle_ay.py`
- `research/cycle_ay.json`
