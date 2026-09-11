# Cycle AW: exactly two double-Green bits for \(I_k\)

Cycle AV classified unique half-window supports. The same doubling
count gives the doubles: for \(a\ge 4\) there are no even
half-window doubles, so both double targets are the odd lifts of the
\(a=4\) pair. Packed bits for \(I_k\) therefore have exactly two
double-Green indices, \(p=3T/2+1\) and \(p=5T/8+1\). All
left-diagonals eventually period 4 is false. Packed bit 33 firing at
every dyadic time is a prefix. Not a prize claim: \(I_k=1\)
infinitely often remains open.

Helper: `python3 research/cycle_aw.py --certify` (~4s). Dump:
`research/cycle_aw.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Mersenne double)

For \(a\ge 2\),

\[
S(a,2^{a-2}-1)=\{2^{a-2}-1,\,2^{a-1}-1\}.
\]

Cycle AP: \(G(n,2^{a-2}-1)=1\) iff \(2^{a-2}\mid(n+1)\). In the
half-window \(n<2^{a-1}\) there are exactly two such \(n\). Certified
\(a\le 12\).

## Lemma (\(5\)-double)

\(S(3,2)=\{1,2\}\). For \(a\ge 4\), Cycle AR’s lift with \(q=3\) and
\(j=a-3\) gives \(G(n,3\cdot 2^{a-3}-1)=1\) iff \(2^{a-3}\mid(n+1)\)
and \(G((n+1)/2^{a-3}-1,2)=1\), hence

\[
S(a,3\cdot 2^{a-3}-1)=\{3\cdot 2^{a-3}-1,\,2^{a-2}-1\}.
\]

Certified \(a\le 12\).

## Lemma (no even doubles for \(a\ge 4\))

Cycle AV’s even count: \(|S(b,2e)|=|B|+2|A\setminus B|\) with
\(A=S(b-1,e)\) and \(B=S(b-1,e-1)\). This equals \(2\) iff either
\(|B|=0\) and \(|A|=1\), or \(|B|=2\) and \(A\subseteq B\).

There are no even doubles at \(a=4\). For \(a\ge 5\) both mechanisms
fail. The only unique \(e\) whose predecessor can leave the \(W=1\)
interval is the leftmost unique \(e=2^{a-2}-1\) (Cycle AV), and then
\(e-1=2^{a-2}-2\) contains the cone point \(G(m,2m)=1\) at
\(m=2^{a-3}-1\), so \(B\) is nonempty. If \(e-1\) is a double at
level \(a-1\), Cycle AV/the previous lemma give two possibilities;
in each, the central coefficient \(G(e,e)=1\) lies off that double’s
support, so \(A\not\subseteq B\). Certified \(a\le 12\), including
the two blockers.

## Lemma (exactly two double \(D\))

Odd doubling (Cycle AV) sends doubles to doubles via \(D\mapsto 2D+1\).
The \(a=4\) pair is \(\{3,5\}=\{2^{2}-1,\,3\cdot 2^{1}-1\}\). The
odd lifts are \(2^{a-2}-1\) and \(3\cdot 2^{a-3}-1\). With no even
doubles, these are all. Certified \(a\le 12\).

## Lemma (exactly two double-Green bits for \(I_k\))

Let \(T=2^{k-1}\) and \(k\ge 4\). Packed bit \(p\) is double-Green on
the dyadic annulus iff \(p=3T/2+1\) (times \(T,3T/2\)) or
\(p=5T/8+1\) (times \(5T/4,3T/2\)). Both lie in the right packed
half \(p>T+1\), as required by even multiplicity (Cycle AN). This
upgrades Cycle AS’s prefix to a theorem. Certified on the annulus
for \(4\le k\le 8\).

The XOR of those two bits is not identically \(0\) (Cycle AV, \(k=12\)).

## All left-diagonals period 4 — killed

Cycles AM–AV closed \(e_8,\ldots,e_{17}\) as period 4. That pattern
does not continue: \(e_{29}\) has period 8 on \(t\ge 64\) (and
\(e_{28}\equiv 0\) is already a white stripe, Cycle AD). **Killed.**
Do not assume a uniform period-4 tail for every left-diagonal, and
do not hunt another finite nested-left family as a formula for
\(I_k\).

## Packed bit 33 fires at \(T\) — prefix

Bit \(p=33=2^5+1\) is the \(j=5\) unique \(2\)-family member, Green
only at \(t=T\). It fires for \(7\le k\le 12\). **Prefix**, not a
theorem: \(e_{32}\) and \(e_{33}\) are period 8 on a window, not a
closed form. Combined with bits 9, 13, 17 this still does not give
\(I_k\).

## Verdict

`LEMMA` (Mersenne double; \(5\)-double; no even doubles for \(a\ge 4\);
exactly two double \(D\); exactly two double-Green bits for \(I_k\)).
`PREFIX` (bit 33 fires at every \(T\)).
`KILLED` (all \(e_j\) eventually period 4).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_aw.md` (this note)
- `research/cycle_aw.py`
- `research/cycle_aw.json`
