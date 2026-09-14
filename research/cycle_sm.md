# Cycle SM: odd-child even-\(j\) clip equals parent \(p=0\); Green rest n3e all \(k\)

For \(k\ge 1\) and \(n=2m+1\), Green doubling gives
\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\). The even-\(j\) clip
\(0\le 2r\le\min(2n,5U)\) therefore telescopes to
\(G(m,\min(2m+1,5\cdot 2^{k-1}))\), which is the parent packed
\(p=0\) bit \(G(m,5\cdot 2^{k-1})\) (and \(0\) off the parent live
window). Child \(n\bmod 4=3\) is odd \(m\), so even-\(j\) clip xor
equals parent odd \(p=0\); \(n\bmod 4=1\) equals parent even \(p=0\).
Cycle SL makes those \(1\) iff \(k=1\) / \(k\ge 2\). Cycle SK forced
on \(n\bmod 4=3\) even \(j\) is \(1\) iff \(k\ge 1\), hence Green
rest there is \(1\) iff \(k\neq 1\) for all \(k\); on \(n\bmod 4=1\)
even \(j\) it is \(1\) iff \(k\le 1\). Cycle QY n3 tot then gives
odd-\(j\) rest \(1\) iff \(k=1\). Packed \(n\bmod 4=3\) even-\(j\)
rest is **not** this bit. Do **not** claim clip equals rest (forced
remains). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
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

Certify: `python3 research/cycle_sm.py --certify` (~0.28s).
Dump: `research/cycle_sm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/OJ/QH/QI/QV/QX/QY/SI/SJ/SK/SL (odd-child even-\(j\) clip
equals parent \(p=0\); Green rest on \(n\bmod 4=3\) even \(j\) is
\(1\) iff \(k\neq 1\) for all \(k\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-child even-\(j\) clip is parent \(p=0\))

For \(k\ge 1\), even-\(j\) clipped \(G=1\) on \(n=2m+1\) equals
\(G(m,5\cdot 2^{k-1})\). Hence \(n\bmod 4=3\) even-\(j\) clip is
\(1\) iff \(k=1\), and Green rest on those cells is \(1\) iff
\(k\neq 1\), for all \(k\). Dual: \(n\bmod 4=1\) even-\(j\) rest
is \(1\) iff \(k\le 1\). Status: **lemma**. Cellwise on
\(1\le k\le 8\); \(k=0\) is four covering cells. **Killed:** clip
equals rest. **Killed:** Green n3 even-\(j\) rest identically \(1\).

## Verdict

`LEMMA` (odd-child even-\(j\) clip equals parent \(p=0\); Green
rest on \(n\bmod 4=3\) even \(j\) is \(1\) iff \(k\neq 1\); on
\(n\bmod 4=1\) even \(j\) is \(1\) iff \(k\le 1\); odd-\(j\) n3
rest is \(1\) iff \(k=1\); Cycles SL/SK/QY).
`CERTIFIED` (cellwise telescope through \(k\le 8\); fold tots
through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (clip equals rest on n3 even \(j\); n3 even-\(j\) rest
identically \(1\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor
at \(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sm.md` (this note)
- `research/cycle_sm.py`
- `research/cycle_sm.json`
