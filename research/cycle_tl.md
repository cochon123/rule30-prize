# Cycle TL: \(G(n,n-1)\) is \(v_2(n+1)\bmod 2\)

The pal-adjacent Green bit equals the 2-adic valuation of \(n+1\)
mod 2. Hence \(d=1\) pal-pairs are covering \(n\) with \(v_2(n+1)\)
odd, and \(d=2\) pal-pairs are covering \(n\) with
\(v_2(\lfloor n/2\rfloor+1)\) odd. The \(d=1\) set is the disjoint
union of arithmetic progressions \(2^a-1, 2^a-1+2^{a+1},\ldots\)
over odd \(a\). Do **not** claim \(G(n,n-1)=1\) iff
\(n\equiv 1\pmod{4}\) (\(n=7\)). Do **not** claim \(d=1\) iff
\(n\equiv 1\pmod{4}\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue leftover \(d\). Do **not**
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

Certify: `python3 research/cycle_tl.py --certify`.
Dump: `research/cycle_tl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SV/SY/TA/TB/TD/TE/TK (\(G(n,n-1)\) is
\(v_2(n+1)\bmod 2\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(n,n-1)=v_2(n+1)\bmod 2\))

Cycle TK's recurrence is the valuation recurrence: even \(n\) has
\(v_2(n+1)=0\); \(n\equiv 1\pmod{4}\) has \(v_2(n+1)=1\); and
\(n\equiv 3\pmod{4}\) has \(v_2(n+1)=v_2(\lfloor n/4\rfloor+1)+2\),
so the parity is \(v_2(\lfloor n/4\rfloor+1)\bmod 2\). Status:
**lemma**. Samples through \(k\le 64\); census through \(k\le 12\).
**Killed:** \(G(n,n-1)=1\) iff \(n\equiv 1\pmod{4}\) (\(n=7\) has
\(v_2(8)=3\)).

## Lemma (\(d=1\) iff \(v_2(n+1)\) odd; \(d=2\) iff \(v_2(\lfloor n/2\rfloor+1)\) odd)

Cycle TD: pal-adjacent iff \(G(n,n-1)=1\). Cycle TE:
\(G(n,n-2)=G(\lfloor n/2\rfloor,\lfloor n/2\rfloor-1)\). Status:
**lemma**. Samples through \(k\le 64\); census through \(k\le 12\).
**Killed:** \(d=1\) iff \(n\equiv 1\pmod{4}\).

## Lemma (\(d=1\) covering \(n\) is a union of APs over odd valuations)

\(\{n:v_2(n+1)=a\}=\{2^a-1+2^{a+1}\ell\}\). Restrict to covering
\(n<4U\) and sum over odd \(a\) with \(2^a-1<4U\). The count is
\(J_{k+2}\). Status: **lemma**. Algebraic counts through
\(k\le 64\); set equality through \(k\le 12\).

## Verdict

`LEMMA` (\(G(n,n-1)=v_2(n+1)\bmod 2\); \(d=1\) iff \(v_2(n+1)\) odd;
\(d=2\) iff \(v_2(\lfloor n/2\rfloor+1)\) odd; \(d=1\) covering \(n\)
is the odd-\(a\) AP union).
`CERTIFIED` (Green census through \(k\le 12\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(G(n,n-1)=1\) iff \(n\equiv 1\pmod{4}\); \(d=1\) iff
\(n\equiv 1\pmod{4}\); \(d=1\) on all \(n\equiv 7\pmod{8}\);
\(d=2\) on all \(n\equiv 6\pmod{8}\); pal-center tot equals
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

- `research/cycle_tl.md` (this note)
- `research/cycle_tl.py`
- `research/cycle_tl.json`
