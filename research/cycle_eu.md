# Cycle EU: reconstruct(\(A,1\)) and \((1,S)\) closed forms; \(n_0=16\) ident-0 in \(k\ge 18\)

Unique continuation against all-1s is a rotate-NOT:
\(\operatorname{reconstruct}(A,1)_t=1\oplus A_{t-1}\). For O-type \(T\) of
half-length \(n_0\) that is \(\operatorname{rot}^{n_0-1}(T)\), so the bit
after \((0,T,1)\) is a rotation of \(T\). Unique continuation of all-0s
against a nonzero \(T\) is all-1s. Unique continuation of all-1s against
any nonzero \(S\) is gap-parity: \(\operatorname{reconstruct}(1,S)_t=1\)
iff the backward distance to the previous 1 of \(S\) is even (NOR
recurrence; isolated 1s). The pair map
\(F(A,B)=(B,\operatorname{reconstruct}(A,B))\) inverts by
\(A_t=U_{t+1}\oplus(B_t\lor U_t)\). Two steps before ident-0 the bits are
\(D(W),W,W,0\). Cycle EP’s min extra 414990 for \(n_0=16\) exceeds
\(2^{18}\), so every \(n_0=16\) ident-0 has packed index \(\ge 414990\)
and sits in annulus \(k\ge 18\): origin \(k\le 15\) lands only in
\(k=18\), origin \(k=16\) splits 18/19, origin \(k=17,18\) lands only in
\(k=19\). Kills: \(n_0=16\) ident-0 (even or odd) in \(k\le 17\); no
closed form for \(\operatorname{reconstruct}(T,1)\). Do **not** claim a
formula for extra 414990. Do **not** claim no \(n_0=16\) ident-0 in
\(k=18\). Do **not** bump all \(n_0=16\) past 414990. Do **not** claim
at-most-one-odd for all \(k\). Do **not** compute \(\varphi^{(3,5,9)}\)
at \(k=16\). Do **not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: closed forms for the first two scar steps and a
landing bound for \(n_0=16\) do not give covering never-fail or
at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_eu.py --certify` (~0.2s). Dump:
`research/cycle_eu.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/DV/EE/EP/EQ/ER/ES/ET (no new packed run,
no Fermat table, no all-\(n_0=16\) window, no \(2^{21}\) rerun).

## Lemma (\(\operatorname{reconstruct}(A,1)_t=1\oplus A_{t-1}\))

Against all-1s the recurrence is \(u_{t+1}=A_t\oplus 1\), independent of
\(u_t\). The wrap is the same identity at \(t=0\). Exhaustive on every
word of length \(1..10\), trials on length \(12,16,24,32\).

## Lemma (O-type \(n_3=\operatorname{rot}^{n_0-1}(T)\))

O-type means \(T_{t+n_0}=\neg T_t\), so \(1\oplus T_{t-1}=T_{t+n_0-1}\),
which is \(\operatorname{rot}^{n_0-1}(T)\). Still O-type. Exhaustive
\(1\le n_0\le 12\).

## Lemma (\(\operatorname{reconstruct}(0,T)=1\) for \(T\not\equiv 0\))

The recurrence is \(u_{t+1}=T_t\lor u_t\). One 1 in \(T\) fills the
circle. Exhaustive on every nonzero word of length \(1..10\).

## Lemma (\(\operatorname{reconstruct}(1,S)\) is gap-parity)

Against all-1s the recurrence is NOR: \(u_{t+1}=\neg(S_t\lor u_t)\). After
each 1 of \(S\) the next \(u\) is 0, then along a 0-run of \(S\) the
values alternate \(0,1,0,1,\ldots\). Equivalently \(u_t=1\) iff the
backward distance to the previous 1 of \(S\) is even. Consecutive gap-1s
are impossible, so the 1s are isolated (Cycle DW). Exhaustive on every
nonzero word of length \(1..10\), trials on length \(12,16,24,32\).

## Lemma (\(F\) inverts by \(A_t=U_{t+1}\oplus(B_t\lor U_t)\))

The recurrence \(U_{t+1}=A_t\oplus(B_t\lor U_t)\) solves for \(A\)
whenever \(B\not\equiv 0\). Exhaustive on every pair of length \(1..8\).

## Lemma (ident-0 ending is \(D(W),W,W,0\))

Cycle CA: \(\operatorname{reconstruct}(A,B)=B\) iff \(A=D(B)\). Cycle DH:
\(\operatorname{reconstruct}(A,A)=0\). So the three pairs before a white
stripe are \((D(W),W)\), \((W,W)\), \((W,0)\). Certified on the FAM414990
predecessor \(W\), and \(n_3=\operatorname{rot}^{15}(U)\),
\(n_4=\operatorname{gap}(n_3)\) on \(U=T^*\|\neg T^*\).

## Lemma (every \(n_0=16\) ident-0 sits in \(k\ge 18\))

Cycle EP: every length-16 \(T_0\) has first ident-0 extra \(\ge 414990\).
Packed next is \(p+E-1\ge E=414990>2^{18}\), so the bit lies in annulus
\(k\ge 18\). Image of extra 414990: origin \(k\le 15\) lands only in
\(k=18\); origin \(k=16\) splits \(k=18/19\); origin \(k=17,18\) lands
only in \(k=19\). Later ident-0s of the same scar are even further.

## Killed

There is a closed form for \(\operatorname{reconstruct}(T,1)\) (rotate
by \(n_0-1\)). \(n_0=16\) ident-0, even or odd, cannot occur in
\(k\le 17\). From origin \(k=16\) the image meets \(k=18\), so “never in
\(k=18\)” is false.

## Verdict

`LEMMA` (\(\operatorname{reconstruct}(A,1)\) rotate-NOT; O-type \(n_3\)
rotation; \(\operatorname{reconstruct}(0,T)=1\); gap-parity;
\(F\)-inverse; ident-0 ending \(D(W),W,W,0\); \(n_0=16\) ident-0 in
\(k\ge 18\)).
`KILLED` (\(n_0=16\) ident-0 in \(k\le 17\); never in \(k=18\); no closed
form for \(\operatorname{reconstruct}(T,1)\)).
`PREFIX` (formula for extra 414990; at-most-one-odd for all \(k\); seed
for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eu.md` (this note)
- `research/cycle_eu.py`
- `research/cycle_eu.json`
