# Cycle EB: \(r\)-fold of \(n_0=2\) O-types ident-0 at extra 22

Unique continuation commutes with repetition:
\(\operatorname{reconstruct}(A^r,B^r)=\operatorname{reconstruct}(A,B)^r\)
whenever \(B\not\equiv 0\). The four length-4 O-types
`0011`,`0110`,`1001`,`1100` therefore lift: odd \(r\) stays O-type of
half-length \(2r\) and odd-ident-0s at extra 22; even \(r\) is E-type
and even-ident-0s at extra 22. Through \(n_0=2,6,10,14\) the only
O-type extra-22 scars are those four \(r\)-folds. Prize \(n_0=4,8,16\)
are 2-powers (even \(r\)) and O-type, so they are not this family.
Kills: min extra increases with \(n_0\); extra \(>22\) for all
\(n_0\ge 4\). Do **not** claim extra \(\ge 22\) for every even \(n_0\).
Do **not** claim the family appears on the prize orbit after \(k=2\).
Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: extra 22 on a fold family does not fill an annulus
and does not place the next prize odd in a 2-power high half.

Helper: `python3 research/cycle_eb.py --certify`. Dump:
`research/cycle_eb.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DI, DM, EA (no new packed run, no Fermat
table).

## Lemma (reconstruct commutes with \(r\)-fold)

If \(B\not\equiv 0\) and \(U=\operatorname{reconstruct}(A,B)\), the
first 1 of \(B\) is also the first 1 of \(B^r\) in \([0,nr)\). Unique
continuation from that bit, together with the local rule
\(U_{t+1}=A_t\oplus(B_t\lor U_t)\), is periodic of period \(n\), so
\(U^r\) is the unique continuation of \((A^r,B^r)\). Certified
exhaustively for \(2\le n\le 6\) and \(r\le 5\), and on random
\(n\in\{8,12,16\}\). The whole \(n_0=2\) scar through extra 22
likewise \(r\)-folds.

## Lemma (\(\operatorname{xorcat}(s^r)=r\cdot\operatorname{xorcat}(s)\))

XOR of \(r\) copies is \(r\) times the XOR, modulo 2.

## Lemma (odd \(r\) is O-type; even \(r\) is E-type)

A length-4 O-type satisfies \(u_{t+2}=\neg u_t\). On \(u^r\),
positions \(t\) and \(t+2r\) differ by \(2r\bmod 4\): odd \(r\) gives
shift 2 (NOT), even \(r\) gives shift 0 (equal).

## Lemma (odd \(r\)-fold odd-ident-0s at extra 22; even \(r\)-fold even)

The \(n_0=2\) scar odd-ident-0s at extra 22 with predecessor XOR 1
(Cycle DI: rotations of `0111`). Folding the scar preserves the
ident-0 index; the predecessor XOR becomes \(r\bmod 2\). Certified
for odd \(r\le 9\) via the standard O-type scar of the half-word, and
for even \(r\le 8\) via the E-type lift of \(u^r\).

## Lemma (extra-22 O-type \(T_0\) through \(n_0=14\) are exactly the folds)

Exhaustive: at \(n_0=2,6,10,14\) (odd \(r=1,3,5,7\)) the only
length-\(n_0\) words whose O-type scar ident-0s at extra 22 are the
four \(r\)-folds of the \(n_0=2\) halves. In particular \(n_0=6\)
extra-22 is \(\{001100,011001,100110,110011\}\). The other 60
length-6 words: 12 even-ident-0 at extra 99, 48 none in 800 extras.
Do not claim a closed form for extra 99. Do not claim the exclusive
count for every odd \(r\).

## Lemma (prize \(n_0=4,8,16\) not in the odd-fold family)

Those lengths are 2-powers \(\ge 4\), hence \(r=n_0/2\) is even. An
\(n_0=2\) fold of even \(r\) would be E-type; the prize scar after
odd doubling is O-type. Direct check: none of the prize \(T_0\)
ident-0s at extra 22.

## Killed

Min extra does not increase with \(n_0\): \(n_0=2\) is 22, \(n_0=4\)
is 89 or 372, \(n_0=6\) is 22, \(n_0=8\) is 6344. Extra \(>22\) for
all \(n_0\ge 4\) is false (the odd-fold family hits 22 at every
\(n_0=2r\) with \(r\) odd). Extra 22 is therefore sharp for
infinitely many even \(n_0\); a universal extra \(\ge 89\) is false.

## Verdict

`LEMMA` (reconstruct commutes with \(r\)-fold; xorcat of \(r\)-fold;
odd \(r\) O-type / even \(r\) E-type; lift commutes; odd \(r\)-fold
odd-ident-0 at 22; even \(r\)-fold even-ident-0 at 22; extra-22
through \(n_0=14\) exactly the folds; \(n_0=6\) extra-22 is the
3-fold; prize \(n_0=4,8,16\) not odd-fold).
`KILLED` (min extra increases with \(n_0\); extra \(>22\) for all
\(n_0\ge 4\)).
`PREFIX` (extra \(\ge 22\) for every even \(n_0\); 11-bit gap;
period-\(H\) seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eb.md` (this note)
- `research/cycle_eb.py`
- `research/cycle_eb.json`
