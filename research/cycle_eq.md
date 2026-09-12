# Cycle EQ: FAM414990 predecessors are the 32 rotations of one word

Cycle EP: 32 type-N \(n_0=16\) \(T_0\)s have first ident-0 at even extra
414990. The 32 length-32 predecessors are exactly the rotation class of
\(W=00000001011101010010010000101011\) (min period 32, weight 12, even
xorcat). The \(T_0\) family is closed under complement (16 pairs). After
that even, bitsliced first-odd continuation of the 32 words finds no
odd ident-0 through \(2^{21}\) extras. Kills: FAM414990 preds not a
rotation orbit; family not complement-closed; these 32 odd-double
before \(2^{21}\). Do **not** claim a closed form for the \(T_0\)
strings beyond this necklace. Do **not** claim \(W\) on the \(n_0=2\)
cascade. Do **not** bump all \(n_0=16\) past 414990. Do **not** claim
min odd extra for every \(n_0=16\) is \(>2^{21}\). Do **not** claim an
11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do
**not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: a necklace for one even family does not give
covering never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_eq.py --certify` (~20.0s). Dump:
`research/cycle_eq.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles EP, EL (`unfold_slice`), EF
(`first_odd_continue`), EH, DN, EE. Bitsliced even-then-odd on the 32
EP words through \(2^{21}\), plus scalar `ident0_events` on both EP
witnesses. No new packed run, no Fermat table, no all-\(n_0=16\) window
past 414990.

## Lemma (predecessors are the rotation class of \(W\))

\(W\) has length 32, min period 32, weight 12, even xorcat, type N, and
32 distinct rotations. Bitsliced unique continuation of FAM414990 hits
even ident-0 at extra 414990 with predecessor set equal to those
rotations. Scalar `ident0_events` on both EP witnesses agrees.

## Lemma (FAM414990 is complement-closed)

The 32 words are 16 complement pairs. EP’s witnesses
`1110100110001101` and `0110011100101110` each have their complement
in the family (`0001011001110010` is the complement of the first).

## Lemma (no odd ident-0 through \(2^{21}\))

Continuing through the even at 414990 via unfold, none of the 32 words
has an odd ident-0 in \(2^{21}\) extras. So the first odd extra on this
family is \(>2^{21}\). Worst-case leftover \(2^k\) for \(k\le 21\)
cannot fit that odd. This does not bound the other 65504 \(n_0=16\)
words, and it does not place \(W\) on the \(n_0=2\) cascade (those
unfolds miss FAM414990).

## Killed

The 32 predecessors are not an unstructured set: they are one necklace.
The family is complement-closed. These 32 words do not odd-double
before \(2^{21}\). \(W\) is not the first-ident-0 predecessor of an
\(n_0=2\) unfold (those have no ident-0 through extras covering
\(k=20\)).

## Verdict

`LEMMA` (preds are rots of \(W\); \(W\) has min period 32; family
complement-closed; no odd through \(2^{21}\)).
`KILLED` (preds not a rotation orbit; not complement-closed; odd before
\(2^{21}\); \(W\) on the \(n_0=2\) cascade).
`PREFIX` (\(T_0\) closed form beyond the necklace; min odd for all
\(n_0=16\) is \(>2^{21}\); at-most-one-odd for all \(k\); seed for all
\(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eq.md` (this note)
- `research/cycle_eq.py`
- `research/cycle_eq.json`
