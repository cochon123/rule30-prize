# Cycle EJ: every \(n_0=2\) scar has at most one odd in each annulus \(2..15\)

Every length-2 \(T_0\) lifts to FAM372 then even-52809 (Cycles EE/EF).
Placed at \(k=2\), extra 22 lands in \(k=4\) (odd), extra 372 in
\(k=8\) (odd), extra 52809 in \(k=15\) (even). Those images skip
\(k=3,5,6,7,9{-}14\). Cycle EI: 87468 cannot occupy the \(k=15\)
leftover. Through \(k=15\) the only odds are at \(k=2,4,8\), one each.
With the \(k=1\) odd, \(\pi_{16}=16\) divides \(2^{15}\): every
\(n_0=2\) scar has the period-\(H\) seed at \(k=16\). Do **not** claim
at-most-one-odd for all \(k\). Do **not** claim the seed for all \(k\).
Do **not** claim a \(k=16\) odd for every \(n_0=2\) scar. Do **not**
claim an 11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\).

Not a prize claim: seed at \(k=16\) for \(n_0=2\) scars does not give
covering never-fail.

Helper: `python3 research/cycle_ej.py --certify`. Dump:
`research/cycle_ej.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DU, EE, EF, EI (no new packed run, no Fermat
table, no \(n_0=16\) window bump).

## Lemma (landings skip non-powers through \(k=15\))

Extra 22 from \(k=2\) lands in \(k=4\); extra 372 from \(k=4\) in
\(k=8\); extra 52809 from \(k=8\) in \(k=15\). Extra 89 from \(k=4\)
would land in \(k=6\) but is unreachable from \(n_0=2\). The skipped
annuli are \(3,5,6,7,9,\ldots,14\).

## Lemma (at most one odd in each annulus \(2\le m\le 15\))

The \(n_0=2\) cascade has odd ident-0s only at \(k=2,4,8\) through
\(k=15\). The \(k=15\) event is even, and 87468 cannot fit in that
leftover (Cycle EI). First ident-0 after the \(k=8\) odd is extra
52809, so there is no ident-0 in \(k=9..14\).

## Lemma (period-\(H\) seed at \(k=16\) for every \(n_0=2\) scar)

Odd counts in annuli \(m=1..15\) are
\((1,1,0,1,0,0,0,1,0^7)\). Cycle DU: \(\pi_{16}=16\mid 2^{15}\).
At most one odd in each of those annuli is exactly this count on the
\(n_0=2\) path.

## Verdict

`LEMMA` (odds only at \(k=2,4,8\) through 15; skip empty annuli;
\(k=15\) even not odd; at most one odd in annuli \(2..15\) on
\(n_0=2\); period-\(H\) seed at \(k=16\) for every \(n_0=2\) scar;
FAM89 would land in \(k=6\)).
`PREFIX` (at-most-one-odd for all \(k\); seed for all \(k\); \(k=16\)
odd for every \(n_0=2\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ej.md` (this note)
- `research/cycle_ej.py`
- `research/cycle_ej.json`
