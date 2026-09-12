# Cycle EV: \(\operatorname{reconstruct}(S,\operatorname{gap}(S))\) run-form; scar \(\operatorname{ham}(n_4,n_5)=n_0\)

Even-\(n_0\) O-type always has a `00` (a `11` in one half is a `00` in
the other; Cycle CH: never alternating). After each `00` the next 1 of
\(S\) has backward distance \(\ge 3\), so
\(\operatorname{reconstruct}(S,\operatorname{gap}(S))\) has \(U=1\)
there and free bit 0. Along the following 0-run, \(U\) is
\((\mathrm{free},\mathrm{free},1,1,\ldots)\); a next 1 at distance 1 or
2 takes that free bit. Those `00`-seeds determine the whole word, so
scar \(n_5=\operatorname{reconstruct}(n_3,\operatorname{gap}(n_3))\) is
this function of \(n_3=\operatorname{rot}^{n_0-1}(T)\). Cycle DX on
\(s=n_3\) gives \(\operatorname{ham}(n_4,n_5)=n_0\) in scar indexing.
For even \(n_0\), \(n_5\) is type N and is not \(0\), \(n_3\), or
\(n_4\). Kills: \(n_5=\operatorname{gap}(n_4)\);
\(\operatorname{ham}(n_4,n_5)\) not \(n_0\); no run-form for \(n_5\);
even \(n_0\) O-type can lack `00`. Do **not** claim 1-runs of \(n_5\)
always alternate. Do **not** claim \(n_6\) type N. Do **not** claim a
formula for extra 414990. Do **not** bump all \(n_0=16\) past 414990.
Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push
the \(n_0=2\) seed past \(k=21\).

Not a prize claim: a run-form for \(n_5\) does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ev.py --certify` (~0.1s). Dump:
`research/cycle_ev.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/CH/DV/DX/ER/EU (no new packed run, no
Fermat table, no ones/gap/inverse rerun, no \(n_0=16\) window).

## Lemma (O-type has `00` iff `11`; even \(n_0\) always both)

\(T_{t+n_0}=\neg T_t\), so a `11` at \(t\) is a `00` at \(t+n_0\).
Neither iff cyclically alternating, which is exactly two words when
\(n_0\) is odd and none when \(n_0\) is even (Cycle EC/DY). Exhaustive
\(1\le n_0\le 12\).

## Lemma (run-form of \(\operatorname{reconstruct}(S,\operatorname{gap}(S))\))

If \(S\) has a `00`, every 1 immediately after a 0-run of length
\(\ge 2\) has backward distance \(\ge 3\), hence \(U=1\) and free bit
\(\neg(G\lor U)=0\). After any 1 at \(p\), the following 0-run of \(S\)
has \(U_{p+1}=U_{p+2}=\mathrm{free}(p)\) and \(U_{p+k}=1\) for
\(k\ge 3\); a next 1 at distance 1 or 2 receives that free bit.
Propagating from the `00`-seeds fills the word and matches
\(\operatorname{reconstruct}\). Certified on every even-\(n_0\) O-type
\(2\le n_0\le 10\) and every length-\(2..8\) word with a `00`.

## Lemma (scar \(n_5\) is the run-form of \(n_3\);
\(\operatorname{ham}(n_4,n_5)=n_0\))

Cycle EU: \(n_3=\operatorname{rot}^{n_0-1}(T)\),
\(n_4=\operatorname{gap}(n_3)\),
\(n_5=\operatorname{reconstruct}(n_3,n_4)\). Cycle DX on the O-type
\(s=n_3\) is \(\operatorname{ham}(\operatorname{reconstruct}(1,s),\operatorname{reconstruct}(s,\operatorname{gap}(s)))=n_0\),
i.e. \(\operatorname{ham}(n_4,n_5)=n_0\) in scar indexing. For even
\(n_0\le 10\), \(n_5\) is type N and is not \(0\), \(n_3\), or \(n_4\).
Certified on \(T^*\|\neg T^*\) (Hamming 16, type N).

## Killed

\(n_5\) is not \(\operatorname{gap}(n_4)\). Even \(n_0\) O-type cannot
lack a `00`. Consecutive 1s of \(S\) need not have opposite \(U\)
(isolated-0 blocks can copy a free 0 onto two consecutive 1s).

## Verdict

`LEMMA` (`00` iff `11`; even \(n_0\) has `00`; run-form; scar \(n_5\)
is the run-form of \(n_3\); \(\operatorname{ham}(n_4,n_5)=n_0\); even
\(n_0\) \(n_5\) type N).
`KILLED` (\(n_5=\operatorname{gap}(n_4)\); even \(n_0\) can lack `00`;
1-runs of \(n_5\) always alternate).
`PREFIX` (formula for extra 414990; at-most-one-odd for all \(k\); seed
for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ev.md` (this note)
- `research/cycle_ev.py`
- `research/cycle_ev.json`
