# Cycle UC: leftover extra plus unpaired extra is \(2^{k+1}(F_{k+2}-1)+(-1)^k\)

Odd-\(n\) even-\(j\) pal-left \(G=1\) cells partition into \(d=1\),
odd clip-edge, leftover extra, and unpaired extra. Pal-left covering
\(j<n<4U<5U\) is never clip-constrained. Even \(n\) never have
\(d=1\) (\(v_2(n+1)=0\)). Clip-edge even cells 2-fold the parent
(Cycle TA), so odd clip-edge is \(2J_k\). Consecutive Green
transitions satisfy \(\mathrm{trans}(m)=\mathrm{wt}(\lfloor m/2\rfloor)\),
and the odd-\(n\) even-\(j\) total is \(2^{k+1}F_{k+2}\). Hence the
two extras sum to \(2^{k+1}(F_{k+2}-1)+(-1)^k\). Do **not** PREFIX
leftover extra or unpaired extra separately. Do **not** catalogue
leftover \(d\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot.
Do **not** claim pal-center tot equals \(S\oplus T\). This is
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
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_uc.py --certify`.
Dump: `research/cycle_uc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TL/TW/TZ/UA/UB
(odd-\(n\) even-\(j\) Fibonacci tot; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(n\) even-\(j\) pal-left partition)

Pal-left covering cells have \(j<n<4U<5U\). Even \(n\) have
\(v_2(n+1)=0\), so every \(d=1\) pal-pair is odd-\(n\) even-\(j\).
Odd clip-edge count is total clip-edge minus even clip-edge
\(J_{k+1}\), hence \(2J_k\). The remainder is leftover extra plus
unpaired extra. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\).

## Lemma (\(\mathrm{trans}(m)=\mathrm{wt}(\lfloor m/2\rfloor)\); tot \(=2^{k+1}F_{k+2}\))

Even \(m=2p\) and odd \(m=2p+1\) both have consecutive Green xor
count \(\mathrm{wt}(p)\). The covering window is \(m<2^{k+1}\), so
the odd-\(n\) even-\(j\) total is \(2W(2^k)\) with
\(W(2^k)=2^k F_{k+2}\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed:** tot
\(=2^{k+2}\). **Killed:** leftover extra plus unpaired extra empty.

## Lemma (extra leftover plus extra unpaired \(=2^{k+1}(F_{k+2}-1)+(-1)^k\))

Subtract \(J_{k+2}\) and \(2J_k\) from the Fibonacci tot.
\(J_{k+2}+2J_k=2^{k+1}-(-1)^k\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). Do **not** PREFIX leftover
extra or unpaired extra separately.

## Verdict

`LEMMA` (odd-\(n\) even-\(j\) pal-left partition; tot
\(=2^{k+1}F_{k+2}\); extra sum \(=2^{k+1}(F_{k+2}-1)+(-1)^k\);
odd clip-edge \(=2J_k\); \(\mathrm{trans}(m)=\mathrm{wt}(\lfloor m/2\rfloor)\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (tot \(=2^{k+2}\); extra sum empty; \(d=1\) on even \(n\);
unpaired extra empty; pair+\(g_0\) in unpaired extra; pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uc.md` (this note)
- `research/cycle_uc.py`
- `research/cycle_uc.json`
