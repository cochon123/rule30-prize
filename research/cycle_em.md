# Cycle EM: every \(n_0=2\) scar has at most one odd in \(k=18\); seed at \(k=19\)

Cycle EL: \(n_0=2\) scars have at most one odd in \(k=17\) and the
period-\(H\) seed at \(k=18\). The last \(n_0=8\) holdout
`00001101` (72177 group, no odd in 261633) first-odds at extra
271197, which lands in \(k=18\). Leftover after that image is
\(524288-271708=252580<E_{16}\), so no second ident-0 in \(k=18\)
leftover. The nine words that already odd-doubled at \(k=16\) or
\(k=17\) are \(n_0=16\); Cycle DR has no ident-0 in 262144 extras,
and extra 262145 from \(k=16\) or \(k=17\) lands in \(k=18\), with a
second such extra past \(k=18\). Hence at most one odd in \(k=18\) on
every \(n_0=2\) scar, and \(\pi_{19}\in\{32,64\}\) divides
\(2^{18}\). Kills: `00001101` never odd-doubles; every \(n_0=2\)
scar skips \(k=18\). Do **not** claim a closed form for 271197. Do
**not** bump the \(n_0=8\) scan past 523777 or \(n_0=16\) extras past
\(2^{18}\). Do **not** claim the seed for all \(k\). Do **not** claim
an 11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: seed at \(k=19\) for \(n_0=2\) scars does not give
covering never-fail.

Helper: `python3 research/cycle_em.py --certify`. Dump:
`research/cycle_em.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DR, DU, EH, EL. Scalar `first_odd_continue` /
`ident0_events` on `00001101` only (no full \(n_0=8\) rescan, no new
packed run, no Fermat table, no \(n_0=16\) window bump).

## Lemma (271197 lands in \(k=18\); leftover shorter than \(E_{16}\))

Image of extra 271197 from \(k=8\) is
\((271453,271708]\subset(2^{18},2^{19}]\). Leftover after the right
endpoint is 252580. Cycle DR: \(E_{16}=262145>252580\). The image
stays in \(k=18\) for extra \(\le 523777\).

## Lemma (`00001101` first-odds at 271197)

`first_odd_continue` and `ident0_events` on `00001101` through 523777
extras: even ident-0s at 52809, 72177, then 165350, 174051, 179001
(all in \(k=17\)), then odd 271197. No wrap. Do **not** claim a
closed form for those even extras.

## Lemma (\(E_{16}\) from \(k=16\) or \(k=17\) lands in \(k=18\))

Image of extra 262145 from \(k=16\) is
\((327681,393216]\subset(2^{18},2^{19}]\). From \(k=17\) it is
\((393217,524288]\), still \(k=18\). A second extra 262145 from
either left endpoint packs past \(2^{19}\), so an \(n_0=16\) scar
that odd-doubled at \(k=16\) or \(k=17\) has at most one ident-0 in
\(k=18\). Cycle DR: no ident-0 in the first 262144 extras.

## Lemma (period-\(H\) seed at \(k=19\) for every \(n_0=2\) scar)

At most one odd in annulus 18, on top of Cycle EL’s counts through
17. A \(k=16\) odd skips \(k=17\), so \(\pi_{19}\in\{32,64\}\), both
dividing \(2^{18}\). Cycle
DU: at most one odd per annulus implies the seed.

## Killed

`00001101` odd-doubles at scar extra 271197 in \(k=18\). Not every
\(n_0=2\) scar skips \(k=18\).

## Verdict

`LEMMA` (271197 from \(k=8\) lands in \(k=18\); leftover \(<E_{16}\);
523777 covers the window; holdout odd at 271197; \(E_{16}\) from
\(k=16\) or \(k=17\) lands in \(k=18\); at most one odd in \(k=18\)
on \(n_0=2\); period-\(H\) seed at \(k=19\) for every \(n_0=2\) scar).
`KILLED` (`00001101` never odd; every \(n_0=2\) scar skips \(k=18\)).
`PREFIX` (closed form for 271197; leftover after 271197 empty at
later \(k\); at-most-one-odd for all \(k\); seed for all \(k\);
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_em.md` (this note)
- `research/cycle_em.py`
- `research/cycle_em.json`
