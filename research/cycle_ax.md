# Cycle AX: triple-Green bits are the 5, 7, 9, 13 families

Cycles AV and AW classified unique and double half-window supports.
The even-count identity for \(|S|=3\) has two mechanisms. Mechanism
(i) uses Cycle AV’s consecutive uniques with distinct supports and
yields \(2^a-6\) and \(2^a-8\). Mechanism (ii) from those even seeds
yields \(2^a-10\) and \(2^a-14\). Odd triples are one doubling of a
triple one level down. Packed bits are \(p=q\cdot 2^j+1\) for
\(q\in\{5,7,9,13\}\). Bits 14 and 15 contribute \(0\). Triple XOR is
not \(I_k\). Not a prize claim: \(I_k=1\) infinitely often remains
open.

Helper: `python3 research/cycle_ax.py --certify` (~4s). Dump:
`research/cycle_ax.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (half-window \(G(n,2^a-14)\))

For \(a\ge 5\) and \(n<2^{a-1}\),

\[
G(n,2^a-14)=1 \quad\text{iff}\quad 2^{a-1}-1-n\in\{0,5,6\}.
\]

The target is even. Cycle AU’s unique \(G(n,2^{a-1}-7)\) and
Jacobsthal \(G(n,2^{a-1}-8)\) (Cycle AT, \(S_3=\{0,2,3\}\)) give
\(A\subseteq B\) in the even-count identity, hence three hits, with
those \(s\). At \(a=4\) there are four hits. Certified \(a\le 12\).

## Lemma (even triples are \(2^a-\{6,8,10,14\}\))

For \(a\ge 5\), even \(D\) with \(|S(a,D)|=3\) are exactly
\(2^a-6\), \(2^a-8\), \(2^a-10\), and \(2^a-14\). Cycle AV’s even
count: \(|S(b,2e)|=3\) iff \(|B|=1\) and \(|A\setminus B|=1\), or
\(|B|=3\) and \(A\subseteq B\).

- (i) \(|B|=1\) forces \(e-1\) unique. If \(e\) is not unique then
  \(|A|\) is odd and at least 3, so \(|A\setminus B|\) cannot be 1.
  Thus both \(e-1\) and \(e\) are unique and \(A\neq B\): consecutive
  uniques with distinct supports. Cycle AV’s only such pairs are
  \((2^{c}-5,2^{c}-4)\) and \((2^{c}-4,2^{c}-3)\), giving
  \(2^{a}-8\) and \(2^{a}-6\).
- (ii) From the even seeds at level \(c\), \(q\in\{6,8\}\) have
  \(A\subseteq B\) (explicit \(s\)-sets versus a unique neighbour),
  giving \(2^{a}-10\) and \(2^{a}-14\); \(q\in\{10,14\}\) do not.

Certified \(a\le 12\), mechanisms \(c\le 11\).

## Lemma (triples are the 5, 7, 9, 13 families)

Odd doubling sends triples to triples. Combined with the four even
seeds, every triple \(D\) is an odd lift of \(2^b-q\) for some
\(q\in\{6,8,10,14\}\) and \(b\le a\). Packed bit
\(p=2^{a}-D=q\cdot 2^{j}+1\) with \(q\in\{5,7,9,13\}\). On the
dyadic annulus, cone cuts the families at the unique/double
thresholds of Cycles AS–AW:

- \(5\cdot 2^{j}+1\) for \(j\le k-4\) (next index is the
  \(5T/8+1\) double);
- \(7\cdot 2^{j}+1\) for \(j\le k-4\) (Cycle AT);
- \(9\cdot 2^{j}+1\) and \(13\cdot 2^{j}+1\) for \(j\le k-5\).

There are \(4k-14\) such bits (\(k\ge 4\)). Times are
\(t=T+s\cdot 2^{j}\) with \(s\in\{0,1,2\}\), \(\{0,2,3\}\),
\(\{1,2,4\}\), \(\{0,5,6\}\) respectively. Certified on the annulus
for \(4\le k\le 8\).

## Lemma (bits 14 and 15 contribute 0)

For \(k\ge 5\), packed bit \(14=13+1\) is the \(j=0\) member of the
\(13\)-family, times \(T,T+5,T+6\). The AND is \(e_{14}\land e_{13}\).
Cycle AV: this fires iff \(t\equiv 0,1\pmod{4}\). Residues of the
three times are \(0,1,2\), hence fires \(1,1,0\) and XOR \(0\).

Packed bit \(15=7\cdot 2+1\) is the \(j=1\) member of the
\(7\)-family, times \(T,T+4,T+6\). The AND \(e_{15}\land e_{14}\)
fires iff \(t\equiv 0\pmod{4}\). Residues \(0,0,2\) give fires
\(1,1,0\) and XOR \(0\). Certified \(5\le k\le 8\). These are not a
nested-left formula for \(I_k\).

## Exactly five quads — prefix

For \(5\le a\le 10\), there are exactly five half-window \(D\) with
\(|S(a,D)|=4\), and they are the odd-lift orbit of
\(\{18,19,23,27,29\}\) at \(a=5\). **Prefix.**

## Triple XOR — killed as a formula for \(I_k\)

On \(4\le k\le 8\) the XOR of triple-Green firings disagrees with
\(I_k\). **Killed.**

## Verdict

`LEMMA` (\(G(n,2^a-14)\); even triples \(2^a-\{6,8,10,14\}\);
5, 7, 9, 13 families; bits 14 and 15 contribute \(0\)).
`PREFIX` (exactly five quads).
`KILLED` (triple XOR as \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ax.md` (this note)
- `research/cycle_ax.py`
- `research/cycle_ax.json`
