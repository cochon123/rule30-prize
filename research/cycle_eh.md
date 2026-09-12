# Cycle EH: 52809-family two-even split; prize is not the 72177 fork

Every even-52809 \(n_0=8\) word has a second even ident-0 at extra
57888 (12 words) or 72177 (4 words). The six extra-87468 odds are
exactly a subset of the 57888 group; prize \(T_0=\)`00000110` is in
that group and has no odd ident-0 in 131000 extras. Prize first-even
predecessor is Cycle DF’s \(k=15\) string `1100001100010100`; packed
image \(400+52809-1=53208\). Extra 57888 from \(k=8\) lands in
\(k=15\); extra 72177 lands in \(k=16\) (packed image 72576). Kills:
prize \(T_0\) hits the 72177/Rowland-adjacent fork. Do **not**
identify 72576 with Rowland 72577. Do **not** claim packed 58287
without a high-half dump. Do **not** claim a closed form for
57888/72177/87468. Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: a two-even census of one family does not place the
next odd in every later annulus.

Helper: `python3 research/cycle_eh.py --certify`. Dump:
`research/cycle_eh.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DF, DE, EG (no new packed run, no Fermat table,
no \(n_0=16\) window bump).

## Lemma (second even is 57888 or 72177)

All 16 words even-ident-0 at extra 52809, then a second even at 57888
(12 words) or 72177 (4 words). No wrap failure in 131000 extras.

## Lemma (87468 odds sit only in the 57888 group)

Six words scar-odd-double at extra 87468, all in the 57888 group. The
four 72177 words have no odd in 131000. Prize `00000110` is in the
57888 group with no odd in 131000.

## Lemma (prize first-even \(a\) is Cycle DF’s \(k=15\) predecessor)

On prize \(T_0\), the extra-52809 predecessor is `1100001100010100`,
matching `K15_A`. Packed image \(400+52809-1=53208\) matches Cycle DF.
Cycle DE: \(k=15\) has two even ident-0s. Extra 57888 from \(k=8\)
lands in annulus 15; extra 72177 lands in annulus 16.

## Killed

Prize \(T_0\) is not in the 72177 family, so it does not hit that
scar extra or packed image 72576. Packed 72576 is not identified with
Rowland’s 72577 fork.

## Verdict

`LEMMA` (second even 57888 or 72177; 87468 only in the 57888 group;
prize in 57888 with no odd in 131000; prize first-even \(a=K15_A\);
57888 from \(k=8\) lands in \(k=15\); 72177 from \(k=8\) lands in
\(k=16\)).
`KILLED` (prize hits 72177 or Rowland 72577; 72576 is Rowland 72577).
`PREFIX` (packed second \(k=15\) even is 58287; closed form for 57888;
scar 87468 is packed 87867 on prize \(T_0\); at-most-one-odd for all
\(k\); period-\(H\) seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eh.md` (this note)
- `research/cycle_eh.py`
- `research/cycle_eh.json`
