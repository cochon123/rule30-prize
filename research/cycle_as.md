# Cycle AS: half-window \(G(n,2^a-2)\); unique-Green bits for \(I_k\)

Cycle AR lifted odd targets. On the *dyadic* annulus the same
recurrence gives unique Green coefficients for \(2^a-2\) and
\(2^a-4\) in the half-window \(n<2^{a-1}\). Those identities classify
two infinite families of unique-Green packed bits for \(I_k\), and
the two double-Green bits. Packed bit 9 always fires at time
\(T=2^{k-1}\). The XOR of unique firings is not \(I_k\). Not a prize
claim: \(I_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_as.py --certify` (~0.01s). Dump:
`research/cycle_as.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (half-window \(G(n,2^a-2)\))

For \(a\ge 1\) and \(0\le n<2^{a-1}\),

\[
G(n,2^a-2)=1 \quad\text{iff}\quad n=2^{a-1}-1.
\]

The target is even. Even \(n=2\ell\) contribute
\(G(\ell,2^{a-1}-1)\), which vanishes in this window by Cycle AP
(Mersenne: \(2^{a-1}\nmid(\ell+1)\) for \(\ell<2^{a-2}\)). Odd
\(n=2\ell+1\) reduce to \(G(\ell,2^{a-1}-2)\) after the Mersenne
term drops, and induction leaves only the all-ones argument
\(n=2^{a-1}-1\), which sits on the cone \(G(m,2m)=1\). Base \(a=1\)
is \(G(0,0)=1\). Certified \(a\le 12\).

## Lemma (half-window \(G(n,2^a-3)\) and \(G(n,2^a-4)\))

For \(a\ge 2\) and \(n<2^{a-1}\), \(G(n,2^a-3)=1\) iff
\(n=2^{a-1}-1\). Cycle AR’s lift writes \(2^a-3=q\cdot 2-1\) with
\(q=2^{a-1}-1\), so the claim is the previous lemma at \(a-1\).

For \(a\ge 3\) and \(n<2^{a-1}\),

\[
G(n,2^a-4)=1 \quad\text{iff}\quad n=2^{a-1}-2.
\]

Even \(n\) reduce to \(G(\ell,2^{a-1}-2)\), hence the unique even hit
\(n=2^{a-1}-2\). Odd \(n\) XOR the two previous lemmas and cancel.
Certified \(a\le 12\).

## Lemma (unique \(2^j+1\) family)

Let \(T=2^{k-1}\) and \(k\ge 2\). Packed bit \(p=2^j+1\) has odd
target \(2^k-2^j-1=(2^{k-j}-1)2^j-1\). The lift and the
\(2^a-2\) lemma with \(a=k-j\) and window \(n<2^{k-1-j}\) give a
unique \(n=2^{k-1-j}-1\), i.e. unique time \(t=T\). The cone
\(p\le 2T\) holds for every \(j=0,\ldots,k-1\). So each of these
\(k\) bits is unique-Green at time \(T\).

## Lemma (unique \(3\cdot 2^j+1\) family)

For \(0\le j\le k-3\) (so \(k-j\ge 3\)), packed bit
\(p=3\cdot 2^j+1\) has target \((2^{k-j}-3)2^j-1\). The lift and the
\(2^a-4\) lemma give unique \(n=2^{k-1-j}-2\), i.e. unique time
\(t=T+2^j\). Cycle AM’s packed bit 4 at \(t=T+1\) is the case
\(j=0\). These are \(k-2\) further unique-Green bits.

## Lemma (two double-Green bits)

The next \(3\)-family index \(j=k-2\) has \(a=2\), where
\(G(n,0)=1\) on the two-point window \(n\in\{0,1\}\). Times \(t=T\)
and \(t=3T/2\), both in cone: packed bit \(p=3\cdot 2^{k-2}+1\) is
double-Green.

Packed bit \(p=5\cdot 2^{k-3}+1\) (\(k\ge 4\)) lifts with \(a=3\) to
\(G(n,2)\) on \(n<4\), hence Cycle AO’s two residues \(n=1,2\). Times
\(t=5T/4\) and \(t=3T/2\). Double-Green.

Certified \(4\le k\le 8\): these two bits are double-Green with those
times.

## Lemma (packed bit 9 always fires at \(T\))

Bit \(p=9=2^3+1\) is the \(j=3\) member of the \(2\)-family, hence
unique-Green at \(t=T\). For \(k\ge 4\), \(T\ge 8\) is past the onset
of \(e_8\) and \(e_9\) (Cycle AM): \(e_9\equiv 1\) and
\(e_8(t)=1\) iff \(t\equiv 0,1\pmod{4}\). Now \(T=2^{k-1}\) is
divisible by \(8\), so \(T\equiv 0\pmod{4}\) and the AND at packed
bit 9 fires. Certified \(4\le k\le 8\).

This upgrades Cycle AM’s prefix that bit 9 has *odd* Green parity to
a unique hit of weight 1. Combined with bits 4 and 6 it is not a new
formula for \(I_k\).

## Unique XOR — killed as a formula for \(I_k\)

On \(4\le k\le 8\) the XOR of unique-Green firings disagrees with
\(I_k\) (already at \(k=5\)). **Killed.** Exhaustiveness of exactly
\(2k-2\) unique-Green bits and exactly two doubles is a certified
prefix, not a theorem for all \(k\).

## Verdict

`LEMMA` (half-window \(G(n,2^a-2)\), \(G(n,2^a-3)\), \(G(n,2^a-4)\);
unique \(2^j+1\) and \(3\cdot 2^j+1\) families; two double bits;
bit 9 always fires at \(T\)).
`PREFIX` (exactly those unique bits; exactly two doubles).
`KILLED` (unique-fire XOR as \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_as.md` (this note)
- `research/cycle_as.py`
- `research/cycle_as.json`
