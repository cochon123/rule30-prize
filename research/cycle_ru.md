# Cycle RU: covering Green \(n\bmod 4=1\) tot equals parent Green even tot

Cycle QX Green \(n\bmod 4=1\) tot is 1 iff \(k=1\) or \(k\ge 3\).
Cycle QW Green even tot is 1 iff \(k\ne 1\), so parent even tot at
\(k-1\) is 1 iff \(k\ne 2\). Those bits agree for every \(k\ge 1\).
Dual: Green \(n\bmod 4=3\) tot xor parent Green odd tot is 1 iff
\(k=2\) or \(k\ge 4\) (Cycle QY n3 tot is 1; parent odd tot is 1
iff \(k\in\{1,3\}\)). Green odd tot xor parent Green even tot is
1 for every \(k\ge 1\), so the odd-\(n\) Green analogue of Cycle
QU dies. Packed n1 tot equals parent even tot dies at \(k=1\)
(Cycle QO). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_ru.py --certify`.
Dump: `research/cycle_ru.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QW/QX/QY/QO/RS/RT (Green n1 tot equals parent Green even
tot; Green n3 tot xor parent Green odd tot is 1 iff \(k=2\) or
\(k\ge 4\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (Green n1 tot equals parent Green even tot)

Green n3 tot xor parent Green odd tot is 1 iff \(k=2\) or \(k\ge 4\).
Green odd tot xor parent Green even tot is 1 for every \(k\ge 1\).
Status: **lemma**. **Killed:** Green n3 tot equals parent Green
odd tot. **Killed:** Green odd tot equals parent Green even tot.
**Killed:** packed n1 tot equals parent even tot.

## Verdict

`LEMMA` (Green \(n\bmod 4=1\) tot equals parent Green even tot;
Green \(n\bmod 4=3\) tot xor parent Green odd tot is 1 iff \(k=2\)
or \(k\ge 4\); Green odd tot xor parent Green even tot is 1 for
every \(k\ge 1\); QX/QY/QW closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green n3 tot equals parent Green odd tot; Green odd tot
equals parent Green even tot; packed n1 tot equals parent even tot;
cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ru.md` (this note)
- `research/cycle_ru.py`
- `research/cycle_ru.json`
