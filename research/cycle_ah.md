# Cycle AH: odd-spine half-step and power-of-2 periods

Cycle Z unfolds one doubling of the dyadic centre \(b_k=c_{2^k}\).
The same Freshman factorisation works at every odd multiple
\(q\cdot 2^k\). Eventual period \(2^m\) forces \((b_k)\) eventually
constant, so a non-vanishing \(I_k\) would kill every power-of-2
period (including period 2 and isolated-zero \(q=3\)). The one-step
Green remainder is local, completing Cycle AF’s \(m=0\) case. Not a
prize claim: \(I_k\) is still not proved non-eventually-zero.

Helper: `python3 research/cycle_ah.py --certify`. Dump:
`research/cycle_ah.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (odd-spine half-step)

Let \(U=2^k\) and let \(q\ge 1\). Over \(\mathrm{GF}(2)\),

\[
(1+x+x^2)^{qU}
=\bigl((1+x+x^2)^q\bigr)^{U}
=Q(x^{U}),
\qquad
Q:=(1+x+x^2)^q,
\]

by the Freshman dream (\(U\) is a power of 2). \(Q\) has degree \(2q\),
with \(Q_0=Q_{2q}=1\) and \(Q_q=G(q,q)=1\) (Cycle AA). The Rule 150
image of the packed row \(P\) at time \(qU\), read at packed bit
\(2qU\) (the centre at time \(2qU\)), is therefore

\[
\bigoplus_{i:\,Q_i=1}P[(2q-i)U]
=\bigoplus_{i:\,Q_i=1}x(qU,(q-i)U).
\]

The summands \(i=0\) and \(i=2q\) are the right and left light-cone
edges, both 1. The summand \(i=q\) is the centre \(c_{qU}\). The
remainder is a palindrome-defect XOR of the extra \(Q\)-support:

\[
\Delta^{(q)}_k
=\bigoplus_{\substack{i\in\mathrm{supp}(Q)\\ i\notin\{0,q,2q\}}}
x\bigl(qU,(q-i)U\bigr).
\]

Packed Rule 30 is Rule 150 XOR adjacent ANDs (Cycle Y), so

\[
c_{2qU}
=c_{qU}\oplus\Delta^{(q)}_k\oplus J^{(q)}_k,
\]

where \(J^{(q)}_k\) is the Green parity of AND injections on the
interval \([qU,2qU)\). Even \(q\) is a coarser sampling of a smaller
odd spine (\(q=2\) is the \(q=1\) spine shifted by one doubling).

For \(q=1\), \(\mathrm{supp}(Q)=\{0,1,2\}\) has no extras, so
\(\Delta^{(1)}=0\) and this is Cycle Z: \(b_{k+1}=b_k\oplus I_{k+1}\).
For \(q=3\), \(Q=1+x+x^3+x^5+x^6\) and the extras are the single pair
at spatial offset \(\pm 2U\):

\[
\Delta^{(3)}_k
=x(3U,2U)\oplus x(3U,-2U).
\]

Certified: Freshman identity \(Q(x^{U})=(1+x+x^2)^{qU}\) for
\(q\in\{1,3,5,7,9\}\) and \(k\le 8\); the half-step against packed
Rule 30 for those \(q\) on \(k\le 9,8,7,6,7\) respectively; edges
cancel and the centre term matches \(G(q,q)=1\).

## \(\Delta\) or \(J\) as a closed form — killed

On those prefixes neither \(\Delta^{(q)}\) nor \(J^{(q)}\) is
identically 0 for \(q\in\{3,5,7\}\), and neither alone equals the
spine flip \(c_{qU}\oplus c_{2qU}\). For \(q=9\),
\(\mathrm{supp}(Q)=\{0,1,2,8,9,10,16,17,18\}\) and \(\Delta^{(9)}_k=0\)
through \(k=7\), but \(\Delta^{(9)}_8=1\). **Killed** as identically
zero, and as a formula for the flip without the AND remainder. The
\(q=1\) case remains \(\Delta=0\) by empty extras, not by a
palindrome.

The \(n_*=3\) kernel disagreements of Cycle V (at \(k=2,6\)) are
exactly the scanned double zeros of \(I\), and on those two times the
3-spine does flip (\(\Delta^{(3)}\oplus J^{(3)}=1\)). That is finite
evidence, not a proof that a vanishing \(I\) still splits the kernel
at \(n=3\).

## Lemma (period constraint on \((b_k)\))

Suppose \(c\) is eventually periodic of period \(p=2^m r\) with \(r\)
odd, onset \(T\). For \(k\ge k_0:=\max(m,\min\{j:2^j\ge T\})\) one has
\(2^k\ge T\) and \(2^k=2^m\cdot 2^{k-m}\), so

\[
(2^k-T)\bmod p
=\bigl(2^m\cdot(2^{k-m}\bmod r)-(T\bmod p)\bigr)\bmod p.
\]

Since \(\gcd(2,r)=1\), the sequence \(2^{k-m}\bmod r\) is purely
periodic of period \(\mathrm{ord}_r(2)\). Hence
\((b_k)_{k\ge k_0}=(c_{2^k})_{k\ge k_0}\) is eventually periodic with
period dividing \(\mathrm{ord}_r(2)\). In particular \(r=1\) (any
eventual period \(2^m\), including the constant sequence and the
isolated-zero periods of length 2 and 4) forces \((b_k)\) eventually
constant, equivalently \(I_k\) eventually 0 (Cycle Z).

Certified on synthetic eventual periods
\((m,r)\in\{(0,1),(1,1),(2,1),(3,1),(0,3),(1,3),(0,5),(2,5),(0,7),(0,9),(1,9)\}\)
with onset 5: the sampled \((b_k)\) has period dividing
\(\mathrm{ord}_r(2)\), and is constant when \(r=1\). Orders:
\(\mathrm{ord}_1(2)=1\), \(\mathrm{ord}_3(2)=2\),
\(\mathrm{ord}_5(2)=4\), \(\mathrm{ord}_7(2)=3\),
\(\mathrm{ord}_9(2)=6\).

This is the precise constraint behind Cycle W’s observation that
aperiodicity of \((b_k)\) implies aperiodicity of \(c\). The new cut
is the \(r=1\) case: **if \(I_k=1\) infinitely often, then \(c\) is
not eventually period \(2^m\) for any \(m\ge 0\)**. Periods 3, 5, 6, 7
and isolated-zero \(q=8\) (period 9) would remain, because they have
an odd factor. A non-eventually-constant \(q\)-spine likewise kills
every pure power-of-2 period, since \(q\cdot 2^k\equiv 0\pmod{2^m}\)
for \(k\ge m\); that is the same \(r=1\) obstruction, not a new family.

## Lemma (one-step Green remainder is local)

\(G(0,d)=1\) iff \(d=0\), so the only time-\(t\) AND that Green-hits
\(c_{t+1}\) is packed bit \(t+1\), i.e. \(c_t\land r_t\). Thus

\[
c_{t+1}=1\oplus(c_t\land r_t)\oplus O^{(1)}_t,
\]

with \(O^{(1)}_t\) the Green parity of older AND injections. On the
prize orbit the 3-window determines \(c_{t+1}\), and solving gives
\(O^{(1)}_t=1\oplus\ell_t\oplus c_t\oplus r_t\). Certified: Green
matches this Boolean for \(t<40\), zero failures. A centre `00` is
then \((c,O^{(1)})=(0,1)\), which is \(\ell=r\) with \(c=0\), i.e.
Cycle AB’s \((c,d)=(0,0)\). The annulus XOR of \(O^{(1)}\) is not
\(I_k\) (fails at \(k=1,3,5,6,8,9,10\)). **Killed** as a bulk `00`
handle and as a formula for \(I_k\).

## Verdict

`LEMMA` (odd-spine half-step, including Cycle Z as \(q=1\); period
constraint on \((b_k)\), with power-of-2 periods forcing eventual
constancy; one-step \(O^{(1)}\) local). `KILLED` (\(\Delta\) or \(J\)
as a closed form for \(q\in\{3,5,7,9\}\); \(O^{(1)}\) as \(I_k\) or a
bulk `00` handle). `OPEN` (eventual vanishing of \(I_k\); infinitely
many `00`s). Prize unsolved.

## Files

- `research/cycle_ah.md` (this note)
- `research/cycle_ah.py`
- `research/cycle_ah.json`
