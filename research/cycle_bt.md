# Cycle BT: freshman extras on non-dyadic covering blocks

For a power-of-two step \(M=2^a\), Freshman factorisation gives
\((1+x+x^2)^M=1+x^M+x^{2M}\) over \(\mathrm{GF}(2)\). The packed
Rule-150 image of the centre after \(M\) steps is therefore the
centre plus the two cells at spatial \(\pm M\), and the Rule-30
defect is the Green AND-parity \(J\) on that interval:

\[
c_{t+M}\oplus c_t
=x(t,M)\oplus x(t,-M)\oplus J_{[t,\,t+M)\to t+M},
\]

with \(x(t,j)=0\) outside the seed cone \(|j|>t\). Cycle AL is the
case \(t=2^k\) and \(M\ge 2t\), where both extras vanish. On the
covering blocks the start times are not dyadic: \(4U<6U\) and
\(8U<10U\), so the palindrome defects survive. The centre coboundary
\(\varphi^{(5)}_{k+1}\oplus\varphi^{(3)}_{k+1}\) equals the Green
AND-parity on \(B\) if and only if that defect vanishes, which it
does not identically. Not a prize claim: the Fermat covering remains
a prefix.

Helper: `python3 research/cycle_bt.py --certify` (~0.3s). Dump:
`research/cycle_bt.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Freshman for \(M=2^a\))

Over \(\mathrm{GF}(2)\), \((1+x+x^2)^{2^a}=1+x^{2^a}+x^{2^{a+1}}\).
Equivalently \(G(2^a,d)=1\) if and only if
\(d\in\{0,2^a,2^{a+1}\}\). Proof: the \(a=0\) case is
\(1+x+x^2\), and the doubling
\((1+x+x^2)^{2m}=(1+x^2+x^4)^m\) iterates. Certified \(a\le 12\).

## Lemma (general freshman defect)

Let \(M=2^a\) and \(t\ge 0\). Packed Rule 150 multiplies by
\(1+x^M+x^{2M}\), so the linear image of packed bit \(t+M\) is
packed bits \(t+M\), \(t\), and \(t-M\) of the row at time \(t\),
i.e. the cells \(x(t,M)\), \(c_t\), and \(x(t,-M)\) (zero if the
packed index lies outside \([0,2t]\)). The AND remainder on
\([t,t+M)\) targeting packed bit \(t+M\) is \(J\), hence the
displayed identity. Certified for \(0\le t\le 24\) and
\(0\le a\le 6\) with \(t+M\le 80\).

## Lemma (extras vanish on \(A\), survive on \(B\) and \(C\))

Let \(U=2^k\). Block \(A\) starts at the dyadic time \(2U\) with
step \(4U\). Then \(4U>2U\), so both extras lie outside the seed
cone and \(d_A:=x(2U,\pm 4U)=0\). Thus
\(\varphi^{(3)}_{k+1}=c_{6U}\oplus c_{2U}=J_A\). Certified as
inequalities for \(k\le 12\), and \(d_A=0\) on \(1\le k\le 8\).

Block \(B\) starts at \(6U\) with the same step \(4U<6U\), so both
cells live. Block \(C\) starts at \(10U\) with step \(8U<10U\).
Write \(d_B:=x(6U,-4U)\oplus x(6U,4U)\) and
\(d_C:=x(10U,-8U)\oplus x(10U,8U)\). Then

\[
\varphi^{(5)}_{k+1}\oplus\varphi^{(3)}_{k+1}
=c_{10U}\oplus c_{6U}
=J_B\oplus d_B,
\qquad
\varphi^{(9)}_{k+1}\oplus\varphi^{(5)}_{k+1}
=c_{18U}\oplus c_{10U}
=J_C\oplus d_C.
\]

Certified as identities for \(1\le k\le 6\), and the cone
inequalities for \(k\le 12\).

## Lemma (\(d_B\) is a Green remainder on \(A\))

The same freshman step of length \(4U\) from the dyadic time \(2U\)
has vanishing extras, so

\[
x(6U,-4U)=c_{2U}\oplus J_A^{\to 2U},
\qquad
x(6U,4U)=c_{2U}\oplus J_A^{\to 10U},
\]

where \(J_A^{\to p}\) is the Green AND-parity on \([2U,6U)\)
targeting packed bit \(p\) at time \(6U\). The centres cancel, and
\(d_B=J_A^{\to 2U}\oplus J_A^{\to 10U}\). Certified \(1\le k\le 6\).

## Lemma (corrected covering failure)

Cycle BQ’s centre form still stands: covering fails at \(k+1\) iff
\(\varphi^{(3)}_{k+1}=\varphi^{(5)}_{k+1}=\varphi^{(9)}_{k+1}=0\).
Substituting the freshman identities, this is

\[
J_A=0
\qquad\text{and}\qquad
J_B=d_B
\qquad\text{and}\qquad
J_C=d_C.
\]

Identifying those centre coboundaries with the raw Green AND-parities
\(J_B\) and \(J_C\) (Cycle BQ’s \(S_B,S_C\)) is equivalent to
\(d_B=d_C=0\), which is not identically true. Certified equivalent
on \(1\le k\le 6\). Cycle BO’s even-spine criterion is unchanged: it
is a statement about the \(\varphi\) values themselves.

## Defects are not identically 0 — killed

On \(1\le k\le 8\),

- \(d_B=\) `01100111`
- \(d_C=\) `00010010`

Both take both values. **Killed** as identically-0 (or identically-1)
productions, and as a justification for dropping the extras.
\(\varphi^{(5)}_{k+1}\oplus\varphi^{(3)}_{k+1}=J_B\) already fails
at \(k=2\). **Killed.**

## Verdict

`LEMMA` (Freshman for \(M=2^a\); general freshman defect; extras
vanish on \(A\) and survive on \(B,C\); \(d_B=J_A^{\to 2U}\oplus
J_A^{\to 10U}\); covering fails iff \(J_A=0\) and \(J_B=d_B\) and
\(J_C=d_C\)).
`KILLED` (\(d_B\equiv 0\); \(d_C\equiv 0\); centre coboundary equals
\(J_B\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bt.md` (this note)
- `research/cycle_bt.py`
- `research/cycle_bt.json`
