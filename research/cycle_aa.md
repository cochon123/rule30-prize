# Cycle AA: every centre-right AND hits \(I_k\)

One production that contributes at every time of a dyadic annulus, plus
kill criteria for taking that production as a closed form. Not a prize
claim: the off-centre remainder still cancels the production on some
\(k\), and \((b_k)\) is still not proved non-eventually-constant.

Helper: `python3 research/cycle_aa.py --certify`. Dump:
`research/cycle_aa.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (central trinomial)

Over \(\mathrm{GF}(2)\),

\[
G(m,m)\,:=\,[x^m](1+x+x^2)^m \;=\; 1
\qquad(m\ge 0).
\]

Proof by the doubling recurrence of \(G\): \(G(0,0)=1\);
\(G(2n,2n)=G(n,n)\); and for odd degree,
\(G(2n+1,2n+1)=G(n,n)\). Certified on \(m<2^{10}\). Palindrome
\(G(m,d)=G(m,2m-d)\) holds as well (the polynomial is reciprocal of
degree \(2m\)).

## Lemma (hitting production)

Write \(T=2^{k-1}\) and \(m=2T-1-t\). An AND at packed bit \(p\) at
time \(t\) contributes to \(I_k\) iff \(G(m,2T-p)=1\). The centre-right
pair is packed bits \(t\) and \(t+1\), so \(p=t+1\) and
\(2T-p=m\). Since \(G(m,m)=1\), **every** bit \(c_t\land r_t\) with
\(t\in[T,2T)\) contributes to \(I_k\). Hence

\[
I_k
=\bigoplus_{t=T}^{2T-1}(c_t\land r_t)
\;\oplus\;
R_k,
\]

where the remainder \(R_k\) is the Green parity of all AND injections
in the same interval with spatial offset \(\delta\neq 0\) (consecutive
cells at positions \(\delta,\delta+1\)). Certified against
\(b_k\oplus b_{k-1}\) for \(k\le 10\).

## Remainder does not vanish — killed as a closed form

If \(R_k\) were identically \(0\), then \(I_k\) would be the parity of
centre-right 11s on the annulus. This already fails at \(k=3\)
(\(I_3=0\) but a single \(c\land r\) fires). On \(k\le 10\) the two
sides disagree at \(k=3,5,6,8,9\). Off-centre hits are not sparse:
\(n_{\mathrm{other}}=0,0,1,6,33,95,314,1015,3445,11322\).

## Lemma (leftmost 11 never hits)

For every \(t\ge 0\), the left edge satisfies \(x(t,-t)=1\), and the
update gives \(x(t+1,-t)=0\oplus(1\lor x(t,-t+1))=1\). Thus packed bit
1 is identically 1 for \(t\ge 1\), and \(A_t\) always contains packed
bit 1 (the leftmost 11). For \(t\in[T,2T)\) one has \(m\le T-1\), so
\(2m\le 2T-2<2T-1=2T-p\) at \(p=1\). The Green function cannot carry
this 11 to the next dyadic centre. Certified: the bit is 1 on
\(1\le t<2^{12}\), and it contributes 0 to \(I_k\) for \(k\le 10\).

## Lemma (near-central trinomial)

\(G(m,m-1)=G(m,m+1)=v_2(m+1)\bmod 2\). Proof: both vanish for even
\(m\) (odd degree, or \(v_2(\mathrm{odd})=0\)); for \(m=2n+1\),
\(G(2n+1,2n)=1\oplus G(n,n-1)\) and
\(v_2(2n+2)=1+v_2(n+1)\). Palindrome gives the \(m+1\) case. Certified
on \(m<2^9\). In particular the pairs \(\ell\land c\) and
\(r\land x(t,2)\) contribute iff \(v_2(2T-t)\) is odd — a thin set,
not the whole remainder.

## Local formulas — killed

No 3-window bit at the Mersenne times \(2^k-1\) or \(2^k-2\) (including
the \(m=1\) Freshman XOR of three ANDs) equals \(I_k\) for every
\(k\le 12\). \(I_k\) is not periodic of period \(\le 4\) and is not
the Fibonacci recurrence \(I_k=I_{k-1}\oplus I_{k-2}\). Cycle Z already
killed the half-time 3-window, unweighted 11-parity, right-edge AND,
and the unweighted sparse slice \(m=2^a\).

## Verdict

`LEMMA` (central trinomial; \(c\land r\) hits \(I_k\); leftmost 11
never hits; \(G(m,m-1)=v_2(m+1)\bmod 2\)). `KILLED` (\(I_k\) equals
the \((c\land r)\) parity; Mersenne locals; small recurrences).
`OPEN` (eventual constancy of \((b_k)\)). Wall time 0.17s. Prize unsolved.

## Files

- `research/cycle_aa.md` (this note)
- `research/cycle_aa.py`
- `research/cycle_aa.json`
