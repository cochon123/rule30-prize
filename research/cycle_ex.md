# Cycle EX: empty \(n_4\)-pair forces next \(n_6\)-pair `11`; even \(n_0\) has \(z\ge 1\)

Scar \(n_4=\operatorname{rot}^{n_0-1}(\operatorname{gap}(T))\) is type N
(Cycle DH) with complementary support (Cycle DW): never both 1s in a
pair \((t,t+n_0)\). Type N forbids O-type, so some pair is `00`
(\(z\ge 1\)). Pair invariants send that empty pair to \(n_5=11\), and
\(\operatorname{reconstruct}(n_4,n_5)\) then sends the next pair to
\(n_6=11\). Every even-\(n_0\) scar therefore has a half-period `11` in
\(n_6\). Exhaustive even \(2\le n_0\le 10\) plus \(T^*\) also find a
consecutive `11` in \(n_6\) (1171 of 1364 words from an empty-slot
successor with \(n_{4,i+1}=0\); the remaining 193 still have one
elsewhere). Kills: \(n_4\) can be O-type for even \(n_0\); \(z\) can be
0; \(n_6\) can lack a half-period `11`; \(n_6\) can lack a consecutive
`11`. Do **not** claim an 11-bit gap. Do **not** claim consecutive `11`
at every empty slot. Do **not** claim \(n_6\) type N for odd \(n_0\).
Do **not** claim a formula for extra 414990. Do **not** bump all
\(n_0=16\) past 414990. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\). Do **not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: a half-period `11` in \(n_6\) does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ex.py --certify` (~0.04s). Dump:
`research/cycle_ex.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/DV/DH/ER/EV/EW (no new packed run, no
Fermat table, no even-spine, no \(n_0=16\) window).

## Lemma (\(n_4\) complementary support)

\(\operatorname{gap}(s)_t=1\) forces \(s_{t-1}=0\) hence
\(\operatorname{gap}(s)_{t+n_0}=0\) on O-type \(s\) (Cycle DW). Scar
\(n_4\) is a rotation of \(\operatorname{gap}(T)\), so never both 1s in
a pair. Certified even \(2\le n_0\le 10\), and \(n_4\) stays type N.

## Lemma (\(z\ge 1\))

Never both 1s, so each pair is `00` or exactly one 1. O-type would be
exactly one 1 in every pair (\(z=0\)). Type N forbids that, so
\(z=n_0-\mathrm{wt}(n_4)\ge 1\). Min \(z=1\) for every even
\(2\le n_0\le 10\). \(T^*\) has \(z=5\), \(\mathrm{wt}(n_4)=11\).

## Lemma (empty \(n_4\)-pair \(\Rightarrow\) next \(n_6\)-pair `11`)

Pair invariants (Cycle DW): both \(n_4=0\) implies both \(n_5=1\). Then
\(n_{6,t+1}=n_{4,t}\oplus(n_{5,t}\lor n_{6,t})=1\), and the same at
\(t+n_0\). Certified on every empty slot, even \(2\le n_0\le 10\), and
on \(T^*\|\neg T^*\).

## Lemma (even \(n_0\): \(n_6\) has a half-period `11`)

Some \(u\) has \(n_{6,u}=n_{6,u+n_0}=1\). Immediate from \(z\ge 1\) and
the previous lemma.

## Lemma (even \(n_0\): \(n_6\) has a consecutive `11`)

Certified on every even-\(n_0\) O-type \(2\le n_0\le 10\) (1364 words)
and on \(T^*\). When an empty slot \(i\) also has \(n_{4,i+1}=0\), the
identity \(n_{6,i+2}=\neg n_{4,i+1}\) gives consecutive `11` at
\(i+1\). That covers 1171 words; the other 193 still have a consecutive
`11` off the empty-slot successor. Do **not** claim every empty slot
produces a consecutive `11`.

## Killed

Even-\(n_0\) \(n_4\) is not O-type. Empty-pair count is not 0. \(n_6\)
does not lack a half-period `11`. \(n_6\) does not lack a consecutive
`11`.

## Verdict

`LEMMA` (\(n_4\) complementary; \(z\ge 1\); empty pair \(\Rightarrow\)
next \(n_6\) `11`; even \(n_0\) \(n_6\) half-period `11`; even \(n_0\)
\(n_6\) consecutive `11`).
`KILLED` (even \(n_0\) \(n_4\) can be O-type; \(z=0\); \(n_6\) can lack
half-period `11`; \(n_6\) can lack consecutive `11`).
`PREFIX` (11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ex.md` (this note)
- `research/cycle_ex.py`
- `research/cycle_ex.json`
