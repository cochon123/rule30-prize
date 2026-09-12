# Cycle EP: \(n_0=16\) first ident-0 is even extra 414990 on 32 words

Cycle DR: every length-16 \(T_0\) is ident-0-free in 262144 extras, so
the min extra is at least 262145. Bitsliced census of all 65536 words
through extra 414990 finds a unique first ident-0: even extra 414990
on exactly 32 type-N words, and none earlier. The 16 \(n_0=2\) unfolds
and packed prize \(u_{16}\) miss it. Kills: all \(n_0=16\) ident-0-free
through extras covering \(k=20\); the 16 unfolds are a sparse
ident-0-free family at this window; min extra still only DR’s lower
bound. Do **not** claim extra 414990 is odd. Do **not** claim
FAM414990 appears on the \(n_0=2\) cascade. Do **not** claim a
one-annulus image from \(k=16\). Do **not** bump all \(n_0=16\) past
414990. Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the \(n_0=2\) seed
past \(k=21\).

Not a prize claim: an even extra on 32 of 65536 words does not give
covering never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ep.py --certify` (~60.7s). Dump:
`research/cycle_ep.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DJ, DK, DN, DR, EE, EH, EN, EO. Bitsliced
`census(16, 414990)` plus scalar `ident0_events` on two witnesses.
No new packed run, no Fermat table, no \(n_0=16\) window past 414990.

## Lemma (min extra is even 414990)

Among all 65536 length-16 \(T_0\), the first ident-0 extra is 414990,
even, on 32 words. The other 65504 have no ident-0 in 414990 extras.
So every \(n_0=16\) scar is ident-0-free in 414989 extras, and the DR
lower bound 262145 is not sharp: the true min is 414990, and it is
even. Min odd extra remains \(\ge 414991\).

## Lemma (FAM414990 is 32 type-N words)

The 32 words are all type N. Bit 0 and xorcat each split 16/16.
Weights lie in \(\{6,7,8,9,10\}\). Witnesses
`1110100110001101` and `0110011100101110` hit even 414990 under
scalar `ident0_events`.

## Lemma ( \(n_0=2\) unfolds and packed prize miss 414990 )

Cycle EN’s 16 unfolds after the \(n_0=8\) odds are type N with
\(u_0=0\), and none of them is in FAM414990. Packed prize
\(u_{16}=0000110011110011\) is type O and also misses. Cycle EO’s
ident-0-free window through \(k=20\) on those unfolds is the generic
miss, not a private family: 65504 of 65536 words miss 414990.

## Lemma ( \(k=16\) leftover is shorter than 414990 )

Prize leftover at \(k=16\) is 43205. Extra 414990 exceeds that, so no
\(n_0=16\) ident-0 fits in the \(k=16\) leftover. From origin \(2^{16}\)
the image of extra 414990 straddles annuli 18 and 19; from \(k=17\)
and \(k=18\) it lands in \(k=19\). Do not claim a one-annulus image
from \(k=16\). Worst-case leftover \(2^{19}=524288\) can fit 414990,
so this even extra can sit in \(k=19\) for some origins.

## Killed

Not every \(n_0=16\) \(T_0\) is ident-0-free through extras covering
\(k=20\): 32 words hit at 414990. The 16 unfolds are not a sparse
ident-0-free family at that scale; they are typical missers.
Extra 414990 is even, not odd, and does not appear on the \(n_0=2\)
cascade.

## Verdict

`LEMMA` (min \(n_0=16\) extra even 414990; FAM414990 has 32 type-N
words; \(n_0=2\) unfolds and packed prize miss it; \(k=16\) leftover
shorter than 414990).
`KILLED` (all \(n_0=16\) ident-0-free through \(k=20\); unfolds sparse
at 2M; extra 414990 odd; FAM414990 on \(n_0=2\)).
`PREFIX` (closed form for extra 414990; at-most-one-odd for all \(k\);
seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ep.md` (this note)
- `research/cycle_ep.py`
- `research/cycle_ep.json`
