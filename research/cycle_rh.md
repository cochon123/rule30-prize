# Cycle RH: UNIQUE_ODD 2-fold stays unique iff \(p\in\{30,38\}\)

Packed column doubling is \(p\mapsto 2p\). UNIQUE_ODD is
\(p\bmod 4=2\) in UNIQUE_REST. Those nine columns all 2-fold to even
packed \(p\) (\(p\bmod 4=0\)). The image meets UNIQUE_REST iff
\(p\in\{30,38\}\), landing on \(\{60,76\}\) which are UNIQUE_EVEN.
The other seven land off unique
(\(42\to 84\), \(54\to 108\), \(58\to 116\), \(86\to 172\),
\(98\to 196\), \(106\to 212\), \(114\to 228\)). This is **not**
UNIQUE_ODD 2-fold all staying unique. **Not** the image is
UNIQUE_ODD (it is even-\(p\)). **Not** packed AND xor at \(p=30\) at
\(k-1\) equals \(p=60\) at \(k\) (\(k=4\): \(0\) vs \(1\)). This is
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
for all \(k\). Do **not** claim UNIQUE_EVEN 2-fold all stay unique
(\(32\to 64\) leftover). Do **not** claim \(p=2\) is unique-rest.

Certify: `python3 research/cycle_rh.py --certify`.
Dump: `research/cycle_rh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/QJ/PM/PN/PX/PZ/RG (UNIQUE_ODD 2-fold stay \(\{30,38\}\)
image \(\{60,76\}\); no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (UNIQUE_ODD 2-fold stays unique iff \(p\in\{30,38\}\))

UNIQUE_ODD 2-folds to even packed \(p\). Intersection with
UNIQUE_REST is the image of \(\{30,38\}\), namely UNIQUE_EVEN
\(\{60,76\}\). Status: **lemma**. **Killed:** UNIQUE_ODD 2-fold all
stay unique. **Killed:** the image is UNIQUE_ODD. **Killed:** packed
AND xor at \(p=30\) at \(k-1\) equals \(p=60\) at \(k\).

## Verdict

`LEMMA` (UNIQUE_ODD 2-fold stays unique iff \(p\in\{30,38\}\), image
\(\{60,76\}\); UNIQUE_ODD 2-fold is even-\(p\); RG spine
\(16\to 32\to 64\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_ODD 2-fold all stay unique; image is UNIQUE_ODD;
\(p=30\) xor at \(k-1\) equals \(p=60\) at \(k\); UNIQUE_EVEN 2-fold
all stay unique; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rh.md` (this note)
- `research/cycle_rh.py`
- `research/cycle_rh.json`
