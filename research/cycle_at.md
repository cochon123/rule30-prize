# Cycle AT: Jacobsthal half-window \(G(n,2^a-2^b)\)

Cycle AS treated \(b=1,2\). The same doubling recurrence gives a
closed form for every \(1\le b<a\): the half-window support is a
Jacobsthal set independent of \(a\). Packed bits
\(p=(2^c-1)2^j+1\) on the dyadic annulus therefore have explicit
Green times. Recovers Cycle AS at \(c=1,2\). The \(c=3\) family is
triple-Green. None of these is an identically-1 production for
\(I_k\). Not a prize claim: \(I_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_at.py --certify` (~0.01s). Dump:
`research/cycle_at.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Jacobsthal sets)

Define \(S_0=\emptyset\), \(S_1=\{0\}\), and
\(S_b=S_{b-2}\cup\{2^{b-2},\ldots,2^{b-1}-1\}\) for \(b\ge 2\). Then
\(|S_b|=(2^b-(-1)^b)/3\), the Jacobsthal number. Equivalently
\(S_b=\{0,\ldots,2^{b-1}-1\}\setminus S_{b-1}\). Two doubling rules,
used below: for \(s'<2^{b-2}\),

- \(2s'+1\in S_b\) iff \(s'\in S_{b-1}\);
- \(2s'\in S_b\) iff \(s'\in S_{b-1}\), when \(s'\ge 1\);
- \(0\in S_b\) iff \(b\) is odd.

Certified \(b\le 12\).

## Lemma (half-window \(G(n,2^a-2^b)\))

For \(1\le b<a\) and \(0\le n<2^{a-1}\),

\[
G(n,2^a-2^b)=1
\quad\text{iff}\quad
2^{a-1}-1-n\in S_b.
\]

Cycle AS is \(b=1\) (\(S_1=\{0\}\)) and \(b=2\) (\(S_2=\{1\}\)).
The target is even. Write \(s=2^{a-1}-1-n\).

Even \(n=2\ell\) reduces to \(G(\ell,2^{a-1}-2^{b-1})\) on
\(\ell<2^{a-2}\). For \(b=1\) this is a Mersenne target and vanishes
(Cycle AP). For \(b\ge 2\) the inductive hypothesis says the hit is
\(s'=2^{a-2}-1-\ell\in S_{b-1}\), and \(s=2s'+1\), so the first
doubling rule closes the even case.

Odd \(n=2\ell+1\) gives \(s=2s'\) and
\(G(\ell,2^{a-1}-2^{b-1})\oplus G(\ell,2^{a-1}-2^{b-1}-1)\). The first
summand is \(s'\in S_{b-1}\). The second target is odd; Cycle AR’s
lift writes it as \((2^{a-b}-1)2^{b-1}-1\), so it fires iff
\(2^{b-1}\mid(\ell+1)\) and \(G(\,\cdot\,,2^{a-b}-2)=1\). In the
window the divisibility holds only for \(s'=0\), and then Cycle AS
supplies the remaining 1. Thus the odd correction is \(1\) iff
\(s'=0\). Combined with the second doubling rule (and \(0\in S_b\)
iff \(b\) odd) this closes the odd case.

Certified \(a\le 12\), all \(1\le b<a\).

## Lemma (Mersenne-odd Green times)

Let \(T=2^{k-1}\) and \(p=(2^c-1)2^j+1\) with \(k-j>c\ge 1\). The
lift reduces the Green target to \(G(n,2^{k-j}-2^c)\) on
\(n<2^{k-1-j}\), hence to \(S_c\). The unique (when \(c=1,2\)) or
Jacobsthal-many times are

\[
t=T+s\cdot 2^j,\qquad s\in S_c,
\]

all in cone. In particular Cycle AS’s unique \(2^j+1\) family
(\(c=1\), \(s=0\), \(t=T\)) and unique \(3\cdot 2^j+1\) family
(\(c=2\), \(s=1\), \(t=T+2^j\)) are the \(J_c=1\) cases. Certified
\(4\le k\le 8\), all admissible \(c,j\).

## Lemma (\(7\)-family triples)

For \(c=3\), \(S_3=\{0,2,3\}\) and \(J_3=3\). Packed bit
\(p=7\cdot 2^j+1\) with \(j\le k-4\) is therefore triple-Green at
times \(T\), \(T+2^{j+1}\), \(T+3\cdot 2^j\). The case \(j=0\) is
packed bit 8: \(e_7\equiv 0\) (Cycle AD), so the AND never fires and
the contribution is 0. Certified \(4\le k\le 8\).

## Families — killed as forced 1s

On \(4\le k\le 8\) the firing XOR of the \(7\)-family bits takes both
values (0 for \(j=0\), which never fires, and 1 at e.g. \(k=7\),
\(j=3\)), so the family is not identically 1. The XOR of *all*
Mersenne-odd family firings disagrees with \(I_k\) (already at
\(k=4\)). **Killed** as formulas for \(I_k\). Non-Mersenne odd \(q\)
and even packed bits remain in the bulk.

## Verdict

`LEMMA` (Jacobsthal \(S_b\); half-window \(G(n,2^a-2^b)\); Mersenne-odd
times recovering AS; \(7\)-family triples).
`KILLED` (\(7\)-family identically 1; Mersenne-odd XOR as \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_at.md` (this note)
- `research/cycle_at.py`
- `research/cycle_at.json`
