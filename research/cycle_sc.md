# Cycle SC: odd-child \(G=1\) even-\(j\) consecutive Green is \((g_1,g_1\oplus g,g,1)\)

Cycle HJ odd-child consecutive Green equals parent green4:
\(\mathrm{cons\_g4}(2m+1,2r)=\mathrm{green4}(m,r)\). On \(G=1\),
\(G(2m+1,2r)=1\) so the last bit is \(1\) and the 4-tuple equals
\((g_1,g_1\oplus g,g,1)\) with \(g=G(m,r)\) and \(g_1=G(m,r+1)\):
one of \((0,1,1,1)\), \((1,1,0,1)\), \((0,0,0,1)\), \((1,0,1,1)\).
None is in AND_ONES (last-bit-\(1\) members \(0011\) and \(1001\)
contradict \(g_1\oplus g\) vs \(g\)). Cycle RX even-child \(G=1\)
consecutive is \((0,x,0,1)\), **not** this 4-tuple. Cycle SA
even-\(j\) green4 is **not** this 4-tuple. Type counts are **not**
equal. Palindrome of consecutive 4-tuples is **not** reverse.
Packed AND at consecutive-\(p\) can still fire (Cycle QV
mismatch). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sc.py --certify` (~0.41s).
Dump: `research/cycle_sc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RX/SA/SB (odd-child \(G=1\) even-\(j\)
consecutive Green is \((g_1,g_1\oplus g,g,1)\); equals parent
green4; never AND; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (odd-child \(G=1\) even-\(j\) consecutive Green)

At \(n=2m+1\), even \(j=2r\), \(G=1\),
\(\mathrm{cons\_g4}=(g_1,g_1\oplus g,g,1)\) with \(g=G(m,r)\) and
\(g_1=G(m,r+1)\). This is Cycle HJ's parent green4 on \(G=1\).
Status: **lemma**. **Killed:** that 4-tuple is identically
\((0,1,1,1)\). **Killed:** it equals Cycle RX consecutive Green.
**Killed:** it equals Cycle SA even-\(j\) green4. **Killed:** the
four type counts are equal.

## Verdict

`LEMMA` (odd-child \(G=1\) even-\(j\) consecutive Green is
\((g_1,g_1\oplus g,g,1)\); equals parent green4; never AND;
RX/SA/SB closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (identically \((0,1,1,1)\); equals RX consecutive; equals
SA green4; type counts equal; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sc.md` (this note)
- `research/cycle_sc.py`
- `research/cycle_sc.json`
