# Cycle AP: Mersenne-target \(G\); 4-point 5-fold; unique-Green bits for \(\theta\)

Cycle AO’s two-point law makes packed bit 1 unique-Green on the 3-fold
annulus. The same doubling recurrence gives a one-residue law for
Mersenne *targets* \(2^a-1\) and a four-residue law for \(5\cdot 2^k-1\).
Those three congruences produce four explicit unique-Green packed bits
on \([2^k,3\cdot 2^k)\) for \(k\ge 3\). The extra three do not always
fire, so they are not further forced 1s. Not a prize claim:
\(\theta_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_ap.py --certify`. Dump:
`research/cycle_ap.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Mersenne target)

\[
G(m,2^a-1)=1 \quad\text{iff}\quad 2^a\mid(m+1)
\]

(for \(a=0\): \(G(m,0)=1\) for all \(m\ge 0\)). The target is odd for
\(a\ge 1\), so even \(m\) vanish and \(2^a\nmid(m+1)\). For odd
\(m=2n+1\), \(G(2n+1,2^a-1)=G(n,2^{a-1}-1)\), and
\(n+1=(m+1)/2\). Certified \(a\le 10\), \(m\le 8\cdot 2^a\).

Cycle AA is the case \(a=k\) on the dyadic annulus: \(m+1\le 2^{k-1}\),
so \(2^k\nmid(m+1)\), and packed bit 1 never hits \(I_k\).

## Lemma (four-point congruence for \(5\cdot 2^k-1\))

\[
G(m,5\cdot 2^k-1)=1
\]
iff \(m\) lies in one of the classes
\(3\cdot 2^k-1\), \(5\cdot 2^k-1\), \(3\cdot 2^{k+1}-1\),
\(2^{k+3}-1\) modulo \(2^{k+3}\). Base \(k=0\) is \(G(m,4)\) on
\(\{2,4,5,7\}\pmod{8}\), from \(G(n,2)\) (Cycle AO) and \(G(n,1)\).
The inductive step is the odd reduction, doubling residues modulo
\(2^{k+3}\). Certified \(k\le 7\), \(m\le 16\cdot 2^k\).

On the 5-fold annulus \(m\le 2^{k+2}-1<2^{k+3}\) only
\(3\cdot 2^k-1\) appears, recovering Cycle AO’s unique \(q=5\) hit.

## Lemma (four unique-Green bits on the 3-fold annulus)

Let \(U=2^k\) with \(k\ge 3\). The following packed bits have exactly
one Green time in \([U,3U)\):

| \(p\) | target \(3U-p\) | time | reason |
| --- | --- | --- | --- |
| \(1\) | \(3\cdot 2^k-1\) | \(U\) | Cycle AO two-point |
| \(2^{k-1}+1\) | \(5\cdot 2^{k-1}-1\) | \(3U/2\) | four-point, one in-range residue |
| \(U+1\) | \(2^{k+1}-1\) | \(U\) | Mersenne; \(t\equiv U\pmod{2U}\) |
| \(2U+1\) | \(2^k-1\) | \(2U\) | Mersenne; \(t=U\) has \(p>2t\) |

Packed bit 1 always fires. \(p=U+1\) at \(t=U\) is the centre-right
AND \(c_U\land r_U\); \(p=2U+1\) at \(t=2U\) is \(c_{2U}\land r_{2U}\).
Certified: each of these four has Green-count 1, with the stated
times, for \(3\le k\le 8\). On that range they are the *only*
unique-Green packed bits (prefix, not a theorem for all \(k\)).

## Extra unique bits — killed as forced 1s

The three bits besides \(p=1\) take both firing values on
\(3\le k\le 8\). They do not supply an extra identically-1 production
to cancel or reinforce \(S_k\). **Killed.** Multi-hit packed bits
remain the obstruction to \(\theta_k\equiv 1\).

## Verdict

`LEMMA` (Mersenne target; four-point 5-fold; four unique-Green bits
with proved times). `PREFIX` (exactly those four unique-Green bits).
`KILLED` (the extra three as always-fire productions).
`OPEN` (\(\theta_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ap.md` (this note)
- `research/cycle_ap.py`
- `research/cycle_ap.json`
