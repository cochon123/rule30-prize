# Cycle Z: dyadic half-step for \(b_k=c_{2^k}\)

One lemma unfolding a doubling of packed Rule 150, plus kill criteria
for local formulas of the AND remainder. Not a prize claim:
\((b_k)\) is still not proved non-eventually-constant.

Helper: `python3 research/cycle_z.py --certify`. Dump:
`research/cycle_z.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (half-step)

Let \(T=2^{k-1}\) and let \(P(x)\) be the packed row at time \(T\).
Pure Rule 150 for \(T\) steps multiplies by \(1+x^T+x^{2T}\) (Freshman).
The coefficient of \(x^{2T}\) in \(P\cdot(1+x^T+x^{2T})\) is

\[
[x^{0}]P\oplus[x^{T}]P\oplus[x^{2T}]P.
\]

Bit \(0\) is the left edge \(x(T,-T)=1\), bit \(2T\) is the right edge
\(x(T,T)=1\), and bit \(T\) is the centre \(b_{k-1}\). Hence the linear
image of the whole half-time row at the next dyadic centre is exactly
\(b_{k-1}\). Packed Rule 30 is Rule 150 XOR adjacent ANDs (Cycle Y), so

\[
b_k=b_{k-1}\oplus I_k,
\]

where \(I_k\) is the Green parity of all AND injections in the time
interval \([T,2T)\):

\[
I_k=\bigoplus_{j=0}^{T-1}
[x^{2T}]\Bigl(A_{T+j}\,(1+x+x^2)^{T-1-j}\Bigr),
\]

\(A_t=(\mathrm{row}_t{\ll}1)\land\mathrm{row}_t\). In particular
\((b_k)\) is eventually constant if and only if \(I_k\) is eventually
\(0\).

Certified: linear edges and \([x^{2T}]\) identity for \(k=1,\ldots,12\);
independent evaluation of the AND sum equals \(b_k\oplus b_{k-1}\) for
\(k=1,\ldots,10\). On that prefix \(I_k\) is \(1\) eight times and \(0\)
four times (last 1 at \(k=12\)), which is finite evidence, not a proof
that \(I_k\) is not eventually \(0\).

## Local formulas for \(I_k\) — killed

At time \(T\), none of \(\ell,c,r,c\land r,\ell\oplus r\) equals \(I_k\)
for every \(k\le 10\). The unweighted parity of 11-pairs in the second
half disagrees with \(I_k\) (already at \(k=1\)). The right-edge AND
\(x(T,T-1)\) is \(0\) for every \(k\ge 2\) (right-edge 1-run has length
1 at dyadic times, as in Cycle W), so it never fires as a universal
witness.

Contributing 11-pairs are not local: their spatial range at \(k=7\) is
already \((-61,57)\), comparable to the light cone. The number of
Green-hitting times grows \(1,1,0,2,7,17,22,68,115,261\).

The sparse slice \(m=2^a\) (three packed bits by Freshman) equals \(I_k\)
for some odd \(k\) and fails for even \(k\le 8\). It is not a closed form.

## Verdict

`LEMMA` (half-step \(b_k=b_{k-1}\oplus I_k\)). `KILLED` (local \(I_k\),
11-parity, right-edge AND). `OPEN` (eventual constancy of \((b_k)\)).
Wall time 0.03s. Prize unsolved.

## Files

- `research/cycle_z.md` (this note)
- `research/cycle_z.py`
- `research/cycle_z.json`
