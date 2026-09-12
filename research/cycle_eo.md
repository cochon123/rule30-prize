# Cycle EO: \(n_0=16\) unfolds ident-0-free through \(k=20\); seed at \(k=21\)

Cycle EN: the 16 unfolds after the \(n_0=8\) odds are ident-0-free
through \(k=19\), so every \(n_0=2\) scar has the period-\(H\) seed at
\(k=20\). Scanning those same unfolds through extras covering \(k=20\)
(image lo to \(2^{21}\)) is still empty: no even, no odd, no wrap.
Cycle ED’s threshold \(v(16)=19\) is already past, and leftover at
\(k=19\) and \(k=20\) still hosts no ident-0. Hence at most one odd in
\(k=20\) (namely zero), and \(\pi_{21}=32\) divides \(2^{20}\). Kills:
next \(n_0=16\) ident-0 forced at \(v(16)=19\); leftover at \(k=20\)
hosts an ident-0 on these scars. Do **not** claim a closed form for
the \(u_{16}\) strings. Do **not** bump all \(n_0=16\) past \(2^{18}\).
Do **not** scan \(k=21\) as a substitute. Do **not** claim the seed
for all \(k\). Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: seed at \(k=21\) for \(n_0=2\) scars does not give
covering never-fail.

Helper: `python3 research/cycle_eo.py --certify`. Dump:
`research/cycle_eo.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles ED, EN (u16 from the EN dump, prize unfold
rechecked). Scalar `ident0_events` on the 16 unfolds through the
\(k=20\) window only.

## Lemma (unfolds ident-0-free through \(k=20\))

Max extras from each image lo to \(2^{21}\): 2009429 (87468), 1867958
(228939), 1914112 (182785), 1901107 (195790), 1825700 (271197). All
exceed \(2^{20}\). `ident0_events` on each EN \(u_{16}\) through that
window is empty. Prize \(u_{16}\) is rechecked as \(\operatorname{unfold}(a)\)
at extra 228939.

## Lemma (period-\(H\) seed at \(k=21\) for every \(n_0=2\) scar)

No odd in annulus 20, on top of Cycle EN’s counts through 19. The
post-\(k=8\) odds remain mutually exclusive, so \(\pi_{21}=32\) divides
\(2^{20}\). Cycle DU: at most one odd per annulus implies the seed.

## Killed

A second ident-0 is not forced at \(k=v(16)=19\): these 16 words pass
both \(k=19\) and \(k=20\) with no ident-0. Leftover at \(k=20\) does
not host an ident-0 on the \(n_0=2\) cascade.

## Verdict

`LEMMA` (16 unfolds ident-0-free through \(k=20\); window covered from
image lo; at most one odd in \(k=20\) on \(n_0=2\); period-\(H\) seed
at \(k=21\) for every \(n_0=2\) scar).
`KILLED` (next \(n_0=16\) ident-0 forced at \(v(16)\); leftover at
\(k=20\) hosts ident-0 on \(n_0=2\)).
`PREFIX` (closed form for the \(u_{16}\) strings; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eo.md` (this note)
- `research/cycle_eo.py`
- `research/cycle_eo.json`
