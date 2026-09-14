# Cycle RL: leftover Green odd-\(n\) tot is 1 iff \(k\notin\{1,3\}\)

Cycle QW Green odd-\(n\) rest is 1 iff \(k\in\{0,2\}\). Cycle RK
unique Green odd-\(n\) tot equals UNIQUE_ODD tot, 1 iff \(k\ge 4\)
(Cycle QJ). Their xor is leftover Green odd-\(n\) tot, 1 iff
\(k\notin\{1,3\}\). Equivalently Cycle QH leftover tot xor leftover
even-\(n\) (Cycle QK even-\(j\) even-\(n\), since
\(G(\mathrm{even},\mathrm{odd})=0\)). This is **not** leftover
Green odd-\(n\) equals packed leftover odd-\(n\) (\(k=6\): Green
\(1\), packed \(0\)). **Not** leftover Green odd-\(n\) equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
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

Certify: `python3 research/cycle_rl.py --certify` (~0.49s).
Dump: `research/cycle_rl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/MD/PB/QH/QJ/QK/QW/RB/RK (leftover Green odd-\(n\) tot
\(1\) iff \(k\notin\{1,3\}\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover Green odd-\(n\) tot is 1 iff \(k\notin\{1,3\}\))

Green odd rest xor unique odd Green. Leftover even-\(n\) is
\(1\) iff \(k\in\{0,2,4,5\}\). Status: **lemma**. **Killed:**
leftover Green odd-\(n\) equals packed leftover odd-\(n\).
**Killed:** leftover Green odd-\(n\) equals \(S\oplus T\).

## Verdict

`LEMMA` (leftover Green odd-\(n\) tot is 1 iff \(k\notin\{1,3\}\);
leftover Green even-\(n\) tot is 1 iff \(k\in\{0,2,4,5\}\); QW/QJ/RK
xor; QH leftover tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover Green odd-\(n\) equals packed leftover odd-\(n\);
leftover Green odd-\(n\) equals \(S\oplus T\); cellwise 2-fold packed
AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rl.md` (this note)
- `research/cycle_rl.py`
- `research/cycle_rl.json`
