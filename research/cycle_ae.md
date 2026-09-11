# Cycle AE: no right white stripes; Green defect; nested-right kill

Cycle AD produced white stripes on the left and killed bounded-depth
nested left as a centre-`00` production. The right-diagonals
\(u(t,k)=x(t,t-k)\) are the chiral dual: each is a pure integrator, so
the only eventually-constant one is the right edge. Nested right
therefore cannot occupy the centred 5-window infinitely often either.
A 1-run ending is followed by `00` iff \(x(t,-2)=r_t\lor x(t,2)\). The
palindrome defect \(d=\ell\oplus r\) is the Green difference of AND
injections to packed bits \(t-1\) and \(t+1\). Not a prize claim:
infinitely many `00`s still need a bulk production.

Helper: `python3 research/cycle_ae.py --certify`. Dump:
`research/cycle_ae.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (right-diagonals are integrators)

Rowland’s coordinates \(u(t,k)=x(t,t-k)\) (packed bit \(2t-k\)) obey

\[
u(t+1,k)=u(t,k)\oplus\bigl(u(t,k-1)\lor u(t,k-2)\bigr)
\]

with \(u(*,k)=0\) for \(k<0\) and \(u(t,0)=1\). Certified on \(t<64\).
The bit being updated is XOR’d with a function of strictly smaller
\(k\); it is never reset. This is the opposite of Cycle AD’s left
recurrence \(e_j'=e_{j-2}\oplus(e_{j-1}\lor e_j)\), which can forget
\(e_j\) when \(e_{j-1}=1\).

## Lemma (no right white stripe)

The only eventually-constant right-diagonal is \(u(*,0)\equiv 1\).

Proof: for \(k=1\), the forcing is \(u_0\lor u_{-1}=1\), so \(u_1\)
toggles; likewise \(k=2\) has forcing \(u_1\lor u_0=1\). Certified
\(t<128\), with \(u(1,1)=1\). For \(k\ge 3\), if every \(u_j\) with
\(1\le j<k\) takes both values infinitely often, then
\(u_{k-2}\) has infinitely many 1s, the forcing has infinitely many 1s,
and \(u_k\) flips infinitely often. Thus no \(k\ge 1\) is eventually
constant: there are no white stripes parallel to the right light cone.
Certified: for \(1\le k\le 12\) the prefix through \(t=128\) already
takes both values, while \(k=0\) is identically 1.

Rowland’s theorem (period dividing \(2^k\)) permits period 1; the
integrator induction rules that out for \(k\ge 1\). Cycle AD’s extra
left stripes \(e_7,e_{28}\) have no right analogue.

## Lemma (finite incidence on the right)

The spatial coordinate of \(u(t,k)\) is \(t-k\), which lies in the
centred 5-window \([-2,2]\) iff \(t\in[k-2,k+2]\), at most five times.
No finite family of right-diagonals can occupy that window infinitely
often. Together with Cycle AD, neither nested edge of bounded depth
is a `00` production. The remaining region is the bulk, where both
the left offset \(j\) and the right offset \(k\) grow with \(t\).

## Lemma (Green formula for \(d\))

Rule 150 from a single 1 is palindromic, and
\(G(t,t-1)=G(t,t+1)\) (Cycle AA), so the linear parts of \(\ell_t\)
and \(r_t\) cancel. An AND at packed bit \(p\) at time \(s\) injects
into row \(s+1\) and contributes \(G(t-s-1,\,q-p)\) to packed bit
\(q\) at time \(t\). Hence

\[
d_t
=\bigoplus_{(s,p)}
\Bigl(
G(\Delta,t-1-p)\oplus G(\Delta,t+1-p)
\Bigr),
\qquad
\Delta=t-s-1.
\]

Certified against packed \(\ell\oplus r\) for \(1\le t<40\), and the
matching centre formula \(c_t=G(t,t)\oplus\bigoplus G(\Delta,t-p)\)
against packed \(c\). This rewrites Cycle AB’s remainder
\(R_k=\bigoplus d\) as a Green difference; it is not a closed form for
\(I_k\) (the annulus still mixes every offset).

## Lemma (`00` after a 1-run ending)

At a time with \((c,\ell)=(1,1)\) one has \(c'=0\). The next bit is 0
iff \(\ell'=r'\). Expanding gives \(\ell'=x(t,-2)\oplus 1\) and
\(r'=1\oplus(r\lor x(t,2))\), so \(c''=0\) iff
\(x(t,-2)=r\lor x(t,2)\). This is the four-window quartet of Cycle AD
as a single Boolean. Certified: zero mismatches on \(t<256\).

## Nested right — killed as a `00` production

A fixed-\(k\) right-diagonal hits the origin at \(t=k\) and the
centred 5-window only in \([k-2,k+2]\). There is no right white stripe
to grow a family of eventual zeros toward the centre. **Killed.**

## Verdict

`LEMMA` (right integrator; no right white stripe; finite incidence;
Green \(d\); `00` iff \(a=r\lor e\)). `KILLED` (nested-right 5-window
`00`; right white stripes like the left; Green \(d\) as a formula for
\(I_k\)). `OPEN` (infinitely many `00`s). Wall time 0.01s. Prize
unsolved.

## Files

- `research/cycle_ae.md` (this note)
- `research/cycle_ae.py`
- `research/cycle_ae.json`
