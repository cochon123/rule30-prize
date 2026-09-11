# Cycle DW: pair invariants imply \(\operatorname{ham}(n_3,n_4)=n_0\)

\(\operatorname{reconstruct}(1,s)\) has isolated 1s for any nonzero \(s\)
(NOR). If \(s\) is O-type of half-length \(n_0\) then \(n_3_t=1\) forces
\(s_{t-1}=0\), hence \(n_{3,t+n_0}=0\) (complementary support). The
Hamming difference \(d=n_3\oplus n_4\) obeys \(d_{t+1}=\neg s_t\) if
\(n_{3,t}\) else \(\neg d_t\). On O-type pair slots, both \(n_3=0\)
implies both \(d=1\), and exactly one \(n_3=1\) implies \(d=0\) on the
zero side. Those pair invariants, certified for \(1\le n_0\le 16\), make
\(\varphi(i)=(i-1)\bmod n_0\) a bijection from \(\{n_3=1,d=0\}\) onto the
empty slots, so \(\operatorname{ham}(n_3,n_4)=n_0\) for every such
\(n_0\). The bijection argument has no further \(n_0\) bound. Pair
invariants fail for generic \(s\) and for E-type length 16. Do **not**
claim the pair invariants for all \(n_0\). Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: Hamming \(n_0\) still does not fill an annulus.

Helper: `python3 research/cycle_dw.py --certify`. Dump:
`research/cycle_dw.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DV (no new packed run, no Fermat table).

## Lemma (isolated 1s; complementary support; \(d\)-recurrence)

For every nonzero \(s\), \(n_3=\operatorname{reconstruct}(1,s)\) satisfies
\(n_{3,t+1}=\operatorname{NOR}(s_t,n_{3,t})\), so a 1 is never followed
by a 1. If \(s\) is O-type then \(s_{t+n_0}=\neg s_t\). A 1 at \(t\)
requires \(s_{t-1}=0\), hence
\(n_{3,t+n_0}=\operatorname{NOR}(1,n_{3,t+n_0-1})=0\). The difference
\(d=n_3\oplus n_4\) satisfies \(d_{t+1}=\neg s_t\) if \(n_{3,t}=1\) and
\(d_{t+1}=\neg d_t\) if \(n_{3,t}=0\). Certified for lengths \(2\le n
\le 8\) (isolated / \(d\)-recurrence) and \(1\le n_0\le 12\)
(complementary support).

## Lemma (pair invariants, \(1\le n_0\le 16\))

On every odd 2-copy of half-length \(n_0\le 16\), writing
\(a=n_{3,t}\), \(b=n_{3,t+n_0}\), \(x=d_t\), \(y=d_{t+n_0}\):

- \(a=b=0\) implies \(x=y=1\);
- \(a=1\) implies \(b=y=0\);
- \(b=1\) implies \(a=x=0\).

Certified exhaustively (\(2^{n_0}\) words each). **PREFIX** for all
\(n_0\).

## Lemma (pair invariants imply \(\operatorname{ham}=n_0\))

Let \(Z\) be the number of empty pair-slots and \(A=\mathrm{wt}(n_3)\).
Pair invariants give Hamming \(2Z+(A-\mathrm{ov})\). Define
\(\psi(t)=t+1\) if \(s_t=0\) else \(t+n_0+1\) on empty slots, and
\(\varphi(i)=(i-1)\bmod n_0\) on \(\{n_3=1,d=0\}\). Recurrence plus the
invariants make \(\psi\) a right inverse of \(\varphi\), and
complementary support makes \(\varphi\) injective, so
\(\mathrm{ov}=Z\) and Hamming \(=Z+A=n_0\). Certified as a bijection
for every \(1\le n_0\le 16\). The argument does not use a bound on
\(n_0\) beyond the invariants. Prize \(k=4,8,16\) remain Hamming
\(\pi\) (Cycle DV).

## Generic \(s\) and E-type — killed

Length-8 non-O-type words can have \(n_{3,t}=n_{3,t+4}=1\). E-type
length-16 words realize Hamming other than 8. **Killed** as identities.

## Verdict

`LEMMA` (isolated 1s; complementary support; \(d\)-recurrence; pair
invariants through \(n_0=16\); pair invariants imply Hamming \(n_0\)).
`PREFIX` (pair invariants for all \(n_0\); period-\(H\) seed; \(\pi\)
formula; Fermat covering).
`KILLED` (pair invariants for generic \(s\); pair invariants / Hamming
\(n_0\) for E-type).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dw.md` (this note)
- `research/cycle_dw.py`
- `research/cycle_dw.json`
