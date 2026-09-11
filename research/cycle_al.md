# Cycle AL: all-q spines; edges cancel; \(P(q)=1\oplus\mathrm{wt}(q)\)

Cycle AK stated the identity
\(\varphi^{(q)}_k=c_{q\cdot 2^k}\oplus c_{2^k}=J\) only for Fermat-odd
\(q=2^a+1\), via a single Cycle-AI step whose extras lie off the cone.
The same identity holds for **every** integer \(q\ge 1\). The XOR of
leftmost-11 Green hits on \([2^k,q\cdot 2^k)\) is independent of \(k\)
and equals \(1\oplus\mathrm{popcount}(q)\), so the forced-1 production
of Cycle AK is the even-Hamming-weight case, not a Fermat monopoly.
Odd \(p=1\) parity is **not** a general-\(q\) production (\(q=7\) has
parity 0). Not a prize claim: some \(\varphi^{(q)}_k=1\) infinitely
often is unproved.

Helper: `python3 research/cycle_al.py --certify`. Dump:
`research/cycle_al.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (all-\(q\) identity)

Let \(U=2^k\) and \(q\ge 1\). Packed Rule 150 for \(M=(q-1)U\) steps
multiplies by \((1+x+x^2)^M=Q_{q-1}(x^U)\) with
\(Q_m=(1+x+x^2)^m=\sum_i G(m,i)\,x^i\). The image of packed bit
\(qU\) (the centre at time \(qU\)) is a sum of packed bits
\((q-i)U\) of the row at time \(U\). Those lie in the light cone
\([0,2U]\) iff \(i\in\{q-2,q-1,q\}\):

- \(i=q-1\): centre, coefficient \(G(q-1,q-1)=1\);
- \(i=q\): left edge \(x(U,-U)\), coefficient \(G(q-1,q)\);
- \(i=q-2\): right edge \(x(U,U)\), coefficient \(G(q-1,q-2)\).

The near-diagonal evaluations are
\(G(m,m\pm 1)=v_2(m+1)\bmod 2\) (doubling: even \(m\) forces both
sides 0 because the target is odd; odd \(m=2n+1\) reduces to
\(G(n,n+1)\oplus 1\), matching \(v_2(m+1)=1+v_2(n+1)\)). Thus
\(G(q-1,q)=G(q-1,q-2)=v_2(q)\bmod 2\). Both prize-orbit edges equal 1
for \(U\ge 1\), so the edge terms cancel, and the linear image is
exactly \(c_U\). The AND remainder on \([U,qU)\) targeting packed bit
\(qU\) is therefore the whole defect:

\[
c_{qU}=c_U\oplus J_{[U,qU)\to qU},
\qquad
\varphi^{(q)}_k:=c_{qU}\oplus c_U=J.
\]

Cycle Z is \(q=2\) (edges on the cone, still cancel). Cycles AJ/AK are
the Fermat-odd cases, where a single power-of-2 step already has extras
off-cone. Certified: identity and linear image \(=c_U\) for
\(q=1,\ldots,12\) and \(k\le 6\); near-diagonal \(G\) for \(m\le 80\).

## Lemma (odd \(q\): extras stay outside under chained AI)

Write \(q-1\) in binary and apply Cycle AI low-bits-first from time
\(U\). After bits \(<j\), the time is
\((1+((q-1)\bmod 2^j))U\). If bit \(j\) of \(q-1\) is set, extras sit
at \(\pm 2^j U\). These lie on or inside the cone iff
\(1+((q-1)\bmod 2^j)\ge 2^j\), iff \(q\equiv 0\pmod{2^j}\). For odd
\(q\) this never happens when \(j\ge 1\), so every extra is strictly
outside. Certified for odd \(q\le 31\) and \(k\le 4\). For \(q=2\) the
extras sit on the cone (Cycle Z).

## Lemma (\(P(q)=1\oplus\mathrm{wt}(q)\), independent of \(k\))

Packed bit 1 fires at every time \(s\ge 1\) (Cycle AA). It Green-hits
the target \(qU\) iff \(G(qU-s-1,qU-1)=1\). As \(s\) runs through
\([U,qU)\), the degree runs through \(\{0,\ldots,(q-1)U-1\}\), so the
hit parity is

\[
P_k(q):=\bigoplus_{m<(q-1)2^k}G\bigl(m,\,q\cdot 2^k-1\bigr).
\]

For \(k\ge 1\) the target is odd, even \(m\) drop, and odd doubling
yields \(P_k(q)=P_{k-1}(q)\). Thus \(P_k(q)=P_0(q)=P(q)\) with

\[
P(q)=\bigoplus_{m=0}^{q-2}G(m,q-1).
\]

The same doubling on \(P(q)\) gives \(P(q)=P(q/2)\) for \(q\) even and
\(P(q)=P((q-1)/2)\oplus 1\) for \(q\) odd. The unique solution with
\(P(1)=0\) is \(P(q)=1\oplus\mathrm{popcount}(q)\). Hence

\[
\varphi^{(q)}_k=P(q)\oplus S^{(q)}_k
\]

for every \(q\ge 1\), where \(S^{(q)}_k\) is the Green parity of hits
with packed bit \(\neq 1\). Fermat-odd \(q=2^a+1\) have popcount 2
(even), recovering Cycle AK. Certified: recurrence versus popcount
and versus \(P_0\) for \(q\le 80\); \(P_k(q)=P(q)\) for \(q\le 20\),
\(k\le 5\); on the prize orbit the packed-bit-1 hit parity equals
\(P(q)\) for \(q=1,\ldots,12\) and \(k\le 6\).

## Lemma (period \(2^m\) forces every integer spine to vanish)

If \(c\) is eventually period \(2^m\), then for all large \(k\) and
every integer \(q\ge 1\), both \(U\) and \(qU\) lie in the periodic
regime and \(qU-U=(q-1)2^k\) is a multiple of \(2^m\), so
\(\varphi^{(q)}_k=0\). In particular this includes every even-popcount
\(q\) (where \(P(q)=1\), so \(S^{(q)}\) would have to equal 1) and
every dyadic \(q=2^a\) (where \(\varphi^{(2^a)}_k=b_{k+a}\oplus b_k\),
recovering eventual constancy of \((b_k)\) from Cycle AH). Certified
on synthetic periods \(2^m\) (\(m\le 4\), onset 5) for
\(q=1,\ldots,12\). Infinitely many \(k\) with some \(\varphi^{(q)}_k=1\)
would kill every eventual period \(2^m\).

## \(P\equiv 1\) for every odd \(q\) — killed

\(q=7\) has popcount 3 (odd), so \(P(7)=0\). On the prize orbit the
packed-bit-1 hit parity is 0 for \(k\le 4\). Odd \(p=1\) parity is
special to even Hamming weight, not to odd \(q\). **Killed.**

## \(S\equiv 0\) on even-weight \(q\) — killed

If \(S^{(q)}\) vanished for an even-popcount \(q\) then
\(\varphi^{(q)}\equiv 1\), already killing every period \(2^m\). For
\(q=3,5,6,9\) on \(k\le 6\) each \(\varphi\) takes both values.
**Killed.**

## Thue–Morse (correction to Cycle AK)

For Thue–Morse \(t_n=\mathrm{popcount}(n)\bmod 2\) one has
\(t_{2^k}=1\) and \(\varphi^{(q)}_k=\mathrm{popcount}(q)\oplus 1=P(q)\).
In particular Fermat-odd (even-weight) spines have \(\varphi\equiv 1\),
not \(0\). Eventual vanishing of every Fermat \(\varphi\) would exclude
Thue–Morse; it is **not** compatible with it. Cycle AK's parenthetical
that TM has Fermat \(\varphi\equiv 0\) was wrong. Vanishing of \(I_k\)
together with Fermat \(\varphi\to 0\) is a strong rigidity, still short
of aperiodicity without a Rule-30 production: some \(\varphi^{(q)}_k=1\)
infinitely often, or infinitely many centre `00`s.

No GF(2) linear combination of
\((I_{k+1},\varphi^{(3)},\varphi^{(5)},\varphi^{(9)},\varphi^{(17)})\)
is constant on \(k\le 13\), including after dropping \(k=0,1\).

## Verdict

`LEMMA` (all-\(q\) identity; edges cancel; \(P(q)=1\oplus\mathrm{wt}(q)\);
period \(2^m\) forces every integer \(\varphi^{(q)}=0\); odd-\(q\) extras
outside). `KILLED` (\(P\equiv 1\) for every odd \(q\); \(S\equiv 0\) on
even-weight \(q\)). `OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often).
Prize unsolved.

## Files

- `research/cycle_al.md` (this note)
- `research/cycle_al.py`
- `research/cycle_al.json`
