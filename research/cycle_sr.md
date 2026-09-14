# Cycle SR: even-\(n\) clip-unpaired \(G=1\) never packed-AND through \(k\le 10\)

Palindrome pairs of even-\(n\) clipped \(G=1\) cancel, and there are
\(2^{k+1}\) pal-centers (all clipped, each \(G=1\)), so even-\(n\)
clipped \(G=1\) xor equals the xor of clip-unpaired cells. Those
unpaired cells are pal-left \(j<2n-5U\) on even \(n>5U/2\); their
pal-partner has negative packed \(p\). Packed AND vanishes on them
through \(k\le 10\), so even-\(n\) rest tot is pal-center AND xor
pal-pair AND-mismatch. That localizes the even-\(n\) obstruction to
Green-only rest. Do **not** claim unpaired silence for all \(k\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sr.py --certify`.
Dump: `research/cycle_sr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/OJ/PB/QV/QW/SO/SQ (even-\(n\) clip-unpaired \(G=1\) never
packed-AND through \(k\le 10\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even-\(n\) clipped \(G=1\) xor is unpaired)

The covering window has \(2^{k+1}\) even \(n\), all pal-centers
\(j=n\) lie in the clip \(j\le 5U\), and \(G(n,n)=1\). Palindrome
pairs cancel, so even-\(n\) clipped \(G=1\) xor equals the unpaired
xor and is \(1\) iff \(k=1\). Status: **lemma**. Cellwise through
\(k\le 8\). **Killed:** unpaired empty. **Killed:** Green even rest
equals packed even rest.

## Lemma (packed AND vanishes on those unpaired cells through \(k\le 10\))

Covering packed AND (hence rest) is \(0\) on every even-\(n\)
clip-unpaired \(G=1\) cell through \(k\le 10\). Even-\(n\) rest tot
equals pal-center packed rest xor pal-pair AND-mismatch, matching
Cycle SO even tot. Status: **certified** \(k\le 10\), **prefix**
all \(k\). **Killed:** pal-center tot equals even rest. **Killed:**
pal-pair mismatch identically \(0\). **Killed:** odd-\(n\) unpaired
AND identically \(0\) (already \(k=3\)).

## Verdict

`LEMMA` (even-\(n\) clipped \(G=1\) xor is unpaired; pal-center
count \(2^{k+1}\); unpaired Green tot is \(1\) iff \(k=1\)).
`CERTIFIED` (unpaired packed AND vanishes through \(k\le 10\);
even rest equals pal-center xor pair-mismatch through \(k\le 10\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals even rest; pair-mismatch identically
\(0\); unpaired empty; odd-\(n\) unpaired AND identically \(0\);
Green even rest equals packed even rest; cellwise 2-fold packed AND).
`PREFIX` (unpaired silence for all \(k\); even-\(n\) rest xor at
\(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed rest
\(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sr.md` (this note)
- `research/cycle_sr.py`
- `research/cycle_sr.json`
