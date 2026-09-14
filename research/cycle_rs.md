# Cycle RS: covering Green \(n\bmod 4=2\) tot xor parent Green odd tot is 1 iff \(k\ge 4\)

Cycle QX Green \(n\bmod 4=2\) tot is 1 iff \(k=1\) or \(k\ge 3\).
Cycle QW Green odd tot is 1 iff \(k\in\{0,2\}\), so parent odd tot
at \(k-1\) is 1 iff \(k\in\{1,3\}\). Their xor is 0 at \(k=1,2,3\)
and 1 for \(k\ge 4\). Dual: Green \(n\bmod 4=0\) tot xor parent
Green even tot is 1 iff \(k\ge 2\). This is **not** Green n2 tot
equals parent Green odd tot (fails \(k\ge 4\)). **Not** Green even
tot equals parent Green odd tot (the Green analogue of Cycle QU).
**Not** packed n2 mismatch equals this bit (Cycle RR is
\(\{2,4,8\}\) through \(k\le 10\)). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rs.py --certify`.
Dump: `research/cycle_rs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QW/QX/RR (Green n2 tot xor parent Green odd tot is 1 iff
\(k\ge 4\); Green n0 tot xor parent Green even tot is 1 iff
\(k\ge 2\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (Green n2 tot xor parent Green odd tot is 1 iff \(k\ge 4\))

Green n0 tot xor parent Green even tot is 1 iff \(k\ge 2\). Status:
**lemma**. **Killed:** Green n2 tot equals parent Green odd tot.
**Killed:** Green even tot equals parent Green odd tot. **Killed:**
packed n2 mismatch equals this bit.

## Verdict

`LEMMA` (Green \(n\bmod 4=2\) tot xor parent Green odd tot is 1 iff
\(k\ge 4\); Green \(n\bmod 4=0\) tot xor parent Green even tot is 1
iff \(k\ge 2\); QX/QW closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green n2 tot equals parent Green odd tot; Green even tot
equals parent Green odd tot; packed n2 mismatch equals this bit;
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

- `research/cycle_rs.md` (this note)
- `research/cycle_rs.py`
- `research/cycle_rs.json`
