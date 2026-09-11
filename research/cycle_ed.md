# Cycle ED: second-odd leftover threshold for 2-power \(n_0\)

After an odd ident-0 of half-length \(n_0\), a second odd fits in the
same high half of annulus \(k\) only if leftover can exceed the first
odd extra. Worst-case leftover is \(2^k\) (odd at packed \(2^k+1\)).
Extra depends on \(T_0\), not on \(k\), so if \(n_0\) persists then
\(2^k\) eventually catches extra. The threshold \(v(n_0)\) is the
least \(k\) with \(2^k\ge\) min odd extra of that \(n_0\):
\(v(1)=3\), \(v(2)=5\), \(v(4)=7\), \(v(8)=15\), \(v(16)=19\), using
extras \(6,22,89,26357,>262144\). Prize 2-power odds sit at
\(k=1,2,4,8,16\), all strictly before \(v\), so both prize leftover
and worst-case \(2^k\) are shorter than extra. Kills leftover always
empty for 2-power \(n_0\) at every \(k\) (\(n_0=2\) at \(k=5\) has
\(32\ge 22\)). Do **not** claim the next odd is forced before \(v\).
Do **not** claim a formula for \(v\). Do **not** bump \(n_0=16\)
extras past \(2^{18}\). Do **not** claim an 11-bit gap. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: a threshold through \(n_0=16\) does not force the
next odd into a 2-power high half.

Helper: `python3 research/cycle_ed.py --certify`. Dump:
`research/cycle_ed.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DE, DI, DJ, DM, DR, EC (no new packed run, no
Fermat table, no \(n_0=16\) window bump).

## Lemma (min odd extra for 2-power \(n_0\le 16\))

\(n_0=1\): extra 6. \(n_0=2\): extra 22 (Cycle DI). \(n_0=4\): min 89
(Cycle DI). \(n_0=8\): min odd extra 26357 (Cycle DM; min any extra is
the even 6344). \(n_0=16\): no ident-0 in 262144 extras, so odd extra
\(\ge 262145\) (Cycle DR).

## Lemma (threshold \(v(n_0)\))

\(v(n_0)\) is the least \(k\) with \(2^k\ge E_{\mathrm{odd}}(n_0)\).
Then \(2^{v-1}<E\le 2^v\), so worst-case leftover first meets extra
at annulus \(v\). Certified: \(v=(3,5,7,15,19)\) for
\(n_0=1,2,4,8,16\).

## Lemma (prize odds sit before \(v\); leftover shorter than extra)

Prize odd ident-0s at \(k=1,2,4,8,16\) (packed \(3,8,29,400,87867\)).
Each \(k<v(n_0)\) with \(n_0=k\), hence \(2^k<E_{\mathrm{odd}}\).
Prize leftover \(R=2^{k+1}-p_k\) is \(0,3,112,43205\) at
\(k=2,4,8,16\) (Cycle DJ), all \(<E_{\mathrm{odd}}\). So neither the
actual leftover nor the worst-case \(2^k\) can hold a second odd at
those prize events.

## Lemma (if \(n_0\) persists to \(v\), a second odd can fit)

At \(k=v(n_0)\), \(2^k\ge E_{\mathrm{odd}}\). An odd at packed
\(2^k+1\) would leave leftover \(2^k-1\ge E-1\), so extra \(E\) lands
inside the same high half. In particular \(n_0=2\) at \(k=5\) has
\(32\ge 22\).

## Killed

Leftover is not automatically empty for every 2-power \(n_0\) at
every \(k\). Extra is a function of \(T_0\); annulus width \(2^k\)
grows. Cycle EC’s reduction to 2-power \(n_0\) does not by itself
give at-most-one-odd for all \(k\).

## Verdict

`LEMMA` (min odd extra for 2-power \(n_0\le 16\); threshold \(v\);
prize odds before \(v\); prize leftover and \(2^k\) below extra;
skip-to-\(v\) lets a second odd fit).
`KILLED` (leftover always empty for 2-power \(n_0\) at every \(k\)).
`PREFIX` (next odd forced before \(v\); \(v\) for every 2-power
\(n_0\); at-most-one-odd for all \(k\); period-\(H\) seed; \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ed.md` (this note)
- `research/cycle_ed.py`
- `research/cycle_ed.json`
