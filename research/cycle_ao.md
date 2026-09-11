# Cycle AO: two-point \(G(m,3\cdot 2^k-1)\); unique leftmost-11 hits

Cycle AJ proved that the leftmost 11 hits \(\theta_k\) at time \(2^k\),
so \(\theta_k=1\oplus S_k\). The Green target \(3\cdot 2^k-1\) has a
complete two-residue closed form, which upgrades that hit to a unique
time in the 3-fold annulus. The same count of leftmost-11 Green times
is independent of \(k\) for every \(q\). Not a prize claim:
\(\theta_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_ao.py --certify` (~0.01s). Dump:
`research/cycle_ao.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (two-point congruence)

\[
G\bigl(m,\,3\cdot 2^k-1\bigr)=1
\quad\text{iff}\quad
m\equiv 2^{k+1}-1 \pmod{2^{k+2}}
\text{ or }
m\equiv 3\cdot 2^k-1 \pmod{2^{k+2}}.
\]

Base \(k=0\): \(G(m,2)=1\) iff \(m\equiv 1\) or \(2\pmod{4}\), by the
doubling recurrence and \(G(\,\cdot\,,0)\equiv 1\), \(G(\,\cdot\,,1)=1\)
iff the first argument is odd. For \(k\ge 1\) the target is odd, so
even \(m\) vanish, and
\(G(2n+1,3\cdot 2^k-1)=G(n,3\cdot 2^{k-1}-1)\). The inductive residues
double to the two stated classes modulo \(2^{k+2}\). Certified
\(k\le 8\) and \(m\le 16\cdot 2^k\).

In the 3-fold annulus the degree is \(m\le 2^{k+1}-1<2^{k+2}\), and
\(3\cdot 2^k-1>2^{k+1}-1\), so the only in-range solution is
\(m=2^{k+1}-1\).

## Lemma (unique leftmost-11 hit for \(\theta_k\))

Packed bit 1 always fires (Cycle AA). Combined with the congruence,
it Green-hits \(\theta_k\) at exactly one time of \([2^k,3\cdot 2^k)\),
namely \(t=2^k\) (\(m=2^{k+1}-1\)). Hence
\(\theta_k=1\oplus S_k\) with \(S_k\) free of packed-bit-1 hits.
Certified \(1\le k\le 9\): count 1, XOR 1, unique time \(2^k\).

## Lemma (\(N(q)\) is independent of \(k\))

Let \(N_k(q)\) be the number of \(m\le(q-1)2^k-1\) with
\(G(m,q\cdot 2^k-1)=1\). For \(k\ge 1\) the target is odd, even \(m\)
drop, and odd \(m=2n+1\) reduce to \(N_{k-1}(q)\). Thus
\(N_k(q)=N_0(q)\), where
\(N(q):=N_0(q)=\#\{m\le q-2:G(m,q-1)=1\}\). Because packed bit 1
always fires, this is exactly the number of leftmost-11 Green hits on
\([2^k,q\cdot 2^k)\). Its parity is Cycle AL’s
\(P(q)=1\oplus\mathrm{wt}(q)\). Certified \(2\le q\le 16\),
\(k\le 6\). In particular \(N(3)=N(5)=1\), \(N(7)=2\), \(N(9)=3\).

## Lemma (unique \(q=5\) hit at \(t=2^{k+1}\))

\(N(5)=1\) and \(G(3\cdot 2^k-1,5\cdot 2^k-1)=1\) by the same odd
reduction down to \(G(2,4)=1\). The unique \(m\) in the 5-fold
annulus is therefore \(3\cdot 2^k-1\), i.e. time \(t=2^{k+1}\).
Certified \(1\le k\le 8\).

## Two-point family — killed as a formula for \(\theta_k\)

For each \(j\le k\), packed bit \(p=3(2^k-2^j)+1\) has Green target
\(3\cdot 2^j-1\), so it can hit at most the two congruent times. The
XOR of those firings over \(j\) is not identically 1 (already both
values on \(1\le k\le 9\)) and is not equal to \(\theta_k\). **Killed.**
Cycle AJ already killed \(S\equiv 0\).

## Verdict

`LEMMA` (two-point congruence; unique \(p=1\) hit for \(\theta_k\);
\(N(q)\) independent of \(k\); unique \(q=5\) hit at \(2^{k+1}\)).
`KILLED` (two-point family XOR as a formula for \(\theta_k\)).
`OPEN` (\(\theta_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ao.md` (this note)
- `research/cycle_ao.py`
- `research/cycle_ao.json`
