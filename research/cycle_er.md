# Cycle ER: FAM414990 \(T_0\)s are 16-prefixes of rotations of one O-type word

Cycle EQ: the 32 predecessors are rotations of \(W\), and FAM414990 is
complement-closed. Aligning each \(T_0\) with the rotation index of
\(W\) shows the family is exactly the length-16 prefixes of the 32
rotations of one O-type necklace
\(U=01100111001011101001100011010001\) (\(U=T^*\|\neg T^*\) with
\(T^*=0110011100101110\)). Min period of \(U\) is 32. The member whose
predecessor is \(W\) itself is \(T^*\). Rotation by 16 is complement.
Kills: no \(T_0\) closed form beyond the predecessor necklace. Do
**not** claim \(U=W\). Do **not** claim a formula for extra 414990.
Do **not** claim \(U\) on the \(n_0=2\) cascade. Do **not** bump all
\(n_0=16\) past 414990. Do **not** claim an 11-bit gap. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the
\(n_0=2\) seed past \(k=21\).

Not a prize claim: a necklace for FAM414990 does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_er.py --certify` (~1.2s). Dump:
`research/cycle_er.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles EP, EQ. Scalar `ident0_events` on \(T^*\) only
(no new packed run, no Fermat table, no all-\(n_0=16\) window, no EQ
\(2^{21}\) rerun).

## Lemma (FAM414990 is the 16-prefixes of rotations of \(U\))

Let \(T^*=0110011100101110\) (Cycle EP witness `0110011100101110`) and
\(U=T^*\|\neg T^*\). Then \(U\) is O-type, length 32, min period 32,
weight 16, even xorcat, and
\(\operatorname{FAM414990}=\{(\operatorname{rot}^k U)[:16]:k=0,\ldots,31\}\).

## Lemma (rotation by 16 is complement)

\((\operatorname{rot}^{k+16} U)[:16]=\neg(\operatorname{rot}^k U)[:16]\).
That is Cycle EQ’s complement-closure, now as a necklace fact.

## Lemma (\(T^*\) is the member with predecessor \(W\))

Scalar `ident0_events` on \(T^*\) hits even extra 414990 with
predecessor exactly \(W=00000001011101010010010000101011\), not a
nontrivial rotation. So the two necklaces share an origin: \(k=0\) on
\(U\) is \(k=0\) on \(W\). \(U\neq W\) (Hamming 20).

## Killed

The \(T_0\) strings are not without a closed form beyond “preds are
rots of \(W\)”: they are the 16-windows of one O-type 32-bit necklace.
\(U\) is not \(W\), and \(U\) is not an \(n_0=2\) unfold (those miss
FAM414990).

## Verdict

`LEMMA` (16-prefixes of rots of \(U\); \(U\) O-type min period 32;
rot-16 is complement; \(T^*\) has pred \(W\)).
`KILLED` (no \(T_0\) closed form beyond \(W\); \(U=W\); \(U\) on the
\(n_0=2\) cascade).
`PREFIX` (formula for extra 414990; at-most-one-odd for all \(k\);
seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_er.md` (this note)
- `research/cycle_er.py`
- `research/cycle_er.json`
