# Cycle TH: \(d=1\) origin is odd children; \(n\equiv 1\pmod{4}\) times are an 8-AP

At \(k\ge 1\), \(d=1\) pal-pairs on \(n\equiv 1\pmod{4}\) are the
odd children of every even covering \(n\) at \(k-1\) (count
\(2^k\)). \(d=1\) pal-pairs on \(n\equiv 3\pmod{4}\) are the odd
children of odd \(d=2\) pal-pairs at \(k-1\) (count \(J_k\)).
Covering times of \(n\equiv 1\pmod{4}\) are the arithmetic
progression \(2U+5,2U+13,\ldots,10U-3\) (difference \(8\)).
Pal-center AND on that AP is **not** identically \(0\). Do **not**
claim pal-center tot on \(n\equiv 1\pmod{4}\) identically \(0\).
Do **not** claim \(d=1\) spat on that residue identically \(0\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
leftover \(d\). Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_th.py --certify` (~0.16s).
Dump: `research/cycle_th.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST/SV/SX/SY/SZ/TA/TD/TE/TF/TG (\(d=1\)
origin is odd children; \(n\equiv 1\pmod{4}\) times are an 8-AP; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (\(d=1\) on \(n\equiv 1\pmod{4}\) is odd children of even covering)

Even parent \(m\) has \(G(m,m-1)=0\), so odd child \(n=2m+1\) has
\(G(n,n-1)=1\) and \(n\equiv 1\pmod{4}\). There are \(2^k\) even
covering clocks at \(k-1\), matching Cycle TF's \(d=1\) count on
this residue. Covering time is Cycle SZ's odd-child 2-fold. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 12\).

## Lemma (\(d=1\) on \(n\equiv 3\pmod{4}\) is odd children of odd \(d=2\))

Odd parent \(d=2\) has \(G(m,m-1)=0\) on the pal-adjacent bit, so
odd child \(n=2m+1\) is \(d=1\) and \(n\equiv 3\pmod{4}\). Count
\(J_k\) matches parent odd \(d=2\) count \(J_{(k-1)+1}\). Together
with Cycle TG, the \(\{d=1,d=2\}\) complex is closed under 2-fold.
Status: **lemma**. Census through \(k\le 12\).

## Lemma (covering times of \(n\equiv 1\pmod{4}\) are an 8-AP)

\(t=10U-2n-1\) with \(n=4\ell+1\), \(\ell=0,\ldots,U-1\) is
\(t=2U+5+8j\) running through \(2U+5,\ldots,10U-3\). For
\(k\ge 2\) these times are \(\equiv 5\pmod{8}\). Pal-center AND
\(c_t\land x(t,1)\) on this AP is not identically \(0\). Status:
**lemma**. Algebra through \(k\le 64\); times through \(k\le 12\);
pal-center tot through \(k\le 8\). **Killed:** pal-center tot on
this AP identically \(0\). **Killed:** \(d=1\) spat on
\(n\equiv 1\pmod{4}\) identically \(0\).

## Verdict

`LEMMA` (\(d=1\) on \(n\equiv 1\pmod{4}\) is odd children of even
covering; \(d=1\) on \(n\equiv 3\pmod{4}\) is odd children of odd
\(d=2\); covering times of \(n\equiv 1\pmod{4}\) are an 8-AP).
`CERTIFIED` (origin census through \(k\le 12\); AP through
\(k\le 12\); pal-center tot through \(k\le 8\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot on \(n\equiv 1\pmod{4}\) identically \(0\);
\(d=1\) spat on that residue identically \(0\); cellwise spat
2-fold; \(d=1\) on all odd \(n\); pal-center tot equals
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

- `research/cycle_th.md` (this note)
- `research/cycle_th.py`
- `research/cycle_th.json`
