# Cycle TD: pal-adjacent \(d=1\) pal-pairs are odd \(n\) with Jacobsthal count

Pal-adjacent pairs have \(d=1\), so \(j=n-1\) and partner \(n+1\).
Even covering \(n\) never has a \(d=1\) pal-pair (\(G(\mathrm{even},\mathrm{odd})=0\)).
Odd \(n=2m+1\) is a pal-pair iff \(G(m,m-1)=0\). Partner
\(n+1\le 4U<5U\), so the pair is always clipped. Count
\(A(k)=\#\{m\in[0,2^{k+1}):G(m,m-1)=0\}\) equals Jacobsthal
\(J_{k+2}\): even \(m\) all contribute and odd \(m=2l+1\) contribute
iff \(G(l,l-1)=1\), hence \(A(k)=2^{k+1}-A(k-1)\) with \(A(0)=1\).
Same integer as clip-edge count, disjoint cells (\(j=n-1\) vs
\(j=2n-5U\)). Spat mismatch is **not** identically \(0\). Do **not**
claim \(d=1\) AND identically \(0\). Do **not** claim \(d=1\) cells
equal clip-edge cells. Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue leftover \(d\). Do **not** catalogue
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

Certify: `python3 research/cycle_td.py --certify` (~0.15s).
Dump: `research/cycle_td.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/SU/SV/SX/SY/TA/TB/TC (pal-adjacent
\(d=1\) pal-pairs are odd \(n\) with Jacobsthal count; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (even covering \(n\) has no \(d=1\) pal-pair)

Distance \(d=1\) is odd, so \(j=n-1\) is odd when \(n\) is even.
\(G(\mathrm{even},\mathrm{odd})=0\), hence no even covering \(n\)
is a pal-adjacent pal-pair. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 12\).

## Lemma (odd covering \(n=2m+1\) is pal-adjacent iff \(G(m,m-1)=0\))

\(G(2m+1,2m)=G(m,m)\oplus G(m,m-1)=1\oplus G(m,m-1)\). Pal-pair
iff that bit is \(1\), i.e. \(G(m,m-1)=0\). Partner \(n+1\le 4U<5U\),
so pal-kind is always pair. Status: **lemma**. \(G\)-fold samples
through \(k\le 64\); census through \(k\le 12\).

## Lemma (pal-adjacent count is Jacobsthal \(J_{k+2}\))

Let \(A(k)=\#\{m\in[0,2^{k+1}):G(m,m-1)=0\}\). Even \(m\) all
contribute (\(2^k\) of them). Odd \(m=2l+1\) contribute iff
\(G(l,l-1)=1\), i.e. \(2^k-A(k-1)\) of them. Hence
\(A(k)=2^{k+1}-A(k-1)\) with \(A(0)=1\). Jacobsthal satisfies
\(J_{n+1}=2^n-J_n\), so \(A(k)=J_{k+2}\). Same integer as clip-edge
count \(E(k)=J_{k+2}\), disjoint cells: \(j=n-1\) equals
\(2n-5U\) iff \(n=5U-1\), which is outside covering
\([0,4U)\). Status: **lemma**. Count through \(k\le 12\); recurrence
through \(k\le 64\). **Killed:** \(d=1\) cells equal clip-edge cells.
**Killed:** \(d=1\) AND identically \(0\) (spat mismatch fires at
\(k=3,6,7\)).

## Verdict

`LEMMA` (even covering \(n\) has no \(d=1\) pal-pair; odd
\(n=2m+1\) is pal-adjacent iff \(G(m,m-1)=0\); pal-adjacent count
is Jacobsthal \(J_{k+2}\); always a clipped pair; disjoint from
clip-edge).
`CERTIFIED` (Green census through \(k\le 12\); spat mismatch through
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=1\) AND identically \(0\); \(d=1\) cells equal
clip-edge cells; \(d=1\) spat tot equals pal-center tot;
pal-center even tot period \(8\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_td.md` (this note)
- `research/cycle_td.py`
- `research/cycle_td.json`
