# Cycle EN: \(n_0=16\) unfolds after \(n_0=2\) odds are ident-0-free through \(k=19\); seed at \(k=20\)

Cycle EM: every \(n_0=2\) scar has at most one odd in \(k=18\) and the
period-\(H\) seed at \(k=19\). After each \(n_0=8\) odd (87468 in
\(k=16\), 228939/182785/195790 in \(k=17\), 271197 in \(k=18\)),
\(\operatorname{unfold}(a)\) is an \(n_0=16\) \(T_0\). `ident0_events`
on those 16 unfolds through extras covering \(k=19\) (from each image
left endpoint to \(2^{20}\)) is empty: no even, no odd, no wrap. So
\(k=19\) has no odd on any \(n_0=2\) scar, and the nine earlier
\(n_0=16\) lifts have no odd in \(k=18\) either. The \(k=16/17/18\) odds are mutually exclusive, so
\(\pi_{20}=32\) divides \(2^{19}\). Kills:
those \(n_0=16\) \(T_0\)s odd-double in \(k=18\) or \(k=19\); leftover
after 271197 hosts an ident-0 before \(k=20\). Do **not** claim a
closed form for the \(u_{16}\) strings. Do **not** bump all \(n_0=16\)
past \(2^{18}\). Do **not** claim the seed for all \(k\). Do **not**
claim an 11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\). Do **not** push the \(n_0=2\) scan through \(k=20\) as a
substitute for a closed form.

Not a prize claim: seed at \(k=20\) for \(n_0=2\) scars does not give
covering never-fail. Prize scar \(u_{16}=0010111001111001\) is not
packed prize \(u_{16}=0000110011110011\).

Helper: `python3 research/cycle_en.py --certify`. Dump:
`research/cycle_en.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DK, DR, DU, EL, EM. Scalar `ident0_events` on
the 16 unfolds only (no exhaustive \(n_0=16\) window bump, no new packed
run, no Fermat table).

## Lemma (unfold after the \(n_0=8\) odd is ident-0-free through \(k=19\))

For each of the 16 even-52809 words, the predecessor \(a\) at the
recorded odd extra unfolds with \(u_0=0\) to a length-16 word. Scanning
that word through extras \(E\) with image-lo \(+E-1\le 2^{20}\) finds
no ident-0. Max extras: 960853 (87468), 819382 (228939), 865536
(182785), 852531 (195790), 777124 (271197), all \(>262144\).

## Lemma (prize scar \(u_{16}\) is not packed \(u_{16}\))

Prize \(T_0=00000110\) unfolds after extra 228939 to
`0010111001111001`, not Cycle DK’s packed prize
`0000110011110011`.

## Lemma (period-\(H\) seed at \(k=20\) for every \(n_0=2\) scar)

No odd in annulus 19, on top of Cycle EM’s counts through 18. The
three post-\(k=8\) odds sit in distinct annuli, so \(\pi_{20}=32\)
divides \(2^{19}\). Cycle DU: at most one odd per annulus implies the
seed.

## Killed

The \(n_0=16\) unfolds do not odd-double in \(k=18\) or \(k=19\).
Leftover after extra 271197 does not host an ident-0 before \(k=20\).

## Verdict

`LEMMA` (16 unfolds ident-0-free through \(k=19\); window covered from
image lo; prize scar \(u_{16}\ne\) packed \(u_{16}\); at most one odd
in \(k=19\) on \(n_0=2\); period-\(H\) seed at \(k=20\) for every
\(n_0=2\) scar).
`KILLED` (\(n_0=16\) odd in \(k=18\) or \(k=19\) after the \(n_0=8\)
odd; leftover after 271197 hosts ident-0 before \(k=20\)).
`PREFIX` (closed form for the \(u_{16}\) strings; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_en.md` (this note)
- `research/cycle_en.py`
- `research/cycle_en.json`
