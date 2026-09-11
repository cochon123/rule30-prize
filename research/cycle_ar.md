# Cycle AR: Green lift; five triples and four quadruples

Cycle AQ listed five triple-Green packed bits on the 3-fold annulus as
a prefix. The doubling recurrence lifts every odd target
\(q\cdot 2^j-1\) to a finite check of \(G(n,q-1)\), and that window
is independent of \(k\). The five triples and four quadruples therefore
have closed times. None of them is an identically-1 production for
\(\theta_k\). Not a prize claim: \(\theta_k=1\) infinitely often
remains open.

Helper: `python3 research/cycle_ar.py --certify` (~0.12s). Dump:
`research/cycle_ar.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Green lift)

For every integer \(q\ge 1\) and every \(j\ge 1\),

\[
G\bigl(m,\,q\cdot 2^j-1\bigr)=1
\quad\text{iff}\quad
2^j\mid(m+1)
\text{ and }
G\bigl((m+1)/2^j-1,\,q-1\bigr)=1.
\]

The target is odd, so even \(m\) vanish. Odd \(m=2n+1\) reduce by the
doubling recurrence to \(G(n,q\cdot 2^{j-1}-1)\). After \(j\) steps,
\(m+1=2^j(n+1)\) and the remaining target is \(q-1\). The degree cut
is compatible: if \(q-1\le 2n\) then \(q\cdot 2^j-1\le 2m\). Case
\(q=1\) is Cycle AP’s Mersenne-target law. Certified \(q\le 16\),
\(j\le 6\), \(m\le 4q\cdot 2^j\).

If the uncut sequence \(n\mapsto G(n,q-1)\) (for \(2n\ge q-1\)) is
periodic of period \(2^e\) with residue set \(R\), the lift is
periodic of period \(2^{e+j}\) with residues
\(\{2^j(r+1)-1:r\in R\}\).

## Lemma (Fermat-odd reduction)

For \(q=2^a+1\) the second factor is Cycle AQ’s \(G(n,2^a)\). In
particular:

- \(a=1\) (\(q=3\)): residues \(\{2^{j+1}-1,\,3\cdot 2^j-1\}\)
  modulo \(2^{j+2}\), which is Cycle AO’s two-point law at \(j=k\).
- \(a=2\) (\(q=5\)): residues
  \(\{3\cdot 2^j-1,\,5\cdot 2^j-1,\,3\cdot 2^{j+1}-1,\,2^{j+3}-1\}\)
  modulo \(2^{j+3}\), which is Cycle AP’s four-point law at \(j=k\).

Certified \(j\le 8\), \(m\le 16\cdot 2^j\).

## Lemma (five triple-Green bits)

Let \(U=2^k\) with \(k\ge 4\). Packed bit \(p\) Green-hits
\(\theta_k\) at those \(m=3U-t-1\) in \([0,2U-1]\) with
\(G(m,3U-p)=1\) and \(p\le 2t\). Writing \(3U-p=q\cdot 2^j-1\), the
lift forces \(m=2^j(n+1)-1\) with \(n\le 2^{k+1-j}-1\). For each of
the five Cycle AQ bits, \(j=k-j_{\mathrm{off}}\) makes that bound
independent of \(k\):

| bit | \(p\) | \(q\) | \(j\) | \(n\le\) | \(n\) with \(G(n,q-1)=1\) | times |
| --- | --- | --- | --- | --- | --- | --- |
| A | \(2^{k-3}+1\) | 23 | \(k-3\) | 15 | \(11,13,14\) | \(9U/8,\,5U/4,\,3U/2\) |
| B | \(2^{k-2}+1\) | 11 | \(k-2\) | 7 | \(5,6,7\) | \(U,\,5U/4,\,3U/2\) |
| C | \(5\cdot 2^{k-3}+1\) | 19 | \(k-3\) | 15 | \(9,10,15\) | \(U,\,13U/8,\,7U/4\) |
| D | \(3\cdot 2^{k-2}+1\) | 9 | \(k-2\) | 7 | \(4,5,7\) | \(U,\,3U/2,\,7U/4\) |
| E | \(5\cdot 2^{k-1}+1\) | 1 | \(k-1\) | 3 | \(0,1,2,3\) | \(3U/2,\,2U,\,5U/2\) |

Bit E is Mersenne \(2^{k-1}-1\): four \(n\), but \(n=3\) is time \(t=U\)
with \(p>2t\), so the cone drops it to a triple. The other four cones
hold for every listed time. The \(n\)-lists are finite evaluations of
\(G\) (for A, \(G(n,22)=0\) automatically on \(n\le 10\) by degree).
Certified: Green times equal the table for \(4\le k\le 8\), and equal
the lift prediction.

## Lemma (four quadruple-Green bits)

The same window produces four bits of Green-count 4:

| bit | \(p\) | \(q\) | \(j\) | \(n\le\) | \(n\) | times |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | \(9\cdot 2^{k-3}+1\) | 15 | \(k-3\) | 15 | \(7,11,13,14\) | \(9U/8,\,5U/4,\,3U/2,\,2U\) |
| Q2 | \(5\cdot 2^{k-2}+1\) | 7 | \(k-2\) | 7 | \(3,5,6,7\) | \(U,\,5U/4,\,3U/2,\,2U\) |
| Q3 | \(7\cdot 2^{k-2}+1\) | 5 | \(k-2\) | 7 | \(2,4,5,7\) | \(U,\,3U/2,\,7U/4,\,9U/4\) |
| Q4 | \(9\cdot 2^{k-2}+1\) | 3 | \(k-2\) | 7 | \(1,2,5,6\) | \(5U/4,\,3U/2,\,9U/4,\,5U/2\) |

Q3 is Cycle AP’s four-point law at \(j=k-2\); Q4 is Cycle AO’s
two-point law at \(j=k-2\), now spanning two periods of length 4
inside \(n\le 7\). Certified \(4\le k\le 8\).

## Extra bits — killed as forced 1s

On \(4\le k\le 8\) the firing XOR of each triple takes the value 0
(so none is identically 1). Each quadruple takes both XOR values.
**Killed.** Cycle AQ’s prefix that bit B’s three firings are
\((k\bmod 2)\) on every time dies at \(k=9\) (all three zeros).
**Killed.** Bit D’s three firings are 0 on \(4\le k\le 8\) (and on
the extra checks \(k=9,10\)); that vanishing is a prefix, not a
theorem. Exhaustiveness of exactly five triples and exactly four
quadruples is likewise a prefix \(4\le k\le 8\).

## Verdict

`LEMMA` (Green lift; Fermat-odd reduction recovering AO/AP; closed
times for the five triples and four quadruples).
`PREFIX` (exactly those five triples and four quadruples; bit D never
fires).
`KILLED` (those bits as identically-1 productions; bit B XOR
\(k\bmod 2\)).
`OPEN` (\(\theta_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ar.md` (this note)
- `research/cycle_ar.py`
- `research/cycle_ar.json`
