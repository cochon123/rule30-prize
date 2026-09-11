# Cycle AQ: closed form for \(G(m,2^a)\); unique double-hit bit

Cycle AP classified unique-Green packed bits on the 3-fold annulus.
Power-of-two *targets* have an explicit bit-run formula, which also
identifies the unique double-Green bit as Cycle AO’s \(j=k-1\)
two-point member. That bit does not always fire. Not a prize claim:
\(\theta_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_aq.py --certify` (~0.11s). Dump:
`research/cycle_aq.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(G(m,2^a)\) bit-run form)

Write \(\chi_a(m)=G(m,2^a)\) when \(0\le 2^a\le 2m\), else \(0\). The
doubling recurrence and Cycle AP’s Mersenne-target law give

\[
\chi_a(m)=\chi_{a-1}(\lfloor m/2\rfloor)\oplus\mathbf{1}_{2^a\mid(m+1)}
\qquad(a\ge 1),
\]

with \(\chi_0(m)=m\bmod 2\). Unfolding,

\[
G(m,2^a)
=\mathrm{bit}_a(m)
\;\oplus\;
\bigl(L_a(m)\bmod 2\bigr),
\]

where \(L_a(m)\) is the length of the run of \(1\)s starting at bit
\(a-1\) and going downward (at most \(a\)). The XOR of the nested
ANDs \(\mathrm{bit}_{a-1}\land\cdots\land\mathrm{bit}_s\) over
\(s=0,\ldots,a-1\) equals \(L_a(m)\bmod 2\). Certified \(a\le 10\),
\(m\le 8\cdot 2^a\).

## Lemma (period and pairing)

The uncut characteristic function is periodic of period \(2^{a+1}\).
Flipping bit \(a\) (i.e. \(m\mapsto m\oplus 2^a\)) leaves \(L_a\)
unchanged and flips \(\mathrm{bit}_a\), so the two halves of each
period are complementary and there are exactly \(2^a\) residues.
Certified \(a\le 10\) (pairing) and \(a\le 8\) (period against \(G\)).

## Lemma (unique double-Green bit)

Cycle AO: packed bit \(p=3(2^k-2^{k-1})+1=3\cdot 2^{k-1}+1\) has
Green target \(3\cdot 2^{k-1}-1\), hence Green times
\(m\in\{2^k-1,\,3\cdot 2^{k-1}-1\}\), i.e. \(t=2U\) and \(t=3U/2\)
with \(U=2^k\). Both lie in \([U,3U)\) and \(p\le 2t\). So this bit
is double-Green. Certified \(3\le k\le 8\): it is the *only*
double-Green packed bit (prefix, not a theorem for all \(k\)). For
\(k\ge 4\) one also has exactly four unique-Green bits (Cycle AP) and
exactly five triple-Green bits

\[
p=2^{k-3}+1,\;
2^{k-2}+1,\;
5\cdot 2^{k-3}+1,\;
3\cdot 2^{k-2}+1,\;
5\cdot 2^{k-1}+1
\]

(prefix). The double-bit’s firing XOR takes both values on this
range, so it is not an identically-1 production. **Killed.** Cycle AO
already killed the full two-point family XOR.

## Verdict

`LEMMA` (bit-run form of \(G(m,2^a)\); period \(2^{a+1}\) and pairing;
the AO two-point member \(p=3U/2+1\) is double-Green).
`PREFIX` (exactly one double; five triples with those \(p\)).
`KILLED` (double-bit XOR identically 1).
`OPEN` (\(\theta_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_aq.md` (this note)
- `research/cycle_aq.py`
- `research/cycle_aq.json`
