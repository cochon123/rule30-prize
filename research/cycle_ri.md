# Cycle RI: UNIQUE_REST 2-fold stays unique iff \(p\in\{16,30,38\}\)

Packed column doubling is \(p\mapsto 2p\). Cycle RG unique-even
chain is \(16\to 32\) (then \(32\to 64\) leftover). Cycle RH
UNIQUE_ODD stay is \(\{30,38\}\) image \(\{60,76\}\). Union:
UNIQUE_REST 2-fold stays in UNIQUE_REST iff \(p\in\{16,30,38\}\),
image \(\{32,60,76\}\) which is UNIQUE_EVEN. This is **not**
UNIQUE_REST 2-fold all staying unique (13 of 16 leave). **Not**
UNIQUE_EVEN 2-fold all staying unique (only \(p=16\)). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_ODD 2-fold all stay unique.
Do **not** claim \(p=2\) is unique-rest.

Certify: `python3 research/cycle_ri.py --certify` (~0.13s).
Dump: `research/cycle_ri.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/QJ/RG/RH (UNIQUE_REST 2-fold stay \(\{16,30,38\}\) image
\(\{32,60,76\}\); no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (UNIQUE_REST 2-fold stays unique iff \(p\in\{16,30,38\}\))

Stay set is Cycle RG \(\{16\}\) union Cycle RH \(\{30,38\}\). Image
\(\{32,60,76\}\) is UNIQUE_EVEN. Status: **lemma**. **Killed:**
UNIQUE_REST 2-fold all stay unique. **Killed:** UNIQUE_EVEN 2-fold
all stay unique.

## Verdict

`LEMMA` (UNIQUE_REST 2-fold stays unique iff \(p\in\{16,30,38\}\),
image \(\{32,60,76\}\); UNIQUE_EVEN stay is only \(p=16\); RH
UNIQUE_ODD stay; RG spine \(16\to 32\to 64\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_REST 2-fold all stay unique; UNIQUE_EVEN 2-fold all
stay unique; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ri.md` (this note)
- `research/cycle_ri.py`
- `research/cycle_ri.json`
