# Cycle TB: odd-\(j\) pal-pairs drop clip-edge; edge count is Jacobsthal

Odd-\(j\) pal-pairs at \(k\) are the 2-fold of parent pal-pairs with
pal-partner \(\le 5U-1\). Parent clip-edge pal-pairs (partner
\(=5U\)) map to unpaired at the child. Clip-edge count is
Jacobsthal \(J_{k+2}\): even-\(n\) edge 2-folds all parent edge, and
each of \(n\equiv 1,3\pmod{4}\) folds onto edge at \(k-2\), so
\(E(k)=E(k-1)+2E(k-2)\). Odd-\(j\) distance doubles and the covering
time is Cycle SZ's odd-child 2-fold. Do **not** claim odd pal-pairs
2-fold all parent pal-pairs (clip-edge is dropped). Do **not** claim
even pal-pair raw tot equals parent pal-pair raw tot. Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
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

Certify: `python3 research/cycle_tb.py --certify` (~0.27s).
Dump: `research/cycle_tb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/SZ/TA (odd-\(j\) pal-pairs drop
clip-edge; edge count is Jacobsthal; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(j\) pal-pairs drop the clip-edge)

At odd child \(n=2m+1\), odd \(j=2r+1\), \(G(n,j)=G(m,r)\). Pal-pair
clip is \(2n-j\le 5U'\), i.e. \(2m-r\le 5U-1\). Parent pal-pairs
with partner \(=5U\) have child partner \(5U'+1\), hence unpaired.
Odd-\(j\) distance is \(d=2(m-r)\) and covering time is
\(t_k(2m+1)=2t_{k-1}(m)-1\). Status: **lemma**. Kind counts through
\(k\le 8\); algebra through \(k\le 64\). **Killed:** odd pal-pairs
2-fold all parent pal-pairs.

## Lemma (clip-edge pal-pair count is Jacobsthal \(J_{k+2}\))

Clip-edge means pal-partner \(=5U\), equivalently \(G(n,5U)=1\) on
\(n\in(5U/2,4U)\). Even \(n=2m\) 2-folds all parent clip-edge, so
\(E_{\mathrm{even}}(k)=E(k-1)\). For \(k\ge 2\),
\(G(4\ell+1,5\cdot 2^k)=G(4\ell+3,5\cdot 2^k)=G(\ell,5\cdot 2^{k-2})\),
and both residue classes run over clip-edge at \(k-2\), so
\(E_{\mathrm{odd}}(k)=2E(k-2)\). Thus
\(E(k)=E(k-1)+2E(k-2)\) with \(E(0)=1\), \(E(1)=3\), hence
\(E(k)=J_{k+2}=(2^{k+2}-(-1)^k)/3\). Status: **lemma**. Count
through \(k\le 12\); \(G\)-fold samples through \(k\le 64\).

## Verdict

`LEMMA` (odd-\(j\) pal-pairs drop clip-edge; odd-\(j\) distance
doubles; clip-edge count is Jacobsthal \(J_{k+2}\)).
`CERTIFIED` (odd-\(j\) fold through \(k\le 8\); edge census through
\(k\le 12\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd pal-pairs 2-fold all parent pal-pairs; even pal-pair
raw tot equals parent pal-pair raw tot; pal-center even tot period
\(8\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tb.md` (this note)
- `research/cycle_tb.py`
- `research/cycle_tb.json`
