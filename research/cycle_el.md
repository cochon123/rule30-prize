# Cycle EL: every \(n_0=2\) scar has at most one odd in \(k=17\); seed at \(k=18\)

Cycle EK: \(n_0=2\) scars have at most one odd in \(k=16\) and the
period-\(H\) seed at \(k=17\). The ten even-52809 words with no odd
in 131000 extras first-odd at extra 228939 (six 57888-miss words,
including prize \(T_0\)), 182785 (two), 195790 (one), or none in
261633 (`00001101`). Those three extras land in \(k=17\). Cycle DR:
an \(n_0=16\) odd at \(k=16\) skips \(k=17\), so the six extra-87468
words have no second odd there. Hence at most one odd in \(k=17\) on
every \(n_0=2\) scar, and \(\pi_{18}\in\{16,32\}\) divides \(2^{17}\).
Kills: prize \(T_0\) has no scar odd after the two \(k=15\) evens;
every \(n_0=2\) scar skips \(k=17\). Do **not** claim a closed form
for 228939. Do **not** equate scar 228939 with packed 87867. Do
**not** claim `00001101` never odd-doubles. Do **not** claim the
seed for all \(k\). Do **not** bump the \(n_0=8\) scan past 261633.
Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: seed at \(k=18\) for \(n_0=2\) scars does not give
covering never-fail.

Helper: `python3 research/cycle_el.py --certify`. Dump:
`research/cycle_el.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DR, DU, EH, EK. Bitsliced first-odd continues
even ident-0 via unfold and is checked against `first_odd_continue` on
prize \(T_0\), `00110111`, and `00001101`. No new packed run, no Fermat
table, no \(n_0=16\) window bump.

## Lemma (228939, 182785, 195790 land in \(k=17\))

Image of extra 228939 from \(k=8\) is
\((229195,229450]\subset(2^{17},2^{18}]\). Extras 182785 and 195790
likewise sit in \(k=17\). Leftover after the 228939 image is
\(262144-229450=32694<262145=E_{16}\). The image stays in \(k=17\)
for extra \(\le 261633\).

## Lemma (ten remaining \(n_0=8\) scars)

A bitsliced first-odd scan of all 256 length-8 words through 261633
extras, continuing even ident-0 via unfold, finds: the six extra-87468
words still first-odd at 87468; the six 57888-miss words, including
prize \(T_0=00000110\), first-odd at 228939; two of the 72177 group at
182785; one at 195790; and `00001101` with no odd in the window.
Scalar `first_odd_continue` matches on prize \(T_0\), `00110111`, and
`00001101`.

## Lemma (period-\(H\) seed at \(k=18\) for every \(n_0=2\) scar)

The six extra-87468 words are \(n_0=16\) after the \(k=16\) odd and
skip \(k=17\) (Cycle DR). The other ten have at most one odd in
\(k=17\). Combined with Cycle EK’s at-most-one through \(k=16\),
\(\pi_{18}=16\) or \(32\), both dividing \(2^{17}\). Cycle DU: at
most one odd per annulus implies the seed.

## Killed

Prize \(T_0\) odd-doubles at scar extra 228939, so it is false that
the prize scar has no odd after the two \(k=15\) evens. Nine of the
ten remaining \(n_0=8\) words land an odd in \(k=17\), so it is false
that every \(n_0=2\) scar skips \(k=17\).

## Verdict

`LEMMA` (228939/182785/195790 from \(k=8\) land in \(k=17\); leftover
after 228939 \(<E_{16}\); 261633 covers the window; prize scar odd at
228939; \(n_0=16\) \(k=16\) odd skips \(k=17\); at most one odd in
\(k=17\) on \(n_0=2\); period-\(H\) seed at \(k=18\) for every
\(n_0=2\) scar).
`KILLED` (prize \(T_0\) has no scar odd after the two \(k=15\) evens;
every \(n_0=2\) scar skips \(k=17\)).
`PREFIX` (closed form for 228939; scar 228939 is packed 87867;
`00001101` never odd; leftover after 228939 empty at later \(k\);
at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\) formula;
Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_el.md` (this note)
- `research/cycle_el.py`
- `research/cycle_el.json`
