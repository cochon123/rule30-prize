# Cycle SB: odd-child \(G=1\) odd-\(j\) green4 is \((g_1\oplus 1,g_1,1,g_{-1})\)

Cycle RZ odd-child green4 at odd \(j=2r+1\) is
\((G(m,r+1)\oplus G(m,r),G(m,r+1),G(m,r),G(m,r-1))\). On \(G=1\),
\(G(m,r)=1\), so the 4-tuple equals \((g_1\oplus 1,g_1,1,g_{-1})\)
with \(g_1=G(m,r+1)\) and \(g_{-1}=G(m,r-1)\): one of
\((1,0,1,0)\), \((1,0,1,1)\), \((0,1,1,0)\), \((0,1,1,1)\). None is
in AND_ONES. Palindrome swaps \((g_1,g_{-1})\), so unclipped
counts of \((1,0,1,1)\) and \((0,1,1,0)\) are equal. Clipped
counts are **not** equal (\(k=2\) is \(8\) vs \(9\)). Cycle SA
even-\(j\) form is **not** this 4-tuple. Packed AND at
consecutive-\(p\) can still fire (Cycle QV mismatch). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sb.py --certify`.
Dump: `research/cycle_sb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RZ/SA (odd-child \(G=1\) odd-\(j\)
green4 is \((g_1\oplus 1,g_1,1,g_{-1})\); palindrome swaps the
bits; never AND; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (odd-child \(G=1\) odd-\(j\) green4)

At \(n=2m+1\), odd \(j=2r+1\), \(G=1\),
\(\mathrm{green4}=(g_1\oplus 1,g_1,1,g_{-1})\). Palindrome swaps
\((g_1,g_{-1})\), so unclipped counts of \((1,0,1,1)\) and
\((0,1,1,0)\) are equal. Status: **lemma**. **Killed:** that
4-tuple is identically one of the four values. **Killed:**
\((1,0,1,0)\) count equals \((0,1,1,1)\) count. **Killed:**
clipped covering counts of \((1,0,1,1)\) and \((0,1,1,0)\) are
equal.

## Verdict

`LEMMA` (odd-child \(G=1\) odd-\(j\) green4 is
\((g_1\oplus 1,g_1,1,g_{-1})\); palindrome swaps the bits;
unclipped \((1,0,1,1)\) count equals \((0,1,1,0)\); never AND;
RZ/SA closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (identically one tuple; \((1,0,1,0)\) count equals
\((0,1,1,1)\); clipped covering split equal; cellwise 2-fold
packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sb.md` (this note)
- `research/cycle_sb.py`
- `research/cycle_sb.json`
