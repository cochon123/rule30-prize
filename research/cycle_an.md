# Cycle AN: dyadic \(W\); Mersenne and Fermat \(G\); cone split of \(I_k\)

Cycle AM evaluated two dyadic prefix XORs by doubling. The generating
function of \(W(n,D)=\bigoplus_{m<n}G(m,D)\) is closed, and at
\(n=2^a\) it is an interval of length \(2^a\). The same identity
gives the Mersenne and Fermat Green coefficients and
\(W(3\cdot 2^a,\cdot)\). The interval of \(W(2^{k-1},\cdot)\) splits
\(I_k\) into packed-index halves. Not a prize claim: \(I_k=1\)
infinitely often remains open.

Helper: `python3 research/cycle_an.py --certify` (~3.8s). Dump:
`research/cycle_an.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (generating function of \(W\))

Over \(\mathrm{GF}(2)\), for any \(r\) and \(n\ge 0\),

\[
(1+r)\sum_{m<n}r^m \;=\; 1+r^n.
\]

Take \(r=1+x+x^2\). Then \(1+r=x(1+x)\), so

\[
x(1+x)\sum_{m<n}(1+x+x^2)^m \;=\; 1+(1+x+x^2)^n.
\]

Equating coefficients, \(G(n,D)=W(n,D-1)\oplus W(n,D-2)\) for every
\(D\ge 1\). Certified \(n\le 48\).

## Lemma (\(W(2^a,D)\) is an interval)

Freshman: \((1+x+x^2)^{2^a}=1+x^{2^a}+x^{2^{a+1}}\). The right-hand
side of the generating-function identity is \(x^{2^a}+x^{2^{a+1}}\),
hence

\[
\sum_D W(2^a,D)\,x^D
= x^{2^a-1}\frac{1+x^{2^a}}{1+x}
= x^{2^a-1}\sum_{j=0}^{2^a-1}x^j
= \sum_{D=2^a-1}^{2^{a+1}-2}x^D,
\]

using \(1+x^{2^a}=(1+x)^{2^a}\). Therefore \(W(2^a,D)=1\) if and only
if \(2^a-1\le D\le 2^{a+1}-2\), and \(0\) otherwise. Certified
\(a\le 10\). Cycle AM’s identities \(W(2^a,2^{a+1}-2)=1\) and
\(W(2^a,2^{a+1}-3)=1\) (\(a\ge 1\)) are the right endpoint and its
neighbour.

If a packed bit \(p\in[2,T+1]\) with \(T=2^{k-1}\) fired at every time
of the annulus, its contribution to \(I_k\) would be
\(W(T,2T-p)=1\). Packed bit \(1\) has target \(2T-1\), one past the
interval, recovering that the leftmost-11 XOR over the whole annulus
is \(0\) (Cycle AA is stronger: each individual Green coefficient
vanishes).

## Lemma (Mersenne \(G(2^a-1,d)\))

\((1+x+x^2)^{2^a-1}=(1+x^{2^a}+x^{2^{a+1}})/(1+x+x^2)\) in
\(\mathrm{GF}(2)[[x]]\). The inverse is
\((1+x)\sum_{k\ge 0}x^{3k}\), because
\((1+x+x^2)(1+x)=1+x^3\). Write \(f(n)=1\) iff \(n\ge 0\) and
\(n\not\equiv 2\pmod{3}\). Then

\[
G(2^a-1,d)=f(d)\oplus f(d-2^a)\oplus f(d-2^{a+1}).
\]

For \(0\le d\le 2^{a+1}-2\) the last term vanishes, and the remaining
XOR is piecewise:

- \(d<2^a\): \(1\) iff \(d\not\equiv 2\pmod{3}\);
- \(d\ge 2^a\) and \(a\) even: \(1\) iff \(d\not\equiv 1\pmod{3}\);
- \(d\ge 2^a\) and \(a\) odd: \(1\) iff \(d\not\equiv 0\pmod{3}\).

Palindrome at time \(T=2^a\) is \(G(T-1,2T-p)=G(T-1,p-2)\). Certified
\(a\le 10\).

## Lemma (Fermat \(G(2^a+1,d)\))

\((1+x+x^2)^{2^a+1}=(1+x^{2^a}+x^{2^{a+1}})(1+x+x^2)\). Hence
\(G(2^a+1,d)=1\) iff an odd number of \(\{d,\,d-2^a,\,d-2^{a+1}\}\)
lie in \(\{0,1,2\}\). Certified \(a\le 8\).

## Lemma (\(W(3\cdot 2^a,D)\) is two intervals)

Let \(U=2^a\). Over \(\mathrm{GF}(2)\),

\[
(1+x^U+x^{2U})^3=1+x^U+x^{3U}+x^{5U}+x^{6U},
\]

so \(1+r^{3U}=x^U+x^{3U}+x^{5U}+x^{6U}\) and

\[
\sum_D W(3U,D)\,x^D
= x^{U-1}\Bigl(\sum_{j<2U}x^j + x^{4U}\sum_{j<U}x^j\Bigr).
\]

Thus \(W(3\cdot 2^a,D)=1\) iff
\(D\in[U-1,\,3U-2]\cup[5U-1,\,6U-2]\). Certified \(a\le 8\).

## Lemma (cone split of \(I_k\))

Write \(T=2^{k-1}\). Packed bit \(0\) never fires. Packed bit \(1\)
never Green-hits \(I_k\) (Cycle AA). The remaining hits split as
\(I_k=I_k^{\mathrm{left}}\oplus I_k^{\mathrm{right}}\), where left
uses packed bits \(p\in[2,T+1]\) (the \(W(T,\cdot)\) support) and
right uses \(p\ge T+2\). Certified \(3\le k\le 12\), including
\(n_{01}=0\).

Almost all of Cycle AA’s centre-right production \(c_t\land r_t\)
(packed bit \(p=t+1\)) lies in the right half: only \(t=T\) has
\(p=T+1\) on the left boundary.

On \(7\le k\le 12\) one has \(I_k^{\mathrm{left}}=0\), hence
\(I_k=I_k^{\mathrm{right}}\). This is a certified prefix, not a
theorem: a vanishing of length 6 is shorter than the Cycle AL 7-term
spine accident that died at \(k=16\). **Not claimed.**

## Time-\(T\) slice — killed as a formula for \(I_k\)

At \(t=T\), the degree is Mersenne, so the slice is the XOR of firing
packed bits \(p\) with \(G(T-1,p-2)=1\). For \(p<T+2\) that filter is
\(p\not\equiv 1\pmod{3}\). The slice equals \(I_k\) at some \(k\) and
not others (fails at \(k=5,7,8,9,11,12\)). The unique packed-bit-4
and bit-6 hits of Cycle AM both occur at \(t=T+1\) and cancel locally
there; other \(T+1\) hits exist for \(k\ge 5\). **Killed** as a closed
form for \(I_k\).

## Verdict

`LEMMA` (dyadic \(W\) interval; \(G=W\) shift; Mersenne mod-3;
Fermat 3-sparse; \(W(3\cdot 2^a)\) two intervals; \(I_k\) cone split).
`PREFIX` (\(I^{\mathrm{left}}=0\) for \(7\le k\le 12\)).
`KILLED` (time-\(T\) slice as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_an.md` (this note)
- `research/cycle_an.py`
- `research/cycle_an.json`
