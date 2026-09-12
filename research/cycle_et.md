# Cycle ET: every \(n_0=8\) rotation class has a first ident-0 extra

Cycle ES: 16 classes of 16; nine extras in 53000, seven none. The seven
miss-class representatives first-ident-0 at extras 62792 (odd), 72474
(even), 93359 (even), 114130 (odd), 125210 (odd), 171542 (odd), 214007
(odd). The two even-first classes later odd-double at 322924 and 119349.
Every length-8 \(T_0\) therefore hits ident-0 by extra 214007. First
ident-0 extra is one plus the first time two consecutive
unique-continuation bits are equal (Cycle DH:
\(\operatorname{reconstruct}(A,A)=0\)). Kills: those seven classes
never ident-0; leftover after 53000 empty for them. Do **not** claim
every \(n_0=16\) class hits. Do **not** claim a formula for extra
414990. Do **not** bump all \(n_0=8\) past 523777. Do **not** bump all
\(n_0=16\) past 414990. Do **not** claim an 11-bit gap. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the
\(n_0=2\) seed past \(k=21\).

Not a prize claim: a complete \(n_0=8\) extra table does not give
covering never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_et.py --certify` (~5.1s). Dump:
`research/cycle_et.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DH/DM/DI/EE/EH/EP/ER/ES. Scalar
`first_ident0_int` / `ident0_events` on the seven ES miss-class
representatives only (no 256-word \(n_0=8\) bump, no \(n_0=16\) window,
no Fermat table, no new packed run).

## Lemma (every \(n_0=8\) class has a first ident-0 extra)

The seven Cycle ES miss representatives hit at
\(62792,72474,93359,114130,125210,171542,214007\), all distinct from
Cycle DM’s nine extras, so all 16 classes are accounted for. Max first
extra is 214007. Two of the seven are even (72474, 93359); those later
odd-double at 322924 and 119349.

## Lemma (from \(k=8\), those extras land in \(k=15..18\))

Odd 62792 lands in \(k=15\); odds 114130 and 125210 and even 72474 in
\(k=16\); odds 171542 and 214007 in \(k=17\); odd 322924 in \(k=18\).
These classes are not the FAM372\(\to\)52809 \(n_0=2\) cascade.

## Lemma (ident-0 extra is \(1+\) first consecutive equal)

Cycle DH: \(\operatorname{reconstruct}(A,B)=0\) iff \(A=B\). So the
first ident-0 extra is one plus the first time two consecutive scar
bits are equal. Certified on \(n_0=2\) (extra 22), prize \(n_0=8\)
(extra 52809), and \(T^*\) (extra 414990).

## Killed

The seven \(n_0=8\) classes that miss 53000 do ident-0, so leftover
after 53000 is not empty for them. “Every class eventually hits” is
now a lemma at \(n_0=8\), not a reason to census the other 2047
\(n_0=16\) classes.

## Verdict

`LEMMA` (every \(n_0=8\) class has an ident-0 extra; seven miss extras
recorded; extra \(=1+\) first consecutive equal).
`KILLED` (seven classes never ident-0; leftover after 53000 empty for
them).
`PREFIX` (every \(n_0=16\) class hits; formula for extra 414990;
at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\) formula;
Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_et.md` (this note)
- `research/cycle_et.py`
- `research/cycle_et.json`
