# Cycle AB: annulus coboundary for \(I_k\), defect remainder

The Green remainder of Cycle AA is a local column parity. One lemma that
\(d=\ell\oplus r\) cannot die out; spatial vacuums do not produce the
observed centre runs. Not a prize claim: \(I_k\) is still not proved
non-eventually-zero, and infinitely many centred `000`s (which would
kill every isolated-zero eventual period, including period 2) are
unproved.

Helper: `python3 research/cycle_ab.py --certify`. Dump:
`research/cycle_ab.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (annulus coboundary)

The Rule 30 update is \(c'=\ell\oplus(c\lor r)=\ell\oplus c\oplus r\oplus(c\land r)\),
hence

\[
c_t\oplus c_{t+1}
=\ell_t\oplus r_t\oplus(c_t\land r_t).
\]

Summing over the dyadic annulus \(t\in[T,2T)\) with \(T=2^{k-1}\)
telescopes on the left:

\[
I_k
=c_T\oplus c_{2T}
=\bigoplus_{t=T}^{2T-1}
\bigl(\ell_t\oplus r_t\oplus(c_t\land r_t)\bigr).
\]

Cycle Z killed every 3-window formula at the single time \(T\). The
same window, **summed** over the annulus, is exactly \(I_k\). Certified
for \(k\le 16\). Combined with Cycle AA (every \(c\land r\) Green-hits),

\[
R_k
=\bigoplus_{t=T}^{2T-1} d_t,
\qquad
d_t=\ell_t\oplus r_t.
\]

So the off-centre Green remainder is the palindrome-defect parity on
the annulus. Certified for \(k\le 16\).

## Lemma (\(d\) is not eventually 0)

If \(\ell=r\) for all large \(t\), then \(c'=c\oplus(c\land\ell)\). Any
later centre 0 stays 0 forever, contradicting infinitely many 1s in
\(c\). Thus \(c\) would be eventually all 1s, contradicting infinitely
many 0s. Therefore \(d_t=1\) for infinitely many \(t\): the remainder
is not a finite perturbation of \(\bigoplus(c\land r)\). This does not
make \(R_k=1\) infinitely often (dyadic block parities of \(d\) may
still vanish).

Eventual \(d=1\) would forbid centre `00` after onset. That is the
isolated-zero regime, not yet excluded.

## Centred `000` and isolated zeros

A centre `00` is exactly a time with \((c,d)=(0,0)\), i.e. the spatial
triple about the origin is `000`. Infinitely many such times would
kill every eventual isolated-zero period \(01^q\), including period 2
(\(q=1\)) and the remaining \(q=8\). One `00` occurs already in the
known 20-bit prefix; on \(t<2^{16}\) there are 16211 centred `000`s
and a longest 0-run of length 19. That is finite evidence, not a
proof of infinitely many `000`s.

While \(c=0\), the 0-run continues iff \(\ell=r\). Certified: no
counterexample on \(t<2^{16}\).

## Spatial vacuums — killed as a run construction

A spatial vacuum of radius \(W\) about the origin (zeros on
\((-W,W)\)) yields a centre 0-run of length at most \(W\). On
\(t<2^{16}\) the largest such radius is 7 (at \(t=5808\)), while the
longest centre 0-run has length 19. Long runs are \(\ell=r\) with
\(c=0\) without a wide vacuum. No scaled gadget is offered.

The annulus parities of \(\ell\) and of \(r\) separately are not
\(I_k\). Cycle AA already killed \(I_k=\bigoplus(c\land r)\).

## Verdict

`LEMMA` (annulus coboundary; \(R_k=\bigoplus d\); \(d\) not eventually
0). `KILLED` (vacuum-run construction; \(I_k\) equals \(\rho_k\),
\(\lambda_k\), or the \((c\land r)\) parity). `OPEN` (eventual
constancy of \((b_k)\); infinitely many `000`; unbounded runs).
Wall time 0.65s. Prize unsolved.

## Files

- `research/cycle_ab.md` (this note)
- `research/cycle_ab.py`
- `research/cycle_ab.json`
