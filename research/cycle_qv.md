# Cycle QV: covering clipped \(G=1\) on even \(n\) at \(k\) is the 2-fold of \(k-1\)

Green even doubling is \(G(2m,2r)=G(m,r)\) and \(G(2m,\mathrm{odd})=0\).
Covering even \(n=2m\) at child \(k\) (\(U'=2U\)) runs \(m\) through the
parent covering window \(n\in\{0,\ldots,4U-1\}\). Clip matches: parent
\(j\le 5U\) iff child \(2j\le 5U'\). Packed column doubles (child
\(p=2\cdot\) parent \(p\)) and the covering even snapshot time doubles
the parent odd covering time. Packed AND is **not** cellwise 2-fold
(\(k=3\): 31 of 110 parent \(G=1\) cells mismatch). Even-\(n\) rest xor
parent rest tot equals that mismatch tot, so even rest at \(k\) equals
parent odd rest iff the mismatch tot equals parent even rest; that is
Cycle QU's all-\(k\) lift, not a packed identity. This is **not** rest
\(=S\oplus T\) for all \(k\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim even-\(n\) rest equals parent rest tot. Do **not**
claim cellwise 2-fold packed AND. Do **not** claim even-\(n\) rest
xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\).

Certify: `python3 research/cycle_qv.py --certify` (~0.35s).
Dump: `research/cycle_qv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/GU/HG/QO/QU (Green 2-fold covering bijection through
\(k\le 8\); covering geometry for \(k\le 64\); cellwise 2-fold kill
at \(k=3\); prefix QU even-\(n\) rest tot vs parent odd-\(n\) rest tot
through \(k\le 10\); no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Certificate (covering clipped \(G=1\) 2-fold bijection)

Even doubling is the recursive definition of \(G\) on even first
argument. Covering range, clip, packed column, and even snapshot
time are algebraic 2-folds for every \(k\ge 1\). Clipped even-\(n\)
\(G=1\) cells at \(k\) match the image of clipped \(G=1\) at \(k-1\)
through \(k\le 8\), including the slice \(n\equiv 0\pmod{4}\) at \(k\)
equals all even-\(n\) \(G=1\) at \(k-1\). Status: **lemma**. **Killed:**
cellwise 2-fold packed AND.

## Verdict

`LEMMA` (covering clipped \(G=1\) on even \(n\) at \(k\) is the 2-fold
of clipped \(G=1\) at \(k-1\); covering even snapshot time and packed
column double).
`CERTIFIED` (bijection counts through \(k\le 8\); \(E_k=0\) on odd-\(s\)
rest for \(q=10\), \(k\le 10\); even-\(n\) rest xor at \(k\) equals
odd-\(n\) rest xor at \(k-1\) for \(1\le k\le 10\)).
`KILLED` (cellwise 2-fold packed AND; even-\(n\) rest equals
\(S\oplus T\) at \(k-1\); \(n\equiv 2\pmod{4}\) tot equals parent odd
tot).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qv.md` (this note)
- `research/cycle_qv.py`
- `research/cycle_qv.json`
