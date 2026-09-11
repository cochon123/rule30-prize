# Cycle BW: left-machine period \(H=2^{k-1}\)

The left \(W+1\) packed bits (\(W=2^k\)) evolve autonomously (Cycle BV).
For \(k=1\) and \(k=2\) they are periodic with period \(H=W/2\) for
every \(t\ge 2\). One seed equality \(F^H(L_k(2W))=L_k(2W)\) then
extends period \(H\) to all later times by autonomy, which is stronger
than Cycle BV's \(F^W=\mathrm{id}\) and still forces
\(J_B^{\to 2U}=0\). The low \(H+1\) bits are the scale-\((k-1)\)
machine, so they inherit period \(H\) from \(P_{k-1}\). Green weights
on a \(W\)-window at degrees \(d<H\) have period \(H\) because
\(G(m+2^a,d)=G(m,d)\) for \(m,d<2^a\). The seed holds through \(k=12\)
(prefix). Period \(H\) from time \(W\) fails at \(k=5\) (high bits
only). Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bw.py --certify`. Dump:
`research/cycle_bw.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Green shift)

Freshman gives \((1+x+x^2)^{2^a}=1+x^{2^a}+x^{2^{a+1}}\), hence

\[
G(m+2^a,d)=G(m,d)\oplus G(m,d-2^a)\oplus G(m,d-2^{a+1}).
\]

For \(0\le m,d<2^a\) the last two terms vanish, so
\(G(m+2^a,d)=G(m,d)\). Certified against the doubling recurrence for
\(a\le 8\) (small-degree form) and \(a\le 6\) (full product).

## Lemma (packed period-\(H\) identity)

A freshman step of length \(H=2^{k-1}\) comparing packed bit \(p\) at
times \(t\) and \(t+H\) is the same-spatial identity at
\(j=p-t-H\):

\[
\lambda_p(t+H)\oplus\lambda_p(t)
=\lambda_{p-H}(t)\oplus\lambda_{p-W}(t)
\oplus J_{[t,\,t+H)\to p}.
\]

Period \(H\) at bit \(p\) iff the Green AND-parity equals the two
extras. Certified on the window \([2W,2W+H)\) for \(1\le k\le 6\) and
every \(0\le p\le W\). High ANDs \(q>p\) cannot hit packed \(p\).

## Lemma (\(k=1\) and \(k=2\))

Packed bits \(0,1,2,4\) are \(1,1,0,1\) for every \(t\ge 2\) (Cycle
BV). The bit-3 update collapses to \(1\oplus\lambda_3\), so bit 3
flips every step. The five-bit word is therefore
\(\mathtt{11001}\) on even times and \(\mathtt{11011}\) on odd times
(LSB first), period \(H=2\). The three-bit word at \(k=1\) is the
constant \(\mathtt{110}\), period \(H=1\). Certified \(t\le 128\).

## Lemma (seed implies global period \(H\))

Write \(F\) for one left-machine step and \(L_k(t)\) for the
\((W+1)\)-bit word at time \(t\). If \(F^H(L_k(2W))=L_k(2W)\),
autonomy gives \(L_k(t+H)=L_k(t)\) for every \(t\ge 2W\). In
particular \(L_k(2W)=L_k(3W)\), which is Cycle BV's freeze, hence
\(J_B^{\to 2U}=0\) at covering scale \(k-1\). Certified: the seed
equals the sampled words at \(2W+H\), and those equal the words at
\(3W\), through \(k=12\).

## Lemma (low half inducts)

Bits \(0,\ldots,H\) of \(L_k(t)\) are exactly \(L_{k-1}(t)\). If
\(P_{k-1}\) holds (period \(H/2\) for \(t\ge 2^{k}=2H\)), then those
low bits have period \(H\) for \(t\ge 2W\). Failures of period \(H\)
at time \(W\) (when they exist) cannot live on bits \(\le H\).
Certified nested truncation for \(2\le k\le 6\); high-only failures
at \(t=W\) for \(k=5,6\).

## Lemma (unique attractor at \(k=3,4\))

On the invariant affine space with packed bits \(0,1,2=1,1,0\), the
9-bit machine (\(k=3\)) has exactly four states with \(F^4=\mathrm{id}\),
a single 4-cycle, and every one of the 64 states reaches it. The
17-bit machine (\(k=4\)) likewise has exactly four states with
\(F^4=\mathrm{id}\), globally attracting among all \(2^{14}\) affine
states. The prize orbit is on the \(k=3\) cycle at \(t=2\) and on the
\(k=4\) cycle at \(t=16=W\). Exhaustive, not a sampling prefix.

## Prefix (seed for all \(k\))

\(F^H(L_k(2W))=L_k(2W)\) holds for \(1\le k\le 12\). **PREFIX**, not
a theorem for all \(k\). On that prefix the left word has period \(H\)
for all \(t\ge 2W\), Cycle BV's freeze holds, and
\(J_B^{\to 2U}=0\) at covering scales \(n\le 11\).

## Period \(H\) from time \(W\) — killed

At \(k=5\), times \(W=32\) and \(W+H=48\) differ in packed bits
\(30,31,32\), all \(>H=16\). **Killed** as a statement for every
\(k\). The high-only location of those failures is the low-half lemma,
not a replacement for the seed at \(2W\).

## \(F^H=\mathrm{id}\) on the whole affine space — killed

Only four of the 64 states at \(k=3\) satisfy \(F^4=\mathrm{id}\).
Period \(H\) is an attractor property, not an identity of the map.

## Verdict

`LEMMA` (Green shift; packed period-\(H\) identity; \(k=1,2\); seed
implies global period \(H\); period \(H\) implies BV freeze; low half
inducts; unique attractor at \(k=3,4\)).
`PREFIX` (seed for all \(k\); Fermat covering for all \(k\ge 2\)).
`KILLED` (period \(H\) from time \(W\) for all \(k\);
\(F^H=\mathrm{id}\) on the whole affine space).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bw.md` (this note)
- `research/cycle_bw.py`
- `research/cycle_bw.json`
