# Cycle EF: every FAM372 scar lifts to the even-52809 \(n_0=8\) family

Every \(n_0=4\) extra-372 \(T_0\) has first-odd predecessor \(a\) a
rotation of `00001011`. \(\operatorname{unfold}(a)\) is an \(n_0=8\)
word whose first ident-0 extra is the even 52809 family (Cycle DM; 16
words, prize \(T_0=\)`00000110` included). Extra 52809 from \(k=8\)
lands in annulus \(k=15\) (even, no period doubling). The odd
\(n_0=8\) extras 26357 (\(k=14\)) and 44842 (\(k=15\)) are
unreachable as first ident-0 after FAM372. FAM89 unfolds have no
ident-0 in 53000 extras. Among the eight FAM372 lifts, three
scar-odd-double at extra 87468 (\(k=16\)) and five, including prize
\(T_0=\)`00000110`, have no odd ident-0 in 131000 extras (the
\(k=16\) window from \(k=8\)). Kills: FAM372 can hit odd extra 26357;
\(k=8\) maps to \(k=16\) for every FAM372 scar. Do **not** claim a
closed form for 52809 or 87468. Do **not** equate scar extra 87468
with packed bit 87867 on prize \(T_0\). Do **not** claim an 11-bit
gap. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: an even ident-0 at \(k=15\) does not place the next
odd in a 2-power high half for every lift.

Helper: `python3 research/cycle_ef.py --certify`. Dump:
`research/cycle_ef.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DI, DM, EE (no new packed run, no Fermat table,
no \(n_0=16\) window bump).

## Lemma (FAM372 unfolds to even extra 52809)

The eight FAM372 words unfold through extra 372 to eight distinct
length-8 \(T_0\)s, each with first ident-0 extra 52809 even. In
particular \(T_0=1101\) has \(a=00001011\) and
\(\operatorname{unfold}(a)=00000110\), the prize \(k=8\) string.
LIFT372 (`0010`,`0100`,`0101`,`0110`) is the \(u_0=0\) subset.

## Lemma (extra 52809 from \(k=8\) lands in \(k=15\))

Packed next \(=p+E-1\). The image of \((2^8,2^9]\) under extra 52809
is \((53065,53320]\subset(2^{15},2^{16}]\), annulus 15. Prize even
ident-0 detection \(400+52809-1=53208\) matches Cycle DF. Extra 26357
from \(k=8\) would land in \(k=14\); extra 44842 in \(k=15\); extra
87468 in \(k=16\).

## Lemma (FAM89 unfolds have no ident-0 in 53000)

The eight FAM89 words unfold through extra 89 to eight length-8
\(T_0\)s with no ident-0 in 53000 extras, so they are not in the
26357, 44842, or 52809 families. That path is unreachable after
\(n_0=2\) (Cycle EE).

## Lemma (scar odd-split at extra 87468 is not universal)

Among the eight FAM372 \(n_0=8\) lifts, `0010`,`1001`,`1011`
scar-odd-double at extra 87468 (annulus 16 from \(k=8\)). The other
five, including prize `00000110`, have no odd ident-0 in 131000
extras, which covers the \(k=16\) window from \(k=8\)
(\(E\le 130561\)).

## Killed

FAM372 cannot produce odd extra 26357 (or 44842) as first ident-0; its
first ident-0 is always even 52809. \(k=8\) does not map to \(k=16\)
for every FAM372 scar: five of eight lifts have no odd ident-0 in the
\(k=16\) window. (Packed bit 87867 on the prize orbit is a different
time origin; do not identify it with scar extra 87468 on prize \(T_0\).)

## Verdict

`LEMMA` (FAM372 unfolds to even 52809; prize \(u_8\) from `1101`;
extra 52809 from \(k=8\) lands in \(k=15\); FAM89 unfolds none in
53000).
`KILLED` (FAM372 first ident-0 odd 26357; \(k=8\) maps to \(k=16\) for
every FAM372 scar).
`PREFIX` (closed form for 87468; scar 87468 is packed 87867 on prize
\(T_0\); at-most-one-odd for all \(k\); period-\(H\) seed; \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ef.md` (this note)
- `research/cycle_ef.py`
- `research/cycle_ef.json`
