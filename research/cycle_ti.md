# Cycle TI: covering times by \(n\bmod 4\) are four 8-APs partitioning odd \(t\)

On \(q=10\), \(t=10U-2n-1\). Covering \(n=4\ell+r\) has times the
AP \(2U+7-2r,\ldots,10U-2r-1\) with difference \(8\). The four
residue APs partition the odd integers in \([2U+1,10U-1]\). For
\(k\ge 2\) they sit in distinct classes \(t\equiv 7,5,3,1\pmod{8}\).
Pal-center tot is the xor of \(c_t\land x(t,1)\) on these four APs
and is **not** identically \(0\) on any residue. Do **not** claim
pal-center tot on a residue identically \(0\). Do **not** PREFIX
pal-center tot by residue from small \(k\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue leftover
\(d\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_ti.py --certify` (~0.14s).
Dump: `research/cycle_ti.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST/SV/SX/SY/TD/TF/TH (covering times by
\(n\bmod 4\) are four 8-APs; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering times of \(n\equiv r\pmod{4}\) are an 8-AP)

\(t=10U-2n-1\) with \(n=4\ell+r\), \(\ell=0,\ldots,U-1\) is
\(t=2U+7-2r+8j\) running through \(2U+7-2r,\ldots,10U-2r-1\).
Cycle TH is the \(r=1\) case. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 12\).

## Lemma (the four APs partition odd covering times)

The endpoints are \(2U+1,2U+3,2U+5,2U+7\) through
\(10U-7,10U-5,10U-3,10U-1\), so the union is every odd \(t\) in
\([2U+1,10U-1]\). That is the pal-center window of Cycle SZ.
Status: **lemma**. Algebra through \(k\le 64\); union through
\(k\le 12\).

## Lemma (for \(k\ge 2\), \(t\bmod 8\) is determined by \(n\bmod 4\))

For \(k\ge 2\), \(10U\equiv 0\pmod{8}\), so
\(t\equiv -2n-1\pmod{8}\). Residues \(n\equiv 0,1,2,3\pmod{4}\)
give \(t\equiv 7,5,3,1\pmod{8}\). Pal-center AND
\(c_t\land x(t,1)\) is not identically \(0\) on any of the four
APs. Status: **lemma**. Algebra through \(k\le 64\); pal-center tot
through \(k\le 8\). **Killed:** pal-center tot on a residue
identically \(0\).

## Verdict

`LEMMA` (covering times of \(n\equiv r\pmod{4}\) are an 8-AP; the
four APs partition odd covering times; for \(k\ge 2\),
\(t\bmod 8\) is determined by \(n\bmod 4\)).
`CERTIFIED` (census through \(k\le 12\); pal-center tot through
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot on a residue identically \(0\); pal-center
tot on \(n\equiv 1\pmod{4}\) identically \(0\); \(d=1\) spat on
that residue identically \(0\); pal-center tot equals
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

- `research/cycle_ti.md` (this note)
- `research/cycle_ti.py`
- `research/cycle_ti.json`
