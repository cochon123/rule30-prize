# Cycle RT: covering Green even tot xor parent Green rest tot is 1 iff \(k\in\{2,3\}\)

Cycle QV packed 2-fold AND-mismatch tot equals parent even rest iff
even rest equals parent odd rest (the QU lift). The Green analogue
is Green even tot xor parent Green rest tot. Cycle QW Green even tot
is 1 iff \(k\ne 1\) and Cycle QH Green rest tot is 1 iff \(k\ge 3\),
so that xor is 1 iff \(k\in\{2,3\}\). Dual of Cycle RS's Green QU
kill: mismatch tot equals parent Green even tot dies (parent even
tot is 1 iff \(k\ne 2\)). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rt.py --certify` (~0.13s).
Dump: `research/cycle_rt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QH/QW/QV/RS (Green even tot xor parent Green rest tot is 1
iff \(k\in\{2,3\}\); Green mismatch tot equals parent Green even tot
dies; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (Green even tot xor parent Green rest tot is 1 iff \(k\in\{2,3\}\))

Green analogue of Cycle QV's packed mismatch tot. Status: **lemma**.
**Killed:** Green mismatch tot equals parent Green even tot.
**Killed:** Green even tot equals parent Green odd tot.

## Verdict

`LEMMA` (Green even tot xor parent Green rest tot is 1 iff
\(k\in\{2,3\}\); QW/QH closed forms; Green QU-lift identity dies).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green mismatch tot equals parent Green even tot; Green
even tot equals parent Green odd tot; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rt.md` (this note)
- `research/cycle_rt.py`
- `research/cycle_rt.json`
